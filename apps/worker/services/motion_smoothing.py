from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import fmean, median
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_schema.skeletons import get_skeleton_definition
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    PoseObservation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
)
from tom_v3_video.time_index import frame_to_timestamp_ms

SMOOTHED_BALL_POSITION_OBSERVATION_TYPE = "smoothed_ball_position_candidate"
SMOOTHED_MAIN_PLAYER_BOX_OBSERVATION_TYPE = "smoothed_main_player_box_candidate"
SMOOTHED_POSE_OBSERVATION_TYPE = "smoothed_pose_candidate"
MOTION_SMOOTHING_OBSERVATION_TYPES = {
    SMOOTHED_BALL_POSITION_OBSERVATION_TYPE,
    SMOOTHED_MAIN_PLAYER_BOX_OBSERVATION_TYPE,
    SMOOTHED_POSE_OBSERVATION_TYPE,
}
MOTION_SMOOTHING_METHOD = "motion_smoothing_stable_replay_candidates_v0"
BALL_SMOOTHING_METHOD = "rolling_median_no_long_gap_interpolation_v0"
PLAYER_BOX_SMOOTHING_METHOD = "exponential_moving_average_bbox_v0"
POSE_SMOOTHING_METHOD = "per_keypoint_ema_v0"
MOTION_SMOOTHING_WARNINGS = {
    "smoothed_candidate_only": True,
    "not_truth": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_bounce_hit_in_out_score": True,
    "no_ball_player_court_projection": True,
    "raw_observations_not_mutated": True,
}


class MotionSmoothingError(ValueError):
    pass


@dataclass(frozen=True)
class MotionSmoothingConfig:
    ball_window_frames: int = 5
    ball_max_gap_frames: int = 3
    player_box_alpha: float = 0.35
    player_box_max_gap_frames: int = 5
    pose_alpha: float = 0.4
    pose_max_gap_frames: int = 5
    min_keypoint_confidence: float | None = None

    def as_dict(self) -> dict[str, float | int | None]:
        return {
            "ball_window_frames": self.ball_window_frames,
            "ball_max_gap_frames": self.ball_max_gap_frames,
            "player_box_alpha": self.player_box_alpha,
            "player_box_max_gap_frames": self.player_box_max_gap_frames,
            "pose_alpha": self.pose_alpha,
            "pose_max_gap_frames": self.pose_max_gap_frames,
            "min_keypoint_confidence": self.min_keypoint_confidence,
        }


@dataclass(frozen=True)
class BallSourcePoint:
    frame_number: int
    timestamp_ms: int
    x: float
    y: float
    width: float | None
    height: float | None
    confidence: float | None
    source_observation_id: str | None
    source_observation_type: str | None
    source_track_point_id: str | None = None
    source_tracklet_id: str | None = None


@dataclass(frozen=True)
class SmoothedBallPoint:
    source: BallSourcePoint
    x: float
    y: float
    width: float | None
    height: float | None
    confidence: float | None
    source_observation_ids: list[str]


@dataclass(frozen=True)
class PlayerBoxSource:
    observation: Observation
    frame_number: int
    timestamp_ms: int
    bbox: dict[str, float]
    track_candidate_id: str | None
    track_role_candidate: str | None
    assignment_score: float | None


@dataclass(frozen=True)
class SmoothedPlayerBox:
    source: PlayerBoxSource
    bbox: dict[str, float]
    confidence: float | None


@dataclass(frozen=True)
class PoseSource:
    row: PoseObservation
    frame_number: int
    timestamp_ms: int
    keypoints: list[dict[str, Any]]
    subject_context: dict[str, Any]


@dataclass(frozen=True)
class SmoothedPose:
    source: PoseSource
    keypoints: list[dict[str, Any]]
    pose_confidence: float | None


