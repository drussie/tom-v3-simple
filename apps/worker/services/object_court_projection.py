from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.court import COURT_TEMPLATE_NAME, COURT_TEMPLATE_VERSION
from tom_v3_schema.enums import (
    CoordinateSpace,
    ObservationFamily,
    ObservationGranularity,
    RelationshipType,
)
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    HomographyCandidateObservation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

BALL_COURT_PROJECTION_OBSERVATION_TYPE = "ball_court_projection_candidate"
MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE = "main_player_court_projection_candidate"
COURT_PROJECTION_OBSERVATION_TYPES = {
    BALL_COURT_PROJECTION_OBSERVATION_TYPE,
    MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE,
}
COURT_PROJECTION_METHOD = "object_to_court_projection_candidates_v0"
BALL_PROJECTION_METHOD = "homography_image_pixels_to_court_template_2d_v0"
PLAYER_PROJECTION_METHOD = "bbox_bottom_center_homography_projection_v0"
DEFAULT_HOMOGRAPHY_MAX_GAP_MS = 1500
COURT_PROJECTION_WARNINGS = {
    "projection_candidate_only": True,
    "not_ball_truth": True,
    "not_player_truth": True,
    "not_court_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_bounce_hit_in_out_score": True,
}


@dataclass(frozen=True)
class ObjectProjectionConfig:
    homography_max_gap_ms: int = DEFAULT_HOMOGRAPHY_MAX_GAP_MS

    def as_dict(self) -> dict[str, int]:
        return {"homography_max_gap_ms": self.homography_max_gap_ms}


@dataclass(frozen=True)
class SourceObjectCandidate:
    observation: Observation
    kind: str
    frame_number: int
    timestamp_ms: int
    image_point: dict[str, float]
    image_anchor: dict[str, Any]
    confidence: float | None
    track_candidate_id: str | None = None
    track_role_candidate: str | None = None


@dataclass(frozen=True)
class HomographyMatch:
    homography: HomographyCandidateObservation
    matrix: list[list[float]]
    policy: str
    time_delta_ms: int
    carried_forward: bool


def build_object_court_projection_plan(
    *,
    media_id: str = "<media_id>",
    motion_smoothing_run_id: str = "<motion_smoothing_run_id>",
    homography_run_id: str = "<homography_run_id>",
    run_name: str = "object-to-court-projection-candidates-v0",
    homography_max_gap_ms: int = DEFAULT_HOMOGRAPHY_MAX_GAP_MS,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    return {
        "steps": [
            "validate_media_and_source_runs",
            "load_smoothed_ball_position_candidates",
            "load_smoothed_main_player_box_candidates",
            "load_homography_candidates",
            "match_object_frames_to_candidate_homographies",
            "project_image_points_to_court_template_2d",
            "persist_ball_and_main_player_court_projection_candidates",
            "write_source_object_and_homography_lineage",
        ],
        "command": (
            "python -m apps.worker.cli project-objects-to-court "
            f"--media-id {media_id} "
            f"--motion-smoothing-run-id {motion_smoothing_run_id} "
            f"--homography-run-id {homography_run_id} "
            f"--run-name {run_name} "
            f"--homography-max-gap-ms {homography_max_gap_ms}"
        ),
        "run_name": run_name,
        "source_run_ids": {
            "motion_smoothing_run_id": motion_smoothing_run_id,
            "homography_run_id": homography_run_id,
        },
        "target_coordinate_space": CoordinateSpace.court_template_2d,
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "homography_match_policy": "exact_frame_then_latest_prior_then_nearest_within_gap_v0",
        "homography_max_gap_ms": homography_max_gap_ms,
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
            f"?motionSmoothingRunId={motion_smoothing_run_id}"
            f"&homographyRunId={homography_run_id}"
            "&courtProjectionRunId=<court_projection_run_id>"
        ),
        "warnings": dict(COURT_PROJECTION_WARNINGS),
    }


