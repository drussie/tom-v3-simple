from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_explicit_human_resolution_record import (
    ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
    ALLOWED_MISSING_INPUT_STATUSES,
    ALLOWED_OPERATOR_ATTESTATION_STATUSES,
    ALLOWED_OPERATOR_IDENTITY_STATUSES,
    ALLOWED_OPERATOR_SIGNOFF_STATUSES,
    ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
    ALLOWED_REEXECUTION_READINESS_STATUSES,
    ALLOWED_RUNTIME_APPLICATION_STATUSES,
    ALLOWED_SELECTED_CANDIDATE_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT,
    FORBIDDEN_HUMAN_RESOLUTION_RECORD_TOKENS,
    _dict,
    _error,
    _list,
    _load_json,
    _load_json_if_exists,
    _missing_required,
    _now_utc,
    _path_string,
    _sha256_file,
    _stable_id,
    _unique_strings,
    _validate_blocked_runtime_state,
    _validate_human_resolution_record_shape,
    _validate_status,
    _write_json_if_requested,
)
from apps.worker.services.controlled_runtime_calibration_explicit_human_resolution_record import (
    SOURCE_CONTRACT_REFS as BP71_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_TYPE = (
    "controlled_runtime_calibration_human_resolution_completeness_gate_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUT_TYPE = (
    "controlled_runtime_calibration_human_resolution_completeness_gate_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_TYPE = (
    "controlled_runtime_calibration_human_resolution_completeness_gate"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_MISSING_INPUT_MATRIX_TYPE = (
    "controlled_runtime_calibration_human_resolution_missing_input_matrix"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_INPUT_COMPLETENESS_REPORT_TYPE = (
    "controlled_runtime_calibration_operator_input_completeness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_INPUT_COMPLETENESS_REPORT_TYPE = (
    "controlled_runtime_calibration_candidate_input_completeness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_readiness_after_human_resolution_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_BLUEPRINT = "blueprint_72"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_human_resolution_completeness_gate_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_human_resolution_completeness_gate_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_completeness_gate_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_completeness_gate_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_human_resolution_completeness_gate_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_completeness_gate.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_MISSING_INPUT_MATRIX_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_missing_input_matrix.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_INPUT_COMPLETENESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_operator_input_completeness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_INPUT_COMPLETENESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_candidate_input_completeness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_READINESS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_final_gate_rerun_readiness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_readiness_after_human_resolution_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_explicit_human_resolution_record_contract_version": "v1",
    **dict(BP71_SOURCE_CONTRACT_REFS),
}

ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES = [
    "human_resolution_completeness_gate_not_ready",
    "human_resolution_completeness_gate_ready_for_final_gate_rerun",
    "human_resolution_completeness_gate_ready_with_warnings",
    "human_resolution_completeness_gate_blocked_invalid_record",
    "human_resolution_completeness_gate_blocked_missing_record",
    "human_resolution_completeness_gate_informational_only",
    "not_applicable",
]
ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES = [
    "operator_inputs_incomplete",
    "operator_inputs_complete",
    "operator_inputs_complete_with_warnings",
    "operator_inputs_invalid",
    "operator_inputs_missing",
    "not_applicable",
]
ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES = [
    "candidate_inputs_incomplete",
    "candidate_inputs_complete",
    "candidate_inputs_complete_with_warnings",
    "candidate_inputs_invalid",
    "candidate_inputs_missing",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "provide_human_resolution_inputs",
    "provide_operator_inputs",
    "provide_selected_candidate_inputs",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_human_resolution",
    "prepare_final_gate_rerun_blueprint",
    "no_runtime_action_recommended",
    "not_applicable",
]

OPERATOR_GATE_REQUIRED_FIELDS = [
    "operator_identity_ref",
    "operator_signoff_timestamp",
    "operator_attestation_text",
    "operator_scope_acknowledgement",
]
CANDIDATE_GATE_REQUIRED_FIELDS = [
    "selected_candidate_config_ref",
    "selected_candidate_id",
    "selected_candidate_version",
    "selected_candidate_source_path",
    "selected_candidate_selection_reason",
    "candidate_selection_timestamp",
    "operator_reference_for_selection",
]
MISSING_INPUT_MATRIX_MINIMUM_FIELDS = [
    "operator_identity_ref",
    "operator_signoff_timestamp",
    "operator_attestation_text",
    "operator_scope_acknowledgement",
    "selected_candidate_config_ref",
    "selected_candidate_source_path",
    "selected_candidate_selection_reason",
    "candidate_selection_timestamp",
    "operator_reference_for_selection",
]

COMPLETENESS_GATE_INPUT_REQUIRED_FIELDS = [
    "completeness_gate_input_id",
    "completeness_gate_input_type",
    "completeness_gate_input_version",
    "generated_at",
    "source_explicit_human_resolution_record_path",
    "source_explicit_human_resolution_record_contract_path",
    "source_human_resolution_provided_packet_path",
    "source_human_resolution_input_packet_path",
    "source_explicit_selected_candidate_artifact_path",
    "source_explicit_operator_signoff_artifact_path",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_change_request_path",
    "source_bp71_human_resolution_record_id",
    "source_bp71_human_resolution_record_status",
    "source_bp71_human_resolution_provided_status",
    "source_bp71_human_resolution_completeness_status",
    "source_bp71_missing_input_status",
    "source_bp70_human_resolution_provided_packet_id",
    "source_bp69_human_resolution_packet_id",
    "source_bp68_selected_candidate_artifact_id",
    "source_bp67_signoff_artifact_id",
    "source_bp66_packet_id",
    "candidate_option_refs",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "mutation_status",
    "runtime_application_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "source_contract_refs",
    "source_artifact_refs",
    "warnings",
    "non_claims",
]
COMPLETENESS_GATE_REQUIRED_FIELDS = [
    "human_resolution_completeness_gate_id",
    "human_resolution_completeness_gate_type",
    "human_resolution_completeness_gate_version",
    "generated_at",
    "source_completeness_gate_input_path",
    "source_explicit_human_resolution_record_path",
    "source_human_resolution_provided_packet_path",
    "source_human_resolution_input_packet_path",
    "source_explicit_selected_candidate_artifact_path",
    "source_explicit_operator_signoff_artifact_path",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_change_request_path",
    "candidate_option_refs",
    "candidate_option_count",
    "human_resolution_completeness_gate_status",
    "human_resolution_record_status",
    "human_resolution_provided_status",
    "human_resolution_completeness_status",
    "missing_input_status",
    "operator_input_completeness_status",
    "candidate_input_completeness_status",
    "operator_signoff_status",
    "operator_attestation_status",
    "operator_identity_status",
    "operator_timestamp_status",
    "selected_candidate_status",
    "candidate_selection_validation_status",
    "final_gate_rerun_status",
    "final_gate_rerun_readiness_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "runtime_config_changed",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "model_asset_ref",
    "model_asset_sha256",
    "missing_input_matrix",
    "operator_input_completeness",
    "candidate_input_completeness",
    "final_gate_rerun_readiness",
    "reexecution_readiness",
    "next_action_recommendation",
    "source_contract_refs",
    "source_artifact_refs",
    "warnings",
    "non_claims",
]
MISSING_INPUT_MATRIX_REQUIRED_FIELDS = [
    "missing_input_matrix_id",
    "missing_input_matrix_type",
    "missing_input_matrix_version",
    "generated_at",
    "source_human_resolution_completeness_gate_id",
    "missing_input_status",
    "operator_input_completeness_status",
    "candidate_input_completeness_status",
    "required_input_count",
    "missing_input_count",
    "entries",
    "minimum_required_fields",
    "warnings",
    "non_claims",
]
OPERATOR_INPUT_COMPLETENESS_REQUIRED_FIELDS = [
    "operator_input_completeness_report_id",
    "operator_input_completeness_report_type",
    "operator_input_completeness_report_version",
    "generated_at",
    "source_human_resolution_completeness_gate_id",
    "operator_input_completeness_status",
    "operator_signoff_status",
    "operator_attestation_status",
    "operator_identity_status",
    "operator_timestamp_status",
    "required_inputs",
    "missing_inputs",
    "completeness_checks",
    "warnings",
    "non_claims",
]
CANDIDATE_INPUT_COMPLETENESS_REQUIRED_FIELDS = [
    "candidate_input_completeness_report_id",
    "candidate_input_completeness_report_type",
    "candidate_input_completeness_report_version",
    "generated_at",
    "source_human_resolution_completeness_gate_id",
    "candidate_input_completeness_status",
    "selected_candidate_status",
    "candidate_selection_validation_status",
    "candidate_option_count",
    "required_inputs",
    "missing_inputs",
    "completeness_checks",
    "warnings",
    "non_claims",
]
FINAL_GATE_RERUN_READINESS_REQUIRED_FIELDS = [
    "final_gate_rerun_readiness_report_id",
    "final_gate_rerun_readiness_report_type",
    "final_gate_rerun_readiness_report_version",
    "generated_at",
    "source_human_resolution_completeness_gate_id",
    "human_resolution_completeness_gate_status",
    "final_gate_rerun_status",
    "final_gate_rerun_readiness_status",
    "readiness_checks",
    "warnings",
    "non_claims",
]
REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REQUIRED_FIELDS = [
    "reexecution_readiness_after_human_resolution_report_id",
    "reexecution_readiness_after_human_resolution_report_type",
    "reexecution_readiness_after_human_resolution_report_version",
    "generated_at",
    "source_human_resolution_completeness_gate_id",
    "reexecution_readiness_status",
    "runtime_application_status",
    "runtime_config_changed",
    "mutation_status",
    "readiness_checks",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "human_resolution_completeness_gate_is_not_truth": True,
    "human_resolution_completeness_gate_is_not_accuracy_scoring": True,
    "human_resolution_completeness_gate_is_not_model_training": True,
    "human_resolution_completeness_gate_is_not_runtime_application": True,
    "completeness_gate_does_not_execute_application": True,
    "completeness_gate_does_not_rerun_final_gate": True,
    "completeness_gate_does_not_create_production_config": True,
    "completeness_gate_does_not_modify_model_weights": True,
    "completeness_gate_does_not_replace_baselines": True,
    "completeness_gate_does_not_infer_operator_signoff": True,
    "completeness_gate_does_not_infer_candidate_selection": True,
    "human_resolution_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
    "operator_signoff_must_be_explicit": True,
    "controlled_runtime_config_update_not_performed": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_resolution_required": True,
}
WARNINGS = {
    "controlled_runtime_calibration_human_resolution_completeness_gate": True,
    "human_resolution_completeness_gate_not_ready": True,
    "human_resolution_record_pending_explicit_inputs": True,
    "human_resolution_not_provided": True,
    "human_resolution_incomplete": True,
    "required_human_inputs_missing": True,
    "operator_inputs_incomplete": True,
    "candidate_inputs_incomplete": True,
    "operator_signoff_required": True,
    "operator_attestation_required": True,
    "operator_identity_required": True,
    "operator_timestamp_required": True,
    "selected_candidate_required": True,
    "candidate_selection_pending_explicit_input": True,
    "candidate_option_discovery_is_not_selection": True,
    "final_gate_rerun_required": True,
    "final_gate_rerun_not_ready_missing_human_resolution": True,
    "reexecution_not_ready_blockers_unresolved": True,
    "runtime_application_not_executed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "classifier_correctness_not_assessed": True,
    **NON_CLAIMS,
}
FORBIDDEN_HUMAN_RESOLUTION_COMPLETENESS_GATE_TOKENS = set(
    FORBIDDEN_HUMAN_RESOLUTION_RECORD_TOKENS
)


def export_controlled_runtime_calibration_human_resolution_completeness_gate_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "human_resolution_completeness_gate_scope": {
            "evaluates_bp71_explicit_human_resolution_record": True,
            "default_state_remains_not_ready_without_explicit_inputs": True,
            "candidate_option_discovery_is_inventory_only": True,
            "single_candidate_option_does_not_create_selection": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_infer_human_resolution": True,
            "does_not_write_runtime_config": True,
            "does_not_rerun_final_gate": True,
            "does_not_execute_runtime_application": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "completeness_gate_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUT_TYPE,  # noqa: E501
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUT_VERSION
            ),
            "required_fields": list(COMPLETENESS_GATE_INPUT_REQUIRED_FIELDS),
        },
        "completeness_gate_schema": {
            "gate_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_TYPE,
            "gate_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
            ),
            "required_fields": list(COMPLETENESS_GATE_REQUIRED_FIELDS),
            "allowed_human_resolution_completeness_gate_statuses": list(
                ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES
            ),
            "allowed_operator_input_completeness_statuses": list(
                ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES
            ),
            "allowed_candidate_input_completeness_statuses": list(
                ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES
            ),
            "allowed_missing_input_statuses": list(ALLOWED_MISSING_INPUT_STATUSES),
            "allowed_final_gate_rerun_readiness_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES
            ),
            "allowed_reexecution_readiness_statuses": list(ALLOWED_REEXECUTION_READINESS_STATUSES),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "missing_input_matrix_schema": {
            "matrix_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_MISSING_INPUT_MATRIX_TYPE
            ),
            "matrix_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
            ),
            "required_fields": list(MISSING_INPUT_MATRIX_REQUIRED_FIELDS),
            "minimum_required_input_fields": list(MISSING_INPUT_MATRIX_MINIMUM_FIELDS),
        },
        "operator_input_completeness_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_INPUT_COMPLETENESS_REPORT_TYPE,
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
            ),
            "required_fields": list(OPERATOR_INPUT_COMPLETENESS_REQUIRED_FIELDS),
        },
        "candidate_input_completeness_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_INPUT_COMPLETENESS_REPORT_TYPE,
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
            ),
            "required_fields": list(CANDIDATE_INPUT_COMPLETENESS_REQUIRED_FIELDS),
        },
        "final_gate_rerun_readiness_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_READINESS_REPORT_TYPE,
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
            ),
            "required_fields": list(FINAL_GATE_RERUN_READINESS_REQUIRED_FIELDS),
        },
        "reexecution_readiness_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
            ),
            "required_fields": list(REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_completeness_gate_input_shape": True,
            "validate_completeness_gate_artifact_shape": True,
            "validate_missing_input_matrix_shape": True,
            "validate_operator_input_completeness_shape": True,
            "validate_candidate_input_completeness_shape": True,
            "validate_final_gate_rerun_readiness_shape": True,
            "validate_reexecution_readiness_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_current_pending_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_gate_remains_not_ready_unless_bp71_record_complete": True,
            "validate_final_gate_rerun_readiness_remains_not_ready_unless_gate_ready": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_candidate_inventory": True,
            "validate_final_gate_rerun_not_executed": True,
            "validate_runtime_application_not_executed": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_review_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp71_explicit_human_resolution_record_path_required": True,
            "bp70_human_resolution_provided_packet_path_preserved": True,
            "bp69_human_resolution_input_packet_path_preserved": True,
            "bp68_selected_candidate_artifact_path_preserved": True,
            "bp67_signoff_artifact_path_preserved": True,
            "bp66_packet_path_preserved": True,
            "bp65_resolution_packet_path_preserved": True,
            "bp64_review_packet_path_preserved": True,
            "bp62_execution_path_preserved": True,
            "candidate_options_preserved_as_inventory": True,
            "runtime_config_hashes_preserved_when_available": True,
            "model_asset_hash_required": True,
            "non_claims_preserved": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    _write_json_if_requested(output_path, contract)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": contract["contract_type"],
        "contract_version": contract["contract_version"],
        "contract": contract,
        "contract_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_human_resolution_completeness_gate_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    source_explicit_human_resolution_record_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    source_explicit_human_resolution_record_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    record = _load_json_if_exists(source_explicit_human_resolution_record_path)
    record_exists = Path(source_explicit_human_resolution_record_path).exists()
    model_asset_ref = record.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = record.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    inputs = {
        "completeness_gate_input_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_completeness_gate_inputs_v1",
            record.get("human_resolution_record_id"),
            record.get("source_bp70_human_resolution_provided_packet_id"),
            record.get("source_bp69_human_resolution_packet_id"),
            record.get("source_bp68_selected_candidate_artifact_id"),
            record.get("source_bp67_signoff_artifact_id"),
            record.get("runtime_config_target_sha256_before"),
            record.get("runtime_config_target_sha256_after"),
            record_exists,
        ),
        "completeness_gate_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUT_TYPE
        ),
        "completeness_gate_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_explicit_human_resolution_record_path": str(
            Path(source_explicit_human_resolution_record_path)
        ),
        "source_explicit_human_resolution_record_contract_path": str(
            Path(source_explicit_human_resolution_record_contract_path)
        ),
        "source_human_resolution_provided_packet_path": record.get(
            "source_human_resolution_provided_packet_path"
        ),
        "source_human_resolution_input_packet_path": record.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": record.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": record.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": record.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": record.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": record.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": record.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": record.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": record.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": record.get("source_application_plan_path"),
        "source_human_approval_gate_path": record.get("source_human_approval_gate_path"),
        "source_change_request_path": record.get("source_change_request_path"),
        "source_bp71_human_resolution_record_id": record.get("human_resolution_record_id"),
        "source_bp71_human_resolution_record_status": record.get(
            "human_resolution_record_status"
        ),
        "source_bp71_human_resolution_provided_status": record.get(
            "human_resolution_provided_status"
        ),
        "source_bp71_human_resolution_completeness_status": record.get(
            "human_resolution_completeness_status"
        ),
        "source_bp71_missing_input_status": record.get("missing_input_status"),
        "source_bp70_human_resolution_provided_packet_id": record.get(
            "source_bp70_human_resolution_provided_packet_id"
        ),
        "source_bp69_human_resolution_packet_id": record.get(
            "source_bp69_human_resolution_packet_id"
        ),
        "source_bp68_selected_candidate_artifact_id": record.get(
            "source_bp68_selected_candidate_artifact_id"
        ),
        "source_bp67_signoff_artifact_id": record.get("source_bp67_signoff_artifact_id"),
        "source_bp66_packet_id": record.get("source_bp66_packet_id"),
        "candidate_option_refs": _list(record.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(record.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": record.get("runtime_config_target_sha256_before"),
        "runtime_config_target_sha256_after": record.get("runtime_config_target_sha256_after"),
        "runtime_config_changed": bool(record.get("runtime_config_changed")),
        "mutation_status": record.get("mutation_status") or "no_runtime_mutation_due_to_blocker",
        "runtime_application_status": record.get("runtime_application_status") or "not_executed",
        "production_config_status": record.get("production_config_status") or "not_created",
        "baseline_update_status": record.get("baseline_update_status") or "not_replaced",
        "model_update_status": record.get("model_update_status") or "not_modified",
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_explicit_human_resolution_record_path,
            source_explicit_human_resolution_record_contract_path,
            record,
        ),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_completeness_gate_inputs",
        "completeness_gate_input_id": inputs["completeness_gate_input_id"],
        **_status_snapshot_from_inputs(inputs),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "next_action_recommendation": _next_actions_from_inputs(inputs),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_human_resolution_completeness_gate_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    completeness_gate_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(completeness_gate_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_human_resolution_completeness_gate_inputs_validation"
        ),
        payload_path=completeness_gate_inputs_path,
        payload_type=inputs.get("completeness_gate_input_type"),
        payload_version=inputs.get("completeness_gate_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot_from_inputs(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_human_resolution_completeness_gate(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    completeness_gate_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(completeness_gate_inputs_path)
    record = _source_record(inputs)
    gate_id = _stable_id(
        "controlled_runtime_calibration_human_resolution_completeness_gate_v1",
        inputs.get("completeness_gate_input_id"),
        record.get("human_resolution_record_id"),
        record.get("human_resolution_record_status"),
        record.get("human_resolution_completeness_status"),
        record.get("missing_input_status"),
        record.get("runtime_config_target_sha256_before"),
        record.get("runtime_config_target_sha256_after"),
    )
    missing_input_matrix = _missing_input_matrix(gate_id, record, inputs, generated_at)
    operator_input_completeness = _operator_input_completeness(
        gate_id,
        record,
        inputs,
        generated_at,
    )
    candidate_input_completeness = _candidate_input_completeness(
        gate_id,
        record,
        inputs,
        generated_at,
    )
    final_gate_rerun_readiness = _final_gate_rerun_readiness(
        gate_id,
        record,
        inputs,
        generated_at,
    )
    reexecution_readiness = _reexecution_readiness_after_human_resolution(
        gate_id,
        record,
        inputs,
        generated_at,
    )
    gate = {
        "human_resolution_completeness_gate_id": gate_id,
        "human_resolution_completeness_gate_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_TYPE
        ),
        "human_resolution_completeness_gate_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_completeness_gate_input_path": str(Path(completeness_gate_inputs_path)),
        "source_explicit_human_resolution_record_path": inputs.get(
            "source_explicit_human_resolution_record_path"
        ),
        "source_human_resolution_provided_packet_path": inputs.get(
            "source_human_resolution_provided_packet_path"
        ),
        "source_human_resolution_input_packet_path": inputs.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": inputs.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": inputs.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": inputs.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": inputs.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": inputs.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": inputs.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": inputs.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": inputs.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": inputs.get("source_application_plan_path"),
        "source_human_approval_gate_path": inputs.get("source_human_approval_gate_path"),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "human_resolution_completeness_gate_status": _completeness_gate_status(record, inputs),
        "human_resolution_record_status": _record_status(
            record,
            "human_resolution_record_status",
            "human_resolution_record_pending_explicit_inputs",
        ),
        "human_resolution_provided_status": _record_status(
            record,
            "human_resolution_provided_status",
            "human_resolution_not_provided",
        ),
        "human_resolution_completeness_status": _record_status(
            record,
            "human_resolution_completeness_status",
            "human_resolution_incomplete",
        ),
        "missing_input_status": _record_status(
            record,
            "missing_input_status",
            "required_human_inputs_missing",
        ),
        "operator_input_completeness_status": _operator_input_completeness_status(record, inputs),
        "candidate_input_completeness_status": _candidate_input_completeness_status(
            record,
            inputs,
        ),
        "operator_signoff_status": _record_status(
            record,
            "operator_signoff_status",
            "operator_signoff_required",
        ),
        "operator_attestation_status": _record_status(
            record,
            "operator_attestation_status",
            "operator_attestation_required",
        ),
        "operator_identity_status": _record_status(
            record,
            "operator_identity_status",
            "operator_identity_required",
        ),
        "operator_timestamp_status": _record_status(
            record,
            "operator_timestamp_status",
            "operator_timestamp_required",
        ),
        "selected_candidate_status": _record_status(
            record,
            "selected_candidate_status",
            "selected_candidate_required",
        ),
        "candidate_selection_validation_status": _record_status(
            record,
            "candidate_selection_validation_status",
            "candidate_selection_pending_explicit_input",
        ),
        "final_gate_rerun_status": _record_status(
            record,
            "final_gate_rerun_status",
            "final_gate_rerun_required",
        ),
        "final_gate_rerun_readiness_status": _final_gate_rerun_readiness_status(record, inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(record, inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_changed": bool(inputs.get("runtime_config_changed")),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get("runtime_config_target_sha256_before"),
        "runtime_config_target_sha256_after": inputs.get("runtime_config_target_sha256_after"),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "missing_input_matrix": missing_input_matrix,
        "operator_input_completeness": operator_input_completeness,
        "candidate_input_completeness": candidate_input_completeness,
        "final_gate_rerun_readiness": final_gate_rerun_readiness,
        "reexecution_readiness": reexecution_readiness,
        "next_action_recommendation": _next_actions_from_gate(record, inputs),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_inputs_shape(inputs))
    errors.extend(_validate_completeness_gate_shape(gate))
    _write_json_if_requested(output_path, gate)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_completeness_gate",
        "human_resolution_completeness_gate_id": gate["human_resolution_completeness_gate_id"],
        **_status_snapshot(gate),
        "candidate_option_count": gate["candidate_option_count"],
        "next_action_recommendation": gate["next_action_recommendation"],
        "human_resolution_completeness_gate_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_human_resolution_completeness_gate(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(human_resolution_completeness_gate_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_shape(gate))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_human_resolution_completeness_gate_validation"
        ),
        payload_path=human_resolution_completeness_gate_path,
        payload_type=gate.get("human_resolution_completeness_gate_type"),
        payload_version=gate.get("human_resolution_completeness_gate_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(gate),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_human_resolution_missing_input_matrix(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_MISSING_INPUT_MATRIX_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(human_resolution_completeness_gate_path)
    matrix = {
        **_dict(gate.get("missing_input_matrix")),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_path": str(
            Path(human_resolution_completeness_gate_path)
        ),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_shape(gate))
    errors.extend(_validate_missing_input_matrix_shape(matrix))
    _write_json_if_requested(output_path, matrix)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_missing_input_matrix",
        "missing_input_matrix_id": matrix.get("missing_input_matrix_id"),
        "missing_input_status": matrix.get("missing_input_status"),
        "operator_input_completeness_status": matrix.get(
            "operator_input_completeness_status"
        ),
        "candidate_input_completeness_status": matrix.get(
            "candidate_input_completeness_status"
        ),
        "human_resolution_missing_input_matrix_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_operator_input_completeness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_INPUT_COMPLETENESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(human_resolution_completeness_gate_path)
    report = {
        **_dict(gate.get("operator_input_completeness")),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_path": str(
            Path(human_resolution_completeness_gate_path)
        ),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_shape(gate))
    errors.extend(_validate_operator_input_completeness_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_input_completeness_report",
        "operator_input_completeness_report_id": report.get(
            "operator_input_completeness_report_id"
        ),
        "operator_input_completeness_status": report.get(
            "operator_input_completeness_status"
        ),
        "operator_input_completeness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_candidate_input_completeness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_INPUT_COMPLETENESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(human_resolution_completeness_gate_path)
    report = {
        **_dict(gate.get("candidate_input_completeness")),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_path": str(
            Path(human_resolution_completeness_gate_path)
        ),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_shape(gate))
    errors.extend(_validate_candidate_input_completeness_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_candidate_input_completeness_report",
        "candidate_input_completeness_report_id": report.get(
            "candidate_input_completeness_report_id"
        ),
        "candidate_input_completeness_status": report.get(
            "candidate_input_completeness_status"
        ),
        "candidate_input_completeness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_final_gate_rerun_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(human_resolution_completeness_gate_path)
    report = {
        **_dict(gate.get("final_gate_rerun_readiness")),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_path": str(
            Path(human_resolution_completeness_gate_path)
        ),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_shape(gate))
    errors.extend(_validate_final_gate_rerun_readiness_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_final_gate_rerun_readiness_report",
        "final_gate_rerun_readiness_report_id": report.get(
            "final_gate_rerun_readiness_report_id"
        ),
        "final_gate_rerun_status": report.get("final_gate_rerun_status"),
        "final_gate_rerun_readiness_status": report.get(
            "final_gate_rerun_readiness_status"
        ),
        "final_gate_rerun_readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_reexecution_readiness_after_human_resolution_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(human_resolution_completeness_gate_path)
    report = {
        **_dict(gate.get("reexecution_readiness")),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_path": str(
            Path(human_resolution_completeness_gate_path)
        ),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_completeness_gate_shape(gate))
    errors.extend(_validate_reexecution_readiness_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_reexecution_readiness_report",
        "reexecution_readiness_after_human_resolution_report_id": report.get(
            "reexecution_readiness_after_human_resolution_report_id"
        ),
        "reexecution_readiness_status": report.get("reexecution_readiness_status"),
        "runtime_application_status": report.get("runtime_application_status"),
        "reexecution_readiness_after_human_resolution_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _source_artifact_refs(
    record_path: str | Path,
    record_contract_path: str | Path,
    record: dict[str, Any],
) -> dict[str, Any]:
    refs = {
        "explicit_human_resolution_record": _artifact_ref(record_path, record),
        "explicit_human_resolution_record_contract": _artifact_ref(
            record_contract_path,
            _load_json_if_exists(record_contract_path),
        ),
    }
    source_paths = {
        "human_resolution_provided_packet": record.get(
            "source_human_resolution_provided_packet_path"
        ),
        "human_resolution_input_packet": record.get("source_human_resolution_input_packet_path"),
        "explicit_selected_candidate_artifact": record.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "explicit_operator_signoff_artifact": record.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "operator_signoff_candidate_selection_packet": record.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "blocked_execution_resolution_packet": record.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "application_execution_review_packet": record.get(
            "source_application_execution_review_packet_path"
        ),
        "application_execution": record.get("source_application_execution_path"),
        "pre_application_final_gate": record.get("source_pre_application_final_gate_path"),
        "runtime_application_staging": record.get("source_runtime_application_staging_path"),
        "application_plan": record.get("source_application_plan_path"),
        "human_approval_gate": record.get("source_human_approval_gate_path"),
        "change_request": record.get("source_change_request_path"),
    }
    for key, path in source_paths.items():
        refs[key] = _artifact_ref(path, _load_json_if_exists(path))
    return refs


def _artifact_ref(path: str | Path | None, payload: dict[str, Any]) -> dict[str, Any]:
    if path is None:
        return {"path": None, "exists": False}
    return {
        "path": str(Path(path)),
        "exists": Path(path).exists(),
        "artifact_type": _artifact_type(payload),
        "artifact_version": _artifact_version(payload),
    }


def _artifact_type(payload: dict[str, Any]) -> Any:
    for key in [
        "human_resolution_completeness_gate_type",
        "human_resolution_record_type",
        "human_resolution_provided_packet_type",
        "human_resolution_packet_type",
        "selected_candidate_artifact_type",
        "signoff_artifact_type",
        "packet_type",
        "resolution_packet_type",
        "review_packet_type",
        "application_execution_type",
        "pre_application_final_gate_type",
        "runtime_application_staging_type",
        "application_plan_type",
        "human_approval_gate_type",
        "change_request_type",
        "contract_type",
    ]:
        if payload.get(key):
            return payload.get(key)
    return None


def _artifact_version(payload: dict[str, Any]) -> Any:
    for key in [
        "human_resolution_completeness_gate_version",
        "human_resolution_record_version",
        "human_resolution_provided_packet_version",
        "human_resolution_packet_version",
        "selected_candidate_artifact_version",
        "signoff_artifact_version",
        "packet_version",
        "resolution_packet_version",
        "review_packet_version",
        "application_execution_version",
        "pre_application_final_gate_version",
        "runtime_application_staging_version",
        "application_plan_version",
        "human_approval_gate_version",
        "change_request_version",
        "contract_version",
    ]:
        if payload.get(key):
            return payload.get(key)
    return None


def _source_record(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(inputs.get("source_explicit_human_resolution_record_path"))


def _record_exists(inputs: dict[str, Any]) -> bool:
    return bool(
        _dict(inputs.get("source_artifact_refs"))
        .get("explicit_human_resolution_record", {})
        .get("exists")
    )


def _record_is_invalid(record: dict[str, Any]) -> bool:
    return any(
        record.get(field)
        in {
            "human_resolution_record_invalid",
            "human_resolution_invalid",
            "human_resolution_invalid_inputs",
            "operator_signoff_invalid",
            "operator_attestation_invalid",
            "selected_candidate_invalid",
        }
        for field in [
            "human_resolution_record_status",
            "human_resolution_provided_status",
            "human_resolution_completeness_status",
            "operator_signoff_status",
            "operator_attestation_status",
            "selected_candidate_status",
        ]
    )


def _record_status(record: dict[str, Any], field: str, default: str) -> str:
    value = record.get(field)
    return str(value) if value else default


def _human_resolution_record_complete(record: dict[str, Any]) -> bool:
    return (
        record.get("human_resolution_record_status")
        == "human_resolution_record_created_with_complete_explicit_inputs"
        and record.get("human_resolution_provided_status") == "human_resolution_explicitly_provided"
        and record.get("human_resolution_completeness_status") == "human_resolution_complete"
        and record.get("missing_input_status") == "no_required_inputs_missing"
    )


def _operator_input_completeness_status(
    record: dict[str, Any],
    inputs: dict[str, Any],
) -> str:
    if not _record_exists(inputs):
        return "operator_inputs_missing"
    if record.get("operator_signoff_status") == "operator_signoff_invalid":
        return "operator_inputs_invalid"
    if all(_field_present(record, field) for field in OPERATOR_GATE_REQUIRED_FIELDS):
        if record.get("operator_signoff_status") == "operator_signoff_explicitly_recorded":
            return "operator_inputs_complete"
        return "operator_inputs_invalid"
    return "operator_inputs_incomplete"


def _candidate_input_completeness_status(
    record: dict[str, Any],
    inputs: dict[str, Any],
) -> str:
    if not _record_exists(inputs):
        return "candidate_inputs_missing"
    if record.get("selected_candidate_status") == "selected_candidate_invalid":
        return "candidate_inputs_invalid"
    if all(_field_present(record, field) for field in CANDIDATE_GATE_REQUIRED_FIELDS):
        if record.get("selected_candidate_status") == "selected_candidate_explicitly_recorded":
            return "candidate_inputs_complete"
        return "candidate_inputs_invalid"
    return "candidate_inputs_incomplete"


def _completeness_gate_status(record: dict[str, Any], inputs: dict[str, Any]) -> str:
    if not _record_exists(inputs):
        return "human_resolution_completeness_gate_blocked_missing_record"
    if _record_is_invalid(record):
        return "human_resolution_completeness_gate_blocked_invalid_record"
    if (
        _human_resolution_record_complete(record)
        and _operator_input_completeness_status(record, inputs) == "operator_inputs_complete"
        and _candidate_input_completeness_status(record, inputs) == "candidate_inputs_complete"
        and _final_gate_rerun_readiness_status(record, inputs)
        == "final_gate_rerun_ready_after_human_resolution"
    ):
        return "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    return "human_resolution_completeness_gate_not_ready"


def _final_gate_rerun_readiness_status(record: dict[str, Any], inputs: dict[str, Any]) -> str:
    if not _record_exists(inputs):
        return "final_gate_rerun_not_ready_missing_human_resolution"
    if _record_is_invalid(record):
        return "final_gate_rerun_blocked_invalid_human_resolution"
    if _human_resolution_record_complete(record):
        return "final_gate_rerun_ready_after_human_resolution"
    return "final_gate_rerun_not_ready_missing_human_resolution"


def _reexecution_readiness_status(record: dict[str, Any], inputs: dict[str, Any]) -> str:
    if _operator_input_completeness_status(record, inputs) in {
        "operator_inputs_missing",
        "operator_inputs_incomplete",
    }:
        return "reexecution_not_ready_blockers_unresolved"
    if _candidate_input_completeness_status(record, inputs) in {
        "candidate_inputs_missing",
        "candidate_inputs_incomplete",
    }:
        return "reexecution_not_ready_blockers_unresolved"
    if _human_resolution_record_complete(record):
        return "reexecution_blocked_final_gate_not_rerun"
    return "reexecution_not_ready_blockers_unresolved"


def _missing_input_status(record: dict[str, Any], inputs: dict[str, Any]) -> str:
    if not _record_exists(inputs):
        return "required_human_inputs_missing"
    missing_operator = any(
        item["input_group"] == "operator" for item in _missing_gate_inputs(record)
    )
    missing_candidate = any(
        item["input_group"] == "selected_candidate" for item in _missing_gate_inputs(record)
    )
    if missing_operator and missing_candidate:
        return "required_human_inputs_missing"
    if missing_operator:
        return "operator_inputs_missing"
    if missing_candidate:
        return "candidate_inputs_missing"
    return "no_required_inputs_missing"


def _field_present(record: dict[str, Any], field: str) -> bool:
    value = record.get(field)
    if isinstance(value, dict):
        return bool(_dict(value))
    return bool(value)


def _missing_gate_inputs(record: dict[str, Any]) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    for field in OPERATOR_GATE_REQUIRED_FIELDS:
        if not _field_present(record, field):
            missing.append({"input_group": "operator", "field": field, "status": "required"})
    for field in CANDIDATE_GATE_REQUIRED_FIELDS:
        if not _field_present(record, field):
            missing.append(
                {"input_group": "selected_candidate", "field": field, "status": "required"}
            )
    return missing


def _missing_input_matrix(
    gate_id: str,
    record: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    entries = []
    for group, fields in [
        ("operator", OPERATOR_GATE_REQUIRED_FIELDS),
        ("selected_candidate", CANDIDATE_GATE_REQUIRED_FIELDS),
    ]:
        for field in fields:
            entries.append(
                {
                    "input_group": group,
                    "field": field,
                    "input_present": _field_present(record, field),
                    "status": "present" if _field_present(record, field) else "required",
                }
            )
    missing = [entry for entry in entries if entry["status"] == "required"]
    return {
        "missing_input_matrix_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_missing_input_matrix_v1",
            gate_id,
        ),
        "missing_input_matrix_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_MISSING_INPUT_MATRIX_TYPE
        ),
        "missing_input_matrix_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_id": gate_id,
        "source_explicit_human_resolution_record_id": record.get("human_resolution_record_id"),
        "missing_input_status": _missing_input_status(record, inputs),
        "operator_input_completeness_status": _operator_input_completeness_status(record, inputs),
        "candidate_input_completeness_status": _candidate_input_completeness_status(
            record,
            inputs,
        ),
        "required_input_count": len(entries),
        "missing_input_count": len(missing),
        "entries": entries,
        "missing_inputs": missing,
        "minimum_required_fields": list(MISSING_INPUT_MATRIX_MINIMUM_FIELDS),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _operator_input_completeness(
    gate_id: str,
    record: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    missing = [item for item in _missing_gate_inputs(record) if item["input_group"] == "operator"]
    return {
        "operator_input_completeness_report_id": _stable_id(
            "controlled_runtime_calibration_operator_input_completeness_report_v1",
            gate_id,
        ),
        "operator_input_completeness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_INPUT_COMPLETENESS_REPORT_TYPE
        ),
        "operator_input_completeness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_id": gate_id,
        "source_explicit_human_resolution_record_id": record.get("human_resolution_record_id"),
        "operator_input_completeness_status": _operator_input_completeness_status(
            record,
            inputs,
        ),
        "operator_signoff_status": _record_status(
            record,
            "operator_signoff_status",
            "operator_signoff_required",
        ),
        "operator_attestation_status": _record_status(
            record,
            "operator_attestation_status",
            "operator_attestation_required",
        ),
        "operator_identity_status": _record_status(
            record,
            "operator_identity_status",
            "operator_identity_required",
        ),
        "operator_timestamp_status": _record_status(
            record,
            "operator_timestamp_status",
            "operator_timestamp_required",
        ),
        "required_inputs": list(OPERATOR_GATE_REQUIRED_FIELDS),
        "missing_inputs": missing,
        "completeness_checks": {
            "operator_signoff_must_be_explicit": True,
            "operator_identity_ref_present": _field_present(record, "operator_identity_ref"),
            "operator_signoff_timestamp_present": _field_present(
                record,
                "operator_signoff_timestamp",
            ),
            "operator_attestation_text_present": _field_present(
                record,
                "operator_attestation_text",
            ),
            "operator_scope_acknowledgement_present": _field_present(
                record,
                "operator_scope_acknowledgement",
            ),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_input_completeness(
    gate_id: str,
    record: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    missing = [
        item for item in _missing_gate_inputs(record) if item["input_group"] == "selected_candidate"
    ]
    return {
        "candidate_input_completeness_report_id": _stable_id(
            "controlled_runtime_calibration_candidate_input_completeness_report_v1",
            gate_id,
        ),
        "candidate_input_completeness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_INPUT_COMPLETENESS_REPORT_TYPE
        ),
        "candidate_input_completeness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_id": gate_id,
        "source_explicit_human_resolution_record_id": record.get("human_resolution_record_id"),
        "candidate_input_completeness_status": _candidate_input_completeness_status(
            record,
            inputs,
        ),
        "selected_candidate_status": _record_status(
            record,
            "selected_candidate_status",
            "selected_candidate_required",
        ),
        "candidate_selection_validation_status": _record_status(
            record,
            "candidate_selection_validation_status",
            "candidate_selection_pending_explicit_input",
        ),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "required_inputs": list(CANDIDATE_GATE_REQUIRED_FIELDS),
        "missing_inputs": missing,
        "completeness_checks": {
            "selected_candidate_must_be_explicit": True,
            "candidate_option_discovery_is_inventory_only": True,
            "single_candidate_option_does_not_create_selection": True,
            "selected_candidate_config_ref_present": _field_present(
                record,
                "selected_candidate_config_ref",
            ),
            "selected_candidate_source_path_present": _field_present(
                record,
                "selected_candidate_source_path",
            ),
            "selected_candidate_selection_reason_present": _field_present(
                record,
                "selected_candidate_selection_reason",
            ),
            "candidate_selection_timestamp_present": _field_present(
                record,
                "candidate_selection_timestamp",
            ),
            "operator_reference_for_selection_present": _field_present(
                record,
                "operator_reference_for_selection",
            ),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_rerun_readiness(
    gate_id: str,
    record: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "final_gate_rerun_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_readiness_report_v1",
            gate_id,
        ),
        "final_gate_rerun_readiness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_READINESS_REPORT_TYPE
        ),
        "final_gate_rerun_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_id": gate_id,
        "source_explicit_human_resolution_record_id": record.get("human_resolution_record_id"),
        "human_resolution_completeness_gate_status": _completeness_gate_status(record, inputs),
        "final_gate_rerun_status": _record_status(
            record,
            "final_gate_rerun_status",
            "final_gate_rerun_required",
        ),
        "final_gate_rerun_readiness_status": _final_gate_rerun_readiness_status(record, inputs),
        "readiness_checks": {
            "human_resolution_record_complete": _human_resolution_record_complete(record),
            "operator_inputs_complete": _operator_input_completeness_status(record, inputs)
            == "operator_inputs_complete",
            "candidate_inputs_complete": _candidate_input_completeness_status(record, inputs)
            == "candidate_inputs_complete",
            "completeness_gate_ready_for_final_gate_rerun": _completeness_gate_status(
                record,
                inputs,
            )
            == "human_resolution_completeness_gate_ready_for_final_gate_rerun",
            "final_gate_not_rerun_by_bp72": True,
            "runtime_application_not_executed_by_bp72": True,
            "runtime_config_unchanged": not bool(inputs.get("runtime_config_changed")),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _reexecution_readiness_after_human_resolution(
    gate_id: str,
    record: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "reexecution_readiness_after_human_resolution_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_readiness_after_human_resolution_report_v1",
            gate_id,
        ),
        "reexecution_readiness_after_human_resolution_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REPORT_TYPE
        ),
        "reexecution_readiness_after_human_resolution_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_id": gate_id,
        "source_explicit_human_resolution_record_id": record.get("human_resolution_record_id"),
        "reexecution_readiness_status": _reexecution_readiness_status(record, inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_changed": bool(inputs.get("runtime_config_changed")),
        "mutation_status": inputs.get("mutation_status"),
        "readiness_checks": {
            "human_resolution_completeness_gate_ready": _completeness_gate_status(record, inputs)
            == "human_resolution_completeness_gate_ready_for_final_gate_rerun",
            "final_gate_rerun_ready": _final_gate_rerun_readiness_status(record, inputs)
            == "final_gate_rerun_ready_after_human_resolution",
            "final_gate_rerun_not_executed_by_bp72": True,
            "runtime_application_not_executed_by_bp72": True,
            "runtime_config_unchanged": not bool(inputs.get("runtime_config_changed")),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _next_actions_from_inputs(inputs: dict[str, Any]) -> list[str]:
    return _next_actions_from_gate(_source_record(inputs), inputs)


def _next_actions_from_gate(record: dict[str, Any], inputs: dict[str, Any]) -> list[str]:
    gate_status = _completeness_gate_status(record, inputs)
    if gate_status == "human_resolution_completeness_gate_ready_for_final_gate_rerun":
        return ["rerun_final_gate_after_human_resolution", "prepare_final_gate_rerun_blueprint"]
    actions: list[str] = []
    if _operator_input_completeness_status(record, inputs) != "operator_inputs_complete":
        actions.append("provide_operator_inputs")
    if _candidate_input_completeness_status(record, inputs) != "candidate_inputs_complete":
        actions.append("provide_selected_candidate_inputs")
    if actions:
        actions.append("provide_operator_signoff_and_selected_candidate")
    else:
        actions.append("provide_human_resolution_inputs")
    actions.append("rerun_final_gate_after_human_resolution")
    return _unique_strings(actions)


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "human_resolution_completeness_gate_scope",
        "source_contract_refs",
        "completeness_gate_input_schema",
        "completeness_gate_schema",
        "missing_input_matrix_schema",
        "operator_input_completeness_schema",
        "candidate_input_completeness_schema",
        "final_gate_rerun_readiness_schema",
        "reexecution_readiness_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_completeness_gate_inputs_shape(
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, COMPLETENESS_GATE_INPUT_REQUIRED_FIELDS, "inputs")
    record = _source_record(inputs)
    if _record_exists(inputs):
        errors.extend(_validate_human_resolution_record_shape(record))
    errors.extend(_validate_blocked_runtime_state(inputs))
    errors.extend(_validate_next_actions(_next_actions_from_inputs(inputs)))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_completeness_gate_shape(gate: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(gate, COMPLETENESS_GATE_REQUIRED_FIELDS, "gate")
    for field, value, allowed in _status_fields_for_gate(gate):
        errors.extend(_validate_status(field, value, allowed))
    if (
        gate.get("human_resolution_completeness_gate_status")
        == "human_resolution_completeness_gate_ready_for_final_gate_rerun"
        and gate.get("human_resolution_completeness_status") != "human_resolution_complete"
    ):
        errors.append(
            _error(
                "completeness_gate_ready_requires_complete_human_resolution",
                "human_resolution_completeness_status",
                gate.get("human_resolution_completeness_status"),
            )
        )
    if (
        gate.get("final_gate_rerun_readiness_status")
        == "final_gate_rerun_ready_after_human_resolution"
        and gate.get("human_resolution_completeness_gate_status")
        != "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    ):
        errors.append(
            _error(
                "final_gate_readiness_requires_ready_completeness_gate",
                "final_gate_rerun_readiness_status",
                gate.get("final_gate_rerun_readiness_status"),
            )
        )
    errors.extend(_validate_blocked_runtime_state(gate))
    errors.extend(_validate_missing_input_matrix_shape(_dict(gate.get("missing_input_matrix"))))
    errors.extend(
        _validate_operator_input_completeness_shape(
            _dict(gate.get("operator_input_completeness"))
        )
    )
    errors.extend(
        _validate_candidate_input_completeness_shape(
            _dict(gate.get("candidate_input_completeness"))
        )
    )
    errors.extend(
        _validate_final_gate_rerun_readiness_shape(
            _dict(gate.get("final_gate_rerun_readiness"))
        )
    )
    errors.extend(_validate_reexecution_readiness_shape(_dict(gate.get("reexecution_readiness"))))
    errors.extend(_validate_next_actions(_list(gate.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(gate.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(gate))
    return errors


def _validate_missing_input_matrix_shape(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(matrix, MISSING_INPUT_MATRIX_REQUIRED_FIELDS, "missing_input_matrix")
    errors.extend(
        _validate_status(
            "missing_input_status",
            matrix.get("missing_input_status"),
            ALLOWED_MISSING_INPUT_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_input_completeness_status",
            matrix.get("operator_input_completeness_status"),
            ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "candidate_input_completeness_status",
            matrix.get("candidate_input_completeness_status"),
            ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
        )
    )
    return errors


def _validate_operator_input_completeness_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        OPERATOR_INPUT_COMPLETENESS_REQUIRED_FIELDS,
        "operator_input_completeness",
    )
    for field, value, allowed in [
        (
            "operator_input_completeness_status",
            report.get("operator_input_completeness_status"),
            ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "operator_signoff_status",
            report.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "operator_attestation_status",
            report.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        ),
        (
            "operator_identity_status",
            report.get("operator_identity_status"),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        ),
        (
            "operator_timestamp_status",
            report.get("operator_timestamp_status"),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        ),
    ]:
        errors.extend(_validate_status(field, value, allowed))
    return errors


def _validate_candidate_input_completeness_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        CANDIDATE_INPUT_COMPLETENESS_REQUIRED_FIELDS,
        "candidate_input_completeness",
    )
    for field, value, allowed in [
        (
            "candidate_input_completeness_status",
            report.get("candidate_input_completeness_status"),
            ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "selected_candidate_status",
            report.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "candidate_selection_validation_status",
            report.get("candidate_selection_validation_status"),
            ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
        ),
    ]:
        errors.extend(_validate_status(field, value, allowed))
    return errors


def _validate_final_gate_rerun_readiness_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        FINAL_GATE_RERUN_READINESS_REQUIRED_FIELDS,
        "final_gate_rerun_readiness",
    )
    for field, value, allowed in [
        (
            "human_resolution_completeness_gate_status",
            report.get("human_resolution_completeness_gate_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES,
        ),
        (
            "final_gate_rerun_status",
            report.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        ),
        (
            "final_gate_rerun_readiness_status",
            report.get("final_gate_rerun_readiness_status"),
            ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
        ),
    ]:
        errors.extend(_validate_status(field, value, allowed))
    return errors


def _validate_reexecution_readiness_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        REEXECUTION_READINESS_AFTER_HUMAN_RESOLUTION_REQUIRED_FIELDS,
        "reexecution_readiness",
    )
    for field, value, allowed in [
        (
            "reexecution_readiness_status",
            report.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "runtime_application_status",
            report.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]:
        errors.extend(_validate_status(field, value, allowed))
    return errors


def _status_fields_for_gate(gate: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "human_resolution_completeness_gate_status",
            gate.get("human_resolution_completeness_gate_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES,
        ),
        (
            "human_resolution_record_status",
            gate.get("human_resolution_record_status"),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        ),
        (
            "human_resolution_provided_status",
            gate.get("human_resolution_provided_status"),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        ),
        (
            "human_resolution_completeness_status",
            gate.get("human_resolution_completeness_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        ),
        ("missing_input_status", gate.get("missing_input_status"), ALLOWED_MISSING_INPUT_STATUSES),
        (
            "operator_input_completeness_status",
            gate.get("operator_input_completeness_status"),
            ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "candidate_input_completeness_status",
            gate.get("candidate_input_completeness_status"),
            ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "operator_signoff_status",
            gate.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "operator_attestation_status",
            gate.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        ),
        (
            "operator_identity_status",
            gate.get("operator_identity_status"),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        ),
        (
            "operator_timestamp_status",
            gate.get("operator_timestamp_status"),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        ),
        (
            "selected_candidate_status",
            gate.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "candidate_selection_validation_status",
            gate.get("candidate_selection_validation_status"),
            ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
        ),
        (
            "final_gate_rerun_status",
            gate.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        ),
        (
            "final_gate_rerun_readiness_status",
            gate.get("final_gate_rerun_readiness_status"),
            ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            gate.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "runtime_application_status",
            gate.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]


def _validate_next_actions(recommendations: list[str]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for index, recommendation in enumerate(recommendations):
        errors.extend(
            _validate_status(
                f"next_action_recommendation[{index}]",
                recommendation,
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS,
            )
        )
    return errors


def _validate_non_claims(non_claims: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key, expected in NON_CLAIMS.items():
        if non_claims.get(key) is not expected:
            errors.append(_error("missing_non_claim", f"non_claims.{key}", non_claims.get(key)))
    return errors


def _validate_no_forbidden_tokens(payload: Any, path: str = "$") -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_HUMAN_RESOLUTION_COMPLETENESS_GATE_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif (
        isinstance(payload, str)
        and payload in FORBIDDEN_HUMAN_RESOLUTION_COMPLETENESS_GATE_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    record = _source_record(inputs)
    return {
        "human_resolution_completeness_gate_status": _completeness_gate_status(record, inputs),
        "human_resolution_record_status": _record_status(
            record,
            "human_resolution_record_status",
            "human_resolution_record_pending_explicit_inputs",
        ),
        "human_resolution_provided_status": _record_status(
            record,
            "human_resolution_provided_status",
            "human_resolution_not_provided",
        ),
        "human_resolution_completeness_status": _record_status(
            record,
            "human_resolution_completeness_status",
            "human_resolution_incomplete",
        ),
        "missing_input_status": _missing_input_status(record, inputs),
        "operator_input_completeness_status": _operator_input_completeness_status(record, inputs),
        "candidate_input_completeness_status": _candidate_input_completeness_status(record, inputs),
        "operator_signoff_status": _record_status(
            record,
            "operator_signoff_status",
            "operator_signoff_required",
        ),
        "operator_attestation_status": _record_status(
            record,
            "operator_attestation_status",
            "operator_attestation_required",
        ),
        "operator_identity_status": _record_status(
            record,
            "operator_identity_status",
            "operator_identity_required",
        ),
        "operator_timestamp_status": _record_status(
            record,
            "operator_timestamp_status",
            "operator_timestamp_required",
        ),
        "selected_candidate_status": _record_status(
            record,
            "selected_candidate_status",
            "selected_candidate_required",
        ),
        "candidate_selection_validation_status": _record_status(
            record,
            "candidate_selection_validation_status",
            "candidate_selection_pending_explicit_input",
        ),
        "final_gate_rerun_status": _record_status(
            record,
            "final_gate_rerun_status",
            "final_gate_rerun_required",
        ),
        "final_gate_rerun_readiness_status": _final_gate_rerun_readiness_status(record, inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(record, inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_changed": inputs.get("runtime_config_changed"),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
    }


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "human_resolution_completeness_gate_status",
        "human_resolution_record_status",
        "human_resolution_provided_status",
        "human_resolution_completeness_status",
        "missing_input_status",
        "operator_input_completeness_status",
        "candidate_input_completeness_status",
        "operator_signoff_status",
        "operator_attestation_status",
        "operator_identity_status",
        "operator_timestamp_status",
        "selected_candidate_status",
        "candidate_selection_validation_status",
        "final_gate_rerun_status",
        "final_gate_rerun_readiness_status",
        "reexecution_readiness_status",
        "runtime_application_status",
        "runtime_config_changed",
        "mutation_status",
        "production_config_status",
        "baseline_update_status",
        "model_update_status",
    ]
    return {key: payload.get(key) for key in keys if key in payload}


def _validation_result(
    *,
    validation_type: str,
    payload_path: str | Path,
    payload_type: Any,
    payload_version: Any,
    contract_path: str | Path,
    validated_at: datetime,
    errors: list[dict[str, Any]],
    status_fields: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": validation_type,
        "validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "contract_path": str(Path(contract_path)),
        "error_count": len(errors),
        "errors": errors,
        **status_fields,
        "warnings": dict(WARNINGS),
    }


def _tom_provenance() -> dict[str, str]:
    return {
        "tom_version": "tom_v3",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_71",
        "scope": "controlled_runtime_calibration_human_resolution_completeness_gate",
        "runtime_boundary": "no_runtime_application_or_config_mutation",
    }
