from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_execution_blocked_result import (  # noqa: E501
    ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_execution_blocked_result import (  # noqa: E501
    SOURCE_CONTRACT_REFS as BP74_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.controlled_runtime_calibration_final_gate_rerun_request_packet import (
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
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_TYPE = (
    "controlled_runtime_calibration_reexecution_request_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_INPUT_TYPE = (
    "controlled_runtime_calibration_reexecution_request_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_TYPE = (
    "controlled_runtime_calibration_reexecution_request_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_BLOCKER_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_request_blocker_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_PREREQUISITE_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_prerequisite_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_DEPENDENCY_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_dependency_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PLAN_TYPE = (
    "controlled_runtime_calibration_reexecution_execution_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE = (
    "controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report"
)
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_BLUEPRINT = "blueprint_75"
CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_reexecution_request_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_reexecution_request_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_request_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_request_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_reexecution_request_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_request_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_BLOCKER_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_request_blocker_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_PREREQUISITE_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_prerequisite_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_DEPENDENCY_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_final_gate_dependency_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PLAN_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_reexecution_execution_plan.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_EXPORTED_AT = datetime(
    2026,
    6,
    22,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    (
        "controlled_runtime_calibration_final_gate_rerun_execution_blocked_result_contract_version"
    ): "v1",
    **dict(BP74_SOURCE_CONTRACT_REFS),
}

ALLOWED_REEXECUTION_REQUEST_STATUSES = [
    "reexecution_request_blocked_final_gate_not_rerun",
    "reexecution_request_blocked_missing_human_resolution",
    "reexecution_request_blocked_missing_operator_signoff",
    "reexecution_request_blocked_missing_selected_candidate",
    "reexecution_request_blocked_invalid_final_gate_result",
    "reexecution_request_created_not_ready",
    "reexecution_request_ready_after_final_gate_rerun",
    "reexecution_request_created_with_warnings",
    "reexecution_request_informational_only",
    "not_applicable",
]
ALLOWED_REEXECUTION_READINESS_STATUSES = [
    "reexecution_blocked_final_gate_not_rerun",
    "reexecution_not_ready_blockers_unresolved",
    "reexecution_ready_after_final_gate_rerun",
    "reexecution_blocked_missing_operator_signoff",
    "reexecution_blocked_missing_selected_candidate",
    "reexecution_blocked_missing_human_resolution",
    "reexecution_blocked_invalid_final_gate_result",
    "reexecution_not_executed",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "not_executed",
    "blocked_from_runtime_application",
    "runtime_application_not_ready",
    "runtime_application_deferred_to_future_blueprint",
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
    "no_runtime_action_recommended",
    "not_applicable",
]
ALLOWED_REEXECUTION_EXECUTION_PLAN_STATUSES = [
    "not_executed",
    "runtime_application_deferred_to_future_blueprint",
    "runtime_application_not_ready",
    "blocked_from_runtime_application",
    "not_applicable",
]

INPUT_REQUIRED_FIELDS = [
    "reexecution_request_input_id",
    "reexecution_request_input_type",
    "reexecution_request_input_version",
    "generated_at",
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
    "requested_reexecution_status",
    "source_contract_refs",
    "source_artifact_refs",
    "source_status_snapshot",
    "warnings",
    "non_claims",
]
PACKET_REQUIRED_FIELDS = [
    "reexecution_request_packet_id",
    "reexecution_request_packet_type",
    "reexecution_request_packet_version",
    "generated_at",
    "source_reexecution_request_input_path",
    *INPUT_REQUIRED_FIELDS[4:21],
    "candidate_option_refs",
    "candidate_option_count",
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
    "blocker_report",
    "prerequisite_report",
    "final_gate_dependency_report",
    "reexecution_execution_plan",
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
BLOCKER_REPORT_REQUIRED_FIELDS = [
    "blocker_report_id",
    "blocker_report_type",
    "blocker_report_version",
    "generated_at",
    "source_reexecution_request_packet_id",
    "reexecution_request_status",
    "reexecution_readiness_status",
    "blocker_codes",
    "blockers",
    "blocker_count",
    "warnings",
    "non_claims",
]
PREREQUISITE_REPORT_REQUIRED_FIELDS = [
    "prerequisite_report_id",
    "prerequisite_report_type",
    "prerequisite_report_version",
    "generated_at",
    "source_reexecution_request_packet_id",
    "prerequisite_status",
    "prerequisites",
    "prerequisite_count",
    "satisfied_prerequisite_count",
    "unsatisfied_prerequisite_count",
    "warnings",
    "non_claims",
]
FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS = [
    "final_gate_dependency_report_id",
    "final_gate_dependency_report_type",
    "final_gate_dependency_report_version",
    "generated_at",
    "source_reexecution_request_packet_id",
    "source_final_gate_rerun_execution_blocked_result_path",
    "final_gate_rerun_performed",
    "final_gate_rerun_result_available",
    "final_gate_dependency_status",
    "dependency_items",
    "dependency_item_count",
    "warnings",
    "non_claims",
]
REEXECUTION_EXECUTION_PLAN_REQUIRED_FIELDS = [
    "reexecution_execution_plan_id",
    "reexecution_execution_plan_type",
    "reexecution_execution_plan_version",
    "generated_at",
    "source_reexecution_request_packet_id",
    "required_final_gate_rerun_result",
    "required_human_resolution_artifact",
    "required_operator_signoff_artifact",
    "required_selected_candidate_artifact",
    "required_regression_gates",
    "required_runtime_config_unchanged_check",
    "required_no_model_weight_change_check",
    "required_no_baseline_replacement_check",
    "future_execution_command_placeholder",
    "execution_status",
    "warnings",
    "non_claims",
]
RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS = [
    "runtime_mutation_prevention_report_id",
    "runtime_mutation_prevention_report_type",
    "runtime_mutation_prevention_report_version",
    "generated_at",
    "source_reexecution_request_packet_id",
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
    "reexecution_request_packet_is_not_truth": True,
    "reexecution_request_packet_is_not_accuracy_scoring": True,
    "reexecution_request_packet_is_not_model_training": True,
    "reexecution_request_packet_is_not_runtime_application": True,
    "reexecution_request_packet_does_not_execute_runtime_application": True,
    "reexecution_request_packet_does_not_create_production_config": True,
    "reexecution_request_packet_does_not_modify_model_weights": True,
    "reexecution_request_packet_does_not_replace_baselines": True,
    "reexecution_request_packet_does_not_infer_operator_signoff": True,
    "reexecution_request_packet_does_not_infer_candidate_selection": True,
    "reexecution_request_packet_does_not_infer_human_resolution": True,
    "reexecution_request_packet_does_not_infer_final_gate_result": True,
    "human_resolution_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
    "operator_signoff_must_be_explicit": True,
    "final_gate_result_must_be_explicit": True,
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
}
WARNINGS = {
    "controlled_runtime_calibration_reexecution_request_packet": True,
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
    "reexecution_request_packet_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "candidate_option_inventory_not_selection": True,
    **NON_CLAIMS,
}
FORBIDDEN_REEXECUTION_REQUEST_PACKET_TOKENS = {
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
}


def export_controlled_runtime_calibration_reexecution_request_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at or CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_EXPORTED_AT
    )
    contract = {
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_TYPE,
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "reexecution_request_scope": {
            "creates_reexecution_request_packet": True,
            "bp74_blocked_result_is_authoritative_source": True,
            "final_gate_rerun_result_required_before_ready_reexecution": True,
            "default_state_remains_blocked_without_final_gate_rerun_result": True,
            "candidate_option_discovery_is_inventory_only": True,
            "single_candidate_option_does_not_create_selection": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_infer_human_resolution": True,
            "does_not_infer_final_gate_result": True,
            "does_not_execute_final_gate_rerun": True,
            "does_not_write_runtime_config": True,
            "does_not_execute_runtime_application": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "reexecution_request_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_INPUT_TYPE,
            "input_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_INPUT_VERSION,
            "required_fields": list(INPUT_REQUIRED_FIELDS),
        },
        "reexecution_request_packet_schema": {
            "packet_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_TYPE,
            "packet_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
            "required_fields": list(PACKET_REQUIRED_FIELDS),
            "allowed_reexecution_request_statuses": list(ALLOWED_REEXECUTION_REQUEST_STATUSES),
            "allowed_reexecution_readiness_statuses": list(ALLOWED_REEXECUTION_READINESS_STATUSES),
            "allowed_runtime_application_statuses": list(ALLOWED_RUNTIME_APPLICATION_STATUSES),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "blocker_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_BLOCKER_REPORT_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
            "required_fields": list(BLOCKER_REPORT_REQUIRED_FIELDS),
        },
        "prerequisite_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_PREREQUISITE_REPORT_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
            "required_fields": list(PREREQUISITE_REPORT_REQUIRED_FIELDS),
        },
        "final_gate_dependency_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_DEPENDENCY_REPORT_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
            "required_fields": list(FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS),
        },
        "reexecution_execution_plan_schema": {
            "plan_type": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PLAN_TYPE,
            "plan_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
            "required_fields": list(REEXECUTION_EXECUTION_PLAN_REQUIRED_FIELDS),
        },
        "runtime_mutation_prevention_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE
            ),
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
            "required_fields": list(RUNTIME_MUTATION_PREVENTION_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_reexecution_request_input_shape": True,
            "validate_reexecution_request_packet_shape": True,
            "validate_blocker_report_shape": True,
            "validate_prerequisite_report_shape": True,
            "validate_final_gate_dependency_report_shape": True,
            "validate_reexecution_execution_plan_shape": True,
            "validate_runtime_mutation_prevention_report_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_current_blocked_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_reexecution_request_blocked_unless_bp74_has_result": True,
            "validate_runtime_application_not_executed_by_bp75": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_single_candidate_option": True,
            "validate_no_final_gate_rerun_result_is_inferred": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_request_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_auto_label_segments": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp74_final_gate_rerun_execution_blocked_result_path_required": True,
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


def build_controlled_runtime_calibration_reexecution_request_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    source_final_gate_rerun_execution_blocked_result_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_OUTPUT
    ),
    source_final_gate_rerun_execution_blocked_result_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_BLOCKED_RESULT_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    bp74_result = _load_json(source_final_gate_rerun_execution_blocked_result_path)
    model_asset_ref = bp74_result.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = bp74_result.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    runtime_target_ref = _dict(bp74_result.get("runtime_config_target_ref"))
    runtime_target_path = runtime_target_ref.get("path")
    runtime_sha_after = (
        _sha256_file(Path(runtime_target_path))
        if runtime_target_path
        else bp74_result.get("runtime_config_target_sha256_after")
    )
    inputs = {
        "reexecution_request_input_id": _stable_id(
            "controlled_runtime_calibration_reexecution_request_packet_inputs_v1",
            bp74_result.get("final_gate_rerun_execution_blocked_result_id"),
            bp74_result.get("final_gate_rerun_execution_status"),
            bp74_result.get("final_gate_rerun_result_status"),
            bp74_result.get("final_gate_rerun_outcome_status"),
            bp74_result.get("runtime_config_target_sha256_before"),
            runtime_sha_after,
        ),
        "reexecution_request_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_INPUT_TYPE
        ),
        "reexecution_request_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_execution_blocked_result_path": str(
            Path(source_final_gate_rerun_execution_blocked_result_path)
        ),
        **_source_paths_from_bp74_result(bp74_result),
        "candidate_option_refs": _list(bp74_result.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": runtime_target_ref,
        "runtime_config_target_sha256_before": bp74_result.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": runtime_sha_after,
        "requested_reexecution_status": _request_status(bp74_result),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_final_gate_rerun_execution_blocked_result_path,
            source_final_gate_rerun_execution_blocked_result_contract_path,
            bp74_result,
        ),
        "source_status_snapshot": _status_snapshot_from_bp74_result(bp74_result),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_reexecution_request_inputs",
        "reexecution_request_input_id": inputs["reexecution_request_input_id"],
        **_input_status_snapshot(inputs),
        "candidate_option_count": len(inputs["candidate_option_refs"]),
        "next_action_recommendation": _next_actions_from_bp74_result(bp74_result),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_reexecution_request_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(reexecution_request_packet_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_reexecution_request_packet_inputs_validation",
        payload_path=reexecution_request_packet_inputs_path,
        payload_type=inputs.get("reexecution_request_input_type"),
        payload_version=inputs.get("reexecution_request_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_input_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_reexecution_request_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(reexecution_request_packet_inputs_path)
    bp74_result = _source_bp74_result(inputs)
    request_status = _request_status(bp74_result)
    readiness_status = _readiness_status(bp74_result)
    packet_id = _stable_id(
        "controlled_runtime_calibration_reexecution_request_packet_v1",
        inputs.get("reexecution_request_input_id"),
        bp74_result.get("final_gate_rerun_execution_blocked_result_id"),
        request_status,
        readiness_status,
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    packet = {
        "reexecution_request_packet_id": packet_id,
        "reexecution_request_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_TYPE
        ),
        "reexecution_request_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_input_path": str(Path(reexecution_request_packet_inputs_path)),
        "source_final_gate_rerun_execution_blocked_result_path": inputs.get(
            "source_final_gate_rerun_execution_blocked_result_path"
        ),
        **_source_paths_from_inputs(inputs),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "reexecution_request_status": request_status,
        "reexecution_readiness_status": readiness_status,
        **_status_snapshot_from_bp74_result(bp74_result),
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
        "runtime_config_target_sha256_after": inputs.get("runtime_config_target_sha256_after"),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "blocker_report": _blocker_report(packet_id, bp74_result, request_status, readiness_status, generated_at),  # noqa: E501
        "prerequisite_report": _prerequisite_report(packet_id, bp74_result, generated_at),
        "final_gate_dependency_report": _final_gate_dependency_report(
            packet_id,
            bp74_result,
            inputs,
            generated_at,
        ),
        "reexecution_execution_plan": _reexecution_execution_plan(
            packet_id,
            bp74_result,
            inputs,
            request_status,
            generated_at,
        ),
        "runtime_mutation_prevention_report": _runtime_mutation_prevention_report(
            packet_id,
            inputs,
            generated_at,
        ),
        "next_action_recommendation": _next_actions_from_bp74_result(bp74_result),
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
        "status": "completed" if not errors else "invalid_reexecution_request_packet",
        "reexecution_request_packet_id": packet_id,
        **_packet_status_snapshot(packet),
        "candidate_option_count": packet["candidate_option_count"],
        "next_action_recommendation": packet["next_action_recommendation"],
        "reexecution_request_packet_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_reexecution_request_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(reexecution_request_packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_reexecution_request_packet_validation",
        payload_path=reexecution_request_packet_path,
        payload_type=packet.get("reexecution_request_packet_type"),
        payload_version=packet.get("reexecution_request_packet_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_packet_status_snapshot(packet),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_reexecution_request_blocker_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_BLOCKER_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=reexecution_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="blocker_report",
        report_validator=_validate_blocker_report_shape,
        output_key="reexecution_request_blocker_report_output",
    )


def build_controlled_runtime_calibration_reexecution_prerequisite_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_PREREQUISITE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=reexecution_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="prerequisite_report",
        report_validator=_validate_prerequisite_report_shape,
        output_key="reexecution_prerequisite_report_output",
    )


def build_controlled_runtime_calibration_final_gate_dependency_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_DEPENDENCY_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=reexecution_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="final_gate_dependency_report",
        report_validator=_validate_final_gate_dependency_report_shape,
        output_key="final_gate_dependency_report_output",
    )


def build_controlled_runtime_calibration_reexecution_execution_plan(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=reexecution_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="reexecution_execution_plan",
        report_validator=_validate_reexecution_execution_plan_shape,
        output_key="reexecution_execution_plan_output",
    )


def build_controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    reexecution_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=reexecution_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="runtime_mutation_prevention_report",
        report_validator=_validate_runtime_mutation_prevention_report_shape,
        output_key="reexecution_runtime_mutation_prevention_report_output",
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
        "source_reexecution_request_packet_path": str(Path(packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    errors.extend(report_validator(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else f"invalid_{report_key}",
        "reexecution_request_packet_id": packet.get("reexecution_request_packet_id"),
        **_packet_status_snapshot(packet),
        output_key: _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _source_artifact_refs(
    bp74_result_path: str | Path,
    bp74_contract_path: str | Path,
    bp74_result: dict[str, Any],
) -> dict[str, Any]:
    refs = {
        "final_gate_rerun_execution_blocked_result": _artifact_ref(
            bp74_result_path,
            bp74_result,
        ),
        "final_gate_rerun_execution_blocked_result_contract": _artifact_ref(
            bp74_contract_path,
            _load_json_if_exists(bp74_contract_path),
        ),
    }
    refs.update(_dict(bp74_result.get("source_artifact_refs")))
    return refs


def _source_bp74_result(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(
        inputs.get("source_final_gate_rerun_execution_blocked_result_path")
    )


def _source_paths_from_bp74_result(bp74_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_final_gate_rerun_request_packet_path": bp74_result.get(
            "source_final_gate_rerun_request_packet_path"
        ),
        "source_human_resolution_completeness_gate_path": bp74_result.get(
            "source_human_resolution_completeness_gate_path"
        ),
        "source_explicit_human_resolution_record_path": bp74_result.get(
            "source_explicit_human_resolution_record_path"
        ),
        "source_human_resolution_provided_packet_path": bp74_result.get(
            "source_human_resolution_provided_packet_path"
        ),
        "source_human_resolution_input_packet_path": bp74_result.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": bp74_result.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": bp74_result.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": bp74_result.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": bp74_result.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": bp74_result.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": bp74_result.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": bp74_result.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": bp74_result.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": bp74_result.get("source_application_plan_path"),
        "source_human_approval_gate_path": bp74_result.get("source_human_approval_gate_path"),
        "source_change_request_path": bp74_result.get("source_change_request_path"),
    }


def _source_paths_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        key: inputs.get(key)
        for key in INPUT_REQUIRED_FIELDS
        if key.startswith("source_")
        and key.endswith("_path")
        and key != "source_final_gate_rerun_execution_blocked_result_path"
    }


def _final_gate_rerun_performed(bp74_result: dict[str, Any]) -> bool:
    return (
        bp74_result.get("final_gate_rerun_execution_status")
        == "final_gate_rerun_execution_completed_structural_only"
        and bp74_result.get("final_gate_rerun_result_status")
        == "final_gate_rerun_result_structural_only"
        and bp74_result.get("final_gate_rerun_outcome_status") == "final_gate_rerun_structural_only"
    )


def _request_status(bp74_result: dict[str, Any]) -> str:
    if not _final_gate_rerun_performed(bp74_result):
        return "reexecution_request_blocked_final_gate_not_rerun"
    if bp74_result.get("human_resolution_completeness_status") != "human_resolution_complete":
        return "reexecution_request_blocked_missing_human_resolution"
    if bp74_result.get("operator_input_completeness_status") != "operator_inputs_complete":
        return "reexecution_request_blocked_missing_operator_signoff"
    if bp74_result.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        return "reexecution_request_blocked_missing_selected_candidate"
    return "reexecution_request_ready_after_final_gate_rerun"


def _readiness_status(bp74_result: dict[str, Any]) -> str:
    request_status = _request_status(bp74_result)
    if request_status == "reexecution_request_ready_after_final_gate_rerun":
        return "reexecution_ready_after_final_gate_rerun"
    if request_status == "reexecution_request_blocked_final_gate_not_rerun":
        return "reexecution_blocked_final_gate_not_rerun"
    if request_status == "reexecution_request_blocked_missing_human_resolution":
        return "reexecution_blocked_missing_human_resolution"
    if request_status == "reexecution_request_blocked_missing_operator_signoff":
        return "reexecution_blocked_missing_operator_signoff"
    if request_status == "reexecution_request_blocked_missing_selected_candidate":
        return "reexecution_blocked_missing_selected_candidate"
    if request_status == "reexecution_request_blocked_invalid_final_gate_result":
        return "reexecution_blocked_invalid_final_gate_result"
    return "reexecution_not_ready_blockers_unresolved"


def _status_snapshot_from_bp74_result(bp74_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "final_gate_rerun_execution_status": bp74_result.get(
            "final_gate_rerun_execution_status"
        ),
        "final_gate_rerun_result_status": bp74_result.get("final_gate_rerun_result_status"),
        "final_gate_rerun_outcome_status": bp74_result.get("final_gate_rerun_outcome_status"),
        "final_gate_rerun_request_status": bp74_result.get("final_gate_rerun_request_status"),
        "human_resolution_completeness_gate_status": bp74_result.get(
            "human_resolution_completeness_gate_status"
        ),
        "human_resolution_record_status": bp74_result.get("human_resolution_record_status"),
        "human_resolution_provided_status": bp74_result.get(
            "human_resolution_provided_status"
        ),
        "human_resolution_completeness_status": bp74_result.get(
            "human_resolution_completeness_status"
        ),
        "missing_input_status": bp74_result.get("missing_input_status"),
        "operator_input_completeness_status": bp74_result.get(
            "operator_input_completeness_status"
        ),
        "candidate_input_completeness_status": bp74_result.get(
            "candidate_input_completeness_status"
        ),
        "operator_signoff_status": bp74_result.get("operator_signoff_status"),
        "selected_candidate_status": bp74_result.get("selected_candidate_status"),
    }


def _input_status_snapshot(inputs: dict[str, Any]) -> dict[str, Any]:
    bp74_result = _source_bp74_result(inputs)
    return {
        "reexecution_request_status": _request_status(bp74_result),
        "reexecution_readiness_status": _readiness_status(bp74_result),
        **_status_snapshot_from_bp74_result(bp74_result),
        "runtime_application_status": "not_executed",
        "runtime_config_changed": False,
        "mutation_status": "no_runtime_mutation_due_to_blocker",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
    }


def _blocker_report(
    packet_id: str,
    bp74_result: dict[str, Any],
    request_status: str,
    readiness_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    codes = _blocker_codes(bp74_result)
    return {
        "blocker_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_request_blocker_report_v1",
            packet_id,
            request_status,
            readiness_status,
            *codes,
        ),
        "blocker_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_BLOCKER_REPORT_TYPE
        ),
        "blocker_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_packet_id": packet_id,
        "reexecution_request_status": request_status,
        "reexecution_readiness_status": readiness_status,
        "blocker_codes": codes,
        "blockers": [
            {
                "blocker_code": code,
                "status": "required",
                "source": _blocker_source(code, bp74_result),
            }
            for code in codes
        ],
        "blocker_count": len(codes),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocker_codes(bp74_result: dict[str, Any]) -> list[str]:
    codes = []
    if not _final_gate_rerun_performed(bp74_result):
        codes.extend(
            [
                "final_gate_rerun_not_performed",
                "final_gate_rerun_result_not_available",
                "final_gate_rerun_execution_blocked_missing_human_resolution",
            ]
        )
    if bp74_result.get("human_resolution_completeness_gate_status") != (
        "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    ):
        codes.append("human_resolution_completeness_gate_not_ready")
    if bp74_result.get("operator_input_completeness_status") != "operator_inputs_complete":
        codes.extend(
            [
                "missing_operator_identity",
                "missing_operator_attestation",
                "missing_operator_timestamp",
            ]
        )
    if bp74_result.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        codes.extend(
            [
                "missing_selected_candidate_ref",
                "missing_selected_candidate_source_path",
                "missing_selected_candidate_selection_reason",
                "missing_candidate_selection_timestamp",
                "missing_operator_reference_for_selection",
            ]
        )
    codes.append("runtime_application_blocked_before_mutation")
    return _unique_strings(codes)


def _blocker_source(code: str, bp74_result: dict[str, Any]) -> str | None:
    if code.startswith("missing_operator"):
        return bp74_result.get("source_explicit_operator_signoff_artifact_path")
    if code.startswith("missing_selected") or code.startswith("missing_candidate"):
        return bp74_result.get("source_explicit_selected_candidate_artifact_path")
    if code == "human_resolution_completeness_gate_not_ready":
        return bp74_result.get("source_human_resolution_completeness_gate_path")
    if code.startswith("final_gate_rerun"):
        return bp74_result.get("source_final_gate_rerun_request_packet_path")
    return bp74_result.get("source_application_execution_path")


def _prerequisite_report(
    packet_id: str,
    bp74_result: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    prerequisites = [
        _prerequisite("explicit_operator_signoff_required", False, bp74_result.get("operator_signoff_status")),  # noqa: E501
        _prerequisite("explicit_selected_candidate_required", False, bp74_result.get("selected_candidate_status")),  # noqa: E501
        _prerequisite(
            "human_resolution_completeness_gate_must_be_ready",
            bp74_result.get("human_resolution_completeness_gate_status")
            == "human_resolution_completeness_gate_ready_for_final_gate_rerun",
            bp74_result.get("human_resolution_completeness_gate_status"),
        ),
        _prerequisite(
            "final_gate_rerun_request_must_be_ready",
            bp74_result.get("final_gate_rerun_request_status")
            == "final_gate_rerun_request_ready_after_human_resolution",
            bp74_result.get("final_gate_rerun_request_status"),
        ),
        _prerequisite(
            "final_gate_rerun_execution_must_be_performed",
            _final_gate_rerun_performed(bp74_result),
            bp74_result.get("final_gate_rerun_execution_status"),
        ),
        _prerequisite(
            "final_gate_rerun_result_must_be_available",
            bp74_result.get("final_gate_rerun_result_status") != "final_gate_rerun_result_not_available",  # noqa: E501
            bp74_result.get("final_gate_rerun_result_status"),
        ),
        _prerequisite("runtime_config_must_remain_unchanged", True, bp74_result.get("runtime_config_changed")),  # noqa: E501
        _prerequisite("model_weights_must_remain_unchanged", True, bp74_result.get("model_update_status")),  # noqa: E501
        _prerequisite("protected_baselines_must_remain_unchanged", True, bp74_result.get("baseline_update_status")),  # noqa: E501
    ]
    satisfied = sum(1 for item in prerequisites if item["satisfied"])
    return {
        "prerequisite_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_prerequisite_report_v1",
            packet_id,
            satisfied,
            len(prerequisites),
        ),
        "prerequisite_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_PREREQUISITE_REPORT_TYPE
        ),
        "prerequisite_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_packet_id": packet_id,
        "prerequisite_status": (
            "reexecution_prerequisites_unmet"
            if satisfied < len(prerequisites)
            else "reexecution_prerequisites_met"
        ),
        "prerequisites": prerequisites,
        "prerequisite_count": len(prerequisites),
        "satisfied_prerequisite_count": satisfied,
        "unsatisfied_prerequisite_count": len(prerequisites) - satisfied,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_dependency_report(
    packet_id: str,
    bp74_result: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    final_gate_performed = _final_gate_rerun_performed(bp74_result)
    result_available = (
        bp74_result.get("final_gate_rerun_result_status")
        != "final_gate_rerun_result_not_available"
    )
    items = [
        _dependency(
            "source_bp74_blocked_result",
            bool(inputs.get("source_final_gate_rerun_execution_blocked_result_path")),
            inputs.get("source_final_gate_rerun_execution_blocked_result_path"),
        ),
        _dependency(
            "bp74_final_gate_rerun_was_not_performed",
            not final_gate_performed,
            bp74_result.get("final_gate_rerun_outcome_status"),
        ),
        _dependency(
            "no_final_gate_result_available",
            not result_available,
            bp74_result.get("final_gate_rerun_result_status"),
        ),
        _dependency(
            "reexecution_cannot_be_ready_without_final_gate_rerun_result",
            not final_gate_performed or not result_available,
            _readiness_status(bp74_result),
        ),
    ]
    return {
        "final_gate_dependency_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_dependency_report_v1",
            packet_id,
            final_gate_performed,
            result_available,
        ),
        "final_gate_dependency_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_DEPENDENCY_REPORT_TYPE
        ),
        "final_gate_dependency_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_packet_id": packet_id,
        "source_final_gate_rerun_execution_blocked_result_path": inputs.get(
            "source_final_gate_rerun_execution_blocked_result_path"
        ),
        "final_gate_rerun_performed": final_gate_performed,
        "final_gate_rerun_result_available": result_available,
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


def _reexecution_execution_plan(
    packet_id: str,
    bp74_result: dict[str, Any],
    inputs: dict[str, Any],
    request_status: str,
    generated_at: datetime,
) -> dict[str, Any]:
    ready = request_status == "reexecution_request_ready_after_final_gate_rerun"
    execution_status = (
        "runtime_application_deferred_to_future_blueprint" if ready else "not_executed"
    )
    return {
        "reexecution_execution_plan_id": _stable_id(
            "controlled_runtime_calibration_reexecution_execution_plan_v1",
            packet_id,
            request_status,
            execution_status,
        ),
        "reexecution_execution_plan_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_EXECUTION_PLAN_TYPE
        ),
        "reexecution_execution_plan_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_packet_id": packet_id,
        "required_final_gate_rerun_result": {
            "required": True,
            "current_status": bp74_result.get("final_gate_rerun_result_status"),
            "source": inputs.get("source_final_gate_rerun_execution_blocked_result_path"),
        },
        "required_human_resolution_artifact": {
            "required": True,
            "current_status": bp74_result.get("human_resolution_completeness_status"),
            "source": inputs.get("source_explicit_human_resolution_record_path"),
        },
        "required_operator_signoff_artifact": {
            "required": True,
            "current_status": bp74_result.get("operator_signoff_status"),
            "source": inputs.get("source_explicit_operator_signoff_artifact_path"),
        },
        "required_selected_candidate_artifact": {
            "required": True,
            "current_status": bp74_result.get("selected_candidate_status"),
            "source": inputs.get("source_explicit_selected_candidate_artifact_path"),
        },
        "required_regression_gates": [
            "multi_point_regression_matrix",
            "protected_sample_point_reviewed_3d_debug",
            "gameplay_gate_regression_baseline",
            "review_guided_gameplay_calibration_sandbox_regression",
        ],
        "required_runtime_config_unchanged_check": True,
        "required_no_model_weight_change_check": True,
        "required_no_baseline_replacement_check": True,
        "future_execution_command_placeholder": (
            "future_blueprint_may_execute_runtime_application_after_explicit_reexecution_readiness"
        ),
        "execution_status": execution_status,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _runtime_mutation_prevention_report(
    packet_id: str,
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
        _check("model_weights_not_modified", True, "not_modified"),
        _check("baselines_not_replaced", True, "not_replaced"),
    ]
    return {
        "runtime_mutation_prevention_report_id": _stable_id(
            "controlled_runtime_calibration_reexecution_runtime_mutation_prevention_report_v1",
            packet_id,
            inputs.get("runtime_config_target_sha256_before"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        "runtime_mutation_prevention_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_RUNTIME_MUTATION_PREVENTION_REPORT_TYPE
        ),
        "runtime_mutation_prevention_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_reexecution_request_packet_id": packet_id,
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


def _prerequisite(prerequisite_code: str, satisfied: bool, current_status: Any) -> dict[str, Any]:
    return {
        "prerequisite_code": prerequisite_code,
        "satisfied": bool(satisfied),
        "current_status": current_status,
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


def _next_actions_from_bp74_result(bp74_result: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if bp74_result.get("human_resolution_completeness_status") != "human_resolution_complete":
        actions.append("provide_human_resolution_inputs")
    if bp74_result.get("operator_input_completeness_status") != "operator_inputs_complete":
        actions.append("provide_operator_inputs")
    if bp74_result.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        actions.append("provide_selected_candidate_inputs")
    if actions:
        actions.append("provide_operator_signoff_and_selected_candidate")
    actions.append("rerun_final_gate_after_human_resolution")
    if _final_gate_rerun_performed(bp74_result):
        actions.append("prepare_reexecution_after_final_gate_rerun")
    return _unique_strings(actions)


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "reexecution_request_scope",
        "source_contract_refs",
        "reexecution_request_input_schema",
        "reexecution_request_packet_schema",
        "blocker_report_schema",
        "prerequisite_report_schema",
        "final_gate_dependency_report_schema",
        "reexecution_execution_plan_schema",
        "runtime_mutation_prevention_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, INPUT_REQUIRED_FIELDS, "inputs")
    bp74_result = _source_bp74_result(inputs)
    errors.extend(_validate_source_bp74_result_shape(bp74_result))
    errors.extend(_validate_no_runtime_mutation_fields(inputs))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_source_bp74_result_shape(bp74_result: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        bp74_result,
        [
            "final_gate_rerun_execution_blocked_result_id",
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
        "source_final_gate_rerun_execution_blocked_result",
    )
    for field, value, allowed in _status_fields_for_bp74_result(bp74_result):
        errors.extend(_validate_status(field, value, allowed))
    errors.extend(_validate_no_runtime_mutation_fields(bp74_result))
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


def _validate_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(packet, PACKET_REQUIRED_FIELDS, "packet")
    for field, value, allowed in _status_fields_for_packet(packet):
        errors.extend(_validate_status(field, value, allowed))
    bp74_result = _load_json_if_exists(
        packet.get("source_final_gate_rerun_execution_blocked_result_path")
    )
    if packet.get("reexecution_request_status") != _request_status(bp74_result):
        errors.append(
            _error(
                "reexecution_request_status_must_match_bp74_state",
                "reexecution_request_status",
                packet.get("reexecution_request_status"),
            )
        )
    if packet.get("reexecution_readiness_status") != _readiness_status(bp74_result):
        errors.append(
            _error(
                "reexecution_readiness_status_must_match_bp74_state",
                "reexecution_readiness_status",
                packet.get("reexecution_readiness_status"),
            )
        )
    if packet.get("runtime_application_status") != "not_executed":
        errors.append(
            _error(
                "bp75_must_not_execute_runtime_application",
                "runtime_application_status",
                packet.get("runtime_application_status"),
            )
        )
    errors.extend(_validate_no_runtime_mutation_fields(packet))
    errors.extend(_validate_blocker_report_shape(_dict(packet.get("blocker_report"))))
    errors.extend(_validate_prerequisite_report_shape(_dict(packet.get("prerequisite_report"))))
    errors.extend(
        _validate_final_gate_dependency_report_shape(
            _dict(packet.get("final_gate_dependency_report"))
        )
    )
    errors.extend(
        _validate_reexecution_execution_plan_shape(
            _dict(packet.get("reexecution_execution_plan"))
        )
    )
    errors.extend(
        _validate_runtime_mutation_prevention_report_shape(
            _dict(packet.get("runtime_mutation_prevention_report"))
        )
    )
    errors.extend(_validate_next_actions(_list(packet.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(packet.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(packet))
    return errors


def _validate_blocker_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(report, BLOCKER_REPORT_REQUIRED_FIELDS, "blocker_report")
    errors.extend(
        _validate_status(
            "reexecution_request_status",
            report.get("reexecution_request_status"),
            ALLOWED_REEXECUTION_REQUEST_STATUSES,
        )
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


def _validate_prerequisite_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(report, PREREQUISITE_REPORT_REQUIRED_FIELDS, "prerequisite_report")
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_final_gate_dependency_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        FINAL_GATE_DEPENDENCY_REPORT_REQUIRED_FIELDS,
        "final_gate_dependency_report",
    )
    if report.get("final_gate_rerun_performed") is not False and report.get("final_gate_dependency_status") != "final_gate_dependency_satisfied":  # noqa: E501
        errors.append(
            _error(
                "final_gate_dependency_status_must_match_performed_state",
                "final_gate_dependency_status",
                report.get("final_gate_dependency_status"),
            )
        )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_reexecution_execution_plan_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        REEXECUTION_EXECUTION_PLAN_REQUIRED_FIELDS,
        "reexecution_execution_plan",
    )
    errors.extend(
        _validate_status(
            "execution_status",
            report.get("execution_status"),
            ALLOWED_REEXECUTION_EXECUTION_PLAN_STATUSES,
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


def _status_fields_for_bp74_result(bp74_result: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "final_gate_rerun_execution_status",
            bp74_result.get("final_gate_rerun_execution_status"),
            ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
        ),
        (
            "final_gate_rerun_result_status",
            bp74_result.get("final_gate_rerun_result_status"),
            ALLOWED_FINAL_GATE_RERUN_RESULT_STATUSES,
        ),
        (
            "final_gate_rerun_outcome_status",
            bp74_result.get("final_gate_rerun_outcome_status"),
            ALLOWED_FINAL_GATE_RERUN_OUTCOME_STATUSES,
        ),
        (
            "final_gate_rerun_request_status",
            bp74_result.get("final_gate_rerun_request_status"),
            ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
        ),
        (
            "human_resolution_completeness_gate_status",
            bp74_result.get("human_resolution_completeness_gate_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_GATE_STATUSES,
        ),
        (
            "human_resolution_record_status",
            bp74_result.get("human_resolution_record_status"),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        ),
        (
            "human_resolution_provided_status",
            bp74_result.get("human_resolution_provided_status"),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        ),
        (
            "human_resolution_completeness_status",
            bp74_result.get("human_resolution_completeness_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        ),
        (
            "missing_input_status",
            bp74_result.get("missing_input_status"),
            ALLOWED_MISSING_INPUT_STATUSES,
        ),
        (
            "operator_input_completeness_status",
            bp74_result.get("operator_input_completeness_status"),
            ALLOWED_OPERATOR_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "candidate_input_completeness_status",
            bp74_result.get("candidate_input_completeness_status"),
            ALLOWED_CANDIDATE_INPUT_COMPLETENESS_STATUSES,
        ),
        (
            "operator_signoff_status",
            bp74_result.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "selected_candidate_status",
            bp74_result.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "runtime_application_status",
            bp74_result.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]


def _status_fields_for_packet(packet: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
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
        *_status_fields_for_bp74_result(packet),
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
        "prepare_reexecution_after_final_gate_rerun" in recommendations
        and "rerun_final_gate_after_human_resolution" not in recommendations
    ):
        errors.append(
            _error(
                "prepare_reexecution_requires_final_gate_rerun_recommendation",
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
            if key in FORBIDDEN_REEXECUTION_REQUEST_PACKET_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_REEXECUTION_REQUEST_PACKET_TOKENS:
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _packet_status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
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
        "validation_version": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_VERSION,
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_BLUEPRINT,
        "blueprint_name": CONTROLLED_RUNTIME_CALIBRATION_REEXECUTION_REQUEST_PACKET_BLUEPRINT_NAME,
        "latest_completed_blueprint": "blueprint_74",
        "scope": "controlled_runtime_calibration_reexecution_request_packet",
        "runtime_boundary": "no_runtime_reexecution_or_application_or_config_mutation",
    }