def build_motion_smoothing_plan(
    *,
    media_id: str = "<media_id>",
    detection_run_id: str | None = "<detection_run_id>",
    tracklet_run_id: str | None = "<tracklet_run_id>",
    main_player_track_run_id: str | None = "<main_player_track_run_id>",
    pose_run_id: str | None = "<pose_run_id>",
    run_name: str = "motion-smoothing-stable-replay-candidates-v0",
    viewer_base_url: str = "http://127.0.0.1:3000",
    config: MotionSmoothingConfig | None = None,
) -> dict[str, Any]:
    resolved_config = config or MotionSmoothingConfig()
    command = [
        "python -m apps.worker.cli smooth-motion-candidates",
        f"--media-id {media_id}",
        f"--run-name {run_name}",
    ]
    if detection_run_id:
        command.append(f"--detection-run-id {detection_run_id}")
    if tracklet_run_id:
        command.append(f"--tracklet-run-id {tracklet_run_id}")
    if main_player_track_run_id:
        command.append(f"--main-player-track-run-id {main_player_track_run_id}")
    if pose_run_id:
        command.append(f"--pose-run-id {pose_run_id}")
    return {
        "steps": [
            "validate_media_and_source_runs",
            "smooth_ball_track_points_or_detections",
            "smooth_main_player_track_assignment_boxes",
            "smooth_main_track_pose_keypoints",
            "persist_smoothed_candidate_observations",
            "write_source_lineage",
        ],
        "command": " ".join(command),
        "smoothing_method": MOTION_SMOOTHING_METHOD,
        "source_run_ids": {
            "detection_run_id": detection_run_id,
            "tracklet_run_id": tracklet_run_id,
            "main_player_track_run_id": main_player_track_run_id,
            "pose_run_id": pose_run_id,
        },
        "config": resolved_config.as_dict(),
        "replay_url_template": (
            f"{viewer_base_url}/replay/{media_id}?motionSmoothingRunId=<motion_smoothing_run_id>"
        ),
        "warnings": dict(MOTION_SMOOTHING_WARNINGS),
    }


def smooth_motion_candidates(
    *,
    session: Session,
    media_id: str,
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    main_player_track_run_id: str | None = None,
    pose_run_id: str | None = None,
    run_name: str = "motion-smoothing-stable-replay-candidates-v0",
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
    config: MotionSmoothingConfig | None = None,
) -> dict[str, Any]:
    resolved_config = config or MotionSmoothingConfig()
    plan = build_motion_smoothing_plan(
        media_id=media_id,
        detection_run_id=detection_run_id,
        tracklet_run_id=tracklet_run_id,
        main_player_track_run_id=main_player_track_run_id,
        pose_run_id=pose_run_id,
        run_name=run_name,
        viewer_base_url=viewer_base_url,
        config=resolved_config,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "motion smoothing candidate build planned",
            "plan": plan,
            "warnings": dict(MOTION_SMOOTHING_WARNINGS),
        }
    if not any([detection_run_id, tracklet_run_id, main_player_track_run_id, pose_run_id]):
        return _failed("missing_sources", "at least one source run id is required")

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    for label, run_id in (
        ("detection_run_id", detection_run_id),
        ("tracklet_run_id", tracklet_run_id),
        ("main_player_track_run_id", main_player_track_run_id),
        ("pose_run_id", pose_run_id),
    ):
        if run_id is None:
            continue
        run = session.get(ProcessingRun, run_id)
        if run is None:
            return _failed(f"missing_{label}", f"source run not found: {run_id}")
        if run.media_id != media.id:
            return _failed(f"{label}_media_mismatch", f"{label} does not match media_id")

    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_model(session)
        runtime_config = _create_runtime_config(
            session=session,
            detection_run_id=detection_run_id,
            tracklet_run_id=tracklet_run_id,
            main_player_track_run_id=main_player_track_run_id,
            pose_run_id=pose_run_id,
            config=resolved_config,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            run_name=run_name,
            detection_run_id=detection_run_id,
            tracklet_run_id=tracklet_run_id,
            main_player_track_run_id=main_player_track_run_id,
            pose_run_id=pose_run_id,
            config=resolved_config,
        )
        step = _create_step(session=session, run=run, runtime_config=runtime_config)
        writer = ObservationWriter(session)

        ball_sources = _load_ball_sources(
            session=session,
            media=media,
            detection_run_id=detection_run_id,
            tracklet_run_id=tracklet_run_id,
        )
        smoothed_ball = _smooth_ball_sources(ball_sources, resolved_config)
        ball_observations = _persist_smoothed_ball(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            detection_run_id=detection_run_id,
            tracklet_run_id=tracklet_run_id,
            smoothed=smoothed_ball,
            config=resolved_config,
        )

        player_sources = _load_player_box_sources(
            session=session,
            media=media,
            main_player_track_run_id=main_player_track_run_id,
        )
        smoothed_boxes = _smooth_player_boxes(player_sources, resolved_config)
        player_observations = _persist_smoothed_player_boxes(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            main_player_track_run_id=main_player_track_run_id,
            smoothed=smoothed_boxes,
            config=resolved_config,
        )

        pose_sources = _load_pose_sources(
            session=session,
            media=media,
            pose_run_id=pose_run_id,
        )
        smoothed_poses = _smooth_pose_sources(pose_sources, resolved_config)
        pose_observations = _persist_smoothed_poses(
            writer=writer,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            pose_run_id=pose_run_id,
            smoothed=smoothed_poses,
            config=resolved_config,
        )
    except Exception as exc:
        if run is not None and step is not None:
            _mark_failed(session, run, step, str(exc))
        return _failed("failed", str(exc), error_type=exc.__class__.__name__)

    counts = Counter(
        observation.observation_type
        for observation in [*ball_observations, *player_observations, *pose_observations]
    )
    sampled_frames = sorted(
        {
            int(observation.frame_start)
            for observation in [*ball_observations, *player_observations, *pose_observations]
            if observation.frame_start is not None
        }
    )
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_counts={
            "ball_sources": len(ball_sources),
            "main_player_track_assignments": len(player_sources),
            "pose_observations": len(pose_sources),
        },
        output_counts=dict(counts),
        sampled_frames=sampled_frames,
    )
    replay_url = f"{viewer_base_url}/replay/{media.id}?motionSmoothingRunId={run.id}"
    return {
        "ok": True,
        "status": "completed",
        "message": "motion smoothing candidate build complete",
        "motion_smoothing_run_id": run.id,
        "media_id": media.id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "source_run_ids": {
            "detection_run_id": detection_run_id,
            "tracklet_run_id": tracklet_run_id,
            "main_player_track_run_id": main_player_track_run_id,
            "pose_run_id": pose_run_id,
        },
        "observations": {
            SMOOTHED_BALL_POSITION_OBSERVATION_TYPE: counts.get(
                SMOOTHED_BALL_POSITION_OBSERVATION_TYPE, 0
            ),
            SMOOTHED_MAIN_PLAYER_BOX_OBSERVATION_TYPE: counts.get(
                SMOOTHED_MAIN_PLAYER_BOX_OBSERVATION_TYPE, 0
            ),
            SMOOTHED_POSE_OBSERVATION_TYPE: counts.get(SMOOTHED_POSE_OBSERVATION_TYPE, 0),
            "total": sum(counts.values()),
        },
        "source_counts": {
            "ball_sources": len(ball_sources),
            "main_player_track_assignments": len(player_sources),
            "pose_observations": len(pose_sources),
        },
        "sampled_frames": sampled_frames,
        "replay_url": replay_url,
        "warnings": dict(MOTION_SMOOTHING_WARNINGS),
    }