def project_objects_to_court(
    *,
    session: Session,
    media_id: str,
    motion_smoothing_run_id: str,
    homography_run_id: str,
    run_name: str = "object-to-court-projection-candidates-v0",
    homography_max_gap_ms: int = DEFAULT_HOMOGRAPHY_MAX_GAP_MS,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    if homography_max_gap_ms < 0:
        return _failed(
            "invalid_homography_max_gap_ms",
            "homography_max_gap_ms must be greater than or equal to zero",
        )
    plan = build_object_court_projection_plan(
        media_id=media_id,
        motion_smoothing_run_id=motion_smoothing_run_id,
        homography_run_id=homography_run_id,
        run_name=run_name,
        homography_max_gap_ms=homography_max_gap_ms,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "object-to-court projection candidate build planned",
            "plan": plan,
            "warnings": dict(COURT_PROJECTION_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")
    for label, run_id in (
        ("motion_smoothing_run_id", motion_smoothing_run_id),
        ("homography_run_id", homography_run_id),
    ):
        run = session.get(ProcessingRun, run_id)
        if run is None:
            return _failed(f"missing_{label}", f"source run not found: {run_id}")
        if run.media_id != media.id:
            return _failed(f"{label}_media_mismatch", f"{label} does not match media_id")

    config = ObjectProjectionConfig(homography_max_gap_ms=homography_max_gap_ms)
    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            motion_smoothing_run_id=motion_smoothing_run_id,
            homography_run_id=homography_run_id,
            config=config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            motion_smoothing_run_id=motion_smoothing_run_id,
            homography_run_id=homography_run_id,
            config=config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        homographies = _load_homographies(
            session=session,
            media=media,
            homography_run_id=homography_run_id,
        )
        ball_sources = _load_smoothed_ball_sources(
            session=session,
            media=media,
            motion_smoothing_run_id=motion_smoothing_run_id,
        )
        player_sources = _load_smoothed_player_sources(
            session=session,
            media=media,
            motion_smoothing_run_id=motion_smoothing_run_id,
        )
        writer = ObservationWriter(session)
        projected = _persist_projection_candidates(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            motion_smoothing_run_id=motion_smoothing_run_id,
            homography_run_id=homography_run_id,
            homographies=homographies,
            sources=[*ball_sources, *player_sources],
            config=config,
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session=session, run=run, step=step, message=str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    counts = Counter(row.observation_type for row in projected["observations"])
    sampled_frames = sorted(
        {
            int(row.frame_start)
            for row in projected["observations"]
            if row.frame_start is not None
        }
    )
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_counts={
            "smoothed_ball_position_candidate": len(ball_sources),
            "smoothed_main_player_box_candidate": len(player_sources),
            "homography_candidate_observation": len(homographies),
        },
        output_counts=dict(counts),
        skipped=projected["skipped"],
        sampled_frames=sampled_frames,
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "object-to-court projection candidate build complete",
        "court_projection_run_id": run.id,
        "run_id": run.id,
        "media_id": media.id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "source_run_ids": {
            "motion_smoothing_run_id": motion_smoothing_run_id,
            "homography_run_id": homography_run_id,
        },
        "observations": {
            BALL_COURT_PROJECTION_OBSERVATION_TYPE: counts.get(
                BALL_COURT_PROJECTION_OBSERVATION_TYPE, 0
            ),
            MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE: counts.get(
                MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE, 0
            ),
            "total": sum(counts.values()),
        },
        "source_counts": {
            "smoothed_ball_position_candidate": len(ball_sources),
            "smoothed_main_player_box_candidate": len(player_sources),
            "homography_candidate_observation": len(homographies),
        },
        "skipped": projected["skipped"],
        "sampled_frames": sampled_frames,
        "observation_ids": [row.id for row in projected["observations"]],
        "replay_url": (
            f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
            f"?motionSmoothingRunId={motion_smoothing_run_id}"
            f"&homographyRunId={homography_run_id}"
            f"&courtProjectionRunId={run.id}"
        ),
        "warnings": dict(COURT_PROJECTION_WARNINGS),
    }


def project_image_point_to_court_template(
    matrix: list[list[float]],
    x: float,
    y: float,
) -> dict[str, float] | None:
    scale = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2]
    if abs(scale) < 1e-12:
        return None
    projected_x = (matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]) / scale
    projected_y = (matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]) / scale
    return {"x": _round(projected_x), "y": _round(projected_y)}


