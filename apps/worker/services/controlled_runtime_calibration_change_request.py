from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.calibration_candidate_config_freeze import (
    CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION,
    DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_ARTIFACT_OUTPUT,
    DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT,
    DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT,
)
from apps.worker.services.calibration_candidate_config_freeze import (
    SOURCE_CONTRACT_REFS as CANDIDATE_CONFIG_FREEZE_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.calibration_candidate_decision_packet import (
    DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT,
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
    PROTECTED_BASELINE_REFS,
    REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION,
    REQUIRED_REGRESSION_GATES,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT,
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT,
)

CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_TYPE = (
    "controlled_runtime_calibration_change_request_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE = (
    "controlled_runtime_calibration_change_request_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE = (
    "controlled_runtime_calibration_change_request"
)
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE = (
    "controlled_runtime_calibration_change_request_dry_run"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_REPORT_TYPE = (
    "controlled_runtime_calibration_change_request_report"
)
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_BLUEPRINT = "blueprint_55"
CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_change_request_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_change_request_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_change_request_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_change_request_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_change_request_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_change_request.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_DRY_RUN_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_change_request_dry_run.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_DRY_RUN_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_change_request_dry_run.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_change_request.report.json"
)

CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "real_broadcast_gameplay_calibration_decision_phase_freeze_version": (
        REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_VERSION
    ),
    "calibration_candidate_config_freeze_contract_version": (
        CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION
    ),
    **dict(CANDIDATE_CONFIG_FREEZE_SOURCE_CONTRACT_REFS),
}

ALLOWED_CHANGE_REQUEST_STATUSES = [
    "draft_change_request",
    "ready_for_human_approval_review",
    "blocked_missing_manual_approval",
    "blocked_missing_candidate_config_freeze",
    "blocked_missing_regression_gate",
    "blocked_unresolved_review_gap",
    "blocked_invalid_candidate",
    "blocked_fixture_only_evidence",
    "blocked_missing_rollback_plan",
    "informational_only",
    "not_applicable",
]
ALLOWED_APPROVAL_STATUSES = [
    "human_approval_required",
    "awaiting_human_approval",
    "human_review_in_progress",
    "human_review_completed_no_runtime_action",
    "blocked_from_approval",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "not_applied",
    "runtime_application_not_supported_in_this_blueprint",
    "future_blueprint_required",
    "blocked_from_runtime_application",
    "not_applicable",
]
ALLOWED_CHANGE_REQUEST_DRY_RUN_STATUSES = [
    "dry_run_required",
    "dry_run_plan_created",
    "dry_run_blocked",
    "dry_run_not_executed",
    "not_applicable",
]
ALLOWED_ROLLBACK_PLAN_STATUSES = [
    "rollback_plan_required",
    "rollback_plan_created",
    "rollback_plan_blocked",
    "rollback_plan_not_executed",
    "not_applicable",
]
ALLOWED_REQUESTED_CHANGE_SCOPES = [
    "gameplay_gate_threshold_candidate",
    "gameplay_gate_smoothing_candidate",
    "gameplay_gate_hysteresis_candidate",
    "combined_gameplay_gate_candidate",
    "no_candidate_selected",
    "not_applicable",
]
ALLOWED_ROLLBACK_STATUSES = [
    "rollback_plan_created",
    "rollback_plan_required",
    "rollback_plan_blocked",
    "rollback_not_executed",
    "not_applicable",
]
ALLOWED_DRY_RUN_MODES = [
    "validate_only",
    "fixture_only",
    "structural_dry_run",
    "no_runtime_mutation",
    "not_applicable",
]
ALLOWED_DRY_RUN_RESULT_STATUSES = [
    "dry_run_plan_created",
    "dry_run_blocked_missing_approval",
    "dry_run_blocked_missing_regression_gate",
    "dry_run_blocked_invalid_candidate",
    "dry_run_not_executed",
    "completed_without_runtime_mutation",
    "not_applicable",
]

