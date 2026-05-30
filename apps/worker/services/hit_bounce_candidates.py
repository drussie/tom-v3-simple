from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal

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

BALL_TRAJECTORY_OBSERVATION_TYPE = "ball_trajectory_court_candidate"
BALL_COURT_PROJECTION_OBSERVATION_TYPE = "ball_court_projection_candidate"
MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE = "main_player_court_projection_candidate"
HIT_CANDIDATE_OBSERVATION_TYPE = "hit_candidate"
BOUNCE_CANDIDATE_OBSERVATION_TYPE = "bounce_candidate"
EVENT_CANDIDATE_OBSERVATION_TYPES = {
    HIT_CANDIDATE_OBSERVATION_TYPE,
    BOUNCE_CANDIDATE_OBSERVATION_TYPE,
}
HIT_CANDIDATE_METHOD = "net_axis_reversal_player_proximity_hit_candidate_v02"
BOUNCE_CANDIDATE_METHOD = "image_vertical_proxy_speed_reduction_bounce_candidate_v02"
EVENT_CANDIDATE_METHOD = "hit_bounce_physics_heuristic_candidate_evidence_v02"
DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE = 0.18
DEFAULT_HIT_PLAYER_REVIEW_DISTANCE_MAX_TEMPLATE = 0.33
DEFAULT_HIT_NEAR_PLAYER_DIRECTION_DELTA_DEGREES = 15.0
DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE = 0.015
DEFAULT_HIT_MIN_SPEED_DELTA_FRACTION = 0.10
DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE = 0.18
DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES = 25.0
DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES = 20.0
DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS = 2.0
DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION = 0.05
DEFAULT_CANDIDATE_DEDUPE_MS = 500
DEFAULT_PLAYER_TIME_WINDOW_MS = 200
DEFAULT_BOUNCE_TEMPLATE_MARGIN = 0.08
HIT_CONFIDENCE_CAP = 0.70
BOUNCE_CONFIDENCE_CAP = 0.60
EVENT_CANDIDATE_WARNINGS = {
    "candidate_only": True,
    "event_candidate_only": True,
    "not_hit_truth": True,
    "not_bounce_truth": True,
    "not_in_out_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_score_or_point_truth": True,
}


@dataclass(frozen=True)
class HitBounceCandidateConfig:
    hit_player_distance_max_template: float = DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE
    hit_player_review_distance_max_template: float = (
        DEFAULT_HIT_PLAYER_REVIEW_DISTANCE_MAX_TEMPLATE
    )
    hit_near_player_direction_delta_degrees: float = (
        DEFAULT_HIT_NEAR_PLAYER_DIRECTION_DELTA_DEGREES
    )
    hit_min_net_axis_delta_template: float = DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE
    hit_min_speed_delta_fraction: float = DEFAULT_HIT_MIN_SPEED_DELTA_FRACTION
    bounce_player_distance_min_template: float = DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE
    hit_min_direction_delta_degrees: float = DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES
    bounce_min_direction_delta_degrees: float = DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES
    bounce_min_image_y_delta_pixels: float = DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS
    bounce_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION
    )
    candidate_dedupe_ms: int = DEFAULT_CANDIDATE_DEDUPE_MS
    player_time_window_ms: int = DEFAULT_PLAYER_TIME_WINDOW_MS
    bounce_inside_template_margin: float = DEFAULT_BOUNCE_TEMPLATE_MARGIN

    def as_dict(self) -> dict[str, float | int]:
        return {
            "hit_player_distance_max_template": self.hit_player_distance_max_template,
            "hit_player_review_distance_max_template": (
                self.hit_player_review_distance_max_template
            ),
            "hit_near_player_direction_delta_degrees": (
                self.hit_near_player_direction_delta_degrees
            ),
            "hit_min_net_axis_delta_template": self.hit_min_net_axis_delta_template,
            "hit_min_speed_delta_fraction": self.hit_min_speed_delta_fraction,
            "bounce_player_distance_min_template": self.bounce_player_distance_min_template,
            "hit_min_direction_delta_degrees": self.hit_min_direction_delta_degrees,
            "bounce_min_direction_delta_degrees": self.bounce_min_direction_delta_degrees,
            "bounce_min_image_y_delta_pixels": self.bounce_min_image_y_delta_pixels,
            "bounce_min_speed_reduction_fraction": (
                self.bounce_min_speed_reduction_fraction
            ),
            "candidate_dedupe_ms": self.candidate_dedupe_ms,
            "player_time_window_ms": self.player_time_window_ms,
            "bounce_inside_template_margin": self.bounce_inside_template_margin,
        }


@dataclass(frozen=True)
class TrajectoryPoint:
    trajectory_observation: Observation
    frame_number: int
    timestamp_ms: int
    court_x: float
    court_y: float
    source_ball_court_projection_observation_id: str | None
    source_homography_observation_id: str | None
    homography_time_delta_ms: int | None
    homography_carried_forward: bool
    inside_template_bounds: bool
    image_x: float | None = None
    image_y: float | None = None


@dataclass(frozen=True)
class TrajectoryContext:
    previous: TrajectoryPoint
    current: TrajectoryPoint
    next: TrajectoryPoint
    direction_before_degrees: float
    direction_after_degrees: float
    direction_delta_degrees: float
    speed_before: float
    speed_after: float
    speed_delta_fraction: float


@dataclass(frozen=True)
class PlayerProjection:
    observation: Observation
    frame_number: int
    timestamp_ms: int
    court_x: float
    court_y: float
    track_candidate_id: str | None
    track_role_candidate: str | None


@dataclass(frozen=True)
class NearestPlayerContext:
    player: PlayerProjection
    distance_template_units: float
    time_delta_ms: int


@dataclass(frozen=True)
class EventCandidateDraft:
    observation_type: Literal["hit_candidate", "bounce_candidate"]
    candidate_method: str
    trajectory_context: TrajectoryContext
    nearest_player: NearestPlayerContext | None
    reason_codes: list[str]
    confidence: float
    player_proximity_gate: dict[str, Any]
    candidate_decision: dict[str, Any]
    net_axis_reversal: dict[str, Any] | None = None
    vertical_motion_proxy: dict[str, Any] | None = None
    speed_reduction: dict[str, Any] | None = None

    @property
    def timestamp_ms(self) -> int:
        return self.trajectory_context.current.timestamp_ms

    @property
    def frame_number(self) -> int:
        return self.trajectory_context.current.frame_number


