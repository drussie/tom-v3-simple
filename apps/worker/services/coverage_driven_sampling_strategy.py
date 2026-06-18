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
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_CONTRACT_TYPE,
    DATASET_CORPUS_CONTRACT_VERSION,
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
)

COVERAGE_SAMPLING_CONTRACT_TYPE = "coverage_sampling_strategy_contract"
COVERAGE_SAMPLING_CONTRACT_VERSION = "v1"
COVERAGE_SAMPLING_PROFILE_TYPE = "coverage_sampling_profile"
COVERAGE_SAMPLING_PROFILE_VERSION = "v1"
COVERAGE_SAMPLING_REPORT_TYPE = "coverage_sampling_report"
COVERAGE_SAMPLING_REPORT_VERSION = "v1"
COVERAGE_SAMPLING_BLUEPRINT = "blueprint_32"
COVERAGE_SAMPLING_BLUEPRINT_NAME = "coverage_driven_sampling_strategy_v1"

DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT = (
    ".data/contracts/coverage_sampling_strategy_contract_v1.json"
)
DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT = (
    ".data/exports/coverage_sampling_profile.current.json"
)
DEFAULT_COVERAGE_SAMPLING_VALIDATION_OUTPUT = (
    ".data/exports/coverage_sampling_profile.validation.json"
)
DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT = (
    ".data/exports/coverage_sampling_report.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)

COVERAGE_AXES = [
    "media_presence",
    "replay_availability",
    "point_manifest_availability",
    "event_candidate_availability",
    "trajectory_3d_availability",
    "review_annotation_availability",
    "observation_quality_coverage",
    "review_label_coverage",
    "reviewer_confidence_coverage",
    "multi_reviewer_coverage",
    "disagreement_coverage",
    "intennse_alignment_coverage",
    "provenance_completeness",
    "regression_protection_coverage",
    "second_point_distinctness",
    "evidence_diversity",
]

COVERAGE_AXIS_STATUS_VALUES = [
    "covered",
    "partial",
    "gap",
    "unknown",
    "not_applicable",
]

COVERAGE_GAP_TYPES = [
    "missing_media",
    "missing_replay",
    "missing_point_manifest",
    "missing_event_candidates",
    "missing_trajectory_3d",
    "missing_review_annotations",
    "missing_observation_quality_profile",
    "missing_review_labels",
    "missing_reviewer_confidence",
    "missing_multi_reviewer_review",
    "missing_disagreement_report",
    "missing_intennse_alignment",
    "missing_provenance",
    "duplicate_manifest_only",
    "demo_stand_in_only",
    "single_point_only",
    "unknown_quality",
    "needs_human_review",
    "not_applicable",
]

SAMPLING_PRIORITY_VALUES = [
    "not_assessed",
    "low",
    "medium",
    "high",
    "blocked",
    "not_applicable",
]

NEXT_ACTION_VALUES = [
    "no_action",
    "collect_distinct_second_point",
    "collect_additional_point_candidate",
    "add_human_review_labels",
    "add_reviewer_confidence_bundle",
    "add_multi_reviewer_review",
    "add_intennse_alignment_reference",
    "improve_provenance_reference",
    "preserve_regression_protected_sample",
    "not_applicable",
]

HUMAN_REVIEW_VALUES = [
    "not_assessed",
    "required",
    "not_required",
    "not_applicable",
]

CANDIDATE_FIELDS = (
    {"key": "sampling_candidate_id", "required": True},
    {"key": "source_corpus_entry_id", "required": True},
    {"key": "point_manifest_id", "required": True},
    {"key": "media_id", "required": True},
    {"key": "replay_url", "required": False},
    {"key": "associated_run_ids", "required": False},
    {"key": "labels", "required": False},
    {"key": "coverage_axes", "required": True},
    {"key": "coverage_gaps", "required": True},
    {"key": "sampling_priority", "required": True, "value_set": "sampling_priority_values"},
    {"key": "priority_reason", "required": True},
    {"key": "required_human_review", "required": True, "value_set": "human_review_values"},
    {"key": "provenance_status", "required": True},
    {"key": "evidence_availability", "required": False},
    {"key": "profile_counts", "required": False},
    {"key": "suggested_next_action", "required": True, "value_set": "next_action_values"},
    {"key": "warnings", "required": True},
)

FORBIDDEN_COVERAGE_SAMPLING_FIELDS = {
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

COVERAGE_SAMPLING_WARNINGS = {
    "coverage_sampling_is_not_truth": True,
    "coverage_sampling_is_not_training_truth": True,
    "planning_only": True,
    "provenance_only": True,
    "observation_only": True,
    "review_support_only": True,
    "no_adjudication": True,
    "does_not_execute_sampling": True,
    "does_not_ingest_media": True,
    "does_not_create_observations": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_labels": True,
    "does_not_create_intennse_labels": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_validate_correctness": True,
    "does_not_resolve_disagreement": True,
    "does_not_score_reviewers": True,
    "not_generalization_claim": True,
}

CANDIDATE_WARNINGS = {
    "structural_sampling_candidate": True,
    "planning_only": True,
    "priority_is_not_truth": True,
    "next_action_is_not_execution": True,
    "does_not_execute_sampling": True,
    "does_not_ingest_media": True,
    "no_adjudication": True,
}


def export_coverage_sampling_strategy_contract(
    *,
    output_path: str | Path | None = DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen coverage-driven sampling strategy contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": COVERAGE_SAMPLING_CONTRACT_TYPE,
        "contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "profile_type": COVERAGE_SAMPLING_PROFILE_TYPE,
        "profile_version": COVERAGE_SAMPLING_PROFILE_VERSION,
        "coverage_axis_count": len(COVERAGE_AXES),
        "coverage_gap_type_count": len(COVERAGE_GAP_TYPES),
        "contract": contract,
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_coverage_sampling_profile(
    *,
    source_corpus_manifest_path: str | Path = DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    source_index_path: str | Path | None = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    source_matrix_path: str | Path | None = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    output_path: str | Path | None = DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a planning-only coverage sampling profile from existing corpus artifacts."""

    loaded_manifest = _load_json(source_corpus_manifest_path, label="corpus_manifest")
    if loaded_manifest.get("ok") is False:
        return loaded_manifest
    corpus_manifest = _dict(loaded_manifest["data"])
    source_validation = _validate_source_manifest(corpus_manifest)
    if source_validation:
        return source_validation

    source_index = _load_optional_source(
        source_index_path,
        label="source_index",
        type_field="index_type",
        expected_type=MULTI_POINT_REPLAY_INDEX_TYPE,
        version_field="index_version",
        expected_version=MULTI_POINT_REPLAY_INDEX_VERSION,
    )
    if source_index.get("ok") is False:
        return source_index
    source_matrix = _load_optional_source(
        source_matrix_path,
        label="source_matrix",
        type_field="matrix_type",
        expected_type=MULTI_POINT_REGRESSION_MATRIX_TYPE,
        version_field="matrix_version",
        expected_version=MULTI_POINT_REGRESSION_MATRIX_VERSION,
    )
    if source_matrix.get("ok") is False:
        return source_matrix

    generated_at = generated_at or datetime.now(UTC)
    entries = _corpus_entries(corpus_manifest)
    corpus_context = _corpus_context(entries=entries)
    candidates = [
        _sampling_candidate(entry=entry, corpus_context=corpus_context)
        for entry in entries
    ]
    profile = {
        "profile_type": COVERAGE_SAMPLING_PROFILE_TYPE,
        "profile_version": COVERAGE_SAMPLING_PROFILE_VERSION,
        "contract_type": COVERAGE_SAMPLING_CONTRACT_TYPE,
        "contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_corpus_manifest_path": str(Path(source_corpus_manifest_path)),
        "source_corpus_manifest_type": corpus_manifest.get("corpus_manifest_type"),
        "source_corpus_manifest_version": corpus_manifest.get("corpus_manifest_version"),
        "source_index_path": _path_or_none(source_index_path),
        "source_index_type": _dict(source_index.get("data")).get("index_type"),
        "source_index_version": _dict(source_index.get("data")).get("index_version"),
        "source_matrix_path": _path_or_none(source_matrix_path),
        "source_matrix_type": _dict(source_matrix.get("data")).get("matrix_type"),
        "source_matrix_version": _dict(source_matrix.get("data")).get("matrix_version"),
        "source_contract_versions": _source_contract_refs(),
        "point_count": len(entries),
        "sampling_candidate_count": len(candidates),
        "sampling_candidates": candidates,
        "coverage_summary": _coverage_summary(candidates=candidates),
        "coverage_gap_summary": _gap_summary(candidates=candidates),
        "priority_summary": _priority_summary(candidates=candidates),
        "known_limitations": _known_limitations(
            candidates=candidates,
            corpus_context=corpus_context,
        ),
        "tom_provenance": _tom_provenance(),
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "profile_type": COVERAGE_SAMPLING_PROFILE_TYPE,
        "profile_version": COVERAGE_SAMPLING_PROFILE_VERSION,
        "point_count": len(entries),
        "sampling_candidate_count": len(candidates),
        "coverage_gap_summary": profile["coverage_gap_summary"],
        "priority_summary": profile["priority_summary"],
        "profile": profile,
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profile, indent=2, sort_keys=True), encoding="utf-8")
        result["profile_output"] = str(path)
    return result


def validate_coverage_sampling_profile(
    *,
    contract_path: str | Path = DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
    profile_path: str | Path,
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
    dataset_corpus_contract_path: str | Path | None = (
        DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_COVERAGE_SAMPLING_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a coverage sampling profile structurally without executing sampling."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    profile_loaded = _load_json(profile_path, label="coverage_sampling_profile")
    if profile_loaded.get("ok") is False:
        return profile_loaded

    contract = _dict(contract_loaded["data"])
    profile = _dict(profile_loaded["data"])
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
            dataset_corpus_contract_path=dataset_corpus_contract_path,
        )
        errors.extend(_list(contract_result.get("errors")))
        structural_warnings.extend(_list(contract_result.get("structural_warnings")))
        contract_validations.extend(_list(contract_result.get("validations")))
        profile_result = _validate_profile_shape(profile=profile)
        errors.extend(_list(profile_result.get("errors")))
        structural_warnings.extend(_list(profile_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "coverage_sampling_profile_validation",
        "validation_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "profile_path": str(Path(profile_path)),
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
            "dataset_corpus_contract_path": _path_or_none(dataset_corpus_contract_path),
        },
        "contract_type": COVERAGE_SAMPLING_CONTRACT_TYPE,
        "contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "profile_type": COVERAGE_SAMPLING_PROFILE_TYPE,
        "profile_version": COVERAGE_SAMPLING_PROFILE_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "referenced_contract_validations": contract_validations,
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
        "known_limitations": [
            "Validation checks coverage profile structure and referenced contract versions only.",
            "Validation reports missing optional review and alignment refs as coverage gaps.",
            "Validation does not infer missing labels.",
            "Validation does not create labels.",
            "Validation does not judge label validity.",
            "Validation does not resolve reviewer disagreement.",
            "Validation does not execute sampling.",
            "Validation does not create dataset truth.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_coverage_sampling_report(
    *,
    contract_path: str | Path = DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
    profile_path: str | Path,
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
    dataset_corpus_contract_path: str | Path | None = (
        DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural coverage sampling report."""

    generated_at = generated_at or datetime.now(UTC)
    validation = validate_coverage_sampling_profile(
        contract_path=contract_path,
        profile_path=profile_path,
        observation_quality_taxonomy_path=observation_quality_taxonomy_path,
        review_label_schema_path=review_label_schema_path,
        reviewer_confidence_schema_path=reviewer_confidence_schema_path,
        multi_reviewer_schema_path=multi_reviewer_schema_path,
        intennse_alignment_contract_path=intennse_alignment_contract_path,
        dataset_corpus_contract_path=dataset_corpus_contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "ok": False,
            "status": "invalid_coverage_sampling_profile",
            "validation": validation,
            "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
        }

    profile_loaded = _load_json(profile_path, label="coverage_sampling_profile")
    if profile_loaded.get("ok") is False:
        return profile_loaded
    profile = _dict(profile_loaded["data"])
    candidate_reports = [
        _candidate_report(candidate)
        for candidate in _list(profile.get("sampling_candidates"))
        if isinstance(candidate, dict)
    ]
    summary = _report_summary(candidate_reports=candidate_reports)
    report = {
        "report_type": COVERAGE_SAMPLING_REPORT_TYPE,
        "report_version": COVERAGE_SAMPLING_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_profile_path": str(Path(profile_path)),
        "contract_path": str(Path(contract_path)),
        "point_count": profile.get("point_count"),
        "sampling_candidate_count": len(candidate_reports),
        "coverage_summary": profile.get("coverage_summary", {}),
        "coverage_gap_summary": profile.get("coverage_gap_summary", {}),
        "priority_summary": profile.get("priority_summary", {}),
        "candidate_reports": candidate_reports,
        "summary": summary,
        "missing_optional_refs": _missing_optional_refs(candidate_reports),
        "known_limitations": profile.get("known_limitations", []),
        "structural_warnings": validation.get("structural_warnings", []),
        "referenced_contract_validations": validation.get(
            "referenced_contract_validations",
            [],
        ),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(COVERAGE_SAMPLING_WARNINGS),
            "report_is_structural_only": True,
            "does_not_evaluate_tennis_quality": True,
            "does_not_execute_next_actions": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": COVERAGE_SAMPLING_REPORT_TYPE,
        "report_version": COVERAGE_SAMPLING_REPORT_VERSION,
        "sampling_candidate_count": len(candidate_reports),
        "summary": summary,
        "report": report,
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": COVERAGE_SAMPLING_CONTRACT_TYPE,
        "contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "profile_type": COVERAGE_SAMPLING_PROFILE_TYPE,
        "profile_version": COVERAGE_SAMPLING_PROFILE_VERSION,
        "report_type": COVERAGE_SAMPLING_REPORT_TYPE,
        "report_version": COVERAGE_SAMPLING_REPORT_VERSION,
        "strategy_scope": {
            "purpose": (
                "Describe structural evidence, provenance, review, and alignment "
                "coverage gaps for future controlled dataset expansion."
            ),
            "planning_only": True,
            "sampling_execution_allowed": False,
            "media_ingestion_allowed": False,
            "observation_generation_allowed": False,
            "truth_creation_allowed": False,
            "training_truth_allowed": False,
            "generalization_claim_allowed": False,
        },
        "source_contract_refs": _source_contract_refs(),
        "coverage_axes": [_axis_definition(axis) for axis in COVERAGE_AXES],
        "coverage_gap_types": [_gap_definition(gap) for gap in COVERAGE_GAP_TYPES],
        "sampling_priority_values": list(SAMPLING_PRIORITY_VALUES),
        "sampling_candidate_fields": [
            _candidate_field_definition(field) for field in CANDIDATE_FIELDS
        ],
        "allowed_next_action_values": list(NEXT_ACTION_VALUES),
        "provenance_requirements": {
            "source_corpus_manifest_path_required": True,
            "point_manifest_id_required": True,
            "media_id_required": True,
            "replay_url_preserved_when_available": True,
            "associated_run_ids_preserved_when_available": True,
            "coverage_gaps_are_structural_only": True,
            "missing_optional_refs_are_coverage_gaps": True,
            "next_actions_are_planning_labels_only": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "referenced_contract_versions_validated_when_paths_available": True,
            "source_profile_paths_must_exist_when_supplied": True,
            "sampling_candidate_required_fields_checked": True,
            "allowed_coverage_axes_only": True,
            "allowed_gap_types_only": True,
            "allowed_priority_values_only": True,
            "allowed_next_action_values_only": True,
            "does_not_infer_missing_labels": True,
            "does_not_create_labels": True,
            "does_not_validate_label_validity": True,
            "does_not_resolve_disagreement": True,
            "does_not_create_truth": True,
            "does_not_create_training_truth": True,
            "does_not_execute_sampling": True,
            "forbidden_fields": sorted(FORBIDDEN_COVERAGE_SAMPLING_FIELDS),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
    }


def _source_contract_refs() -> dict[str, str]:
    return {
        "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "intennse_label_alignment_contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "versioned_dataset_corpus_contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_manifest_version": POINT_MANIFEST_VERSION,
    }


def _axis_definition(axis: str) -> dict[str, Any]:
    return {
        "key": axis,
        "allowed_status_values": list(COVERAGE_AXIS_STATUS_VALUES),
        "structural_only": True,
        "planning_only": True,
        "warnings": dict(CANDIDATE_WARNINGS),
    }


def _gap_definition(gap: str) -> dict[str, Any]:
    return {
        "key": gap,
        "structural_only": True,
        "planning_only": True,
        "warnings": dict(CANDIDATE_WARNINGS),
    }


def _candidate_field_definition(field: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": field["key"],
        "required": field["required"],
        "value_set": field.get("value_set"),
        "structural_only": True,
        "planning_only": True,
        "warnings": dict(CANDIDATE_WARNINGS),
    }


def _validate_source_manifest(manifest: dict[str, Any]) -> dict[str, Any] | None:
    errors: list[dict[str, Any]] = []
    if manifest.get("corpus_manifest_type") != DATASET_CORPUS_MANIFEST_TYPE:
        errors.append(
            _error(
                "invalid_source_corpus_manifest_type",
                "corpus_manifest_type",
                manifest.get("corpus_manifest_type"),
            )
        )
    if manifest.get("corpus_manifest_version") != DATASET_CORPUS_MANIFEST_VERSION:
        errors.append(
            _error(
                "invalid_source_corpus_manifest_version",
                "corpus_manifest_version",
                manifest.get("corpus_manifest_version"),
            )
        )
    if not isinstance(manifest.get("corpus_entries"), list):
        errors.append(_error("corpus_entries_must_be_list", "corpus_entries", None))
    if not errors:
        return None
    return {
        "ok": False,
        "status": "invalid_source_corpus_manifest",
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
    }


def _load_optional_source(
    path: str | Path | None,
    *,
    label: str,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {"ok": True, "data": {}, "source_present": False}
    loaded = _load_json(path, label=label)
    if loaded.get("ok") is False:
        return loaded
    data = _dict(loaded["data"])
    if data.get(type_field) != expected_type:
        return _failed(
            f"invalid_{label}_type",
            f"{label} has unsupported type: {data.get(type_field)}",
        )
    if data.get(version_field) != expected_version:
        return _failed(
            f"invalid_{label}_version",
            f"{label} has unsupported version: {data.get(version_field)}",
        )
    return {"ok": True, "data": data, "source_present": True}


def _corpus_context(*, entries: list[dict[str, Any]]) -> dict[str, Any]:
    labels = [_string_list(entry.get("labels")) for entry in entries]
    protected_count = sum(1 for item in labels if "protected_sample_point" in item)
    stand_in_count = sum(1 for item in labels if "second_point_parity_stand_in" in item)
    media_ids = {
        media_id
        for media_id in (_string_or_none(entry.get("media_id")) for entry in entries)
        if media_id is not None
    }
    return {
        "point_count": len(entries),
        "distinct_media_count": len(media_ids),
        "protected_sample_point_count": protected_count,
        "second_point_parity_stand_in_count": stand_in_count,
        "single_point_only": len(entries) <= 1,
        "demo_stand_in_only": bool(entries) and stand_in_count == len(entries),
    }


def _sampling_candidate(
    *,
    entry: dict[str, Any],
    corpus_context: dict[str, Any],
) -> dict[str, Any]:
    labels = _string_list(entry.get("labels"))
    evidence = _bool_dict(entry.get("evidence_availability"))
    gaps = _coverage_gaps(entry=entry, labels=labels, corpus_context=corpus_context)
    axes = _coverage_axes(entry=entry, evidence=evidence, gaps=gaps, labels=labels)
    priority = _sampling_priority(gaps)
    next_action = _suggested_next_action(gaps=gaps, labels=labels)
    required_human_review = (
        "required"
        if "needs_human_review" in gaps
        or "missing_review_labels" in gaps
        or "missing_reviewer_confidence" in gaps
        else "not_assessed"
    )
    return {
        "sampling_candidate_id": _sampling_candidate_id(entry),
        "source_corpus_entry_id": _string_or_none(entry.get("corpus_entry_id")),
        "point_manifest_id": _string_or_none(entry.get("point_manifest_id")),
        "media_id": _string_or_none(entry.get("media_id")),
        "replay_url": _string_or_none(entry.get("replay_url")),
        "associated_run_ids": _string_dict(entry.get("associated_run_ids")),
        "labels": labels,
        "coverage_axes": axes,
        "coverage_gaps": gaps,
        "sampling_priority": priority,
        "priority_reason": _priority_reason(gaps=gaps, priority=priority),
        "required_human_review": required_human_review,
        "provenance_status": _string_or_none(entry.get("provenance_status"))
        or "not_assessed",
        "evidence_availability": evidence,
        "profile_counts": _int_dict(entry.get("profile_counts")),
        "suggested_next_action": next_action,
        "source_warnings": _bool_dict(entry.get("warnings")),
        "warnings": {
            **dict(CANDIDATE_WARNINGS),
            "coverage_gap_present": bool(gaps),
            "distinct_second_point_needed": "single_point_only" in gaps,
            "demo_stand_in_only": "demo_stand_in_only" in gaps,
        },
    }


def _coverage_gaps(
    *,
    entry: dict[str, Any],
    labels: list[str],
    corpus_context: dict[str, Any],
) -> list[str]:
    evidence = _bool_dict(entry.get("evidence_availability"))
    gaps: list[str] = []
    if evidence.get("media_indexed") is not True:
        gaps.append("missing_media")
    if evidence.get("replay_available") is not True:
        gaps.append("missing_replay")
    if _string_or_none(entry.get("point_manifest_id")) is None:
        gaps.append("missing_point_manifest")
    if evidence.get("event_candidates_available") is not True:
        gaps.append("missing_event_candidates")
    if evidence.get("trajectory_3d_candidates_available") is not True:
        gaps.append("missing_trajectory_3d")
    if evidence.get("review_annotations_available") is not True:
        gaps.append("missing_review_annotations")
    if _string_or_none(entry.get("observation_quality_profile_path")) is None:
        gaps.extend(["missing_observation_quality_profile", "unknown_quality"])
    if not _list(entry.get("review_label_bundle_refs")):
        gaps.append("missing_review_labels")
    if not _list(entry.get("reviewer_confidence_bundle_refs")):
        gaps.append("missing_reviewer_confidence")
    if not _list(entry.get("multi_reviewer_review_set_refs")):
        gaps.append("missing_multi_reviewer_review")
    if not _list(entry.get("disagreement_report_refs")):
        gaps.append("missing_disagreement_report")
    if not _list(entry.get("intennse_alignment_refs")):
        gaps.append("missing_intennse_alignment")
    if entry.get("provenance_status") != "provenance_present":
        gaps.append("missing_provenance")
    if entry.get("requires_human_review") == "required":
        gaps.append("needs_human_review")
    if corpus_context.get("single_point_only") is True:
        gaps.append("single_point_only")
    if "second_point_parity_stand_in" in labels:
        gaps.append("demo_stand_in_only")
    return sorted(set(gaps), key=COVERAGE_GAP_TYPES.index)


def _coverage_axes(
    *,
    entry: dict[str, Any],
    evidence: dict[str, bool],
    gaps: list[str],
    labels: list[str],
) -> dict[str, str]:
    return {
        "media_presence": _covered_if(evidence.get("media_indexed")),
        "replay_availability": _covered_if(evidence.get("replay_available")),
        "point_manifest_availability": (
            "covered" if _string_or_none(entry.get("point_manifest_id")) else "gap"
        ),
        "event_candidate_availability": _covered_if(
            evidence.get("event_candidates_available")
        ),
        "trajectory_3d_availability": _covered_if(
            evidence.get("trajectory_3d_candidates_available")
        ),
        "review_annotation_availability": _covered_if(
            evidence.get("review_annotations_available")
        ),
        "observation_quality_coverage": (
            "gap"
            if "missing_observation_quality_profile" in gaps
            else "covered"
        ),
        "review_label_coverage": "gap" if "missing_review_labels" in gaps else "covered",
        "reviewer_confidence_coverage": (
            "gap" if "missing_reviewer_confidence" in gaps else "covered"
        ),
        "multi_reviewer_coverage": (
            "gap" if "missing_multi_reviewer_review" in gaps else "covered"
        ),
        "disagreement_coverage": (
            "gap" if "missing_disagreement_report" in gaps else "covered"
        ),
        "intennse_alignment_coverage": (
            "gap" if "missing_intennse_alignment" in gaps else "covered"
        ),
        "provenance_completeness": (
            "gap" if "missing_provenance" in gaps else "covered"
        ),
        "regression_protection_coverage": (
            "covered" if "protected_sample_point" in labels else "not_applicable"
        ),
        "second_point_distinctness": (
            "gap"
            if "single_point_only" in gaps or "demo_stand_in_only" in gaps
            else "covered"
        ),
        "evidence_diversity": (
            "gap" if "single_point_only" in gaps else "partial" if gaps else "covered"
        ),
    }


def _covered_if(value: bool | None) -> str:
    if value is True:
        return "covered"
    if value is False:
        return "gap"
    return "unknown"


def _sampling_priority(gaps: list[str]) -> str:
    if any(gap in gaps for gap in ("missing_media", "missing_replay", "missing_point_manifest")):
        return "blocked"
    if any(
        gap in gaps
        for gap in (
            "single_point_only",
            "missing_event_candidates",
            "missing_trajectory_3d",
            "demo_stand_in_only",
        )
    ):
        return "high"
    if any(
        gap in gaps
        for gap in (
            "missing_review_labels",
            "missing_reviewer_confidence",
            "missing_multi_reviewer_review",
            "missing_disagreement_report",
            "missing_intennse_alignment",
            "missing_observation_quality_profile",
        )
    ):
        return "medium"
    if gaps:
        return "low"
    return "not_applicable"


def _priority_reason(*, gaps: list[str], priority: str) -> str:
    if not gaps:
        return "no_coverage_gap_present"
    for gap in (
        "single_point_only",
        "demo_stand_in_only",
        "missing_media",
        "missing_replay",
        "missing_point_manifest",
        "missing_event_candidates",
        "missing_trajectory_3d",
    ):
        if gap in gaps:
            return f"{priority}_priority_due_to_{gap}"
    return f"{priority}_priority_due_to_{gaps[0]}"


def _suggested_next_action(*, gaps: list[str], labels: list[str]) -> str:
    if "single_point_only" in gaps:
        return "collect_distinct_second_point"
    if "demo_stand_in_only" in gaps:
        return "collect_additional_point_candidate"
    if "missing_review_labels" in gaps:
        return "add_human_review_labels"
    if "missing_reviewer_confidence" in gaps:
        return "add_reviewer_confidence_bundle"
    if "missing_multi_reviewer_review" in gaps:
        return "add_multi_reviewer_review"
    if "missing_intennse_alignment" in gaps:
        return "add_intennse_alignment_reference"
    if "missing_provenance" in gaps:
        return "improve_provenance_reference"
    if "protected_sample_point" in labels:
        return "preserve_regression_protected_sample"
    return "no_action"


def _coverage_summary(*, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, dict[str, int]] = {
        axis: {status: 0 for status in COVERAGE_AXIS_STATUS_VALUES}
        for axis in COVERAGE_AXES
    }
    for candidate in candidates:
        axes = _dict(candidate.get("coverage_axes"))
        for axis in COVERAGE_AXES:
            status = str(axes.get(axis) or "unknown")
            counts[axis][status] = counts[axis].get(status, 0) + 1
    return {
        "axis_status_counts": counts,
        "structural_coverage_only": True,
        "does_not_execute_sampling": True,
    }


def _gap_summary(*, candidates: list[dict[str, Any]]) -> dict[str, int]:
    counts = {gap: 0 for gap in COVERAGE_GAP_TYPES}
    for candidate in candidates:
        for gap in _string_list(candidate.get("coverage_gaps")):
            counts[gap] = counts.get(gap, 0) + 1
    return {key: value for key, value in counts.items() if value}


def _priority_summary(*, candidates: list[dict[str, Any]]) -> dict[str, int]:
    counts = {priority: 0 for priority in SAMPLING_PRIORITY_VALUES}
    for candidate in candidates:
        priority = str(candidate.get("sampling_priority") or "not_assessed")
        counts[priority] = counts.get(priority, 0) + 1
    return {key: value for key, value in counts.items() if value}


def _known_limitations(
    *,
    candidates: list[dict[str, Any]],
    corpus_context: dict[str, Any],
) -> list[dict[str, Any]]:
    limitations: list[dict[str, Any]] = []
    if corpus_context.get("single_point_only") is True:
        limitations.append(
            _limitation(
                "single_point_only",
                "collect_distinct_second_point",
                planning_label="distinct_second_point_needed",
            )
        )
    if corpus_context.get("second_point_parity_stand_in_count", 0):
        limitations.append(_limitation("demo_stand_in_only", "collect_additional_point_candidate"))
    gaps = _gap_summary(candidates=candidates)
    for gap, action in (
        ("missing_review_labels", "add_human_review_labels"),
        ("missing_reviewer_confidence", "add_reviewer_confidence_bundle"),
        ("missing_multi_reviewer_review", "add_multi_reviewer_review"),
        ("missing_intennse_alignment", "add_intennse_alignment_reference"),
        ("missing_provenance", "improve_provenance_reference"),
    ):
        if gaps.get(gap):
            limitations.append(_limitation(gap, action))
    return limitations


def _limitation(
    limitation_type: str,
    suggested_next_action: str,
    *,
    planning_label: str | None = None,
) -> dict[str, Any]:
    limitation = {
        "limitation_type": limitation_type,
        "suggested_next_action": suggested_next_action,
        "planning_only": True,
        "does_not_execute_sampling": True,
        "not_generalization_claim": True,
    }
    if planning_label is not None:
        limitation["planning_label"] = planning_label
    return limitation


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != COVERAGE_SAMPLING_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != COVERAGE_SAMPLING_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "strategy_scope",
        "source_contract_refs",
        "coverage_axes",
        "coverage_gap_types",
        "sampling_priority_values",
        "sampling_candidate_fields",
        "allowed_next_action_values",
        "provenance_requirements",
        "validation_rules",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors

    errors.extend(
        _source_contract_ref_errors(
            _dict(contract.get("source_contract_refs")),
            path="contract",
        )
    )
    contract_axes = {
        item.get("key")
        for item in _list(contract.get("coverage_axes"))
        if isinstance(item, dict)
    }
    if not set(COVERAGE_AXES) <= contract_axes:
        errors.append(
            _error(
                "missing_coverage_axes",
                "coverage_axes",
                sorted(set(COVERAGE_AXES) - contract_axes),
            )
        )
    contract_gaps = {
        item.get("key")
        for item in _list(contract.get("coverage_gap_types"))
        if isinstance(item, dict)
    }
    if not set(COVERAGE_GAP_TYPES) <= contract_gaps:
        errors.append(
            _error(
                "missing_coverage_gap_types",
                "coverage_gap_types",
                sorted(set(COVERAGE_GAP_TYPES) - contract_gaps),
            )
        )
    if set(_string_list(contract.get("sampling_priority_values"))) != set(
        SAMPLING_PRIORITY_VALUES
    ):
        errors.append(
            _error(
                "invalid_sampling_priority_values",
                "sampling_priority_values",
                contract.get("sampling_priority_values"),
            )
        )
    if set(_string_list(contract.get("allowed_next_action_values"))) != set(
        NEXT_ACTION_VALUES
    ):
        errors.append(
            _error(
                "invalid_next_action_values",
                "allowed_next_action_values",
                contract.get("allowed_next_action_values"),
            )
        )
    rules = _dict(contract.get("validation_rules"))
    for rule in (
        "structural_validation_only",
        "referenced_contract_versions_validated_when_paths_available",
        "source_profile_paths_must_exist_when_supplied",
        "sampling_candidate_required_fields_checked",
        "allowed_coverage_axes_only",
        "allowed_gap_types_only",
        "allowed_priority_values_only",
        "allowed_next_action_values_only",
        "does_not_infer_missing_labels",
        "does_not_create_labels",
        "does_not_validate_label_validity",
        "does_not_resolve_disagreement",
        "does_not_create_truth",
        "does_not_create_training_truth",
        "does_not_execute_sampling",
    ):
        if rules.get(rule) is not True:
            errors.append(
                _error("invalid_validation_rule", f"validation_rules.{rule}", rules.get(rule))
            )
    return errors


def _validate_profile_shape(profile: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(profile, path="coverage_sampling_profile")
    structural_warnings: list[dict[str, Any]] = []
    if profile.get("profile_type") != COVERAGE_SAMPLING_PROFILE_TYPE:
        errors.append(
            _error("invalid_profile_type", "profile_type", profile.get("profile_type"))
        )
    if profile.get("profile_version") != COVERAGE_SAMPLING_PROFILE_VERSION:
        errors.append(
            _error(
                "invalid_profile_version",
                "profile_version",
                profile.get("profile_version"),
            )
        )
    if profile.get("contract_version") != COVERAGE_SAMPLING_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_profile_contract_version",
                "contract_version",
                profile.get("contract_version"),
            )
        )
    errors.extend(
        _source_contract_ref_errors(
            _dict(profile.get("source_contract_versions")),
            path="coverage_sampling_profile",
        )
    )
    for path_key in ("source_corpus_manifest_path", "source_index_path", "source_matrix_path"):
        path_value = _string_or_none(profile.get(path_key))
        if path_value is None:
            if path_key == "source_corpus_manifest_path":
                errors.append(_error("missing_source_path", path_key, path_value))
            continue
        if not Path(path_value).expanduser().is_file():
            errors.append(_error("source_path_not_found", path_key, path_value))

    candidates = profile.get("sampling_candidates")
    if not isinstance(candidates, list):
        errors.append(_error("sampling_candidates_must_be_list", "sampling_candidates", None))
        return {"errors": errors, "structural_warnings": structural_warnings}
    for index, candidate in enumerate(candidates):
        path = f"sampling_candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(_error("sampling_candidate_must_be_object", path, candidate))
            continue
        candidate_result = _validate_candidate(candidate=candidate, path=path)
        errors.extend(_list(candidate_result.get("errors")))
        structural_warnings.extend(_list(candidate_result.get("structural_warnings")))
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_candidate(*, candidate: dict[str, Any], path: str) -> dict[str, Any]:
    errors = _forbidden_field_errors(candidate, path=path)
    structural_warnings: list[dict[str, Any]] = []
    for field in CANDIDATE_FIELDS:
        if field["required"] and field["key"] not in candidate:
            errors.append(
                _error(
                    "missing_sampling_candidate_field",
                    f"{path}.{field['key']}",
                    None,
                )
            )
    for field in (
        "sampling_candidate_id",
        "source_corpus_entry_id",
        "point_manifest_id",
        "media_id",
    ):
        if _string_or_none(candidate.get(field)) is None:
            errors.append(
                _error("invalid_sampling_candidate_field", f"{path}.{field}", candidate.get(field))
            )
    axes = _dict(candidate.get("coverage_axes"))
    if set(axes) - set(COVERAGE_AXES):
        errors.append(
            _error(
                "unknown_coverage_axis",
                f"{path}.coverage_axes",
                sorted(set(axes) - set(COVERAGE_AXES)),
            )
        )
    for axis, value in axes.items():
        if value not in COVERAGE_AXIS_STATUS_VALUES:
            errors.append(
                _error(
                    "invalid_coverage_axis_status",
                    f"{path}.coverage_axes.{axis}",
                    value,
                )
            )
    for gap in _string_list(candidate.get("coverage_gaps")):
        if gap not in COVERAGE_GAP_TYPES:
            errors.append(_error("invalid_coverage_gap", f"{path}.coverage_gaps", gap))
        elif gap != "not_applicable":
            structural_warnings.append(
                _warning("coverage_gap_present", f"{path}.coverage_gaps", gap)
            )
    if candidate.get("sampling_priority") not in SAMPLING_PRIORITY_VALUES:
        errors.append(
            _error(
                "invalid_sampling_priority",
                f"{path}.sampling_priority",
                candidate.get("sampling_priority"),
            )
        )
    if candidate.get("suggested_next_action") not in NEXT_ACTION_VALUES:
        errors.append(
            _error(
                "invalid_suggested_next_action",
                f"{path}.suggested_next_action",
                candidate.get("suggested_next_action"),
            )
        )
    if candidate.get("required_human_review") not in HUMAN_REVIEW_VALUES:
        errors.append(
            _error(
                "invalid_required_human_review",
                f"{path}.required_human_review",
                candidate.get("required_human_review"),
            )
        )
    for field in (
        "coverage_axes",
        "associated_run_ids",
        "evidence_availability",
        "profile_counts",
        "warnings",
    ):
        if field in candidate and not isinstance(candidate[field], dict):
            errors.append(
                _error(
                    "sampling_candidate_field_must_be_object",
                    f"{path}.{field}",
                    candidate[field],
                )
            )
    for field in ("labels", "coverage_gaps"):
        if field in candidate and not isinstance(candidate[field], list):
            errors.append(
                _error(
                    "sampling_candidate_field_must_be_list",
                    f"{path}.{field}",
                    candidate[field],
                )
            )
    return {"errors": errors, "structural_warnings": _dedupe_warnings(structural_warnings)}


def _validate_referenced_contracts(
    *,
    observation_quality_taxonomy_path: str | Path | None,
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
    multi_reviewer_schema_path: str | Path | None,
    intennse_alignment_contract_path: str | Path | None,
    dataset_corpus_contract_path: str | Path | None,
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
        {
            "contract": "versioned_dataset_corpus_contract",
            "path": dataset_corpus_contract_path,
            "type_field": "contract_type",
            "expected_type": DATASET_CORPUS_CONTRACT_TYPE,
            "version_field": "contract_version",
            "expected_version": DATASET_CORPUS_CONTRACT_VERSION,
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


def _source_contract_ref_errors(refs: dict[str, Any], *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    expected = _source_contract_refs()
    for key, expected_value in expected.items():
        if refs.get(key) != expected_value:
            errors.append(
                _error(
                    "invalid_source_contract_ref",
                    f"{path}.source_contract_refs.{key}",
                    refs.get(key),
                )
            )
    return errors


def _candidate_report(candidate: dict[str, Any]) -> dict[str, Any]:
    gaps = _string_list(candidate.get("coverage_gaps"))
    return {
        "structural_sampling_candidate": True,
        "sampling_candidate_id": candidate.get("sampling_candidate_id"),
        "source_corpus_entry_id": candidate.get("source_corpus_entry_id"),
        "point_manifest_id": candidate.get("point_manifest_id"),
        "media_id": candidate.get("media_id"),
        "sampling_priority": candidate.get("sampling_priority"),
        "priority_reason": candidate.get("priority_reason"),
        "suggested_next_action": candidate.get("suggested_next_action"),
        "required_human_review": candidate.get("required_human_review"),
        "provenance_status": candidate.get("provenance_status"),
        "coverage_gap_present": bool(gaps),
        "coverage_gaps": gaps,
        "coverage_axes": _dict(candidate.get("coverage_axes")),
        "missing_optional_ref_types": [
            gap
            for gap in gaps
            if gap
            in {
                "missing_observation_quality_profile",
                "missing_review_labels",
                "missing_reviewer_confidence",
                "missing_multi_reviewer_review",
                "missing_disagreement_report",
                "missing_intennse_alignment",
            }
        ],
        "warnings": {
            "structural_coverage_only": True,
            "planning_only": True,
            "does_not_execute_sampling": True,
            "does_not_evaluate_tennis_quality": True,
        },
    }


def _report_summary(*, candidate_reports: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "sampling_candidate_count": len(candidate_reports),
        "coverage_gap_present_count": sum(
            1 for report in candidate_reports if report.get("coverage_gap_present") is True
        ),
        "high_priority_count": sum(
            1 for report in candidate_reports if report.get("sampling_priority") == "high"
        ),
        "medium_priority_count": sum(
            1 for report in candidate_reports if report.get("sampling_priority") == "medium"
        ),
        "blocked_priority_count": sum(
            1 for report in candidate_reports if report.get("sampling_priority") == "blocked"
        ),
        "requires_human_review_count": sum(
            1
            for report in candidate_reports
            if report.get("required_human_review") == "required"
        ),
        "distinct_second_point_needed_count": sum(
            1
            for report in candidate_reports
            if "single_point_only" in _string_list(report.get("coverage_gaps"))
        ),
        "demo_stand_in_only_count": sum(
            1
            for report in candidate_reports
            if "demo_stand_in_only" in _string_list(report.get("coverage_gaps"))
        ),
    }


def _missing_optional_refs(
    candidate_reports: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for report in candidate_reports:
        for gap in _string_list(report.get("missing_optional_ref_types")):
            refs.append(
                {
                    "coverage_gap_type": gap,
                    "sampling_candidate_id": report.get("sampling_candidate_id"),
                    "point_manifest_id": report.get("point_manifest_id"),
                    "planning_only": True,
                    "does_not_execute_sampling": True,
                }
            )
    return refs


def _sampling_candidate_id(entry: dict[str, Any]) -> str:
    payload = json.dumps(
        {
            "corpus_entry_id": entry.get("corpus_entry_id"),
            "point_manifest_id": entry.get("point_manifest_id"),
            "media_id": entry.get("media_id"),
        },
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"coverage_sampling_candidate_v1_{digest}"


def _corpus_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry for entry in _list(manifest.get("corpus_entries")) if isinstance(entry, dict)
    ]


def _dedupe_warnings(warnings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for warning in warnings:
        key = (
            str(warning.get("warning_type")),
            str(warning.get("field")),
            str(warning.get("value")),
        )
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
            if key in FORBIDDEN_COVERAGE_SAMPLING_FIELDS:
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
        "planning_only": True,
        "no_adjudication": True,
    }


def _warning(warning_type: str, field: str, value: Any) -> dict[str, Any]:
    return {
        "warning_type": warning_type,
        "field": field,
        "value": value,
        "structural_only": True,
        "planning_only": True,
        "no_adjudication": True,
    }


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": COVERAGE_SAMPLING_BLUEPRINT,
        "blueprint_name": COVERAGE_SAMPLING_BLUEPRINT_NAME,
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
        "contract_type": COVERAGE_SAMPLING_CONTRACT_TYPE,
        "contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "warnings": dict(COVERAGE_SAMPLING_WARNINGS),
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
