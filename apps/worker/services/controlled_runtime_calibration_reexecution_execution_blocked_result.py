from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_execution_blocked_result import (  # noqa: E501
    ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES,
)
from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_request_packet import (  # noqa: E501
    ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
)
from apps.worker.services.controlled_runtime_calibration_human_resolution_completeness_gate import (  # noqa: E501
    ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
    ALLOWED_MISSING_INPUT_STATUSES,
    ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
    ALLOWED_OPERATOR_SIGNOFF_STATUSES,
    ALLOWED_SELECTED_CANDIDATE_STATUSES,
    _artifact_ref,
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
    _validate_status,
    _write_json_if_requested,
)
from apps.worker.services.controlled_runtime_calibration_reexecution_request_packet import (
    ALLOWED_REEXECUTION_READINESS_STATUSES,
    ALLOWED_REEXECUTION_REQUEST_STATUSES,
    ALLOWED_RUNTIME_APPLICATION_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_reexecution_request_packet import (
    SOURCE_CONTRACT_REFS as BP75_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_TYPE = (
    "controlled_runtime_calibration_reexecution_execution_blocked_result_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUT_TYPE = (
    "controlled_runtime_calibration_reexecution_execution_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_TYPE = (
    "controlled_runtime_calibration_reexecution_execution_blocked_result"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PRECHECK_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_execution_precheck_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_BLOCKED_REASON_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_blocked_reason_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_final_gate_dependency_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_NON_EXECUTION_EVIDENCE_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_non_execution_evidence_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_POST_EXECUTION_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_post_execution_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_BLUEPRINT = (
    "blueprint_76"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_reexecution_execution_blocked_result_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_reexecution_execution_blocked_result_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_execution_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_execution_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_reexecution_execution_blocked_result_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_execution_blocked_result.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PRECHECK_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_execution_precheck_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_BLOCKED_REASON_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_blocked_reason_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_final_gate_dependency_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_NON_EXECUTION_EVIDENCE_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_non_execution_evidence_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_POST_EXECUTION_READINESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_post_execution_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_EXPORTED_AT = (
    datetime(2026, 6, 22, 0, 0, tzinfo=UTC)
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_reexecution_request_packet_contract_version": "v1",
    **dict(BP75_SOURCE_CONTRACT_REFS),
}

ALLOWED_REEXECUTION_EXECUTION_STATUSES = [
    "reexecution_execution_blocked_final_gate_not_rerun",
    "reexecution_execution_blocked_missing_human_resolution",
    "reexecution_execution_blocked_missing_operator_signoff",
    "reexecution_execution_blocked_missing_selected_candidate",
    "reexecution_execution_blocked_invalid_final_gate_result",
    "reexecution_execution_blocked_request_not_ready",
    "reexecution_execution_not_attempted",
    "reexecution_execution_deferred_to_future_blueprint",
    "reexecution_execution_completed_structural_only",
    "not_applicable",
]
ALLOWED_REEXECUTION_RESULT_STATUSES = [
    "reexecution_result_not_available",
    "reexecution_result_blocked",
    "reexecution_result_deferred",
    "reexecution_result_structural_only",
    "not_applicable",
]
ALLOWED_REEXECUTION_OUTCOME_STATUSES = [
    "reexecution_not_performed",
    "reexecution_blocked",
    "reexecution_deferred",
    "reexecution_structural_only",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "provide_human_resolution_inputs",
    "provide_operator_inputs",
    "provide_selected_candidate_inputs",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_human_resolution",
    "prepare_final_gate_rerun_execution_after_human_resolution",
    "prepare_reexecution_after_final_gate_rerun",
    "prepare_post_reexecution_verification_after_runtime_execution",
    "no_runtime_action_recommended",
    "not_applicable",
]

INPUT_REQUIRED_FIELDS = [
    "reexecution_execution_input_id",
    "reexecution_execution_input_type",
    "reexecution_execution_input_version",
    "generated_at",
    "source_reexecution_request_packet_path",
    "source_final_gate_rerun_execution_blocked_result_path",
    "source_final_gate_rerun_request_packet_path",
    "source_human_resolution_completeness_gate_path",
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
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "requested_reexecution_execution_status",
    "source_contract_refs",
    "source_artifact_refs",
    "source_status_snapshot",
    "warnings",
    "non_claims",
]
RESULT_REQUIRED_FIELDS = [
    "reexecution_execution_blocked_result_id",
    "reexecution_execution_blocked_result_type",
    "reexecution_execution_blocked_result_version",
    "generated_at",
    "source_reexecution_execution_input_path",
    *INPUT_REQUIRED_FIELDS[4:22],
    "candidate_option_refs",
    "candidate_option_count",
    "reexecution_execution_status",
    "reexecution_result_status",
    "reexecution_outcome_status",
    "reexecution_request_status",
    "reexecution_readiness_status",
    "final_gate_rerun_execution_status",
    "final_gate_rerun_result_status",
    "final_gate_rerun_outcome_status",
    "final_gate_rerun_request_status",
    "human_resolution_completeness_gate_status",
    "human_resolution_record_status",
    "human_resolution_provided_status",
    "human_resolution_completeness_status",
    "missing_input_status",
    "operator_input_completeness_status",
    "candidate_input_completeness_status",
    "operator_signoff_status",
    "selected_candidate_status",
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
    "execution_precheck_report",
    "blocked_reason_report",
    "final_gate_dependency_report",
    "non_execution_evidence_report",
    "runtime_mutation_prevention_report",
    "post_execution_readiness_report",
    "next_action_recommendation",
    "source_contract_refs",
    "source_artifact_refs",
    "warnings",
    "non_claims",
]
EXECUTION_PRECHECK_REPORT_REQUIRED_FIELDS = [
    "execution_precheck_report_id",
    "execution_precheck_report_type",
    "execution_precheck_report_version",
    "generated_at",
    "source_reexecution_execution_blocked_result_id",
    "source_reexecution_request_packet_id",
    "source_reexecution_request_packet_exists",
    "reexecution_request_packet_blocked_final_gate_not_rerun",
    "bp74_final_gate_rerun_blocked_missing_human_resolution",
    "final_gate_rerun_result_not_available",
    "human_resolution_completeness_gate_not_ready",
    "explicit_human_resolution_record_pending",
    "operator_inputs_complete",
    "candidate_inputs_complete",
    "runtime_reexecution_blocked_before_command_execution",
    "runtime_application_blocked_before_any_mutation",
    "reexecution_execution_status",
    "precheck_items",
    "precheck_item_count",
    "warnings",
    "non_claims",
]
BLOCKED_REASON_REPORT_REQUIRED_FIELDS = [
    "blocked_reason_report_id",
    "blocked_reason_report_type",
    "blocked_reason_report_version",
    "generated_at",
    "source_reexecution_execution_blocked_result_id",
    "source_reexecution_request_packet_id",
    "reexecution_execution_status",
    "blocked_reason_codes",
    "blocked_reasons",
    "blocked_reason_count",
    "warnings",
    "non_claims",
]
FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS = [
    "final_gate_dependency_report_id",
    "final_gate_dependency_report_type",
    "final_gate_dependency_report_version",
    "generated_at",
    "source_reexecution_execution_blocked_result_id",
    "source_reexecution_request_packet_id",
    "source_reexecution_request_packet_path",
    "source_final_gate_rerun_execution_blocked_result_path",
    "final_gate_rerun_performed",
    "final_gate_rerun_result_available",
    "runtime_reexecution_requires_final_gate_rerun_result",
    "final_gate_dependency_status",
    "dependency_items",
    "dependency_item_count",
    "warnings",
    "non_claims",
]
NON_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS = [
    "non_execution_evidence_report_id",
    "non_execution_evidence_report_type",
    "non_execution_evidence_report_version",
    "generated_at",
    "source_reexecution_execution_blocked_result_id",
    "source_reexecution_request_packet_id",
    "reexecution_command_not_executed",
    "runtime_application_command_not_executed",
    "runtime_config_sha_unchanged",
    "model_asset_sha_unchanged",
    "protected_baselines_not_replaced",
    "production_config_not_created",
    "candidate_option_inventory_not_selection",
    "evidence_items",
    "evidence_item_count",
    "warnings",
    "non_claims",
]
RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS = [
    "runtime_mutation_prevention_report_id",
    "runtime_mutation_prevention_report_type",
    "runtime_mutation_prevention_report_version",
    "generated_at",
    "source_reexecution_execution_blocked_result_id",
    "source_reexecution_request_packet_id",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "mutation_status",
    "application_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "prevention_checks",
    "prevention_check_count",
    "warnings",
    "non_claims",
]
POST_EXECUTION_READINESS_REPORT_REQUIRED_FIELDS = [
    "post_execution_readiness_report_id",
    "post_execution_readiness_report_type",
    "post_execution_readiness_report_version",
    "generated_at",
    "source_reexecution_execution_blocked_result_id",
    "source_reexecution_request_packet_id",
    "reexecution_execution_status",
    "reexecution_result_status",
    "reexecution_outcome_status",
    "runtime_application_status",
    "post_execution_verification_status",
    "reason",
    "next_eligible_steps",
    "readiness_items",
    "readiness_item_count",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "reexecution_execution_blocked_result_is_not_truth": True,
    "reexecution_execution_blocked_result_is_not_accuracy_scoring": True,
    "reexecution_execution_blocked_result_is_not_model_training": True,
    "reexecution_execution_blocked_result_is_not_runtime_application": True,
    "reexecution_execution_blocked_result_does_not_execute_runtime_application": True,
    "reexecution_execution_blocked_result_does_not_create_production_config": True,
    "reexecution_execution_blocked_result_does_not_modify_model_weights": True,
    "reexecution_execution_blocked_result_does_not_replace_baselines": True,
    "reexecution_execution_blocked_result_does_not_infer_operator_signoff": True,
    "reexecution_execution_blocked_result_does_not_infer_candidate_selection": True,
    "reexecution_execution_blocked_result_does_not_infer_human_resolution": True,
    "reexecution_execution_blocked_result_does_not_infer_final_gate_result": True,
    "reexecution_execution_blocked_result_does_not_infer_reexecution_approval": True,
    "human_resolution_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
    "operator_signoff_must_be_explicit": True,
    "final_gate_result_must_be_explicit": True,
    "runtime_reexecution_not_performed_in_blocked_state": True,
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
    "final_gate_rerun_required_before_reexecution_execution": True,
}
WARNINGS = {
    "controlled_runtime_calibration_reexecution_execution_blocked_result": True,
    "reexecution_execution_blocked_final_gate_not_rerun": True,
    "reexecution_result_not_available": True,
    "reexecution_not_performed": True,
    "reexecution_request_blocked_final_gate_not_rerun": True,
    "reexecution_blocked_final_gate_not_rerun": True,
    "final_gate_rerun_result_not_available": True,
    "final_gate_rerun_not_performed": True,
    "runtime_application_not_executed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "candidate_option_inventory_not_selection": True,
    "post_execution_verification_not_available": True,
    "classifier_correctness_not_assessed": True,
    **NON_CLAIMS,
}
FORBIDDEN_REEXECUTION_EXECUTION_BLOCKED_RESULT_TOKENS = {
    "uncontrolled_runtime_config_update",
    "runtime_application_without_final_gate",
    "runtime_application_without_rollback_package",
    "runtime_application_without_post_apply_verification",
    "production_config_created",
    "model_updated",
    "model_weights_modified",
    "baseline_replaced",
    "auto_approved",
    "auto_rejected",
    "fake_operator_signoff",
    "inferred_operator_signoff",
    "fake_candidate_selection",
    "inferred_candidate_selection",
    "selected_candidate_inferred_from_single_option",
    "fake_human_resolution",
    "inferred_human_resolution",
    "fake_final_gate_result",
    "inferred_final_gate_result",
    "fake_reexecution_approval",
    "inferred_reexecution_approval",
    "runtime_application_success_without_final_gate_rerun",
}


def export_controlled_runtime_calibration_reexecution_execution_blocked_result_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "reexecution_execution_scope": {
            "creates_reexecution_execution_blocked_result": True,
            "bp75_reexecution_request_packet_is_authoritative_source": True,
            "final_gate_rerun_result_required_before_runtime_reexecution": True,
            "default_state_remains_blocked_without_final_gate_rerun_result": True,
            "candidate_option_discovery_is_inventory_only": True,
            "single_candidate_option_does_not_create_selection": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_infer_human_resolution": True,
            "does_not_infer_final_gate_result": True,
            "does_not_infer_reexecution_approval": True,
            "does_not_execute_final_gate_rerun": True,
            "does_not_execute_runtime_reexecution": True,
            "does_not_execute_runtime_application": True,
            "does_not_write_runtime_config": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "reexecution_execution_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUT_TYPE,
            "input_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUT_VERSION,
            "required_fields": list(INPUT_REQUIRED_FIELDS),
        },
        "reexecution_execution_blocked_result_schema": {
            "result_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_TYPE
            ),
            "result_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(RESULT_REQUIRED_FIELDS),
            "allowed_reexecution_execution_statuses": list(
                ALLOWED_REEXECUTION_EXECUTION_STATUSES
            ),
            "allowed_reexecution_result_statuses": list(ALLOWED_REEXECUTION_RESULT_STATUSES),
            "allowed_reexecution_outcome_statuses": list(ALLOWED_REEXECUTION_OUTCOME_STATUSES),
            "allowed_runtime_application_statuses": list(ALLOWED_RUNTIME_APPLICATION_STATUSES),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "execution_precheck_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PRECHECK_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(EXECUTION_PRECHECK_REPORT_REQUIRED_FIELDS),
        },
        "blocked_reason_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_BLOCKED_REASON_REPORT_TYPE,
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(BLOCKED_REASON_REPORT_REQUIRED_FIELDS),
        },
        "final_gate_dependency_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS),
        },
        "non_execution_evidence_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_NON_EXECUTION_EVIDENCE_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(NON_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS),
        },
        "runtime_mutation_prevention_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS),
        },
        "post_execution_readiness_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_POST_EXECUTION_READINESS_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(POST_EXECUTION_READINESS_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_reexecution_execution_input_shape": True,
            "validate_reexecution_execution_blocked_result_shape": True,
            "validate_execution_precheck_report_shape": True,
            "validate_blocked_reason_report_shape": True,
            "validate_final_gate_dependency_report_shape": True,
            "validate_non_execution_evidence_report_shape": True,
            "validate_runtime_mutation_prevention_report_shape": True,
            "validate_post_execution_readiness_report_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_current_blocked_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_reexecution_execution_blocked_unless_bp75_ready": True,
            "validate_runtime_application_not_executed_by_bp76": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_single_candidate_option": True,
            "validate_no_final_gate_result_is_inferred": True,
            "validate_no_reexecution_approval_is_inferred": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_request_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_auto_label_segments": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp75_reexecution_request_packet_path_required": True,
            "bp74_final_gate_rerun_execution_blocked_result_path_preserved": True,
            "bp73_final_gate_rerun_request_packet_path_preserved": True,
            "bp72_human_resolution_completeness_gate_path_preserved": True,
            "bp71_explicit_human_resolution_record_path_preserved": True,
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


