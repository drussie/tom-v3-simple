from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_request_packet import (  # noqa: E501
    ALLOWED_BP73_FINAL_GATE_RERUN_READINESS_STATUSES,
    ALLOWED_BP73_REEXECUTION_READINESS_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT,
    FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS,
)
from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_request_packet import (  # noqa: E501
    SOURCE_CONTRACT_REFS as BP73_SOURCE_CONTRACT_REFS,
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
    ALLOWED_RUNTIME_APPLICATION_STATUSES,
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
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_VERSION = (  # noqa: E501
    "v1"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_execution_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PRECHECK_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_execution_precheck_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_BLOCKED_REASON_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_blocked_reason_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_NON_EXECUTION_EVIDENCE_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_non_execution_evidence_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_BLOCKER_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_reexecution_blocker_report"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE = (
    "controlled_runtime_calibration_runtime_mutation_prevention_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_BLUEPRINT = (
    "blueprint_74"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_BLUEPRINT_NAME = (  # noqa: E501
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_final_gate_rerun_execution_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_execution_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PRECHECK_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_execution_precheck_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_BLOCKED_REASON_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_blocked_reason_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_NON_EXECUTION_EVIDENCE_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_non_execution_evidence_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_BLOCKER_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_reexecution_blocker_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_MUTATION_PREVENTION_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_runtime_mutation_prevention_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_EXPORTED_AT = datetime(  # noqa: E501
    2026,
    6,
    22,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_final_gate_rerun_request_packet_contract_version": "v1",
    **dict(BP73_SOURCE_CONTRACT_REFS),
}

ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES = [
    "final_gate_rerun_execution_blocked_missing_human_resolution",
    "final_gate_rerun_execution_blocked_invalid_human_resolution",
    "final_gate_rerun_execution_blocked_missing_operator_signoff",
    "final_gate_rerun_execution_blocked_missing_selected_candidate",
    "final_gate_rerun_execution_blocked_request_not_ready",
    "final_gate_rerun_execution_not_attempted",
    "final_gate_rerun_execution_deferred_to_future_blueprint",
    "final_gate_rerun_execution_completed_structural_only",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES = [
    "final_gate_rerun_result_not_available",
    "final_gate_rerun_result_blocked",
    "final_gate_rerun_result_deferred",
    "final_gate_rerun_result_structural_only",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES = [
    "final_gate_rerun_not_performed",
    "final_gate_rerun_blocked",
    "final_gate_rerun_deferred",
    "final_gate_rerun_structural_only",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES = [
    "final_gate_rerun_not_ready_missing_human_resolution",
    "final_gate_rerun_ready_after_human_resolution",
    "final_gate_rerun_blocked_invalid_human_resolution",
    "final_gate_rerun_not_executed",
    "not_applicable",
]
ALLOWED_REEXECUTION_READINESS_STATUSES = [
    "reexecution_not_ready_blockers_unresolved",
    "reexecution_ready_after_final_gate_rerun",
    "reexecution_blocked_missing_operator_signoff",
    "reexecution_blocked_missing_selected_candidate",
    "reexecution_blocked_final_gate_not_rerun",
    "reexecution_not_executed",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "provide_human_resolution_inputs",
    "provide_operator_inputs",
    "provide_selected_candidate_inputs",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_human_resolution",
    "prepare_final_gate_rerun_execution_after_human_resolution",
    "prepare_reexecution_request_packet_after_final_gate_rerun",
    "no_runtime_action_recommended",
    "not_applicable",
]

EXECUTION_INPUT_REQUIRED_FIELDS = [
    "final_gate_rerun_execution_input_id",
    "final_gate_rerun_execution_input_type",
    "final_gate_rerun_execution_input_version",
    "generated_at",
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
    "requested_final_gate_rerun_status",
    "source_contract_refs",
    "source_artifact_refs",
    "source_status_snapshot",
    "warnings",
    "non_claims",
]
BLOCKED_RESULT_REQUIRED_FIELDS = [
    "final_gate_rerun_execution_blocked_result_id",
    "final_gate_rerun_execution_blocked_result_type",
    "final_gate_rerun_execution_blocked_result_version",
    "generated_at",
    "source_final_gate_rerun_execution_input_path",
    *EXECUTION_INPUT_REQUIRED_FIELDS[4:20],
    "candidate_option_refs",
    "candidate_option_count",
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
    "final_gate_rerun_readiness_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "runtime_config_changed",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "execution_precheck_report",
    "blocked_reason_report",
    "non_execution_evidence_report",
    "reexecution_blocker_report",
    "runtime_mutation_prevention_report",
    "next_action_recommendation",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "model_asset_ref",
    "model_asset_sha256",
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
    "source_final_gate_rerun_request_packet_id",
    "bp73_request_packet_exists",
    "bp73_request_status",
    "bp72_completeness_gate_status",
    "bp71_human_resolution_record_status",
    "operator_input_completeness_status",
    "candidate_input_completeness_status",
    "final_gate_rerun_execution_blocked_before_command_execution",
    "runtime_application_blocked_before_any_mutation",
    "prechecks",
    "precheck_count",
    "satisfied_precheck_count",
    "unsatisfied_precheck_count",
    "warnings",
    "non_claims",
]
BLOCKED_REASON_REPORT_REQUIRED_FIELDS = [
    "blocked_reason_report_id",
    "blocked_reason_report_type",
    "blocked_reason_report_version",
    "generated_at",
    "source_final_gate_rerun_request_packet_id",
    "final_gate_rerun_execution_status",
    "blocked_reason_status",
    "blocked_reason_codes",
    "blocked_reasons",
    "blocked_reason_count",
    "warnings",
    "non_claims",
]
NON_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS = [
    "non_execution_evidence_report_id",
    "non_execution_evidence_report_type",
    "non_execution_evidence_report_version",
    "generated_at",
    "source_final_gate_rerun_request_packet_id",
    "final_gate_rerun_command_not_executed",
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
REEXECUTION_BLOCKER_REPORT_REQUIRED_FIELDS = [
    "reexecution_blocker_report_id",
    "reexecution_blocker_report_type",
    "reexecution_blocker_report_version",
    "generated_at",
    "source_final_gate_rerun_request_packet_id",
    "reexecution_readiness_status",
    "blockers",
    "blocker_count",
    "warnings",
    "non_claims",
]
RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS = [
    "runtime_mutation_prevention_report_id",
    "runtime_mutation_prevention_report_type",
    "runtime_mutation_prevention_report_version",
    "generated_at",
    "source_final_gate_rerun_request_packet_id",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "mutation_status",
    "application_status",
    "prevention_checks",
    "prevention_check_count",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "final_gate_rerun_execution_blocked_result_is_not_truth": True,
    "final_gate_rerun_execution_blocked_result_is_not_accuracy_scoring": True,
    "final_gate_rerun_execution_blocked_result_is_not_model_training": True,
    "final_gate_rerun_execution_blocked_result_is_not_runtime_application": True,
    "final_gate_rerun_execution_blocked_result_does_not_execute_final_gate_in_blocked_state": True,
    "final_gate_rerun_execution_blocked_result_does_not_execute_application": True,
    "final_gate_rerun_execution_blocked_result_does_not_create_production_config": True,
    "final_gate_rerun_execution_blocked_result_does_not_modify_model_weights": True,
    "final_gate_rerun_execution_blocked_result_does_not_replace_baselines": True,
    "final_gate_rerun_execution_blocked_result_does_not_infer_operator_signoff": True,
    "final_gate_rerun_execution_blocked_result_does_not_infer_candidate_selection": True,
    "final_gate_rerun_execution_blocked_result_does_not_infer_human_resolution": True,
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
    "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result": True,
    "final_gate_rerun_execution_blocked_missing_human_resolution": True,
    "final_gate_rerun_result_not_available": True,
    "final_gate_rerun_not_performed": True,
    "final_gate_rerun_command_not_executed": True,
    "runtime_application_command_not_executed": True,
    "human_resolution_completeness_gate_not_ready": True,
    "required_human_inputs_missing": True,
    "operator_inputs_incomplete": True,
    "candidate_inputs_incomplete": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "classifier_correctness_not_assessed": True,
    "candidate_option_inventory_not_selection": True,
    **NON_CLAIMS,
}
FORBIDDEN_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TOKENS = {
    *FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS,
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
}


def export_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract(  # noqa: E501
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "final_gate_rerun_execution_scope": {
            "creates_final_gate_rerun_execution_blocked_result": True,
            "bp73_request_packet_is_authoritative_source": True,
            "bp72_completeness_gate_must_be_ready_before_execution": True,
            "default_state_remains_blocked_without_complete_human_resolution": True,
            "candidate_option_discovery_is_inventory_only": True,
            "single_candidate_option_does_not_create_selection": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_infer_human_resolution": True,
            "does_not_execute_final_gate_in_blocked_state": True,
            "does_not_write_runtime_config": True,
            "does_not_execute_runtime_application": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "execution_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUT_TYPE,
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUT_VERSION
            ),
            "required_fields": list(EXECUTION_INPUT_REQUIRED_FIELDS),
        },
        "blocked_result_schema": {
            "result_type": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TYPE
            ),
            "result_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(BLOCKED_RESULT_REQUIRED_FIELDS),
            "allowed_final_gate_rerun_execution_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES
            ),
            "allowed_final_gate_rerun_result_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES
            ),
            "allowed_final_gate_rerun_outcome_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES
            ),
            "allowed_final_gate_rerun_request_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES
            ),
            "allowed_final_gate_rerun_readiness_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES
            ),
            "allowed_reexecution_readiness_statuses": list(
                ALLOWED_REEXECUTION_READINESS_STATUSES
            ),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "execution_precheck_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PRECHECK_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(EXECUTION_PRECHECK_REPORT_REQUIRED_FIELDS),
        },
        "blocked_reason_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_BLOCKED_REASON_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(BLOCKED_REASON_REPORT_REQUIRED_FIELDS),
        },
        "non_execution_evidence_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_NON_EXECUTION_EVIDENCE_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(NON_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS),
        },
        "reexecution_blocker_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_BLOCKER_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(REEXECUTION_BLOCKER_REPORT_REQUIRED_FIELDS),
        },
        "runtime_mutation_prevention_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
            ),
            "required_fields": list(RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_execution_input_shape": True,
            "validate_blocked_result_artifact_shape": True,
            "validate_execution_precheck_report_shape": True,
            "validate_blocked_reason_report_shape": True,
            "validate_non_execution_evidence_report_shape": True,
            "validate_reexecution_blocker_report_shape": True,
            "validate_runtime_mutation_prevention_report_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_current_blocked_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_execution_blocked_unless_bp73_and_bp72_are_ready": True,
            "validate_final_gate_rerun_command_not_executed_by_bp74": True,
            "validate_runtime_application_not_executed_by_bp74": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_single_candidate_option": True,
            "validate_no_human_resolution_is_inferred": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_execution_block_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_auto_label_segments": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp73_final_gate_rerun_request_packet_path_required": True,
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


def build_controlled_runtime_calibration_final_gate_rerun_execution_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    source_final_gate_rerun_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    source_final_gate_rerun_request_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(source_final_gate_rerun_request_packet_path)
    model_asset_ref = packet.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = packet.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    runtime_target_ref = _dict(packet.get("runtime_config_target_ref"))
    runtime_target_path = runtime_target_ref.get("path")
    runtime_sha_after = (
        _sha256_file(Path(runtime_target_path))
        if runtime_target_path
        else packet.get("runtime_config_target_sha256_after")
    )
    inputs = {
        "final_gate_rerun_execution_input_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_execution_inputs_v1",
            packet.get("final_gate_rerun_request_packet_id"),
            packet.get("final_gate_rerun_request_status"),
            packet.get("human_resolution_completeness_gate_status"),
            packet.get("final_gate_rerun_readiness_status"),
            packet.get("runtime_config_target_sha256_before"),
            runtime_sha_after,
        ),
        "final_gate_rerun_execution_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUT_TYPE
        ),
        "final_gate_rerun_execution_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_path": str(
            Path(source_final_gate_rerun_request_packet_path)
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
        "candidate_option_refs": _list(packet.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": runtime_target_ref,
        "runtime_config_target_sha256_before": packet.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": runtime_sha_after,
        "requested_final_gate_rerun_status": packet.get("final_gate_rerun_request_status"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_final_gate_rerun_request_packet_path,
            source_final_gate_rerun_request_packet_contract_path,
            packet,
        ),
        "source_status_snapshot": _status_snapshot_from_packet(packet),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_execution_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_execution_inputs",
        "final_gate_rerun_execution_input_id": inputs[
            "final_gate_rerun_execution_input_id"
        ],
        **_execution_status_snapshot_from_inputs(inputs),
        "candidate_option_count": len(inputs["candidate_option_refs"]),
        "next_action_recommendation": _next_actions_from_packet(packet),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_final_gate_rerun_execution_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(final_gate_rerun_execution_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_execution_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_final_gate_rerun_execution_inputs_validation"
        ),
        payload_path=final_gate_rerun_execution_inputs_path,
        payload_type=inputs.get("final_gate_rerun_execution_input_type"),
        payload_version=inputs.get("final_gate_rerun_execution_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_execution_status_snapshot_from_inputs(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(final_gate_rerun_execution_inputs_path)
    packet = _source_request_packet(inputs)
    result_id = _stable_id(
        "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_v1",
        inputs.get("final_gate_rerun_execution_input_id"),
        packet.get("final_gate_rerun_request_packet_id"),
        packet.get("final_gate_rerun_request_status"),
        packet.get("final_gate_rerun_readiness_status"),
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    execution_status = _execution_status(packet)
    result_status = _result_status(execution_status)
    outcome_status = _outcome_status(execution_status)
    runtime_application_status = "not_executed"
    result = {
        "final_gate_rerun_execution_blocked_result_id": result_id,
        "final_gate_rerun_execution_blocked_result_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TYPE
        ),
        "final_gate_rerun_execution_blocked_result_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_execution_input_path": str(
            Path(final_gate_rerun_execution_inputs_path)
        ),
        **_source_paths_from_inputs(inputs),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "final_gate_rerun_execution_status": execution_status,
        "final_gate_rerun_result_status": result_status,
        "final_gate_rerun_outcome_status": outcome_status,
        **_status_snapshot_from_packet(packet),
        "runtime_application_status": runtime_application_status,
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get("runtime_config_target_sha256_after"),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "execution_precheck_report": _execution_precheck_report(
            result_id,
            packet,
            inputs,
            generated_at,
        ),
        "blocked_reason_report": _blocked_reason_report(
            result_id,
            packet,
            execution_status,
            generated_at,
        ),
        "non_execution_evidence_report": _non_execution_evidence_report(
            result_id,
            packet,
            inputs,
            generated_at,
        ),
        "reexecution_blocker_report": _reexecution_blocker_report(
            result_id,
            packet,
            generated_at,
        ),
        "runtime_mutation_prevention_report": _runtime_mutation_prevention_report(
            result_id,
            packet,
            inputs,
            generated_at,
        ),
        "next_action_recommendation": _next_actions_from_packet(packet),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_execution_inputs_shape(inputs))
    errors.extend(_validate_blocked_result_shape(result))
    _write_json_if_requested(output_path, result)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_execution_blocked_result",
        "final_gate_rerun_execution_blocked_result_id": result_id,
        **_result_status_snapshot(result),
        "candidate_option_count": result["candidate_option_count"],
        "next_action_recommendation": result["next_action_recommendation"],
        "final_gate_rerun_execution_blocked_result_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_final_gate_rerun_execution_blocked_result(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    result_payload = _load_json(final_gate_rerun_execution_blocked_result_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_blocked_result_shape(result_payload))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_validation"
        ),
        payload_path=final_gate_rerun_execution_blocked_result_path,
        payload_type=result_payload.get("final_gate_rerun_execution_blocked_result_type"),
        payload_version=result_payload.get("final_gate_rerun_execution_blocked_result_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_result_status_snapshot(result_payload),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_final_gate_rerun_execution_precheck_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PRECHECK_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=final_gate_rerun_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="execution_precheck_report",
        report_validator=_validate_execution_precheck_report_shape,
        output_key="final_gate_rerun_execution_precheck_report_output",
    )


def build_controlled_runtime_calibration_final_gate_rerun_blocked_reason_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_BLOCKED_REASON_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=final_gate_rerun_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="blocked_reason_report",
        report_validator=_validate_blocked_reason_report_shape,
        output_key="final_gate_rerun_blocked_reason_report_output",
    )


def build_controlled_runtime_calibration_final_gate_rerun_non_execution_evidence_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_NON_EXECUTION_EVIDENCE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=final_gate_rerun_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="non_execution_evidence_report",
        report_validator=_validate_non_execution_evidence_report_shape,
        output_key="final_gate_rerun_non_execution_evidence_report_output",
    )