def build_hit_bounce_candidates_plan(
    *,
    media_id: str = "<media_id>",
    ball_trajectory_run_id: str = "<ball_trajectory_run_id>",
    court_projection_run_id: str = "<court_projection_run_id>",
    run_name: str = "hit-bounce-candidate-evidence-v0",
    hit_player_distance_max_template: float = DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE,
    bounce_player_distance_min_template: float = DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE,
    hit_min_direction_delta_degrees: float = DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES,
    bounce_min_direction_delta_degrees: float = DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES,
    hit_min_net_axis_delta_template: float = DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE,
    bounce_min_image_y_delta_pixels: float = DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS,
    bounce_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION
    ),
    candidate_dedupe_ms: int = DEFAULT_CANDIDATE_DEDUPE_MS,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    return {
        "steps": [
            "validate_media_and_source_runs",
            "load_ball_trajectory_court_candidates",
            "load_main_player_court_projection_candidates",
            "load_source_ball_projection_image_points",
            "evaluate_net_axis_reversal_vertical_proxy_speed_and_player_proximity",
            "dedupe_candidate_clusters",
            "persist_hit_and_bounce_candidate_observations",
            "write_candidate_source_lineage",
        ],
        "command": (
            "python -m apps.worker.cli build-hit-bounce-candidates "
            f"--media-id {media_id} "
            f"--ball-trajectory-run-id {ball_trajectory_run_id} "
            f"--court-projection-run-id {court_projection_run_id} "
            f"--run-name {run_name} "
            f"--hit-player-distance-max-template {hit_player_distance_max_template} "
            f"--bounce-player-distance-min-template {bounce_player_distance_min_template} "
            f"--hit-min-direction-delta-degrees {hit_min_direction_delta_degrees} "
            f"--bounce-min-direction-delta-degrees {bounce_min_direction_delta_degrees} "
            f"--hit-min-net-axis-delta-template {hit_min_net_axis_delta_template} "
            f"--bounce-min-image-y-delta-pixels {bounce_min_image_y_delta_pixels} "
            f"--bounce-min-speed-reduction-fraction {bounce_min_speed_reduction_fraction} "
            f"--candidate-dedupe-ms {candidate_dedupe_ms}"
        ),
        "run_name": run_name,
        "source_run_ids": {
            "ball_trajectory_run_id": ball_trajectory_run_id,
            "court_projection_run_id": court_projection_run_id,
        },
        "candidate_method": EVENT_CANDIDATE_METHOD,
        "hit_candidate_method": HIT_CANDIDATE_METHOD,
        "bounce_candidate_method": BOUNCE_CANDIDATE_METHOD,
        "classification_priority": "hit_first_when_player_proximate",
        "coordinate_space": CoordinateSpace.court_template_2d,
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "thresholds": {
            "hit_player_distance_max_template": hit_player_distance_max_template,
            "hit_player_review_distance_max_template": (
                DEFAULT_HIT_PLAYER_REVIEW_DISTANCE_MAX_TEMPLATE
            ),
            "hit_near_player_direction_delta_degrees": (
                DEFAULT_HIT_NEAR_PLAYER_DIRECTION_DELTA_DEGREES
            ),
            "hit_min_net_axis_delta_template": hit_min_net_axis_delta_template,
            "hit_min_speed_delta_fraction": DEFAULT_HIT_MIN_SPEED_DELTA_FRACTION,
            "bounce_player_distance_min_template": bounce_player_distance_min_template,
            "hit_min_direction_delta_degrees": hit_min_direction_delta_degrees,
            "bounce_min_direction_delta_degrees": bounce_min_direction_delta_degrees,
            "bounce_min_image_y_delta_pixels": bounce_min_image_y_delta_pixels,
            "bounce_min_speed_reduction_fraction": bounce_min_speed_reduction_fraction,
            "candidate_dedupe_ms": candidate_dedupe_ms,
        },
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
            f"?courtProjectionRunId={court_projection_run_id}"
            f"&ballTrajectoryRunId={ball_trajectory_run_id}"
            "&eventCandidateRunId=<event_candidate_run_id>"
        ),
        "warnings": dict(EVENT_CANDIDATE_WARNINGS),
    }


