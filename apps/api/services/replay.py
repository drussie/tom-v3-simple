from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_schema.skeletons import get_skeleton_definition
from tom_v3_storage.db_models import (
    AtomicObservation,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    PoseObservation,
    ProcessingRun,
    Tracklet,
    TrackPoint,
)
from tom_v3_video.paths import local_path_from_uri_or_path

DETECTION_TYPES = {"ball_detection", "player_detection"}
TRACKLET_TYPES = {
    "ball_tracklet_candidate",
    "player_tracklet_candidate",
    "track_point_candidate",
}
POSE_TYPES = {"player_pose_observation"}
GAMEPLAY_TYPES = {"view_state"}


def timestamp_ms_to_replay_frame(media: MediaAsset, timestamp_ms: int | float | None) -> int:
    fps = _positive_float(media.fps)
    frame_count = _positive_int(media.frame_count)
    if fps is None or frame_count is None or timestamp_ms is None:
        return 0
    frame = round((float(timestamp_ms) / 1000.0) * fps)
    return _clamp_frame(frame, frame_count)


def frame_to_replay_timestamp_ms(media: MediaAsset, frame_number: int | float | None) -> int:
    fps = _positive_float(media.fps)
    frame_count = _positive_int(media.frame_count)
    if fps is None or frame_number is None:
        return 0
    frame = int(round(float(frame_number)))
    if frame_count is not None:
        frame = _clamp_frame(frame, frame_count)
    else:
        frame = max(0, frame)
    return int(round((frame / fps) * 1000.0))


def current_time_seconds_to_frame(
    media: MediaAsset,
    current_time_seconds: int | float | None,
) -> int:
    if current_time_seconds is None:
        return 0
    return timestamp_ms_to_replay_frame(media, float(current_time_seconds) * 1000.0)


def build_replay_info(session: Session, media_id: str) -> dict[str, Any] | None:
    media = session.get(MediaAsset, media_id)
    if media is None:
        return None

    frame_time_index = (media.metadata_jsonb or {}).get("frame_time_index")
    return {
        "media_id": media.id,
        "video_url": f"/media/{media.id}/video",
        "source_uri": media.source_uri,
        "width": media.width,
        "height": media.height,
        "duration_ms": media.duration_ms,
        "fps": media.fps,
        "frame_count": media.frame_count,
        "frame_time_mode": "indexed" if media.fps and media.frame_count else "unavailable",
        "frame_time_index": frame_time_index,
        "available_runs": available_runs_for_media(session, media.id),
        "observation_only": True,
        "no_adjudication": True,
    }


def build_replay_overlay_chunk(
    session: Session,
    *,
    media_id: str,
    start_ms: int,
    end_ms: int,
    layers: set[str],
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    pose_run_id: str | None = None,
    min_confidence: float | None = None,
    min_pose_confidence: float | None = None,
) -> dict[str, Any] | None:
    media = session.get(MediaAsset, media_id)
    if media is None:
        return None

    detections = (
        build_detection_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            detection_run_id=detection_run_id,
            min_confidence=min_confidence,
        )
        if "detections" in layers
        else []
    )
    tracklets = (
        build_tracklet_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            tracklet_run_id=tracklet_run_id,
        )
        if "tracklets" in layers
        else []
    )
    poses = (
        build_pose_overlay_items(
            session=session,
            media=media,
            start_ms=start_ms,
            end_ms=end_ms,
            pose_run_id=pose_run_id,
            min_pose_confidence=min_pose_confidence,
        )
        if "pose" in layers
        else []
    )
    return {
        "media_id": media.id,
        "start_ms": start_ms,
        "end_ms": end_ms,
        "coordinate_space": "image_pixels",
        "video_width": media.width,
        "video_height": media.height,
        "detections": detections,
        "tracklets": tracklets,
        "poses": poses,
        "observation_only": True,
        "no_adjudication": True,
    }


