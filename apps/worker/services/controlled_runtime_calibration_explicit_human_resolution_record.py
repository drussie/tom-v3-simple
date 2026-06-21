from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_human_resolution_provided_packet import (  # noqa: E501
    ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
    ALLOWED_FINAL_GATE_RERUN_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
    ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
    ALLOWED_MISSING_INPUT_STATUSES,
    ALLOWED_OPERATOR_ATTESTATION_STATUSES,
    ALLOWED_OPERATOR_IDENTITY_STATUSES,
    ALLOWED_OPERATOR_SIGNOFF_STATUSES,
    ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
    ALLOWED_REEXECUTION_READINESS_STATUSES,
    ALLOWED_RUNTIME_APPLICATION_STATUSES,
    ALLOWED_SELECTED_CANDIDATE_STATUSES,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PROVIDED_PACKET_CONTRACT_OUTPUT,  # noqa: E501
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PROVIDED_PACKET_OUTPUT,
    FORBIDDEN_HUMAN_RESOLUTION_PROVIDED_TOKENS,
    OPERATOR_REQUIRED_INPUT_FIELDS,
    SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS,
    _artifact_ref,
    _dict,
    _error,
    _explicit_ref,
    _list,
    _load_json,
    _load_json_if_exists,
    _missing_required,
    _now_utc,
    _path_string,
    _sha256_file,
    _stable_id,
    _unique_strings,
    _validate_status,
    _write_json_if_requested,
)
from apps.worker.services.controlled_runtime_calibration_human_resolution_provided_packet import (
    SOURCE_CONTRACT_REFS as BP70_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_TYPE = (
    "controlled_runtime_calibration_explicit_human_resolution_record_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUT_TYPE = (
    "controlled_runtime_calibration_explicit_human_resolution_record_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_TYPE = (
    "controlled_runtime_calibration_explicit_human_resolution_record"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_COMPLETENESS_REPORT_TYPE = (
    "controlled_runtime_calibration_human_resolution_record_completeness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_MISSING_INPUT_REPORT_TYPE = (
    "controlled_runtime_calibration_human_resolution_record_missing_input_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_FINAL_GATE_READINESS_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_human_resolution_record_final_gate_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_REEXECUTION_READINESS_REPORT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_human_resolution_record_reexecution_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_BLUEPRINT = "blueprint_71"
CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_explicit_human_resolution_record_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_explicit_human_resolution_record_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_explicit_human_resolution_record_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_explicit_human_resolution_record_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_explicit_human_resolution_record_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/controlled_runtime_calibration_explicit_human_resolution_record.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_COMPLETENESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_record_completeness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_MISSING_INPUT_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_record_missing_input_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_FINAL_GATE_READINESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_record_final_gate_readiness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_REEXECUTION_READINESS_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_human_resolution_record_reexecution_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_human_resolution_provided_packet_contract_version": "v1",
    **dict(BP70_SOURCE_CONTRACT_REFS),
}

ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES = [
    "human_resolution_record_pending_explicit_inputs",
    "human_resolution_record_created_with_complete_explicit_inputs",
    "human_resolution_record_created_with_partial_inputs",
    "human_resolution_record_invalid",
    "human_resolution_record_blocked",
    "human_resolution_record_not_applicable",
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

HUMAN_RESOLUTION_RECORD_INPUT_REQUIRED_FIELDS = [
    "human_resolution_record_input_id",
    "human_resolution_record_input_type",
    "human_resolution_record_input_version",
    "generated_at",
    "source_human_resolution_provided_packet_path",
    "source_human_resolution_provided_packet_contract_path",
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
    *OPERATOR_REQUIRED_INPUT_FIELDS,
    *SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS,
    "source_bp70_human_resolution_provided_packet_id",
    "source_bp70_human_resolution_provided_status",
    "source_bp70_human_resolution_completeness_status",
    "source_bp70_missing_input_status",
    "source_bp69_human_resolution_packet_id",
    "source_bp69_human_resolution_status",
    "source_bp68_selected_candidate_artifact_id",
    "source_bp68_selected_candidate_artifact_status",
    "source_bp67_signoff_artifact_id",
    "source_bp67_signoff_artifact_status",
    "source_bp66_packet_id",
    "source_bp66_candidate_option_count",
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
HUMAN_RESOLUTION_RECORD_REQUIRED_FIELDS = [
    "human_resolution_record_id",
    "human_resolution_record_type",
    "human_resolution_record_version",
    "generated_at",
    "source_human_resolution_record_input_path",
    "source_human_resolution_provided_packet_path",
    "source_human_resolution_input_packet_path",
    "source_explicit_selected_candidate_artifact_path",
    "source_explicit_operator_signoff_artifact_path",
    "source_operator_signoff_candidate_selection_packet_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "candidate_option_refs",
    "candidate_option_count",
    "operator_identity_ref",
    "operator_signoff_timestamp",
    "operator_attestation_text",
    "operator_scope_acknowledgement",
    "selected_candidate_config_ref",
    "selected_candidate_id",
    "selected_candidate_version",
    "selected_candidate_source_path",
    "selected_candidate_selection_reason",
    "candidate_selection_timestamp",
    "operator_reference_for_selection",
    "human_resolution_record_status",
    "human_resolution_provided_status",
    "human_resolution_completeness_status",
    "missing_input_status",
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
    "completeness_report",
    "missing_input_report",
    "final_gate_readiness",
    "reexecution_readiness",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]
COMPLETENESS_REPORT_REQUIRED_FIELDS = [
    "completeness_report_id",
    "completeness_report_version",
    "generated_at",
    "source_human_resolution_record_id",
    "human_resolution_record_status",
    "human_resolution_completeness_status",
    "human_resolution_provided_status",
    "completeness_checks",
    "warnings",
    "non_claims",
]
MISSING_INPUT_REPORT_REQUIRED_FIELDS = [
    "missing_input_report_id",
    "missing_input_report_version",
    "generated_at",
    "source_human_resolution_record_id",
    "missing_input_status",
    "missing_inputs",
    "operator_signoff_status",
    "selected_candidate_status",
    "candidate_option_count",
    "warnings",
    "non_claims",
]
FINAL_GATE_READINESS_REPORT_REQUIRED_FIELDS = [
    "final_gate_readiness_report_id",
    "final_gate_readiness_report_version",
    "generated_at",
    "source_human_resolution_record_id",
    "final_gate_rerun_status",
    "final_gate_rerun_readiness_status",
    "readiness_checks",
    "warnings",
    "non_claims",
]
REEXECUTION_READINESS_REPORT_REQUIRED_FIELDS = [
    "reexecution_readiness_report_id",
    "reexecution_readiness_report_version",
    "generated_at",
    "source_human_resolution_record_id",
    "reexecution_readiness_status",
    "readiness_checks",
    "runtime_application_status",
    "runtime_config_changed",
    "mutation_status",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "human_resolution_record_is_not_truth": True,
    "human_resolution_record_is_not_accuracy_scoring": True,
    "human_resolution_record_is_not_model_training": True,
    "human_resolution_record_is_not_runtime_application": True,
    "human_resolution_record_does_not_execute_application": True,
    "human_resolution_record_does_not_rerun_final_gate": True,
    "human_resolution_record_does_not_create_production_config": True,
    "human_resolution_record_does_not_modify_model_weights": True,
    "human_resolution_record_does_not_replace_baselines": True,
    "human_resolution_record_does_not_infer_operator_signoff": True,
    "human_resolution_record_does_not_infer_candidate_selection": True,
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
    "controlled_runtime_calibration_explicit_human_resolution_record": True,
    "human_resolution_record_pending_explicit_inputs": True,
    "human_resolution_not_provided": True,
    "human_resolution_incomplete": True,
    "required_human_inputs_missing": True,
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
FORBIDDEN_HUMAN_RESOLUTION_RECORD_TOKENS = set(FORBIDDEN_HUMAN_RESOLUTION_PROVIDED_TOKENS)


def export_controlled_runtime_calibration_explicit_human_resolution_record_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at or CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "human_resolution_record_scope": {
            "records_explicit_human_resolution_fields_when_supplied": True,
            "default_state_remains_pending_without_explicit_inputs": True,
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
        "human_resolution_record_input_schema": {
            "input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUT_TYPE
            ),
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUT_VERSION
            ),
            "required_fields": list(HUMAN_RESOLUTION_RECORD_INPUT_REQUIRED_FIELDS),
            "explicit_operator_fields": list(OPERATOR_REQUIRED_INPUT_FIELDS),
            "explicit_selected_candidate_fields": list(SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS),
        },
        "human_resolution_record_schema": {
            "record_type": CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_TYPE,
            "record_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
            ),
            "required_fields": list(HUMAN_RESOLUTION_RECORD_REQUIRED_FIELDS),
            "allowed_human_resolution_record_statuses": list(
                ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES
            ),
            "allowed_human_resolution_provided_statuses": list(
                ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES
            ),
            "allowed_human_resolution_completeness_statuses": list(
                ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES
            ),
            "allowed_missing_input_statuses": list(ALLOWED_MISSING_INPUT_STATUSES),
            "allowed_final_gate_rerun_readiness_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES
            ),
            "allowed_reexecution_readiness_statuses": list(ALLOWED_REEXECUTION_READINESS_STATUSES),
            "allowed_operator_signoff_statuses": list(ALLOWED_OPERATOR_SIGNOFF_STATUSES),
            "allowed_selected_candidate_statuses": list(ALLOWED_SELECTED_CANDIDATE_STATUSES),
            "allowed_next_action_recommendations": list(ALLOWED_NEXT_ACTION_RECOMMENDATIONS),
        },
        "operator_resolution_record_schema": {
            "required_explicit_fields": list(OPERATOR_REQUIRED_INPUT_FIELDS),
            "scope_acknowledgement_value": "acknowledged",
            "empty_defaults_do_not_create_signoff": True,
        },
        "selected_candidate_resolution_record_schema": {
            "required_explicit_fields": list(SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS),
            "candidate_ref_must_match_candidate_option": True,
            "candidate_option_count_does_not_create_selection": True,
            "single_candidate_option_does_not_create_selection": True,
        },
        "completeness_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_COMPLETENESS_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
            ),
            "required_fields": list(COMPLETENESS_REPORT_REQUIRED_FIELDS),
        },
        "missing_input_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_MISSING_INPUT_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
            ),
            "required_fields": list(MISSING_INPUT_REPORT_REQUIRED_FIELDS),
        },
        "final_gate_readiness_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_FINAL_GATE_READINESS_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
            ),
            "required_fields": list(FINAL_GATE_READINESS_REPORT_REQUIRED_FIELDS),
        },
        "reexecution_readiness_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_REEXECUTION_READINESS_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
            ),
            "required_fields": list(REEXECUTION_READINESS_REPORT_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_human_resolution_record_input_shape": True,
            "validate_human_resolution_record_shape": True,
            "validate_operator_resolution_record_shape": True,
            "validate_selected_candidate_resolution_record_shape": True,
            "validate_completeness_report_shape": True,
            "validate_missing_input_report_shape": True,
            "validate_final_gate_readiness_shape": True,
            "validate_reexecution_readiness_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_record_pending_without_explicit_inputs": True,
            "validate_final_gate_not_ready_without_complete_record": True,
            "validate_candidate_option_count_is_inventory_only": True,
            "validate_no_operator_signoff_inferred_from_validation_success": True,
            "validate_no_selected_candidate_inferred_from_candidate_inventory": True,
            "validate_no_human_resolution_inferred_from_prior_pending_artifacts": True,
            "validate_final_gate_rerun_not_executed": True,
            "validate_runtime_application_not_executed": True,
            "reject_forbidden_exact_tokens": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp70_human_resolution_provided_packet_path_required": True,
            "bp69_human_resolution_input_packet_path_required": True,
            "bp68_selected_candidate_artifact_path_required": True,
            "bp67_signoff_artifact_path_required": True,
            "bp66_packet_path_required": True,
            "bp65_resolution_packet_path_required": True,
            "bp64_review_packet_path_required": True,
            "bp62_execution_path_required": True,
            "candidate_options_preserved": True,
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


def build_controlled_runtime_calibration_explicit_human_resolution_record_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    source_human_resolution_provided_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PROVIDED_PACKET_OUTPUT
    ),
    source_human_resolution_provided_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_PROVIDED_PACKET_CONTRACT_OUTPUT
    ),
    explicit_operator_identity_ref: str | None = None,
    explicit_operator_signoff_timestamp: str | None = None,
    explicit_operator_attestation_text: str | None = None,
    explicit_operator_scope_acknowledgement: str | None = None,
    explicit_selected_candidate_ref: str | None = None,
    explicit_selected_candidate_id: str | None = None,
    explicit_selected_candidate_version: str | None = None,
    explicit_selected_candidate_source_path: str | None = None,
    explicit_selected_candidate_selection_reason: str | None = None,
    explicit_candidate_selection_timestamp: str | None = None,
    explicit_operator_reference_for_selection: str | None = None,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    bp70_packet = _load_json(source_human_resolution_provided_packet_path)
    explicit_candidate_ref = _explicit_ref(explicit_selected_candidate_ref)
    candidate_options = _list(bp70_packet.get("candidate_option_refs"))
    model_asset_ref = bp70_packet.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = bp70_packet.get("model_asset_sha256") or _sha256_file(
        Path(str(model_asset_ref))
    )
    inputs = {
        "human_resolution_record_input_id": _stable_id(
            "controlled_runtime_calibration_explicit_human_resolution_record_inputs_v1",
            bp70_packet.get("human_resolution_provided_packet_id"),
            explicit_operator_identity_ref,
            explicit_operator_signoff_timestamp,
            explicit_candidate_ref,
            explicit_candidate_selection_timestamp,
        ),
        "human_resolution_record_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUT_TYPE
        ),
        "human_resolution_record_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_provided_packet_path": str(
            Path(source_human_resolution_provided_packet_path)
        ),
        "source_human_resolution_provided_packet_contract_path": str(
            Path(source_human_resolution_provided_packet_contract_path)
        ),
        "source_human_resolution_input_packet_path": bp70_packet.get(
            "source_human_resolution_input_packet_path"
        ),
        "source_explicit_selected_candidate_artifact_path": bp70_packet.get(
            "source_explicit_selected_candidate_artifact_path"
        ),
        "source_explicit_operator_signoff_artifact_path": bp70_packet.get(
            "source_explicit_operator_signoff_artifact_path"
        ),
        "source_operator_signoff_candidate_selection_packet_path": bp70_packet.get(
            "source_operator_signoff_candidate_selection_packet_path"
        ),
        "source_blocked_execution_resolution_packet_path": bp70_packet.get(
            "source_blocked_execution_resolution_packet_path"
        ),
        "source_application_execution_review_packet_path": bp70_packet.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": bp70_packet.get("source_application_execution_path"),
        "source_pre_application_final_gate_path": bp70_packet.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": bp70_packet.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": bp70_packet.get("source_application_plan_path"),
        "source_human_approval_gate_path": bp70_packet.get("source_human_approval_gate_path"),
        "source_change_request_path": bp70_packet.get("source_change_request_path"),
        "candidate_option_refs": candidate_options,
        "explicit_operator_identity_ref": explicit_operator_identity_ref,
        "explicit_operator_signoff_timestamp": explicit_operator_signoff_timestamp,
        "explicit_operator_attestation_text": explicit_operator_attestation_text,
        "explicit_operator_scope_acknowledgement": explicit_operator_scope_acknowledgement,
        "explicit_selected_candidate_ref": explicit_candidate_ref,
        "explicit_selected_candidate_id": explicit_selected_candidate_id,
        "explicit_selected_candidate_version": explicit_selected_candidate_version,
        "explicit_selected_candidate_source_path": explicit_selected_candidate_source_path,
        "explicit_selected_candidate_selection_reason": (
            explicit_selected_candidate_selection_reason
        ),
        "explicit_candidate_selection_timestamp": explicit_candidate_selection_timestamp,
        "explicit_operator_reference_for_selection": explicit_operator_reference_for_selection,
        "source_bp70_human_resolution_provided_packet_id": bp70_packet.get(
            "human_resolution_provided_packet_id"
        ),
        "source_bp70_human_resolution_provided_status": bp70_packet.get(
            "human_resolution_provided_status"
        ),
        "source_bp70_human_resolution_completeness_status": bp70_packet.get(
            "human_resolution_completeness_status"
        ),
        "source_bp70_missing_input_status": bp70_packet.get("missing_input_status"),
        "source_bp69_human_resolution_packet_id": bp70_packet.get(
            "source_bp69_human_resolution_packet_id"
        ),
        "source_bp69_human_resolution_status": bp70_packet.get(
            "source_bp69_human_resolution_status"
        ),
        "source_bp68_selected_candidate_artifact_id": bp70_packet.get(
            "source_bp68_selected_candidate_artifact_id"
        ),
        "source_bp68_selected_candidate_artifact_status": bp70_packet.get(
            "source_bp68_selected_candidate_artifact_status"
        ),
        "source_bp67_signoff_artifact_id": bp70_packet.get("source_bp67_signoff_artifact_id"),
        "source_bp67_signoff_artifact_status": bp70_packet.get(
            "source_bp67_signoff_artifact_status"
        ),
        "source_bp66_packet_id": bp70_packet.get("source_bp66_packet_id"),
        "source_bp66_candidate_option_count": bp70_packet.get("source_bp66_candidate_option_count"),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(bp70_packet.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": bp70_packet.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": bp70_packet.get("runtime_config_target_sha256_after"),
        "runtime_config_changed": bool(bp70_packet.get("runtime_config_changed")),
        "mutation_status": bp70_packet.get("mutation_status"),
        "runtime_application_status": bp70_packet.get("runtime_application_status"),
        "production_config_status": bp70_packet.get("production_config_status"),
        "baseline_update_status": bp70_packet.get("baseline_update_status"),
        "model_update_status": bp70_packet.get("model_update_status"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": {
            "human_resolution_provided_packet": _artifact_ref(
                source_human_resolution_provided_packet_path,
                bp70_packet,
            ),
            "human_resolution_provided_packet_contract": _artifact_ref(
                source_human_resolution_provided_packet_contract_path,
                _load_json_if_exists(source_human_resolution_provided_packet_contract_path),
            ),
            "human_resolution_input_packet": _artifact_ref(
                bp70_packet.get("source_human_resolution_input_packet_path"),
                _load_json_if_exists(bp70_packet.get("source_human_resolution_input_packet_path")),
            ),
            "explicit_selected_candidate_artifact": _artifact_ref(
                bp70_packet.get("source_explicit_selected_candidate_artifact_path"),
                _load_json_if_exists(
                    bp70_packet.get("source_explicit_selected_candidate_artifact_path")
                ),
            ),
            "explicit_operator_signoff_artifact": _artifact_ref(
                bp70_packet.get("source_explicit_operator_signoff_artifact_path"),
                _load_json_if_exists(
                    bp70_packet.get("source_explicit_operator_signoff_artifact_path")
                ),
            ),
            "operator_signoff_candidate_selection_packet": _artifact_ref(
                bp70_packet.get("source_operator_signoff_candidate_selection_packet_path"),
                _load_json_if_exists(
                    bp70_packet.get("source_operator_signoff_candidate_selection_packet_path")
                ),
            ),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": ("completed" if not errors else "invalid_human_resolution_record_inputs"),
        "human_resolution_record_input_id": inputs["human_resolution_record_input_id"],
        **_status_snapshot_from_inputs(inputs),
        "candidate_option_count": len(candidate_options),
        "next_action_recommendation": _next_actions(inputs),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_explicit_human_resolution_record_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(human_resolution_record_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_explicit_human_resolution_record_inputs_validation"
        ),
        payload_path=human_resolution_record_inputs_path,
        payload_type=inputs.get("human_resolution_record_input_type"),
        payload_version=inputs.get("human_resolution_record_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot_from_inputs(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_explicit_human_resolution_record(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(human_resolution_record_inputs_path)
    record_id = _stable_id(
        "controlled_runtime_calibration_explicit_human_resolution_record_v1",
        inputs.get("human_resolution_record_input_id"),
        inputs.get("source_bp70_human_resolution_provided_packet_id"),
        inputs.get("source_bp69_human_resolution_packet_id"),
        inputs.get("source_bp68_selected_candidate_artifact_id"),
        inputs.get("source_bp67_signoff_artifact_id"),
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    missing_inputs = _missing_human_resolution_inputs(inputs)
    record = {
        "human_resolution_record_id": record_id,
        "human_resolution_record_type": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_TYPE
        ),
        "human_resolution_record_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_record_input_path": str(Path(human_resolution_record_inputs_path)),
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
        "operator_identity_ref": inputs.get("explicit_operator_identity_ref"),
        "operator_signoff_timestamp": inputs.get("explicit_operator_signoff_timestamp"),
        "operator_attestation_text": inputs.get("explicit_operator_attestation_text"),
        "operator_scope_acknowledgement": inputs.get("explicit_operator_scope_acknowledgement"),
        "selected_candidate_config_ref": _dict(inputs.get("explicit_selected_candidate_ref"))
        or None,
        "selected_candidate_id": inputs.get("explicit_selected_candidate_id"),
        "selected_candidate_version": inputs.get("explicit_selected_candidate_version"),
        "selected_candidate_source_path": inputs.get("explicit_selected_candidate_source_path"),
        "selected_candidate_selection_reason": inputs.get(
            "explicit_selected_candidate_selection_reason"
        ),
        "candidate_selection_timestamp": inputs.get("explicit_candidate_selection_timestamp"),
        "operator_reference_for_selection": inputs.get("explicit_operator_reference_for_selection"),
        "source_bp70_human_resolution_provided_packet_id": inputs.get(
            "source_bp70_human_resolution_provided_packet_id"
        ),
        "source_bp70_human_resolution_provided_status": inputs.get(
            "source_bp70_human_resolution_provided_status"
        ),
        "source_bp70_human_resolution_completeness_status": inputs.get(
            "source_bp70_human_resolution_completeness_status"
        ),
        "source_bp70_missing_input_status": inputs.get("source_bp70_missing_input_status"),
        "source_bp69_human_resolution_packet_id": inputs.get(
            "source_bp69_human_resolution_packet_id"
        ),
        "source_bp69_human_resolution_status": inputs.get("source_bp69_human_resolution_status"),
        "source_bp68_selected_candidate_artifact_id": inputs.get(
            "source_bp68_selected_candidate_artifact_id"
        ),
        "source_bp68_selected_candidate_artifact_status": inputs.get(
            "source_bp68_selected_candidate_artifact_status"
        ),
        "source_bp67_signoff_artifact_id": inputs.get("source_bp67_signoff_artifact_id"),
        "source_bp67_signoff_artifact_status": inputs.get("source_bp67_signoff_artifact_status"),
        "source_bp66_packet_id": inputs.get("source_bp66_packet_id"),
        "source_bp66_candidate_option_count": inputs.get("source_bp66_candidate_option_count"),
        "human_resolution_record_status": _human_resolution_record_status(inputs),
        "human_resolution_provided_status": _human_resolution_provided_status(inputs),
        "human_resolution_completeness_status": _human_resolution_completeness_status(inputs),
        "missing_input_status": _missing_input_status(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "candidate_selection_validation_status": _candidate_selection_validation_status(inputs),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "final_gate_rerun_readiness_status": _final_gate_rerun_readiness_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get("runtime_config_target_sha256_before"),
        "runtime_config_target_sha256_after": inputs.get("runtime_config_target_sha256_after"),
        "runtime_config_changed": bool(inputs.get("runtime_config_changed")),
        "mutation_status": inputs.get("mutation_status"),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "missing_inputs": missing_inputs,
        "completeness_report": _completeness_report(record_id, inputs, generated_at),
        "missing_input_report": _missing_input_report(record_id, inputs, generated_at),
        "final_gate_readiness": _final_gate_readiness(record_id, inputs, generated_at),
        "reexecution_readiness": _reexecution_readiness(record_id, inputs, generated_at),
        "next_action_recommendation": _next_actions(inputs),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_inputs_shape(inputs))
    errors.extend(_validate_human_resolution_record_shape(record))
    _write_json_if_requested(output_path, record)
    return {
        "ok": not errors,
        "status": ("completed" if not errors else "invalid_human_resolution_record"),
        "human_resolution_record_id": record["human_resolution_record_id"],
        **_status_snapshot(record),
        "candidate_option_count": record["candidate_option_count"],
        "next_action_recommendation": record["next_action_recommendation"],
        "human_resolution_record_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_explicit_human_resolution_record(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    record = _load_json(human_resolution_record_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_shape(record))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_explicit_human_resolution_record_validation"
        ),
        payload_path=human_resolution_record_path,
        payload_type=record.get("human_resolution_record_type"),
        payload_version=record.get("human_resolution_record_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(record),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_human_resolution_record_completeness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_COMPLETENESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    record = _load_json(human_resolution_record_path)
    report = {
        **_dict(record.get("completeness_report")),
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_COMPLETENESS_REPORT_TYPE
        ),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_record_path": str(Path(human_resolution_record_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_shape(record))
    errors.extend(_validate_completeness_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_completeness_report",
        "completeness_report_id": report.get("completeness_report_id"),
        "human_resolution_record_status": report.get("human_resolution_record_status"),
        "human_resolution_completeness_status": report.get("human_resolution_completeness_status"),
        "human_resolution_record_completeness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_human_resolution_record_missing_input_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_MISSING_INPUT_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    record = _load_json(human_resolution_record_path)
    report = {
        **_dict(record.get("missing_input_report")),
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_MISSING_INPUT_REPORT_TYPE
        ),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_record_path": str(Path(human_resolution_record_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_shape(record))
    errors.extend(_validate_missing_input_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_missing_input_report",
        "missing_input_report_id": report.get("missing_input_report_id"),
        "missing_input_status": report.get("missing_input_status"),
        "human_resolution_record_missing_input_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_human_resolution_record_final_gate_readiness_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_FINAL_GATE_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    record = _load_json(human_resolution_record_path)
    report = {
        **_dict(record.get("final_gate_readiness")),
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_FINAL_GATE_READINESS_REPORT_TYPE
        ),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_record_path": str(Path(human_resolution_record_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_shape(record))
    errors.extend(_validate_final_gate_readiness_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_final_gate_readiness_report",
        "final_gate_readiness_report_id": report.get("final_gate_readiness_report_id"),
        "final_gate_rerun_status": report.get("final_gate_rerun_status"),
        "final_gate_rerun_readiness_status": report.get("final_gate_rerun_readiness_status"),
        "human_resolution_record_final_gate_readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_human_resolution_record_reexecution_readiness_report(  # noqa: E501
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_OUTPUT
    ),
    human_resolution_record_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_REEXECUTION_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    record = _load_json(human_resolution_record_path)
    report = {
        **_dict(record.get("reexecution_readiness")),
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_RESOLUTION_RECORD_REEXECUTION_READINESS_REPORT_TYPE
        ),
        "exported_at": generated_at.isoformat(),
        "source_human_resolution_record_path": str(Path(human_resolution_record_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_human_resolution_record_shape(record))
    errors.extend(_validate_reexecution_readiness_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_reexecution_readiness_report",
        "reexecution_readiness_report_id": report.get("reexecution_readiness_report_id"),
        "reexecution_readiness_status": report.get("reexecution_readiness_status"),
        "runtime_application_status": report.get("runtime_application_status"),
        "human_resolution_record_reexecution_readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _completeness_report(
    record_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "completeness_report_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_record_completeness_report_v1",
            record_id,
        ),
        "completeness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_record_id": record_id,
        "human_resolution_record_status": _human_resolution_record_status(inputs),
        "human_resolution_completeness_status": _human_resolution_completeness_status(inputs),
        "human_resolution_provided_status": _human_resolution_provided_status(inputs),
        "completeness_checks": {
            "explicit_human_resolution_required": True,
            "operator_signoff_explicitly_recorded": _operator_signoff_status(inputs)
            == "operator_signoff_explicitly_recorded",
            "operator_identity_explicitly_recorded": _operator_identity_status(inputs)
            == "operator_identity_explicitly_recorded",
            "operator_timestamp_explicitly_recorded": _operator_timestamp_status(inputs)
            == "operator_timestamp_explicitly_recorded",
            "operator_attestation_explicitly_recorded": _operator_attestation_status(inputs)
            == "operator_attestation_explicitly_recorded",
            "selected_candidate_explicitly_recorded": _selected_candidate_status(inputs)
            == "selected_candidate_explicitly_recorded",
            "candidate_selection_validation_completed": (
                _candidate_selection_validation_status(inputs)
                == "candidate_selection_valid_explicit_candidate"
            ),
            "candidate_option_count_does_not_create_selection": True,
            "human_resolution_explicitly_provided": _human_resolution_provided_status(inputs)
            == "human_resolution_explicitly_provided",
        },
        "missing_inputs": _missing_human_resolution_inputs(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _missing_input_report(
    record_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "missing_input_report_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_record_missing_input_report_v1",
            record_id,
        ),
        "missing_input_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_record_id": record_id,
        "missing_input_status": _missing_input_status(inputs),
        "missing_inputs": _missing_human_resolution_inputs(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "candidate_option_count": len(_list(inputs.get("candidate_option_refs"))),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_readiness(
    record_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "final_gate_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_record_final_gate_readiness_report_v1",
            record_id,
        ),
        "final_gate_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_record_id": record_id,
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "final_gate_rerun_readiness_status": _final_gate_rerun_readiness_status(inputs),
        "readiness_checks": {
            "explicit_human_resolution_required": True,
            "explicit_human_resolution_record_complete": _human_resolution_record_status(inputs)
            == "human_resolution_record_created_with_complete_explicit_inputs",
            "final_gate_not_rerun_by_bp71": True,
            "runtime_application_not_executed_by_bp71": True,
            "runtime_config_unchanged": not bool(inputs.get("runtime_config_changed")),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _reexecution_readiness(
    record_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "reexecution_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_human_resolution_record_reexecution_readiness_report_v1",
            record_id,
        ),
        "reexecution_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_resolution_record_id": record_id,
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "readiness_checks": {
            "human_resolution_record_complete": _human_resolution_record_status(inputs)
            == "human_resolution_record_created_with_complete_explicit_inputs",
            "final_gate_rerun_ready": _final_gate_rerun_readiness_status(inputs)
            == "final_gate_rerun_ready_after_human_resolution",
            "final_gate_rerun_not_executed_by_bp71": True,
            "runtime_application_not_executed_by_bp71": True,
            "runtime_config_unchanged": not bool(inputs.get("runtime_config_changed")),
        },
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_changed": bool(inputs.get("runtime_config_changed")),
        "mutation_status": inputs.get("mutation_status"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _human_resolution_record_status(payload: dict[str, Any]) -> str:
    human_status = _human_resolution_provided_status(payload)
    if human_status == "human_resolution_invalid":
        return "human_resolution_record_invalid"
    if human_status == "human_resolution_explicitly_provided":
        return "human_resolution_record_created_with_complete_explicit_inputs"
    if _operator_input_started(payload) or _selected_candidate_input_started(payload):
        return "human_resolution_record_created_with_partial_inputs"
    return "human_resolution_record_pending_explicit_inputs"


def _human_resolution_provided_status(payload: dict[str, Any]) -> str:
    operator_status = _operator_signoff_status(payload)
    selected_status = _selected_candidate_status(payload)
    if operator_status == "operator_signoff_invalid" or selected_status == (
        "selected_candidate_invalid"
    ):
        return "human_resolution_invalid"
    if (
        operator_status == "operator_signoff_explicitly_recorded"
        and selected_status == "selected_candidate_explicitly_recorded"
    ):
        return "human_resolution_explicitly_provided"
    if _operator_input_started(payload) or _selected_candidate_input_started(payload):
        return "human_resolution_partially_provided"
    return "human_resolution_not_provided"


def _operator_signoff_status(payload: dict[str, Any]) -> str:
    if not _operator_input_started(payload):
        return "operator_signoff_required"
    if (
        _operator_identity_status(payload) != "operator_identity_explicitly_recorded"
        or _operator_timestamp_status(payload) != "operator_timestamp_explicitly_recorded"
        or _operator_attestation_status(payload) != "operator_attestation_explicitly_recorded"
    ):
        return "operator_signoff_invalid"
    return "operator_signoff_explicitly_recorded"


def _operator_attestation_status(payload: dict[str, Any]) -> str:
    if not payload.get("explicit_operator_attestation_text"):
        return "operator_attestation_required"
    if payload.get("explicit_operator_scope_acknowledgement") != "acknowledged":
        return "operator_attestation_invalid"
    return "operator_attestation_explicitly_recorded"


def _operator_identity_status(payload: dict[str, Any]) -> str:
    if not payload.get("explicit_operator_identity_ref"):
        return "operator_identity_required"
    return "operator_identity_explicitly_recorded"


def _operator_timestamp_status(payload: dict[str, Any]) -> str:
    if not payload.get("explicit_operator_signoff_timestamp"):
        return "operator_timestamp_required"
    return "operator_timestamp_explicitly_recorded"


def _selected_candidate_status(payload: dict[str, Any]) -> str:
    if not _selected_candidate_input_started(payload):
        return "selected_candidate_required"
    if _candidate_selection_validation_status(payload) != (
        "candidate_selection_valid_explicit_candidate"
    ):
        return "selected_candidate_invalid"
    return "selected_candidate_explicitly_recorded"


def _candidate_selection_validation_status(payload: dict[str, Any]) -> str:
    explicit_ref = _dict(payload.get("explicit_selected_candidate_ref"))
    if not _selected_candidate_input_started(payload):
        return "candidate_selection_pending_explicit_input"
    if not explicit_ref:
        return "candidate_selection_invalid_missing_ref"
    errors = _validate_explicit_selected_candidate_input(payload)
    error_codes = {str(error.get("code")) for error in errors}
    if "invalid_explicit_selected_candidate_ref" in error_codes:
        return "candidate_selection_invalid_unknown_candidate"
    if errors:
        return "candidate_selection_invalid_missing_provenance"
    return "candidate_selection_valid_explicit_candidate"


def _human_resolution_completeness_status(payload: dict[str, Any]) -> str:
    provided_status = _human_resolution_provided_status(payload)
    if provided_status == "human_resolution_explicitly_provided":
        return "human_resolution_complete"
    if provided_status == "human_resolution_invalid":
        return "human_resolution_invalid_inputs"
    operator_missing = _operator_signoff_status(payload) != "operator_signoff_explicitly_recorded"
    candidate_missing = (
        _selected_candidate_status(payload) != "selected_candidate_explicitly_recorded"
    )
    if operator_missing and not candidate_missing:
        return "human_resolution_missing_operator_inputs"
    if candidate_missing and not operator_missing:
        return "human_resolution_missing_candidate_inputs"
    return "human_resolution_incomplete"


def _missing_input_status(payload: dict[str, Any]) -> str:
    missing_inputs = _missing_human_resolution_inputs(payload)
    if not missing_inputs:
        return "no_required_inputs_missing"
    operator_missing = any(item.get("input_group") == "operator" for item in missing_inputs)
    candidate_missing = any(
        item.get("input_group") == "selected_candidate" for item in missing_inputs
    )
    if operator_missing and candidate_missing:
        return "required_human_inputs_missing"
    if operator_missing:
        return "operator_inputs_missing"
    return "candidate_inputs_missing"


def _final_gate_rerun_status(payload: dict[str, Any]) -> str:
    if _human_resolution_provided_status(payload) == "human_resolution_invalid":
        return "final_gate_rerun_blocked_invalid_human_resolution"
    return "final_gate_rerun_required"


def _final_gate_rerun_readiness_status(payload: dict[str, Any]) -> str:
    human_status = _human_resolution_provided_status(payload)
    if human_status == "human_resolution_invalid":
        return "final_gate_rerun_blocked_invalid_human_resolution"
    if human_status == "human_resolution_explicitly_provided":
        return "final_gate_rerun_ready_after_human_resolution"
    return "final_gate_rerun_not_ready_missing_human_resolution"


def _reexecution_readiness_status(payload: dict[str, Any]) -> str:
    if _operator_signoff_status(payload) != "operator_signoff_explicitly_recorded":
        return "reexecution_not_ready_blockers_unresolved"
    if _selected_candidate_status(payload) != "selected_candidate_explicitly_recorded":
        return "reexecution_not_ready_blockers_unresolved"
    if _human_resolution_provided_status(payload) == "human_resolution_explicitly_provided":
        return "reexecution_blocked_final_gate_not_rerun"
    return "reexecution_not_ready_blockers_unresolved"


def _next_actions(payload: dict[str, Any]) -> list[str]:
    if _human_resolution_provided_status(payload) == "human_resolution_explicitly_provided":
        return [
            "rerun_final_gate_after_human_resolution",
            "prepare_final_gate_rerun_blueprint",
        ]
    actions: list[str] = ["provide_human_resolution_inputs"]
    if _operator_signoff_status(payload) != "operator_signoff_explicitly_recorded":
        actions.append("provide_operator_inputs")
    if _selected_candidate_status(payload) != "selected_candidate_explicitly_recorded":
        actions.append("provide_selected_candidate_inputs")
    if _human_resolution_provided_status(payload) != "human_resolution_explicitly_provided":
        actions.append("provide_operator_signoff_and_selected_candidate")
    actions.append("rerun_final_gate_after_human_resolution")
    return _unique_strings(actions)


def _missing_human_resolution_inputs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    for field in OPERATOR_REQUIRED_INPUT_FIELDS:
        value = payload.get(field)
        is_missing = value != "acknowledged" if field.endswith("acknowledgement") else not value
        if is_missing:
            missing.append({"input_group": "operator", "field": field, "status": "required"})
    for field in SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS:
        value = _dict(payload.get(field)) if field.endswith("_ref") else payload.get(field)
        if not value:
            missing.append(
                {"input_group": "selected_candidate", "field": field, "status": "required"}
            )
    return missing


def _operator_input_started(payload: dict[str, Any]) -> bool:
    return any(bool(payload.get(field)) for field in OPERATOR_REQUIRED_INPUT_FIELDS)


def _selected_candidate_input_started(payload: dict[str, Any]) -> bool:
    return any(
        bool(_dict(payload.get(field)) if field.endswith("_ref") else payload.get(field))
        for field in SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS
    )


def _matched_candidate_option(payload: dict[str, Any]) -> dict[str, Any] | None:
    explicit_ref = _dict(payload.get("explicit_selected_candidate_ref"))
    if not explicit_ref:
        return None
    explicit_tokens = _candidate_ref_tokens(explicit_ref)
    for option in _list(payload.get("candidate_option_refs")):
        option_dict = _dict(option)
        if explicit_tokens & _candidate_ref_tokens(option_dict):
            return option_dict
    return None


def _candidate_ref_tokens(ref: dict[str, Any]) -> set[str]:
    tokens: set[str] = set()
    for key in [
        "ref",
        "path",
        "source_path",
        "candidate_id",
        "candidate_config_freeze_id",
        "candidate_packet_id",
        "candidate_version",
        "candidate_config_freeze_version",
    ]:
        value = ref.get(key)
        if value:
            tokens.add(str(value))
    return tokens


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "human_resolution_record_scope",
        "source_contract_refs",
        "human_resolution_record_input_schema",
        "human_resolution_record_schema",
        "operator_resolution_record_schema",
        "selected_candidate_resolution_record_schema",
        "completeness_report_schema",
        "missing_input_report_schema",
        "final_gate_readiness_schema",
        "reexecution_readiness_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_human_resolution_record_inputs_shape(
    inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        inputs,
        HUMAN_RESOLUTION_RECORD_INPUT_REQUIRED_FIELDS,
        "human_resolution_record_inputs",
    )
    errors.extend(_validate_blocked_runtime_state(inputs))
    errors.extend(_validate_explicit_operator_input(inputs))
    errors.extend(_validate_explicit_selected_candidate_input(inputs))
    for field, value, allowed in _status_fields_for_inputs(inputs):
        errors.extend(_validate_status(field, value, allowed))
    errors.extend(_validate_next_actions(_next_actions(inputs)))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_human_resolution_record_shape(record: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        record,
        HUMAN_RESOLUTION_RECORD_REQUIRED_FIELDS,
        "human_resolution_record",
    )
    for field, value, allowed in _status_fields_for_record(record):
        errors.extend(_validate_status(field, value, allowed))
    if record.get(
        "human_resolution_record_status"
    ) == "human_resolution_record_created_with_complete_explicit_inputs" and record.get(
        "missing_inputs"
    ):
        errors.append(
            _error(
                "complete_human_resolution_record_with_missing_inputs",
                "missing_inputs",
                record.get("missing_inputs"),
            )
        )
    if (
        record.get("final_gate_rerun_readiness_status")
        == "final_gate_rerun_ready_after_human_resolution"
        and record.get("human_resolution_record_status")
        != "human_resolution_record_created_with_complete_explicit_inputs"
    ):
        errors.append(
            _error(
                "final_gate_readiness_requires_complete_record",
                "final_gate_rerun_readiness_status",
                record.get("final_gate_rerun_readiness_status"),
            )
        )
    errors.extend(_validate_blocked_runtime_state(record))
    errors.extend(_validate_completeness_report_shape(_dict(record.get("completeness_report"))))
    errors.extend(_validate_missing_input_report_shape(_dict(record.get("missing_input_report"))))
    errors.extend(
        _validate_final_gate_readiness_report_shape(_dict(record.get("final_gate_readiness")))
    )
    errors.extend(
        _validate_reexecution_readiness_report_shape(_dict(record.get("reexecution_readiness")))
    )
    errors.extend(_validate_next_actions(_list(record.get("next_action_recommendation"))))
    errors.extend(_validate_non_claims(_dict(record.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(record))
    return errors


def _validate_explicit_operator_input(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if not _operator_input_started(payload):
        return []
    if _operator_signoff_status(payload) == "operator_signoff_explicitly_recorded":
        return []
    return [
        _error(
            "invalid_explicit_operator_resolution_input",
            "operator_resolution_input",
            _operator_signoff_status(payload),
        )
    ]


def _validate_explicit_selected_candidate_input(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not _selected_candidate_input_started(payload):
        return errors
    explicit_ref = _dict(payload.get("explicit_selected_candidate_ref"))
    if not explicit_ref:
        errors.append(
            _error(
                "missing_explicit_selected_candidate_ref",
                "explicit_selected_candidate_ref",
                payload.get("explicit_selected_candidate_ref"),
            )
        )
        return errors
    if not _matched_candidate_option(payload):
        errors.append(
            _error(
                "invalid_explicit_selected_candidate_ref",
                "explicit_selected_candidate_ref",
                payload.get("explicit_selected_candidate_ref"),
            )
        )
    for field in SELECTED_CANDIDATE_REQUIRED_INPUT_FIELDS:
        if field == "explicit_selected_candidate_ref":
            continue
        if not payload.get(field):
            errors.append(_error("missing_explicit_candidate_provenance", field, None))
    return errors


def _validate_blocked_runtime_state(payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if payload.get("runtime_config_changed") is not False:
        errors.append(
            _error(
                "runtime_config_changed_must_remain_false",
                "runtime_config_changed",
                payload.get("runtime_config_changed"),
            )
        )
    if payload.get("mutation_status") != "no_runtime_mutation_due_to_blocker":
        errors.append(
            _error(
                "mutation_status_must_remain_blocked",
                "mutation_status",
                payload.get("mutation_status"),
            )
        )
    if payload.get("runtime_application_status") not in {
        "not_executed",
        "blocked_from_runtime_application",
    }:
        errors.append(
            _error(
                "runtime_application_status_must_remain_not_executed",
                "runtime_application_status",
                payload.get("runtime_application_status"),
            )
        )
    if payload.get("model_update_status") != "not_modified":
        errors.append(
            _error(
                "model_update_status_must_remain_not_modified",
                "model_update_status",
                payload.get("model_update_status"),
            )
        )
    if payload.get("production_config_status") != "not_created":
        errors.append(
            _error(
                "production_config_status_must_remain_not_created",
                "production_config_status",
                payload.get("production_config_status"),
            )
        )
    if payload.get("baseline_update_status") != "not_replaced":
        errors.append(
            _error(
                "baseline_update_status_must_remain_not_replaced",
                "baseline_update_status",
                payload.get("baseline_update_status"),
            )
        )
    before = payload.get("runtime_config_target_sha256_before")
    after = payload.get("runtime_config_target_sha256_after")
    if before and after and before != after:
        errors.append(
            _error(
                "runtime_config_hashes_must_match_for_pending_artifact",
                "runtime_config_target_sha256_after",
                after,
            )
        )
    return errors


def _validate_completeness_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(report, COMPLETENESS_REPORT_REQUIRED_FIELDS, "completeness_report")
    errors.extend(
        _validate_status(
            "human_resolution_record_status",
            report.get("human_resolution_record_status"),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "human_resolution_completeness_status",
            report.get("human_resolution_completeness_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "human_resolution_provided_status",
            report.get("human_resolution_provided_status"),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        )
    )
    return errors


def _validate_missing_input_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(report, MISSING_INPUT_REPORT_REQUIRED_FIELDS, "missing_input_report")
    errors.extend(
        _validate_status(
            "missing_input_status",
            report.get("missing_input_status"),
            ALLOWED_MISSING_INPUT_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            report.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "selected_candidate_status",
            report.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        )
    )
    return errors


def _validate_final_gate_readiness_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        FINAL_GATE_READINESS_REPORT_REQUIRED_FIELDS,
        "final_gate_readiness_report",
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            report.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_readiness_status",
            report.get("final_gate_rerun_readiness_status"),
            ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
        )
    )
    return errors


def _validate_reexecution_readiness_report_shape(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        report,
        REEXECUTION_READINESS_REPORT_REQUIRED_FIELDS,
        "reexecution_readiness_report",
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            report.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "runtime_application_status",
            report.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        )
    )
    return errors


def _status_fields_for_inputs(payload: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "human_resolution_record_status",
            _human_resolution_record_status(payload),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        ),
        (
            "human_resolution_provided_status",
            _human_resolution_provided_status(payload),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        ),
        (
            "human_resolution_completeness_status",
            _human_resolution_completeness_status(payload),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        ),
        ("missing_input_status", _missing_input_status(payload), ALLOWED_MISSING_INPUT_STATUSES),
        (
            "operator_signoff_status",
            _operator_signoff_status(payload),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "operator_attestation_status",
            _operator_attestation_status(payload),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        ),
        (
            "operator_identity_status",
            _operator_identity_status(payload),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        ),
        (
            "operator_timestamp_status",
            _operator_timestamp_status(payload),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        ),
        (
            "selected_candidate_status",
            _selected_candidate_status(payload),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "candidate_selection_validation_status",
            _candidate_selection_validation_status(payload),
            ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
        ),
        (
            "final_gate_rerun_status",
            _final_gate_rerun_status(payload),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        ),
        (
            "final_gate_rerun_readiness_status",
            _final_gate_rerun_readiness_status(payload),
            ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            _reexecution_readiness_status(payload),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "runtime_application_status",
            payload.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        ),
    ]


def _status_fields_for_record(record: dict[str, Any]) -> list[tuple[str, Any, list[str]]]:
    return [
        (
            "human_resolution_record_status",
            record.get("human_resolution_record_status"),
            ALLOWED_HUMAN_RESOLUTION_RECORD_STATUSES,
        ),
        (
            "human_resolution_provided_status",
            record.get("human_resolution_provided_status"),
            ALLOWED_HUMAN_RESOLUTION_PROVIDED_STATUSES,
        ),
        (
            "human_resolution_completeness_status",
            record.get("human_resolution_completeness_status"),
            ALLOWED_HUMAN_RESOLUTION_COMPLETENESS_STATUSES,
        ),
        (
            "missing_input_status",
            record.get("missing_input_status"),
            ALLOWED_MISSING_INPUT_STATUSES,
        ),
        (
            "operator_signoff_status",
            record.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        ),
        (
            "operator_attestation_status",
            record.get("operator_attestation_status"),
            ALLOWED_OPERATOR_ATTESTATION_STATUSES,
        ),
        (
            "operator_identity_status",
            record.get("operator_identity_status"),
            ALLOWED_OPERATOR_IDENTITY_STATUSES,
        ),
        (
            "operator_timestamp_status",
            record.get("operator_timestamp_status"),
            ALLOWED_OPERATOR_TIMESTAMP_STATUSES,
        ),
        (
            "selected_candidate_status",
            record.get("selected_candidate_status"),
            ALLOWED_SELECTED_CANDIDATE_STATUSES,
        ),
        (
            "candidate_selection_validation_status",
            record.get("candidate_selection_validation_status"),
            ALLOWED_CANDIDATE_SELECTION_VALIDATION_STATUSES,
        ),
        (
            "final_gate_rerun_status",
            record.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        ),
        (
            "final_gate_rerun_readiness_status",
            record.get("final_gate_rerun_readiness_status"),
            ALLOWED_FINAL_GATE_RERUN_READINESS_STATUSES,
        ),
        (
            "reexecution_readiness_status",
            record.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        ),
        (
            "runtime_application_status",
            record.get("runtime_application_status"),
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
            if key in FORBIDDEN_HUMAN_RESOLUTION_RECORD_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_HUMAN_RESOLUTION_RECORD_TOKENS:
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot_from_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "human_resolution_record_status": _human_resolution_record_status(inputs),
        "human_resolution_provided_status": _human_resolution_provided_status(inputs),
        "human_resolution_completeness_status": _human_resolution_completeness_status(inputs),
        "missing_input_status": _missing_input_status(inputs),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "operator_attestation_status": _operator_attestation_status(inputs),
        "operator_identity_status": _operator_identity_status(inputs),
        "operator_timestamp_status": _operator_timestamp_status(inputs),
        "selected_candidate_status": _selected_candidate_status(inputs),
        "candidate_selection_validation_status": _candidate_selection_validation_status(inputs),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "final_gate_rerun_readiness_status": _final_gate_rerun_readiness_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_changed": inputs.get("runtime_config_changed"),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
    }


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "human_resolution_record_status",
        "human_resolution_provided_status",
        "human_resolution_completeness_status",
        "missing_input_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_VERSION
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_EXPLICIT_HUMAN_RESOLUTION_RECORD_BLUEPRINT_NAME
        ),
        "latest_completed_blueprint": "blueprint_70",
        "scope": "controlled_runtime_calibration_explicit_human_resolution_record",
        "runtime_boundary": "no_runtime_application_or_config_mutation",
    }