def build_hit_bounce_candidates(
    *,
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    run_name: str = "hit-bounce-candidate-evidence-v0",
    hit_player_distance_max_template: float = DEFAULT_HIT_PLAYER_DISTANCE_MAX_TEMPLATE,
    bounce_player_distance_min_template: float = DEFAULT_BOUNCE_PLAYER_DISTANCE_MIN_TEMPLATE,
    hit_min_direction_delta_degrees: float = DEFAULT_HIT_MIN_DIRECTION_DELTA_DEGREES,
    bounce_min_direction_delta_degrees: float = DEFAULT_BOUNCE_MIN_DIRECTION_DELTA_DEGREES,
    hit_min_net_axis_delta_template: float = DEFAULT_HIT_MIN_NET_AXIS_DELTA_TEMPLATE,
    bounce_min_image_y_delta_pixels: float = DEFAULT_BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS,
    bounce_min_speed_reduction_fraction: float = (
        DEFAULT_BOUNCE_MIN_SPEED_REDUCTION_FRACTION
    ),
    candidate_dedupe_ms: int = DEFAULT_CANDIDATE_DEDUPE_MS,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    config = HitBounceCandidateConfig(
        hit_player_distance_max_template=hit_player_distance_max_template,
        bounce_player_distance_min_template=bounce_player_distance_min_template,
        hit_min_direction_delta_degrees=hit_min_direction_delta_degrees,
        bounce_min_direction_delta_degrees=bounce_min_direction_delta_degrees,
        hit_min_net_axis_delta_template=hit_min_net_axis_delta_template,
        bounce_min_image_y_delta_pixels=bounce_min_image_y_delta_pixels,
        bounce_min_speed_reduction_fraction=bounce_min_speed_reduction_fraction,
        candidate_dedupe_ms=candidate_dedupe_ms,
    )
    invalid = _validate_config(config)
    if invalid is not None:
        return invalid
    plan = build_hit_bounce_candidates_plan(
        media_id=media_id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        court_projection_run_id=court_projection_run_id,
        run_name=run_name,
        hit_player_distance_max_template=hit_player_distance_max_template,
        bounce_player_distance_min_template=bounce_player_distance_min_template,
        hit_min_direction_delta_degrees=hit_min_direction_delta_degrees,
        bounce_min_direction_delta_degrees=bounce_min_direction_delta_degrees,
        hit_min_net_axis_delta_template=hit_min_net_axis_delta_template,
        bounce_min_image_y_delta_pixels=bounce_min_image_y_delta_pixels,
        bounce_min_speed_reduction_fraction=bounce_min_speed_reduction_fraction,
        candidate_dedupe_ms=candidate_dedupe_ms,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "hit/bounce candidate evidence build planned",
            "plan": plan,
            "warnings": dict(EVENT_CANDIDATE_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")
    for label, run_id in (
        ("ball_trajectory_run_id", ball_trajectory_run_id),
        ("court_projection_run_id", court_projection_run_id),
    ):
        source_run = session.get(ProcessingRun, run_id)
        if source_run is None:
            return _failed(f"missing_{label}", f"source run not found: {run_id}")
        if source_run.media_id != media.id:
            return _failed(f"{label}_media_mismatch", f"{label} does not match media_id")

    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            config=config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            config=config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        trajectory_segments = load_ball_trajectory_segments(
            session=session,
            media=media,
            ball_trajectory_run_id=ball_trajectory_run_id,
        )
        player_projections = load_main_player_court_projections(
            session=session,
            media=media,
            court_projection_run_id=court_projection_run_id,
        )
        evaluated_contexts, hit_drafts, bounce_drafts = evaluate_event_candidates(
            trajectory_segments=trajectory_segments,
            player_projections=player_projections,
            config=config,
        )
        deduped_hits = dedupe_event_candidates(
            hit_drafts,
            candidate_dedupe_ms=config.candidate_dedupe_ms,
        )
        deduped_bounces = dedupe_event_candidates(
            bounce_drafts,
            candidate_dedupe_ms=config.candidate_dedupe_ms,
        )
        deduped_bounces, suppressed_bounce_conflict_count = suppress_bounces_near_hits(
            deduped_hits,
            deduped_bounces,
            candidate_dedupe_ms=config.candidate_dedupe_ms,
        )
        writer = ObservationWriter(session)
        observations = _persist_event_candidates(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            candidates=[*deduped_hits, *deduped_bounces],
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session=session, run=run, step=step, message=str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    counts = Counter(row.observation_type for row in observations)
    candidate_summary = {
        "trajectory_segment_count": len(trajectory_segments),
        "evaluated_trajectory_points": evaluated_contexts,
        "hit_candidate_count": len(hit_drafts),
        "bounce_candidate_count": len(bounce_drafts),
        "deduped_hit_candidate_count": len(deduped_hits),
        "deduped_bounce_candidate_count": len(deduped_bounces),
        "suppressed_bounce_conflict_count": suppressed_bounce_conflict_count,
        "classification_priority": "hit_first_when_player_proximate",
        "physics_heuristic_version": "v0.2",
    }
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_counts={
            BALL_TRAJECTORY_OBSERVATION_TYPE: len(trajectory_segments),
            MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE: len(player_projections),
        },
        output_counts=dict(counts),
        candidate_summary=candidate_summary,
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "hit/bounce candidate evidence build complete",
        "event_candidate_run_id": run.id,
        "run_id": run.id,
        "media_id": media.id,
        "source_run_ids": {
            "ball_trajectory_run_id": ball_trajectory_run_id,
            "court_projection_run_id": court_projection_run_id,
        },
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            HIT_CANDIDATE_OBSERVATION_TYPE: counts.get(HIT_CANDIDATE_OBSERVATION_TYPE, 0),
            BOUNCE_CANDIDATE_OBSERVATION_TYPE: counts.get(
                BOUNCE_CANDIDATE_OBSERVATION_TYPE, 0
            ),
            "total": sum(counts.values()),
        },
        "candidate_summary": candidate_summary,
        "observation_ids": [row.id for row in observations],
        "replay_url": (
            f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
            f"?courtProjectionRunId={court_projection_run_id}"
            f"&ballTrajectoryRunId={ball_trajectory_run_id}"
            f"&eventCandidateRunId={run.id}"
        ),
        "warnings": dict(EVENT_CANDIDATE_WARNINGS),
    }


def load_ball_trajectory_segments(
    *,
    session: Session,
    media: MediaAsset,
    ball_trajectory_run_id: str,
) -> list[list[TrajectoryPoint]]:
    rows = list(
        session.scalars(
            select(Observation)
            .where(
                Observation.media_id == media.id,
                Observation.run_id == ball_trajectory_run_id,
                Observation.observation_type == BALL_TRAJECTORY_OBSERVATION_TYPE,
                Observation.timestamp_start_ms.is_not(None),
            )
            .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
        ).all()
    )
    image_points_by_observation_id = _load_source_ball_projection_image_points(
        session=session,
        media=media,
        trajectory_rows=rows,
    )
    segments = []
    for row in rows:
        points = _trajectory_points_from_observation(
            row,
            image_points_by_observation_id=image_points_by_observation_id,
        )
        if points:
            segments.append(points)
    return segments


def _load_source_ball_projection_image_points(
    *,
    session: Session,
    media: MediaAsset,
    trajectory_rows: list[Observation],
) -> dict[str, tuple[float, float]]:
    source_ids: set[str] = set()
    for row in trajectory_rows:
        payload = row.payload_jsonb or {}
        raw_points = payload.get("points")
        if not isinstance(raw_points, list):
            continue
        for raw_point in raw_points:
            if not isinstance(raw_point, dict):
                continue
            source_id = _string_or_none(
                raw_point.get("source_observation_id")
                or raw_point.get("source_ball_court_projection_observation_id")
            )
            if source_id is not None:
                source_ids.add(source_id)
    if not source_ids:
        return {}
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.id.in_(source_ids),
            Observation.observation_type == BALL_COURT_PROJECTION_OBSERVATION_TYPE,
        )
    ).all()
    image_points: dict[str, tuple[float, float]] = {}
    for row in rows:
        image_point = _image_point_tuple((row.payload_jsonb or {}).get("image_point"))
        if image_point is not None:
            image_points[row.id] = image_point
    return image_points


def load_main_player_court_projections(
    *,
    session: Session,
    media: MediaAsset,
    court_projection_run_id: str,
) -> list[PlayerProjection]:
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == court_projection_run_id,
            Observation.observation_type == MAIN_PLAYER_COURT_PROJECTION_OBSERVATION_TYPE,
            Observation.timestamp_start_ms.is_not(None),
        )
        .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
    ).all()
    projections = []
    for row in rows:
        projection = _player_projection_from_observation(row)
        if projection is not None:
            projections.append(projection)
    return projections


