from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.multi_reviewer_disagreement import (
    DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    MULTI_REVIEWER_SCHEMA_TYPE,
    MULTI_REVIEWER_SCHEMA_VERSION,
)
from apps.worker.services.observation_quality_taxonomy import (
    DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
    OBSERVATION_QUALITY_TAXONOMY_TYPE,
    OBSERVATION_QUALITY_TAXONOMY_VERSION,
)
from apps.worker.services.review_label_schema import (
    DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    REVIEW_LABEL_SCHEMA_TYPE,
    REVIEW_LABEL_SCHEMA_VERSION,
)
from apps.worker.services.reviewer_confidence_schema import (
    DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    REVIEWER_CONFIDENCE_SCHEMA_TYPE,
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
)

INTENNSE_ALIGNMENT_CONTRACT_TYPE = "intennse_label_alignment_contract"
INTENNSE_ALIGNMENT_CONTRACT_VERSION = "v1"
INTENNSE_ALIGNMENT_BUNDLE_TYPE = "intennse_label_alignment_bundle"
INTENNSE_ALIGNMENT_BUNDLE_VERSION = "v1"
INTENNSE_ALIGNMENT_REPORT_TYPE = "intennse_label_alignment_report"
INTENNSE_ALIGNMENT_REPORT_VERSION = "v1"
INTENNSE_ALIGNMENT_BLUEPRINT = "blueprint_30"
INTENNSE_ALIGNMENT_BLUEPRINT_NAME = "intennse_label_alignment_contract_v1"

DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT = (
    ".data/contracts/intennse_label_alignment_contract_v1.json"
)
DEFAULT_INTENNSE_ALIGNMENT_TEMPLATE_OUTPUT = (
    ".data/exports/intennse_alignment_template.current.json"
)
DEFAULT_INTENNSE_ALIGNMENT_VALIDATION_OUTPUT = (
    ".data/exports/intennse_alignment_bundle.validation.json"
)
DEFAULT_INTENNSE_ALIGNMENT_REPORT_OUTPUT = (
    ".data/exports/intennse_alignment_report.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)

ALIGNMENT_STATUS_VALUES = [
    "not_assessed",
    "unknown",
    "aligned_by_reference",
    "partially_aligned",
    "not_aligned",
    "missing_tom_context",
    "missing_intennse_context",
    "requires_human_alignment_review",
    "not_applicable",
]

PROVENANCE_STATUS_VALUES = [
    "not_assessed",
    "unknown",
    "provenance_present",
    "provenance_partial",
    "provenance_missing",
    "conflicting_references",
    "not_applicable",
]

HUMAN_ALIGNMENT_REVIEW_VALUES = [
    "not_assessed",
    "unknown",
    "required",
    "not_required",
    "not_applicable",
]

ALIGNMENT_ENTITIES = (
    {
        "key": "point_manifest_alignment",
        "name": "Point manifest alignment",
        "description": (
            "Alignment between a TOM point manifest and an INTENNSE label bundle "
            "reference."
        ),
    },
    {
        "key": "replay_context_alignment",
        "name": "Replay context alignment",
        "description": (
            "Alignment between TOM replay URL/run context and external interpretation "
            "references."
        ),
    },
    {
        "key": "observation_quality_alignment",
        "name": "Observation quality alignment",
        "description": (
            "Alignment between TOM observation-quality structure and external "
            "interpretation context."
        ),
    },
    {
        "key": "review_label_alignment",
        "name": "Review label alignment",
        "description": (
            "Alignment between TOM human review-label bundles and external label "
            "references."
        ),
    },
    {
        "key": "reviewer_confidence_alignment",
        "name": "Reviewer confidence alignment",
        "description": (
            "Alignment between TOM reviewer confidence/ambiguity bundles and external "
            "label references."
        ),
    },
    {
        "key": "multi_reviewer_disagreement_alignment",
        "name": "Multi-reviewer disagreement alignment",
        "description": (
            "Alignment between TOM multi-reviewer disagreement reports and external "
            "review references."
        ),
    },
    {
        "key": "expert_interpretation_placeholder",
        "name": "Expert interpretation placeholder",
        "description": "Placeholder for future INTENNSE expert interpretation references.",
    },
    {
        "key": "dataset_export_alignment",
        "name": "Dataset export alignment",
        "description": "Alignment between TOM provenance exports and external dataset references.",
    },
)

ALIGNMENT_FIELDS = (
    {
        "key": "tom_point_manifest_id",
        "description": "TOM point manifest identifier, when known.",
        "required": False,
    },
    {
        "key": "tom_media_id",
        "description": "TOM media identifier, when known.",
        "required": False,
    },
    {
        "key": "tom_replay_url",
        "description": "Replay URL for human review, when available.",
        "required": False,
    },
    {
        "key": "tom_associated_run_ids",
        "description": "Optional TOM event, 3D, and camera geometry run IDs.",
        "required": False,
    },
    {
        "key": "tom_review_label_bundle_ref",
        "description": "Reference to a TOM structured review-label bundle.",
        "required": False,
    },
    {
        "key": "tom_reviewer_confidence_bundle_ref",
        "description": "Reference to a TOM reviewer confidence/ambiguity bundle.",
        "required": False,
    },
    {
        "key": "tom_multi_reviewer_review_set_ref",
        "description": "Reference to a TOM multi-reviewer review-set bundle.",
        "required": False,
    },
    {
        "key": "tom_disagreement_report_ref",
        "description": "Reference to a TOM structural disagreement report.",
        "required": False,
    },
    {
        "key": "intennse_label_bundle_ref",
        "description": (
            "External reference to a future INTENNSE expert interpretation label bundle."
        ),
        "required": False,
    },
    {
        "key": "intennse_schema_version",
        "description": "External INTENNSE schema version, when supplied.",
        "required": False,
    },
    {
        "key": "alignment_status",
        "description": "Human-provided structural alignment status.",
        "required": True,
        "value_set": "alignment_status_values",
    },
    {
        "key": "alignment_notes",
        "description": "Optional human-provided alignment note.",
        "required": False,
    },
    {
        "key": "provenance_status",
        "description": "Human-provided provenance status for this alignment reference.",
        "required": True,
        "value_set": "provenance_status_values",
    },
    {
        "key": "requires_human_alignment_review",
        "description": (
            "Human-provided status for whether another alignment review pass is "
            "requested."
        ),
        "required": True,
        "value_set": "human_alignment_review_values",
    },
)

FORBIDDEN_INTENNSE_ALIGNMENT_FIELDS = {
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
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "reviewer_score",
    "reviewer_rank",
    "reviewer_quality_score",
    "reviewer_reliability",
    "disagreement_resolution",
}

ALIGNMENT_WARNINGS = {
    "alignment_is_not_truth": True,
    "intennse_alignment_is_not_adjudication": True,
    "does_not_import_intennse_truth": True,
    "does_not_create_intennse_labels": True,
    "does_not_create_tom_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_resolve_disagreement": True,
    "does_not_score_reviewers": True,
    "does_not_validate_correctness": True,
    "observation_only": True,
    "review_support_only": True,
    "provenance_only": True,
    "no_adjudication": True,
    "not_training_truth": True,
    "not_generalization_claim": True,
}

ENTRY_WARNINGS = {
    "alignment_is_not_truth": True,
    "human_provided_only": True,
    "machine_inferred": False,
    "provenance_only": True,
    "no_adjudication": True,
    "does_not_create_intennse_labels": True,
    "does_not_create_tom_labels": True,
    "does_not_validate_correctness": True,
    "does_not_resolve_disagreement": True,
}


def export_intennse_label_alignment_contract(
    *,
    output_path: str | Path | None = DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen INTENNSE label alignment contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": INTENNSE_ALIGNMENT_CONTRACT_TYPE,
        "contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "alignment_bundle_type": INTENNSE_ALIGNMENT_BUNDLE_TYPE,
        "alignment_bundle_version": INTENNSE_ALIGNMENT_BUNDLE_VERSION,
        "alignment_entity_count": len(ALIGNMENT_ENTITIES),
        "alignment_field_count": len(ALIGNMENT_FIELDS),
        "contract": contract,
        "warnings": dict(ALIGNMENT_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_intennse_alignment_template(
    *,
    point_manifest_id: str | None = None,
    media_id: str | None = None,
    replay_url: str | None = None,
    associated_run_ids: dict[str, str] | None = None,
    tom_review_label_bundle_ref: str | None = None,
    tom_reviewer_confidence_bundle_ref: str | None = None,
    tom_multi_reviewer_review_set_ref: str | None = None,
    tom_disagreement_report_ref: str | None = None,
    intennse_label_bundle_ref: str | None = None,
    intennse_schema_version: str | None = None,
    output_path: str | Path | None = DEFAULT_INTENNSE_ALIGNMENT_TEMPLATE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a blank INTENNSE alignment bundle template."""

    generated_at = generated_at or datetime.now(UTC)
    tom_refs = {
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "replay_url": replay_url,
        "associated_run_ids": _string_dict(associated_run_ids),
        "review_label_bundle_ref": tom_review_label_bundle_ref,
        "reviewer_confidence_bundle_ref": tom_reviewer_confidence_bundle_ref,
        "multi_reviewer_review_set_ref": tom_multi_reviewer_review_set_ref,
        "disagreement_report_ref": tom_disagreement_report_ref,
    }
    intennse_refs = {
        "label_bundle_ref": intennse_label_bundle_ref,
        "schema_version": intennse_schema_version,
    }
    bundle = {
        "alignment_bundle_type": INTENNSE_ALIGNMENT_BUNDLE_TYPE,
        "alignment_bundle_version": INTENNSE_ALIGNMENT_BUNDLE_VERSION,
        "contract_type": INTENNSE_ALIGNMENT_CONTRACT_TYPE,
        "contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "generated_at": generated_at.isoformat(),
        "tom_schema_refs": _tom_schema_refs(),
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "replay_url": replay_url,
        "associated_run_ids": _string_dict(associated_run_ids),
        "tom_review_label_bundle_ref": tom_review_label_bundle_ref,
        "tom_reviewer_confidence_bundle_ref": tom_reviewer_confidence_bundle_ref,
        "tom_multi_reviewer_review_set_ref": tom_multi_reviewer_review_set_ref,
        "tom_disagreement_report_ref": tom_disagreement_report_ref,
        "intennse_label_bundle_ref": intennse_label_bundle_ref,
        "intennse_schema_version": intennse_schema_version,
        "alignment_entries": [
            _template_alignment_entry(
                entity=entity["key"],
                tom_refs=tom_refs,
                intennse_refs=intennse_refs,
            )
            for entity in ALIGNMENT_ENTITIES
        ],
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(ALIGNMENT_WARNINGS),
            "template_is_not_a_completed_alignment": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "alignment_bundle_type": INTENNSE_ALIGNMENT_BUNDLE_TYPE,
        "alignment_bundle_version": INTENNSE_ALIGNMENT_BUNDLE_VERSION,
        "contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "alignment_entry_count": len(bundle["alignment_entries"]),
        "alignment_bundle": bundle,
        "warnings": dict(ALIGNMENT_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        result["alignment_bundle_output"] = str(path)
    return result


def validate_intennse_alignment_bundle(
    *,
    contract_path: str | Path = DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    bundle_path: str | Path,
    observation_quality_taxonomy_path: str | Path | None = (
        DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT
    ),
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    multi_reviewer_schema_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    output_path: str | Path | None = DEFAULT_INTENNSE_ALIGNMENT_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate an INTENNSE alignment bundle without importing or judging labels."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    bundle_loaded = _load_json(bundle_path, label="alignment_bundle")
    if bundle_loaded.get("ok") is False:
        return bundle_loaded

    contract = _dict(contract_loaded["data"])
    bundle = _dict(bundle_loaded["data"])
    errors = _validate_contract_shape(contract)
    structural_warnings: list[dict[str, Any]] = []
    tom_contract_validations: list[dict[str, Any]] = []

    if not errors:
        contract_result = _validate_referenced_tom_contracts(
            observation_quality_taxonomy_path=observation_quality_taxonomy_path,
            review_label_schema_path=review_label_schema_path,
            reviewer_confidence_schema_path=reviewer_confidence_schema_path,
            multi_reviewer_schema_path=multi_reviewer_schema_path,
        )
        errors.extend(_list(contract_result.get("errors")))
        structural_warnings.extend(_list(contract_result.get("structural_warnings")))
        tom_contract_validations.extend(_list(contract_result.get("validations")))
        bundle_result = _validate_alignment_bundle_shape(bundle=bundle)
        errors.extend(_list(bundle_result.get("errors")))
        structural_warnings.extend(_list(bundle_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "intennse_alignment_bundle_validation",
        "validation_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "bundle_path": str(Path(bundle_path)),
        "tom_contract_paths": {
            "observation_quality_taxonomy_path": (
                str(Path(observation_quality_taxonomy_path))
                if observation_quality_taxonomy_path
                else None
            ),
            "review_label_schema_path": (
                str(Path(review_label_schema_path)) if review_label_schema_path else None
            ),
            "reviewer_confidence_schema_path": (
                str(Path(reviewer_confidence_schema_path))
                if reviewer_confidence_schema_path
                else None
            ),
            "multi_reviewer_schema_path": (
                str(Path(multi_reviewer_schema_path)) if multi_reviewer_schema_path else None
            ),
        },
        "contract_type": INTENNSE_ALIGNMENT_CONTRACT_TYPE,
        "contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "alignment_bundle_type": INTENNSE_ALIGNMENT_BUNDLE_TYPE,
        "alignment_bundle_version": INTENNSE_ALIGNMENT_BUNDLE_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "tom_contract_validations": tom_contract_validations,
        "warnings": dict(ALIGNMENT_WARNINGS),
        "known_limitations": [
            "Validation checks alignment structure and referenced TOM contract versions only.",
            (
                "Validation treats INTENNSE references as external placeholders unless "
                "supplied by a future local fixture."
            ),
            "Validation does not infer missing TOM labels.",
            "Validation does not create INTENNSE labels.",
            "Validation does not say whether expert interpretation is correct.",
            "Validation does not resolve reviewer disagreement.",
            "Validation does not create truth.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_intennse_alignment_report(
    *,
    contract_path: str | Path = DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    bundle_path: str | Path,
    observation_quality_taxonomy_path: str | Path | None = (
        DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT
    ),
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    multi_reviewer_schema_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    output_path: str | Path | None = DEFAULT_INTENNSE_ALIGNMENT_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural alignment report without importing INTENNSE labels."""

    generated_at = generated_at or datetime.now(UTC)
    validation = validate_intennse_alignment_bundle(
        contract_path=contract_path,
        bundle_path=bundle_path,
        observation_quality_taxonomy_path=observation_quality_taxonomy_path,
        review_label_schema_path=review_label_schema_path,
        reviewer_confidence_schema_path=reviewer_confidence_schema_path,
        multi_reviewer_schema_path=multi_reviewer_schema_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_alignment_bundle",
            "validation": validation,
            "warnings": dict(ALIGNMENT_WARNINGS),
        }

    bundle_loaded = _load_json(bundle_path, label="alignment_bundle")
    if bundle_loaded.get("ok") is False:
        return bundle_loaded
    bundle = _dict(bundle_loaded["data"])
    entries = [_sanitize_alignment_entry(entry) for entry in _alignment_entries(bundle)]
    entry_reports = [_entry_report(entry) for entry in entries]
    summary = _report_summary(entry_reports=entry_reports)
    reference_summary = _reference_summary(bundle)
    report = {
        "alignment_report_type": INTENNSE_ALIGNMENT_REPORT_TYPE,
        "alignment_report_version": INTENNSE_ALIGNMENT_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_alignment_bundle_path": str(Path(bundle_path)),
        "contract_path": str(Path(contract_path)),
        "point_manifest_id": bundle.get("point_manifest_id"),
        "media_id": bundle.get("media_id"),
        "replay_url": bundle.get("replay_url"),
        "reference_summary": reference_summary,
        "alignment_entries": entry_reports,
        "summary": summary,
        "provenance_issues": _provenance_issues(entry_reports=entry_reports),
        "structural_warnings": validation.get("structural_warnings", []),
        "tom_contract_validations": validation.get("tom_contract_validations", []),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(ALIGNMENT_WARNINGS),
            "report_is_structural_only": True,
            "intennse_references_are_external_placeholders": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "alignment_report_type": INTENNSE_ALIGNMENT_REPORT_TYPE,
        "alignment_report_version": INTENNSE_ALIGNMENT_REPORT_VERSION,
        "alignment_entry_count": len(entry_reports),
        "summary": summary,
        "report": report,
        "warnings": dict(ALIGNMENT_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": INTENNSE_ALIGNMENT_CONTRACT_TYPE,
        "contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "alignment_bundle_type": INTENNSE_ALIGNMENT_BUNDLE_TYPE,
        "alignment_bundle_version": INTENNSE_ALIGNMENT_BUNDLE_VERSION,
        "report_type": INTENNSE_ALIGNMENT_REPORT_TYPE,
        "report_version": INTENNSE_ALIGNMENT_REPORT_VERSION,
        "tom_schema_refs": _tom_schema_refs(),
        "intennse_alignment_scope": {
            "purpose": (
                "Align TOM evidence/review/provenance structures with future INTENNSE "
                "expert interpretation references."
            ),
            "tom_role": "observable evidence substrate and provenance record",
            "intennse_role": "external structured human expert interpretation reference",
            "automatic_import_allowed": False,
            "automatic_label_creation_allowed": False,
            "automatic_conclusion_creation_allowed": False,
            "provenance_only": True,
            "review_support_only": True,
        },
        "alignment_entities": [
            _alignment_entity_definition(entity) for entity in ALIGNMENT_ENTITIES
        ],
        "alignment_fields": [_alignment_field_definition(field) for field in ALIGNMENT_FIELDS],
        "alignment_value_sets": [
            _value_set(
                key="alignment_status_values",
                name="Alignment status values",
                description="Neutral human-provided structural alignment statuses.",
                allowed_values=ALIGNMENT_STATUS_VALUES,
            ),
            _value_set(
                key="provenance_status_values",
                name="Provenance status values",
                description="Neutral human-provided provenance statuses.",
                allowed_values=PROVENANCE_STATUS_VALUES,
            ),
            _value_set(
                key="human_alignment_review_values",
                name="Human alignment review values",
                description=(
                    "Neutral values for whether another human alignment review pass is "
                    "requested."
                ),
                allowed_values=HUMAN_ALIGNMENT_REVIEW_VALUES,
            ),
        ],
        "provenance_requirements": {
            "tom_point_manifest_id_recommended": True,
            "tom_media_id_recommended": True,
            "tom_replay_url_recommended": True,
            "tom_associated_run_ids_allowed": [
                "event_candidate_run_id",
                "trajectory_3d_run_id",
                "camera_geometry_id",
            ],
            "tom_review_label_bundle_ref_allowed": True,
            "tom_reviewer_confidence_bundle_ref_allowed": True,
            "tom_multi_reviewer_review_set_ref_allowed": True,
            "tom_disagreement_report_ref_allowed": True,
            "intennse_label_bundle_ref_allowed": True,
            "intennse_references_are_external_placeholders": True,
            "provenance_only": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "referenced_tom_contract_versions_validated_when_paths_available": True,
            "intennse_references_treated_as_external_placeholders": True,
            "allowed_alignment_entities": [entity["key"] for entity in ALIGNMENT_ENTITIES],
            "allowed_alignment_status_values": list(ALIGNMENT_STATUS_VALUES),
            "allowed_provenance_status_values": list(PROVENANCE_STATUS_VALUES),
            "allowed_human_alignment_review_values": list(HUMAN_ALIGNMENT_REVIEW_VALUES),
            "human_provided_only_required": True,
            "machine_inferred_must_be_false": True,
            "does_not_infer_missing_tom_labels": True,
            "does_not_create_intennse_labels": True,
            "does_not_create_tom_labels": True,
            "does_not_validate_correctness": True,
            "does_not_resolve_disagreement": True,
            "does_not_create_truth": True,
            "forbidden_fields": sorted(FORBIDDEN_INTENNSE_ALIGNMENT_FIELDS),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(ALIGNMENT_WARNINGS),
    }


def _tom_schema_refs() -> dict[str, str]:
    return {
        "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
    }


def _alignment_entity_definition(entity: dict[str, str]) -> dict[str, Any]:
    return {
        "key": entity["key"],
        "name": entity["name"],
        "description": entity["description"],
        "structural_only": True,
        "human_alignment_review_supported": True,
        "warnings": dict(ENTRY_WARNINGS),
    }


def _alignment_field_definition(field: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": field["key"],
        "description": field["description"],
        "required": field["required"],
        "value_set": field.get("value_set"),
        "human_provided_only": True,
        "machine_inferred": False,
        "warnings": dict(ENTRY_WARNINGS),
    }


def _value_set(
    *,
    key: str,
    name: str,
    description: str,
    allowed_values: list[str],
) -> dict[str, Any]:
    return {
        "key": key,
        "name": name,
        "description": description,
        "allowed_values": list(allowed_values),
        "default_value": "not_assessed",
        "free_text": False,
        "warnings": {
            "value_set_is_not_truth": True,
            "provenance_only": True,
            "review_support_only": True,
            "no_adjudication": True,
        },
    }


def _template_alignment_entry(
    *,
    entity: str,
    tom_refs: dict[str, Any],
    intennse_refs: dict[str, Any],
) -> dict[str, Any]:
    return {
        "alignment_entity": entity,
        "tom_reference": _tom_reference_for_entity(entity=entity, refs=tom_refs),
        "intennse_reference": {
            "reference_type": "intennse_label_bundle",
            "intennse_label_bundle_ref": intennse_refs.get("label_bundle_ref"),
            "intennse_schema_version": intennse_refs.get("schema_version"),
            "external_placeholder": True,
        },
        "alignment_status": "not_assessed",
        "provenance_status": "not_assessed",
        "alignment_notes": None,
        "requires_human_alignment_review": "not_assessed",
        "human_provided_only": True,
        "machine_inferred": False,
        "template_entry": True,
        "warnings": dict(ENTRY_WARNINGS),
    }


def _tom_reference_for_entity(*, entity: str, refs: dict[str, Any]) -> dict[str, Any]:
    base = {
        "reference_type": entity,
        "point_manifest_id": refs.get("point_manifest_id"),
        "media_id": refs.get("media_id"),
        "replay_url": refs.get("replay_url"),
        "associated_run_ids": _string_dict(refs.get("associated_run_ids")),
    }
    if entity == "review_label_alignment":
        base["tom_review_label_bundle_ref"] = refs.get("review_label_bundle_ref")
    elif entity == "reviewer_confidence_alignment":
        base["tom_reviewer_confidence_bundle_ref"] = refs.get(
            "reviewer_confidence_bundle_ref"
        )
    elif entity == "multi_reviewer_disagreement_alignment":
        base["tom_multi_reviewer_review_set_ref"] = refs.get(
            "multi_reviewer_review_set_ref"
        )
        base["tom_disagreement_report_ref"] = refs.get("disagreement_report_ref")
    elif entity == "dataset_export_alignment":
        base["tom_review_label_bundle_ref"] = refs.get("review_label_bundle_ref")
        base["tom_reviewer_confidence_bundle_ref"] = refs.get(
            "reviewer_confidence_bundle_ref"
        )
        base["tom_multi_reviewer_review_set_ref"] = refs.get(
            "multi_reviewer_review_set_ref"
        )
        base["tom_disagreement_report_ref"] = refs.get("disagreement_report_ref")
    return base


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != INTENNSE_ALIGNMENT_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != INTENNSE_ALIGNMENT_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "tom_schema_refs",
        "intennse_alignment_scope",
        "alignment_entities",
        "alignment_fields",
        "alignment_value_sets",
        "provenance_requirements",
        "validation_rules",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors

    errors.extend(_schema_ref_errors(_dict(contract.get("tom_schema_refs")), path="contract"))
    known_entities = {entity["key"] for entity in ALIGNMENT_ENTITIES}
    contract_entities = {
        entity.get("key")
        for entity in _list(contract.get("alignment_entities"))
        if isinstance(entity, dict)
    }
    if not known_entities <= contract_entities:
        errors.append(
            _error(
                "missing_alignment_entities",
                "alignment_entities",
                sorted(known_entities - contract_entities),
            )
        )
    known_fields = {field["key"] for field in ALIGNMENT_FIELDS}
    contract_fields = {
        field.get("key")
        for field in _list(contract.get("alignment_fields"))
        if isinstance(field, dict)
    }
    if not known_fields <= contract_fields:
        errors.append(
            _error(
                "missing_alignment_fields",
                "alignment_fields",
                sorted(known_fields - contract_fields),
            )
        )
    value_sets = _value_set_map(contract)
    for key, expected_values in {
        "alignment_status_values": ALIGNMENT_STATUS_VALUES,
        "provenance_status_values": PROVENANCE_STATUS_VALUES,
        "human_alignment_review_values": HUMAN_ALIGNMENT_REVIEW_VALUES,
    }.items():
        actual_values = set(_string_list(_dict(value_sets.get(key)).get("allowed_values")))
        if not set(expected_values) <= actual_values:
            errors.append(
                _error(
                    "missing_alignment_value_set_values",
                    key,
                    sorted(set(expected_values) - actual_values),
                )
            )
    rules = _dict(contract.get("validation_rules"))
    expected_true_rules = (
        "structural_validation_only",
        "intennse_references_treated_as_external_placeholders",
        "human_provided_only_required",
        "does_not_create_intennse_labels",
        "does_not_create_tom_labels",
        "does_not_validate_correctness",
        "does_not_resolve_disagreement",
        "does_not_create_truth",
    )
    for rule in expected_true_rules:
        if rules.get(rule) is not True:
            errors.append(
                _error(
                    "invalid_validation_rule",
                    f"validation_rules.{rule}",
                    rules.get(rule),
                )
            )
    if rules.get("machine_inferred_must_be_false") is not True:
        errors.append(
            _error(
                "invalid_validation_rule",
                "validation_rules.machine_inferred_must_be_false",
                rules.get("machine_inferred_must_be_false"),
            )
        )
    return errors


def _validate_alignment_bundle_shape(bundle: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(bundle, path="alignment_bundle")
    structural_warnings: list[dict[str, Any]] = []
    if bundle.get("alignment_bundle_type") != INTENNSE_ALIGNMENT_BUNDLE_TYPE:
        errors.append(
            _error(
                "invalid_alignment_bundle_type",
                "alignment_bundle_type",
                bundle.get("alignment_bundle_type"),
            )
        )
    if bundle.get("alignment_bundle_version") != INTENNSE_ALIGNMENT_BUNDLE_VERSION:
        errors.append(
            _error(
                "invalid_alignment_bundle_version",
                "alignment_bundle_version",
                bundle.get("alignment_bundle_version"),
            )
        )
    if bundle.get("contract_version") != INTENNSE_ALIGNMENT_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_alignment_contract_version",
                "contract_version",
                bundle.get("contract_version"),
            )
        )
    errors.extend(_schema_ref_errors(_dict(bundle.get("tom_schema_refs")), path="alignment_bundle"))

    entries = bundle.get("alignment_entries")
    if not isinstance(entries, list):
        errors.append(_error("alignment_entries_must_be_list", "alignment_entries", entries))
        return {"errors": errors, "structural_warnings": structural_warnings}

    for index, entry in enumerate(entries):
        path = f"alignment_entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("alignment_entry_must_be_object", path, entry))
            continue
        entry_result = _validate_alignment_entry(entry=entry, path=path)
        errors.extend(_list(entry_result.get("errors")))
        structural_warnings.extend(_list(entry_result.get("structural_warnings")))
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_alignment_entry(*, entry: dict[str, Any], path: str) -> dict[str, Any]:
    errors = _forbidden_field_errors(entry, path=path)
    structural_warnings: list[dict[str, Any]] = []
    entity = _string_or_none(entry.get("alignment_entity"))
    if entity not in {item["key"] for item in ALIGNMENT_ENTITIES}:
        errors.append(_error("invalid_alignment_entity", f"{path}.alignment_entity", entity))
    if entry.get("alignment_status") not in ALIGNMENT_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_alignment_status",
                f"{path}.alignment_status",
                entry.get("alignment_status"),
            )
        )
    if entry.get("provenance_status") not in PROVENANCE_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_provenance_status",
                f"{path}.provenance_status",
                entry.get("provenance_status"),
            )
        )
    if entry.get("requires_human_alignment_review") not in HUMAN_ALIGNMENT_REVIEW_VALUES:
        errors.append(
            _error(
                "invalid_requires_human_alignment_review",
                f"{path}.requires_human_alignment_review",
                entry.get("requires_human_alignment_review"),
            )
        )
    if entry.get("human_provided_only") is not True:
        errors.append(
            _error(
                "alignment_entry_must_be_human_provided_only",
                f"{path}.human_provided_only",
                entry.get("human_provided_only"),
            )
        )
    if entry.get("machine_inferred", False) is not False:
        errors.append(
            _error(
                "alignment_entry_must_not_be_machine_inferred",
                f"{path}.machine_inferred",
                entry.get("machine_inferred"),
            )
        )
    tom_reference = _dict(entry.get("tom_reference"))
    intennse_reference = _dict(entry.get("intennse_reference"))
    if not tom_reference:
        errors.append(
            _error(
                "tom_reference_must_be_object",
                f"{path}.tom_reference",
                entry.get("tom_reference"),
            )
        )
    elif not _has_reference_value(tom_reference):
        structural_warnings.append(
            _warning("missing_tom_reference", f"{path}.tom_reference", entity)
        )
    if not intennse_reference:
        errors.append(
            _error(
                "intennse_reference_must_be_object",
                f"{path}.intennse_reference",
                entry.get("intennse_reference"),
            )
        )
    elif not _has_reference_value(intennse_reference, exclude_keys={"external_placeholder"}):
        structural_warnings.append(
            _warning(
                "missing_intennse_reference",
                f"{path}.intennse_reference",
                entity,
            )
        )
    if entry.get("provenance_status") in {
        "provenance_partial",
        "provenance_missing",
        "conflicting_references",
    }:
        structural_warnings.append(
            _warning(
                entry["provenance_status"],
                f"{path}.provenance_status",
                entity,
            )
        )
    if entry.get("alignment_status") in {
        "missing_tom_context",
        "missing_intennse_context",
        "requires_human_alignment_review",
    }:
        structural_warnings.append(
            _warning(
                entry["alignment_status"],
                f"{path}.alignment_status",
                entity,
            )
        )
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_referenced_tom_contracts(
    *,
    observation_quality_taxonomy_path: str | Path | None,
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
    multi_reviewer_schema_path: str | Path | None,
) -> dict[str, Any]:
    checks = [
        {
            "contract": "observation_quality_taxonomy",
            "path": observation_quality_taxonomy_path,
            "type_field": "taxonomy_type",
            "expected_type": OBSERVATION_QUALITY_TAXONOMY_TYPE,
            "version_field": "taxonomy_version",
            "expected_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        },
        {
            "contract": "review_label_schema",
            "path": review_label_schema_path,
            "type_field": "schema_type",
            "expected_type": REVIEW_LABEL_SCHEMA_TYPE,
            "version_field": "schema_version",
            "expected_version": REVIEW_LABEL_SCHEMA_VERSION,
        },
        {
            "contract": "reviewer_confidence_schema",
            "path": reviewer_confidence_schema_path,
            "type_field": "schema_type",
            "expected_type": REVIEWER_CONFIDENCE_SCHEMA_TYPE,
            "version_field": "schema_version",
            "expected_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        },
        {
            "contract": "multi_reviewer_disagreement_schema",
            "path": multi_reviewer_schema_path,
            "type_field": "schema_type",
            "expected_type": MULTI_REVIEWER_SCHEMA_TYPE,
            "version_field": "schema_version",
            "expected_version": MULTI_REVIEWER_SCHEMA_VERSION,
        },
    ]
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    validations: list[dict[str, Any]] = []
    for check in checks:
        path = check["path"]
        if path is None or not str(path).strip():
            structural_warnings.append(
                _warning(
                    "missing_tom_contract_path",
                    str(check["contract"]),
                    path,
                )
            )
            continue
        loaded = _load_json(path, label=str(check["contract"]))
        if loaded.get("ok") is False:
            errors.append(
                _error(
                    "missing_or_invalid_tom_contract",
                    str(check["contract"]),
                    loaded,
                )
            )
            validations.append(
                _tom_contract_validation(
                    check=check,
                    ok=False,
                    status=loaded.get("status"),
                )
            )
            continue
        data = _dict(loaded["data"])
        ok = (
            data.get(check["type_field"]) == check["expected_type"]
            and data.get(check["version_field"]) == check["expected_version"]
        )
        validations.append(
            _tom_contract_validation(
                check=check,
                ok=ok,
                status="valid" if ok else "invalid",
            )
        )
        if not ok:
            errors.append(
                _error(
                    "tom_contract_version_mismatch",
                    str(check["contract"]),
                    {
                        "path": str(path),
                        "actual_type": data.get(check["type_field"]),
                        "actual_version": data.get(check["version_field"]),
                        "expected_type": check["expected_type"],
                        "expected_version": check["expected_version"],
                    },
                )
            )
    return {
        "errors": errors,
        "structural_warnings": structural_warnings,
        "validations": validations,
    }


def _tom_contract_validation(
    *,
    check: dict[str, Any],
    ok: bool,
    status: object,
) -> dict[str, Any]:
    return {
        "contract": check["contract"],
        "path": str(check["path"]),
        "ok": ok,
        "status": status,
        "expected_type": check["expected_type"],
        "expected_version": check["expected_version"],
    }


def _schema_ref_errors(schema_refs: dict[str, Any], *, path: str) -> list[dict[str, Any]]:
    expected = _tom_schema_refs()
    errors: list[dict[str, Any]] = []
    for key, value in expected.items():
        if schema_refs.get(key) != value:
            errors.append(
                _error(
                    "invalid_tom_schema_ref",
                    f"{path}.tom_schema_refs.{key}",
                    schema_refs.get(key),
                )
            )
    return errors


def _value_set_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["key"]: item
        for item in _list(contract.get("alignment_value_sets"))
        if isinstance(item, dict) and isinstance(item.get("key"), str)
    }


def _alignment_entries(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry for entry in _list(bundle.get("alignment_entries")) if isinstance(entry, dict)
    ]


def _sanitize_alignment_entry(entry: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "alignment_entity",
        "tom_reference",
        "intennse_reference",
        "alignment_status",
        "provenance_status",
        "alignment_notes",
        "requires_human_alignment_review",
        "human_provided_only",
        "machine_inferred",
        "warnings",
    }
    return {key: entry.get(key) for key in allowed if key in entry}


def _entry_report(entry: dict[str, Any]) -> dict[str, Any]:
    tom_reference = _dict(entry.get("tom_reference"))
    intennse_reference = _dict(entry.get("intennse_reference"))
    tom_reference_present = _has_reference_value(tom_reference)
    intennse_reference_present = _has_reference_value(
        intennse_reference,
        exclude_keys={"external_placeholder"},
    )
    provenance_issues = []
    if not tom_reference_present:
        provenance_issues.append("missing_tom_reference")
    if not intennse_reference_present:
        provenance_issues.append("missing_intennse_reference")
    provenance_status = entry.get("provenance_status")
    if provenance_status in {
        "provenance_partial",
        "provenance_missing",
        "conflicting_references",
    }:
        provenance_issues.append(str(provenance_status))
    return {
        "alignment_entity": entry.get("alignment_entity"),
        "alignment_status": entry.get("alignment_status"),
        "provenance_status": provenance_status,
        "requires_human_alignment_review": entry.get("requires_human_alignment_review"),
        "tom_reference_present": tom_reference_present,
        "intennse_reference_present": intennse_reference_present,
        "alignment_reference_present": tom_reference_present and intennse_reference_present,
        "provenance_issue_types": sorted(set(provenance_issues)),
        "alignment_notes_present": bool(entry.get("alignment_notes")),
        "warnings": {
            "structural_alignment_only": True,
            "provenance_only": True,
            "does_not_import_intennse_truth": True,
            "does_not_validate_correctness": True,
        },
    }


def _reference_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    associated_run_ids = _string_dict(bundle.get("associated_run_ids"))
    fields = {
        "tom_point_manifest_id_present": _string_or_none(bundle.get("point_manifest_id"))
        is not None,
        "tom_media_id_present": _string_or_none(bundle.get("media_id")) is not None,
        "tom_replay_url_present": _string_or_none(bundle.get("replay_url")) is not None,
        "tom_associated_run_ids_present": bool(associated_run_ids),
        "tom_review_label_bundle_ref_present": _string_or_none(
            bundle.get("tom_review_label_bundle_ref")
        )
        is not None,
        "tom_reviewer_confidence_bundle_ref_present": _string_or_none(
            bundle.get("tom_reviewer_confidence_bundle_ref")
        )
        is not None,
        "tom_multi_reviewer_review_set_ref_present": _string_or_none(
            bundle.get("tom_multi_reviewer_review_set_ref")
        )
        is not None,
        "tom_disagreement_report_ref_present": _string_or_none(
            bundle.get("tom_disagreement_report_ref")
        )
        is not None,
        "intennse_label_bundle_ref_present": _string_or_none(
            bundle.get("intennse_label_bundle_ref")
        )
        is not None,
        "intennse_schema_version_present": _string_or_none(
            bundle.get("intennse_schema_version")
        )
        is not None,
    }
    return {
        **fields,
        "present_reference_count": sum(1 for value in fields.values() if value is True),
        "associated_run_id_keys": sorted(associated_run_ids.keys()),
    }


def _report_summary(*, entry_reports: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "alignment_entry_count": len(entry_reports),
        "alignment_reference_present_count": sum(
            1 for entry in entry_reports if entry.get("alignment_reference_present") is True
        ),
        "missing_tom_reference_count": sum(
            1 for entry in entry_reports if entry.get("tom_reference_present") is not True
        ),
        "missing_intennse_reference_count": sum(
            1
            for entry in entry_reports
            if entry.get("intennse_reference_present") is not True
        ),
        "provenance_partial_count": sum(
            1
            for entry in entry_reports
            if entry.get("provenance_status")
            in {"provenance_partial", "provenance_missing", "conflicting_references"}
        ),
        "requires_human_alignment_review_count": sum(
            1
            for entry in entry_reports
            if entry.get("requires_human_alignment_review") == "required"
            or entry.get("alignment_status") == "requires_human_alignment_review"
        ),
    }


def _provenance_issues(*, entry_reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for entry in entry_reports:
        for issue_type in _string_list(entry.get("provenance_issue_types")):
            issues.append(
                {
                    "issue_type": issue_type,
                    "alignment_entity": entry.get("alignment_entity"),
                    "provenance_only": True,
                    "requires_human_alignment_review": (
                        issue_type
                        in {
                            "missing_tom_reference",
                            "missing_intennse_reference",
                            "provenance_partial",
                            "provenance_missing",
                            "conflicting_references",
                        }
                    ),
                }
            )
    return issues


def _has_reference_value(
    value: Any,
    *,
    exclude_keys: set[str] | None = None,
) -> bool:
    exclude_keys = exclude_keys or set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in exclude_keys or key == "reference_type":
                continue
            if _has_reference_value(item, exclude_keys=exclude_keys):
                return True
    if isinstance(value, list):
        return any(_has_reference_value(item, exclude_keys=exclude_keys) for item in value)
    return isinstance(value, str) and bool(value)


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}"
            if key in FORBIDDEN_INTENNSE_ALIGNMENT_FIELDS:
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
        "provenance_only": True,
        "no_adjudication": True,
    }


def _warning(warning_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "warning_type": warning_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "provenance_only": True,
        "no_adjudication": True,
    }


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": INTENNSE_ALIGNMENT_BLUEPRINT,
        "blueprint_name": INTENNSE_ALIGNMENT_BLUEPRINT_NAME,
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
        "contract_type": INTENNSE_ALIGNMENT_CONTRACT_TYPE,
        "contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "warnings": dict(ALIGNMENT_WARNINGS),
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
