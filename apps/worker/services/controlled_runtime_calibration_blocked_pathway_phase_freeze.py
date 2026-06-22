from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_post_reexecution_verification_not_available_packet import (  # noqa: E501
    ALLOWED_POST_REEXECUTION_OUTCOME_STATUSES,
    ALLOWED_POST_REEXECUTION_RESULT_STATUSES,
    ALLOWED_POST_REEXECUTION_VERIFICATION_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT,  # noqa: E501
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT,  # noqa: E501
)
from apps.worker.services.controlled_runtime_calibration_post_reexecution_verification_not_available_packet import (  # noqa: E501
    SOURCE_CONTRACT_REFS as BP77_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.controlled_runtime_calibration_post_reexecution_verification_not_available_packet import (  # noqa: E501
    _validate_packet_shape as _validate_bp77_packet_shape,
)
from apps.worker.services.controlled_runtime_calibration_reexecution_execution_blocked_result import (  # noqa: E501
    ALLOWED_REEXECUTION_OUTCOME_STATUSES,
    ALLOWED_REEXECUTION_RESULT_STATUSES,
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
    ALLOWED_RUNTIME_APPLICATION_STATUSES,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_TYPE = (
    "controlled_runtime_calibration_blocked_pathway_phase_freeze_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUT_TYPE = (
    "controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_TYPE = (
    "controlled_runtime_calibration_blocked_pathway_phase_freeze"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_COMPLETION_SUMMARY_TYPE = (
    "controlled_runtime_calibration_blocked_pathway_completion_summary"
)
CONTROLLED_RUNTIME_CALIBRATION_UNRESOLVED_HUMAN_INPUTS_REPORT_TYPE = (
    "controlled_runtime_calibration_unresolved_human_inputs_report"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_blocked_pathway_runtime_non_mutation_evidence_report"
)
CONTROLLED_RUNTIME_CALIBRATION_SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_TYPE = (
    "controlled_runtime_calibration_successful_pathway_remaining_work_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FUTURE_UNBLOCK_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_future_unblock_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_BLUEPRINT = "blueprint_78"
CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_blocked_pathway_phase_freeze_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/controlled_runtime_calibration_blocked_pathway_phase_freeze_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_blocked_pathway_phase_freeze_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_blocked_pathway_phase_freeze.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_COMPLETION_SUMMARY_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_blocked_pathway_completion_summary.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_UNRESOLVED_HUMAN_INPUTS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_unresolved_human_inputs_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_blocked_pathway_runtime_non_mutation_evidence_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_successful_pathway_remaining_work_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FUTURE_UNBLOCK_READINESS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_future_unblock_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_EXPORTED_AT = (
    datetime(2026, 6, 22, 0, 0, tzinfo=UTC)
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract_version": "v1",  # noqa: E501
    **dict(BP77_SOURCE_CONTRACT_REFS),
}

ALLOWED_BLOCKED_PATHWAY_PHASE_FREEZE_STATUSES = [
    "blocked_pathway_phase_freeze_completed",
    "blocked_pathway_phase_freeze_completed_with_warnings",
    "blocked_pathway_phase_freeze_blocked_missing_source_artifacts",
    "blocked_pathway_phase_freeze_informational_only",
    "not_applicable",
]
ALLOWED_BLOCKED_PATHWAY_COMPLETION_STATUSES = [
    "complete_for_blocked_pathway",
    "complete_for_blocked_pathway_with_warnings",
    "incomplete_missing_blocked_evidence",
    "not_applicable",
]
ALLOWED_SUCCESSFUL_PATHWAY_COMPLETION_STATUSES = [
    "incomplete_pending_explicit_human_resolution",
    "incomplete_pending_final_gate_rerun",
    "incomplete_pending_runtime_reexecution",
    "incomplete_pending_post_reexecution_verification",
    "complete_successful_runtime_calibration",
    "not_applicable",
]
ALLOWED_SUCCESSFUL_CALIBRATION_APPLICATION_STATUSES = [
    "not_completed",
    "completed_structural_only",
    "not_applicable",
]
ALLOWED_HUMAN_RESOLUTION_STATUSES = [
    "human_resolution_missing",
    "human_resolution_provided",
    "not_applicable",
]
ALLOWED_OPERATOR_SIGNOFF_STATUSES = [
    "operator_signoff_required",
    "operator_signoff_provided",
    "not_applicable",
]
ALLOWED_SELECTED_CANDIDATE_STATUSES = [
    "selected_candidate_required",
    "selected_candidate_provided",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_STATUSES = [
    "final_gate_rerun_not_performed",
    "final_gate_rerun_performed_structural_only",
    "not_applicable",
]
ALLOWED_REEXECUTION_STATUSES = [
    "reexecution_not_performed",
    "reexecution_performed_structural_only",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "stop_blocked_calibration_pathway",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_human_resolution",
    "successful_pathway_requires_new_human_resolution_cycle",
    "no_runtime_action_recommended",
]

INPUT_REQUIRED_FIELDS = [
    "blocked_pathway_phase_freeze_input_id",
    "blocked_pathway_phase_freeze_input_type",
    "blocked_pathway_phase_freeze_input_version",
    "generated_at",
    "source_post_reexecution_verification_not_available_packet_path",
    "source_reexecution_execution_blocked_result_path",
    "source_reexecution_request_packet_path",
    "source_final_gate_rerun_execution_blocked_result_path",
    "source_final_gate_rerun_request_packet_path",
    "source_human_resolution_completeness_gate_path",
    "source_explicit_human_resolution_record_path",
    "source_human_resolution_provided_packet_path",
    "source_human_resolution_input_packet_path",
    "source_explicit_selected_candidate_artifact_path",
    "source_explicit_operator_signoff_artifact_path",
    "candidate_option_refs",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "requested_blocked_pathway_phase_freeze_status",
    "source_contract_refs",
    "source_artifact_refs",
    "source_status_snapshot",
    "warnings",
    "non_claims",
]
FREEZE_REQUIRED_FIELDS = [
    "blocked_pathway_phase_freeze_id",
    "blocked_pathway_phase_freeze_type",
    "blocked_pathway_phase_freeze_version",
    "generated_at",
    "source_blocked_pathway_phase_freeze_input_path",
    *INPUT_REQUIRED_FIELDS[4:15],
    "candidate_option_refs",
    "candidate_option_count",
    "blocked_pathway_phase_freeze_status",
    "blocked_pathway_freeze_reason",
    "blocked_pathway_completion_status",
    "successful_pathway_completion_status",
    "successful_calibration_application_status",
    "human_resolution_status",
    "operator_signoff_status",
    "selected_candidate_status",
    "final_gate_rerun_status",
    "final_gate_rerun_result_status",
    "reexecution_status",
    "reexecution_result_status",
    "post_reexecution_verification_status",
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
    "blocked_pathway_completion_summary",
    "unresolved_human_inputs_report",
    "runtime_non_mutation_evidence_report",
    "successful_pathway_remaining_work_report",
    "future_unblock_readiness_report",
    "next_action_recommendation",
    "source_contract_refs",
    "source_artifact_refs",
    "warnings",
    "non_claims",
]
BLOCKED_PATHWAY_COMPLETION_SUMMARY_REQUIRED_FIELDS = [
    "blocked_pathway_completion_summary_id",
    "blocked_pathway_completion_summary_type",
    "blocked_pathway_completion_summary_version",
    "generated_at",
    "source_blocked_pathway_phase_freeze_id",
    "source_post_reexecution_verification_not_available_packet_id",
    "blocked_pathway_phase_freeze_completed",
    "blocked_pathway_completion_status",
    "successful_pathway_completion_status",
    "successful_calibration_application_status",
    "complete_for_blocked_pathway",
    "successful_runtime_calibration_not_completed",
    "runtime_config_changed",
    "mutation_status",
    "summary_items",
    "summary_item_count",
    "warnings",
    "non_claims",
]
UNRESOLVED_HUMAN_INPUTS_REPORT_REQUIRED_FIELDS = [
    "unresolved_human_inputs_report_id",
    "unresolved_human_inputs_report_type",
    "unresolved_human_inputs_report_version",
    "generated_at",
    "source_blocked_pathway_phase_freeze_id",
    "source_post_reexecution_verification_not_available_packet_id",
    "explicit_human_resolution_provided",
    "operator_signoff_provided",
    "selected_candidate_supplied",
    "final_gate_rerun_performed",
    "runtime_reexecution_performed",
    "unresolved_items",
    "unresolved_item_count",
    "warnings",
    "non_claims",
]
RUNTIME_NON_MUTATION_EVIDENCE_REPORT_REQUIRED_FIELDS = [
    "runtime_non_mutation_evidence_report_id",
    "runtime_non_mutation_evidence_report_type",
    "runtime_non_mutation_evidence_report_version",
    "generated_at",
    "source_blocked_pathway_phase_freeze_id",
    "source_post_reexecution_verification_not_available_packet_id",
    "runtime_application_command_not_executed",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "mutation_status",
    "model_asset_sha_unchanged",
    "protected_baselines_not_replaced",
    "production_config_not_created",
    "baseline_update_status",
    "model_update_status",
    "non_mutation_items",
    "non_mutation_item_count",
    "warnings",
    "non_claims",
]
SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_REQUIRED_FIELDS = [
    "successful_pathway_remaining_work_report_id",
    "successful_pathway_remaining_work_report_type",
    "successful_pathway_remaining_work_report_version",
    "generated_at",
    "source_blocked_pathway_phase_freeze_id",
    "source_post_reexecution_verification_not_available_packet_id",
    "successful_pathway_completion_status",
    "successful_calibration_application_status",
    "successful_runtime_calibration_not_completed",
    "remaining_work_items",
    "remaining_work_item_count",
    "warnings",
    "non_claims",
]
FUTURE_UNBLOCK_READINESS_REPORT_REQUIRED_FIELDS = [
    "future_unblock_readiness_report_id",
    "future_unblock_readiness_report_type",
    "future_unblock_readiness_report_version",
    "generated_at",
    "source_blocked_pathway_phase_freeze_id",
    "source_post_reexecution_verification_not_available_packet_id",
    "future_unblock_readiness_status",
    "ready_to_start_new_human_resolution_cycle",
    "ready_for_runtime_application",
    "runtime_config_changed",
    "mutation_status",
    "required_next_steps",
    "required_next_step_count",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "blocked_pathway_phase_freeze_is_not_truth": True,
    "blocked_pathway_phase_freeze_is_not_accuracy_scoring": True,
    "blocked_pathway_phase_freeze_is_not_model_training": True,
    "blocked_pathway_phase_freeze_is_not_runtime_application": True,
    "blocked_pathway_phase_freeze_does_not_execute_runtime_application": True,
    "blocked_pathway_phase_freeze_does_not_create_production_config": True,
    "blocked_pathway_phase_freeze_does_not_modify_model_weights": True,
    "blocked_pathway_phase_freeze_does_not_replace_baselines": True,
    "blocked_pathway_phase_freeze_does_not_infer_operator_signoff": True,
    "blocked_pathway_phase_freeze_does_not_infer_candidate_selection": True,
    "blocked_pathway_phase_freeze_does_not_infer_human_resolution": True,
    "blocked_pathway_phase_freeze_does_not_infer_final_gate_result": True,
    "blocked_pathway_phase_freeze_does_not_infer_runtime_reexecution_output": True,
    "successful_runtime_calibration_not_completed": True,
    "human_resolution_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
    "operator_signoff_must_be_explicit": True,
    "final_gate_result_must_be_explicit": True,
    "runtime_reexecution_output_must_be_explicit": True,
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
    "final_gate_rerun_required_before_reexecution": True,
    "runtime_reexecution_required_before_post_verification": True,
}
WARNINGS = {
    "controlled_runtime_calibration_blocked_pathway_phase_freeze": True,
    "blocked_pathway_phase_freeze_completed": True,
    "complete_for_blocked_pathway": True,
    "successful_pathway_not_completed": True,
    "incomplete_pending_explicit_human_resolution": True,
    "controlled_pathway_blocked_missing_human_resolution": True,
    "runtime_application_not_executed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "post_reexecution_verification_not_available": True,
    "final_gate_rerun_not_performed": True,
    "reexecution_not_performed": True,
    "classifier_correctness_not_assessed": True,
    **NON_CLAIMS,
}
FORBIDDEN_BLOCKED_PATHWAY_PHASE_FREEZE_TOKENS = {
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
    "true_gameplay",
    "false_gameplay",
    "confirmed_gameplay",
    "point_truth",
    "event_truth",
    "rally_truth",
    "line_call_truth",
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "training_truth",
    "model_ready_truth",
    "generalization_proven",
    "production_ready_truth",
    "classifier_accuracy_claim",
    "accuracy",
    "precision",
    "recall",
    "f1",
    "auc",
    "reviewer_score",
    "reviewer_rank",
    "reviewer_quality",
    "model_updated",
    "model_weights_modified",
    "baseline_replaced",
    "auto_approved",
    "auto_rejected",
    "production_config_created",
    "uncontrolled_runtime_config_update",
    "runtime_application_without_final_gate",
    "runtime_application_without_rollback_package",
    "runtime_application_without_post_apply_verification",
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
    "fake_runtime_reexecution_output",
    "inferred_runtime_reexecution_output",
    "fake_post_reexecution_verification",
    "inferred_post_reexecution_verification",
    "runtime_application_success_without_final_gate_rerun",
    "successful_calibration_completed_without_human_resolution",
}


def export_controlled_runtime_calibration_blocked_pathway_phase_freeze_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_EXPORTED_AT
    )
    contract = {
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_TYPE,  # noqa: E501
        "contract_version": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_VERSION,  # noqa: E501
        "exported_at": exported_at.isoformat(),
        "blocked_pathway_phase_freeze_scope": {
            "creates_blocked_pathway_phase_freeze": True,
            "bp77_post_reexecution_verification_not_available_packet_is_authoritative_source": True,  # noqa: E501
            "freezes_blocked_pathway_only": True,
            "blocked_pathway_complete_for_blocked_purpose": True,
            "successful_runtime_calibration_not_completed": True,
            "human_resolution_required_for_successful_pathway": True,
            "single_candidate_option_does_not_create_selection": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_infer_human_resolution": True,
            "does_not_infer_final_gate_result": True,
            "does_not_infer_reexecution_approval": True,
            "does_not_infer_runtime_reexecution_output": True,
            "does_not_infer_post_reexecution_verification": True,
            "does_not_execute_runtime_reexecution": True,
            "does_not_execute_runtime_application": True,
            "does_not_write_runtime_config": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "blocked_pathway_phase_freeze_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUT_TYPE,  # noqa: E501
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUT_VERSION
            ),
            "required_fields": list(INPUT_REQUIRED_FIELDS),
        },
        "blocked_pathway_phase_freeze_schema": {
            "freeze_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_TYPE,  # noqa: E501
            "freeze_version": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
            ),
            "required_fields": list(FREEZE_REQUIRED_FIELDS),
            "allowed_blocked_pathway_phase_freeze_statuses": list(
                ALLOWED_BLOCKED_PATHWAY_PHASE_FREEZE_STATUSES
            ),
            "allowed_blocked_pathway_completion_statuses": list(
                ALLOWED_BLOCKED_PATHWAY_COMPLETION_STATUSES
            ),
            "allowed_successful_pathway_completion_statuses": list(
                ALLOWED_SUCCESSFUL_PATHWAY_COMPLETION_STATUSES
            ),
            "allowed_next_action_recommendations": list(
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS
            ),
        },
        "blocked_pathway_completion_summary_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_COMPLETION_SUMMARY_TYPE,  # noqa: E501
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION,  # noqa: E501
            "required_fields": list(BLOCKED_PATHWAY_COMPLETION_SUMMARY_REQUIRED_FIELDS),
        },
        "unresolved_human_inputs_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_UNRESOLVED_HUMAN_INPUTS_REPORT_TYPE,  # noqa: E501
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION,  # noqa: E501
            "required_fields": list(UNRESOLVED_HUMAN_INPUTS_REPORT_REQUIRED_FIELDS),
        },
        "runtime_non_mutation_evidence_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_TYPE
            ),
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION,  # noqa: E501
            "required_fields": list(RUNTIME_NON_MUTATION_EVIDENCE_REPORT_REQUIRED_FIELDS),
        },
        "successful_pathway_remaining_work_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_TYPE,  # noqa: E501
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION,  # noqa: E501
            "required_fields": list(
                SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_REQUIRED_FIELDS
            ),
        },
        "future_unblock_readiness_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FUTURE_UNBLOCK_READINESS_REPORT_TYPE,  # noqa: E501
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION,  # noqa: E501
            "required_fields": list(FUTURE_UNBLOCK_READINESS_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_phase_freeze_input_shape": True,
            "validate_phase_freeze_artifact_shape": True,
            "validate_blocked_pathway_completion_summary_shape": True,
            "validate_unresolved_human_inputs_report_shape": True,
            "validate_runtime_non_mutation_evidence_report_shape": True,
            "validate_successful_pathway_remaining_work_report_shape": True,
            "validate_future_unblock_readiness_report_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_successful_pathway_is_not_marked_complete": True,
            "validate_blocked_pathway_complete_only_when_bp77_is_freeze_ready": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_single_candidate_option": True,
            "validate_no_final_gate_rerun_result_is_inferred": True,
            "validate_no_runtime_reexecution_output_is_inferred": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_phase_freeze_evidence_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_auto_label_segments": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp77_post_reexecution_verification_not_available_packet_path_required": True,  # noqa: E501
            "bp76_reexecution_execution_blocked_result_path_preserved": True,
            "bp75_reexecution_request_packet_path_preserved": True,
            "bp74_final_gate_rerun_execution_blocked_result_path_preserved": True,
            "bp73_final_gate_rerun_request_packet_path_preserved": True,
            "bp72_human_resolution_completeness_gate_path_preserved": True,
            "bp71_explicit_human_resolution_record_path_preserved": True,
            "bp70_human_resolution_provided_packet_path_preserved": True,
            "bp69_human_resolution_input_packet_path_preserved": True,
            "bp68_selected_candidate_artifact_path_preserved": True,
            "bp67_signoff_artifact_path_preserved": True,
            "candidate_options_preserved_as_inventory": True,
            "runtime_config_hashes_preserved": True,
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


def build_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    source_post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    source_post_reexecution_verification_not_available_packet_contract_path: str | Path = (  # noqa: E501
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    source = _load_json(source_post_reexecution_verification_not_available_packet_path)
    model_asset_ref = source.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = source.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    runtime_target_ref = _dict(source.get("runtime_config_target_ref"))
    runtime_target_path = runtime_target_ref.get("path")
    runtime_sha_after = (
        _sha256_file(Path(runtime_target_path))
        if runtime_target_path
        else source.get("runtime_config_target_sha256_after")
    )
    freeze_status = _blocked_pathway_phase_freeze_status(source)
    inputs = {
        "blocked_pathway_phase_freeze_input_id": _stable_id(
            "controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs_v1",
            source.get("post_reexecution_verification_not_available_packet_id"),
            source.get("post_reexecution_verification_status"),
            freeze_status,
            source.get("runtime_config_target_sha256_before"),
            runtime_sha_after,
        ),
        "blocked_pathway_phase_freeze_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUT_TYPE
        ),
        "blocked_pathway_phase_freeze_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_path": str(
            Path(source_post_reexecution_verification_not_available_packet_path)
        ),
        **_source_paths_from_bp77_packet(source),
        "candidate_option_refs": _list(source.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": runtime_target_ref,
        "runtime_config_target_sha256_before": source.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": runtime_sha_after,
        "requested_blocked_pathway_phase_freeze_status": freeze_status,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_post_reexecution_verification_not_available_packet_path,
            source_post_reexecution_verification_not_available_packet_contract_path,
            source,
        ),
        "source_status_snapshot": _status_snapshot_from_bp77_packet(source),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_phase_freeze_inputs",
        "blocked_pathway_phase_freeze_input_id": inputs[
            "blocked_pathway_phase_freeze_input_id"
        ],
        **_input_status_snapshot(inputs),
        "candidate_option_count": len(inputs["candidate_option_refs"]),
        "next_action_recommendation": _next_actions_from_bp77_packet(source),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(blocked_pathway_phase_freeze_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    validation = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_blocked_pathway_phase_freeze_inputs_validation"
        ),
        payload_path=blocked_pathway_phase_freeze_inputs_path,
        payload_type=inputs.get("blocked_pathway_phase_freeze_input_type"),
        payload_version=inputs.get("blocked_pathway_phase_freeze_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_input_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, validation)
    return validation


def build_controlled_runtime_calibration_blocked_pathway_phase_freeze(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(blocked_pathway_phase_freeze_inputs_path)
    source = _source_bp77_packet(inputs)
    freeze_status = _blocked_pathway_phase_freeze_status(source)
    completion_status = _blocked_pathway_completion_status(source)
    successful_status = _successful_pathway_completion_status(source)
    application_status = _successful_calibration_application_status(source)
    freeze_id = _stable_id(
        "controlled_runtime_calibration_blocked_pathway_phase_freeze_v1",
        inputs.get("blocked_pathway_phase_freeze_input_id"),
        source.get("post_reexecution_verification_not_available_packet_id"),
        freeze_status,
        completion_status,
        successful_status,
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    freeze = {
        "blocked_pathway_phase_freeze_id": freeze_id,
        "blocked_pathway_phase_freeze_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_TYPE
        ),
        "blocked_pathway_phase_freeze_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_input_path": str(
            Path(blocked_pathway_phase_freeze_inputs_path)
        ),
        "source_post_reexecution_verification_not_available_packet_path": inputs.get(
            "source_post_reexecution_verification_not_available_packet_path"
        ),
        **_source_paths_from_inputs(inputs),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "blocked_pathway_phase_freeze_status": freeze_status,
        "blocked_pathway_freeze_reason": "controlled_pathway_blocked_missing_human_resolution",  # noqa: E501
        "blocked_pathway_completion_status": completion_status,
        "successful_pathway_completion_status": successful_status,
        "successful_calibration_application_status": application_status,
        "human_resolution_status": _human_resolution_status(source),
        "operator_signoff_status": source.get("operator_signoff_status"),
        "selected_candidate_status": source.get("selected_candidate_status"),
        "final_gate_rerun_status": _final_gate_rerun_status(source),
        "final_gate_rerun_result_status": source.get("final_gate_rerun_result_status"),
        "reexecution_status": _reexecution_status(source),
        "reexecution_result_status": source.get("reexecution_result_status"),
        "post_reexecution_verification_status": source.get(
            "post_reexecution_verification_status"
        ),
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
        "blocked_pathway_completion_summary": _blocked_pathway_completion_summary(
            freeze_id,
            source,
            freeze_status,
            completion_status,
            successful_status,
            application_status,
            generated_at,
        ),
        "unresolved_human_inputs_report": _unresolved_human_inputs_report(
            freeze_id,
            source,
            generated_at,
        ),
        "runtime_non_mutation_evidence_report": _runtime_non_mutation_evidence_report(
            freeze_id,
            source,
            inputs,
            generated_at,
        ),
        "successful_pathway_remaining_work_report": (
            _successful_pathway_remaining_work_report(
                freeze_id,
                source,
                successful_status,
                application_status,
                generated_at,
            )
        ),
        "future_unblock_readiness_report": _future_unblock_readiness_report(
            freeze_id,
            source,
            generated_at,
        ),
        "next_action_recommendation": _next_actions_from_bp77_packet(source),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    errors.extend(_validate_freeze_shape(freeze))
    _write_json_if_requested(output_path, freeze)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_phase_freeze",
        "blocked_pathway_phase_freeze_id": freeze_id,
        **_freeze_status_snapshot(freeze),
        "candidate_option_count": freeze["candidate_option_count"],
        "next_action_recommendation": freeze["next_action_recommendation"],
        "blocked_pathway_phase_freeze_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_blocked_pathway_phase_freeze(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    freeze = _load_json(blocked_pathway_phase_freeze_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_freeze_shape(freeze))
    validation = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_blocked_pathway_phase_freeze_validation"
        ),
        payload_path=blocked_pathway_phase_freeze_path,
        payload_type=freeze.get("blocked_pathway_phase_freeze_type"),
        payload_version=freeze.get("blocked_pathway_phase_freeze_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_freeze_status_snapshot(freeze),
    )
    _write_json_if_requested(output_path, validation)
    return validation


def build_controlled_runtime_calibration_blocked_pathway_completion_summary(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_COMPLETION_SUMMARY_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        freeze_path=blocked_pathway_phase_freeze_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="blocked_pathway_completion_summary",
        report_validator=_validate_blocked_pathway_completion_summary_shape,
        output_key="blocked_pathway_completion_summary_output",
    )


def build_controlled_runtime_calibration_unresolved_human_inputs_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_UNRESOLVED_HUMAN_INPUTS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        freeze_path=blocked_pathway_phase_freeze_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="unresolved_human_inputs_report",
        report_validator=_validate_unresolved_human_inputs_report_shape,
        output_key="unresolved_human_inputs_report_output",
    )


def build_controlled_runtime_calibration_runtime_non_mutation_evidence_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        freeze_path=blocked_pathway_phase_freeze_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="runtime_non_mutation_evidence_report",
        report_validator=_validate_runtime_non_mutation_evidence_report_shape,
        output_key="runtime_non_mutation_evidence_report_output",
    )


def build_controlled_runtime_calibration_successful_pathway_remaining_work_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        freeze_path=blocked_pathway_phase_freeze_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="successful_pathway_remaining_work_report",
        report_validator=_validate_successful_pathway_remaining_work_report_shape,
        output_key="successful_pathway_remaining_work_report_output",
    )


def build_controlled_runtime_calibration_future_unblock_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_OUTPUT
    ),
    blocked_pathway_phase_freeze_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FUTURE_UNBLOCK_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        freeze_path=blocked_pathway_phase_freeze_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="future_unblock_readiness_report",
        report_validator=_validate_future_unblock_readiness_report_shape,
        output_key="future_unblock_readiness_report_output",
    )


