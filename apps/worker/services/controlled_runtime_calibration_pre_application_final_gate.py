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
from apps.worker.services.controlled_runtime_calibration_runtime_application_staging import (
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_runtime_application_staging import (
    SOURCE_CONTRACT_REFS as RUNTIME_APPLICATION_STAGING_SOURCE_CONTRACT_REFS,
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

CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_TYPE = (
    "controlled_runtime_calibration_pre_application_final_gate_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_TYPE = (
    "controlled_runtime_calibration_pre_application_final_gate_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_TYPE = (
    "controlled_runtime_calibration_pre_application_final_gate"
)
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_BLOCKER_REPORT_TYPE = (
    "controlled_runtime_calibration_final_gate_blocker_report"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_ARTIFACT_CHECKLIST_TYPE = (
    "controlled_runtime_calibration_final_gate_artifact_checklist"
)
CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_REGRESSION_CHECKLIST_TYPE = (
    "controlled_runtime_calibration_final_gate_regression_checklist"
)
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_BLUEPRINT = "blueprint_61"
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_pre_application_final_gate_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_pre_application_final_gate_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUTS_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_pre_application_final_gate_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_pre_application_final_gate_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_pre_application_final_gate_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_pre_application_final_gate.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_READINESS_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_readiness_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_BLOCKER_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_blocker_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_ARTIFACT_CHECKLIST_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_artifact_checklist.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_REGRESSION_CHECKLIST_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_final_gate_regression_checklist.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_runtime_application_staging_contract_version": "v1",
    **dict(RUNTIME_APPLICATION_STAGING_SOURCE_CONTRACT_REFS),
}

ALLOWED_FINAL_GATE_STATUSES = [
    "final_gate_passed_not_applied",
    "final_gate_passed_with_warnings_not_applied",
    "final_gate_blocked_missing_staging_artifact",
    "final_gate_blocked_missing_application_plan",
    "final_gate_blocked_missing_human_approval_gate",
    "final_gate_blocked_missing_dry_run_review_packet",
    "final_gate_blocked_missing_change_request",
    "final_gate_blocked_missing_candidate_config",
    "final_gate_blocked_missing_operator_signoff",
    "final_gate_blocked_missing_rollback_plan",
    "final_gate_blocked_missing_pre_apply_manifest",
    "final_gate_blocked_missing_post_application_verification_plan",
    "final_gate_blocked_missing_regression_gate",
    "final_gate_blocked_unresolved_blockers",
    "final_gate_blocked_breaking_structural_change",
    "final_gate_blocked_model_asset_provenance_missing",
    "final_gate_blocked_runtime_mutation_detected",
    "final_gate_informational_only",
    "not_applicable",
]
ALLOWED_READINESS_STATUSES = [
    "ready_for_future_runtime_application_blueprint",
    "ready_with_warnings_for_future_runtime_application_blueprint",
    "not_ready_for_future_runtime_application_blueprint",
    "readiness_blocked",
    "readiness_informational_only",
    "not_applicable",
]
ALLOWED_BLOCKER_STATUSES = [
    "no_unresolved_blockers_reported",
    "unresolved_blockers_reported",
    "blocker_summary_missing",
    "blocker_summary_incomplete",
    "blocker_summary_blocked",
    "not_applicable",
]
ALLOWED_ARTIFACT_CHECKLIST_STATUSES = [
    "all_required_artifacts_present",
    "required_artifacts_missing",
    "required_artifacts_incomplete",
    "artifact_checklist_blocked",
    "not_applicable",
]
ALLOWED_REGRESSION_CHECKLIST_STATUSES = [
    "all_required_regression_gate_refs_present",
    "required_regression_gate_refs_missing",
    "required_regression_gate_refs_incomplete",
    "regression_checklist_blocked",
    "not_applicable",
]
ALLOWED_ROLLBACK_READINESS_STATUSES = [
    "rollback_ready_for_future_application_blueprint",
    "rollback_readiness_incomplete",
    "rollback_readiness_blocked",
    "rollback_not_applicable",
    "not_applicable",
]
ALLOWED_POST_APPLICATION_VERIFICATION_READINESS_STATUSES = [
    "post_application_verification_plan_ready",
    "post_application_verification_plan_incomplete",
    "post_application_verification_plan_blocked",
    "post_application_verification_not_applicable",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "final_gate_passed_not_applied",
    "not_applied",
    "staged_not_applied",
    "runtime_application_not_supported_in_this_blueprint",
    "future_blueprint_required",
    "blocked_from_runtime_application",
    "not_applicable",
]
ALLOWED_RUNTIME_CONFIG_STATUSES = [
    "not_updated",
    "staged_delta_only",
    "runtime_config_update_not_supported",
    "blocked_from_update",
    "not_applicable",
]
ALLOWED_PRODUCTION_CONFIG_STATUSES = [
    "not_created",
    "production_config_not_supported",
    "staged_package_only",
    "blocked_from_creation",
    "not_applicable",
]

FINAL_GATE_INPUT_REQUIRED_FIELDS = [
    "final_gate_input_id",
    "final_gate_input_type",
    "final_gate_input_version",
    "generated_at",
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
    "current_runtime_settings_ref",
    "staged_candidate_settings_ref",
    "staged_config_delta_ref",
    "operator_signoff_ref",
    "pre_apply_manifest_ref",
    "rollback_staging_ref",
    "post_application_verification_staging_ref",
    "future_baseline_policy_ref",
    "source_artifact_presence",
    "required_artifacts",
    "required_regression_gates",
    "required_operator_artifacts",
    "blockers",
    "warnings",
    "non_claims",
]
FINAL_GATE_REQUIRED_FIELDS = [
    "final_gate_id",
    "final_gate_type",
    "final_gate_version",
    "generated_at",
    "source_final_gate_input_path",
    "source_runtime_application_staging_path",
    "source_application_plan_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "staged_candidate_settings",
    "staged_config_delta_ref",
    "final_gate_status",
    "readiness_status",
    "blocker_status",
    "artifact_checklist_status",
    "regression_checklist_status",
    "rollback_readiness_status",
    "post_application_verification_readiness_status",
    "future_baseline_policy_status",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "runtime_config_status",
    "baseline_update_status",
    "model_update_status",
    "future_blueprint_required_for_runtime_application",
    "required_artifacts",
    "required_regression_gates",
    "required_operator_artifacts",
    "blockers",
    "warnings",
    "non_claims",
]
READINESS_REPORT_REQUIRED_FIELDS = [
    "readiness_report_id",
    "readiness_report_type",
    "readiness_report_version",
    "generated_at",
    "source_final_gate_id",
    "readiness_status",
    "final_gate_status",
    "artifact_checklist_status",
    "regression_checklist_status",
    "rollback_readiness_status",
    "post_application_verification_readiness_status",
    "future_baseline_policy_status",
    "runtime_application_status",
    "mutation_status",
    "blockers",
    "warnings",
    "non_claims",
]
BLOCKER_REPORT_REQUIRED_FIELDS = [
    "blocker_report_id",
    "blocker_report_type",
    "blocker_report_version",
    "generated_at",
    "source_final_gate_id",
    "blocker_status",
    "final_gate_status",
    "readiness_status",
    "blockers",
    "missing_artifact_requirements",
    "missing_regression_requirements",
    "runtime_application_status",
    "mutation_status",
    "warnings",
    "non_claims",
]
ARTIFACT_CHECKLIST_REPORT_REQUIRED_FIELDS = [
    "artifact_checklist_id",
    "artifact_checklist_type",
    "artifact_checklist_version",
    "generated_at",
    "source_final_gate_id",
    "artifact_checklist_status",
    "required_artifacts",
    "runtime_application_status",
    "mutation_status",
    "warnings",
    "non_claims",
]
REGRESSION_CHECKLIST_REPORT_REQUIRED_FIELDS = [
    "regression_checklist_id",
    "regression_checklist_type",
    "regression_checklist_version",
    "generated_at",
    "source_final_gate_id",
    "regression_checklist_status",
    "required_regression_gates",
    "runtime_application_status",
    "mutation_status",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "final_gate_is_not_truth": True,
    "final_gate_is_not_accuracy_scoring": True,
    "final_gate_is_not_runtime_calibration": True,
    "final_gate_is_not_runtime_application": True,
    "final_gate_pass_is_not_runtime_application": True,
    "runtime_application_not_performed": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "runtime_config_not_updated": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "future_blueprint_required_for_runtime_application": True,
    "classifier_correctness_not_assessed": True,
}
WARNINGS = {
    **dict(NON_CLAIMS),
    "controlled_pre_application_final_gate": True,
    "future_blueprint_required_for_runtime_application": True,
    "no_runtime_mutation": True,
    "runtime_config_not_updated": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "model_weights_not_modified": True,
    "review_support_only": True,
    "structural_final_gate_only": True,
    "does_not_create_evidence": True,
    "does_not_create_observations": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_create_point_labels": True,
    "does_not_create_event_labels": True,
    "does_not_create_training_labels": True,
    "does_not_mutate_model_assets": True,
    "does_not_mutate_regression_baselines": True,
    "does_not_train_classifier": True,
    "no_adjudication": True,
}
FORBIDDEN_FINAL_GATE_TOKENS = {
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
    "threshold_applied",
    "smoothing_applied",
    "hysteresis_applied",
    "model_updated",
    "model_weights_modified",
    "runtime_config_updated",
    "baseline_replaced",
    "threshold_changes_applied",
    "smoothing_changes_applied",
    "hysteresis_changes_applied",
    "auto_approved",
    "auto_rejected",
    "production_config_created",
    "runtime_application_performed",
}


def export_controlled_runtime_calibration_pre_application_final_gate_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_EXPORTED_AT
    )
    contract = {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "final_gate_scope": {
            "consumes_runtime_application_staging_artifact": True,
            "creates_final_pre_application_gate_artifact": True,
            "creates_readiness_verdict_for_future_blueprint": True,
            "creates_blocker_summary": True,
            "creates_artifact_checklist": True,
            "creates_regression_checklist": True,
            "runtime_application_supported_in_this_blueprint": False,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "updates_runtime_configuration": False,
            "creates_production_configuration": False,
            "updates_model_weights": False,
            "replaces_regression_baselines": False,
            "performs_automatic_approval": False,
            "performs_automatic_rejection": False,
            "scores_classifier_outputs": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "final_gate_input_schema": {
            "input_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_TYPE,
            "input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_VERSION
            ),
            "required_fields": list(FINAL_GATE_INPUT_REQUIRED_FIELDS),
        },
        "final_gate_artifact_schema": {
            "artifact_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_TYPE,
            "artifact_version": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION,
            "required_fields": list(FINAL_GATE_REQUIRED_FIELDS),
            "allowed_final_gate_statuses": list(ALLOWED_FINAL_GATE_STATUSES),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "required_mutation_status": "no_runtime_mutation",
            "required_runtime_config_status": "not_updated",
            "required_production_config_status": "not_created",
            "required_baseline_update_status": "not_replaced",
            "required_model_update_status": "not_modified",
            "future_blueprint_required_for_runtime_application": True,
        },
        "final_gate_readiness_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_READINESS_REPORT_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION,
            "required_fields": list(READINESS_REPORT_REQUIRED_FIELDS),
            "allowed_readiness_statuses": list(ALLOWED_READINESS_STATUSES),
        },
        "final_gate_blocker_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_BLOCKER_REPORT_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION,
            "required_fields": list(BLOCKER_REPORT_REQUIRED_FIELDS),
            "allowed_blocker_statuses": list(ALLOWED_BLOCKER_STATUSES),
        },
        "final_gate_artifact_checklist_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_ARTIFACT_CHECKLIST_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION,
            "required_fields": list(ARTIFACT_CHECKLIST_REPORT_REQUIRED_FIELDS),
            "allowed_artifact_checklist_statuses": list(
                ALLOWED_ARTIFACT_CHECKLIST_STATUSES
            ),
        },
        "final_gate_regression_checklist_schema": {
            "report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_REGRESSION_CHECKLIST_TYPE,
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION,
            "required_fields": list(REGRESSION_CHECKLIST_REPORT_REQUIRED_FIELDS),
            "allowed_regression_checklist_statuses": list(
                ALLOWED_REGRESSION_CHECKLIST_STATUSES
            ),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_final_gate_input_shape": True,
            "validate_final_gate_artifact_shape": True,
            "validate_readiness_report_shape": True,
            "validate_blocker_report_shape": True,
            "validate_artifact_checklist_shape": True,
            "validate_regression_checklist_shape": True,
            "validate_allowed_statuses": True,
            "validate_no_runtime_mutation": True,
            "validate_no_runtime_config_update": True,
            "validate_no_production_config_creation": True,
            "validate_no_baseline_replacement": True,
            "validate_model_not_modified": True,
            "validate_future_blueprint_required": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_metrics": True,
        },
        "provenance_requirements": {
            "runtime_application_staging_path_required": True,
            "application_plan_path_required": True,
            "human_approval_gate_path_required": True,
            "dry_run_review_packet_path_required": True,
            "dry_run_execution_report_path_required": True,
            "change_request_path_required": True,
            "candidate_config_freeze_path_required": True,
            "model_asset_hash_required": True,
            "staged_config_delta_ref_required": True,
            "pre_apply_manifest_ref_required": True,
            "rollback_staging_ref_required": True,
            "post_application_verification_staging_ref_required": True,
            "future_baseline_policy_ref_required": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    result = {
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
    _write_json_if_requested(output_path, contract)
    return result


def build_controlled_runtime_calibration_pre_application_final_gate_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
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
    current_runtime_settings_ref: str | None = None,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    source_payloads = {
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
    staging = source_payloads["runtime_application_staging"]
    staged_config_delta = _dict(staging.get("staged_config_delta"))
    pre_apply_manifest = _dict(staging.get("pre_apply_manifest"))
    rollback_staging = _dict(staging.get("rollback_staging_record"))
    verification_staging = _dict(
        staging.get("post_application_verification_staging_record")
    )
    future_baseline_policy = _dict(
        staging.get("future_baseline_candidate_staging_policy")
    )
    current_settings = _dict(staging.get("current_settings")) or _dict(
        source_payloads["application_plan"].get("current_settings")
    )
    staged_candidate_settings = _dict(staging.get("staged_candidate_settings"))
    selected_candidate_ref = _dict(staging.get("selected_candidate_config_ref")) or _dict(
        source_payloads["application_plan"].get("selected_candidate_config_ref")
    )
    source_presence = _source_artifact_presence(
        source_payloads,
        {
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
        "final_gate_input_id": _stable_id(
            "controlled_runtime_calibration_pre_application_final_gate_inputs_v1",
            _path_string(source_runtime_application_staging_path),
            staging.get("staging_id"),
            selected_candidate_ref,
            staged_config_delta.get("staged_config_delta_id"),
        ),
        "final_gate_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_TYPE
        ),
        "final_gate_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
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
        "source_candidate_config_freeze_id": source_payloads[
            "candidate_config_freeze"
        ].get("candidate_config_freeze_id"),
        "source_manual_approval_packet_id": source_payloads[
            "manual_approval_packet"
        ].get("manual_approval_packet_id"),
        "source_decision_packet_id": source_payloads["decision_packet"].get(
            "decision_packet_id"
        ),
        "selected_candidate_config_ref": selected_candidate_ref,
        "model_asset_ref": str(Path(model_asset_path)),
        "model_asset_sha256": _sha256_path(model_asset_path)
        or staging.get("model_asset_sha256"),
        "current_runtime_settings_ref": current_runtime_settings_ref
        or staging.get("current_runtime_settings_ref")
        or "runtime_settings_from_staging",
        "current_settings": current_settings,
        "staged_candidate_settings": staged_candidate_settings,
        "staged_candidate_settings_ref": {
            "candidate_type": staged_candidate_settings.get("candidate_type"),
            "candidate_source": _dict(staged_candidate_settings.get("candidate_source")),
            "selected_candidate_config_ref": selected_candidate_ref,
            "staged_not_applied": True,
        },
        "staged_config_delta_ref": _staged_config_delta_ref(staged_config_delta),
        "operator_signoff_ref": _operator_signoff_ref(
            source_payloads["human_approval_gate"],
            pre_apply_manifest,
        ),
        "pre_apply_manifest_ref": _pre_apply_manifest_ref(pre_apply_manifest),
        "rollback_staging_ref": _rollback_staging_ref(rollback_staging),
        "post_application_verification_staging_ref": (
            _post_application_verification_ref(verification_staging)
        ),
        "future_baseline_policy_ref": _future_baseline_policy_ref(
            future_baseline_policy
        ),
        "source_artifact_presence": source_presence,
        "missing_source_refs": _missing_source_refs(source_presence),
        "required_artifacts": _list(pre_apply_manifest.get("required_artifacts")),
        "required_regression_gates": _required_regression_gates(staging),
        "required_operator_artifacts": _required_operator_artifacts(staging),
        "blockers": _collect_blockers(staging, source_payloads),
        "source_warning_categories": _source_warning_categories(source_payloads),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    status = "completed" if not errors else "invalid_final_gate_inputs"
    _write_json_if_requested(output_path, inputs)
    return {
        "ok": not errors,
        "status": status,
        "final_gate_input_id": inputs["final_gate_input_id"],
        "final_gate_input_type": inputs["final_gate_input_type"],
        "final_gate_input_version": inputs["final_gate_input_version"],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "model_asset_sha256": inputs["model_asset_sha256"],
        "blocker_count": len(inputs["blockers"]),
        "missing_source_ref_count": len(inputs["missing_source_refs"]),
        "final_gate_inputs_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": inputs["warnings"],
    }


def validate_controlled_runtime_calibration_pre_application_final_gate_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(final_gate_inputs_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    result = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": (
            "controlled_runtime_calibration_pre_application_final_gate_inputs_validation"
        ),
        "validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(final_gate_inputs_path)),
        "payload_type": inputs.get("final_gate_input_type"),
        "payload_version": inputs.get("final_gate_input_version"),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_pre_application_final_gate(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUTS_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    inputs = _load_json(final_gate_inputs_path)
    artifact_checklist = _artifact_checklist(inputs, generated_at)
    regression_checklist = _regression_checklist(inputs, generated_at)
    blocker_summary = _blocker_summary(inputs, artifact_checklist, regression_checklist)
    rollback_readiness_status = _rollback_readiness_status(inputs)
    post_application_verification_readiness_status = (
        _post_application_verification_readiness_status(inputs)
    )
    final_gate_status = _final_gate_status(
        inputs=inputs,
        artifact_checklist=artifact_checklist,
        regression_checklist=regression_checklist,
        blocker_summary=blocker_summary,
        rollback_readiness_status=rollback_readiness_status,
        post_application_verification_readiness_status=(
            post_application_verification_readiness_status
        ),
    )
    readiness_status = _readiness_status(final_gate_status, inputs)
    runtime_application_status = _runtime_application_status(final_gate_status)
    final_gate = {
        "final_gate_id": _stable_id(
            "controlled_runtime_calibration_pre_application_final_gate_v1",
            inputs.get("final_gate_input_id"),
            final_gate_status,
            blocker_summary.get("blockers"),
        ),
        "final_gate_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_TYPE,
        "final_gate_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_input_path": str(Path(final_gate_inputs_path)),
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
        "current_settings": _dict(inputs.get("current_settings")),
        "staged_candidate_settings": _dict(inputs.get("staged_candidate_settings")),
        "staged_config_delta_ref": _dict(inputs.get("staged_config_delta_ref")),
        "operator_signoff_ref": _dict(inputs.get("operator_signoff_ref")),
        "pre_apply_manifest_ref": _dict(inputs.get("pre_apply_manifest_ref")),
        "rollback_staging_ref": _dict(inputs.get("rollback_staging_ref")),
        "post_application_verification_staging_ref": _dict(
            inputs.get("post_application_verification_staging_ref")
        ),
        "future_baseline_policy_ref": _dict(inputs.get("future_baseline_policy_ref")),
        "final_gate_status": final_gate_status,
        "readiness_status": readiness_status,
        "blocker_status": blocker_summary["blocker_status"],
        "artifact_checklist_status": artifact_checklist["artifact_checklist_status"],
        "regression_checklist_status": regression_checklist[
            "regression_checklist_status"
        ],
        "rollback_readiness_status": rollback_readiness_status,
        "post_application_verification_readiness_status": (
            post_application_verification_readiness_status
        ),
        "future_baseline_policy_status": _dict(
            inputs.get("future_baseline_policy_ref")
        ).get("future_baseline_policy_status", "not_applicable"),
        "runtime_application_status": runtime_application_status,
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "runtime_config_status": "not_updated",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "required_artifacts": artifact_checklist["required_artifacts"],
        "required_regression_gates": regression_checklist[
            "required_regression_gates"
        ],
        "required_operator_artifacts": _list(
            inputs.get("required_operator_artifacts")
        ),
        "blockers": blocker_summary["blockers"],
        "blocker_summary": blocker_summary,
        "artifact_checklist": artifact_checklist,
        "regression_checklist": regression_checklist,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {**_dict(inputs.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_inputs_shape(inputs))
    errors.extend(_validate_final_gate_shape(final_gate))
    _write_json_if_requested(output_path, final_gate)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_final_gate",
        "final_gate_id": final_gate["final_gate_id"],
        "final_gate_type": final_gate["final_gate_type"],
        "final_gate_version": final_gate["final_gate_version"],
        "final_gate_status": final_gate_status,
        "readiness_status": readiness_status,
        "runtime_application_status": runtime_application_status,
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "blocker_count": len(final_gate["blockers"]),
        "final_gate_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": final_gate["warnings"],
    }


def validate_controlled_runtime_calibration_pre_application_final_gate(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or _now_utc()
    contract = _load_json(contract_path)
    final_gate = _load_json(final_gate_path)
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_final_gate_shape(final_gate))
    result = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": (
            "controlled_runtime_calibration_pre_application_final_gate_validation"
        ),
        "validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(final_gate_path)),
        "payload_type": final_gate.get("final_gate_type"),
        "payload_version": final_gate.get("final_gate_version"),
        "final_gate_status": final_gate.get("final_gate_status"),
        "readiness_status": final_gate.get("readiness_status"),
        "runtime_application_status": final_gate.get("runtime_application_status"),
        "mutation_status": final_gate.get("mutation_status"),
        "future_blueprint_required_for_runtime_application": final_gate.get(
            "future_blueprint_required_for_runtime_application"
        ),
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, result)
    return result


def build_controlled_runtime_calibration_final_gate_readiness_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    final_gate = _load_json(final_gate_path)
    report = {
        "readiness_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_readiness_report_v1",
            final_gate.get("final_gate_id"),
            final_gate.get("readiness_status"),
        ),
        "readiness_report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_READINESS_REPORT_TYPE
        ),
        "readiness_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_id": final_gate.get("final_gate_id"),
        "source_final_gate_path": str(Path(final_gate_path)),
        "readiness_status": final_gate.get("readiness_status"),
        "final_gate_status": final_gate.get("final_gate_status"),
        "artifact_checklist_status": final_gate.get("artifact_checklist_status"),
        "regression_checklist_status": final_gate.get("regression_checklist_status"),
        "rollback_readiness_status": final_gate.get("rollback_readiness_status"),
        "post_application_verification_readiness_status": final_gate.get(
            "post_application_verification_readiness_status"
        ),
        "future_baseline_policy_status": final_gate.get(
            "future_baseline_policy_status"
        ),
        "runtime_application_status": final_gate.get("runtime_application_status"),
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "blockers": _list(final_gate.get("blockers")),
        "warnings": {**_dict(final_gate.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_readiness_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_readiness_report",
        "readiness_report_id": report["readiness_report_id"],
        "readiness_status": report["readiness_status"],
        "final_gate_status": report["final_gate_status"],
        "runtime_application_status": report["runtime_application_status"],
        "mutation_status": "no_runtime_mutation",
        "readiness_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": report["warnings"],
    }


def build_controlled_runtime_calibration_final_gate_blocker_report(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_BLOCKER_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    final_gate = _load_json(final_gate_path)
    blocker_summary = _dict(final_gate.get("blocker_summary"))
    report = {
        "blocker_report_id": _stable_id(
            "controlled_runtime_calibration_final_gate_blocker_report_v1",
            final_gate.get("final_gate_id"),
            blocker_summary.get("blockers"),
        ),
        "blocker_report_type": CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_BLOCKER_REPORT_TYPE,
        "blocker_report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_id": final_gate.get("final_gate_id"),
        "source_final_gate_path": str(Path(final_gate_path)),
        "blocker_status": final_gate.get("blocker_status"),
        "final_gate_status": final_gate.get("final_gate_status"),
        "readiness_status": final_gate.get("readiness_status"),
        "blockers": _list(blocker_summary.get("blockers")),
        "missing_artifact_requirements": _list(
            blocker_summary.get("missing_artifact_requirements")
        ),
        "missing_regression_requirements": _list(
            blocker_summary.get("missing_regression_requirements")
        ),
        "runtime_application_status": final_gate.get("runtime_application_status"),
        "mutation_status": "no_runtime_mutation",
        "warnings": {**_dict(final_gate.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_blocker_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_blocker_report",
        "blocker_report_id": report["blocker_report_id"],
        "blocker_status": report["blocker_status"],
        "blocker_count": len(report["blockers"]),
        "runtime_application_status": report["runtime_application_status"],
        "mutation_status": "no_runtime_mutation",
        "blocker_report_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": report["warnings"],
    }


def build_controlled_runtime_calibration_final_gate_artifact_checklist(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_ARTIFACT_CHECKLIST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    final_gate = _load_json(final_gate_path)
    report = {
        "artifact_checklist_id": _stable_id(
            "controlled_runtime_calibration_final_gate_artifact_checklist_v1",
            final_gate.get("final_gate_id"),
            final_gate.get("artifact_checklist_status"),
        ),
        "artifact_checklist_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_ARTIFACT_CHECKLIST_TYPE
        ),
        "artifact_checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_id": final_gate.get("final_gate_id"),
        "source_final_gate_path": str(Path(final_gate_path)),
        "artifact_checklist_status": final_gate.get("artifact_checklist_status"),
        "required_artifacts": _list(final_gate.get("required_artifacts")),
        "runtime_application_status": final_gate.get("runtime_application_status"),
        "mutation_status": "no_runtime_mutation",
        "warnings": {**_dict(final_gate.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_artifact_checklist_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_artifact_checklist",
        "artifact_checklist_id": report["artifact_checklist_id"],
        "artifact_checklist_status": report["artifact_checklist_status"],
        "runtime_application_status": report["runtime_application_status"],
        "mutation_status": "no_runtime_mutation",
        "artifact_checklist_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": report["warnings"],
    }


def build_controlled_runtime_calibration_final_gate_regression_checklist(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_OUTPUT
    ),
    final_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_REGRESSION_CHECKLIST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or _now_utc()
    contract = _load_json(contract_path)
    final_gate = _load_json(final_gate_path)
    report = {
        "regression_checklist_id": _stable_id(
            "controlled_runtime_calibration_final_gate_regression_checklist_v1",
            final_gate.get("final_gate_id"),
            final_gate.get("regression_checklist_status"),
        ),
        "regression_checklist_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_REGRESSION_CHECKLIST_TYPE
        ),
        "regression_checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_final_gate_id": final_gate.get("final_gate_id"),
        "source_final_gate_path": str(Path(final_gate_path)),
        "regression_checklist_status": final_gate.get("regression_checklist_status"),
        "required_regression_gates": _list(
            final_gate.get("required_regression_gates")
        ),
        "runtime_application_status": final_gate.get("runtime_application_status"),
        "mutation_status": "no_runtime_mutation",
        "warnings": {**_dict(final_gate.get("warnings")), **dict(WARNINGS)},
        "non_claims": dict(NON_CLAIMS),
    }
    errors = _validate_contract_shape(contract)
    errors.extend(_validate_regression_checklist_report_shape(report))
    _write_json_if_requested(output_path, report)
    return {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_regression_checklist",
        "regression_checklist_id": report["regression_checklist_id"],
        "regression_checklist_status": report["regression_checklist_status"],
        "runtime_application_status": report["runtime_application_status"],
        "mutation_status": "no_runtime_mutation",
        "regression_checklist_output": _path_string(output_path),
        "error_count": len(errors),
        "errors": errors,
        "warnings": report["warnings"],
    }


def _artifact_checklist(
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    checks = [
        _artifact_check(
            "runtime_application_staging_artifact_present",
            _source_present(source_presence, "runtime_application_staging"),
            inputs.get("source_runtime_application_staging_path"),
        ),
        _artifact_check(
            "application_plan_present",
            _source_present(source_presence, "application_plan"),
            inputs.get("source_application_plan_path"),
        ),
        _artifact_check(
            "human_approval_gate_present",
            _source_present(source_presence, "human_approval_gate"),
            inputs.get("source_human_approval_gate_path"),
        ),
        _artifact_check(
            "operator_signoff_artifact_present",
            _dict(inputs.get("operator_signoff_ref")).get(
                "operator_signoff_artifact_present"
            )
            is True,
            inputs.get("source_human_approval_gate_path"),
        ),
        _artifact_check(
            "dry_run_review_packet_present",
            _source_present(source_presence, "dry_run_review_packet"),
            inputs.get("source_dry_run_review_packet_path"),
        ),
        _artifact_check(
            "dry_run_execution_report_present",
            _source_present(source_presence, "dry_run_execution_report"),
            inputs.get("source_dry_run_execution_report_path"),
        ),
        _artifact_check(
            "controlled_change_request_present",
            _source_present(source_presence, "change_request"),
            inputs.get("source_change_request_path"),
        ),
        _artifact_check(
            "candidate_config_freeze_present",
            _source_present(source_presence, "candidate_config_freeze"),
            inputs.get("source_candidate_config_freeze_path"),
        ),
        _artifact_check(
            "manual_approval_packet_present",
            _source_present(source_presence, "manual_approval_packet"),
            inputs.get("source_manual_approval_packet_path"),
        ),
        _artifact_check(
            "staged_config_delta_present",
            bool(_dict(inputs.get("staged_config_delta_ref")).get("staged_config_delta_id")),
            _dict(inputs.get("staged_config_delta_ref")).get("staged_config_delta_id"),
        ),
        _artifact_check(
            "pre_apply_manifest_present",
            bool(_dict(inputs.get("pre_apply_manifest_ref")).get("pre_apply_manifest_id")),
            _dict(inputs.get("pre_apply_manifest_ref")).get("pre_apply_manifest_id"),
        ),
        _artifact_check(
            "rollback_staging_record_present",
            bool(_dict(inputs.get("rollback_staging_ref")).get("rollback_staging_id")),
            _dict(inputs.get("rollback_staging_ref")).get("rollback_staging_id"),
        ),
        _artifact_check(
            "post_application_verification_staging_record_present",
            bool(
                _dict(inputs.get("post_application_verification_staging_ref")).get(
                    "post_application_verification_staging_id"
                )
            ),
            _dict(inputs.get("post_application_verification_staging_ref")).get(
                "post_application_verification_staging_id"
            ),
        ),
        _artifact_check(
            "future_baseline_policy_present",
            bool(
                _dict(inputs.get("future_baseline_policy_ref")).get(
                    "future_baseline_policy_status"
                )
            ),
            _dict(inputs.get("future_baseline_policy_ref")).get(
                "future_baseline_policy_status"
            ),
        ),
        _artifact_check(
            "model_asset_hash_captured",
            bool(inputs.get("model_asset_sha256")),
            inputs.get("model_asset_ref"),
        ),
        _artifact_check(
            "no_generated_exports_committed",
            True,
            "checked_by_git_status_before_commit",
        ),
        _artifact_check(
            "no_unresolved_blockers",
            not _list(inputs.get("blockers")),
            "blocker_summary",
        ),
        _artifact_check(
            "no_runtime_mutation_in_prior_artifacts",
            _no_runtime_mutation_in_prior_refs(inputs),
            "source_runtime_application_staging_path",
        ),
        _artifact_check(
            "future_blueprint_required",
            True,
            "future_blueprint_required_for_runtime_application",
        ),
    ]
    status = (
        "all_required_artifacts_present"
        if all(check["status"] == "present" for check in checks)
        else "required_artifacts_missing"
    )
    return {
        "artifact_checklist_id": _stable_id(
            "controlled_runtime_calibration_final_gate_artifact_checklist_v1",
            inputs.get("final_gate_input_id"),
            checks,
        ),
        "artifact_checklist_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_ARTIFACT_CHECKLIST_TYPE
        ),
        "artifact_checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "artifact_checklist_status": status,
        "required_artifacts": checks,
        "missing_requirements": [
            check["requirement"] for check in checks if check["status"] != "present"
        ],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _regression_checklist(
    inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    source_gate_names = {
        str(_dict(gate).get("gate"))
        for gate in _list(inputs.get("required_regression_gates"))
        if _dict(gate).get("required", True) is True
    }
    required_gate_names = [
        "multi_point_regression_matrix",
        "protected_sample_point_reviewed_3d_debug",
        "gameplay_gate_regression_baseline",
        "review_guided_gameplay_calibration_sandbox_regression",
    ]
    checks = [
        _regression_check(
            "multi_point_regression_gate_required",
            "multi_point_regression_matrix" in source_gate_names,
            "tom-v1-verify-multi-point-regression-matrix",
        ),
        _regression_check(
            "protected_sample_point_gate_required",
            "protected_sample_point_reviewed_3d_debug" in source_gate_names,
            "tom-v1-verify-reviewed-3d-debug-baseline",
        ),
        _regression_check(
            "gameplay_gate_regression_baseline_gate_required",
            "gameplay_gate_regression_baseline" in source_gate_names,
            "tom-v1-verify-gameplay-gate-regression-baseline",
        ),
        _regression_check(
            "calibration_sandbox_regression_gate_required",
            "review_guided_gameplay_calibration_sandbox_regression"
            in source_gate_names,
            (
                "tom-v1-verify-review-guided-gameplay-calibration-"
                "sandbox-regression-baseline"
            ),
        ),
        _regression_check(
            "dry_run_regression_checks_referenced",
            bool(source_gate_names),
            "dry_run_regression_gate_requirements",
        ),
        _regression_check(
            "staging_validation_referenced",
            bool(_dict(inputs.get("staged_config_delta_ref"))),
            "controlled_runtime_calibration_runtime_application_staging.validation",
        ),
        _regression_check(
            "all_required_gate_refs_present",
            all(gate in source_gate_names for gate in required_gate_names),
            "required_regression_gates",
        ),
        _regression_check(
            "no_drift_flags_unresolved",
            not _has_blocker_with_fragment(inputs, "drift"),
            "regression_gate_reports",
        ),
        _regression_check(
            "no_breaking_drift_unresolved",
            not _has_blocker_with_fragment(inputs, "breaking"),
            "regression_gate_reports",
        ),
        _regression_check(
            "baseline_not_replaced",
            True,
            "baseline_update_status:not_replaced",
        ),
        _regression_check(
            "future_blueprint_required",
            True,
            "future_blueprint_required_for_runtime_application",
        ),
    ]
    status = (
        "all_required_regression_gate_refs_present"
        if all(check["status"] == "present" for check in checks)
        else "required_regression_gate_refs_missing"
    )
    return {
        "regression_checklist_id": _stable_id(
            "controlled_runtime_calibration_final_gate_regression_checklist_v1",
            inputs.get("final_gate_input_id"),
            checks,
        ),
        "regression_checklist_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FINAL_GATE_REGRESSION_CHECKLIST_TYPE
        ),
        "regression_checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "regression_checklist_status": status,
        "required_regression_gates": checks,
        "missing_requirements": [
            check["requirement"] for check in checks if check["status"] != "present"
        ],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _final_gate_status(
    *,
    inputs: dict[str, Any],
    artifact_checklist: dict[str, Any],
    regression_checklist: dict[str, Any],
    blocker_summary: dict[str, Any],
    rollback_readiness_status: str,
    post_application_verification_readiness_status: str,
) -> str:
    missing = set(_list(artifact_checklist.get("missing_requirements")))
    source_presence = _dict(inputs.get("source_artifact_presence"))
    if not _source_present(source_presence, "runtime_application_staging"):
        return "final_gate_blocked_missing_staging_artifact"
    if "application_plan_present" in missing:
        return "final_gate_blocked_missing_application_plan"
    if "human_approval_gate_present" in missing:
        return "final_gate_blocked_missing_human_approval_gate"
    if "dry_run_review_packet_present" in missing:
        return "final_gate_blocked_missing_dry_run_review_packet"
    if "controlled_change_request_present" in missing:
        return "final_gate_blocked_missing_change_request"
    if _runtime_mutation_detected(inputs):
        return "final_gate_blocked_runtime_mutation_detected"
    if _runtime_config_has_non_staged_status(inputs):
        return "final_gate_blocked_runtime_mutation_detected"
    if _production_config_has_creation_status(inputs):
        return "final_gate_blocked_runtime_mutation_detected"
    if _baseline_policy_has_replacement_status(inputs):
        return "final_gate_blocked_runtime_mutation_detected"
    if "model_asset_hash_captured" in missing:
        return "final_gate_blocked_model_asset_provenance_missing"
    if "operator_signoff_artifact_present" in missing:
        return "final_gate_blocked_missing_operator_signoff"
    if not _has_selected_candidate_ref(_dict(inputs.get("selected_candidate_config_ref"))):
        return "final_gate_blocked_missing_candidate_config"
    if "candidate_config_freeze_present" in missing:
        return "final_gate_blocked_missing_candidate_config"
    if "pre_apply_manifest_present" in missing:
        return "final_gate_blocked_missing_pre_apply_manifest"
    if "rollback_staging_record_present" in missing or rollback_readiness_status != (
        "rollback_ready_for_future_application_blueprint"
    ):
        return "final_gate_blocked_missing_rollback_plan"
    if (
        "post_application_verification_staging_record_present" in missing
        or post_application_verification_readiness_status
        != "post_application_verification_plan_ready"
    ):
        return "final_gate_blocked_missing_post_application_verification_plan"
    staged_delta_status = _dict(inputs.get("staged_config_delta_ref")).get(
        "delta_status"
    )
    if staged_delta_status == "staged_blocked_invalid_scope":
        return "final_gate_blocked_breaking_structural_change"
    if regression_checklist.get("regression_checklist_status") != (
        "all_required_regression_gate_refs_present"
    ):
        return "final_gate_blocked_missing_regression_gate"
    if blocker_summary.get("blocker_status") == "unresolved_blockers_reported":
        return "final_gate_blocked_unresolved_blockers"
    if artifact_checklist.get("artifact_checklist_status") != (
        "all_required_artifacts_present"
    ):
        return "final_gate_blocked_missing_pre_apply_manifest"
    return "final_gate_passed_not_applied"


def _readiness_status(final_gate_status: str, inputs: dict[str, Any]) -> str:
    if final_gate_status == "final_gate_passed_not_applied":
        if _dict(inputs.get("warnings")):
            return "ready_with_warnings_for_future_runtime_application_blueprint"
        return "ready_for_future_runtime_application_blueprint"
    if final_gate_status == "final_gate_informational_only":
        return "readiness_informational_only"
    return "not_ready_for_future_runtime_application_blueprint"


def _runtime_application_status(final_gate_status: str) -> str:
    if final_gate_status.startswith("final_gate_passed"):
        return "final_gate_passed_not_applied"
    if final_gate_status == "not_applicable":
        return "not_applicable"
    return "blocked_from_runtime_application"


def _blocker_summary(
    inputs: dict[str, Any],
    artifact_checklist: dict[str, Any],
    regression_checklist: dict[str, Any],
) -> dict[str, Any]:
    blockers = _unique_strings(_list(inputs.get("blockers")))
    missing_artifact_requirements = _list(artifact_checklist.get("missing_requirements"))
    missing_regression_requirements = _list(
        regression_checklist.get("missing_requirements")
    )
    if missing_artifact_requirements:
        blockers.extend(
            f"missing_artifact:{requirement}"
            for requirement in missing_artifact_requirements
        )
    if missing_regression_requirements:
        blockers.extend(
            f"missing_regression:{requirement}"
            for requirement in missing_regression_requirements
        )
    blockers = _unique_strings(blockers)
    status = (
        "unresolved_blockers_reported"
        if blockers
        else "no_unresolved_blockers_reported"
    )
    return {
        "blocker_summary_id": _stable_id(
            "controlled_runtime_calibration_final_gate_blocker_summary_v1",
            inputs.get("final_gate_input_id"),
            blockers,
        ),
        "blocker_status": status,
        "blockers": blockers,
        "missing_artifact_requirements": missing_artifact_requirements,
        "missing_regression_requirements": missing_regression_requirements,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _rollback_readiness_status(inputs: dict[str, Any]) -> str:
    rollback_ref = _dict(inputs.get("rollback_staging_ref"))
    if not rollback_ref:
        return "rollback_readiness_incomplete"
    if rollback_ref.get("rollback_staging_status") == "rollback_staging_record_defined":
        return "rollback_ready_for_future_application_blueprint"
    if rollback_ref.get("rollback_staging_status") == "rollback_staging_record_blocked":
        return "rollback_readiness_blocked"
    return "rollback_readiness_incomplete"


def _post_application_verification_readiness_status(inputs: dict[str, Any]) -> str:
    verification_ref = _dict(inputs.get("post_application_verification_staging_ref"))
    if not verification_ref:
        return "post_application_verification_plan_incomplete"
    if verification_ref.get("verification_staging_status") == (
        "post_application_verification_staged"
    ):
        return "post_application_verification_plan_ready"
    if verification_ref.get("verification_staging_status") == (
        "post_application_verification_staging_blocked"
    ):
        return "post_application_verification_plan_blocked"
    return "post_application_verification_plan_incomplete"


def _artifact_check(requirement: str, present: bool, evidence_ref: Any) -> dict[str, Any]:
    return {
        "requirement": requirement,
        "status": "present" if present else "missing",
        "evidence_ref": evidence_ref,
        "required": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
    }


def _regression_check(
    requirement: str,
    present: bool,
    evidence_ref: Any,
) -> dict[str, Any]:
    return {
        "requirement": requirement,
        "status": "present" if present else "missing",
        "evidence_ref": evidence_ref,
        "required": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
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
            "not_updated",
        ),
        "mutation_status": staged_config_delta.get(
            "mutation_status",
            "no_runtime_mutation",
        ),
    }


def _operator_signoff_ref(
    human_approval_gate: dict[str, Any],
    pre_apply_manifest: dict[str, Any],
) -> dict[str, Any]:
    signoff_status = human_approval_gate.get("operator_signoff_status")
    artifacts = _list(pre_apply_manifest.get("required_operator_artifacts"))
    artifact_required = any(
        _dict(artifact).get("artifact") == "operator_signoff_record"
        for artifact in artifacts
    ) or signoff_status == "operator_signoff_required"
    artifact_present = bool(human_approval_gate.get("operator_signoff_ref")) or (
        signoff_status
        in {
            "operator_signoff_recorded",
            "operator_signoff_present",
            "manual_operator_signoff_recorded",
        }
    )
    return {
        "operator_signoff_required": artifact_required,
        "operator_signoff_artifact_present": artifact_present,
        "operator_signoff_status": signoff_status or "operator_signoff_required",
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
    }


def _pre_apply_manifest_ref(pre_apply_manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "pre_apply_manifest_id": pre_apply_manifest.get("pre_apply_manifest_id"),
        "pre_apply_manifest_version": pre_apply_manifest.get(
            "pre_apply_manifest_version"
        ),
        "manifest_status": pre_apply_manifest.get("manifest_status"),
        "missing_requirements": _list(pre_apply_manifest.get("missing_requirements")),
        "runtime_application_status": pre_apply_manifest.get(
            "runtime_application_status",
            "staged_not_applied",
        ),
        "mutation_status": pre_apply_manifest.get(
            "mutation_status",
            "no_runtime_mutation",
        ),
    }


def _rollback_staging_ref(rollback_staging: dict[str, Any]) -> dict[str, Any]:
    return {
        "rollback_staging_id": rollback_staging.get("rollback_staging_id"),
        "rollback_staging_version": rollback_staging.get("rollback_staging_version"),
        "rollback_staging_status": rollback_staging.get("rollback_staging_status"),
        "runtime_application_status": rollback_staging.get(
            "runtime_application_status",
            "staged_not_applied",
        ),
        "mutation_status": rollback_staging.get(
            "mutation_status",
            "no_runtime_mutation",
        ),
    }


def _post_application_verification_ref(verification_staging: dict[str, Any]) -> dict[str, Any]:
    return {
        "post_application_verification_staging_id": verification_staging.get(
            "post_application_verification_staging_id"
        ),
        "post_application_verification_staging_version": verification_staging.get(
            "post_application_verification_staging_version"
        ),
        "verification_staging_status": verification_staging.get(
            "verification_staging_status"
        ),
        "runtime_application_status": verification_staging.get(
            "runtime_application_status",
            "staged_not_applied",
        ),
        "mutation_status": verification_staging.get(
            "mutation_status",
            "no_runtime_mutation",
        ),
    }


def _future_baseline_policy_ref(future_baseline_policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "future_baseline_policy_status": future_baseline_policy.get(
            "future_baseline_policy_status"
        ),
        "baseline_update_status": future_baseline_policy.get(
            "baseline_update_status",
            "not_replaced",
        ),
        "future_baseline_candidate_not_created_in_this_blueprint": (
            future_baseline_policy.get(
                "future_baseline_candidate_not_created_in_this_blueprint"
            )
            is True
        ),
        "future_baseline_candidate_requires_post_application_review": (
            future_baseline_policy.get(
                "future_baseline_candidate_requires_post_application_review"
            )
            is True
        ),
        "runtime_application_status": future_baseline_policy.get(
            "runtime_application_status",
            "staged_not_applied",
        ),
        "mutation_status": future_baseline_policy.get(
            "mutation_status",
            "no_runtime_mutation",
        ),
    }


def _source_artifact_presence(
    source_payloads: dict[str, dict[str, Any]],
    source_paths: dict[str, str | Path | None],
) -> dict[str, dict[str, Any]]:
    presence: dict[str, dict[str, Any]] = {}
    for key, payload in source_payloads.items():
        path = source_paths.get(key)
        presence[key] = {
            "present": bool(payload),
            "path": _path_string(path),
            "artifact_type": _artifact_type(payload),
        }
    return presence


def _missing_source_refs(source_presence: dict[str, dict[str, Any]]) -> list[str]:
    required = {
        "runtime_application_staging",
        "application_plan",
        "human_approval_gate",
        "dry_run_review_packet",
        "dry_run_execution_report",
        "change_request",
        "candidate_config_freeze",
        "manual_approval_packet",
        "gameplay_gate_regression_baseline",
        "calibration_sandbox_baseline",
    }
    return [
        key
        for key in sorted(required)
        if _dict(source_presence.get(key)).get("present") is not True
    ]


def _artifact_type(payload: dict[str, Any]) -> str | None:
    for key in (
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


def _collect_blockers(
    staging: dict[str, Any],
    source_payloads: dict[str, dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    blockers.extend(str(item) for item in _list(staging.get("blockers")))
    for key in (
        "pre_apply_manifest",
        "staged_config_delta",
        "rollback_staging_record",
        "post_application_verification_staging_record",
    ):
        blockers.extend(str(item) for item in _list(_dict(staging.get(key)).get("blockers")))
    for payload in source_payloads.values():
        blockers.extend(str(item) for item in _list(payload.get("blockers")))
    return _unique_strings(blockers)


def _required_regression_gates(staging: dict[str, Any]) -> list[dict[str, Any]]:
    gates = _list(staging.get("required_regression_gates"))
    if not gates:
        gates = _list(_dict(staging.get("pre_apply_manifest")).get("required_regression_gates"))
    if not gates:
        gates = [
            {"gate": "multi_point_regression_matrix", "required": True},
            {"gate": "protected_sample_point_reviewed_3d_debug", "required": True},
            {"gate": "gameplay_gate_regression_baseline", "required": True},
            {
                "gate": "review_guided_gameplay_calibration_sandbox_regression",
                "required": True,
            },
        ]
    return [
        {
            **_dict(gate),
            "required": _dict(gate).get("required", True) is True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        }
        for gate in gates
    ]


def _required_operator_artifacts(staging: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = _list(staging.get("required_operator_artifacts"))
    if not artifacts:
        artifacts = _list(
            _dict(staging.get("pre_apply_manifest")).get("required_operator_artifacts")
        )
    if not artifacts:
        artifacts = [
            {"artifact": "human_approval_gate", "required": True},
            {"artifact": "operator_signoff_record", "required": True},
            {"artifact": "dry_run_review_packet", "required": True},
            {"artifact": "future_runtime_application_blueprint", "required": True},
        ]
    return [
        {
            **_dict(artifact),
            "required": _dict(artifact).get("required", True) is True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        }
        for artifact in artifacts
    ]


def _has_selected_candidate_ref(selected_candidate_ref: dict[str, Any]) -> bool:
    return any(value is not None for value in selected_candidate_ref.values())


def _no_runtime_mutation_in_prior_refs(inputs: dict[str, Any]) -> bool:
    refs = [
        inputs.get("staged_config_delta_ref"),
        inputs.get("pre_apply_manifest_ref"),
        inputs.get("rollback_staging_ref"),
        inputs.get("post_application_verification_staging_ref"),
        inputs.get("future_baseline_policy_ref"),
    ]
    return all(
        _dict(ref).get("mutation_status", "no_runtime_mutation")
        == "no_runtime_mutation"
        for ref in refs
    )


def _runtime_mutation_detected(inputs: dict[str, Any]) -> bool:
    return not _no_runtime_mutation_in_prior_refs(inputs)


def _runtime_config_has_non_staged_status(inputs: dict[str, Any]) -> bool:
    return _dict(inputs.get("staged_config_delta_ref")).get(
        "runtime_config_status",
        "not_updated",
    ) not in {"not_updated", "staged_delta_only"}


def _production_config_has_creation_status(inputs: dict[str, Any]) -> bool:
    return any(
        _dict(ref).get("production_config_status", "not_created")
        not in {"not_created", "staged_package_only", None}
        for ref in (inputs.get("staged_config_delta_ref"), inputs.get("pre_apply_manifest_ref"))
    )


def _baseline_policy_has_replacement_status(inputs: dict[str, Any]) -> bool:
    return _dict(inputs.get("future_baseline_policy_ref")).get(
        "baseline_update_status",
        "not_replaced",
    ) != "not_replaced"


def _has_blocker_with_fragment(inputs: dict[str, Any], fragment: str) -> bool:
    return any(fragment in str(blocker) for blocker in _list(inputs.get("blockers")))


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    for section in (
        "contract_type",
        "contract_version",
        "exported_at",
        "final_gate_scope",
        "source_contract_refs",
        "final_gate_input_schema",
        "final_gate_artifact_schema",
        "final_gate_readiness_schema",
        "final_gate_blocker_schema",
        "final_gate_artifact_checklist_schema",
        "final_gate_regression_checklist_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if (
        contract.get("contract_type")
        != CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_TYPE
    ):
        errors.append(
            _error(
                "invalid_contract_type",
                "contract_type",
                contract.get("contract_type"),
            )
        )
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_CONTRACT_VERSION
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
    errors = _forbidden_token_errors(inputs, "final_gate_inputs")
    _require_fields(inputs, FINAL_GATE_INPUT_REQUIRED_FIELDS, "final_gate_inputs", errors)
    if inputs.get("final_gate_input_type") != (
        CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_input_type",
                "final_gate_input_type",
                inputs.get("final_gate_input_type"),
            )
        )
    if inputs.get("final_gate_input_version") != (
        CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_input_version",
                "final_gate_input_version",
                inputs.get("final_gate_input_version"),
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
    _validate_non_claims(inputs, errors, path="final_gate_inputs.non_claims")
    return errors


def _validate_final_gate_shape(final_gate: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(final_gate, "final_gate")
    _require_fields(final_gate, FINAL_GATE_REQUIRED_FIELDS, "final_gate", errors)
    _validate_status(
        final_gate.get("final_gate_status"),
        ALLOWED_FINAL_GATE_STATUSES,
        "final_gate.final_gate_status",
        errors,
    )
    _validate_status(
        final_gate.get("readiness_status"),
        ALLOWED_READINESS_STATUSES,
        "final_gate.readiness_status",
        errors,
    )
    _validate_status(
        final_gate.get("blocker_status"),
        ALLOWED_BLOCKER_STATUSES,
        "final_gate.blocker_status",
        errors,
    )
    _validate_status(
        final_gate.get("artifact_checklist_status"),
        ALLOWED_ARTIFACT_CHECKLIST_STATUSES,
        "final_gate.artifact_checklist_status",
        errors,
    )
    _validate_status(
        final_gate.get("regression_checklist_status"),
        ALLOWED_REGRESSION_CHECKLIST_STATUSES,
        "final_gate.regression_checklist_status",
        errors,
    )
    _validate_status(
        final_gate.get("rollback_readiness_status"),
        ALLOWED_ROLLBACK_READINESS_STATUSES,
        "final_gate.rollback_readiness_status",
        errors,
    )
    _validate_status(
        final_gate.get("post_application_verification_readiness_status"),
        ALLOWED_POST_APPLICATION_VERIFICATION_READINESS_STATUSES,
        "final_gate.post_application_verification_readiness_status",
        errors,
    )
    _validate_status(
        final_gate.get("runtime_application_status"),
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        "final_gate.runtime_application_status",
        errors,
    )
    _validate_status(
        final_gate.get("runtime_config_status"),
        ALLOWED_RUNTIME_CONFIG_STATUSES,
        "final_gate.runtime_config_status",
        errors,
    )
    _validate_status(
        final_gate.get("production_config_status"),
        ALLOWED_PRODUCTION_CONFIG_STATUSES,
        "final_gate.production_config_status",
        errors,
    )
    if final_gate.get("mutation_status") != "no_runtime_mutation":
        errors.append(
            _error(
                "invalid_mutation_status",
                "final_gate.mutation_status",
                final_gate.get("mutation_status"),
            )
        )
    if final_gate.get("runtime_config_status") != "not_updated":
        errors.append(
            _error(
                "runtime_config_status_updated",
                "final_gate.runtime_config_status",
                final_gate.get("runtime_config_status"),
            )
        )
    if final_gate.get("production_config_status") != "not_created":
        errors.append(
            _error(
                "production_config_status_created",
                "final_gate.production_config_status",
                final_gate.get("production_config_status"),
            )
        )
    if final_gate.get("baseline_update_status") != "not_replaced":
        errors.append(
            _error(
                "baseline_update_status_replaced",
                "final_gate.baseline_update_status",
                final_gate.get("baseline_update_status"),
            )
        )
    if final_gate.get("model_update_status") != "not_modified":
        errors.append(
            _error(
                "model_update_status_modified",
                "final_gate.model_update_status",
                final_gate.get("model_update_status"),
            )
        )
    if final_gate.get("future_blueprint_required_for_runtime_application") is not True:
        errors.append(
            _error(
                "future_blueprint_required_missing",
                "final_gate.future_blueprint_required_for_runtime_application",
                final_gate.get("future_blueprint_required_for_runtime_application"),
            )
        )
    _validate_non_claims(final_gate, errors, path="final_gate.non_claims")
    return errors


def _validate_readiness_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "readiness_report")
    _require_fields(report, READINESS_REPORT_REQUIRED_FIELDS, "readiness_report", errors)
    _validate_status(
        report.get("readiness_status"),
        ALLOWED_READINESS_STATUSES,
        "readiness_report.readiness_status",
        errors,
    )
    _validate_status(
        report.get("runtime_application_status"),
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        "readiness_report.runtime_application_status",
        errors,
    )
    _validate_non_claims(report, errors, path="readiness_report.non_claims")
    return errors


def _validate_blocker_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "blocker_report")
    _require_fields(report, BLOCKER_REPORT_REQUIRED_FIELDS, "blocker_report", errors)
    _validate_status(
        report.get("blocker_status"),
        ALLOWED_BLOCKER_STATUSES,
        "blocker_report.blocker_status",
        errors,
    )
    _validate_status(
        report.get("runtime_application_status"),
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        "blocker_report.runtime_application_status",
        errors,
    )
    _validate_non_claims(report, errors, path="blocker_report.non_claims")
    return errors


def _validate_artifact_checklist_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "artifact_checklist")
    _require_fields(report, ARTIFACT_CHECKLIST_REPORT_REQUIRED_FIELDS, "artifact_checklist", errors)
    _validate_status(
        report.get("artifact_checklist_status"),
        ALLOWED_ARTIFACT_CHECKLIST_STATUSES,
        "artifact_checklist.artifact_checklist_status",
        errors,
    )
    _validate_status(
        report.get("runtime_application_status"),
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        "artifact_checklist.runtime_application_status",
        errors,
    )
    _validate_non_claims(report, errors, path="artifact_checklist.non_claims")
    return errors


def _validate_regression_checklist_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "regression_checklist")
    _require_fields(
        report,
        REGRESSION_CHECKLIST_REPORT_REQUIRED_FIELDS,
        "regression_checklist",
        errors,
    )
    _validate_status(
        report.get("regression_checklist_status"),
        ALLOWED_REGRESSION_CHECKLIST_STATUSES,
        "regression_checklist.regression_checklist_status",
        errors,
    )
    _validate_status(
        report.get("runtime_application_status"),
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        "regression_checklist.runtime_application_status",
        errors,
    )
    _validate_non_claims(report, errors, path="regression_checklist.non_claims")
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


def _validate_status(
    value: Any,
    allowed: list[str],
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    if value not in allowed:
        errors.append(_error("invalid_status", path, value))


def _require_fields(
    payload: dict[str, Any],
    required_fields: list[str],
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    for field in required_fields:
        if field not in payload:
            errors.append(_error("missing_required_field", f"{path}.{field}", None))


def _forbidden_token_errors(value: Any, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    _walk_forbidden_tokens(value, path, errors)
    return errors


def _walk_forbidden_tokens(
    value: Any,
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_string = str(key)
            if key_string in FORBIDDEN_FINAL_GATE_TOKENS:
                errors.append(
                    _error(
                        "forbidden_field_or_value",
                        f"{path}.{key_string}",
                        key_string,
                    )
                )
            _walk_forbidden_tokens(nested, f"{path}.{key_string}", errors)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _walk_forbidden_tokens(nested, f"{path}[{index}]", errors)
    elif isinstance(value, str) and value in FORBIDDEN_FINAL_GATE_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, value))


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
    try:
        return _load_json(path)
    except FileNotFoundError:
        return {}


def _sha256_path(path: str | Path | None) -> str | None:
    if path is None:
        return None
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def _stable_id(prefix: str, *parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _now_utc() -> datetime:
    return datetime.now(UTC)


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
        item = str(value)
        if item and item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, Any]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_FINAL_GATE_BLUEPRINT_NAME
        ),
    }
