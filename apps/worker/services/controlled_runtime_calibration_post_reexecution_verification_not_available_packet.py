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
)
from apps.worker.services.controlled_runtime_calibration_reexecution_execution_blocked_result import (  # noqa: E501
    ALLOWED_REEXECUTION_EXECUTION_STATUSES,
    ALLOWED_REEXECUTION_OUTCOME_STATUSES,
    ALLOWED_REEXECUTION_RESULT_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT,
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
from apps.worker.services.controlled_runtime_calibration_reexecution_execution_blocked_result import (  # noqa: E501
    SOURCE_CONTRACT_REFS as BP76_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.controlled_runtime_calibration_reexecution_request_packet import (
    ALLOWED_REEXECUTION_READINESS_STATUSES,
    ALLOWED_REEXECUTION_REQUEST_STATUSES,
    ALLOWED_RUNTIME_APPLICATION_STATUSES,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_VERSION = "v1"  # noqa: E501
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUT_TYPE = (
    "controlled_runtime_calibration_post_reexecution_verification_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION = "v1"  # noqa: E501
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_AVAILABILITY_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_verification_availability_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_MISSING_EXECUTION_EVIDENCE_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_missing_execution_evidence_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_runtime_non_mutation_evidence_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_final_gate_dependency_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_PHASE_FREEZE_READINESS_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_post_reexecution_phase_freeze_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_BLUEPRINT = "blueprint_77"
CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_verification_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_verification_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_AVAILABILITY_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_verification_availability_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_MISSING_EXECUTION_EVIDENCE_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_missing_execution_evidence_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_runtime_non_mutation_evidence_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_final_gate_dependency_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_PHASE_FREEZE_READINESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_post_reexecution_phase_freeze_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_EXPORTED_AT = (
    datetime(2026, 6, 22, 0, 0, tzinfo=UTC)
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_reexecution_execution_blocked_result_contract_version": "v1",
    **dict(BP76_SOURCE_CONTRACT_REFS),
}

ALLOWED_POST_REEXECUTION_VERIFICATION_STATUSES = [
    "post_reexecution_verification_not_available",
    "post_reexecution_verification_blocked_runtime_reexecution_not_performed",
    "post_reexecution_verification_blocked_missing_final_gate_result",
    "post_reexecution_verification_blocked_missing_human_resolution",
    "post_reexecution_verification_ready_after_runtime_reexecution",
    "post_reexecution_verification_completed_structural_only",
    "post_reexecution_verification_informational_only",
    "not_applicable",
]
ALLOWED_POST_REEXECUTION_RESULT_STATUSES = [
    "post_reexecution_result_not_available",
    "post_reexecution_result_blocked",
    "post_reexecution_result_deferred",
    "post_reexecution_result_structural_only",
    "not_applicable",
]
ALLOWED_POST_REEXECUTION_OUTCOME_STATUSES = [
    "post_reexecution_not_verified",
    "post_reexecution_verification_blocked",
    "post_reexecution_verification_deferred",
    "post_reexecution_verification_structural_only",
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
    "prepare_controlled_calibration_phase_freeze_blocked",
    "no_runtime_action_recommended",
    "not_applicable",
]

INPUT_REQUIRED_FIELDS = [
    "post_reexecution_verification_input_id",
    "post_reexecution_verification_input_type",
    "post_reexecution_verification_input_version",
    "generated_at",
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
    "requested_post_reexecution_verification_status",
    "source_contract_refs",
    "source_artifact_refs",
    "source_status_snapshot",
    "warnings",
    "non_claims",
]
PACKET_REQUIRED_FIELDS = [
    "post_reexecution_verification_not_available_packet_id",
    "post_reexecution_verification_not_available_packet_type",
    "post_reexecution_verification_not_available_packet_version",
    "generated_at",
    "source_post_reexecution_verification_input_path",
    *INPUT_REQUIRED_FIELDS[4:23],
    "candidate_option_refs",
    "candidate_option_count",
    "post_reexecution_verification_status",
    "post_reexecution_verification_reason",
    "post_reexecution_result_status",
    "post_reexecution_outcome_status",
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
    "verification_availability_report",
    "missing_execution_evidence_report",
    "runtime_non_mutation_evidence_report",
    "final_gate_dependency_report",
    "phase_freeze_readiness_report",
    "next_action_recommendation",
    "source_contract_refs",
    "source_artifact_refs",
    "warnings",
    "non_claims",
]
VERIFICATION_AVAILABILITY_REPORT_REQUIRED_FIELDS = [
    "verification_availability_report_id",
    "verification_availability_report_type",
    "verification_availability_report_version",
    "generated_at",
    "source_post_reexecution_verification_not_available_packet_id",
    "source_reexecution_execution_blocked_result_id",
    "runtime_reexecution_not_performed",
    "reexecution_result_not_available",
    "runtime_application_not_executed",
    "post_reexecution_verification_not_available",
    "final_gate_rerun_result_not_available",
    "human_resolution_completeness_gate_not_ready",
    "availability_items",
    "availability_item_count",
    "warnings",
    "non_claims",
]
MISSING_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS = [
    "missing_execution_evidence_report_id",
    "missing_execution_evidence_report_type",
    "missing_execution_evidence_report_version",
    "generated_at",
    "source_post_reexecution_verification_not_available_packet_id",
    "source_reexecution_execution_blocked_result_id",
    "missing_runtime_reexecution_output",
    "missing_runtime_application_output",
    "missing_final_gate_rerun_result",
    "missing_explicit_human_resolution",
    "missing_explicit_operator_signoff",
    "missing_explicit_selected_candidate",
    "missing_evidence_items",
    "missing_evidence_item_count",
    "warnings",
    "non_claims",
]
RUNTIME_NON_MUTATION_EVIDENCE_REPORT_REQUIRED_FIELDS = [
    "runtime_non_mutation_evidence_report_id",
    "runtime_non_mutation_evidence_report_type",
    "runtime_non_mutation_evidence_report_version",
    "generated_at",
    "source_post_reexecution_verification_not_available_packet_id",
    "source_reexecution_execution_blocked_result_id",
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
FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS = [
    "final_gate_dependency_report_id",
    "final_gate_dependency_report_type",
    "final_gate_dependency_report_version",
    "generated_at",
    "source_post_reexecution_verification_not_available_packet_id",
    "source_reexecution_execution_blocked_result_id",
    "source_final_gate_rerun_execution_blocked_result_path",
    "bp74_final_gate_rerun_not_performed",
    "bp76_runtime_reexecution_not_performed",
    "final_gate_rerun_result_available",
    "post_reexecution_verification_requires_runtime_execution",
    "final_gate_dependency_status",
    "dependency_items",
    "dependency_item_count",
    "warnings",
    "non_claims",
]
PHASE_FREEZE_READINESS_REPORT_REQUIRED_FIELDS = [
    "phase_freeze_readiness_report_id",
    "phase_freeze_readiness_report_type",
    "phase_freeze_readiness_report_version",
    "generated_at",
    "source_post_reexecution_verification_not_available_packet_id",
    "source_reexecution_execution_blocked_result_id",
    "ready_to_freeze_blocked_pathway",
    "freeze_reason",
    "runtime_config_changed",
    "mutation_status",
    "phase_freeze_recommended_status",
    "next_possible_blueprint",
    "readiness_items",
    "readiness_item_count",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "post_reexecution_verification_not_available_packet_is_not_truth": True,
    "post_reexecution_verification_not_available_packet_is_not_accuracy_scoring": True,
    "post_reexecution_verification_not_available_packet_is_not_model_training": True,
    "post_reexecution_verification_not_available_packet_is_not_runtime_application": True,
    "post_reexecution_verification_not_available_packet_does_not_execute_runtime_application": True,
    "post_reexecution_verification_not_available_packet_does_not_create_production_config": True,
    "post_reexecution_verification_not_available_packet_does_not_modify_model_weights": True,
    "post_reexecution_verification_not_available_packet_does_not_replace_baselines": True,
    "post_reexecution_verification_not_available_packet_does_not_infer_operator_signoff": True,
    "post_reexecution_verification_not_available_packet_does_not_infer_candidate_selection": True,
    "post_reexecution_verification_not_available_packet_does_not_infer_human_resolution": True,
    "post_reexecution_verification_not_available_packet_does_not_infer_final_gate_result": True,
    (
        "post_reexecution_verification_not_available_packet"
        "_does_not_infer_runtime_reexecution_output"
    ): True,
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
    "controlled_runtime_calibration_post_reexecution_verification_not_available_packet": True,
    "post_reexecution_verification_not_available": True,
    "runtime_reexecution_not_performed": True,
    "post_reexecution_result_not_available": True,
    "post_reexecution_not_verified": True,
    "runtime_application_not_executed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "final_gate_rerun_result_not_available": True,
    "final_gate_rerun_not_performed": True,
    "human_resolution_completeness_gate_not_ready": True,
    "required_human_inputs_missing": True,
    "classifier_correctness_not_assessed": True,
    **NON_CLAIMS,
}
FORBIDDEN_POST_REEXECUTION_VERIFICATION_TOKENS = {
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
    "fake_runtime_reexecution_output",
    "inferred_runtime_reexecution_output",
    "fake_post_reexecution_verification",
    "inferred_post_reexecution_verification",
    "runtime_application_success_without_final_gate_rerun",
}


def export_controlled_runtime_calibration_post_reexecution_verification_not_available_packet_contract(  # noqa: E501
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "post_reexecution_verification_scope": {
            "creates_post_reexecution_verification_not_available_packet": True,
            "bp76_reexecution_execution_blocked_result_is_authoritative_source": True,
            "default_state_not_available_without_runtime_reexecution": True,
            "runtime_reexecution_required_before_post_verification": True,
            "final_gate_rerun_result_required_before_runtime_reexecution": True,
            "candidate_option_discovery_is_inventory_only": True,
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
        "post_reexecution_verification_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUT_TYPE,
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUT_VERSION
            ),
            "required_fields": list(INPUT_REQUIRED_FIELDS),
        },
        "post_reexecution_verification_not_available_packet_schema": {
            "packet_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_TYPE
            ),
            "packet_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
            ),
            "required_fields": list(PACKET_REQUIRED_FIELDS),
            "allowed_post_reexecution_verification_statuses": list(
                ALLOWED_POST_REEXECUTION_VERIFICATION_STATUSES
            ),
            "allowed_post_reexecution_result_statuses": list(
                ALLOWED_POST_REEXECUTION_RESULT_STATUSES
            ),
            "allowed_post_reexecution_outcome_statuses": list(
                ALLOWED_POST_REEXECUTION_OUTCOME_STATUSES
            ),
            "allowed_reexecution_execution_statuses": list(
                ALLOWED_REEXECUTION_EXECUTION_STATUSES
            ),
            "allowed_reexecution_result_statuses": list(ALLOWED_REEXECUTION_RESULT_STATUSES),
            "allowed_reexecution_outcome_statuses": list(ALLOWED_REEXECUTION_OUTCOME_STATUSES),
            "allowed_runtime_application_statuses": list(ALLOWED_RUNTIME_APPLICATION_STATUSES),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "verification_availability_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_AVAILABILITY_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
            ),
            "required_fields": list(VERIFICATION_AVAILABILITY_REPORT_REQUIRED_FIELDS),
        },
        "missing_execution_evidence_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_MISSING_EXECUTION_EVIDENCE_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
            ),
            "required_fields": list(MISSING_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS),
        },
        "runtime_non_mutation_evidence_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
            ),
            "required_fields": list(RUNTIME_NON_MUTATION_EVIDENCE_REPORT_REQUIRED_FIELDS),
        },
        "final_gate_dependency_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
            ),
            "required_fields": list(FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS),
        },
        "phase_freeze_readiness_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_PHASE_FREEZE_READINESS_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
            ),
            "required_fields": list(PHASE_FREEZE_READINESS_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_post_reexecution_verification_input_shape": True,
            "validate_post_reexecution_verification_not_available_packet_shape": True,
            "validate_verification_availability_report_shape": True,
            "validate_missing_execution_evidence_report_shape": True,
            "validate_runtime_non_mutation_evidence_report_shape": True,
            "validate_final_gate_dependency_report_shape": True,
            "validate_phase_freeze_readiness_report_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_current_blocked_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_verification_not_available_unless_runtime_reexecution_exists": True,
            "validate_runtime_application_command_not_executed_by_bp77": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_single_candidate_option": True,
            "validate_no_final_gate_rerun_result_is_inferred": True,
            "validate_no_reexecution_approval_is_inferred": True,
            "validate_no_runtime_reexecution_output_is_inferred": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_verification_availability_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_auto_label_segments": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp76_reexecution_execution_blocked_result_path_required": True,
            "bp75_reexecution_request_packet_path_preserved": True,
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


def build_controlled_runtime_calibration_post_reexecution_verification_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    source_reexecution_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    source_reexecution_execution_blocked_result_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    source = _load_json(source_reexecution_execution_blocked_result_path)
    model_asset_ref = source.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = source.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    runtime_target_ref = _dict(source.get("runtime_config_target_ref"))
    runtime_target_path = runtime_target_ref.get("path")
    runtime_sha_after = (
        _sha256_file(Path(runtime_target_path))
        if runtime_target_path
        else source.get("runtime_config_target_sha256_after")
    )
    verification_status = _post_reexecution_verification_status(source)
    inputs = {
        "post_reexecution_verification_input_id": _stable_id(
            "controlled_runtime_calibration_post_reexecution_verification_inputs_v1",
            source.get("reexecution_execution_blocked_result_id"),
            source.get("reexecution_execution_status"),
            source.get("reexecution_result_status"),
            verification_status,
            source.get("runtime_config_target_sha256_before"),
            runtime_sha_after,
        ),
        "post_reexecution_verification_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUT_TYPE
        ),
        "post_reexecution_verification_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_execution_blocked_result_path": str(
            Path(source_reexecution_execution_blocked_result_path)
        ),
        **_source_paths_from_bp76_result(source),
        "candidate_option_refs": _list(source.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": runtime_target_ref,
        "runtime_config_target_sha256_before": source.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": runtime_sha_after,
        "requested_post_reexecution_verification_status": verification_status,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_reexecution_execution_blocked_result_path,
            source_reexecution_execution_blocked_result_contract_path,
            source,
        ),
        "source_status_snapshot": _status_snapshot_from_bp76_result(source),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_post_reexecution_inputs",
        "post_reexecution_verification_input_id": inputs[
            "post_reexecution_verification_input_id"
        ],
        **_input_status_snapshot(inputs),
        "candidate_option_count": len(inputs["candidate_option_refs"]),
        "next_action_recommendation": _next_actions_from_bp76_result(source),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_post_reexecution_verification_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(post_reexecution_verification_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_post_reexecution_verification_inputs_validation"
        ),
        payload_path=post_reexecution_verification_inputs_path,
        payload_type=inputs.get("post_reexecution_verification_input_type"),
        payload_version=inputs.get("post_reexecution_verification_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_input_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_post_reexecution_verification_not_available_packet(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(post_reexecution_verification_inputs_path)
    source = _source_bp76_result(inputs)
    verification_status = _post_reexecution_verification_status(source)
    result_status = _post_reexecution_result_status(source)
    outcome_status = _post_reexecution_outcome_status(source)
    reason = _post_reexecution_verification_reason(source)
    packet_id = _stable_id(
        "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_v1",
        inputs.get("post_reexecution_verification_input_id"),
        source.get("reexecution_execution_blocked_result_id"),
        verification_status,
        result_status,
        outcome_status,
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    status_snapshot = _status_snapshot_from_bp76_result(source)
    packet = {
        "post_reexecution_verification_not_available_packet_id": packet_id,
        "post_reexecution_verification_not_available_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_TYPE
        ),
        "post_reexecution_verification_not_available_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_input_path": str(
            Path(post_reexecution_verification_inputs_path)
        ),
        "source_reexecution_execution_blocked_result_path": inputs.get(
            "source_reexecution_execution_blocked_result_path"
        ),
        **_source_paths_from_inputs(inputs),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "post_reexecution_verification_status": verification_status,
        "post_reexecution_verification_reason": reason,
        "post_reexecution_result_status": result_status,
        "post_reexecution_outcome_status": outcome_status,
        "reexecution_execution_status": source.get("reexecution_execution_status"),
        "reexecution_result_status": source.get("reexecution_result_status"),
        "reexecution_outcome_status": source.get("reexecution_outcome_status"),
        **status_snapshot,
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
        "verification_availability_report": _verification_availability_report(
            packet_id,
            source,
            verification_status,
            generated_at,
        ),
        "missing_execution_evidence_report": _missing_execution_evidence_report(
            packet_id,
            source,
            generated_at,
        ),
        "runtime_non_mutation_evidence_report": _runtime_non_mutation_evidence_report(
            packet_id,
            source,
            inputs,
            generated_at,
        ),
        "final_gate_dependency_report": _final_gate_dependency_report(
            packet_id,
            source,
            inputs,
            generated_at,
        ),
        "phase_freeze_readiness_report": _phase_freeze_readiness_report(
            packet_id,
            source,
            generated_at,
        ),
        "next_action_recommendation": _next_actions_from_bp76_result(source),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    errors.extend(_validate_packet_shape(packet))
    _write_json_if_requested(output_path, packet)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_post_reexecution_packet",
        "post_reexecution_verification_not_available_packet_id": packet_id,
        **_packet_status_snapshot(packet),
        "candidate_option_count": packet["candidate_option_count"],
        "next_action_recommendation": packet["next_action_recommendation"],
        "post_reexecution_verification_not_available_packet_output": _path_string(
            output_path
        ),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_post_reexecution_verification_not_available_packet(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(post_reexecution_verification_not_available_packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    validation = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_post_reexecution_verification_not_available_packet_validation"
        ),
        payload_path=post_reexecution_verification_not_available_packet_path,
        payload_type=packet.get(
            "post_reexecution_verification_not_available_packet_type"
        ),
        payload_version=packet.get(
            "post_reexecution_verification_not_available_packet_version"
        ),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_packet_status_snapshot(packet),
    )
    _write_json_if_requested(output_path, validation)
    return validation


def build_controlled_runtime_calibration_post_reexecution_verification_availability_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_AVAILABILITY_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=post_reexecution_verification_not_available_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="verification_availability_report",
        report_validator=_validate_verification_availability_report_shape,
        output_key="post_reexecution_verification_availability_report_output",
    )


def build_controlled_runtime_calibration_post_reexecution_missing_execution_evidence_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_MISSING_EXECUTION_EVIDENCE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=post_reexecution_verification_not_available_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="missing_execution_evidence_report",
        report_validator=_validate_missing_execution_evidence_report_shape,
        output_key="post_reexecution_missing_execution_evidence_report_output",
    )


def build_controlled_runtime_calibration_post_reexecution_runtime_non_mutation_evidence_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=post_reexecution_verification_not_available_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="runtime_non_mutation_evidence_report",
        report_validator=_validate_runtime_non_mutation_evidence_report_shape,
        output_key="post_reexecution_runtime_non_mutation_evidence_report_output",
    )