def build_controlled_runtime_calibration_reexecution_execution_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    source_reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    source_reexecution_request_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(source_reexecution_request_packet_path)
    model_asset_ref = packet.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = packet.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    runtime_target_ref = _dict(packet.get("runtime_config_target_ref"))
    runtime_target_path = runtime_target_ref.get("path")
    runtime_sha_after = (
        _sha256_file(Path(runtime_target_path))
        if runtime_target_path
        else packet.get("runtime_config_target_sha256_after")
    )
    execution_status = _execution_status(packet)
    inputs = {
        "reexecution_execution_input_id": _stable_id(
            "controlled_runtime_calibration_reexecution_execution_inputs_v1",
            packet.get("reexecution_request_packet_id"),
            packet.get("reexecution_request_status"),
            packet.get("reexecution_readiness_status"),
            execution_status,
            packet.get("runtime_config_target_sha256_before"),
            runtime_sha_after,
        ),
        "reexecution_execution_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUT_TYPE
        ),
        "reexecution_execution_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_packet_path": str(
            Path(source_reexecution_request_packet_path)
        ),
        **_source_paths_from_bp75_packet(packet),
        "candidate_option_refs": _list(packet.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": runtime_target_ref,
        "runtime_config_target_sha256_before": packet.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": runtime_sha_after,
        "requested_reexecution_execution_status": execution_status,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_reexecution_request_packet_path,
            source_reexecution_request_packet_contract_path,
            packet,
        ),
        "source_status_snapshot": _status_snapshot_from_bp75_packet(packet),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_reexecution_execution_inputs",
        "reexecution_execution_input_id": inputs["reexecution_execution_input_id"],
        **_input_status_snapshot(inputs),
        "candidate_option_count": len(inputs["candidate_option_refs"]),
        "next_action_recommendation": _next_actions_from_bp75_packet(packet, execution_status),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_reexecution_execution_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(reexecution_execution_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_reexecution_execution_inputs_validation",
        payload_path=reexecution_execution_inputs_path,
        payload_type=inputs.get("reexecution_execution_input_type"),
        payload_version=inputs.get("reexecution_execution_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_input_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_reexecution_execution_blocked_result(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(reexecution_execution_inputs_path)
    packet = _source_bp75_packet(inputs)
    execution_status = _execution_status(packet)
    result_status = _result_status(execution_status)
    outcome_status = _outcome_status(execution_status)
    result_id = _stable_id(
        "controlled_runtime_calibration_reexecution_execution_blocked_result_v1",
        inputs.get("reexecution_execution_input_id"),
        packet.get("reexecution_request_packet_id"),
        execution_status,
        result_status,
        outcome_status,
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    result = {
        "reexecution_execution_blocked_result_id": result_id,
        "reexecution_execution_blocked_result_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_TYPE
        ),
        "reexecution_execution_blocked_result_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_input_path": str(Path(reexecution_execution_inputs_path)),
        "source_reexecution_request_packet_path": inputs.get(
            "source_reexecution_request_packet_path"
        ),
        **_source_paths_from_inputs(inputs),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "reexecution_execution_status": execution_status,
        "reexecution_result_status": result_status,
        "reexecution_outcome_status": outcome_status,
        **_status_snapshot_from_bp75_packet(packet),
        "runtime_application_status": "not_executed",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "execution_precheck_report": _execution_precheck_report(
            result_id,
            packet,
            execution_status,
            generated_at,
        ),
        "blocked_reason_report": _blocked_reason_report(
            result_id,
            packet,
            execution_status,
            generated_at,
        ),
        "final_gate_dependency_report": _final_gate_dependency_report(
            result_id,
            packet,
            inputs,
            generated_at,
        ),
        "non_execution_evidence_report": _non_execution_evidence_report(
            result_id,
            packet,
            inputs,
            generated_at,
        ),
        "runtime_mutation_prevention_report": _runtime_mutation_prevention_report(
            result_id,
            packet,
            inputs,
            generated_at,
        ),
        "post_execution_readiness_report": _post_execution_readiness_report(
            result_id,
            packet,
            execution_status,
            result_status,
            outcome_status,
            generated_at,
        ),
        "next_action_recommendation": _next_actions_from_bp75_packet(packet, execution_status),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    errors.extend(_validate_result_shape(result))
    _write_json_if_requested(output_path, result)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_reexecution_execution_result",
        "reexecution_execution_blocked_result_id": result_id,
        **_result_status_snapshot(result),
        "candidate_option_count": result["candidate_option_count"],
        "next_action_recommendation": result["next_action_recommendation"],
        "reexecution_execution_blocked_result_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_reexecution_execution_blocked_result(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    result = _load_json(reexecution_execution_blocked_result_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_result_shape(result))
    validation = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_reexecution_execution_blocked_result_validation"
        ),
        payload_path=reexecution_execution_blocked_result_path,
        payload_type=result.get("reexecution_execution_blocked_result_type"),
        payload_version=result.get("reexecution_execution_blocked_result_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_result_status_snapshot(result),
    )
    _write_json_if_requested(output_path, validation)
    return validation


def build_controlled_runtime_calibration_reexecution_execution_precheck_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PRECHECK_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=reexecution_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="execution_precheck_report",
        report_validator=_validate_execution_precheck_report_shape,
        output_key="reexecution_execution_precheck_report_output",
    )


def build_controlled_runtime_calibration_reexecution_blocked_reason_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_BLOCKED_REASON_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=reexecution_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="blocked_reason_report",
        report_validator=_validate_blocked_reason_report_shape,
        output_key="reexecution_blocked_reason_report_output",
    )