def build_controlled_runtime_calibration_final_gate_rerun_reexecution_blocker_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_BLOCKER_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=final_gate_rerun_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="reexecution_blocker_report",
        report_validator=_validate_reexecution_blocker_report_shape,
        output_key="final_gate_rerun_reexecution_blocker_report_output",
    )


def build_controlled_runtime_calibration_runtime_mutation_prevention_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_MUTATION_PREVENTION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        result_path=final_gate_rerun_execution_blocked_result_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="runtime_mutation_prevention_report",
        report_validator=_validate_runtime_mutation_prevention_report_shape,
        output_key="runtime_mutation_prevention_report_output",
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
        "source_final_gate_rerun_execution_blocked_result_path": str(Path(result_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_blocked_result_shape(result))
    errors.extend(report_validator(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else f"invalid_{report_key}",
        "final_gate_rerun_execution_blocked_result_id": result.get(
            "final_gate_rerun_execution_blocked_result_id"
        ),
        **_result_status_snapshot(result),
        output_key: _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _source_artifact_refs(
    request_packet_path: str | Path,
    request_contract_path: str | Path,
    packet: dict[str, Any],
) -> dict[str, Any]:
    refs = {
        "final_gate_rerun_request_packet": _artifact_ref(request_packet_path, packet),
        "final_gate_rerun_request_packet_contract": _artifact_ref(
            request_contract_path,
            _load_json_if_exists(request_contract_path),
        ),
    }
    refs.update(_dict(packet.get("source_artifact_refs")))
    return refs


def _source_request_packet(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(inputs.get("source_final_gate_rerun_request_packet_path"))


def _source_paths_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_final_gate_rerun_request_packet_path": inputs.get(
            "source_final_gate_rerun_request_packet_path"
        ),
        "source_human_resolution_completeness_gate_path": inputs.get(
            "source_human_resolution_completeness_gate_path"
        ),
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
    }


def _request_ready(packet: dict[str, Any]) -> bool:
    return (
        packet.get("final_gate_rerun_request_status")
        == "final_gate_rerun_request_ready_after_human_resolution"
        and packet.get("human_resolution_completeness_gate_status")
        == "human_resolution_completeness_gate_ready_for_final_gate_rerun"
        and packet.get("human_resolution_completeness_status") == "human_resolution_complete"
        and packet.get("missing_input_status") == "no_required_inputs_missing"
        and packet.get("operator_input_completeness_status") == "operator_inputs_complete"
        and packet.get("candidate_input_completeness_status") == "candidate_inputs_complete"
        and packet.get("final_gate_rerun_readiness_status")
        == "final_gate_rerun_ready_after_human_resolution"
    )


def _execution_status(packet: dict[str, Any]) -> str:
    if _request_ready(packet):
        return "final_gate_rerun_execution_deferred_to_future_blueprint"
    if packet.get("final_gate_rerun_request_status") == (
        "final_gate_rerun_request_blocked_invalid_human_resolution"
    ):
        return "final_gate_rerun_execution_blocked_invalid_human_resolution"
    if packet.get("human_resolution_completeness_status") != "human_resolution_complete":
        return "final_gate_rerun_execution_blocked_missing_human_resolution"
    if packet.get("operator_input_completeness_status") != "operator_inputs_complete":
        return "final_gate_rerun_execution_blocked_missing_operator_signoff"
    if packet.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        return "final_gate_rerun_execution_blocked_missing_selected_candidate"
    return "final_gate_rerun_execution_blocked_request_not_ready"


def _result_status(execution_status: str) -> str:
    if execution_status == "final_gate_rerun_execution_deferred_to_future_blueprint":
        return "final_gate_rerun_result_deferred"
    if execution_status == "final_gate_rerun_execution_completed_structural_only":
        return "final_gate_rerun_result_structural_only"
    return "final_gate_rerun_result_not_available"


def _outcome_status(execution_status: str) -> str:
    if execution_status == "final_gate_rerun_execution_deferred_to_future_blueprint":
        return "final_gate_rerun_deferred"
    if execution_status == "final_gate_rerun_execution_completed_structural_only":
        return "final_gate_rerun_structural_only"
    return "final_gate_rerun_not_performed"


def _reexecution_readiness_status(packet: dict[str, Any]) -> str:
    if _request_ready(packet):
        return "reexecution_blocked_final_gate_not_rerun"
    status = packet.get("reexecution_readiness_status")
    if status in ALLOWED_REEXECUTION_READINESS_STATUSES:
        return status
    return "reexecution_not_ready_blockers_unresolved"


def _status_snapshot_from_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "final_gate_rerun_request_status": packet.get("final_gate_rerun_request_status"),
        "human_resolution_completeness_gate_status": packet.get(
            "human_resolution_completeness_gate_status"
        ),
        "human_resolution_record_status": packet.get("human_resolution_record_status"),
        "human_resolution_provided_status": packet.get("human_resolution_provided_status"),
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
        "final_gate_rerun_readiness_status": packet.get(
            "final_gate_rerun_readiness_status"
        ),
        "reexecution_readiness_status": _reexecution_readiness_status(packet),
    }


def _execution_status_snapshot_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    packet = _source_request_packet(inputs)
    return {
        "final_gate_rerun_execution_status": _execution_status(packet),
        "final_gate_rerun_result_status": _result_status(_execution_status(packet)),
        "final_gate_rerun_outcome_status": _outcome_status(_execution_status(packet)),
        **_status_snapshot_from_packet(packet),
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
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    prechecks = [
        _check(
            "bp73_request_packet_exists",
            bool(packet),
            bool(packet),
            inputs.get("source_final_gate_rerun_request_packet_path"),
        ),
        _check(
            "bp73_request_status_is_ready",
            packet.get("final_gate_rerun_request_status")
            == "final_gate_rerun_request_ready_after_human_resolution",
            packet.get("final_gate_rerun_request_status"),
            inputs.get("source_final_gate_rerun_request_packet_path"),
        ),
        _check(
            "bp72_completeness_gate_ready",
            packet.get("human_resolution_completeness_gate_status")
            == "human_resolution_completeness_gate_ready_for_final_gate_rerun",
            packet.get("human_resolution_completeness_gate_status"),
            packet.get("source_human_resolution_completeness_gate_path"),
        ),
        _check(
            "bp71_explicit_human_resolution_record_complete",
            packet.get("human_resolution_record_status")
            == "human_resolution_record_created_with_complete_explicit_inputs",
            packet.get("human_resolution_record_status"),
            packet.get("source_explicit_human_resolution_record_path"),
        ),
        _check(
            "operator_inputs_complete",
            packet.get("operator_input_completeness_status") == "operator_inputs_complete",
            packet.get("operator_input_completeness_status"),
            packet.get("source_explicit_operator_signoff_artifact_path"),
        ),
        _check(
            "candidate_inputs_complete",
            packet.get("candidate_input_completeness_status") == "candidate_inputs_complete",
            packet.get("candidate_input_completeness_status"),
            packet.get("source_explicit_selected_candidate_artifact_path"),
        ),
        _check(
            "final_gate_rerun_command_not_executed",
            True,
            "final_gate_rerun_command_not_executed",
            None,
        ),
        _check(
            "runtime_application_command_not_executed",
            True,
            "runtime_application_command_not_executed",
            None,
        ),
    ]
    satisfied = sum(1 for item in prechecks if item["satisfied"])
    return {
        "execution_precheck_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_execution_precheck_report_v1",
            result_id,
            satisfied,
            len(prechecks),
        ),
        "execution_precheck_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PRECHECK_REPORT_TYPE
        ),
        "execution_precheck_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet.get(
            "final_gate_rerun_request_packet_id"
        ),
        "bp73_request_packet_exists": bool(packet),
        "bp73_request_status": packet.get("final_gate_rerun_request_status"),
        "bp72_completeness_gate_status": packet.get(
            "human_resolution_completeness_gate_status"
        ),
        "bp71_human_resolution_record_status": packet.get(
            "human_resolution_record_status"
        ),
        "operator_input_completeness_status": packet.get(
            "operator_input_completeness_status"
        ),
        "candidate_input_completeness_status": packet.get(
            "candidate_input_completeness_status"
        ),
        "final_gate_rerun_execution_blocked_before_command_execution": not _request_ready(
            packet
        ),
        "runtime_application_blocked_before_any_mutation": True,
        "prechecks": prechecks,
        "precheck_count": len(prechecks),
        "satisfied_precheck_count": satisfied,
        "unsatisfied_precheck_count": len(prechecks) - satisfied,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocked_reason_report(
    result_id: str,
    packet: dict[str, Any],
    execution_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    codes = _blocked_reason_codes(packet)
    reasons = [
        {
            "blocked_reason_code": code,
            "status": "required",
            "source": _blocked_reason_source(code, packet),
        }
        for code in codes
    ]
    return {
        "blocked_reason_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_blocked_reason_report_v1",
            result_id,
            execution_status,
            *codes,
        ),
        "blocked_reason_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_BLOCKED_REASON_REPORT_TYPE
        ),
        "blocked_reason_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet.get(
            "final_gate_rerun_request_packet_id"
        ),
        "final_gate_rerun_execution_status": execution_status,
        "blocked_reason_status": "blocked_reasons_present" if codes else "no_blockers_detected",
        "blocked_reason_codes": codes,
        "blocked_reasons": reasons,
        "blocked_reason_count": len(reasons),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocked_reason_codes(packet: dict[str, Any]) -> list[str]:
    blocker_codes = [
        str(blocker.get("blocker_code"))
        for blocker in _list(_dict(packet.get("blocker_report")).get("blockers"))
        if blocker.get("blocker_code")
    ]
    required = [
        "missing_operator_identity",
        "missing_operator_attestation",
        "missing_operator_timestamp",
        "missing_selected_candidate_ref",
        "missing_selected_candidate_source_path",
        "missing_selected_candidate_selection_reason",
        "missing_candidate_selection_timestamp",
        "missing_operator_reference_for_selection",
        "human_resolution_completeness_gate_not_ready",
        "final_gate_rerun_request_blocked_missing_human_resolution",
    ]
    if packet.get("operator_input_completeness_status") == "operator_inputs_complete":
        required = [code for code in required if not code.startswith("missing_operator")]
    if packet.get("candidate_input_completeness_status") == "candidate_inputs_complete":
        required = [code for code in required if not code.startswith("missing_selected")]
    if packet.get("human_resolution_completeness_gate_status") == (
        "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    ):
        required = [
            code
            for code in required
            if code
            not in {
                "human_resolution_completeness_gate_not_ready",
                "final_gate_rerun_request_blocked_missing_human_resolution",
            }
        ]
    return _unique_strings([*blocker_codes, *required])


def _blocked_reason_source(code: str, packet: dict[str, Any]) -> str | None:
    if code.startswith("missing_operator"):
        return packet.get("source_explicit_operator_signoff_artifact_path")
    if code.startswith("missing_selected") or code.startswith("missing_candidate"):
        return packet.get("source_explicit_selected_candidate_artifact_path")
    if code == "human_resolution_completeness_gate_not_ready":
        return packet.get("source_human_resolution_completeness_gate_path")
    return packet.get("source_final_gate_rerun_request_packet_path")


def _non_execution_evidence_report(
    result_id: str,
    packet: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    model_sha_before = packet.get("model_asset_sha256")
    model_sha_after = inputs.get("model_asset_sha256")
    runtime_before = inputs.get("runtime_config_target_sha256_before")
    runtime_after = inputs.get("runtime_config_target_sha256_after")
    evidence_items = [
        _evidence("final_gate_rerun_command_not_executed", True, None),
        _evidence("runtime_application_command_not_executed", True, None),
        _evidence("runtime_config_sha_unchanged", runtime_before == runtime_after, runtime_after),
        _evidence(
            "model_asset_sha_unchanged",
            model_sha_before == model_sha_after,
            model_sha_after,
        ),
        _evidence("protected_baselines_not_replaced", True, None),
        _evidence("production_config_not_created", True, packet.get("production_config_status")),
        _evidence(
            "candidate_option_inventory_not_selection",
            True,
            len(_list(inputs.get("candidate_option_refs"))),
        ),
    ]
    return {
        "non_execution_evidence_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_non_execution_evidence_report_v1",
            result_id,
            runtime_before,
            runtime_after,
            model_sha_before,
            model_sha_after,
        ),
        "non_execution_evidence_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_NON_EXECUTION_EVIDENCE_REPORT_TYPE
        ),
        "non_execution_evidence_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet.get(
            "final_gate_rerun_request_packet_id"
        ),
        "final_gate_rerun_command_not_executed": True,
        "runtime_application_command_not_executed": True,
        "runtime_config_sha_unchanged": runtime_before == runtime_after,
        "model_asset_sha_unchanged": model_sha_before == model_sha_after,
        "protected_baselines_not_replaced": True,
        "production_config_not_created": True,
        "candidate_option_inventory_not_selection": True,
        "evidence_items": evidence_items,
        "evidence_item_count": len(evidence_items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _reexecution_blocker_report(
    result_id: str,
    packet: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    blockers = [
        _blocker(
            "human_resolution_complete",
            packet.get("human_resolution_completeness_status") == "human_resolution_complete",
            packet.get("human_resolution_completeness_status"),
        ),
        _blocker(
            "operator_inputs_complete",
            packet.get("operator_input_completeness_status") == "operator_inputs_complete",
            packet.get("operator_input_completeness_status"),
        ),
        _blocker(
            "candidate_inputs_complete",
            packet.get("candidate_input_completeness_status") == "candidate_inputs_complete",
            packet.get("candidate_input_completeness_status"),
        ),
        _blocker(
            "final_gate_rerun_performed",
            False,
            "final_gate_rerun_not_performed",
        ),
        _blocker(
            "runtime_application_not_executed",
            True,
            "not_executed",
        ),
    ]
    unresolved = [item for item in blockers if not item["satisfied"]]
    return {
        "reexecution_blocker_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_reexecution_blocker_report_v1",
            result_id,
            *[item["blocker_code"] for item in unresolved],
        ),
        "reexecution_blocker_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_BLOCKER_REPORT_TYPE
        ),
        "reexecution_blocker_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet.get(
            "final_gate_rerun_request_packet_id"
        ),
        "reexecution_readiness_status": _reexecution_readiness_status(packet),
        "blockers": blockers,
        "blocker_count": len(unresolved),
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
            _dict(inputs.get("runtime_config_target_ref")).get("path"),
        ),
        _check("runtime_config_changed_false", True, False, None),
        _check("mutation_status_blocked", True, "no_runtime_mutation_due_to_blocker", None),
        _check("runtime_application_not_executed", True, "not_executed", None),
        _check("model_weights_not_modified", True, packet.get("model_update_status"), None),
        _check("baselines_not_replaced", True, packet.get("baseline_update_status"), None),
    ]
    return {
        "runtime_mutation_prevention_report_id": _stable_id(
            "controlled_runtime_calibration_runtime_mutation_prevention_report_v1",
            result_id,
            inputs.get("runtime_config_target_sha256_before"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        "runtime_mutation_prevention_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE
        ),
        "runtime_mutation_prevention_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet.get(
            "final_gate_rerun_request_packet_id"
        ),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get("runtime_config_target_sha256_after"),
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "application_status": "not_executed",
        "prevention_checks": checks,
        "prevention_check_count": len(checks),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _check(
    check_code: str,
    satisfied: bool,
    observed_value: Any,
    source_path: str | None,
) -> dict[str, Any]:
    return {
        "check_code": check_code,
        "satisfied": bool(satisfied),
        "observed_value": observed_value,
        "source_path": source_path,
    }


def _evidence(evidence_code: str, present: bool, observed_value: Any) -> dict[str, Any]:
    return {
        "evidence_code": evidence_code,
        "present": bool(present),
        "observed_value": observed_value,
    }


def _blocker(blocker_code: str, satisfied: bool, current_status: Any) -> dict[str, Any]:
    return {
        "blocker_code": blocker_code,
        "satisfied": bool(satisfied),
        "current_status": current_status,
    }


def _next_actions_from_packet(packet: dict[str, Any]) -> list[str]:
    if _request_ready(packet):
        return [
            "rerun_final_gate_after_human_resolution",
            "prepare_final_gate_rerun_execution_after_human_resolution",
            "prepare_reexecution_request_packet_after_final_gate_rerun",
        ]
    actions: list[str] = []
    if packet.get("operator_input_completeness_status") != "operator_inputs_complete":
        actions.append("provide_operator_inputs")
    if packet.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        actions.append("provide_selected_candidate_inputs")
    actions.append("provide_operator_signoff_and_selected_candidate")
    actions.append("rerun_final_gate_after_human_resolution")
    return _unique_strings(actions)


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "final_gate_rerun_execution_scope",
        "source_contract_refs",
        "execution_input_schema",
        "blocked_result_schema",
        "execution_precheck_report_schema",
        "blocked_reason_report_schema",
        "non_execution_evidence_report_schema",
        "reexecution_blocker_report_schema",
        "runtime_mutation_prevention_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_execution_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, EXECUTION_INPUT_REQUIRED_FIELDS, "inputs")
    packet = _source_request_packet(inputs)
    errors.extend(_validate_execution_source_packet_shape(packet))
    errors.extend(_validate_no_runtime_mutation_fields(inputs))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_execution_source_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        packet,
        [
            "final_gate_rerun_request_packet_id",
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
            "final_gate_rerun_readiness_status",
            "reexecution_readiness_status",
            "runtime_application_status",
            "runtime_config_changed",
            "mutation_status",
            "production_config_status",
            "baseline_update_status",
            "model_update_status",
        ],
        "source_final_gate_rerun_request_packet",
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_request_status",
            packet.get("final_gate_rerun_request_status"),
            ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_readiness_status",
            packet.get("final_gate_rerun_readiness_status"),
            ALLOWED_BP73_FINAL_GATE_RERUN_READINESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            packet.get("reexecution_readiness_status"),
            ALLOWED_BP73_REEXECUTION_READINESS_STATUSES,
        )
    )
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


