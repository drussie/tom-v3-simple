from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.review_label_schema import (
    REVIEW_LABEL_DEFINITIONS,
    REVIEW_LABEL_SCHEMA_TYPE,
    REVIEW_LABEL_SCHEMA_VERSION,
)

REVIEWER_CONFIDENCE_SCHEMA_TYPE = "reviewer_confidence_ambiguity_schema"
REVIEWER_CONFIDENCE_SCHEMA_VERSION = "v1"
REVIEWER_CONFIDENCE_BUNDLE_TYPE = "reviewer_confidence_ambiguity_bundle"
REVIEWER_CONFIDENCE_BUNDLE_VERSION = "v1"
REVIEWER_CONFIDENCE_BLUEPRINT = "blueprint_28"
REVIEWER_CONFIDENCE_BLUEPRINT_NAME = "reviewer_confidence_ambiguity_capture_v1"
DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT = (
    ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json"
)
DEFAULT_REVIEWER_CONFIDENCE_TEMPLATE_OUTPUT = (
    ".data/exports/reviewer_confidence_ambiguity_template.current.json"
)
DEFAULT_REVIEWER_CONFIDENCE_VALIDATION_OUTPUT = (
    ".data/exports/reviewer_confidence_ambiguity.validation.json"
)

FORBIDDEN_CONFIDENCE_FIELDS = {
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
    "correct",
    "incorrect",
}

