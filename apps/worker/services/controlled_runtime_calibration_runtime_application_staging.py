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
    CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_application_plan import (
    SOURCE_CONTRACT_REFS as APPLICATION_PLAN_SOURCE_CONTRACT_REFS,
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

CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_TYPE = (
    "controlled_runtime_calibration_runtime_application_staging_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE = (
    "controlled_runtime_calibration_runtime_application_staging_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE = (
    "controlled_runtime_calibration_runtime_application_staging"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_TYPE = (
    "controlled_runtime_calibration_staged_config_delta"
)
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_TYPE = (
    "controlled_runtime_calibration_pre_apply_manifest"
)
CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE = (
    "controlled_runtime_calibration_staged_rollback_report"
)
CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE = (
    "controlled_runtime_calibration_staged_post_application_verification_report"
)
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_BLUEPRINT = "blueprint_60"
CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_runtime_application_staging_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_runtime_application_staging_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUTS_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_runtime_application_staging_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_runtime_application_staging_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT = (
    ".data/contracts/"
    "controlled_runtime_calibration_runtime_application_staging_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VALIDATION_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_runtime_application_staging.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_staged_config_delta.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_staged_config_delta.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_pre_apply_manifest.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_staged_rollback_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_staged_post_application_verification_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_application_plan_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION
    ),
    **dict(APPLICATION_PLAN_SOURCE_CONTRACT_REFS),
}

ALLOWED_STAGING_STATUSES = [
    "staging_artifact_created",
    "staging_artifact_created_with_warnings",
    "staging_blocked_missing_application_plan",
    "staging_blocked_missing_human_approval_gate",
    "staging_blocked_missing_dry_run_review_packet",
    "staging_blocked_missing_change_request",
    "staging_blocked_missing_candidate_config",
    "staging_blocked_missing_rollback_plan",
    "staging_blocked_missing_pre_apply_gate",
    "staging_blocked_missing_post_application_verification_plan",
    "staging_blocked_missing_regression_gate",
    "staging_blocked_unresolved_blockers",
    "staging_blocked_breaking_structural_change",
    "staging_informational_only",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "staged_not_applied",
    "not_applied",
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
ALLOWED_STAGED_CONFIG_DELTA_STATUSES = [
    "staged_for_future_blueprint",
    "staged_with_warnings",
    "staged_blocked_missing_current_settings",
    "staged_blocked_missing_candidate_settings",
    "staged_blocked_invalid_scope",
    "staged_informational_only",
    "not_applicable",
]
ALLOWED_PRE_APPLY_MANIFEST_STATUSES = [
    "pre_apply_manifest_defined",
    "pre_apply_manifest_incomplete",
    "pre_apply_manifest_blocked",
    "not_applicable",
]
ALLOWED_ROLLBACK_STAGING_STATUSES = [
    "rollback_staging_record_defined",
    "rollback_staging_record_incomplete",
    "rollback_staging_record_blocked",
    "rollback_not_executed",
    "not_applicable",
]
ALLOWED_POST_APPLICATION_VERIFICATION_STAGING_STATUSES = [
    "post_application_verification_staged",
    "post_application_verification_staging_incomplete",
    "post_application_verification_staging_blocked",
    "post_application_verification_not_executed",
    "not_applicable",
]
ALLOWED_FUTURE_BASELINE_STAGING_POLICY_STATUSES = [
    "future_baseline_candidate_staging_policy_defined",
    "future_baseline_candidate_staging_policy_incomplete",
    "future_baseline_candidate_staging_policy_blocked",
    "baseline_update_not_performed",
    "not_applicable",
]

STAGING_INPUT_REQUIRED_FIELDS = [
    "staging_input_id",
    "staging_input_type",
    "staging_input_version",
    "generated_at",
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
    "current_threshold",
    "current_smoothing_window",
    "current_hysteresis_settings",
    "staged_candidate_threshold",
    "staged_candidate_smoothing_window",
    "staged_candidate_hysteresis_settings",
    "operator_signoff_ref",
    "pre_apply_gate_context",
    "rollback_context",
    "post_application_verification_context",
    "future_baseline_policy_context",
    "warnings",
    "non_claims",
]
STAGING_REQUIRED_FIELDS = [
    "staging_id",
    "staging_type",
    "staging_version",
    "generated_at",
    "source_staging_input_path",
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
    "staged_config_delta",
    "pre_apply_manifest",
    "rollback_staging_record",
    "post_application_verification_staging_record",
    "future_baseline_candidate_staging_policy",
    "staging_status",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "runtime_config_status",
    "baseline_update_status",
    "model_update_status",
    "future_blueprint_required_for_runtime_application",
    "required_regression_gates",
    "required_operator_artifacts",
    "blockers",
    "warnings",
    "non_claims",
]
STAGED_CONFIG_DELTA_REQUIRED_FIELDS = [
    "staged_config_delta_id",
    "staged_config_delta_type",
    "staged_config_delta_version",
    "generated_at",
    "source_staging_id",
    "current_settings",
    "staged_candidate_settings",
    "delta_fields",
    "delta_status",
    "runtime_application_status",
    "mutation_status",
    "runtime_config_status",
    "production_config_status",
    "warnings",
    "non_claims",
]
PRE_APPLY_MANIFEST_REQUIRED_FIELDS = [
    "pre_apply_manifest_id",
    "pre_apply_manifest_type",
    "pre_apply_manifest_version",
    "generated_at",
    "source_staging_id",
    "required_artifacts",
    "required_regression_gates",
    "required_operator_artifacts",
    "required_model_asset_checks",
    "required_no_mutation_checks",
    "required_no_baseline_replacement_checks",
    "manifest_status",
    "warnings",
    "non_claims",
]
ROLLBACK_STAGING_REQUIRED_FIELDS = [
    "rollback_staging_id",
    "rollback_staging_type",
    "rollback_staging_version",
    "generated_at",
    "source_staging_id",
    "rollback_scope",
    "rollback_target_settings",
    "rollback_trigger_conditions",
    "rollback_steps_for_future_blueprint",
    "rollback_verification_gates",
    "rollback_artifact_refs",
    "rollback_staging_status",
    "runtime_application_status",
    "mutation_status",
    "non_claims",
]
POST_APPLICATION_VERIFICATION_STAGING_REQUIRED_FIELDS = [
    "post_application_verification_staging_id",
    "post_application_verification_staging_type",
    "post_application_verification_staging_version",
    "generated_at",
    "source_staging_id",
    "verification_scope",
    "required_regression_gates",
    "required_replay_checks",
    "required_post_application_review_packet",
    "required_operator_review_after_application",
    "required_rollback_readiness_check",
    "future_baseline_candidate_conditions",
    "verification_staging_status",
    "non_claims",
]
FUTURE_BASELINE_STAGING_POLICY_REQUIRED_FIELDS = [
    "baseline_not_replaced_in_this_blueprint",
    "future_baseline_candidate_not_created_in_this_blueprint",
    "future_baseline_candidate_may_be_considered_only_after_runtime_application",
    "future_baseline_candidate_requires_post_application_review",
    "future_baseline_candidate_requires_regression_gates",
    "future_baseline_candidate_requires_human_review",
    "future_baseline_candidate_not_truth",
    "future_baseline_policy_status",
]

NON_CLAIMS = {
    "staging_artifact_is_not_truth": True,
    "staging_artifact_is_not_accuracy_scoring": True,
    "staging_artifact_is_not_runtime_calibration": True,
    "staging_artifact_is_not_runtime_application": True,
    "staged_config_delta_is_not_runtime_config": True,
    "staged_config_delta_is_not_production_config": True,
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
    "controlled_runtime_application_staging": True,
    "staged_config_delta": True,
    "staged_not_applied": True,
    "future_blueprint_required_for_runtime_application": True,
    "no_runtime_mutation": True,
    "runtime_application_status_staged_not_applied": True,
    "runtime_config_not_updated": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "model_weights_not_modified": True,
    "pre_apply_manifest": True,
    "rollback_staging_record": True,
    "post_application_verification_staging_record": True,
    "staging_artifact_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "review_support_only": True,
    "staging_artifact_only": True,
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
FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS = {
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


def export_controlled_runtime_calibration_runtime_application_staging_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_EXPORTED_AT
    )
    contract = _contract_payload(exported_at=exported_at)
    errors = _validate_contract_shape(contract)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_VERSION
        ),
        "contract": contract,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_controlled_runtime_calibration_runtime_application_staging_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
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
    source_candidate_config_freeze_path: str | Path = (
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
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_result(
            status="invalid_runtime_application_staging_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE
            ),
            result_key="staging_inputs_output",
        )

    source_payloads = {
        "application_plan": _load_optional_json(source_application_plan_path),
        "human_approval_gate": _load_optional_json(source_human_approval_gate_path),
        "dry_run_review_packet": _load_optional_json(
            source_dry_run_review_packet_path
        ),
        "dry_run_execution_report": _load_optional_json(
            source_dry_run_execution_report_path
        ),
        "change_request": _load_optional_json(source_change_request_path),
        "candidate_config_freeze": _load_optional_json(
            source_candidate_config_freeze_path
        ),
        "manual_approval_packet": _load_optional_json(
            source_manual_approval_packet_path
        ),
        "decision_packet": _load_optional_json(source_decision_packet_path),
        "phase_freeze": _load_optional_json(source_phase_freeze_path),
        "gameplay_gate_regression_baseline": _load_optional_json(
            source_gameplay_gate_regression_baseline_path
        ),
        "calibration_sandbox_baseline": _load_optional_json(
            source_calibration_sandbox_baseline_path
        ),
    }
    application_plan = source_payloads["application_plan"]
    current_settings = _dict(application_plan.get("current_settings"))
    staged_candidate_settings = _staged_candidate_settings(
        _dict(application_plan.get("proposed_candidate_settings"))
    )
    selected_candidate_ref = _dict(
        application_plan.get("selected_candidate_config_ref")
    )
    inputs = {
        "staging_input_id": _stable_id(
            "controlled_runtime_calibration_runtime_application_staging_inputs_v1",
            _path_string(source_application_plan_path),
            application_plan.get("application_plan_id"),
            selected_candidate_ref,
            _sha256_path(model_asset_path),
        ),
        "staging_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE
        ),
        "staging_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_plan_path": str(Path(source_application_plan_path)),
        "source_human_approval_gate_path": _source_path_from_plan(
            application_plan,
            "source_human_approval_gate_path",
            source_human_approval_gate_path,
        ),
        "source_dry_run_review_packet_path": _source_path_from_plan(
            application_plan,
            "source_dry_run_review_packet_path",
            source_dry_run_review_packet_path,
        ),
        "source_dry_run_execution_report_path": _source_path_from_plan(
            application_plan,
            "source_dry_run_execution_report_path",
            source_dry_run_execution_report_path,
        ),
        "source_change_request_path": _source_path_from_plan(
            application_plan,
            "source_change_request_path",
            source_change_request_path,
        ),
        "source_candidate_config_freeze_path": str(
            Path(source_candidate_config_freeze_path)
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
        "source_application_plan_id": application_plan.get("application_plan_id"),
        "source_human_approval_gate_id": source_payloads["human_approval_gate"].get(
            "approval_gate_id"
        ),
        "source_dry_run_review_packet_id": source_payloads[
            "dry_run_review_packet"
        ].get("review_packet_id"),
        "source_dry_run_execution_report_id": source_payloads[
            "dry_run_execution_report"
        ].get("dry_run_id"),
        "change_request_id": source_payloads["change_request"].get(
            "change_request_id"
        ),
        "candidate_config_freeze_id": source_payloads[
            "candidate_config_freeze"
        ].get("candidate_config_freeze_id"),
        "manual_approval_packet_id": source_payloads[
            "manual_approval_packet"
        ].get("manual_approval_packet_id"),
        "selected_candidate_config_ref": selected_candidate_ref,
        "model_asset_ref": str(Path(model_asset_path)),
        "model_asset_sha256": _sha256_path(model_asset_path),
        "current_runtime_settings_ref": current_runtime_settings_ref,
        "current_threshold": current_settings.get("current_threshold"),
        "current_smoothing_window": current_settings.get("current_smoothing_window"),
        "current_hysteresis_settings": _dict(
            current_settings.get("current_hysteresis_settings")
        ),
        "staged_candidate_threshold": staged_candidate_settings.get(
            "staged_candidate_threshold"
        ),
        "staged_candidate_smoothing_window": staged_candidate_settings.get(
            "staged_candidate_smoothing_window"
        ),
        "staged_candidate_hysteresis_settings": _dict(
            staged_candidate_settings.get("staged_candidate_hysteresis_settings")
        ),
        "current_settings": current_settings,
        "staged_candidate_settings": staged_candidate_settings,
        "operator_signoff_ref": _operator_signoff_ref(application_plan),
        "pre_apply_gate_context": _dict(application_plan.get("pre_application_gate")),
        "rollback_context": _dict(application_plan.get("rollback_plan")),
        "post_application_verification_context": _dict(
            application_plan.get("post_application_verification_plan")
        ),
        "future_baseline_policy_context": _dict(
            application_plan.get("future_baseline_candidate_policy")
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_presence": _source_artifact_presence(source_payloads),
        "missing_source_refs": _missing_source_refs(source_payloads),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_inputs_shape(inputs)
    if validation_errors:
        return _failed_result(
            status="invalid_runtime_application_staging_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE
            ),
            result_key="staging_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "staging_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE
        ),
        "staging_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_VERSION
        ),
        "staging_input_id": inputs["staging_input_id"],
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "future_blueprint_required_for_runtime_application": True,
        "staging_inputs": inputs,
        "warnings": inputs["warnings"],
    }
    _write_json_if_requested(output_path, inputs, result, "staging_inputs_output")
    return result


def validate_controlled_runtime_calibration_runtime_application_staging_inputs(
    *,
    staging_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(staging_inputs_path, "staging_inputs", errors)
    if inputs:
        errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        ok=not errors,
        validation_type=(
            "controlled_runtime_calibration_runtime_application_staging_inputs_validation"
        ),
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=staging_inputs_path,
        payload_type=inputs.get("staging_input_type") if inputs else None,
        payload_version=inputs.get("staging_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_runtime_application_staging(
    *,
    staging_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_runtime_application_staging_inputs(
        staging_inputs_path=staging_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_runtime_application_staging_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
            ),
            result_key="staging_output",
        )

    inputs = _dict(_load_json(staging_inputs_path, label="staging_inputs").get("data"))
    application_plan = _load_optional_json(inputs.get("source_application_plan_path"))
    current_settings = _dict(inputs.get("current_settings"))
    staged_candidate_settings = _dict(inputs.get("staged_candidate_settings"))
    selected_candidate_ref = _dict(inputs.get("selected_candidate_config_ref"))
    staging_id = _stable_id(
        "controlled_runtime_calibration_runtime_application_staging_v1",
        inputs.get("staging_input_id"),
        application_plan.get("application_plan_id"),
        selected_candidate_ref,
        current_settings,
        staged_candidate_settings,
    )
    staged_config_delta = _staged_config_delta(
        source_staging_id=staging_id,
        current_settings=current_settings,
        staged_candidate_settings=staged_candidate_settings,
        generated_at=generated_at,
    )
    pre_apply_manifest = _pre_apply_manifest(
        source_staging_id=staging_id,
        inputs=inputs,
        application_plan=application_plan,
        generated_at=generated_at,
    )
    rollback_staging_record = _rollback_staging_record(
        source_staging_id=staging_id,
        inputs=inputs,
        application_plan=application_plan,
        current_settings=current_settings,
        generated_at=generated_at,
    )
    post_application_verification_staging_record = (
        _post_application_verification_staging_record(
            source_staging_id=staging_id,
            application_plan=application_plan,
            generated_at=generated_at,
        )
    )
    future_baseline_candidate_staging_policy = (
        _future_baseline_candidate_staging_policy()
    )
    blockers = sorted(
        set(_list(application_plan.get("blockers")))
        | set(_list(pre_apply_manifest.get("blockers")))
    )
    staging_status = _staging_status(
        inputs=inputs,
        application_plan=application_plan,
        staged_config_delta_status=staged_config_delta["delta_status"],
        pre_apply_manifest_status=pre_apply_manifest["manifest_status"],
        rollback_staging_status=rollback_staging_record["rollback_staging_status"],
        verification_staging_status=post_application_verification_staging_record[
            "verification_staging_status"
        ],
        blockers=blockers,
    )
    staging = {
        "staging_id": staging_id,
        "staging_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
        ),
        "staging_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_input_path": str(Path(staging_inputs_path)),
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
        "selected_candidate_config_ref": selected_candidate_ref,
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "current_settings": current_settings,
        "staged_candidate_settings": staged_candidate_settings,
        "staged_config_delta": staged_config_delta,
        "pre_apply_manifest": pre_apply_manifest,
        "rollback_staging_record": rollback_staging_record,
        "post_application_verification_staging_record": (
            post_application_verification_staging_record
        ),
        "future_baseline_candidate_staging_policy": (
            future_baseline_candidate_staging_policy
        ),
        "staging_status": staging_status,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "runtime_config_status": "not_updated",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "required_regression_gates": _staged_regression_gates(
            application_plan.get("required_regression_gates")
        ),
        "required_operator_artifacts": _staged_operator_artifacts(
            application_plan.get("required_operator_artifacts")
        ),
        "blockers": blockers,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(inputs.get("warnings")),
            **dict(WARNINGS),
            "runtime_application_status_staged_not_applied": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_staging_shape(staging)
    if validation_errors:
        return _failed_result(
            status="invalid_runtime_application_staging",
            errors=validation_errors,
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
            ),
            result_key="staging_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "staging_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
        ),
        "staging_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "staging_id": staging["staging_id"],
        "staging_status": staging["staging_status"],
        "staged_config_delta_status": staging["staged_config_delta"][
            "delta_status"
        ],
        "pre_apply_manifest_status": staging["pre_apply_manifest"][
            "manifest_status"
        ],
        "rollback_staging_status": staging["rollback_staging_record"][
            "rollback_staging_status"
        ],
        "post_application_verification_staging_status": staging[
            "post_application_verification_staging_record"
        ]["verification_staging_status"],
        "future_baseline_policy_status": staging[
            "future_baseline_candidate_staging_policy"
        ]["future_baseline_policy_status"],
        "runtime_application_status": staging["runtime_application_status"],
        "mutation_status": staging["mutation_status"],
        "runtime_config_status": staging["runtime_config_status"],
        "production_config_status": staging["production_config_status"],
        "baseline_update_status": staging["baseline_update_status"],
        "model_update_status": staging["model_update_status"],
        "future_blueprint_required_for_runtime_application": staging[
            "future_blueprint_required_for_runtime_application"
        ],
        "staging": staging,
        "warnings": staging["warnings"],
    }
    _write_json_if_requested(output_path, staging, result, "staging_output")
    return result