CHANGE_REQUEST_INPUT_REQUIRED_FIELDS = [
    "change_request_input_id",
    "change_request_input_type",
    "change_request_input_version",
    "generated_at",
    "source_phase_freeze_path",
    "source_candidate_config_freeze_path",
    "source_manual_approval_packet_path",
    "source_decision_packet_path",
    "source_sandbox_evaluation_report_path",
    "source_sandbox_regression_verification_path",
    "source_gameplay_gate_regression_baseline_path",
    "source_calibration_sandbox_baseline_path",
    "model_asset_ref",
    "model_asset_sha256",
    "current_threshold",
    "current_smoothing_window",
    "current_hysteresis_settings",
    "requested_candidate_settings",
    "requested_change_scope",
    "approval_context",
    "rollback_context",
    "warnings",
    "non_claims",
]
CHANGE_REQUEST_REQUIRED_FIELDS = [
    "change_request_id",
    "change_request_type",
    "change_request_version",
    "generated_at",
    "source_change_request_input_path",
    "source_phase_freeze_path",
    "source_candidate_config_freeze_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "requested_candidate_settings",
    "change_request_status",
    "approval_status",
    "runtime_application_status",
    "dry_run_required",
    "dry_run_status",
    "rollback_plan_required",
    "rollback_plan_status",
    "preconditions",
    "blockers",
    "required_regression_gates",
    "supporting_evidence_refs",
    "operator_approval_requirements",
    "rollback_plan",
    "warnings",
    "non_claims",
]
ROLLBACK_PLAN_REQUIRED_FIELDS = [
    "rollback_plan_id",
    "rollback_plan_version",
    "generated_at",
    "source_change_request_id",
    "rollback_scope",
    "rollback_target",
    "rollback_preconditions",
    "rollback_verification_gates",
    "rollback_status",
    "warnings",
    "non_claims",
]
DRY_RUN_REQUIRED_FIELDS = [
    "dry_run_id",
    "dry_run_type",
    "dry_run_version",
    "generated_at",
    "source_change_request_id",
    "dry_run_mode",
    "dry_run_status",
    "dry_run_inputs",
    "expected_structural_changes",
    "regression_gate_requirements",
    "rollback_plan_ref",
    "rollback_plan",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "change_request_is_not_truth": True,
    "change_request_is_not_accuracy_scoring": True,
    "change_request_is_not_runtime_calibration": True,
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
    "human_operator_approval_required": True,
    "future_blueprint_required_for_runtime_application": True,
    "classifier_correctness_not_assessed": True,
}
WARNINGS = {
    **dict(NON_CLAIMS),
    "controlled_change_request": True,
    "human_approval_required": True,
    "rollback_plan_required": True,
    "dry_run_required": True,
    "runtime_application_status_not_applied": True,
    "future_blueprint_required_for_runtime_application": True,
    "no_runtime_mutation": True,
    "structural_dry_run": True,
    "review_support_only": True,
    "provenance_only": True,
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
FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS = {
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
    "production_config",
    "production_config_created",
    "runtime_application_performed",
}


def export_controlled_runtime_calibration_change_request_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    errors = _validate_contract_shape(contract)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_TYPE,
        "contract_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION,
        "contract": contract,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_controlled_runtime_calibration_change_request_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    source_phase_freeze_path: str | Path = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT
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
    source_sandbox_evaluation_report_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    source_sandbox_regression_verification_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT
    ),
    source_gameplay_gate_regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    source_calibration_sandbox_baseline_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    phase_freeze = _load_required_json(source_phase_freeze_path, "phase_freeze", errors)
    candidate_config_freeze = _load_required_json(
        source_candidate_config_freeze_path,
        "candidate_config_freeze",
        errors,
    )
    manual_approval_packet = _load_optional_json(source_manual_approval_packet_path)
    decision_packet = _load_optional_json(source_decision_packet_path)
    sandbox_evaluation_report = _load_optional_json(source_sandbox_evaluation_report_path)
    sandbox_regression_verification = _load_optional_json(
        source_sandbox_regression_verification_path
    )
    gameplay_gate_regression_baseline = _load_optional_json(
        source_gameplay_gate_regression_baseline_path
    )
    calibration_sandbox_baseline = _load_optional_json(
        source_calibration_sandbox_baseline_path
    )
    if errors:
        return _failed_result(
            status="invalid_change_request_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE,
            result_key="change_request_inputs_output",
        )

    current_settings = _current_settings(candidate_config_freeze)
    requested_candidate_settings = _requested_candidate_settings(candidate_config_freeze)
    requested_change_scope = _requested_change_scope(requested_candidate_settings)
    source_payloads = {
        "phase_freeze": phase_freeze,
        "candidate_config_freeze": candidate_config_freeze,
        "manual_approval_packet": manual_approval_packet,
        "decision_packet": decision_packet,
        "sandbox_evaluation_report": sandbox_evaluation_report,
        "sandbox_regression_verification": sandbox_regression_verification,
        "gameplay_gate_regression_baseline": gameplay_gate_regression_baseline,
        "calibration_sandbox_baseline": calibration_sandbox_baseline,
    }
    model_asset_sha256 = _sha256_path(model_asset_path)
    inputs = {
        "change_request_input_id": _stable_id(
            "controlled_runtime_calibration_change_request_inputs_v1",
            _path_string(source_phase_freeze_path),
            _path_string(source_candidate_config_freeze_path),
            candidate_config_freeze.get("candidate_config_freeze_id"),
            model_asset_sha256,
            requested_change_scope,
        ),
        "change_request_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE
        ),
        "change_request_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_phase_freeze_path": str(Path(source_phase_freeze_path)),
        "source_candidate_config_freeze_path": str(
            Path(source_candidate_config_freeze_path)
        ),
        "source_manual_approval_packet_path": _path_string(
            source_manual_approval_packet_path
        ),
        "source_decision_packet_path": _path_string(source_decision_packet_path),
        "source_sandbox_evaluation_report_path": _path_string(
            source_sandbox_evaluation_report_path
        ),
        "source_sandbox_regression_verification_path": _path_string(
            source_sandbox_regression_verification_path
        ),
        "source_gameplay_gate_regression_baseline_path": _path_string(
            source_gameplay_gate_regression_baseline_path
        ),
        "source_calibration_sandbox_baseline_path": _path_string(
            source_calibration_sandbox_baseline_path
        ),
        "source_phase_freeze_id": phase_freeze.get("freeze_type"),
        "source_candidate_config_freeze_id": candidate_config_freeze.get(
            "candidate_config_freeze_id"
        ),
        "source_manual_approval_packet_id": manual_approval_packet.get(
            "manual_approval_packet_id"
        ),
        "source_decision_packet_id": decision_packet.get("decision_packet_id"),
        "model_asset_ref": str(Path(model_asset_path)),
        "model_asset_sha256": model_asset_sha256,
        "current_threshold": current_settings.get("current_threshold"),
        "current_smoothing_window": current_settings.get("current_smoothing_window"),
        "current_hysteresis_settings": _dict(
            current_settings.get("current_hysteresis_settings")
        ),
        "current_settings": current_settings,
        "requested_candidate_settings": requested_candidate_settings,
        "requested_change_scope": requested_change_scope,
        "approval_context": _approval_context(
            candidate_config_freeze=candidate_config_freeze,
            manual_approval_packet=manual_approval_packet,
        ),
        "rollback_context": _rollback_context(current_settings=current_settings),
        "required_regression_gates": list(REQUIRED_REGRESSION_GATES),
        "supporting_evidence_refs": _supporting_evidence_refs(
            phase_freeze=phase_freeze,
            candidate_config_freeze=candidate_config_freeze,
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_presence": _source_artifact_presence(source_payloads),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_inputs_shape(inputs)
    if validation_errors:
        return _failed_result(
            status="invalid_change_request_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE,
            result_key="change_request_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "change_request_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE
        ),
        "change_request_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_VERSION
        ),
        "change_request_input_id": inputs["change_request_input_id"],
        "requested_change_scope": inputs["requested_change_scope"],
        "runtime_application_status": "not_applied",
        "change_request_inputs": inputs,
        "warnings": inputs["warnings"],
    }
    _write_json_if_requested(output_path, inputs, result, "change_request_inputs_output")
    return result


