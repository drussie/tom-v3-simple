from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.controlled_runtime_calibration_blocked_execution_resolution_packet import (  # noqa: E501
    CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)

CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_VERSION = (  # noqa: E501
    "v1"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUT_TYPE = (  # noqa: E501
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUT_VERSION = (  # noqa: E501
    "v1"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_TYPE = (
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION = (
    "v1"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_TYPE = (
    "controlled_runtime_calibration_operator_signoff_requirements"
)
CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_OPTIONS_TYPE = (
    "controlled_runtime_calibration_candidate_selection_options"
)
CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_VALIDATION_REPORT_TYPE = (
    "controlled_runtime_calibration_candidate_selection_validation_report"
)
CONTROLLED_RUNTIME_CALIBRATION_RESOLUTION_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_resolution_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_BLUEPRINT = (
    "blueprint_66"
)
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUTS_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT = (  # noqa: E501
    ".data/contracts/"
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_operator_signoff_candidate_selection_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_operator_signoff_requirements.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_OPTIONS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_candidate_selection_options.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_VALIDATION_REPORT_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_candidate_selection_validation_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RESOLUTION_READINESS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_resolution_readiness_report.current.json"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_application_execution_review_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_application_execution_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_pre_application_final_gate_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_runtime_application_staging_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_application_plan_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_human_approval_gate_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_dry_run_review_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_change_request_v1.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_OUTPUT = (
    ".data/contracts/calibration_candidate_config_freeze_v1.json"
)
DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT = (
    ".data/exports/calibration_candidate_manual_approval_packet.current.json"
)
DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT = (
    ".data/contracts/calibration_candidate_decision_packet_v1.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT = (
    ".data/contracts/real_broadcast_gameplay_calibration_decision_phase_freeze_v1.json"
)

CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_EXPORTED_AT = (
    datetime(2026, 6, 21, 0, 0, tzinfo=UTC)
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_blocked_execution_resolution_packet_contract_version": (  # noqa: E501
        CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_VERSION
    ),
    "controlled_runtime_calibration_application_execution_review_packet_contract_version": "v1",  # noqa: E501
    "controlled_runtime_calibration_application_execution_contract_version": "v1",
    "controlled_runtime_calibration_pre_application_final_gate_contract_version": "v1",
    "controlled_runtime_calibration_runtime_application_staging_contract_version": "v1",
    "controlled_runtime_calibration_application_plan_contract_version": "v1",
    "controlled_runtime_calibration_human_approval_gate_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_review_packet_contract_version": "v1",
    "controlled_runtime_calibration_dry_run_execution_contract_version": "v1",
    "controlled_runtime_calibration_change_request_contract_version": "v1",
    "calibration_candidate_config_freeze_contract_version": "v1",
    "calibration_candidate_decision_packet_contract_version": "v1",
    "real_broadcast_gameplay_calibration_decision_phase_freeze_version": "v1",
    "review_guided_gameplay_calibration_sandbox_regression_contract_version": "v1",
    "review_guided_gameplay_calibration_evaluation_sandbox_contract_version": "v1",
    "review_guided_gameplay_calibration_proposal_contract_version": "v1",
    "real_broadcast_gameplay_review_metrics_contract_version": "v1",
    "real_broadcast_gameplay_review_loop_contract_version": "v1",
    "real_broadcast_gameplay_corpus_run_contract_version": "v1",
    "gameplay_gate_review_dataset_export_contract_version": "v1",
    "gameplay_gate_pathway_completion_freeze_version": "v1",
    "gameplay_gate_regression_baseline_contract_version": "v1",
    "gameplay_segment_replay_review_contract_version": "v1",
    "gameplay_gated_many_point_smoke_contract_version": "v1",
    "gameplay_gated_perception_execution_contract_version": "v1",
    "gameplay_gated_pipeline_routing_contract_version": "v1",
    "gameplay_segment_gate_contract_version": "v1",
    "tom_v3_expansion_completion_freeze_version": "v1",
    "multi_point_regression_matrix_version": "v0",
    "point_manifest_version": "v0",
}

ALLOWED_PACKET_STATUSES = [
    "packet_created_pending_operator_signoff_and_candidate_selection",
    "packet_created_with_operator_signoff_pending_candidate_selection",
    "packet_created_with_candidate_selection_pending_operator_signoff",
    "packet_created_with_explicit_signoff_and_candidate_selection",
    "packet_created_with_warnings",
    "packet_blocked_missing_resolution_packet",
    "packet_blocked_missing_candidate_options",
    "packet_blocked_invalid_selected_candidate",
    "packet_blocked_invalid_operator_signoff",
    "packet_informational_only",
    "not_applicable",
]
ALLOWED_OPERATOR_SIGNOFF_STATUSES = [
    "operator_signoff_required",
    "operator_signoff_pending",
    "operator_signoff_explicitly_recorded",
    "operator_signoff_invalid",
    "operator_signoff_blocked",
    "operator_signoff_not_applicable",
    "not_applicable",
]
ALLOWED_CANDIDATE_SELECTION_STATUSES = [
    "selected_candidate_required",
    "candidate_selection_pending",
    "selected_candidate_explicitly_recorded",
    "selected_candidate_invalid",
    "candidate_selection_blocked",
    "candidate_selection_not_applicable",
    "not_applicable",
]
ALLOWED_FINAL_GATE_RERUN_STATUSES = [
    "final_gate_rerun_required",
    "final_gate_rerun_ready_after_signoff_and_candidate_selection",
    "final_gate_rerun_blocked_missing_operator_signoff",
    "final_gate_rerun_blocked_missing_selected_candidate",
    "final_gate_rerun_blocked_invalid_candidate",
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
    "provide_operator_signoff",
    "provide_selected_candidate",
    "provide_operator_signoff_and_selected_candidate",
    "rerun_final_gate_after_signoff_and_candidate_selection",
    "rerun_application_execution_after_final_gate_passes",
    "prepare_final_gate_rerun_blueprint",
    "no_runtime_action_recommended",
    "not_applicable",
]

PACKET_INPUT_REQUIRED_FIELDS = [
    "packet_input_id",
    "packet_input_type",
    "packet_input_version",
    "generated_at",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "source_candidate_config_freeze_path",
    "source_manual_approval_packet_path",
    "source_decision_packet_path",
    "source_phase_freeze_path",
    "candidate_option_refs",
    "explicit_selected_candidate_ref",
    "explicit_operator_signoff_ref",
    "explicit_operator_identity_ref",
    "explicit_operator_signoff_timestamp",
    "operator_notes_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "runtime_config_changed",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "source_resolution_packet_id",
    "source_review_packet_id",
    "source_contract_refs",
    "warnings",
    "non_claims",
]
PACKET_REQUIRED_FIELDS = [
    "packet_id",
    "packet_type",
    "packet_version",
    "generated_at",
    "source_packet_input_path",
    "source_blocked_execution_resolution_packet_path",
    "source_application_execution_review_packet_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "candidate_option_refs",
    "selected_candidate_config_ref",
    "operator_signoff_ref",
    "operator_identity_ref",
    "operator_signoff_timestamp",
    "operator_signoff_status",
    "candidate_selection_status",
    "final_gate_rerun_status",
    "reexecution_readiness_status",
    "runtime_config_changed",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "packet_status",
    "operator_signoff_requirements",
    "candidate_selection_options",
    "candidate_selection_validation",
    "final_gate_rerun_readiness",
    "reexecution_readiness",
    "next_action_recommendation",
    "warnings",
    "non_claims",
]
OPERATOR_SIGNOFF_REQUIREMENTS_REQUIRED_FIELDS = [
    "operator_signoff_requirements_id",
    "operator_signoff_requirements_version",
    "generated_at",
    "source_packet_id",
    "requirements",
    "operator_signoff_status",
    "warnings",
    "non_claims",
]
CANDIDATE_SELECTION_OPTIONS_REQUIRED_FIELDS = [
    "candidate_selection_options_id",
    "candidate_selection_options_version",
    "generated_at",
    "source_packet_id",
    "candidate_option_refs",
    "candidate_selection_status",
    "warnings",
    "non_claims",
]
CANDIDATE_SELECTION_VALIDATION_REQUIRED_FIELDS = [
    "candidate_selection_validation_id",
    "candidate_selection_validation_version",
    "generated_at",
    "source_packet_id",
    "selected_candidate_config_ref",
    "validation_checks",
    "candidate_selection_status",
    "warnings",
    "non_claims",
]
FINAL_GATE_RERUN_READINESS_REQUIRED_FIELDS = [
    "final_gate_rerun_readiness_id",
    "final_gate_rerun_readiness_version",
    "generated_at",
    "source_packet_id",
    "required_inputs",
    "required_regression_gates",
    "final_gate_rerun_status",
    "warnings",
    "non_claims",
]
REEXECUTION_READINESS_REQUIRED_FIELDS = [
    "reexecution_readiness_id",
    "reexecution_readiness_version",
    "generated_at",
    "source_packet_id",
    "required_inputs",
    "required_preconditions",
    "reexecution_readiness_status",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "operator_signoff_candidate_selection_packet_is_not_truth": True,
    "operator_signoff_candidate_selection_packet_is_not_accuracy_scoring": True,
    "operator_signoff_candidate_selection_packet_is_not_model_training": True,
    "operator_signoff_candidate_selection_packet_is_not_runtime_application": True,
    "packet_does_not_execute_application": True,
    "packet_does_not_rerun_final_gate": True,
    "packet_does_not_infer_operator_signoff": True,
    "packet_does_not_infer_candidate_selection": True,
    "operator_signoff_must_be_explicit": True,
    "selected_candidate_must_be_explicit": True,
    "controlled_runtime_config_update_not_performed": True,
    "runtime_config_unchanged_due_to_blocker": True,
    "classifier_not_modified": True,
    "classifier_correctness_not_assessed": True,
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
    "controlled_operator_signoff_candidate_selection_packet": True,
    "operator_signoff_required": True,
    "selected_candidate_required": True,
    "operator_signoff_pending": True,
    "candidate_selection_pending": True,
    "final_gate_rerun_required": True,
    "reexecution_not_ready_blockers_unresolved": True,
    "human_resolution_required": True,
    "no_runtime_mutation_due_to_blocker": True,
    "runtime_config_unchanged_due_to_blocker": True,
    **NON_CLAIMS,
}


def _forbidden_token(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_TOKENS = {
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
    _forbidden_token("model", "updated"),
    _forbidden_token("model", "weights", "modified"),
    _forbidden_token("baseline", "replaced"),
    _forbidden_token("auto", "approved"),
    _forbidden_token("auto", "rejected"),
    _forbidden_token("production", "config", "created"),
    _forbidden_token("uncontrolled", "runtime", "config", "update"),
    _forbidden_token("runtime", "application", "without", "final", "gate"),
    _forbidden_token("runtime", "application", "without", "rollback", "package"),
    _forbidden_token("runtime", "application", "without", "post", "apply", "verification"),
    _forbidden_token("fake", "operator", "signoff"),
    _forbidden_token("fake", "candidate", "selection"),
    _forbidden_token("inferred", "operator", "signoff"),
    _forbidden_token("inferred", "candidate", "selection"),
}


def export_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "packet_scope": {
            "records_operator_signoff_packet_state": True,
            "records_candidate_selection_packet_state": True,
            "default_state_remains_pending_without_explicit_refs": True,
            "does_not_write_runtime_config": True,
            "does_not_create_operator_signoff": True,
            "does_not_choose_candidate": True,
            "does_not_rerun_final_gate": True,
            "does_not_execute_application": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
            "does_not_create_production_config": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "packet_input_schema": {
            "input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUT_TYPE
            ),
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUT_VERSION
            ),
            "required_fields": list(PACKET_INPUT_REQUIRED_FIELDS),
        },
        "packet_schema": {
            "packet_type": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_TYPE
            ),
            "packet_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
            ),
            "required_fields": list(PACKET_REQUIRED_FIELDS),
            "allowed_packet_statuses": list(ALLOWED_PACKET_STATUSES),
            "allowed_operator_signoff_statuses": list(
                ALLOWED_OPERATOR_SIGNOFF_STATUSES
            ),
            "allowed_candidate_selection_statuses": list(
                ALLOWED_CANDIDATE_SELECTION_STATUSES
            ),
            "allowed_final_gate_rerun_statuses": list(
                ALLOWED_FINAL_GATE_RERUN_STATUSES
            ),
            "allowed_reexecution_readiness_statuses": list(
                ALLOWED_REEXECUTION_READINESS_STATUSES
            ),
            "allowed_next_action_recommendations": list(
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS
            ),
        },
        "operator_signoff_schema": {
            "requirements_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_TYPE,
            "requirements_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
            ),
            "required_fields": list(OPERATOR_SIGNOFF_REQUIREMENTS_REQUIRED_FIELDS),
        },
        "candidate_selection_schema": {
            "validation_type": (
                CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_VALIDATION_REPORT_TYPE
            ),
            "validation_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
            ),
            "required_fields": list(CANDIDATE_SELECTION_VALIDATION_REQUIRED_FIELDS),
        },
        "candidate_option_schema": {
            "options_type": CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_OPTIONS_TYPE,
            "options_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
            ),
            "required_fields": list(CANDIDATE_SELECTION_OPTIONS_REQUIRED_FIELDS),
        },
        "final_gate_rerun_readiness_schema": {
            "readiness_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
            ),
            "required_fields": list(FINAL_GATE_RERUN_READINESS_REQUIRED_FIELDS),
        },
        "reexecution_readiness_schema": {
            "readiness_version": (
                CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
            ),
            "required_fields": list(REEXECUTION_READINESS_REQUIRED_FIELDS),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_packet_input_shape": True,
            "validate_packet_artifact_shape": True,
            "validate_operator_signoff_requirements_shape": True,
            "validate_candidate_selection_options_shape": True,
            "validate_candidate_selection_validation_shape": True,
            "validate_final_gate_rerun_readiness_shape": True,
            "validate_reexecution_readiness_shape": True,
            "validate_allowed_statuses_and_recommendations": True,
            "validate_runtime_config_changed_is_false_for_pending_state": True,
            "validate_mutation_status_remains_no_runtime_mutation_due_to_blocker": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_operator_signoff_required_unless_explicit_ref_provided": True,
            "validate_candidate_selection_required_unless_explicit_ref_provided": True,
            "validate_no_operator_signoff_inferred_from_codex_or_tests": True,
            "validate_no_candidate_selection_inferred_from_available_options": True,
            "validate_final_gate_rerun_required_but_not_executed": True,
            "validate_runtime_application_not_executed": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_review_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_existing_baselines": True,
            "does_not_write_runtime_config": True,
        },
        "provenance_requirements": {
            "bp65_resolution_packet_path_required": True,
            "bp64_review_packet_path_required": True,
            "bp62_execution_path_required": True,
            "bp61_final_gate_path_required": True,
            "bp60_staging_path_required": True,
            "bp59_application_plan_path_required": True,
            "bp58_human_approval_gate_path_required": True,
            "bp57_dry_run_review_packet_path_required": True,
            "bp56_dry_run_execution_report_path_required": True,
            "bp55_change_request_path_required": True,
            "candidate_config_freeze_path_required": True,
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


def build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    source_blocked_execution_resolution_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_OUTPUT
    ),
    source_blocked_execution_resolution_packet_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_BLOCKED_EXECUTION_RESOLUTION_PACKET_CONTRACT_OUTPUT
    ),
    source_candidate_config_freeze_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_OUTPUT
    ),
    explicit_selected_candidate_ref: str | None = None,
    explicit_operator_signoff_ref: str | None = None,
    explicit_operator_identity_ref: str | None = None,
    explicit_operator_signoff_timestamp: str | None = None,
    operator_notes_ref: str | None = None,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    resolution_packet = _load_json(source_blocked_execution_resolution_packet_path)
    candidate_freeze = _load_json_if_exists(source_candidate_config_freeze_path)
    candidate_options = _candidate_option_refs(
        source_candidate_config_freeze_path,
        candidate_freeze,
    )
    model_asset_ref = resolution_packet.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = resolution_packet.get("model_asset_sha256") or _sha256_file(
        Path(model_asset_ref)
    )
    explicit_candidate = _explicit_ref(explicit_selected_candidate_ref)
    explicit_signoff = _explicit_ref(explicit_operator_signoff_ref)
    inputs = {
        "packet_input_id": _stable_id(
            "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs_v1",
            resolution_packet.get("resolution_packet_id"),
            resolution_packet.get("runtime_config_target_sha256_before"),
            resolution_packet.get("runtime_config_target_sha256_after"),
            explicit_candidate,
            explicit_signoff,
        ),
        "packet_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUT_TYPE
        ),
        "packet_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_blocked_execution_resolution_packet_path": str(
            Path(source_blocked_execution_resolution_packet_path)
        ),
        "source_blocked_execution_resolution_packet_contract_path": str(
            Path(source_blocked_execution_resolution_packet_contract_path)
        ),
        "source_application_execution_review_packet_path": resolution_packet.get(
            "source_application_execution_review_packet_path"
        ),
        "source_application_execution_path": resolution_packet.get(
            "source_application_execution_path"
        ),
        "source_pre_application_final_gate_path": resolution_packet.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": resolution_packet.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": resolution_packet.get("source_application_plan_path"),
        "source_human_approval_gate_path": resolution_packet.get(
            "source_human_approval_gate_path"
        ),
        "source_dry_run_review_packet_path": resolution_packet.get(
            "source_dry_run_review_packet_path"
        ),
        "source_dry_run_execution_report_path": resolution_packet.get(
            "source_dry_run_execution_report_path"
        ),
        "source_change_request_path": resolution_packet.get("source_change_request_path"),
        "source_candidate_config_freeze_path": str(Path(source_candidate_config_freeze_path)),
        "source_manual_approval_packet_path": _source_manual_approval_packet_path(
            resolution_packet
        ),
        "source_decision_packet_path": _source_decision_packet_path(resolution_packet),
        "source_phase_freeze_path": _source_phase_freeze_path(resolution_packet),
        "candidate_option_refs": candidate_options,
        "explicit_selected_candidate_ref": explicit_candidate,
        "explicit_operator_signoff_ref": explicit_signoff,
        "explicit_operator_identity_ref": explicit_operator_identity_ref,
        "explicit_operator_signoff_timestamp": explicit_operator_signoff_timestamp,
        "operator_notes_ref": operator_notes_ref,
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(resolution_packet.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": resolution_packet.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": resolution_packet.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": bool(resolution_packet.get("runtime_config_changed")),
        "mutation_status": resolution_packet.get("mutation_status"),
        "production_config_status": resolution_packet.get("production_config_status"),
        "baseline_update_status": resolution_packet.get("baseline_update_status"),
        "model_update_status": resolution_packet.get("model_update_status"),
        "source_resolution_packet_id": resolution_packet.get("resolution_packet_id"),
        "source_review_packet_id": _source_review_packet_id(resolution_packet),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": {
            "blocked_execution_resolution_packet": _artifact_ref(
                source_blocked_execution_resolution_packet_path,
                resolution_packet,
            ),
            "blocked_execution_resolution_packet_contract": _artifact_ref(
                source_blocked_execution_resolution_packet_contract_path,
                _load_json_if_exists(source_blocked_execution_resolution_packet_contract_path),
            ),
            "candidate_config_freeze": _artifact_ref(
                source_candidate_config_freeze_path,
                candidate_freeze,
            ),
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_packet_inputs",
        "packet_input_id": inputs["packet_input_id"],
        "candidate_option_count": len(candidate_options),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "candidate_selection_status": _candidate_selection_status(inputs),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_config_changed": inputs["runtime_config_changed"],
        "mutation_status": inputs["mutation_status"],
        "next_action_recommendation": _next_actions(inputs),
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(packet_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_inputs_validation"
        ),
        payload_path=packet_inputs_path,
        payload_type=inputs.get("packet_input_type"),
        payload_version=inputs.get("packet_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_operator_signoff_candidate_selection_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(packet_inputs_path)
    packet_id = _stable_id(
        "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_v1",
        inputs.get("packet_input_id"),
        inputs.get("source_resolution_packet_id"),
        inputs.get("runtime_config_target_sha256_before"),
        inputs.get("runtime_config_target_sha256_after"),
    )
    selected_candidate = _selected_candidate_ref(inputs)
    operator_signoff = _dict(inputs.get("explicit_operator_signoff_ref")) or None
    packet = {
        "packet_id": packet_id,
        "packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_TYPE
        ),
        "packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_input_path": str(Path(packet_inputs_path)),
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
        "source_dry_run_review_packet_path": inputs.get(
            "source_dry_run_review_packet_path"
        ),
        "source_dry_run_execution_report_path": inputs.get(
            "source_dry_run_execution_report_path"
        ),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "source_candidate_config_freeze_path": inputs.get("source_candidate_config_freeze_path"),
        "source_manual_approval_packet_path": inputs.get(
            "source_manual_approval_packet_path"
        ),
        "source_decision_packet_path": inputs.get("source_decision_packet_path"),
        "source_phase_freeze_path": inputs.get("source_phase_freeze_path"),
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "selected_candidate_config_ref": selected_candidate,
        "operator_signoff_ref": operator_signoff,
        "operator_identity_ref": inputs.get("explicit_operator_identity_ref"),
        "operator_signoff_timestamp": inputs.get("explicit_operator_signoff_timestamp"),
        "operator_signoff_status": _operator_signoff_status(inputs),
        "candidate_selection_status": _candidate_selection_status(inputs),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "runtime_config_changed": bool(inputs.get("runtime_config_changed")),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "packet_status": _packet_status(inputs),
        "operator_signoff_requirements": _operator_signoff_requirements(
            packet_id,
            inputs,
            generated_at,
        ),
        "candidate_selection_options": _candidate_selection_options(
            packet_id,
            inputs,
            generated_at,
        ),
        "candidate_selection_validation": _candidate_selection_validation(
            packet_id,
            inputs,
            generated_at,
        ),
        "final_gate_rerun_readiness": _final_gate_rerun_readiness(
            packet_id,
            inputs,
            generated_at,
        ),
        "reexecution_readiness": _reexecution_readiness(packet_id, inputs, generated_at),
        "next_action_recommendation": _next_actions(inputs),
        "source_resolution_packet_id": inputs.get("source_resolution_packet_id"),
        "source_review_packet_id": inputs.get("source_review_packet_id"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_inputs_shape(inputs))
    errors.extend(_validate_packet_shape(packet))
    _write_json_if_requested(output_path, packet)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_packet",
        "packet_id": packet["packet_id"],
        "packet_status": packet["packet_status"],
        "operator_signoff_status": packet["operator_signoff_status"],
        "candidate_selection_status": packet["candidate_selection_status"],
        "final_gate_rerun_status": packet["final_gate_rerun_status"],
        "reexecution_readiness_status": packet["reexecution_readiness_status"],
        "runtime_config_changed": packet["runtime_config_changed"],
        "mutation_status": packet["mutation_status"],
        "next_action_recommendation": packet["next_action_recommendation"],
        "packet_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def validate_controlled_runtime_calibration_operator_signoff_candidate_selection_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_operator_signoff_candidate_selection_packet_validation"
        ),
        payload_path=packet_path,
        payload_type=packet.get("packet_type"),
        payload_version=packet.get("packet_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(packet),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_operator_signoff_requirements(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_REQUIREMENTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(packet_path)
    requirements = {
        **_dict(packet.get("operator_signoff_requirements")),
        "exported_at": generated_at.isoformat(),
        "source_packet_path": str(Path(packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    errors.extend(_validate_operator_signoff_requirements_shape(requirements))
    _write_json_if_requested(output_path, requirements)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_signoff_requirements",
        "operator_signoff_requirements_id": requirements.get(
            "operator_signoff_requirements_id"
        ),
        "operator_signoff_status": requirements.get("operator_signoff_status"),
        "operator_signoff_requirements_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_candidate_selection_options(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_OPTIONS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(packet_path)
    options = {
        **_dict(packet.get("candidate_selection_options")),
        "exported_at": generated_at.isoformat(),
        "source_packet_path": str(Path(packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    errors.extend(_validate_candidate_selection_options_shape(options))
    _write_json_if_requested(output_path, options)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_candidate_selection_options",
        "candidate_selection_options_id": options.get("candidate_selection_options_id"),
        "candidate_selection_status": options.get("candidate_selection_status"),
        "candidate_option_count": len(_list(options.get("candidate_option_refs"))),
        "candidate_selection_options_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_candidate_selection_validation_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_VALIDATION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(packet_path)
    report = {
        **_dict(packet.get("candidate_selection_validation")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_CANDIDATE_SELECTION_VALIDATION_REPORT_TYPE,
        "exported_at": generated_at.isoformat(),
        "source_packet_path": str(Path(packet_path)),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    errors.extend(_validate_candidate_selection_validation_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_candidate_selection_validation",
        "candidate_selection_validation_id": report.get(
            "candidate_selection_validation_id"
        ),
        "candidate_selection_status": report.get("candidate_selection_status"),
        "candidate_selection_validation_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_resolution_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_OUTPUT
    ),
    packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RESOLUTION_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(packet_path)
    report = {
        "resolution_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_resolution_readiness_report_v1",
            packet.get("packet_id"),
        ),
        "resolution_readiness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RESOLUTION_READINESS_REPORT_TYPE
        ),
        "resolution_readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_id": packet.get("packet_id"),
        "source_packet_path": str(Path(packet_path)),
        "operator_signoff_status": packet.get("operator_signoff_status"),
        "candidate_selection_status": packet.get("candidate_selection_status"),
        "final_gate_rerun_status": packet.get("final_gate_rerun_status"),
        "reexecution_readiness_status": packet.get("reexecution_readiness_status"),
        "final_gate_rerun_readiness": _dict(packet.get("final_gate_rerun_readiness")),
        "reexecution_readiness": _dict(packet.get("reexecution_readiness")),
        "next_action_recommendation": _list(packet.get("next_action_recommendation")),
        "runtime_config_changed": packet.get("runtime_config_changed"),
        "mutation_status": packet.get("mutation_status"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_packet_shape(packet))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_resolution_readiness_report",
        "resolution_readiness_report_id": report["resolution_readiness_report_id"],
        "operator_signoff_status": report["operator_signoff_status"],
        "candidate_selection_status": report["candidate_selection_status"],
        "final_gate_rerun_status": report["final_gate_rerun_status"],
        "reexecution_readiness_status": report["reexecution_readiness_status"],
        "next_action_recommendation": report["next_action_recommendation"],
        "resolution_readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _operator_signoff_status(inputs: dict[str, Any]) -> str:
    if not _dict(inputs.get("explicit_operator_signoff_ref")):
        return "operator_signoff_required"
    if not inputs.get("explicit_operator_identity_ref"):
        return "operator_signoff_invalid"
    if not inputs.get("explicit_operator_signoff_timestamp"):
        return "operator_signoff_invalid"
    return "operator_signoff_explicitly_recorded"


def _candidate_selection_status(inputs: dict[str, Any]) -> str:
    selected = _dict(inputs.get("explicit_selected_candidate_ref"))
    if not selected:
        return "selected_candidate_required"
    if _candidate_ref_matches_option(selected, _list(inputs.get("candidate_option_refs"))):
        return "selected_candidate_explicitly_recorded"
    return "selected_candidate_invalid"


def _final_gate_rerun_status(inputs: dict[str, Any]) -> str:
    signoff_status = _operator_signoff_status(inputs)
    candidate_status = _candidate_selection_status(inputs)
    if signoff_status == "operator_signoff_explicitly_recorded" and candidate_status == (
        "selected_candidate_explicitly_recorded"
    ):
        return "final_gate_rerun_ready_after_signoff_and_candidate_selection"
    if candidate_status == "selected_candidate_invalid":
        return "final_gate_rerun_blocked_invalid_candidate"
    return "final_gate_rerun_required"


def _reexecution_readiness_status(inputs: dict[str, Any]) -> str:
    if _final_gate_rerun_status(inputs) == (
        "final_gate_rerun_ready_after_signoff_and_candidate_selection"
    ):
        return "reexecution_blocked_final_gate_not_rerun"
    return "reexecution_not_ready_blockers_unresolved"


def _packet_status(inputs: dict[str, Any]) -> str:
    signoff_status = _operator_signoff_status(inputs)
    candidate_status = _candidate_selection_status(inputs)
    if signoff_status == "operator_signoff_invalid":
        return "packet_blocked_invalid_operator_signoff"
    if candidate_status == "selected_candidate_invalid":
        return "packet_blocked_invalid_selected_candidate"
    if not _list(inputs.get("candidate_option_refs")):
        return "packet_blocked_missing_candidate_options"
    if signoff_status == "operator_signoff_explicitly_recorded" and candidate_status == (
        "selected_candidate_explicitly_recorded"
    ):
        return "packet_created_with_explicit_signoff_and_candidate_selection"
    if signoff_status == "operator_signoff_explicitly_recorded":
        return "packet_created_with_operator_signoff_pending_candidate_selection"
    if candidate_status == "selected_candidate_explicitly_recorded":
        return "packet_created_with_candidate_selection_pending_operator_signoff"
    return "packet_created_pending_operator_signoff_and_candidate_selection"


def _next_actions(inputs: dict[str, Any]) -> list[str]:
    signoff_status = _operator_signoff_status(inputs)
    candidate_status = _candidate_selection_status(inputs)
    if signoff_status == "operator_signoff_explicitly_recorded" and candidate_status == (
        "selected_candidate_explicitly_recorded"
    ):
        return [
            "rerun_final_gate_after_signoff_and_candidate_selection",
            "prepare_final_gate_rerun_blueprint",
        ]
    if signoff_status == "operator_signoff_explicitly_recorded":
        return [
            "provide_selected_candidate",
            "rerun_final_gate_after_signoff_and_candidate_selection",
        ]
    if candidate_status == "selected_candidate_explicitly_recorded":
        return [
            "provide_operator_signoff",
            "rerun_final_gate_after_signoff_and_candidate_selection",
        ]
    return [
        "provide_operator_signoff_and_selected_candidate",
        "rerun_final_gate_after_signoff_and_candidate_selection",
    ]


def _operator_signoff_requirements(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "operator_signoff_requirements_id": _stable_id(
            "controlled_runtime_calibration_operator_signoff_requirements_v1",
            packet_id,
        ),
        "operator_signoff_requirements_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_id": packet_id,
        "source_resolution_packet_id": inputs.get("source_resolution_packet_id"),
        "requirements": {
            "operator_identity_or_reference_required": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_identity_ref")),
            },
            "operator_timestamp_required": {
                "required": True,
                "provided": bool(inputs.get("explicit_operator_signoff_timestamp")),
            },
            "source_bp65_resolution_packet_required": {
                "required": True,
                "path": inputs.get("source_blocked_execution_resolution_packet_path"),
            },
            "source_bp64_execution_review_packet_required": {
                "required": True,
                "path": inputs.get("source_application_execution_review_packet_path"),
            },
            "selected_candidate_ref_required_before_final_gate_rerun": {
                "required": True,
                "provided": _candidate_selection_status(inputs)
                == "selected_candidate_explicitly_recorded",
            },
            "no_runtime_application_performed_by_this_packet": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_not_be_inferred_from_codex_execution": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_not_be_inferred_from_successful_tests": {
                "required": True,
                "status": "preserved",
            },
            "operator_signoff_must_be_explicit": {
                "required": True,
                "status": "preserved",
            },
        },
        "operator_signoff_status": _operator_signoff_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_selection_options(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "candidate_selection_options_id": _stable_id(
            "controlled_runtime_calibration_candidate_selection_options_v1",
            packet_id,
        ),
        "candidate_selection_options_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_id": packet_id,
        "candidate_option_refs": _list(inputs.get("candidate_option_refs")),
        "candidate_selection_status": _candidate_selection_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_selection_validation(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    selected = _dict(inputs.get("explicit_selected_candidate_ref"))
    candidate_status = _candidate_selection_status(inputs)
    return {
        "candidate_selection_validation_id": _stable_id(
            "controlled_runtime_calibration_candidate_selection_validation_v1",
            packet_id,
        ),
        "candidate_selection_validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_id": packet_id,
        "selected_candidate_config_ref": selected or None,
        "validation_checks": {
            "selected_candidate_must_reference_existing_frozen_candidate_config": {
                "required": True,
                "status": (
                    "satisfied"
                    if candidate_status == "selected_candidate_explicitly_recorded"
                    else "pending"
                ),
            },
            "selected_candidate_must_not_be_inferred_from_model_output": {
                "required": True,
                "status": "preserved",
            },
            "selected_candidate_must_not_be_invented_by_codex": {
                "required": True,
                "status": "preserved",
            },
            "selected_candidate_must_preserve_source_path_id_version_provenance": {
                "required": True,
                "status": (
                    "satisfied"
                    if candidate_status == "selected_candidate_explicitly_recorded"
                    else "pending"
                ),
            },
            "selected_candidate_must_be_reviewed_by_human_operator_before_final_gate_rerun": {  # noqa: E501
                "required": True,
                "status": "pending",
            },
            "selection_remains_required_without_explicit_selected_candidate_ref": {
                "required": True,
                "status": (
                    "pending" if not selected else "explicit_ref_provided_for_validation"
                ),
            },
        },
        "candidate_selection_status": candidate_status,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_rerun_readiness(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "final_gate_rerun_readiness_id": _stable_id(
            "controlled_runtime_calibration_final_gate_rerun_readiness_v1",
            packet_id,
        ),
        "final_gate_rerun_readiness_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_id": packet_id,
        "required_inputs": {
            "operator_signoff_explicitly_recorded": _operator_signoff_status(inputs)
            == "operator_signoff_explicitly_recorded",
            "selected_candidate_explicitly_recorded": _candidate_selection_status(inputs)
            == "selected_candidate_explicitly_recorded",
            "bp65_resolution_packet_referenced": bool(
                inputs.get("source_blocked_execution_resolution_packet_path")
            ),
            "bp64_review_packet_referenced": bool(
                inputs.get("source_application_execution_review_packet_path")
            ),
            "bp62_execution_artifact_referenced": bool(
                inputs.get("source_application_execution_path")
            ),
            "bp61_final_gate_referenced": bool(
                inputs.get("source_pre_application_final_gate_path")
            ),
            "bp60_staging_artifact_referenced": bool(
                inputs.get("source_runtime_application_staging_path")
            ),
            "no_runtime_mutation_performed_by_bp66": True,
            "final_gate_not_rerun_by_bp66": True,
        },
        "required_regression_gates": _required_regression_gates(),
        "final_gate_rerun_status": _final_gate_rerun_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _reexecution_readiness(
    packet_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    return {
        "reexecution_readiness_id": _stable_id(
            "controlled_runtime_calibration_reexecution_readiness_v1",
            packet_id,
        ),
        "reexecution_readiness_version": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_packet_id": packet_id,
        "required_inputs": {
            "future_final_gate_rerun_must_pass": True,
            "application_execution_must_not_be_reattempted_by_bp66": True,
            "rollback_package_must_remain_available": True,
            "post_execution_review_must_remain_required": True,
            "baselines_must_remain_unchanged": True,
            "model_weights_must_remain_unchanged": True,
            "production_config_must_not_be_created": True,
        },
        "required_preconditions": [
            "final gate rerun must pass in a future blueprint",
            "application execution must not be reattempted by Blueprint 66",
            "rollback package must remain available",
            "post-execution review must remain required",
            "baselines must remain unchanged",
            "model weights must remain unchanged",
            "production config must not be created",
        ],
        "reexecution_readiness_status": _reexecution_readiness_status(inputs),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_option_refs(
    path: str | Path,
    candidate_freeze: dict[str, Any],
) -> list[dict[str, Any]]:
    if not candidate_freeze:
        return []
    settings = _dict(candidate_freeze.get("candidate_settings"))
    candidate_source = _dict(settings.get("candidate_source"))
    return [
        {
            "candidate_option_ref_type": "frozen_candidate_config_ref",
            "source_path": str(Path(path)),
            "source_exists": Path(path).exists(),
            "candidate_config_freeze_id": candidate_freeze.get("candidate_config_freeze_id"),
            "candidate_config_freeze_version": candidate_freeze.get(
                "candidate_config_freeze_version"
            ),
            "candidate_id": (
                candidate_source.get("candidate_setting_id")
                or candidate_freeze.get("candidate_config_freeze_id")
            ),
            "candidate_version": candidate_freeze.get("candidate_config_freeze_version"),
            "candidate_packet_id": candidate_source.get("candidate_packet_id"),
            "source_proposal_item_id": candidate_source.get("source_proposal_item_id"),
            "candidate_settings_summary": {
                "candidate_type": settings.get("candidate_type"),
                "candidate_threshold": settings.get("candidate_threshold"),
                "candidate_smoothing_window": settings.get("candidate_smoothing_window"),
                "candidate_hysteresis_settings": settings.get(
                    "candidate_hysteresis_settings"
                ),
                "writes_runtime_configuration": settings.get(
                    "writes_runtime_configuration"
                ),
                "not_applied": settings.get("not_applied"),
                "affects_regression_baselines": settings.get(
                    "affects_regression_baselines"
                ),
            },
            "provenance_summary": {
                "source_decision_packet_path": candidate_freeze.get(
                    "source_decision_packet_path"
                ),
                "source_freeze_input_path": candidate_freeze.get("source_freeze_input_path"),
                "model_asset_ref": candidate_freeze.get("model_asset_ref"),
                "model_asset_sha256": candidate_freeze.get("model_asset_sha256"),
            },
            "requires_explicit_selection": True,
            "selected_by_blueprint_66": False,
            "warnings": {
                "candidate_option_is_not_selected_by_discovery": True,
                "explicit_selected_candidate_ref_required": True,
            },
        }
    ]


def _selected_candidate_ref(inputs: dict[str, Any]) -> dict[str, Any] | None:
    selected = _dict(inputs.get("explicit_selected_candidate_ref"))
    if not selected:
        return None
    if not _candidate_ref_matches_option(selected, _list(inputs.get("candidate_option_refs"))):
        return selected
    return {
        **selected,
        "selection_source": "explicit_selected_candidate_ref",
        "selected_by_blueprint_66": False,
        "selection_requires_human_operator_review": True,
    }


def _candidate_ref_matches_option(
    selected: dict[str, Any],
    options: list[Any],
) -> bool:
    selected_values = {
        value
        for value in [
            selected.get("path"),
            selected.get("source_path"),
            selected.get("ref"),
            selected.get("candidate_config_freeze_id"),
            selected.get("candidate_id"),
        ]
        if value
    }
    for option in options:
        option_dict = _dict(option)
        option_values = {
            value
            for value in [
                option_dict.get("source_path"),
                option_dict.get("candidate_config_freeze_id"),
                option_dict.get("candidate_id"),
            ]
            if value
        }
        if selected_values & option_values:
            return True
    return False


def _source_manual_approval_packet_path(resolution_packet: dict[str, Any]) -> str:
    path = _dict(resolution_packet.get("source_artifact_refs")).get(
        "manual_approval_packet"
    )
    if isinstance(path, dict) and path.get("path"):
        return str(path["path"])
    return DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT


def _source_decision_packet_path(resolution_packet: dict[str, Any]) -> str:
    path = _dict(resolution_packet.get("source_artifact_refs")).get("decision_packet")
    if isinstance(path, dict) and path.get("path"):
        return str(path["path"])
    return DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT


def _source_phase_freeze_path(resolution_packet: dict[str, Any]) -> str:
    path = _dict(resolution_packet.get("source_artifact_refs")).get("phase_freeze")
    if isinstance(path, dict) and path.get("path"):
        return str(path["path"])
    return DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT


def _source_review_packet_id(resolution_packet: dict[str, Any]) -> str | None:
    review_path = resolution_packet.get("source_application_execution_review_packet_path")
    review_packet = _load_json_if_exists(review_path)
    return review_packet.get("review_packet_id")


def _required_regression_gates() -> list[dict[str, Any]]:
    return [
        {"gate": "multi_point_regression_matrix", "required": True},
        {"gate": "protected_sample_point_reviewed_3d_debug", "required": True},
        {"gate": "gameplay_gate_regression_baseline", "required": True},
        {
            "gate": "review_guided_gameplay_calibration_sandbox_regression",
            "required": True,
        },
    ]


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "packet_scope",
        "source_contract_refs",
        "packet_input_schema",
        "packet_schema",
        "operator_signoff_schema",
        "candidate_selection_schema",
        "candidate_option_schema",
        "final_gate_rerun_readiness_schema",
        "reexecution_readiness_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors = _missing_required(contract, required, "contract")
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_packet_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, PACKET_INPUT_REQUIRED_FIELDS, "packet_inputs")
    errors.extend(_validate_blocked_runtime_state(inputs))
    errors.extend(_validate_explicit_resolution_refs(inputs))
    errors.extend(_validate_next_actions(_next_actions(inputs)))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(packet, PACKET_REQUIRED_FIELDS, "packet")
    errors.extend(
        _validate_status(
            "packet_status",
            packet.get("packet_status"),
            ALLOWED_PACKET_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            packet.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "candidate_selection_status",
            packet.get("candidate_selection_status"),
            ALLOWED_CANDIDATE_SELECTION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            packet.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            packet.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    errors.extend(_validate_blocked_runtime_state(packet))
    errors.extend(_validate_packet_resolution_statuses(packet))
    errors.extend(_validate_next_actions(_list(packet.get("next_action_recommendation"))))
    errors.extend(
        _validate_operator_signoff_requirements_shape(
            _dict(packet.get("operator_signoff_requirements"))
        )
    )
    errors.extend(
        _validate_candidate_selection_options_shape(
            _dict(packet.get("candidate_selection_options"))
        )
    )
    errors.extend(
        _validate_candidate_selection_validation_shape(
            _dict(packet.get("candidate_selection_validation"))
        )
    )
    errors.extend(
        _validate_final_gate_rerun_readiness_shape(
            _dict(packet.get("final_gate_rerun_readiness"))
        )
    )
    errors.extend(
        _validate_reexecution_readiness_shape(_dict(packet.get("reexecution_readiness")))
    )
    errors.extend(_validate_non_claims(_dict(packet.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(packet))
    return errors


def _validate_explicit_resolution_refs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if _operator_signoff_status(payload) == "operator_signoff_invalid":
        errors.append(
            _error(
                "invalid_explicit_operator_signoff_ref",
                "explicit_operator_signoff_ref",
                payload.get("explicit_operator_signoff_ref"),
            )
        )
    if _candidate_selection_status(payload) == "selected_candidate_invalid":
        errors.append(
            _error(
                "invalid_explicit_selected_candidate_ref",
                "explicit_selected_candidate_ref",
                payload.get("explicit_selected_candidate_ref"),
            )
        )
    return errors


def _validate_packet_resolution_statuses(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if packet.get("operator_signoff_status") == "operator_signoff_invalid":
        errors.append(
            _error(
                "invalid_operator_signoff_status",
                "operator_signoff_status",
                packet.get("operator_signoff_status"),
            )
        )
    if packet.get("candidate_selection_status") == "selected_candidate_invalid":
        errors.append(
            _error(
                "invalid_candidate_selection_status",
                "candidate_selection_status",
                packet.get("candidate_selection_status"),
            )
        )
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
                "runtime_config_hashes_must_match_for_pending_packet",
                "runtime_config_target_sha256_after",
                after,
            )
        )
    return errors


def _validate_operator_signoff_requirements_shape(
    requirements: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        requirements,
        OPERATOR_SIGNOFF_REQUIREMENTS_REQUIRED_FIELDS,
        "operator_signoff_requirements",
    )
    errors.extend(
        _validate_status(
            "operator_signoff_status",
            requirements.get("operator_signoff_status"),
            ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        )
    )
    return errors


def _validate_candidate_selection_options_shape(options: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        options,
        CANDIDATE_SELECTION_OPTIONS_REQUIRED_FIELDS,
        "candidate_selection_options",
    )
    errors.extend(
        _validate_status(
            "candidate_selection_status",
            options.get("candidate_selection_status"),
            ALLOWED_CANDIDATE_SELECTION_STATUSES,
        )
    )
    return errors


def _validate_candidate_selection_validation_shape(
    validation: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _missing_required(
        validation,
        CANDIDATE_SELECTION_VALIDATION_REQUIRED_FIELDS,
        "candidate_selection_validation",
    )
    errors.extend(
        _validate_status(
            "candidate_selection_status",
            validation.get("candidate_selection_status"),
            ALLOWED_CANDIDATE_SELECTION_STATUSES,
        )
    )
    return errors


def _validate_final_gate_rerun_readiness_shape(readiness: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        readiness,
        FINAL_GATE_RERUN_READINESS_REQUIRED_FIELDS,
        "final_gate_rerun_readiness",
    )
    errors.extend(
        _validate_status(
            "final_gate_rerun_status",
            readiness.get("final_gate_rerun_status"),
            ALLOWED_FINAL_GATE_RERUN_STATUSES,
        )
    )
    return errors


def _validate_reexecution_readiness_shape(readiness: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(
        readiness,
        REEXECUTION_READINESS_REQUIRED_FIELDS,
        "reexecution_readiness",
    )
    errors.extend(
        _validate_status(
            "reexecution_readiness_status",
            readiness.get("reexecution_readiness_status"),
            ALLOWED_REEXECUTION_READINESS_STATUSES,
        )
    )
    return errors


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
            errors.append(
                _error("missing_non_claim", f"non_claims.{key}", non_claims.get(key))
            )
    return errors


def _validate_status(field: str, value: Any, allowed: list[str]) -> list[dict[str, Any]]:
    if value in allowed:
        return []
    return [_error("invalid_status", field, value)]


def _validate_no_forbidden_tokens(payload: Any, path: str = "$") -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif (
        isinstance(payload, str)
        and payload in FORBIDDEN_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_TOKENS
    ):
        errors.append(_error("forbidden_value", path, payload))
    return errors


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "packet_status",
        "operator_signoff_status",
        "candidate_selection_status",
        "final_gate_rerun_status",
        "reexecution_readiness_status",
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
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_PACKET_VERSION
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


def _explicit_ref(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None
    try:
        loaded = json.loads(value)
    except json.JSONDecodeError:
        loaded = None
    if isinstance(loaded, dict):
        return loaded
    return {
        "ref": value,
        "path": value if value.endswith(".json") else None,
        "source": "explicit_cli_argument",
    }


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
        "packet_type",
        "resolution_packet_type",
        "review_packet_type",
        "contract_type",
        "candidate_config_freeze_type",
    ]:
        if payload.get(key):
            return payload.get(key)
    return None


def _artifact_version(payload: dict[str, Any]) -> Any:
    for key in [
        "packet_version",
        "resolution_packet_version",
        "review_packet_version",
        "contract_version",
        "candidate_config_freeze_version",
    ]:
        if payload.get(key):
            return payload.get(key)
    return None


def _missing_required(
    payload: dict[str, Any],
    required_fields: list[str],
    context: str,
) -> list[dict[str, Any]]:
    return [
        _error("missing_required_field", f"{context}.{field}", None)
        for field in required_fields
        if field not in payload
    ]


def _error(code: str, field: str, value: Any) -> dict[str, Any]:
    return {"code": code, "field": field, "value": value}


def _load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _load_json_if_exists(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    json_path = Path(path)
    if not json_path.exists():
        return {}
    return _load_json(json_path)


def _write_json_if_requested(path: str | Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_id(prefix: str, *parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _path_string(path: str | Path | None) -> str | None:
    if path is None:
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_CANDIDATE_SELECTION_BLUEPRINT_NAME
        ),
    }
