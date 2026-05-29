from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import mean
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
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

BALL_COURT_PROJECTION_OBSERVATION_TYPE = "ball_court_projection_candidate"
BALL_TRAJECTORY_OBSERVATION_TYPE = "ball_trajectory_court_candidate"
BALL_TRAJECTORY_METHOD = "ordered_projection_sequence_with_gap_segmentation_v0"
DEFAULT_MAX_GAP_FRAMES = 6
DEFAULT_MAX_GAP_MS = 250
DEFAULT_MIN_POINTS_PER_SEGMENT = 3
BALL_TRAJECTORY_WARNINGS = {
    "trajectory_candidate_only": True,
    "not_ball_truth": True,
    "not_bounce_truth": True,
    "not_hit_truth": True,
    "not_in_out_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_bounce_hit_in_out_score": True,
}


@dataclass(frozen=True)
class BallTrajectoryConfig:
    max_gap_frames: int = DEFAULT_MAX_GAP_FRAMES
    max_gap_ms: int = DEFAULT_MAX_GAP_MS
    min_points_per_segment: int = DEFAULT_MIN_POINTS_PER_SEGMENT

    def as_dict(self) -> dict[str, int]:
        return {
            "max_gap_frames": self.max_gap_frames,
            "max_gap_ms": self.max_gap_ms,
            "min_points_per_segment": self.min_points_per_segment,
        }


@dataclass(frozen=True)
class BallCourtProjectionPoint:
    observation: Observation
    frame_number: int
    timestamp_ms: int
    court_x: float
    court_y: float
    source_homography_observation_id: str | None
    homography_time_delta_ms: int | None
    homography_carried_forward: bool
    confidence: float | None

    @property
    def inside_template_bounds(self) -> bool:
        return 0.0 <= self.court_x <= 1.0 and 0.0 <= self.court_y <= 1.0


@dataclass(frozen=True)
class SegmentBuildResult:
    persisted_segments: list[list[BallCourtProjectionPoint]]
    dropped_short_segments: list[list[BallCourtProjectionPoint]]
    gap_split_count: int


def build_ball_court_trajectory_plan(
    *,
    media_id: str = "<media_id>",
    court_projection_run_id: str = "<court_projection_run_id>",
    run_name: str = "ball-trajectory-court-candidate-v0",
    max_gap_frames: int = DEFAULT_MAX_GAP_FRAMES,
    max_gap_ms: int = DEFAULT_MAX_GAP_MS,
    min_points_per_segment: int = DEFAULT_MIN_POINTS_PER_SEGMENT,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    return {
        "steps": [
            "validate_media_and_court_projection_run",
            "load_ball_court_projection_candidates",
            "order_projection_points_by_media_time",
            "split_trajectory_segments_by_frame_and_time_gaps",
            "compute_velocity_direction_and_gap_diagnostics",
            "persist_ball_trajectory_court_candidate_observations",
            "write_projection_point_lineage",
        ],
        "command": (
            "python -m apps.worker.cli build-ball-court-trajectory "
            f"--media-id {media_id} "
            f"--court-projection-run-id {court_projection_run_id} "
            f"--run-name {run_name} "
            f"--max-gap-frames {max_gap_frames} "
            f"--max-gap-ms {max_gap_ms} "
            f"--min-points-per-segment {min_points_per_segment}"
        ),
        "run_name": run_name,
        "source_run_ids": {"court_projection_run_id": court_projection_run_id},
        "trajectory_method": BALL_TRAJECTORY_METHOD,
        "coordinate_space": CoordinateSpace.court_template_2d,
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "max_gap_frames": max_gap_frames,
        "max_gap_ms": max_gap_ms,
        "min_points_per_segment": min_points_per_segment,
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
            f"?courtProjectionRunId={court_projection_run_id}"
            "&ballTrajectoryRunId=<ball_trajectory_run_id>"
        ),
        "warnings": dict(BALL_TRAJECTORY_WARNINGS),
    }