def _register_model(session: Session) -> ModelRegistry:
    existing = session.scalar(
        select(ModelRegistry)
        .where(
            ModelRegistry.name == "motion-smoothing-stable-replay-candidates",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "derived",
            ModelRegistry.source == "apps.worker.services.motion_smoothing",
        )
        .limit(1)
    )
    if existing is not None:
        return existing
    model = ModelRegistry(
        name="motion-smoothing-stable-replay-candidates",
        version="v0",
        model_family="derived",
        source="apps.worker.services.motion_smoothing",
        metadata_jsonb={
            "smoothing_method": MOTION_SMOOTHING_METHOD,
            **MOTION_SMOOTHING_WARNINGS,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    detection_run_id: str | None,
    tracklet_run_id: str | None,
    main_player_track_run_id: str | None,
    pose_run_id: str | None,
    config: MotionSmoothingConfig,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="motion-smoothing-stable-replay-candidates-config",
        config_version="v0",
        payload_jsonb={
            "smoothing_method": MOTION_SMOOTHING_METHOD,
            "source_run_ids": {
                "detection_run_id": detection_run_id,
                "tracklet_run_id": tracklet_run_id,
                "main_player_track_run_id": main_player_track_run_id,
                "pose_run_id": pose_run_id,
            },
            "smoothing_config": config.as_dict(),
            **MOTION_SMOOTHING_WARNINGS,
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
    detection_run_id: str | None,
    tracklet_run_id: str | None,
    main_player_track_run_id: str | None,
    pose_run_id: str | None,
    config: MotionSmoothingConfig,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "smoothing_method": MOTION_SMOOTHING_METHOD,
            "source_detection_run_id": detection_run_id,
            "source_tracklet_run_id": tracklet_run_id,
            "source_main_player_track_run_id": main_player_track_run_id,
            "source_pose_run_id": pose_run_id,
            "smoothing_config": config.as_dict(),
            "evidence_source": "motion_smoothing_candidate",
            "source_label": "motion smoothing stable replay candidates",
            **MOTION_SMOOTHING_WARNINGS,
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
        step_name="motion_smoothing_stable_replay_candidates_v0",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "smoothing_method": MOTION_SMOOTHING_METHOD,
            **MOTION_SMOOTHING_WARNINGS,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _load_ball_sources(
    *,
    session: Session,
    media: MediaAsset,
    detection_run_id: str | None,
    tracklet_run_id: str | None,
) -> list[BallSourcePoint]:
    if tracklet_run_id is not None:
        tracklets = session.scalars(
            select(Tracklet)
            .where(
                Tracklet.media_id == media.id,
                Tracklet.run_id == tracklet_run_id,
                Tracklet.track_family == "ball",
            )
            .order_by(Tracklet.frame_start, Tracklet.id)
        ).all()
        sources: list[BallSourcePoint] = []
        for tracklet in tracklets:
            for point in sorted(tracklet.points, key=lambda row: (row.frame_number, row.id)):
                payload = point.payload_jsonb or {}
                source_observation_id = (
                    point.observation_id
                    or _string_or_none(payload.get("source_detection_observation_id"))
                )
                source_type = None
                if source_observation_id:
                    source = session.get(Observation, source_observation_id)
                    source_type = None if source is None else source.observation_type
                sources.append(
                    BallSourcePoint(
                        frame_number=int(point.frame_number),
                        timestamp_ms=_timestamp_for_frame(
                            media,
                            point.frame_number,
                            point.timestamp_ms,
                        ),
                        x=float(point.x),
                        y=float(point.y),
                        width=_number(point.width),
                        height=_number(point.height),
                        confidence=_number(point.confidence),
                        source_observation_id=source_observation_id,
                        source_observation_type=source_type,
                        source_track_point_id=point.id,
                        source_tracklet_id=tracklet.id,
                    )
                )
        if sources:
            return sorted(
                sources,
                key=lambda point: (point.frame_number, point.source_track_point_id or ""),
            )

    if detection_run_id is None:
        return []
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == detection_run_id,
            Observation.observation_type == "ball_detection",
            Observation.frame_start.is_not(None),
        )
        .order_by(Observation.frame_start, Observation.id)
    ).all()
    sources = []
    for row in rows:
        bbox = _bbox(_merged_payload(row))
        if bbox is None or row.frame_start is None:
            continue
        center_x = bbox["x"] + bbox["w"] / 2.0
        center_y = bbox["y"] + bbox["h"] / 2.0
        sources.append(
            BallSourcePoint(
                frame_number=int(row.frame_start),
                timestamp_ms=_timestamp_for_frame(
                    media,
                    int(row.frame_start),
                    row.timestamp_start_ms,
                ),
                x=center_x,
                y=center_y,
                width=bbox["w"],
                height=bbox["h"],
                confidence=_number(row.confidence),
                source_observation_id=row.id,
                source_observation_type=row.observation_type,
            )
        )
    return sources


def _smooth_ball_sources(
    sources: list[BallSourcePoint],
    config: MotionSmoothingConfig,
) -> list[SmoothedBallPoint]:
    by_track: dict[str, list[BallSourcePoint]] = defaultdict(list)
    for source in sources:
        by_track[source.source_tracklet_id or "ball_detection_fallback"].append(source)

    smoothed: list[SmoothedBallPoint] = []
    half_window = max(0, int(config.ball_window_frames) // 2)
    for group in by_track.values():
        ordered = sorted(group, key=lambda item: item.frame_number)
        for segment in _split_ball_segments(ordered, config):
            for index, source in enumerate(segment):
                start = max(0, index - half_window)
                end = min(len(segment), index + half_window + 1)
                window = segment[start:end]
                source_ids = [
                    item.source_observation_id
                    for item in window
                    if item.source_observation_id is not None
                ]
                widths = [item.width for item in window if item.width is not None]
                heights = [item.height for item in window if item.height is not None]
                confidences = [item.confidence for item in window if item.confidence is not None]
                smoothed.append(
                    SmoothedBallPoint(
                        source=source,
                        x=round(float(median(item.x for item in window)), 6),
                        y=round(float(median(item.y for item in window)), 6),
                        width=round(float(median(widths)), 6) if widths else source.width,
                        height=round(float(median(heights)), 6) if heights else source.height,
                        confidence=(
                            round(fmean(confidences), 6)
                            if confidences
                            else source.confidence
                        ),
                        source_observation_ids=list(dict.fromkeys(source_ids)),
                    )
                )
    return sorted(
        smoothed,
        key=lambda item: (
            item.source.frame_number,
            item.source.source_observation_id or "",
        ),
    )


def _split_ball_segments(
    sources: list[BallSourcePoint],
    config: MotionSmoothingConfig,
) -> list[list[BallSourcePoint]]:
    segments: list[list[BallSourcePoint]] = []
    current: list[BallSourcePoint] = []
    previous_frame: int | None = None
    for source in sources:
        if (
            previous_frame is not None
            and source.frame_number - previous_frame > config.ball_max_gap_frames
        ):
            if current:
                segments.append(current)
            current = []
        current.append(source)
        previous_frame = source.frame_number
    if current:
        segments.append(current)
    return segments


def _load_player_box_sources(
    *,
    session: Session,
    media: MediaAsset,
    main_player_track_run_id: str | None,
) -> list[PlayerBoxSource]:
    if main_player_track_run_id is None:
        return []
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == main_player_track_run_id,
            Observation.observation_type == "main_player_track_assignment_candidate",
            Observation.frame_start.is_not(None),
        )
        .order_by(Observation.frame_start, Observation.id)
    ).all()
    sources = []
    for row in rows:
        payload = row.payload_jsonb or {}
        bbox = _bbox(payload)
        if bbox is None or row.frame_start is None:
            continue
        sources.append(
            PlayerBoxSource(
                observation=row,
                frame_number=int(row.frame_start),
                timestamp_ms=_timestamp_for_frame(
                    media,
                    int(row.frame_start),
                    row.timestamp_start_ms,
                ),
                bbox=bbox,
                track_candidate_id=_string_or_none(payload.get("track_candidate_id")),
                track_role_candidate=_string_or_none(payload.get("track_role_candidate")),
                assignment_score=_number(payload.get("assignment_score") or row.confidence),
            )
        )
    return sources


