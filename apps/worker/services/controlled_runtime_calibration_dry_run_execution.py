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
    CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_change_request import (
    SOURCE_CONTRACT_REFS as CHANGE_REQUEST_SOURCE_CONTRACT_REFS,
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
    REQUIRED_REGRESSION_GATES,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT,
)

CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_TYPE = (
    "controlled_runtime_calibration_dry_run_execution_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE = (
    "controlled_runtime_calibration_dry_run_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE = (
    "controlled_runtime_calibration_dry_run_execution"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_SUMMARY_TYPE = (
    "controlled_runtime_calibration_dry_run_summary"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_dry_run_rollback_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_BLUEPRINT = "blueprint_56"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_dry_run_execution_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_dry_run_execution_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_execution.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_execution.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_SUMMARY_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_summary.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_rollback_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_change_request_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_CHANGE_REQUEST_CONTRACT_VERSION
    ),
    **dict(CHANGE_REQUEST_SOURCE_CONTRACT_REFS),
}

ALLOWED_DRY_RUN_MODES = [
    "validate_only",
    "fixture_only",
    "structural_dry_run",
    "explicit_local_media_dry_run",
    "no_runtime_mutation",
    "not_applicable",
]
ALLOWED_DRY_RUN_STATUSES = [
    "dry_run_completed_without_runtime_mutation",
    "dry_run_blocked_missing_change_request",
    "dry_run_blocked_missing_manual_approval_packet",
    "dry_run_blocked_missing_candidate_config",
    "dry_run_blocked_missing_regression_gate",
    "dry_run_blocked_missing_rollback_plan",
    "dry_run_blocked_invalid_candidate",
    "dry_run_blocked_unsafe_mode",
    "dry_run_completed_with_warnings",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "not_applied",
    "runtime_application_not_supported_in_this_blueprint",
    "future_blueprint_required",
    "blocked_from_runtime_application",
    "not_applicable",
]
ALLOWED_MUTATION_STATUSES = [
    "no_runtime_mutation",
    "mutation_not_supported",
    "blocked_from_mutation",
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
ALLOWED_ROLLBACK_READINESS_STATUSES = [
    "rollback_plan_present",
    "rollback_plan_missing",
    "rollback_plan_incomplete",
    "rollback_readiness_blocked",
    "not_applicable",
]
STRUCTURAL_COMPARISON_TYPES = [
    "compare_gameplay_segment_counts",
    "compare_routing_window_counts",
    "compare_execution_window_counts",
    "compare_replay_timeline_entry_counts",
    "compare_review_dataset_entry_counts",
    "compare_warning_categories",
    "compare_regression_gate_requirements",
    "compare_rollback_readiness",
]
ALLOWED_COMPARISON_STATUSES = [
    "no_structural_change",
    "structural_change_detected",
    "structural_change_warning",
    "breaking_structural_change",
    "comparison_blocked",
    "not_applicable",
]

DRY_RUN_INPUT_REQUIRED_FIELDS = [
    "dry_run_input_id",
    "dry_run_input_type",
    "dry_run_input_version",
    "generated_at",
    "source_change_request_path",
    "source_candidate_config_freeze_path",
    "source_manual_approval_packet_path",
    "source_decision_packet_path",
    "source_phase_freeze_path",
    "source_gameplay_gate_regression_baseline_path",
    "source_calibration_sandbox_baseline_path",
    "model_asset_ref",
    "model_asset_sha256",
    "current_threshold",
    "current_smoothing_window",
    "current_hysteresis_settings",
    "candidate_threshold",
    "candidate_smoothing_window",
    "candidate_hysteresis_settings",
    "dry_run_mode",
    "fixture_mode_allowed",
    "requested_structural_comparisons",
    "rollback_plan_ref",
    "warnings",
    "non_claims",
]
DRY_RUN_EXECUTION_REQUIRED_FIELDS = [
    "dry_run_id",
    "dry_run_type",
    "dry_run_version",
    "generated_at",
    "source_dry_run_input_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "candidate_settings",
    "dry_run_mode",
    "dry_run_status",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "rollback_readiness_status",
    "regression_gate_requirements",
    "structural_comparison_plan",
    "structural_comparison_results",
    "blockers",
    "warnings",
    "non_claims",
]
ROLLBACK_READINESS_REQUIRED_FIELDS = [
    "rollback_readiness_report_id",
    "report_type",
    "report_version",
    "generated_at",
    "source_dry_run_report_path",
    "dry_run_id",
    "rollback_readiness_status",
    "rollback_plan_ref",
    "required_verification_gates",
    "blockers",
    "warnings",
    "non_claims",
]

NON_CLAIMS = {
    "dry_run_is_not_truth": True,
    "dry_run_is_not_accuracy_scoring": True,
    "dry_run_is_not_runtime_calibration": True,
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
    "controlled_dry_run": True,
    "structural_dry_run": True,
    "no_runtime_mutation": True,
    "runtime_application_status_not_applied": True,
    "rollback_readiness": True,
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
FORBIDDEN_DRY_RUN_EXECUTION_TOKENS = {
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


def export_controlled_runtime_calibration_dry_run_execution_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    errors = _validate_contract_shape(contract)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_TYPE,
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION
        ),
        "contract": contract,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_controlled_runtime_calibration_dry_run_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
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
    dry_run_mode: str = "validate_only",
    dry_run_media_manifest_path: str | Path | None = None,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    change_request = _load_required_json(
        source_change_request_path,
        "change_request",
        errors,
    )
    candidate_config_freeze = _load_required_json(
        source_candidate_config_freeze_path,
        "candidate_config_freeze",
        errors,
    )
    manual_approval_packet = _load_optional_json(source_manual_approval_packet_path)
    decision_packet = _load_optional_json(source_decision_packet_path)
    phase_freeze = _load_optional_json(source_phase_freeze_path)
    gameplay_gate_regression_baseline = _load_optional_json(
        source_gameplay_gate_regression_baseline_path
    )
    calibration_sandbox_baseline = _load_optional_json(
        source_calibration_sandbox_baseline_path
    )
    if errors:
        return _failed_result(
            status="invalid_dry_run_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE,
            result_key="dry_run_inputs_output",
        )

    current_settings = _current_settings(change_request, candidate_config_freeze)
    candidate_settings = _candidate_settings(change_request, candidate_config_freeze)
    source_payloads = {
        "change_request": change_request,
        "candidate_config_freeze": candidate_config_freeze,
        "manual_approval_packet": manual_approval_packet,
        "decision_packet": decision_packet,
        "phase_freeze": phase_freeze,
        "gameplay_gate_regression_baseline": gameplay_gate_regression_baseline,
        "calibration_sandbox_baseline": calibration_sandbox_baseline,
    }
    inputs = {
        "dry_run_input_id": _stable_id(
            "controlled_runtime_calibration_dry_run_inputs_v1",
            _path_string(source_change_request_path),
            change_request.get("change_request_id"),
            candidate_config_freeze.get("candidate_config_freeze_id"),
            dry_run_mode,
            _sha256_path(model_asset_path),
        ),
        "dry_run_input_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE,
        "dry_run_input_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_VERSION,
        "generated_at": generated_at.isoformat(),
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
        "change_request_id": change_request.get("change_request_id"),
        "candidate_config_freeze_id": candidate_config_freeze.get(
            "candidate_config_freeze_id"
        ),
        "manual_approval_packet_id": manual_approval_packet.get(
            "manual_approval_packet_id"
        ),
        "model_asset_ref": str(Path(model_asset_path)),
        "model_asset_sha256": _sha256_path(model_asset_path),
        "current_threshold": current_settings.get("current_threshold"),
        "current_smoothing_window": current_settings.get("current_smoothing_window"),
        "current_hysteresis_settings": _dict(
            current_settings.get("current_hysteresis_settings")
        ),
        "current_settings": current_settings,
        "candidate_threshold": candidate_settings.get("candidate_threshold"),
        "candidate_smoothing_window": candidate_settings.get(
            "candidate_smoothing_window"
        ),
        "candidate_hysteresis_settings": _dict(
            candidate_settings.get("candidate_hysteresis_settings")
        ),
        "candidate_settings": candidate_settings,
        "selected_candidate_config_ref": _dict(
            change_request.get("selected_candidate_config_ref")
        ),
        "dry_run_mode": dry_run_mode,
        "dry_run_media_manifest_path": _path_string(dry_run_media_manifest_path),
        "fixture_mode_allowed": True,
        "requested_structural_comparisons": list(STRUCTURAL_COMPARISON_TYPES),
        "rollback_plan_ref": _rollback_plan_ref(change_request),
        "regression_gate_requirements": _list(
            change_request.get("required_regression_gates")
        )
        or list(REQUIRED_REGRESSION_GATES),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_artifact_presence": _source_artifact_presence(source_payloads),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_inputs_shape(inputs)
    if validation_errors:
        return _failed_result(
            status="invalid_dry_run_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE,
            result_key="dry_run_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "dry_run_input_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE,
        "dry_run_input_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_VERSION,
        "dry_run_input_id": inputs["dry_run_input_id"],
        "dry_run_mode": inputs["dry_run_mode"],
        "runtime_application_status": "not_applied",
        "dry_run_inputs": inputs,
        "warnings": inputs["warnings"],
    }
    _write_json_if_requested(output_path, inputs, result, "dry_run_inputs_output")
    return result


def validate_controlled_runtime_calibration_dry_run_inputs(
    *,
    dry_run_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(dry_run_inputs_path, "dry_run_inputs", errors)
    if inputs:
        errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_dry_run_inputs_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=dry_run_inputs_path,
        payload_type=inputs.get("dry_run_input_type") if inputs else None,
        payload_version=inputs.get("dry_run_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def run_controlled_runtime_calibration_dry_run(
    *,
    dry_run_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_dry_run_inputs(
        dry_run_inputs_path=dry_run_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_dry_run_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE,
            result_key="dry_run_report_output",
        )
    inputs = _dict(
        _load_json(dry_run_inputs_path, label="dry_run_inputs").get("data")
    )
    blockers = _dry_run_blockers(inputs)
    rollback_status = _rollback_readiness_status(inputs)
    execution = {
        "dry_run_id": _stable_id(
            "controlled_runtime_calibration_dry_run_execution_v1",
            inputs.get("dry_run_input_id"),
            inputs.get("model_asset_sha256"),
            inputs.get("dry_run_mode"),
        ),
        "dry_run_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE,
        "dry_run_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_dry_run_input_path": str(Path(dry_run_inputs_path)),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "selected_candidate_config_ref": _dict(
            inputs.get("selected_candidate_config_ref")
        ),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "current_settings": _dict(inputs.get("current_settings")),
        "candidate_settings": _dict(inputs.get("candidate_settings")),
        "dry_run_mode": inputs.get("dry_run_mode"),
        "dry_run_status": _dry_run_status(blockers),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "rollback_readiness_status": rollback_status,
        "regression_gate_requirements": _list(
            inputs.get("regression_gate_requirements")
        ),
        "structural_comparison_plan": _structural_comparison_plan(inputs),
        "structural_comparison_results": _structural_comparison_results(
            inputs=inputs,
            rollback_status=rollback_status,
        ),
        "blockers": blockers,
        "rollback_plan_ref": _dict(inputs.get("rollback_plan_ref")),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(inputs.get("warnings")),
            **dict(WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_execution_shape(execution)
    if validation_errors:
        return _failed_result(
            status="invalid_dry_run_execution",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE,
            result_key="dry_run_report_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "dry_run_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE,
        "dry_run_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
        "dry_run_id": execution["dry_run_id"],
        "dry_run_status": execution["dry_run_status"],
        "runtime_application_status": execution["runtime_application_status"],
        "mutation_status": execution["mutation_status"],
        "production_config_status": execution["production_config_status"],
        "baseline_update_status": execution["baseline_update_status"],
        "model_update_status": execution["model_update_status"],
        "rollback_readiness_status": execution["rollback_readiness_status"],
        "dry_run_report": execution,
        "warnings": execution["warnings"],
    }
    _write_json_if_requested(output_path, execution, result, "dry_run_report_output")
    return result


def validate_controlled_runtime_calibration_dry_run_report(
    *,
    dry_run_report_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    report = _load_required_json(dry_run_report_path, "dry_run_report", errors)
    if report:
        errors.extend(_validate_execution_shape(report))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_dry_run_report_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=dry_run_report_path,
        payload_type=report.get("dry_run_type") if report else None,
        payload_version=report.get("dry_run_version") if report else None,
        errors=errors,
        extra={
            "runtime_application_status": report.get("runtime_application_status")
            if report
            else None,
            "mutation_status": report.get("mutation_status") if report else None,
            "production_config_status": report.get("production_config_status")
            if report
            else None,
            "baseline_update_status": report.get("baseline_update_status")
            if report
            else None,
            "model_update_status": report.get("model_update_status")
            if report
            else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_dry_run_summary(
    *,
    dry_run_report_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_SUMMARY_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_dry_run_report(
        dry_run_report_path=dry_run_report_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_dry_run_report",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_SUMMARY_TYPE,
            result_key="summary_output",
        )
    report = _dict(_load_json(dry_run_report_path, label="dry_run_report").get("data"))
    summary = {
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_SUMMARY_TYPE,
        "summary_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_dry_run_report_path": str(Path(dry_run_report_path)),
        "dry_run_id": report.get("dry_run_id"),
        "dry_run_status": report.get("dry_run_status"),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "rollback_readiness_status": report.get("rollback_readiness_status"),
        "structural_comparison_count": len(
            _list(report.get("structural_comparison_results"))
        ),
        "blocker_count": len(_list(report.get("blockers"))),
        "validation_snapshot": validation,
        "warnings": {
            **_dict(report.get("warnings")),
            **dict(WARNINGS),
            "summary_is_review_only": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _forbidden_token_errors(summary, "summary")
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_summary",
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_SUMMARY_TYPE,
        "summary_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
        "dry_run_id": report.get("dry_run_id"),
        "error_count": len(errors),
        "errors": errors,
        "summary": summary,
        "warnings": summary["warnings"],
    }
    _write_json_if_requested(output_path, summary, result, "summary_output")
    return result


def build_controlled_runtime_calibration_dry_run_rollback_readiness_report(
    *,
    dry_run_report_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_dry_run_report(
        dry_run_report_path=dry_run_report_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_dry_run_report",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_TYPE
            ),
            result_key="rollback_readiness_report_output",
        )
    report = _dict(_load_json(dry_run_report_path, label="dry_run_report").get("data"))
    readiness = {
        "rollback_readiness_report_id": _stable_id(
            "controlled_runtime_calibration_dry_run_rollback_readiness_report_v1",
            report.get("dry_run_id"),
            report.get("rollback_readiness_status"),
        ),
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_dry_run_report_path": str(Path(dry_run_report_path)),
        "dry_run_id": report.get("dry_run_id"),
        "rollback_readiness_status": report.get("rollback_readiness_status"),
        "rollback_plan_ref": _dict(report.get("rollback_plan_ref")),
        "required_verification_gates": _list(
            report.get("regression_gate_requirements")
        ),
        "blockers": _list(report.get("blockers")),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "validation_snapshot": validation,
        "warnings": {
            **_dict(report.get("warnings")),
            **dict(WARNINGS),
            "rollback_readiness_report_only": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_rollback_readiness_shape(readiness)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_rollback_readiness_report",
        "report_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_TYPE,
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
        "dry_run_id": report.get("dry_run_id"),
        "rollback_readiness_status": report.get("rollback_readiness_status"),
        "error_count": len(errors),
        "errors": errors,
        "rollback_readiness_report": readiness,
        "warnings": readiness["warnings"],
    }
    _write_json_if_requested(
        output_path,
        readiness,
        result,
        "rollback_readiness_report_output",
    )
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_TYPE,
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "dry_run_scope": {
            "purpose": "controlled_runtime_calibration_dry_run_execution",
            "executes_change_request_in_dry_run_mode": True,
            "builds_structural_comparison_plan": True,
            "builds_rollback_readiness_report": True,
            "default_modes": ["validate_only", "fixture_only"],
            "requires_human_approval_context": True,
            "requires_rollback_plan_context": True,
            "requires_regression_gate_refs": True,
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
        "dry_run_input_schema": {
            "dry_run_input_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE,
            "dry_run_input_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_VERSION,
            "required_fields": list(DRY_RUN_INPUT_REQUIRED_FIELDS),
            "allowed_dry_run_modes": list(ALLOWED_DRY_RUN_MODES),
            "default_dry_run_mode": "validate_only",
        },
        "dry_run_execution_schema": {
            "dry_run_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE,
            "dry_run_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
            "required_fields": list(DRY_RUN_EXECUTION_REQUIRED_FIELDS),
            "allowed_dry_run_statuses": list(ALLOWED_DRY_RUN_STATUSES),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_mutation_statuses": list(ALLOWED_MUTATION_STATUSES),
            "allowed_production_config_statuses": list(
                ALLOWED_PRODUCTION_CONFIG_STATUSES
            ),
            "allowed_baseline_update_statuses": list(ALLOWED_BASELINE_UPDATE_STATUSES),
            "allowed_model_update_statuses": list(ALLOWED_MODEL_UPDATE_STATUSES),
            "allowed_rollback_readiness_statuses": list(
                ALLOWED_ROLLBACK_READINESS_STATUSES
            ),
            "required_runtime_application_status": "not_applied",
            "required_mutation_status": "no_runtime_mutation",
            "required_production_config_status": "not_created",
            "required_baseline_update_status": "not_replaced",
            "required_model_update_status": "not_modified",
        },
        "dry_run_report_schema": {
            "structural_comparison_types": list(STRUCTURAL_COMPARISON_TYPES),
            "allowed_comparison_statuses": list(ALLOWED_COMPARISON_STATUSES),
            "structural_change_is_not_accuracy_improvement": True,
            "structural_change_is_not_classifier_correctness": True,
            "structural_change_is_not_truth": True,
        },
        "rollback_readiness_schema": {
            "report_type": (
                CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_ROLLBACK_READINESS_REPORT_TYPE
            ),
            "report_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
            "required_fields": list(ROLLBACK_READINESS_REQUIRED_FIELDS),
            "allowed_rollback_readiness_statuses": list(
                ALLOWED_ROLLBACK_READINESS_STATUSES
            ),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_dry_run_input_shape": True,
            "validate_dry_run_execution_shape": True,
            "validate_rollback_readiness_shape": True,
            "validate_allowed_modes": True,
            "validate_allowed_statuses": True,
            "validate_allowed_comparison_types": True,
            "validate_runtime_application_status": True,
            "validate_mutation_status": True,
            "validate_production_config_status": True,
            "validate_baseline_update_status": True,
            "validate_model_update_status": True,
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
            "source_change_request_path_required": True,
            "source_candidate_config_freeze_path_required": True,
            "source_phase_freeze_path_recorded_when_available": True,
            "source_manual_approval_packet_path_recorded_when_available": True,
            "model_asset_ref_required": True,
            "model_asset_sha256_when_available": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _current_settings(
    change_request: dict[str, Any],
    candidate_config_freeze: dict[str, Any],
) -> dict[str, Any]:
    settings = _dict(change_request.get("current_settings")) or _dict(
        candidate_config_freeze.get("current_settings")
    )
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


def _candidate_settings(
    change_request: dict[str, Any],
    candidate_config_freeze: dict[str, Any],
) -> dict[str, Any]:
    settings = _dict(change_request.get("requested_candidate_settings")) or _dict(
        candidate_config_freeze.get("candidate_settings")
    )
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


def _rollback_plan_ref(change_request: dict[str, Any]) -> dict[str, Any]:
    rollback_plan = _dict(change_request.get("rollback_plan"))
    return {
        "rollback_plan_id": rollback_plan.get("rollback_plan_id"),
        "rollback_plan_version": rollback_plan.get("rollback_plan_version"),
        "rollback_status": rollback_plan.get("rollback_status"),
        "rollback_scope": rollback_plan.get("rollback_scope"),
    }


def _dry_run_blockers(inputs: dict[str, Any]) -> list[str]:
    blockers = {"human_operator_approval_required"}
    selected_ref = _dict(inputs.get("selected_candidate_config_ref"))
    if not selected_ref.get("candidate_packet_id"):
        blockers.add("no_candidate_selected")
    if not _dict(inputs.get("rollback_plan_ref")).get("rollback_plan_id"):
        blockers.add("rollback_plan_missing")
    if not _list(inputs.get("regression_gate_requirements")):
        blockers.add("regression_gate_missing")
    if inputs.get("dry_run_mode") not in {"validate_only", "fixture_only"}:
        blockers.add("requires_explicit_safe_mode_review")
    return sorted(blockers)


def _dry_run_status(blockers: list[str]) -> str:
    if "regression_gate_missing" in blockers:
        return "dry_run_blocked_missing_regression_gate"
    if "rollback_plan_missing" in blockers:
        return "dry_run_blocked_missing_rollback_plan"
    if "no_candidate_selected" in blockers:
        return "dry_run_completed_with_warnings"
    return "dry_run_completed_without_runtime_mutation"


def _rollback_readiness_status(inputs: dict[str, Any]) -> str:
    rollback_plan_ref = _dict(inputs.get("rollback_plan_ref"))
    if not rollback_plan_ref.get("rollback_plan_id"):
        return "rollback_plan_missing"
    if rollback_plan_ref.get("rollback_status") not in {
        "rollback_plan_created",
        "rollback_plan_required",
    }:
        return "rollback_plan_incomplete"
    return "rollback_plan_present"


def _structural_comparison_plan(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "comparison_type": comparison_type,
            "source": "bp56_controlled_dry_run",
            "requested": comparison_type
            in set(_list(inputs.get("requested_structural_comparisons"))),
        }
        for comparison_type in STRUCTURAL_COMPARISON_TYPES
    ]


def _structural_comparison_results(
    *,
    inputs: dict[str, Any],
    rollback_status: str,
) -> list[dict[str, Any]]:
    has_candidate = bool(
        _dict(inputs.get("selected_candidate_config_ref")).get("candidate_packet_id")
    )
    comparison_values = {
        "compare_gameplay_segment_counts": _comparison_value("gameplay_segment_count"),
        "compare_routing_window_counts": _comparison_value("routing_window_count"),
        "compare_execution_window_counts": _comparison_value("execution_window_count"),
        "compare_replay_timeline_entry_counts": _comparison_value(
            "replay_timeline_entry_count"
        ),
        "compare_review_dataset_entry_counts": _comparison_value(
            "review_dataset_entry_count"
        ),
        "compare_warning_categories": {
            "current_value": sorted(_dict(inputs.get("warnings")).keys()),
            "candidate_value": sorted(_dict(inputs.get("warnings")).keys()),
            "baseline_value": None,
        },
        "compare_regression_gate_requirements": {
            "current_value": len(_list(inputs.get("regression_gate_requirements"))),
            "candidate_value": len(_list(inputs.get("regression_gate_requirements"))),
            "baseline_value": len(REQUIRED_REGRESSION_GATES),
        },
        "compare_rollback_readiness": {
            "current_value": rollback_status,
            "candidate_value": rollback_status,
            "baseline_value": "rollback_plan_present",
        },
    }
    results: list[dict[str, Any]] = []
    for comparison_type in STRUCTURAL_COMPARISON_TYPES:
        values = comparison_values[comparison_type]
        status = "no_structural_change" if has_candidate else "not_applicable"
        results.append(
            {
                "comparison_id": _stable_id(
                    "controlled_runtime_calibration_dry_run_comparison_v1",
                    inputs.get("dry_run_input_id"),
                    comparison_type,
                ),
                "comparison_type": comparison_type,
                "current_value": values["current_value"],
                "candidate_value": values["candidate_value"],
                "baseline_value": values["baseline_value"],
                "comparison_status": status,
                "drift_detected": False,
                "breaking_drift_detected": False,
                "warnings": {
                    "structural_change_is_not_accuracy_improvement": True,
                    "structural_change_is_not_classifier_correctness": True,
                    "structural_change_is_not_truth": True,
                },
            }
        )
    return results


def _comparison_value(name: str) -> dict[str, Any]:
    return {"current_value": None, "candidate_value": None, "baseline_value": None}


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
    for payload in source_payloads.values():
        warnings = _dict(payload.get("warnings"))
        for key, value in warnings.items():
            merged[key] = value
    merged.update(WARNINGS)
    return merged


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    if (
        contract.get("contract_type")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_TYPE
    ):
        errors.append(_error("invalid_contract_type", "contract_type", None))
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION
    ):
        errors.append(_error("invalid_contract_version", "contract_version", None))
    for section in (
        "dry_run_scope",
        "source_contract_refs",
        "dry_run_input_schema",
        "dry_run_execution_schema",
        "dry_run_report_schema",
        "rollback_readiness_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "dry_run_inputs")
    _require_fields(inputs, DRY_RUN_INPUT_REQUIRED_FIELDS, "dry_run_inputs", errors)
    if inputs.get("dry_run_input_type") != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_TYPE:
        errors.append(
            _error(
                "invalid_dry_run_input_type",
                "dry_run_input_type",
                inputs.get("dry_run_input_type"),
            )
        )
    if (
        inputs.get("dry_run_input_version")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_dry_run_input_version",
                "dry_run_input_version",
                inputs.get("dry_run_input_version"),
            )
        )
    if inputs.get("dry_run_mode") not in ALLOWED_DRY_RUN_MODES:
        errors.append(
            _error("invalid_dry_run_mode", "dry_run_mode", inputs.get("dry_run_mode"))
        )
    _validate_non_claims(inputs, errors, path="dry_run_inputs.non_claims")
    return errors


def _validate_execution_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "dry_run_report")
    _require_fields(report, DRY_RUN_EXECUTION_REQUIRED_FIELDS, "dry_run_report", errors)
    if report.get("dry_run_type") != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_TYPE:
        errors.append(
            _error("invalid_dry_run_type", "dry_run_type", report.get("dry_run_type"))
        )
    if (
        report.get("dry_run_version")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION
    ):
        errors.append(
            _error(
                "invalid_dry_run_version",
                "dry_run_version",
                report.get("dry_run_version"),
            )
        )
    _validate_allowed(
        report.get("dry_run_mode"),
        ALLOWED_DRY_RUN_MODES,
        "dry_run_mode",
        errors,
    )
    _validate_allowed(
        report.get("dry_run_status"),
        ALLOWED_DRY_RUN_STATUSES,
        "dry_run_status",
        errors,
    )
    _validate_required_status(
        report,
        "runtime_application_status",
        "not_applied",
        ALLOWED_RUNTIME_APPLICATION_STATUSES,
        errors,
    )
    _validate_required_status(
        report,
        "mutation_status",
        "no_runtime_mutation",
        ALLOWED_MUTATION_STATUSES,
        errors,
    )
    _validate_required_status(
        report,
        "production_config_status",
        "not_created",
        ALLOWED_PRODUCTION_CONFIG_STATUSES,
        errors,
    )
    _validate_required_status(
        report,
        "baseline_update_status",
        "not_replaced",
        ALLOWED_BASELINE_UPDATE_STATUSES,
        errors,
    )
    _validate_required_status(
        report,
        "model_update_status",
        "not_modified",
        ALLOWED_MODEL_UPDATE_STATUSES,
        errors,
    )
    _validate_allowed(
        report.get("rollback_readiness_status"),
        ALLOWED_ROLLBACK_READINESS_STATUSES,
        "rollback_readiness_status",
        errors,
    )
    for index, comparison in enumerate(_list(report.get("structural_comparison_results"))):
        comparison_dict = _dict(comparison)
        _validate_allowed(
            comparison_dict.get("comparison_type"),
            STRUCTURAL_COMPARISON_TYPES,
            f"structural_comparison_results[{index}].comparison_type",
            errors,
        )
        _validate_allowed(
            comparison_dict.get("comparison_status"),
            ALLOWED_COMPARISON_STATUSES,
            f"structural_comparison_results[{index}].comparison_status",
            errors,
        )
        if comparison_dict.get("drift_detected") is not False:
            errors.append(
                _error(
                    "dry_run_must_not_report_drift",
                    f"structural_comparison_results[{index}].drift_detected",
                    comparison_dict.get("drift_detected"),
                )
            )
        if comparison_dict.get("breaking_drift_detected") is not False:
            errors.append(
                _error(
                    "dry_run_must_not_report_breaking_drift",
                    f"structural_comparison_results[{index}].breaking_drift_detected",
                    comparison_dict.get("breaking_drift_detected"),
                )
            )
    _validate_non_claims(report, errors, path="dry_run_report.non_claims")
    return errors


def _validate_rollback_readiness_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, "rollback_readiness")
    _require_fields(
        report,
        ROLLBACK_READINESS_REQUIRED_FIELDS,
        "rollback_readiness",
        errors,
    )
    _validate_allowed(
        report.get("rollback_readiness_status"),
        ALLOWED_ROLLBACK_READINESS_STATUSES,
        "rollback_readiness_status",
        errors,
    )
    _validate_non_claims(report, errors, path="rollback_readiness.non_claims")
    return errors


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
        "validation_version": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_VERSION,
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
            if str(key) in FORBIDDEN_DRY_RUN_EXECUTION_TOKENS:
                errors.append(_error("forbidden_field_or_value", child_path, key))
            errors.extend(_forbidden_token_errors(nested, child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_DRY_RUN_EXECUTION_TOKENS:
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_BLUEPRINT,
        "blueprint_name": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _path_string(value: str | Path | None) -> str | None:
    if value is None:
        return None
    return str(Path(value))
