from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import fmean
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)

DETECTION_OBSERVATION_TYPES = {"ball_detection", "player_detection"}


class TrackletBuilderError(ValueError):
    pass


@dataclass(frozen=True)
class DetectionSource:
    observation: Observation
    label: str
    bbox: dict[str, float]
    center: dict[str, float]


def build_tracklets_from_detection_run(
    session: Session,
    detection_run_id: str,
    run_name: str = "tracklet-builder-run",
    config_name: str = "tracklet-builder-config",
    config_version: str = "v0",
    max_gap_frames: int = 30,
    max_center_distance_px: float | None = 120.0,
    grouping_method: str = "simple-frame-gap",
    include_ball: bool = True,
    include_players: bool = True,
) -> dict[str, Any]:
    if max_gap_frames < 0:
        raise TrackletBuilderError("max_gap_frames must be greater than or equal to 0")

    detection_run = session.get(ProcessingRun, detection_run_id)
    if detection_run is None:
        raise TrackletBuilderError(f"detection run not found: {detection_run_id}")
    media = session.get(MediaAsset, detection_run.media_id)
    if media is None:
        raise TrackletBuilderError(f"media asset not found: {detection_run.media_id}")

    runtime_config = _create_runtime_config(
        session=session,
        config_name=config_name,
        config_version=config_version,
        detection_run_id=detection_run_id,
        max_gap_frames=max_gap_frames,
        max_center_distance_px=max_center_distance_px,
        grouping_method=grouping_method,
        include_ball=include_ball,
        include_players=include_players,
    )
    model = _get_or_create_model(session)
    run = _create_run(
        session=session,
        media=media,
        runtime_config=runtime_config,
        run_name=run_name,
        detection_run_id=detection_run_id,
        model=model,
    )
    step = _create_step(
        session=session,
        run=run,
        runtime_config=runtime_config,
        detection_run_id=detection_run_id,
        grouping_method=grouping_method,
        max_gap_frames=max_gap_frames,
        max_center_distance_px=max_center_distance_px,
    )

    try:
        detections = _load_detection_sources(session, detection_run_id)
        grouped = _group_detections(
            detections=detections,
            include_ball=include_ball,
            include_players=include_players,
            max_gap_frames=max_gap_frames,
        )
        tracklets = _persist_tracklets(
            session=session,
            media=media,
            run=run,
            model=model,
            runtime_config=runtime_config,
            step=step,
            detections_by_track=grouped,
            source_detection_run_id=detection_run_id,
            grouping_method=grouping_method,
            max_gap_frames=max_gap_frames,
            max_center_distance_px=max_center_distance_px,
        )
    except Exception:
        _mark_failed(session, run, step)
        raise

    _mark_completed(session, run, step, tracklets)
    tracklet_ids = [tracklet.id for tracklet in tracklets]
    track_point_count = sum(len(tracklet.points) for tracklet in tracklets)
    return {
        "media_id": media.id,
        "source_detection_run_id": detection_run_id,
        "tracklet_run_id": run.id,
        "model_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "tracklet_count": len(tracklets),
        "track_point_count": track_point_count,
        "tracklets_by_family": dict(Counter(tracklet.track_family for tracklet in tracklets)),
        "tracklet_ids": tracklet_ids,
    }


