from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.time_index import frame_to_timestamp_ms

MAIN_SUBJECT_OBSERVATION_TYPE = "main_player_subject_candidate"
MAIN_SUBJECT_FILTER_METHOD = "main_tennis_subject_filter_v0"
MAIN_SUBJECT_WARNINGS = {
    "candidate_subject_only": True,
    "not_identity_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "raw_detections_not_mutated": True,
}


class MainSubjectFilterError(ValueError):
    pass


@dataclass(frozen=True)
class MainSubjectFilterConfig:
    min_area_ratio: float = 0.0015
    edge_exclusion_x: float = 0.04
    soft_edge_x: float = 0.12
    near_y_min: float = 0.45
    far_y_min: float = 0.15
    far_y_max: float = 0.58
    central_x_min: float = 0.20
    central_x_max: float = 0.80
    min_selection_score: float = 0.35

    def as_dict(self) -> dict[str, float]:
        return {
            "min_area_ratio": self.min_area_ratio,
            "edge_exclusion_x": self.edge_exclusion_x,
            "soft_edge_x": self.soft_edge_x,
            "near_y_min": self.near_y_min,
            "far_y_min": self.far_y_min,
            "far_y_max": self.far_y_max,
            "central_x_min": self.central_x_min,
            "central_x_max": self.central_x_max,
            "min_selection_score": self.min_selection_score,
        }


@dataclass(frozen=True)
class DetectionScore:
    observation: Observation
    bbox: dict[str, float]
    features: dict[str, float | str | bool]
    near_score: float
    far_score: float


def build_main_subject_filter_plan(
    *,
    media_id: str = "<media_id>",
    source_detection_run_id: str = "<source_detection_run_id>",
    run_name: str = "main-player-subject-filter-v0",
    every_n_frames: int = 1,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 214,
    viewer_base_url: str = "http://127.0.0.1:3000",
    config: MainSubjectFilterConfig | None = None,
) -> dict[str, Any]:
    resolved_config = config or MainSubjectFilterConfig()
    command_parts = [
        "python -m apps.worker.cli select-main-player-subjects",
        f"--media-id {media_id}",
        f"--source-detection-run-id {source_detection_run_id}",
        f"--run-name {run_name}",
        f"--every-n-frames {every_n_frames}",
    ]
    if frame_start is not None:
        command_parts.append(f"--frame-start {frame_start}")
    if frame_end is not None:
        command_parts.append(f"--frame-end {frame_end}")
    if max_frames is not None:
        command_parts.append(f"--max-frames {max_frames}")

    return {
        "steps": [
            "validate_media",
            "validate_source_detection_run",
            "query_player_detection_observations",
            "score_near_and_far_player_candidates",
            "persist_main_player_subject_candidate_observations",
            "write_source_detection_lineage",
        ],
        "command": " ".join(command_parts),
        "selection_method": MAIN_SUBJECT_FILTER_METHOD,
        "source_detection_run_id": source_detection_run_id,
        "run_name": run_name,
        "sampling": {
            "every_n_frames": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "frame_time_owner": "media_indexing",
        },
        "filter_config": resolved_config.as_dict(),
        "replay_url_template": (
            f"{viewer_base_url}/replay/{media_id}?"
            "detectionRunId=<source_detection_run_id>&subjectRunId=<main_subject_run_id>"
        ),
        "warnings": dict(MAIN_SUBJECT_WARNINGS),
    }