def _validate_blocked_result_shape(result: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(result, BLOCKED_RESULT_REQUIRED_FIELDS, "blocked_result")
    for field, value, allowed in _status_fields_for_result(result):
        errors.extend(_validate_status(field, value, allowed))
    if result.get("final_gate_rerun_execution_status") != _execution_status(result):
        errors.append(
            _error(
                "execution_status_must_match_source_request_state",
                "final_gate_rerun_execution_status",
                result.get("final_gate_rerun_execution_status"),
            )
        )
    if result.get("final_gate_rerun_result_status") != _result_status(
        result.get("final_gate_rerun_execution_status")
    ):
        errors.append(
            _error(
                "result_status_must_match_execution_status",
                "final_gate_rerun_result_status",
                result.get("final_gate_rerun_result_status"),
            )
        )
    if result.get("final_gate_rerun_outcome_status") != _outcome_status(
        result.get("final_gate_rerun_execution_status")
    ):
        errors.append(
            _error(
                "outcome_status_must_match_execution_status",
                "final_gate_rerun_outcome_status",
                result.get("final_gate_rerun_outcome_status"),
            )
        )
    if result.get("runtime_application_status") != "not_executed":
        errors.append(
            _error(
                "bp74_must_not_execute_runtime_application",
                "runtime_application_status",
                result.get("runtime_application_status"),
            )
        )
    errors.extend(_validate_no_runtime_mutation_fields(result))
    errors.extend(
        _validate_execution_precheck_report_shape(
            _dict(result.get("execution_precheck_report"))
        )
    )
    errors.extend(
        _validate_blocked_reason_report_shape(_dict(result.get("blocked_reason_report")))
    )
    errors.extend(
        _validate_non_execution_evidence_report_shape(
            _dict(result.get("non_execution_evidence_report"))
        )
    )
    errors.extend(
        _validate_reexecution_blocker_report_shape(
            _dict(result.get("reexecution_blocker_report"))
        )
    )
    errors.extend(
        _validate_runtime_mutation_prevention_report_shape(
            _dict(result.get("runtime_mutation_prevention_report"))
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
            "final_gate_rerun_execution_status",
            report.get("final_gate_rerun_execution_status"),
            ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
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
        "final_gate_rerun_command_not_executed",
        "runtime_application_command_not_executed",
        "runtime_config_sha_unchanged",
        "model_asset_sha_unchanged",
        "protected_baselines_not_replaced",
        "production_config_not_created",
        "candidate_option_inventory_not_selection",
    ]:
        if report.get(field) is not True:
            errors.append(
                _error("required_non_execution_evidence_missing", field, report.get(field))
            )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_reexecution_blocker_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        REEXECUTION_BLOCKER_REPORT_REQUIRED_FIELDS,
        "reexecution_blocker_report",
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            report.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
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


def _status_fields_for_result(result: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "final_gate_rerun_execution_status",
            result.get("final_gate_rerun_execution_status"),
            ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
        ),
        (
            "final_gate_rerun_result_status",
            result.get("final_gate_rerun_result_status"),
            ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES,
        ),
        (
            "final_gate_rerun_outcome_status",
            result.get("final_gate_rerun_outcome_status"),
            ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES,
        ),
        (
            "final_gate_rerun_request_status",
            result.get("final_gate_rerun_request_status"),
            ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
        ),
        (
            "human_resolution_completeness_gate_status",
            result.get("human_resolution_completeness_gate_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES,
        ),
        (
            "human_resolution_record_status",
            result.get("human_resolution_record_status"),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        ),
        (
            "human_resolution_provided_status",
            result.get("human_resolution_provided_status"),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        ),
        (
            "human_resolution_completeness_status",
            result.get("human_resolution_completeness_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        ),
        (
            "missing_input_status",
            result.get("missing_input_status"),
            ALLOWED_MISSING_INPUT_STATUSES,
        ),
        (
            "operator_input_completeness_status",
            result.get("operator_input_completeness_status"),
            ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "candidate_input_completeness_status",
            result.get("candidate_input_completeness_status"),
            ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "operator_signoff_status",
            result.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "selected_candidate_status",
            result.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "final_gate_rerun_readiness_status",
            result.get("final_gate_rerun_readiness_status"),
            ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            result.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "runtime_application_status",
            result.get("runtime_application_status"),
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
    if (
        "prepare_final_gate_rerun_execution_after_human_resolution" in recommendations
        and "rerun_final_gate_after_human_resolution" not in recommendations
    ):
        errors.append(
            _error(
                "prepare_execution_requires_rerun_recommendation",
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
            if key in FORBIDDEN_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif (
        isinstance(payload, str)
        and payload in FORBIDDEN_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _result_status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
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
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_VERSION
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
        "blueprint": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_BLUEPRINT
        ),
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_73",
        "scope": "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result",
        "runtime_boundary": "no_final_gate_rerun_or_runtime_application_or_config_mutation",
    }