def evaluate_event_candidates(
    *,
    trajectory_segments: list[list[TrajectoryPoint]],
    player_projections: list[PlayerProjection],
    config: HitBounceCandidateConfig,
) -> tuple[int, list[EventCandidateDraft], list[EventCandidateDraft]]:
    hit_candidates: list[EventCandidateDraft] = []
    bounce_candidates: list[EventCandidateDraft] = []
    evaluated_contexts = 0
    for segment in trajectory_segments:
        for index in range(1, len(segment) - 1):
            context = trajectory_context(
                segment[index - 1],
                segment[index],
                segment[index + 1],
            )
            if context is None:
                continue
            evaluated_contexts += 1
            net_axis_reversal = _net_axis_reversal_payload(segment, index, config)
            vertical_motion_proxy = _vertical_motion_proxy_payload(segment, index, config)
            speed_reduction = _speed_reduction_payload(context, config)
            nearest_player = nearest_main_player_projection(
                segment[index],
                player_projections,
                time_window_ms=config.player_time_window_ms,
            )
            if _is_player_proximate_hit_context(
                context,
                nearest_player,
                config,
                net_axis_reversal=net_axis_reversal,
            ):
                hit_candidates.append(
                    _hit_candidate_from_context(
                        context,
                        nearest_player,
                        config,
                        net_axis_reversal=net_axis_reversal,
                    )
                )
                continue
            if _is_bounce_context(
                context,
                nearest_player,
                config,
                vertical_motion_proxy=vertical_motion_proxy,
                speed_reduction=speed_reduction,
            ):
                bounce_candidates.append(
                    _bounce_candidate_from_context(
                        context,
                        nearest_player,
                        config,
                        vertical_motion_proxy=vertical_motion_proxy,
                        speed_reduction=speed_reduction,
                    )
                )
    return evaluated_contexts, hit_candidates, bounce_candidates


def trajectory_context(
    previous: TrajectoryPoint,
    current: TrajectoryPoint,
    next_point: TrajectoryPoint,
) -> TrajectoryContext | None:
    dt_before_ms = current.timestamp_ms - previous.timestamp_ms
    dt_after_ms = next_point.timestamp_ms - current.timestamp_ms
    if dt_before_ms <= 0 or dt_after_ms <= 0:
        return None
    dx_before = current.court_x - previous.court_x
    dy_before = current.court_y - previous.court_y
    dx_after = next_point.court_x - current.court_x
    dy_after = next_point.court_y - current.court_y
    speed_before = math.hypot(dx_before, dy_before) / (dt_before_ms / 1000.0)
    speed_after = math.hypot(dx_after, dy_after) / (dt_after_ms / 1000.0)
    if speed_before <= 0 and speed_after <= 0:
        return None
    direction_before = math.degrees(math.atan2(dy_before, dx_before))
    direction_after = math.degrees(math.atan2(dy_after, dx_after))
    direction_delta = angle_delta_degrees(direction_before, direction_after)
    speed_delta_fraction = abs(speed_after - speed_before) / max(
        speed_before,
        speed_after,
        1e-9,
    )
    return TrajectoryContext(
        previous=previous,
        current=current,
        next=next_point,
        direction_before_degrees=_round(direction_before),
        direction_after_degrees=_round(direction_after),
        direction_delta_degrees=_round(direction_delta),
        speed_before=_round(speed_before),
        speed_after=_round(speed_after),
        speed_delta_fraction=_round(speed_delta_fraction),
    )


def angle_delta_degrees(a: float, b: float) -> float:
    return abs((b - a + 180.0) % 360.0 - 180.0)


def nearest_main_player_projection(
    point: TrajectoryPoint,
    player_projections: list[PlayerProjection],
    *,
    time_window_ms: int,
) -> NearestPlayerContext | None:
    candidates: list[NearestPlayerContext] = []
    for player in player_projections:
        time_delta = abs(player.timestamp_ms - point.timestamp_ms)
        if time_delta > time_window_ms:
            continue
        distance = math.hypot(player.court_x - point.court_x, player.court_y - point.court_y)
        candidates.append(
            NearestPlayerContext(
                player=player,
                distance_template_units=_round(distance),
                time_delta_ms=time_delta,
            )
        )
    return min(
        candidates,
        key=lambda candidate: (
            candidate.time_delta_ms,
            candidate.distance_template_units,
            candidate.player.observation.id,
        ),
        default=None,
    )


