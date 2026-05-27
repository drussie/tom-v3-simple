from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import AtomicObservation, MediaAsset, Observation, ProcessingRun
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
    min_confidence: float | None = None,
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
    return {
        "media_id": media.id,
        "start_ms": start_ms,
        "end_ms": end_ms,
        "coordinate_space": "image_pixels",
        "video_width": media.width,
        "video_height": media.height,
        "detections": detections,
        "tracklets": [],
        "poses": [],
        "observation_only": True,
        "no_adjudication": True,
    }


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
    return {layer.strip().lower() for layer in raw_layers if layer.strip()}


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
    return [
        {
            "run_id": run.id,
            "run_name": run.run_name,
            "run_status": run.run_status,
            "created_at": run.started_at.isoformat() if run.started_at else None,
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            "observation_count": int(counts.get(run.id, 0)),
        }
        for run in runs
    ]


def _merged_detection_payload(observation: Observation) -> dict[str, Any]:
    atomic = observation.atomic_detail
    return {
        **(observation.payload_jsonb or {}),
        **(atomic.payload_jsonb if isinstance(atomic, AtomicObservation) else {}),
    }


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


def _numeric(value: Any) -> float | None:
    if isinstance(value, int | float) and not isinstance(value, bool):
        number = float(value)
        return number if math.isfinite(number) else None
    return None


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


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