def build_replay_timeline(
    session: Session,
    *,
    media_id: str,
    detection_run_id: str | None = None,
    tracklet_run_id: str | None = None,
    pose_run_id: str | None = None,
    include_annotations: bool = True,
) -> dict[str, Any] | None:
    media = session.get(MediaAsset, media_id)
    if media is None:
        return None

    annotation_items: list[dict[str, Any]] = []
    annotations_without_time_count = 0
    if include_annotations:
        annotation_items, annotations_without_time_count = build_annotation_timeline_items(
            session=session,
            media=media,
            selected_run_ids={
                run_id
                for run_id in (detection_run_id, tracklet_run_id, pose_run_id)
                if run_id is not None
            },
        )

    return {
        "media_id": media.id,
        "duration_ms": media.duration_ms,
        "frame_count": media.frame_count,
        "fps": media.fps,
        "observation_only": True,
        "no_adjudication": True,
        "annotations_without_time_count": annotations_without_time_count,
        "lanes": [
            {
                "lane_type": "detections",
                "label": "Detection observations",
                "items": build_detection_timeline_items(
                    session=session,
                    media=media,
                    detection_run_id=detection_run_id,
                ),
            },
            {
                "lane_type": "tracklets",
                "label": "Tracklet candidates",
                "items": build_tracklet_timeline_items(
                    session=session,
                    media=media,
                    tracklet_run_id=tracklet_run_id,
                ),
            },
            {
                "lane_type": "pose",
                "label": "Pose observations",
                "items": build_pose_timeline_items(
                    session=session,
                    media=media,
                    pose_run_id=pose_run_id,
                ),
            },
            {
                "lane_type": "annotations",
                "label": "Review annotations",
                "items": annotation_items,
            },
        ],
    }


def build_detection_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    detection_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.observation_family == "atomic",
            Observation.observation_type.in_(sorted(DETECTION_TYPES)),
        )
        .order_by(Observation.timestamp_start_ms, Observation.frame_start, Observation.id)
    )
    if detection_run_id is not None:
        query = query.where(Observation.run_id == detection_run_id)

    items: list[dict[str, Any]] = []
    for observation in session.scalars(query).all():
        item = detection_timeline_item_from_observation(observation)
        if item is not None:
            items.append(item)
    return items


def detection_timeline_item_from_observation(
    observation: Observation,
) -> dict[str, Any] | None:
    if observation.observation_type not in DETECTION_TYPES:
        return None

    frame_number, timestamp_ms = _observation_frame_time(observation)
    if frame_number is None or timestamp_ms is None:
        return None

    payload = _merged_detection_payload(observation)
    label = _detection_label(observation, payload)
    source_metadata = _detection_source_metadata(observation, payload)
    return {
        "item_type": "detection",
        "observation_id": observation.id,
        "run_id": observation.run_id,
        "timestamp_ms": timestamp_ms,
        "frame_number": frame_number,
        "label": label,
        "observation_type": observation.observation_type,
        "confidence": observation.confidence,
        "display_label": f"{label} detection observation · {source_metadata['source_label']}",
        **source_metadata,
    }


def build_tracklet_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    tracklet_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(Tracklet)
        .where(Tracklet.media_id == media.id)
        .order_by(Tracklet.frame_start, Tracklet.id)
    )
    if tracklet_run_id is not None:
        query = query.where(Tracklet.run_id == tracklet_run_id)

    items: list[dict[str, Any]] = []
    for tracklet in session.scalars(query).all():
        item = tracklet_timeline_item_from_row(media, tracklet)
        if item is not None:
            items.append(item)
    return items


def tracklet_timeline_item_from_row(
    media: MediaAsset,
    tracklet: Tracklet,
) -> dict[str, Any] | None:
    overlay_item = tracklet_overlay_item_from_row(media, tracklet)
    if overlay_item is None:
        return None

    label_hint = overlay_item["label_hint"] or overlay_item["track_type"]
    return {
        "item_type": "tracklet",
        "observation_id": overlay_item["observation_id"],
        "tracklet_id": overlay_item["tracklet_id"],
        "run_id": overlay_item["run_id"],
        "timestamp_start_ms": overlay_item["timestamp_start_ms"],
        "timestamp_end_ms": overlay_item["timestamp_end_ms"],
        "frame_start": overlay_item["frame_start"],
        "frame_end": overlay_item["frame_end"],
        "label_hint": overlay_item["label_hint"],
        "track_type": overlay_item["track_type"],
        "track_status": overlay_item["track_status"],
        "identity_status": overlay_item["identity_status"],
        "track_point_count": len(overlay_item["points"]),
        "display_label": f"{label_hint} tracklet candidate",
        "source_detection_run_id": overlay_item["source_detection_run_id"],
        "source_detection_evidence_source": overlay_item["source_detection_evidence_source"],
        "source_detection_source_label": overlay_item["source_detection_source_label"],
        "source_detection_runtime": overlay_item["source_detection_runtime"],
        "source_detection_real_model_output": overlay_item[
            "source_detection_real_model_output"
        ],
        "is_real_detection_derived": overlay_item["is_real_detection_derived"],
        "candidate_evidence_only": overlay_item["candidate_evidence_only"],
    }


