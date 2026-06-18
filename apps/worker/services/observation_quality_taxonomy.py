from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_OUTPUT,
    MULTI_POINT_REPLAY_INDEX_TYPE,
    MULTI_POINT_REPLAY_INDEX_VERSION,
)

OBSERVATION_QUALITY_TAXONOMY_TYPE = "observation_quality_taxonomy"
OBSERVATION_QUALITY_TAXONOMY_VERSION = "v1"
OBSERVATION_QUALITY_PROFILE_TYPE = "observation_quality_profile"
OBSERVATION_QUALITY_PROFILE_VERSION = "v1"
OBSERVATION_QUALITY_BLUEPRINT = "blueprint_26"
OBSERVATION_QUALITY_BLUEPRINT_NAME = "observation_quality_taxonomy_v1"
DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT = (
    ".data/contracts/observation_quality_taxonomy_v1.json"
)
DEFAULT_OBSERVATION_QUALITY_PROFILE_OUTPUT = (
    ".data/exports/observation_quality_profile.current.json"
)

OBSERVATION_QUALITY_WARNINGS = {
    "taxonomy_is_not_truth": True,
    "observation_quality_is_not_adjudication": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_observations": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
    "observation_only": True,
    "review_support_only": True,
    "no_adjudication": True,
}

DIMENSION_WARNINGS = {
    "dimension_is_not_truth": True,
    "observation_quality_is_not_adjudication": True,
    "review_support_only": True,
    "no_adjudication": True,
}

QUALITY_ALLOWED_VALUES = (
    "unknown",
    "unavailable",
    "low",
    "medium",
    "high",
    "mixed",
    "not_applicable",
    "clear",
    "partially_obscured",
    "heavily_obscured",
    "sufficient_for_review",
    "insufficient_for_review",
    "needs_human_review",
)

VISUAL_QUALITY_DIMENSIONS = (
    "media_quality",
    "camera_stability",
    "court_visibility",
    "ball_visibility",
    "player_visibility",
    "occlusion",
    "motion_blur",
    "lighting",
    "frame_continuity",
)

QUALITY_DIMENSION_SPECS = (
    {
        "key": "media_quality",
        "name": "Media quality",
        "description": "Review-support description of source media condition when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "camera_stability",
        "name": "Camera stability",
        "description": "Review-support description of apparent camera steadiness when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "court_visibility",
        "name": "Court visibility",
        "description": "Review-support description of court visibility when known.",
        "applies_to": ["media", "replay", "review", "camera_geometry"],
    },
    {
        "key": "ball_visibility",
        "name": "Ball visibility",
        "description": "Review-support description of ball visibility when known.",
        "applies_to": ["media", "replay", "event_candidates", "trajectory_3d"],
    },
    {
        "key": "player_visibility",
        "name": "Player visibility",
        "description": "Review-support description of player visibility when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "occlusion",
        "name": "Occlusion",
        "description": "Review-support description of visual obstruction when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "motion_blur",
        "name": "Motion blur",
        "description": "Review-support description of motion blur when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "lighting",
        "name": "Lighting",
        "description": "Review-support description of lighting condition when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "frame_continuity",
        "name": "Frame continuity",
        "description": "Review-support description of frame continuity when known.",
        "applies_to": ["media", "replay", "review"],
    },
    {
        "key": "replay_context_completeness",
        "name": "Replay context completeness",
        "description": "Whether existing artifacts provide enough replay context for review.",
        "applies_to": ["point_manifest", "multi_point_replay_index", "review"],
    },
    {
        "key": "evidence_completeness",
        "name": "Evidence completeness",
        "description": "Availability summary for existing evidence categories only.",
        "applies_to": ["point_manifest", "multi_point_replay_index", "review"],
    },
    {
        "key": "calibration_readiness",
        "name": "Calibration readiness",
        "description": "Availability summary for existing camera geometry context only.",
        "applies_to": ["camera_geometry", "trajectory_3d", "review"],
    },
    {
        "key": "trajectory_3d_readiness",
        "name": "3D trajectory readiness",
        "description": "Availability summary for existing 3D trajectory context only.",
        "applies_to": ["trajectory_3d", "review"],
    },
    {
        "key": "review_readiness",
        "name": "Review readiness",
        "description": "Whether existing replay and evidence context can support human review.",
        "applies_to": ["replay", "review", "review_annotations"],
    },
    {
        "key": "annotation_readiness",
        "name": "Annotation readiness",
        "description": "Availability summary for existing review annotation context only.",
        "applies_to": ["review_annotations", "review"],
    },
    {
        "key": "provenance_completeness",
        "name": "Provenance completeness",
        "description": "Whether existing artifacts carry point, media, manifest, and run context.",
        "applies_to": ["point_manifest", "multi_point_replay_index", "exports"],
    },
)


