from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_schema.ids import new_uuid
from tom_v3_video.probe import FfprobeError, VideoProbeResult, probe_video
from tom_v3_video.time_index import build_frame_time_summary

from tom_v3_storage.db_models import MediaAsset
from tom_v3_storage.local_media import LocalMediaStorage, calculate_sha256, resolve_media_file


class MediaIndexingError(ValueError):
    pass


def index_media_file(
    session: Session,
    source_path: str | Path,
    copy_to_storage: bool = True,
    media_name: str | None = None,
    storage_root: str | Path = ".data/media",
    probe_result: VideoProbeResult | None = None,
    probe_runner: Any | None = None,
) -> MediaAsset:
    try:
        source = resolve_media_file(source_path)
        probe = probe_result or probe_video(source, runner=probe_runner)
    except (FileNotFoundError, FfprobeError) as exc:
        raise MediaIndexingError(str(exc)) from exc

    checksum = calculate_sha256(source)
    media_id = new_uuid()
    original_uri = source.as_uri()
    storage = LocalMediaStorage(storage_root)
    stored_media = storage.store_file(source, media_id) if copy_to_storage else None
    stored_uri = stored_media.uri if stored_media is not None else original_uri
    stored_path = str(stored_media.path) if stored_media is not None else str(source)
    frame_time_summary = build_frame_time_summary(
        fps=probe.fps,
        frame_count=probe.frame_count,
        duration_ms=probe.duration_ms,
    )

    media = MediaAsset(
        id=media_id,
        source_uri=stored_uri,
        media_type="video",
        duration_ms=probe.duration_ms,
        frame_count=probe.frame_count,
        fps=probe.fps,
        width=probe.width,
        height=probe.height,
        checksum=checksum,
        metadata_jsonb={
            "media_name": media_name or source.name,
            "original_source_uri": original_uri,
            "original_source_path": str(source),
            "stored_uri": stored_uri,
            "stored_path": stored_path,
            "storage_mode": "copied" if copy_to_storage else "registered",
            "storage_root": str(Path(storage_root).expanduser().resolve()),
            "checksum_algorithm": "sha256",
            "probe": probe.to_metadata(),
            "frame_time_index": frame_time_summary,
        },
    )
    session.add(media)
    session.commit()
    session.refresh(media)
    return media