def build_ball_court_trajectory(
    *,
    session: Session,
    media_id: str,
    court_projection_run_id: str,
    run_name: str = "ball-trajectory-court-candidate-v0",
    max_gap_frames: int = DEFAULT_MAX_GAP_FRAMES,
    max_gap_ms: int = DEFAULT_MAX_GAP_MS,
    min_points_per_segment: int = DEFAULT_MIN_POINTS_PER_SEGMENT,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    invalid = _validate_config(max_gap_frames, max_gap_ms, min_points_per_segment)
    if invalid is not None:
        return invalid
    plan = build_ball_court_trajectory_plan(
        media_id=media_id,
        court_projection_run_id=court_projection_run_id,
        run_name=run_name,
        max_gap_frames=max_gap_frames,
        max_gap_ms=max_gap_ms,
        min_points_per_segment=min_points_per_segment,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "ball court trajectory candidate build planned",
            "plan": plan,
            "warnings": dict(BALL_TRAJECTORY_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")
    source_run = session.get(ProcessingRun, court_projection_run_id)
    if source_run is None:
        return _failed(
            "missing_court_projection_run",
            f"source run not found: {court_projection_run_id}",
        )
    if source_run.media_id != media.id:
        return _failed(
            "court_projection_run_media_mismatch",
            "court_projection_run_id does not match media_id",
        )

    config = BallTrajectoryConfig(
        max_gap_frames=max_gap_frames,
        max_gap_ms=max_gap_ms,
        min_points_per_segment=min_points_per_segment,
    )
    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            court_projection_run_id=court_projection_run_id,
            config=config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            court_projection_run_id=court_projection_run_id,
            config=config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        points = load_ball_court_projection_points(
            session=session,
            media=media,
            court_projection_run_id=court_projection_run_id,
        )
        segmented = segment_ball_court_projection_points(points, config)
        writer = ObservationWriter(session)
        observations = _persist_trajectory_segments(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            court_projection_run_id=court_projection_run_id,
            segments=segmented.persisted_segments,
            segment_offset=0,
            config=config,
            gap_split_count=segmented.gap_split_count,
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session=session, run=run, step=step, message=str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    counts = Counter(row.observation_type for row in observations)
    source_point_count = len(points)
    trajectory_summary = {
        "source_point_count": source_point_count,
        "segment_count": len(segmented.persisted_segments)
        + len(segmented.dropped_short_segments),
        "persisted_segment_count": len(segmented.persisted_segments),
        "dropped_short_segment_count": len(segmented.dropped_short_segments),
        "gap_split_count": segmented.gap_split_count,
        "out_of_template_count": sum(
            1 for point in points if not point.inside_template_bounds
        ),
    }
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_counts={
            BALL_COURT_PROJECTION_OBSERVATION_TYPE: source_point_count,
        },
        output_counts=dict(counts),
        trajectory_summary=trajectory_summary,
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "ball court trajectory candidate build complete",
        "ball_trajectory_run_id": run.id,
        "run_id": run.id,
        "media_id": media.id,
        "source_court_projection_run_id": court_projection_run_id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            BALL_TRAJECTORY_OBSERVATION_TYPE: counts.get(
                BALL_TRAJECTORY_OBSERVATION_TYPE, 0
            ),
            "total": sum(counts.values()),
        },
        "trajectory_summary": trajectory_summary,
        "observation_ids": [row.id for row in observations],
        "replay_url": (
            f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
            f"?courtProjectionRunId={court_projection_run_id}"
            f"&ballTrajectoryRunId={run.id}"
        ),
        "warnings": dict(BALL_TRAJECTORY_WARNINGS),
    }


def load_ball_court_projection_points(
    *,
    session: Session,
    media: MediaAsset,
    court_projection_run_id: str,
) -> list[BallCourtProjectionPoint]:
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == court_projection_run_id,
            Observation.observation_type == BALL_COURT_PROJECTION_OBSERVATION_TYPE,
            Observation.timestamp_start_ms.is_not(None),
        )
        .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
    ).all()
    points: list[BallCourtProjectionPoint] = []
    for row in rows:
        point = _point_from_observation(row)
        if point is not None:
            points.append(point)
    return points