def _net_axis_reversal_payload(
    segment: list[TrajectoryPoint],
    index: int,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    current = segment[index]
    previous = next(
        (
            point
            for point in reversed(segment[:index])
            if abs(current.court_y - point.court_y)
            >= config.hit_min_net_axis_delta_template
        ),
        None,
    )
    next_point = next(
        (
            point
            for point in segment[index + 1 :]
            if abs(point.court_y - current.court_y)
            >= config.hit_min_net_axis_delta_template
        ),
        None,
    )
    vy_before = current.court_y - previous.court_y if previous is not None else None
    vy_after = next_point.court_y - current.court_y if next_point is not None else None
    reversal = (
        vy_before is not None
        and vy_after is not None
        and abs(vy_before) >= config.hit_min_net_axis_delta_template
        and abs(vy_after) >= config.hit_min_net_axis_delta_template
        and vy_before * vy_after < 0
    )
    return {
        "axis": "court_y",
        "vy_before": _round(vy_before) if vy_before is not None else None,
        "vy_after": _round(vy_after) if vy_after is not None else None,
        "reversal": reversal,
        "min_axis_delta": config.hit_min_net_axis_delta_template,
        "previous_frame": previous.frame_number if previous is not None else None,
        "current_frame": current.frame_number,
        "next_frame": next_point.frame_number if next_point is not None else None,
        "previous_timestamp_ms": (
            previous.timestamp_ms if previous is not None else None
        ),
        "current_timestamp_ms": current.timestamp_ms,
        "next_timestamp_ms": next_point.timestamp_ms if next_point is not None else None,
    }


def _vertical_motion_proxy_payload(
    segment: list[TrajectoryPoint],
    index: int,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    current = segment[index]
    if current.image_y is None:
        return {
            "proxy_type": "image_y_descending_to_ascending_v0",
            "status": "unavailable",
            "image_y_before": None,
            "image_y_current": None,
            "image_y_after": None,
            "image_vy_before": None,
            "image_vy_after": None,
            "descending_to_ascending": False,
            "min_image_y_delta_pixels": config.bounce_min_image_y_delta_pixels,
            "proxy_warning": "image_y is camera-space proxy, not true ball height",
        }

    previous = next(
        (
            point
            for point in reversed(segment[:index])
            if point.image_y is not None
            and current.image_y - point.image_y
            >= config.bounce_min_image_y_delta_pixels
        ),
        None,
    )
    next_point = next(
        (
            point
            for point in segment[index + 1 :]
            if point.image_y is not None
            and point.image_y - current.image_y
            <= -config.bounce_min_image_y_delta_pixels
        ),
        None,
    )
    image_vy_before = (
        current.image_y - previous.image_y
        if previous is not None and previous.image_y is not None
        else None
    )
    image_vy_after = (
        next_point.image_y - current.image_y
        if next_point is not None and next_point.image_y is not None
        else None
    )
    descending_to_ascending = (
        image_vy_before is not None
        and image_vy_after is not None
        and image_vy_before >= config.bounce_min_image_y_delta_pixels
        and image_vy_after <= -config.bounce_min_image_y_delta_pixels
    )
    return {
        "proxy_type": "image_y_descending_to_ascending_v0",
        "status": "available" if previous is not None and next_point is not None else "partial",
        "image_y_before": _round(previous.image_y) if previous is not None else None,
        "image_y_current": _round(current.image_y),
        "image_y_after": _round(next_point.image_y) if next_point is not None else None,
        "image_vy_before": (
            _round(image_vy_before) if image_vy_before is not None else None
        ),
        "image_vy_after": _round(image_vy_after) if image_vy_after is not None else None,
        "descending_to_ascending": descending_to_ascending,
        "min_image_y_delta_pixels": config.bounce_min_image_y_delta_pixels,
        "previous_frame": previous.frame_number if previous is not None else None,
        "current_frame": current.frame_number,
        "next_frame": next_point.frame_number if next_point is not None else None,
        "previous_timestamp_ms": (
            previous.timestamp_ms if previous is not None else None
        ),
        "current_timestamp_ms": current.timestamp_ms,
        "next_timestamp_ms": next_point.timestamp_ms if next_point is not None else None,
        "proxy_warning": "image_y is camera-space proxy, not true ball height",
    }


def _speed_reduction_payload(
    context: TrajectoryContext,
    config: HitBounceCandidateConfig,
) -> dict[str, Any]:
    if context.speed_before <= 0:
        reduction_fraction = None
        speed_reduced = False
    else:
        reduction_fraction = (context.speed_before - context.speed_after) / max(
            context.speed_before,
            1e-9,
        )
        speed_reduced = reduction_fraction >= config.bounce_min_speed_reduction_fraction
    return {
        "speed_before": context.speed_before,
        "speed_after": context.speed_after,
        "speed_reduction_fraction": (
            _round(reduction_fraction) if reduction_fraction is not None else None
        ),
        "speed_reduced": speed_reduced,
        "min_speed_reduction_fraction": config.bounce_min_speed_reduction_fraction,
    }


def dedupe_event_candidates(
    candidates: list[EventCandidateDraft],
    *,
    candidate_dedupe_ms: int,
) -> list[EventCandidateDraft]:
    kept: list[EventCandidateDraft] = []
    for candidate in sorted(
        candidates,
        key=lambda item: (
            -item.confidence,
            item.timestamp_ms,
            item.frame_number,
            item.trajectory_context.current.source_ball_court_projection_observation_id or "",
        ),
    ):
        key = _dedupe_key(candidate)
        if any(
            _dedupe_key(existing) == key
            and abs(existing.timestamp_ms - candidate.timestamp_ms) <= candidate_dedupe_ms
            for existing in kept
        ):
            continue
        kept.append(candidate)
    return sorted(kept, key=lambda item: (item.timestamp_ms, item.frame_number))


def suppress_bounces_near_hits(
    hit_candidates: list[EventCandidateDraft],
    bounce_candidates: list[EventCandidateDraft],
    *,
    candidate_dedupe_ms: int,
) -> tuple[list[EventCandidateDraft], int]:
    filtered_bounces: list[EventCandidateDraft] = []
    suppressed_count = 0
    for bounce in bounce_candidates:
        suppressing_hit = next(
            (
                hit
                for hit in hit_candidates
                if abs(hit.timestamp_ms - bounce.timestamp_ms) <= candidate_dedupe_ms
                and hit.nearest_player is not None
            ),
            None,
        )
        if suppressing_hit is not None:
            suppressed_count += 1
            continue
        filtered_bounces.append(bounce)
    return filtered_bounces, suppressed_count


def _is_player_proximate_hit_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
) -> bool:
    if nearest_player is None:
        return False
    if nearest_player.distance_template_units > config.hit_player_review_distance_max_template:
        return False
    if net_axis_reversal.get("reversal") is not True:
        return False
    strong_direction_change = (
        context.direction_delta_degrees >= config.hit_min_direction_delta_degrees
    )
    meaningful_speed_change = (
        context.speed_delta_fraction >= config.hit_min_speed_delta_fraction
    )
    relaxed_contact_change = (
        context.direction_delta_degrees
        >= config.hit_near_player_direction_delta_degrees
        or meaningful_speed_change
    )
    close_contact_zone = (
        nearest_player.distance_template_units <= config.hit_player_distance_max_template
    )
    return strong_direction_change or (close_contact_zone and relaxed_contact_change)


def _is_bounce_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    vertical_motion_proxy: dict[str, Any],
    speed_reduction: dict[str, Any],
) -> bool:
    away_from_player = (
        nearest_player is None
        or nearest_player.distance_template_units
        >= config.bounce_player_distance_min_template
    )
    return (
        away_from_player
        and vertical_motion_proxy.get("descending_to_ascending") is True
        and speed_reduction.get("speed_reduced") is True
        and _inside_or_near_template(context.current, config.bounce_inside_template_margin)
    )


