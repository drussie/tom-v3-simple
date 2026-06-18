from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.intennse_label_alignment import (
    DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    INTENNSE_ALIGNMENT_CONTRACT_TYPE,
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
)
from apps.worker.services.multi_point_regression_matrix import (
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    MULTI_POINT_REGRESSION_MATRIX_TYPE,
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_OUTPUT,
    MULTI_POINT_REPLAY_INDEX_TYPE,
    MULTI_POINT_REPLAY_INDEX_VERSION,
)
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
from apps.worker.services.point_manifest import POINT_MANIFEST_VERSION
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

DATASET_CORPUS_CONTRACT_TYPE = "versioned_dataset_corpus_contract"
DATASET_CORPUS_CONTRACT_VERSION = "v1"
DATASET_CORPUS_MANIFEST_TYPE = "versioned_dataset_corpus_manifest"
DATASET_CORPUS_MANIFEST_VERSION = "v1"
DATASET_CORPUS_REPORT_TYPE = "versioned_dataset_corpus_report"
DATASET_CORPUS_REPORT_VERSION = "v1"
DATASET_CORPUS_BLUEPRINT = "blueprint_31"
DATASET_CORPUS_BLUEPRINT_NAME = "versioned_dataset_corpus_v1"

DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT = (
    ".data/contracts/versioned_dataset_corpus_contract_v1.json"
)
DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT = (
    ".data/exports/versioned_dataset_corpus_manifest.current.json"
)
DEFAULT_DATASET_CORPUS_VALIDATION_OUTPUT = (
    ".data/exports/versioned_dataset_corpus_manifest.validation.json"
)
DEFAULT_DATASET_CORPUS_REPORT_OUTPUT = (
    ".data/exports/versioned_dataset_corpus_report.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)
DEFAULT_CORPUS_VERSION = "v1"

CORPUS_SPLIT_VALUES = [
    "unassigned",
    "holdout_candidate",
    "review_candidate",
    "regression_protected",
    "not_applicable",
]

CORPUS_ENTRY_STATUS_VALUES = [
    "not_assessed",
    "evidence_present",
    "evidence_partial",
    "evidence_missing",
    "review_ready",
    "needs_human_review",
    "provenance_partial",
    "provenance_missing",
    "not_applicable",
]

PROVENANCE_STATUS_VALUES = [
    "not_assessed",
    "provenance_present",
    "provenance_partial",
    "provenance_missing",
    "conflicting_references",
    "not_applicable",
]

HUMAN_REVIEW_VALUES = [
    "not_assessed",
    "unknown",
    "required",
    "not_required",
    "not_applicable",
]

CORPUS_ENTITIES = (
    {
        "key": "corpus_manifest",
        "description": "Versioned dataset corpus manifest metadata.",
    },
    {
        "key": "corpus_point_entry",
        "description": "One manifest-backed point entry in a versioned corpus.",
    },
    {
        "key": "evidence_asset_ref",
        "description": "Reference to existing TOM evidence assets.",
    },
    {
        "key": "point_manifest_ref",
        "description": "Reference to a TOM point manifest.",
    },
    {
        "key": "replay_context_ref",
        "description": "Replay URL and run-ID context for human review.",
    },
    {
        "key": "observation_quality_profile_ref",
        "description": "Optional reference to a TOM observation-quality profile.",
    },
    {
        "key": "review_label_bundle_ref",
        "description": "Optional reference to TOM structured review-label bundles.",
    },
    {
        "key": "reviewer_confidence_bundle_ref",
        "description": "Optional reference to TOM reviewer confidence bundles.",
    },
    {
        "key": "multi_reviewer_review_set_ref",
        "description": "Optional reference to TOM multi-reviewer review sets.",
    },
    {
        "key": "disagreement_report_ref",
        "description": "Optional reference to TOM structural disagreement reports.",
    },
    {
        "key": "intennse_alignment_bundle_ref",
        "description": "Optional reference to INTENNSE alignment bundles.",
    },
    {
        "key": "regression_matrix_ref",
        "description": "Reference to a TOM multi-point regression matrix.",
    },
    {
        "key": "dataset_export_ref",
        "description": "Optional reference to existing dataset/export artifacts.",
    },
)

CORPUS_ENTRY_FIELDS = (
    {"key": "corpus_entry_id", "required": True},
    {"key": "point_manifest_id", "required": True},
    {"key": "media_id", "required": True},
    {"key": "replay_url", "required": False},
    {"key": "associated_run_ids", "required": False},
    {"key": "labels", "required": False},
    {"key": "corpus_split", "required": True, "value_set": "corpus_split_values"},
    {"key": "source_media_path", "required": False},
    {"key": "source_uri", "required": False},
    {"key": "stored_uri", "required": False},
    {"key": "point_manifest_path", "required": False},
    {"key": "multi_point_replay_index_path", "required": True},
    {"key": "multi_point_regression_matrix_path", "required": True},
    {"key": "observation_quality_profile_path", "required": False},
    {"key": "review_label_bundle_refs", "required": False},
    {"key": "reviewer_confidence_bundle_refs", "required": False},
    {"key": "multi_reviewer_review_set_refs", "required": False},
    {"key": "disagreement_report_refs", "required": False},
    {"key": "intennse_alignment_refs", "required": False},
    {"key": "dataset_export_refs", "required": False},
    {"key": "evidence_availability", "required": False},
    {"key": "profile_counts", "required": False},
    {"key": "provenance_status", "required": True, "value_set": "provenance_status_values"},
    {"key": "corpus_entry_status", "required": True, "value_set": "corpus_entry_status_values"},
    {"key": "requires_human_review", "required": True, "value_set": "human_review_values"},
    {"key": "provenance_gaps", "required": False},
    {"key": "warnings", "required": True},
)

FORBIDDEN_DATASET_CORPUS_FIELDS = {
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
    "training_truth",
    "model_ready_truth",
    "disagreement_resolution",
}

DATASET_CORPUS_WARNINGS = {
    "dataset_corpus_is_not_truth": True,
    "dataset_corpus_is_not_training_truth": True,
    "manifest_is_not_truth": True,
    "provenance_only": True,
    "observation_only": True,
    "review_support_only": True,
    "no_adjudication": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_observations": True,
    "does_not_create_labels": True,
    "does_not_create_intennse_labels": True,
    "does_not_infer_truth": True,
    "does_not_validate_correctness": True,
    "does_not_resolve_disagreement": True,
    "does_not_score_reviewers": True,
    "not_generalization_claim": True,
}

ENTRY_WARNINGS = {
    "corpus_entry_is_not_truth": True,
    "split_is_not_training_truth": True,
    "provenance_only": True,
    "review_support_only": True,
    "no_adjudication": True,
    "does_not_create_labels": True,
    "does_not_validate_correctness": True,
}

OPTIONAL_REF_FIELDS = (
    "observation_quality_profile_path",
    "review_label_bundle_refs",
    "reviewer_confidence_bundle_refs",
    "multi_reviewer_review_set_refs",
    "disagreement_report_refs",
    "intennse_alignment_refs",
    "dataset_export_refs",
)


def export_versioned_dataset_corpus_contract(
    *,
    output_path: str | Path | None = DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen versioned dataset corpus contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": DATASET_CORPUS_CONTRACT_TYPE,
        "contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "corpus_entity_count": len(CORPUS_ENTITIES),
        "corpus_entry_field_count": len(CORPUS_ENTRY_FIELDS),
        "contract": contract,
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_versioned_dataset_corpus_manifest(
    *,
    source_index_path: str | Path = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    source_matrix_path: str | Path = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    corpus_id: str | None = None,
    corpus_version: str = DEFAULT_CORPUS_VERSION,
    output_path: str | Path | None = DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a versioned dataset corpus manifest from existing TOM artifacts."""

    source_index_loaded = _load_json(source_index_path, label="source_index")
    if source_index_loaded.get("ok") is False:
        return source_index_loaded
    source_matrix_loaded = _load_json(source_matrix_path, label="source_matrix")
    if source_matrix_loaded.get("ok") is False:
        return source_matrix_loaded
    source_index = _dict(source_index_loaded["data"])
    source_matrix = _dict(source_matrix_loaded["data"])
    source_validation = _validate_source_artifacts(
        source_index=source_index,
        source_matrix=source_matrix,
    )
    if source_validation:
        return source_validation

    generated_at = generated_at or datetime.now(UTC)
    entries = _build_corpus_entries(
        source_index=source_index,
        source_matrix=source_matrix,
        source_index_path=source_index_path,
        source_matrix_path=source_matrix_path,
    )
    skipped_entries = _skipped_entries(source_index=source_index, source_matrix=source_matrix)
    resolved_corpus_id = corpus_id or _corpus_id(
        corpus_version=corpus_version,
        source_index_path=source_index_path,
        source_matrix_path=source_matrix_path,
        entries=entries,
    )
    manifest = {
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "contract_type": DATASET_CORPUS_CONTRACT_TYPE,
        "contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "corpus_id": resolved_corpus_id,
        "corpus_version": corpus_version,
        "generated_at": generated_at.isoformat(),
        "source_index_path": str(Path(source_index_path)),
        "source_index_type": source_index.get("index_type"),
        "source_index_version": source_index.get("index_version"),
        "source_matrix_path": str(Path(source_matrix_path)),
        "source_matrix_type": source_matrix.get("matrix_type"),
        "source_matrix_version": source_matrix.get("matrix_version"),
        "source_contract_versions": _included_contract_refs(),
        "point_count": len(entries),
        "corpus_entries": entries,
        "skipped_entries": skipped_entries,
        "summary": _manifest_summary(entries=entries),
        "tom_provenance": _tom_provenance(),
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "corpus_id": resolved_corpus_id,
        "corpus_version": corpus_version,
        "point_count": len(entries),
        "summary": manifest["summary"],
        "manifest": manifest,
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        result["manifest_output"] = str(path)
    return result


def validate_versioned_dataset_corpus_manifest(
    *,
    contract_path: str | Path = DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    observation_quality_taxonomy_path: str | Path | None = (
        DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT
    ),
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    multi_reviewer_schema_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    intennse_alignment_contract_path: str | Path | None = (
        DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_DATASET_CORPUS_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a corpus manifest structurally without creating dataset truth."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    manifest_loaded = _load_json(manifest_path, label="corpus_manifest")
    if manifest_loaded.get("ok") is False:
        return manifest_loaded

    contract = _dict(contract_loaded["data"])
    manifest = _dict(manifest_loaded["data"])
    errors = _validate_contract_shape(contract)
    structural_warnings: list[dict[str, Any]] = []
    contract_validations: list[dict[str, Any]] = []
    if not errors:
        contract_result = _validate_referenced_contracts(
            observation_quality_taxonomy_path=observation_quality_taxonomy_path,
            review_label_schema_path=review_label_schema_path,
            reviewer_confidence_schema_path=reviewer_confidence_schema_path,
            multi_reviewer_schema_path=multi_reviewer_schema_path,
            intennse_alignment_contract_path=intennse_alignment_contract_path,
        )
        errors.extend(_list(contract_result.get("errors")))
        structural_warnings.extend(_list(contract_result.get("structural_warnings")))
        contract_validations.extend(_list(contract_result.get("validations")))
        manifest_result = _validate_manifest_shape(manifest=manifest)
        errors.extend(_list(manifest_result.get("errors")))
        structural_warnings.extend(_list(manifest_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "versioned_dataset_corpus_manifest_validation",
        "validation_version": DATASET_CORPUS_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "manifest_path": str(Path(manifest_path)),
        "contract_paths": {
            "observation_quality_taxonomy_path": _path_or_none(
                observation_quality_taxonomy_path
            ),
            "review_label_schema_path": _path_or_none(review_label_schema_path),
            "reviewer_confidence_schema_path": _path_or_none(
                reviewer_confidence_schema_path
            ),
            "multi_reviewer_schema_path": _path_or_none(multi_reviewer_schema_path),
            "intennse_alignment_contract_path": _path_or_none(
                intennse_alignment_contract_path
            ),
        },
        "contract_type": DATASET_CORPUS_CONTRACT_TYPE,
        "contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "referenced_contract_validations": contract_validations,
        "warnings": dict(DATASET_CORPUS_WARNINGS),
        "known_limitations": [
            "Validation checks corpus structure and referenced contract versions only.",
            "Validation reports missing optional review and alignment refs as provenance gaps.",
            "Validation does not infer missing labels.",
            "Validation does not create labels.",
            "Validation does not judge label validity.",
            "Validation does not resolve reviewer disagreement.",
            "Validation does not create dataset truth.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_versioned_dataset_corpus_report(
    *,
    contract_path: str | Path = DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    manifest_path: str | Path,
    observation_quality_taxonomy_path: str | Path | None = (
        DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT
    ),
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    multi_reviewer_schema_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    intennse_alignment_contract_path: str | Path | None = (
        DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_DATASET_CORPUS_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural dataset corpus report."""

    generated_at = generated_at or datetime.now(UTC)
    validation = validate_versioned_dataset_corpus_manifest(
        contract_path=contract_path,
        manifest_path=manifest_path,
        observation_quality_taxonomy_path=observation_quality_taxonomy_path,
        review_label_schema_path=review_label_schema_path,
        reviewer_confidence_schema_path=reviewer_confidence_schema_path,
        multi_reviewer_schema_path=multi_reviewer_schema_path,
        intennse_alignment_contract_path=intennse_alignment_contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_corpus_manifest",
            "validation": validation,
            "warnings": dict(DATASET_CORPUS_WARNINGS),
        }

    manifest_loaded = _load_json(manifest_path, label="corpus_manifest")
    if manifest_loaded.get("ok") is False:
        return manifest_loaded
    manifest = _dict(manifest_loaded["data"])
    entry_reports = [_entry_report(entry) for entry in _corpus_entries(manifest)]
    summary = _report_summary(entry_reports=entry_reports)
    report = {
        "corpus_report_type": DATASET_CORPUS_REPORT_TYPE,
        "corpus_report_version": DATASET_CORPUS_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_corpus_manifest_path": str(Path(manifest_path)),
        "contract_path": str(Path(contract_path)),
        "corpus_id": manifest.get("corpus_id"),
        "corpus_version": manifest.get("corpus_version"),
        "point_count": manifest.get("point_count"),
        "source_index_path": manifest.get("source_index_path"),
        "source_matrix_path": manifest.get("source_matrix_path"),
        "entry_reports": entry_reports,
        "summary": summary,
        "coverage": _coverage_summary(entry_reports=entry_reports),
        "provenance_issues": _provenance_issues(entry_reports=entry_reports),
        "structural_warnings": validation.get("structural_warnings", []),
        "referenced_contract_validations": validation.get(
            "referenced_contract_validations",
            [],
        ),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(DATASET_CORPUS_WARNINGS),
            "report_is_structural_only": True,
            "does_not_evaluate_tennis_quality": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "corpus_report_type": DATASET_CORPUS_REPORT_TYPE,
        "corpus_report_version": DATASET_CORPUS_REPORT_VERSION,
        "corpus_entry_count": len(entry_reports),
        "summary": summary,
        "report": report,
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": DATASET_CORPUS_CONTRACT_TYPE,
        "contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "corpus_report_type": DATASET_CORPUS_REPORT_TYPE,
        "corpus_report_version": DATASET_CORPUS_REPORT_VERSION,
        "corpus_scope": {
            "purpose": (
                "Package TOM evidence, provenance, review structures, reviewer "
                "confidence, multi-reviewer disagreement, and INTENNSE alignment "
                "references into a versioned corpus manifest."
            ),
            "dataset_productization_layer": True,
            "training_truth_allowed": False,
            "automatic_label_creation_allowed": False,
            "automatic_correctness_claims_allowed": False,
            "provenance_only": True,
            "review_support_only": True,
        },
        "corpus_entities": [_entity_definition(entity) for entity in CORPUS_ENTITIES],
        "corpus_entry_fields": [
            _entry_field_definition(field) for field in CORPUS_ENTRY_FIELDS
        ],
        "corpus_split_policy": {
            "allowed_values": list(CORPUS_SPLIT_VALUES),
            "default_value": "unassigned",
            "current_manifest_default": "unassigned",
            "protected_regression_entries_use": "regression_protected",
            "split_values_are_not_training_truth": True,
            "no_training_evaluation_assignment": True,
            "warnings": {
                "split_is_not_training_truth": True,
                "provenance_only": True,
                "no_adjudication": True,
            },
        },
        "corpus_versioning_policy": {
            "corpus_id_required": True,
            "corpus_version_required": True,
            "corpus_manifest_version_required": DATASET_CORPUS_MANIFEST_VERSION,
            "generated_at_required": True,
            "source_index_path_required": True,
            "source_matrix_path_required": True,
            "source_contract_versions_required": True,
            "point_count_required": True,
            "corpus_entries_required": True,
            "skipped_entries_allowed": True,
            "summary_required": True,
        },
        "provenance_requirements": {
            "point_manifest_id_required": True,
            "media_id_required": True,
            "replay_url_recommended": True,
            "associated_run_ids_allowed": [
                "event_candidate_run_id",
                "trajectory_3d_run_id",
                "camera_geometry_id",
            ],
            "point_manifest_path_recommended": True,
            "source_index_path_required": True,
            "source_matrix_path_required": True,
            "missing_optional_review_refs_are_provenance_gaps": True,
            "missing_intennse_alignment_refs_are_provenance_gaps": True,
        },
        "included_contract_refs": _included_contract_refs(),
        "corpus_value_sets": [
            _value_set(
                key="corpus_split_values",
                allowed_values=CORPUS_SPLIT_VALUES,
                default_value="unassigned",
            ),
            _value_set(
                key="corpus_entry_status_values",
                allowed_values=CORPUS_ENTRY_STATUS_VALUES,
                default_value="not_assessed",
            ),
            _value_set(
                key="provenance_status_values",
                allowed_values=PROVENANCE_STATUS_VALUES,
                default_value="not_assessed",
            ),
            _value_set(
                key="human_review_values",
                allowed_values=HUMAN_REVIEW_VALUES,
                default_value="not_assessed",
            ),
        ],
        "validation_rules": {
            "structural_validation_only": True,
            "referenced_contract_versions_validated_when_paths_available": True,
            "source_matrix_and_index_paths_must_exist_when_supplied": True,
            "corpus_entry_required_fields_checked": True,
            "allowed_split_values_only": True,
            "allowed_status_values_only": True,
            "does_not_infer_missing_labels": True,
            "does_not_create_labels": True,
            "does_not_validate_label_validity": True,
            "does_not_resolve_disagreement": True,
            "does_not_create_truth": True,
            "does_not_create_training_truth": True,
            "forbidden_fields": sorted(FORBIDDEN_DATASET_CORPUS_FIELDS),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }


def _included_contract_refs() -> dict[str, str]:
    return {
        "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "intennse_label_alignment_contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_manifest_version": POINT_MANIFEST_VERSION,
    }


def _entity_definition(entity: dict[str, str]) -> dict[str, Any]:
    return {
        "key": entity["key"],
        "description": entity["description"],
        "structural_only": True,
        "provenance_only": True,
        "warnings": dict(ENTRY_WARNINGS),
    }


def _entry_field_definition(field: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": field["key"],
        "required": field["required"],
        "value_set": field.get("value_set"),
        "structural_only": True,
        "provenance_only": True,
        "warnings": dict(ENTRY_WARNINGS),
    }


def _value_set(
    *,
    key: str,
    allowed_values: list[str],
    default_value: str,
) -> dict[str, Any]:
    return {
        "key": key,
        "allowed_values": list(allowed_values),
        "default_value": default_value,
        "free_text": False,
        "warnings": {
            "value_set_is_not_truth": True,
            "provenance_only": True,
            "review_support_only": True,
            "no_adjudication": True,
        },
    }


def _validate_source_artifacts(
    *,
    source_index: dict[str, Any],
    source_matrix: dict[str, Any],
) -> dict[str, Any] | None:
    errors: list[dict[str, Any]] = []
    if source_index.get("index_type") != MULTI_POINT_REPLAY_INDEX_TYPE:
        errors.append(
            _error(
                "invalid_source_index_type",
                "source_index.index_type",
                source_index.get("index_type"),
            )
        )
    if source_index.get("index_version") != MULTI_POINT_REPLAY_INDEX_VERSION:
        errors.append(
            _error(
                "invalid_source_index_version",
                "source_index.index_version",
                source_index.get("index_version"),
            )
        )
    if source_matrix.get("matrix_type") != MULTI_POINT_REGRESSION_MATRIX_TYPE:
        errors.append(
            _error(
                "invalid_source_matrix_type",
                "source_matrix.matrix_type",
                source_matrix.get("matrix_type"),
            )
        )
    if source_matrix.get("matrix_version") != MULTI_POINT_REGRESSION_MATRIX_VERSION:
        errors.append(
            _error(
                "invalid_source_matrix_version",
                "source_matrix.matrix_version",
                source_matrix.get("matrix_version"),
            )
        )
    if not isinstance(source_index.get("points"), list):
        errors.append(_error("source_index_points_must_be_list", "source_index.points", None))
    if not isinstance(source_matrix.get("points"), list):
        errors.append(_error("source_matrix_points_must_be_list", "source_matrix.points", None))
    if not errors:
        return None
    return {
        "ok": False,
        "status": "invalid_source_artifacts",
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }


def _build_corpus_entries(
    *,
    source_index: dict[str, Any],
    source_matrix: dict[str, Any],
    source_index_path: str | Path,
    source_matrix_path: str | Path,
) -> list[dict[str, Any]]:
    index_points = {
        _point_key(point): point
        for point in _list(source_index.get("points"))
        if isinstance(point, dict)
    }
    entries: list[dict[str, Any]] = []
    for matrix_point in _list(source_matrix.get("points")):
        if not isinstance(matrix_point, dict):
            continue
        index_point = index_points.get(_point_key(matrix_point), {})
        merged = {**_dict(index_point), **matrix_point}
        labels = _string_list(merged.get("labels"))
        evidence_availability = _bool_dict(merged.get("evidence_availability"))
        profile_counts = _int_dict(merged.get("profile_counts"))
        optional_refs = _optional_refs()
        provenance_gaps = _provenance_gaps(optional_refs=optional_refs)
        corpus_split = (
            "regression_protected"
            if "protected_sample_point" in labels
            else "unassigned"
        )
        provenance_status = _provenance_status(merged=merged, gaps=provenance_gaps)
        entry_status = _entry_status(
            evidence_availability=evidence_availability,
            provenance_status=provenance_status,
        )
        requires_human_review = (
            "required"
            if entry_status in {"needs_human_review", "provenance_missing"}
            else "not_assessed"
        )
        entry = {
            "corpus_entry_id": _corpus_entry_id(merged),
            "point_manifest_id": _string_or_none(merged.get("point_manifest_id")),
            "media_id": _string_or_none(merged.get("media_id")),
            "replay_url": _string_or_none(merged.get("replay_url")),
            "associated_run_ids": _string_dict(merged.get("associated_run_ids")),
            "labels": labels,
            "corpus_split": corpus_split,
            "source_media_path": _string_or_none(merged.get("source_media_path")),
            "source_uri": _string_or_none(merged.get("source_uri")),
            "stored_uri": _string_or_none(merged.get("stored_uri")),
            "point_manifest_path": _string_or_none(
                merged.get("manifest_path") or merged.get("point_manifest_path")
            ),
            "multi_point_replay_index_path": str(Path(source_index_path)),
            "multi_point_regression_matrix_path": str(Path(source_matrix_path)),
            "observation_quality_profile_path": optional_refs[
                "observation_quality_profile_path"
            ],
            "review_label_bundle_refs": optional_refs["review_label_bundle_refs"],
            "reviewer_confidence_bundle_refs": optional_refs[
                "reviewer_confidence_bundle_refs"
            ],
            "multi_reviewer_review_set_refs": optional_refs[
                "multi_reviewer_review_set_refs"
            ],
            "disagreement_report_refs": optional_refs["disagreement_report_refs"],
            "intennse_alignment_refs": optional_refs["intennse_alignment_refs"],
            "dataset_export_refs": optional_refs["dataset_export_refs"],
            "evidence_availability": evidence_availability,
            "profile_counts": profile_counts,
            "provenance_status": provenance_status,
            "corpus_entry_status": entry_status,
            "requires_human_review": requires_human_review,
            "provenance_gaps": provenance_gaps,
            "warnings": {
                **dict(ENTRY_WARNINGS),
                **_bool_dict(merged.get("warnings")),
                "regression_protected_entry": corpus_split == "regression_protected",
            },
        }
        entries.append(entry)
    return entries


def _optional_refs() -> dict[str, Any]:
    return {
        "observation_quality_profile_path": None,
        "review_label_bundle_refs": [],
        "reviewer_confidence_bundle_refs": [],
        "multi_reviewer_review_set_refs": [],
        "disagreement_report_refs": [],
        "intennse_alignment_refs": [],
        "dataset_export_refs": [],
    }


def _provenance_gaps(*, optional_refs: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    if optional_refs["observation_quality_profile_path"] is None:
        gaps.append("missing_optional_observation_quality_profile_ref")
    for field in (
        "review_label_bundle_refs",
        "reviewer_confidence_bundle_refs",
        "multi_reviewer_review_set_refs",
        "disagreement_report_refs",
    ):
        if not optional_refs[field]:
            gaps.append("missing_optional_review_ref")
    if not optional_refs["intennse_alignment_refs"]:
        gaps.append("missing_optional_intennse_alignment_ref")
    if not optional_refs["dataset_export_refs"]:
        gaps.append("missing_optional_dataset_export_ref")
    return sorted(set(gaps))


def _provenance_status(*, merged: dict[str, Any], gaps: list[str]) -> str:
    required_present = all(
        _string_or_none(merged.get(key)) is not None
        for key in ("point_manifest_id", "media_id", "replay_url")
    )
    has_manifest_path = _string_or_none(
        merged.get("manifest_path") or merged.get("point_manifest_path")
    )
    if not required_present:
        return "provenance_missing"
    if gaps or has_manifest_path is None:
        return "provenance_partial"
    return "provenance_present"


def _entry_status(
    *,
    evidence_availability: dict[str, bool],
    provenance_status: str,
) -> str:
    if provenance_status == "provenance_missing":
        return "provenance_missing"
    if provenance_status == "provenance_partial":
        return "provenance_partial"
    if not evidence_availability:
        return "evidence_missing"
    values = list(evidence_availability.values())
    if not any(values):
        return "evidence_missing"
    if (
        evidence_availability.get("media_indexed") is True
        and evidence_availability.get("replay_available") is True
        and evidence_availability.get("review_annotations_available") is True
    ):
        return "review_ready"
    if all(values):
        return "evidence_present"
    return "evidence_partial"


def _skipped_entries(
    *,
    source_index: dict[str, Any],
    source_matrix: dict[str, Any],
) -> list[dict[str, Any]]:
    skipped = []
    matrix_keys = {
        _point_key(point)
        for point in _list(source_matrix.get("points"))
        if isinstance(point, dict)
    }
    for point in _list(source_index.get("points")):
        if not isinstance(point, dict):
            continue
        if _point_key(point) not in matrix_keys:
            skipped.append(
                {
                    "reason": "point_not_present_in_regression_matrix",
                    "point_manifest_id": point.get("point_manifest_id"),
                    "media_id": point.get("media_id"),
                    "provenance_only": True,
                }
            )
    for skipped_manifest in _list(source_index.get("skipped_manifests")):
        if isinstance(skipped_manifest, dict):
            skipped.append(
                {
                    "reason": skipped_manifest.get("reason", "source_index_skipped_manifest"),
                    "path": skipped_manifest.get("path"),
                    "provenance_only": True,
                }
            )
    return skipped


def _manifest_summary(*, entries: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "point_count": len(entries),
        "regression_protected_entry_count": _count_entries(
            entries,
            key="corpus_split",
            value="regression_protected",
        ),
        "unassigned_entry_count": _count_entries(
            entries,
            key="corpus_split",
            value="unassigned",
        ),
        "review_ready_entry_count": _count_entries(
            entries,
            key="corpus_entry_status",
            value="review_ready",
        ),
        "provenance_partial_entry_count": _count_entries(
            entries,
            key="provenance_status",
            value="provenance_partial",
        ),
        "provenance_missing_entry_count": _count_entries(
            entries,
            key="provenance_status",
            value="provenance_missing",
        ),
        "missing_optional_review_ref_count": _count_gap(
            entries,
            "missing_optional_review_ref",
        ),
        "missing_optional_intennse_alignment_ref_count": _count_gap(
            entries,
            "missing_optional_intennse_alignment_ref",
        ),
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != DATASET_CORPUS_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != DATASET_CORPUS_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "corpus_scope",
        "corpus_entities",
        "corpus_entry_fields",
        "corpus_split_policy",
        "corpus_versioning_policy",
        "provenance_requirements",
        "included_contract_refs",
        "corpus_value_sets",
        "validation_rules",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors

    errors.extend(
        _included_contract_ref_errors(
            _dict(contract.get("included_contract_refs")),
            path="contract",
        )
    )
    expected_entities = {entity["key"] for entity in CORPUS_ENTITIES}
    contract_entities = {
        item.get("key")
        for item in _list(contract.get("corpus_entities"))
        if isinstance(item, dict)
    }
    if not expected_entities <= contract_entities:
        errors.append(
            _error(
                "missing_corpus_entities",
                "corpus_entities",
                sorted(expected_entities - contract_entities),
            )
        )
    expected_fields = {field["key"] for field in CORPUS_ENTRY_FIELDS}
    contract_fields = {
        item.get("key")
        for item in _list(contract.get("corpus_entry_fields"))
        if isinstance(item, dict)
    }
    if not expected_fields <= contract_fields:
        errors.append(
            _error(
                "missing_corpus_entry_fields",
                "corpus_entry_fields",
                sorted(expected_fields - contract_fields),
            )
        )
    value_sets = _value_set_map(contract)
    for key, expected_values in {
        "corpus_split_values": CORPUS_SPLIT_VALUES,
        "corpus_entry_status_values": CORPUS_ENTRY_STATUS_VALUES,
        "provenance_status_values": PROVENANCE_STATUS_VALUES,
        "human_review_values": HUMAN_REVIEW_VALUES,
    }.items():
        actual_values = set(_string_list(_dict(value_sets.get(key)).get("allowed_values")))
        if not set(expected_values) <= actual_values:
            errors.append(
                _error(
                    "missing_corpus_value_set_values",
                    key,
                    sorted(set(expected_values) - actual_values),
                )
            )
    rules = _dict(contract.get("validation_rules"))
    for rule in (
        "structural_validation_only",
        "referenced_contract_versions_validated_when_paths_available",
        "source_matrix_and_index_paths_must_exist_when_supplied",
        "corpus_entry_required_fields_checked",
        "allowed_split_values_only",
        "allowed_status_values_only",
        "does_not_infer_missing_labels",
        "does_not_create_labels",
        "does_not_validate_label_validity",
        "does_not_resolve_disagreement",
        "does_not_create_truth",
        "does_not_create_training_truth",
    ):
        if rules.get(rule) is not True:
            errors.append(
                _error("invalid_validation_rule", f"validation_rules.{rule}", rules.get(rule))
            )
    return errors


def _validate_manifest_shape(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(manifest, path="corpus_manifest")
    structural_warnings: list[dict[str, Any]] = []
    if manifest.get("corpus_manifest_type") != DATASET_CORPUS_MANIFEST_TYPE:
        errors.append(
            _error(
                "invalid_corpus_manifest_type",
                "corpus_manifest_type",
                manifest.get("corpus_manifest_type"),
            )
        )
    if manifest.get("corpus_manifest_version") != DATASET_CORPUS_MANIFEST_VERSION:
        errors.append(
            _error(
                "invalid_corpus_manifest_version",
                "corpus_manifest_version",
                manifest.get("corpus_manifest_version"),
            )
        )
    if manifest.get("contract_version") != DATASET_CORPUS_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_manifest_contract_version",
                "contract_version",
                manifest.get("contract_version"),
            )
        )
    errors.extend(
        _included_contract_ref_errors(
            _dict(manifest.get("source_contract_versions")),
            path="corpus_manifest",
        )
    )
    for path_key in ("source_index_path", "source_matrix_path"):
        path_value = _string_or_none(manifest.get(path_key))
        if path_value is None:
            errors.append(_error("missing_source_path", path_key, path_value))
        elif not Path(path_value).expanduser().is_file():
            errors.append(_error("source_path_not_found", path_key, path_value))

    entries = manifest.get("corpus_entries")
    if not isinstance(entries, list):
        errors.append(_error("corpus_entries_must_be_list", "corpus_entries", entries))
        return {"errors": errors, "structural_warnings": structural_warnings}
    for index, entry in enumerate(entries):
        path = f"corpus_entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(_error("corpus_entry_must_be_object", path, entry))
            continue
        entry_result = _validate_corpus_entry(entry=entry, path=path)
        errors.extend(_list(entry_result.get("errors")))
        structural_warnings.extend(_list(entry_result.get("structural_warnings")))
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_corpus_entry(*, entry: dict[str, Any], path: str) -> dict[str, Any]:
    errors = _forbidden_field_errors(entry, path=path)
    structural_warnings: list[dict[str, Any]] = []
    for field in CORPUS_ENTRY_FIELDS:
        if field["required"] and field["key"] not in entry:
            errors.append(_error("missing_corpus_entry_field", f"{path}.{field['key']}", None))
    for field in ("corpus_entry_id", "point_manifest_id", "media_id"):
        if _string_or_none(entry.get(field)) is None:
            errors.append(_error("invalid_corpus_entry_field", f"{path}.{field}", entry.get(field)))
    if entry.get("corpus_split") not in CORPUS_SPLIT_VALUES:
        errors.append(
            _error("invalid_corpus_split", f"{path}.corpus_split", entry.get("corpus_split"))
        )
    if entry.get("corpus_entry_status") not in CORPUS_ENTRY_STATUS_VALUES:
        errors.append(
            _error(
                "invalid_corpus_entry_status",
                f"{path}.corpus_entry_status",
                entry.get("corpus_entry_status"),
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
    if entry.get("requires_human_review") not in HUMAN_REVIEW_VALUES:
        errors.append(
            _error(
                "invalid_requires_human_review",
                f"{path}.requires_human_review",
                entry.get("requires_human_review"),
            )
        )
    for field in (
        "associated_run_ids",
        "evidence_availability",
        "profile_counts",
        "warnings",
    ):
        if field in entry and not isinstance(entry[field], dict):
            errors.append(
                _error(
                    "corpus_entry_field_must_be_object",
                    f"{path}.{field}",
                    entry[field],
                )
            )
    for field in (
        "labels",
        "review_label_bundle_refs",
        "reviewer_confidence_bundle_refs",
        "multi_reviewer_review_set_refs",
        "disagreement_report_refs",
        "intennse_alignment_refs",
        "dataset_export_refs",
        "provenance_gaps",
    ):
        if field in entry and not isinstance(entry[field], list):
            errors.append(
                _error(
                    "corpus_entry_field_must_be_list",
                    f"{path}.{field}",
                    entry[field],
                )
            )
    for gap in _string_list(entry.get("provenance_gaps")):
        structural_warnings.append(
            _warning(gap, f"{path}.provenance_gaps", entry.get("corpus_entry_id"))
        )
    for field in OPTIONAL_REF_FIELDS:
        if field == "observation_quality_profile_path":
            if _string_or_none(entry.get(field)) is None:
                structural_warnings.append(
                    _warning(
                        "missing_optional_observation_quality_profile_ref",
                        f"{path}.{field}",
                        None,
                    )
                )
            continue
        if not _list(entry.get(field)):
            warning_type = (
                "missing_optional_intennse_alignment_ref"
                if field == "intennse_alignment_refs"
                else "missing_optional_review_ref"
                if field != "dataset_export_refs"
                else "missing_optional_dataset_export_ref"
            )
            structural_warnings.append(_warning(warning_type, f"{path}.{field}", None))
    return {"errors": errors, "structural_warnings": _dedupe_warnings(structural_warnings)}


def _validate_referenced_contracts(
    *,
    observation_quality_taxonomy_path: str | Path | None,
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
    multi_reviewer_schema_path: str | Path | None,
    intennse_alignment_contract_path: str | Path | None,
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
        {
            "contract": "intennse_label_alignment_contract",
            "path": intennse_alignment_contract_path,
            "type_field": "contract_type",
            "expected_type": INTENNSE_ALIGNMENT_CONTRACT_TYPE,
            "version_field": "contract_version",
            "expected_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        },
    ]
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    validations: list[dict[str, Any]] = []
    for check in checks:
        path = check["path"]
        if path is None or not str(path).strip():
            structural_warnings.append(
                _warning("missing_referenced_contract_path", str(check["contract"]), path)
            )
            continue
        loaded = _load_json(path, label=str(check["contract"]))
        if loaded.get("ok") is False:
            errors.append(
                _error("missing_or_invalid_referenced_contract", str(check["contract"]), loaded)
            )
            validations.append(
                _contract_validation(check=check, ok=False, status=loaded.get("status"))
            )
            continue
        data = _dict(loaded["data"])
        ok = (
            data.get(check["type_field"]) == check["expected_type"]
            and data.get(check["version_field"]) == check["expected_version"]
        )
        validations.append(
            _contract_validation(check=check, ok=ok, status="valid" if ok else "invalid")
        )
        if not ok:
            errors.append(
                _error(
                    "referenced_contract_version_mismatch",
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


def _contract_validation(*, check: dict[str, Any], ok: bool, status: object) -> dict[str, Any]:
    return {
        "contract": check["contract"],
        "path": str(check["path"]),
        "ok": ok,
        "status": status,
        "expected_type": check["expected_type"],
        "expected_version": check["expected_version"],
    }


def _included_contract_ref_errors(refs: dict[str, Any], *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    expected = _included_contract_refs()
    for key, expected_value in expected.items():
        if refs.get(key) != expected_value:
            errors.append(
                _error(
                    "invalid_included_contract_ref",
                    f"{path}.included_contract_refs.{key}",
                    refs.get(key),
                )
            )
    return errors


def _entry_report(entry: dict[str, Any]) -> dict[str, Any]:
    evidence_availability = _bool_dict(entry.get("evidence_availability"))
    present_evidence_fields = sorted(
        key for key, value in evidence_availability.items() if value is True
    )
    missing_evidence_fields = sorted(
        key for key, value in evidence_availability.items() if value is not True
    )
    gaps = _string_list(entry.get("provenance_gaps"))
    return {
        "corpus_entry_present": True,
        "corpus_entry_id": entry.get("corpus_entry_id"),
        "point_manifest_id": entry.get("point_manifest_id"),
        "media_id": entry.get("media_id"),
        "corpus_split": entry.get("corpus_split"),
        "corpus_entry_status": entry.get("corpus_entry_status"),
        "provenance_status": entry.get("provenance_status"),
        "requires_human_review": entry.get("requires_human_review"),
        "regression_protected_entry": entry.get("corpus_split") == "regression_protected",
        "evidence_present_fields": present_evidence_fields,
        "evidence_missing_fields": missing_evidence_fields,
        "missing_optional_ref_types": sorted(set(gaps)),
        "profile_counts": _int_dict(entry.get("profile_counts")),
        "warnings": {
            "structural_coverage_only": True,
            "provenance_only": True,
            "does_not_create_training_truth": True,
            "does_not_evaluate_tennis_quality": True,
        },
    }


def _report_summary(*, entry_reports: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "corpus_entry_count": len(entry_reports),
        "corpus_entry_present_count": sum(
            1 for entry in entry_reports if entry.get("corpus_entry_present") is True
        ),
        "regression_protected_entry_count": sum(
            1 for entry in entry_reports if entry.get("regression_protected_entry") is True
        ),
        "review_ready_entry_count": sum(
            1 for entry in entry_reports if entry.get("corpus_entry_status") == "review_ready"
        ),
        "provenance_partial_count": sum(
            1 for entry in entry_reports if entry.get("provenance_status") == "provenance_partial"
        ),
        "provenance_missing_count": sum(
            1 for entry in entry_reports if entry.get("provenance_status") == "provenance_missing"
        ),
        "requires_human_review_count": sum(
            1 for entry in entry_reports if entry.get("requires_human_review") == "required"
        ),
        "missing_optional_review_ref_count": sum(
            1
            for entry in entry_reports
            if "missing_optional_review_ref"
            in _string_list(entry.get("missing_optional_ref_types"))
        ),
        "missing_optional_intennse_alignment_ref_count": sum(
            1
            for entry in entry_reports
            if "missing_optional_intennse_alignment_ref"
            in _string_list(entry.get("missing_optional_ref_types"))
        ),
    }


def _coverage_summary(*, entry_reports: list[dict[str, Any]]) -> dict[str, Any]:
    evidence_fields: dict[str, int] = {}
    for entry in entry_reports:
        for field in _string_list(entry.get("evidence_present_fields")):
            evidence_fields[field] = evidence_fields.get(field, 0) + 1
    return {
        "evidence_present_counts": dict(sorted(evidence_fields.items())),
        "review_ready_entry_count": _report_summary(entry_reports=entry_reports)[
            "review_ready_entry_count"
        ],
        "structural_coverage_only": True,
    }


def _provenance_issues(*, entry_reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for entry in entry_reports:
        for gap in _string_list(entry.get("missing_optional_ref_types")):
            issues.append(
                {
                    "issue_type": gap,
                    "corpus_entry_id": entry.get("corpus_entry_id"),
                    "point_manifest_id": entry.get("point_manifest_id"),
                    "provenance_only": True,
                    "requires_human_review": entry.get("requires_human_review"),
                }
            )
    return issues


def _corpus_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry for entry in _list(manifest.get("corpus_entries")) if isinstance(entry, dict)
    ]


def _value_set_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["key"]: item
        for item in _list(contract.get("corpus_value_sets"))
        if isinstance(item, dict) and isinstance(item.get("key"), str)
    }


def _point_key(point: dict[str, Any]) -> tuple[str, str]:
    return (
        str(point.get("point_manifest_id") or ""),
        str(point.get("media_id") or ""),
    )


def _corpus_entry_id(point: dict[str, Any]) -> str:
    payload = json.dumps(
        {
            "point_manifest_id": point.get("point_manifest_id"),
            "media_id": point.get("media_id"),
            "associated_run_ids": _string_dict(point.get("associated_run_ids")),
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"corpus_entry_v1_{digest}"


def _corpus_id(
    *,
    corpus_version: str,
    source_index_path: str | Path,
    source_matrix_path: str | Path,
    entries: list[dict[str, Any]],
) -> str:
    payload = json.dumps(
        {
            "corpus_version": corpus_version,
            "source_index_path": str(Path(source_index_path)),
            "source_matrix_path": str(Path(source_matrix_path)),
            "entries": [
                {
                    "point_manifest_id": entry.get("point_manifest_id"),
                    "media_id": entry.get("media_id"),
                }
                for entry in entries
            ],
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"versioned_dataset_corpus_v1_{digest}"


def _count_entries(entries: list[dict[str, Any]], *, key: str, value: str) -> int:
    return sum(1 for entry in entries if entry.get(key) == value)


def _count_gap(entries: list[dict[str, Any]], gap: str) -> int:
    return sum(1 for entry in entries if gap in _string_list(entry.get("provenance_gaps")))


def _dedupe_warnings(warnings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for warning in warnings:
        key = (str(warning.get("warning_type")), str(warning.get("field")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(warning)
    return deduped


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}"
            if key in FORBIDDEN_DATASET_CORPUS_FIELDS:
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
        "blueprint": DATASET_CORPUS_BLUEPRINT,
        "blueprint_name": DATASET_CORPUS_BLUEPRINT_NAME,
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
        "contract_type": DATASET_CORPUS_CONTRACT_TYPE,
        "contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "warnings": dict(DATASET_CORPUS_WARNINGS),
    }


def _path_or_none(value: str | Path | None) -> str | None:
    return str(Path(value)) if value else None


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


def _bool_dict(value: object) -> dict[str, bool]:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items() if isinstance(item, bool)}


def _int_dict(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): item
        for key, item in value.items()
        if isinstance(item, int) and not isinstance(item, bool)
    }


def _string_dict(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items() if isinstance(item, str) and item}
