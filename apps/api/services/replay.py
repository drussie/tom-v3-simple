from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import MediaAsset, Observation, ProcessingRun
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


def available_runs_for_media(session: Session, media_id: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "detection": _run_summaries_for_observation_types(session, media_id, DETECTION_TYPES),
        "tracklet": _run_summaries_for_observation_types(session, media_id, TRACKLET_TYPES),
        "pose": _run_summaries_for_observation_types(session, media_id, POSE_TYPES),
        "gameplay": _run_summaries_for_observation_types(session, media_id, GAMEPLAY_TYPES),
    }


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