def build_pose_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    pose_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(PoseObservation)
        .where(PoseObservation.media_id == media.id)
        .order_by(PoseObservation.timestamp_ms, PoseObservation.observation_id)
    )
    if pose_run_id is not None:
        query = query.where(PoseObservation.run_id == pose_run_id)

    items: list[dict[str, Any]] = []
    for pose in session.scalars(query).all():
        item = pose_timeline_item_from_row(pose)
        if item is not None:
            items.append(item)
    return items


def pose_timeline_item_from_row(pose: PoseObservation) -> dict[str, Any] | None:
    if pose.frame_number is None or pose.timestamp_ms is None:
        return None

    return {
        "item_type": "pose",
        "observation_id": pose.observation_id,
        "run_id": pose.run_id,
        "timestamp_ms": pose.timestamp_ms,
        "frame_number": pose.frame_number,
        "pose_confidence": pose.pose_confidence,
        "keypoints_present_count": pose.keypoints_present_count,
        "keypoints_missing_count": pose.keypoints_missing_count,
        "display_label": "pose observation",
    }


def build_annotation_timeline_items(
    session: Session,
    *,
    media: MediaAsset,
    selected_run_ids: set[str],
) -> tuple[list[dict[str, Any]], int]:
    annotations = session.scalars(
        select(HumanAnnotation)
        .where(HumanAnnotation.media_id == media.id)
        .order_by(
            HumanAnnotation.timestamp_start_ms,
            HumanAnnotation.frame_start,
            HumanAnnotation.id,
        )
    ).all()

    items: list[dict[str, Any]] = []
    annotations_without_time_count = 0
    for annotation in annotations:
        target = (
            session.get(Observation, annotation.observation_id)
            if annotation.observation_id is not None
            else None
        )
        if selected_run_ids and (target is None or target.run_id not in selected_run_ids):
            continue

        frame_number = (
            annotation.frame_start
            if annotation.frame_start is not None
            else target.frame_start
            if target is not None
            else None
        )
        timestamp_ms = (
            annotation.timestamp_start_ms
            if annotation.timestamp_start_ms is not None
            else target.timestamp_start_ms
            if target is not None
            else None
        )
        if frame_number is None or timestamp_ms is None:
            annotations_without_time_count += 1
            continue

        items.append(
            {
                "item_type": "annotation",
                "annotation_id": annotation.id,
                "target_observation_id": annotation.observation_id,
                "target_observation_type": target.observation_type if target is not None else None,
                "target_run_id": target.run_id if target is not None else None,
                "timestamp_ms": timestamp_ms,
                "frame_number": frame_number,
                "annotation_label": _annotation_label(annotation),
                "created_by": annotation.created_by,
                "display_label": "review annotation",
            }
        )

    items.sort(key=lambda item: (item["timestamp_ms"], item["frame_number"], item["annotation_id"]))
    return items, annotations_without_time_count


def build_detection_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    detection_run_id: str | None = None,
    min_confidence: float | None = None,
) -> list[dict[str, Any]]:
    timestamp_end = func.coalesce(Observation.timestamp_end_ms, Observation.timestamp_start_ms)
    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.observation_family == "atomic",
            Observation.observation_type.in_(sorted(DETECTION_TYPES)),
            Observation.timestamp_start_ms.is_not(None),
            Observation.timestamp_start_ms <= end_ms,
            timestamp_end >= start_ms,
        )
        .order_by(Observation.timestamp_start_ms, Observation.observation_type, Observation.id)
    )
    if detection_run_id is not None:
        query = query.where(Observation.run_id == detection_run_id)
    if min_confidence is not None:
        query = query.where(
            Observation.confidence.is_not(None),
            Observation.confidence >= min_confidence,
        )

    items: list[dict[str, Any]] = []
    for observation in session.scalars(query).all():
        item = detection_overlay_item_from_observation(observation)
        if item is not None:
            items.append(item)
    return items


