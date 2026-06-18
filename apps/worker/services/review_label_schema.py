from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REVIEW_LABEL_SCHEMA_TYPE = "structured_review_label_schema"
REVIEW_LABEL_SCHEMA_VERSION = "v1"
REVIEW_LABEL_BUNDLE_TYPE = "structured_review_label_bundle"
REVIEW_LABEL_BUNDLE_VERSION = "v1"
REVIEW_LABEL_BLUEPRINT = "blueprint_27"
REVIEW_LABEL_BLUEPRINT_NAME = "structured_review_label_schema_v1"
DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT = ".data/contracts/review_label_schema_v1.json"
DEFAULT_REVIEW_LABEL_TEMPLATE_OUTPUT = ".data/exports/review_label_template.current.json"
DEFAULT_REVIEW_LABEL_VALIDATION_OUTPUT = ".data/exports/review_label_bundle.validation.json"

FORBIDDEN_REVIEW_LABEL_FIELDS = {
    "in_out",
    "score",
    "winner",
    "point_winner",
    "player_identity",
    "server",
    "receiver",
    "adjudication",
    "accepted",
    "rejected",
}

FORBIDDEN_REVIEW_LABEL_VALUES = {
    "in",
    "out",
    "winner",
    "score",
    "correct",
    "incorrect",
    "accepted",
    "rejected",
    "player_a",
    "player_b",
    "server",
    "receiver",
}

REVIEW_LABEL_WARNINGS = {
    "schema_is_not_truth": True,
    "label_is_not_truth": True,
    "human_review_only": True,
    "no_adjudication": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_observations": True,
    "does_not_create_labels": True,
    "does_not_infer_truth": True,
    "does_not_validate_correctness": True,
    "observation_only": True,
    "review_support_only": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
}

LABEL_DEFINITION_WARNINGS = {
    "label_is_not_truth": True,
    "human_review_only": True,
    "no_adjudication": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "observation_only": True,
    "review_support_only": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
}

REVIEW_LABEL_FAMILIES = (
    {
        "key": "evidence_visibility_review",
        "name": "Evidence visibility review",
        "description": "Human review labels for whether evidence is visible or obscured.",
    },
    {
        "key": "replay_review_readiness",
        "name": "Replay review readiness",
        "description": "Human review labels for whether replay context supports review.",
    },
    {
        "key": "observation_quality_review",
        "name": "Observation quality review",
        "description": "Human review labels for observation-quality profile context.",
    },
    {
        "key": "event_candidate_review_context",
        "name": "Event candidate review context",
        "description": "Human review labels for event-candidate context availability.",
    },
    {
        "key": "trajectory_3d_review_context",
        "name": "3D trajectory review context",
        "description": "Human review labels for trajectory-candidate context availability.",
    },
    {
        "key": "provenance_review",
        "name": "Provenance review",
        "description": "Human review labels for provenance context availability.",
    },
    {
        "key": "reviewer_note_context",
        "name": "Reviewer note context",
        "description": "Human review labels for whether reviewer notes are present.",
    },
)