def build_controlled_runtime_calibration_reexecution_final_gate_dependency_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=reexecution_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="final_gate_dependency_report",
        report_validator=_validate_final_gate_dependency_report_shape,
        output_key="reexecution_final_gate_dependency_report_output",
    )


def build_controlled_runtime_calibration_reexecution_non_execution_evidence_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_NON_EXECUTION_EVIDENCE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=reexecution_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="non_execution_evidence_report",
        report_validator=_validate_non_execution_evidence_report_shape,
        output_key="reexecution_non_execution_evidence_report_output",
    )


def build_controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=reexecution_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="runtime_mutation_prevention_report",
        report_validator=_validate_runtime_mutation_prevention_report_shape,
        output_key="reexecution_runtime_mutation_prevention_report_output",
    )


def build_controlled_runtime_calibration_reexecution_post_execution_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_POST_EXECUTION_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=reexecution_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="post_execution_readiness_report",
        report_validator=_validate_post_execution_readiness_report_shape,
        output_key="reexecution_post_execution_readiness_report_output",
    )


def _export_embedded_report(
    *,
    contract_path: str | Path,
    result_path: str | Path,
    output_path: str | Path | None,
    generated_at: datetime | None,
    report_key: str,
    report_validator: Any,
    output_key: str,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    result = _load_json(result_path)
    report = {
        **_dict(result.get(report_key)),
        "exported_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_path": str(Path(result_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_result_shape(result))
    errors.extend(report_validator(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else f"invalid_{report_key}",
        "reexecution_execution_blocked_result_id": result.get(
            "reexecution_execution_blocked_result_id"
        ),
        **_result_status_snapshot(result),
        output_key: _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _source_artifact_refs(
    packet_path: str | Path,
    packet_contract_path: str | Path,
    packet: dict[str, Any],
) -> dict[str, Any]:
    refs = {
        "reexecution_request_packet": _artifact_ref(packet_path, packet),
        "reexecution_request_packet_contract": _artifact_ref(
            packet_contract_path,
            _load_json_if_exists(packet_contract_path),
        ),
    }
    refs.update(_dict(packet.get("source_artifact_refs")))
    return refs


def _source_bp75_packet(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(inputs.get("source_reexecution_request_packet_path"))


def _source_paths_from_bp75_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_final_gate_rerun_execution_blocked_result_path": packet.get(
            "source_final_gate_rerun_execution_blocked_result_path"
        ),
        "source_final_gate_rerun_request_packet_path": packet.get(
            "source_final_gate_rerun_request_packet_path"
        ),
        "source_human_resolution_completeness_gate_path": packet.get(
            "source_human_resolution_completeness_gate_path"
        ),
        "source_explicit_human_resolution_record_path": packet.get(
            "source_explicit_human_resolution_record_path"
        ),
        "source_human_resolution_provided_packet_path": packet.get(
            "source_human_resolution_provided_packet_path"
        ),
        "source_human_resolution_input_packet_path": packet.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": packet.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": packet.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": packet.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": packet.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": packet.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": packet.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": packet.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": packet.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": packet.get("source_application_plan_path"),
        "source_human_approval_gate_path": packet.get("source_human_approval_gate_path"),
        "source_change_request_path": packet.get("source_change_request_path"),
    }


def _source_paths_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        key: inputs.get(key)
        for key in INPUT_REQUIRED_FIELDS
        if key.startswith("source_")
        and key.endswith("_path")
        and key != "source_reexecution_request_packet_path"
    }


def _final_gate_rerun_performed(packet: dict[str, Any]) -> bool:
    return (
        packet.get("final_gate_rerun_execution_status")
        == "final_gate_rerun_execution_completed_structural_only"
        and packet.get("final_gate_rerun_result_status")
        == "final_gate_rerun_result_structural_only"
        and packet.get("final_gate_rerun_outcome_status") == "final_gate_rerun_structural_only"
    )


def _source_request_ready(packet: dict[str, Any]) -> bool:
    return (
        packet.get("reexecution_request_status")
        == "reexecution_request_ready_after_final_gate_rerun"
        and packet.get("reexecution_readiness_status")
        == "reexecution_ready_after_final_gate_rerun"
        and _final_gate_rerun_performed(packet)
    )


def _execution_status(packet: dict[str, Any]) -> str:
    if _source_request_ready(packet):
        return "reexecution_execution_deferred_to_future_blueprint"
    if (
        not _final_gate_rerun_performed(packet)
        or packet.get("reexecution_request_status")
        == "reexecution_request_blocked_final_gate_not_rerun"
    ):
        return "reexecution_execution_blocked_final_gate_not_rerun"
    if packet.get("reexecution_request_status") == (
        "reexecution_request_blocked_invalid_final_gate_result"
    ):
        return "reexecution_execution_blocked_invalid_final_gate_result"
    if packet.get("human_resolution_completeness_status") != "human_resolution_complete":
        return "reexecution_execution_blocked_missing_human_resolution"
    if packet.get("operator_input_completeness_status") != "operator_inputs_complete":
        return "reexecution_execution_blocked_missing_operator_signoff"
    if packet.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        return "reexecution_execution_blocked_missing_selected_candidate"
    return "reexecution_execution_blocked_request_not_ready"


def _result_status(execution_status: str) -> str:
    if execution_status == "reexecution_execution_deferred_to_future_blueprint":
        return "reexecution_result_deferred"
    if execution_status == "reexecution_execution_completed_structural_only":
        return "reexecution_result_structural_only"
    return "reexecution_result_not_available"


def _outcome_status(execution_status: str) -> str:
    if execution_status == "reexecution_execution_deferred_to_future_blueprint":
        return "reexecution_deferred"
    if execution_status == "reexecution_execution_completed_structural_only":
        return "reexecution_structural_only"
    return "reexecution_not_performed"


def _status_snapshot_from_bp75_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "reexecution_request_status": packet.get("reexecution_request_status"),
        "reexecution_readiness_status": packet.get("reexecution_readiness_status"),
        "final_gate_rerun_execution_status": packet.get(
            "final_gate_rerun_execution_status"
        ),
        "final_gate_rerun_result_status": packet.get("final_gate_rerun_result_status"),
        "final_gate_rerun_outcome_status": packet.get("final_gate_rerun_outcome_status"),
        "final_gate_rerun_request_status": packet.get("final_gate_rerun_request_status"),
        "human_resolution_completeness_gate_status": packet.get(
            "human_resolution_completeness_gate_status"
        ),
        "human_resolution_record_status": packet.get("human_resolution_record_status"),
        "human_resolution_provided_status": packet.get(
            "human_resolution_provided_status"
        ),
        "human_resolution_completeness_status": packet.get(
            "human_resolution_completeness_status"
        ),
        "missing_input_status": packet.get("missing_input_status"),
        "operator_input_completeness_status": packet.get(
            "operator_input_completeness_status"
        ),
        "candidate_input_completeness_status": packet.get(
            "candidate_input_completeness_status"
        ),
        "operator_signoff_status": packet.get("operator_signoff_status"),
        "selected_candidate_status": packet.get("selected_candidate_status"),
    }


def _input_status_snapshot(inputs: dict[str, Any]) -> dict[str, Any]:
    packet = _source_bp75_packet(inputs)
    execution_status = _execution_status(packet)
    return {
        "reexecution_execution_status": execution_status,
        "reexecution_result_status": _result_status(execution_status),
        "reexecution_outcome_status": _outcome_status(execution_status),
        **_status_snapshot_from_bp75_packet(packet),
        "runtime_application_status": "not_executed",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
    }


def _execution_precheck_report(
    result_id: str,
    packet: dict[str, Any],
    execution_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    items = [
        _item("bp75_reexecution_request_packet_exists", bool(packet), True),
        _item(
            "bp75_reexecution_request_blocked_final_gate_not_rerun",
            packet.get("reexecution_request_status")
            == "reexecution_request_blocked_final_gate_not_rerun",
            packet.get("reexecution_request_status"),
        ),
        _item(
            "bp74_final_gate_rerun_blocked_missing_human_resolution",
            packet.get("final_gate_rerun_execution_status")
            == "final_gate_rerun_execution_blocked_missing_human_resolution",
            packet.get("final_gate_rerun_execution_status"),
        ),
        _item(
            "final_gate_rerun_result_not_available",
            packet.get("final_gate_rerun_result_status")
            == "final_gate_rerun_result_not_available",
            packet.get("final_gate_rerun_result_status"),
        ),
        _item(
            "bp72_human_resolution_gate_not_ready",
            packet.get("human_resolution_completeness_gate_status")
            == "human_resolution_completeness_gate_not_ready",
            packet.get("human_resolution_completeness_gate_status"),
        ),
        _item(
            "bp71_explicit_human_resolution_record_pending",
            packet.get("human_resolution_record_status")
            == "human_resolution_record_pending_explicit_inputs",
            packet.get("human_resolution_record_status"),
        ),
        _item(
            "operator_inputs_incomplete",
            packet.get("operator_input_completeness_status") != "operator_inputs_complete",
            packet.get("operator_input_completeness_status"),
        ),
        _item(
            "candidate_inputs_incomplete",
            packet.get("candidate_input_completeness_status") != "candidate_inputs_complete",
            packet.get("candidate_input_completeness_status"),
        ),
        _item("runtime_reexecution_blocked_before_command_execution", True, execution_status),
        _item("runtime_application_blocked_before_any_mutation", True, "not_executed"),
    ]
    return {
        "execution_precheck_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_execution_precheck_report_v1",
            result_id,
            execution_status,
            len(items),
        ),
        "execution_precheck_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PRECHECK_REPORT_TYPE
        ),
        "execution_precheck_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_id": result_id,
        "source_reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        "source_reexecution_request_packet_exists": bool(packet),
        "reexecution_request_packet_blocked_final_gate_not_rerun": (
            packet.get("reexecution_request_status")
            == "reexecution_request_blocked_final_gate_not_rerun"
        ),
        "bp74_final_gate_rerun_blocked_missing_human_resolution": (
            packet.get("final_gate_rerun_execution_status")
            == "final_gate_rerun_execution_blocked_missing_human_resolution"
        ),
        "final_gate_rerun_result_not_available": (
            packet.get("final_gate_rerun_result_status")
            == "final_gate_rerun_result_not_available"
        ),
        "human_resolution_completeness_gate_not_ready": (
            packet.get("human_resolution_completeness_gate_status")
            == "human_resolution_completeness_gate_not_ready"
        ),
        "explicit_human_resolution_record_pending": (
            packet.get("human_resolution_record_status")
            == "human_resolution_record_pending_explicit_inputs"
        ),
        "operator_inputs_complete": (
            packet.get("operator_input_completeness_status") == "operator_inputs_complete"
        ),
        "candidate_inputs_complete": (
            packet.get("candidate_input_completeness_status") == "candidate_inputs_complete"
        ),
        "runtime_reexecution_blocked_before_command_execution": True,
        "runtime_application_blocked_before_any_mutation": True,
        "reexecution_execution_status": execution_status,
        "precheck_items": items,
        "precheck_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocked_reason_report(
    result_id: str,
    packet: dict[str, Any],
    execution_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    codes = _blocked_reason_codes(packet, execution_status)
    return {
        "blocked_reason_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_blocked_reason_report_v1",
            result_id,
            execution_status,
            *codes,
        ),
        "blocked_reason_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_BLOCKED_REASON_REPORT_TYPE
        ),
        "blocked_reason_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_id": result_id,
        "source_reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        "reexecution_execution_status": execution_status,
        "blocked_reason_codes": codes,
        "blocked_reasons": [
            {
                "blocked_reason_code": code,
                "status": "required",
                "source": _blocked_reason_source(code, packet),
            }
            for code in codes
        ],
        "blocked_reason_count": len(codes),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocked_reason_codes(packet: dict[str, Any], execution_status: str) -> list[str]:
    codes = []
    if not _final_gate_rerun_performed(packet):
        codes.extend(
            [
                "final_gate_rerun_not_performed",
                "final_gate_rerun_result_not_available",
            ]
        )
    if packet.get("reexecution_request_status") == (
        "reexecution_request_blocked_final_gate_not_rerun"
    ):
        codes.append("reexecution_request_blocked_final_gate_not_rerun")
    if packet.get("human_resolution_completeness_gate_status") != (
        "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    ):
        codes.append("human_resolution_completeness_gate_not_ready")
    if packet.get("operator_input_completeness_status") != "operator_inputs_complete":
        codes.extend(
            [
                "missing_operator_identity",
                "missing_operator_attestation",
                "missing_operator_timestamp",
            ]
        )
    if packet.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        codes.extend(
            [
                "missing_selected_candidate_ref",
                "missing_selected_candidate_source_path",
                "missing_selected_candidate_selection_reason",
                "missing_candidate_selection_timestamp",
                "missing_operator_reference_for_selection",
            ]
        )
    if execution_status != "reexecution_execution_completed_structural_only":
        codes.append("runtime_application_blocked_before_mutation")
    return _unique_strings(codes)


def _blocked_reason_source(code: str, packet: dict[str, Any]) -> str | None:
    if code.startswith("missing_operator"):
        return packet.get("source_explicit_operator_signoff_artifact_path")
    if code.startswith("missing_selected") or code.startswith("missing_candidate"):
        return packet.get("source_explicit_selected_candidate_artifact_path")
    if code == "human_resolution_completeness_gate_not_ready":
        return packet.get("source_human_resolution_completeness_gate_path")
    if code.startswith("reexecution_request"):
        return packet.get("source_reexecution_request_input_path")
    if code.startswith("final_gate_rerun"):
        return packet.get("source_final_gate_rerun_execution_blocked_result_path")
    return packet.get("source_application_execution_path")


def _final_gate_dependency_report(
    result_id: str,
    packet: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    final_gate_performed = _final_gate_rerun_performed(packet)
    result_available = (
        packet.get("final_gate_rerun_result_status") != "final_gate_rerun_result_not_available"
    )
    items = [
        _dependency(
            "source_bp75_reexecution_request_packet",
            bool(inputs.get("source_reexecution_request_packet_path")),
            inputs.get("source_reexecution_request_packet_path"),
        ),
        _dependency(
            "source_bp74_blocked_final_gate_rerun_result",
            bool(inputs.get("source_final_gate_rerun_execution_blocked_result_path")),
            inputs.get("source_final_gate_rerun_execution_blocked_result_path"),
        ),
        _dependency(
            "bp74_final_gate_rerun_not_performed",
            not final_gate_performed,
            packet.get("final_gate_rerun_outcome_status"),
        ),
        _dependency(
            "no_final_gate_result_available",
            not result_available,
            packet.get("final_gate_rerun_result_status"),
        ),
        _dependency(
            "runtime_reexecution_cannot_execute_without_final_gate_rerun_result",
            not final_gate_performed or not result_available,
            packet.get("reexecution_readiness_status"),
        ),
    ]
    return {
        "final_gate_dependency_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_final_gate_dependency_report_v1",
            result_id,
            final_gate_performed,
            result_available,
        ),
        "final_gate_dependency_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_TYPE
        ),
        "final_gate_dependency_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_id": result_id,
        "source_reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        "source_reexecution_request_packet_path": inputs.get(
            "source_reexecution_request_packet_path"
        ),
        "source_final_gate_rerun_execution_blocked_result_path": inputs.get(
            "source_final_gate_rerun_execution_blocked_result_path"
        ),
        "final_gate_rerun_performed": final_gate_performed,
        "final_gate_rerun_result_available": result_available,
        "runtime_reexecution_requires_final_gate_rerun_result": True,
        "final_gate_dependency_status": (
            "final_gate_dependency_satisfied"
            if final_gate_performed and result_available
            else "final_gate_dependency_unresolved"
        ),
        "dependency_items": items,
        "dependency_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _non_execution_evidence_report(
    result_id: str,
    packet: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    runtime_sha_unchanged = (
        inputs.get("runtime_config_target_sha256_before")
        == inputs.get("runtime_config_target_sha256_after")
    )
    items = [
        _item("reexecution_command_not_executed", True, "not_executed"),
        _item("runtime_application_command_not_executed", True, "not_executed"),
        _item(
            "runtime_config_sha_unchanged",
            runtime_sha_unchanged,
            inputs.get("runtime_config_target_sha256_after"),
        ),
        _item("model_asset_sha_unchanged", True, inputs.get("model_asset_sha256")),
        _item("protected_baselines_not_replaced", True, "not_replaced"),
        _item("production_config_not_created", True, "not_created"),
        _item(
            "candidate_option_inventory_not_selection",
            True,
            len(_list(packet.get("candidate_option_refs"))),
        ),
    ]
    return {
        "non_execution_evidence_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_non_execution_evidence_report_v1",
            result_id,
            runtime_sha_unchanged,
            inputs.get("model_asset_sha256"),
        ),
        "non_execution_evidence_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_NON_EXECUTION_EVIDENCE_REPORT_TYPE
        ),
        "non_execution_evidence_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_id": result_id,
        "source_reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        "reexecution_command_not_executed": True,
        "runtime_application_command_not_executed": True,
        "runtime_config_sha_unchanged": runtime_sha_unchanged,
        "model_asset_sha_unchanged": True,
        "protected_baselines_not_replaced": True,
        "production_config_not_created": True,
        "candidate_option_inventory_not_selection": True,
        "evidence_items": items,
        "evidence_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _runtime_mutation_prevention_report(
    result_id: str,
    packet: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    checks = [
        _check(
            "runtime_config_sha_unchanged",
            inputs.get("runtime_config_target_sha256_before")
            == inputs.get("runtime_config_target_sha256_after"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        _check("runtime_config_changed_false", True, False),
        _check("mutation_status_blocked", True, "no_runtime_mutation_due_to_blocker"),
        _check("runtime_application_not_executed", True, "not_executed"),
        _check("production_config_not_created", True, "not_created"),
        _check("model_weights_not_modified", True, "not_modified"),
        _check("baselines_not_replaced", True, "not_replaced"),
    ]
    return {
        "runtime_mutation_prevention_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report_v1",
            result_id,
            inputs.get("runtime_config_target_sha256_before"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        "runtime_mutation_prevention_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE
        ),
        "runtime_mutation_prevention_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_id": result_id,
        "source_reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "application_status": "not_executed",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "prevention_checks": checks,
        "prevention_check_count": len(checks),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _post_execution_readiness_report(
    result_id: str,
    packet: dict[str, Any],
    execution_status: str,
    result_status: str,
    outcome_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    final_gate_ready = _final_gate_rerun_performed(packet)
    runtime_executed = execution_status == "reexecution_execution_completed_structural_only"
    items = [
        _item(
            "final_gate_rerun_result_available_before_runtime_reexecution",
            final_gate_ready,
            packet.get("final_gate_rerun_result_status"),
        ),
        _item("runtime_reexecution_performed", runtime_executed, execution_status),
        _item("post_execution_verification_available", False, "not_available"),
    ]
    return {
        "post_execution_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_post_execution_readiness_report_v1",
            result_id,
            execution_status,
            result_status,
            outcome_status,
        ),
        "post_execution_readiness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_POST_EXECUTION_READINESS_REPORT_TYPE
        ),
        "post_execution_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_id": result_id,
        "source_reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        "reexecution_execution_status": execution_status,
        "reexecution_result_status": result_status,
        "reexecution_outcome_status": outcome_status,
        "runtime_application_status": "not_executed",
        "post_execution_verification_status": "post_execution_verification_not_available",
        "reason": "runtime_reexecution_not_performed",
        "next_eligible_steps": _post_execution_next_steps(packet, runtime_executed),
        "readiness_items": items,
        "readiness_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _post_execution_next_steps(packet: dict[str, Any], runtime_executed: bool) -> list[str]:
    if runtime_executed:
        return ["prepare_post_reexecution_verification_after_runtime_execution"]
    if _final_gate_rerun_performed(packet):
        return ["prepare_reexecution_after_final_gate_rerun"]
    return ["rerun_final_gate_after_human_resolution"]


def _item(item_code: str, satisfied: bool, observed_value: Any) -> dict[str, Any]:
    return {
        "item_code": item_code,
        "satisfied": bool(satisfied),
        "observed_value": observed_value,
    }


def _dependency(dependency_code: str, present: bool, observed_value: Any) -> dict[str, Any]:
    return {
        "dependency_code": dependency_code,
        "present": bool(present),
        "observed_value": observed_value,
    }


def _check(check_code: str, satisfied: bool, observed_value: Any) -> dict[str, Any]:
    return {
        "check_code": check_code,
        "satisfied": bool(satisfied),
        "observed_value": observed_value,
    }


def _next_actions_from_bp75_packet(
    packet: dict[str, Any],
    execution_status: str,
) -> list[str]:
    actions: list[str] = []
    if packet.get("human_resolution_completeness_status") != "human_resolution_complete":
        actions.append("provide_human_resolution_inputs")
    if packet.get("operator_input_completeness_status") != "operator_inputs_complete":
        actions.append("provide_operator_inputs")
    if packet.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        actions.append("provide_selected_candidate_inputs")
    if (
        "provide_operator_inputs" in actions
        or "provide_selected_candidate_inputs" in actions
    ):
        actions.append("provide_operator_signoff_and_selected_candidate")
    if not _final_gate_rerun_performed(packet):
        actions.append("rerun_final_gate_after_human_resolution")
    if _final_gate_rerun_performed(packet):
        actions.append("prepare_reexecution_after_final_gate_rerun")
    if execution_status == "reexecution_execution_completed_structural_only":
        actions.append("prepare_post_reexecution_verification_after_runtime_execution")
    return _unique_strings(actions) or ["no_runtime_action_recommended"]


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "reexecution_execution_scope",
        "source_contract_refs",
        "reexecution_execution_input_schema",
        "reexecution_execution_blocked_result_schema",
        "execution_precheck_report_schema",
        "blocked_reason_report_schema",
        "final_gate_dependency_report_schema",
        "non_execution_evidence_report_schema",
        "runtime_mutation_prevention_report_schema",
        "post_execution_readiness_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, INPUT_REQUIRED_FIELDS, "inputs")
    packet = _source_bp75_packet(inputs)
    errors.extend(_validate_source_bp75_packet_shape(packet))
    errors.extend(_validate_no_runtime_mutation_fields(inputs))
    expected_execution = _execution_status(packet)
    if inputs.get("requested_reexecution_execution_status") != expected_execution:
        errors.append(
            _error(
                "requested_reexecution_execution_status_must_match_bp75_state",
                "requested_reexecution_execution_status",
                inputs.get("requested_reexecution_execution_status"),
            )
        )
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_source_bp75_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        packet,
        [
            "reexecution_request_packet_id",
            "reexecution_request_status",
            "reexecution_readiness_status",
            "final_gate_rerun_execution_status",
            "final_gate_rerun_result_status",
            "final_gate_rerun_outcome_status",
            "final_gate_rerun_request_status",
            "human_resolution_completeness_gate_status",
            "human_resolution_record_status",
            "human_resolution_provided_status",
            "human_resolution_completeness_status",
            "missing_input_status",
            "operator_input_completeness_status",
            "candidate_input_completeness_status",
            "operator_signoff_status",
            "selected_candidate_status",
            "runtime_application_status",
            "runtime_config_changed",
            "mutation_status",
            "production_config_status",
            "baseline_update_status",
            "model_update_status",
        ],
        "source_reexecution_request_packet",
    )
    for field, value, allowed in _status_fields_for_bp75_packet(packet):
        errors.extend(_validate_status(field, value, allowed))
    errors.extend(_validate_no_runtime_mutation_fields(packet))
    return errors


def _validate_no_runtime_mutation_fields(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_payload = {
        "runtime_config_changed": payload.get("runtime_config_changed", False),
        "mutation_status": payload.get("mutation_status", "no_runtime_mutation_due_to_blocker"),
        "runtime_application_status": payload.get("runtime_application_status", "not_executed"),
        "model_update_status": payload.get("model_update_status", "not_modified"),
        "production_config_status": payload.get("production_config_status", "not_created"),
        "baseline_update_status": payload.get("baseline_update_status", "not_replaced"),
        "runtime_config_target_sha256_before": payload.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": payload.get("runtime_config_target_sha256_after"),
    }
    return _validate_blocked_runtime_state(runtime_payload)


def _validate_result_shape(result: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(result, RESULT_REQUIRED_FIELDS, "result")
    for field, value, allowed in _status_fields_for_result(result):
        errors.extend(_validate_status(field, value, allowed))
    packet = _load_json_if_exists(result.get("source_reexecution_request_packet_path"))
    expected_execution = _execution_status(packet)
    if result.get("reexecution_execution_status") != expected_execution:
        errors.append(
            _error(
                "reexecution_execution_status_must_match_bp75_state",
                "reexecution_execution_status",
                result.get("reexecution_execution_status"),
            )
        )
    if result.get("reexecution_result_status") != _result_status(expected_execution):
        errors.append(
            _error(
                "reexecution_result_status_must_match_execution_status",
                "reexecution_result_status",
                result.get("reexecution_result_status"),
            )
        )
    if result.get("reexecution_outcome_status") != _outcome_status(expected_execution):
        errors.append(
            _error(
                "reexecution_outcome_status_must_match_execution_status",
                "reexecution_outcome_status",
                result.get("reexecution_outcome_status"),
            )
        )
    if result.get("runtime_application_status") != "not_executed":
        errors.append(
            _error(
                "bp76_must_not_execute_runtime_application",
                "runtime_application_status",
                result.get("runtime_application_status"),
            )
        )
    errors.extend(_validate_no_runtime_mutation_fields(result))
    errors.extend(
        _validate_execution_precheck_report_shape(_dict(result.get("execution_precheck_report")))
    )
    errors.extend(_validate_blocked_reason_report_shape(_dict(result.get("blocked_reason_report"))))
    errors.extend(
        _validate_final_gate_dependency_report_shape(
            _dict(result.get("final_gate_dependency_report"))
        )
    )
    errors.extend(
        _validate_non_execution_evidence_report_shape(
            _dict(result.get("non_execution_evidence_report"))
        )
    )
    errors.extend(
        _validate_runtime_mutation_prevention_report_shape(
            _dict(result.get("runtime_mutation_prevention_report"))
        )
    )
    errors.extend(
        _validate_post_execution_readiness_report_shape(
            _dict(result.get("post_execution_readiness_report"))
        )
    )
    errors.extend(_validate_next_actions(_list(result.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(result.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(result))
    return errors


def _validate_execution_precheck_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        EXECUTION_PRECHECK_REPORT_REQUIRED_FIELDS,
        "execution_precheck_report",
    )
    errors.extend(
        _validate_status(
            "reexecution_execution_status",
            report.get("reexecution_execution_status"),
            ALLOWED_REEXECUTION_EXECUTION_STATUSES,
        )
    )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_blocked_reason_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        BLOCKED_REASON_REPORT_REQUIRED_FIELDS,
        "blocked_reason_report",
    )
    errors.extend(
        _validate_status(
            "reexecution_execution_status",
            report.get("reexecution_execution_status"),
            ALLOWED_REEXECUTION_EXECUTION_STATUSES,
        )
    )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_final_gate_dependency_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS,
        "final_gate_dependency_report",
    )
    if report.get("final_gate_rerun_performed") is not False and report.get(
        "final_gate_dependency_status"
    ) != "final_gate_dependency_satisfied":
        errors.append(
            _error(
                "final_gate_dependency_status_must_match_performed_state",
                "final_gate_dependency_status",
                report.get("final_gate_dependency_status"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_non_execution_evidence_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        NON_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS,
        "non_execution_evidence_report",
    )
    for field in [
        "reexecution_command_not_executed",
        "runtime_application_command_not_executed",
        "model_asset_sha_unchanged",
        "protected_baselines_not_replaced",
        "production_config_not_created",
        "candidate_option_inventory_not_selection",
    ]:
        if report.get(field) is not True:
            errors.append(_error(f"{field}_must_be_true", field, report.get(field)))
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_runtime_mutation_prevention_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS,
        "runtime_mutation_prevention_report",
    )
    if report.get("runtime_config_changed") is not False:
        errors.append(
            _error(
                "runtime_config_changed_must_remain_false",
                "runtime_config_changed",
                report.get("runtime_config_changed"),
            )
        )
    if report.get("mutation_status") != "no_runtime_mutation_due_to_blocker":
        errors.append(
            _error(
                "mutation_status_must_remain_blocked",
                "mutation_status",
                report.get("mutation_status"),
            )
        )
    if report.get("application_status") != "not_executed":
        errors.append(
            _error(
                "application_status_must_remain_not_executed",
                "application_status",
                report.get("application_status"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_post_execution_readiness_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        POST_EXECUTION_READINESS_REPORT_REQUIRED_FIELDS,
        "post_execution_readiness_report",
    )
    errors.extend(
        _validate_status(
            "reexecution_execution_status",
            report.get("reexecution_execution_status"),
            ALLOWED_REEXECUTION_EXECUTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_result_status",
            report.get("reexecution_result_status"),
            ALLOWED_REEXECUTION_RESULT_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_outcome_status",
            report.get("reexecution_outcome_status"),
            ALLOWED_REEXECUTION_OUTCOME_STATUSES,
        )
    )
    if report.get("post_execution_verification_status") != (
        "post_execution_verification_not_available"
    ):
        errors.append(
            _error(
                "post_execution_verification_status_must_remain_unavailable",
                "post_execution_verification_status",
                report.get("post_execution_verification_status"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _status_fields_for_bp75_packet(packet: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "reexecution_request_status",
            packet.get("reexecution_request_status"),
            ALLOWED_REEXECUTION_REQUEST_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            packet.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "final_gate_rerun_execution_status",
            packet.get("final_gate_rerun_execution_status"),
            ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
        ),
        (
            "final_gate_rerun_result_status",
            packet.get("final_gate_rerun_result_status"),
            ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES,
        ),
        (
            "final_gate_rerun_outcome_status",
            packet.get("final_gate_rerun_outcome_status"),
            ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES,
        ),
        (
            "final_gate_rerun_request_status",
            packet.get("final_gate_rerun_request_status"),
            ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
        ),
        (
            "human_resolution_completeness_gate_status",
            packet.get("human_resolution_completeness_gate_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES,
        ),
        (
            "human_resolution_record_status",
            packet.get("human_resolution_record_status"),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        ),
        (
            "human_resolution_provided_status",
            packet.get("human_resolution_provided_status"),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        ),
        (
            "human_resolution_completeness_status",
            packet.get("human_resolution_completeness_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        ),
        (
            "missing_input_status",
            packet.get("missing_input_status"),
            ALLOWED_MISSING_INPUT_STATUSES,
        ),
        (
            "operator_input_completeness_status",
            packet.get("operator_input_completeness_status"),
            ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "candidate_input_completeness_status",
            packet.get("candidate_input_completeness_status"),
            ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "operator_signoff_status",
            packet.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "selected_candidate_status",
            packet.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "runtime_application_status",
            packet.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]


def _status_fields_for_result(result: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "reexecution_execution_status",
            result.get("reexecution_execution_status"),
            ALLOWED_REEXECUTION_EXECUTION_STATUSES,
        ),
        (
            "reexecution_result_status",
            result.get("reexecution_result_status"),
            ALLOWED_REEXECUTION_RESULT_STATUSES,
        ),
        (
            "reexecution_outcome_status",
            result.get("reexecution_outcome_status"),
            ALLOWED_REEXECUTION_OUTCOME_STATUSES,
        ),
        *_status_fields_for_bp75_packet(result),
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
    if (
        "prepare_post_reexecution_verification_after_runtime_execution" in recommendations
        and "prepare_reexecution_after_final_gate_rerun" not in recommendations
    ):
        errors.append(
            _error(
                "post_reexecution_verification_requires_runtime_reexecution_readiness",
                "next_action_recommendation",
                recommendations,
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
            if key in FORBIDDEN_REEXECUTION_EXECUTION_BLOCKED_RESULT_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif (
        isinstance(payload, str)
        and payload in FORBIDDEN_REEXECUTION_EXECUTION_BLOCKED_RESULT_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _result_status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "reexecution_execution_status",
        "reexecution_result_status",
        "reexecution_outcome_status",
        "reexecution_request_status",
        "reexecution_readiness_status",
        "final_gate_rerun_execution_status",
        "final_gate_rerun_result_status",
        "final_gate_rerun_outcome_status",
        "final_gate_rerun_request_status",
        "human_resolution_completeness_gate_status",
        "human_resolution_record_status",
        "human_resolution_provided_status",
        "human_resolution_completeness_status",
        "missing_input_status",
        "operator_input_completeness_status",
        "candidate_input_completeness_status",
        "operator_signoff_status",
        "selected_candidate_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_VERSION
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_75",
        "scope": "controlled_runtime_calibration_reexecution_execution_blocked_result",
        "runtime_boundary": "no_runtime_reexecution_or_application_or_config_mutation",
    }