def detection_overlay_item_from_observation(
    observation: Observation,
) -> dict[str, Any] | None:
    if observation.observation_type not in DETECTION_TYPES:
        return None

    payload = _merged_detection_payload(observation)
    bbox = _bbox_from_payload(payload)
    frame_number = (
        observation.frame_start if observation.frame_start is not None else observation.frame_end
    )
    timestamp_ms = (
        observation.timestamp_start_ms
        if observation.timestamp_start_ms is not None
        else observation.timestamp_end_ms
    )
    if bbox is None or frame_number is None or timestamp_ms is None:
        return None

    source_metadata = _detection_source_metadata(observation, payload)
    return {
        "overlay_type": "detection_bbox",
        "observation_id": observation.id,
        "run_id": observation.run_id,
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "observation_type": observation.observation_type,
        "label": _detection_label(observation, payload),
        "confidence": observation.confidence,
        "bbox": bbox,
        "source_language": "detection observation",
        "source_runtime": _string_or_none(payload.get("source_runtime")),
        "coordinate_space": observation.coordinate_space or "image_pixels",
        "class_id": _optional_int(payload.get("class_id")),
        "class_label": _string_or_none(payload.get("class_label")),
        "frame_time_owner": _string_or_none(payload.get("frame_time_owner")),
        **source_metadata,
    }


def build_tracklet_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    tracklet_run_id: str | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(Tracklet)
        .where(Tracklet.media_id == media.id)
        .order_by(Tracklet.frame_start, Tracklet.id)
    )
    if tracklet_run_id is not None:
        query = query.where(Tracklet.run_id == tracklet_run_id)

    items: list[dict[str, Any]] = []
    for tracklet in session.scalars(query).all():
        item = tracklet_overlay_item_from_row(media, tracklet)
        if item is None:
            continue
        if _time_ranges_overlap(
            item["timestamp_start_ms"],
            item["timestamp_end_ms"],
            start_ms,
            end_ms,
        ):
            items.append(item)
    return items


def tracklet_overlay_item_from_row(
    media: MediaAsset,
    tracklet: Tracklet,
) -> dict[str, Any] | None:
    points = []
    for point in tracklet.points:
        item = point_overlay_item_from_row(media, point)
        if item is not None:
            points.append(item)
    points.sort(
        key=lambda item: (item["timestamp_ms"], item["frame_number"], item["track_point_id"])
    )
    if not points:
        return None

    timestamps = [point["timestamp_ms"] for point in points]
    metadata = tracklet.metadata_jsonb or {}
    observation_id = _string_or_none(tracklet.observation_id)
    source_metadata = _tracklet_source_metadata(metadata)
    return {
        "overlay_type": "tracklet_candidate",
        "observation_id": observation_id,
        "tracklet_id": tracklet.id,
        "run_id": tracklet.run_id,
        "track_type": tracklet.track_family,
        "label_hint": _tracklet_label_hint(tracklet),
        "track_status": _string_or_none(metadata.get("track_status")) or "candidate",
        "identity_status": _string_or_none(metadata.get("identity_status")) or "unverified",
        "frame_start": tracklet.frame_start,
        "frame_end": tracklet.frame_end,
        "timestamp_start_ms": min(timestamps),
        "timestamp_end_ms": max(timestamps),
        "points": points,
        "source_language": "tracklet candidate",
        **source_metadata,
    }


def point_overlay_item_from_row(
    media: MediaAsset,
    point: TrackPoint,
) -> dict[str, Any] | None:
    frame_number = point.frame_number
    timestamp_ms = (
        point.timestamp_ms
        if point.timestamp_ms is not None
        else frame_to_replay_timestamp_ms(media, frame_number)
    )
    x = _numeric(point.x)
    y = _numeric(point.y)
    if frame_number is None or timestamp_ms is None or x is None or y is None:
        return None

    payload = point.payload_jsonb or {}
    bbox = _track_point_bbox(point, payload)
    return {
        "track_point_id": point.id,
        "observation_id": point.observation_id,
        "source_detection_observation_id": _string_or_none(
            payload.get("source_detection_observation_id")
        ),
        "source_detection_run_id": _string_or_none(payload.get("source_detection_run_id")),
        "source_detection_evidence_source": _string_or_none(
            payload.get("source_detection_evidence_source")
        ),
        "source_detection_source_label": _string_or_none(
            payload.get("source_detection_source_label")
        ),
        "source_detection_runtime": _string_or_none(payload.get("source_detection_runtime")),
        "source_detection_real_model_output": _truthy(
            payload.get("source_detection_real_model_output")
        )
        or _truthy(payload.get("source_detection_is_real_model_output")),
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "x": x,
        "y": y,
        "bbox": bbox,
        "confidence": point.confidence,
    }