def export_observation_quality_taxonomy(
    *,
    output_path: str | Path | None = DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the versioned observation-quality vocabulary without reading evidence."""

    exported_at = exported_at or datetime.now(UTC)
    taxonomy = {
        "taxonomy_type": OBSERVATION_QUALITY_TAXONOMY_TYPE,
        "taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "exported_at": exported_at.isoformat(),
        "dimensions": [_taxonomy_dimension(spec) for spec in QUALITY_DIMENSION_SPECS],
        "tom_provenance": _tom_provenance(),
        "warnings": dict(OBSERVATION_QUALITY_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "taxonomy_type": OBSERVATION_QUALITY_TAXONOMY_TYPE,
        "taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "dimension_count": len(taxonomy["dimensions"]),
        "taxonomy": taxonomy,
        "warnings": dict(OBSERVATION_QUALITY_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(taxonomy, indent=2, sort_keys=True), encoding="utf-8")
        result["taxonomy_output"] = str(path)
    return result


def build_observation_quality_profile(
    *,
    source_index_path: str | Path = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    output_path: str | Path | None = DEFAULT_OBSERVATION_QUALITY_PROFILE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a conservative observation-quality profile from an existing replay index."""

    loaded_index = _load_json(source_index_path, label="source_index")
    if loaded_index.get("ok") is False:
        return loaded_index
    source_index = _dict(loaded_index["data"])
    validation = _validate_source_index(source_index)
    if validation is not None:
        return validation

    generated_at = generated_at or datetime.now(UTC)
    points = [
        _profile_point_from_index_point(point)
        for point in _list(source_index.get("points"))
        if isinstance(point, dict)
    ]
    summary = _profile_summary(points)
    profile = {
        "profile_type": OBSERVATION_QUALITY_PROFILE_TYPE,
        "profile_version": OBSERVATION_QUALITY_PROFILE_VERSION,
        "generated_at": generated_at.isoformat(),
        "taxonomy_type": OBSERVATION_QUALITY_TAXONOMY_TYPE,
        "taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "source_index_path": str(Path(source_index_path)),
        "source_index_type": source_index.get("index_type"),
        "source_index_version": source_index.get("index_version"),
        "source_index_generated_at": source_index.get("generated_at"),
        "point_count": len(points),
        "points": points,
        "summary": summary,
        "tom_provenance": _tom_provenance(),
        "warnings": dict(OBSERVATION_QUALITY_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "profile_type": OBSERVATION_QUALITY_PROFILE_TYPE,
        "profile_version": OBSERVATION_QUALITY_PROFILE_VERSION,
        "source_index_path": str(Path(source_index_path)),
        "point_count": len(points),
        "summary": summary,
        "profile": profile,
        "warnings": dict(OBSERVATION_QUALITY_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profile, indent=2, sort_keys=True), encoding="utf-8")
        result["profile_output"] = str(path)
    return result


def _taxonomy_dimension(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": spec["key"],
        "name": spec["name"],
        "description": spec["description"],
        "allowed_values": list(QUALITY_ALLOWED_VALUES),
        "default_value": "unknown",
        "applies_to": list(spec["applies_to"]),
        "warnings": dict(DIMENSION_WARNINGS),
    }


def _profile_point_from_index_point(point: dict[str, Any]) -> dict[str, Any]:
    availability = _bool_dict(point.get("evidence_availability"))
    counts = _int_dict(point.get("profile_counts"))
    run_ids = _string_dict(point.get("associated_run_ids"))
    return {
        "point_manifest_id": _string_or_none(point.get("point_manifest_id")),
        "media_id": _string_or_none(point.get("media_id")),
        "labels": sorted(_string_list(point.get("labels"))),
        "manifest_path": _string_or_none(point.get("manifest_path")),
        "replay_url": _string_or_none(point.get("replay_url")),
        "source_media_path": _string_or_none(point.get("source_media_path")),
        "source_uri": _string_or_none(point.get("source_uri")),
        "stored_path": _string_or_none(point.get("stored_path")),
        "stored_uri": _string_or_none(point.get("stored_uri")),
        "associated_run_ids": run_ids,
        "evidence_availability": availability,
        "profile_counts": counts,
        "quality_dimensions": _quality_dimensions_for_point(
            point=point,
            availability=availability,
            counts=counts,
            run_ids=run_ids,
        ),
        "warnings": {
            **dict(OBSERVATION_QUALITY_WARNINGS),
            **_bool_dict(point.get("warnings")),
            "quality_profile_is_not_truth": True,
            "visual_quality_requires_human_review": True,
        },
    }


def _quality_dimensions_for_point(
    *,
    point: dict[str, Any],
    availability: dict[str, bool],
    counts: dict[str, int],
    run_ids: dict[str, str],
) -> list[dict[str, Any]]:
    dimensions: list[dict[str, Any]] = []
    has_media_context = _has_media_context(point=point, availability=availability)
    for key in VISUAL_QUALITY_DIMENSIONS:
        dimensions.append(
            _dimension_profile(
                key,
                value="unknown" if has_media_context else "unavailable",
                reason=(
                    "Existing artifacts identify media or replay context, but this profile "
                    "does not inspect video content."
                    if has_media_context
                    else "The source index does not report media or replay context."
                ),
                source="source_index.evidence_availability",
                requires_human_review=True,
            )
        )

    replay_url = _string_or_none(point.get("replay_url"))
    media_id = _string_or_none(point.get("media_id"))
    dimensions.append(
        _dimension_profile(
            "replay_context_completeness",
            value=(
                "sufficient_for_review"
                if replay_url is not None and media_id is not None
                else "unavailable"
            ),
            reason=(
                "The source index provides a replay URL and media id."
                if replay_url is not None and media_id is not None
                else "The source index does not provide replay context."
            ),
            source="source_index.replay_url",
            requires_human_review=replay_url is None or media_id is None,
        )
    )

    has_any_evidence = any(availability.values()) or any(count > 0 for count in counts.values())
    dimensions.append(
        _dimension_profile(
            "evidence_completeness",
            value="mixed" if has_any_evidence else "unavailable",
            reason=(
                "The source index reports one or more existing evidence categories."
                if has_any_evidence
                else "The source index does not report existing evidence categories."
            ),
            source="source_index.evidence_availability",
            requires_human_review=True,
        )
    )

    has_calibration_context = bool(run_ids.get("camera_geometry_id")) or availability.get(
        "event_candidate_3d_diagnostics_available"
    )
    dimensions.append(
        _dimension_profile(
            "calibration_readiness",
            value="unknown" if has_calibration_context else "unavailable",
            reason=(
                "Existing artifacts report camera geometry or 3D diagnostic context; "
                "readiness quality is not inferred."
                if has_calibration_context
                else "Existing artifacts do not report camera geometry context."
            ),
            source="source_index.associated_run_ids",
            requires_human_review=True,
        )
    )

    has_trajectory_context = bool(run_ids.get("trajectory_3d_run_id")) or availability.get(
        "trajectory_3d_candidates_available"
    )
    dimensions.append(
        _dimension_profile(
            "trajectory_3d_readiness",
            value="unknown" if has_trajectory_context else "unavailable",
            reason=(
                "Existing artifacts report 3D trajectory context; readiness quality is not "
                "inferred."
                if has_trajectory_context
                else "Existing artifacts do not report 3D trajectory context."
            ),
            source="source_index.associated_run_ids",
            requires_human_review=True,
        )
    )

    review_ready = replay_url is not None and has_any_evidence
    dimensions.append(
        _dimension_profile(
            "review_readiness",
            value="needs_human_review" if review_ready else "unavailable",
            reason=(
                "Existing replay and evidence context can support human review."
                if review_ready
                else "Existing artifacts do not provide replay plus evidence context."
            ),
            source="source_index.replay_url",
            requires_human_review=True,
        )
    )

    has_annotation_context = (
        availability.get("review_annotations_available") is True
        or availability.get("trajectory_3d_debug_reviews_available") is True
        or counts.get("event_marker_review_count", 0) > 0
        or counts.get("trajectory_3d_debug_review_count", 0) > 0
        or counts.get("human_annotation_count", 0) > 0
        or counts.get("review_annotation_count", 0) > 0
    )
    dimensions.append(
        _dimension_profile(
            "annotation_readiness",
            value="unknown" if has_annotation_context else "unavailable",
            reason=(
                "Existing artifacts report review annotation context; annotation quality is "
                "not inferred."
                if has_annotation_context
                else "Existing artifacts do not report review annotation context."
            ),
            source="source_index.profile_counts",
            requires_human_review=True,
        )
    )

    has_core_provenance = all(
        _string_or_none(point.get(key)) is not None
        for key in ("point_manifest_id", "media_id", "manifest_path")
    )
    dimensions.append(
        _dimension_profile(
            "provenance_completeness",
            value="sufficient_for_review" if has_core_provenance else "unknown",
            reason=(
                "The source index provides point manifest, media, and manifest path context."
                if has_core_provenance
                else "The source index has incomplete point provenance context."
            ),
            source="source_index.point_manifest_id",
            requires_human_review=not has_core_provenance,
        )
    )
    return dimensions


def _dimension_profile(
    dimension_key: str,
    *,
    value: str,
    reason: str,
    source: str,
    requires_human_review: bool,
) -> dict[str, Any]:
    if value not in QUALITY_ALLOWED_VALUES:
        value = "unknown"
    return {
        "dimension_key": dimension_key,
        "value": value,
        "reason": reason,
        "source": source,
        "requires_human_review": requires_human_review,
        "warnings": dict(DIMENSION_WARNINGS),
    }


def _has_media_context(
    *,
    point: dict[str, Any],
    availability: dict[str, bool],
) -> bool:
    return (
        availability.get("media_indexed") is True
        or availability.get("replay_available") is True
        or _string_or_none(point.get("source_media_path")) is not None
        or _string_or_none(point.get("source_uri")) is not None
        or _string_or_none(point.get("stored_path")) is not None
        or _string_or_none(point.get("stored_uri")) is not None
        or _string_or_none(point.get("replay_url")) is not None
    )


def _profile_summary(points: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "point_count": len(points),
        "replay_available_count": 0,
        "review_ready_count": 0,
        "unknown_quality_count": 0,
        "requires_human_review_count": 0,
    }
    for point in points:
        availability = _bool_dict(point.get("evidence_availability"))
        dimensions = [
            item for item in _list(point.get("quality_dimensions")) if isinstance(item, dict)
        ]
        if point.get("replay_url") or availability.get("replay_available") is True:
            summary["replay_available_count"] += 1
        if _dimension_value(dimensions, "review_readiness") == "needs_human_review":
            summary["review_ready_count"] += 1
        if any(item.get("value") == "unknown" for item in dimensions):
            summary["unknown_quality_count"] += 1
        if any(item.get("requires_human_review") is True for item in dimensions):
            summary["requires_human_review_count"] += 1
    return summary


def _dimension_value(dimensions: list[dict[str, Any]], dimension_key: str) -> str | None:
    for dimension in dimensions:
        if dimension.get("dimension_key") == dimension_key:
            return _string_or_none(dimension.get("value"))
    return None


def _validate_source_index(source_index: dict[str, Any]) -> dict[str, Any] | None:
    if source_index.get("index_type") != MULTI_POINT_REPLAY_INDEX_TYPE:
        return _failed(
            "invalid_source_index_type",
            f"source index must have index_type {MULTI_POINT_REPLAY_INDEX_TYPE}",
        )
    if source_index.get("index_version") != MULTI_POINT_REPLAY_INDEX_VERSION:
        return _failed(
            "unsupported_source_index_version",
            f"source index must have index_version {MULTI_POINT_REPLAY_INDEX_VERSION}",
        )
    return None


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": OBSERVATION_QUALITY_BLUEPRINT,
        "blueprint_name": OBSERVATION_QUALITY_BLUEPRINT_NAME,
    }


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return _failed(f"missing_{label}_json", f"{label} JSON not found: {path}")
    except json.JSONDecodeError as exc:
        return _failed(f"invalid_{label}_json", f"{label} JSON is not valid: {path}: {exc}")
    if not isinstance(data, dict):
        return _failed(f"invalid_{label}_json", f"{label} JSON must be an object: {path}")
    return {"ok": True, "data": data}


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "profile_type": OBSERVATION_QUALITY_PROFILE_TYPE,
        "profile_version": OBSERVATION_QUALITY_PROFILE_VERSION,
        "taxonomy_type": OBSERVATION_QUALITY_TAXONOMY_TYPE,
        "taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "warnings": dict(OBSERVATION_QUALITY_WARNINGS),
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


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
