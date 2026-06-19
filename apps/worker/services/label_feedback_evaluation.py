from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_CONTRACT_TYPE,
    COVERAGE_SAMPLING_CONTRACT_VERSION,
    COVERAGE_SAMPLING_PROFILE_TYPE,
    COVERAGE_SAMPLING_PROFILE_VERSION,
    COVERAGE_SAMPLING_REPORT_TYPE,
    COVERAGE_SAMPLING_REPORT_VERSION,
    DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
)
from apps.worker.services.intennse_label_alignment import (
    DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    INTENNSE_ALIGNMENT_CONTRACT_TYPE,
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
)
from apps.worker.services.many_point_ingestion_gate import (
    DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    MANY_POINT_INGESTION_CONTRACT_TYPE,
    MANY_POINT_INGESTION_CONTRACT_VERSION,
)
from apps.worker.services.multi_point_regression_matrix import (
    DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    MULTI_POINT_REGRESSION_MATRIX_TYPE,
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
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
from apps.worker.services.review_ops_metrics import (
    DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT,
    DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
    DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
    REVIEW_OPS_DASHBOARD_DATA_TYPE,
    REVIEW_OPS_DASHBOARD_DATA_VERSION,
    REVIEW_OPS_METRICS_CONTRACT_TYPE,
    REVIEW_OPS_METRICS_CONTRACT_VERSION,
    REVIEW_OPS_METRICS_REPORT_TYPE,
    REVIEW_OPS_METRICS_REPORT_VERSION,
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

LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE = "label_feedback_evaluation_contract"
LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION = "v1"
LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE = "label_feedback_evaluation_inputs"
LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION = "v1"
LABEL_FEEDBACK_EVALUATION_REPORT_TYPE = "label_feedback_evaluation_report"
LABEL_FEEDBACK_EVALUATION_REPORT_VERSION = "v1"
LABEL_FEEDBACK_BLUEPRINT = "blueprint_35"
LABEL_FEEDBACK_BLUEPRINT_NAME = "label_feedback_loop_evaluation_harness_v1"

DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT = (
    ".data/contracts/label_feedback_evaluation_contract_v1.json"
)
DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT = (
    ".data/exports/label_feedback_evaluation_inputs.current.json"
)
DEFAULT_LABEL_FEEDBACK_EVALUATION_VALIDATION_OUTPUT = (
    ".data/exports/label_feedback_evaluation_inputs.validation.json"
)
DEFAULT_LABEL_FEEDBACK_EVALUATION_REPORT_OUTPUT = (
    ".data/exports/label_feedback_evaluation_report.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)

FEEDBACK_INPUT_ENTITIES = [
    "feedback_bundle",
    "feedback_entry",
    "corpus_entry_ref",
    "point_manifest_ref",
    "review_label_bundle_ref",
    "reviewer_confidence_bundle_ref",
    "multi_reviewer_review_set_ref",
    "disagreement_report_ref",
    "intennse_alignment_ref",
    "evaluation_case_ref",
    "regression_case_ref",
    "coverage_gap_ref",
    "provenance_ref",
]

FEEDBACK_ENTRY_FIELDS = [
    "feedback_entry_id",
    "source_corpus_entry_id",
    "point_manifest_id",
    "media_id",
    "replay_url",
    "associated_run_ids",
    "review_label_bundle_refs",
    "reviewer_confidence_bundle_refs",
    "multi_reviewer_review_set_refs",
    "disagreement_report_refs",
    "intennse_alignment_refs",
    "observation_quality_refs",
    "corpus_manifest_ref",
    "coverage_sampling_ref",
    "review_ops_metrics_ref",
    "evaluation_signal_type",
    "evaluation_signal_status",
    "evaluation_harness_action",
    "provenance_status",
    "requires_human_review",
    "warnings",
]

EVALUATION_SIGNAL_TYPES = [
    "not_assessed",
    "structural_review_available",
    "structural_review_missing",
    "reviewer_confidence_available",
    "reviewer_confidence_missing",
    "multi_reviewer_review_available",
    "disagreement_present",
    "disagreement_missing",
    "intennse_alignment_available",
    "intennse_alignment_missing",
    "provenance_partial",
    "provenance_missing",
    "coverage_gap_present",
    "regression_protected_entry",
    "not_applicable",
]

EVALUATION_SIGNAL_STATUSES = [
    "not_assessed",
    "present",
    "missing",
    "partial",
    "structurally_usable",
    "structurally_blocked",
    "requires_human_review",
    "not_applicable",
]

EVALUATION_HARNESS_ACTIONS = [
    "no_action",
    "include_as_structural_eval_case",
    "include_as_review_coverage_case",
    "include_as_regression_context",
    "flag_missing_review_artifact",
    "flag_missing_confidence_artifact",
    "flag_missing_disagreement_artifact",
    "flag_missing_intennse_alignment",
    "flag_provenance_gap",
    "preserve_regression_protected_sample",
    "not_applicable",
]

FORBIDDEN_LABEL_FEEDBACK_FIELDS = {
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
    "quality_score",
    "training_truth",
    "model_ready_truth",
    "pass_due_to_label",
    "fail_due_to_label",
}

LABEL_FEEDBACK_WARNINGS = {
    "label_feedback_evaluation_is_not_truth": True,
    "evaluation_bridge_is_structural_only": True,
    "feedback_loop_does_not_create_labels": True,
    "feedback_loop_does_not_create_training_truth": True,
    "feedback_loop_does_not_change_model_behavior": True,
    "feedback_loop_does_not_modify_baselines": True,
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
    "does_not_ingest_media": True,
    "does_not_execute_sampling": True,
    "does_not_rank_reviewers": True,
    "does_not_score_reviewers": True,
    "does_not_resolve_disagreement": True,
    "not_generalization_claim": True,
}

ENTRY_WARNINGS = {
    "structural_feedback_entry": True,
    "evaluation_routing_only": True,
    "human_review_artifacts_are_not_truth": True,
    "no_adjudication": True,
    "does_not_create_labels": True,
    "does_not_modify_evaluation_baselines": True,
}


def export_label_feedback_evaluation_contract(
    *,
    output_path: str | Path | None = DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen label-feedback evaluation bridge contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE,
        "contract_version": LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
        "feedback_inputs_type": LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        "feedback_inputs_version": LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
        "report_type": LABEL_FEEDBACK_EVALUATION_REPORT_TYPE,
        "report_version": LABEL_FEEDBACK_EVALUATION_REPORT_VERSION,
        "contract": contract,
        "warnings": dict(LABEL_FEEDBACK_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_label_feedback_evaluation_inputs(
    *,
    contract_path: str | Path = DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
    corpus_manifest_path: str | Path | None = DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    review_ops_metrics_report_path: str | Path | None = (
        DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT
    ),
    review_ops_dashboard_data_path: str | Path | None = (
        DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT
    ),
    coverage_sampling_profile_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT
    ),
    coverage_sampling_report_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT
    ),
    multi_point_regression_matrix_path: str | Path | None = (
        DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT
    ),
    output_path: str | Path | None = DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural feedback bundle for evaluation harness routing."""

    generated_at = generated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="label_feedback_evaluation_contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    contract = _dict(contract_loaded["data"])
    contract_errors = _validate_contract_shape(contract)
    if contract_errors:
        return {
            "ok": False,
            "status": "invalid_label_feedback_evaluation_contract",
            "error_count": len(contract_errors),
            "errors": contract_errors,
            "warnings": dict(LABEL_FEEDBACK_WARNINGS),
        }

    corpus_source = _load_optional_json(
        corpus_manifest_path,
        label="corpus_manifest",
        type_field="corpus_manifest_type",
        expected_type=DATASET_CORPUS_MANIFEST_TYPE,
        version_field="corpus_manifest_version",
        expected_version=DATASET_CORPUS_MANIFEST_VERSION,
    )
    review_ops_source = _load_optional_json(
        review_ops_metrics_report_path,
        label="review_ops_metrics_report",
        type_field="report_type",
        expected_type=REVIEW_OPS_METRICS_REPORT_TYPE,
        version_field="report_version",
        expected_version=REVIEW_OPS_METRICS_REPORT_VERSION,
    )
    dashboard_source = _load_optional_json(
        review_ops_dashboard_data_path,
        label="review_ops_dashboard_data",
        type_field="dashboard_data_type",
        expected_type=REVIEW_OPS_DASHBOARD_DATA_TYPE,
        version_field="dashboard_data_version",
        expected_version=REVIEW_OPS_DASHBOARD_DATA_VERSION,
    )
    coverage_profile_source = _load_optional_json(
        coverage_sampling_profile_path,
        label="coverage_sampling_profile",
        type_field="profile_type",
        expected_type=COVERAGE_SAMPLING_PROFILE_TYPE,
        version_field="profile_version",
        expected_version=COVERAGE_SAMPLING_PROFILE_VERSION,
    )
    coverage_report_source = _load_optional_json(
        coverage_sampling_report_path,
        label="coverage_sampling_report",
        type_field="report_type",
        expected_type=COVERAGE_SAMPLING_REPORT_TYPE,
        version_field="report_version",
        expected_version=COVERAGE_SAMPLING_REPORT_VERSION,
    )
    matrix_source = _load_optional_json(
        multi_point_regression_matrix_path,
        label="multi_point_regression_matrix",
        type_field="matrix_type",
        expected_type=MULTI_POINT_REGRESSION_MATRIX_TYPE,
        version_field="matrix_version",
        expected_version=MULTI_POINT_REGRESSION_MATRIX_VERSION,
    )
    sources = {
        "corpus_manifest": corpus_source,
        "review_ops_metrics_report": review_ops_source,
        "review_ops_dashboard_data": dashboard_source,
        "coverage_sampling_profile": coverage_profile_source,
        "coverage_sampling_report": coverage_report_source,
        "multi_point_regression_matrix": matrix_source,
    }

    corpus_manifest = _dict(corpus_source.get("data"))
    coverage_profile = _dict(coverage_profile_source.get("data"))
    coverage_report = _dict(coverage_report_source.get("data"))
    matrix = _dict(matrix_source.get("data"))
    review_ops_report = _dict(review_ops_source.get("data"))
    entries = _corpus_entries(corpus_manifest)
    source_paths = {
        "contract_path": str(Path(contract_path)),
        "corpus_manifest_path": _path_or_none(corpus_manifest_path),
        "review_ops_metrics_report_path": _path_or_none(review_ops_metrics_report_path),
        "review_ops_dashboard_data_path": _path_or_none(review_ops_dashboard_data_path),
        "coverage_sampling_profile_path": _path_or_none(coverage_sampling_profile_path),
        "coverage_sampling_report_path": _path_or_none(coverage_sampling_report_path),
        "multi_point_regression_matrix_path": _path_or_none(
            multi_point_regression_matrix_path
        ),
    }
    feedback_entries = _feedback_entries(
        entries=entries,
        source_paths=source_paths,
        coverage_profile=coverage_profile,
        coverage_report=coverage_report,
        matrix=matrix,
        review_ops_report=review_ops_report,
    )
    source_warnings = _source_warnings(sources)
    bundle = {
        "feedback_inputs_type": LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        "feedback_inputs_version": LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
        "feedback_bundle_id": _bundle_id(feedback_entries),
        "generated_at": generated_at.isoformat(),
        "source_paths": source_paths,
        "source_statuses": _source_statuses(sources),
        "source_contract_versions": _source_contract_refs(),
        "feedback_entry_count": len(feedback_entries),
        "feedback_entries": feedback_entries,
        "summary": _summary_counts(feedback_entries),
        "source_warnings": source_warnings,
        "review_ops_summary": _dict(review_ops_report.get("summary")),
        "review_ops_dashboard_card_count": len(
            _list(_dict(dashboard_source.get("data")).get("cards"))
        ),
        "known_limitations": _known_limitations(
            entry_count=len(feedback_entries),
            source_warnings=source_warnings,
        ),
        "validation_summary": {
            "status": "not_assessed",
            "structural_error_count": 0,
            "structural_warning_count": len(source_warnings),
            "validation_does_not_create_labels": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(LABEL_FEEDBACK_WARNINGS),
            "missing_review_artifacts_are_structural_gaps": True,
            "evaluation_actions_are_routing_only": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "feedback_inputs_type": LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        "feedback_inputs_version": LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
        "feedback_entry_count": len(feedback_entries),
        "summary": bundle["summary"],
        "feedback_inputs": bundle,
        "warnings": dict(LABEL_FEEDBACK_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        result["feedback_inputs_output"] = str(path)
    return result


def validate_label_feedback_evaluation_inputs(
    *,
    contract_path: str | Path = DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
    feedback_inputs_path: str | Path,
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
    coverage_sampling_contract_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT
    ),
    many_point_ingestion_contract_path: str | Path | None = (
        DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT
    ),
    review_ops_metrics_contract_path: str | Path | None = (
        DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_LABEL_FEEDBACK_EVALUATION_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate feedback inputs structurally without interpreting labels."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="label_feedback_evaluation_contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    inputs_loaded = _load_json(feedback_inputs_path, label="label_feedback_evaluation_inputs")
    if inputs_loaded.get("ok") is False:
        return inputs_loaded
    contract = _dict(contract_loaded["data"])
    feedback_inputs = _dict(inputs_loaded["data"])
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
            coverage_sampling_contract_path=coverage_sampling_contract_path,
            many_point_ingestion_contract_path=many_point_ingestion_contract_path,
            review_ops_metrics_contract_path=review_ops_metrics_contract_path,
        )
        errors.extend(_list(contract_result.get("errors")))
        structural_warnings.extend(_list(contract_result.get("structural_warnings")))
        contract_validations.extend(_list(contract_result.get("validations")))
        inputs_result = _validate_feedback_inputs_shape(feedback_inputs)
        errors.extend(_list(inputs_result.get("errors")))
        structural_warnings.extend(_list(inputs_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "label_feedback_evaluation_inputs_validation",
        "validation_version": LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "feedback_inputs_path": str(Path(feedback_inputs_path)),
        "contract_type": LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE,
        "contract_version": LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
        "feedback_inputs_type": LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        "feedback_inputs_version": LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "referenced_contract_validations": contract_validations,
        "warnings": dict(LABEL_FEEDBACK_WARNINGS),
        "known_limitations": [
            "Validation checks contract, feedback-input, signal, status, and action shape.",
            "Validation reports missing optional review artifacts as structural gaps.",
            "Validation does not infer missing labels.",
            "Validation does not create labels.",
            "Validation does not rank reviewers.",
            "Validation does not resolve disagreement.",
            "Validation does not create training truth.",
            "Validation does not modify evaluation baselines.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_label_feedback_evaluation_report(
    *,
    contract_path: str | Path = DEFAULT_LABEL_FEEDBACK_EVALUATION_CONTRACT_OUTPUT,
    feedback_inputs_path: str | Path = DEFAULT_LABEL_FEEDBACK_EVALUATION_INPUTS_OUTPUT,
    output_path: str | Path | None = DEFAULT_LABEL_FEEDBACK_EVALUATION_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a structural label-feedback evaluation report."""

    generated_at = generated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="label_feedback_evaluation_contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    inputs_loaded = _load_json(feedback_inputs_path, label="label_feedback_evaluation_inputs")
    if inputs_loaded.get("ok") is False:
        return inputs_loaded
    contract = _dict(contract_loaded["data"])
    feedback_inputs = _dict(inputs_loaded["data"])
    errors = _validate_contract_shape(contract)
    errors.extend(_list(_validate_feedback_inputs_shape(feedback_inputs).get("errors")))
    if errors:
        return {
            "ok": False,
            "status": "invalid_feedback_inputs",
            "error_count": len(errors),
            "errors": errors,
            "warnings": dict(LABEL_FEEDBACK_WARNINGS),
        }
    entries = [
        entry for entry in _list(feedback_inputs.get("feedback_entries")) if isinstance(entry, dict)
    ]
    action_counts = Counter()
    signal_counts = Counter()
    status_counts = Counter()
    for entry in entries:
        action_counts.update(_string_list(entry.get("evaluation_harness_actions")))
        signal_counts.update(
            signal.get("signal_type")
            for signal in _list(entry.get("evaluation_signals"))
            if isinstance(signal, dict) and signal.get("signal_type")
        )
        status = _string_or_none(entry.get("evaluation_signal_status"))
        if status:
            status_counts[status] += 1
    summary = _report_summary(entries)
    report = {
        "report_type": LABEL_FEEDBACK_EVALUATION_REPORT_TYPE,
        "report_version": LABEL_FEEDBACK_EVALUATION_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_feedback_inputs_path": str(Path(feedback_inputs_path)),
        "source_paths": _dict(feedback_inputs.get("source_paths")),
        "source_contract_versions": _source_contract_refs(),
        "feedback_entry_count": len(entries),
        "summary": summary,
        "signal_counts": dict(sorted(signal_counts.items())),
        "signal_status_counts": dict(sorted(status_counts.items())),
        "evaluation_harness_action_counts": dict(sorted(action_counts.items())),
        "report_sections": _report_sections(summary),
        "source_warnings": _list(feedback_inputs.get("source_warnings")),
        "known_limitations": _list(feedback_inputs.get("known_limitations")),
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(LABEL_FEEDBACK_WARNINGS),
            "report_does_not_create_labels": True,
            "report_does_not_modify_evaluation_baselines": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": LABEL_FEEDBACK_EVALUATION_REPORT_TYPE,
        "report_version": LABEL_FEEDBACK_EVALUATION_REPORT_VERSION,
        "feedback_entry_count": len(entries),
        "summary": summary,
        "report": report,
        "warnings": dict(LABEL_FEEDBACK_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE,
        "contract_version": LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "feedback_inputs_type": LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        "feedback_inputs_version": LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
        "report_type": LABEL_FEEDBACK_EVALUATION_REPORT_TYPE,
        "report_version": LABEL_FEEDBACK_EVALUATION_REPORT_VERSION,
        "feedback_scope": {
            "purpose": (
                "Bridge human review structures into evaluation coverage and "
                "regression diagnostics as structural inputs."
            ),
            "read_only": True,
            "feedback_loop_infrastructure_only": True,
            "truth_creation_allowed": False,
            "automatic_review_label_creation_allowed": False,
            "automatic_confidence_score_creation_allowed": False,
            "reviewer_ranking_allowed": False,
            "reviewer_quality_scoring_allowed": False,
            "disagreement_resolution_allowed": False,
            "evaluation_pass_fail_from_human_label_allowed": False,
            "model_retraining_allowed": False,
            "media_ingestion_allowed": False,
            "sampling_execution_allowed": False,
            "event_generation_allowed": False,
            "three_d_generation_allowed": False,
        },
        "source_contract_refs": _source_contract_refs(),
        "feedback_input_schema": {
            "entities": list(FEEDBACK_INPUT_ENTITIES),
            "feedback_entry_fields": [
                {"key": field, "required": True} for field in FEEDBACK_ENTRY_FIELDS
            ],
            "allows_evaluation_signals_array": True,
            "missing_review_artifacts_are_gaps": True,
            "read_only": True,
        },
        "evaluation_bridge_schema": {
            "evaluation_signal_type_field": "evaluation_signal_type",
            "evaluation_signal_status_field": "evaluation_signal_status",
            "evaluation_harness_action_field": "evaluation_harness_action",
            "allowed_evaluation_signal_types": list(EVALUATION_SIGNAL_TYPES),
            "allowed_evaluation_signal_statuses": list(EVALUATION_SIGNAL_STATUSES),
            "allowed_evaluation_harness_actions": list(EVALUATION_HARNESS_ACTIONS),
            "actions_are_structural_routing_only": True,
            "actions_do_not_decide_candidate_validity": True,
        },
        "evaluation_signal_types": list(EVALUATION_SIGNAL_TYPES),
        "evaluation_signal_statuses": list(EVALUATION_SIGNAL_STATUSES),
        "evaluation_harness_actions": list(EVALUATION_HARNESS_ACTIONS),
        "validation_rules": {
            "structural_validation_only": True,
            "contract_shape_validated": True,
            "feedback_input_shape_validated": True,
            "allowed_signal_type_values_only": True,
            "allowed_signal_status_values_only": True,
            "allowed_evaluation_harness_action_values_only": True,
            "referenced_contract_versions_validated_when_paths_available": True,
            "missing_optional_refs_are_structural_warnings": True,
            "does_not_infer_missing_labels": True,
            "does_not_create_labels": True,
            "does_not_create_confidence_scores": True,
            "does_not_rank_reviewers": True,
            "does_not_score_reviewers": True,
            "does_not_resolve_disagreement": True,
            "does_not_create_truth": True,
            "does_not_create_training_truth": True,
            "does_not_modify_evaluation_baselines": True,
            "does_not_ingest_media": True,
            "does_not_execute_sampling": True,
            "forbidden_fields": sorted(FORBIDDEN_LABEL_FEEDBACK_FIELDS),
            "forbidden_values": sorted(FORBIDDEN_LABEL_FEEDBACK_FIELDS),
        },
        "provenance_requirements": {
            "source_paths_preserved": True,
            "source_contract_versions_preserved": True,
            "replay_urls_preserved": True,
            "associated_run_ids_preserved": True,
            "evidence_availability_preserved": True,
            "profile_counts_preserved": True,
            "source_warnings_preserved_when_available": True,
            "protected_sample_point_preserved_as_regression_context": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(LABEL_FEEDBACK_WARNINGS),
    }


def _source_contract_refs() -> dict[str, str]:
    return {
        "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "intennse_label_alignment_contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "versioned_dataset_corpus_contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "coverage_sampling_strategy_contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "many_point_ingestion_gate_contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "review_ops_metrics_contract_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
        "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_manifest_version": POINT_MANIFEST_VERSION,
    }


def _feedback_entries(
    *,
    entries: list[dict[str, Any]],
    source_paths: dict[str, Any],
    coverage_profile: dict[str, Any],
    coverage_report: dict[str, Any],
    matrix: dict[str, Any],
    review_ops_report: dict[str, Any],
) -> list[dict[str, Any]]:
    matrix_by_manifest = _matrix_points_by_manifest(matrix)
    coverage_by_entry = _coverage_candidates_by_entry(coverage_profile, coverage_report)
    review_ops_by_entry = _review_ops_metrics_by_entry(review_ops_report)
    return [
        _feedback_entry(
            entry=entry,
            source_paths=source_paths,
            matrix_point=matrix_by_manifest.get(_string_or_none(entry.get("point_manifest_id"))),
            coverage_candidate=coverage_by_entry.get(_string_or_none(entry.get("corpus_entry_id"))),
            review_ops_entry=review_ops_by_entry.get(_string_or_none(entry.get("corpus_entry_id"))),
        )
        for entry in entries
    ]


def _feedback_entry(
    *,
    entry: dict[str, Any],
    source_paths: dict[str, Any],
    matrix_point: dict[str, Any] | None,
    coverage_candidate: dict[str, Any] | None,
    review_ops_entry: dict[str, Any] | None,
) -> dict[str, Any]:
    review_refs = _list(entry.get("review_label_bundle_refs"))
    confidence_refs = _list(entry.get("reviewer_confidence_bundle_refs"))
    multi_refs = _list(entry.get("multi_reviewer_review_set_refs"))
    disagreement_refs = _list(entry.get("disagreement_report_refs"))
    intennse_refs = _list(entry.get("intennse_alignment_refs"))
    quality_refs = _quality_refs(entry)
    labels = set(_string_list(entry.get("labels")))
    regression_available = "protected_sample_point" in labels or bool(matrix_point)
    coverage_gaps = _coverage_gaps(entry=entry, coverage_candidate=coverage_candidate)
    provenance_status = _provenance_status(_string_or_none(entry.get("provenance_status")))
    provenance_gaps = _string_list(entry.get("provenance_gaps"))
    signals = _signals(
        review_refs=review_refs,
        confidence_refs=confidence_refs,
        multi_refs=multi_refs,
        disagreement_refs=disagreement_refs,
        intennse_refs=intennse_refs,
        provenance_status=provenance_status,
        provenance_gaps=provenance_gaps,
        coverage_gaps=coverage_gaps,
        regression_available=regression_available,
    )
    primary_signal = _primary_signal(signals)
    actions = _ordered_unique(
        signal["evaluation_harness_action"]
        for signal in signals
        if signal["evaluation_harness_action"] != "not_applicable"
    )
    if not actions:
        actions = ["no_action"]
    requires_human_review = _requires_human_review(
        entry=entry,
        review_refs=review_refs,
        confidence_refs=confidence_refs,
        provenance_status=provenance_status,
    )
    return {
        "feedback_entry_id": _feedback_entry_id(entry),
        "source_corpus_entry_id": _string_or_none(entry.get("corpus_entry_id")),
        "point_manifest_id": _string_or_none(entry.get("point_manifest_id")),
        "media_id": _string_or_none(entry.get("media_id")),
        "replay_url": _string_or_none(entry.get("replay_url")),
        "associated_run_ids": _dict(entry.get("associated_run_ids")),
        "review_label_bundle_refs": review_refs,
        "reviewer_confidence_bundle_refs": confidence_refs,
        "multi_reviewer_review_set_refs": multi_refs,
        "disagreement_report_refs": disagreement_refs,
        "intennse_alignment_refs": intennse_refs,
        "observation_quality_refs": quality_refs,
        "corpus_manifest_ref": {
            "path": source_paths.get("corpus_manifest_path"),
            "corpus_entry_id": _string_or_none(entry.get("corpus_entry_id")),
        },
        "coverage_sampling_ref": {
            "profile_path": source_paths.get("coverage_sampling_profile_path"),
            "report_path": source_paths.get("coverage_sampling_report_path"),
            "coverage_gaps": coverage_gaps,
        },
        "review_ops_metrics_ref": {
            "report_path": source_paths.get("review_ops_metrics_report_path"),
            "entry_metrics": review_ops_entry or {},
        },
        "point_manifest_ref": {
            "point_manifest_id": _string_or_none(entry.get("point_manifest_id")),
            "path": _string_or_none(entry.get("point_manifest_path")),
        },
        "evaluation_case_ref": {
            "structural_eval_case": bool(
                set(actions)
                & {
                    "include_as_structural_eval_case",
                    "include_as_review_coverage_case",
                    "include_as_regression_context",
                }
            ),
            "evaluation_actions": actions,
        },
        "regression_case_ref": {
            "regression_context_available": regression_available,
            "matrix_path": source_paths.get("multi_point_regression_matrix_path"),
            "matrix_point_manifest_id": _string_or_none(
                (matrix_point or {}).get("point_manifest_id")
            ),
        },
        "coverage_gap_ref": {
            "coverage_gap_count": len(coverage_gaps),
            "coverage_gaps": coverage_gaps,
        },
        "provenance_ref": {
            "provenance_status": provenance_status,
            "provenance_gaps": provenance_gaps,
        },
        "evidence_availability": _bool_dict(entry.get("evidence_availability")),
        "profile_counts": _int_dict(entry.get("profile_counts")),
        "source_warnings": _dict(entry.get("warnings")),
        "evaluation_signal_type": primary_signal["signal_type"],
        "evaluation_signal_status": (
            "requires_human_review"
            if requires_human_review
            else primary_signal["signal_status"]
        ),
        "evaluation_harness_action": primary_signal["evaluation_harness_action"],
        "evaluation_harness_actions": actions,
        "evaluation_signals": signals,
        "provenance_status": provenance_status,
        "requires_human_review": requires_human_review,
        "warnings": {
            **dict(ENTRY_WARNINGS),
            "review_artifact_missing": not bool(review_refs),
            "confidence_artifact_missing": not bool(confidence_refs),
            "provenance_gap_present": bool(provenance_gaps),
            "coverage_gap_present": bool(coverage_gaps),
        },
    }


def _signals(
    *,
    review_refs: list[Any],
    confidence_refs: list[Any],
    multi_refs: list[Any],
    disagreement_refs: list[Any],
    intennse_refs: list[Any],
    provenance_status: str,
    provenance_gaps: list[str],
    coverage_gaps: list[str],
    regression_available: bool,
) -> list[dict[str, Any]]:
    signals = [
        _signal(
            "structural_review_available" if review_refs else "structural_review_missing",
            "present" if review_refs else "missing",
            "include_as_review_coverage_case"
            if review_refs
            else "flag_missing_review_artifact",
        ),
        _signal(
            "reviewer_confidence_available"
            if confidence_refs
            else "reviewer_confidence_missing",
            "present" if confidence_refs else "missing",
            "include_as_review_coverage_case"
            if confidence_refs
            else "flag_missing_confidence_artifact",
        ),
        _signal(
            "multi_reviewer_review_available" if multi_refs else "not_assessed",
            "present" if multi_refs else "not_assessed",
            "include_as_review_coverage_case" if multi_refs else "not_applicable",
        ),
        _signal(
            "disagreement_present" if disagreement_refs else "disagreement_missing",
            "present" if disagreement_refs else "missing",
            "include_as_structural_eval_case"
            if disagreement_refs
            else "flag_missing_disagreement_artifact",
        ),
        _signal(
            "intennse_alignment_available" if intennse_refs else "intennse_alignment_missing",
            "present" if intennse_refs else "missing",
            "include_as_structural_eval_case"
            if intennse_refs
            else "flag_missing_intennse_alignment",
        ),
    ]
    if provenance_status == "provenance_missing":
        signals.append(_signal("provenance_missing", "missing", "flag_provenance_gap"))
    elif provenance_status == "provenance_partial" or provenance_gaps:
        signals.append(_signal("provenance_partial", "partial", "flag_provenance_gap"))
    if coverage_gaps:
        signals.append(
            _signal(
                "coverage_gap_present",
                "partial",
                "include_as_structural_eval_case",
            )
        )
    if regression_available:
        signals.append(
            _signal(
                "regression_protected_entry",
                "present",
                "preserve_regression_protected_sample",
            )
        )
        signals.append(
            _signal(
                "regression_protected_entry",
                "present",
                "include_as_regression_context",
            )
        )
    if not signals:
        signals.append(_signal("not_assessed", "not_assessed", "no_action"))
    return signals


def _signal(signal_type: str, status: str, action: str) -> dict[str, Any]:
    return {
        "signal_type": signal_type,
        "signal_status": status,
        "evaluation_harness_action": action,
        "structural_routing_only": True,
    }


def _primary_signal(signals: list[dict[str, str]]) -> dict[str, str]:
    priority = [
        "flag_missing_review_artifact",
        "flag_missing_confidence_artifact",
        "flag_missing_disagreement_artifact",
        "flag_missing_intennse_alignment",
        "flag_provenance_gap",
        "preserve_regression_protected_sample",
        "include_as_regression_context",
        "include_as_review_coverage_case",
        "include_as_structural_eval_case",
        "no_action",
    ]
    action_rank = {action: index for index, action in enumerate(priority)}
    return sorted(
        signals,
        key=lambda item: action_rank.get(item["evaluation_harness_action"], len(priority)),
    )[0]


def _summary_counts(entries: list[dict[str, Any]]) -> dict[str, int]:
    summary = Counter()
    summary["feedback_entry_count"] = len(entries)
    for entry in entries:
        status = _string_or_none(entry.get("evaluation_signal_status"))
        actions = set(_string_list(entry.get("evaluation_harness_actions")))
        summary["structurally_usable_entries"] += status in {
            "structurally_usable",
            "present",
        }
        summary["structurally_blocked_entries"] += status == "structurally_blocked"
        summary["requires_human_review_entries"] += (
            entry.get("requires_human_review") is True
        )
        summary["review_artifact_missing_entries"] += (
            "flag_missing_review_artifact" in actions
        )
        summary["confidence_artifact_missing_entries"] += (
            "flag_missing_confidence_artifact" in actions
        )
        summary["disagreement_artifact_missing_entries"] += (
            "flag_missing_disagreement_artifact" in actions
        )
        summary["disagreement_context_available_entries"] += (
            _has_signal(entry, "disagreement_present")
        )
        summary["intennse_alignment_missing_entries"] += (
            "flag_missing_intennse_alignment" in actions
        )
        summary["provenance_gap_entries"] += "flag_provenance_gap" in actions
        summary["coverage_gap_entries"] += _has_signal(entry, "coverage_gap_present")
        summary["regression_context_available_entries"] += (
            "include_as_regression_context" in actions
        )
        summary["protected_sample_point_entries"] += (
            "preserve_regression_protected_sample" in actions
        )
        summary["include_as_structural_eval_case_entries"] += (
            "include_as_structural_eval_case" in actions
        )
        summary["include_as_review_coverage_case_entries"] += (
            "include_as_review_coverage_case" in actions
        )
    return {key: int(value) for key, value in sorted(summary.items())}


def _report_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    summary = _summary_counts(entries)
    summary["structural_feedback_entry_count"] = summary.get("feedback_entry_count", 0)
    summary["review_artifact_missing_count"] = summary.get(
        "review_artifact_missing_entries", 0
    )
    summary["confidence_artifact_missing_count"] = summary.get(
        "confidence_artifact_missing_entries", 0
    )
    summary["intennse_alignment_missing_count"] = summary.get(
        "intennse_alignment_missing_entries", 0
    )
    summary["provenance_partial_count"] = sum(
        _dict(entry.get("provenance_ref")).get("provenance_status")
        == "provenance_partial"
        for entry in entries
    )
    return summary


def _report_sections(summary: dict[str, int]) -> list[dict[str, Any]]:
    section_specs = [
        ("structural_feedback_entry", "feedback_entry_count"),
        ("review_artifact_missing", "review_artifact_missing_count"),
        ("confidence_artifact_missing", "confidence_artifact_missing_count"),
        ("disagreement_context_available", "disagreement_context_available_entries"),
        ("intennse_alignment_missing", "intennse_alignment_missing_count"),
        ("provenance_partial", "provenance_partial_count"),
        ("regression_context_available", "regression_context_available_entries"),
        ("include_as_structural_eval_case", "include_as_structural_eval_case_entries"),
    ]
    return [
        {
            "section_id": section_id,
            "entry_count": int(summary.get(count_key, 0)),
            "status": "present" if int(summary.get(count_key, 0)) else "not_applicable",
            "structural_only": True,
            "warnings": dict(ENTRY_WARNINGS),
        }
        for section_id, count_key in section_specs
    ]


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION:
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "feedback_scope",
        "source_contract_refs",
        "feedback_input_schema",
        "evaluation_bridge_schema",
        "evaluation_signal_types",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors
    errors.extend(_source_contract_ref_errors(_dict(contract.get("source_contract_refs"))))
    if set(_string_list(contract.get("evaluation_signal_types"))) != set(
        EVALUATION_SIGNAL_TYPES
    ):
        errors.append(
            _error(
                "invalid_evaluation_signal_types",
                "evaluation_signal_types",
                contract.get("evaluation_signal_types"),
            )
        )
    bridge = _dict(contract.get("evaluation_bridge_schema"))
    if set(_string_list(bridge.get("allowed_evaluation_signal_statuses"))) != set(
        EVALUATION_SIGNAL_STATUSES
    ):
        errors.append(
            _error(
                "invalid_evaluation_signal_statuses",
                "evaluation_bridge_schema.allowed_evaluation_signal_statuses",
                bridge.get("allowed_evaluation_signal_statuses"),
            )
        )
    if set(_string_list(bridge.get("allowed_evaluation_harness_actions"))) != set(
        EVALUATION_HARNESS_ACTIONS
    ):
        errors.append(
            _error(
                "invalid_evaluation_harness_actions",
                "evaluation_bridge_schema.allowed_evaluation_harness_actions",
                bridge.get("allowed_evaluation_harness_actions"),
            )
        )
    rules = _dict(contract.get("validation_rules"))
    for rule in (
        "structural_validation_only",
        "contract_shape_validated",
        "feedback_input_shape_validated",
        "allowed_signal_type_values_only",
        "allowed_signal_status_values_only",
        "allowed_evaluation_harness_action_values_only",
        "does_not_infer_missing_labels",
        "does_not_create_labels",
        "does_not_create_confidence_scores",
        "does_not_rank_reviewers",
        "does_not_score_reviewers",
        "does_not_resolve_disagreement",
        "does_not_create_truth",
        "does_not_create_training_truth",
        "does_not_modify_evaluation_baselines",
        "does_not_ingest_media",
        "does_not_execute_sampling",
    ):
        if rules.get(rule) is not True:
            errors.append(
                _error("invalid_validation_rule", f"validation_rules.{rule}", rules.get(rule))
            )
    return errors


def _validate_feedback_inputs_shape(feedback_inputs: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(feedback_inputs, path="feedback_inputs")
    errors.extend(_forbidden_value_errors(feedback_inputs, path="feedback_inputs"))
    structural_warnings: list[dict[str, Any]] = []
    if feedback_inputs.get("feedback_inputs_type") != LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE:
        errors.append(
            _error(
                "invalid_feedback_inputs_type",
                "feedback_inputs_type",
                feedback_inputs.get("feedback_inputs_type"),
            )
        )
    if (
        feedback_inputs.get("feedback_inputs_version")
        != LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION
    ):
        errors.append(
            _error(
                "invalid_feedback_inputs_version",
                "feedback_inputs_version",
                feedback_inputs.get("feedback_inputs_version"),
            )
        )
    errors.extend(
        _source_contract_ref_errors(_dict(feedback_inputs.get("source_contract_versions")))
    )
    for field in (
        "generated_at",
        "source_paths",
        "feedback_entry_count",
        "feedback_entries",
        "summary",
        "warnings",
        "validation_summary",
    ):
        if field not in feedback_inputs:
            errors.append(_error("missing_feedback_inputs_field", field, None))
    entries = _list(feedback_inputs.get("feedback_entries"))
    if feedback_inputs.get("feedback_entry_count") != len(entries):
        errors.append(
            _error(
                "feedback_entry_count_mismatch",
                "feedback_entry_count",
                feedback_inputs.get("feedback_entry_count"),
            )
        )
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(_error("feedback_entry_must_be_object", f"entries[{index}]", entry))
            continue
        entry_result = _validate_feedback_entry(entry=entry, path=f"feedback_entries[{index}]")
        errors.extend(_list(entry_result.get("errors")))
        structural_warnings.extend(_list(entry_result.get("structural_warnings")))
    if _list(feedback_inputs.get("source_warnings")):
        structural_warnings.append(
            {
                "warning_type": "source_gap_present",
                "path": "source_warnings",
                "structural_only": True,
            }
        )
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_feedback_entry(*, entry: dict[str, Any], path: str) -> dict[str, Any]:
    errors = _forbidden_field_errors(entry, path=path)
    errors.extend(_forbidden_value_errors(entry, path=path))
    structural_warnings: list[dict[str, Any]] = []
    for field in FEEDBACK_ENTRY_FIELDS:
        if field not in entry:
            errors.append(_error("missing_feedback_entry_field", f"{path}.{field}", None))
    signal_type = _string_or_none(entry.get("evaluation_signal_type"))
    status = _string_or_none(entry.get("evaluation_signal_status"))
    action = _string_or_none(entry.get("evaluation_harness_action"))
    if signal_type not in EVALUATION_SIGNAL_TYPES:
        errors.append(_error("invalid_evaluation_signal_type", f"{path}.signal_type", signal_type))
    if status not in EVALUATION_SIGNAL_STATUSES:
        errors.append(_error("invalid_evaluation_signal_status", f"{path}.status", status))
    if action not in EVALUATION_HARNESS_ACTIONS:
        errors.append(_error("invalid_evaluation_harness_action", f"{path}.action", action))
    for index, signal in enumerate(_list(entry.get("evaluation_signals"))):
        if not isinstance(signal, dict):
            errors.append(
                _error("evaluation_signal_must_be_object", f"{path}.signals[{index}]", signal)
            )
            continue
        nested_type = _string_or_none(signal.get("signal_type"))
        nested_status = _string_or_none(signal.get("signal_status"))
        nested_action = _string_or_none(signal.get("evaluation_harness_action"))
        if nested_type not in EVALUATION_SIGNAL_TYPES:
            errors.append(
                _error(
                    "invalid_nested_signal_type",
                    f"{path}.signals[{index}].signal_type",
                    nested_type,
                )
            )
        if nested_status not in EVALUATION_SIGNAL_STATUSES:
            errors.append(
                _error(
                    "invalid_nested_signal_status",
                    f"{path}.signals[{index}].signal_status",
                    nested_status,
                )
            )
        if nested_action not in EVALUATION_HARNESS_ACTIONS:
            errors.append(
                _error(
                    "invalid_nested_signal_action",
                    f"{path}.signals[{index}].evaluation_harness_action",
                    nested_action,
                )
            )
    if entry.get("requires_human_review") is True:
        structural_warnings.append(
            {
                "warning_type": "requires_human_review",
                "path": f"{path}.requires_human_review",
                "structural_only": True,
            }
        )
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_referenced_contracts(
    *,
    observation_quality_taxonomy_path: str | Path | None,
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
    multi_reviewer_schema_path: str | Path | None,
    intennse_alignment_contract_path: str | Path | None,
    dataset_corpus_contract_path: str | Path | None,
    coverage_sampling_contract_path: str | Path | None,
    many_point_ingestion_contract_path: str | Path | None,
    review_ops_metrics_contract_path: str | Path | None,
) -> dict[str, Any]:
    specs = [
        (
            "observation_quality_taxonomy",
            observation_quality_taxonomy_path,
            "taxonomy_type",
            OBSERVATION_QUALITY_TAXONOMY_TYPE,
            "taxonomy_version",
            OBSERVATION_QUALITY_TAXONOMY_VERSION,
        ),
        (
            "review_label_schema",
            review_label_schema_path,
            "schema_type",
            REVIEW_LABEL_SCHEMA_TYPE,
            "schema_version",
            REVIEW_LABEL_SCHEMA_VERSION,
        ),
        (
            "reviewer_confidence_schema",
            reviewer_confidence_schema_path,
            "schema_type",
            REVIEWER_CONFIDENCE_SCHEMA_TYPE,
            "schema_version",
            REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        ),
        (
            "multi_reviewer_disagreement_schema",
            multi_reviewer_schema_path,
            "schema_type",
            MULTI_REVIEWER_SCHEMA_TYPE,
            "schema_version",
            MULTI_REVIEWER_SCHEMA_VERSION,
        ),
        (
            "intennse_alignment_contract",
            intennse_alignment_contract_path,
            "contract_type",
            INTENNSE_ALIGNMENT_CONTRACT_TYPE,
            "contract_version",
            INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        ),
        (
            "versioned_dataset_corpus_contract",
            dataset_corpus_contract_path,
            "contract_type",
            DATASET_CORPUS_CONTRACT_TYPE,
            "contract_version",
            DATASET_CORPUS_CONTRACT_VERSION,
        ),
        (
            "coverage_sampling_strategy_contract",
            coverage_sampling_contract_path,
            "contract_type",
            COVERAGE_SAMPLING_CONTRACT_TYPE,
            "contract_version",
            COVERAGE_SAMPLING_CONTRACT_VERSION,
        ),
        (
            "many_point_ingestion_gate_contract",
            many_point_ingestion_contract_path,
            "contract_type",
            MANY_POINT_INGESTION_CONTRACT_TYPE,
            "contract_version",
            MANY_POINT_INGESTION_CONTRACT_VERSION,
        ),
        (
            "review_ops_metrics_contract",
            review_ops_metrics_contract_path,
            "contract_type",
            REVIEW_OPS_METRICS_CONTRACT_TYPE,
            "contract_version",
            REVIEW_OPS_METRICS_CONTRACT_VERSION,
        ),
    ]
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    validations: list[dict[str, Any]] = []
    for label, path, type_field, expected_type, version_field, expected_version in specs:
        validation = _validate_contract_file(
            label=label,
            path=path,
            type_field=type_field,
            expected_type=expected_type,
            version_field=version_field,
            expected_version=expected_version,
        )
        validations.append(validation)
        if validation.get("ok") is False:
            if validation.get("missing") is True:
                structural_warnings.append(
                    {
                        "warning_type": "missing_referenced_contract",
                        "label": label,
                        "path": _path_or_none(path),
                        "structural_only": True,
                    }
                )
            else:
                errors.append(_error("invalid_referenced_contract", label, validation))
    return {
        "errors": errors,
        "structural_warnings": structural_warnings,
        "validations": validations,
    }


def _validate_contract_file(
    *,
    label: str,
    path: str | Path | None,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {"ok": False, "label": label, "path": None, "missing": True}
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return {"ok": False, "label": label, "path": str(file_path), "missing": True}
    loaded = _load_json(file_path, label=label)
    if loaded.get("ok") is False:
        return {"ok": False, "label": label, "path": str(file_path), "error": loaded}
    data = _dict(loaded.get("data"))
    return {
        "ok": data.get(type_field) == expected_type
        and data.get(version_field) == expected_version,
        "label": label,
        "path": str(file_path),
        "type_field": type_field,
        "type_value": data.get(type_field),
        "expected_type": expected_type,
        "version_field": version_field,
        "version_value": data.get(version_field),
        "expected_version": expected_version,
    }


def _source_contract_ref_errors(refs: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    expected = _source_contract_refs()
    for key, value in expected.items():
        if refs.get(key) != value:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _corpus_entries(corpus_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    entries = corpus_manifest.get("corpus_entries")
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def _matrix_points_by_manifest(matrix: dict[str, Any]) -> dict[str | None, dict[str, Any]]:
    return {
        _string_or_none(point.get("point_manifest_id")): point
        for point in _list(matrix.get("points"))
        if isinstance(point, dict)
    }


def _coverage_candidates_by_entry(
    coverage_profile: dict[str, Any],
    coverage_report: dict[str, Any],
) -> dict[str | None, dict[str, Any]]:
    candidates = _list(coverage_profile.get("sampling_candidates")) or _list(
        coverage_report.get("sampling_candidates")
    )
    return {
        _string_or_none(candidate.get("source_corpus_entry_id")): candidate
        for candidate in candidates
        if isinstance(candidate, dict)
    }


def _review_ops_metrics_by_entry(
    review_ops_report: dict[str, Any],
) -> dict[str | None, dict[str, Any]]:
    return {
        _string_or_none(metric.get("corpus_entry_id")): metric
        for metric in _list(review_ops_report.get("entry_metrics"))
        if isinstance(metric, dict)
    }


def _coverage_gaps(
    *,
    entry: dict[str, Any],
    coverage_candidate: dict[str, Any] | None,
) -> list[str]:
    gaps = _string_list((coverage_candidate or {}).get("coverage_gaps"))
    if gaps:
        return gaps
    derived: list[str] = []
    if not _list(entry.get("review_label_bundle_refs")):
        derived.append("missing_review_labels")
    if not _list(entry.get("reviewer_confidence_bundle_refs")):
        derived.append("missing_reviewer_confidence")
    if not _list(entry.get("multi_reviewer_review_set_refs")):
        derived.append("missing_multi_reviewer_review")
    if not _list(entry.get("disagreement_report_refs")):
        derived.append("missing_disagreement_report")
    if not _list(entry.get("intennse_alignment_refs")):
        derived.append("missing_intennse_alignment")
    if _string_or_none(entry.get("observation_quality_profile_path")) is None:
        derived.append("missing_observation_quality_profile")
    if _string_list(entry.get("provenance_gaps")):
        derived.append("missing_provenance")
    return derived


def _quality_refs(entry: dict[str, Any]) -> list[Any]:
    profile_path = _string_or_none(entry.get("observation_quality_profile_path"))
    return [profile_path] if profile_path else []


def _requires_human_review(
    *,
    entry: dict[str, Any],
    review_refs: list[Any],
    confidence_refs: list[Any],
    provenance_status: str,
) -> bool:
    return (
        entry.get("requires_human_review") == "required"
        or not review_refs
        or not confidence_refs
        or provenance_status in {"provenance_partial", "provenance_missing"}
    )


def _has_signal(entry: dict[str, Any], signal_type: str) -> bool:
    return any(
        signal.get("signal_type") == signal_type
        for signal in _list(entry.get("evaluation_signals"))
        if isinstance(signal, dict)
    )


def _provenance_status(status: str | None) -> str:
    if status in {"provenance_partial", "provenance_missing"}:
        return status
    return "not_applicable" if status == "not_applicable" else "not_assessed"


def _bundle_id(entries: list[dict[str, Any]]) -> str:
    seed = "|".join(
        sorted(_string_or_none(entry.get("feedback_entry_id")) or "" for entry in entries)
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
    return f"label_feedback_bundle_v1_{digest}"


def _feedback_entry_id(entry: dict[str, Any]) -> str:
    seed = "|".join(
        [
            _string_or_none(entry.get("corpus_entry_id")) or "",
            _string_or_none(entry.get("point_manifest_id")) or "",
            _string_or_none(entry.get("media_id")) or "",
        ]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
    return f"label_feedback_entry_v1_{digest}"


def _known_limitations(
    *,
    entry_count: int,
    source_warnings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    limitations = [
        {
            "limitation_type": "structural_feedback_only",
            "description": "Feedback entries route evidence and review structure only.",
            "not_generalization_claim": True,
        }
    ]
    if entry_count <= 1:
        limitations.append(
            {
                "limitation_type": "demo_or_single_point_limited",
                "description": "Current feedback bundle size does not prove many real points.",
                "not_generalization_claim": True,
            }
        )
    if source_warnings:
        limitations.append(
            {
                "limitation_type": "source_gap_present",
                "description": "At least one optional source was missing or structurally partial.",
                "not_generalization_claim": True,
            }
        )
    return limitations


def _load_optional_json(
    path: str | Path | None,
    *,
    label: str,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {"ok": True, "present": False, "data": {}, "warning": "source_not_supplied"}
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return {
            "ok": True,
            "present": False,
            "data": {},
            "warning": "source_path_missing",
            "path": str(file_path),
        }
    loaded = _load_json(file_path, label=label)
    if loaded.get("ok") is False:
        return {
            "ok": True,
            "present": False,
            "data": {},
            "warning": "source_unreadable",
            "path": str(file_path),
            "load_error": loaded,
        }
    data = _dict(loaded["data"])
    if data.get(type_field) != expected_type or data.get(version_field) != expected_version:
        return {
            "ok": True,
            "present": False,
            "data": data,
            "warning": "source_shape_mismatch",
            "path": str(file_path),
            "type_value": data.get(type_field),
            "version_value": data.get(version_field),
        }
    return {"ok": True, "present": True, "data": data, "path": str(file_path)}


def _source_statuses(sources: dict[str, dict[str, Any]]) -> dict[str, str]:
    return {
        label: "present" if source.get("present") is True else "missing"
        for label, source in sources.items()
    }


def _source_warnings(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for label, source in sources.items():
        warning = source.get("warning")
        if warning:
            warnings.append(
                {
                    "warning_type": str(warning),
                    "source_label": label,
                    "path": source.get("path"),
                    "structural_only": True,
                }
            )
    return warnings


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return _failed("source_file_not_found", f"{label} not found: {file_path}")
    try:
        return {"ok": True, "data": json.loads(file_path.read_text(encoding="utf-8"))}
    except json.JSONDecodeError as exc:
        return _failed("invalid_json", f"{label} is not valid JSON: {exc}")


def _failed(error_type: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": error_type,
        "error_type": error_type,
        "message": message,
        "warnings": dict(LABEL_FEEDBACK_WARNINGS),
    }


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            if key in FORBIDDEN_LABEL_FEEDBACK_FIELDS:
                errors.append(_error("forbidden_field", nested_path, key))
            errors.extend(_forbidden_field_errors(nested, path=nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_field_errors(nested, path=f"{path}[{index}]"))
    return errors


def _forbidden_value_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    if path.endswith(".forbidden_fields") or path.endswith(".forbidden_values"):
        return []
    errors: list[dict[str, Any]] = []
    if isinstance(value, str):
        if value in FORBIDDEN_LABEL_FEEDBACK_FIELDS:
            errors.append(_error("forbidden_value", path, value))
    elif isinstance(value, dict):
        for key, nested in value.items():
            errors.extend(_forbidden_value_errors(nested, path=f"{path}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_value_errors(nested, path=f"{path}[{index}]"))
    return errors


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "path": path,
        "value": value,
        "structural_only": True,
    }


def _path_or_none(path: str | Path | None) -> str | None:
    if path is None or not str(path).strip():
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None and str(item).strip()]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _bool_dict(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        return {}
    return {str(key): bool(item) for key, item in value.items() if isinstance(item, bool)}


def _int_dict(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): int(item)
        for key, item in value.items()
        if isinstance(item, int) and not isinstance(item, bool)
    }


def _ordered_unique(values: Any) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        text = _string_or_none(value)
        if text and text not in seen:
            seen.add(text)
            output.append(text)
    return output


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": LABEL_FEEDBACK_BLUEPRINT,
        "blueprint_name": LABEL_FEEDBACK_BLUEPRINT_NAME,
    }
