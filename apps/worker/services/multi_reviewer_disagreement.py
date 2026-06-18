from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.review_label_schema import (
    DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    REVIEW_LABEL_DEFINITIONS,
    REVIEW_LABEL_SCHEMA_VERSION,
    validate_review_label_bundle,
)
from apps.worker.services.reviewer_confidence_schema import (
    DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
    validate_reviewer_confidence_bundle,
)

MULTI_REVIEWER_SCHEMA_TYPE = "multi_reviewer_disagreement_schema"
MULTI_REVIEWER_SCHEMA_VERSION = "v1"
MULTI_REVIEWER_REVIEW_SET_TYPE = "multi_reviewer_review_set"
MULTI_REVIEWER_REVIEW_SET_VERSION = "v1"
DISAGREEMENT_REPORT_TYPE = "reviewer_disagreement_report"
DISAGREEMENT_REPORT_VERSION = "v1"
MULTI_REVIEWER_BLUEPRINT = "blueprint_29"
MULTI_REVIEWER_BLUEPRINT_NAME = "multi_reviewer_disagreement_foundation_v1"

DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT = (
    ".data/contracts/multi_reviewer_disagreement_schema_v1.json"
)
DEFAULT_MULTI_REVIEWER_REVIEW_SET_TEMPLATE_OUTPUT = (
    ".data/exports/multi_reviewer_review_set_template.current.json"
)
DEFAULT_MULTI_REVIEWER_REVIEW_SET_VALIDATION_OUTPUT = (
    ".data/exports/multi_reviewer_review_set.validation.json"
)
DEFAULT_REVIEWER_DISAGREEMENT_REPORT_OUTPUT = (
    ".data/exports/reviewer_disagreement_report.current.json"
)

FORBIDDEN_MULTI_REVIEWER_FIELDS = {
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
    "truth",
    "reviewer_score",
    "reviewer_rank",
    "reviewer_reliability",
}

DISALLOWED_REVIEWER_IDENTITY_FIELDS = {
    "name",
    "real_name",
    "reviewer_name",
    "email",
    "reviewer_email",
    "reviewer_authority_score",
    "reviewer_correctness_score",
    "reviewer_quality_score",
    "reviewer_rank",
    "reviewer_reliability",
    "reviewer_score",
}

MULTI_REVIEWER_WARNINGS = {
    "schema_is_not_truth": True,
    "review_set_is_not_truth": True,
    "disagreement_is_not_truth": True,
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
    "does_not_score_reviewers": True,
    "does_not_rank_reviewers": True,
    "does_not_resolve_disagreement": True,
    "does_not_create_automatic_confidence_scores": True,
    "observation_only": True,
    "review_support_only": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
}

REVIEWER_ENTRY_WARNINGS = {
    "reviewer_identity_is_pseudonymous": True,
    "human_review_only": True,
    "machine_inferred": False,
    "no_adjudication": True,
    "does_not_score_reviewers": True,
    "does_not_rank_reviewers": True,
    "does_not_validate_correctness": True,
    "does_not_resolve_disagreement": True,
    "review_support_only": True,
}

DISAGREEMENT_VALUES = [
    "not_assessed",
    "no_disagreement_observed",
    "disagreement_observed",
    "partial_disagreement",
    "missing_reviewer_input",
    "insufficient_reviewer_input",
    "ambiguous",
    "not_applicable",
]

DISAGREEMENT_DIMENSIONS = (
    {
        "key": "label_value_disagreement",
        "name": "Label value disagreement",
        "description": "Structural difference across human-provided label values.",
    },
    {
        "key": "confidence_disagreement",
        "name": "Confidence disagreement",
        "description": "Structural difference across human-provided confidence values.",
    },
    {
        "key": "ambiguity_disagreement",
        "name": "Ambiguity disagreement",
        "description": "Structural difference across human-provided ambiguity values.",
    },
    {
        "key": "evidence_sufficiency_disagreement",
        "name": "Evidence sufficiency disagreement",
        "description": "Structural difference across human-provided evidence sufficiency values.",
    },
    {
        "key": "missing_review_bundle",
        "name": "Missing review bundle",
        "description": "A reviewer entry has no available structured review-label bundle.",
    },
    {
        "key": "missing_confidence_bundle",
        "name": "Missing confidence bundle",
        "description": "A reviewer entry has no available reviewer confidence bundle.",
    },
    {
        "key": "reviewer_note_difference",
        "name": "Reviewer note difference",
        "description": "Structural difference across human-provided reviewer notes.",
    },
    {
        "key": "provenance_mismatch",
        "name": "Provenance mismatch",
        "description": "Reviewer bundle context differs from the review-set context.",
    },
    {
        "key": "not_assessed_difference",
        "name": "Not assessed difference",
        "description": "At least one reviewer left a compared value not assessed.",
    },
)