def _smooth_player_boxes(
    sources: list[PlayerBoxSource],
    config: MotionSmoothingConfig,
) -> list[SmoothedPlayerBox]:
    by_role: dict[str, list[PlayerBoxSource]] = defaultdict(list)
    for source in sources:
        by_role[source.track_role_candidate or "unknown_track_role"].append(source)

    smoothed: list[SmoothedPlayerBox] = []
    for role_sources in by_role.values():
        previous_frame: int | None = None
        previous_bbox: dict[str, float] | None = None
        for source in sorted(
            role_sources,
            key=lambda item: (item.frame_number, item.observation.id),
        ):
            if (
                previous_frame is None
                or source.frame_number - previous_frame > config.player_box_max_gap_frames
                or previous_bbox is None
            ):
                bbox = dict(source.bbox)
            else:
                bbox = _ema_bbox(previous_bbox, source.bbox, config.player_box_alpha)
            smoothed.append(
                SmoothedPlayerBox(
                    source=source,
                    bbox=bbox,
                    confidence=source.assignment_score,
                )
            )
            previous_frame = source.frame_number
            previous_bbox = bbox
    return sorted(smoothed, key=lambda item: (item.source.frame_number, item.source.observation.id))


def _load_pose_sources(
    *,
    session: Session,
    media: MediaAsset,
    pose_run_id: str | None,
) -> list[PoseSource]:
    if pose_run_id is None:
        return []
    rows = session.scalars(
        select(PoseObservation)
        .where(
            PoseObservation.media_id == media.id,
            PoseObservation.run_id == pose_run_id,
        )
        .order_by(PoseObservation.frame_number, PoseObservation.observation_id)
    ).all()
    sources = []
    for row in rows:
        subject_context = dict((row.metadata_jsonb or {}).get("subject_context") or {})
        sources.append(
            PoseSource(
                row=row,
                frame_number=int(row.frame_number),
                timestamp_ms=_timestamp_for_frame(media, row.frame_number, row.timestamp_ms),
                keypoints=list(row.keypoints_jsonb or []),
                subject_context=subject_context,
            )
        )
    return sources