def validate_controlled_runtime_calibration_change_request_inputs(
    *,
    change_request_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(change_request_inputs_path, "change_request_inputs", errors)
    if inputs:
        errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_change_request_inputs_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=change_request_inputs_path,
        payload_type=inputs.get("change_request_input_type") if inputs else None,
        payload_version=inputs.get("change_request_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_change_request(
    *,
    change_request_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_EXPORTED_AT
    validation = validate_controlled_runtime_calibration_change_request_inputs(
        change_request_inputs_path=change_request_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_change_request_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE,
            result_key="change_request_output",
        )
    inputs = _dict(
        _load_json(
            change_request_inputs_path,
            label="change_request_inputs",
        ).get("data")
    )
    change_request_status = _change_request_status(inputs)
    blockers = _blockers(inputs=inputs, change_request_status=change_request_status)
    rollback_plan = _rollback_plan(
        change_request_id=_stable_id(
            "controlled_runtime_calibration_change_request_v1",
            inputs.get("change_request_input_id"),
            inputs.get("requested_change_scope"),
            inputs.get("model_asset_sha256"),
        ),
        generated_at=generated_at,
        current_settings=_dict(inputs.get("current_settings")),
    )
    change_request = {
        "change_request_id": rollback_plan["source_change_request_id"],
        "change_request_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE,
        "change_request_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_change_request_input_path": str(Path(change_request_inputs_path)),
        "source_phase_freeze_path": inputs.get("source_phase_freeze_path"),
        "source_candidate_config_freeze_path": inputs.get(
            "source_candidate_config_freeze_path"
        ),
        "source_manual_approval_packet_path": inputs.get(
            "source_manual_approval_packet_path"
        ),
        "selected_candidate_config_ref": _dict(
            _dict(inputs.get("requested_candidate_settings")).get("candidate_source")
        ),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "current_settings": _dict(inputs.get("current_settings")),
        "requested_candidate_settings": _dict(
            inputs.get("requested_candidate_settings")
        ),
        "requested_change_scope": inputs.get("requested_change_scope"),
        "change_request_status": change_request_status,
        "approval_status": "human_approval_required",
        "runtime_application_status": "not_applied",
        "dry_run_required": True,
        "dry_run_status": "dry_run_plan_created",
        "rollback_plan_required": True,
        "rollback_plan_status": "rollback_plan_created",
        "preconditions": _preconditions(inputs),
        "blockers": blockers,
        "required_regression_gates": _list(inputs.get("required_regression_gates")),
        "supporting_evidence_refs": _dict(inputs.get("supporting_evidence_refs")),
        "operator_approval_requirements": _operator_approval_requirements(inputs),
        "approval_context": _dict(inputs.get("approval_context")),
        "rollback_plan": rollback_plan,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(inputs.get("warnings")),
            **dict(WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_change_request_shape(change_request)
    if validation_errors:
        return _failed_result(
            status="invalid_change_request",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE,
            result_key="change_request_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "change_request_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE,
        "change_request_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
        "change_request_id": change_request["change_request_id"],
        "change_request_status": change_request["change_request_status"],
        "approval_status": change_request["approval_status"],
        "runtime_application_status": change_request["runtime_application_status"],
        "dry_run_required": change_request["dry_run_required"],
        "rollback_plan_required": change_request["rollback_plan_required"],
        "change_request": change_request,
        "warnings": change_request["warnings"],
    }
    _write_json_if_requested(output_path, change_request, result, "change_request_output")
    return result


def validate_controlled_runtime_calibration_change_request(
    *,
    change_request_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VALIDATION_OUTPUT
    ),
    repo_root: str | Path = ".",
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    change_request = _load_required_json(
        change_request_path,
        "controlled_runtime_calibration_change_request",
        errors,
    )
    if change_request:
        errors.extend(_validate_change_request_shape(change_request))
    ref_validations = _validate_expected_tracked_refs(repo_root=repo_root)
    for validation in ref_validations:
        if validation["ok"] is not True:
            errors.append(_error("missing_or_untracked_ref", validation["path"], validation))
    clean_validations = _tracked_refs_clean(repo_root=repo_root)
    for validation in clean_validations:
        if validation["clean"] is not True:
            errors.append(_error("tracked_ref_dirty", validation["path"], validation))
    model_asset_validation = _validate_model_asset(repo_root=repo_root)
    if model_asset_validation["ok"] is not True:
        errors.append(
            _error(
                "model_asset_committed_or_modified",
                DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
                model_asset_validation,
            )
        )
    tracked_exports = _tracked_files(".data/exports", repo_root=repo_root)
    if tracked_exports:
        errors.append(_error("generated_exports_tracked", ".data/exports", tracked_exports))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_change_request_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=change_request_path,
        payload_type=change_request.get("change_request_type") if change_request else None,
        payload_version=(
            change_request.get("change_request_version") if change_request else None
        ),
        errors=errors,
        extra={
            "runtime_application_status": change_request.get(
                "runtime_application_status"
            )
            if change_request
            else None,
            "approval_status": change_request.get("approval_status")
            if change_request
            else None,
            "dry_run_required": change_request.get("dry_run_required")
            if change_request
            else None,
            "rollback_plan_required": change_request.get("rollback_plan_required")
            if change_request
            else None,
            "tracked_ref_validations": ref_validations,
            "tracked_contract_baseline_clean_validations": clean_validations,
            "gameplay_classifier_asset_validation": model_asset_validation,
            "tracked_exports": tracked_exports,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_change_request_dry_run(
    *,
    change_request_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_DRY_RUN_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_change_request(
        change_request_path=change_request_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_change_request",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE,
            result_key="dry_run_output",
        )
    change_request = _dict(
        _load_json(change_request_path, label="change_request").get("data")
    )
    rollback_plan = _dict(change_request.get("rollback_plan"))
    dry_run = {
        "dry_run_id": _stable_id(
            "controlled_runtime_calibration_change_request_dry_run_v1",
            change_request.get("change_request_id"),
            change_request.get("model_asset_sha256"),
        ),
        "dry_run_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE,
        "dry_run_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_change_request_id": change_request.get("change_request_id"),
        "source_change_request_path": str(Path(change_request_path)),
        "dry_run_mode": "structural_dry_run",
        "dry_run_status": "dry_run_plan_created",
        "dry_run_inputs": {
            "current_settings": _dict(change_request.get("current_settings")),
            "requested_candidate_settings": _dict(
                change_request.get("requested_candidate_settings")
            ),
            "requested_change_scope": change_request.get("requested_change_scope"),
            "runtime_application_status": "not_applied",
            "no_runtime_mutation": True,
        },
        "expected_structural_changes": {
            "runtime_config_changes": False,
            "threshold_changes": False,
            "smoothing_changes": False,
            "hysteresis_changes": False,
            "model_asset_changes": False,
            "baseline_changes": False,
            "generated_review_artifacts_only": True,
        },
        "regression_gate_requirements": _list(
            change_request.get("required_regression_gates")
        ),
        "rollback_plan_ref": {
            "rollback_plan_id": rollback_plan.get("rollback_plan_id"),
            "rollback_plan_status": rollback_plan.get("rollback_status"),
        },
        "rollback_plan": rollback_plan,
        "validation_snapshot": validation,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(change_request.get("warnings")),
            **dict(WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_dry_run_shape(dry_run)
    if validation_errors:
        return _failed_result(
            status="invalid_dry_run",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE,
            result_key="dry_run_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "dry_run_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE,
        "dry_run_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_VERSION,
        "dry_run_id": dry_run["dry_run_id"],
        "dry_run_status": dry_run["dry_run_status"],
        "runtime_application_status": "not_applied",
        "dry_run": dry_run,
        "rollback_plan": rollback_plan,
        "warnings": dry_run["warnings"],
    }
    _write_json_if_requested(output_path, dry_run, result, "dry_run_output")
    return result


def validate_controlled_runtime_calibration_change_request_dry_run(
    *,
    dry_run_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_DRY_RUN_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    dry_run = _load_required_json(dry_run_path, "dry_run", errors)
    if dry_run:
        errors.extend(_validate_dry_run_shape(dry_run))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_change_request_dry_run_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=dry_run_path,
        payload_type=dry_run.get("dry_run_type") if dry_run else None,
        payload_version=dry_run.get("dry_run_version") if dry_run else None,
        errors=errors,
        extra={
            "dry_run_status": dry_run.get("dry_run_status") if dry_run else None,
            "rollback_plan_status": _dict(dry_run.get("rollback_plan")).get(
                "rollback_status"
            )
            if dry_run
            else None,
            "runtime_application_status": "not_applied" if dry_run else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_change_request_report(
    *,
    change_request_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT
    ),
    dry_run_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_DRY_RUN_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    change_request_validation = validate_controlled_runtime_calibration_change_request(
        change_request_path=change_request_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    dry_run_validation = validate_controlled_runtime_calibration_change_request_dry_run(
        dry_run_path=dry_run_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    change_request = _dict(
        _load_json(change_request_path, label="change_request").get("data")
    )
    dry_run = _dict(_load_json(dry_run_path, label="dry_run").get("data"))
    errors = [
        *_list(change_request_validation.get("errors")),
        *_list(dry_run_validation.get("errors")),
    ]
    report = {
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_change_request_path": str(Path(change_request_path)),
        "source_dry_run_path": str(Path(dry_run_path)),
        "change_request_id": change_request.get("change_request_id"),
        "dry_run_id": dry_run.get("dry_run_id"),
        "summary": {
            "change_request_status": change_request.get("change_request_status"),
            "approval_status": change_request.get("approval_status"),
            "runtime_application_status": "not_applied",
            "dry_run_status": dry_run.get("dry_run_status"),
            "rollback_plan_status": _dict(dry_run.get("rollback_plan")).get(
                "rollback_status"
            ),
            "required_regression_gate_count": len(
                _list(change_request.get("required_regression_gates"))
            ),
            "blocker_count": len(_list(change_request.get("blockers"))),
            "change_request_validation_status": change_request_validation.get("status"),
            "change_request_validation_error_count": change_request_validation.get(
                "error_count"
            ),
            "dry_run_validation_status": dry_run_validation.get("status"),
            "dry_run_validation_error_count": dry_run_validation.get("error_count"),
        },
        "change_request_snapshot": change_request,
        "dry_run_snapshot": dry_run,
        "change_request_validation_snapshot": change_request_validation,
        "dry_run_validation_snapshot": dry_run_validation,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(change_request.get("warnings")),
            **_dict(dry_run.get("warnings")),
            **dict(WARNINGS),
            "report_is_change_request_review_only": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors.extend(_forbidden_token_errors(report, "report"))
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_report",
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
        "change_request_id": change_request.get("change_request_id"),
        "dry_run_id": dry_run.get("dry_run_id"),
        "error_count": len(errors),
        "errors": errors,
        "summary": report["summary"],
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_TYPE,
        "contract_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "change_request_scope": {
            "purpose": "controlled_runtime_calibration_change_request",
            "creates_reviewable_change_request": True,
            "creates_structural_dry_run_plan": True,
            "creates_rollback_plan": True,
            "requires_human_approval": True,
            "requires_regression_gates": True,
            "requires_rollback_plan": True,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "updates_runtime_configuration": False,
            "updates_model_weights": False,
            "mutates_regression_baselines": False,
            "automatic_approval_allowed": False,
            "automatic_rejection_allowed": False,
            "creates_deployable_configuration": False,
            "calculates_classifier_correctness": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "change_request_input_schema": {
            "change_request_input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE
            ),
            "change_request_input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_VERSION
            ),
            "required_fields": list(CHANGE_REQUEST_INPUT_REQUIRED_FIELDS),
            "allowed_requested_change_scopes": list(ALLOWED_REQUESTED_CHANGE_SCOPES),
        },
        "change_request_schema": {
            "change_request_type": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE,
            "change_request_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
            "required_fields": list(CHANGE_REQUEST_REQUIRED_FIELDS),
            "allowed_change_request_statuses": list(ALLOWED_CHANGE_REQUEST_STATUSES),
            "allowed_approval_statuses": list(ALLOWED_APPROVAL_STATUSES),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_dry_run_statuses": list(ALLOWED_CHANGE_REQUEST_DRY_RUN_STATUSES),
            "allowed_rollback_plan_statuses": list(ALLOWED_ROLLBACK_PLAN_STATUSES),
            "requires_runtime_application_status": "not_applied",
            "requires_approval_status": "human_approval_required",
            "requires_dry_run_required": True,
            "requires_rollback_plan_required": True,
        },
        "dry_run_schema": {
            "dry_run_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE,
            "dry_run_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_VERSION,
            "required_fields": list(DRY_RUN_REQUIRED_FIELDS),
            "allowed_dry_run_modes": list(ALLOWED_DRY_RUN_MODES),
            "allowed_dry_run_result_statuses": list(ALLOWED_DRY_RUN_RESULT_STATUSES),
        },
        "rollback_plan_schema": {
            "required_fields": list(ROLLBACK_PLAN_REQUIRED_FIELDS),
            "allowed_rollback_statuses": list(ALLOWED_ROLLBACK_STATUSES),
        },
        "approval_requirements_schema": {
            "human_operator_approval_required": True,
            "automatic_approval_allowed": False,
            "automatic_rejection_allowed": False,
            "future_blueprint_required_for_runtime_application": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_change_request_input_shape": True,
            "validate_change_request_shape": True,
            "validate_dry_run_shape": True,
            "validate_rollback_plan_shape": True,
            "validate_approval_requirements": True,
            "validate_allowed_statuses": True,
            "validate_allowed_requested_change_scopes": True,
            "validate_runtime_application_status": True,
            "validate_approval_status_requires_human_approval": True,
            "validate_dry_run_required": True,
            "validate_rollback_plan_required": True,
            "validate_referenced_contracts_where_available": True,
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
            "source_phase_freeze_path_required": True,
            "source_candidate_config_freeze_path_required": True,
            "source_manual_approval_packet_path_recorded_when_available": True,
            "source_decision_packet_path_recorded_when_available": True,
            "model_asset_ref_required": True,
            "model_asset_sha256_when_available": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _current_settings(candidate_config_freeze: dict[str, Any]) -> dict[str, Any]:
    settings = _dict(candidate_config_freeze.get("current_settings"))
    hysteresis = _dict(settings.get("current_hysteresis_settings"))
    return {
        "current_threshold": settings.get("current_threshold", DEFAULT_THRESHOLD),
        "current_smoothing_window": settings.get(
            "current_smoothing_window",
            DEFAULT_SMOOTHING_WINDOW,
        ),
        "current_hysteresis_settings": {
            "enter_gameplay_probability": hysteresis.get(
                "enter_gameplay_probability",
                DEFAULT_HYSTERESIS_ENTER,
            ),
            "exit_gameplay_probability": hysteresis.get(
                "exit_gameplay_probability",
                DEFAULT_HYSTERESIS_EXIT,
            ),
        },
        "runtime_application_status": "not_applied",
    }


def _requested_candidate_settings(
    candidate_config_freeze: dict[str, Any],
) -> dict[str, Any]:
    settings = _dict(candidate_config_freeze.get("candidate_settings"))
    return {
        "candidate_threshold": settings.get("candidate_threshold"),
        "candidate_smoothing_window": settings.get("candidate_smoothing_window"),
        "candidate_hysteresis_settings": _dict(
            settings.get("candidate_hysteresis_settings")
        ),
        "candidate_type": settings.get("candidate_type", "not_applicable"),
        "candidate_source": _dict(settings.get("candidate_source")),
        "not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }


def _requested_change_scope(requested_candidate_settings: dict[str, Any]) -> str:
    candidate_type = str(requested_candidate_settings.get("candidate_type") or "")
    if candidate_type == "threshold_candidate":
        return "gameplay_gate_threshold_candidate"
    if candidate_type == "smoothing_window_candidate":
        return "gameplay_gate_smoothing_candidate"
    if candidate_type == "hysteresis_candidate":
        return "gameplay_gate_hysteresis_candidate"
    if candidate_type == "combined_candidate":
        return "combined_gameplay_gate_candidate"
    if candidate_type in {"not_applicable", "no_candidate", ""}:
        return "no_candidate_selected"
    return "not_applicable"


def _approval_context(
    *,
    candidate_config_freeze: dict[str, Any],
    manual_approval_packet: dict[str, Any],
) -> dict[str, Any]:
    return {
        "candidate_config_status": candidate_config_freeze.get(
            "candidate_config_status",
            "not_applicable",
        ),
        "source_manual_approval_status": candidate_config_freeze.get(
            "manual_approval_status",
            "not_applicable",
        ),
        "source_candidate_approval_required": candidate_config_freeze.get(
            "approval_required"
        )
        is True,
        "manual_approval_packet_present": bool(manual_approval_packet),
        "manual_approval_packet_id": manual_approval_packet.get(
            "manual_approval_packet_id"
        ),
        "human_operator_approval_required": True,
        "automatic_approval_occurred": False,
        "automatic_rejection_occurred": False,
        "runtime_application_status": "not_applied",
    }


def _rollback_context(*, current_settings: dict[str, Any]) -> dict[str, Any]:
    return {
        "rollback_plan_required": True,
        "rollback_scope": "no_runtime_mutation",
        "rollback_target": {
            "current_settings": current_settings,
            "runtime_application_status": "not_applied",
        },
        "rollback_status": "rollback_plan_created",
    }


def _supporting_evidence_refs(
    *,
    phase_freeze: dict[str, Any],
    candidate_config_freeze: dict[str, Any],
) -> dict[str, Any]:
    candidate_supporting_refs = _dict(
        candidate_config_freeze.get("supporting_evidence_refs")
    )
    return {
        "source_phase_freeze_contract_refs": _list(
            phase_freeze.get("frozen_contract_refs")
        ),
        "source_protected_baseline_refs": _list(
            phase_freeze.get("protected_baseline_refs")
        ),
        "candidate_supporting_evidence_refs": candidate_supporting_refs,
        "candidate_config_freeze_id": candidate_config_freeze.get(
            "candidate_config_freeze_id"
        ),
        "selected_candidate_packet_ref": candidate_config_freeze.get(
            "selected_candidate_packet_ref"
        ),
    }


def _source_artifact_presence(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        name: {
            "present": bool(payload),
            "artifact_type": _artifact_type(payload),
        }
        for name, payload in source_payloads.items()
    }


def _artifact_type(payload: dict[str, Any]) -> str | None:
    for key in (
        "freeze_type",
        "candidate_config_freeze_type",
        "manual_approval_packet_type",
        "decision_packet_type",
        "report_type",
        "baseline_type",
        "verification_type",
    ):
        value = payload.get(key)
        if value:
            return str(value)
    return None


def _merged_warnings(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for payload in source_payloads.values():
        warnings = _dict(payload.get("warnings"))
        for key, value in warnings.items():
            merged[key] = value
    merged.update(WARNINGS)
    return merged


def _change_request_status(inputs: dict[str, Any]) -> str:
    approval_context = _dict(inputs.get("approval_context"))
    requested_change_scope = str(inputs.get("requested_change_scope") or "")
    candidate_status = str(approval_context.get("candidate_config_status") or "")
    if requested_change_scope == "no_candidate_selected":
        return "informational_only"
    if not inputs.get("source_candidate_config_freeze_id"):
        return "blocked_missing_candidate_config_freeze"
    if candidate_status == "blocked_fixture_only_data":
        return "blocked_fixture_only_evidence"
    if candidate_status == "blocked_invalid_candidate":
        return "blocked_invalid_candidate"
    if candidate_status in {
        "blocked_missing_review_data",
        "blocked_insufficient_sample_size",
        "blocked_regression_drift",
    }:
        return "blocked_unresolved_review_gap"
    if (
        approval_context.get("source_candidate_approval_required") is True
        and approval_context.get("manual_approval_packet_present") is not True
    ):
        return "blocked_missing_manual_approval"
    if candidate_status == "frozen_for_manual_review":
        return "ready_for_human_approval_review"
    return "draft_change_request"


def _blockers(*, inputs: dict[str, Any], change_request_status: str) -> list[str]:
    blockers = {"human_operator_approval_required"}
    requested_change_scope = str(inputs.get("requested_change_scope") or "")
    if requested_change_scope == "no_candidate_selected":
        blockers.add("no_candidate_selected")
    if change_request_status.startswith("blocked_"):
        blockers.add(change_request_status)
    approval_context = _dict(inputs.get("approval_context"))
    if approval_context.get("source_candidate_approval_required") is True:
        blockers.add("manual_approval_review_required")
    if not _list(inputs.get("required_regression_gates")):
        blockers.add("missing_regression_gate")
    return sorted(blockers)


def _preconditions(inputs: dict[str, Any]) -> list[str]:
    preconditions = {
        "review_source_phase_freeze",
        "review_candidate_config_freeze",
        "review_manual_approval_packet_when_available",
        "review_regression_gates",
        "review_non_claims",
        "confirm_no_runtime_application",
        "confirm_model_weights_unchanged",
        "confirm_baselines_unchanged",
        "confirm_human_approval_required",
        "prepare_structural_dry_run",
        "prepare_rollback_plan",
    }
    if inputs.get("requested_change_scope") == "no_candidate_selected":
        preconditions.add("select_candidate_before_future_runtime_application")
    return sorted(preconditions)


def _operator_approval_requirements(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "approval_status": "human_approval_required",
        "human_operator_approval_required": True,
        "manual_packet_review_required": True,
        "dry_run_review_required": True,
        "rollback_plan_review_required": True,
        "all_regression_gates_required": True,
        "runtime_application_status": "not_applied",
        "future_blueprint_required_for_runtime_application": True,
        "requested_change_scope": inputs.get("requested_change_scope"),
        "automatic_approval_allowed": False,
        "automatic_rejection_allowed": False,
    }


def _rollback_plan(
    *,
    change_request_id: str,
    generated_at: datetime,
    current_settings: dict[str, Any],
) -> dict[str, Any]:
    return {
        "rollback_plan_id": _stable_id(
            "controlled_runtime_calibration_rollback_plan_v1",
            change_request_id,
            current_settings,
        ),
        "rollback_plan_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_change_request_id": change_request_id,
        "rollback_scope": "no_runtime_mutation",
        "rollback_target": {
            "current_settings": current_settings,
            "runtime_application_status": "not_applied",
        },
        "rollback_preconditions": [
            "runtime_application_status_must_be_not_applied",
            "model_weights_must_remain_unchanged",
            "baselines_must_remain_unchanged",
            "threshold_changes_must_remain_not_applied",
            "smoothing_changes_must_remain_not_applied",
            "hysteresis_changes_must_remain_not_applied",
        ],
        "rollback_verification_gates": list(REQUIRED_REGRESSION_GATES),
        "rollback_status": "rollback_plan_created",
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    if (
        contract.get("contract_type")
        != CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_TYPE
    ):
        errors.append(_error("invalid_contract_type", "contract_type", None))
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION
    ):
        errors.append(_error("invalid_contract_version", "contract_version", None))
    for section in (
        "change_request_scope",
        "source_contract_refs",
        "change_request_input_schema",
        "change_request_schema",
        "dry_run_schema",
        "rollback_plan_schema",
        "approval_requirements_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "change_request_inputs")
    _require_fields(
        inputs,
        CHANGE_REQUEST_INPUT_REQUIRED_FIELDS,
        "change_request_inputs",
        errors,
    )
    if (
        inputs.get("change_request_input_type")
        != CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_change_request_input_type",
                "change_request_input_type",
                inputs.get("change_request_input_type"),
            )
        )
    if (
        inputs.get("change_request_input_version")
        != CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_change_request_input_version",
                "change_request_input_version",
                inputs.get("change_request_input_version"),
            )
        )
    if inputs.get("requested_change_scope") not in ALLOWED_REQUESTED_CHANGE_SCOPES:
        errors.append(
            _error(
                "invalid_requested_change_scope",
                "requested_change_scope",
                inputs.get("requested_change_scope"),
            )
        )
    _validate_non_claims(inputs, errors, path="change_request_inputs.non_claims")
    return errors


def _validate_change_request_shape(change_request: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(change_request, "change_request")
    _require_fields(
        change_request,
        CHANGE_REQUEST_REQUIRED_FIELDS,
        "change_request",
        errors,
    )
    if (
        change_request.get("change_request_type")
        != CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TYPE
    ):
        errors.append(
            _error(
                "invalid_change_request_type",
                "change_request_type",
                change_request.get("change_request_type"),
            )
        )
    if (
        change_request.get("change_request_version")
        != CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION
    ):
        errors.append(
            _error(
                "invalid_change_request_version",
                "change_request_version",
                change_request.get("change_request_version"),
            )
        )
    if change_request.get("change_request_status") not in ALLOWED_CHANGE_REQUEST_STATUSES:
        errors.append(
            _error(
                "invalid_change_request_status",
                "change_request_status",
                change_request.get("change_request_status"),
            )
        )
    if change_request.get("approval_status") != "human_approval_required":
        errors.append(
            _error(
                "approval_status_must_require_human_approval",
                "approval_status",
                change_request.get("approval_status"),
            )
        )
    if change_request.get("runtime_application_status") != "not_applied":
        errors.append(
            _error(
                "runtime_application_status_must_remain_not_applied",
                "runtime_application_status",
                change_request.get("runtime_application_status"),
            )
        )
    if change_request.get("dry_run_required") is not True:
        errors.append(
            _error("dry_run_required_must_be_true", "dry_run_required", None)
        )
    if change_request.get("rollback_plan_required") is not True:
        errors.append(
            _error(
                "rollback_plan_required_must_be_true",
                "rollback_plan_required",
                None,
            )
        )
    if change_request.get("dry_run_status") not in ALLOWED_CHANGE_REQUEST_DRY_RUN_STATUSES:
        errors.append(
            _error(
                "invalid_dry_run_status",
                "dry_run_status",
                change_request.get("dry_run_status"),
            )
        )
    if change_request.get("rollback_plan_status") not in ALLOWED_ROLLBACK_PLAN_STATUSES:
        errors.append(
            _error(
                "invalid_rollback_plan_status",
                "rollback_plan_status",
                change_request.get("rollback_plan_status"),
            )
        )
    if change_request.get("requested_change_scope") not in ALLOWED_REQUESTED_CHANGE_SCOPES:
        errors.append(
            _error(
                "invalid_requested_change_scope",
                "requested_change_scope",
                change_request.get("requested_change_scope"),
            )
        )
    errors.extend(
        _validate_rollback_plan_shape(_dict(change_request.get("rollback_plan")))
    )
    _validate_non_claims(change_request, errors, path="change_request.non_claims")
    return errors


def _validate_rollback_plan_shape(rollback_plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(rollback_plan, "rollback_plan")
    _require_fields(rollback_plan, ROLLBACK_PLAN_REQUIRED_FIELDS, "rollback_plan", errors)
    if rollback_plan.get("rollback_status") not in ALLOWED_ROLLBACK_STATUSES:
        errors.append(
            _error(
                "invalid_rollback_status",
                "rollback_status",
                rollback_plan.get("rollback_status"),
            )
        )
    _validate_non_claims(rollback_plan, errors, path="rollback_plan.non_claims")
    return errors


def _validate_dry_run_shape(dry_run: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(dry_run, "dry_run")
    _require_fields(dry_run, DRY_RUN_REQUIRED_FIELDS, "dry_run", errors)
    if dry_run.get("dry_run_type") != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_TYPE:
        errors.append(
            _error(
                "invalid_dry_run_type",
                "dry_run_type",
                dry_run.get("dry_run_type"),
            )
        )
    if dry_run.get("dry_run_version") != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_VERSION:
        errors.append(
            _error(
                "invalid_dry_run_version",
                "dry_run_version",
                dry_run.get("dry_run_version"),
            )
        )
    if dry_run.get("dry_run_mode") not in ALLOWED_DRY_RUN_MODES:
        errors.append(
            _error(
                "invalid_dry_run_mode",
                "dry_run_mode",
                dry_run.get("dry_run_mode"),
            )
        )
    if dry_run.get("dry_run_status") not in ALLOWED_DRY_RUN_RESULT_STATUSES:
        errors.append(
            _error(
                "invalid_dry_run_status",
                "dry_run_status",
                dry_run.get("dry_run_status"),
            )
        )
    errors.extend(_validate_rollback_plan_shape(_dict(dry_run.get("rollback_plan"))))
    _validate_non_claims(dry_run, errors, path="dry_run.non_claims")
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


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
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
        "validation_version": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
        "known_limitations": [
            "Validation checks structure, allowed statuses, required guardrails, "
            "tracked refs where applicable, and exact forbidden fields or values.",
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
            if str(key) in FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS:
                errors.append(_error("forbidden_field_or_value", child_path, key))
            errors.extend(_forbidden_token_errors(nested, child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif (
        isinstance(value, str)
        and value in FORBIDDEN_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_TOKENS
    ):
        errors.append(_error("forbidden_field_or_value", path, value))
    return errors


def _validate_expected_tracked_refs(*, repo_root: str | Path) -> list[dict[str, Any]]:
    refs = [
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT,
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT,
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_ARTIFACT_OUTPUT,
        *[item["path"] for item in PROTECTED_BASELINE_REFS],
    ]
    return [
        {
            "path": ref,
            "exists": (Path(repo_root) / ref).is_file(),
            "tracked": _is_tracked(ref, repo_root=repo_root),
            "ok": (Path(repo_root) / ref).is_file()
            and _is_tracked(ref, repo_root=repo_root),
        }
        for ref in refs
    ]


def _tracked_refs_clean(*, repo_root: str | Path) -> list[dict[str, Any]]:
    refs = [
        DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT,
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT,
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_ARTIFACT_OUTPUT,
        *[item["path"] for item in PROTECTED_BASELINE_REFS],
    ]
    return [
        {
            "path": ref,
            "worktree_clean": _git_quiet(["diff", "--quiet", "--", ref], repo_root),
            "index_clean": _git_quiet(["diff", "--cached", "--quiet", "--", ref], repo_root),
            "clean": _git_quiet(["diff", "--quiet", "--", ref], repo_root)
            and _git_quiet(["diff", "--cached", "--quiet", "--", ref], repo_root),
        }
        for ref in refs
    ]


def _validate_model_asset(*, repo_root: str | Path) -> dict[str, Any]:
    worktree_clean = _git_quiet(
        ["diff", "--quiet", "--", DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH],
        repo_root,
    )
    index_clean = _git_quiet(
        ["diff", "--cached", "--quiet", "--", DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH],
        repo_root,
    )
    return {
        "path": DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
        "exists": (Path(repo_root) / DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH).is_file(),
        "tracked": _is_tracked(DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH, repo_root=repo_root),
        "worktree_clean": worktree_clean,
        "index_clean": index_clean,
        "ok": worktree_clean and index_clean,
    }


def _tracked_files(pathspec: str, *, repo_root: str | Path) -> list[str]:
    output = _git_output(["ls-files", pathspec], repo_root=repo_root)
    return [line for line in output.splitlines() if line.strip()] if output else []


def _is_tracked(path: str, *, repo_root: str | Path) -> bool:
    return _git_quiet(["ls-files", "--error-unmatch", path], repo_root)


def _git_output(args: list[str], *, repo_root: str | Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _git_quiet(args: list[str], repo_root: str | Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    return result.returncode == 0


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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_BLUEPRINT,
        "blueprint_name": CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _path_string(value: str | Path | None) -> str | None:
    if value is None:
        return None
    return str(Path(value))