def select_main_player_subjects(
    *,
    session: Session,
    media_id: str,
    source_detection_run_id: str,
    run_name: str = "main-player-subject-filter-v0",
    every_n_frames: int = 1,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 214,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
    config: MainSubjectFilterConfig | None = None,
) -> dict[str, Any]:
    resolved_config = config or MainSubjectFilterConfig()
    plan = build_main_subject_filter_plan(
        media_id=media_id,
        source_detection_run_id=source_detection_run_id,
        run_name=run_name,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
        viewer_base_url=viewer_base_url,
        config=resolved_config,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "main tennis player subject filter planned",
            "plan": plan,
            "warnings": dict(MAIN_SUBJECT_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    source_run = session.get(ProcessingRun, source_detection_run_id)
    if source_run is None:
        return _failed(
            "missing_source_detection_run",
            f"source detection run not found: {source_detection_run_id}",
        )
    if source_run.media_id != media.id:
        return _failed(
            "source_detection_run_media_mismatch",
            "source detection run media_id does not match media_id.",
        )

    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            source_detection_run_id=source_detection_run_id,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
            config=resolved_config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            source_detection_run_id=source_detection_run_id,
            config=resolved_config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        source_rows = _source_player_detection_rows(
            session=session,
            media=media,
            source_detection_run_id=source_detection_run_id,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
        )
        selected = _select_candidates_by_frame(
            media=media,
            detections=source_rows,
            config=resolved_config,
        )
        observations = _persist_subject_candidates(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            selected=selected,
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session, run, step, str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    role_counts = Counter(
        str(observation.payload_jsonb.get("subject_role_candidate"))
        for observation in observations
    )
    selected_frames = sorted(
        {
            int(observation.frame_start)
            for observation in observations
            if observation.frame_start is not None
        }
    )
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_detection_count=len(source_rows),
        subject_candidate_count=len(observations),
        selected_frames=selected_frames,
        role_counts=role_counts,
    )
    replay_url = (
        f"{viewer_base_url}/replay/{media.id}?"
        f"detectionRunId={source_detection_run_id}&subjectRunId={run.id}"
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "main tennis player subject filter complete",
        "main_subject_run_id": run.id,
        "media_id": media.id,
        "source_detection_run_id": source_detection_run_id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            "near_player_candidate": role_counts.get("near_player_candidate", 0),
            "far_player_candidate": role_counts.get("far_player_candidate", 0),
            "total": len(observations),
        },
        "source_player_detections_considered": len(source_rows),
        "selected_frames": len(selected_frames),
        "sampled_frames": selected_frames,
        "replay_url": replay_url,
        "warnings": dict(MAIN_SUBJECT_WARNINGS),
    }


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "main-tennis-subject-filter",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "tracking",
            ModelRegistry.source == "apps.worker.services.main_subject_filter",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="main-tennis-subject-filter",
        version="v0",
        model_family="tracking",
        source="apps.worker.services.main_subject_filter",
        metadata_jsonb={
            "selection_method": MAIN_SUBJECT_FILTER_METHOD,
            "candidate_subject_only": True,
            "not_identity_truth": True,
            "observation_only": True,
            "no_adjudication": True,
            "raw_detections_not_mutated": True,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    source_detection_run_id: str,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    config: MainSubjectFilterConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="main-tennis-subject-filter-config",
        config_version="v0",
        payload_jsonb={
            "selection_method": MAIN_SUBJECT_FILTER_METHOD,
            "source_detection_run_id": source_detection_run_id,
            "every_n_frames": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "filter_config": config.as_dict(),
            "candidate_subject_only": True,
            "not_identity_truth": True,
            "observation_only": True,
            "no_adjudication": True,
            "raw_detections_not_mutated": True,
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _create_run(
    *,
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    source_detection_run_id: str,
    config: MainSubjectFilterConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "selection_method": MAIN_SUBJECT_FILTER_METHOD,
            "source_detection_run_id": source_detection_run_id,
            "filter_config": config.as_dict(),
            "candidate_subject_only": True,
            "not_identity_truth": True,
            "observation_only": True,
            "no_adjudication": True,
            "raw_detections_not_mutated": True,
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    *,
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="main_tennis_subject_filter_v0",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "selection_method": MAIN_SUBJECT_FILTER_METHOD,
            "candidate_subject_only": True,
            "not_identity_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _source_player_detection_rows(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
) -> list[Observation]:
    if every_n_frames <= 0:
        raise MainSubjectFilterError("every_n_frames must be greater than 0")
    resolved_start = 0 if frame_start is None else int(frame_start)
    resolved_end = None if frame_end is None else int(frame_end)
    if resolved_start < 0:
        raise MainSubjectFilterError("frame_start must be greater than or equal to 0")
    if resolved_end is not None and resolved_start > resolved_end:
        raise MainSubjectFilterError("frame_start must be less than or equal to frame_end")

    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == source_detection_run_id,
            Observation.observation_type == "player_detection",
            Observation.frame_start.is_not(None),
            Observation.timestamp_start_ms.is_not(None),
        )
        .order_by(Observation.frame_start, Observation.id)
    )
    query = query.where(Observation.frame_start >= resolved_start)
    if resolved_end is not None:
        query = query.where(Observation.frame_start <= resolved_end)
    rows = list(session.scalars(query).all())
    if every_n_frames > 1:
        rows = [
            row
            for row in rows
            if row.frame_start is not None
            and (int(row.frame_start) - resolved_start) % every_n_frames == 0
        ]
    if max_frames is None:
        return rows

    allowed_frames = set(
        sorted({int(row.frame_start) for row in rows})[: max(0, max_frames)]
    )
    return [
        row
        for row in rows
        if row.frame_start is not None and int(row.frame_start) in allowed_frames
    ]


def _select_candidates_by_frame(
    *,
    media: MediaAsset,
    detections: list[Observation],
    config: MainSubjectFilterConfig,
) -> list[tuple[str, DetectionScore]]:
    by_frame: dict[int, list[DetectionScore]] = defaultdict(list)
    for detection in detections:
        score = _score_detection(media=media, detection=detection, config=config)
        if score is not None:
            by_frame[int(detection.frame_start)].append(score)

    selected: list[tuple[str, DetectionScore]] = []
    for frame_number in sorted(by_frame):
        scores = by_frame[frame_number]
        near = _best_score(scores, role="near", config=config)
        far = _best_score(
            [
                score
                for score in scores
                if near is None or score.observation.id != near.observation.id
            ],
            role="far",
            config=config,
        )
        if near is not None:
            selected.append(("near_player_candidate", near))
        if far is not None:
            selected.append(("far_player_candidate", far))
    return selected


def _score_detection(
    *,
    media: MediaAsset,
    detection: Observation,
    config: MainSubjectFilterConfig,
) -> DetectionScore | None:
    payload = _merged_payload(detection)
    bbox = _bbox(payload)
    if bbox is None:
        return None

    width = float(media.width or payload.get("image_width") or 1)
    height = float(media.height or payload.get("image_height") or 1)
    image_area = max(1.0, width * height)
    cx = (bbox["x"] + bbox["width"] / 2.0) / max(1.0, width)
    cy = (bbox["y"] + bbox["height"] / 2.0) / max(1.0, height)
    area_ratio = (bbox["width"] * bbox["height"]) / image_area
    confidence = float(detection.confidence or payload.get("confidence") or 0.0)
    if area_ratio < config.min_area_ratio:
        return None
    if cx < config.edge_exclusion_x or cx > 1.0 - config.edge_exclusion_x:
        return None

    central_score = _window_score(cx, config.central_x_min, config.central_x_max)
    edge_penalty = max(0.0, (config.soft_edge_x - cx) / config.soft_edge_x)
    edge_penalty = max(
        edge_penalty,
        max(0.0, (cx - (1.0 - config.soft_edge_x)) / config.soft_edge_x),
    )
    area_score = min(1.0, area_ratio / 0.06)
    near_position_score = _window_score(cy, config.near_y_min, 0.95)
    far_position_score = _window_score(cy, config.far_y_min, config.far_y_max)
    near_score = _bounded(
        0.30 * confidence
        + 0.25 * area_score
        + 0.25 * near_position_score
        + 0.20 * central_score
        - 0.30 * edge_penalty
    )
    far_score = _bounded(
        0.25 * confidence
        + 0.20 * area_score
        + 0.35 * far_position_score
        + 0.20 * central_score
        - 0.30 * edge_penalty
    )
    features: dict[str, float | str | bool] = {
        "bbox_area": bbox["width"] * bbox["height"],
        "bbox_area_ratio": round(area_ratio, 6),
        "bbox_center_x": round(cx, 6),
        "bbox_center_y": round(cy, 6),
        "edge_penalty": round(edge_penalty, 6),
        "central_score": round(central_score, 6),
        "area_score": round(area_score, 6),
        "bottom_half_score": round(near_position_score, 6),
        "top_half_score": round(far_position_score, 6),
        "court_region_hint": _court_region_hint(cx, cy),
        "candidate_subject_only": True,
    }
    return DetectionScore(
        observation=detection,
        bbox=bbox,
        features=features,
        near_score=near_score,
        far_score=far_score,
    )


def _best_score(
    scores: list[DetectionScore],
    *,
    role: str,
    config: MainSubjectFilterConfig,
) -> DetectionScore | None:
    field = "near_score" if role == "near" else "far_score"
    eligible = [
        score for score in scores if getattr(score, field) >= config.min_selection_score
    ]
    if not eligible:
        return None
    return max(
        eligible,
        key=lambda score: (getattr(score, field), score.observation.confidence or 0.0),
    )


def _persist_subject_candidates(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    selected: list[tuple[str, DetectionScore]],
) -> list[Any]:
    writer = ObservationWriter(session)
    observations = []
    for index, (role, score) in enumerate(selected):
        detection = score.observation
        frame_number = int(detection.frame_start)
        timestamp_ms = int(
            detection.timestamp_start_ms
            if detection.timestamp_start_ms is not None
            else frame_to_timestamp_ms(media.fps or 30.0, frame_number)
        )
        selection_score = score.near_score if role == "near_player_candidate" else score.far_score
        payload = {
            "subject_role_candidate": role,
            "source_detection_observation_id": detection.id,
            "source_detection_run_id": detection.run_id,
            "frame_number": frame_number,
            "timestamp_ms": timestamp_ms,
            "selection_method": MAIN_SUBJECT_FILTER_METHOD,
            "selection_score": selection_score,
            "selection_scores": {
                "near_player_candidate": score.near_score,
                "far_player_candidate": score.far_score,
            },
            "selection_features": score.features,
            "bbox": score.bbox,
            "candidate_subject_only": True,
            "not_identity_truth": True,
            "observation_only": True,
            "no_adjudication": True,
            "raw_detection_not_mutated": True,
        }
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family="tracking",
                    observation_type=MAIN_SUBJECT_OBSERVATION_TYPE,
                    granularity="frame",
                    frame_start=frame_number,
                    frame_end=frame_number,
                    timestamp_start_ms=timestamp_ms,
                    timestamp_end_ms=timestamp_ms,
                    confidence=selection_score,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space="image_pixels",
                    payload_jsonb=payload,
                    idempotency_key=(
                        f"{run.id}:main-subject:{frame_number}:{role}:{detection.id}:{index}"
                    ),
                    lineage=[
                        ObservationLineageCreate(
                            parent_observation_id=detection.id,
                            relationship_type="main_subject_candidate_from_player_detection",
                            processing_step_id=step.id,
                            payload_jsonb={
                                "selection_method": MAIN_SUBJECT_FILTER_METHOD,
                                "subject_role_candidate": role,
                                "selection_score": selection_score,
                                "candidate_subject_only": True,
                                "not_identity_truth": True,
                                "observation_only": True,
                                "no_adjudication": True,
                            },
                        )
                    ],
                )
            )
        )
    return observations


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_detection_count: int,
    subject_candidate_count: int,
    selected_frames: list[int],
    role_counts: Counter[str],
) -> None:
    now = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "source_player_detection_count": source_detection_count,
        "main_subject_candidate_count": subject_candidate_count,
        "selected_frames": selected_frames,
        "counts_by_role": dict(role_counts),
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "source_player_detection_count": source_detection_count,
        "main_subject_candidate_count": subject_candidate_count,
        "selected_frames": selected_frames,
        "counts_by_role": dict(role_counts),
    }
    session.commit()