def _hit_candidate_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext,
    config: HitBounceCandidateConfig,
    *,
    net_axis_reversal: dict[str, Any],
) -> EventCandidateDraft:
    proximity_score = 1.0 - min(
        nearest_player.distance_template_units
        / max(config.hit_player_review_distance_max_template, 1e-9),
        1.0,
    )
    axis_strength = (
        (abs(float(net_axis_reversal.get("vy_before") or 0.0)))
        + (abs(float(net_axis_reversal.get("vy_after") or 0.0)))
    ) / max(config.hit_min_net_axis_delta_template * 4.0, 1e-9)
    axis_score = min(axis_strength, 1.0)
    direction_score = min(context.direction_delta_degrees / 90.0, 1.0)
    speed_score = min(context.speed_delta_fraction, 1.0)
    time_score = 1.0 - min(
        nearest_player.time_delta_ms / max(config.player_time_window_ms, 1),
        1.0,
    )
    confidence = min(
        HIT_CONFIDENCE_CAP,
        0.15
        + 0.27 * proximity_score
        + 0.22 * axis_score
        + 0.16 * direction_score
        + 0.08 * speed_score
        + 0.05 * time_score,
    )
    reason_codes = [
        "near_main_player_projection",
        "net_axis_reversal",
        "trajectory_direction_change",
        "player_proximate_event_priority",
    ]
    if context.speed_delta_fraction >= config.hit_min_speed_delta_fraction:
        reason_codes.append("speed_change_candidate")
    if nearest_player.time_delta_ms <= config.player_time_window_ms:
        reason_codes.append("within_time_window")
    return EventCandidateDraft(
        observation_type=HIT_CANDIDATE_OBSERVATION_TYPE,
        candidate_method=HIT_CANDIDATE_METHOD,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=reason_codes,
        confidence=_round(confidence),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.hit_player_review_distance_max_template,
            away_from_player=False,
        ),
        candidate_decision={
            "selected_candidate_type": HIT_CANDIDATE_OBSERVATION_TYPE,
            "suppressed_candidate_types": [BOUNCE_CANDIDATE_OBSERVATION_TYPE],
            "reason": "player_proximate_trajectory_change",
            "classification_priority": "hit_first_when_player_proximate",
        },
        net_axis_reversal=net_axis_reversal,
    )


def _bounce_candidate_from_context(
    context: TrajectoryContext,
    nearest_player: NearestPlayerContext | None,
    config: HitBounceCandidateConfig,
    *,
    vertical_motion_proxy: dict[str, Any],
    speed_reduction: dict[str, Any],
) -> EventCandidateDraft:
    image_vy_before = abs(float(vertical_motion_proxy.get("image_vy_before") or 0.0))
    image_vy_after = abs(float(vertical_motion_proxy.get("image_vy_after") or 0.0))
    vertical_score = min(
        (image_vy_before + image_vy_after)
        / max(config.bounce_min_image_y_delta_pixels * 12.0, 1e-9),
        1.0,
    )
    speed_reduction_fraction = float(
        speed_reduction.get("speed_reduction_fraction") or 0.0
    )
    speed_score = min(
        speed_reduction_fraction
        / max(config.bounce_min_speed_reduction_fraction * 4.0, 1e-9),
        1.0,
    )
    away_score = (
        1.0
        if nearest_player is None
        else min(
            nearest_player.distance_template_units
            / max(config.bounce_player_distance_min_template * 2.0, 1e-9),
            1.0,
        )
    )
    inside_score = (
        1.0
        if context.current.inside_template_bounds
        else 0.6
        if _inside_or_near_template(context.current, config.bounce_inside_template_margin)
        else 0.0
    )
    confidence = min(
        BOUNCE_CONFIDENCE_CAP,
        0.12
        + 0.28 * vertical_score
        + 0.18 * speed_score
        + 0.20 * away_score
        + 0.15 * inside_score
    )
    reason_codes = [
        "descending_to_ascending_image_proxy",
        "speed_reduction_candidate",
        "away_from_main_player_projection",
        "inside_or_near_court_template",
    ]
    if context.direction_delta_degrees >= config.bounce_min_direction_delta_degrees:
        reason_codes.append("trajectory_direction_change")
    if context.speed_delta_fraction >= 0.2:
        reason_codes.append("local_motion_discontinuity")
    return EventCandidateDraft(
        observation_type=BOUNCE_CANDIDATE_OBSERVATION_TYPE,
        candidate_method=BOUNCE_CANDIDATE_METHOD,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=reason_codes,
        confidence=_round(confidence),
        player_proximity_gate=_player_proximity_gate_payload(
            nearest_player=nearest_player,
            threshold=config.bounce_player_distance_min_template,
            away_from_player=(
                nearest_player is None
                or nearest_player.distance_template_units
                >= config.bounce_player_distance_min_template
            ),
        ),
        candidate_decision={
            "selected_candidate_type": BOUNCE_CANDIDATE_OBSERVATION_TYPE,
            "suppressed_candidate_types": [],
            "reason": "away_from_player_descending_ascending_speed_reduction",
            "classification_priority": "hit_first_when_player_proximate",
        },
        vertical_motion_proxy=vertical_motion_proxy,
        speed_reduction=speed_reduction,
    )


def _persist_event_candidates(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    candidates: list[EventCandidateDraft],
) -> list[Any]:
    observations = []
    for index, candidate in enumerate(candidates):
        observations.append(
            writer.write(
                _event_candidate_observation_create(
                    media=media,
                    run=run,
                    step=step,
                    model=model,
                    runtime_config=runtime_config,
                    ball_trajectory_run_id=ball_trajectory_run_id,
                    court_projection_run_id=court_projection_run_id,
                    candidate=candidate,
                    index=index,
                )
            )
        )
    return observations


