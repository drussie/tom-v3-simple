from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from apps.worker.services.point_manifest import (
    POINT_MANIFEST_OUTPUT_DIR,
    POINT_MANIFEST_TYPE,
    POINT_MANIFEST_VERSION,
    POINT_MANIFEST_WARNINGS,
)

MULTI_POINT_REPLAY_INDEX_TYPE = "multi_point_replay_index"
MULTI_POINT_REPLAY_INDEX_VERSION = "v0"
MULTI_POINT_REPLAY_INDEX_BLUEPRINT = "blueprint_24"
MULTI_POINT_REPLAY_INDEX_BLUEPRINT_NAME = (
    "multi_point_replay_navigation_review_surface_v0"
)
MULTI_POINT_REPLAY_INDEX_OUTPUT = ".data/manifests/multi_point_replay_index.json"
PROTECTED_SAMPLE_POINT_MEDIA_ID = "9518fb01-0da1-4344-9a84-ff88ec8e9b1e"
PROTECTED_SAMPLE_POINT_RUN_IDS = {
    "event_candidate_run_id": "1b946366-7ec1-426f-8b40-494535a9b3fb",
    "trajectory_3d_run_id": "ea76ccab-c51d-4a63-9682-9fd0bbb83f14",
    "camera_geometry_id": "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97",
}

MULTI_POINT_REPLAY_INDEX_WARNINGS = {
    "navigation_only": True,
    "manifest_index_is_not_truth": True,
    "does_not_create_observations": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    **POINT_MANIFEST_WARNINGS,
}

RUN_ID_REPLAY_QUERY_KEYS = {
    "event_candidate_run_id": "eventCandidateRunId",
    "trajectory_3d_run_id": "trajectory3dRunId",
    "camera_geometry_id": "cameraGeometryId",
}