def _mark_failed(
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    error_message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {**run.metadata_jsonb, "error": error_message}
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {**step.metadata_jsonb, "error": error_message}
    session.commit()


def _merged_payload(observation: Observation) -> dict[str, Any]:
    atomic_payload = (
        observation.atomic_detail.payload_jsonb
        if observation.atomic_detail is not None
        else {}
    )
    return {**observation.payload_jsonb, **atomic_payload}


def _bbox(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if not isinstance(value, dict):
        return None
    x = _number(value.get("x"))
    y = _number(value.get("y"))
    width = _number(value.get("width", value.get("w")))
    height = _number(value.get("height", value.get("h")))
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {"x": x, "y": y, "width": width, "height": height}


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _window_score(value: float, low: float, high: float) -> float:
    if low <= value <= high:
        return 1.0
    if value < low:
        return max(0.0, 1.0 - ((low - value) / 0.25))
    return max(0.0, 1.0 - ((value - high) / 0.25))


def _bounded(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 6)


def _court_region_hint(cx: float, cy: float) -> str:
    horizontal = "center"
    if cx < 0.25:
        horizontal = "left_edge"
    elif cx > 0.75:
        horizontal = "right_edge"
    vertical = "mid_court"
    if cy >= 0.55:
        vertical = "near_court"
    elif cy <= 0.35:
        vertical = "far_court_or_background"
    return f"{vertical}_{horizontal}"


def _failed(
    status: str,
    message: str,
    error_type: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(MAIN_SUBJECT_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
