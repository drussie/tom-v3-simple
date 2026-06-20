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
    CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_human_approval_gate import (
    SOURCE_CONTRACT_REFS as HUMAN_APPROVAL_GATE_SOURCE_CONTRACT_REFS,
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

CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_TYPE = (
    "controlled_runtime_calibration_application_plan_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE = (
    "controlled_runtime_calibration_application_plan_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE = (
    "controlled_runtime_calibration_application_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_CONFIG_DELTA_PROPOSAL_TYPE = (
    "controlled_runtime_calibration_config_delta_proposal"
)
CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_GATE_REPORT_TYPE = (
    "controlled_runtime_calibration_pre_application_gate_report"
)
CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PLAN_REPORT_TYPE = (
    "controlled_runtime_calibration_rollback_plan_report"
)
CONTROLLED_RUNTIME_CALIBRATION_POST_APPLICATION_VERIFICATION_PLAN_TYPE = (
    "controlled_runtime_calibration_post_application_verification_plan"
)
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_BLUEPRINT = "blueprint_59"
CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_application_plan_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_application_plan_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_application_plan_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_application_plan_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_application_plan_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_application_plan.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_GATE_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_pre_application_gate_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PLAN_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_rollback_plan_report.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_APPLICATION_VERIFICATION_PLAN_OUTPUT = (
    ".data/exports/"
    "controlled_runtime_calibration_post_application_verification_plan.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_human_approval_gate_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION
    ),
    **dict(HUMAN_APPROVAL_GATE_SOURCE_CONTRACT_REFS),
}

ALLOWED_APPLICATION_PLAN_STATUSES = [
    "application_plan_created",
    "application_plan_created_with_warnings",
    "application_plan_blocked_missing_human_approval_gate",
    "application_plan_blocked_missing_dry_run_review_packet",
    "application_plan_blocked_missing_change_request",
    "application_plan_blocked_missing_candidate_config",
    "application_plan_blocked_missing_rollback_plan",
    "application_plan_blocked_missing_regression_gate",
    "application_plan_blocked_unresolved_blockers",
    "application_plan_blocked_breaking_structural_change",
    "application_plan_informational_only",
    "not_applicable",
]
ALLOWED_PRE_APPLICATION_GATE_STATUSES = [
    "pre_application_gates_defined",
    "pre_application_gates_missing",
    "pre_application_gates_incomplete",
    "pre_application_gates_blocked",
    "not_applicable",
]
ALLOWED_ROLLBACK_PLAN_STATUSES = [
    "rollback_plan_defined",
    "rollback_plan_missing",
    "rollback_plan_incomplete",
    "rollback_plan_blocked",
    "rollback_not_executed",
    "not_applicable",
]
ALLOWED_POST_APPLICATION_VERIFICATION_STATUSES = [
    "post_application_verification_plan_defined",
    "post_application_verification_plan_missing",
    "post_application_verification_plan_incomplete",
    "post_application_verification_plan_blocked",
    "post_application_verification_not_executed",
    "not_applicable",
]
ALLOWED_FUTURE_BASELINE_POLICY_STATUSES = [
    "future_baseline_candidate_policy_defined",
    "future_baseline_candidate_policy_missing",
    "future_baseline_candidate_policy_incomplete",
    "future_baseline_candidate_policy_blocked",
    "baseline_update_not_performed",
    "not_applicable",
]
ALLOWED_CONFIG_DELTA_STATUSES = [
    "config_delta_proposed_for_future_blueprint",
    "config_delta_blocked_missing_current_settings",
    "config_delta_blocked_missing_candidate_settings",
    "config_delta_blocked_invalid_scope",
    "config_delta_informational_only",
    "not_applicable",
]

APPLICATION_PLAN_INPUT_REQUIRED_FIELDS = [
    "application_plan_input_id",
    "application_plan_input_type",
    "application_plan_input_version",
    "generated_at",
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
    "proposed_candidate_threshold",
    "proposed_candidate_smoothing_window",
    "proposed_candidate_hysteresis_settings",
    "operator_signoff_ref",
    "rollback_context",
    "post_application_verification_context",
    "future_baseline_policy_context",
    "warnings",
    "non_claims",
]
APPLICATION_PLAN_REQUIRED_FIELDS = [
    "application_plan_id",
    "application_plan_type",
    "application_plan_version",
    "generated_at",
    "source_application_plan_input_path",
    "source_human_approval_gate_path",
    "source_dry_run_review_packet_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "proposed_candidate_settings",
    "config_delta_proposal",
    "application_plan_status",
    "pre_application_gate_status",
    "rollback_plan_status",
    "post_application_verification_status",
    "future_baseline_policy_status",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "future_blueprint_required_for_runtime_application",
    "required_regression_gates",
    "required_operator_artifacts",
    "blockers",
    "warnings",
    "non_claims",
]
CONFIG_DELTA_REQUIRED_FIELDS = [
    "config_delta_proposal_id",
    "config_delta_proposal_type",
    "config_delta_proposal_version",
    "generated_at",
    "source_application_plan_id",
    "current_settings",
    "proposed_candidate_settings",
    "delta_fields",
    "delta_status",
    "runtime_application_status",
    "mutation_status",
    "warnings",
    "non_claims",
]
PRE_APPLICATION_GATE_REQUIRED_FIELDS = [
    "pre_application_gate_status",
    "requirements",
    "missing_requirements",
    "blockers",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "future_blueprint_required_for_runtime_application",
    "warnings",
    "non_claims",
]
ROLLBACK_PLAN_REQUIRED_FIELDS = [
    "rollback_scope",
    "rollback_target_settings",
    "rollback_trigger_conditions",
    "rollback_execution_steps_for_future_blueprint",
    "rollback_verification_gates",
    "rollback_artifact_refs",
    "rollback_status",
    "runtime_application_status",
    "mutation_status",
    "non_claims",
]
POST_APPLICATION_VERIFICATION_REQUIRED_FIELDS = [
    "verification_scope",
    "required_regression_gates",
    "required_replay_checks",
    "required_review_packet_after_application",
    "required_operator_review_after_application",
    "required_rollback_readiness_check",
    "future_baseline_candidate_conditions",
    "verification_status",
    "non_claims",
]
FUTURE_BASELINE_POLICY_REQUIRED_FIELDS = [
    "baseline_not_replaced_in_this_blueprint",
    "future_baseline_candidate_may_be_considered_only_after_runtime_application",
    "future_baseline_candidate_requires_post_application_review",
    "future_baseline_candidate_requires_regression_gates",
    "future_baseline_candidate_requires_human_review",
    "future_baseline_candidate_not_truth",
    "future_baseline_policy_status",
]