def _smooth_pose_sources(
    sources: list[PoseSource],
    config: MotionSmoothingConfig,
) -> list[SmoothedPose]:
    by_subject: dict[str, list[PoseSource]] = defaultdict(list)
    for source in sources:
        context = source.subject_context
        key = (
            _string_or_none(context.get("track_candidate_id"))
            or _string_or_none(context.get("track_role_candidate"))
            or _string_or_none(context.get("subject_detection_observation_id"))
            or "unknown_pose_subject"
        )
        by_subject[key].append(source)

    smoothed: list[SmoothedPose] = []
    for group in by_subject.values():
        previous_frame: int | None = None
        previous_by_name: dict[str, dict[str, Any]] = {}
        for source in sorted(
            group,
            key=lambda item: (item.frame_number, item.row.observation_id),
        ):
            if (
                previous_frame is None
                or source.frame_number - previous_frame > config.pose_max_gap_frames
            ):
                previous_by_name = {}
            keypoints = _smooth_pose_keypoints(
                current=source.keypoints,
                previous_by_name=previous_by_name,
                alpha=config.pose_alpha,
                min_keypoint_confidence=config.min_keypoint_confidence,
            )
            current_present = {
                str(item.get("name") or item.get("index")): item
                for item in keypoints
                if item.get("present") is True
            }
            previous_by_name = current_present
            previous_frame = source.frame_number
            smoothed.append(
                SmoothedPose(
                    source=source,
                    keypoints=keypoints,
                    pose_confidence=source.row.pose_confidence,
                )
            )
    return sorted(
        smoothed,
        key=lambda item: (item.source.frame_number, item.source.row.observation_id),
    )