def match_homography_for_timestamp(
    homographies: list[HomographyCandidateObservation],
    *,
    frame_number: int,
    timestamp_ms: int,
    max_gap_ms: int,
) -> HomographyMatch | None:
    candidates = [
        (homography, _image_to_template_matrix(homography))
        for homography in homographies
        if homography.status == "candidate"
    ]
    candidates = [(homography, matrix) for homography, matrix in candidates if matrix is not None]
    if not candidates:
        return None

    exact_frame = [
        (homography, matrix)
        for homography, matrix in candidates
        if homography.frame_number == frame_number
    ]
    if exact_frame:
        homography, matrix = sorted(
            exact_frame,
            key=lambda item: (
                abs(int(item[0].timestamp_ms) - timestamp_ms),
                item[0].observation_id,
            ),
        )[0]
        return HomographyMatch(
            homography=homography,
            matrix=matrix,
            policy="exact_frame",
            time_delta_ms=abs(int(homography.timestamp_ms) - timestamp_ms),
            carried_forward=False,
        )

    prior = [
        (homography, matrix)
        for homography, matrix in candidates
        if int(homography.timestamp_ms) <= timestamp_ms
        and timestamp_ms - int(homography.timestamp_ms) <= max_gap_ms
    ]
    if prior:
        homography, matrix = sorted(
            prior,
            key=lambda item: (-int(item[0].timestamp_ms), item[0].observation_id),
        )[0]
        return HomographyMatch(
            homography=homography,
            matrix=matrix,
            policy="latest_prior_within_gap",
            time_delta_ms=timestamp_ms - int(homography.timestamp_ms),
            carried_forward=homography.frame_number != frame_number,
        )

    nearest = [
        (homography, matrix)
        for homography, matrix in candidates
        if abs(int(homography.timestamp_ms) - timestamp_ms) <= max_gap_ms
    ]
    if nearest:
        homography, matrix = sorted(
            nearest,
            key=lambda item: (
                abs(int(item[0].timestamp_ms) - timestamp_ms),
                item[0].observation_id,
            ),
        )[0]
        return HomographyMatch(
            homography=homography,
            matrix=matrix,
            policy="nearest_within_gap",
            time_delta_ms=abs(int(homography.timestamp_ms) - timestamp_ms),
            carried_forward=homography.frame_number != frame_number,
        )
    return None


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "object-to-court-projection-candidates",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "projection",
            ModelRegistry.source == "apps.worker.services.object_court_projection",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="object-to-court-projection-candidates",
        version="v0",
        model_family="projection",
        source="apps.worker.services.object_court_projection",
        metadata_jsonb={
            "projection_method": COURT_PROJECTION_METHOD,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            **COURT_PROJECTION_WARNINGS,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    motion_smoothing_run_id: str,
    homography_run_id: str,
    config: ObjectProjectionConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="object-to-court-projection-candidates-config",
        config_version="v0",
        payload_jsonb={
            "projection_method": COURT_PROJECTION_METHOD,
            "source_motion_smoothing_run_id": motion_smoothing_run_id,
            "source_homography_run_id": homography_run_id,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "target_coordinate_space": CoordinateSpace.court_template_2d,
            "homography_match_policy": (
                "exact_frame_then_latest_prior_then_nearest_within_gap_v0"
            ),
            "homography_max_gap_ms": config.homography_max_gap_ms,
            "ball_projection_anchor": "smoothed_ball_center",
            "main_player_projection_anchor": "bbox_bottom_center",
            **COURT_PROJECTION_WARNINGS,
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
    motion_smoothing_run_id: str,
    homography_run_id: str,
    config: ObjectProjectionConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "projection_method": COURT_PROJECTION_METHOD,
            "source_motion_smoothing_run_id": motion_smoothing_run_id,
            "source_homography_run_id": homography_run_id,
            "homography_max_gap_ms": config.homography_max_gap_ms,
            "evidence_source": "court_projection_candidate",
            "source_label": "object-to-court projection candidates",
            **COURT_PROJECTION_WARNINGS,
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
        step_name="object_to_court_projection_candidates_v0",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "projection_method": COURT_PROJECTION_METHOD,
            **COURT_PROJECTION_WARNINGS,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _load_homographies(
    *,
    session: Session,
    media: MediaAsset,
    homography_run_id: str,
) -> list[HomographyCandidateObservation]:
    return list(
        session.scalars(
            select(HomographyCandidateObservation)
            .where(
                HomographyCandidateObservation.media_id == media.id,
                HomographyCandidateObservation.run_id == homography_run_id,
            )
            .order_by(
                HomographyCandidateObservation.timestamp_ms,
                HomographyCandidateObservation.frame_number,
                HomographyCandidateObservation.observation_id,
            )
        ).all()
    )


def _load_smoothed_ball_sources(
    *,
    session: Session,
    media: MediaAsset,
    motion_smoothing_run_id: str,
) -> list[SourceObjectCandidate]:
    rows = _load_smoothed_rows(
        session=session,
        media=media,
        motion_smoothing_run_id=motion_smoothing_run_id,
        observation_type="smoothed_ball_position_candidate",
    )
    sources = []
    for row in rows:
        payload = row.payload_jsonb or {}
        x = _number(payload.get("x"))
        y = _number(payload.get("y"))
        frame_number, timestamp_ms = _frame_time(row)
        if x is None or y is None or frame_number is None or timestamp_ms is None:
            continue
        sources.append(
            SourceObjectCandidate(
                observation=row,
                kind="ball",
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                image_point={"x": x, "y": y},
                image_anchor={"anchor_type": "smoothed_ball_center", "x": x, "y": y},
                confidence=row.confidence,
            )
        )
    return sources


def _load_smoothed_player_sources(
    *,
    session: Session,
    media: MediaAsset,
    motion_smoothing_run_id: str,
) -> list[SourceObjectCandidate]:
    rows = _load_smoothed_rows(
        session=session,
        media=media,
        motion_smoothing_run_id=motion_smoothing_run_id,
        observation_type="smoothed_main_player_box_candidate",
    )
    sources = []
    for row in rows:
        payload = row.payload_jsonb or {}
        bbox = _bbox(payload)
        frame_number, timestamp_ms = _frame_time(row)
        if bbox is None or frame_number is None or timestamp_ms is None:
            continue
        x = bbox["x"] + bbox["w"] / 2.0
        y = bbox["y"] + bbox["h"]
        sources.append(
            SourceObjectCandidate(
                observation=row,
                kind="main_player",
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                image_point={"x": _round(x), "y": _round(y)},
                image_anchor={
                    "anchor_type": "bbox_bottom_center",
                    "x": _round(x),
                    "y": _round(y),
                    "bbox": bbox,
                },
                confidence=row.confidence,
                track_candidate_id=_string_or_none(payload.get("track_candidate_id")),
                track_role_candidate=_string_or_none(payload.get("track_role_candidate")),
            )
        )
    return sources


def _load_smoothed_rows(
    *,
    session: Session,
    media: MediaAsset,
    motion_smoothing_run_id: str,
    observation_type: str,
) -> list[Observation]:
    return list(
        session.scalars(
            select(Observation)
            .where(
                Observation.media_id == media.id,
                Observation.run_id == motion_smoothing_run_id,
                Observation.observation_type == observation_type,
                Observation.timestamp_start_ms.is_not(None),
            )
            .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
        ).all()
    )


def _persist_projection_candidates(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    motion_smoothing_run_id: str,
    homography_run_id: str,
    homographies: list[HomographyCandidateObservation],
    sources: list[SourceObjectCandidate],
    config: ObjectProjectionConfig,
) -> dict[str, Any]:
    observations = []
    skipped = Counter({"missing_homography": 0, "invalid_projection": 0})
    for source in sources:
        match = match_homography_for_timestamp(
            homographies,
            frame_number=source.frame_number,
            timestamp_ms=source.timestamp_ms,
            max_gap_ms=config.homography_max_gap_ms,
        )
        if match is None:
            skipped["missing_homography"] += 1
            continue
        court_point = project_image_point_to_court_template(
            match.matrix,
            source.image_point["x"],
            source.image_point["y"],
        )
        if court_point is None:
            skipped["invalid_projection"] += 1
            continue
        observations.append(
            writer.write(
                _projection_observation_create(
                    media=media,
                    run=run,
                    step=step,
                    model=model,
                    runtime_config=runtime_config,
                    motion_smoothing_run_id=motion_smoothing_run_id,
                    homography_run_id=homography_run_id,
                    source=source,
                    match=match,
                    court_point=court_point,
                )
            )
        )
    return {"observations": observations, "skipped": dict(skipped)}


def _projection_observation_create(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    motion_smoothing_run_id: str,
    homography_run_id: str,
    source: SourceObjectCandidate,
    match: HomographyMatch,
    court_point: dict[str, float],
) -> ObservationCreate:
    is_ball = source.kind == "ball"
    observation_type = (
        BALL_COURT_PROJECTION_OBSERVATION_TYPE
        if is_ball
        else MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE
    )
    payload = {
        "source_motion_smoothing_run_id": motion_smoothing_run_id,
        "source_homography_run_id": homography_run_id,
        "source_homography_observation_id": match.homography.observation_id,
        "source_homography_candidate_observation_id": match.homography.observation_id,
        "frame_number": source.frame_number,
        "timestamp_ms": source.timestamp_ms,
        "court_point": court_point,
        "court_coordinate_space": CoordinateSpace.court_template_2d,
        "template_name": match.homography.template_name or COURT_TEMPLATE_NAME,
        "template_version": match.homography.template_version or COURT_TEMPLATE_VERSION,
        "source_homography_status": match.homography.status,
        "source_homography_confidence": match.homography.confidence,
        "homography_match_policy": match.policy,
        "homography_time_delta_ms": match.time_delta_ms,
        "homography_carried_forward": match.carried_forward,
        "homography_source_frame_number": match.homography.frame_number,
        "projection_frame_number": source.frame_number,
        "projection_candidate_only": True,
        "not_court_truth": True,
        "observation_only": True,
        "no_adjudication": True,
        "no_bounce_hit_in_out_score": True,
        "source_observation_ids": [
            source.observation.id,
            match.homography.observation_id,
        ],
    }
    if is_ball:
        payload.update(
            {
                "source_ball_observation_id": source.observation.id,
                "image_point": source.image_point,
                "projection_method": BALL_PROJECTION_METHOD,
                "not_ball_truth": True,
            }
        )
    else:
        payload.update(
            {
                "source_player_box_observation_id": source.observation.id,
                "source_main_player_track_run_id": (
                    source.observation.payload_jsonb or {}
                ).get("source_main_player_track_run_id"),
                "track_candidate_id": source.track_candidate_id,
                "track_role_candidate": source.track_role_candidate,
                "image_anchor": source.image_anchor,
                "projection_method": PLAYER_PROJECTION_METHOD,
                "not_player_truth": True,
                "not_identity_truth": True,
            }
        )
    return ObservationCreate(
        media_id=media.id,
        run_id=run.id,
        observation_family=ObservationFamily.projection,
        observation_type=observation_type,
        granularity=ObservationGranularity.frame,
        frame_start=source.frame_number,
        frame_end=source.frame_number,
        timestamp_start_ms=source.timestamp_ms,
        timestamp_end_ms=source.timestamp_ms,
        confidence=source.confidence,
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space=CoordinateSpace.court_template_2d,
        payload_jsonb={
            **payload,
            "processing_step_id": step.id,
            "projection_method": payload["projection_method"],
            "evidence_source": "court_projection_candidate",
            "source_label": (
                "ball court projection candidate"
                if is_ball
                else "main player court projection candidate"
            ),
            **COURT_PROJECTION_WARNINGS,
        },
        idempotency_key=f"{run.id}:{observation_type}:{source.observation.id}",
        lineage=[
            ObservationLineageCreate(
                parent_observation_id=source.observation.id,
                relationship_type=(
                    RelationshipType.projected_from_smoothed_ball_position
                    if is_ball
                    else RelationshipType.projected_from_smoothed_main_player_box
                ),
                processing_step_id=step.id,
                payload_jsonb={
                    "projection_method": payload["projection_method"],
                    "source_evidence_type": source.observation.observation_type,
                    **COURT_PROJECTION_WARNINGS,
                },
            ),
            ObservationLineageCreate(
                parent_observation_id=match.homography.observation_id,
                relationship_type=RelationshipType.projected_with_homography_candidate,
                processing_step_id=step.id,
                payload_jsonb={
                    "projection_method": payload["projection_method"],
                    "homography_match_policy": match.policy,
                    "homography_time_delta_ms": match.time_delta_ms,
                    "homography_carried_forward": match.carried_forward,
                    **COURT_PROJECTION_WARNINGS,
                },
            ),
        ],
    )


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_counts: dict[str, int],
    output_counts: dict[str, int],
    skipped: dict[str, int],
    sampled_frames: list[int],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "projection_method": COURT_PROJECTION_METHOD,
        "source_counts": source_counts,
        "output_counts": output_counts,
        "skipped": skipped,
        "sampled_frames": sampled_frames,
        "ball_court_projection_count": output_counts.get(
            BALL_COURT_PROJECTION_OBSERVATION_TYPE, 0
        ),
        "main_player_court_projection_count": output_counts.get(
            MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE, 0
        ),
        **COURT_PROJECTION_WARNINGS,
    }
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {**(run.metadata_jsonb or {}), **summary}
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {**(step.metadata_jsonb or {}), **summary}
    session.commit()


def _mark_failed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        "error": message,
        **COURT_PROJECTION_WARNINGS,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        **COURT_PROJECTION_WARNINGS,
    }
    session.commit()