def build_pose_overlay_items(
    session: Session,
    *,
    media: MediaAsset,
    start_ms: int,
    end_ms: int,
    pose_run_id: str | None = None,
    min_pose_confidence: float | None = None,
) -> list[dict[str, Any]]:
    query = (
        select(PoseObservation)
        .where(
            PoseObservation.media_id == media.id,
            PoseObservation.timestamp_ms.is_not(None),
            PoseObservation.timestamp_ms >= start_ms,
            PoseObservation.timestamp_ms <= end_ms,
        )
        .order_by(PoseObservation.timestamp_ms, PoseObservation.observation_id)
    )
    if pose_run_id is not None:
        query = query.where(PoseObservation.run_id == pose_run_id)
    if min_pose_confidence is not None:
        query = query.where(
            PoseObservation.pose_confidence.is_not(None),
            PoseObservation.pose_confidence >= min_pose_confidence,
        )

    return [pose_overlay_item_from_row(pose) for pose in session.scalars(query).all()]


def pose_overlay_item_from_row(pose: PoseObservation) -> dict[str, Any]:
    keypoints = _pose_overlay_keypoints(pose.keypoints_jsonb or [])
    return {
        "overlay_type": "pose_skeleton",
        "observation_id": pose.observation_id,
        "run_id": pose.run_id,
        "frame_number": pose.frame_number,
        "timestamp_ms": pose.timestamp_ms,
        "skeleton_format": pose.skeleton_format,
        "skeleton_version": pose.skeleton_version,
        "pose_confidence": pose.pose_confidence,
        "bbox": _pose_bbox(pose),
        "keypoint_count": pose.keypoint_count,
        "keypoints_present_count": pose.keypoints_present_count,
        "keypoints_missing_count": pose.keypoints_missing_count,
        "mean_keypoint_confidence": pose.mean_keypoint_confidence,
        "min_keypoint_confidence": pose.min_keypoint_confidence,
        "max_keypoint_confidence": pose.max_keypoint_confidence,
        "keypoints": keypoints,
        "edges": [list(edge) for edge in _pose_edges(pose)],
        "subject_context": {
            "subject_ref_type": pose.subject_ref_type,
            "subject_detection_observation_id": pose.subject_detection_observation_id,
            "subject_tracklet_id": pose.subject_tracklet_id,
            "subject_track_point_id": pose.subject_track_point_id,
            "association_status": pose.association_status,
            "association_method": pose.association_method,
            "association_confidence": pose.association_confidence,
        },
        "source_language": "pose keypoint evidence",
    }


def available_runs_for_media(session: Session, media_id: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "detection": _run_summaries_for_observation_types(session, media_id, DETECTION_TYPES),
        "tracklet": _run_summaries_for_observation_types(session, media_id, TRACKLET_TYPES),
        "pose": _run_summaries_for_observation_types(session, media_id, POSE_TYPES),
        "gameplay": _run_summaries_for_observation_types(session, media_id, GAMEPLAY_TYPES),
    }


def normalize_replay_layers(layers: str | list[str] | tuple[str, ...] | None) -> set[str]:
    if layers is None:
        return {"detections"}
    if isinstance(layers, str):
        raw_layers = layers.split(",")
    else:
        raw_layers = [part for layer in layers for part in str(layer).split(",")]
    normalized: set[str] = set()
    for raw_layer in raw_layers:
        layer = raw_layer.strip().lower()
        if not layer:
            continue
        if layer == "poses":
            layer = "pose"
        if layer == "tracklet":
            layer = "tracklets"
        normalized.add(layer)
    return normalized


def resolve_media_video_path(media: MediaAsset) -> Path | None:
    metadata = media.metadata_jsonb or {}
    candidates = [
        metadata.get("stored_uri"),
        metadata.get("stored_path"),
        media.source_uri,
        metadata.get("original_source_uri"),
        metadata.get("original_source_path"),
    ]
    for candidate in candidates:
        if not isinstance(candidate, str) or not candidate.strip():
            continue
        try:
            path = local_path_from_uri_or_path(candidate)
        except ValueError:
            continue
        if path.is_file():
            return path
    return None