NON_CLAIMS = {
    "application_plan_is_not_truth": True,
    "application_plan_is_not_accuracy_scoring": True,
    "application_plan_is_not_runtime_calibration": True,
    "application_plan_is_not_runtime_application": True,
    "config_delta_proposal_is_not_runtime_config": True,
    "config_delta_proposal_is_not_production_config": True,
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
    "controlled_application_plan": True,
    "config_delta_proposal": True,
    "future_blueprint_required_for_runtime_application": True,
    "no_runtime_mutation": True,
    "runtime_application_status_not_applied": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "model_weights_not_modified": True,
    "post_application_verification_plan": True,
    "rollback_plan_defined": True,
    "application_plan_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "review_support_only": True,
    "planning_artifact_only": True,
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
FORBIDDEN_APPLICATION_PLAN_TOKENS = {
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


def export_controlled_runtime_calibration_application_plan_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at or CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_EXPORTED_AT
    )
    contract = _contract_payload(exported_at=exported_at)
    errors = _validate_contract_shape(contract)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_TYPE,
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION
        ),
        "contract": contract,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_controlled_runtime_calibration_application_plan_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
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
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_result(
            status="invalid_application_plan_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE,
            result_key="application_plan_inputs_output",
        )

    source_payloads = {
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
    approval_gate = source_payloads["human_approval_gate"]
    review_packet = source_payloads["dry_run_review_packet"]
    change_request = source_payloads["change_request"]
    candidate_config_freeze = source_payloads["candidate_config_freeze"]
    current_settings = _current_settings(
        approval_gate=approval_gate,
        review_packet=review_packet,
        change_request=change_request,
    )
    candidate_settings = _candidate_settings(
        approval_gate=approval_gate,
        review_packet=review_packet,
        change_request=change_request,
        candidate_config_freeze=candidate_config_freeze,
    )
    selected_candidate_ref = _selected_candidate_ref(
        approval_gate=approval_gate,
        review_packet=review_packet,
        change_request=change_request,
        candidate_config_freeze=candidate_config_freeze,
    )
    operator_signoff_record = _dict(approval_gate.get("operator_signoff_record"))
    inputs = {
        "application_plan_input_id": _stable_id(
            "controlled_runtime_calibration_application_plan_inputs_v1",
            _path_string(source_human_approval_gate_path),
            approval_gate.get("approval_gate_id"),
            review_packet.get("review_packet_id"),
            change_request.get("change_request_id"),
            selected_candidate_ref,
            _sha256_path(model_asset_path),
        ),
        "application_plan_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE
        ),
        "application_plan_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_human_approval_gate_path": str(Path(source_human_approval_gate_path)),
        "source_dry_run_review_packet_path": str(
            Path(source_dry_run_review_packet_path)
        ),
        "source_dry_run_execution_report_path": str(
            Path(source_dry_run_execution_report_path)
        ),
        "source_change_request_path": str(Path(source_change_request_path)),
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
        "source_human_approval_gate_id": approval_gate.get("approval_gate_id"),
        "source_dry_run_review_packet_id": review_packet.get("review_packet_id"),
        "source_dry_run_execution_report_id": source_payloads[
            "dry_run_execution_report"
        ].get("dry_run_id"),
        "change_request_id": change_request.get("change_request_id"),
        "candidate_config_freeze_id": candidate_config_freeze.get(
            "candidate_config_freeze_id"
        ),
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
        "proposed_candidate_threshold": candidate_settings.get("candidate_threshold"),
        "proposed_candidate_smoothing_window": candidate_settings.get(
            "candidate_smoothing_window"
        ),
        "proposed_candidate_hysteresis_settings": _dict(
            candidate_settings.get("candidate_hysteresis_settings")
        ),
        "current_settings": current_settings,
        "proposed_candidate_settings": _proposed_candidate_settings(
            candidate_settings
        ),
        "operator_signoff_ref": {
            "operator_signoff_id": operator_signoff_record.get("operator_signoff_id"),
            "operator_signoff_status": approval_gate.get("operator_signoff_status"),
            "source_human_approval_gate_path": str(Path(source_human_approval_gate_path)),
        },
        "rollback_context": _rollback_context(review_packet=review_packet),
        "post_application_verification_context": {
            "required_after_future_application": True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "future_baseline_policy_context": {
            "baseline_not_replaced_in_this_blueprint": True,
            "future_blueprint_required_for_runtime_application": True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
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
            status="invalid_application_plan_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE,
            result_key="application_plan_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "application_plan_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE
        ),
        "application_plan_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_VERSION
        ),
        "application_plan_input_id": inputs["application_plan_input_id"],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "future_blueprint_required_for_runtime_application": True,
        "application_plan_inputs": inputs,
        "warnings": inputs["warnings"],
    }
    _write_json_if_requested(
        output_path,
        inputs,
        result,
        "application_plan_inputs_output",
    )
    return result