def _export_embedded_report(
    *,
    contract_path: str | Path,
    freeze_path: str | Path,
    output_path: str | Path | None,
    generated_at: datetime | None,
    report_key: str,
    report_validator: Any,
    output_key: str,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    freeze = _load_json(freeze_path)
    report = {
        **_dict(freeze.get(report_key)),
        "exported_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_path": str(Path(freeze_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_freeze_shape(freeze))
    errors.extend(report_validator(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else f"invalid_{report_key}",
        "blocked_pathway_phase_freeze_id": freeze.get(
            "blocked_pathway_phase_freeze_id"
        ),
        **_freeze_status_snapshot(freeze),
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
        "post_reexecution_verification_not_available_packet": _artifact_ref(
            packet_path,
            packet,
        ),
        "post_reexecution_verification_not_available_packet_contract": _artifact_ref(
            packet_contract_path,
            _load_json_if_exists(packet_contract_path),
        ),
    }
    refs.update(_dict(packet.get("source_artifact_refs")))
    return refs


def _source_bp77_packet(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(
        inputs.get("source_post_reexecution_verification_not_available_packet_path")
    )


def _source_paths_from_bp77_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_reexecution_execution_blocked_result_path": packet.get(
            "source_reexecution_execution_blocked_result_path"
        ),
        "source_reexecution_request_packet_path": packet.get(
            "source_reexecution_request_packet_path"
        ),
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
    }


def _source_paths_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        key: inputs.get(key)
        for key in INPUT_REQUIRED_FIELDS
        if key.startswith("source_")
        and key.endswith("_path")
        and key != "source_post_reexecution_verification_not_available_packet_path"
    }


def _bp77_ready_to_freeze(packet: dict[str, Any]) -> bool:
    report = _dict(packet.get("phase_freeze_readiness_report"))
    return (
        packet.get("post_reexecution_verification_status")
        == "post_reexecution_verification_not_available"
        and report.get("ready_to_freeze_blocked_pathway") is True
        and report.get("phase_freeze_recommended_status") == "blocked_pathway_freeze_ready"
        and packet.get("runtime_config_changed") is False
        and packet.get("mutation_status") == "no_runtime_mutation_due_to_blocker"
    )


def _blocked_pathway_phase_freeze_status(packet: dict[str, Any]) -> str:
    if _bp77_ready_to_freeze(packet):
        return "blocked_pathway_phase_freeze_completed"
    return "blocked_pathway_phase_freeze_blocked_missing_source_artifacts"


def _blocked_pathway_completion_status(packet: dict[str, Any]) -> str:
    if _bp77_ready_to_freeze(packet):
        return "complete_for_blocked_pathway"
    return "incomplete_missing_blocked_evidence"


def _successful_pathway_completion_status(packet: dict[str, Any]) -> str:
    if packet.get("human_resolution_completeness_status") != "human_resolution_complete":
        return "incomplete_pending_explicit_human_resolution"
    if packet.get("final_gate_rerun_result_status") == "final_gate_rerun_result_not_available":
        return "incomplete_pending_final_gate_rerun"
    if packet.get("reexecution_result_status") == "reexecution_result_not_available":
        return "incomplete_pending_runtime_reexecution"
    if (
        packet.get("post_reexecution_verification_status")
        == "post_reexecution_verification_not_available"
    ):
        return "incomplete_pending_post_reexecution_verification"
    return "complete_successful_runtime_calibration"


def _successful_calibration_application_status(packet: dict[str, Any]) -> str:
    if _successful_pathway_completion_status(packet) == "complete_successful_runtime_calibration":
        return "completed_structural_only"
    return "not_completed"


def _human_resolution_status(packet: dict[str, Any]) -> str:
    if packet.get("human_resolution_completeness_status") == "human_resolution_complete":
        return "human_resolution_provided"
    return "human_resolution_missing"


def _final_gate_rerun_status(packet: dict[str, Any]) -> str:
    if packet.get("final_gate_rerun_outcome_status") == "final_gate_rerun_not_performed":
        return "final_gate_rerun_not_performed"
    return "final_gate_rerun_performed_structural_only"


def _reexecution_status(packet: dict[str, Any]) -> str:
    if packet.get("reexecution_outcome_status") == "reexecution_not_performed":
        return "reexecution_not_performed"
    return "reexecution_performed_structural_only"


def _status_snapshot_from_bp77_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "post_reexecution_verification_status": packet.get(
            "post_reexecution_verification_status"
        ),
        "post_reexecution_result_status": packet.get("post_reexecution_result_status"),
        "post_reexecution_outcome_status": packet.get("post_reexecution_outcome_status"),
        "final_gate_rerun_result_status": packet.get("final_gate_rerun_result_status"),
        "final_gate_rerun_outcome_status": packet.get("final_gate_rerun_outcome_status"),
        "reexecution_result_status": packet.get("reexecution_result_status"),
        "reexecution_outcome_status": packet.get("reexecution_outcome_status"),
        "human_resolution_completeness_status": packet.get(
            "human_resolution_completeness_status"
        ),
        "missing_input_status": packet.get("missing_input_status"),
        "operator_signoff_status": packet.get("operator_signoff_status"),
        "selected_candidate_status": packet.get("selected_candidate_status"),
        "runtime_application_status": packet.get("runtime_application_status"),
        "runtime_config_changed": packet.get("runtime_config_changed"),
        "mutation_status": packet.get("mutation_status"),
        "production_config_status": packet.get("production_config_status"),
        "baseline_update_status": packet.get("baseline_update_status"),
        "model_update_status": packet.get("model_update_status"),
    }


def _input_status_snapshot(inputs: dict[str, Any]) -> dict[str, Any]:
    packet = _source_bp77_packet(inputs)
    return {
        "blocked_pathway_phase_freeze_status": (
            _blocked_pathway_phase_freeze_status(packet)
        ),
        "blocked_pathway_freeze_reason": (
            "controlled_pathway_blocked_missing_human_resolution"
        ),
        "blocked_pathway_completion_status": _blocked_pathway_completion_status(packet),
        "successful_pathway_completion_status": (
            _successful_pathway_completion_status(packet)
        ),
        "successful_calibration_application_status": (
            _successful_calibration_application_status(packet)
        ),
        "human_resolution_status": _human_resolution_status(packet),
        "operator_signoff_status": packet.get("operator_signoff_status"),
        "selected_candidate_status": packet.get("selected_candidate_status"),
        "final_gate_rerun_status": _final_gate_rerun_status(packet),
        "final_gate_rerun_result_status": packet.get("final_gate_rerun_result_status"),
        "reexecution_status": _reexecution_status(packet),
        "reexecution_result_status": packet.get("reexecution_result_status"),
        "post_reexecution_verification_status": packet.get(
            "post_reexecution_verification_status"
        ),
        "runtime_application_status": "not_executed",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
    }


def _blocked_pathway_completion_summary(
    freeze_id: str,
    packet: dict[str, Any],
    freeze_status: str,
    completion_status: str,
    successful_status: str,
    application_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    items = [
        _item("bp77_not_available_packet_exists", True, packet.get(
            "post_reexecution_verification_not_available_packet_id"
        )),
        _item("bp77_phase_freeze_ready", _bp77_ready_to_freeze(packet), "blocked_pathway_freeze_ready"),  # noqa: E501
        _item("blocked_pathway_phase_freeze_completed", freeze_status == "blocked_pathway_phase_freeze_completed", freeze_status),  # noqa: E501
        _item("successful_runtime_calibration_not_completed", application_status == "not_completed", application_status),  # noqa: E501
        _item("runtime_config_changed_false", True, False),
    ]
    return {
        "blocked_pathway_completion_summary_id": _stable_id(
            "controlled_runtime_calibration_blocked_pathway_completion_summary_v1",
            freeze_id,
            completion_status,
            successful_status,
        ),
        "blocked_pathway_completion_summary_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_COMPLETION_SUMMARY_TYPE
        ),
        "blocked_pathway_completion_summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_id": freeze_id,
        "source_post_reexecution_verification_not_available_packet_id": packet.get(
            "post_reexecution_verification_not_available_packet_id"
        ),
        "blocked_pathway_phase_freeze_completed": (
            freeze_status == "blocked_pathway_phase_freeze_completed"
        ),
        "blocked_pathway_completion_status": completion_status,
        "successful_pathway_completion_status": successful_status,
        "successful_calibration_application_status": application_status,
        "complete_for_blocked_pathway": completion_status == "complete_for_blocked_pathway",
        "successful_runtime_calibration_not_completed": application_status == "not_completed",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "summary_items": items,
        "summary_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _unresolved_human_inputs_report(
    freeze_id: str,
    packet: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    items = [
        _item("missing_explicit_human_resolution", True, packet.get(
            "human_resolution_completeness_status"
        )),
        _item("missing_explicit_operator_signoff", True, packet.get(
            "operator_signoff_status"
        )),
        _item("missing_explicit_selected_candidate", True, packet.get(
            "selected_candidate_status"
        )),
        _item("final_gate_rerun_not_performed", True, packet.get(
            "final_gate_rerun_outcome_status"
        )),
        _item("runtime_reexecution_not_performed", True, packet.get(
            "reexecution_outcome_status"
        )),
    ]
    return {
        "unresolved_human_inputs_report_id": _stable_id(
            "controlled_runtime_calibration_unresolved_human_inputs_report_v1",
            freeze_id,
            packet.get("missing_input_status"),
            packet.get("operator_signoff_status"),
            packet.get("selected_candidate_status"),
        ),
        "unresolved_human_inputs_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_UNRESOLVED_HUMAN_INPUTS_REPORT_TYPE
        ),
        "unresolved_human_inputs_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_id": freeze_id,
        "source_post_reexecution_verification_not_available_packet_id": packet.get(
            "post_reexecution_verification_not_available_packet_id"
        ),
        "explicit_human_resolution_provided": False,
        "operator_signoff_provided": False,
        "selected_candidate_supplied": False,
        "final_gate_rerun_performed": False,
        "runtime_reexecution_performed": False,
        "unresolved_items": items,
        "unresolved_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _runtime_non_mutation_evidence_report(
    freeze_id: str,
    packet: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    runtime_sha_unchanged = (
        inputs.get("runtime_config_target_sha256_before")
        == inputs.get("runtime_config_target_sha256_after")
    )
    items = [
        _item("runtime_application_command_not_executed", True, "not_executed"),
        _item(
            "runtime_config_sha_unchanged",
            runtime_sha_unchanged,
            inputs.get("runtime_config_target_sha256_after"),
        ),
        _item("model_asset_sha_unchanged", True, inputs.get("model_asset_sha256")),
        _item("protected_baselines_not_replaced", True, "not_replaced"),
        _item("production_config_not_created", True, "not_created"),
    ]
    return {
        "runtime_non_mutation_evidence_report_id": _stable_id(
            "controlled_runtime_calibration_blocked_pathway_runtime_non_mutation_evidence_report_v1",  # noqa: E501
            freeze_id,
            inputs.get("runtime_config_target_sha256_before"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        "runtime_non_mutation_evidence_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_TYPE
        ),
        "runtime_non_mutation_evidence_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_id": freeze_id,
        "source_post_reexecution_verification_not_available_packet_id": packet.get(
            "post_reexecution_verification_not_available_packet_id"
        ),
        "runtime_application_command_not_executed": True,
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "model_asset_sha_unchanged": True,
        "protected_baselines_not_replaced": True,
        "production_config_not_created": True,
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "non_mutation_items": items,
        "non_mutation_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _successful_pathway_remaining_work_report(
    freeze_id: str,
    packet: dict[str, Any],
    successful_status: str,
    application_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    items = [
        _item("provide_explicit_human_resolution_inputs", True, packet.get(
            "missing_input_status"
        )),
        _item("provide_operator_signoff_and_selected_candidate", True, packet.get(
            "operator_signoff_status"
        )),
        _item("rerun_final_gate_after_human_resolution", True, packet.get(
            "final_gate_rerun_result_status"
        )),
        _item("perform_runtime_reexecution_after_final_gate", True, packet.get(
            "reexecution_result_status"
        )),
        _item("rebuild_post_reexecution_verification_after_runtime_output", True, packet.get(
            "post_reexecution_verification_status"
        )),
    ]
    return {
        "successful_pathway_remaining_work_report_id": _stable_id(
            "controlled_runtime_calibration_successful_pathway_remaining_work_report_v1",
            freeze_id,
            successful_status,
            application_status,
        ),
        "successful_pathway_remaining_work_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_TYPE
        ),
        "successful_pathway_remaining_work_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_id": freeze_id,
        "source_post_reexecution_verification_not_available_packet_id": packet.get(
            "post_reexecution_verification_not_available_packet_id"
        ),
        "successful_pathway_completion_status": successful_status,
        "successful_calibration_application_status": application_status,
        "successful_runtime_calibration_not_completed": application_status == "not_completed",
        "remaining_work_items": items,
        "remaining_work_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _future_unblock_readiness_report(
    freeze_id: str,
    packet: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    steps = [
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_human_resolution",
        "prepare_reexecution_after_final_gate_rerun",
        "prepare_post_reexecution_verification_after_runtime_execution",
    ]
    return {
        "future_unblock_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_future_unblock_readiness_report_v1",
            freeze_id,
            packet.get("missing_input_status"),
            packet.get("post_reexecution_verification_status"),
        ),
        "future_unblock_readiness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FUTURE_UNBLOCK_READINESS_REPORT_TYPE
        ),
        "future_unblock_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_pathway_phase_freeze_id": freeze_id,
        "source_post_reexecution_verification_not_available_packet_id": packet.get(
            "post_reexecution_verification_not_available_packet_id"
        ),
        "future_unblock_readiness_status": (
            "blocked_pending_explicit_human_resolution_cycle"
        ),
        "ready_to_start_new_human_resolution_cycle": True,
        "ready_for_runtime_application": False,
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "required_next_steps": steps,
        "required_next_step_count": len(steps),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _item(item_code: str, satisfied: bool, observed_value: Any) -> dict[str, Any]:
    return {
        "item_code": item_code,
        "satisfied": bool(satisfied),
        "observed_value": observed_value,
    }


def _next_actions_from_bp77_packet(packet: dict[str, Any]) -> list[str]:
    actions = [
        "stop_blocked_calibration_pathway",
        "successful_pathway_requires_new_human_resolution_cycle",
        "no_runtime_action_recommended",
    ]
    if packet.get("operator_signoff_status") != "operator_signoff_provided":
        actions.insert(1, "provide_operator_signoff_and_selected_candidate")
    if packet.get("final_gate_rerun_result_status") == "final_gate_rerun_result_not_available":
        actions.insert(-1, "rerun_final_gate_after_human_resolution")
    return _unique_strings(actions)


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "blocked_pathway_phase_freeze_scope",
        "source_contract_refs",
        "blocked_pathway_phase_freeze_input_schema",
        "blocked_pathway_phase_freeze_schema",
        "blocked_pathway_completion_summary_schema",
        "unresolved_human_inputs_report_schema",
        "runtime_non_mutation_evidence_report_schema",
        "successful_pathway_remaining_work_report_schema",
        "future_unblock_readiness_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, INPUT_REQUIRED_FIELDS, "inputs")
    source = _source_bp77_packet(inputs)
    errors.extend(_validate_source_bp77_packet_shape(source))
    errors.extend(_validate_no_runtime_mutation_fields(inputs))
    expected_status = _blocked_pathway_phase_freeze_status(source)
    if inputs.get("requested_blocked_pathway_phase_freeze_status") != expected_status:
        errors.append(
            _error(
                "requested_blocked_pathway_phase_freeze_status_must_match_bp77_state",
                "requested_blocked_pathway_phase_freeze_status",
                inputs.get("requested_blocked_pathway_phase_freeze_status"),
            )
        )
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_source_bp77_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _validate_bp77_packet_shape(packet)
    required = [
        "post_reexecution_verification_not_available_packet_id",
        "post_reexecution_verification_status",
        "post_reexecution_result_status",
        "post_reexecution_outcome_status",
        "final_gate_rerun_result_status",
        "final_gate_rerun_outcome_status",
        "reexecution_result_status",
        "reexecution_outcome_status",
        "human_resolution_completeness_status",
        "missing_input_status",
        "operator_signoff_status",
        "selected_candidate_status",
        "runtime_application_status",
        "runtime_config_changed",
        "mutation_status",
        "production_config_status",
        "baseline_update_status",
        "model_update_status",
        "phase_freeze_readiness_report",
    ]
    errors.extend(_missing_required(packet, required, "source_bp77_packet"))
    for field, value, allowed in _status_fields_for_bp77_packet(packet):
        errors.extend(_validate_status(field, value, allowed))
    if not _bp77_ready_to_freeze(packet):
        errors.append(
            _error(
                "bp77_packet_must_be_ready_to_freeze_blocked_pathway",
                "phase_freeze_readiness_report",
                packet.get("phase_freeze_readiness_report"),
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
        "runtime_config_target_sha256_after": payload.get(
            "runtime_config_target_sha256_after"
        ),
    }
    return _validate_blocked_runtime_state(runtime_payload)


def _validate_freeze_shape(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(freeze, FREEZE_REQUIRED_FIELDS, "phase_freeze")
    for field, value, allowed in _status_fields_for_freeze(freeze):
        errors.extend(_validate_status(field, value, allowed))
    source = _load_json_if_exists(
        freeze.get("source_post_reexecution_verification_not_available_packet_path")
    )
    expected_status = _blocked_pathway_phase_freeze_status(source)
    if freeze.get("blocked_pathway_phase_freeze_status") != expected_status:
        errors.append(
            _error(
                "blocked_pathway_phase_freeze_status_must_match_bp77_state",
                "blocked_pathway_phase_freeze_status",
                freeze.get("blocked_pathway_phase_freeze_status"),
            )
        )
    if (
        freeze.get("blocked_pathway_phase_freeze_status")
        == "blocked_pathway_phase_freeze_completed"
        and not _bp77_ready_to_freeze(source)
    ):
        errors.append(
            _error(
                "blocked_pathway_phase_freeze_completed_requires_bp77_freeze_ready",
                "blocked_pathway_phase_freeze_status",
                freeze.get("blocked_pathway_phase_freeze_status"),
            )
        )
    if (
        freeze.get("successful_pathway_completion_status")
        == "complete_successful_runtime_calibration"
    ):
        errors.append(
            _error(
                "successful_pathway_must_not_be_marked_complete_in_blocked_state",
                "successful_pathway_completion_status",
                freeze.get("successful_pathway_completion_status"),
            )
        )
    if freeze.get("successful_calibration_application_status") != "not_completed":
        errors.append(
            _error(
                "successful_calibration_application_must_not_be_completed",
                "successful_calibration_application_status",
                freeze.get("successful_calibration_application_status"),
            )
        )
    errors.extend(_validate_no_runtime_mutation_fields(freeze))
    errors.extend(
        _validate_blocked_pathway_completion_summary_shape(
            _dict(freeze.get("blocked_pathway_completion_summary"))
        )
    )
    errors.extend(
        _validate_unresolved_human_inputs_report_shape(
            _dict(freeze.get("unresolved_human_inputs_report"))
        )
    )
    errors.extend(
        _validate_runtime_non_mutation_evidence_report_shape(
            _dict(freeze.get("runtime_non_mutation_evidence_report"))
        )
    )
    errors.extend(
        _validate_successful_pathway_remaining_work_report_shape(
            _dict(freeze.get("successful_pathway_remaining_work_report"))
        )
    )
    errors.extend(
        _validate_future_unblock_readiness_report_shape(
            _dict(freeze.get("future_unblock_readiness_report"))
        )
    )
    errors.extend(_validate_next_actions(_list(freeze.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(freeze.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(freeze))
    return errors


def _validate_blocked_pathway_completion_summary_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        BLOCKED_PATHWAY_COMPLETION_SUMMARY_REQUIRED_FIELDS,
        "blocked_pathway_completion_summary",
    )
    for field in [
        "blocked_pathway_phase_freeze_completed",
        "complete_for_blocked_pathway",
        "successful_runtime_calibration_not_completed",
    ]:
        if report.get(field) is not True:
            errors.append(_error(f"{field}_must_be_true", field, report.get(field)))
    if report.get("runtime_config_changed") is not False:
        errors.append(
            _error(
                "runtime_config_changed_must_remain_false",
                "runtime_config_changed",
                report.get("runtime_config_changed"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_unresolved_human_inputs_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        UNRESOLVED_HUMAN_INPUTS_REPORT_REQUIRED_FIELDS,
        "unresolved_human_inputs_report",
    )
    for field in [
        "explicit_human_resolution_provided",
        "operator_signoff_provided",
        "selected_candidate_supplied",
        "final_gate_rerun_performed",
        "runtime_reexecution_performed",
    ]:
        if report.get(field) is not False:
            errors.append(_error(f"{field}_must_be_false", field, report.get(field)))
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_runtime_non_mutation_evidence_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        RUNTIME_NON_MUTATION_EVIDENCE_REPORT_REQUIRED_FIELDS,
        "runtime_non_mutation_evidence_report",
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
    for field in [
        "runtime_application_command_not_executed",
        "model_asset_sha_unchanged",
        "protected_baselines_not_replaced",
        "production_config_not_created",
    ]:
        if report.get(field) is not True:
            errors.append(_error(f"{field}_must_be_true", field, report.get(field)))
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_successful_pathway_remaining_work_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        SUCCESSFUL_PATHWAY_REMAINING_WORK_REPORT_REQUIRED_FIELDS,
        "successful_pathway_remaining_work_report",
    )
    if report.get("successful_runtime_calibration_not_completed") is not True:
        errors.append(
            _error(
                "successful_runtime_calibration_not_completed_must_be_true",
                "successful_runtime_calibration_not_completed",
                report.get("successful_runtime_calibration_not_completed"),
            )
        )
    if report.get("successful_calibration_application_status") != "not_completed":
        errors.append(
            _error(
                "successful_calibration_application_status_must_remain_not_completed",
                "successful_calibration_application_status",
                report.get("successful_calibration_application_status"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_future_unblock_readiness_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        FUTURE_UNBLOCK_READINESS_REPORT_REQUIRED_FIELDS,
        "future_unblock_readiness_report",
    )
    if report.get("ready_to_start_new_human_resolution_cycle") is not True:
        errors.append(
            _error(
                "ready_to_start_new_human_resolution_cycle_must_be_true",
                "ready_to_start_new_human_resolution_cycle",
                report.get("ready_to_start_new_human_resolution_cycle"),
            )
        )
    if report.get("ready_for_runtime_application") is not False:
        errors.append(
            _error(
                "ready_for_runtime_application_must_be_false",
                "ready_for_runtime_application",
                report.get("ready_for_runtime_application"),
            )
        )
    if report.get("runtime_config_changed") is not False:
        errors.append(
            _error(
                "runtime_config_changed_must_remain_false",
                "runtime_config_changed",
                report.get("runtime_config_changed"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _status_fields_for_bp77_packet(packet: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "post_reexecution_verification_status",
            packet.get("post_reexecution_verification_status"),
            ALLOWED_POST_REEXECUTION_VERIFICATION_STATUSES,
        ),
        (
            "post_reexecution_result_status",
            packet.get("post_reexecution_result_status"),
            ALLOWED_POST_REEXECUTION_RESULT_STATUSES,
        ),
        (
            "post_reexecution_outcome_status",
            packet.get("post_reexecution_outcome_status"),
            ALLOWED_POST_REEXECUTION_OUTCOME_STATUSES,
        ),
        (
            "final_gate_rerun_status",
            _final_gate_rerun_status(packet),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        ),
        (
            "reexecution_status",
            _reexecution_status(packet),
            ALLOWED_REEXECUTION_STATUSES,
        ),
        (
            "reexecution_result_status",
            packet.get("reexecution_result_status"),
            ALLOWED_REEXECUTION_RESULT_STATUSES,
        ),
        (
            "reexecution_outcome_status",
            packet.get("reexecution_outcome_status"),
            ALLOWED_REEXECUTION_OUTCOME_STATUSES,
        ),
        (
            "runtime_application_status",
            packet.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]


def _status_fields_for_freeze(freeze: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "blocked_pathway_phase_freeze_status",
            freeze.get("blocked_pathway_phase_freeze_status"),
            ALLOWED_BLOCKED_PATHWAY_PHASE_FREEZE_STATUSES,
        ),
        (
            "blocked_pathway_completion_status",
            freeze.get("blocked_pathway_completion_status"),
            ALLOWED_BLOCKED_PATHWAY_COMPLETION_STATUSES,
        ),
        (
            "successful_pathway_completion_status",
            freeze.get("successful_pathway_completion_status"),
            ALLOWED_SUCCESSFUL_PATHWAY_COMPLETION_STATUSES,
        ),
        (
            "successful_calibration_application_status",
            freeze.get("successful_calibration_application_status"),
            ALLOWED_SUCCESSFUL_CALIBRATION_APPLICATION_STATUSES,
        ),
        (
            "human_resolution_status",
            freeze.get("human_resolution_status"),
            ALLOWED_HUMAN_RESOLUTION_STATUSES,
        ),
        (
            "operator_signoff_status",
            freeze.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "selected_candidate_status",
            freeze.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "final_gate_rerun_status",
            freeze.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        ),
        (
            "reexecution_status",
            freeze.get("reexecution_status"),
            ALLOWED_REEXECUTION_STATUSES,
        ),
        (
            "reexecution_result_status",
            freeze.get("reexecution_result_status"),
            ALLOWED_REEXECUTION_RESULT_STATUSES,
        ),
        (
            "post_reexecution_verification_status",
            freeze.get("post_reexecution_verification_status"),
            ALLOWED_POST_REEXECUTION_VERIFICATION_STATUSES,
        ),
        (
            "runtime_application_status",
            freeze.get("runtime_application_status"),
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
    for required in [
        "stop_blocked_calibration_pathway",
        "successful_pathway_requires_new_human_resolution_cycle",
    ]:
        if required not in recommendations:
            errors.append(
                _error("missing_required_next_action", "next_action_recommendation", required)
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
            if key in FORBIDDEN_BLOCKED_PATHWAY_PHASE_FREEZE_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in (
        FORBIDDEN_BLOCKED_PATHWAY_PHASE_FREEZE_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _freeze_status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "blocked_pathway_phase_freeze_status",
        "blocked_pathway_freeze_reason",
        "blocked_pathway_completion_status",
        "successful_pathway_completion_status",
        "successful_calibration_application_status",
        "human_resolution_status",
        "operator_signoff_status",
        "selected_candidate_status",
        "final_gate_rerun_status",
        "final_gate_rerun_result_status",
        "reexecution_status",
        "reexecution_result_status",
        "post_reexecution_verification_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_VERSION
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_BLUEPRINT,  # noqa: E501
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_PATHWAY_PHASE_FREEZE_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_77",
        "scope": "controlled_runtime_calibration_blocked_pathway_phase_freeze",
        "runtime_boundary": "no_runtime_reexecution_or_application_or_config_mutation",
    }