def _run_summaries_for_observation_types(
    session: Session,
    media_id: str,
    observation_types: set[str],
) -> list[dict[str, Any]]:
    counts = dict(
        session.execute(
            select(Observation.run_id, func.count())
            .where(
                Observation.media_id == media_id,
                Observation.observation_type.in_(sorted(observation_types)),
            )
            .group_by(Observation.run_id)
        ).all()
    )
    if not counts:
        return []

    runs = session.scalars(
        select(ProcessingRun)
        .where(ProcessingRun.id.in_(list(counts.keys())))
        .order_by(ProcessingRun.started_at, ProcessingRun.id)
    ).all()
    summaries: list[dict[str, Any]] = []
    for run in runs:
        source_metadata = _run_source_metadata(
            session=session,
            run=run,
            media_id=media_id,
            observation_types=observation_types,
        )
        summaries.append(
            {
                "run_id": run.id,
                "run_name": run.run_name,
                "run_status": run.run_status,
                "created_at": run.started_at.isoformat() if run.started_at else None,
                "completed_at": run.completed_at.isoformat() if run.completed_at else None,
                "observation_count": int(counts.get(run.id, 0)),
                "runtime_config_id": run.runtime_config_id,
                **source_metadata,
            }
        )
    return summaries


def _merged_detection_payload(observation: Observation) -> dict[str, Any]:
    atomic = observation.atomic_detail
    return {
        **(observation.payload_jsonb or {}),
        **(atomic.payload_jsonb if isinstance(atomic, AtomicObservation) else {}),
    }


def _run_source_metadata(
    session: Session,
    run: ProcessingRun,
    media_id: str,
    observation_types: set[str],
) -> dict[str, Any]:
    observation = session.scalar(
        select(Observation)
        .where(
            Observation.media_id == media_id,
            Observation.run_id == run.id,
            Observation.observation_type.in_(sorted(observation_types)),
        )
        .order_by(Observation.created_at, Observation.id)
        .limit(1)
    )
    payload = _merged_detection_payload(observation) if observation is not None else {}
    runtime_payload = run.runtime_config.payload_jsonb if run.runtime_config is not None else {}
    run_metadata = run.metadata_jsonb or {}
    diagnostics = (run.metadata_jsonb or {}).get("diagnostics")
    if not isinstance(diagnostics, dict):
        diagnostics = {}

    tracklet_source_metadata = _tracklet_run_source_metadata(
        run_metadata=run_metadata,
        runtime_payload=runtime_payload,
        payload=payload,
    )
    if tracklet_source_metadata is not None:
        model = (
            session.get(ModelRegistry, observation.model_id)
            if observation and observation.model_id
            else None
        )
        return {
            **tracklet_source_metadata,
            "adapter_name": None,
            "source_runtime": tracklet_source_metadata["source_detection_runtime"],
            "model_name": model.name if model is not None else None,
            "model_version": model.version if model is not None else None,
            "model_registry_id": model.id if model is not None else None,
            "is_real_model_output": False,
            "model_output_not_truth": False,
        }

    model = (
        session.get(ModelRegistry, observation.model_id)
        if observation and observation.model_id
        else None
    )
    source_runtime = (
        _string_or_none(payload.get("source_runtime"))
        or _string_or_none(diagnostics.get("source_runtime"))
        or _string_or_none(runtime_payload.get("source_runtime"))
    )
    adapter_name = (
        _string_or_none(runtime_payload.get("adapter"))
        or _string_or_none((run.metadata_jsonb or {}).get("adapter_name"))
    )
    is_real_model_output = _truthy(payload.get("real_model_output")) or (
        source_runtime == "ultralytics_yolo" and adapter_name in {"yolo", "ultralytics"}
    )
    is_fixture = (
        _string_or_none(runtime_payload.get("adapter")) == "fixture"
        or source_runtime == "fixture"
        or "fixture" in run.run_name.lower()
        or "fixture" in (adapter_name or "").lower()
    )
    evidence_source = (
        "real_model_output"
        if is_real_model_output
        else "fixture_demo"
        if is_fixture
        else "persisted_evidence"
    )
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "adapter_name": adapter_name,
        "source_runtime": source_runtime,
        "model_name": model.name if model is not None else None,
        "model_version": model.version if model is not None else None,
        "model_registry_id": model.id if model is not None else None,
        "is_fixture": is_fixture,
        "is_real_model_output": is_real_model_output,
        "model_output_not_truth": is_real_model_output,
    }