def _persist_smoothed_ball(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    detection_run_id: str | None,
    tracklet_run_id: str | None,
    smoothed: list[SmoothedBallPoint],
    config: MotionSmoothingConfig,
) -> list[Any]:
    observations = []
    for index, item in enumerate(smoothed):
        source = item.source
        width = item.width if item.width is not None else 0.0
        height = item.height if item.height is not None else 0.0
        bbox = {
            "x": round(item.x - width / 2.0, 6),
            "y": round(item.y - height / 2.0, 6),
            "w": round(width, 6),
            "h": round(height, 6),
        }
        payload = {
            "source_detection_run_id": detection_run_id,
            "source_tracklet_run_id": tracklet_run_id,
            "source_tracklet_id": source.source_tracklet_id,
            "source_track_point_id": source.source_track_point_id,
            "frame_number": source.frame_number,
            "timestamp_ms": source.timestamp_ms,
            "x": item.x,
            "y": item.y,
            "bbox": bbox,
            "smoothing_method": BALL_SMOOTHING_METHOD,
            "window_frames": config.ball_window_frames,
            "max_gap_frames": config.ball_max_gap_frames,
            "source_observation_ids": item.source_observation_ids,
            "source_observation_id": source.source_observation_id,
            "source_observation_type": source.source_observation_type,
            "smoothed_candidate_only": True,
            "not_ball_truth": True,
            **MOTION_SMOOTHING_WARNINGS,
        }
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family="tracking",
                    observation_type=SMOOTHED_BALL_POSITION_OBSERVATION_TYPE,
                    granularity="frame",
                    frame_start=source.frame_number,
                    frame_end=source.frame_number,
                    timestamp_start_ms=source.timestamp_ms,
                    timestamp_end_ms=source.timestamp_ms,
                    confidence=item.confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space="image_pixels",
                    payload_jsonb=payload,
                    idempotency_key=f"{run.id}:smoothed-ball:{source.frame_number}:{index}",
                    lineage=_lineage_for_sources(
                        source_ids=item.source_observation_ids or [source.source_observation_id],
                        relationship_type=_ball_relationship_type(source),
                        step=step,
                        payload={
                            "smoothing_method": BALL_SMOOTHING_METHOD,
                            "frame_number": source.frame_number,
                            **MOTION_SMOOTHING_WARNINGS,
                        },
                    ),
                )
            )
        )
    return observations