def _image_to_template_matrix(
    homography: HomographyCandidateObservation,
) -> list[list[float]] | None:
    if homography.matrix_direction == "image_pixels_to_court_template_2d":
        return _matrix_or_none(homography.homography_matrix_jsonb)
    if (
        homography.matrix_direction == "court_template_2d_to_image_pixels"
        and homography.inverse_homography_matrix_jsonb is not None
    ):
        return _matrix_or_none(homography.inverse_homography_matrix_jsonb)
    return None


def _matrix_or_none(value: Any) -> list[list[float]] | None:
    if not isinstance(value, list) or len(value) != 3:
        return None
    matrix: list[list[float]] = []
    for row in value:
        if not isinstance(row, list) or len(row) != 3:
            return None
        matrix.append([float(cell) for cell in row])
    return matrix


def _bbox(payload: dict[str, Any]) -> dict[str, float] | None:
    raw = payload.get("bbox")
    if not isinstance(raw, dict):
        return None
    x = _number(raw.get("x"))
    y = _number(raw.get("y"))
    w = _number(raw.get("w") or raw.get("width"))
    h = _number(raw.get("h") or raw.get("height"))
    if x is None or y is None or w is None or h is None:
        return None
    return {"x": x, "y": y, "w": w, "h": h}


def _frame_time(row: Observation) -> tuple[int | None, int | None]:
    frame_number = row.frame_start if row.frame_start is not None else row.frame_end
    timestamp_ms = (
        row.timestamp_start_ms
        if row.timestamp_start_ms is not None
        else row.timestamp_end_ms
    )
    return (
        int(frame_number) if frame_number is not None else None,
        int(timestamp_ms) if timestamp_ms is not None else None,
    )


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _round(value: float) -> float:
    return round(float(value), 6)


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
        "warnings": dict(COURT_PROJECTION_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