def _detection_source_metadata(
    observation: Observation,
    payload: dict[str, Any],
) -> dict[str, Any]:
    source_runtime = _string_or_none(payload.get("source_runtime"))
    is_real_model_output = _truthy(payload.get("real_model_output")) or (
        source_runtime == "ultralytics_yolo"
    )
    adapter_name = _string_or_none(payload.get("adapter_name")) or ""
    is_fixture = (
        source_runtime == "fixture"
        or _string_or_none(payload.get("adapter_type")) == "fixture"
        or "fixture" in adapter_name.lower()
    )
    evidence_source = (
        "real_model_output"
        if is_real_model_output
        else "fixture_demo"
        if is_fixture
        else "persisted_evidence"
    )
    model = observation.model
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "real_model_output": is_real_model_output,
        "model_output_not_truth": is_real_model_output,
        "model_registry_id": observation.model_id,
        "model_name": model.name if model is not None else None,
        "model_version": model.version if model is not None else None,
        "runtime_config_id": observation.runtime_config_id,
        "is_fixture": is_fixture,
        "is_real_model_output": is_real_model_output,
    }


def _tracklet_run_source_metadata(
    *,
    run_metadata: dict[str, Any],
    runtime_payload: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    source_detection_run_id = (
        _string_or_none(payload.get("source_detection_run_id"))
        or _string_or_none(run_metadata.get("source_detection_run_id"))
        or _string_or_none(runtime_payload.get("source_detection_run_id"))
    )
    if source_detection_run_id is None:
        return None

    source_detection_evidence_source = (
        _string_or_none(payload.get("source_detection_evidence_source"))
        or _string_or_none(run_metadata.get("source_detection_evidence_source"))
        or _string_or_none(runtime_payload.get("source_detection_evidence_source"))
        or "persisted_evidence"
    )
    is_real_detection_derived = (
        source_detection_evidence_source == "real_model_output"
        or _truthy(payload.get("source_detection_real_model_output"))
        or _truthy(run_metadata.get("source_detection_real_model_output"))
        or _truthy(runtime_payload.get("source_detection_real_model_output"))
        or _truthy(payload.get("source_detection_is_real_model_output"))
        or _truthy(run_metadata.get("source_detection_is_real_model_output"))
        or _truthy(runtime_payload.get("source_detection_is_real_model_output"))
    )
    is_fixture = source_detection_evidence_source == "fixture_demo" or _truthy(
        payload.get("source_detection_is_fixture")
    )
    evidence_source = (
        "real_detection_derived_tracklet"
        if is_real_detection_derived
        else "fixture_derived_tracklet"
        if is_fixture
        else "persisted_tracklet"
    )
    return {
        "evidence_source": evidence_source,
        "source_label": _source_label(evidence_source),
        "source_detection_run_id": source_detection_run_id,
        "source_detection_evidence_source": source_detection_evidence_source,
        "source_detection_source_label": _source_label(source_detection_evidence_source),
        "source_detection_runtime": (
            _string_or_none(payload.get("source_detection_runtime"))
            or _string_or_none(run_metadata.get("source_detection_runtime"))
            or _string_or_none(runtime_payload.get("source_detection_runtime"))
        ),
        "is_fixture": is_fixture,
        "is_real_detection_derived": is_real_detection_derived,
    }


def _tracklet_source_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    source_detection_evidence_source = (
        _string_or_none(metadata.get("source_detection_evidence_source"))
        or "persisted_evidence"
    )
    is_real_detection_derived = (
        source_detection_evidence_source == "real_model_output"
        or _truthy(metadata.get("source_detection_real_model_output"))
        or _truthy(metadata.get("source_detection_is_real_model_output"))
        or _truthy(metadata.get("is_real_detection_derived"))
    )
    return {
        "source_detection_run_id": _string_or_none(metadata.get("source_detection_run_id")),
        "source_detection_evidence_source": source_detection_evidence_source,
        "source_detection_source_label": _source_label(source_detection_evidence_source),
        "source_detection_runtime": _string_or_none(metadata.get("source_detection_runtime")),
        "source_detection_real_model_output": is_real_detection_derived,
        "is_real_detection_derived": is_real_detection_derived,
        "candidate_evidence_only": bool(metadata.get("candidate_evidence_only", True)),
    }


def _source_label(evidence_source: str) -> str:
    if evidence_source == "real_model_output":
        return "real model output"
    if evidence_source == "fixture_demo":
        return "fixture evidence"
    if evidence_source == "real_detection_derived_tracklet":
        return "real-detection-derived tracklet candidates"
    if evidence_source == "fixture_derived_tracklet":
        return "fixture-derived tracklet candidates"
    if evidence_source == "persisted_tracklet":
        return "persisted tracklet candidates"
    return "persisted evidence"


def _bbox_from_payload(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if isinstance(value, dict):
        x = _numeric(value.get("x"))
        y = _numeric(value.get("y"))
        width = _numeric(value.get("width", value.get("w")))
        height = _numeric(value.get("height", value.get("h")))
    elif isinstance(value, list | tuple) and len(value) == 4:
        x = _numeric(value[0])
        y = _numeric(value[1])
        width = _numeric(value[2])
        height = _numeric(value[3])
    else:
        return None

    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {"x": x, "y": y, "w": width, "h": height}


def _track_point_bbox(point: TrackPoint, payload: dict[str, Any]) -> dict[str, float] | None:
    payload_bbox = _bbox_from_payload(payload)
    if payload_bbox is not None:
        return payload_bbox

    width = _numeric(point.width)
    height = _numeric(point.height)
    x = _numeric(point.x)
    y = _numeric(point.y)
    if width is None or height is None or x is None or y is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {
        "x": x - width / 2.0,
        "y": y - height / 2.0,
        "w": width,
        "h": height,
    }


def _tracklet_label_hint(tracklet: Tracklet) -> str | None:
    if tracklet.subject_ref:
        return tracklet.subject_ref
    if tracklet.track_family == "ball":
        return "ball"
    if tracklet.track_family == "player":
        return "player_unknown"
    return None


def _pose_bbox(pose: PoseObservation) -> dict[str, float | None] | None:
    x = _numeric(pose.bbox_x)
    y = _numeric(pose.bbox_y)
    width = _numeric(pose.bbox_w)
    height = _numeric(pose.bbox_h)
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {
        "x": x,
        "y": y,
        "w": width,
        "h": height,
        "confidence": pose.bbox_confidence,
    }


def _pose_overlay_keypoints(keypoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for keypoint in keypoints:
        if not isinstance(keypoint, dict):
            continue
        normalized.append(
            {
                "index": keypoint.get("index"),
                "name": keypoint.get("name"),
                "x": keypoint.get("x"),
                "y": keypoint.get("y"),
                "confidence": keypoint.get("confidence"),
                "present": bool(keypoint.get("present")),
            }
        )
    return normalized


def _pose_edges(pose: PoseObservation) -> list[tuple[str, str]]:
    try:
        return list(get_skeleton_definition(pose.skeleton_format, pose.skeleton_version).edges)
    except ValueError:
        return []


def _time_ranges_overlap(
    start_a: int | float | None,
    end_a: int | float | None,
    start_b: int,
    end_b: int,
) -> bool:
    if start_a is None or end_a is None:
        return False
    return float(start_a) <= end_b and float(end_a) >= start_b


def _observation_frame_time(observation: Observation) -> tuple[int | None, int | None]:
    frame_number = (
        observation.frame_start if observation.frame_start is not None else observation.frame_end
    )
    timestamp_ms = (
        observation.timestamp_start_ms
        if observation.timestamp_start_ms is not None
        else observation.timestamp_end_ms
    )
    return frame_number, timestamp_ms


def _detection_label(observation: Observation, payload: dict[str, Any]) -> str:
    for key in ("label", "class_label"):
        value = _string_or_none(payload.get(key))
        if value is not None:
            return value

    detector = payload.get("detector")
    if isinstance(detector, dict):
        detector_label = _string_or_none(detector.get("label"))
        if detector_label is not None:
            return detector_label

    return observation.observation_type.replace("_detection", "")


def _annotation_label(annotation: HumanAnnotation) -> str:
    payload = annotation.payload_jsonb or {}
    label = _string_or_none(payload.get("annotation_label"))
    return label if label is not None else annotation.annotation_type


def _numeric(value: Any) -> float | None:
    if isinstance(value, int | float) and not isinstance(value, bool):
        number = float(value)
        return number if math.isfinite(number) else None
    return None


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _truthy(value: Any) -> bool:
    return value is True or value == "true" or value == 1


def _positive_float(value: float | None) -> float | None:
    if value is None or value <= 0:
        return None
    return float(value)


def _positive_int(value: int | None) -> int | None:
    if value is None or value <= 0:
        return None
    return int(value)


def _clamp_frame(frame: int, frame_count: int) -> int:
    return max(0, min(frame, frame_count - 1))
