from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.calibration_candidate_config_freeze import (
    DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_ARTIFACT_OUTPUT,
    DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT,
)
from apps.worker.services.calibration_candidate_decision_packet import (
    DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_application_execution import (
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_ROLLBACK_PACKAGE_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_application_execution import (
    SOURCE_CONTRACT_REFS as APPLICATION_EXECUTION_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.controlled_runtime_calibration_application_plan import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_change_request import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_dry_run_execution import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_dry_run_review_packet import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_human_approval_gate import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_pre_application_final_gate import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_runtime_application_staging import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT,
)
from apps.worker.services.gameplay_gate_regression_baseline import (
    DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)
from apps.worker.services.real_broadcast_gameplay_calibration_decision_phase_freeze import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT,
)

CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_TYPE = (
    "controlled_runtime_calibration_application_execution_review_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUT_TYPE = (
    "controlled_runtime_calibration_application_execution_review_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_TYPE = (
    "controlled_runtime_calibration_application_execution_review_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_SUMMARY_TYPE = (
    "controlled_runtime_calibration_post_execution_summary"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_BLOCKER_REPORT_TYPE = (
    "controlled_runtime_calibration_post_execution_blocker_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_OPERATOR_CHECKLIST_TYPE = (
    "controlled_runtime_calibration_post_execution_operator_checklist"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_NEXT_ACTION_REPORT_TYPE = (
    "controlled_runtime_calibration_post_execution_next_action_report"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_BLUEPRINT = (
    "blueprint_64"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_application_execution_review_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_application_execution_review_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUTS_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_application_execution_review_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUTS_VALIDATION_OUTPUT = (  # noqa: E501
    ".data/exports/"
    "controlled_runtime_calibration_application_execution_review_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_application_execution_review_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_application_execution_review_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_SUMMARY_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_post_execution_summary.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_BLOCKER_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_post_execution_blocker_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_OPERATOR_CHECKLIST_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_post_execution_operator_checklist.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_NEXT_ACTION_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_post_execution_next_action_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_EXPORTED_AT = datetime(
    2026,
    6,
    21,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_application_execution_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION
    ),
    **dict(APPLICATION_EXECUTION_SOURCE_CONTRACT_REFS),
}

ALLOWED_REVIEW_PACKET_STATUSES = [
    "review_packet_created_for_blocked_execution",
    "review_packet_created_for_controlled_application",
    "review_packet_created_with_warnings",
    "review_packet_blocked_missing_execution_artifact",
    "review_packet_blocked_missing_final_gate",
    "review_packet_blocked_missing_rollback_package",
    "review_packet_blocked_missing_post_apply_verification",
    "review_packet_informational_only",
    "not_applicable",
]
ALLOWED_APPLICATION_OUTCOME_STATUSES = [
    "application_blocked_safely_before_runtime_mutation",
    "application_executed_controlled_runtime_config_write",
    "application_executed_with_warnings_controlled_runtime_config_write",
    "application_failed_and_restored_previous_config",
    "application_failed_requires_rollback_followup",
    "application_outcome_unknown",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "applied_by_controlled_blueprint",
    "blocked_from_runtime_application",
    "not_applicable",
]
ALLOWED_RUNTIME_CONFIG_STATUSES = [
    "updated_by_controlled_application",
    "unchanged_due_to_blocker",
    "restored_after_failed_verification",
    "not_applicable",
]
ALLOWED_MUTATION_STATUSES = [
    "controlled_runtime_config_mutation_performed",
    "no_runtime_mutation_due_to_blocker",
    "controlled_runtime_config_restored_after_failed_verification",
    "not_applicable",
]
ALLOWED_PRODUCTION_CONFIG_STATUSES = [
    "not_created",
    "production_config_not_supported",
    "blocked_from_creation",
    "not_applicable",
]
ALLOWED_BASELINE_UPDATE_STATUSES = [
    "not_replaced",
    "baseline_update_not_supported",
    "blocked_from_baseline_update",
    "not_applicable",
]
ALLOWED_MODEL_UPDATE_STATUSES = [
    "not_modified",
    "model_update_not_supported",
    "blocked_from_model_update",
    "not_applicable",
]
ALLOWED_ATOMIC_WRITE_STATUSES = [
    "atomic_write_completed",
    "atomic_write_blocked",
    "atomic_write_failed",
    "atomic_write_restored_previous_config",
    "not_applicable",
]
ALLOWED_RUNTIME_READBACK_STATUSES = [
    "readback_verified",
    "readback_mismatch",
    "readback_blocked",
    "readback_not_applicable",
]
ALLOWED_ROLLBACK_PACKAGE_STATUSES = [
    "rollback_package_created",
    "rollback_package_missing",
    "rollback_package_incomplete",
    "rollback_package_blocked",
    "rollback_package_not_needed_for_blocked_execution",
    "not_applicable",
]
ALLOWED_POST_APPLY_VERIFICATION_STATUSES = [
    "post_apply_verification_passed",
    "post_apply_verification_passed_with_warnings",
    "post_apply_verification_failed",
    "post_apply_verification_blocked",
    "post_apply_verification_not_needed_for_blocked_execution",
    "not_applicable",
]
ALLOWED_VERIFICATION_SUMMARY_STATUSES = [
    "verification_passed_for_blocked_execution",
    "verification_passed_for_controlled_application",
    "verification_passed_with_warnings",
    "verification_failed",
    "verification_blocked",
    "not_applicable",
]
ALLOWED_NEXT_ACTION_RECOMMENDATIONS = [
    "resolve_operator_signoff_before_reapplying",
    "resolve_selected_candidate_before_reapplying",
    "rerun_final_gate_after_operator_signoff",
    "rerun_application_execution_after_final_gate_passes",
    "proceed_to_post_application_review_after_controlled_apply",
    "prepare_rollback_followup",
    "freeze_controlled_calibration_phase",
    "no_runtime_action_recommended",
    "not_applicable",
]

REVIEW_PACKET_INPUT_REQUIRED_FIELDS = [
    "review_packet_input_id",
    "review_packet_input_type",
    "review_packet_input_version",
    "generated_at",
    "source_application_execution_path",
    "source_application_execution_contract_path",
    "source_runtime_config_artifact_path",
    "source_rollback_package_path",
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
    "source_gameplay_gate_regression_baseline_path",
    "source_calibration_sandbox_baseline_path",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "application_execution_status",
    "runtime_application_status",
    "runtime_config_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "atomic_write_status",
    "runtime_readback_status",
    "rollback_package_status",
    "post_apply_verification_status",
    "warnings",
    "non_claims",
]

REVIEW_PACKET_REQUIRED_FIELDS = [
    "review_packet_id",
    "review_packet_type",
    "review_packet_version",
    "generated_at",
    "source_review_packet_input_path",
    "source_application_execution_path",
    "source_pre_application_final_gate_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "runtime_config_target_ref",
    "runtime_config_target_sha256_before",
    "runtime_config_target_sha256_after",
    "application_execution_status",
    "runtime_application_status",
    "runtime_config_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "atomic_write_status",
    "runtime_readback_status",
    "rollback_package_status",
    "post_apply_verification_status",
    "execution_outcome_summary",
    "blocker_summary",
    "verification_summary",
    "rollback_summary",
    "operator_review_checklist",
    "next_action_recommendation",
    "review_packet_status",
    "warnings",
    "non_claims",
]

OUTCOME_SUMMARY_REQUIRED_FIELDS = [
    "outcome_summary_id",
    "outcome_summary_version",
    "generated_at",
    "source_application_execution_id",
    "application_outcome_status",
    "runtime_application_status",
    "runtime_config_status",
    "mutation_status",
    "applied_delta_present",
    "runtime_config_sha_before",
    "runtime_config_sha_after",
    "runtime_config_changed",
    "blocked_reason_count",
    "blocker_types",
    "warnings",
    "non_claims",
]

VERIFICATION_SUMMARY_REQUIRED_FIELDS = [
    "verification_summary_id",
    "verification_summary_version",
    "generated_at",
    "source_application_execution_id",
    "multi_point_regression_gate_result",
    "protected_sample_point_gate_result",
    "gameplay_gate_regression_baseline_result",
    "calibration_sandbox_regression_baseline_result",
    "runtime_readback_result",
    "model_asset_hash_check",
    "baseline_replacement_check",
    "production_config_check",
    "verification_summary_status",
    "warnings",
    "non_claims",
]

ROLLBACK_SUMMARY_REQUIRED_FIELDS = [
    "rollback_summary_id",
    "rollback_summary_version",
    "generated_at",
    "source_application_execution_id",
    "rollback_package_ref",
    "rollback_package_status",
    "rollback_needed",
    "rollback_ready",
    "rollback_reason",
    "rollback_verification_gates",
    "warnings",
    "non_claims",
]

OPERATOR_CHECKLIST_REQUIRED_FIELDS = [
    "inspect_application_execution_artifact",
    "inspect_final_gate_status",
    "inspect_runtime_config_before_after_hashes",
    "inspect_runtime_config_changed_flag",
    "inspect_blocked_reason",
    "inspect_runtime_readback_status",
    "inspect_rollback_package",
    "inspect_post_apply_verification",
    "inspect_regression_gate_results",
    "confirm_model_weights_not_modified",
    "confirm_baselines_not_replaced",
    "confirm_production_config_not_created",
    "confirm_no_truth_claims",
    "decide_next_action",
]

WARNINGS = {
    "controlled_application_execution_review": True,
    "post_execution_review_packet": True,
    "post_execution_human_review_required": True,
    "execution_review_packet_is_not_truth": True,
    "execution_review_packet_is_not_accuracy_scoring": True,
    "execution_review_packet_is_not_model_training": True,
    "execution_review_packet_is_not_production_config": True,
    "controlled_runtime_config_update_is_not_tennis_truth": True,
    "classifier_correctness_not_assessed": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "no_adjudication": True,
    "review_support_only": True,
}

NON_CLAIMS = {
    "execution_review_packet_is_not_truth": True,
    "execution_review_packet_is_not_accuracy_scoring": True,
    "execution_review_packet_is_not_model_training": True,
    "execution_review_packet_is_not_production_config": True,
    "controlled_runtime_config_update_is_not_tennis_truth": True,
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
    "post_execution_human_review_required": True,
}


def _forbidden_token(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_REVIEW_PACKET_TOKENS = {
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
}


def export_controlled_runtime_calibration_application_execution_review_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "review_packet_scope": {
            "reviews_application_execution_artifact": True,
            "supports_blocked_execution_review": True,
            "supports_controlled_application_review": True,
            "does_not_write_runtime_config": True,
            "does_not_create_production_config": True,
            "does_not_modify_model_weights": True,
            "does_not_replace_baselines": True,
            "does_not_perform_automatic_approval": True,
            "does_not_perform_automatic_rejection": True,
            "requires_post_execution_human_review": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "review_packet_input_schema": {
            "input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUT_TYPE
            ),
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUT_VERSION
            ),
            "required_fields": list(REVIEW_PACKET_INPUT_REQUIRED_FIELDS),
        },
        "review_packet_schema": {
            "packet_type": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_TYPE
            ),
            "packet_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
            ),
            "required_fields": list(REVIEW_PACKET_REQUIRED_FIELDS),
            "allowed_review_packet_statuses": list(ALLOWED_REVIEW_PACKET_STATUSES),
            "allowed_application_outcome_statuses": list(
                ALLOWED_APPLICATION_OUTCOME_STATUSES
            ),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_runtime_config_statuses": list(ALLOWED_RUNTIME_CONFIG_STATUSES),
            "allowed_mutation_statuses": list(ALLOWED_MUTATION_STATUSES),
            "allowed_production_config_statuses": list(
                ALLOWED_PRODUCTION_CONFIG_STATUSES
            ),
            "allowed_baseline_update_statuses": list(ALLOWED_BASELINE_UPDATE_STATUSES),
            "allowed_model_update_statuses": list(ALLOWED_MODEL_UPDATE_STATUSES),
            "allowed_atomic_write_statuses": list(ALLOWED_ATOMIC_WRITE_STATUSES),
            "allowed_runtime_readback_statuses": list(ALLOWED_RUNTIME_READBACK_STATUSES),
            "allowed_rollback_package_statuses": list(ALLOWED_ROLLBACK_PACKAGE_STATUSES),
            "allowed_post_apply_verification_statuses": list(
                ALLOWED_POST_APPLY_VERIFICATION_STATUSES
            ),
        },
        "post_execution_summary_schema": {
            "summary_type": CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_SUMMARY_TYPE,
            "summary_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
            ),
            "required_fields": list(OUTCOME_SUMMARY_REQUIRED_FIELDS),
        },
        "blocker_report_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_BLOCKER_REPORT_TYPE,
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
            ),
            "reports_missing_operator_signoff": True,
            "reports_missing_selected_candidate": True,
            "reports_final_gate_blocker": True,
        },
        "operator_checklist_schema": {
            "checklist_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_OPERATOR_CHECKLIST_TYPE
            ),
            "checklist_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
            ),
            "required_fields": list(OPERATOR_CHECKLIST_REQUIRED_FIELDS),
        },
        "next_action_report_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_NEXT_ACTION_REPORT_TYPE
            ),
            "report_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
            ),
            "allowed_next_action_recommendations": list(
                ALLOWED_NEXT_ACTION_RECOMMENDATIONS
            ),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_review_packet_input_shape": True,
            "validate_review_packet_artifact_shape": True,
            "validate_execution_outcome_summary_shape": True,
            "validate_verification_summary_shape": True,
            "validate_rollback_summary_shape": True,
            "validate_operator_checklist_shape": True,
            "validate_allowed_statuses_and_scopes": True,
            "validate_model_update_status_remains_not_modified": True,
            "validate_production_config_status_remains_not_created": True,
            "validate_baseline_update_status_remains_not_replaced": True,
            "validate_blocked_runtime_hashes_match_when_present": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_review_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
            "does_not_modify_runtime_config": True,
        },
        "provenance_requirements": {
            "application_execution_path_required": True,
            "application_execution_contract_path_required": True,
            "pre_application_final_gate_path_required": True,
            "runtime_application_staging_path_required": True,
            "application_plan_path_required": True,
            "human_approval_gate_path_required": True,
            "dry_run_review_packet_path_required": True,
            "dry_run_execution_report_path_required": True,
            "change_request_path_required": True,
            "model_asset_hash_required": True,
            "runtime_config_hashes_preserved_when_available": True,
            "rollback_package_ref_recorded_when_available": True,
            "post_apply_verification_status_recorded": True,
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


def build_controlled_runtime_calibration_application_execution_review_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    source_application_execution_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    source_application_execution_contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    source_runtime_config_artifact_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_OUTPUT
    ),
    source_rollback_package_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_ROLLBACK_PACKAGE_OUTPUT
    ),
    source_pre_application_final_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    source_runtime_application_staging_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT
    ),
    source_application_plan_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT
    ),
    source_human_approval_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT
    ),
    source_dry_run_review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT
    ),
    source_dry_run_execution_report_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT
    ),
    source_change_request_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT
    ),
    source_candidate_config_freeze_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_ARTIFACT_OUTPUT
    ),
    source_manual_approval_packet_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT
    ),
    source_decision_packet_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT
    ),
    source_phase_freeze_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT
    ),
    source_gameplay_gate_regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    source_calibration_sandbox_baseline_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    execution = _load_json(source_application_execution_path)
    application_execution_contract = _load_json_if_exists(
        source_application_execution_contract_path
    )
    final_gate = _load_json_if_exists(source_pre_application_final_gate_path)
    rollback_package = _load_json_if_exists(source_rollback_package_path)
    runtime_config_artifact = _load_json_if_exists(source_runtime_config_artifact_path)
    model_asset_ref = execution.get("model_asset_ref") or str(Path(model_asset_path))
    model_asset_sha = execution.get("model_asset_sha256") or _sha256_file(
        Path(model_asset_path)
    )
    inputs = {
        "review_packet_input_id": _stable_id(
            "controlled_runtime_calibration_application_execution_review_packet_inputs_v1",
            execution.get("application_execution_id"),
            execution.get("application_execution_status"),
            execution.get("runtime_config_target_sha256_before"),
            execution.get("runtime_config_target_sha256_after"),
        ),
        "review_packet_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUT_TYPE
        ),
        "review_packet_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_path": str(Path(source_application_execution_path)),
        "source_application_execution_contract_path": str(
            Path(source_application_execution_contract_path)
        ),
        "source_runtime_config_artifact_path": _path_string(
            source_runtime_config_artifact_path
        ),
        "source_rollback_package_path": _path_string(source_rollback_package_path),
        "source_pre_application_final_gate_path": _source_path(
            execution,
            "source_pre_application_final_gate_path",
            source_pre_application_final_gate_path,
        ),
        "source_runtime_application_staging_path": _source_path(
            execution,
            "source_runtime_application_staging_path",
            source_runtime_application_staging_path,
        ),
        "source_application_plan_path": _source_path(
            execution,
            "source_application_plan_path",
            source_application_plan_path,
        ),
        "source_human_approval_gate_path": _source_path(
            execution,
            "source_human_approval_gate_path",
            source_human_approval_gate_path,
        ),
        "source_dry_run_review_packet_path": _source_path(
            execution,
            "source_dry_run_review_packet_path",
            source_dry_run_review_packet_path,
        ),
        "source_dry_run_execution_report_path": _source_path(
            execution,
            "source_dry_run_execution_report_path",
            source_dry_run_execution_report_path,
        ),
        "source_change_request_path": _source_path(
            execution,
            "source_change_request_path",
            source_change_request_path,
        ),
        "source_candidate_config_freeze_path": _path_string(
            source_candidate_config_freeze_path
        ),
        "source_manual_approval_packet_path": _path_string(
            source_manual_approval_packet_path
        ),
        "source_decision_packet_path": _path_string(source_decision_packet_path),
        "source_phase_freeze_path": _path_string(source_phase_freeze_path),
        "source_gameplay_gate_regression_baseline_path": _path_string(
            source_gameplay_gate_regression_baseline_path
        ),
        "source_calibration_sandbox_baseline_path": _path_string(
            source_calibration_sandbox_baseline_path
        ),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha,
        "runtime_config_target_ref": _dict(execution.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": execution.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": execution.get(
            "runtime_config_target_sha256_after"
        ),
        "application_execution_status": execution.get("application_execution_status"),
        "runtime_application_status": execution.get("runtime_application_status"),
        "runtime_config_status": execution.get("runtime_config_status"),
        "mutation_status": execution.get("mutation_status"),
        "production_config_status": execution.get("production_config_status"),
        "baseline_update_status": execution.get("baseline_update_status"),
        "model_update_status": execution.get("model_update_status"),
        "atomic_write_status": execution.get("atomic_write_status"),
        "runtime_readback_status": execution.get("runtime_readback_status"),
        "rollback_package_status": execution.get("rollback_package_status"),
        "post_apply_verification_status": execution.get(
            "post_apply_verification_status"
        ),
        "source_application_execution_id": execution.get("application_execution_id"),
        "source_application_execution_contract_type": application_execution_contract.get(
            "contract_type"
        ),
        "source_pre_application_final_gate_status": final_gate.get("final_gate_status"),
        "selected_candidate_config_ref": _dict(
            execution.get("selected_candidate_config_ref")
        ),
        "operator_signoff_ref": _dict(final_gate.get("operator_signoff_ref")),
        "application_execution_blockers": _list(execution.get("blockers")),
        "final_gate_blockers": _list(final_gate.get("blockers")),
        "applied_config_delta": _dict(execution.get("applied_config_delta")),
        "current_settings_before": _dict(execution.get("current_settings_before")),
        "applied_settings_after": _dict(execution.get("applied_settings_after")),
        "post_apply_verification_report": _dict(
            execution.get("post_apply_verification_report")
        ),
        "rollback_package_ref": _dict(execution.get("rollback_package_ref")),
        "rollback_package": rollback_package or _dict(execution.get("rollback_package")),
        "runtime_config_artifact_ref": _artifact_ref(
            source_runtime_config_artifact_path,
            runtime_config_artifact,
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _source_artifact_refs(
            {
                "application_execution": source_application_execution_path,
                "application_execution_contract": (
                    source_application_execution_contract_path
                ),
                "runtime_config_artifact": source_runtime_config_artifact_path,
                "rollback_package": source_rollback_package_path,
                "pre_application_final_gate": source_pre_application_final_gate_path,
                "runtime_application_staging": source_runtime_application_staging_path,
                "application_plan": source_application_plan_path,
                "human_approval_gate": source_human_approval_gate_path,
                "dry_run_review_packet": source_dry_run_review_packet_path,
                "dry_run_execution_report": source_dry_run_execution_report_path,
                "change_request": source_change_request_path,
                "candidate_config_freeze": source_candidate_config_freeze_path,
                "manual_approval_packet": source_manual_approval_packet_path,
                "decision_packet": source_decision_packet_path,
                "phase_freeze": source_phase_freeze_path,
                "gameplay_gate_regression_baseline": (
                    source_gameplay_gate_regression_baseline_path
                ),
                "calibration_sandbox_baseline": (
                    source_calibration_sandbox_baseline_path
                ),
            }
        ),
        "warnings": {**_dict(execution.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_review_packet_inputs",
        "review_packet_input_id": inputs["review_packet_input_id"],
        "application_execution_status": inputs["application_execution_status"],
        "runtime_application_status": inputs["runtime_application_status"],
        "runtime_config_status": inputs["runtime_config_status"],
        "mutation_status": inputs["mutation_status"],
        "runtime_config_target_sha256_before": inputs[
            "runtime_config_target_sha256_before"
        ],
        "runtime_config_target_sha256_after": inputs[
            "runtime_config_target_sha256_after"
        ],
        "inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": inputs["warnings"],
    }


def validate_controlled_runtime_calibration_application_execution_review_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(review_packet_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_inputs_shape(inputs))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_application_execution_review_packet_inputs_validation"
        ),
        payload_path=review_packet_inputs_path,
        payload_type=inputs.get("review_packet_input_type"),
        payload_version=inputs.get("review_packet_input_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields=_status_snapshot(inputs),
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_application_execution_review_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(review_packet_inputs_path)
    outcome_summary = _execution_outcome_summary(inputs, generated_at)
    blocker_summary = _blocker_summary(inputs, generated_at)
    verification_summary = _verification_summary(inputs, generated_at)
    rollback_summary = _rollback_summary(inputs, generated_at)
    operator_checklist = _operator_review_checklist(inputs, generated_at)
    next_action = _next_action_recommendation(inputs, generated_at)
    review_packet_status = _review_packet_status(outcome_summary, inputs)
    packet = {
        "review_packet_id": _stable_id(
            "controlled_runtime_calibration_application_execution_review_packet_v1",
            inputs.get("review_packet_input_id"),
            outcome_summary.get("application_outcome_status"),
            inputs.get("runtime_config_target_sha256_before"),
            inputs.get("runtime_config_target_sha256_after"),
        ),
        "review_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_TYPE
        ),
        "review_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_input_path": str(Path(review_packet_inputs_path)),
        "source_application_execution_path": inputs.get(
            "source_application_execution_path"
        ),
        "source_pre_application_final_gate_path": inputs.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": inputs.get(
            "source_runtime_application_staging_path"
        ),
        "source_application_plan_path": inputs.get("source_application_plan_path"),
        "source_human_approval_gate_path": inputs.get(
            "source_human_approval_gate_path"
        ),
        "source_dry_run_review_packet_path": inputs.get(
            "source_dry_run_review_packet_path"
        ),
        "source_dry_run_execution_report_path": inputs.get(
            "source_dry_run_execution_report_path"
        ),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "selected_candidate_config_ref": _dict(
            inputs.get("selected_candidate_config_ref")
        ),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "runtime_config_target_ref": _dict(inputs.get("runtime_config_target_ref")),
        "runtime_config_target_sha256_before": inputs.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": inputs.get(
            "runtime_config_target_sha256_after"
        ),
        "application_execution_status": inputs.get("application_execution_status"),
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_status": inputs.get("runtime_config_status"),
        "mutation_status": inputs.get("mutation_status"),
        "production_config_status": inputs.get("production_config_status"),
        "baseline_update_status": inputs.get("baseline_update_status"),
        "model_update_status": inputs.get("model_update_status"),
        "atomic_write_status": inputs.get("atomic_write_status"),
        "runtime_readback_status": inputs.get("runtime_readback_status"),
        "rollback_package_status": inputs.get("rollback_package_status"),
        "post_apply_verification_status": inputs.get("post_apply_verification_status"),
        "execution_outcome_summary": outcome_summary,
        "blocker_summary": blocker_summary,
        "verification_summary": verification_summary,
        "rollback_summary": rollback_summary,
        "operator_review_checklist": operator_checklist,
        "next_action_recommendation": next_action,
        "review_packet_status": review_packet_status,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_refs": _dict(inputs.get("source_artifact_refs")),
        "warnings": {**_dict(inputs.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_inputs_shape(inputs))
    errors.extend(_validate_review_packet_shape(packet))
    _write_json_if_requested(output_path, packet)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_review_packet",
        "review_packet_id": packet["review_packet_id"],
        "review_packet_status": packet["review_packet_status"],
        "application_outcome_status": outcome_summary["application_outcome_status"],
        "runtime_application_status": packet["runtime_application_status"],
        "runtime_config_status": packet["runtime_config_status"],
        "mutation_status": packet["mutation_status"],
        "runtime_config_changed": outcome_summary["runtime_config_changed"],
        "next_action_recommendation": next_action["recommendation"],
        "review_packet_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": packet["warnings"],
    }


def validate_controlled_runtime_calibration_application_execution_review_packet(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(review_packet_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_shape(packet))
    result = _validation_result(
        validation_type=(
            "controlled_runtime_calibration_application_execution_review_packet_validation"
        ),
        payload_path=review_packet_path,
        payload_type=packet.get("review_packet_type"),
        payload_version=packet.get("review_packet_version"),
        contract_path=contract_path,
        validated_at=validated_at,
        errors=errors,
        status_fields={
            **_status_snapshot(packet),
            "review_packet_status": packet.get("review_packet_status"),
            "application_outcome_status": _dict(
                packet.get("execution_outcome_summary")
            ).get("application_outcome_status"),
            "verification_summary_status": _dict(
                packet.get("verification_summary")
            ).get("verification_summary_status"),
        },
    )
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_post_execution_summary(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_SUMMARY_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(review_packet_path)
    summary = {
        "summary_id": _stable_id(
            "controlled_runtime_calibration_post_execution_summary_v1",
            packet.get("review_packet_id"),
            packet.get("review_packet_status"),
        ),
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_SUMMARY_TYPE,
        "summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_id": packet.get("review_packet_id"),
        "source_review_packet_path": str(Path(review_packet_path)),
        "execution_outcome_summary": packet.get("execution_outcome_summary"),
        "verification_summary": packet.get("verification_summary"),
        "rollback_summary": packet.get("rollback_summary"),
        "next_action_recommendation": packet.get("next_action_recommendation"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_shape(packet))
    _write_json_if_requested(output_path, summary)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_summary",
        "summary_id": summary["summary_id"],
        "application_outcome_status": _dict(packet.get("execution_outcome_summary")).get(
            "application_outcome_status"
        ),
        "runtime_config_changed": _dict(packet.get("execution_outcome_summary")).get(
            "runtime_config_changed"
        ),
        "summary_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_post_execution_blocker_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_BLOCKER_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(review_packet_path)
    blocker_summary = _dict(packet.get("blocker_summary"))
    report = {
        "blocker_report_id": _stable_id(
            "controlled_runtime_calibration_post_execution_blocker_report_v1",
            packet.get("review_packet_id"),
            blocker_summary.get("blocked_reason_count"),
        ),
        "blocker_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_BLOCKER_REPORT_TYPE
        ),
        "blocker_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_id": packet.get("review_packet_id"),
        "source_review_packet_path": str(Path(review_packet_path)),
        "blocker_summary": blocker_summary,
        "next_action_recommendation": packet.get("next_action_recommendation"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_shape(packet))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_blocker_report",
        "blocker_report_id": report["blocker_report_id"],
        "blocked_reason_count": blocker_summary.get("blocked_reason_count"),
        "blocker_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_post_execution_operator_checklist(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_OPERATOR_CHECKLIST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(review_packet_path)
    checklist = {
        "operator_checklist_report_id": _stable_id(
            "controlled_runtime_calibration_post_execution_operator_checklist_v1",
            packet.get("review_packet_id"),
        ),
        "operator_checklist_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_OPERATOR_CHECKLIST_TYPE
        ),
        "operator_checklist_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_id": packet.get("review_packet_id"),
        "source_review_packet_path": str(Path(review_packet_path)),
        "operator_review_checklist": packet.get("operator_review_checklist"),
        "next_action_recommendation": packet.get("next_action_recommendation"),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_shape(packet))
    _write_json_if_requested(output_path, checklist)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_checklist",
        "operator_checklist_report_id": checklist["operator_checklist_report_id"],
        "check_count": len(OPERATOR_CHECKLIST_REQUIRED_FIELDS),
        "operator_checklist_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_post_execution_next_action_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_NEXT_ACTION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    packet = _load_json(review_packet_path)
    next_action = _dict(packet.get("next_action_recommendation"))
    report = {
        "next_action_report_id": _stable_id(
            "controlled_runtime_calibration_post_execution_next_action_report_v1",
            packet.get("review_packet_id"),
            next_action.get("recommendation"),
        ),
        "next_action_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_EXECUTION_NEXT_ACTION_REPORT_TYPE
        ),
        "next_action_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_id": packet.get("review_packet_id"),
        "source_review_packet_path": str(Path(review_packet_path)),
        "next_action_recommendation": next_action,
        "post_execution_human_review_required": True,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_review_packet_shape(packet))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_next_action_report",
        "next_action_report_id": report["next_action_report_id"],
        "next_action_recommendation": next_action.get("recommendation"),
        "next_action_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _execution_outcome_summary(
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    application_outcome_status = _application_outcome_status(inputs)
    sha_before = inputs.get("runtime_config_target_sha256_before")
    sha_after = inputs.get("runtime_config_target_sha256_after")
    runtime_config_changed = bool(sha_before and sha_after and sha_before != sha_after)
    blockers = _blockers(inputs)
    return {
        "outcome_summary_id": _stable_id(
            "controlled_runtime_calibration_post_execution_outcome_summary_v1",
            inputs.get("source_application_execution_id"),
            application_outcome_status,
            sha_before,
            sha_after,
        ),
        "outcome_summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": inputs.get("source_application_execution_id"),
        "application_outcome_status": application_outcome_status,
        "runtime_application_status": inputs.get("runtime_application_status"),
        "runtime_config_status": inputs.get("runtime_config_status"),
        "mutation_status": inputs.get("mutation_status"),
        "applied_delta_present": _applied_delta_present(inputs),
        "runtime_config_sha_before": sha_before,
        "runtime_config_sha_after": sha_after,
        "runtime_config_changed": runtime_config_changed,
        "blocked_reason_count": len(blockers),
        "blocker_types": blockers,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocker_summary(inputs: dict[str, Any], generated_at: datetime) -> dict[str, Any]:
    blockers = _blockers(inputs)
    final_gate_status = inputs.get("source_pre_application_final_gate_status")
    return {
        "blocker_summary_id": _stable_id(
            "controlled_runtime_calibration_post_execution_blocker_summary_v1",
            inputs.get("source_application_execution_id"),
            blockers,
        ),
        "blocker_summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": inputs.get("source_application_execution_id"),
        "blocked_reason_count": len(blockers),
        "blocker_types": blockers,
        "final_gate_status": final_gate_status,
        "operator_signoff_missing": _contains_any(blockers, ["operator_signoff"]),
        "selected_candidate_missing": _contains_any(blockers, ["no_candidate"]),
        "final_gate_not_passed": final_gate_status
        not in {"final_gate_passed_not_applied", "not_applicable"},
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _verification_summary(
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    post_apply = _dict(inputs.get("post_apply_verification_report"))
    outcome_status = _application_outcome_status(inputs)
    model_asset_check = _model_asset_hash_check(inputs)
    baseline_check = _dict(post_apply.get("baseline_replacement_check")) or {
        "status": inputs.get("baseline_update_status"),
        "baseline_not_replaced": inputs.get("baseline_update_status") == "not_replaced",
    }
    production_check = _dict(post_apply.get("production_config_check")) or {
        "status": inputs.get("production_config_status"),
        "production_config_not_created": (
            inputs.get("production_config_status") == "not_created"
        ),
    }
    if outcome_status == "application_blocked_safely_before_runtime_mutation":
        verification_status = "verification_passed_for_blocked_execution"
    elif outcome_status in {
        "application_executed_controlled_runtime_config_write",
        "application_executed_with_warnings_controlled_runtime_config_write",
    }:
        verification_status = "verification_passed_for_controlled_application"
    else:
        verification_status = "verification_blocked"
    return {
        "verification_summary_id": _stable_id(
            "controlled_runtime_calibration_post_execution_verification_summary_v1",
            inputs.get("source_application_execution_id"),
            verification_status,
        ),
        "verification_summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": inputs.get("source_application_execution_id"),
        "multi_point_regression_gate_result": _dict(
            post_apply.get("multi_point_regression_gate_result")
        ),
        "protected_sample_point_gate_result": _dict(
            post_apply.get("protected_sample_point_gate_result")
        ),
        "gameplay_gate_regression_baseline_result": _dict(
            post_apply.get("gameplay_gate_regression_baseline_result")
        ),
        "calibration_sandbox_regression_baseline_result": _dict(
            post_apply.get("calibration_sandbox_regression_baseline_result")
        ),
        "runtime_readback_result": _dict(post_apply.get("runtime_readback_result"))
        or {"runtime_readback_status": inputs.get("runtime_readback_status")},
        "model_asset_hash_check": model_asset_check,
        "baseline_replacement_check": baseline_check,
        "production_config_check": production_check,
        "verification_summary_status": verification_status,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _rollback_summary(inputs: dict[str, Any], generated_at: datetime) -> dict[str, Any]:
    rollback_package = _dict(inputs.get("rollback_package"))
    rollback_ref = _dict(inputs.get("rollback_package_ref"))
    mutation_status = inputs.get("mutation_status")
    runtime_config_changed = inputs.get("runtime_config_target_sha256_before") != inputs.get(
        "runtime_config_target_sha256_after"
    )
    rollback_needed = mutation_status != "no_runtime_mutation_due_to_blocker" and bool(
        runtime_config_changed
    )
    rollback_status = inputs.get("rollback_package_status") or rollback_package.get(
        "rollback_status"
    )
    return {
        "rollback_summary_id": _stable_id(
            "controlled_runtime_calibration_post_execution_rollback_summary_v1",
            inputs.get("source_application_execution_id"),
            rollback_status,
            rollback_needed,
        ),
        "rollback_summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": inputs.get("source_application_execution_id"),
        "rollback_package_ref": rollback_ref,
        "rollback_package_status": rollback_status,
        "rollback_needed": rollback_needed,
        "rollback_ready": rollback_status == "rollback_package_created",
        "rollback_reason": (
            "no_runtime_mutation_due_to_blocker"
            if not rollback_needed
            else "controlled_runtime_config_change_requires_reviewable_rollback"
        ),
        "rollback_verification_gates": _list(
            rollback_package.get("rollback_verification_gates")
        ),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _operator_review_checklist(
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    for field in OPERATOR_CHECKLIST_REQUIRED_FIELDS:
        checks[field] = {
            "required": True,
            "status": "post_execution_human_review_required",
        }
    checks["checklist_id"] = _stable_id(
        "controlled_runtime_calibration_post_execution_operator_checklist_v1",
        inputs.get("source_application_execution_id"),
    )
    checks["checklist_version"] = (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
    )
    checks["generated_at"] = generated_at.isoformat()
    checks["source_application_execution_id"] = inputs.get(
        "source_application_execution_id"
    )
    checks["warnings"] = dict(WARNINGS)
    checks["non_claims"] = dict(NON_CLAIMS)
    return checks


def _next_action_recommendation(
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    blockers = _blockers(inputs)
    outcome_status = _application_outcome_status(inputs)
    if _contains_any(blockers, ["operator_signoff"]):
        recommendation = "resolve_operator_signoff_before_reapplying"
        reason = "operator signoff is required before a future controlled application attempt"
    elif _contains_any(blockers, ["no_candidate"]):
        recommendation = "resolve_selected_candidate_before_reapplying"
        reason = "selected candidate is required before a future controlled application attempt"
    elif outcome_status == "application_blocked_safely_before_runtime_mutation":
        recommendation = "rerun_final_gate_after_operator_signoff"
        reason = "final gate did not allow runtime application"
    elif outcome_status in {
        "application_executed_controlled_runtime_config_write",
        "application_executed_with_warnings_controlled_runtime_config_write",
    }:
        recommendation = "proceed_to_post_application_review_after_controlled_apply"
        reason = "controlled application path reported a runtime config write"
    elif outcome_status == "application_failed_requires_rollback_followup":
        recommendation = "prepare_rollback_followup"
        reason = "application failure requires rollback follow-up review"
    else:
        recommendation = "no_runtime_action_recommended"
        reason = "packet is informational only"
    return {
        "next_action_report_id": _stable_id(
            "controlled_runtime_calibration_post_execution_next_action_v1",
            inputs.get("source_application_execution_id"),
            recommendation,
        ),
        "next_action_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": inputs.get("source_application_execution_id"),
        "recommendation": recommendation,
        "reason": reason,
        "post_execution_human_review_required": True,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _application_outcome_status(inputs: dict[str, Any]) -> str:
    application_status = inputs.get("application_execution_status")
    mutation_status = inputs.get("mutation_status")
    atomic_write_status = inputs.get("atomic_write_status")
    runtime_application_status = inputs.get("runtime_application_status")
    if application_status == "application_executed_controlled_runtime_config_write":
        return "application_executed_controlled_runtime_config_write"
    if application_status == "application_executed_with_warnings_controlled_runtime_config_write":
        return "application_executed_with_warnings_controlled_runtime_config_write"
    if atomic_write_status == "atomic_write_restored_previous_config":
        return "application_failed_and_restored_previous_config"
    if atomic_write_status == "atomic_write_failed":
        return "application_failed_requires_rollback_followup"
    if (
        runtime_application_status == "blocked_from_runtime_application"
        or mutation_status == "no_runtime_mutation_due_to_blocker"
        or str(application_status or "").startswith("application_blocked")
    ):
        return "application_blocked_safely_before_runtime_mutation"
    if application_status == "not_applicable":
        return "not_applicable"
    return "application_outcome_unknown"


def _review_packet_status(
    outcome_summary: dict[str, Any],
    inputs: dict[str, Any],
) -> str:
    outcome_status = outcome_summary.get("application_outcome_status")
    if outcome_status == "application_blocked_safely_before_runtime_mutation":
        return "review_packet_created_for_blocked_execution"
    if outcome_status in {
        "application_executed_controlled_runtime_config_write",
        "application_executed_with_warnings_controlled_runtime_config_write",
    }:
        if _blockers(inputs):
            return "review_packet_created_with_warnings"
        return "review_packet_created_for_controlled_application"
    if not inputs.get("source_application_execution_path"):
        return "review_packet_blocked_missing_execution_artifact"
    return "review_packet_informational_only"


def _applied_delta_present(inputs: dict[str, Any]) -> bool:
    delta = _dict(inputs.get("applied_config_delta"))
    for item in _list(delta.get("delta_applied")):
        if isinstance(item, dict) and item.get("change_applied") is True:
            return True
    return False


def _model_asset_hash_check(inputs: dict[str, Any]) -> dict[str, Any]:
    model_asset_ref = inputs.get("model_asset_ref")
    expected_sha = inputs.get("model_asset_sha256")
    current_sha = _sha256_file(Path(model_asset_ref)) if model_asset_ref else None
    return {
        "status": "present" if current_sha else "not_applicable",
        "model_asset_ref": model_asset_ref,
        "expected_sha256": expected_sha,
        "current_sha256": current_sha,
        "model_weights_not_modified": current_sha in {None, expected_sha},
    }


def _blockers(inputs: dict[str, Any]) -> list[str]:
    return _unique_strings(
        [
            *_list(inputs.get("application_execution_blockers")),
            *_list(inputs.get("final_gate_blockers")),
        ]
    )


def _contains_any(values: list[str], needles: list[str]) -> bool:
    return any(any(needle in value for needle in needles) for value in values)


def _source_path(payload: dict[str, Any], key: str, fallback: str | Path | None) -> str | None:
    value = payload.get(key)
    return str(value) if value else _path_string(fallback)


def _artifact_ref(path: str | Path | None, payload: dict[str, Any]) -> dict[str, Any]:
    if path is None:
        return {"path": None, "exists": False}
    return {
        "path": str(Path(path)),
        "exists": Path(path).exists(),
        "artifact_type": (
            payload.get("runtime_config_type")
            or payload.get("rollback_package_type")
            or payload.get("contract_type")
        ),
        "artifact_version": (
            payload.get("runtime_config_version")
            or payload.get("rollback_package_version")
            or payload.get("contract_version")
        ),
    }


def _source_artifact_refs(paths: dict[str, str | Path | None]) -> dict[str, Any]:
    return {key: _artifact_ref(path, _load_json_if_exists(path)) for key, path in paths.items()}


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    required = [
        "contract_type",
        "contract_version",
        "exported_at",
        "review_packet_scope",
        "source_contract_refs",
        "review_packet_input_schema",
        "review_packet_schema",
        "post_execution_summary_schema",
        "blocker_report_schema",
        "operator_checklist_schema",
        "next_action_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ]
    errors.extend(_missing_required(contract, required, "contract"))
    if contract.get("contract_type") not in {
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_CONTRACT_TYPE
    }:
        errors.append(
            _error(
                "invalid_contract_type",
                "contract_type",
                contract.get("contract_type"),
            )
        )
    errors.extend(_validate_non_claims(_dict(contract.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(contract))
    return errors


def _validate_review_packet_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(inputs, REVIEW_PACKET_INPUT_REQUIRED_FIELDS, "inputs")
    errors.extend(
        _validate_status(
            "runtime_application_status",
            inputs.get("runtime_application_status"),
            ALLOWED_RUNTIME_APPLICATION_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "runtime_config_status",
            inputs.get("runtime_config_status"),
            ALLOWED_RUNTIME_CONFIG_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "mutation_status",
            inputs.get("mutation_status"),
            ALLOWED_MUTATION_STATUSES,
        )
    )
    errors.extend(_validate_safety_statuses(inputs))
    errors.extend(_validate_non_claims(_dict(inputs.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(inputs))
    return errors


def _validate_review_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _missing_required(packet, REVIEW_PACKET_REQUIRED_FIELDS, "review_packet")
    errors.extend(
        _validate_status(
            "review_packet_status",
            packet.get("review_packet_status"),
            ALLOWED_REVIEW_PACKET_STATUSES,
        )
    )
    errors.extend(_validate_summary_shapes(packet))
    errors.extend(_validate_safety_statuses(packet))
    errors.extend(_validate_blocked_hash_behavior(packet))
    errors.extend(_validate_non_claims(_dict(packet.get("non_claims"))))
    errors.extend(_validate_no_forbidden_tokens(packet))
    return errors


def _validate_summary_shapes(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    outcome = _dict(packet.get("execution_outcome_summary"))
    verification = _dict(packet.get("verification_summary"))
    rollback = _dict(packet.get("rollback_summary"))
    checklist = _dict(packet.get("operator_review_checklist"))
    next_action = _dict(packet.get("next_action_recommendation"))
    errors.extend(_missing_required(outcome, OUTCOME_SUMMARY_REQUIRED_FIELDS, "outcome_summary"))
    errors.extend(
        _validate_status(
            "application_outcome_status",
            outcome.get("application_outcome_status"),
            ALLOWED_APPLICATION_OUTCOME_STATUSES,
        )
    )
    errors.extend(
        _missing_required(
            verification,
            VERIFICATION_SUMMARY_REQUIRED_FIELDS,
            "verification_summary",
        )
    )
    errors.extend(
        _validate_status(
            "verification_summary_status",
            verification.get("verification_summary_status"),
            ALLOWED_VERIFICATION_SUMMARY_STATUSES,
        )
    )
    errors.extend(_missing_required(rollback, ROLLBACK_SUMMARY_REQUIRED_FIELDS, "rollback_summary"))
    errors.extend(
        _validate_status(
            "rollback_package_status",
            rollback.get("rollback_package_status"),
            ALLOWED_ROLLBACK_PACKAGE_STATUSES,
        )
    )
    errors.extend(
        _missing_required(
            checklist,
            OPERATOR_CHECKLIST_REQUIRED_FIELDS,
            "operator_review_checklist",
        )
    )
    errors.extend(
        _validate_status(
            "next_action_recommendation",
            next_action.get("recommendation"),
            ALLOWED_NEXT_ACTION_RECOMMENDATIONS,
        )
    )
    return errors


def _validate_safety_statuses(payload: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    errors.extend(
        _validate_status(
            "production_config_status",
            payload.get("production_config_status"),
            ALLOWED_PRODUCTION_CONFIG_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "baseline_update_status",
            payload.get("baseline_update_status"),
            ALLOWED_BASELINE_UPDATE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "model_update_status",
            payload.get("model_update_status"),
            ALLOWED_MODEL_UPDATE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "atomic_write_status",
            payload.get("atomic_write_status"),
            ALLOWED_ATOMIC_WRITE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "runtime_readback_status",
            payload.get("runtime_readback_status"),
            ALLOWED_RUNTIME_READBACK_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "rollback_package_status",
            payload.get("rollback_package_status"),
            ALLOWED_ROLLBACK_PACKAGE_STATUSES,
        )
    )
    errors.extend(
        _validate_status(
            "post_apply_verification_status",
            payload.get("post_apply_verification_status"),
            ALLOWED_POST_APPLY_VERIFICATION_STATUSES,
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
    return errors


def _validate_blocked_hash_behavior(payload: dict[str, Any]) -> list[dict[str, Any]]:
    outcome = _dict(payload.get("execution_outcome_summary"))
    if outcome.get("application_outcome_status") != (
        "application_blocked_safely_before_runtime_mutation"
    ):
        return []
    before = payload.get("runtime_config_target_sha256_before")
    after = payload.get("runtime_config_target_sha256_after")
    if before and after and before != after:
        return [
            _error(
                "blocked_execution_runtime_config_hash_mismatch",
                "runtime_config_target_sha256_after",
                after,
            )
        ]
    if outcome.get("runtime_config_changed") is True:
        return [
            _error(
                "blocked_execution_runtime_config_changed",
                "runtime_config_changed",
                outcome.get("runtime_config_changed"),
            )
        ]
    return []


def _validate_non_claims(non_claims: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key, expected in NON_CLAIMS.items():
        if non_claims.get(key) is not expected:
            errors.append(_error("missing_non_claim", f"non_claims.{key}", non_claims.get(key)))
    return errors


def _validate_status(field: str, value: Any, allowed: list[str]) -> list[dict[str, Any]]:
    if value in allowed:
        return []
    return [_error("invalid_status", field, value)]


def _validate_no_forbidden_tokens(payload: Any, path: str = "$") -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_REVIEW_PACKET_TOKENS:
                errors.append(_error("forbidden_key", f"{path}.{key}", key))
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_validate_no_forbidden_tokens(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_REVIEW_PACKET_TOKENS:
        errors.append(_error("forbidden_value", path, payload))
    return errors


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
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        **status_fields,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def _status_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "application_execution_status": payload.get("application_execution_status"),
        "runtime_application_status": payload.get("runtime_application_status"),
        "runtime_config_status": payload.get("runtime_config_status"),
        "mutation_status": payload.get("mutation_status"),
        "production_config_status": payload.get("production_config_status"),
        "baseline_update_status": payload.get("baseline_update_status"),
        "model_update_status": payload.get("model_update_status"),
        "atomic_write_status": payload.get("atomic_write_status"),
        "runtime_readback_status": payload.get("runtime_readback_status"),
        "rollback_package_status": payload.get("rollback_package_status"),
        "post_apply_verification_status": payload.get("post_apply_verification_status"),
    }


def _source_contract_refs() -> dict[str, str]:
    return dict(SOURCE_CONTRACT_REFS)


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_REVIEW_PACKET_BLUEPRINT_NAME
        ),
    }


def _write_json_if_requested(output_path: str | Path | None, payload: dict[str, Any]) -> None:
    if output_path is None:
        return
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_json_if_exists(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    path_obj = Path(path)
    if not path_obj.exists():
        return {}
    return _load_json(path_obj)


def _stable_id(prefix: str, *parts: Any) -> str:
    raw = json.dumps(parts, sort_keys=True, default=str)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _path_string(path: str | Path | None) -> str | None:
    if path is None:
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value not in result:
            result.append(value)
    return result


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def _error(code: str, path: str, value: Any) -> dict[str, Any]:
    return {"code": code, "path": path, "value": value}