def build_multi_point_replay_index(
    *,
    manifest_root: str | Path = POINT_MANIFEST_OUTPUT_DIR,
    output_path: str | Path | None = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    viewer_base_url: str = "http://127.0.0.1:3000",
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a read-only navigation index over existing point manifests."""

    generated_at = generated_at or datetime.now(UTC)
    root = Path(manifest_root).expanduser()
    points, skipped_manifests = discover_point_manifest_points(
        manifest_root=root,
        viewer_base_url=viewer_base_url,
    )
    index: dict[str, Any] = {
        "index_type": MULTI_POINT_REPLAY_INDEX_TYPE,
        "index_version": MULTI_POINT_REPLAY_INDEX_VERSION,
        "generated_at": generated_at.isoformat(),
        "manifest_roots": [str(root)],
        "point_count": len(points),
        "points": points,
        "skipped_manifest_count": len(skipped_manifests),
        "skipped_manifests": skipped_manifests,
        "tom_provenance": {
            "project": "tom-v3-simple",
            "project_version": "0.0.0",
            "blueprint": MULTI_POINT_REPLAY_INDEX_BLUEPRINT,
            "blueprint_name": MULTI_POINT_REPLAY_INDEX_BLUEPRINT_NAME,
        },
        "warnings": dict(MULTI_POINT_REPLAY_INDEX_WARNINGS),
    }

    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "index_type": MULTI_POINT_REPLAY_INDEX_TYPE,
        "index_version": MULTI_POINT_REPLAY_INDEX_VERSION,
        "point_count": len(points),
        "points": points,
        "skipped_manifest_count": len(skipped_manifests),
        "warnings": dict(MULTI_POINT_REPLAY_INDEX_WARNINGS),
        "index": index,
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")
        result["index_output"] = str(path)
    return result


def discover_point_manifest_points(
    *,
    manifest_root: str | Path = POINT_MANIFEST_OUTPUT_DIR,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    root = Path(manifest_root).expanduser()
    if not root.exists():
        return [], []

    points: list[dict[str, Any]] = []
    skipped_manifests: list[dict[str, str]] = []
    seen_point_keys: set[tuple[str, str, tuple[tuple[str, str], ...]]] = set()
    for path in sorted(root.rglob("*.json")):
        if not path.is_file():
            continue
        payload = _read_json(path)
        if payload is None:
            skipped_manifests.append({"path": str(path), "reason": "invalid_json"})
            continue
        if payload.get("index_type") == MULTI_POINT_REPLAY_INDEX_TYPE:
            continue
        if payload.get("manifest_type") != POINT_MANIFEST_TYPE:
            skipped_manifests.append({"path": str(path), "reason": "not_point_manifest"})
            continue
        if payload.get("manifest_version") != POINT_MANIFEST_VERSION:
            skipped_manifests.append(
                {"path": str(path), "reason": "unsupported_point_manifest_version"}
            )
            continue
        point = _point_from_manifest(
            manifest=payload,
            manifest_path=path,
            viewer_base_url=viewer_base_url,
        )
        if point is None:
            skipped_manifests.append({"path": str(path), "reason": "missing_point_identity"})
            continue
        point_key = _point_identity_key(point)
        if point_key in seen_point_keys:
            skipped_manifests.append({"path": str(path), "reason": "duplicate_point_manifest"})
            continue
        seen_point_keys.add(point_key)
        points.append(point)

    return sorted(points, key=_point_sort_key), skipped_manifests


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _point_from_manifest(
    *,
    manifest: dict[str, Any],
    manifest_path: Path,
    viewer_base_url: str,
) -> dict[str, Any] | None:
    point_manifest_id = _string_or_none(manifest.get("point_manifest_id"))
    media_id = _string_or_none(manifest.get("media_id"))
    if point_manifest_id is None or media_id is None:
        return None

    associated_run_ids = _string_dict(manifest.get("associated_run_ids"))
    profile_counts = _int_dict(manifest.get("profile_counts"))
    evidence_availability = _bool_dict(manifest.get("evidence_availability"))
    warnings = _bool_dict(manifest.get("warnings"))
    labels = _infer_labels(
        manifest=manifest,
        manifest_path=manifest_path,
        associated_run_ids=associated_run_ids,
    )
    return {
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "manifest_path": str(manifest_path),
        "replay_url": _replay_url(
            manifest=manifest,
            media_id=media_id,
            associated_run_ids=associated_run_ids,
            viewer_base_url=viewer_base_url,
        ),
        "source_media_path": _string_or_none(manifest.get("source_media_path")),
        "source_uri": _string_or_none(manifest.get("source_uri")),
        "stored_path": _string_or_none(manifest.get("stored_path")),
        "stored_uri": _string_or_none(manifest.get("stored_uri")),
        "associated_run_ids": associated_run_ids,
        "evidence_availability": evidence_availability,
        "profile_counts": profile_counts,
        "warnings": {**dict(POINT_MANIFEST_WARNINGS), **warnings},
        "labels": labels,
    }


def _replay_url(
    *,
    manifest: dict[str, Any],
    media_id: str,
    associated_run_ids: dict[str, str],
    viewer_base_url: str,
) -> str:
    manifest_replay_url = _string_or_none(manifest.get("replay_url"))
    url = manifest_replay_url or f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for run_id_key, query_key in RUN_ID_REPLAY_QUERY_KEYS.items():
        run_id = associated_run_ids.get(run_id_key)
        if run_id:
            query[query_key] = run_id
    return urlunparse(parsed._replace(query=urlencode(query)))


def _infer_labels(
    *,
    manifest: dict[str, Any],
    manifest_path: Path,
    associated_run_ids: dict[str, str],
) -> list[str]:
    labels: list[str] = []
    media_id = _string_or_none(manifest.get("media_id"))
    protected = media_id == PROTECTED_SAMPLE_POINT_MEDIA_ID or any(
        associated_run_ids.get(key) == value
        for key, value in PROTECTED_SAMPLE_POINT_RUN_IDS.items()
    )
    if protected:
        labels.append("protected_sample_point")

    label_text = _manifest_label_text(manifest, manifest_path)
    second_point_named = any(
        token in label_text
        for token in ("second_point", "second-point", "second point", "secondpoint")
    )
    sample_point_stand_in = (
        not protected
        and ("sample_point.mp4" in label_text or "sample_point" in manifest_path.stem.lower())
    )
    if not protected and (second_point_named or sample_point_stand_in):
        labels.append("second_point_parity_stand_in")
    return labels


def _manifest_label_text(manifest: dict[str, Any], manifest_path: Path) -> str:
    values: list[str] = [str(manifest_path)]
    for key in (
        "source_media_path",
        "source_uri",
        "stored_path",
        "stored_uri",
        "replay_url",
    ):
        value = manifest.get(key)
        if isinstance(value, str):
            values.append(value)
    provenance = manifest.get("tom_provenance")
    if isinstance(provenance, dict):
        values.extend(str(value) for value in provenance.values())
    return " ".join(values).lower()


def _point_sort_key(point: dict[str, Any]) -> tuple[int, str, str]:
    labels = point.get("labels")
    label_set = set(labels) if isinstance(labels, list) else set()
    if "protected_sample_point" in label_set:
        priority = 0
    elif "second_point_parity_stand_in" in label_set:
        priority = 1
    else:
        priority = 2
    return (
        priority,
        str(point.get("media_id") or ""),
        str(point.get("point_manifest_id") or ""),
    )


def _point_identity_key(point: dict[str, Any]) -> tuple[str, str, tuple[tuple[str, str], ...]]:
    associated_run_ids = point.get("associated_run_ids")
    run_items = (
        tuple(sorted(associated_run_ids.items()))
        if isinstance(associated_run_ids, dict)
        else ()
    )
    return (
        str(point.get("point_manifest_id") or ""),
        str(point.get("media_id") or ""),
        run_items,
    )


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _string_dict(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): item
        for key, item in value.items()
        if isinstance(item, str) and item
    }


def _bool_dict(value: object) -> dict[str, bool]:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items() if isinstance(item, bool)}


def _int_dict(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    counts: dict[str, int] = {}
    for key, item in value.items():
        if isinstance(item, bool):
            continue
        if isinstance(item, int):
            counts[str(key)] = item
    return counts