def segment_ball_court_projection_points(
    points: list[BallCourtProjectionPoint],
    config: BallTrajectoryConfig,
) -> SegmentBuildResult:
    if not points:
        return SegmentBuildResult(
            persisted_segments=[],
            dropped_short_segments=[],
            gap_split_count=0,
        )

    segments: list[list[BallCourtProjectionPoint]] = []
    current: list[BallCourtProjectionPoint] = []
    gap_split_count = 0
    for point in sorted(
        points,
        key=lambda item: (
            item.timestamp_ms,
            item.frame_number,
            item.observation.id,
        ),
    ):
        if not current:
            current = [point]
            continue
        previous = current[-1]
        frame_gap = max(0, point.frame_number - previous.frame_number)
        time_gap = max(0, point.timestamp_ms - previous.timestamp_ms)
        if frame_gap > config.max_gap_frames or time_gap > config.max_gap_ms:
            segments.append(current)
            gap_split_count += 1
            current = [point]
        else:
            current.append(point)
    if current:
        segments.append(current)

    persisted = [
        segment
        for segment in segments
        if len(segment) >= config.min_points_per_segment
    ]
    dropped = [
        segment
        for segment in segments
        if len(segment) < config.min_points_per_segment
    ]
    return SegmentBuildResult(
        persisted_segments=persisted,
        dropped_short_segments=dropped,
        gap_split_count=gap_split_count,
    )


def compute_trajectory_kinematics(
    points: list[BallCourtProjectionPoint],
) -> list[dict[str, Any]]:
    kinematics: list[dict[str, Any]] = []
    for previous, current in zip(points, points[1:], strict=False):
        dt_ms = current.timestamp_ms - previous.timestamp_ms
        if dt_ms <= 0:
            continue
        dx = current.court_x - previous.court_x
        dy = current.court_y - previous.court_y
        speed = math.hypot(dx, dy) / (dt_ms / 1000.0)
        direction = math.degrees(math.atan2(dy, dx))
        kinematics.append(
            {
                "from_frame": previous.frame_number,
                "to_frame": current.frame_number,
                "dt_ms": dt_ms,
                "dx": _round(dx),
                "dy": _round(dy),
                "speed_template_units_per_second": _round(speed),
                "direction_angle_degrees": _round(direction),
            }
        )
    return kinematics


def _persist_trajectory_segments(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    court_projection_run_id: str,
    segments: list[list[BallCourtProjectionPoint]],
    segment_offset: int,
    config: BallTrajectoryConfig,
    gap_split_count: int,
) -> list[Any]:
    observations = []
    for index, segment in enumerate(segments, start=segment_offset):
        observations.append(
            writer.write(
                _trajectory_observation_create(
                    media=media,
                    run=run,
                    step=step,
                    model=model,
                    runtime_config=runtime_config,
                    court_projection_run_id=court_projection_run_id,
                    segment=segment,
                    segment_index=index,
                    config=config,
                    gap_split_count=gap_split_count,
                )
            )
        )
    return observations