def validate_controlled_runtime_calibration_application_plan_inputs(
    *,
    application_plan_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(
        application_plan_inputs_path,
        "application_plan_inputs",
        errors,
    )
    if inputs:
        errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        ok=not errors,
        validation_type=(
            "controlled_runtime_calibration_application_plan_inputs_validation"
        ),
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=application_plan_inputs_path,
        payload_type=inputs.get("application_plan_input_type") if inputs else None,
        payload_version=inputs.get("application_plan_input_version")
        if inputs
        else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_application_plan(
    *,
    application_plan_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_application_plan_inputs(
        application_plan_inputs_path=application_plan_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_application_plan_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE,
            result_key="application_plan_output",
        )

    inputs = _dict(
        _load_json(application_plan_inputs_path, label="application_plan_inputs").get(
            "data"
        )
    )
    approval_gate = _load_optional_json(inputs.get("source_human_approval_gate_path"))
    review_packet = _load_optional_json(inputs.get("source_dry_run_review_packet_path"))
    current_settings = _dict(inputs.get("current_settings"))
    candidate_settings = _dict(inputs.get("proposed_candidate_settings"))
    selected_candidate_ref = _dict(inputs.get("selected_candidate_config_ref"))
    pre_application_gate = _pre_application_gate(
        inputs=inputs,
        approval_gate=approval_gate,
        review_packet=review_packet,
    )
    application_plan_id = _stable_id(
        "controlled_runtime_calibration_application_plan_v1",
        inputs.get("application_plan_input_id"),
        approval_gate.get("approval_gate_id"),
        review_packet.get("review_packet_id"),
        selected_candidate_ref,
        pre_application_gate.get("pre_application_gate_status"),
    )
    rollback_plan = _rollback_plan(
        source_application_plan_id=application_plan_id,
        source_application_plan_input_path=str(Path(application_plan_inputs_path)),
        inputs=inputs,
        current_settings=current_settings,
    )
    post_application_verification_plan = _post_application_verification_plan(
        source_application_plan_id=application_plan_id
    )
    future_baseline_policy = _future_baseline_candidate_policy()
    config_delta_proposal = _config_delta_proposal(
        source_application_plan_id=application_plan_id,
        current_settings=current_settings,
        proposed_candidate_settings=candidate_settings,
        generated_at=generated_at,
    )
    blockers = sorted(set(_list(pre_application_gate.get("blockers"))))
    application_plan_status = _application_plan_status(
        inputs=inputs,
        approval_gate=approval_gate,
        review_packet=review_packet,
        config_delta_status=config_delta_proposal["delta_status"],
        blockers=blockers,
    )
    plan = {
        "application_plan_id": application_plan_id,
        "application_plan_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE,
        "application_plan_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_application_plan_input_path": str(Path(application_plan_inputs_path)),
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
        "proposed_candidate_settings": candidate_settings,
        "config_delta_proposal": config_delta_proposal,
        "pre_application_gate": pre_application_gate,
        "rollback_plan": rollback_plan,
        "post_application_verification_plan": post_application_verification_plan,
        "future_baseline_candidate_policy": future_baseline_policy,
        "application_plan_status": application_plan_status,
        "pre_application_gate_status": pre_application_gate[
            "pre_application_gate_status"
        ],
        "rollback_plan_status": rollback_plan["rollback_status"],
        "post_application_verification_status": post_application_verification_plan[
            "verification_status"
        ],
        "future_baseline_policy_status": future_baseline_policy[
            "future_baseline_policy_status"
        ],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "required_regression_gates": _required_regression_gates(),
        "required_operator_artifacts": _required_operator_artifacts(),
        "blockers": blockers,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(inputs.get("warnings")),
            **dict(WARNINGS),
            "runtime_application_status_not_applied": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_plan_shape(plan)
    if validation_errors:
        return _failed_result(
            status="invalid_application_plan",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE,
            result_key="application_plan_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "application_plan_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE,
        "application_plan_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION
        ),
        "application_plan_id": plan["application_plan_id"],
        "application_plan_status": plan["application_plan_status"],
        "pre_application_gate_status": plan["pre_application_gate_status"],
        "rollback_plan_status": plan["rollback_plan_status"],
        "post_application_verification_status": (
            plan["post_application_verification_status"]
        ),
        "future_baseline_policy_status": plan["future_baseline_policy_status"],
        "runtime_application_status": plan["runtime_application_status"],
        "mutation_status": plan["mutation_status"],
        "production_config_status": plan["production_config_status"],
        "baseline_update_status": plan["baseline_update_status"],
        "model_update_status": plan["model_update_status"],
        "future_blueprint_required_for_runtime_application": plan[
            "future_blueprint_required_for_runtime_application"
        ],
        "application_plan": plan,
        "warnings": plan["warnings"],
    }
    _write_json_if_requested(output_path, plan, result, "application_plan_output")
    return result


def validate_controlled_runtime_calibration_application_plan(
    *,
    application_plan_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    plan = _load_required_json(application_plan_path, "application_plan", errors)
    if plan:
        errors.extend(_validate_plan_shape(plan))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_application_plan_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=application_plan_path,
        payload_type=plan.get("application_plan_type") if plan else None,
        payload_version=plan.get("application_plan_version") if plan else None,
        errors=errors,
        extra={
            "application_plan_status": plan.get("application_plan_status")
            if plan
            else None,
            "pre_application_gate_status": plan.get("pre_application_gate_status")
            if plan
            else None,
            "runtime_application_status": plan.get("runtime_application_status")
            if plan
            else None,
            "mutation_status": plan.get("mutation_status") if plan else None,
            "production_config_status": plan.get("production_config_status")
            if plan
            else None,
            "baseline_update_status": plan.get("baseline_update_status")
            if plan
            else None,
            "model_update_status": plan.get("model_update_status")
            if plan
            else None,
            "future_blueprint_required_for_runtime_application": plan.get(
                "future_blueprint_required_for_runtime_application"
            )
            if plan
            else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_pre_application_gate_report(
    *,
    application_plan_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_GATE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_application_plan(
        application_plan_path=application_plan_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_application_plan",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_GATE_REPORT_TYPE,
            result_key="pre_application_gate_report_output",
        )
    plan = _dict(_load_json(application_plan_path, label="application_plan").get("data"))
    gate = {
        **_dict(plan.get("pre_application_gate")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_GATE_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_application_plan_path": str(Path(application_plan_path)),
        "application_plan_id": plan.get("application_plan_id"),
    }
    errors = _validate_pre_application_gate_shape(gate)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_pre_application_gate_report",
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_PRE_APPLICATION_GATE_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "application_plan_id": plan.get("application_plan_id"),
        "pre_application_gate_status": gate.get("pre_application_gate_status"),
        "error_count": len(errors),
        "errors": errors,
        "pre_application_gate_report": gate,
        "warnings": _dict(gate.get("warnings")),
    }
    _write_json_if_requested(
        output_path,
        gate,
        result,
        "pre_application_gate_report_output",
    )
    return result


def build_controlled_runtime_calibration_rollback_plan_report(
    *,
    application_plan_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PLAN_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_application_plan(
        application_plan_path=application_plan_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_application_plan",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PLAN_REPORT_TYPE,
            result_key="rollback_plan_report_output",
        )
    plan = _dict(_load_json(application_plan_path, label="application_plan").get("data"))
    rollback = {
        **_dict(plan.get("rollback_plan")),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PLAN_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_application_plan_path": str(Path(application_plan_path)),
        "application_plan_id": plan.get("application_plan_id"),
    }
    errors = _validate_rollback_plan_shape(rollback)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_rollback_plan_report",
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_ROLLBACK_PLAN_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "application_plan_id": plan.get("application_plan_id"),
        "rollback_status": rollback.get("rollback_status"),
        "runtime_application_status": rollback.get("runtime_application_status"),
        "mutation_status": rollback.get("mutation_status"),
        "error_count": len(errors),
        "errors": errors,
        "rollback_plan_report": rollback,
        "warnings": _dict(rollback.get("warnings")),
    }
    _write_json_if_requested(output_path, rollback, result, "rollback_plan_report_output")
    return result


def build_controlled_runtime_calibration_post_application_verification_plan(
    *,
    application_plan_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_POST_APPLICATION_VERIFICATION_PLAN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_application_plan(
        application_plan_path=application_plan_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_application_plan",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_POST_APPLICATION_VERIFICATION_PLAN_TYPE
            ),
            result_key="post_application_verification_plan_output",
        )
    plan = _dict(_load_json(application_plan_path, label="application_plan").get("data"))
    verification_plan = {
        **_dict(plan.get("post_application_verification_plan")),
        "plan_type": (
            CONTROLLED_RUNTIME_CALIBRATION_POST_APPLICATION_VERIFICATION_PLAN_TYPE
        ),
        "plan_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_application_plan_path": str(Path(application_plan_path)),
        "application_plan_id": plan.get("application_plan_id"),
    }
    errors = _validate_post_application_verification_shape(verification_plan)
    result = {
        "ok": not errors,
        "status": "completed"
        if not errors
        else "invalid_post_application_verification_plan",
        "plan_type": CONTROLLED_RUNTIME_CALIBRATION_POST_APPLICATION_VERIFICATION_PLAN_TYPE,
        "plan_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "application_plan_id": plan.get("application_plan_id"),
        "verification_status": verification_plan.get("verification_status"),
        "error_count": len(errors),
        "errors": errors,
        "post_application_verification_plan": verification_plan,
        "warnings": _dict(verification_plan.get("warnings")),
    }
    _write_json_if_requested(
        output_path,
        verification_plan,
        result,
        "post_application_verification_plan_output",
    )
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_TYPE,
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "application_plan_scope": {
            "purpose": "controlled_runtime_calibration_application_plan",
            "consumes_human_approval_gate": True,
            "consumes_dry_run_review_packet": True,
            "consumes_dry_run_execution_report": True,
            "consumes_controlled_change_request": True,
            "defines_config_delta_proposal": True,
            "defines_pre_application_gates": True,
            "defines_rollback_plan": True,
            "defines_post_application_verification_plan": True,
            "defines_future_baseline_candidate_policy": True,
            "future_blueprint_required_for_runtime_application": True,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "updates_runtime_configuration": False,
            "creates_deployable_configuration": False,
            "updates_model_weights": False,
            "mutates_regression_baselines": False,
            "automatic_approval_allowed": False,
            "automatic_rejection_allowed": False,
            "calculates_classifier_correctness": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "application_plan_input_schema": {
            "application_plan_input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE
            ),
            "application_plan_input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_VERSION
            ),
            "required_fields": list(APPLICATION_PLAN_INPUT_REQUIRED_FIELDS),
        },
        "application_plan_schema": {
            "application_plan_type": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE,
            "application_plan_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION
            ),
            "required_fields": list(APPLICATION_PLAN_REQUIRED_FIELDS),
            "allowed_application_plan_statuses": list(
                ALLOWED_APPLICATION_PLAN_STATUSES
            ),
            "required_runtime_application_status": "not_applied",
            "required_mutation_status": "no_runtime_mutation",
            "required_production_config_status": "not_created",
            "required_baseline_update_status": "not_replaced",
            "required_model_update_status": "not_modified",
            "future_blueprint_required_for_runtime_application": True,
        },
        "config_delta_proposal_schema": {
            "config_delta_proposal_type": (
                CONTROLLED_RUNTIME_CALIBRATION_CONFIG_DELTA_PROPOSAL_TYPE
            ),
            "config_delta_proposal_version": (
                CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION
            ),
            "required_fields": list(CONFIG_DELTA_REQUIRED_FIELDS),
            "allowed_config_delta_statuses": list(ALLOWED_CONFIG_DELTA_STATUSES),
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
            "not_runtime_config": True,
            "not_production_config": True,
        },
        "pre_application_gate_schema": {
            "required_fields": list(PRE_APPLICATION_GATE_REQUIRED_FIELDS),
            "allowed_pre_application_gate_statuses": list(
                ALLOWED_PRE_APPLICATION_GATE_STATUSES
            ),
        },
        "rollback_plan_schema": {
            "required_fields": list(ROLLBACK_PLAN_REQUIRED_FIELDS),
            "allowed_rollback_plan_statuses": list(ALLOWED_ROLLBACK_PLAN_STATUSES),
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "post_application_verification_schema": {
            "required_fields": list(POST_APPLICATION_VERIFICATION_REQUIRED_FIELDS),
            "allowed_post_application_verification_statuses": list(
                ALLOWED_POST_APPLICATION_VERIFICATION_STATUSES
            ),
        },
        "future_baseline_candidate_policy_schema": {
            "required_fields": list(FUTURE_BASELINE_POLICY_REQUIRED_FIELDS),
            "allowed_future_baseline_policy_statuses": list(
                ALLOWED_FUTURE_BASELINE_POLICY_STATUSES
            ),
            "baseline_update_status": "not_replaced",
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_application_plan_input_shape": True,
            "validate_application_plan_shape": True,
            "validate_config_delta_proposal_shape": True,
            "validate_pre_application_gate_shape": True,
            "validate_rollback_plan_shape": True,
            "validate_post_application_verification_plan_shape": True,
            "validate_future_baseline_candidate_policy_shape": True,
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
            "operator_signoff_ref_recorded": True,
            "rollback_context_recorded": True,
            "post_application_verification_context_recorded": True,
            "future_baseline_policy_context_recorded": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _application_plan_status(
    *,
    inputs: dict[str, Any],
    approval_gate: dict[str, Any],
    review_packet: dict[str, Any],
    config_delta_status: str,
    blockers: list[str],
) -> str:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    if not _source_present(source_presence, "human_approval_gate"):
        return "application_plan_blocked_missing_human_approval_gate"
    if not _source_present(source_presence, "dry_run_review_packet"):
        return "application_plan_blocked_missing_dry_run_review_packet"
    if not _source_present(source_presence, "change_request"):
        return "application_plan_blocked_missing_change_request"
    if not _has_selected_candidate_ref(_dict(inputs.get("selected_candidate_config_ref"))):
        if blockers:
            return "application_plan_blocked_unresolved_blockers"
        return "application_plan_blocked_missing_candidate_config"
    if _dict(review_packet.get("rollback_readiness_summary")).get(
        "rollback_readiness_status"
    ) != "rollback_ready_for_future_phase_review":
        return "application_plan_blocked_missing_rollback_plan"
    if _dict(review_packet.get("regression_gate_summary")).get(
        "gate_summary_status"
    ) != "gate_refs_present":
        return "application_plan_blocked_missing_regression_gate"
    if _dict(review_packet.get("structural_comparison_summary")).get(
        "summary_status"
    ) == "breaking_structural_change_observed":
        return "application_plan_blocked_breaking_structural_change"
    if blockers:
        return "application_plan_blocked_unresolved_blockers"
    if approval_gate.get("approval_gate_status") == "approval_gate_informational_only":
        return "application_plan_informational_only"
    if config_delta_status != "config_delta_proposed_for_future_blueprint":
        return "application_plan_created_with_warnings"
    return "application_plan_created"


def _pre_application_gate(
    *,
    inputs: dict[str, Any],
    approval_gate: dict[str, Any],
    review_packet: dict[str, Any],
) -> dict[str, Any]:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    blocker_summary = _dict(approval_gate.get("blocker_resolution_summary"))
    source_blockers = set(str(item) for item in _list(blocker_summary.get("unresolved_blockers")))
    requirements = [
        _requirement(
            "human_approval_gate_artifact_present",
            _source_present(source_presence, "human_approval_gate"),
        ),
        _requirement(
            "operator_signoff_artifact_present",
            bool(_dict(approval_gate.get("operator_signoff_record"))),
        ),
        _requirement(
            "dry_run_review_packet_present",
            _source_present(source_presence, "dry_run_review_packet"),
        ),
        _requirement(
            "dry_run_execution_report_present",
            _source_present(source_presence, "dry_run_execution_report"),
        ),
        _requirement(
            "controlled_change_request_present",
            _source_present(source_presence, "change_request"),
        ),
        _requirement(
            "candidate_config_freeze_present",
            _source_present(source_presence, "candidate_config_freeze"),
        ),
        _requirement("rollback_plan_present", True),
        _requirement("post_application_verification_plan_present", True),
        _requirement(
            "multi_point_regression_gate_required",
            _dict(review_packet.get("regression_gate_summary")).get(
                "multi_point_regression_required"
            )
            is True,
        ),
        _requirement(
            "protected_sample_point_gate_required",
            _dict(review_packet.get("regression_gate_summary")).get(
                "protected_sample_point_gate_required"
            )
            is True,
        ),
        _requirement(
            "gameplay_gate_regression_baseline_gate_required",
            _dict(review_packet.get("regression_gate_summary")).get(
                "gameplay_gate_regression_required"
            )
            is True,
        ),
        _requirement(
            "calibration_sandbox_regression_gate_required",
            _dict(review_packet.get("regression_gate_summary")).get(
                "calibration_sandbox_regression_required"
            )
            is True,
        ),
        _requirement("no_unresolved_blockers", not source_blockers),
        _requirement(
            "no_runtime_mutation_in_prior_artifacts",
            _prior_artifacts_preserve_no_mutation(inputs),
        ),
        _requirement("model_asset_hash_captured", bool(inputs.get("model_asset_sha256"))),
        _requirement("generated_exports_not_committed", True),
        _requirement("future_blueprint_required", True),
    ]
    missing_requirements = [
        str(item["requirement"]) for item in requirements if item["status"] != "present"
    ]
    blockers = set(source_blockers)
    blockers.update(str(item) for item in missing_requirements)
    if not requirements:
        status = "pre_application_gates_missing"
    elif source_blockers:
        status = "pre_application_gates_blocked"
    elif missing_requirements:
        status = "pre_application_gates_incomplete"
    else:
        status = "pre_application_gates_defined"
    return {
        "pre_application_gate_status": status,
        "requirements": requirements,
        "missing_requirements": missing_requirements,
        "blockers": sorted(blockers),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "warnings": {
            "pre_application_gate": True,
            "runtime_application_status_not_applied": True,
            "no_runtime_mutation": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _config_delta_proposal(
    *,
    source_application_plan_id: str,
    current_settings: dict[str, Any],
    proposed_candidate_settings: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    delta_fields = _delta_fields(current_settings, proposed_candidate_settings)
    delta_status = _delta_status(
        current_settings=current_settings,
        proposed_candidate_settings=proposed_candidate_settings,
        delta_fields=delta_fields,
    )
    return {
        "config_delta_proposal_id": _stable_id(
            "controlled_runtime_calibration_config_delta_proposal_v1",
            source_application_plan_id,
            current_settings,
            proposed_candidate_settings,
            delta_fields,
        ),
        "config_delta_proposal_type": (
            CONTROLLED_RUNTIME_CALIBRATION_CONFIG_DELTA_PROPOSAL_TYPE
        ),
        "config_delta_proposal_version": (
            CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_application_plan_id": source_application_plan_id,
        "current_settings": current_settings,
        "proposed_candidate_settings": proposed_candidate_settings,
        "delta_fields": delta_fields,
        "delta_status": delta_status,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "config_delta_proposal": True,
            "config_delta_proposal_is_not_runtime_config": True,
            "config_delta_proposal_is_not_production_config": True,
            "runtime_application_status_not_applied": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _delta_fields(
    current_settings: dict[str, Any],
    proposed_candidate_settings: dict[str, Any],
) -> list[dict[str, Any]]:
    candidates = [
        ("threshold", "current_threshold", "proposed_candidate_threshold"),
        (
            "smoothing_window",
            "current_smoothing_window",
            "proposed_candidate_smoothing_window",
        ),
        (
            "hysteresis_settings",
            "current_hysteresis_settings",
            "proposed_candidate_hysteresis_settings",
        ),
    ]
    deltas = []
    for field_name, current_key, proposed_key in candidates:
        current_value = current_settings.get(current_key)
        proposed_value = proposed_candidate_settings.get(proposed_key)
        deltas.append(
            {
                "field": field_name,
                "current_value": current_value,
                "proposed_value": proposed_value,
                "change_present": proposed_value is not None
                and proposed_value != current_value,
                "runtime_application_status": "not_applied",
                "mutation_status": "no_runtime_mutation",
            }
        )
    return deltas


def _delta_status(
    *,
    current_settings: dict[str, Any],
    proposed_candidate_settings: dict[str, Any],
    delta_fields: list[dict[str, Any]],
) -> str:
    if not current_settings:
        return "config_delta_blocked_missing_current_settings"
    if not _has_candidate_settings(proposed_candidate_settings):
        return "config_delta_blocked_missing_candidate_settings"
    if any(_dict(proposed_candidate_settings).get(key) for key in (
        "writes_runtime_configuration",
        "affects_regression_baselines",
    )):
        return "config_delta_blocked_invalid_scope"
    if any(item.get("change_present") is True for item in delta_fields):
        return "config_delta_proposed_for_future_blueprint"
    return "config_delta_informational_only"


def _rollback_plan(
    *,
    source_application_plan_id: str,
    source_application_plan_input_path: str,
    inputs: dict[str, Any],
    current_settings: dict[str, Any],
) -> dict[str, Any]:
    return {
        "rollback_scope": {
            "source_application_plan_id": source_application_plan_id,
            "future_blueprint_only": True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "rollback_target_settings": current_settings,
        "rollback_trigger_conditions": [
            "operator requests rollback after separate future runtime application",
            "future post-application verification gate blocks",
            "future regression gate blocks",
            "future review packet raises blocker",
        ],
        "rollback_execution_steps_for_future_blueprint": [
            "capture pre-application runtime settings",
            "restore captured runtime settings in a separate runtime application blueprint",
            "run required regression gates",
            "build post-rollback review packet",
            "record human operator review state",
        ],
        "rollback_verification_gates": _required_regression_gates(),
        "rollback_artifact_refs": {
            "source_application_plan_input_path": source_application_plan_input_path,
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
        },
        "rollback_status": "rollback_plan_defined",
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "rollback_plan_defined": True,
            "rollback_not_executed": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _post_application_verification_plan(
    *,
    source_application_plan_id: str,
) -> dict[str, Any]:
    return {
        "verification_scope": {
            "source_application_plan_id": source_application_plan_id,
            "separate_future_runtime_application_required": True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "required_regression_gates": _required_regression_gates(),
        "required_replay_checks": [
            "manifest-backed multi-point replay review",
            "protected sample_point replay review",
            "gameplay segment replay review timeline check",
        ],
        "required_review_packet_after_application": True,
        "required_operator_review_after_application": True,
        "required_rollback_readiness_check": True,
        "future_baseline_candidate_conditions": [
            "separate future runtime application exists",
            "post-application review packet exists",
            "required regression gates pass structurally",
            "human operator review is recorded",
            "future baseline candidate remains review-only",
        ],
        "verification_status": "post_application_verification_plan_defined",
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "post_application_verification_plan": True,
            "post_application_verification_not_executed": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _future_baseline_candidate_policy() -> dict[str, Any]:
    return {
        "baseline_not_replaced_in_this_blueprint": True,
        "future_baseline_candidate_may_be_considered_only_after_runtime_application": True,
        "future_baseline_candidate_requires_post_application_review": True,
        "future_baseline_candidate_requires_regression_gates": True,
        "future_baseline_candidate_requires_human_review": True,
        "future_baseline_candidate_not_truth": True,
        "future_baseline_policy_status": (
            "future_baseline_candidate_policy_defined"
        ),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "baseline_update_status": "not_replaced",
        "warnings": {
            "baseline_not_replaced": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _current_settings(
    *,
    approval_gate: dict[str, Any],
    review_packet: dict[str, Any],
    change_request: dict[str, Any],
) -> dict[str, Any]:
    return (
        _dict(approval_gate.get("current_settings"))
        or _dict(review_packet.get("current_settings"))
        or _dict(change_request.get("current_settings"))
    )


def _candidate_settings(
    *,
    approval_gate: dict[str, Any],
    review_packet: dict[str, Any],
    change_request: dict[str, Any],
    candidate_config_freeze: dict[str, Any],
) -> dict[str, Any]:
    return (
        _dict(approval_gate.get("candidate_settings"))
        or _dict(review_packet.get("candidate_settings"))
        or _dict(change_request.get("requested_candidate_settings"))
        or _dict(candidate_config_freeze.get("candidate_settings"))
    )


def _proposed_candidate_settings(candidate_settings: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposed_candidate_threshold": candidate_settings.get("candidate_threshold"),
        "proposed_candidate_smoothing_window": candidate_settings.get(
            "candidate_smoothing_window"
        ),
        "proposed_candidate_hysteresis_settings": _dict(
            candidate_settings.get("candidate_hysteresis_settings")
        ),
        "candidate_type": candidate_settings.get("candidate_type", "not_applicable"),
        "candidate_source": _dict(candidate_settings.get("candidate_source")),
        "not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }


def _selected_candidate_ref(
    *,
    approval_gate: dict[str, Any],
    review_packet: dict[str, Any],
    change_request: dict[str, Any],
    candidate_config_freeze: dict[str, Any],
) -> dict[str, Any]:
    return (
        _dict(approval_gate.get("selected_candidate_config_ref"))
        or _dict(review_packet.get("selected_candidate_config_ref"))
        or _dict(change_request.get("selected_candidate_config_ref"))
        or _dict(candidate_config_freeze.get("selected_candidate_config_ref"))
    )


def _has_selected_candidate_ref(selected_candidate_ref: dict[str, Any]) -> bool:
    return any(value is not None for value in selected_candidate_ref.values())


def _has_candidate_settings(proposed_candidate_settings: dict[str, Any]) -> bool:
    return any(
        proposed_candidate_settings.get(key) is not None
        for key in (
            "proposed_candidate_threshold",
            "proposed_candidate_smoothing_window",
        )
    ) or bool(
        _dict(
            proposed_candidate_settings.get("proposed_candidate_hysteresis_settings")
        )
    )


def _rollback_context(review_packet: dict[str, Any]) -> dict[str, Any]:
    rollback_summary = _dict(review_packet.get("rollback_readiness_summary"))
    return {
        "source_rollback_readiness_summary": rollback_summary,
        "rollback_plan_present": rollback_summary.get("rollback_plan_present") is True,
        "rollback_plan_status": rollback_summary.get(
            "rollback_plan_status", "not_applicable"
        ),
        "rollback_readiness_status": rollback_summary.get(
            "rollback_readiness_status", "not_applicable"
        ),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
    }


def _required_regression_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate": "multi_point_regression_matrix",
            "required": True,
            "runtime_application_status": "not_applied",
        },
        {
            "gate": "protected_sample_point_reviewed_3d_debug",
            "required": True,
            "runtime_application_status": "not_applied",
        },
        {
            "gate": "gameplay_gate_regression_baseline",
            "required": True,
            "runtime_application_status": "not_applied",
        },
        {
            "gate": "review_guided_gameplay_calibration_sandbox_regression",
            "required": True,
            "runtime_application_status": "not_applied",
        },
    ]


def _required_operator_artifacts() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "human_approval_gate",
            "required": True,
            "runtime_application_status": "not_applied",
        },
        {
            "artifact": "operator_signoff_record",
            "required": True,
            "runtime_application_status": "not_applied",
        },
        {
            "artifact": "dry_run_review_packet",
            "required": True,
            "runtime_application_status": "not_applied",
        },
        {
            "artifact": "future_runtime_application_blueprint",
            "required": True,
            "runtime_application_status": "not_applied",
        },
    ]


def _requirement(name: str, present: bool) -> dict[str, Any]:
    return {
        "requirement": name,
        "status": "present" if present else "missing",
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
    }


def _prior_artifacts_preserve_no_mutation(inputs: dict[str, Any]) -> bool:
    source_presence = _dict(inputs.get("source_artifact_presence"))
    required = (
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


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    if (
        contract.get("contract_type")
        != CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_TYPE
    ):
        errors.append(_error("invalid_contract_type", "contract_type", None))
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_CONTRACT_VERSION
    ):
        errors.append(_error("invalid_contract_version", "contract_version", None))
    for section in (
        "application_plan_scope",
        "source_contract_refs",
        "application_plan_input_schema",
        "application_plan_schema",
        "config_delta_proposal_schema",
        "pre_application_gate_schema",
        "rollback_plan_schema",
        "post_application_verification_schema",
        "future_baseline_candidate_policy_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "application_plan_inputs")
    _require_fields(
        inputs,
        APPLICATION_PLAN_INPUT_REQUIRED_FIELDS,
        "application_plan_inputs",
        errors,
    )
    if (
        inputs.get("application_plan_input_type")
        != CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_application_plan_input_type",
                "application_plan_input_type",
                inputs.get("application_plan_input_type"),
            )
        )
    if (
        inputs.get("application_plan_input_version")
        != CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_application_plan_input_version",
                "application_plan_input_version",
                inputs.get("application_plan_input_version"),
            )
        )
    _validate_non_claims(inputs, errors, path="application_plan_inputs.non_claims")
    return errors


def _validate_plan_shape(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(plan, "application_plan")
    _require_fields(plan, APPLICATION_PLAN_REQUIRED_FIELDS, "application_plan", errors)
    if (
        plan.get("application_plan_type")
        != CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_TYPE
    ):
        errors.append(
            _error(
                "invalid_application_plan_type",
                "application_plan_type",
                plan.get("application_plan_type"),
            )
        )
    if (
        plan.get("application_plan_version")
        != CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION
    ):
        errors.append(
            _error(
                "invalid_application_plan_version",
                "application_plan_version",
                plan.get("application_plan_version"),
            )
        )
    _validate_required_no_mutation_statuses(plan, errors)
    _validate_required_bool(
        plan,
        "future_blueprint_required_for_runtime_application",
        True,
        errors,
    )
    _validate_allowed(
        plan.get("application_plan_status"),
        ALLOWED_APPLICATION_PLAN_STATUSES,
        "application_plan_status",
        errors,
    )
    _validate_allowed(
        plan.get("pre_application_gate_status"),
        ALLOWED_PRE_APPLICATION_GATE_STATUSES,
        "pre_application_gate_status",
        errors,
    )
    _validate_allowed(
        plan.get("rollback_plan_status"),
        ALLOWED_ROLLBACK_PLAN_STATUSES,
        "rollback_plan_status",
        errors,
    )
    _validate_allowed(
        plan.get("post_application_verification_status"),
        ALLOWED_POST_APPLICATION_VERIFICATION_STATUSES,
        "post_application_verification_status",
        errors,
    )
    _validate_allowed(
        plan.get("future_baseline_policy_status"),
        ALLOWED_FUTURE_BASELINE_POLICY_STATUSES,
        "future_baseline_policy_status",
        errors,
    )
    errors.extend(
        _validate_config_delta_shape(_dict(plan.get("config_delta_proposal")))
    )
    errors.extend(
        _validate_pre_application_gate_shape(_dict(plan.get("pre_application_gate")))
    )
    errors.extend(_validate_rollback_plan_shape(_dict(plan.get("rollback_plan"))))
    errors.extend(
        _validate_post_application_verification_shape(
            _dict(plan.get("post_application_verification_plan"))
        )
    )
    errors.extend(
        _validate_future_baseline_policy_shape(
            _dict(plan.get("future_baseline_candidate_policy"))
        )
    )
    _validate_non_claims(plan, errors, path="application_plan.non_claims")
    return errors


def _validate_config_delta_shape(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(proposal, "config_delta_proposal")
    _require_fields(
        proposal,
        CONFIG_DELTA_REQUIRED_FIELDS,
        "config_delta_proposal",
        errors,
    )
    if (
        proposal.get("config_delta_proposal_type")
        != CONTROLLED_RUNTIME_CALIBRATION_CONFIG_DELTA_PROPOSAL_TYPE
    ):
        errors.append(
            _error(
                "invalid_config_delta_proposal_type",
                "config_delta_proposal.config_delta_proposal_type",
                proposal.get("config_delta_proposal_type"),
            )
        )
    _validate_allowed(
        proposal.get("delta_status"),
        ALLOWED_CONFIG_DELTA_STATUSES,
        "config_delta_proposal.delta_status",
        errors,
    )
    _validate_required_status(
        proposal,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
        errors,
    )
    _validate_required_status(
        proposal,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_non_claims(proposal, errors, path="config_delta_proposal.non_claims")
    return errors


def _validate_pre_application_gate_shape(gate: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(gate, "pre_application_gate")
    _require_fields(
        gate,
        PRE_APPLICATION_GATE_REQUIRED_FIELDS,
        "pre_application_gate",
        errors,
    )
    _validate_allowed(
        gate.get("pre_application_gate_status"),
        ALLOWED_PRE_APPLICATION_GATE_STATUSES,
        "pre_application_gate.pre_application_gate_status",
        errors,
    )
    _validate_required_no_mutation_statuses(gate, errors)
    _validate_required_bool(
        gate,
        "future_blueprint_required_for_runtime_application",
        True,
        errors,
    )
    _validate_non_claims(gate, errors, path="pre_application_gate.non_claims")
    return errors


def _validate_rollback_plan_shape(rollback: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(rollback, "rollback_plan")
    _require_fields(rollback, ROLLBACK_PLAN_REQUIRED_FIELDS, "rollback_plan", errors)
    _validate_allowed(
        rollback.get("rollback_status"),
        ALLOWED_ROLLBACK_PLAN_STATUSES,
        "rollback_plan.rollback_status",
        errors,
    )
    _validate_required_status(
        rollback,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
        errors,
    )
    _validate_required_status(
        rollback,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_non_claims(rollback, errors, path="rollback_plan.non_claims")
    return errors


def _validate_post_application_verification_shape(
    verification_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(
        verification_plan,
        "post_application_verification_plan",
    )
    _require_fields(
        verification_plan,
        POST_APPLICATION_VERIFICATION_REQUIRED_FIELDS,
        "post_application_verification_plan",
        errors,
    )
    _validate_allowed(
        verification_plan.get("verification_status"),
        ALLOWED_POST_APPLICATION_VERIFICATION_STATUSES,
        "post_application_verification_plan.verification_status",
        errors,
    )
    _validate_non_claims(
        verification_plan,
        errors,
        path="post_application_verification_plan.non_claims",
    )
    return errors


def _validate_future_baseline_policy_shape(policy: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(policy, "future_baseline_candidate_policy")
    _require_fields(
        policy,
        FUTURE_BASELINE_POLICY_REQUIRED_FIELDS,
        "future_baseline_candidate_policy",
        errors,
    )
    _validate_allowed(
        policy.get("future_baseline_policy_status"),
        ALLOWED_FUTURE_BASELINE_POLICY_STATUSES,
        "future_baseline_candidate_policy.future_baseline_policy_status",
        errors,
    )
    _validate_non_claims(
        policy,
        errors,
        path="future_baseline_candidate_policy.non_claims",
    )
    return errors


def _validate_required_no_mutation_statuses(
    payload: dict[str, Any],
    errors: list[dict[str, Any]],
) -> None:
    _validate_required_status(
        payload,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
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
        ["not_created", "not_applicable"],
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
            errors.append(_error("missing_non_claim", f"{path}.{key}", None))


def _require_fields(
    payload: dict[str, Any],
    fields: list[str],
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    for field in fields:
        if field not in payload:
            errors.append(_error("missing_required_field", f"{path}.{field}", None))


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    contract = _load_required_json(contract_path, "contract", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    return contract


def _load_required_json(
    path: str | Path,
    label: str,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(path, label=label)
    if loaded.get("ok") is not True:
        errors.append(_error(f"missing_or_invalid_{label}", str(path), loaded))
        return {}
    return _dict(loaded.get("data"))


def _load_optional_json(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    loaded = _load_json(path, label=str(path))
    if loaded.get("ok") is not True:
        return {}
    return _dict(loaded.get("data"))


def _load_json(path: str | Path | None, *, label: str) -> dict[str, Any]:
    if path is None:
        return {
            "ok": False,
            "status": "missing",
            "label": label,
            "path": None,
            "error": f"{label} not provided",
        }
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return {
            "ok": False,
            "status": "missing",
            "label": label,
            "path": str(file_path),
            "error": f"{label} not found: {file_path}",
        }
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(file_path),
            "error": str(exc),
        }
    return {
        "ok": True,
        "status": "loaded",
        "label": label,
        "path": str(file_path),
        "data": data,
    }


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
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, result, result, result_key)
    return result


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
        "validation_version": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed statuses, and exact forbidden fields or values.",
            "Validation does not apply candidate settings or update runtime behavior.",
            "Validation does not score classifier output or infer tennis outcomes.",
        ],
    }
    if extra:
        result.update(extra)
    return result


def _forbidden_token_errors(value: Any, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_APPLICATION_PLAN_TOKENS:
                errors.append(_error("forbidden_field_or_value", child_path, key))
            errors.extend(_forbidden_token_errors(nested, child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_APPLICATION_PLAN_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, value))
    return errors


def _sha256_path(path: str | Path) -> str | None:
    file_path = Path(path)
    if not file_path.is_file():
        return None
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_id(prefix: str, *parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _write_json_if_requested(
    output_path: str | Path | None,
    payload: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None or not str(output_path).strip():
        return
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result[result_key] = str(path)


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "path": path, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_BLUEPRINT,
        "blueprint_name": CONTROLLED_RUNTIME_CALIBRATION_APPLICATION_PLAN_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _path_string(value: str | Path | None) -> str | None:
    if value is None:
        return None
    return str(Path(value))