FORBIDDEN_CONFIDENCE_VALUES = {
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

CONFIDENCE_WARNINGS = {
    "schema_is_not_truth": True,
    "confidence_is_not_truth": True,
    "ambiguity_is_not_truth": True,
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
    "does_not_create_automatic_confidence_scores": True,
    "observation_only": True,
    "review_support_only": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
}

METADATA_DEFINITION_WARNINGS = {
    "confidence_is_not_truth": True,
    "ambiguity_is_not_truth": True,
    "human_review_only": True,
    "no_adjudication": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_validate_correctness": True,
    "observation_only": True,
    "review_support_only": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
}

CONFIDENCE_VALUE_SETS = (
    {
        "key": "reviewer_confidence_values",
        "name": "Reviewer confidence values",
        "description": "Neutral human-provided confidence values.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "low",
            "medium",
            "high",
            "mixed",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
)

AMBIGUITY_VALUE_SETS = (
    {
        "key": "ambiguity_level_values",
        "name": "Ambiguity level values",
        "description": "Neutral human-provided ambiguity level values.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "none_observed",
            "minor_ambiguity",
            "moderate_ambiguity",
            "high_ambiguity",
            "unresolved",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "ambiguity_reason_values",
        "name": "Ambiguity reason values",
        "description": "Neutral human-provided ambiguity reason values.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "occlusion",
            "motion_blur",
            "low_resolution",
            "lighting",
            "camera_angle",
            "partial_evidence",
            "conflicting_evidence",
            "missing_context",
            "reviewer_uncertain",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
)

EVIDENCE_SUFFICIENCY_VALUE_SETS = (
    {
        "key": "evidence_sufficiency_values",
        "name": "Evidence sufficiency values",
        "description": "Neutral human-provided evidence sufficiency values.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "sufficient_for_review",
            "partially_sufficient",
            "insufficient_for_review",
            "evidence_missing",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
)

METADATA_VALUE_SETS = (
    {
        "key": "additional_review_values",
        "name": "Additional review values",
        "description": "Neutral values for whether additional review is requested.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "required",
            "not_required",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "time_spent_bucket_values",
        "name": "Review time spent bucket values",
        "description": "Optional neutral review duration buckets.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "under_30_seconds",
            "30_to_120_seconds",
            "over_120_seconds",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "review_context_complete_values",
        "name": "Review context completeness values",
        "description": "Neutral values for human review-context completeness.",
        "allowed_values": [
            "not_assessed",
            "unknown",
            "complete",
            "partially_complete",
            "incomplete",
            "not_applicable",
        ],
        "default_value": "not_assessed",
    },
    {
        "key": "free_text_optional",
        "name": "Optional free text",
        "description": "Optional human-provided reviewer text.",
        "allowed_values": [],
        "free_text": True,
        "default_value": None,
    },
)

METADATA_DEFINITIONS = (
    {
        "key": "reviewer_confidence",
        "name": "Reviewer confidence",
        "description": "Human-provided confidence about a review label or review context.",
        "value_set": "reviewer_confidence_values",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
    },
    {
        "key": "ambiguity_level",
        "name": "Ambiguity level",
        "description": "Human-provided ambiguity level for a label or review context.",
        "value_set": "ambiguity_level_values",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
    },
    {
        "key": "ambiguity_reasons",
        "name": "Ambiguity reasons",
        "description": "Human-provided reasons for ambiguity.",
        "value_set": "ambiguity_reason_values",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
        "multi_select": True,
    },
    {
        "key": "evidence_sufficiency",
        "name": "Evidence sufficiency",
        "description": "Human-provided evidence sufficiency for review.",
        "value_set": "evidence_sufficiency_values",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
    },
    {
        "key": "reviewer_uncertainty_note",
        "name": "Reviewer uncertainty note",
        "description": "Optional human-provided note about uncertainty or ambiguity.",
        "value_set": "free_text_optional",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
    },
    {
        "key": "requires_additional_review",
        "name": "Requires additional review",
        "description": "Human-provided flag for whether another review pass is requested.",
        "value_set": "additional_review_values",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
    },
    {
        "key": "reviewer_time_spent_bucket",
        "name": "Reviewer time spent bucket",
        "description": "Optional neutral bucket for reviewer time spent.",
        "value_set": "time_spent_bucket_values",
        "applies_to": ["label_entry", "review_session"],
    },
    {
        "key": "review_context_complete",
        "name": "Review context complete",
        "description": "Human-provided review-context completeness label.",
        "value_set": "review_context_complete_values",
        "applies_to": [
            "structured_review_label_bundle",
            "label_entry",
            "review_session",
            "point_manifest",
            "replay",
            "observation_quality_profile",
        ],
    },
)


def export_reviewer_confidence_schema(
    *,
    output_path: str | Path | None = DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the reviewer confidence and ambiguity metadata schema."""

    exported_at = exported_at or datetime.now(UTC)
    schema = _schema_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "metadata_definition_count": len(schema["metadata_definitions"]),
        "schema": schema,
        "warnings": dict(CONFIDENCE_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(schema, indent=2, sort_keys=True), encoding="utf-8")
        result["schema_output"] = str(path)
    return result


def build_reviewer_confidence_template(
    *,
    point_manifest_id: str | None = None,
    media_id: str | None = None,
    replay_url: str | None = None,
    associated_run_ids: dict[str, str] | None = None,
    output_path: str | Path | None = DEFAULT_REVIEWER_CONFIDENCE_TEMPLATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a blank reviewer confidence template without inferring confidence."""

    generated_at = generated_at or datetime.now(UTC)
    bundle = {
        "confidence_bundle_type": REVIEWER_CONFIDENCE_BUNDLE_TYPE,
        "confidence_bundle_version": REVIEWER_CONFIDENCE_BUNDLE_VERSION,
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "generated_at": generated_at.isoformat(),
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "replay_url": replay_url,
        "associated_run_ids": _string_dict(associated_run_ids),
        "confidence_entries": [
            _template_entry(label_key=definition["key"])
            for definition in REVIEW_LABEL_DEFINITIONS
        ],
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(CONFIDENCE_WARNINGS),
            "template_is_not_a_completed_review": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "confidence_bundle_type": REVIEWER_CONFIDENCE_BUNDLE_TYPE,
        "confidence_bundle_version": REVIEWER_CONFIDENCE_BUNDLE_VERSION,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "confidence_entry_count": len(bundle["confidence_entries"]),
        "bundle": bundle,
        "warnings": dict(CONFIDENCE_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        result["template_output"] = str(path)
    return result


def validate_reviewer_confidence_bundle(
    *,
    schema_path: str | Path = DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    bundle_path: str | Path,
    review_label_schema_path: str | Path | None = None,
    output_path: str | Path | None = None,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate confidence bundle structure without judging confidence quality."""

    validated_at = validated_at or datetime.now(UTC)
    schema_loaded = _load_json(schema_path, label="schema")
    if schema_loaded.get("ok") is False:
        return schema_loaded
    bundle_loaded = _load_json(bundle_path, label="confidence_bundle")
    if bundle_loaded.get("ok") is False:
        return bundle_loaded

    schema = _dict(schema_loaded["data"])
    bundle = _dict(bundle_loaded["data"])
    errors = _validate_schema_shape(schema)
    if not errors:
        known_label_keys = _known_label_keys(review_label_schema_path)
        if known_label_keys.get("ok") is False:
            errors.append(
                _error(
                    "invalid_review_label_schema",
                    "review_label_schema_path",
                    known_label_keys.get("message"),
                )
            )
        else:
            errors.extend(
                _validate_bundle_shape(
                    schema=schema,
                    bundle=bundle,
                    known_label_keys=set(_string_list(known_label_keys.get("label_keys"))),
                    enforce_known_label_keys=review_label_schema_path is not None,
                )
            )
    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "reviewer_confidence_ambiguity_bundle_validation",
        "validation_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "validated_at": validated_at.isoformat(),
        "schema_path": str(Path(schema_path)),
        "bundle_path": str(Path(bundle_path)),
        "review_label_schema_path": (
            str(Path(review_label_schema_path)) if review_label_schema_path else None
        ),
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(CONFIDENCE_WARNINGS),
        "known_limitations": [
            "Validation checks structure and allowed metadata values only.",
            "Validation does not infer missing confidence or ambiguity values.",
            "Validation does not create labels or confidence scores.",
            "Validation does not decide whether confidence is appropriate.",
            "Validation does not decide whether a human label is true or correct.",
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
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "exported_at": exported_at.isoformat(),
        "confidence_value_sets": [_value_set(item) for item in CONFIDENCE_VALUE_SETS],
        "ambiguity_value_sets": [_value_set(item) for item in AMBIGUITY_VALUE_SETS],
        "evidence_sufficiency_value_sets": [
            _value_set(item) for item in EVIDENCE_SUFFICIENCY_VALUE_SETS
        ],
        "metadata_value_sets": [_value_set(item) for item in METADATA_VALUE_SETS],
        "metadata_definitions": [
            _metadata_definition(definition) for definition in METADATA_DEFINITIONS
        ],
        "provenance_requirements": {
            "confidence_bundle_type_required": REVIEWER_CONFIDENCE_BUNDLE_TYPE,
            "confidence_bundle_version_required": REVIEWER_CONFIDENCE_BUNDLE_VERSION,
            "schema_version_required": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
            "review_label_schema_version_required": REVIEW_LABEL_SCHEMA_VERSION,
            "point_manifest_id_recommended": True,
            "media_id_recommended": True,
            "replay_url_recommended": True,
            "associated_run_ids_allowed": [
                "event_candidate_run_id",
                "trajectory_3d_run_id",
                "camera_geometry_id",
            ],
            "provenance_only": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "known_metadata_keys_only": True,
            "allowed_values_only": True,
            "optional_review_label_schema_label_key_validation": True,
            "human_provided_only_required": True,
            "machine_inferred_must_be_false": True,
            "does_not_infer_missing_confidence": True,
            "does_not_create_labels": True,
            "does_not_validate_truth": True,
            "does_not_validate_confidence_appropriateness": True,
            "forbidden_fields": sorted(FORBIDDEN_CONFIDENCE_FIELDS),
            "forbidden_values": sorted(FORBIDDEN_CONFIDENCE_VALUES),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(CONFIDENCE_WARNINGS),
    }


def _value_set(value_set: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": value_set["key"],
        "name": value_set["name"],
        "description": value_set["description"],
        "allowed_values": list(value_set.get("allowed_values", [])),
        "default_value": value_set.get("default_value"),
        "free_text": value_set.get("free_text", False),
        "warnings": {
            "value_set_is_not_truth": True,
            "human_review_only": True,
            "review_support_only": True,
            "no_adjudication": True,
        },
    }


def _metadata_definition(definition: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": definition["key"],
        "name": definition["name"],
        "description": definition["description"],
        "value_set": definition["value_set"],
        "applies_to": list(definition["applies_to"]),
        "required": False,
        "multi_select": definition.get("multi_select", False),
        "human_provided_only": True,
        "machine_inferred": False,
        "warnings": dict(METADATA_DEFINITION_WARNINGS),
    }


def _template_entry(*, label_key: str) -> dict[str, Any]:
    return {
        "label_key": label_key,
        "label_entry_id": None,
        "reviewer_confidence": "not_assessed",
        "ambiguity_level": "not_assessed",
        "ambiguity_reasons": ["not_assessed"],
        "evidence_sufficiency": "not_assessed",
        "reviewer_uncertainty_note": None,
        "requires_additional_review": "not_assessed",
        "reviewer_time_spent_bucket": "not_assessed",
        "review_context_complete": "not_assessed",
        "reviewed_at": None,
        "human_provided_only": True,
        "machine_inferred": False,
        "template_entry": True,
        "warnings": dict(METADATA_DEFINITION_WARNINGS),
    }


def _validate_schema_shape(schema: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if schema.get("schema_type") != REVIEWER_CONFIDENCE_SCHEMA_TYPE:
        errors.append(_error("invalid_schema_type", "schema_type", schema.get("schema_type")))
    if schema.get("schema_version") != REVIEWER_CONFIDENCE_SCHEMA_VERSION:
        errors.append(
            _error("invalid_schema_version", "schema_version", schema.get("schema_version"))
        )
    for section in (
        "confidence_value_sets",
        "ambiguity_value_sets",
        "evidence_sufficiency_value_sets",
        "metadata_definitions",
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
    for definition in _list(schema.get("metadata_definitions")):
        if not isinstance(definition, dict):
            errors.append(_error("invalid_metadata_definition", "metadata_definitions", definition))
            continue
        for field in (
            "key",
            "name",
            "description",
            "value_set",
            "applies_to",
            "required",
            "multi_select",
            "human_provided_only",
            "machine_inferred",
            "warnings",
        ):
            if field not in definition:
                errors.append(
                    _error("missing_metadata_definition_field", field, definition.get("key"))
                )
        if definition.get("value_set") not in value_sets:
            errors.append(_error("unknown_value_set", "value_set", definition.get("value_set")))
        if definition.get("required") is not False:
            errors.append(_error("metadata_definition_must_be_optional", "required", definition))
        if definition.get("human_provided_only") is not True:
            errors.append(
                _error(
                    "metadata_must_be_human_provided_only",
                    "human_provided_only",
                    definition,
                )
            )
        if definition.get("machine_inferred") is not False:
            errors.append(
                _error("metadata_must_not_be_machine_inferred", "machine_inferred", definition)
            )
        warnings = _bool_dict(definition.get("warnings"))
        for warning, expected in METADATA_DEFINITION_WARNINGS.items():
            if warnings.get(warning) is not expected:
                errors.append(_error("missing_metadata_warning", warning, definition.get("key")))
    for value_set in value_sets.values():
        if value_set.get("free_text") is True:
            continue
        allowed_values = _string_list(value_set.get("allowed_values"))
        if not allowed_values:
            errors.append(_error("empty_value_set", "allowed_values", value_set.get("key")))
        forbidden_values = sorted(set(allowed_values) & FORBIDDEN_CONFIDENCE_VALUES)
        if forbidden_values:
            errors.append(
                _error("forbidden_value_in_value_set", "allowed_values", forbidden_values)
            )
    return errors


def _validate_bundle_shape(
    *,
    schema: dict[str, Any],
    bundle: dict[str, Any],
    known_label_keys: set[str],
    enforce_known_label_keys: bool,
) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(bundle, path="confidence_bundle")
    if bundle.get("confidence_bundle_type") != REVIEWER_CONFIDENCE_BUNDLE_TYPE:
        errors.append(
            _error(
                "invalid_confidence_bundle_type",
                "confidence_bundle_type",
                bundle.get("confidence_bundle_type"),
            )
        )
    if bundle.get("confidence_bundle_version") != REVIEWER_CONFIDENCE_BUNDLE_VERSION:
        errors.append(
            _error(
                "invalid_confidence_bundle_version",
                "confidence_bundle_version",
                bundle.get("confidence_bundle_version"),
            )
        )
    if bundle.get("schema_version") != REVIEWER_CONFIDENCE_SCHEMA_VERSION:
        errors.append(
            _error(
                "invalid_bundle_schema_version",
                "schema_version",
                bundle.get("schema_version"),
            )
        )
    if bundle.get("review_label_schema_version") != REVIEW_LABEL_SCHEMA_VERSION:
        errors.append(
            _error(
                "invalid_review_label_schema_version",
                "review_label_schema_version",
                bundle.get("review_label_schema_version"),
            )
        )

    entries = bundle.get("confidence_entries")
    if not isinstance(entries, list):
        errors.append(_error("confidence_entries_must_be_list", "confidence_entries", entries))
        return errors

    value_sets = _value_set_map(schema)
    for index, entry in enumerate(entries):
        path = f"confidence_entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("confidence_entry_must_be_object", path, entry))
            continue
        label_key = _string_or_none(entry.get("label_key"))
        label_entry_id = _string_or_none(entry.get("label_entry_id"))
        if label_key is None and label_entry_id is None:
            errors.append(_error("missing_label_reference", path, entry))
        if enforce_known_label_keys and label_key is not None and label_key not in known_label_keys:
            errors.append(_error("unknown_label_key", f"{path}.label_key", label_key))
        _append_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="reviewer_confidence_values",
            value=entry.get("reviewer_confidence"),
            field=f"{path}.reviewer_confidence",
        )
        _append_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="ambiguity_level_values",
            value=entry.get("ambiguity_level"),
            field=f"{path}.ambiguity_level",
        )
        _append_multi_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="ambiguity_reason_values",
            value=entry.get("ambiguity_reasons"),
            field=f"{path}.ambiguity_reasons",
        )
        _append_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="evidence_sufficiency_values",
            value=entry.get("evidence_sufficiency"),
            field=f"{path}.evidence_sufficiency",
        )
        _append_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="additional_review_values",
            value=entry.get("requires_additional_review"),
            field=f"{path}.requires_additional_review",
        )
        _append_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="time_spent_bucket_values",
            value=entry.get("reviewer_time_spent_bucket"),
            field=f"{path}.reviewer_time_spent_bucket",
        )
        _append_value_error(
            errors,
            value_sets=value_sets,
            value_set_key="review_context_complete_values",
            value=entry.get("review_context_complete"),
            field=f"{path}.review_context_complete",
        )
        uncertainty_note = entry.get("reviewer_uncertainty_note")
        if uncertainty_note is not None and not isinstance(uncertainty_note, str):
            errors.append(
                _error("reviewer_uncertainty_note_must_be_text", f"{path}.note", uncertainty_note)
            )
        if entry.get("human_provided_only") is not True:
            errors.append(
                _error(
                    "confidence_entry_must_be_human_provided_only",
                    f"{path}.human_provided_only",
                    entry.get("human_provided_only"),
                )
            )
        if entry.get("machine_inferred", False) is not False:
            errors.append(
                _error(
                    "confidence_entry_must_not_be_machine_inferred",
                    f"{path}.machine_inferred",
                    entry.get("machine_inferred"),
                )
            )
    return errors


def _append_value_error(
    errors: list[dict[str, Any]],
    *,
    value_sets: dict[str, dict[str, Any]],
    value_set_key: str,
    value: Any,
    field: str,
) -> None:
    value_set = value_sets.get(value_set_key, {})
    allowed_values = set(_string_list(value_set.get("allowed_values")))
    if not isinstance(value, str) or value not in allowed_values:
        errors.append(_error("invalid_metadata_value", field, value))
    if value in FORBIDDEN_CONFIDENCE_VALUES:
        errors.append(_error("forbidden_metadata_value", field, value))


def _append_multi_value_error(
    errors: list[dict[str, Any]],
    *,
    value_sets: dict[str, dict[str, Any]],
    value_set_key: str,
    value: Any,
    field: str,
) -> None:
    if not isinstance(value, list):
        errors.append(_error("metadata_value_must_be_list", field, value))
        return
    value_set = value_sets.get(value_set_key, {})
    allowed_values = set(_string_list(value_set.get("allowed_values")))
    for item in value:
        if not isinstance(item, str) or item not in allowed_values:
            errors.append(_error("invalid_metadata_value", field, item))
        if item in FORBIDDEN_CONFIDENCE_VALUES:
            errors.append(_error("forbidden_metadata_value", field, item))


def _known_label_keys(review_label_schema_path: str | Path | None) -> dict[str, Any]:
    if review_label_schema_path is None:
        return {"ok": True, "label_keys": []}
    loaded = _load_json(review_label_schema_path, label="review_label_schema")
    if loaded.get("ok") is False:
        return loaded
    schema = _dict(loaded.get("data"))
    if schema.get("schema_type") != REVIEW_LABEL_SCHEMA_TYPE:
        return {
            "ok": False,
            "message": f"review label schema must have schema_type {REVIEW_LABEL_SCHEMA_TYPE}",
        }
    if schema.get("schema_version") != REVIEW_LABEL_SCHEMA_VERSION:
        return {
            "ok": False,
            "message": (
                f"review label schema must have schema_version {REVIEW_LABEL_SCHEMA_VERSION}"
            ),
        }
    label_keys = [
        str(item["key"])
        for item in _list(schema.get("label_definitions"))
        if isinstance(item, dict) and isinstance(item.get("key"), str)
    ]
    return {"ok": True, "label_keys": label_keys}


def _value_set_map(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for section in (
        "confidence_value_sets",
        "ambiguity_value_sets",
        "evidence_sufficiency_value_sets",
        "metadata_value_sets",
    ):
        for item in _list(schema.get(section)):
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
            if key in FORBIDDEN_CONFIDENCE_FIELDS:
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
        "blueprint": REVIEWER_CONFIDENCE_BLUEPRINT,
        "blueprint_name": REVIEWER_CONFIDENCE_BLUEPRINT_NAME,
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
        "schema_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
        "schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "warnings": dict(CONFIDENCE_WARNINGS),
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
