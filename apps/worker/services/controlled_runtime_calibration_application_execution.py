from __future__ import annotations

import hashlib
import json
import os
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
    CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_pre_application_final_gate import (
    SOURCE_CONTRACT_REFS as PRE_APPLICATION_FINAL_GATE_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.controlled_runtime_calibration_runtime_application_staging import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT,
)
from apps.worker.services.gameplay_gate_regression_baseline import (
    DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    DEFAULT_HYSTERESIS_ENTER,
    DEFAULT_HYSTERESIS_EXIT,
    DEFAULT_SMOOTHING_WINDOW,
    DEFAULT_THRESHOLD,
)
from apps.worker.services.real_broadcast_gameplay_calibration_decision_phase_freeze import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT,
)

CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_TYPE = (
    "controlled_runtime_calibration_application_execution_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_TYPE = (
    "controlled_runtime_calibration_application_execution_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_TYPE = (
    "controlled_runtime_calibration_application_execution"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_TYPE = (
    "controlled_runtime_calibration_applied_runtime_config"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_CONFIG_UPDATE_RECORD_TYPE = (
    "controlled_runtime_calibration_runtime_config_update_record"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_READBACK_TYPE = (
    "controlled_runtime_calibration_runtime_readback_verification"
)
CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PACKAGE_TYPE = (
    "controlled_runtime_calibration_application_rollback_package"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_APPLY_VERIFICATION_TYPE = (
    "controlled_runtime_calibration_post_apply_verification_report"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_AUDIT_REPORT_TYPE = (
    "controlled_runtime_calibration_application_audit_report"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_BLUEPRINT = "blueprint_62"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_application_execution_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_application_execution_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUTS_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_application_execution_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_application_execution_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_application_execution_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_application_execution.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_applied_runtime_config_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_ROLLBACK_PACKAGE_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_application_rollback_package_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_READBACK_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_runtime_readback.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_AUDIT_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_application_audit_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_APPLY_VERIFICATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_post_apply_verification.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_pre_application_final_gate_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION
    ),
    **dict(PRE_APPLICATION_FINAL_GATE_SOURCE_CONTRACT_REFS),
}

ALLOWED_APPLICATION_EXECUTION_STATUSES = [
    "application_executed_controlled_runtime_config_write",
    "application_executed_with_warnings_controlled_runtime_config_write",
    "application_blocked_missing_final_gate",
    "application_blocked_final_gate_not_passed",
    "application_blocked_missing_staging_artifact",
    "application_blocked_missing_application_plan",
    "application_blocked_missing_human_approval_gate",
    "application_blocked_missing_change_request",
    "application_blocked_missing_candidate_config",
    "application_blocked_missing_operator_signoff",
    "application_blocked_missing_rollback_package",
    "application_blocked_missing_pre_apply_manifest",
    "application_blocked_missing_post_application_verification_plan",
    "application_blocked_missing_regression_gate",
    "application_blocked_delta_mismatch",
    "application_blocked_model_asset_hash_mismatch",
    "application_blocked_runtime_config_target_missing",
    "application_blocked_unsafe_config_target",
    "application_blocked_unresolved_blockers",
    "application_blocked_breaking_structural_change",
    "application_blocked_pre_apply_gate_failed",
    "application_blocked_post_apply_verification_failed",
    "application_blocked_runtime_readback_failed",
    "application_informational_only",
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
    "not_applicable",
]
ALLOWED_POST_APPLY_VERIFICATION_STATUSES = [
    "post_apply_verification_passed",
    "post_apply_verification_passed_with_warnings",
    "post_apply_verification_failed",
    "post_apply_verification_blocked",
    "not_applicable",
]

APPLICATION_EXECUTION_INPUT_REQUIRED_FIELDS = [
    "application_execution_input_id",
    "application_execution_input_type",
    "application_execution_input_version",
    "generated_at",
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
    "current_runtime_settings",
    "staged_candidate_settings",
    "staged_config_delta_ref",
    "operator_signoff_ref",
    "pre_apply_manifest_ref",
    "rollback_staging_ref",
    "post_application_verification_staging_ref",
    "future_baseline_policy_ref",
    "warnings",
    "non_claims",
]

APPLICATION_EXECUTION_REQUIRED_FIELDS = [
    "application_execution_id",
    "application_execution_type",
    "application_execution_version",
    "generated_at",
    "source_application_execution_input_path",
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
    "current_settings_before",
    "applied_settings_after",
    "applied_config_delta",
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
    "required_regression_gates",
    "post_apply_regression_results",
    "audit_record",
    "rollback_package_ref",
    "blockers",
    "warnings",
    "non_claims",
]

RUNTIME_CONFIG_UPDATE_RECORD_REQUIRED_FIELDS = [
    "update_record_id",
    "update_record_type",
    "update_record_version",
    "generated_at",
    "runtime_config_target_ref",
    "sha256_before",
    "sha256_after",
    "settings_before",
    "settings_after",
    "delta_applied",
    "atomic_write_status",
    "readback_status",
    "warnings",
    "non_claims",
]

ROLLBACK_PACKAGE_REQUIRED_FIELDS = [
    "rollback_package_id",
    "rollback_package_type",
    "rollback_package_version",
    "generated_at",
    "source_application_execution_id",
    "runtime_config_target_ref",
    "rollback_target_sha256",
    "rollback_target_settings",
    "rollback_trigger_conditions",
    "rollback_execution_steps",
    "rollback_verification_gates",
    "rollback_status",
    "non_claims",
]

POST_APPLY_VERIFICATION_REQUIRED_FIELDS = [
    "post_apply_verification_id",
    "post_apply_verification_type",
    "post_apply_verification_version",
    "generated_at",
    "source_application_execution_id",
    "required_regression_gates",
    "multi_point_regression_gate_result",
    "protected_sample_point_gate_result",
    "gameplay_gate_regression_baseline_result",
    "calibration_sandbox_regression_baseline_result",
    "runtime_readback_result",
    "model_asset_hash_check",
    "baseline_replacement_check",
    "production_config_check",
    "verification_status",
    "blockers",
    "warnings",
    "non_claims",
]

WARNINGS = {
    "controlled_runtime_calibration_application_execution": True,
    "controlled_runtime_config_update": True,
    "post_apply_verification_required": True,
    "post_apply_review_required": True,
    "rollback_package_required": True,
    "application_execution_is_not_truth": True,
    "application_execution_is_not_accuracy_scoring": True,
    "application_execution_is_not_model_training": True,
    "application_execution_is_not_production_config": True,
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
    "application_execution_is_not_truth": True,
    "application_execution_is_not_accuracy_scoring": True,
    "application_execution_is_not_model_training": True,
    "application_execution_is_not_production_config": True,
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
    "post_apply_review_required": True,
    "rollback_package_required": True,
}


def _forbidden_token(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_APPLICATION_EXECUTION_TOKENS = {
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


def export_controlled_runtime_calibration_application_execution_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_EXPORTED_AT
    contract = {
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_TYPE,
        "contract_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "application_execution_scope": {
            "consumes_pre_application_final_gate": True,
            "requires_passed_final_gate_before_staged_delta_application": True,
            "updates_runtime_configuration": True,
            "runtime_config_update_mode": (
                "runtime_config_updated_only_by_controlled_application_execution"
            ),
            "writes_only_explicit_controlled_runtime_config_target": True,
            "creates_production_configuration": False,
            "updates_model_weights": False,
            "replaces_regression_baselines": False,
            "performs_automatic_approval": False,
            "performs_automatic_rejection": False,
            "scores_classifier_outputs": False,
            "requires_atomic_write": True,
            "requires_runtime_readback": True,
            "requires_rollback_package": True,
            "requires_post_apply_verification": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "application_execution_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_TYPE,
            "input_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_VERSION,
            "required_fields": list(APPLICATION_EXECUTION_INPUT_REQUIRED_FIELDS),
        },
        "application_execution_schema": {
            "artifact_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_TYPE,
            "artifact_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
            "required_fields": list(APPLICATION_EXECUTION_REQUIRED_FIELDS),
            "allowed_application_execution_statuses": list(
                ALLOWED_APPLICATION_EXECUTION_STATUSES
            ),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_runtime_config_statuses": list(ALLOWED_RUNTIME_CONFIG_STATUSES),
            "allowed_mutation_statuses": list(ALLOWED_MUTATION_STATUSES),
            "allowed_atomic_write_statuses": list(ALLOWED_ATOMIC_WRITE_STATUSES),
            "required_successful_execution_statuses": {
                "application_execution_status": (
                    "application_executed_controlled_runtime_config_write"
                ),
                "runtime_application_status": "applied_by_controlled_blueprint",
                "runtime_config_status": "updated_by_controlled_application",
                "mutation_status": "controlled_runtime_config_mutation_performed",
                "production_config_status": "not_created",
                "baseline_update_status": "not_replaced",
                "model_update_status": "not_modified",
                "atomic_write_status": "atomic_write_completed",
                "runtime_readback_status": "readback_verified",
                "rollback_package_status": "rollback_package_created",
            },
        },
        "runtime_config_update_schema": {
            "update_record_type": CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_CONFIG_UPDATE_RECORD_TYPE,
            "update_record_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
            "required_fields": list(RUNTIME_CONFIG_UPDATE_RECORD_REQUIRED_FIELDS),
            "target_artifact_type": CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_TYPE,
            "default_target_path": (
                DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_OUTPUT
            ),
            "target_is_not_production_config": True,
            "target_is_not_model_weights": True,
            "target_is_not_baseline": True,
        },
        "runtime_readback_schema": {
            "readback_type": CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_READBACK_TYPE,
            "readback_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
            "allowed_readback_statuses": list(ALLOWED_RUNTIME_READBACK_STATUSES),
        },
        "rollback_package_schema": {
            "rollback_package_type": CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PACKAGE_TYPE,
            "rollback_package_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION
            ),
            "required_fields": list(ROLLBACK_PACKAGE_REQUIRED_FIELDS),
            "allowed_rollback_package_statuses": list(ALLOWED_ROLLBACK_PACKAGE_STATUSES),
        },
        "post_apply_verification_schema": {
            "post_apply_verification_type": (
                CONTROLLED_RUNTIME_CALIBRATION_POST_APPLY_VERIFICATION_TYPE
            ),
            "post_apply_verification_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION
            ),
            "required_fields": list(POST_APPLY_VERIFICATION_REQUIRED_FIELDS),
            "allowed_post_apply_verification_statuses": list(
                ALLOWED_POST_APPLY_VERIFICATION_STATUSES
            ),
            "required_gates": _default_required_regression_gate_names(),
        },
        "audit_record_schema": {
            "audit_report_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_AUDIT_REPORT_TYPE,
            "audit_report_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
            "records_before_after_hashes": True,
            "records_source_artifact_paths": True,
            "records_atomic_write_status": True,
            "records_readback_status": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_application_execution_input_shape": True,
            "validate_application_execution_artifact_shape": True,
            "validate_runtime_config_update_record_shape": True,
            "validate_rollback_package_shape": True,
            "validate_post_apply_verification_report_shape": True,
            "validate_allowed_statuses": True,
            "validate_model_not_modified": True,
            "validate_production_config_not_created": True,
            "validate_baseline_not_replaced": True,
            "validate_runtime_config_target_is_explicit_and_safe": True,
            "validate_runtime_config_update_linked_to_required_artifacts": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_config_execution_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
        },
        "provenance_requirements": {
            "pre_application_final_gate_path_required": True,
            "runtime_application_staging_path_required": True,
            "application_plan_path_required": True,
            "human_approval_gate_path_required": True,
            "dry_run_review_packet_path_required": True,
            "dry_run_execution_report_path_required": True,
            "change_request_path_required": True,
            "candidate_config_freeze_path_required": True,
            "model_asset_hash_required": True,
            "runtime_config_target_ref_required": True,
            "runtime_config_before_hash_required_when_target_exists": True,
            "runtime_config_after_hash_required_after_write": True,
            "rollback_package_required": True,
            "post_apply_verification_required": True,
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


def build_controlled_runtime_calibration_application_execution_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
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
    runtime_config_target_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    source_payloads = {
        "pre_application_final_gate": _load_json_if_exists(
            source_pre_application_final_gate_path
        ),
        "runtime_application_staging": _load_json_if_exists(
            source_runtime_application_staging_path
        ),
        "application_plan": _load_json_if_exists(source_application_plan_path),
        "human_approval_gate": _load_json_if_exists(source_human_approval_gate_path),
        "dry_run_review_packet": _load_json_if_exists(
            source_dry_run_review_packet_path
        ),
        "dry_run_execution_report": _load_json_if_exists(
            source_dry_run_execution_report_path
        ),
        "change_request": _load_json_if_exists(source_change_request_path),
        "candidate_config_freeze": _load_json_if_exists(
            source_candidate_config_freeze_path
        ),
        "manual_approval_packet": _load_json_if_exists(
            source_manual_approval_packet_path
        ),
        "decision_packet": _load_json_if_exists(source_decision_packet_path),
        "phase_freeze": _load_json_if_exists(source_phase_freeze_path),
        "gameplay_gate_regression_baseline": _load_json_if_exists(
            source_gameplay_gate_regression_baseline_path
        ),
        "calibration_sandbox_baseline": _load_json_if_exists(
            source_calibration_sandbox_baseline_path
        ),
    }
    final_gate = source_payloads["pre_application_final_gate"]
    staging = source_payloads["runtime_application_staging"]
    target_path = Path(runtime_config_target_path)
    target_payload = _load_json_if_exists(target_path)
    current_settings = _settings_from_source(
        final_gate.get("current_settings"),
        staging.get("current_settings"),
        source_payloads["application_plan"].get("current_settings"),
    )
    staged_candidate_settings = _dict(
        final_gate.get("staged_candidate_settings")
    ) or _dict(staging.get("staged_candidate_settings"))
    staged_config_delta_ref = _dict(
        final_gate.get("staged_config_delta_ref")
    ) or _dict(staging.get("staged_config_delta"))
    source_presence = _source_artifact_presence(
        source_payloads,
        {
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
            "calibration_sandbox_baseline": source_calibration_sandbox_baseline_path,
        },
    )
    inputs = {
        "application_execution_input_id": _stable_id(
            "controlled_runtime_calibration_application_execution_inputs_v1",
            final_gate.get("final_gate_id"),
            staging.get("staging_id"),
            _path_string(runtime_config_target_path),
            staged_config_delta_ref,
        ),
        "application_execution_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_TYPE
        ),
        "application_execution_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_pre_application_final_gate_path": _path_string(
            source_pre_application_final_gate_path
        ),
        "source_runtime_application_staging_path": _path_string(
            source_runtime_application_staging_path
        ),
        "source_application_plan_path": _path_string(source_application_plan_path),
        "source_human_approval_gate_path": _path_string(
            source_human_approval_gate_path
        ),
        "source_dry_run_review_packet_path": _path_string(
            source_dry_run_review_packet_path
        ),
        "source_dry_run_execution_report_path": _path_string(
            source_dry_run_execution_report_path
        ),
        "source_change_request_path": _path_string(source_change_request_path),
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
        "source_pre_application_final_gate_id": final_gate.get("final_gate_id"),
        "source_pre_application_final_gate_status": final_gate.get(
            "final_gate_status"
        ),
        "source_pre_application_readiness_status": final_gate.get(
            "readiness_status"
        ),
        "source_pre_application_runtime_application_status": final_gate.get(
            "runtime_application_status"
        ),
        "source_runtime_application_staging_id": staging.get("staging_id"),
        "source_application_plan_id": source_payloads["application_plan"].get(
            "application_plan_id"
        ),
        "source_human_approval_gate_id": source_payloads["human_approval_gate"].get(
            "approval_gate_id"
        ),
        "source_dry_run_review_packet_id": source_payloads[
            "dry_run_review_packet"
        ].get("review_packet_id"),
        "source_dry_run_execution_report_id": source_payloads[
            "dry_run_execution_report"
        ].get("dry_run_id"),
        "source_change_request_id": source_payloads["change_request"].get(
            "change_request_id"
        ),
        "selected_candidate_config_ref": _dict(
            final_gate.get("selected_candidate_config_ref")
        )
        or _dict(staging.get("selected_candidate_config_ref")),
        "model_asset_ref": str(Path(model_asset_path)),
        "model_asset_sha256": _sha256_path(model_asset_path)
        or final_gate.get("model_asset_sha256")
        or staging.get("model_asset_sha256"),
        "runtime_config_target_ref": _runtime_config_target_ref(
            target_path,
            target_payload,
        ),
        "runtime_config_target_sha256_before": _sha256_path(target_path),
        "current_runtime_settings": current_settings,
        "staged_candidate_settings": staged_candidate_settings,
        "staged_config_delta_ref": _staged_config_delta_ref(staged_config_delta_ref),
        "operator_signoff_ref": _dict(final_gate.get("operator_signoff_ref")),
        "pre_apply_manifest_ref": _dict(final_gate.get("pre_apply_manifest_ref")),
        "rollback_staging_ref": _dict(final_gate.get("rollback_staging_ref")),
        "post_application_verification_staging_ref": _dict(
            final_gate.get("post_application_verification_staging_ref")
        ),
        "future_baseline_policy_ref": _dict(
            final_gate.get("future_baseline_policy_ref")
        ),
        "source_artifact_presence": source_presence,
        "required_regression_gates": _required_regression_gates(final_gate, staging),
        "required_operator_artifacts": _list(
            final_gate.get("required_operator_artifacts")
        ),
        "blockers": _collect_input_blockers(final_gate, source_payloads),
        "source_warning_categories": _source_warning_categories(source_payloads),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_application_execution_inputs",
        "application_execution_input_id": inputs["application_execution_input_id"],
        "application_execution_input_type": inputs["application_execution_input_type"],
        "application_execution_input_version": inputs[
            "application_execution_input_version"
        ],
        "runtime_config_target_path": str(target_path),
        "runtime_config_target_sha256_before": inputs[
            "runtime_config_target_sha256_before"
        ],
        "model_asset_sha256": inputs["model_asset_sha256"],
        "blocker_count": len(inputs["blockers"]),
        "application_execution_inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": inputs["warnings"],
    }


def validate_controlled_runtime_calibration_application_execution_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(application_execution_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    result = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": (
            "controlled_runtime_calibration_application_execution_inputs_validation"
        ),
        "validation_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(application_execution_inputs_path)),
        "payload_type": inputs.get("application_execution_input_type"),
        "payload_version": inputs.get("application_execution_input_version"),
        "runtime_config_target_ref": inputs.get("runtime_config_target_ref"),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, result)
    return result


def execute_controlled_runtime_calibration_application(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    rollback_package_output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_ROLLBACK_PACKAGE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(application_execution_inputs_path)
    target_path = Path(_dict(inputs.get("runtime_config_target_ref")).get("path") or "")
    target_before = _load_runtime_config_target(
        target_path,
        _settings_from_source(inputs.get("current_runtime_settings")),
    )
    settings_before = _settings_from_runtime_config(target_before)
    sha_before = _sha256_path(target_path) or _canonical_sha256(target_before)
    application_execution_status = _application_execution_status(inputs, target_path)
    blockers = _application_blockers(application_execution_status, inputs, target_path)
    settings_after = settings_before
    atomic_write_status = "atomic_write_blocked"
    runtime_readback_status = "readback_blocked"
    runtime_config_status = "unchanged_due_to_blocker"
    mutation_status = "no_runtime_mutation_due_to_blocker"
    runtime_application_status = "blocked_from_runtime_application"
    post_apply_verification_status = "post_apply_verification_blocked"
    restored_after_failed_verification = False
    if application_execution_status.startswith("application_executed"):
        settings_after = _apply_staged_delta(
            settings_before,
            _dict(inputs.get("staged_candidate_settings")),
            _dict(inputs.get("staged_config_delta_ref")),
        )
        target_after = _runtime_config_payload(
            settings=settings_after,
            generated_at=generated_at,
            source_inputs=inputs,
            status="updated_by_controlled_application",
        )
        _write_json_atomic(target_path, target_after)
        atomic_write_status = "atomic_write_completed"
        readback = _verify_runtime_config_readback_payload(
            runtime_config_target_path=target_path,
            expected_settings=settings_after,
        )
        runtime_readback_status = readback["runtime_readback_status"]
        if runtime_readback_status == "readback_verified":
            runtime_config_status = "updated_by_controlled_application"
            mutation_status = "controlled_runtime_config_mutation_performed"
            runtime_application_status = "applied_by_controlled_blueprint"
            post_apply_verification_status = "post_apply_verification_passed"
        else:
            _write_json_atomic(target_path, target_before)
            restored_after_failed_verification = True
            atomic_write_status = "atomic_write_restored_previous_config"
            runtime_config_status = "restored_after_failed_verification"
            mutation_status = "controlled_runtime_config_restored_after_failed_verification"
            runtime_application_status = "blocked_from_runtime_application"
            post_apply_verification_status = "post_apply_verification_failed"
            application_execution_status = "application_blocked_runtime_readback_failed"
            settings_after = settings_before
            blockers.append("runtime_readback_failed")
    sha_after = _sha256_path(target_path) or sha_before
    rollback_package = _rollback_package(
        inputs=inputs,
        generated_at=generated_at,
        source_application_execution_id_seed=application_execution_status,
        runtime_config_target_path=target_path,
        settings_before=settings_before,
        sha_before=sha_before,
        status="rollback_package_created",
    )
    update_record = _runtime_config_update_record(
        inputs=inputs,
        generated_at=generated_at,
        runtime_config_target_path=target_path,
        sha_before=sha_before,
        sha_after=sha_after,
        settings_before=settings_before,
        settings_after=settings_after,
        atomic_write_status=atomic_write_status,
        runtime_readback_status=runtime_readback_status,
    )
    post_apply = _post_apply_verification_report(
        inputs=inputs,
        generated_at=generated_at,
        source_application_execution_id_seed=application_execution_status,
        runtime_readback_status=runtime_readback_status,
        post_apply_verification_status=post_apply_verification_status,
        blockers=blockers,
    )
    execution_id = _stable_id(
        "controlled_runtime_calibration_application_execution_v1",
        inputs.get("application_execution_input_id"),
        application_execution_status,
        sha_before,
        sha_after,
    )
    rollback_package["source_application_execution_id"] = execution_id
    post_apply["source_application_execution_id"] = execution_id
    audit_record = _audit_record(
        execution_id=execution_id,
        inputs=inputs,
        generated_at=generated_at,
        sha_before=sha_before,
        sha_after=sha_after,
        application_execution_status=application_execution_status,
        atomic_write_status=atomic_write_status,
        runtime_readback_status=runtime_readback_status,
    )
    execution = {
        "application_execution_id": execution_id,
        "application_execution_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_TYPE,
        "application_execution_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_input_path": str(
            Path(application_execution_inputs_path)
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
        "runtime_config_target_ref": _runtime_config_target_ref(
            target_path,
            _load_json_if_exists(target_path),
        ),
        "runtime_config_target_sha256_before": sha_before,
        "runtime_config_target_sha256_after": sha_after,
        "current_settings_before": settings_before,
        "applied_settings_after": settings_after,
        "applied_config_delta": update_record,
        "application_execution_status": application_execution_status,
        "runtime_application_status": runtime_application_status,
        "runtime_config_status": runtime_config_status,
        "mutation_status": mutation_status,
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "atomic_write_status": atomic_write_status,
        "runtime_readback_status": runtime_readback_status,
        "rollback_package_status": rollback_package["rollback_status"],
        "post_apply_verification_status": post_apply_verification_status,
        "restored_after_failed_verification": restored_after_failed_verification,
        "required_regression_gates": _list(inputs.get("required_regression_gates")),
        "post_apply_regression_results": post_apply["required_regression_gates"],
        "post_apply_verification_report": post_apply,
        "audit_record": audit_record,
        "rollback_package_ref": {
            "rollback_package_id": rollback_package["rollback_package_id"],
            "rollback_package_path": _path_string(rollback_package_output_path),
            "rollback_status": rollback_package["rollback_status"],
        },
        "rollback_package": rollback_package,
        "blockers": _unique_strings(blockers),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {**_dict(inputs.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    errors.extend(_validate_execution_shape(execution))
    _write_json_if_requested(output_path, execution)
    if rollback_package_output_path is not None:
        _write_json_if_requested(rollback_package_output_path, rollback_package)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_application_execution",
        "application_execution_id": execution["application_execution_id"],
        "application_execution_status": application_execution_status,
        "runtime_application_status": runtime_application_status,
        "runtime_config_status": runtime_config_status,
        "mutation_status": mutation_status,
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "atomic_write_status": atomic_write_status,
        "runtime_readback_status": runtime_readback_status,
        "rollback_package_status": rollback_package["rollback_status"],
        "post_apply_verification_status": post_apply_verification_status,
        "runtime_config_target_path": str(target_path),
        "runtime_config_target_sha256_before": sha_before,
        "runtime_config_target_sha256_after": sha_after,
        "application_execution_output": _path_string(output_path),
        "rollback_package_output": _path_string(rollback_package_output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": execution["warnings"],
    }


def validate_controlled_runtime_calibration_application_execution(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    execution = _load_json(application_execution_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_execution_shape(execution))
    result = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": (
            "controlled_runtime_calibration_application_execution_validation"
        ),
        "validation_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(application_execution_path)),
        "payload_type": execution.get("application_execution_type"),
        "payload_version": execution.get("application_execution_version"),
        "application_execution_status": execution.get("application_execution_status"),
        "runtime_application_status": execution.get("runtime_application_status"),
        "runtime_config_status": execution.get("runtime_config_status"),
        "mutation_status": execution.get("mutation_status"),
        "production_config_status": execution.get("production_config_status"),
        "baseline_update_status": execution.get("baseline_update_status"),
        "model_update_status": execution.get("model_update_status"),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, result)
    return result


def verify_controlled_runtime_calibration_runtime_readback(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    runtime_config_target_path: str | Path | None = None,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_READBACK_OUTPUT
    ),
    verified_at: datetime | None = None,
) -> dict[str, Any]:
    verified_at = verified_at or _now_utc()
    contract = _load_json(contract_path)
    execution = _load_json(application_execution_path)
    target_path = Path(
        runtime_config_target_path
        or _dict(execution.get("runtime_config_target_ref")).get("path")
        or ""
    )
    expected_settings = _dict(execution.get("applied_settings_after"))
    readback = _verify_runtime_config_readback_payload(
        runtime_config_target_path=target_path,
        expected_settings=expected_settings,
    )
    if execution.get("runtime_application_status") != "applied_by_controlled_blueprint":
        readback["runtime_readback_status"] = "readback_not_applicable"
        readback["ok"] = True
    readback.update(
        {
            "readback_type": CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_READBACK_TYPE,
            "readback_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
            "verified_at": verified_at.isoformat(),
            "source_application_execution_id": execution.get(
                "application_execution_id"
            ),
            "source_application_execution_path": str(Path(application_execution_path)),
            "warnings": dict(WARNINGS),
            "non_claims": dict(NON_CLAIMS),
        }
    )
    errors = _validate_contract_shape(contract)
    if readback["runtime_readback_status"] not in ALLOWED_RUNTIME_READBACK_STATUSES:
        errors.append(
            _error(
                "invalid_runtime_readback_status",
                "runtime_readback_status",
                readback["runtime_readback_status"],
            )
        )
    readback["error_count"] = len(errors)
    readback["errors"] = errors
    readback["ok"] = readback["ok"] and not errors
    readback["status"] = "completed" if readback["ok"] else "invalid_readback"
    _write_json_if_requested(output_path, readback)
    return readback


def build_controlled_runtime_calibration_application_audit_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_AUDIT_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    execution = _load_json(application_execution_path)
    report = {
        "audit_report_id": _stable_id(
            "controlled_runtime_calibration_application_audit_report_v1",
            execution.get("application_execution_id"),
            execution.get("runtime_config_target_sha256_before"),
            execution.get("runtime_config_target_sha256_after"),
        ),
        "audit_report_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_AUDIT_REPORT_TYPE,
        "audit_report_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": execution.get("application_execution_id"),
        "source_application_execution_path": str(Path(application_execution_path)),
        "application_execution_status": execution.get("application_execution_status"),
        "runtime_application_status": execution.get("runtime_application_status"),
        "runtime_config_status": execution.get("runtime_config_status"),
        "mutation_status": execution.get("mutation_status"),
        "atomic_write_status": execution.get("atomic_write_status"),
        "runtime_readback_status": execution.get("runtime_readback_status"),
        "runtime_config_target_ref": execution.get("runtime_config_target_ref"),
        "runtime_config_target_sha256_before": execution.get(
            "runtime_config_target_sha256_before"
        ),
        "runtime_config_target_sha256_after": execution.get(
            "runtime_config_target_sha256_after"
        ),
        "applied_config_delta": execution.get("applied_config_delta"),
        "audit_record": execution.get("audit_record"),
        "warnings": {**_dict(execution.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_audit_report",
        "audit_report_id": report["audit_report_id"],
        "application_execution_status": report["application_execution_status"],
        "runtime_config_status": report["runtime_config_status"],
        "audit_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": report["warnings"],
    }


def build_controlled_runtime_calibration_rollback_package(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_ROLLBACK_PACKAGE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    execution = _load_json(application_execution_path)
    rollback = _dict(execution.get("rollback_package")) or _rollback_package(
        inputs={},
        generated_at=generated_at,
        source_application_execution_id_seed=execution.get("application_execution_id"),
        runtime_config_target_path=Path(
            _dict(execution.get("runtime_config_target_ref")).get("path") or ""
        ),
        settings_before=_dict(execution.get("current_settings_before")),
        sha_before=execution.get("runtime_config_target_sha256_before"),
        status="rollback_package_created",
    )
    rollback["source_application_execution_id"] = execution.get("application_execution_id")
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_rollback_package_shape(rollback))
    _write_json_if_requested(output_path, rollback)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_rollback_package",
        "rollback_package_id": rollback["rollback_package_id"],
        "rollback_package_status": rollback["rollback_status"],
        "rollback_target_sha256": rollback["rollback_target_sha256"],
        "rollback_package_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }


def build_controlled_runtime_calibration_post_apply_verification_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_OUTPUT
    ),
    application_execution_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_APPLY_VERIFICATION_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    execution = _load_json(application_execution_path)
    report = _dict(execution.get("post_apply_verification_report")) or (
        _post_apply_verification_report(
            inputs={},
            generated_at=generated_at,
            source_application_execution_id_seed=execution.get(
                "application_execution_id"
            ),
            runtime_readback_status=str(execution.get("runtime_readback_status")),
            post_apply_verification_status=str(
                execution.get("post_apply_verification_status")
            ),
            blockers=_list(execution.get("blockers")),
        )
    )
    report["source_application_execution_id"] = execution.get("application_execution_id")
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_post_apply_verification_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_post_apply_verification",
        "post_apply_verification_id": report["post_apply_verification_id"],
        "post_apply_verification_status": report["verification_status"],
        "runtime_readback_status": _dict(report.get("runtime_readback_result")).get(
            "runtime_readback_status"
        ),
        "post_apply_verification_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": report["warnings"],
    }


def build_controlled_runtime_calibration_applied_runtime_config(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_EXPORTED_AT
    settings = _default_runtime_settings()
    payload = _runtime_config_payload(
        settings=settings,
        generated_at=generated_at,
        source_inputs={},
        status="controlled_runtime_config_target_initialized",
    )
    _write_json_if_requested(output_path, payload)
    return {
        "ok": True,
        "status": "completed",
        "runtime_config_type": payload["runtime_config_type"],
        "runtime_config_version": payload["runtime_config_version"],
        "runtime_config_target_path": _path_string(output_path),
        "runtime_config_sha256": _sha256_path(output_path),
        "warnings": dict(WARNINGS),
    }


def _application_execution_status(inputs: dict[str, Any], target_path: Path) -> str:
    final_gate_status = inputs.get("source_pre_application_final_gate_status")
    if not inputs.get("source_pre_application_final_gate_id"):
        return "application_blocked_missing_final_gate"
    if final_gate_status != "final_gate_passed_not_applied":
        return "application_blocked_final_gate_not_passed"
    source_presence = _dict(inputs.get("source_artifact_presence"))
    if not _source_present(source_presence, "runtime_application_staging"):
        return "application_blocked_missing_staging_artifact"
    if not _source_present(source_presence, "application_plan"):
        return "application_blocked_missing_application_plan"
    if not _source_present(source_presence, "human_approval_gate"):
        return "application_blocked_missing_human_approval_gate"
    if not _source_present(source_presence, "change_request"):
        return "application_blocked_missing_change_request"
    if _dict(inputs.get("operator_signoff_ref")).get(
        "operator_signoff_artifact_present"
    ) is not True:
        return "application_blocked_missing_operator_signoff"
    if not _has_selected_candidate_ref(_dict(inputs.get("selected_candidate_config_ref"))):
        return "application_blocked_missing_candidate_config"
    if not _source_present(source_presence, "candidate_config_freeze"):
        return "application_blocked_missing_candidate_config"
    if not _dict(inputs.get("pre_apply_manifest_ref")).get("pre_apply_manifest_id"):
        return "application_blocked_missing_pre_apply_manifest"
    if not _dict(inputs.get("rollback_staging_ref")).get("rollback_staging_id"):
        return "application_blocked_missing_rollback_package"
    if not _dict(inputs.get("post_application_verification_staging_ref")).get(
        "post_application_verification_staging_id"
    ):
        return "application_blocked_missing_post_application_verification_plan"
    if not _safe_runtime_config_target_path(target_path):
        return "application_blocked_unsafe_config_target"
    if _has_unresolved_blockers(inputs):
        return "application_blocked_unresolved_blockers"
    if not _required_regression_gate_refs_present(inputs):
        return "application_blocked_missing_regression_gate"
    if not _model_asset_hash_matches(inputs):
        return "application_blocked_model_asset_hash_mismatch"
    if _staged_delta_invalid(inputs):
        return "application_blocked_delta_mismatch"
    return "application_executed_controlled_runtime_config_write"


def _application_blockers(
    status: str,
    inputs: dict[str, Any],
    target_path: Path,
) -> list[str]:
    blockers = _list(inputs.get("blockers"))
    if status.startswith("application_executed"):
        return []
    blockers.append(status)
    if not _safe_runtime_config_target_path(target_path):
        blockers.append("unsafe_runtime_config_target")
    return _unique_strings(blockers)


def _runtime_config_update_record(
    *,
    inputs: dict[str, Any],
    generated_at: datetime,
    runtime_config_target_path: Path,
    sha_before: str | None,
    sha_after: str | None,
    settings_before: dict[str, Any],
    settings_after: dict[str, Any],
    atomic_write_status: str,
    runtime_readback_status: str,
) -> dict[str, Any]:
    return {
        "update_record_id": _stable_id(
            "controlled_runtime_calibration_runtime_config_update_record_v1",
            inputs.get("application_execution_input_id"),
            sha_before,
            sha_after,
            settings_after,
        ),
        "update_record_type": CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_CONFIG_UPDATE_RECORD_TYPE,
        "update_record_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "runtime_config_target_ref": {
            "path": str(runtime_config_target_path),
            "runtime_config_type": CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_TYPE,
            "not_production_config": True,
            "not_model_weights": True,
            "not_baseline": True,
        },
        "sha256_before": sha_before,
        "sha256_after": sha_after,
        "settings_before": settings_before,
        "settings_after": settings_after,
        "delta_applied": _delta_applied(settings_before, settings_after),
        "atomic_write_status": atomic_write_status,
        "readback_status": runtime_readback_status,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _rollback_package(
    *,
    inputs: dict[str, Any],
    generated_at: datetime,
    source_application_execution_id_seed: Any,
    runtime_config_target_path: Path,
    settings_before: dict[str, Any],
    sha_before: str | None,
    status: str,
) -> dict[str, Any]:
    return {
        "rollback_package_id": _stable_id(
            "controlled_runtime_calibration_application_rollback_package_v1",
            inputs.get("application_execution_input_id"),
            source_application_execution_id_seed,
            sha_before,
            settings_before,
        ),
        "rollback_package_type": CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PACKAGE_TYPE,
        "rollback_package_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": source_application_execution_id_seed,
        "runtime_config_target_ref": {
            "path": str(runtime_config_target_path),
            "runtime_config_type": CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_TYPE,
        },
        "rollback_target_sha256": sha_before,
        "rollback_target_settings": settings_before,
        "rollback_trigger_conditions": [
            "runtime readback mismatch",
            "post-apply verification blocks",
            "operator requests rollback review",
        ],
        "rollback_execution_steps": [
            "write rollback_target_settings to runtime_config_target_ref using atomic rename",
            "read back runtime config target",
            "run required regression gates",
            "record operator review state after rollback",
        ],
        "rollback_verification_gates": _required_regression_gates_from_inputs(inputs),
        "rollback_status": status,
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _post_apply_verification_report(
    *,
    inputs: dict[str, Any],
    generated_at: datetime,
    source_application_execution_id_seed: Any,
    runtime_readback_status: str,
    post_apply_verification_status: str,
    blockers: list[str],
) -> dict[str, Any]:
    required_gates = _required_regression_gates_from_inputs(inputs)
    gate_result = {
        "status": (
            "passed_by_required_external_gate"
            if post_apply_verification_status == "post_apply_verification_passed"
            else "blocked_until_required_external_gate_passes"
        ),
        "drift_detected": False,
        "breaking_drift_detected": False,
        "baseline_is_not_truth": True,
    }
    return {
        "post_apply_verification_id": _stable_id(
            "controlled_runtime_calibration_post_apply_verification_v1",
            inputs.get("application_execution_input_id"),
            post_apply_verification_status,
            runtime_readback_status,
            blockers,
        ),
        "post_apply_verification_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_APPLY_VERIFICATION_TYPE
        ),
        "post_apply_verification_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": source_application_execution_id_seed,
        "required_regression_gates": required_gates,
        "multi_point_regression_gate_result": {
            **gate_result,
            "gate": "multi_point_regression_matrix",
            "matrix_is_not_truth": True,
        },
        "protected_sample_point_gate_result": {
            **gate_result,
            "gate": "protected_sample_point_reviewed_3d_debug",
        },
        "gameplay_gate_regression_baseline_result": {
            **gate_result,
            "gate": "gameplay_gate_regression_baseline",
            "gameplay_gate_is_not_truth": True,
            "classifier_correctness_not_assessed": True,
            "generalization_not_claimed": True,
        },
        "calibration_sandbox_regression_baseline_result": {
            **gate_result,
            "gate": "review_guided_gameplay_calibration_sandbox_regression",
            "sandbox_is_not_truth": True,
            "sandbox_is_not_accuracy_scoring": True,
            "model_weights_not_modified": True,
            "baseline_not_replaced": True,
            "classifier_correctness_not_assessed": True,
            "generalization_not_claimed": True,
        },
        "runtime_readback_result": {
            "runtime_readback_status": runtime_readback_status,
            "readback_verified": runtime_readback_status == "readback_verified",
        },
        "model_asset_hash_check": {
            "status": "present",
            "model_weights_not_modified": True,
        },
        "baseline_replacement_check": {
            "status": "not_replaced",
            "baseline_not_replaced": True,
        },
        "production_config_check": {
            "status": "not_created",
            "production_config_not_created": True,
        },
        "verification_status": post_apply_verification_status,
        "blockers": _unique_strings(blockers),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _audit_record(
    *,
    execution_id: str,
    inputs: dict[str, Any],
    generated_at: datetime,
    sha_before: str | None,
    sha_after: str | None,
    application_execution_status: str,
    atomic_write_status: str,
    runtime_readback_status: str,
) -> dict[str, Any]:
    return {
        "audit_record_id": _stable_id(
            "controlled_runtime_calibration_application_audit_record_v1",
            execution_id,
            sha_before,
            sha_after,
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_execution_id": execution_id,
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
        "source_change_request_path": inputs.get("source_change_request_path"),
        "application_execution_status": application_execution_status,
        "atomic_write_status": atomic_write_status,
        "runtime_readback_status": runtime_readback_status,
        "runtime_config_target_sha256_before": sha_before,
        "runtime_config_target_sha256_after": sha_after,
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
    }


def _runtime_config_payload(
    *,
    settings: dict[str, Any],
    generated_at: datetime,
    source_inputs: dict[str, Any],
    status: str,
) -> dict[str, Any]:
    return {
        "runtime_config_id": _stable_id(
            "controlled_runtime_calibration_applied_runtime_config_v1",
            settings,
            source_inputs.get("application_execution_input_id"),
            status,
        ),
        "runtime_config_type": CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_TYPE,
        "runtime_config_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "runtime_config_status": status,
        "config_scope": {
            "controlled_runtime_calibration_config": True,
            "not_production_config": True,
            "not_model_weights": True,
            "not_baseline": True,
            "not_truth": True,
            "applied_only_through_bp62_controlled_execution": True,
        },
        "settings": settings,
        "source_application_execution_input_id": source_inputs.get(
            "application_execution_input_id"
        ),
        "source_pre_application_final_gate_path": source_inputs.get(
            "source_pre_application_final_gate_path"
        ),
        "source_runtime_application_staging_path": source_inputs.get(
            "source_runtime_application_staging_path"
        ),
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }


def _load_runtime_config_target(
    target_path: Path,
    default_settings: dict[str, Any],
) -> dict[str, Any]:
    payload = _load_json_if_exists(target_path)
    if payload:
        return payload
    return _runtime_config_payload(
        settings=default_settings,
        generated_at=CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_EXPORTED_AT,
        source_inputs={},
        status="controlled_runtime_config_target_initialized",
    )


def _verify_runtime_config_readback_payload(
    *,
    runtime_config_target_path: Path,
    expected_settings: dict[str, Any],
) -> dict[str, Any]:
    payload = _load_json_if_exists(runtime_config_target_path)
    actual_settings = _settings_from_runtime_config(payload)
    verified = bool(payload) and actual_settings == expected_settings
    return {
        "ok": verified,
        "status": "completed" if verified else "readback_mismatch",
        "runtime_config_target_path": str(runtime_config_target_path),
        "runtime_config_target_sha256": _sha256_path(runtime_config_target_path),
        "runtime_readback_status": (
            "readback_verified" if verified else "readback_mismatch"
        ),
        "expected_settings": expected_settings,
        "actual_settings": actual_settings,
    }


def _apply_staged_delta(
    settings_before: dict[str, Any],
    staged_candidate_settings: dict[str, Any],
    staged_config_delta_ref: dict[str, Any],
) -> dict[str, Any]:
    settings = dict(settings_before)
    threshold = staged_candidate_settings.get("staged_candidate_threshold")
    smoothing_window = staged_candidate_settings.get("staged_candidate_smoothing_window")
    hysteresis_settings = staged_candidate_settings.get(
        "staged_candidate_hysteresis_settings"
    )
    for field in _list(staged_config_delta_ref.get("delta_fields")):
        field_name = _dict(field).get("field")
        if _dict(field).get("change_present") is not True:
            continue
        if field_name == "threshold":
            threshold = _dict(field).get("staged_value")
        if field_name == "smoothing_window":
            smoothing_window = _dict(field).get("staged_value")
        if field_name == "hysteresis_settings":
            hysteresis_settings = _dict(field).get("staged_value")
    if threshold is not None:
        settings["threshold"] = threshold
    if smoothing_window is not None:
        settings["smoothing_window"] = smoothing_window
    if hysteresis_settings:
        settings["hysteresis_settings"] = _dict(hysteresis_settings)
    settings["runtime_config_status"] = "updated_by_controlled_application"
    return settings


def _delta_applied(
    settings_before: dict[str, Any],
    settings_after: dict[str, Any],
) -> list[dict[str, Any]]:
    fields = ["threshold", "smoothing_window", "hysteresis_settings"]
    return [
        {
            "field": field,
            "before": settings_before.get(field),
            "after": settings_after.get(field),
            "change_applied": settings_before.get(field) != settings_after.get(field),
            "runtime_config_status": "updated_by_controlled_application"
            if settings_before.get(field) != settings_after.get(field)
            else "unchanged_due_to_blocker",
        }
        for field in fields
    ]


def _settings_from_source(*values: Any) -> dict[str, Any]:
    for value in values:
        candidate = _dict(value)
        if candidate:
            return {
                "threshold": candidate.get(
                    "threshold",
                    candidate.get("current_threshold", DEFAULT_THRESHOLD),
                ),
                "smoothing_window": candidate.get(
                    "smoothing_window",
                    candidate.get("current_smoothing_window", DEFAULT_SMOOTHING_WINDOW),
                ),
                "hysteresis_settings": _dict(
                    candidate.get(
                        "hysteresis_settings",
                        candidate.get("current_hysteresis_settings"),
                    )
                )
                or {
                    "enter_gameplay_probability": DEFAULT_HYSTERESIS_ENTER,
                    "exit_gameplay_probability": DEFAULT_HYSTERESIS_EXIT,
                },
                "runtime_config_status": candidate.get(
                    "runtime_config_status",
                    "not_updated",
                ),
            }
    return _default_runtime_settings()


def _settings_from_runtime_config(payload: dict[str, Any]) -> dict[str, Any]:
    return _settings_from_source(_dict(payload.get("settings")))


def _default_runtime_settings() -> dict[str, Any]:
    return {
        "threshold": DEFAULT_THRESHOLD,
        "smoothing_window": DEFAULT_SMOOTHING_WINDOW,
        "hysteresis_settings": {
            "enter_gameplay_probability": DEFAULT_HYSTERESIS_ENTER,
            "exit_gameplay_probability": DEFAULT_HYSTERESIS_EXIT,
        },
        "runtime_config_status": "controlled_runtime_config_target_initialized",
    }


def _staged_config_delta_ref(staged_config_delta: dict[str, Any]) -> dict[str, Any]:
    return {
        "staged_config_delta_id": staged_config_delta.get("staged_config_delta_id"),
        "staged_config_delta_type": staged_config_delta.get("staged_config_delta_type"),
        "staged_config_delta_version": staged_config_delta.get(
            "staged_config_delta_version"
        ),
        "delta_status": staged_config_delta.get("delta_status"),
        "delta_fields": _list(staged_config_delta.get("delta_fields")),
        "runtime_application_status": staged_config_delta.get(
            "runtime_application_status",
            "staged_not_applied",
        ),
        "runtime_config_status": staged_config_delta.get(
            "runtime_config_status",
            "staged_delta_only",
        ),
        "mutation_status": staged_config_delta.get(
            "mutation_status",
            "no_runtime_mutation",
        ),
    }


def _runtime_config_target_ref(
    target_path: Path,
    target_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "path": str(target_path),
        "exists": bool(target_payload),
        "runtime_config_type": target_payload.get(
            "runtime_config_type",
            CONTROLLED_RUNTIME_CALIBRATION_APPLIED_RUNTIME_CONFIG_TYPE,
        ),
        "runtime_config_version": target_payload.get(
            "runtime_config_version",
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_VERSION,
        ),
        "runtime_config_status": target_payload.get("runtime_config_status"),
        "not_production_config": True,
        "not_model_weights": True,
        "not_baseline": True,
        "not_truth": True,
    }


def _source_artifact_presence(
    source_payloads: dict[str, dict[str, Any]],
    source_paths: dict[str, str | Path | None],
) -> dict[str, dict[str, Any]]:
    return {
        key: {
            "present": bool(payload),
            "path": _path_string(source_paths.get(key)),
            "artifact_type": _artifact_type(payload),
        }
        for key, payload in source_payloads.items()
    }


def _artifact_type(payload: dict[str, Any]) -> str | None:
    for key in (
        "final_gate_type",
        "staging_type",
        "application_plan_type",
        "approval_gate_type",
        "review_packet_type",
        "dry_run_type",
        "change_request_type",
        "candidate_config_freeze_type",
        "manual_approval_packet_type",
        "decision_packet_type",
        "baseline_type",
        "contract_type",
        "freeze_type",
    ):
        if payload.get(key):
            return str(payload[key])
    return None


def _source_present(source_presence: dict[str, Any], key: str) -> bool:
    return _dict(source_presence.get(key)).get("present") is True


def _source_warning_categories(source_payloads: dict[str, dict[str, Any]]) -> list[str]:
    categories: set[str] = set()
    for payload in source_payloads.values():
        categories.update(str(key) for key in _dict(payload.get("warnings")).keys())
    return sorted(categories)


def _merged_warnings(source_payloads: dict[str, dict[str, Any]]) -> dict[str, bool]:
    merged = dict(WARNINGS)
    for category in _source_warning_categories(source_payloads):
        merged[category] = True
    return merged


def _collect_input_blockers(
    final_gate: dict[str, Any],
    source_payloads: dict[str, dict[str, Any]],
) -> list[str]:
    blockers = [str(item) for item in _list(final_gate.get("blockers"))]
    for payload in source_payloads.values():
        blockers.extend(str(item) for item in _list(payload.get("blockers")))
    return _unique_strings(blockers)


def _required_regression_gates(
    final_gate: dict[str, Any],
    staging: dict[str, Any],
) -> list[dict[str, Any]]:
    gates = _list(final_gate.get("required_regression_gates")) or _list(
        staging.get("required_regression_gates")
    )
    if not gates:
        gates = [
            {"gate": gate, "required": True}
            for gate in _default_required_regression_gate_names()
        ]
    return [
        {
            "gate": _dict(gate).get("gate"),
            "required": _dict(gate).get("required", True) is True,
            "post_apply_verification_required": True,
        }
        for gate in gates
    ]


def _required_regression_gates_from_inputs(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    gates = _list(inputs.get("required_regression_gates"))
    if not gates:
        gates = [
            {"gate": gate, "required": True}
            for gate in _default_required_regression_gate_names()
        ]
    return [
        {
            **_dict(gate),
            "required": _dict(gate).get("required", True) is True,
        }
        for gate in gates
    ]


def _default_required_regression_gate_names() -> list[str]:
    return [
        "multi_point_regression_matrix",
        "protected_sample_point_reviewed_3d_debug",
        "gameplay_gate_regression_baseline",
        "review_guided_gameplay_calibration_sandbox_regression",
    ]


def _has_selected_candidate_ref(selected_candidate_ref: dict[str, Any]) -> bool:
    return any(value is not None for value in selected_candidate_ref.values())


def _required_regression_gate_refs_present(inputs: dict[str, Any]) -> bool:
    names = {
        str(_dict(gate).get("gate"))
        for gate in _list(inputs.get("required_regression_gates"))
        if _dict(gate).get("required", True) is True
    }
    return all(gate in names for gate in _default_required_regression_gate_names())


def _has_unresolved_blockers(inputs: dict[str, Any]) -> bool:
    benign = {
        "no_unresolved_blockers",
        "not_applicable",
    }
    return any(str(blocker) not in benign for blocker in _list(inputs.get("blockers")))


def _model_asset_hash_matches(inputs: dict[str, Any]) -> bool:
    model_asset_ref = inputs.get("model_asset_ref")
    expected = inputs.get("model_asset_sha256")
    actual = _sha256_path(model_asset_ref)
    return not actual or actual == expected


def _staged_delta_invalid(inputs: dict[str, Any]) -> bool:
    delta = _dict(inputs.get("staged_config_delta_ref"))
    if delta.get("delta_status") in {
        "staged_blocked_invalid_scope",
        "staged_blocked_missing_candidate_settings",
        "config_delta_blocked_invalid_scope",
        "config_delta_blocked_missing_candidate_settings",
    }:
        return True
    return not any(
        _dict(field).get("change_present") is True
        for field in _list(delta.get("delta_fields"))
    )


def _safe_runtime_config_target_path(path: Path) -> bool:
    path_str = str(path)
    if not path_str.endswith(".json"):
        return False
    if "model_assets" in path.parts or ".data/baselines" in path_str:
        return False
    if ".data/exports" in path_str:
        return False
    return "controlled_runtime_calibration" in path.name


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    for section in (
        "contract_type",
        "contract_version",
        "exported_at",
        "application_execution_scope",
        "source_contract_refs",
        "application_execution_input_schema",
        "application_execution_schema",
        "runtime_config_update_schema",
        "runtime_readback_schema",
        "rollback_package_schema",
        "post_apply_verification_schema",
        "audit_record_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if contract.get("contract_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_TYPE
    ):
        errors.append(
            _error(
                "invalid_contract_type",
                "contract_type",
                contract.get("contract_type"),
            )
        )
    if contract.get("contract_version") != (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    _validate_non_claims(contract, errors, path="contract.non_claims")
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "application_execution_inputs")
    _require_fields(
        inputs,
        APPLICATION_EXECUTION_INPUT_REQUIRED_FIELDS,
        "application_execution_inputs",
        errors,
    )
    if inputs.get("application_execution_input_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_input_type",
                "application_execution_input_type",
                inputs.get("application_execution_input_type"),
            )
        )
    if inputs.get("application_execution_input_version") != (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_input_version",
                "application_execution_input_version",
                inputs.get("application_execution_input_version"),
            )
        )
    if inputs.get("model_asset_sha256") in (None, ""):
        errors.append(
            _error(
                "missing_model_asset_sha256",
                "model_asset_sha256",
                inputs.get("model_asset_sha256"),
            )
        )
    target_ref = _dict(inputs.get("runtime_config_target_ref"))
    if not _safe_runtime_config_target_path(Path(str(target_ref.get("path", "")))):
        errors.append(
            _error(
                "unsafe_runtime_config_target",
                "runtime_config_target_ref.path",
                target_ref.get("path"),
            )
        )
    _validate_non_claims(inputs, errors, path="application_execution_inputs.non_claims")
    return errors


def _validate_execution_shape(execution: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(execution, "application_execution")
    _require_fields(
        execution,
        APPLICATION_EXECUTION_REQUIRED_FIELDS,
        "application_execution",
        errors,
    )
    _validate_status(
        execution.get("application_execution_status"),
        ALLOWED_APPLICATION_EXECUTION_STATUSES,
        "application_execution.application_execution_status",
        errors,
    )
    _validate_status(
        execution.get("runtime_application_status"),
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        "application_execution.runtime_application_status",
        errors,
    )
    _validate_status(
        execution.get("runtime_config_status"),
        ALLOWED_RUNTIME_CONFIG_STATUSES,
        "application_execution.runtime_config_status",
        errors,
    )
    _validate_status(
        execution.get("mutation_status"),
        ALLOWED_MUTATION_STATUSES,
        "application_execution.mutation_status",
        errors,
    )
    _validate_status(
        execution.get("production_config_status"),
        ALLOWED_PRODUCTION_CONFIG_STATUSES,
        "application_execution.production_config_status",
        errors,
    )
    _validate_status(
        execution.get("baseline_update_status"),
        ALLOWED_BASELINE_UPDATE_STATUSES,
        "application_execution.baseline_update_status",
        errors,
    )
    _validate_status(
        execution.get("model_update_status"),
        ALLOWED_MODEL_UPDATE_STATUSES,
        "application_execution.model_update_status",
        errors,
    )
    _validate_status(
        execution.get("atomic_write_status"),
        ALLOWED_ATOMIC_WRITE_STATUSES,
        "application_execution.atomic_write_status",
        errors,
    )
    _validate_status(
        execution.get("runtime_readback_status"),
        ALLOWED_RUNTIME_READBACK_STATUSES,
        "application_execution.runtime_readback_status",
        errors,
    )
    _validate_status(
        execution.get("rollback_package_status"),
        ALLOWED_ROLLBACK_PACKAGE_STATUSES,
        "application_execution.rollback_package_status",
        errors,
    )
    _validate_status(
        execution.get("post_apply_verification_status"),
        ALLOWED_POST_APPLY_VERIFICATION_STATUSES,
        "application_execution.post_apply_verification_status",
        errors,
    )
    if execution.get("production_config_status") != "not_created":
        errors.append(
            _error(
                "production_config_status_not_allowed",
                "production_config_status",
                execution.get("production_config_status"),
            )
        )
    if execution.get("baseline_update_status") != "not_replaced":
        errors.append(
            _error(
                "baseline_update_status_not_allowed",
                "baseline_update_status",
                execution.get("baseline_update_status"),
            )
        )
    if execution.get("model_update_status") != "not_modified":
        errors.append(
            _error(
                "model_update_status_not_allowed",
                "model_update_status",
                execution.get("model_update_status"),
            )
        )
    if execution.get("runtime_config_status") == "updated_by_controlled_application":
        if execution.get("runtime_application_status") != "applied_by_controlled_blueprint":
            errors.append(
                _error(
                    "runtime_config_update_not_linked_to_controlled_application",
                    "runtime_application_status",
                    execution.get("runtime_application_status"),
                )
            )
        if execution.get("atomic_write_status") != "atomic_write_completed":
            errors.append(
                _error(
                    "runtime_config_update_missing_atomic_write",
                    "atomic_write_status",
                    execution.get("atomic_write_status"),
                )
            )
        if execution.get("runtime_readback_status") != "readback_verified":
            errors.append(
                _error(
                    "runtime_config_update_missing_readback",
                    "runtime_readback_status",
                    execution.get("runtime_readback_status"),
                )
            )
    _validate_non_claims(execution, errors, path="application_execution.non_claims")
    errors.extend(_validate_rollback_package_shape(_dict(execution.get("rollback_package"))))
    errors.extend(
        _validate_post_apply_verification_shape(
            _dict(execution.get("post_apply_verification_report"))
        )
    )
    return errors


def _validate_rollback_package_shape(rollback: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(rollback, "rollback_package")
    _require_fields(rollback, ROLLBACK_PACKAGE_REQUIRED_FIELDS, "rollback_package", errors)
    if rollback.get("rollback_status") not in ALLOWED_ROLLBACK_PACKAGE_STATUSES:
        errors.append(
            _error(
                "invalid_rollback_status",
                "rollback_status",
                rollback.get("rollback_status"),
            )
        )
    _validate_non_claims(rollback, errors, path="rollback_package.non_claims")
    return errors


def _validate_post_apply_verification_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "post_apply_verification")
    _require_fields(
        report,
        POST_APPLY_VERIFICATION_REQUIRED_FIELDS,
        "post_apply_verification",
        errors,
    )
    if report.get("verification_status") not in ALLOWED_POST_APPLY_VERIFICATION_STATUSES:
        errors.append(
            _error(
                "invalid_post_apply_verification_status",
                "verification_status",
                report.get("verification_status"),
            )
        )
    _validate_non_claims(report, errors, path="post_apply_verification.non_claims")
    return errors


def _validate_non_claims(
    payload: dict[str, Any],
    errors: list[dict[str, Any]],
    *,
    path: str,
) -> None:
    non_claims = _dict(payload.get("non_claims"))
    for key, expected in NON_CLAIMS.items():
        if non_claims.get(key) is not expected:
            errors.append(_error("missing_non_claim", f"{path}.{key}", non_claims.get(key)))


def _require_fields(
    payload: dict[str, Any],
    required_fields: list[str],
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    for field in required_fields:
        if field not in payload:
            errors.append(_error("missing_required_field", f"{path}.{field}", None))


def _validate_status(
    value: Any,
    allowed: list[str],
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    if value not in allowed:
        errors.append(_error("invalid_status", path, value))


def _forbidden_token_errors(value: Any, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_APPLICATION_EXECUTION_TOKENS:
                errors.append(_error("forbidden_key", key_path, key))
            errors.extend(_forbidden_token_errors(child, key_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_forbidden_token_errors(child, f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_APPLICATION_EXECUTION_TOKENS:
        errors.append(_error("forbidden_value", path, value))
    return errors


def _error(code: str, path: str, value: Any) -> dict[str, Any]:
    return {"code": code, "path": path, "value": value}


def _write_json_if_requested(output_path: str | Path | None, payload: dict[str, Any]) -> None:
    if output_path is None:
        return
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with tmp_path.open("r+", encoding="utf-8") as handle:
        handle.flush()
        os.fsync(handle.fileno())
    tmp_path.replace(path)
    try:
        dir_fd = os.open(path.parent, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def _load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_json_if_exists(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    candidate = Path(path)
    if not candidate.exists():
        return {}
    try:
        return _load_json(candidate)
    except json.JSONDecodeError:
        return {}


def _sha256_path(path: str | Path | None) -> str | None:
    if path is None:
        return None
    candidate = Path(path)
    if not candidate.exists() or not candidate.is_file():
        return None
    digest = hashlib.sha256()
    with candidate.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _stable_id(prefix: str, *parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str, separators=(",", ":"))
    return f"{prefix}_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:24]}"


def _path_string(path: str | Path | None) -> str | None:
    if path is None:
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        text = str(value)
        if text not in seen:
            seen.add(text)
            unique.append(text)
    return unique


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_BLUEPRINT,
        "blueprint_name": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_EXECUTION_BLUEPRINT_NAME,
    }