def _persist_smoothed_player_boxes(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    main_player_track_run_id: str | None,
    smoothed: list[SmoothedPlayerBox],
    config: MotionSmoothingConfig,
) -> list[Any]:
    observations = []
    for item in smoothed:
        source = item.source
        payload = {
            "source_main_player_track_run_id": main_player_track_run_id,
            "source_track_assignment_observation_id": source.observation.id,
            "track_candidate_id": source.track_candidate_id,
            "track_role_candidate": source.track_role_candidate,
            "frame_number": source.frame_number,
            "timestamp_ms": source.timestamp_ms,
            "bbox": item.bbox,
            "smoothing_method": PLAYER_BOX_SMOOTHING_METHOD,
            "alpha": config.player_box_alpha,
            "max_gap_frames": config.player_box_max_gap_frames,
            "source_observation_ids": [source.observation.id],
            "smoothed_candidate_only": True,
            "not_identity_truth": True,
            **MOTION_SMOOTHING_WARNINGS,
        }
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family="tracking",
                    observation_type=SMOOTHED_MAIN_PLAYER_BOX_OBSERVATION_TYPE,
                    granularity="frame",
                    frame_start=source.frame_number,
                    frame_end=source.frame_number,
                    timestamp_start_ms=source.timestamp_ms,
                    timestamp_end_ms=source.timestamp_ms,
                    confidence=item.confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space="image_pixels",
                    payload_jsonb=payload,
                    idempotency_key=(
                        f"{run.id}:smoothed-player-box:{source.track_role_candidate}:"
                        f"{source.frame_number}:{source.observation.id}"
                    ),
                    lineage=[
                        ObservationLineageCreate(
                            parent_observation_id=source.observation.id,
                            relationship_type="smoothed_from_main_player_track_assignment",
                            processing_step_id=step.id,
                            payload_jsonb={
                                "smoothing_method": PLAYER_BOX_SMOOTHING_METHOD,
                                "track_candidate_id": source.track_candidate_id,
                                "track_role_candidate": source.track_role_candidate,
                                **MOTION_SMOOTHING_WARNINGS,
                            },
                        )
                    ],
                )
            )
        )
    return observations


def _persist_smoothed_poses(
    *,
    writer: ObservationWriter,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    pose_run_id: str | None,
    smoothed: list[SmoothedPose],
    config: MotionSmoothingConfig,
) -> list[Any]:
    observations = []
    for item in smoothed:
        source = item.source
        context = source.subject_context
        skeleton_format = source.row.skeleton_format
        skeleton_version = source.row.skeleton_version
        payload = {
            "source_pose_run_id": pose_run_id,
            "source_pose_observation_id": source.row.observation_id,
            "source_track_candidate_id": context.get("track_candidate_id"),
            "track_candidate_id": context.get("track_candidate_id"),
            "track_role_candidate": context.get("track_role_candidate"),
            "source_track_run_id": context.get("source_track_run_id"),
            "track_assignment_observation_id": context.get("track_assignment_observation_id"),
            "frame_number": source.frame_number,
            "timestamp_ms": source.timestamp_ms,
            "skeleton_format": skeleton_format,
            "skeleton_version": skeleton_version,
            "keypoints": item.keypoints,
            "edges": [list(edge) for edge in get_skeleton_definition(skeleton_format).edges],
            "bbox": _pose_bbox(source.row),
            "smoothing_method": POSE_SMOOTHING_METHOD,
            "alpha": config.pose_alpha,
            "max_gap_frames": config.pose_max_gap_frames,
            "source_observation_ids": [source.row.observation_id],
            "subject_context": context,
            "smoothed_candidate_only": True,
            "not_pose_truth": True,
            **MOTION_SMOOTHING_WARNINGS,
        }
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family="pose",
                    observation_type=SMOOTHED_POSE_OBSERVATION_TYPE,
                    granularity="frame",
                    frame_start=source.frame_number,
                    frame_end=source.frame_number,
                    timestamp_start_ms=source.timestamp_ms,
                    timestamp_end_ms=source.timestamp_ms,
                    confidence=item.pose_confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space="image_pixels",
                    payload_jsonb=payload,
                    idempotency_key=f"{run.id}:smoothed-pose:{source.row.observation_id}",
                    lineage=[
                        ObservationLineageCreate(
                            parent_observation_id=source.row.observation_id,
                            relationship_type="smoothed_from_pose_observation",
                            processing_step_id=step.id,
                            payload_jsonb={
                                "smoothing_method": POSE_SMOOTHING_METHOD,
                                "track_candidate_id": context.get("track_candidate_id"),
                                "track_role_candidate": context.get("track_role_candidate"),
                                **MOTION_SMOOTHING_WARNINGS,
                            },
                        )
                    ],
                )
            )
        )
    return observations