def _trajectory_observation_create(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    court_projection_run_id: str,
    segment: list[BallCourtProjectionPoint],
    segment_index: int,
    config: BallTrajectoryConfig,
    gap_split_count: int,
) -> ObservationCreate:
    first = segment[0]
    last = segment[-1]
    points = [_point_payload(point) for point in segment]
    kinematics = compute_trajectory_kinematics(segment)
    source_ids = [point.observation.id for point in segment]
    homography_time_deltas = [
        point.homography_time_delta_ms
        for point in segment
        if point.homography_time_delta_ms is not None
    ]
    confidences = [
        point.confidence for point in segment if point.confidence is not None
    ]
    diagnostics = {
        "max_gap_frames": config.max_gap_frames,
        "max_gap_ms": config.max_gap_ms,
        "gap_count": gap_split_count,
        "segment_split_count": gap_split_count,
        "out_of_template_count": sum(
            1 for point in segment if not point.inside_template_bounds
        ),
        "out_of_template_fraction": _round(
            sum(1 for point in segment if not point.inside_template_bounds)
            / max(1, len(segment))
        ),
        "homography_carried_forward_count": sum(
            1 for point in segment if point.homography_carried_forward
        ),
        "mean_homography_time_delta_ms": (
            _round(mean(homography_time_deltas)) if homography_time_deltas else None
        ),
        "point_count": len(segment),
        "kinematic_step_count": len(kinematics),
    }
    return ObservationCreate(
        media_id=media.id,
        run_id=run.id,
        observation_family=ObservationFamily.trajectory,
        observation_type=BALL_TRAJECTORY_OBSERVATION_TYPE,
        granularity=ObservationGranularity.segment,
        frame_start=first.frame_number,
        frame_end=last.frame_number,
        timestamp_start_ms=first.timestamp_ms,
        timestamp_end_ms=last.timestamp_ms,
        confidence=_round(mean(confidences)) if confidences else None,
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space=CoordinateSpace.court_template_2d,
        payload_jsonb={
            "source_court_projection_run_id": court_projection_run_id,
            "source_ball_court_projection_observation_ids": source_ids,
            "trajectory_segment_index": segment_index,
            "frame_start": first.frame_number,
            "frame_end": last.frame_number,
            "timestamp_start_ms": first.timestamp_ms,
            "timestamp_end_ms": last.timestamp_ms,
            "point_count": len(segment),
            "points": points,
            "kinematics": kinematics,
            "diagnostics": diagnostics,
            "trajectory_method": BALL_TRAJECTORY_METHOD,
            "coordinate_space": CoordinateSpace.court_template_2d,
            "template_name": COURT_TEMPLATE_NAME,
            "template_version": COURT_TEMPLATE_VERSION,
            "processing_step_id": step.id,
            "evidence_source": "ball_trajectory_court_candidate",
            "source_label": "ball trajectory court candidate",
            **BALL_TRAJECTORY_WARNINGS,
        },
        idempotency_key=f"{run.id}:{BALL_TRAJECTORY_OBSERVATION_TYPE}:{segment_index}",
        lineage=[
            ObservationLineageCreate(
                parent_observation_id=point.observation.id,
                relationship_type=RelationshipType.trajectory_from_ball_court_projection,
                processing_step_id=step.id,
                payload_jsonb={
                    "trajectory_method": BALL_TRAJECTORY_METHOD,
                    "trajectory_segment_index": segment_index,
                    "source_evidence_type": point.observation.observation_type,
                    **BALL_TRAJECTORY_WARNINGS,
                },
            )
            for point in segment
        ],
    )


def _point_from_observation(row: Observation) -> BallCourtProjectionPoint | None:
    payload = row.payload_jsonb or {}
    court_point = payload.get("court_point")
    frame_number = _optional_int(row.frame_start)
    timestamp_ms = _optional_int(row.timestamp_start_ms)
    if frame_number is None:
        frame_number = _optional_int(payload.get("frame_number"))
    if timestamp_ms is None:
        timestamp_ms = _optional_int(payload.get("timestamp_ms"))
    if not isinstance(court_point, dict) or frame_number is None or timestamp_ms is None:
        return None
    court_x = _number(court_point.get("x"))
    court_y = _number(court_point.get("y"))
    if court_x is None or court_y is None:
        return None
    return BallCourtProjectionPoint(
        observation=row,
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        court_x=court_x,
        court_y=court_y,
        source_homography_observation_id=_string_or_none(
            payload.get("source_homography_observation_id")
            or payload.get("source_homography_candidate_observation_id")
        ),
        homography_time_delta_ms=_optional_int(payload.get("homography_time_delta_ms")),
        homography_carried_forward=bool(payload.get("homography_carried_forward")),
        confidence=row.confidence,
    )


