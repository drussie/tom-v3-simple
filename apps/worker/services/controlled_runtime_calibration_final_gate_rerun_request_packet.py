from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT,
    FORBIDDEN_HUMAN_RESOLUTION_COMPLETENESS_GATE_TOKENS,
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
    _validate_completeness_gate_shape,
    _validate_status,
    _write_json_if_requested,
)
from apps.worker.services.controlled_runtime_calibration_human_resolution_completeness_gate import (  # noqa: E501
    SOURCE_CONTRACT_REFS as BP72_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_request_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_request_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_request_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_BLOCKER_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_request_blocker_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_prerequisite_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PLAN_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_execution_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_DEPENDENCY_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_rerun_reexecution_dependency_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_BLUEPRINT = "blueprint_73"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_final_gate_rerun_request_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_final_gate_rerun_request_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_request_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_request_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_final_gate_rerun_request_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_request_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_BLOCKER_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_request_blocker_report.current.json"
)
DEFAULT_BP73_FINAL_GATE_RERUN_PREREQUISITE_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_request_prerequisite_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PLAN_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_final_gate_rerun_execution_plan.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_DEPENDENCY_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_rerun_reexecution_dependency_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_human_resolution_completeness_gate_contract_version": "v1",
    **dict(BP72_SOURCE_CONTRACT_REFS),
}

ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES = [
    "final_gate_rerun_request_blocked_missing_human_resolution",
    "final_gate_rerun_request_blocked_invalid_human_resolution",
    "final_gate_rerun_request_blocked_missing_operator_signoff",
    "final_gate_rerun_request_blocked_missing_selected_candidate",
    "final_gate_rerun_request_created_not_ready",
    "final_gate_rerun_request_ready_after_human_resolution",
    "final_gate_rerun_request_created_with_warnings",
    "final_gate_rerun_request_informational_only",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES = [
    "final_gate_rerun_not_executed",
    "final_gate_rerun_blocked",
    "final_gate_rerun_execution_deferred_to_future_blueprint",
    "not_applicable",
]
ALLOWED_BP73_FINAL_GATE_RERUN_READINESS_STATUSES = [
    "final_gate_rerun_not_ready_missing_human_resolution",
    "final_gate_rerun_ready_after_human_resolution",
    "final_gate_rerun_blocked_invalid_human_resolution",
    "final_gate_rerun_not_executed",
    "not_applicable",
]
ALLOWED_BP73_REEXECUTION_READINESS_STATUSES = [
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
    "prepare_final_gate_rerun_execution_blueprint",
    "no_runtime_action_recommended",
    "not_applicable",
]

RERUN_REQUEST_INPUT_REQUIRED_FIELDS = [
    "final_gate_rerun_request_input_id",
    "final_gate_rerun_request_input_type",
    "final_gate_rerun_request_input_version",
    "generated_at",
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
RERUN_REQUEST_PACKET_REQUIRED_FIELDS = [
    "final_gate_rerun_request_packet_id",
    "final_gate_rerun_request_packet_type",
    "final_gate_rerun_request_packet_version",
    "generated_at",
    "source_final_gate_rerun_request_input_path",
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
    "candidate_option_count",
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
    "final_gate_rerun_execution_status",
    "reexecution_readiness_status",
    "runtime_application_status",
    "runtime_config_changed",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "blocker_report",
    "prerequisite_report",
    "final_gate_rerun_execution_plan",
    "reexecution_dependency_report",
    "next_action_recommendation",
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
    "source_final_gate_rerun_request_packet_id",
    "final_gate_rerun_request_status",
    "blocker_status",
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
    "source_final_gate_rerun_request_packet_id",
    "final_gate_rerun_request_status",
    "prerequisites",
    "prerequisite_count",
    "satisfied_prerequisite_count",
    "unsatisfied_prerequisite_count",
    "warnings",
    "non_claims",
]
EXECUTION_PLAN_REQUIRED_FIELDS = [
    "final_gate_rerun_execution_plan_id",
    "final_gate_rerun_execution_plan_type",
    "final_gate_rerun_execution_plan_version",
    "generated_at",
    "source_final_gate_rerun_request_packet_id",
    "execution_status",
    "required_artifacts",
    "required_checks",
    "future_execution_command_placeholder",
    "warnings",
    "non_claims",
]
REEXECUTION_DEPENDENCY_REPORT_REQUIRED_FIELDS = [
    "reexecution_dependency_report_id",
    "reexecution_dependency_report_type",
    "reexecution_dependency_report_version",
    "generated_at",
    "source_final_gate_rerun_request_packet_id",
    "reexecution_readiness_status",
    "dependencies",
    "dependency_count",
    "satisfied_dependency_count",
    "unsatisfied_dependency_count",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "final_gate_rerun_request_packet_is_not_truth": True,
    "final_gate_rerun_request_packet_is_not_accuracy_scoring": True,
    "final_gate_rerun_request_packet_is_not_model_training": True,
    "final_gate_rerun_request_packet_is_not_runtime_application": True,
    "final_gate_rerun_request_packet_does_not_execute_runtime_application": True,
    "final_gate_rerun_request_packet_does_not_rerun_final_gate": True,
    "final_gate_rerun_request_packet_does_not_create_production_config": True,
    "final_gate_rerun_request_packet_does_not_modify_model_weights": True,
    "final_gate_rerun_request_packet_does_not_replace_baselines": True,
    "final_gate_rerun_request_packet_does_not_infer_operator_signoff": True,
    "final_gate_rerun_request_packet_does_not_infer_candidate_selection": True,
    "final_gate_rerun_request_packet_does_not_infer_human_resolution": True,
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
    "controlled_runtime_calibration_final_gate_rerun_request_packet": True,
    "final_gate_rerun_request_blocked_missing_human_resolution": True,
    "human_resolution_completeness_gate_not_ready": True,
    "human_resolution_record_pending_explicit_inputs": True,
    "human_resolution_not_provided": True,
    "human_resolution_incomplete": True,
    "required_human_inputs_missing": True,
    "operator_inputs_incomplete": True,
    "candidate_inputs_incomplete": True,
    "operator_signoff_required": True,
    "selected_candidate_required": True,
    "candidate_option_discovery_is_not_selection": True,
    "final_gate_rerun_not_ready_missing_human_resolution": True,
    "final_gate_rerun_not_executed": True,
    "reexecution_not_ready_blockers_unresolved": True,
    "runtime_application_not_executed": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "classifier_correctness_not_assessed": True,
    **NON_CLAIMS,
}
FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS = {
    *FORBIDDEN_HUMAN_RESOLUTION_COMPLETENESS_GATE_TOKENS,
    "accuracy",
    "precision",
    "recall",
    "f1",
    "auc",
    "classifier_accuracy_claim",
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
}


def export_controlled_runtime_calibration_final_gate_rerun_request_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "final_gate_rerun_request_scope": {
            "creates_future_final_gate_rerun_request_packet": True,
            "default_state_remains_blocked_without_complete_human_resolution": True,
            "bp72_completeness_gate_is_authoritative_source_for_readiness": True,
            "candidate_option_discovery_is_inventory_only": True,
            "single_candidate_option_does_not_create_selection": True,
            "does_not_infer_operator_signoff": True,
            "does_not_infer_candidate_selection": True,
            "does_not_infer_human_resolution": True,
            "does_not_execute_final_gate_rerun": True,
            "does_not_write_runtime_config": True,
            "does_not_execute_runtime_application": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "rerun_request_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUT_TYPE,  # noqa: E501
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUT_VERSION
            ),
            "required_fields": list(RERUN_REQUEST_INPUT_REQUIRED_FIELDS),
        },
        "rerun_request_packet_schema": {
            "packet_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_TYPE,
            "packet_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
            ),
            "required_fields": list(RERUN_REQUEST_PACKET_REQUIRED_FIELDS),
            "allowed_final_gate_rerun_request_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES
            ),
            "allowed_final_gate_rerun_execution_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES
            ),
            "allowed_final_gate_rerun_readiness_statuses": list(
                ALLOWED_BP73_FINAL_GATE_RERUN_READINESS_STATUSES
            ),
            "allowed_reexecution_readiness_statuses": list(
                ALLOWED_BP73_REEXECUTION_READINESS_STATUSES
            ),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "blocker_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_BLOCKER_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
            ),
            "required_fields": list(BLOCKER_REPORT_REQUIRED_FIELDS),
        },
        "prerequisite_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_TYPE,  # noqa: E501
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
            ),
            "required_fields": list(PREREQUISITE_REPORT_REQUIRED_FIELDS),
        },
        "execution_plan_schema": {
            "plan_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PLAN_TYPE,
            "plan_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
            ),
            "required_fields": list(EXECUTION_PLAN_REQUIRED_FIELDS),
        },
        "reexecution_dependency_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_DEPENDENCY_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
            ),
            "required_fields": list(REEXECUTION_DEPENDENCY_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_rerun_request_input_shape": True,
            "validate_rerun_request_packet_shape": True,
            "validate_blocker_report_shape": True,
            "validate_prerequisite_report_shape": True,
            "validate_final_gate_rerun_execution_plan_shape": True,
            "validate_reexecution_dependency_report_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_blocked_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_request_blocked_unless_bp72_gate_ready": True,
            "validate_final_gate_rerun_not_executed_by_bp73": True,
            "validate_runtime_application_not_executed_by_bp73": True,
            "validate_no_operator_signoff_is_inferred": True,
            "validate_no_selected_candidate_is_inferred_from_candidate_inventory": True,
            "validate_no_human_resolution_is_inferred": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_request_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp72_human_resolution_completeness_gate_path_required": True,
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


def build_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    source_human_resolution_completeness_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_OUTPUT
    ),
    source_human_resolution_completeness_gate_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_COMPLETENESS_GATE_CONTRACT_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    gate = _load_json(source_human_resolution_completeness_gate_path)
    model_asset_ref = gate.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = gate.get("model_asset_sha256") or _sha256_file(Path(model_asset_ref))
    inputs = {
        "final_gate_rerun_request_input_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_request_packet_inputs_v1",
            gate.get("human_resolution_completeness_gate_id"),
            gate.get("human_resolution_completeness_gate_status"),
            gate.get("human_resolution_record_status"),
            gate.get("human_resolution_completeness_status"),
            gate.get("missing_input_status"),
            gate.get("runtime_config_target_sha256_before"),
            gate.get("runtime_config_target_sha256_after"),
        ),
        "final_gate_rerun_request_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUT_TYPE
        ),
        "final_gate_rerun_request_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_completeness_gate_path": str(
            Path(source_human_resolution_completeness_gate_path)
        ),
        "source_explicit_human_resolution_record_path": gate.get(
            "source_explicit_human_resolution_record_path"
        ),
        "source_human_resolution_provided_packet_path": gate.get(
            "source_human_resolution_provided_packet_path"
        ),
        "source_human_resolution_input_packet_path": gate.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": gate.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": gate.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": gate.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": gate.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": gate.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": gate.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": gate.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": gate.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": gate.get("source_application_plan_path"),
        "source_human_approval_gate_path": gate.get("source_human_approval_gate_path"),
        "source_change_request_path": gate.get("source_change_request_path"),
        "candidate_option_refs": _list(gate.get("candidate_option_refs")),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(gate.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": gate.get("runtime_config_target_sha256_before"),
        "runtime_config_target_sha256_after": gate.get("runtime_config_target_sha256_after"),
        "runtime_config_changed": bool(gate.get("runtime_config_changed")),
        "mutation_status": gate.get("mutation_status") or "no_runtime_mutation_due_to_blocker",
        "runtime_application_status": gate.get("runtime_application_status") or "not_executed",
        "production_config_status": gate.get("production_config_status") or "not_created",
        "baseline_update_status": gate.get("baseline_update_status") or "not_replaced",
        "model_update_status": gate.get("model_update_status") or "not_modified",
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            source_human_resolution_completeness_gate_path,
            source_human_resolution_completeness_gate_contract_path,
            gate,
        ),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_rerun_request_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_rerun_request_inputs",
        "final_gate_rerun_request_input_id": inputs["final_gate_rerun_request_input_id"],
        **_status_snapshot_from_inputs(inputs),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "next_action_recommendation": _next_actions_from_inputs(inputs),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_final_gate_rerun_request_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(final_gate_rerun_request_packet_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_rerun_request_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_final_gate_rerun_request_packet_inputs_validation"
        ),
        payload_path=final_gate_rerun_request_packet_inputs_path,
        payload_type=inputs.get("final_gate_rerun_request_input_type"),
        payload_version=inputs.get("final_gate_rerun_request_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot_from_inputs(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_final_gate_rerun_request_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(final_gate_rerun_request_packet_inputs_path)
    gate = _source_gate(inputs)
    packet_id = _stable_id(
        "controlled_runtime_calibration_final_gate_rerun_request_packet_v1",
        inputs.get("final_gate_rerun_request_input_id"),
        gate.get("human_resolution_completeness_gate_id"),
        gate.get("human_resolution_completeness_gate_status"),
        gate.get("final_gate_rerun_readiness_status"),
        gate.get("runtime_config_target_sha256_before"),
        gate.get("runtime_config_target_sha256_after"),
    )
    blocker_report = _blocker_report(packet_id, gate, inputs, generated_at)
    prerequisite_report = _prerequisite_report(packet_id, gate, inputs, generated_at)
    execution_plan = _execution_plan(packet_id, gate, inputs, generated_at)
    reexecution_dependency_report = _reexecution_dependency_report(
        packet_id,
        gate,
        inputs,
        generated_at,
    )
    packet = {
        "final_gate_rerun_request_packet_id": packet_id,
        "final_gate_rerun_request_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_TYPE
        ),
        "final_gate_rerun_request_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_input_path": str(
            Path(final_gate_rerun_request_packet_inputs_path)
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
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "final_gate_rerun_request_status": _final_gate_rerun_request_status(gate),
        **_status_snapshot_from_gate(gate),
        "final_gate_rerun_execution_status": "final_gate_rerun_not_executed",
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
        "blocker_report": blocker_report,
        "prerequisite_report": prerequisite_report,
        "final_gate_rerun_execution_plan": execution_plan,
        "reexecution_dependency_report": reexecution_dependency_report,
        "next_action_recommendation": _next_actions_from_gate(gate),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_rerun_request_inputs_shape(inputs))
    errors.extend(_validate_rerun_request_packet_shape(packet))
    _write_json_if_requested(output_path, packet)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_rerun_request_packet",
        "final_gate_rerun_request_packet_id": packet["final_gate_rerun_request_packet_id"],
        **_status_snapshot(packet),
        "candidate_option_count": packet["candidate_option_count"],
        "next_action_recommendation": packet["next_action_recommendation"],
        "final_gate_rerun_request_packet_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_final_gate_rerun_request_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(final_gate_rerun_request_packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_rerun_request_packet_shape(packet))
    result = _validation_result(
        validation_type="controlled_runtime_calibration_final_gate_rerun_request_packet_validation",
        payload_path=final_gate_rerun_request_packet_path,
        payload_type=packet.get("final_gate_rerun_request_packet_type"),
        payload_version=packet.get("final_gate_rerun_request_packet_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(packet),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_final_gate_rerun_request_blocker_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_BLOCKER_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=final_gate_rerun_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="blocker_report",
        report_validator=_validate_blocker_report_shape,
        output_key="final_gate_rerun_request_blocker_report_output",
    )


def build_controlled_runtime_calibration_final_gate_rerun_prerequisite_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_BP73_FINAL_GATE_RERUN_PREREQUISITE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=final_gate_rerun_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="prerequisite_report",
        report_validator=_validate_prerequisite_report_shape,
        output_key="final_gate_rerun_prerequisite_report_output",
    )


def build_controlled_runtime_calibration_final_gate_rerun_execution_plan(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=final_gate_rerun_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="final_gate_rerun_execution_plan",
        report_validator=_validate_execution_plan_shape,
        output_key="final_gate_rerun_execution_plan_output",
    )


def build_controlled_runtime_calibration_final_gate_rerun_reexecution_dependency_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_OUTPUT
    ),
    final_gate_rerun_request_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_DEPENDENCY_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    return _export_embedded_report(
        contract_path=contract_path,
        packet_path=final_gate_rerun_request_packet_path,
        output_path=output_path,
        generated_at=generated_at,
        report_key="reexecution_dependency_report",
        report_validator=_validate_reexecution_dependency_report_shape,
        output_key="final_gate_rerun_reexecution_dependency_report_output",
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
        "source_final_gate_rerun_request_packet_path": str(Path(packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_rerun_request_packet_shape(packet))
    errors.extend(report_validator(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else f"invalid_{report_key}",
        "final_gate_rerun_request_packet_id": packet.get("final_gate_rerun_request_packet_id"),
        **_status_snapshot(packet),
        output_key: _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _source_artifact_refs(
    gate_path: str | Path,
    gate_contract_path: str | Path,
    gate: dict[str, Any],
) -> dict[str, Any]:
    refs = {
        "human_resolution_completeness_gate": _artifact_ref(gate_path, gate),
        "human_resolution_completeness_gate_contract": _artifact_ref(
            gate_contract_path,
            _load_json_if_exists(gate_contract_path),
        ),
    }
    refs.update(_dict(gate.get("source_artifact_refs")))
    return refs


def _source_gate(inputs: dict[str, Any]) -> dict[str, Any]:
    return _load_json_if_exists(inputs.get("source_human_resolution_completeness_gate_path"))


def _gate_ready(gate: dict[str, Any]) -> bool:
    return (
        gate.get("human_resolution_completeness_gate_status")
        == "human_resolution_completeness_gate_ready_for_final_gate_rerun"
        and gate.get("human_resolution_completeness_status") == "human_resolution_complete"
        and gate.get("missing_input_status") == "no_required_inputs_missing"
        and gate.get("operator_input_completeness_status") == "operator_inputs_complete"
        and gate.get("candidate_input_completeness_status") == "candidate_inputs_complete"
        and gate.get("final_gate_rerun_readiness_status")
        == "final_gate_rerun_ready_after_human_resolution"
    )


def _final_gate_rerun_request_status(gate: dict[str, Any]) -> str:
    if _gate_ready(gate):
        return "final_gate_rerun_request_ready_after_human_resolution"
    if gate.get("human_resolution_completeness_gate_status") in {
        "human_resolution_completeness_gate_blocked_invalid_record",
        "human_resolution_completeness_gate_ready_with_warnings",
    } or gate.get("final_gate_rerun_readiness_status") == (
        "final_gate_rerun_blocked_invalid_human_resolution"
    ):
        return "final_gate_rerun_request_blocked_invalid_human_resolution"
    if gate.get("human_resolution_completeness_status") != "human_resolution_complete":
        return "final_gate_rerun_request_blocked_missing_human_resolution"
    if gate.get("operator_input_completeness_status") != "operator_inputs_complete":
        return "final_gate_rerun_request_blocked_missing_operator_signoff"
    if gate.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        return "final_gate_rerun_request_blocked_missing_selected_candidate"
    return "final_gate_rerun_request_created_not_ready"


def _bp73_reexecution_readiness_status(gate: dict[str, Any]) -> str:
    if _gate_ready(gate):
        return "reexecution_blocked_final_gate_not_rerun"
    if gate.get("operator_input_completeness_status") != "operator_inputs_complete":
        return "reexecution_not_ready_blockers_unresolved"
    if gate.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        return "reexecution_not_ready_blockers_unresolved"
    return gate.get("reexecution_readiness_status") or "reexecution_not_ready_blockers_unresolved"


def _status_snapshot_from_gate(gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "human_resolution_completeness_gate_status": gate.get(
            "human_resolution_completeness_gate_status"
        ),
        "human_resolution_record_status": gate.get("human_resolution_record_status"),
        "human_resolution_provided_status": gate.get("human_resolution_provided_status"),
        "human_resolution_completeness_status": gate.get("human_resolution_completeness_status"),
        "missing_input_status": gate.get("missing_input_status"),
        "operator_input_completeness_status": gate.get("operator_input_completeness_status"),
        "candidate_input_completeness_status": gate.get("candidate_input_completeness_status"),
        "operator_signoff_status": gate.get("operator_signoff_status"),
        "selected_candidate_status": gate.get("selected_candidate_status"),
        "final_gate_rerun_readiness_status": gate.get("final_gate_rerun_readiness_status"),
        "reexecution_readiness_status": _bp73_reexecution_readiness_status(gate),
    }


def _status_snapshot_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    gate = _source_gate(inputs)
    return {
        "final_gate_rerun_request_status": _final_gate_rerun_request_status(gate),
        **_status_snapshot_from_gate(gate),
        "final_gate_rerun_execution_status": "final_gate_rerun_not_executed",
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_changed": inputs.get("runtime_config_changed"),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
    }


def _blocker_report(
    packet_id: str,
    gate: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    blockers = _blockers(gate, inputs)
    return {
        "blocker_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_request_blocker_report_v1",
            packet_id,
            _final_gate_rerun_request_status(gate),
            *[blocker["blocker_code"] for blocker in blockers],
        ),
        "blocker_report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_BLOCKER_REPORT_TYPE,  # noqa: E501
        "blocker_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet_id,
        "final_gate_rerun_request_status": _final_gate_rerun_request_status(gate),
        "blocker_status": "blockers_unresolved" if blockers else "no_blockers_detected",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blockers(gate: dict[str, Any], inputs: dict[str, Any]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    missing_entries = _list(_dict(gate.get("missing_input_matrix")).get("entries"))
    missing_fields = {str(entry.get("field")) for entry in missing_entries}
    field_to_code = {
        "operator_identity_ref": "missing_operator_identity",
        "operator_attestation_text": "missing_operator_attestation",
        "operator_signoff_timestamp": "missing_operator_timestamp",
        "operator_scope_acknowledgement": "missing_operator_scope_acknowledgement",
        "selected_candidate_config_ref": "missing_selected_candidate_ref",
        "selected_candidate_source_path": "missing_selected_candidate_source_path",
        "selected_candidate_selection_reason": "missing_selected_candidate_selection_reason",
        "candidate_selection_timestamp": "missing_candidate_selection_timestamp",
        "operator_reference_for_selection": "missing_operator_reference_for_selection",
    }
    for field, code in field_to_code.items():
        if field in missing_fields:
            blockers.append(
                {
                    "blocker_code": code,
                    "source_field": field,
                    "status": "required",
                    "source": "bp72_missing_input_matrix",
                }
            )
    if gate.get("human_resolution_completeness_gate_status") != (
        "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    ):
        blockers.append(
            {
                "blocker_code": "human_resolution_completeness_gate_not_ready",
                "source_field": "human_resolution_completeness_gate_status",
                "status": gate.get("human_resolution_completeness_gate_status"),
                "source": inputs.get("source_human_resolution_completeness_gate_path"),
            }
        )
    if gate.get("final_gate_rerun_readiness_status") != (
        "final_gate_rerun_ready_after_human_resolution"
    ):
        blockers.append(
            {
                "blocker_code": "final_gate_rerun_not_ready_missing_human_resolution",
                "source_field": "final_gate_rerun_readiness_status",
                "status": gate.get("final_gate_rerun_readiness_status"),
                "source": inputs.get("source_human_resolution_completeness_gate_path"),
            }
        )
    return blockers


def _prerequisite_report(
    packet_id: str,
    gate: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    prerequisites = [
        _prerequisite(
            "bp72_completeness_gate_ready",
            "BP72 completeness gate must be ready.",
            gate.get("human_resolution_completeness_gate_status")
            == "human_resolution_completeness_gate_ready_for_final_gate_rerun",
            gate.get("human_resolution_completeness_gate_status"),
        ),
        _prerequisite(
            "bp71_explicit_human_resolution_record_complete",
            "BP71 explicit human resolution record must be complete.",
            gate.get("human_resolution_record_status")
            == "human_resolution_record_created_with_complete_explicit_inputs",
            gate.get("human_resolution_record_status"),
        ),
        _prerequisite(
            "bp70_human_resolution_provided",
            "BP70 human resolution must be provided.",
            gate.get("human_resolution_provided_status") == "human_resolution_explicitly_provided",
            gate.get("human_resolution_provided_status"),
        ),
        _prerequisite(
            "bp69_human_resolution_input_explicit",
            "BP69 input must contain explicit operator and candidate fields.",
            gate.get("missing_input_status") == "no_required_inputs_missing",
            gate.get("missing_input_status"),
        ),
        _prerequisite(
            "bp68_selected_candidate_explicit",
            "BP68 selected candidate must be explicit.",
            gate.get("selected_candidate_status") == "selected_candidate_explicitly_recorded",
            gate.get("selected_candidate_status"),
        ),
        _prerequisite(
            "bp67_operator_signoff_explicit",
            "BP67 operator signoff must be explicit.",
            gate.get("operator_signoff_status") == "operator_signoff_explicitly_recorded",
            gate.get("operator_signoff_status"),
        ),
        _prerequisite(
            "future_blueprint_performs_final_gate_rerun",
            "Final gate rerun must be performed in a future blueprint.",
            False,
            "final_gate_rerun_not_executed",
        ),
        _prerequisite(
            "bp73_runtime_application_not_performed",
            "Runtime application must not be performed by BP73.",
            inputs.get("runtime_application_status") == "not_executed",
            inputs.get("runtime_application_status"),
        ),
    ]
    satisfied = sum(1 for item in prerequisites if item["satisfied"])
    return {
        "prerequisite_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_prerequisite_report_v1",
            packet_id,
            satisfied,
            len(prerequisites),
        ),
        "prerequisite_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_PREREQUISITE_REPORT_TYPE
        ),
        "prerequisite_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet_id,
        "final_gate_rerun_request_status": _final_gate_rerun_request_status(gate),
        "prerequisites": prerequisites,
        "prerequisite_count": len(prerequisites),
        "satisfied_prerequisite_count": satisfied,
        "unsatisfied_prerequisite_count": len(prerequisites) - satisfied,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _prerequisite(
    prerequisite_code: str,
    requirement: str,
    satisfied: bool,
    current_status: Any,
) -> dict[str, Any]:
    return {
        "prerequisite_code": prerequisite_code,
        "requirement": requirement,
        "satisfied": bool(satisfied),
        "current_status": current_status,
    }


def _execution_plan(
    packet_id: str,
    gate: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    execution_status = (
        "final_gate_rerun_execution_deferred_to_future_blueprint"
        if _gate_ready(gate)
        else "final_gate_rerun_not_executed"
    )
    return {
        "final_gate_rerun_execution_plan_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_execution_plan_v1",
            packet_id,
            execution_status,
            gate.get("human_resolution_completeness_gate_id"),
        ),
        "final_gate_rerun_execution_plan_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_EXECUTION_PLAN_TYPE
        ),
        "final_gate_rerun_execution_plan_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet_id,
        "execution_status": execution_status,
        "required_artifacts": [
            {
                "artifact": "human_resolution_completeness_gate",
                "path": inputs.get("source_human_resolution_completeness_gate_path"),
                "required_status": "human_resolution_completeness_gate_ready_for_final_gate_rerun",
                "current_status": gate.get("human_resolution_completeness_gate_status"),
            },
            {
                "artifact": "explicit_human_resolution_record",
                "path": inputs.get("source_explicit_human_resolution_record_path"),
                "required_status": "human_resolution_record_created_with_complete_explicit_inputs",
                "current_status": gate.get("human_resolution_record_status"),
            },
            {
                "artifact": "explicit_operator_signoff_artifact",
                "path": inputs.get("source_explicit_operator_signoff_artifact_path"),
                "required_status": "operator_signoff_explicitly_recorded",
                "current_status": gate.get("operator_signoff_status"),
            },
            {
                "artifact": "explicit_selected_candidate_artifact",
                "path": inputs.get("source_explicit_selected_candidate_artifact_path"),
                "required_status": "selected_candidate_explicitly_recorded",
                "current_status": gate.get("selected_candidate_status"),
            },
        ],
        "required_checks": [
            "runtime_config_unchanged_check_before_rerun",
            "no_model_weight_change_check",
            "no_baseline_replacement_check",
            "protected_sample_point_gate_check",
            "gameplay_gate_regression_check",
            "calibration_sandbox_regression_check",
        ],
        "future_execution_command_placeholder": (
            "future_blueprint_runs_pre_application_final_gate_after_complete_human_resolution"
        ),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _reexecution_dependency_report(
    packet_id: str,
    gate: dict[str, Any],
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    dependencies = [
        _dependency(
            "human_resolution_complete",
            gate.get("human_resolution_completeness_status") == "human_resolution_complete",
            gate.get("human_resolution_completeness_status"),
        ),
        _dependency(
            "operator_inputs_complete",
            gate.get("operator_input_completeness_status") == "operator_inputs_complete",
            gate.get("operator_input_completeness_status"),
        ),
        _dependency(
            "candidate_inputs_complete",
            gate.get("candidate_input_completeness_status") == "candidate_inputs_complete",
            gate.get("candidate_input_completeness_status"),
        ),
        _dependency(
            "future_final_gate_rerun_performed",
            False,
            "final_gate_rerun_not_executed",
        ),
        _dependency(
            "runtime_config_unchanged_before_reexecution",
            inputs.get("runtime_config_changed") is False,
            inputs.get("runtime_config_changed"),
        ),
        _dependency(
            "runtime_application_not_executed_by_bp73",
            inputs.get("runtime_application_status") == "not_executed",
            inputs.get("runtime_application_status"),
        ),
    ]
    satisfied = sum(1 for item in dependencies if item["satisfied"])
    return {
        "reexecution_dependency_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_reexecution_dependency_report_v1",
            packet_id,
            satisfied,
            len(dependencies),
        ),
        "reexecution_dependency_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REEXECUTION_DEPENDENCY_REPORT_TYPE
        ),
        "reexecution_dependency_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_rerun_request_packet_id": packet_id,
        "reexecution_readiness_status": _bp73_reexecution_readiness_status(gate),
        "dependencies": dependencies,
        "dependency_count": len(dependencies),
        "satisfied_dependency_count": satisfied,
        "unsatisfied_dependency_count": len(dependencies) - satisfied,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _dependency(
    dependency_code: str,
    satisfied: bool,
    current_status: Any,
) -> dict[str, Any]:
    return {
        "dependency_code": dependency_code,
        "satisfied": bool(satisfied),
        "current_status": current_status,
    }


def _next_actions_from_inputs(inputs: dict[str, Any]) -> list[str]:
    return _next_actions_from_gate(_source_gate(inputs))


def _next_actions_from_gate(gate: dict[str, Any]) -> list[str]:
    if _gate_ready(gate):
        return [
            "rerun_final_gate_after_human_resolution",
            "prepare_final_gate_rerun_execution_blueprint",
        ]
    actions: list[str] = []
    if gate.get("operator_input_completeness_status") != "operator_inputs_complete":
        actions.append("provide_operator_inputs")
    if gate.get("candidate_input_completeness_status") != "candidate_inputs_complete":
        actions.append("provide_selected_candidate_inputs")
    actions.append("provide_operator_signoff_and_selected_candidate")
    actions.append("rerun_final_gate_after_human_resolution")
    return _unique_strings(actions)


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "final_gate_rerun_request_scope",
        "source_contract_refs",
        "rerun_request_input_schema",
        "rerun_request_packet_schema",
        "blocker_report_schema",
        "prerequisite_report_schema",
        "execution_plan_schema",
        "reexecution_dependency_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_rerun_request_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, RERUN_REQUEST_INPUT_REQUIRED_FIELDS, "inputs")
    gate = _source_gate(inputs)
    errors.extend(_validate_completeness_gate_shape(gate))
    errors.extend(_validate_blocked_runtime_state(inputs))
    errors.extend(_validate_next_actions(_next_actions_from_inputs(inputs)))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_rerun_request_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(packet, RERUN_REQUEST_PACKET_REQUIRED_FIELDS, "packet")
    for field, value, allowed in _status_fields_for_packet(packet):
        errors.extend(_validate_status(field, value, allowed))
    if (
        packet.get("final_gate_rerun_request_status")
        == "final_gate_rerun_request_ready_after_human_resolution"
        and packet.get("human_resolution_completeness_gate_status")
        != "human_resolution_completeness_gate_ready_for_final_gate_rerun"
    ):
        errors.append(
            _error(
                "rerun_request_ready_requires_ready_bp72_gate",
                "human_resolution_completeness_gate_status",
                packet.get("human_resolution_completeness_gate_status"),
            )
        )
    if packet.get("final_gate_rerun_execution_status") != "final_gate_rerun_not_executed":
        errors.append(
            _error(
                "bp73_must_not_execute_final_gate_rerun",
                "final_gate_rerun_execution_status",
                packet.get("final_gate_rerun_execution_status"),
            )
        )
    if packet.get("runtime_application_status") != "not_executed":
        errors.append(
            _error(
                "bp73_must_not_execute_runtime_application",
                "runtime_application_status",
                packet.get("runtime_application_status"),
            )
        )
    errors.extend(_validate_blocked_runtime_state(packet))
    errors.extend(_validate_blocker_report_shape(_dict(packet.get("blocker_report"))))
    errors.extend(_validate_prerequisite_report_shape(_dict(packet.get("prerequisite_report"))))
    errors.extend(
        _validate_execution_plan_shape(_dict(packet.get("final_gate_rerun_execution_plan")))
    )
    errors.extend(
        _validate_reexecution_dependency_report_shape(
            _dict(packet.get("reexecution_dependency_report"))
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
            "final_gate_rerun_request_status",
            report.get("final_gate_rerun_request_status"),
            ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
        )
    )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_prerequisite_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(report, PREREQUISITE_REPORT_REQUIRED_FIELDS, "prerequisite_report")
    errors.extend(
        _validate_status(
            "final_gate_rerun_request_status",
            report.get("final_gate_rerun_request_status"),
            ALLOWED_FINAL_GATE_RERUN_REQUEST_STATUSES,
        )
    )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _validate_execution_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(plan, EXECUTION_PLAN_REQUIRED_FIELDS, "execution_plan")
    errors.extend(
        _validate_status(
            "execution_status",
            plan.get("execution_status"),
            ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
        )
    )
    errors.extend(_validate_no_forbidden_tokens(plan))
    return errors


def _validate_reexecution_dependency_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        REEXECUTION_DEPENDENCY_REPORT_REQUIRED_FIELDS,
        "reexecution_dependency_report",
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            report.get("reexecution_readiness_status"),
            ALLOWED_BP73_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(_validate_no_forbidden_tokens(report))
    return errors


def _status_fields_for_packet(packet: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
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
            "final_gate_rerun_readiness_status",
            packet.get("final_gate_rerun_readiness_status"),
            ALLOWED_BP73_FINAL_GATE_RERUN_READINESS_STATUSES,
        ),
        (
            "final_gate_rerun_execution_status",
            packet.get("final_gate_rerun_execution_status"),
            ALLOWED_FINAL_GATE_RERUN_EXECUTION_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            packet.get("reexecution_readiness_status"),
            ALLOWED_BP73_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "runtime_application_status",
            packet.get("runtime_application_status"),
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
            if key in FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif (
        isinstance(payload, str)
        and payload in FORBIDDEN_FINAL_GATE_RERUN_REQUEST_PACKET_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
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
        "final_gate_rerun_execution_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_VERSION
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_RERUN_REQUEST_PACKET_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_72",
        "scope": "controlled_runtime_calibration_final_gate_rerun_request_packet",
        "runtime_boundary": "no_final_gate_rerun_or_runtime_application_or_config_mutation",
    }