REVIEWER_ENTRY_DEFINITIONS = (
    {
        "key": "reviewer_id",
        "description": "Required neutral or pseudonymous reviewer identifier.",
        "required": True,
    },
    {
        "key": "reviewer_role",
        "description": "Optional neutral reviewer role.",
        "required": False,
    },
    {
        "key": "reviewer_session_id",
        "description": "Optional neutral review session identifier.",
        "required": False,
    },
    {
        "key": "reviewer_notes",
        "description": "Optional human-provided reviewer note for this entry.",
        "required": False,
    },
    {
        "key": "review_label_bundle_path",
        "description": "Optional local path to a Blueprint 27 review-label bundle.",
        "required": False,
    },
    {
        "key": "review_label_bundle_ref",
        "description": "Optional non-path reference to a Blueprint 27 review-label bundle.",
        "required": False,
    },
    {
        "key": "reviewer_confidence_bundle_path",
        "description": "Optional local path to a Blueprint 28 confidence bundle.",
        "required": False,
    },
    {
        "key": "reviewer_confidence_bundle_ref",
        "description": "Optional non-path reference to a Blueprint 28 confidence bundle.",
        "required": False,
    },
)


def export_multi_reviewer_disagreement_schema(
    *,
    output_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the multi-reviewer disagreement schema contract."""

    exported_at = exported_at or datetime.now(UTC)
    schema = _schema_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "schema_type": MULTI_REVIEWER_SCHEMA_TYPE,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "review_set_type": MULTI_REVIEWER_REVIEW_SET_TYPE,
        "review_set_version": MULTI_REVIEWER_REVIEW_SET_VERSION,
        "disagreement_dimension_count": len(DISAGREEMENT_DIMENSIONS),
        "schema": schema,
        "warnings": dict(MULTI_REVIEWER_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(schema, indent=2, sort_keys=True), encoding="utf-8")
        result["schema_output"] = str(path)
    return result


def build_multi_reviewer_review_set_template(
    *,
    point_manifest_id: str | None = None,
    media_id: str | None = None,
    replay_url: str | None = None,
    associated_run_ids: dict[str, str] | None = None,
    reviewer_count: int = 2,
    output_path: str | Path | None = DEFAULT_MULTI_REVIEWER_REVIEW_SET_TEMPLATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a blank multi-reviewer review-set template."""

    generated_at = generated_at or datetime.now(UTC)
    safe_reviewer_count = max(1, reviewer_count)
    review_set = {
        "review_set_type": MULTI_REVIEWER_REVIEW_SET_TYPE,
        "review_set_version": MULTI_REVIEWER_REVIEW_SET_VERSION,
        "schema_type": MULTI_REVIEWER_SCHEMA_TYPE,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "generated_at": generated_at.isoformat(),
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "replay_url": replay_url,
        "associated_run_ids": _string_dict(associated_run_ids),
        "reviewer_entries": [
            _template_reviewer_entry(
                reviewer_index=index,
                point_manifest_id=point_manifest_id,
                media_id=media_id,
                replay_url=replay_url,
                associated_run_ids=associated_run_ids,
            )
            for index in range(1, safe_reviewer_count + 1)
        ],
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(MULTI_REVIEWER_WARNINGS),
            "template_is_not_a_completed_review_set": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "review_set_type": MULTI_REVIEWER_REVIEW_SET_TYPE,
        "review_set_version": MULTI_REVIEWER_REVIEW_SET_VERSION,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "reviewer_count": len(review_set["reviewer_entries"]),
        "review_set": review_set,
        "warnings": dict(MULTI_REVIEWER_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(review_set, indent=2, sort_keys=True), encoding="utf-8")
        result["review_set_output"] = str(path)
    return result


def validate_multi_reviewer_review_set(
    *,
    schema_path: str | Path = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    review_set_path: str | Path,
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    output_path: str | Path | None = None,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a multi-reviewer review set without resolving disagreement."""

    validated_at = validated_at or datetime.now(UTC)
    schema_loaded = _load_json(schema_path, label="schema")
    if schema_loaded.get("ok") is False:
        return schema_loaded
    review_set_loaded = _load_json(review_set_path, label="review_set")
    if review_set_loaded.get("ok") is False:
        return review_set_loaded

    schema = _dict(schema_loaded["data"])
    review_set = _dict(review_set_loaded["data"])
    errors = _validate_schema_shape(schema)
    structural_warnings: list[dict[str, Any]] = []
    nested_validations: list[dict[str, Any]] = []
    if not errors:
        review_set_result = _validate_review_set_shape(
            review_set=review_set,
            review_label_schema_path=review_label_schema_path,
            reviewer_confidence_schema_path=reviewer_confidence_schema_path,
        )
        errors.extend(_list(review_set_result.get("errors")))
        structural_warnings.extend(_list(review_set_result.get("structural_warnings")))
        nested_validations.extend(_list(review_set_result.get("nested_validations")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "multi_reviewer_review_set_validation",
        "validation_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "validated_at": validated_at.isoformat(),
        "schema_path": str(Path(schema_path)),
        "review_set_path": str(Path(review_set_path)),
        "review_label_schema_path": (
            str(Path(review_label_schema_path)) if review_label_schema_path else None
        ),
        "reviewer_confidence_schema_path": (
            str(Path(reviewer_confidence_schema_path))
            if reviewer_confidence_schema_path
            else None
        ),
        "schema_type": MULTI_REVIEWER_SCHEMA_TYPE,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "nested_validations": nested_validations,
        "warnings": dict(MULTI_REVIEWER_WARNINGS),
        "known_limitations": [
            "Validation checks structure and referenced bundle structure only.",
            "Validation does not infer missing labels or confidence values.",
            "Validation does not create labels or confidence scores.",
            "Validation does not say which reviewer is correct.",
            "Validation does not resolve disagreements.",
            "Validation does not score, rank, or assess reviewer quality.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_reviewer_disagreement_report(
    *,
    schema_path: str | Path = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    review_set_path: str | Path,
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_REVIEWER_DISAGREEMENT_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural disagreement report without resolving reviewer differences."""

    generated_at = generated_at or datetime.now(UTC)
    validation = validate_multi_reviewer_review_set(
        schema_path=schema_path,
        review_set_path=review_set_path,
        review_label_schema_path=review_label_schema_path,
        reviewer_confidence_schema_path=reviewer_confidence_schema_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_review_set",
            "validation": validation,
            "warnings": dict(MULTI_REVIEWER_WARNINGS),
        }

    review_set_loaded = _load_json(review_set_path, label="review_set")
    if review_set_loaded.get("ok") is False:
        return review_set_loaded
    review_set = _dict(review_set_loaded["data"])
    reviewer_entries = [_sanitize_reviewer_entry(item) for item in _entries(review_set)]
    reviewer_contexts = [_reviewer_context(item) for item in reviewer_entries]
    label_keys = _label_keys(reviewer_contexts)

    comparison_groups = [
        _comparison_group(label_key=label_key, reviewer_contexts=reviewer_contexts)
        for label_key in label_keys
    ]
    summary = _report_summary(
        reviewer_count=len(reviewer_entries),
        comparison_groups=comparison_groups,
    )
    report = {
        "disagreement_report_type": DISAGREEMENT_REPORT_TYPE,
        "disagreement_report_version": DISAGREEMENT_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_review_set_path": str(Path(review_set_path)),
        "point_manifest_id": review_set.get("point_manifest_id"),
        "media_id": review_set.get("media_id"),
        "replay_url": review_set.get("replay_url"),
        "reviewer_count": len(reviewer_entries),
        "reviewer_entries": reviewer_entries,
        "comparison_groups": comparison_groups,
        "summary": summary,
        "structural_warnings": validation.get("structural_warnings", []),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(MULTI_REVIEWER_WARNINGS),
            "report_is_structural_only": True,
            "conflicting_human_inputs_are_not_resolved": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "disagreement_report_type": DISAGREEMENT_REPORT_TYPE,
        "disagreement_report_version": DISAGREEMENT_REPORT_VERSION,
        "reviewer_count": len(reviewer_entries),
        "comparison_group_count": len(comparison_groups),
        "summary": summary,
        "report": report,
        "warnings": dict(MULTI_REVIEWER_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _schema_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "schema_type": MULTI_REVIEWER_SCHEMA_TYPE,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "exported_at": exported_at.isoformat(),
        "review_set_type": MULTI_REVIEWER_REVIEW_SET_TYPE,
        "review_set_version": MULTI_REVIEWER_REVIEW_SET_VERSION,
        "reviewer_identity_policy": {
            "pseudonymous_identifiers_only": True,
            "allowed_reviewer_identity_fields": [
                "reviewer_id",
                "reviewer_role",
                "reviewer_session_id",
                "reviewer_notes",
            ],
            "required_reviewer_identity_fields": ["reviewer_id"],
            "real_name_required": False,
            "email_required": False,
            "reviewer_ranking_allowed": False,
            "reviewer_quality_scoring_allowed": False,
            "reviewer_correctness_scoring_allowed": False,
            "reviewer_authority_scoring_allowed": False,
            "disallowed_reviewer_identity_fields": sorted(
                DISALLOWED_REVIEWER_IDENTITY_FIELDS
            ),
            "warnings": dict(REVIEWER_ENTRY_WARNINGS),
        },
        "reviewer_entry_definitions": [
            _reviewer_entry_definition(item) for item in REVIEWER_ENTRY_DEFINITIONS
        ],
        "disagreement_dimensions": [
            _disagreement_dimension(item) for item in DISAGREEMENT_DIMENSIONS
        ],
        "disagreement_value_sets": [
            {
                "key": "disagreement_status_values",
                "name": "Disagreement status values",
                "description": "Neutral structural disagreement statuses.",
                "allowed_values": list(DISAGREEMENT_VALUES),
                "default_value": "not_assessed",
                "warnings": {
                    "value_set_is_not_truth": True,
                    "does_not_resolve_disagreement": True,
                    "review_support_only": True,
                    "no_adjudication": True,
                },
            }
        ],
        "provenance_requirements": {
            "review_set_type_required": MULTI_REVIEWER_REVIEW_SET_TYPE,
            "review_set_version_required": MULTI_REVIEWER_REVIEW_SET_VERSION,
            "review_label_schema_version_supported": REVIEW_LABEL_SCHEMA_VERSION,
            "reviewer_confidence_schema_version_supported": (
                REVIEWER_CONFIDENCE_SCHEMA_VERSION
            ),
            "point_manifest_id_recommended": True,
            "media_id_recommended": True,
            "replay_url_recommended": True,
            "associated_run_ids_allowed": [
                "event_candidate_run_id",
                "trajectory_3d_run_id",
                "camera_geometry_id",
            ],
            "review_label_bundle_path_or_ref_allowed": True,
            "reviewer_confidence_bundle_path_or_ref_allowed": True,
            "provenance_only": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "reviewer_ids_required": True,
            "reviewer_ids_unique_within_review_set": True,
            "referenced_review_label_bundles_validated_when_paths_available": True,
            "referenced_confidence_bundles_validated_when_paths_available": True,
            "missing_bundle_refs_are_structural_warnings": True,
            "human_provided_only_required": True,
            "machine_inferred_must_be_false": True,
            "does_not_infer_missing_labels": True,
            "does_not_create_labels": True,
            "does_not_validate_truth": True,
            "does_not_validate_correctness": True,
            "does_not_resolve_disagreements": True,
            "does_not_score_reviewers": True,
            "does_not_rank_reviewers": True,
            "forbidden_fields": sorted(FORBIDDEN_MULTI_REVIEWER_FIELDS),
            "disallowed_reviewer_identity_fields": sorted(
                DISALLOWED_REVIEWER_IDENTITY_FIELDS
            ),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(MULTI_REVIEWER_WARNINGS),
    }


def _reviewer_entry_definition(definition: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": definition["key"],
        "description": definition["description"],
        "required": definition["required"],
        "human_provided_only": True,
        "machine_inferred": False,
        "warnings": dict(REVIEWER_ENTRY_WARNINGS),
    }


def _disagreement_dimension(dimension: dict[str, str]) -> dict[str, Any]:
    return {
        "key": dimension["key"],
        "name": dimension["name"],
        "description": dimension["description"],
        "allowed_values": list(DISAGREEMENT_VALUES),
        "required": False,
        "structural_only": True,
        "does_not_resolve_disagreement": True,
        "warnings": {
            "dimension_is_not_truth": True,
            "no_adjudication": True,
            "review_support_only": True,
            "does_not_validate_correctness": True,
        },
    }


def _template_reviewer_entry(
    *,
    reviewer_index: int,
    point_manifest_id: str | None,
    media_id: str | None,
    replay_url: str | None,
    associated_run_ids: dict[str, str] | None,
) -> dict[str, Any]:
    return {
        "reviewer_id": f"reviewer_{reviewer_index}",
        "reviewer_role": None,
        "reviewer_session_id": None,
        "reviewer_notes": None,
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "replay_url": replay_url,
        "review_label_bundle_path": None,
        "review_label_bundle_ref": None,
        "reviewer_confidence_bundle_path": None,
        "reviewer_confidence_bundle_ref": None,
        "associated_run_ids": _string_dict(associated_run_ids),
        "submitted_at": None,
        "human_provided_only": True,
        "machine_inferred": False,
        "template_entry": True,
        "warnings": dict(REVIEWER_ENTRY_WARNINGS),
    }


def _validate_schema_shape(schema: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if schema.get("schema_type") != MULTI_REVIEWER_SCHEMA_TYPE:
        errors.append(_error("invalid_schema_type", "schema_type", schema.get("schema_type")))
    if schema.get("schema_version") != MULTI_REVIEWER_SCHEMA_VERSION:
        errors.append(
            _error("invalid_schema_version", "schema_version", schema.get("schema_version"))
        )
    for section in (
        "review_set_type",
        "review_set_version",
        "reviewer_identity_policy",
        "reviewer_entry_definitions",
        "disagreement_dimensions",
        "disagreement_value_sets",
        "provenance_requirements",
        "validation_rules",
        "warnings",
    ):
        if section not in schema:
            errors.append(_error("missing_schema_section", section, None))
    errors.extend(_forbidden_field_errors(schema, path="schema"))
    policy = _dict(schema.get("reviewer_identity_policy"))
    allowed_fields = set(_string_list(policy.get("allowed_reviewer_identity_fields")))
    if "reviewer_id" not in allowed_fields:
        errors.append(_error("reviewer_id_not_allowed", "reviewer_identity_policy", policy))
    if policy.get("pseudonymous_identifiers_only") is not True:
        errors.append(
            _error(
                "reviewer_identity_must_be_pseudonymous",
                "reviewer_identity_policy",
                policy,
            )
        )
    if (
        policy.get("real_name_required") is not False
        or policy.get("email_required") is not False
    ):
        errors.append(
            _error("real_identity_must_not_be_required", "reviewer_identity_policy", policy)
        )
    if policy.get("reviewer_ranking_allowed") is not False:
        errors.append(
            _error(
                "reviewer_ranking_must_not_be_allowed",
                "reviewer_identity_policy",
                policy,
            )
        )
    if policy.get("reviewer_quality_scoring_allowed") is not False:
        errors.append(
            _error(
                "reviewer_quality_scoring_must_not_be_allowed",
                "reviewer_identity_policy",
                policy,
            )
        )
    if policy.get("reviewer_correctness_scoring_allowed") is not False:
        errors.append(
            _error(
                "reviewer_correctness_scoring_must_not_be_allowed",
                "reviewer_identity_policy",
                policy,
            )
        )
    if errors:
        return errors
    known_dimensions = {item["key"] for item in DISAGREEMENT_DIMENSIONS}
    schema_dimensions = {
        item.get("key")
        for item in _list(schema.get("disagreement_dimensions"))
        if isinstance(item, dict)
    }
    if not known_dimensions <= schema_dimensions:
        errors.append(
            _error(
                "missing_disagreement_dimensions",
                "disagreement_dimensions",
                sorted(known_dimensions - schema_dimensions),
            )
        )
    allowed_values = set()
    for value_set in _list(schema.get("disagreement_value_sets")):
        if isinstance(value_set, dict):
            allowed_values.update(_string_list(value_set.get("allowed_values")))
    if not set(DISAGREEMENT_VALUES) <= allowed_values:
        errors.append(
            _error(
                "missing_disagreement_values",
                "disagreement_value_sets",
                sorted(set(DISAGREEMENT_VALUES) - allowed_values),
            )
        )
    return errors


def _validate_review_set_shape(
    *,
    review_set: dict[str, Any],
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
) -> dict[str, Any]:
    errors = _forbidden_field_errors(review_set, path="review_set")
    errors.extend(_disallowed_identity_field_errors(review_set, path="review_set"))
    structural_warnings: list[dict[str, Any]] = []
    nested_validations: list[dict[str, Any]] = []
    if review_set.get("review_set_type") != MULTI_REVIEWER_REVIEW_SET_TYPE:
        errors.append(
            _error("invalid_review_set_type", "review_set_type", review_set.get("review_set_type"))
        )
    if review_set.get("review_set_version") != MULTI_REVIEWER_REVIEW_SET_VERSION:
        errors.append(
            _error(
                "invalid_review_set_version",
                "review_set_version",
                review_set.get("review_set_version"),
            )
        )
    if review_set.get("schema_version") != MULTI_REVIEWER_SCHEMA_VERSION:
        errors.append(
            _error(
                "invalid_review_set_schema_version",
                "schema_version",
                review_set.get("schema_version"),
            )
        )
    entries = review_set.get("reviewer_entries")
    if not isinstance(entries, list):
        errors.append(_error("reviewer_entries_must_be_list", "reviewer_entries", entries))
        return {
            "errors": errors,
            "structural_warnings": structural_warnings,
            "nested_validations": nested_validations,
        }
    seen_reviewer_ids: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"reviewer_entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("reviewer_entry_must_be_object", path, entry))
            continue
        reviewer_id = _string_or_none(entry.get("reviewer_id"))
        if reviewer_id is None:
            errors.append(
                _error("missing_reviewer_id", f"{path}.reviewer_id", entry.get("reviewer_id"))
            )
        elif reviewer_id in seen_reviewer_ids:
            errors.append(_error("duplicate_reviewer_id", f"{path}.reviewer_id", reviewer_id))
        else:
            seen_reviewer_ids.add(reviewer_id)
        if entry.get("human_provided_only") is not True:
            errors.append(
                _error(
                    "reviewer_entry_must_be_human_provided_only",
                    f"{path}.human_provided_only",
                    entry.get("human_provided_only"),
                )
            )
        if entry.get("machine_inferred", False) is not False:
            errors.append(
                _error(
                    "reviewer_entry_must_not_be_machine_inferred",
                    f"{path}.machine_inferred",
                    entry.get("machine_inferred"),
                )
            )
        label_path = _string_or_none(entry.get("review_label_bundle_path"))
        confidence_path = _string_or_none(entry.get("reviewer_confidence_bundle_path"))
        if (
            label_path is None
            and _string_or_none(entry.get("review_label_bundle_ref")) is None
        ):
            structural_warnings.append(
                _warning("missing_review_bundle", f"{path}.review_label_bundle_path", reviewer_id)
            )
        if (
            confidence_path is None
            and _string_or_none(entry.get("reviewer_confidence_bundle_ref")) is None
        ):
            structural_warnings.append(
                _warning(
                    "missing_confidence_bundle",
                    f"{path}.reviewer_confidence_bundle_path",
                    reviewer_id,
                )
            )
        if label_path is not None:
            nested = validate_review_label_bundle(
                schema_path=review_label_schema_path or DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
                bundle_path=label_path,
                output_path=None,
            )
            nested_validations.append(
                _nested_validation(
                    reviewer_id=reviewer_id,
                    bundle_type="review_label_bundle",
                    path=label_path,
                    result=nested,
                )
            )
            if nested.get("ok") is not True:
                errors.append(
                    _error(
                        "invalid_review_label_bundle",
                        f"{path}.review_label_bundle_path",
                        nested,
                    )
                )
        if confidence_path is not None:
            nested = validate_reviewer_confidence_bundle(
                schema_path=(
                    reviewer_confidence_schema_path
                    or DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
                ),
                bundle_path=confidence_path,
                review_label_schema_path=review_label_schema_path,
                output_path=None,
            )
            nested_validations.append(
                _nested_validation(
                    reviewer_id=reviewer_id,
                    bundle_type="reviewer_confidence_bundle",
                    path=confidence_path,
                    result=nested,
                )
            )
            if nested.get("ok") is not True:
                errors.append(
                    _error(
                        "invalid_reviewer_confidence_bundle",
                        f"{path}.reviewer_confidence_bundle_path",
                        nested,
                    )
                )
    return {
        "errors": errors,
        "structural_warnings": structural_warnings,
        "nested_validations": nested_validations,
    }


def _nested_validation(
    *,
    reviewer_id: str | None,
    bundle_type: str,
    path: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "reviewer_id": reviewer_id,
        "bundle_type": bundle_type,
        "path": path,
        "ok": result.get("ok") is True,
        "status": result.get("status"),
        "error_count": result.get("error_count", 0),
    }


def _entries(review_set: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in _list(review_set.get("reviewer_entries")) if isinstance(item, dict)]


def _sanitize_reviewer_entry(entry: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "reviewer_id",
        "reviewer_role",
        "reviewer_session_id",
        "reviewer_notes",
        "point_manifest_id",
        "media_id",
        "replay_url",
        "review_label_bundle_path",
        "review_label_bundle_ref",
        "reviewer_confidence_bundle_path",
        "reviewer_confidence_bundle_ref",
        "associated_run_ids",
        "submitted_at",
        "human_provided_only",
        "machine_inferred",
        "warnings",
    }
    return {key: entry.get(key) for key in allowed if key in entry}


def _reviewer_context(entry: dict[str, Any]) -> dict[str, Any]:
    label_bundle = _load_review_label_bundle(_string_or_none(entry.get("review_label_bundle_path")))
    confidence_bundle = _load_confidence_bundle(
        _string_or_none(entry.get("reviewer_confidence_bundle_path"))
    )
    return {
        "entry": entry,
        "reviewer_id": entry.get("reviewer_id"),
        "label_bundle": label_bundle,
        "confidence_bundle": confidence_bundle,
    }


def _load_review_label_bundle(path: str | None) -> dict[str, Any]:
    if path is None:
        return {"available": False, "values": {}, "notes": {}, "bundle": None}
    loaded = _load_json(path, label="review_label_bundle")
    if loaded.get("ok") is False:
        return {"available": False, "values": {}, "notes": {}, "bundle": None, "load_error": loaded}
    bundle = _dict(loaded["data"])
    values: dict[str, str] = {}
    notes: dict[str, str] = {}
    for entry in _list(bundle.get("label_entries")):
        if not isinstance(entry, dict):
            continue
        label_key = _string_or_none(entry.get("label_key"))
        if label_key is None:
            continue
        value = _string_or_none(entry.get("value"))
        if value is not None:
            values[label_key] = value
        note = _string_or_none(entry.get("reviewer_note"))
        if note is not None:
            notes[label_key] = note
    return {"available": True, "values": values, "notes": notes, "bundle": bundle}


def _load_confidence_bundle(path: str | None) -> dict[str, Any]:
    if path is None:
        return {"available": False, "values": {}, "bundle": None}
    loaded = _load_json(path, label="reviewer_confidence_bundle")
    if loaded.get("ok") is False:
        return {"available": False, "values": {}, "bundle": None, "load_error": loaded}
    bundle = _dict(loaded["data"])
    values: dict[str, dict[str, Any]] = {}
    for entry in _list(bundle.get("confidence_entries")):
        if not isinstance(entry, dict):
            continue
        label_key = _string_or_none(entry.get("label_key"))
        if label_key is None:
            continue
        values[label_key] = {
            "reviewer_confidence": entry.get("reviewer_confidence"),
            "ambiguity_level": entry.get("ambiguity_level"),
            "evidence_sufficiency": entry.get("evidence_sufficiency"),
            "requires_additional_review": entry.get("requires_additional_review"),
        }
    return {"available": True, "values": values, "bundle": bundle}


def _label_keys(reviewer_contexts: list[dict[str, Any]]) -> list[str]:
    keys = {definition["key"] for definition in REVIEW_LABEL_DEFINITIONS}
    for context in reviewer_contexts:
        keys.update(_dict(context["label_bundle"].get("values")).keys())
        keys.update(_dict(context["confidence_bundle"].get("values")).keys())
    return sorted(keys)


def _comparison_group(
    *,
    label_key: str,
    reviewer_contexts: list[dict[str, Any]],
) -> dict[str, Any]:
    reviewer_values: list[dict[str, Any]] = []
    confidence_values: list[dict[str, Any]] = []
    ambiguity_values: list[dict[str, Any]] = []
    evidence_sufficiency_values: list[dict[str, Any]] = []
    note_values: list[dict[str, Any]] = []
    dimensions: list[str] = []
    notes: set[str] = set()

    for context in reviewer_contexts:
        reviewer_id = context.get("reviewer_id")
        label_bundle = _dict(context.get("label_bundle"))
        confidence_bundle = _dict(context.get("confidence_bundle"))
        label_values = _dict(label_bundle.get("values"))
        label_notes = _dict(label_bundle.get("notes"))
        confidence_map = _dict(confidence_bundle.get("values"))
        confidence_entry = _dict(confidence_map.get(label_key))

        reviewer_values.append(
            {
                "reviewer_id": reviewer_id,
                "value": label_values.get(label_key, "missing_reviewer_input"),
                "source_available": label_bundle.get("available") is True,
            }
        )
        confidence_values.append(
            {
                "reviewer_id": reviewer_id,
                "value": confidence_entry.get("reviewer_confidence", "missing_reviewer_input"),
                "source_available": confidence_bundle.get("available") is True,
            }
        )
        ambiguity_values.append(
            {
                "reviewer_id": reviewer_id,
                "value": confidence_entry.get("ambiguity_level", "missing_reviewer_input"),
                "source_available": confidence_bundle.get("available") is True,
            }
        )
        evidence_sufficiency_values.append(
            {
                "reviewer_id": reviewer_id,
                "value": confidence_entry.get("evidence_sufficiency", "missing_reviewer_input"),
                "source_available": confidence_bundle.get("available") is True,
            }
        )
        note_values.append(
            {
                "reviewer_id": reviewer_id,
                "value": label_notes.get(label_key),
                "source_available": label_bundle.get("available") is True,
            }
        )
        if label_bundle.get("available") is not True:
            dimensions.append("missing_review_bundle")
            notes.add("missing_reviewer_input")
        if confidence_bundle.get("available") is not True:
            dimensions.append("missing_confidence_bundle")
            notes.add("missing_reviewer_input")
        if confidence_entry.get("requires_additional_review") == "required":
            notes.add("needs_additional_review")
        if _context_has_provenance_mismatch(context):
            dimensions.append("provenance_mismatch")
            notes.add("needs_additional_review")

    if _has_value_disagreement(reviewer_values):
        dimensions.append("label_value_disagreement")
        notes.add("conflicting_human_inputs")
    if _has_value_disagreement(confidence_values):
        dimensions.append("confidence_disagreement")
        notes.add("conflicting_human_inputs")
    if _has_value_disagreement(ambiguity_values):
        dimensions.append("ambiguity_disagreement")
        notes.add("conflicting_human_inputs")
    if _has_value_disagreement(evidence_sufficiency_values):
        dimensions.append("evidence_sufficiency_disagreement")
        notes.add("conflicting_human_inputs")
    if _has_note_difference(note_values):
        dimensions.append("reviewer_note_difference")
    if _has_not_assessed_difference(
        reviewer_values
        + confidence_values
        + ambiguity_values
        + evidence_sufficiency_values
    ):
        dimensions.append("not_assessed_difference")
        notes.add("needs_additional_review")

    unique_dimensions = sorted(set(dimensions))
    disagreement_dimensions = [
        {
            "dimension": dimension,
            "value": _dimension_value(dimension),
            "structural_only": True,
        }
        for dimension in unique_dimensions
    ]
    disagreement_observed = any(
        dimension
        in {
            "label_value_disagreement",
            "confidence_disagreement",
            "ambiguity_disagreement",
            "evidence_sufficiency_disagreement",
            "reviewer_note_difference",
            "provenance_mismatch",
        }
        for dimension in unique_dimensions
    )
    missing_input_observed = any(
        dimension in {"missing_review_bundle", "missing_confidence_bundle"}
        for dimension in unique_dimensions
    )
    requires_additional_review = disagreement_observed or missing_input_observed
    if requires_additional_review:
        notes.add("needs_additional_review")
    if not unique_dimensions:
        notes.add("no_disagreement_observed")
    return {
        "label_key": label_key,
        "reviewer_values": reviewer_values,
        "confidence_values": confidence_values,
        "ambiguity_values": ambiguity_values,
        "evidence_sufficiency_values": evidence_sufficiency_values,
        "disagreement_dimensions": disagreement_dimensions,
        "disagreement_observed": disagreement_observed,
        "requires_additional_review": requires_additional_review,
        "report_notes": sorted(notes),
        "warnings": {
            "structural_disagreement_only": True,
            "does_not_identify_correct_reviewer": True,
            "does_not_resolve_disagreement": True,
            "no_adjudication": True,
        },
    }


def _dimension_value(dimension: str) -> str:
    if dimension in {"missing_review_bundle", "missing_confidence_bundle"}:
        return "missing_reviewer_input"
    if dimension == "not_assessed_difference":
        return "partial_disagreement"
    if dimension == "provenance_mismatch":
        return "ambiguous"
    return "disagreement_observed"


def _has_value_disagreement(values: list[dict[str, Any]]) -> bool:
    comparable = {
        item.get("value")
        for item in values
        if item.get("value") not in {None, "missing_reviewer_input", "not_assessed"}
    }
    return len(comparable) > 1


def _has_note_difference(values: list[dict[str, Any]]) -> bool:
    comparable = {item.get("value") for item in values if item.get("value")}
    return len(comparable) > 1


def _has_not_assessed_difference(values: list[dict[str, Any]]) -> bool:
    raw_values = [
        item.get("value")
        for item in values
        if item.get("value") not in {None, "missing_reviewer_input"}
    ]
    return "not_assessed" in raw_values and len(set(raw_values)) > 1


def _context_has_provenance_mismatch(context: dict[str, Any]) -> bool:
    entry = _dict(context.get("entry"))
    for bundle_key in ("label_bundle", "confidence_bundle"):
        bundle_context = _dict(context.get(bundle_key))
        bundle = _dict(bundle_context.get("bundle"))
        if not bundle:
            continue
        for field in ("point_manifest_id", "media_id", "replay_url"):
            entry_value = entry.get(field)
            bundle_value = bundle.get(field)
            if entry_value and bundle_value and entry_value != bundle_value:
                return True
    return False


def _report_summary(
    *,
    reviewer_count: int,
    comparison_groups: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "reviewer_count": reviewer_count,
        "label_key_count": len(comparison_groups),
        "disagreement_observed_count": sum(
            1 for group in comparison_groups if group.get("disagreement_observed") is True
        ),
        "missing_input_count": sum(
            1
            for group in comparison_groups
            if any(
                item.get("dimension") in {"missing_review_bundle", "missing_confidence_bundle"}
                for item in _list(group.get("disagreement_dimensions"))
            )
        ),
        "requires_additional_review_count": sum(
            1 for group in comparison_groups if group.get("requires_additional_review") is True
        ),
    }


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}"
            if key in FORBIDDEN_MULTI_REVIEWER_FIELDS:
                errors.append(_error("forbidden_field", next_path, key))
            errors.extend(_forbidden_field_errors(item, path=next_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_forbidden_field_errors(item, path=f"{path}[{index}]"))
    return errors


def _disallowed_identity_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}"
            if key in DISALLOWED_REVIEWER_IDENTITY_FIELDS:
                errors.append(_error("disallowed_reviewer_identity_field", next_path, key))
            errors.extend(_disallowed_identity_field_errors(item, path=next_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_disallowed_identity_field_errors(item, path=f"{path}[{index}]"))
    return errors


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "does_not_judge_truth": True,
        "does_not_resolve_disagreement": True,
    }


def _warning(warning_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "warning_type": warning_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "does_not_judge_truth": True,
        "does_not_resolve_disagreement": True,
    }


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": MULTI_REVIEWER_BLUEPRINT,
        "blueprint_name": MULTI_REVIEWER_BLUEPRINT_NAME,
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
        "schema_type": MULTI_REVIEWER_SCHEMA_TYPE,
        "schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "warnings": dict(MULTI_REVIEWER_WARNINGS),
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
    return {str(key): item for key, item in value.items() if isinstance(item, str) and item}