def validate_controlled_runtime_calibration_runtime_application_staging(
    *,
    staging_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    staging = _load_required_json(staging_path, "staging", errors)
    if staging:
        errors.extend(_validate_staging_shape(staging))
    result = _validation_result(
        ok=not errors,
        validation_type=(
            "controlled_runtime_calibration_runtime_application_staging_validation"
        ),
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=staging_path,
        payload_type=staging.get("staging_type") if staging else None,
        payload_version=staging.get("staging_version") if staging else None,
        errors=errors,
        extra={
            "staging_status": staging.get("staging_status") if staging else None,
            "runtime_application_status": staging.get("runtime_application_status")
            if staging
            else None,
            "mutation_status": staging.get("mutation_status") if staging else None,
            "runtime_config_status": staging.get("runtime_config_status")
            if staging
            else None,
            "production_config_status": staging.get("production_config_status")
            if staging
            else None,
            "future_blueprint_required_for_runtime_application": staging.get(
                "future_blueprint_required_for_runtime_application"
            )
            if staging
            else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_staged_config_delta(
    *,
    staging_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_runtime_application_staging(
        staging_path=staging_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_runtime_application_staging",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_TYPE,
            result_key="staged_config_delta_output",
        )
    staging = _dict(_load_json(staging_path, label="staging").get("data"))
    staged_delta = {
        **_dict(staging.get("staged_config_delta")),
        "generated_at": generated_at.isoformat(),
        "source_staging_path": str(Path(staging_path)),
    }
    errors = _validate_staged_config_delta_shape(staged_delta)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_staged_config_delta",
        "staged_config_delta_type": CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_TYPE,
        "staged_config_delta_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "staged_config_delta_id": staged_delta.get("staged_config_delta_id"),
        "delta_status": staged_delta.get("delta_status"),
        "runtime_application_status": staged_delta.get("runtime_application_status"),
        "mutation_status": staged_delta.get("mutation_status"),
        "runtime_config_status": staged_delta.get("runtime_config_status"),
        "production_config_status": staged_delta.get("production_config_status"),
        "error_count": len(errors),
        "errors": errors,
        "staged_config_delta": staged_delta,
        "warnings": _dict(staged_delta.get("warnings")),
    }
    _write_json_if_requested(
        output_path,
        staged_delta,
        result,
        "staged_config_delta_output",
    )
    return result


def validate_controlled_runtime_calibration_staged_config_delta(
    *,
    staged_config_delta_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    staged_delta = _load_required_json(
        staged_config_delta_path,
        "staged_config_delta",
        errors,
    )
    if staged_delta:
        errors.extend(_validate_staged_config_delta_shape(staged_delta))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_staged_config_delta_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=staged_config_delta_path,
        payload_type=staged_delta.get("staged_config_delta_type")
        if staged_delta
        else None,
        payload_version=staged_delta.get("staged_config_delta_version")
        if staged_delta
        else None,
        errors=errors,
        extra={
            "delta_status": staged_delta.get("delta_status")
            if staged_delta
            else None,
            "runtime_application_status": staged_delta.get(
                "runtime_application_status"
            )
            if staged_delta
            else None,
            "mutation_status": staged_delta.get("mutation_status")
            if staged_delta
            else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_pre_apply_manifest(
    *,
    staging_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    staging = _validated_staging_or_failed(
        staging_path=staging_path,
        contract_path=contract_path,
        output_path=output_path,
        result_key="pre_apply_manifest_output",
        payload_type=CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_TYPE,
        generated_at=generated_at,
    )
    if "failed_result" in staging:
        return _dict(staging["failed_result"])
    manifest = {
        **_dict(staging.get("pre_apply_manifest")),
        "generated_at": generated_at.isoformat(),
        "source_staging_path": str(Path(staging_path)),
    }
    errors = _validate_pre_apply_manifest_shape(manifest)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_pre_apply_manifest",
        "manifest_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_TYPE,
        "manifest_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "pre_apply_manifest_id": manifest.get("pre_apply_manifest_id"),
        "manifest_status": manifest.get("manifest_status"),
        "error_count": len(errors),
        "errors": errors,
        "pre_apply_manifest": manifest,
        "warnings": _dict(manifest.get("warnings")),
    }
    _write_json_if_requested(output_path, manifest, result, "pre_apply_manifest_output")
    return result


def build_controlled_runtime_calibration_staged_rollback_report(
    *,
    staging_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    staging = _validated_staging_or_failed(
        staging_path=staging_path,
        contract_path=contract_path,
        output_path=output_path,
        result_key="staged_rollback_report_output",
        payload_type=CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE,
        generated_at=generated_at,
    )
    if "failed_result" in staging:
        return _dict(staging["failed_result"])
    rollback = {
        **_dict(staging.get("rollback_staging_record")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE,
        "report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_path": str(Path(staging_path)),
    }
    errors = _validate_rollback_staging_shape(rollback)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_staged_rollback_report",
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE,
        "report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "rollback_staging_id": rollback.get("rollback_staging_id"),
        "rollback_staging_status": rollback.get("rollback_staging_status"),
        "runtime_application_status": rollback.get("runtime_application_status"),
        "mutation_status": rollback.get("mutation_status"),
        "error_count": len(errors),
        "errors": errors,
        "rollback_staging_record": rollback,
        "warnings": _dict(rollback.get("warnings")),
    }
    _write_json_if_requested(
        output_path,
        rollback,
        result,
        "staged_rollback_report_output",
    )
    return result


def build_controlled_runtime_calibration_staged_post_application_verification_report(
    *,
    staging_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    staging = _validated_staging_or_failed(
        staging_path=staging_path,
        contract_path=contract_path,
        output_path=output_path,
        result_key="staged_post_application_verification_report_output",
        payload_type=(
            CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE
        ),
        generated_at=generated_at,
    )
    if "failed_result" in staging:
        return _dict(staging["failed_result"])
    verification = {
        **_dict(staging.get("post_application_verification_staging_record")),
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE
        ),
        "report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_path": str(Path(staging_path)),
    }
    errors = _validate_post_application_verification_staging_shape(verification)
    result = {
        "ok": not errors,
        "status": "completed"
        if not errors
        else "invalid_staged_post_application_verification_report",
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE
        ),
        "report_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "post_application_verification_staging_id": verification.get(
            "post_application_verification_staging_id"
        ),
        "verification_staging_status": verification.get(
            "verification_staging_status"
        ),
        "error_count": len(errors),
        "errors": errors,
        "post_application_verification_staging_record": verification,
        "warnings": _dict(verification.get("warnings")),
    }
    _write_json_if_requested(
        output_path,
        verification,
        result,
        "staged_post_application_verification_report_output",
    )
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "staging_scope": {
            "purpose": "controlled_runtime_application_staging",
            "consumes_application_plan": True,
            "consumes_human_approval_gate": True,
            "consumes_dry_run_review_packet": True,
            "consumes_dry_run_execution_report": True,
            "consumes_controlled_change_request": True,
            "creates_staged_application_package": True,
            "creates_staged_config_delta": True,
            "creates_pre_apply_manifest": True,
            "creates_rollback_staging_record": True,
            "creates_post_application_verification_staging_record": True,
            "creates_future_baseline_candidate_staging_policy": True,
            "future_blueprint_required_for_runtime_application": True,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "updates_runtime_configuration": False,
            "creates_deployable_configuration": False,
            "creates_production_configuration": False,
            "updates_model_weights": False,
            "mutates_regression_baselines": False,
            "automatic_approval_allowed": False,
            "automatic_rejection_allowed": False,
            "calculates_classifier_correctness": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "staging_input_schema": {
            "staging_input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE
            ),
            "staging_input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_VERSION
            ),
            "required_fields": list(STAGING_INPUT_REQUIRED_FIELDS),
        },
        "staging_artifact_schema": {
            "staging_type": (
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
            ),
            "staging_version": (
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
            ),
            "required_fields": list(STAGING_REQUIRED_FIELDS),
            "allowed_staging_statuses": list(ALLOWED_STAGING_STATUSES),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_runtime_config_statuses": list(ALLOWED_RUNTIME_CONFIG_STATUSES),
            "allowed_production_config_statuses": list(
                ALLOWED_PRODUCTION_CONFIG_STATUSES
            ),
            "required_runtime_application_status": "staged_not_applied",
            "required_mutation_status": "no_runtime_mutation",
            "required_runtime_config_status": "not_updated",
            "required_production_config_status": "not_created",
            "required_baseline_update_status": "not_replaced",
            "required_model_update_status": "not_modified",
            "future_blueprint_required_for_runtime_application": True,
        },
        "staged_config_delta_schema": {
            "staged_config_delta_type": (
                CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_TYPE
            ),
            "staged_config_delta_version": (
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
            ),
            "required_fields": list(STAGED_CONFIG_DELTA_REQUIRED_FIELDS),
            "allowed_staged_config_delta_statuses": list(
                ALLOWED_STAGED_CONFIG_DELTA_STATUSES
            ),
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
            "runtime_config_status": "not_updated",
            "production_config_status": "not_created",
            "not_runtime_config": True,
            "not_production_config": True,
        },
        "pre_apply_manifest_schema": {
            "pre_apply_manifest_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_TYPE,
            "pre_apply_manifest_version": (
                CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
            ),
            "required_fields": list(PRE_APPLY_MANIFEST_REQUIRED_FIELDS),
            "allowed_manifest_statuses": list(ALLOWED_PRE_APPLY_MANIFEST_STATUSES),
        },
        "rollback_staging_schema": {
            "rollback_staging_type": (
                CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE
            ),
            "required_fields": list(ROLLBACK_STAGING_REQUIRED_FIELDS),
            "allowed_rollback_staging_statuses": list(
                ALLOWED_ROLLBACK_STAGING_STATUSES
            ),
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "post_application_verification_staging_schema": {
            "post_application_verification_staging_type": (
                CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE
            ),
            "required_fields": list(
                POST_APPLICATION_VERIFICATION_STAGING_REQUIRED_FIELDS
            ),
            "allowed_post_application_verification_staging_statuses": list(
                ALLOWED_POST_APPLICATION_VERIFICATION_STAGING_STATUSES
            ),
        },
        "future_baseline_candidate_staging_schema": {
            "required_fields": list(FUTURE_BASELINE_STAGING_POLICY_REQUIRED_FIELDS),
            "allowed_future_baseline_staging_policy_statuses": list(
                ALLOWED_FUTURE_BASELINE_STAGING_POLICY_STATUSES
            ),
            "baseline_update_status": "not_replaced",
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_staging_input_shape": True,
            "validate_staging_artifact_shape": True,
            "validate_staged_config_delta_shape": True,
            "validate_pre_apply_manifest_shape": True,
            "validate_rollback_staging_record_shape": True,
            "validate_post_application_verification_staging_record_shape": True,
            "validate_future_baseline_candidate_staging_policy_shape": True,
            "validate_allowed_statuses_and_scopes": True,
            "validate_required_no_mutation_statuses": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_fields_and_values": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_outcomes": True,
            "does_not_calculate_classifier_correctness": True,
            "does_not_auto_label_segments": True,
            "does_not_alter_thresholds": True,
            "does_not_alter_smoothing": True,
            "does_not_alter_hysteresis": True,
            "does_not_modify_existing_baselines": True,
        },
        "provenance_requirements": {
            "source_application_plan_path_recorded": True,
            "source_human_approval_gate_path_recorded": True,
            "source_dry_run_review_packet_path_recorded": True,
            "source_dry_run_execution_report_path_recorded": True,
            "source_change_request_path_recorded": True,
            "source_candidate_config_freeze_path_recorded_when_available": True,
            "source_manual_approval_packet_path_recorded_when_available": True,
            "source_decision_packet_path_recorded_when_available": True,
            "source_phase_freeze_path_recorded_when_available": True,
            "model_asset_ref_required": True,
            "model_asset_sha256_when_available": True,
            "pre_apply_manifest_required": True,
            "rollback_staging_record_required": True,
            "post_application_verification_staging_record_required": True,
            "future_baseline_candidate_staging_policy_required": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _staging_status(
    *,
    inputs: dict[str, Any],
    application_plan: dict[str, Any],
    staged_config_delta_status: str,
    pre_apply_manifest_status: str,
    rollback_staging_status: str,
    verification_staging_status: str,
    blockers: list[str],
) -> str:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    if not _source_present(source_presence, "application_plan"):
        return "staging_blocked_missing_application_plan"
    if not _source_present(source_presence, "human_approval_gate"):
        return "staging_blocked_missing_human_approval_gate"
    if not _source_present(source_presence, "dry_run_review_packet"):
        return "staging_blocked_missing_dry_run_review_packet"
    if not _source_present(source_presence, "change_request"):
        return "staging_blocked_missing_change_request"
    if not _has_selected_candidate_ref(_dict(inputs.get("selected_candidate_config_ref"))):
        if blockers:
            return "staging_blocked_unresolved_blockers"
        return "staging_blocked_missing_candidate_config"
    if _dict(application_plan.get("rollback_plan")).get("rollback_status") not in (
        "rollback_plan_defined",
        "rollback_not_executed",
    ):
        return "staging_blocked_missing_rollback_plan"
    if pre_apply_manifest_status in (
        "pre_apply_manifest_blocked",
        "pre_apply_manifest_incomplete",
    ):
        if blockers:
            return "staging_blocked_unresolved_blockers"
        return "staging_blocked_missing_pre_apply_gate"
    if verification_staging_status in (
        "post_application_verification_staging_incomplete",
        "post_application_verification_staging_blocked",
    ):
        return "staging_blocked_missing_post_application_verification_plan"
    if rollback_staging_status == "rollback_staging_record_blocked":
        return "staging_blocked_missing_rollback_plan"
    if staged_config_delta_status == "staged_blocked_missing_candidate_settings":
        if blockers:
            return "staging_blocked_unresolved_blockers"
        return "staging_blocked_missing_candidate_config"
    if staged_config_delta_status == "staged_blocked_invalid_scope":
        return "staging_blocked_breaking_structural_change"
    if _dict(application_plan.get("pre_application_gate")).get(
        "pre_application_gate_status"
    ) == "pre_application_gates_blocked":
        return "staging_blocked_unresolved_blockers"
    if blockers:
        return "staging_blocked_unresolved_blockers"
    if staged_config_delta_status == "staged_informational_only":
        return "staging_informational_only"
    if staged_config_delta_status != "staged_for_future_blueprint":
        return "staging_artifact_created_with_warnings"
    return "staging_artifact_created"


def _staged_config_delta(
    *,
    source_staging_id: str,
    current_settings: dict[str, Any],
    staged_candidate_settings: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    delta_fields = _delta_fields(current_settings, staged_candidate_settings)
    delta_status = _delta_status(
        current_settings=current_settings,
        staged_candidate_settings=staged_candidate_settings,
        delta_fields=delta_fields,
    )
    return {
        "staged_config_delta_id": _stable_id(
            "controlled_runtime_calibration_staged_config_delta_v1",
            source_staging_id,
            current_settings,
            staged_candidate_settings,
            delta_fields,
        ),
        "staged_config_delta_type": (
            CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_TYPE
        ),
        "staged_config_delta_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_id": source_staging_id,
        "current_settings": current_settings,
        "staged_candidate_settings": staged_candidate_settings,
        "delta_fields": delta_fields,
        "delta_status": delta_status,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "warnings": {
            "staged_config_delta": True,
            "staged_config_delta_is_not_runtime_config": True,
            "staged_config_delta_is_not_production_config": True,
            "runtime_application_status_staged_not_applied": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _delta_fields(
    current_settings: dict[str, Any],
    staged_candidate_settings: dict[str, Any],
) -> list[dict[str, Any]]:
    candidates = [
        ("threshold", "current_threshold", "staged_candidate_threshold"),
        (
            "smoothing_window",
            "current_smoothing_window",
            "staged_candidate_smoothing_window",
        ),
        (
            "hysteresis_settings",
            "current_hysteresis_settings",
            "staged_candidate_hysteresis_settings",
        ),
    ]
    deltas = []
    for field_name, current_key, staged_key in candidates:
        current_value = current_settings.get(current_key)
        staged_value = staged_candidate_settings.get(staged_key)
        staged_value_present = _staged_candidate_value_present(staged_value)
        deltas.append(
            {
                "field": field_name,
                "current_value": current_value,
                "staged_value": staged_value,
                "change_present": staged_value_present and staged_value != current_value,
                "runtime_application_status": "staged_not_applied",
                "mutation_status": "no_runtime_mutation",
                "runtime_config_status": "not_updated",
            }
        )
    return deltas


def _staged_candidate_value_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict | list | tuple | set):
        return bool(value)
    return True


def _delta_status(
    *,
    current_settings: dict[str, Any],
    staged_candidate_settings: dict[str, Any],
    delta_fields: list[dict[str, Any]],
) -> str:
    if not current_settings:
        return "staged_blocked_missing_current_settings"
    if not _has_staged_candidate_settings(staged_candidate_settings):
        return "staged_blocked_missing_candidate_settings"
    if any(
        _dict(staged_candidate_settings).get(key)
        for key in ("writes_runtime_configuration", "affects_regression_baselines")
    ):
        return "staged_blocked_invalid_scope"
    if any(item.get("change_present") is True for item in delta_fields):
        return "staged_for_future_blueprint"
    return "staged_informational_only"


def _pre_apply_manifest(
    *,
    source_staging_id: str,
    inputs: dict[str, Any],
    application_plan: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    plan_gate = _dict(application_plan.get("pre_application_gate"))
    plan_blockers = set(str(item) for item in _list(application_plan.get("blockers")))
    plan_missing_requirements = set(
        str(item) for item in _list(plan_gate.get("missing_requirements"))
    )
    required_artifacts = [
        _manifest_requirement(
            "application_plan_present",
            _source_present(source_presence, "application_plan"),
        ),
        _manifest_requirement(
            "human_approval_gate_present",
            _source_present(source_presence, "human_approval_gate"),
        ),
        _manifest_requirement(
            "operator_signoff_artifact_present",
            _operator_signoff_present(inputs, application_plan),
        ),
        _manifest_requirement(
            "dry_run_review_packet_present",
            _source_present(source_presence, "dry_run_review_packet"),
        ),
        _manifest_requirement(
            "dry_run_execution_report_present",
            _source_present(source_presence, "dry_run_execution_report"),
        ),
        _manifest_requirement(
            "controlled_change_request_present",
            _source_present(source_presence, "change_request"),
        ),
        _manifest_requirement(
            "candidate_config_freeze_present",
            _source_present(source_presence, "candidate_config_freeze"),
        ),
        _manifest_requirement(
            "rollback_plan_present",
            _dict(application_plan.get("rollback_plan")).get("rollback_status")
            == "rollback_plan_defined",
        ),
        _manifest_requirement(
            "post_application_verification_plan_present",
            _dict(application_plan.get("post_application_verification_plan")).get(
                "verification_status"
            )
            == "post_application_verification_plan_defined",
        ),
    ]
    required_regression_gates = _staged_regression_gates(
        application_plan.get("required_regression_gates")
    )
    required_operator_artifacts = _staged_operator_artifacts(
        application_plan.get("required_operator_artifacts")
    )
    required_model_asset_checks = [
        _manifest_requirement(
            "model_asset_hash_captured",
            bool(inputs.get("model_asset_sha256")),
        )
    ]
    required_no_mutation_checks = [
        _manifest_requirement("no_generated_exports_committed", True),
        _manifest_requirement("no_unresolved_blockers", not plan_blockers),
        _manifest_requirement(
            "no_runtime_mutation_in_prior_artifacts",
            _prior_artifacts_preserve_no_mutation(inputs),
        ),
        _manifest_requirement("future_blueprint_required", True),
    ]
    required_no_baseline_replacement_checks = [
        _manifest_requirement(
            "baseline_not_replaced",
            application_plan.get("baseline_update_status") == "not_replaced",
        )
    ]
    missing = _missing_requirements(
        required_artifacts
        + required_regression_gates
        + required_operator_artifacts
        + required_model_asset_checks
        + required_no_mutation_checks
        + required_no_baseline_replacement_checks
    )
    missing = sorted(set(missing) | plan_missing_requirements)
    blockers = sorted(plan_blockers | set(missing))
    if blockers:
        manifest_status = "pre_apply_manifest_blocked"
    elif missing:
        manifest_status = "pre_apply_manifest_incomplete"
    else:
        manifest_status = "pre_apply_manifest_defined"
    return {
        "pre_apply_manifest_id": _stable_id(
            "controlled_runtime_calibration_pre_apply_manifest_v1",
            source_staging_id,
            required_artifacts,
            required_regression_gates,
            blockers,
        ),
        "pre_apply_manifest_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_TYPE,
        "pre_apply_manifest_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_id": source_staging_id,
        "required_artifacts": required_artifacts,
        "required_regression_gates": required_regression_gates,
        "required_operator_artifacts": required_operator_artifacts,
        "required_model_asset_checks": required_model_asset_checks,
        "required_no_mutation_checks": required_no_mutation_checks,
        "required_no_baseline_replacement_checks": (
            required_no_baseline_replacement_checks
        ),
        "missing_requirements": missing,
        "blockers": blockers,
        "manifest_status": manifest_status,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "warnings": {
            "pre_apply_manifest": True,
            "runtime_application_status_staged_not_applied": True,
            "no_runtime_mutation": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _rollback_staging_record(
    *,
    source_staging_id: str,
    inputs: dict[str, Any],
    application_plan: dict[str, Any],
    current_settings: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    rollback_plan = _dict(application_plan.get("rollback_plan"))
    rollback_status = (
        "rollback_staging_record_defined"
        if rollback_plan.get("rollback_status") == "rollback_plan_defined"
        else "rollback_staging_record_incomplete"
    )
    return {
        "rollback_staging_id": _stable_id(
            "controlled_runtime_calibration_rollback_staging_v1",
            source_staging_id,
            rollback_plan,
            current_settings,
        ),
        "rollback_staging_type": (
            CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE
        ),
        "rollback_staging_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_id": source_staging_id,
        "rollback_scope": {
            **_dict(rollback_plan.get("rollback_scope")),
            "source_staging_id": source_staging_id,
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
            "future_blueprint_only": True,
        },
        "rollback_target_settings": (
            _dict(rollback_plan.get("rollback_target_settings")) or current_settings
        ),
        "rollback_trigger_conditions": _list(
            rollback_plan.get("rollback_trigger_conditions")
        )
        or [
            "operator requests rollback after separate future runtime application",
            "future post-application verification gate blocks",
            "future regression gate blocks",
            "future review packet raises blocker",
        ],
        "rollback_steps_for_future_blueprint": _list(
            rollback_plan.get("rollback_execution_steps_for_future_blueprint")
        )
        or [
            "capture pre-application runtime settings",
            "restore captured runtime settings in a separate runtime application blueprint",
            "run required regression gates",
            "build post-rollback review packet",
            "record human operator review state",
        ],
        "rollback_verification_gates": _staged_regression_gates(
            rollback_plan.get("rollback_verification_gates")
        ),
        "rollback_artifact_refs": {
            **_dict(rollback_plan.get("rollback_artifact_refs")),
            "source_application_plan_path": inputs.get("source_application_plan_path"),
            "source_staging_input_path": inputs.get("source_staging_input_path"),
        },
        "rollback_staging_status": rollback_status,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "rollback_staging_record": True,
            "rollback_not_executed": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _post_application_verification_staging_record(
    *,
    source_staging_id: str,
    application_plan: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    verification_plan = _dict(application_plan.get("post_application_verification_plan"))
    status = (
        "post_application_verification_staged"
        if verification_plan.get("verification_status")
        == "post_application_verification_plan_defined"
        else "post_application_verification_staging_incomplete"
    )
    return {
        "post_application_verification_staging_id": _stable_id(
            "controlled_runtime_calibration_post_application_verification_staging_v1",
            source_staging_id,
            verification_plan,
        ),
        "post_application_verification_staging_type": (
            CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE
        ),
        "post_application_verification_staging_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_staging_id": source_staging_id,
        "verification_scope": {
            **_dict(verification_plan.get("verification_scope")),
            "source_staging_id": source_staging_id,
            "separate_future_runtime_application_required": True,
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "required_regression_gates": _staged_regression_gates(
            verification_plan.get("required_regression_gates")
        ),
        "required_replay_checks": _list(verification_plan.get("required_replay_checks"))
        or [
            "manifest-backed multi-point replay review",
            "protected sample_point replay review",
            "gameplay segment replay review timeline check",
        ],
        "required_post_application_review_packet": bool(
            verification_plan.get("required_review_packet_after_application", True)
        ),
        "required_operator_review_after_application": bool(
            verification_plan.get("required_operator_review_after_application", True)
        ),
        "required_rollback_readiness_check": bool(
            verification_plan.get("required_rollback_readiness_check", True)
        ),
        "future_baseline_candidate_conditions": _list(
            verification_plan.get("future_baseline_candidate_conditions")
        )
        or [
            "separate future runtime application exists",
            "post-application review packet exists",
            "required regression gates pass structurally",
            "human operator review is recorded",
            "future baseline candidate remains review-only",
        ],
        "verification_staging_status": status,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "post_application_verification_staging_record": True,
            "post_application_verification_not_executed": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _future_baseline_candidate_staging_policy() -> dict[str, Any]:
    return {
        "baseline_not_replaced_in_this_blueprint": True,
        "future_baseline_candidate_not_created_in_this_blueprint": True,
        "future_baseline_candidate_may_be_considered_only_after_runtime_application": True,
        "future_baseline_candidate_requires_post_application_review": True,
        "future_baseline_candidate_requires_regression_gates": True,
        "future_baseline_candidate_requires_human_review": True,
        "future_baseline_candidate_not_truth": True,
        "future_baseline_policy_status": (
            "future_baseline_candidate_staging_policy_defined"
        ),
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "baseline_update_status": "not_replaced",
        "warnings": {
            "baseline_not_replaced": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _staged_candidate_settings(proposed_candidate_settings: dict[str, Any]) -> dict[str, Any]:
    return {
        "staged_candidate_threshold": proposed_candidate_settings.get(
            "proposed_candidate_threshold"
        ),
        "staged_candidate_smoothing_window": proposed_candidate_settings.get(
            "proposed_candidate_smoothing_window"
        ),
        "staged_candidate_hysteresis_settings": _dict(
            proposed_candidate_settings.get("proposed_candidate_hysteresis_settings")
        ),
        "candidate_type": proposed_candidate_settings.get(
            "candidate_type",
            "not_applicable",
        ),
        "candidate_source": _dict(proposed_candidate_settings.get("candidate_source")),
        "staged_not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }


def _operator_signoff_ref(application_plan: dict[str, Any]) -> dict[str, Any]:
    gate = _dict(application_plan.get("pre_application_gate"))
    operator_artifacts = _list(application_plan.get("required_operator_artifacts"))
    return {
        "operator_signoff_required": True,
        "operator_signoff_artifact_present": any(
            _dict(item).get("artifact") == "operator_signoff_record"
            for item in operator_artifacts
        ),
        "pre_application_gate_status": gate.get("pre_application_gate_status"),
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
    }


def _operator_signoff_present(
    inputs: dict[str, Any],
    application_plan: dict[str, Any],
) -> bool:
    signoff_ref = _dict(inputs.get("operator_signoff_ref"))
    if signoff_ref.get("operator_signoff_artifact_present") is True:
        return True
    return any(
        _dict(item).get("artifact") == "operator_signoff_record"
        for item in _list(application_plan.get("required_operator_artifacts"))
    )


def _has_selected_candidate_ref(selected_candidate_ref: dict[str, Any]) -> bool:
    return any(value is not None for value in selected_candidate_ref.values())


def _has_staged_candidate_settings(staged_candidate_settings: dict[str, Any]) -> bool:
    return any(
        staged_candidate_settings.get(key) is not None
        for key in (
            "staged_candidate_threshold",
            "staged_candidate_smoothing_window",
        )
    ) or bool(
        _dict(staged_candidate_settings.get("staged_candidate_hysteresis_settings"))
    )


def _staged_regression_gates(source_gates: Any) -> list[dict[str, Any]]:
    gates = _list(source_gates) or [
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
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        }
        for gate in gates
    ]


def _staged_operator_artifacts(source_artifacts: Any) -> list[dict[str, Any]]:
    artifacts = _list(source_artifacts) or [
        {"artifact": "human_approval_gate", "required": True},
        {"artifact": "operator_signoff_record", "required": True},
        {"artifact": "dry_run_review_packet", "required": True},
        {"artifact": "future_runtime_application_blueprint", "required": True},
    ]
    return [
        {
            **_dict(artifact),
            "required": _dict(artifact).get("required", True) is True,
            "runtime_application_status": "staged_not_applied",
            "mutation_status": "no_runtime_mutation",
        }
        for artifact in artifacts
    ]


def _manifest_requirement(name: str, present: bool) -> dict[str, Any]:
    return {
        "requirement": name,
        "status": "present" if present else "missing",
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
    }


def _missing_requirements(requirements: list[dict[str, Any]]) -> list[str]:
    missing: list[str] = []
    for item in requirements:
        record = _dict(item)
        name = record.get("requirement") or record.get("gate") or record.get("artifact")
        if record.get("status") == "missing":
            missing.append(str(name))
        elif record.get("required") is True and name and record.get("present") is False:
            missing.append(str(name))
    return sorted(set(missing))


def _prior_artifacts_preserve_no_mutation(inputs: dict[str, Any]) -> bool:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    required = (
        "application_plan",
        "human_approval_gate",
        "dry_run_review_packet",
        "dry_run_execution_report",
        "change_request",
    )
    return all(_source_present(source_presence, name) for name in required)


def _source_artifact_presence(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        name: {
            "present": bool(payload),
            "artifact_type": _artifact_type(payload),
            "runtime_application_status": payload.get("runtime_application_status"),
            "mutation_status": payload.get("mutation_status"),
        }
        for name, payload in source_payloads.items()
    }


def _source_present(source_presence: dict[str, Any], name: str) -> bool:
    return _dict(source_presence.get(name)).get("present") is True


def _missing_source_refs(source_payloads: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(name for name, payload in source_payloads.items() if not payload)


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
        "freeze_type",
        "baseline_type",
        "report_type",
    ):
        value = payload.get(key)
        if value:
            return str(value)
    return None


def _merged_warnings(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for name, payload in source_payloads.items():
        warnings = _dict(payload.get("warnings"))
        for key, value in warnings.items():
            merged[key] = value
        if not payload:
            merged[f"missing_source_{name}"] = True
    merged.update(WARNINGS)
    return merged


def _source_path_from_plan(
    application_plan: dict[str, Any],
    key: str,
    default_path: str | Path | None,
) -> str | None:
    value = application_plan.get(key)
    if value:
        return str(value)
    return _path_string(default_path)


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    if (
        contract.get("contract_type")
        != CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_TYPE
    ):
        errors.append(_error("invalid_contract_type", "contract_type", None))
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_CONTRACT_VERSION
    ):
        errors.append(_error("invalid_contract_version", "contract_version", None))
    for section in (
        "staging_scope",
        "source_contract_refs",
        "staging_input_schema",
        "staging_artifact_schema",
        "staged_config_delta_schema",
        "pre_apply_manifest_schema",
        "rollback_staging_schema",
        "post_application_verification_staging_schema",
        "future_baseline_candidate_staging_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "staging_inputs")
    _require_fields(inputs, STAGING_INPUT_REQUIRED_FIELDS, "staging_inputs", errors)
    if (
        inputs.get("staging_input_type")
        != CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_staging_input_type",
                "staging_input_type",
                inputs.get("staging_input_type"),
            )
        )
    if (
        inputs.get("staging_input_version")
        != CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_staging_input_version",
                "staging_input_version",
                inputs.get("staging_input_version"),
            )
        )
    _validate_non_claims(inputs, errors, path="staging_inputs.non_claims")
    return errors


def _validate_staging_shape(staging: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(staging, "staging")
    _require_fields(staging, STAGING_REQUIRED_FIELDS, "staging", errors)
    if (
        staging.get("staging_type")
        != CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_TYPE
    ):
        errors.append(
            _error(
                "invalid_staging_type",
                "staging_type",
                staging.get("staging_type"),
            )
        )
    if (
        staging.get("staging_version")
        != CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
    ):
        errors.append(
            _error(
                "invalid_staging_version",
                "staging_version",
                staging.get("staging_version"),
            )
        )
    _validate_required_staging_statuses(staging, errors)
    _validate_required_bool(
        staging,
        "future_blueprint_required_for_runtime_application",
        True,
        errors,
    )
    _validate_allowed(
        staging.get("staging_status"),
        ALLOWED_STAGING_STATUSES,
        "staging_status",
        errors,
    )
    errors.extend(
        _validate_staged_config_delta_shape(_dict(staging.get("staged_config_delta")))
    )
    errors.extend(
        _validate_pre_apply_manifest_shape(_dict(staging.get("pre_apply_manifest")))
    )
    errors.extend(
        _validate_rollback_staging_shape(_dict(staging.get("rollback_staging_record")))
    )
    errors.extend(
        _validate_post_application_verification_staging_shape(
            _dict(staging.get("post_application_verification_staging_record"))
        )
    )
    errors.extend(
        _validate_future_baseline_staging_policy_shape(
            _dict(staging.get("future_baseline_candidate_staging_policy"))
        )
    )
    _validate_non_claims(staging, errors, path="staging.non_claims")
    return errors


def _validate_staged_config_delta_shape(
    staged_delta: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(staged_delta, "staged_config_delta")
    _require_fields(
        staged_delta,
        STAGED_CONFIG_DELTA_REQUIRED_FIELDS,
        "staged_config_delta",
        errors,
    )
    if (
        staged_delta.get("staged_config_delta_type")
        != CONTROLLED_RUNTIME_CALIBRATION_STAGED_CONFIG_DELTA_TYPE
    ):
        errors.append(
            _error(
                "invalid_staged_config_delta_type",
                "staged_config_delta.staged_config_delta_type",
                staged_delta.get("staged_config_delta_type"),
            )
        )
    _validate_allowed(
        staged_delta.get("delta_status"),
        ALLOWED_STAGED_CONFIG_DELTA_STATUSES,
        "staged_config_delta.delta_status",
        errors,
    )
    _validate_required_runtime_status(
        staged_delta,
        "runtime_application_status",
        "staged_not_applied",
        errors,
    )
    _validate_required_status(
        staged_delta,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_required_status(
        staged_delta,
        "runtime_config_status",
        "not_updated",
        ALLOWED_RUNTIME_CONFIG_STATUSES,
        errors,
    )
    _validate_required_status(
        staged_delta,
        "production_config_status",
        "not_created",
        ALLOWED_PRODUCTION_CONFIG_STATUSES,
        errors,
    )
    _validate_non_claims(
        staged_delta,
        errors,
        path="staged_config_delta.non_claims",
    )
    return errors


def _validate_pre_apply_manifest_shape(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(manifest, "pre_apply_manifest")
    _require_fields(
        manifest,
        PRE_APPLY_MANIFEST_REQUIRED_FIELDS,
        "pre_apply_manifest",
        errors,
    )
    if (
        manifest.get("pre_apply_manifest_type")
        != CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLY_MANIFEST_TYPE
    ):
        errors.append(
            _error(
                "invalid_pre_apply_manifest_type",
                "pre_apply_manifest.pre_apply_manifest_type",
                manifest.get("pre_apply_manifest_type"),
            )
        )
    _validate_allowed(
        manifest.get("manifest_status"),
        ALLOWED_PRE_APPLY_MANIFEST_STATUSES,
        "pre_apply_manifest.manifest_status",
        errors,
    )
    _validate_non_claims(manifest, errors, path="pre_apply_manifest.non_claims")
    return errors


def _validate_rollback_staging_shape(
    rollback: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(rollback, "rollback_staging_record")
    _require_fields(
        rollback,
        ROLLBACK_STAGING_REQUIRED_FIELDS,
        "rollback_staging_record",
        errors,
    )
    if (
        rollback.get("rollback_staging_type")
        != CONTROLLED_RUNTIME_CALIBRATION_STAGED_ROLLBACK_REPORT_TYPE
    ):
        errors.append(
            _error(
                "invalid_rollback_staging_type",
                "rollback_staging_record.rollback_staging_type",
                rollback.get("rollback_staging_type"),
            )
        )
    _validate_allowed(
        rollback.get("rollback_staging_status"),
        ALLOWED_ROLLBACK_STAGING_STATUSES,
        "rollback_staging_record.rollback_staging_status",
        errors,
    )
    _validate_required_runtime_status(
        rollback,
        "runtime_application_status",
        "staged_not_applied",
        errors,
    )
    _validate_required_status(
        rollback,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_non_claims(
        rollback,
        errors,
        path="rollback_staging_record.non_claims",
    )
    return errors


def _validate_post_application_verification_staging_shape(
    verification: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(
        verification,
        "post_application_verification_staging_record",
    )
    _require_fields(
        verification,
        POST_APPLICATION_VERIFICATION_STAGING_REQUIRED_FIELDS,
        "post_application_verification_staging_record",
        errors,
    )
    if (
        verification.get("post_application_verification_staging_type")
        != CONTROLLED_RUNTIME_CALIBRATION_STAGED_POST_APPLICATION_VERIFICATION_REPORT_TYPE
    ):
        errors.append(
            _error(
                "invalid_post_application_verification_staging_type",
                (
                    "post_application_verification_staging_record."
                    "post_application_verification_staging_type"
                ),
                verification.get("post_application_verification_staging_type"),
            )
        )
    _validate_allowed(
        verification.get("verification_staging_status"),
        ALLOWED_POST_APPLICATION_VERIFICATION_STAGING_STATUSES,
        "post_application_verification_staging_record.verification_staging_status",
        errors,
    )
    _validate_non_claims(
        verification,
        errors,
        path="post_application_verification_staging_record.non_claims",
    )
    return errors


def _validate_future_baseline_staging_policy_shape(
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(policy, "future_baseline_candidate_staging_policy")
    _require_fields(
        policy,
        FUTURE_BASELINE_STAGING_POLICY_REQUIRED_FIELDS,
        "future_baseline_candidate_staging_policy",
        errors,
    )
    _validate_allowed(
        policy.get("future_baseline_policy_status"),
        ALLOWED_FUTURE_BASELINE_STAGING_POLICY_STATUSES,
        "future_baseline_candidate_staging_policy.future_baseline_policy_status",
        errors,
    )
    _validate_non_claims(
        policy,
        errors,
        path="future_baseline_candidate_staging_policy.non_claims",
    )
    return errors


def _validate_required_staging_statuses(
    payload: dict[str, Any],
    errors: list[dict[str, Any]],
) -> None:
    _validate_required_runtime_status(
        payload,
        "runtime_application_status",
        "staged_not_applied",
        errors,
    )
    _validate_required_status(
        payload,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_required_status(
        payload,
        "production_config_status",
        "not_created",
        ALLOWED_PRODUCTION_CONFIG_STATUSES,
        errors,
    )
    _validate_required_status(
        payload,
        "runtime_config_status",
        "not_updated",
        ALLOWED_RUNTIME_CONFIG_STATUSES,
        errors,
    )
    _validate_required_status(
        payload,
        "baseline_update_status",
        "not_replaced",
        ["not_replaced", "not_applicable"],
        errors,
    )
    _validate_required_status(
        payload,
        "model_update_status",
        "not_modified",
        ["not_modified", "not_applicable"],
        errors,
    )


def _validate_required_runtime_status(
    report: dict[str, Any],
    field: str,
    required_value: str,
    errors: list[dict[str, Any]],
) -> None:
    _validate_required_status(
        report,
        field,
        required_value,
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        errors,
    )


def _validate_required_status(
    report: dict[str, Any],
    field: str,
    required_value: str,
    allowed_values: list[str],
    errors: list[dict[str, Any]],
) -> None:
    value = report.get(field)
    _validate_allowed(value, allowed_values, field, errors)
    if value != required_value:
        errors.append(_error(f"{field}_must_be_{required_value}", field, value))


def _validate_required_bool(
    payload: dict[str, Any],
    field: str,
    required_value: bool,
    errors: list[dict[str, Any]],
) -> None:
    if payload.get(field) is not required_value:
        errors.append(
            _error(f"{field}_must_be_{required_value}", field, payload.get(field))
        )


def _validate_allowed(
    value: Any,
    allowed_values: list[str],
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    if value not in allowed_values:
        errors.append(_error("invalid_allowed_value", path, value))


def _validate_non_claims(
    payload: dict[str, Any],
    errors: list[dict[str, Any]],
    *,
    path: str,
) -> None:
    non_claims = _dict(payload.get("non_claims"))
    for key, expected in NON_CLAIMS.items():
        if non_claims.get(key) is not expected:
            errors.append(_error("missing_required_non_claim", f"{path}.{key}", None))


def _forbidden_token_errors(payload: Any, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            if key_text in FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS:
                errors.append(_error("forbidden_field_or_value", f"{path}.{key_text}", key_text))
            errors.extend(_forbidden_token_errors(value, f"{path}.{key_text}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(_forbidden_token_errors(value, f"{path}[{index}]"))
    elif isinstance(payload, str) and payload in FORBIDDEN_RUNTIME_APPLICATION_STAGING_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, payload))
    return errors


def _require_fields(
    payload: dict[str, Any],
    fields: list[str],
    payload_name: str,
    errors: list[dict[str, Any]],
) -> None:
    for field in fields:
        if field not in payload:
            errors.append(_error("missing_required_field", f"{payload_name}.{field}", None))


def _validation_result(
    *,
    ok: bool,
    validation_type: str,
    validated_at: datetime,
    contract_path: str | Path,
    payload_path: str | Path,
    payload_type: str | None,
    payload_version: str | None,
    errors: list[dict[str, Any]],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "ok": ok,
        "status": "valid" if ok else "invalid",
        "validation_type": validation_type,
        "validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "warnings": dict(WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed statuses, and forbidden values.",
            "Validation does not apply candidate settings or update runtime behavior.",
            "Validation does not score classifier output or infer tennis outcomes.",
        ],
    }
    if extra:
        result.update(extra)
    return result


def _validated_staging_or_failed(
    *,
    staging_path: str | Path,
    contract_path: str | Path,
    output_path: str | Path | None,
    result_key: str,
    payload_type: str,
    generated_at: datetime,
) -> dict[str, Any]:
    validation = validate_controlled_runtime_calibration_runtime_application_staging(
        staging_path=staging_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return {
            "failed_result": _failed_result(
                status="invalid_runtime_application_staging",
                errors=_list(validation.get("errors")),
                output_path=output_path,
                payload_type=payload_type,
                result_key=result_key,
            )
        }
    return _dict(_load_json(staging_path, label="staging").get("data"))


def _failed_result(
    *,
    status: str,
    errors: list[dict[str, Any]],
    output_path: str | Path | None,
    payload_type: str,
    result_key: str,
) -> dict[str, Any]:
    result = {
        "ok": False,
        "status": status,
        "payload_type": payload_type,
        "error_count": len(errors),
        "errors": errors,
        "runtime_application_status": "staged_not_applied",
        "mutation_status": "no_runtime_mutation",
        "runtime_config_status": "not_updated",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, result, result, result_key)
    return result


def _load_contract(*, contract_path: str | Path, errors: list[dict[str, Any]]) -> None:
    contract = _load_required_json(contract_path, "contract", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))


def _load_required_json(
    path: str | Path,
    label: str,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(path, label=label)
    if loaded["ok"] is False:
        errors.append(_error("missing_or_invalid_json", str(path), loaded.get("error")))
        return {}
    data = _dict(loaded.get("data"))
    if not data:
        errors.append(_error("missing_required_json", str(path), None))
    return data


def _load_optional_json(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    loaded = _load_json(path, label="optional_json")
    if loaded["ok"] is False:
        return {}
    return _dict(loaded.get("data"))


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "label": label, "error": "file_not_found"}
    except json.JSONDecodeError as exc:
        return {"ok": False, "label": label, "error": str(exc)}
    if not isinstance(data, dict):
        return {"ok": False, "label": label, "error": "json_root_not_object"}
    return {"ok": True, "label": label, "data": data}


def _write_json_if_requested(
    output_path: str | Path | None,
    payload: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None:
        return
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    result[result_key] = str(path)


def _stable_id(prefix: str, *values: Any) -> str:
    encoded = json.dumps(values, sort_keys=True, default=str).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(encoded).hexdigest()[:24]}"


def _sha256_path(path: str | Path | None) -> str | None:
    if path is None:
        return None
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def _path_string(path: str | Path | None) -> str | None:
    if path is None:
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, Any]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_RUNTIME_APPLICATION_STAGING_BLUEPRINT_NAME
        ),
    }