def _point_payload(point: BallCourtProjectionPoint) -> dict[str, Any]:
    return {
        "frame_number": point.frame_number,
        "timestamp_ms": point.timestamp_ms,
        "court_x": _round(point.court_x),
        "court_y": _round(point.court_y),
        "source_observation_id": point.observation.id,
        "source_homography_observation_id": point.source_homography_observation_id,
        "homography_time_delta_ms": point.homography_time_delta_ms,
        "homography_carried_forward": point.homography_carried_forward,
        "inside_template_bounds": point.inside_template_bounds,
    }


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "ball-trajectory-court-candidate",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "trajectory",
            ModelRegistry.source == "apps.worker.services.ball_court_trajectory",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="ball-trajectory-court-candidate",
        version="v0",
        model_family="trajectory",
        source="apps.worker.services.ball_court_trajectory",
        metadata_jsonb={
            "trajectory_method": BALL_TRAJECTORY_METHOD,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            **BALL_TRAJECTORY_WARNINGS,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    court_projection_run_id: str,
    config: BallTrajectoryConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="ball-trajectory-court-candidate-config",
        config_version="v0",
        payload_jsonb={
            "trajectory_method": BALL_TRAJECTORY_METHOD,
            "source_court_projection_run_id": court_projection_run_id,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "coordinate_space": CoordinateSpace.court_template_2d,
            **config.as_dict(),
            **BALL_TRAJECTORY_WARNINGS,
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
    court_projection_run_id: str,
    config: BallTrajectoryConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "trajectory_method": BALL_TRAJECTORY_METHOD,
            "source_court_projection_run_id": court_projection_run_id,
            "evidence_source": "ball_trajectory_court_candidate",
            "source_label": "ball trajectory court candidate",
            **config.as_dict(),
            **BALL_TRAJECTORY_WARNINGS,
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
        step_name="ball_trajectory_court_candidate_v0",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "trajectory_method": BALL_TRAJECTORY_METHOD,
            **BALL_TRAJECTORY_WARNINGS,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_counts: dict[str, int],
    output_counts: dict[str, int],
    trajectory_summary: dict[str, int],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "trajectory_method": BALL_TRAJECTORY_METHOD,
        "source_counts": source_counts,
        "output_counts": output_counts,
        "trajectory_summary": trajectory_summary,
        "ball_trajectory_court_candidate_count": output_counts.get(
            BALL_TRAJECTORY_OBSERVATION_TYPE,
            0,
        ),
        **BALL_TRAJECTORY_WARNINGS,
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
        **BALL_TRAJECTORY_WARNINGS,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        **BALL_TRAJECTORY_WARNINGS,
    }
    session.commit()


def _validate_config(
    max_gap_frames: int,
    max_gap_ms: int,
    min_points_per_segment: int,
) -> dict[str, Any] | None:
    if max_gap_frames < 0:
        return _failed(
            "invalid_max_gap_frames",
            "max_gap_frames must be greater than or equal to zero",
        )
    if max_gap_ms < 0:
        return _failed(
            "invalid_max_gap_ms",
            "max_gap_ms must be greater than or equal to zero",
        )
    if min_points_per_segment < 1:
        return _failed(
            "invalid_min_points_per_segment",
            "min_points_per_segment must be at least one",
        )
    return None


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(BALL_TRAJECTORY_WARNINGS),
        **extra,
    }


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        number = float(value)
        return number if math.isfinite(number) else None
    return None


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return int(value)
    return None


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _round(value: float, digits: int = 6) -> float:
    return round(float(value), digits)