def _create_runtime_config(
    session: Session,
    config_name: str,
    config_version: str,
    detection_run_id: str,
    max_gap_frames: int,
    max_center_distance_px: float | None,
    grouping_method: str,
    include_ball: bool,
    include_players: bool,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name=config_name,
        config_version=config_version,
        payload_jsonb={
            "source_detection_run_id": detection_run_id,
            "max_gap_frames": max_gap_frames,
            "max_center_distance_px": max_center_distance_px,
            "grouping_method": grouping_method,
            "include_ball": include_ball,
            "include_players": include_players,
            "track_status": "candidate",
            "identity_status": "unverified",
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _get_or_create_model(session: Session) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == "deterministic-tracklet-builder",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "tracker",
        )
    )
    if model is not None:
        return model

    model = ModelRegistry(
        name="deterministic-tracklet-builder",
        version="v0",
        model_family="tracker",
        source="apps.worker.services.tracklet_builder",
        metadata_jsonb={
            "algorithm_type": "deterministic",
            "track_status": "candidate",
            "identity_status": "unverified",
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_run(
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    detection_run_id: str,
    model: ModelRegistry,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "source_detection_run_id": detection_run_id,
            "source": "worker tracklet builder",
            "model_id": model.id,
            "track_status": "candidate",
            "identity_status": "unverified",
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
    detection_run_id: str,
    grouping_method: str,
    max_gap_frames: int,
    max_center_distance_px: float | None,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="tracklet_candidate_builder",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "source_detection_run_id": detection_run_id,
            "grouping_method": grouping_method,
            "max_gap_frames": max_gap_frames,
            "max_center_distance_px": max_center_distance_px,
            "track_status": "candidate",
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _load_detection_sources(session: Session, detection_run_id: str) -> list[DetectionSource]:
    rows = session.scalars(
        select(Observation)
        .where(
            Observation.run_id == detection_run_id,
            Observation.observation_family == "atomic",
            Observation.observation_type.in_(sorted(DETECTION_OBSERVATION_TYPES)),
            Observation.frame_start.is_not(None),
        )
        .order_by(Observation.observation_type, Observation.frame_start, Observation.id)
    ).all()
    return [source for row in rows if (source := _source_from_observation(row)) is not None]


def _source_from_observation(observation: Observation) -> DetectionSource | None:
    payload = _merged_payload(observation)
    bbox = _bbox(payload)
    if bbox is None:
        return None
    center = _center(payload, bbox)
    return DetectionSource(
        observation=observation,
        label=_label(observation, payload),
        bbox=bbox,
        center=center,
    )


def _group_detections(
    detections: list[DetectionSource],
    include_ball: bool,
    include_players: bool,
    max_gap_frames: int,
) -> dict[tuple[str, str], list[list[DetectionSource]]]:
    by_subject: dict[tuple[str, str], list[DetectionSource]] = defaultdict(list)
    for detection in detections:
        if detection.observation.observation_type == "ball_detection":
            if include_ball:
                by_subject[("ball", "ball")].append(detection)
            continue
        if include_players:
            by_subject[("player", _player_subject(detection.label))].append(detection)

    grouped: dict[tuple[str, str], list[list[DetectionSource]]] = {}
    for subject, subject_detections in by_subject.items():
        sorted_detections = sorted(
            subject_detections,
            key=lambda detection: (
                detection.observation.frame_start or 0,
                detection.observation.id,
            ),
        )
        grouped[subject] = _split_by_frame_gap(sorted_detections, max_gap_frames)
    return grouped


def _split_by_frame_gap(
    detections: list[DetectionSource],
    max_gap_frames: int,
) -> list[list[DetectionSource]]:
    groups: list[list[DetectionSource]] = []
    current: list[DetectionSource] = []
    previous_frame: int | None = None
    for detection in detections:
        frame = detection.observation.frame_start
        if frame is None:
            continue
        if previous_frame is not None and frame - previous_frame > max_gap_frames:
            if current:
                groups.append(current)
            current = []
        current.append(detection)
        previous_frame = frame
    if current:
        groups.append(current)
    return groups


def _persist_tracklets(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    step: ProcessingStep,
    detections_by_track: dict[tuple[str, str], list[list[DetectionSource]]],
    source_detection_run_id: str,
    grouping_method: str,
    max_gap_frames: int,
    max_center_distance_px: float | None,
) -> list[Tracklet]:
    tracklets: list[Tracklet] = []
    for (track_family, subject_ref), groups in detections_by_track.items():
        for group_index, group in enumerate(groups):
            tracklet = _create_tracklet(
                session=session,
                media=media,
                run=run,
                model=model,
                runtime_config=runtime_config,
                track_family=track_family,
                subject_ref=subject_ref,
                group=group,
                group_index=group_index,
                source_detection_run_id=source_detection_run_id,
                grouping_method=grouping_method,
                max_gap_frames=max_gap_frames,
                max_center_distance_px=max_center_distance_px,
            )
            _create_track_points(
                session=session,
                tracklet=tracklet,
                group=group,
                media=media,
                run=run,
                model=model,
                runtime_config=runtime_config,
                step=step,
            )
            tracklets.append(tracklet)
    session.commit()
    for tracklet in tracklets:
        session.refresh(tracklet)
    return tracklets


def _create_tracklet(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    track_family: str,
    subject_ref: str,
    group: list[DetectionSource],
    group_index: int,
    source_detection_run_id: str,
    grouping_method: str,
    max_gap_frames: int,
    max_center_distance_px: float | None,
) -> Tracklet:
    summary = _tracklet_summary(group)
    observation = _create_tracklet_observation(
        session=session,
        media=media,
        run=run,
        model=model,
        runtime_config=runtime_config,
        track_family=track_family,
        subject_ref=subject_ref,
        source_detection_run_id=source_detection_run_id,
        grouping_method=grouping_method,
        max_gap_frames=max_gap_frames,
        max_center_distance_px=max_center_distance_px,
        summary=summary,
    )
    tracklet = Tracklet(
        media_id=media.id,
        run_id=run.id,
        track_family=track_family,
        subject_ref=subject_ref,
        frame_start=summary["frame_start"],
        frame_end=summary["frame_end"],
        confidence=summary["tracklet_confidence"],
        observation_id=observation.id,
        metadata_jsonb={
            "track_status": "candidate",
            "grouping_method": grouping_method,
            "source_detection_run_id": source_detection_run_id,
            "source_observation_count": len(group),
            "track_point_count": len(group),
            "gap_count": summary["gap_count"],
            "max_gap_frames_observed": summary["max_gap_frames_observed"],
            "mean_source_confidence": summary["mean_source_confidence"],
            "min_source_confidence": summary["min_source_confidence"],
            "max_source_confidence": summary["max_source_confidence"],
            "tracklet_confidence": summary["tracklet_confidence"],
            "frame_time_owner": "media_indexing",
            "identity_status": "unverified",
            "group_index": group_index,
            "max_gap_frames": max_gap_frames,
            "max_center_distance_px": max_center_distance_px,
            "viewer_row": _viewer_row(track_family, subject_ref),
            "coverage_segments": [
                {
                    "state": "candidate",
                    "frame_start": summary["frame_start"],
                    "frame_end": summary["frame_end"],
                }
            ]
            if summary["frame_start"] is not None and summary["frame_end"] is not None
            else [],
        },
    )
    session.add(tracklet)
    session.flush()
    return tracklet


def _create_track_points(
    session: Session,
    tracklet: Tracklet,
    group: list[DetectionSource],
    media: MediaAsset,
    run: ProcessingRun,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    step: ProcessingStep,
) -> None:
    points: list[TrackPoint] = []
    for sequence_index, source in enumerate(group):
        observation = source.observation
        frame = observation.frame_start
        if frame is None:
            continue
        point_observation = _create_track_point_observation(
            session=session,
            media=media,
            run=run,
            model=model,
            runtime_config=runtime_config,
            source=source,
            sequence_index=sequence_index,
        )
        points.append(
            TrackPoint(
                tracklet_id=tracklet.id,
                observation_id=point_observation.id,
                frame_number=frame,
                timestamp_ms=observation.timestamp_start_ms,
                x=source.center["x"],
                y=source.center["y"],
                width=source.bbox["width"],
                height=source.bbox["height"],
                confidence=observation.confidence,
                payload_jsonb={
                    "source_detection_observation_id": observation.id,
                    "source_observation_type": observation.observation_type,
                    "source_label": source.label,
                    "bbox": source.bbox,
                    "center": source.center,
                    "source_confidence": observation.confidence,
                    "point_confidence": observation.confidence,
                    "sequence_index": sequence_index,
                    "is_interpolated": False,
                    "frame_time_owner": "media_indexing",
                    "track_status": "candidate",
                    "identity_status": "unverified",
                },
            )
        )
        _create_lineage(
            session=session,
            parent_observation_id=observation.id,
            child_observation_id=point_observation.id,
            relationship_type="tracked_from",
            processing_step_id=step.id,
            payload={
                "frame_number": frame,
                "sequence_index": sequence_index,
                "frame_time_owner": "media_indexing",
            },
        )
        _create_lineage(
            session=session,
            parent_observation_id=point_observation.id,
            child_observation_id=tracklet.observation_id,
            relationship_type="grouped_from",
            processing_step_id=step.id,
            payload={
                "tracklet_id": tracklet.id,
                "sequence_index": sequence_index,
                "frame_time_owner": "media_indexing",
            },
        )
    session.add_all(points)


def _tracklet_summary(group: list[DetectionSource]) -> dict[str, Any]:
    frames = [
        source.observation.frame_start
        for source in group
        if source.observation.frame_start is not None
    ]
    frame_ends = [
        source.observation.frame_end
        if source.observation.frame_end is not None
        else source.observation.frame_start
        for source in group
        if source.observation.frame_start is not None
    ]
    timestamp_starts = [
        source.observation.timestamp_start_ms
        for source in group
        if source.observation.timestamp_start_ms is not None
    ]
    timestamp_ends = [
        source.observation.timestamp_end_ms
        if source.observation.timestamp_end_ms is not None
        else source.observation.timestamp_start_ms
        for source in group
        if source.observation.timestamp_start_ms is not None
    ]
    confidence_values = [
        source.observation.confidence
        for source in group
        if source.observation.confidence is not None
    ]
    sorted_frames = sorted(frames)
    frame_gaps = [
        current_frame - previous_frame
        for previous_frame, current_frame in zip(
            sorted_frames, sorted_frames[1:], strict=False
        )
    ]
    mean_confidence = fmean(confidence_values) if confidence_values else None
    return {
        "source_observation_count": len(group),
        "track_point_count": len(frames),
        "frame_start": min(frames) if frames else None,
        "frame_end": max(frame_ends) if frame_ends else None,
        "timestamp_start_ms": min(timestamp_starts) if timestamp_starts else None,
        "timestamp_end_ms": max(timestamp_ends) if timestamp_ends else None,
        "gap_count": len([gap for gap in frame_gaps if gap > 1]),
        "max_gap_frames_observed": max(frame_gaps) if frame_gaps else 0,
        "mean_source_confidence": mean_confidence,
        "min_source_confidence": min(confidence_values) if confidence_values else None,
        "max_source_confidence": max(confidence_values) if confidence_values else None,
        "tracklet_confidence": mean_confidence,
    }


def _create_tracklet_observation(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    track_family: str,
    subject_ref: str,
    source_detection_run_id: str,
    grouping_method: str,
    max_gap_frames: int,
    max_center_distance_px: float | None,
    summary: dict[str, Any],
) -> Observation:
    observation_type = (
        "ball_tracklet_candidate"
        if track_family == "ball"
        else "player_tracklet_candidate"
    )
    observation = Observation(
        media_id=media.id,
        run_id=run.id,
        observation_family="track",
        observation_type=observation_type,
        granularity="tracklet",
        frame_start=summary["frame_start"],
        frame_end=summary["frame_end"],
        timestamp_start_ms=summary["timestamp_start_ms"],
        timestamp_end_ms=summary["timestamp_end_ms"],
        confidence=summary["tracklet_confidence"],
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space="image_pixels",
        payload_jsonb={
            "track_status": "candidate",
            "identity_status": "unverified",
            "track_family": track_family,
            "subject_ref": subject_ref,
            "grouping_method": grouping_method,
            "source_detection_run_id": source_detection_run_id,
            "source_observation_count": summary.get("source_observation_count", 0),
            "track_point_count": summary.get("track_point_count", 0),
            "gap_count": summary["gap_count"],
            "max_gap_frames_observed": summary["max_gap_frames_observed"],
            "mean_source_confidence": summary["mean_source_confidence"],
            "min_source_confidence": summary["min_source_confidence"],
            "max_source_confidence": summary["max_source_confidence"],
            "tracklet_confidence": summary["tracklet_confidence"],
            "max_gap_frames": max_gap_frames,
            "max_center_distance_px": max_center_distance_px,
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(observation)
    session.flush()
    return observation


def _create_track_point_observation(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    source: DetectionSource,
    sequence_index: int,
) -> Observation:
    source_observation = source.observation
    observation = Observation(
        media_id=media.id,
        run_id=run.id,
        observation_family="track",
        observation_type="track_point_candidate",
        granularity="frame",
        frame_start=source_observation.frame_start,
        frame_end=source_observation.frame_end,
        timestamp_start_ms=source_observation.timestamp_start_ms,
        timestamp_end_ms=source_observation.timestamp_end_ms,
        confidence=source_observation.confidence,
        model_id=model.id,
        runtime_config_id=runtime_config.id,
        coordinate_space="image_pixels",
        payload_jsonb={
            "source_detection_observation_id": source_observation.id,
            "source_observation_type": source_observation.observation_type,
            "source_label": source.label,
            "bbox": source.bbox,
            "center": source.center,
            "source_confidence": source_observation.confidence,
            "point_confidence": source_observation.confidence,
            "sequence_index": sequence_index,
            "is_interpolated": False,
            "frame_time_owner": "media_indexing",
            "track_status": "candidate",
            "identity_status": "unverified",
        },
    )
    session.add(observation)
    session.flush()
    return observation


def _create_lineage(
    session: Session,
    parent_observation_id: str,
    child_observation_id: str | None,
    relationship_type: str,
    processing_step_id: str,
    payload: dict[str, Any],
) -> None:
    if child_observation_id is None:
        raise TrackletBuilderError("child observation id is required for tracklet lineage")
    session.add(
        ObservationLineage(
            parent_observation_id=parent_observation_id,
            child_observation_id=child_observation_id,
            relationship_type=relationship_type,
            processing_step_id=processing_step_id,
            payload_jsonb=payload,
        )
    )


def _mark_completed(
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    tracklets: list[Tracklet],
) -> None:
    now = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "tracklet_count": len(tracklets),
        "track_point_count": sum(len(tracklet.points) for tracklet in tracklets),
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "tracklet_count": len(tracklets),
        "track_point_count": sum(len(tracklet.points) for tracklet in tracklets),
    }
    session.commit()


def _mark_failed(session: Session, run: ProcessingRun, step: ProcessingStep) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    step.step_status = "failed"
    step.completed_at = now
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
    if isinstance(value, dict):
        x = _number(value.get("x"))
        y = _number(value.get("y"))
        width = _number(value.get("width"))
        height = _number(value.get("height"))
        if None not in {x, y, width, height}:
            return {
                "x": float(x),
                "y": float(y),
                "width": float(width),
                "height": float(height),
            }
    if isinstance(value, list | tuple) and len(value) >= 4:
        x = _number(value[0])
        y = _number(value[1])
        width = _number(value[2])
        height = _number(value[3])
        if None not in {x, y, width, height}:
            return {
                "x": float(x),
                "y": float(y),
                "width": float(width),
                "height": float(height),
            }
    return None


def _center(payload: dict[str, Any], bbox: dict[str, float]) -> dict[str, float]:
    value = payload.get("center")
    if isinstance(value, dict):
        x = _number(value.get("x"))
        y = _number(value.get("y"))
        if x is not None and y is not None:
            return {"x": float(x), "y": float(y)}
    if isinstance(value, list | tuple) and len(value) >= 2:
        x = _number(value[0])
        y = _number(value[1])
        if x is not None and y is not None:
            return {"x": float(x), "y": float(y)}
    return {
        "x": bbox["x"] + bbox["width"] / 2,
        "y": bbox["y"] + bbox["height"] / 2,
    }


def _label(observation: Observation, payload: dict[str, Any]) -> str:
    label = payload.get("label")
    if isinstance(label, str) and label:
        return label
    subject_ref = payload.get("subject_ref")
    if isinstance(subject_ref, str) and subject_ref:
        return subject_ref
    detector = payload.get("detector")
    if isinstance(detector, dict):
        detector_label = detector.get("label")
        if isinstance(detector_label, str) and detector_label:
            return detector_label
    class_label = payload.get("class_label")
    if isinstance(class_label, str) and class_label:
        return class_label
    return "ball" if observation.observation_type == "ball_detection" else "player_unknown"


def _player_subject(label: str) -> str:
    if label in {"near_player", "far_player"}:
        return label
    if label in {"player", "player_unknown"}:
        return "player_unknown"
    return "player_unknown"


def _viewer_row(track_family: str, subject_ref: str) -> str:
    if track_family == "ball":
        return "Ball track"
    if subject_ref == "near_player":
        return "Near player"
    if subject_ref == "far_player":
        return "Far player"
    return "Player unknown"


def _number(value: Any) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    return None