def _event_candidate_observation_create(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    candidate: EventCandidateDraft,
    index: int,
) -> ObservationCreate:
    current = candidate.trajectory_context.current
    is_hit = candidate.observation_type == HIT_CANDIDATE_OBSERVATION_TYPE
    payload = {
        "candidate_type": candidate.observation_type,
        "source_ball_trajectory_run_id": ball_trajectory_run_id,
        "source_ball_trajectory_observation_id": current.trajectory_observation.id,
        "source_court_projection_run_id": court_projection_run_id,
        "source_ball_court_projection_observation_id": (
            current.source_ball_court_projection_observation_id
        ),
        "frame_number": current.frame_number,
        "timestamp_ms": current.timestamp_ms,
        "court_point": {"x": _round(current.court_x), "y": _round(current.court_y)},
        "trajectory_context": _trajectory_context_payload(candidate.trajectory_context),
        "reason_codes": candidate.reason_codes,
        "confidence": candidate.confidence,
        "candidate_method": candidate.candidate_method,
        "classification_priority": "hit_first_when_player_proximate",
        "player_proximity_gate": candidate.player_proximity_gate,
        "candidate_decision": candidate.candidate_decision,
        "coordinate_space": CoordinateSpace.court_template_2d,
        "template_name": COURT_TEMPLATE_NAME,
        "template_version": COURT_TEMPLATE_VERSION,
        "source_label": (
            "hit candidate evidence" if is_hit else "bounce candidate evidence"
        ),
        "evidence_source": "event_candidate",
        "not_ball_truth": True,
        **EVENT_CANDIDATE_WARNINGS,
    }
    if candidate.nearest_player is not None:
        payload["nearest_player"] = _nearest_player_payload(candidate.nearest_player)
        payload["source_player_court_projection_observation_id"] = (
            candidate.nearest_player.player.observation.id
        )
    else:
        payload["nearest_player"] = None
        payload["source_player_court_projection_observation_id"] = None
    if candidate.net_axis_reversal is not None:
        payload["net_axis_reversal"] = candidate.net_axis_reversal
    if candidate.vertical_motion_proxy is not None:
        payload["vertical_motion_proxy"] = candidate.vertical_motion_proxy
    if candidate.speed_reduction is not None:
        payload["speed_reduction"] = candidate.speed_reduction
    lineage = [
        ObservationLineageCreate(
            parent_observation_id=current.trajectory_observation.id,
            relationship_type=RelationshipType.candidate_from_ball_trajectory,
            processing_step_id=step.id,
            payload_jsonb={
                "candidate_type": candidate.observation_type,
                "candidate_method": candidate.candidate_method,
                **EVENT_CANDIDATE_WARNINGS,
            },
        )
    ]
    if current.source_ball_court_projection_observation_id is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=current.source_ball_court_projection_observation_id,
                relationship_type=RelationshipType.candidate_from_ball_court_projection,
                processing_step_id=step.id,
                payload_jsonb={
                    "candidate_type": candidate.observation_type,
                    "candidate_method": candidate.candidate_method,
                    **EVENT_CANDIDATE_WARNINGS,
                },
            )
        )
    if candidate.nearest_player is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=candidate.nearest_player.player.observation.id,
                relationship_type=RelationshipType.candidate_from_main_player_court_projection,
                processing_step_id=step.id,
                payload_jsonb={
                    "candidate_type": candidate.observation_type,
                    "candidate_method": candidate.candidate_method,
                    **EVENT_CANDIDATE_WARNINGS,
                },
            )
        )
    return ObservationCreate(
        media_id=media.id,
        run_id=run.id,
        observation_family=ObservationFamily.event_candidate,
        observation_type=candidate.observation_type,
        granularity=ObservationGranularity.frame,
        frame_start=current.frame_number,
        frame_end=current.frame_number,
        timestamp_start_ms=current.timestamp_ms,
        timestamp_end_ms=current.timestamp_ms,
        confidence=candidate.confidence,
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space=CoordinateSpace.court_template_2d,
        payload_jsonb={
            **payload,
            "processing_step_id": step.id,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
        },
        idempotency_key=(
            f"{run.id}:{candidate.observation_type}:"
            f"{current.trajectory_observation.id}:{current.frame_number}:{index}"
        ),
        lineage=lineage,
    )


def _trajectory_points_from_observation(
    row: Observation,
    *,
    image_points_by_observation_id: dict[str, tuple[float, float]] | None = None,
) -> list[TrajectoryPoint]:
    payload = row.payload_jsonb or {}
    raw_points = payload.get("points")
    if not isinstance(raw_points, list):
        return []
    image_points_by_observation_id = image_points_by_observation_id or {}
    points = []
    for raw_point in raw_points:
        if not isinstance(raw_point, dict):
            continue
        frame_number = _optional_int(raw_point.get("frame_number"))
        timestamp_ms = _optional_int(raw_point.get("timestamp_ms"))
        court_x = _number(raw_point.get("court_x"))
        court_y = _number(raw_point.get("court_y"))
        if frame_number is None or timestamp_ms is None or court_x is None or court_y is None:
            continue
        source_ball_court_projection_observation_id = _string_or_none(
            raw_point.get("source_observation_id")
            or raw_point.get("source_ball_court_projection_observation_id")
        )
        image_point = (
            image_points_by_observation_id.get(
                source_ball_court_projection_observation_id or ""
            )
            or _image_point_tuple(raw_point.get("image_point"))
        )
        points.append(
            TrajectoryPoint(
                trajectory_observation=row,
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                court_x=court_x,
                court_y=court_y,
                source_ball_court_projection_observation_id=(
                    source_ball_court_projection_observation_id
                ),
                source_homography_observation_id=_string_or_none(
                    raw_point.get("source_homography_observation_id")
                ),
                homography_time_delta_ms=_optional_int(
                    raw_point.get("homography_time_delta_ms")
                ),
                homography_carried_forward=bool(
                    raw_point.get("homography_carried_forward")
                ),
                inside_template_bounds=bool(
                    raw_point.get(
                        "inside_template_bounds",
                        0.0 <= court_x <= 1.0 and 0.0 <= court_y <= 1.0,
                    )
                ),
                image_x=image_point[0] if image_point is not None else None,
                image_y=image_point[1] if image_point is not None else None,
            )
        )
    return sorted(points, key=lambda point: (point.timestamp_ms, point.frame_number))


def _player_projection_from_observation(row: Observation) -> PlayerProjection | None:
    payload = row.payload_jsonb or {}
    court_point = payload.get("court_point")
    frame_number = _optional_int(row.frame_start)
    if frame_number is None:
        frame_number = _optional_int(payload.get("frame_number"))
    timestamp_ms = _optional_int(row.timestamp_start_ms)
    if timestamp_ms is None:
        timestamp_ms = _optional_int(payload.get("timestamp_ms"))
    if not isinstance(court_point, dict) or frame_number is None or timestamp_ms is None:
        return None
    court_x = _number(court_point.get("x"))
    court_y = _number(court_point.get("y"))
    if court_x is None or court_y is None:
        return None
    return PlayerProjection(
        observation=row,
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        court_x=court_x,
        court_y=court_y,
        track_candidate_id=_string_or_none(payload.get("track_candidate_id")),
        track_role_candidate=_string_or_none(payload.get("track_role_candidate")),
    )


def _trajectory_context_payload(context: TrajectoryContext) -> dict[str, Any]:
    return {
        "previous_frame": context.previous.frame_number,
        "next_frame": context.next.frame_number,
        "previous_timestamp_ms": context.previous.timestamp_ms,
        "next_timestamp_ms": context.next.timestamp_ms,
        "direction_before_degrees": context.direction_before_degrees,
        "direction_after_degrees": context.direction_after_degrees,
        "direction_delta_degrees": context.direction_delta_degrees,
        "speed_before": context.speed_before,
        "speed_after": context.speed_after,
        "speed_delta_fraction": context.speed_delta_fraction,
    }