REVIEW_LABEL_VALUE_SETS = (
    {
        "key": "visibility_review_values",
        "name": "Visibility review values",
        "description": "Neutral values for human visibility review.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "unavailable",
            "visible",
            "partially_visible",
            "obscured",
            "ambiguous",
            "needs_human_review",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "review_readiness_values",
        "name": "Review readiness values",
        "description": "Neutral values for human review-readiness labels.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "unavailable",
            "needs_human_review",
            "sufficient_for_review",
            "insufficient_for_review",
            "ambiguous",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "evidence_presence_values",
        "name": "Evidence presence values",
        "description": "Neutral values for human evidence-presence labels.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "unavailable",
            "evidence_present",
            "evidence_missing",
            "ambiguous",
            "needs_human_review",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "provenance_presence_values",
        "name": "Provenance presence values",
        "description": "Neutral values for human provenance-presence labels.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "unavailable",
            "provenance_present",
            "provenance_missing",
            "ambiguous",
            "needs_human_review",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "reviewer_note_values",
        "name": "Reviewer note values",
        "description": "Neutral values for human reviewer-note labels.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "reviewer_note_present",
            "reviewer_note_missing",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
)

REVIEW_LABEL_DEFINITIONS = (
    {
        "key": "media_visibility_review",
        "name": "Media visibility review",
        "description": "Human-provided review label for overall media visibility context.",
        "family": "evidence_visibility_review",
        "applies_to": ["point_manifest", "replay"],
        "value_set": "visibility_review_values",
    },
    {
        "key": "court_visibility_review",
        "name": "Court visibility review",
        "description": "Human-provided review label for court visibility context.",
        "family": "evidence_visibility_review",
        "applies_to": ["replay", "observation_quality_profile"],
        "value_set": "visibility_review_values",
    },
    {
        "key": "ball_visibility_review",
        "name": "Ball visibility review",
        "description": "Human-provided review label for ball visibility context.",
        "family": "evidence_visibility_review",
        "applies_to": ["replay", "event_candidate", "trajectory_3d_candidate"],
        "value_set": "visibility_review_values",
    },
    {
        "key": "replay_readiness_review",
        "name": "Replay readiness review",
        "description": "Human-provided review label for whether replay context supports review.",
        "family": "replay_review_readiness",
        "applies_to": ["replay", "review_session"],
        "value_set": "review_readiness_values",
    },
    {
        "key": "observation_quality_profile_review",
        "name": "Observation quality profile review",
        "description": "Human-provided review label for observation-quality profile context.",
        "family": "observation_quality_review",
        "applies_to": ["observation_quality_profile", "review_session"],
        "value_set": "review_readiness_values",
    },
    {
        "key": "event_candidate_context_review",
        "name": "Event candidate context review",
        "description": "Human-provided review label for event-candidate context availability.",
        "family": "event_candidate_review_context",
        "applies_to": ["event_candidate", "replay", "review_session"],
        "value_set": "evidence_presence_values",
    },
    {
        "key": "trajectory_3d_context_review",
        "name": "3D trajectory context review",
        "description": "Human-provided review label for 3D trajectory context availability.",
        "family": "trajectory_3d_review_context",
        "applies_to": ["trajectory_3d_candidate", "replay", "review_session"],
        "value_set": "evidence_presence_values",
    },
    {
        "key": "provenance_context_review",
        "name": "Provenance context review",
        "description": "Human-provided review label for provenance context availability.",
        "family": "provenance_review",
        "applies_to": ["point_manifest", "provenance", "review_session"],
        "value_set": "provenance_presence_values",
    },
    {
        "key": "reviewer_note_context_review",
        "name": "Reviewer note context review",
        "description": "Human-provided review label for reviewer-note context availability.",
        "family": "reviewer_note_context",
        "applies_to": ["review_session"],
        "value_set": "reviewer_note_values",
    },
)


def export_review_label_schema(
    *,
    output_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the structured human-review label schema contract."""

    exported_at = exported_at or datetime.now(UTC)
    schema = _schema_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "schema_type": REVIEW_LABEL_SCHEMA_TYPE,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "label_family_count": len(schema["label_families"]),
        "label_definition_count": len(schema["label_definitions"]),
        "value_set_count": len(schema["value_sets"]),
        "schema": schema,
        "warnings": dict(REVIEW_LABEL_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(schema, indent=2, sort_keys=True), encoding="utf-8")
        result["schema_output"] = str(path)
    return result


def build_review_label_template(
    *,
    point_manifest_id: str | None = None,
    media_id: str | None = None,
    replay_url: str | None = None,
    associated_run_ids: dict[str, str] | None = None,
    output_path: str | Path | None = DEFAULT_REVIEW_LABEL_TEMPLATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a blank human-review label template without inferring labels."""

    generated_at = generated_at or datetime.now(UTC)
    schema = _schema_payload(exported_at=generated_at)
    label_definitions = _label_definition_map(schema)
    value_sets = _value_set_map(schema)
    bundle = {
        "label_bundle_type": REVIEW_LABEL_BUNDLE_TYPE,
        "label_bundle_version": REVIEW_LABEL_BUNDLE_VERSION,
        "schema_type": REVIEW_LABEL_SCHEMA_TYPE,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "generated_at": generated_at.isoformat(),
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "replay_url": replay_url,
        "associated_run_ids": _string_dict(associated_run_ids),
        "label_entries": [
            _template_entry(
                definition=definition,
                value_sets=value_sets,
            )
            for definition in label_definitions.values()
        ],
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(REVIEW_LABEL_WARNINGS),
            "template_is_not_a_completed_review": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "label_bundle_type": REVIEW_LABEL_BUNDLE_TYPE,
        "label_bundle_version": REVIEW_LABEL_BUNDLE_VERSION,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "label_entry_count": len(bundle["label_entries"]),
        "bundle": bundle,
        "warnings": dict(REVIEW_LABEL_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        result["template_output"] = str(path)
    return result


def validate_review_label_bundle(
    *,
    schema_path: str | Path = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    bundle_path: str | Path,
    output_path: str | Path | None = None,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate review-label bundle structure without judging label truth."""

    validated_at = validated_at or datetime.now(UTC)
    schema_loaded = _load_json(schema_path, label="schema")
    if schema_loaded.get("ok") is False:
        return schema_loaded
    bundle_loaded = _load_json(bundle_path, label="label_bundle")
    if bundle_loaded.get("ok") is False:
        return bundle_loaded

    schema = _dict(schema_loaded["data"])
    bundle = _dict(bundle_loaded["data"])
    errors = _validate_schema_shape(schema)
    if not errors:
        errors.extend(_validate_bundle_shape(schema=schema, bundle=bundle))
    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "structured_review_label_bundle_validation",
        "validation_version": REVIEW_LABEL_SCHEMA_VERSION,
        "validated_at": validated_at.isoformat(),
        "schema_path": str(Path(schema_path)),
        "bundle_path": str(Path(bundle_path)),
        "schema_type": REVIEW_LABEL_SCHEMA_TYPE,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(REVIEW_LABEL_WARNINGS),
        "known_limitations": [
            "Validation checks structure, label keys, and allowed values only.",
            "Validation does not infer missing labels or create labels.",
            "Validation does not decide whether a human label is true or correct.",
            (
                "Validation does not create in/out, score, point winner, player identity, "
                "accepted/rejected lifecycle, or adjudication."
            ),
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def _schema_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "schema_type": REVIEW_LABEL_SCHEMA_TYPE,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "exported_at": exported_at.isoformat(),
        "label_families": [_label_family(family) for family in REVIEW_LABEL_FAMILIES],
        "label_definitions": [
            _label_definition(definition) for definition in REVIEW_LABEL_DEFINITIONS
        ],
        "value_sets": [_value_set(value_set) for value_set in REVIEW_LABEL_VALUE_SETS],
        "provenance_requirements": {
            "label_bundle_type_required": REVIEW_LABEL_BUNDLE_TYPE,
            "label_bundle_version_required": REVIEW_LABEL_BUNDLE_VERSION,
            "schema_version_required": REVIEW_LABEL_SCHEMA_VERSION,
            "point_manifest_id_recommended": True,
            "media_id_recommended": True,
            "replay_url_recommended": True,
            "associated_run_ids_allowed": [
                "event_candidate_run_id",
                "trajectory_3d_run_id",
                "camera_geometry_id",
            ],
            "reviewer_identity_not_required": True,
            "provenance_only": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "known_label_keys_only": True,
            "allowed_values_only": True,
            "human_provided_only_required": True,
            "machine_inferred_must_be_false": True,
            "does_not_infer_missing_labels": True,
            "does_not_create_labels": True,
            "does_not_validate_truth": True,
            "forbidden_fields": sorted(FORBIDDEN_REVIEW_LABEL_FIELDS),
            "forbidden_label_values": sorted(FORBIDDEN_REVIEW_LABEL_VALUES),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(REVIEW_LABEL_WARNINGS),
    }


def _label_family(family: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": family["key"],
        "name": family["name"],
        "description": family["description"],
        "warnings": {
            "family_is_not_truth": True,
            "human_review_only": True,
            "review_support_only": True,
            "no_adjudication": True,
        },
    }


def _label_definition(definition: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": definition["key"],
        "name": definition["name"],
        "description": definition["description"],
        "family": definition["family"],
        "applies_to": list(definition["applies_to"]),
        "value_set": definition["value_set"],
        "required": False,
        "multi_select": False,
        "human_provided_only": True,
        "machine_inferred": False,
        "warnings": dict(LABEL_DEFINITION_WARNINGS),
    }


def _value_set(value_set: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": value_set["key"],
        "name": value_set["name"],
        "description": value_set["description"],
        "allowed_values": list(value_set["allowed_values"]),
        "default_value": value_set["default_value"],
        "warnings": {
            "value_set_is_not_truth": True,
            "human_review_only": True,
            "review_support_only": True,
            "no_adjudication": True,
        },
    }


def _template_entry(
    *,
    definition: dict[str, Any],
    value_sets: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    value_set = value_sets.get(str(definition.get("value_set")), {})
    return {
        "label_key": definition.get("key"),
        "value": value_set.get("default_value", "not_assessed"),
        "reviewer_note": None,
        "evidence_reference": None,
        "reviewed_at": None,
        "human_provided_only": True,
        "machine_inferred": False,
        "template_entry": True,
        "warnings": dict(LABEL_DEFINITION_WARNINGS),
    }


def _validate_schema_shape(schema: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if schema.get("schema_type") != REVIEW_LABEL_SCHEMA_TYPE:
        errors.append(_error("invalid_schema_type", "schema_type", schema.get("schema_type")))
    if schema.get("schema_version") != REVIEW_LABEL_SCHEMA_VERSION:
        errors.append(
            _error("invalid_schema_version", "schema_version", schema.get("schema_version"))
        )
    for section in (
        "label_families",
        "label_definitions",
        "value_sets",
        "provenance_requirements",
        "validation_rules",
        "warnings",
    ):
        if section not in schema:
            errors.append(_error("missing_schema_section", section, None))
    errors.extend(_forbidden_field_errors(schema, path="schema"))
    if errors:
        return errors

    value_sets = _value_set_map(schema)
    family_keys = {
        item.get("key")
        for item in _list(schema.get("label_families"))
        if isinstance(item, dict)
    }
    for definition in _list(schema.get("label_definitions")):
        if not isinstance(definition, dict):
            errors.append(_error("invalid_label_definition", "label_definitions", definition))
            continue
        for field in (
            "key",
            "name",
            "description",
            "family",
            "applies_to",
            "value_set",
            "required",
            "multi_select",
            "human_provided_only",
            "machine_inferred",
            "warnings",
        ):
            if field not in definition:
                errors.append(
                    _error("missing_label_definition_field", field, definition.get("key"))
                )
        if definition.get("family") not in family_keys:
            errors.append(_error("unknown_label_family", "family", definition.get("family")))
        if definition.get("value_set") not in value_sets:
            errors.append(_error("unknown_value_set", "value_set", definition.get("value_set")))
        if definition.get("required") is not False:
            errors.append(_error("label_definition_must_be_optional", "required", definition))
        if definition.get("multi_select") is not False:
            errors.append(
                _error("label_definition_must_be_single_select", "multi_select", definition)
            )
        if definition.get("human_provided_only") is not True:
            errors.append(
                _error("label_must_be_human_provided_only", "human_provided_only", definition)
            )
        if definition.get("machine_inferred") is not False:
            errors.append(
                _error("label_must_not_be_machine_inferred", "machine_inferred", definition)
            )
        warnings = _bool_dict(definition.get("warnings"))
        for warning, expected in LABEL_DEFINITION_WARNINGS.items():
            if warnings.get(warning) is not expected:
                errors.append(_error("missing_label_warning", warning, definition.get("key")))
    for value_set in value_sets.values():
        allowed_values = _string_list(value_set.get("allowed_values"))
        if not allowed_values:
            errors.append(_error("empty_value_set", "allowed_values", value_set.get("key")))
        forbidden_values = sorted(set(allowed_values) & FORBIDDEN_REVIEW_LABEL_VALUES)
        if forbidden_values:
            errors.append(
                _error("forbidden_value_in_value_set", "allowed_values", forbidden_values)
            )
    return errors


def _validate_bundle_shape(
    *,
    schema: dict[str, Any],
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(bundle, path="label_bundle")
    if bundle.get("label_bundle_type") != REVIEW_LABEL_BUNDLE_TYPE:
        errors.append(
            _error(
                "invalid_label_bundle_type",
                "label_bundle_type",
                bundle.get("label_bundle_type"),
            )
        )
    if bundle.get("label_bundle_version") != REVIEW_LABEL_BUNDLE_VERSION:
        errors.append(
            _error(
                "invalid_label_bundle_version",
                "label_bundle_version",
                bundle.get("label_bundle_version"),
            )
        )
    if bundle.get("schema_version") != REVIEW_LABEL_SCHEMA_VERSION:
        errors.append(
            _error(
                "invalid_bundle_schema_version",
                "schema_version",
                bundle.get("schema_version"),
            )
        )
    entries = bundle.get("label_entries")
    if not isinstance(entries, list):
        errors.append(_error("label_entries_must_be_list", "label_entries", entries))
        return errors

    definitions = _label_definition_map(schema)
    value_sets = _value_set_map(schema)
    for index, entry in enumerate(entries):
        path = f"label_entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("label_entry_must_be_object", path, entry))
            continue
        label_key = _string_or_none(entry.get("label_key"))
        if label_key is None:
            errors.append(_error("missing_label_key", f"{path}.label_key", entry.get("label_key")))
            continue
        definition = definitions.get(label_key)
        if definition is None:
            errors.append(_error("unknown_label_key", f"{path}.label_key", label_key))
            continue
        value = entry.get("value")
        value_set = value_sets.get(str(definition.get("value_set")), {})
        allowed_values = set(_string_list(value_set.get("allowed_values")))
        if not isinstance(value, str) or value not in allowed_values:
            errors.append(_error("invalid_label_value", f"{path}.value", value))
        if value in FORBIDDEN_REVIEW_LABEL_VALUES:
            errors.append(_error("forbidden_label_value", f"{path}.value", value))
        if entry.get("human_provided_only") is not True:
            errors.append(
                _error(
                    "label_entry_must_be_human_provided_only",
                    f"{path}.human_provided_only",
                    entry.get("human_provided_only"),
                )
            )
        if entry.get("machine_inferred", False) is not False:
            errors.append(
                _error(
                    "label_entry_must_not_be_machine_inferred",
                    f"{path}.machine_inferred",
                    entry.get("machine_inferred"),
                )
            )
    return errors


def _label_definition_map(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for item in _list(schema.get("label_definitions")):
        if not isinstance(item, dict):
            continue
        key = _string_or_none(item.get("key"))
        if key is not None:
            mapped[key] = item
    return mapped


def _value_set_map(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for item in _list(schema.get("value_sets")):
        if not isinstance(item, dict):
            continue
        key = _string_or_none(item.get("key"))
        if key is not None:
            mapped[key] = item
    return mapped


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}"
            if key in FORBIDDEN_REVIEW_LABEL_FIELDS:
                errors.append(_error("forbidden_field", next_path, key))
            errors.extend(_forbidden_field_errors(item, path=next_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_forbidden_field_errors(item, path=f"{path}[{index}]"))
    return errors


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "does_not_judge_truth": True,
    }


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": REVIEW_LABEL_BLUEPRINT,
        "blueprint_name": REVIEW_LABEL_BLUEPRINT_NAME,
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
        "schema_type": REVIEW_LABEL_SCHEMA_TYPE,
        "schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "warnings": dict(REVIEW_LABEL_WARNINGS),
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