def _smooth_pose_keypoints(
    *,
    current: list[dict[str, Any]],
    previous_by_name: dict[str, dict[str, Any]],
    alpha: float,
    min_keypoint_confidence: float | None,
) -> list[dict[str, Any]]:
    smoothed: list[dict[str, Any]] = []
    for raw in current:
        item = dict(raw)
        key = str(item.get("name") or item.get("index"))
        present = item.get("present", True) is True
        confidence = _number(item.get("confidence"))
        if min_keypoint_confidence is not None and confidence is not None:
            present = present and confidence >= min_keypoint_confidence
        x = _number(item.get("x"))
        y = _number(item.get("y"))
        previous = previous_by_name.get(key)
        previous_x = _number(previous.get("x")) if previous is not None else None
        previous_y = _number(previous.get("y")) if previous is not None else None
        if (
            present
            and x is not None
            and y is not None
            and previous_x is not None
            and previous_y is not None
        ):
            item["x"] = round(alpha * x + (1.0 - alpha) * previous_x, 6)
            item["y"] = round(alpha * y + (1.0 - alpha) * previous_y, 6)
            item["smoothing_source_count"] = 2
        elif present and x is not None and y is not None:
            item["x"] = x
            item["y"] = y
            item["smoothing_source_count"] = 1
        else:
            item["present"] = False
            item["smoothing_source_count"] = 0
        smoothed.append(item)
    return smoothed


def _lineage_for_sources(
    *,
    source_ids: list[str | None],
    relationship_type: str,
    step: ProcessingStep,
    payload: dict[str, Any],
) -> list[ObservationLineageCreate]:
    lineage: list[ObservationLineageCreate] = []
    for source_id in dict.fromkeys(source_id for source_id in source_ids if source_id):
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=str(source_id),
                relationship_type=relationship_type,
                processing_step_id=step.id,
                payload_jsonb=payload,
            )
        )
    return lineage


def _ball_relationship_type(source: BallSourcePoint) -> str:
    if source.source_observation_type == "track_point_candidate":
        return "smoothed_from_track_point_candidate"
    return "smoothed_from_ball_detection"


def _ema_bbox(
    previous: dict[str, float],
    current: dict[str, float],
    alpha: float,
) -> dict[str, float]:
    previous_center = _bbox_center(previous)
    current_center = _bbox_center(current)
    center_x = alpha * current_center[0] + (1.0 - alpha) * previous_center[0]
    center_y = alpha * current_center[1] + (1.0 - alpha) * previous_center[1]
    width = alpha * current["w"] + (1.0 - alpha) * previous["w"]
    height = alpha * current["h"] + (1.0 - alpha) * previous["h"]
    return {
        "x": round(center_x - width / 2.0, 6),
        "y": round(center_y - height / 2.0, 6),
        "w": round(width, 6),
        "h": round(height, 6),
    }


def _bbox_center(bbox: dict[str, float]) -> tuple[float, float]:
    return bbox["x"] + bbox["w"] / 2.0, bbox["y"] + bbox["h"] / 2.0


def _pose_bbox(row: PoseObservation) -> dict[str, float | None] | None:
    if row.bbox_x is None or row.bbox_y is None or row.bbox_w is None or row.bbox_h is None:
        return None
    return {
        "x": row.bbox_x,
        "y": row.bbox_y,
        "w": row.bbox_w,
        "h": row.bbox_h,
        "confidence": row.bbox_confidence,
    }


def _merged_payload(observation: Observation) -> dict[str, Any]:
    atomic_payload = (
        observation.atomic_detail.payload_jsonb
        if observation.atomic_detail is not None
        else {}
    )
    return {**(observation.payload_jsonb or {}), **atomic_payload}


def _bbox(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if not isinstance(value, dict):
        return None
    x = _number(value.get("x"))
    y = _number(value.get("y"))
    width = _number(value.get("w", value.get("width")))
    height = _number(value.get("h", value.get("height")))
    if x is None or y is None or width is None or height is None or width <= 0 or height <= 0:
        return None
    return {"x": x, "y": y, "w": width, "h": height}


def _timestamp_for_frame(
    media: MediaAsset,
    frame_number: int,
    timestamp_ms: int | None,
) -> int:
    if timestamp_ms is not None:
        return int(timestamp_ms)
    return frame_to_timestamp_ms(media.fps or 30.0, frame_number)


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_counts: dict[str, int],
    output_counts: dict[str, int],
    sampled_frames: list[int],
) -> None:
    now = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "source_counts": source_counts,
        "counts_by_observation_type": output_counts,
        "sampled_frames": sampled_frames,
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "source_counts": source_counts,
        "counts_by_observation_type": output_counts,
        "sampled_frames": sampled_frames,
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
        "warnings": dict(MOTION_SMOOTHING_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