def _nearest_player_payload(nearest_player: NearestPlayerContext) -> dict[str, Any]:
    player = nearest_player.player
    return {
        "track_role_candidate": player.track_role_candidate,
        "track_candidate_id": player.track_candidate_id,
        "source_player_court_projection_observation_id": player.observation.id,
        "court_x": _round(player.court_x),
        "court_y": _round(player.court_y),
        "distance_template_units": nearest_player.distance_template_units,
        "time_delta_ms": nearest_player.time_delta_ms,
    }


def _player_proximity_gate_payload(
    *,
    nearest_player: NearestPlayerContext | None,
    threshold: float,
    away_from_player: bool,
) -> dict[str, Any]:
    if nearest_player is None:
        return {
            "nearest_player_found": False,
            "distance_template_units": None,
            "time_delta_ms": None,
            "threshold": threshold,
            "away_from_player": away_from_player,
        }
    return {
        "nearest_player_found": True,
        "distance_template_units": nearest_player.distance_template_units,
        "time_delta_ms": nearest_player.time_delta_ms,
        "threshold": threshold,
        "away_from_player": away_from_player,
    }


def _dedupe_key(candidate: EventCandidateDraft) -> str:
    if candidate.observation_type == BOUNCE_CANDIDATE_OBSERVATION_TYPE:
        return candidate.observation_type
    role = (
        candidate.nearest_player.player.track_role_candidate
        if candidate.nearest_player is not None
        else None
    )
    return f"{candidate.observation_type}:{role or 'unknown'}"


def _inside_or_near_template(point: TrajectoryPoint, margin: float) -> bool:
    return (
        -margin <= point.court_x <= 1.0 + margin
        and -margin <= point.court_y <= 1.0 + margin
    )


def _image_point_tuple(value: Any) -> tuple[float, float] | None:
    if not isinstance(value, dict):
        return None
    x = _number(value.get("x"))
    y = _number(value.get("y"))
    if x is None or y is None:
        return None
    return (x, y)


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "hit-bounce-candidate-evidence",
            ModelRegistry.version == "v0.2",
            ModelRegistry.model_family == "event_candidate",
            ModelRegistry.source == "apps.worker.services.hit_bounce_candidates",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="hit-bounce-candidate-evidence",
        version="v0.2",
        model_family="event_candidate",
        source="apps.worker.services.hit_bounce_candidates",
        metadata_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            "hit_candidate_method": HIT_CANDIDATE_METHOD,
            "bounce_candidate_method": BOUNCE_CANDIDATE_METHOD,
            **EVENT_CANDIDATE_WARNINGS,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    config: HitBounceCandidateConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="hit-bounce-candidate-evidence-config",
        config_version="v0.2",
        payload_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            "source_ball_trajectory_run_id": ball_trajectory_run_id,
            "source_court_projection_run_id": court_projection_run_id,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "coordinate_space": CoordinateSpace.court_template_2d,
            **config.as_dict(),
            **EVENT_CANDIDATE_WARNINGS,
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
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    config: HitBounceCandidateConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            "source_ball_trajectory_run_id": ball_trajectory_run_id,
            "source_court_projection_run_id": court_projection_run_id,
            "evidence_source": "event_candidate",
            "source_label": "hit/bounce candidate evidence",
            **config.as_dict(),
            **EVENT_CANDIDATE_WARNINGS,
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
        step_name="hit_bounce_physics_heuristic_repair_v02",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "candidate_method": EVENT_CANDIDATE_METHOD,
            **EVENT_CANDIDATE_WARNINGS,
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
    candidate_summary: dict[str, Any],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "candidate_method": EVENT_CANDIDATE_METHOD,
        "source_counts": source_counts,
        "output_counts": output_counts,
        "candidate_summary": candidate_summary,
        "hit_candidate_count": output_counts.get(HIT_CANDIDATE_OBSERVATION_TYPE, 0),
        "bounce_candidate_count": output_counts.get(BOUNCE_CANDIDATE_OBSERVATION_TYPE, 0),
        **EVENT_CANDIDATE_WARNINGS,
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
        **EVENT_CANDIDATE_WARNINGS,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        **EVENT_CANDIDATE_WARNINGS,
    }
    session.commit()


def _validate_config(config: HitBounceCandidateConfig) -> dict[str, Any] | None:
    if config.hit_player_distance_max_template <= 0:
        return _failed(
            "invalid_hit_player_distance_max_template",
            "hit_player_distance_max_template must be greater than zero",
        )
    if config.hit_player_review_distance_max_template < config.hit_player_distance_max_template:
        return _failed(
            "invalid_hit_player_review_distance_max_template",
            "hit_player_review_distance_max_template must be greater than or equal to "
            "hit_player_distance_max_template",
        )
    if config.hit_near_player_direction_delta_degrees < 0:
        return _failed(
            "invalid_hit_near_player_direction_delta_degrees",
            "hit_near_player_direction_delta_degrees must be greater than or equal to zero",
        )
    if config.hit_min_net_axis_delta_template <= 0:
        return _failed(
            "invalid_hit_min_net_axis_delta_template",
            "hit_min_net_axis_delta_template must be greater than zero",
        )
    if config.hit_min_speed_delta_fraction < 0:
        return _failed(
            "invalid_hit_min_speed_delta_fraction",
            "hit_min_speed_delta_fraction must be greater than or equal to zero",
        )
    if config.bounce_player_distance_min_template < 0:
        return _failed(
            "invalid_bounce_player_distance_min_template",
            "bounce_player_distance_min_template must be greater than or equal to zero",
        )
    if config.hit_min_direction_delta_degrees < 0:
        return _failed(
            "invalid_hit_min_direction_delta_degrees",
            "hit_min_direction_delta_degrees must be greater than or equal to zero",
        )
    if config.bounce_min_direction_delta_degrees < 0:
        return _failed(
            "invalid_bounce_min_direction_delta_degrees",
            "bounce_min_direction_delta_degrees must be greater than or equal to zero",
        )
    if config.bounce_min_image_y_delta_pixels <= 0:
        return _failed(
            "invalid_bounce_min_image_y_delta_pixels",
            "bounce_min_image_y_delta_pixels must be greater than zero",
        )
    if config.bounce_min_speed_reduction_fraction < 0:
        return _failed(
            "invalid_bounce_min_speed_reduction_fraction",
            "bounce_min_speed_reduction_fraction must be greater than or equal to zero",
        )
    if config.candidate_dedupe_ms < 0:
        return _failed(
            "invalid_candidate_dedupe_ms",
            "candidate_dedupe_ms must be greater than or equal to zero",
        )
    return None


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(EVENT_CANDIDATE_WARNINGS),
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
