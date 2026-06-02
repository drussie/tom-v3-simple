from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_storage.media_indexer import MediaIndexingError

from apps.worker.services.media_indexer import index_media

SECOND_POINT_SMOKE_TYPE = "second_point_ingestion_evidence_replay_smoke"
SECOND_POINT_SMOKE_VERSION = "v0"


def run_second_point_ingestion_smoke(
    *,
    session: Session,
    media_path: str | None,
    run_name: str = "second-point-ingestion-smoke-v0",
    viewer_base_url: str = "http://127.0.0.1:3000",
    storage_root: str | Path = ".data/media",
    copy_to_storage: bool = True,
    manifest_output: str | Path | None = None,
    probe_runner: Any | None = None,
) -> dict[str, Any]:
    warnings = _warnings()
    if media_path is None or not str(media_path).strip():
        return {
            "ok": False,
            "status": "missing_second_point_media_path",
            "message": "SECOND_POINT_MEDIA_PATH or --media-path is required.",
            "smoke_type": SECOND_POINT_SMOKE_TYPE,
            "smoke_version": SECOND_POINT_SMOKE_VERSION,
            "warnings": warnings,
        }

    source_path = Path(str(media_path)).expanduser()
    if not source_path.is_file():
        return {
            "ok": False,
            "status": "second_point_media_path_not_found",
            "message": f"second point media file not found: {source_path}",
            "smoke_type": SECOND_POINT_SMOKE_TYPE,
            "smoke_version": SECOND_POINT_SMOKE_VERSION,
            "source_media_path": str(source_path),
            "warnings": warnings,
        }

    try:
        media = index_media(
            session=session,
            source_path=source_path,
            copy_to_storage=copy_to_storage,
            media_name=run_name,
            storage_root=storage_root,
            probe_runner=probe_runner,
        )
    except MediaIndexingError as error:
        return {
            "ok": False,
            "status": "second_point_media_indexing_failed",
            "message": str(error),
            "smoke_type": SECOND_POINT_SMOKE_TYPE,
            "smoke_version": SECOND_POINT_SMOKE_VERSION,
            "source_media_path": str(source_path),
            "warnings": warnings,
        }

    replay_url = f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "smoke_type": SECOND_POINT_SMOKE_TYPE,
        "smoke_version": SECOND_POINT_SMOKE_VERSION,
        "run_name": run_name,
        "media_id": media.id,
        "source_media_path": str(source_path.resolve()),
        "source_uri": media.source_uri,
        "stored_uri": (media.metadata_jsonb or {}).get("stored_uri"),
        "stored_path": (media.metadata_jsonb or {}).get("stored_path"),
        "storage_mode": (media.metadata_jsonb or {}).get("storage_mode"),
        "checksum": media.checksum,
        "media_metadata": _media_metadata(media),
        "replay_url": replay_url,
        "warnings": warnings,
    }

    if manifest_output is not None and str(manifest_output).strip():
        output_path = Path(manifest_output).expanduser()
        _write_manifest(result, output_path)
        result["manifest_output"] = str(output_path)

    return result


def _media_metadata(media: Any) -> dict[str, Any]:
    return {
        "duration_ms": media.duration_ms or 0,
        "frame_count": media.frame_count or 0,
        "fps": media.fps or 0,
        "width": media.width or 0,
        "height": media.height or 0,
    }


def _write_manifest(result: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "manifest_type": "second_point_ingestion_smoke_manifest",
        "manifest_version": SECOND_POINT_SMOKE_VERSION,
        "media_id": result["media_id"],
        "source_media_path": result["source_media_path"],
        "replay_url": result["replay_url"],
        "smoke_only": True,
        "not_truth": True,
        "not_generalization_claim": True,
        "warnings": result["warnings"],
    }
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _warnings() -> dict[str, bool]:
    return {
        "second_point_smoke_only": True,
        "candidate_only": True,
        "observation_only": True,
        "not_truth": True,
        "not_generalization_claim": True,
        "does_not_change_sample_point": True,
        "does_not_create_in_out": True,
        "does_not_create_score": True,
        "no_adjudication": True,
    }