def build_controlled_runtime_calibration_post_reexecution_final_gate_dependency_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=post_reexecution_verification_not_available_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="final_gate_dependency_report",
        report_validator=_validate_final_gate_dependency_report_shape,
        output_key="post_reexecution_final_gate_dependency_report_output",
    )


def build_controlled_runtime_calibration_post_reexecution_phase_freeze_readiness_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_OUTPUT
    ),
    post_reexecution_verification_not_available_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_PHASE_FREEZE_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=post_reexecution_verification_not_available_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="phase_freeze_readiness_report",
        report_validator=_validate_phase_freeze_readiness_report_shape,
        output_key="post_reexecution_phase_freeze_readiness_report_output",
    )


def _export_embedded_report(
    *,
    contract_path: str | Path,
    packet_path: str | Path,
    output_path: str | Path | None,
    generated_at: datetime | None,
    report_key: str,
    report_validator: Any,
    output_key: str,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(packet_path)
    report = {
        **_dict(packet.get(report_key)),
        "exported_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_path": str(
            Path(packet_path)
        ),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    errors.extend(report_validator(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else f"invalid_{report_key}",
        "post_reexecution_verification_not_available_packet_id": packet.get(
            "post_reexecution_verification_not_available_packet_id"
        ),
        **_packet_status_snapshot(packet),
        output_key: _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _source_artifact_refs(
    result_path: str | Path,
    result_contract_path: str | Path,
    result: dict[str, Any],
) -> dict[str, Any]:
    refs = {
        "reexecution_execution_blocked_result": _artifact_ref(result_path, result),
        "reexecution_execution_blocked_result_contract": _artifact_ref(
            result_contract_path,
            _load_json_if_exists(result_contract_path),
        ),
    }
    refs.update(_dict(result.get("source_artifact_refs")))
    return refs


def _source_bp76_result(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(inputs.get("source_reexecution_execution_blocked_result_path"))


def _source_paths_from_bp76_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_reexecution_request_packet_path": result.get(
            "source_reexecution_request_packet_path"
        ),
        "source_final_gate_rerun_execution_blocked_result_path": result.get(
            "source_final_gate_rerun_execution_blocked_result_path"
        ),
        "source_final_gate_rerun_request_packet_path": result.get(
            "source_final_gate_rerun_request_packet_path"
        ),
        "source_human_resolution_completeness_gate_path": result.get(
            "source_human_resolution_completeness_gate_path"
        ),
        "source_explicit_human_resolution_record_path": result.get(
            "source_explicit_human_resolution_record_path"
        ),
        "source_human_resolution_provided_packet_path": result.get(
            "source_human_resolution_provided_packet_path"
        ),
        "source_human_resolution_input_packet_path": result.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": result.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": result.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": result.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": result.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": result.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": result.get(
            "source_application_execution_path"
        ),
        "source_pre_application_final_gate_path": result.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": result.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": result.get("source_application_plan_path"),
        "source_human_approval_gate_path": result.get("source_human_approval_gate_path"),
        "source_change_request_path": result.get("source_change_request_path"),
    }


def _source_paths_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        key: inputs.get(key)
        for key in INPUT_REQUIRED_FIELDS
        if key.startswith("source_")
        and key.endswith("_path")
        and key != "source_reexecution_execution_blocked_result_path"
    }


def _runtime_reexecution_performed(result: dict[str, Any]) -> bool:
    return (
        result.get("reexecution_execution_status")
        == "reexecution_execution_completed_structural_only"
        and result.get("reexecution_result_status") == "reexecution_result_structural_only"
        and result.get("reexecution_outcome_status") == "reexecution_structural_only"
    )


def _post_reexecution_verification_status(result: dict[str, Any]) -> str:
    if _runtime_reexecution_performed(result):
        return "post_reexecution_verification_ready_after_runtime_reexecution"
    return "post_reexecution_verification_not_available"


def _post_reexecution_verification_reason(result: dict[str, Any]) -> str:
    if _runtime_reexecution_performed(result):
        return "runtime_reexecution_output_available_for_future_verification"
    return "runtime_reexecution_not_performed"


def _post_reexecution_result_status(result: dict[str, Any]) -> str:
    if _runtime_reexecution_performed(result):
        return "post_reexecution_result_deferred"
    return "post_reexecution_result_not_available"


def _post_reexecution_outcome_status(result: dict[str, Any]) -> str:
    if _runtime_reexecution_performed(result):
        return "post_reexecution_verification_deferred"
    return "post_reexecution_not_verified"


def _status_snapshot_from_bp76_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "reexecution_request_status": result.get("reexecution_request_status"),
        "reexecution_readiness_status": result.get("reexecution_readiness_status"),
        "final_gate_rerun_execution_status": result.get(
            "final_gate_rerun_execution_status"
        ),
        "final_gate_rerun_result_status": result.get("final_gate_rerun_result_status"),
        "final_gate_rerun_outcome_status": result.get("final_gate_rerun_outcome_status"),
        "final_gate_rerun_request_status": result.get("final_gate_rerun_request_status"),
        "human_resolution_completeness_gate_status": result.get(
            "human_resolution_completeness_gate_status"
        ),
        "human_resolution_record_status": result.get("human_resolution_record_status"),
        "human_resolution_provided_status": result.get(
            "human_resolution_provided_status"
        ),
        "human_resolution_completeness_status": result.get(
            "human_resolution_completeness_status"
        ),
        "missing_input_status": result.get("missing_input_status"),
        "operator_input_completeness_status": result.get(
            "operator_input_completeness_status"
        ),
        "candidate_input_completeness_status": result.get(
            "candidate_input_completeness_status"
        ),
        "operator_signoff_status": result.get("operator_signoff_status"),
        "selected_candidate_status": result.get("selected_candidate_status"),
    }


def _input_status_snapshot(inputs: dict[str, Any]) -> dict[str, Any]:
    result = _source_bp76_result(inputs)
    return {
        "post_reexecution_verification_status": _post_reexecution_verification_status(result),
        "post_reexecution_verification_reason": _post_reexecution_verification_reason(result),
        "post_reexecution_result_status": _post_reexecution_result_status(result),
        "post_reexecution_outcome_status": _post_reexecution_outcome_status(result),
        "reexecution_execution_status": result.get("reexecution_execution_status"),
        "reexecution_result_status": result.get("reexecution_result_status"),
        "reexecution_outcome_status": result.get("reexecution_outcome_status"),
        **_status_snapshot_from_bp76_result(result),
        "runtime_application_status": "not_executed",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
    }


def _verification_availability_report(
    packet_id: str,
    result: dict[str, Any],
    verification_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    runtime_not_performed = not _runtime_reexecution_performed(result)
    result_not_available = result.get("reexecution_result_status") == (
        "reexecution_result_not_available"
    )
    final_gate_result_not_available = result.get("final_gate_rerun_result_status") == (
        "final_gate_rerun_result_not_available"
    )
    gate_not_ready = result.get("human_resolution_completeness_gate_status") == (
        "human_resolution_completeness_gate_not_ready"
    )
    items = [
        _item(
            "runtime_reexecution_not_performed",
            runtime_not_performed,
            result.get("reexecution_execution_status"),
        ),
        _item(
            "reexecution_result_not_available",
            result_not_available,
            result.get("reexecution_result_status"),
        ),
        _item("runtime_application_not_executed", True, "not_executed"),
        _item(
            "post_reexecution_verification_not_available",
            verification_status == "post_reexecution_verification_not_available",
            verification_status,
        ),
        _item(
            "final_gate_rerun_result_not_available",
            final_gate_result_not_available,
            result.get("final_gate_rerun_result_status"),
        ),
        _item(
            "human_resolution_completeness_gate_not_ready",
            gate_not_ready,
            result.get("human_resolution_completeness_gate_status"),
        ),
    ]
    return {
        "verification_availability_report_id": _stable_id(
            "controlled_runtime_calibration_post_reexecution_verification_availability_report_v1",
            packet_id,
            verification_status,
            result.get("reexecution_execution_status"),
        ),
        "verification_availability_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_AVAILABILITY_REPORT_TYPE
        ),
        "verification_availability_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_id": packet_id,
        "source_reexecution_execution_blocked_result_id": result.get(
            "reexecution_execution_blocked_result_id"
        ),
        "runtime_reexecution_not_performed": runtime_not_performed,
        "reexecution_result_not_available": result_not_available,
        "runtime_application_not_executed": True,
        "post_reexecution_verification_not_available": (
            verification_status == "post_reexecution_verification_not_available"
        ),
        "final_gate_rerun_result_not_available": final_gate_result_not_available,
        "human_resolution_completeness_gate_not_ready": gate_not_ready,
        "availability_items": items,
        "availability_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _missing_execution_evidence_report(
    packet_id: str,
    result: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    items = [
        _item("missing_runtime_reexecution_output", True, result.get("reexecution_result_status")),
        _item("missing_runtime_application_output", True, "not_executed"),
        _item(
            "missing_final_gate_rerun_result",
            True,
            result.get("final_gate_rerun_result_status"),
        ),
        _item(
            "missing_explicit_human_resolution",
            True,
            result.get("human_resolution_completeness_status"),
        ),
        _item("missing_explicit_operator_signoff", True, result.get("operator_signoff_status")),
        _item("missing_explicit_selected_candidate", True, result.get("selected_candidate_status")),
    ]
    return {
        "missing_execution_evidence_report_id": _stable_id(
            "controlled_runtime_calibration_post_reexecution_missing_execution_evidence_report_v1",
            packet_id,
            result.get("reexecution_result_status"),
            result.get("final_gate_rerun_result_status"),
        ),
        "missing_execution_evidence_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_MISSING_EXECUTION_EVIDENCE_REPORT_TYPE
        ),
        "missing_execution_evidence_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_id": packet_id,
        "source_reexecution_execution_blocked_result_id": result.get(
            "reexecution_execution_blocked_result_id"
        ),
        "missing_runtime_reexecution_output": True,
        "missing_runtime_application_output": True,
        "missing_final_gate_rerun_result": True,
        "missing_explicit_human_resolution": True,
        "missing_explicit_operator_signoff": True,
        "missing_explicit_selected_candidate": True,
        "missing_evidence_items": items,
        "missing_evidence_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _runtime_non_mutation_evidence_report(
    packet_id: str,
    result: dict[str, Any],
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
            "controlled_runtime_calibration_post_reexecution_runtime_non_mutation_evidence_report_v1",
            packet_id,
            inputs.get("runtime_config_target_sha256_before"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        "runtime_non_mutation_evidence_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_RUNTIME_NON_MUTATION_EVIDENCE_REPORT_TYPE
        ),
        "runtime_non_mutation_evidence_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_id": packet_id,
        "source_reexecution_execution_blocked_result_id": result.get(
            "reexecution_execution_blocked_result_id"
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


def _final_gate_dependency_report(
    packet_id: str,
    result: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    final_gate_not_performed = result.get("final_gate_rerun_outcome_status") == (
        "final_gate_rerun_not_performed"
    )
    result_available = result.get("final_gate_rerun_result_status") != (
        "final_gate_rerun_result_not_available"
    )
    runtime_not_performed = not _runtime_reexecution_performed(result)
    items = [
        _item(
            "bp74_final_gate_rerun_not_performed",
            final_gate_not_performed,
            result.get("final_gate_rerun_outcome_status"),
        ),
        _item(
            "bp76_runtime_reexecution_not_performed",
            runtime_not_performed,
            result.get("reexecution_outcome_status"),
        ),
        _item(
            "no_final_gate_result_available",
            not result_available,
            result.get("final_gate_rerun_result_status"),
        ),
        _item(
            "post_reexecution_verification_cannot_be_available_without_runtime_execution",
            runtime_not_performed,
            result.get("reexecution_execution_status"),
        ),
        _item(
            "final_gate_dependency_unresolved",
            not result_available,
            result.get("reexecution_readiness_status"),
        ),
    ]
    return {
        "final_gate_dependency_report_id": _stable_id(
            "controlled_runtime_calibration_post_reexecution_final_gate_dependency_report_v1",
            packet_id,
            final_gate_not_performed,
            runtime_not_performed,
            result_available,
        ),
        "final_gate_dependency_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_FINAL_GATE_DEPENDENCY_REPORT_TYPE
        ),
        "final_gate_dependency_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_id": packet_id,
        "source_reexecution_execution_blocked_result_id": result.get(
            "reexecution_execution_blocked_result_id"
        ),
        "source_final_gate_rerun_execution_blocked_result_path": inputs.get(
            "source_final_gate_rerun_execution_blocked_result_path"
        ),
        "bp74_final_gate_rerun_not_performed": final_gate_not_performed,
        "bp76_runtime_reexecution_not_performed": runtime_not_performed,
        "final_gate_rerun_result_available": result_available,
        "post_reexecution_verification_requires_runtime_execution": True,
        "final_gate_dependency_status": (
            "final_gate_dependency_satisfied"
            if result_available and not runtime_not_performed
            else "final_gate_dependency_unresolved"
        ),
        "dependency_items": items,
        "dependency_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _phase_freeze_readiness_report(
    packet_id: str,
    result: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    items = [
        _item("post_reexecution_verification_not_available_packet_exists", True, packet_id),
        _item("runtime_config_changed_false", True, False),
        _item("no_runtime_mutation_due_to_blocker", True, "no_runtime_mutation_due_to_blocker"),
        _item(
            "controlled_pathway_blocked_missing_human_resolution",
            True,
            result.get("missing_input_status"),
        ),
    ]
    return {
        "phase_freeze_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_post_reexecution_phase_freeze_readiness_report_v1",
            packet_id,
            result.get("missing_input_status"),
            result.get("mutation_status"),
        ),
        "phase_freeze_readiness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_PHASE_FREEZE_READINESS_REPORT_TYPE
        ),
        "phase_freeze_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_post_reexecution_verification_not_available_packet_id": packet_id,
        "source_reexecution_execution_blocked_result_id": result.get(
            "reexecution_execution_blocked_result_id"
        ),
        "ready_to_freeze_blocked_pathway": True,
        "freeze_reason": "controlled_pathway_blocked_missing_human_resolution",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "phase_freeze_recommended_status": "blocked_pathway_freeze_ready",
        "next_possible_blueprint": "controlled_calibration_blocked_pathway_phase_freeze",
        "readiness_items": items,
        "readiness_item_count": len(items),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _item(item_code: str, satisfied: bool, observed_value: Any) -> dict[str, Any]:
    return {
        "item_code": item_code,
        "satisfied": bool(satisfied),
        "observed_value": observed_value,
    }


def _next_actions_from_bp76_result(result: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if result.get("human_resolution_completeness_status") != "human_resolution_complete":
        actions.append("provide_human_resolution_inputs")
    if result.get("operator_input_completeness_status") != "operator_inputs_complete":
        actions.append("provide_operator_inputs")
    if result.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        actions.append("provide_selected_candidate_inputs")
    if (
        "provide_operator_inputs" in actions
        or "provide_selected_candidate_inputs" in actions
    ):
        actions.append("provide_operator_signoff_and_selected_candidate")
    if result.get("final_gate_rerun_outcome_status") != "final_gate_rerun_structural_only":
        actions.append("rerun_final_gate_after_human_resolution")
    if result.get("final_gate_rerun_result_status") != "final_gate_rerun_result_not_available":
        actions.append("prepare_reexecution_after_final_gate_rerun")
    if _runtime_reexecution_performed(result):
        actions.append("prepare_post_reexecution_verification_after_runtime_execution")
    actions.append("prepare_controlled_calibration_phase_freeze_blocked")
    return _unique_strings(actions) or ["no_runtime_action_recommended"]


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "post_reexecution_verification_scope",
        "source_contract_refs",
        "post_reexecution_verification_input_schema",
        "post_reexecution_verification_not_available_packet_schema",
        "verification_availability_report_schema",
        "missing_execution_evidence_report_schema",
        "runtime_non_mutation_evidence_report_schema",
        "final_gate_dependency_report_schema",
        "phase_freeze_readiness_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, INPUT_REQUIRED_FIELDS, "inputs")
    source = _source_bp76_result(inputs)
    errors.extend(_validate_source_bp76_result_shape(source))
    errors.extend(_validate_no_runtime_mutation_fields(inputs))
    expected_status = _post_reexecution_verification_status(source)
    if inputs.get("requested_post_reexecution_verification_status") != expected_status:
        errors.append(
            _error(
                "requested_post_reexecution_verification_status_must_match_bp76_state",
                "requested_post_reexecution_verification_status",
                inputs.get("requested_post_reexecution_verification_status"),
            )
        )
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_source_bp76_result_shape(result: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        result,
        [
            "reexecution_execution_blocked_result_id",
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
        ],
        "source_reexecution_execution_blocked_result",
    )
    for field, value, allowed in _status_fields_for_bp76_result(result):
        errors.extend(_validate_status(field, value, allowed))
    errors.extend(_validate_no_runtime_mutation_fields(result))
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


def _validate_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(packet, PACKET_REQUIRED_FIELDS, "packet")
    for field, value, allowed in _status_fields_for_packet(packet):
        errors.extend(_validate_status(field, value, allowed))
    source = _load_json_if_exists(
        packet.get("source_reexecution_execution_blocked_result_path")
    )
    expected_status = _post_reexecution_verification_status(source)
    if packet.get("post_reexecution_verification_status") != expected_status:
        errors.append(
            _error(
                "post_reexecution_verification_status_must_match_bp76_state",
                "post_reexecution_verification_status",
                packet.get("post_reexecution_verification_status"),
            )
        )
    if (
        not _runtime_reexecution_performed(source)
        and packet.get("post_reexecution_verification_status")
        != "post_reexecution_verification_not_available"
    ):
        errors.append(
            _error(
                "post_reexecution_verification_must_be_unavailable_without_runtime_reexecution",
                "post_reexecution_verification_status",
                packet.get("post_reexecution_verification_status"),
            )
        )
    if packet.get("runtime_application_status") != "not_executed":
        errors.append(
            _error(
                "bp77_must_not_execute_runtime_application",
                "runtime_application_status",
                packet.get("runtime_application_status"),
            )
        )
    errors.extend(_validate_no_runtime_mutation_fields(packet))
    errors.extend(
        _validate_verification_availability_report_shape(
            _dict(packet.get("verification_availability_report"))
        )
    )
    errors.extend(
        _validate_missing_execution_evidence_report_shape(
            _dict(packet.get("missing_execution_evidence_report"))
        )
    )
    errors.extend(
        _validate_runtime_non_mutation_evidence_report_shape(
            _dict(packet.get("runtime_non_mutation_evidence_report"))
        )
    )
    errors.extend(
        _validate_final_gate_dependency_report_shape(
            _dict(packet.get("final_gate_dependency_report"))
        )
    )
    errors.extend(
        _validate_phase_freeze_readiness_report_shape(
            _dict(packet.get("phase_freeze_readiness_report"))
        )
    )
    errors.extend(_validate_next_actions(_list(packet.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(packet.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(packet))
    return errors


def _validate_verification_availability_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        VERIFICATION_AVAILABILITY_REPORT_REQUIRED_FIELDS,
        "verification_availability_report",
    )
    for field in [
        "runtime_reexecution_not_performed",
        "reexecution_result_not_available",
        "runtime_application_not_executed",
        "post_reexecution_verification_not_available",
        "final_gate_rerun_result_not_available",
        "human_resolution_completeness_gate_not_ready",
    ]:
        if report.get(field) is not True:
            errors.append(_error(f"{field}_must_be_true", field, report.get(field)))
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_missing_execution_evidence_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        MISSING_EXECUTION_EVIDENCE_REPORT_REQUIRED_FIELDS,
        "missing_execution_evidence_report",
    )
    for field in [
        "missing_runtime_reexecution_output",
        "missing_runtime_application_output",
        "missing_final_gate_rerun_result",
        "missing_explicit_human_resolution",
        "missing_explicit_operator_signoff",
        "missing_explicit_selected_candidate",
    ]:
        if report.get(field) is not True:
            errors.append(_error(f"{field}_must_be_true", field, report.get(field)))
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


def _validate_final_gate_dependency_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS,
        "final_gate_dependency_report",
    )
    if report.get("bp74_final_gate_rerun_not_performed") is not True:
        errors.append(
            _error(
                "bp74_final_gate_rerun_not_performed_must_be_true",
                "bp74_final_gate_rerun_not_performed",
                report.get("bp74_final_gate_rerun_not_performed"),
            )
        )
    if report.get("bp76_runtime_reexecution_not_performed") is not True:
        errors.append(
            _error(
                "bp76_runtime_reexecution_not_performed_must_be_true",
                "bp76_runtime_reexecution_not_performed",
                report.get("bp76_runtime_reexecution_not_performed"),
            )
        )
    if report.get("final_gate_dependency_status") != "final_gate_dependency_unresolved":
        errors.append(
            _error(
                "final_gate_dependency_status_must_remain_unresolved",
                "final_gate_dependency_status",
                report.get("final_gate_dependency_status"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_phase_freeze_readiness_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        PHASE_FREEZE_READINESS_REPORT_REQUIRED_FIELDS,
        "phase_freeze_readiness_report",
    )
    if report.get("ready_to_freeze_blocked_pathway") is not True:
        errors.append(
            _error(
                "ready_to_freeze_blocked_pathway_must_be_true",
                "ready_to_freeze_blocked_pathway",
                report.get("ready_to_freeze_blocked_pathway"),
            )
        )
    if report.get("phase_freeze_recommended_status") != "blocked_pathway_freeze_ready":
        errors.append(
            _error(
                "phase_freeze_recommended_status_must_be_blocked_pathway_freeze_ready",
                "phase_freeze_recommended_status",
                report.get("phase_freeze_recommended_status"),
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


def _status_fields_for_bp76_result(result: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
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
        (
            "reexecution_request_status",
            result.get("reexecution_request_status"),
            ALLOWED_REEXECUTION_REQUEST_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            result.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
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
            "runtime_application_status",
            result.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]


def _status_fields_for_packet(packet: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
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
        *_status_fields_for_bp76_result(packet),
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
            if key in FORBIDDEN_POST_REEXECUTION_VERIFICATION_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif (
        isinstance(payload, str)
        and payload in FORBIDDEN_POST_REEXECUTION_VERIFICATION_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _packet_status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "post_reexecution_verification_status",
        "post_reexecution_verification_reason",
        "post_reexecution_result_status",
        "post_reexecution_outcome_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_NOT_AVAILABLE_PACKET_VERSION
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_REEXECUTION_VERIFICATION_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_76",
        "scope": (
            "controlled_runtime_calibration_post_reexecution_verification"
            "_not_available_packet"
        ),
        "runtime_boundary": "no_runtime_reexecution_or_application_or_config_mutation",
    }
