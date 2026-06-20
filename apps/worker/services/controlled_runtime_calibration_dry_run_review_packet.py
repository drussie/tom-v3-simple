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
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_OUTPUT,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_dry_run_execution import (
    SOURCE_CONTRACT_REFS as DRY_RUN_EXECUTION_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.gameplay_gate_regression_baseline import (
    DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)
from apps.worker.services.real_broadcast_gameplay_calibration_decision_phase_freeze import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CALIBRATION_DECISION_PHASE_FREEZE_OUTPUT,
    REQUIRED_REGRESSION_GATES,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT,
)

CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_TYPE = (
    "controlled_runtime_calibration_dry_run_review_packet_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE = (
    "controlled_runtime_calibration_dry_run_review_packet_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE = (
    "controlled_runtime_calibration_dry_run_review_packet"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_SUMMARY_TYPE = (
    "controlled_runtime_calibration_dry_run_review_summary"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_OPERATOR_CHECKLIST_TYPE = (
    "controlled_runtime_calibration_dry_run_operator_checklist"
)
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_BLUEPRINT = "blueprint_57"
CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_dry_run_review_packet_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_dry_run_review_packet_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_review_packet_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_review_packet_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_dry_run_review_packet_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_review_packet.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_SUMMARY_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_review_summary.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_OPERATOR_CHECKLIST_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_dry_run_operator_checklist.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_dry_run_execution_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_EXECUTION_CONTRACT_VERSION
    ),
    **dict(DRY_RUN_EXECUTION_SOURCE_CONTRACT_REFS),
}

ALLOWED_REVIEW_PACKET_STATUSES = [
    "review_packet_created",
    "review_packet_created_with_warnings",
    "review_packet_blocked_missing_dry_run",
    "review_packet_blocked_missing_change_request",
    "review_packet_blocked_missing_candidate_config",
    "review_packet_blocked_missing_rollback_plan",
    "review_packet_blocked_missing_regression_gate",
    "review_packet_blocked_breaking_structural_change",
    "review_packet_informational_only",
    "not_applicable",
]
ALLOWED_NEXT_STEP_RECOMMENDATIONS = [
    "human_review_required",
    "resolve_blockers_before_future_phase",
    "rerun_dry_run_with_explicit_media",
    "rerun_dry_run_after_review_gap_resolution",
    "prepare_future_runtime_application_request",
    "no_future_runtime_action_recommended",
    "not_applicable",
]
ALLOWED_STRUCTURAL_SUMMARY_STATUSES = [
    "no_structural_change_observed",
    "structural_changes_observed",
    "structural_warnings_observed",
    "breaking_structural_change_observed",
    "structural_summary_blocked",
    "not_applicable",
]
ALLOWED_ROLLBACK_READINESS_STATUSES = [
    "rollback_ready_for_future_phase_review",
    "rollback_readiness_incomplete",
    "rollback_readiness_blocked",
    "rollback_not_required_for_this_packet",
    "not_applicable",
]
ALLOWED_GATE_SUMMARY_STATUSES = [
    "gate_refs_present",
    "gate_refs_missing",
    "gate_refs_incomplete",
    "gate_summary_blocked",
    "not_applicable",
]
ALLOWED_CHECKLIST_STATUSES = [
    "required",
    "present",
    "missing",
    "blocked",
    "not_applicable",
]
OPERATOR_CHECKLIST_ITEMS = [
    "verify_candidate_config_ref",
    "verify_manual_approval_packet_ref",
    "verify_dry_run_report_ref",
    "inspect_structural_comparison_summary",
    "inspect_breaking_structural_changes",
    "inspect_rollback_readiness",
    "inspect_regression_gate_requirements",
    "inspect_blockers",
    "inspect_warnings",
    "confirm_no_runtime_application",
    "confirm_no_runtime_mutation",
    "confirm_no_production_config",
    "confirm_no_model_change",
    "confirm_no_baseline_replacement",
    "decide_next_phase_readiness",
]

REVIEW_PACKET_INPUT_REQUIRED_FIELDS = [
    "review_packet_input_id",
    "review_packet_input_type",
    "review_packet_input_version",
    "generated_at",
    "source_dry_run_execution_report_path",
    "source_dry_run_inputs_path",
    "source_change_request_path",
    "source_candidate_config_freeze_path",
    "source_manual_approval_packet_path",
    "source_decision_packet_path",
    "source_phase_freeze_path",
    "source_gameplay_gate_regression_baseline_path",
    "source_calibration_sandbox_baseline_path",
    "model_asset_ref",
    "model_asset_sha256",
    "operator_review_context",
    "required_regression_gate_refs",
    "rollback_plan_ref",
    "warnings",
    "non_claims",
]
REVIEW_PACKET_REQUIRED_FIELDS = [
    "review_packet_id",
    "review_packet_type",
    "review_packet_version",
    "generated_at",
    "source_review_packet_input_path",
    "source_dry_run_execution_report_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "candidate_settings",
    "dry_run_status",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "operator_review_required",
    "future_blueprint_required_for_runtime_application",
    "structural_comparison_summary",
    "rollback_readiness_summary",
    "regression_gate_summary",
    "blocker_summary",
    "warning_summary",
    "operator_review_checklist",
    "review_packet_status",
    "next_step_recommendation",
    "warnings",
    "non_claims",
]
STRUCTURAL_SUMMARY_REQUIRED_FIELDS = [
    "total_comparisons",
    "structural_change_count",
    "breaking_structural_change_count",
    "warning_count",
    "blocked_comparison_count",
    "comparison_types_present",
    "drift_detected",
    "breaking_drift_detected",
    "summary_status",
    "warnings",
]
ROLLBACK_SUMMARY_REQUIRED_FIELDS = [
    "rollback_plan_present",
    "rollback_plan_status",
    "rollback_verification_gate_count",
    "rollback_readiness_status",
    "blockers",
    "warnings",
]
GATE_SUMMARY_REQUIRED_FIELDS = [
    "multi_point_regression_required",
    "protected_sample_point_gate_required",
    "gameplay_gate_regression_required",
    "calibration_sandbox_regression_required",
    "dry_run_regression_required",
    "all_required_gate_refs_present",
    "gate_summary_status",
    "warnings",
]

NON_CLAIMS = {
    "review_packet_is_not_truth": True,
    "review_packet_is_not_accuracy_scoring": True,
    "review_packet_is_not_runtime_calibration": True,
    "review_packet_is_not_human_approval": True,
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
    "human_operator_review_required": True,
    "future_blueprint_required_for_runtime_application": True,
    "classifier_correctness_not_assessed": True,
}
WARNINGS = {
    **dict(NON_CLAIMS),
    "controlled_dry_run_review_packet": True,
    "human_operator_review_required": True,
    "no_runtime_mutation": True,
    "runtime_application_status_not_applied": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "model_weights_not_modified": True,
    "rollback_readiness": True,
    "future_blueprint_required_for_runtime_application": True,
    "review_packet_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "structural_change_summary": True,
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


def export_controlled_runtime_calibration_dry_run_review_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at
        or CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_EXPORTED_AT
    )
    contract = _contract_payload(exported_at=exported_at)
    errors = _validate_contract_shape(contract)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION
        ),
        "contract": contract,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_controlled_runtime_calibration_dry_run_review_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    source_dry_run_execution_report_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REPORT_OUTPUT
    ),
    source_dry_run_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_INPUTS_OUTPUT
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
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_result(
            status="invalid_review_packet_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE,
            result_key="review_packet_inputs_output",
        )

    source_payloads = {
        "dry_run_execution_report": _load_optional_json(
            source_dry_run_execution_report_path
        ),
        "dry_run_inputs": _load_optional_json(source_dry_run_inputs_path),
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
    dry_run_report = source_payloads["dry_run_execution_report"]
    dry_run_inputs = source_payloads["dry_run_inputs"]
    change_request = source_payloads["change_request"]
    candidate_config_freeze = source_payloads["candidate_config_freeze"]
    regression_gate_refs = (
        _list(dry_run_report.get("regression_gate_requirements"))
        or _list(dry_run_inputs.get("regression_gate_requirements"))
        or list(REQUIRED_REGRESSION_GATES)
    )
    rollback_plan_ref = (
        _dict(dry_run_report.get("rollback_plan_ref"))
        or _dict(dry_run_inputs.get("rollback_plan_ref"))
        or _rollback_plan_ref(change_request)
    )
    inputs = {
        "review_packet_input_id": _stable_id(
            "controlled_runtime_calibration_dry_run_review_packet_inputs_v1",
            _path_string(source_dry_run_execution_report_path),
            dry_run_report.get("dry_run_id"),
            dry_run_inputs.get("dry_run_input_id"),
            change_request.get("change_request_id"),
            candidate_config_freeze.get("candidate_config_freeze_id"),
            _sha256_path(model_asset_path),
        ),
        "review_packet_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE
        ),
        "review_packet_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_dry_run_execution_report_path": str(
            Path(source_dry_run_execution_report_path)
        ),
        "source_dry_run_inputs_path": str(Path(source_dry_run_inputs_path)),
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
        "source_dry_run_execution_report_id": dry_run_report.get("dry_run_id"),
        "source_dry_run_input_id": dry_run_inputs.get("dry_run_input_id"),
        "change_request_id": change_request.get("change_request_id"),
        "candidate_config_freeze_id": candidate_config_freeze.get(
            "candidate_config_freeze_id"
        ),
        "manual_approval_packet_id": source_payloads[
            "manual_approval_packet"
        ].get("manual_approval_packet_id"),
        "model_asset_ref": str(Path(model_asset_path)),
        "model_asset_sha256": _sha256_path(model_asset_path),
        "operator_review_context": {
            "operator_review_required": True,
            "human_operator_review_required": True,
            "controlled_dry_run_review_packet": True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
            "production_config_status": "not_created",
            "baseline_update_status": "not_replaced",
            "model_update_status": "not_modified",
            "future_blueprint_required_for_runtime_application": True,
        },
        "required_regression_gate_refs": regression_gate_refs,
        "rollback_plan_ref": rollback_plan_ref,
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
            status="invalid_review_packet_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE,
            result_key="review_packet_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "review_packet_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE
        ),
        "review_packet_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_VERSION
        ),
        "review_packet_input_id": inputs["review_packet_input_id"],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "review_packet_inputs": inputs,
        "warnings": inputs["warnings"],
    }
    _write_json_if_requested(
        output_path,
        inputs,
        result,
        "review_packet_inputs_output",
    )
    return result


def validate_controlled_runtime_calibration_dry_run_review_packet_inputs(
    *,
    review_packet_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(
        review_packet_inputs_path,
        "review_packet_inputs",
        errors,
    )
    if inputs:
        errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        ok=not errors,
        validation_type=(
            "controlled_runtime_calibration_dry_run_review_packet_inputs_validation"
        ),
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=review_packet_inputs_path,
        payload_type=inputs.get("review_packet_input_type") if inputs else None,
        payload_version=inputs.get("review_packet_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_dry_run_review_packet(
    *,
    review_packet_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_dry_run_review_packet_inputs(
        review_packet_inputs_path=review_packet_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_review_packet_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE,
            result_key="review_packet_output",
        )

    inputs = _dict(
        _load_json(review_packet_inputs_path, label="review_packet_inputs").get("data")
    )
    dry_run_report = _load_optional_json(
        inputs.get("source_dry_run_execution_report_path")
    )
    change_request = _load_optional_json(inputs.get("source_change_request_path"))
    candidate_config_freeze = _load_optional_json(
        inputs.get("source_candidate_config_freeze_path")
    )
    source_presence = _dict(inputs.get("source_artifact_presence"))
    structural_summary = _structural_comparison_summary(dry_run_report)
    rollback_summary = _rollback_readiness_summary(
        dry_run_report=dry_run_report,
        inputs=inputs,
    )
    gate_summary = _regression_gate_summary(
        dry_run_report=dry_run_report,
        inputs=inputs,
    )
    blocker_summary = _blocker_summary(
        dry_run_report=dry_run_report,
        source_presence=source_presence,
        structural_summary=structural_summary,
        rollback_summary=rollback_summary,
        gate_summary=gate_summary,
    )
    packet_status = _review_packet_status(blocker_summary)
    checklist = _operator_review_checklist(
        inputs=inputs,
        dry_run_report=dry_run_report,
        source_presence=source_presence,
        structural_summary=structural_summary,
        rollback_summary=rollback_summary,
        gate_summary=gate_summary,
        blocker_summary=blocker_summary,
    )
    warnings = {
        **_dict(inputs.get("warnings")),
        **_dict(dry_run_report.get("warnings")),
        **dict(WARNINGS),
    }
    packet = {
        "review_packet_id": _stable_id(
            "controlled_runtime_calibration_dry_run_review_packet_v1",
            inputs.get("review_packet_input_id"),
            dry_run_report.get("dry_run_id"),
            inputs.get("model_asset_sha256"),
            packet_status,
        ),
        "review_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE
        ),
        "review_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_input_path": str(Path(review_packet_inputs_path)),
        "source_dry_run_execution_report_path": inputs.get(
            "source_dry_run_execution_report_path"
        ),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "selected_candidate_config_ref": (
            _dict(dry_run_report.get("selected_candidate_config_ref"))
            or _dict(change_request.get("selected_candidate_config_ref"))
            or _dict(candidate_config_freeze.get("selected_candidate_config_ref"))
        ),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "current_settings": (
            _dict(dry_run_report.get("current_settings"))
            or _dict(change_request.get("current_settings"))
        ),
        "candidate_settings": (
            _dict(dry_run_report.get("candidate_settings"))
            or _dict(change_request.get("requested_candidate_settings"))
            or _dict(candidate_config_freeze.get("candidate_settings"))
        ),
        "dry_run_status": dry_run_report.get("dry_run_status", "not_applicable"),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "operator_review_required": True,
        "future_blueprint_required_for_runtime_application": True,
        "structural_comparison_summary": structural_summary,
        "rollback_readiness_summary": rollback_summary,
        "regression_gate_summary": gate_summary,
        "blocker_summary": blocker_summary,
        "warning_summary": _warning_summary(warnings),
        "operator_review_checklist": checklist,
        "review_packet_status": packet_status,
        "next_step_recommendation": _next_step_recommendation(
            packet_status=packet_status,
            blocker_summary=blocker_summary,
            warning_summary=_warning_summary(warnings),
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": warnings,
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_packet_shape(packet)
    if validation_errors:
        return _failed_result(
            status="invalid_review_packet",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE,
            result_key="review_packet_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "review_packet_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE
        ),
        "review_packet_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
        "review_packet_id": packet["review_packet_id"],
        "review_packet_status": packet["review_packet_status"],
        "next_step_recommendation": packet["next_step_recommendation"],
        "runtime_application_status": packet["runtime_application_status"],
        "mutation_status": packet["mutation_status"],
        "production_config_status": packet["production_config_status"],
        "baseline_update_status": packet["baseline_update_status"],
        "model_update_status": packet["model_update_status"],
        "operator_review_required": packet["operator_review_required"],
        "future_blueprint_required_for_runtime_application": packet[
            "future_blueprint_required_for_runtime_application"
        ],
        "review_packet": packet,
        "warnings": packet["warnings"],
    }
    _write_json_if_requested(output_path, packet, result, "review_packet_output")
    return result


def validate_controlled_runtime_calibration_dry_run_review_packet(
    *,
    review_packet_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    packet = _load_required_json(review_packet_path, "review_packet", errors)
    if packet:
        errors.extend(_validate_packet_shape(packet))
    result = _validation_result(
        ok=not errors,
        validation_type=(
            "controlled_runtime_calibration_dry_run_review_packet_validation"
        ),
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=review_packet_path,
        payload_type=packet.get("review_packet_type") if packet else None,
        payload_version=packet.get("review_packet_version") if packet else None,
        errors=errors,
        extra={
            "review_packet_status": packet.get("review_packet_status")
            if packet
            else None,
            "next_step_recommendation": packet.get("next_step_recommendation")
            if packet
            else None,
            "runtime_application_status": packet.get("runtime_application_status")
            if packet
            else None,
            "mutation_status": packet.get("mutation_status") if packet else None,
            "production_config_status": packet.get("production_config_status")
            if packet
            else None,
            "baseline_update_status": packet.get("baseline_update_status")
            if packet
            else None,
            "model_update_status": packet.get("model_update_status")
            if packet
            else None,
            "operator_review_required": packet.get("operator_review_required")
            if packet
            else None,
            "future_blueprint_required_for_runtime_application": packet.get(
                "future_blueprint_required_for_runtime_application"
            )
            if packet
            else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_dry_run_review_summary(
    *,
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_SUMMARY_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_dry_run_review_packet(
        review_packet_path=review_packet_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_review_packet",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_SUMMARY_TYPE,
            result_key="summary_output",
        )
    packet = _dict(_load_json(review_packet_path, label="review_packet").get("data"))
    summary = {
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_SUMMARY_TYPE,
        "summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_path": str(Path(review_packet_path)),
        "review_packet_id": packet.get("review_packet_id"),
        "review_packet_status": packet.get("review_packet_status"),
        "next_step_recommendation": packet.get("next_step_recommendation"),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "operator_review_required": True,
        "future_blueprint_required_for_runtime_application": True,
        "structural_comparison_summary": _dict(
            packet.get("structural_comparison_summary")
        ),
        "rollback_readiness_summary": _dict(packet.get("rollback_readiness_summary")),
        "regression_gate_summary": _dict(packet.get("regression_gate_summary")),
        "blocker_summary": _dict(packet.get("blocker_summary")),
        "warning_summary": _dict(packet.get("warning_summary")),
        "validation_snapshot": validation,
        "warnings": {
            **_dict(packet.get("warnings")),
            **dict(WARNINGS),
            "summary_is_review_only": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _forbidden_token_errors(summary, "review_summary")
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_review_summary",
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_SUMMARY_TYPE,
        "summary_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
        "review_packet_id": packet.get("review_packet_id"),
        "error_count": len(errors),
        "errors": errors,
        "summary": summary,
        "warnings": summary["warnings"],
    }
    _write_json_if_requested(output_path, summary, result, "summary_output")
    return result


def build_controlled_runtime_calibration_dry_run_operator_checklist(
    *,
    review_packet_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_OPERATOR_CHECKLIST_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_dry_run_review_packet(
        review_packet_path=review_packet_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_review_packet",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_OPERATOR_CHECKLIST_TYPE,
            result_key="operator_checklist_output",
        )
    packet = _dict(_load_json(review_packet_path, label="review_packet").get("data"))
    checklist = {
        "checklist_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_OPERATOR_CHECKLIST_TYPE
        ),
        "checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_review_packet_path": str(Path(review_packet_path)),
        "review_packet_id": packet.get("review_packet_id"),
        "review_packet_status": packet.get("review_packet_status"),
        "operator_review_required": True,
        "future_blueprint_required_for_runtime_application": True,
        "items": _list(packet.get("operator_review_checklist")),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "warnings": {
            **_dict(packet.get("warnings")),
            **dict(WARNINGS),
            "operator_checklist_is_review_only": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_operator_checklist_shape(checklist["items"])
    errors.extend(_forbidden_token_errors(checklist, "operator_checklist"))
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_operator_checklist",
        "checklist_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_OPERATOR_CHECKLIST_TYPE
        ),
        "checklist_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
        "review_packet_id": packet.get("review_packet_id"),
        "error_count": len(errors),
        "errors": errors,
        "operator_checklist": checklist,
        "warnings": checklist["warnings"],
    }
    _write_json_if_requested(output_path, checklist, result, "operator_checklist_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "review_packet_scope": {
            "purpose": "controlled_runtime_calibration_dry_run_review_packet",
            "packages_existing_dry_run_report": True,
            "builds_structural_change_summary": True,
            "builds_rollback_readiness_summary": True,
            "builds_regression_gate_summary": True,
            "builds_operator_checklist": True,
            "requires_human_operator_review": True,
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
        "review_packet_input_schema": {
            "review_packet_input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE
            ),
            "review_packet_input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_VERSION
            ),
            "required_fields": list(REVIEW_PACKET_INPUT_REQUIRED_FIELDS),
        },
        "review_packet_schema": {
            "review_packet_type": (
                CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE
            ),
            "review_packet_version": (
                CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
            ),
            "required_fields": list(REVIEW_PACKET_REQUIRED_FIELDS),
            "allowed_review_packet_statuses": list(ALLOWED_REVIEW_PACKET_STATUSES),
            "allowed_next_step_recommendations": list(
                ALLOWED_NEXT_STEP_RECOMMENDATIONS
            ),
            "required_runtime_application_status": "not_applied",
            "required_mutation_status": "no_runtime_mutation",
            "required_production_config_status": "not_created",
            "required_baseline_update_status": "not_replaced",
            "required_model_update_status": "not_modified",
            "operator_review_required": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "structural_summary_schema": {
            "required_fields": list(STRUCTURAL_SUMMARY_REQUIRED_FIELDS),
            "allowed_statuses": list(ALLOWED_STRUCTURAL_SUMMARY_STATUSES),
            "structural_change_is_not_accuracy_improvement": True,
            "structural_change_is_not_classifier_correctness": True,
            "structural_change_is_not_truth": True,
        },
        "rollback_readiness_schema": {
            "required_fields": list(ROLLBACK_SUMMARY_REQUIRED_FIELDS),
            "allowed_statuses": list(ALLOWED_ROLLBACK_READINESS_STATUSES),
        },
        "regression_gate_schema": {
            "required_fields": list(GATE_SUMMARY_REQUIRED_FIELDS),
            "allowed_statuses": list(ALLOWED_GATE_SUMMARY_STATUSES),
        },
        "operator_checklist_schema": {
            "required_items": list(OPERATOR_CHECKLIST_ITEMS),
            "allowed_item_statuses": list(ALLOWED_CHECKLIST_STATUSES),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_review_packet_input_shape": True,
            "validate_review_packet_shape": True,
            "validate_structural_summary_shape": True,
            "validate_rollback_summary_shape": True,
            "validate_regression_gate_summary_shape": True,
            "validate_operator_checklist_shape": True,
            "validate_allowed_statuses": True,
            "validate_required_no_mutation_statuses": True,
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
            "source_dry_run_execution_report_path_recorded": True,
            "source_dry_run_inputs_path_recorded": True,
            "source_change_request_path_recorded": True,
            "source_candidate_config_freeze_path_recorded": True,
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


def _structural_comparison_summary(report: dict[str, Any]) -> dict[str, Any]:
    if not report:
        return {
            "total_comparisons": 0,
            "structural_change_count": 0,
            "breaking_structural_change_count": 0,
            "warning_count": 0,
            "blocked_comparison_count": 0,
            "comparison_types_present": [],
            "drift_detected": False,
            "breaking_drift_detected": False,
            "summary_status": "structural_summary_blocked",
            "warnings": {
                "missing_source_dry_run_execution_report": True,
                "structural_change_summary": True,
            },
        }
    comparisons = [_dict(item) for item in _list(report.get("structural_comparison_results"))]
    structural_change_count = sum(
        1
        for item in comparisons
        if item.get("comparison_status")
        in {"structural_change_detected", "breaking_structural_change"}
    )
    breaking_count = sum(
        1
        for item in comparisons
        if item.get("comparison_status") == "breaking_structural_change"
        or item.get("breaking_drift_detected") is True
    )
    warning_count = sum(
        1
        for item in comparisons
        if item.get("comparison_status") == "structural_change_warning"
        or bool(_dict(item.get("warnings")))
    )
    blocked_count = sum(
        1 for item in comparisons if item.get("comparison_status") == "comparison_blocked"
    )
    drift_detected = any(item.get("drift_detected") is True for item in comparisons)
    breaking_drift_detected = any(
        item.get("breaking_drift_detected") is True for item in comparisons
    )
    if breaking_count:
        summary_status = "breaking_structural_change_observed"
    elif blocked_count:
        summary_status = "structural_summary_blocked"
    elif structural_change_count:
        summary_status = "structural_changes_observed"
    elif warning_count:
        summary_status = "structural_warnings_observed"
    else:
        summary_status = "no_structural_change_observed"
    return {
        "total_comparisons": len(comparisons),
        "structural_change_count": structural_change_count,
        "breaking_structural_change_count": breaking_count,
        "warning_count": warning_count,
        "blocked_comparison_count": blocked_count,
        "comparison_types_present": sorted(
            str(item.get("comparison_type"))
            for item in comparisons
            if item.get("comparison_type")
        ),
        "drift_detected": drift_detected,
        "breaking_drift_detected": breaking_drift_detected,
        "summary_status": summary_status,
        "warnings": {
            "structural_change_summary": True,
            "classifier_correctness_not_assessed": True,
        },
    }


def _rollback_readiness_summary(
    *,
    dry_run_report: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    if not dry_run_report:
        return {
            "rollback_plan_present": False,
            "rollback_plan_status": "not_applicable",
            "rollback_verification_gate_count": 0,
            "rollback_readiness_status": "not_applicable",
            "blockers": ["missing_dry_run_execution_report"],
            "warnings": {
                "rollback_readiness": True,
                "missing_source_dry_run_execution_report": True,
            },
        }
    rollback_plan_ref = _dict(dry_run_report.get("rollback_plan_ref")) or _dict(
        inputs.get("rollback_plan_ref")
    )
    regression_gate_refs = _list(dry_run_report.get("regression_gate_requirements"))
    rollback_plan_present = bool(rollback_plan_ref.get("rollback_plan_id"))
    blockers: list[str] = []
    if not rollback_plan_present:
        blockers.append("rollback_plan_missing")
        readiness_status = "rollback_readiness_blocked"
    elif not regression_gate_refs:
        blockers.append("rollback_verification_gate_missing")
        readiness_status = "rollback_readiness_incomplete"
    else:
        readiness_status = "rollback_ready_for_future_phase_review"
    return {
        "rollback_plan_present": rollback_plan_present,
        "rollback_plan_status": (
            rollback_plan_ref.get("rollback_status")
            or dry_run_report.get("rollback_readiness_status")
            or "not_applicable"
        ),
        "rollback_verification_gate_count": len(regression_gate_refs),
        "rollback_readiness_status": readiness_status,
        "blockers": blockers,
        "warnings": {
            "rollback_readiness": True,
            "future_blueprint_required_for_runtime_application": True,
        },
    }


def _regression_gate_summary(
    *,
    dry_run_report: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    regression_gate_refs = _list(
        dry_run_report.get("regression_gate_requirements")
    ) or _list(inputs.get("required_regression_gate_refs"))
    gate_tokens = _gate_tokens(regression_gate_refs)
    multi_point_required = any(
        "multi_point_regression_matrix" in token for token in gate_tokens
    )
    protected_sample_required = any(
        "protected_sample_point" in token or "reviewed_3d_debug" in token
        for token in gate_tokens
    )
    gameplay_gate_required = any(
        "gameplay_gate_regression" in token for token in gate_tokens
    )
    calibration_sandbox_required = any(
        "calibration_sandbox" in token or "sandbox_regression" in token
        for token in gate_tokens
    )
    dry_run_required = bool(dry_run_report)
    all_required_present = all(
        [
            multi_point_required,
            protected_sample_required,
            gameplay_gate_required,
            calibration_sandbox_required,
            dry_run_required,
        ]
    )
    if not dry_run_report:
        gate_status = "gate_summary_blocked"
    elif all_required_present:
        gate_status = "gate_refs_present"
    elif regression_gate_refs:
        gate_status = "gate_refs_incomplete"
    else:
        gate_status = "gate_refs_missing"
    return {
        "multi_point_regression_required": multi_point_required,
        "protected_sample_point_gate_required": protected_sample_required,
        "gameplay_gate_regression_required": gameplay_gate_required,
        "calibration_sandbox_regression_required": calibration_sandbox_required,
        "dry_run_regression_required": dry_run_required,
        "all_required_gate_refs_present": all_required_present,
        "gate_summary_status": gate_status,
        "warnings": {
            "required_regression_gate_refs_are_review_requirements": True,
            "future_blueprint_required_for_runtime_application": True,
        },
    }


def _blocker_summary(
    *,
    dry_run_report: dict[str, Any],
    source_presence: dict[str, Any],
    structural_summary: dict[str, Any],
    rollback_summary: dict[str, Any],
    gate_summary: dict[str, Any],
) -> dict[str, Any]:
    blockers = set(_list(dry_run_report.get("blockers")))
    if not _source_present(source_presence, "dry_run_execution_report"):
        blockers.add("missing_dry_run_execution_report")
    if not _source_present(source_presence, "change_request"):
        blockers.add("missing_change_request")
    if not _source_present(source_presence, "candidate_config_freeze"):
        blockers.add("missing_candidate_config")
    if rollback_summary.get("rollback_readiness_status") in {
        "rollback_readiness_blocked",
        "rollback_readiness_incomplete",
    }:
        blockers.update(str(item) for item in _list(rollback_summary.get("blockers")))
    if gate_summary.get("gate_summary_status") in {
        "gate_refs_missing",
        "gate_refs_incomplete",
        "gate_summary_blocked",
    }:
        blockers.add("regression_gate_incomplete")
    if (
        structural_summary.get("summary_status")
        == "breaking_structural_change_observed"
    ):
        blockers.add("breaking_structural_change_observed")
    return {
        "blocker_count": len(blockers),
        "blockers": sorted(blockers),
        "human_operator_review_required": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "inspect_blockers": True,
            "human_operator_review_required": True,
        },
    }


def _warning_summary(warnings: dict[str, Any]) -> dict[str, Any]:
    warning_keys = sorted(str(key) for key, value in warnings.items() if value)
    return {
        "warning_count": len(warning_keys),
        "warnings_present": bool(warning_keys),
        "warning_keys": warning_keys,
        "human_operator_review_required": True,
        "warnings": {
            "inspect_warnings": True,
            "review_packet_is_not_truth": True,
        },
    }


def _operator_review_checklist(
    *,
    inputs: dict[str, Any],
    dry_run_report: dict[str, Any],
    source_presence: dict[str, Any],
    structural_summary: dict[str, Any],
    rollback_summary: dict[str, Any],
    gate_summary: dict[str, Any],
    blocker_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    selected_candidate_ref = _dict(dry_run_report.get("selected_candidate_config_ref"))
    selected_candidate_ref_present = bool(
        selected_candidate_ref.get("candidate_packet_id")
        or selected_candidate_ref.get("candidate_setting_id")
    )
    blocker_count = int(blocker_summary.get("blocker_count", 0))
    return [
        _checklist_item(
            "verify_candidate_config_ref",
            "present" if selected_candidate_ref_present else "missing",
            "Review the selected candidate config reference before any future phase.",
        ),
        _checklist_item(
            "verify_manual_approval_packet_ref",
            "present"
            if _source_present(source_presence, "manual_approval_packet")
            else "missing",
            "Confirm the manual approval packet reference is present for review.",
        ),
        _checklist_item(
            "verify_dry_run_report_ref",
            "present"
            if _source_present(source_presence, "dry_run_execution_report")
            else "missing",
            "Confirm the source dry-run report path and identifier.",
        ),
        _checklist_item(
            "inspect_structural_comparison_summary",
            "required",
            f"Summary status: {structural_summary.get('summary_status')}.",
        ),
        _checklist_item(
            "inspect_breaking_structural_changes",
            "blocked"
            if structural_summary.get("breaking_structural_change_count")
            else "present",
            "Review any breaking structural changes before future phases.",
        ),
        _checklist_item(
            "inspect_rollback_readiness",
            "present"
            if rollback_summary.get("rollback_readiness_status")
            == "rollback_ready_for_future_phase_review"
            else "blocked",
            f"Rollback readiness: {rollback_summary.get('rollback_readiness_status')}.",
        ),
        _checklist_item(
            "inspect_regression_gate_requirements",
            "present"
            if gate_summary.get("gate_summary_status") == "gate_refs_present"
            else "blocked",
            f"Gate summary: {gate_summary.get('gate_summary_status')}.",
        ),
        _checklist_item(
            "inspect_blockers",
            "blocked" if blocker_count else "present",
            f"Blocker count: {blocker_count}.",
        ),
        _checklist_item(
            "inspect_warnings",
            "required",
            "Review packet warnings are informational and require operator review.",
        ),
        _checklist_item(
            "confirm_no_runtime_application",
            "present",
            "Runtime application status remains not_applied.",
        ),
        _checklist_item(
            "confirm_no_runtime_mutation",
            "present",
            "Mutation status remains no_runtime_mutation.",
        ),
        _checklist_item(
            "confirm_no_production_config",
            "present",
            "Production config status remains not_created.",
        ),
        _checklist_item(
            "confirm_no_model_change",
            "present",
            "Model update status remains not_modified.",
        ),
        _checklist_item(
            "confirm_no_baseline_replacement",
            "present",
            "Baseline update status remains not_replaced.",
        ),
        _checklist_item(
            "decide_next_phase_readiness",
            "blocked" if blocker_count else "required",
            "Human operator decides whether a future blueprint should be requested.",
        ),
    ]


def _review_packet_status(blocker_summary: dict[str, Any]) -> str:
    blockers = set(str(item) for item in _list(blocker_summary.get("blockers")))
    if "missing_dry_run_execution_report" in blockers:
        return "review_packet_blocked_missing_dry_run"
    if "missing_change_request" in blockers:
        return "review_packet_blocked_missing_change_request"
    if "missing_candidate_config" in blockers:
        return "review_packet_blocked_missing_candidate_config"
    if "rollback_plan_missing" in blockers:
        return "review_packet_blocked_missing_rollback_plan"
    if "regression_gate_incomplete" in blockers:
        return "review_packet_blocked_missing_regression_gate"
    if "breaking_structural_change_observed" in blockers:
        return "review_packet_blocked_breaking_structural_change"
    if "no_candidate_selected" in blockers:
        return "review_packet_informational_only"
    if blockers:
        return "review_packet_created_with_warnings"
    return "review_packet_created"


def _next_step_recommendation(
    *,
    packet_status: str,
    blocker_summary: dict[str, Any],
    warning_summary: dict[str, Any],
) -> str:
    blockers = set(str(item) for item in _list(blocker_summary.get("blockers")))
    if packet_status.startswith("review_packet_blocked_"):
        return "resolve_blockers_before_future_phase"
    if "no_candidate_selected" in blockers:
        return "no_future_runtime_action_recommended"
    if warning_summary.get("warning_count", 0):
        return "human_review_required"
    if packet_status == "review_packet_created":
        return "prepare_future_runtime_application_request"
    return "not_applicable"


def _checklist_item(
    item: str,
    status: str,
    operator_note: str,
) -> dict[str, Any]:
    return {
        "checklist_item": item,
        "status": status,
        "required": item in OPERATOR_CHECKLIST_ITEMS,
        "operator_note": operator_note,
        "warnings": {
            "operator_review_required": True,
            "runtime_application_status_not_applied": True,
        },
    }


def _rollback_plan_ref(change_request: dict[str, Any]) -> dict[str, Any]:
    rollback_plan = _dict(change_request.get("rollback_plan"))
    return {
        "rollback_plan_id": rollback_plan.get("rollback_plan_id"),
        "rollback_plan_version": rollback_plan.get("rollback_plan_version"),
        "rollback_status": rollback_plan.get("rollback_status"),
        "rollback_scope": rollback_plan.get("rollback_scope"),
    }


def _gate_tokens(regression_gate_refs: list[Any]) -> list[str]:
    tokens: list[str] = []
    for gate_ref in regression_gate_refs:
        if isinstance(gate_ref, str):
            tokens.append(gate_ref)
        elif isinstance(gate_ref, dict):
            for key in ("gate_id", "make_target", "path", "baseline_type"):
                value = gate_ref.get(key)
                if value:
                    tokens.append(str(value))
    return tokens


def _source_artifact_presence(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        name: {
            "present": bool(payload),
            "artifact_type": _artifact_type(payload),
        }
        for name, payload in source_payloads.items()
    }


def _source_present(source_presence: dict[str, Any], name: str) -> bool:
    return _dict(source_presence.get(name)).get("present") is True


def _missing_source_refs(source_payloads: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(name for name, payload in source_payloads.items() if not payload)


def _artifact_type(payload: dict[str, Any]) -> str | None:
    for key in (
        "dry_run_type",
        "dry_run_input_type",
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
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_TYPE
    ):
        errors.append(_error("invalid_contract_type", "contract_type", None))
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION
    ):
        errors.append(_error("invalid_contract_version", "contract_version", None))
    for section in (
        "review_packet_scope",
        "source_contract_refs",
        "review_packet_input_schema",
        "review_packet_schema",
        "structural_summary_schema",
        "rollback_readiness_schema",
        "regression_gate_schema",
        "operator_checklist_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "review_packet_inputs")
    _require_fields(
        inputs,
        REVIEW_PACKET_INPUT_REQUIRED_FIELDS,
        "review_packet_inputs",
        errors,
    )
    if (
        inputs.get("review_packet_input_type")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_review_packet_input_type",
                "review_packet_input_type",
                inputs.get("review_packet_input_type"),
            )
        )
    if (
        inputs.get("review_packet_input_version")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_review_packet_input_version",
                "review_packet_input_version",
                inputs.get("review_packet_input_version"),
            )
        )
    _validate_non_claims(inputs, errors, path="review_packet_inputs.non_claims")
    return errors


def _validate_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(packet, "review_packet")
    _require_fields(packet, REVIEW_PACKET_REQUIRED_FIELDS, "review_packet", errors)
    if (
        packet.get("review_packet_type")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_TYPE
    ):
        errors.append(
            _error(
                "invalid_review_packet_type",
                "review_packet_type",
                packet.get("review_packet_type"),
            )
        )
    if (
        packet.get("review_packet_version")
        != CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
    ):
        errors.append(
            _error(
                "invalid_review_packet_version",
                "review_packet_version",
                packet.get("review_packet_version"),
            )
        )
    _validate_required_status(
        packet,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
        errors,
    )
    _validate_required_status(
        packet,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_required_status(
        packet,
        "production_config_status",
        "not_created",
        ["not_created", "not_applicable"],
        errors,
    )
    _validate_required_status(
        packet,
        "baseline_update_status",
        "not_replaced",
        ["not_replaced", "not_applicable"],
        errors,
    )
    _validate_required_status(
        packet,
        "model_update_status",
        "not_modified",
        ["not_modified", "not_applicable"],
        errors,
    )
    _validate_required_bool(
        packet,
        "operator_review_required",
        True,
        errors,
    )
    _validate_required_bool(
        packet,
        "future_blueprint_required_for_runtime_application",
        True,
        errors,
    )
    _validate_allowed(
        packet.get("review_packet_status"),
        ALLOWED_REVIEW_PACKET_STATUSES,
        "review_packet_status",
        errors,
    )
    _validate_allowed(
        packet.get("next_step_recommendation"),
        ALLOWED_NEXT_STEP_RECOMMENDATIONS,
        "next_step_recommendation",
        errors,
    )
    errors.extend(
        _validate_structural_summary_shape(
            _dict(packet.get("structural_comparison_summary"))
        )
    )
    errors.extend(
        _validate_rollback_summary_shape(
            _dict(packet.get("rollback_readiness_summary"))
        )
    )
    errors.extend(
        _validate_regression_gate_summary_shape(
            _dict(packet.get("regression_gate_summary"))
        )
    )
    errors.extend(
        _validate_operator_checklist_shape(
            _list(packet.get("operator_review_checklist"))
        )
    )
    _validate_non_claims(packet, errors, path="review_packet.non_claims")
    return errors


def _validate_structural_summary_shape(summary: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(summary, "structural_comparison_summary")
    _require_fields(
        summary,
        STRUCTURAL_SUMMARY_REQUIRED_FIELDS,
        "structural_comparison_summary",
        errors,
    )
    _validate_allowed(
        summary.get("summary_status"),
        ALLOWED_STRUCTURAL_SUMMARY_STATUSES,
        "structural_comparison_summary.summary_status",
        errors,
    )
    for bool_field in ("drift_detected", "breaking_drift_detected"):
        if not isinstance(summary.get(bool_field), bool):
            errors.append(
                _error(
                    "invalid_structural_summary_boolean",
                    f"structural_comparison_summary.{bool_field}",
                    summary.get(bool_field),
                )
            )
    return errors


def _validate_rollback_summary_shape(summary: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(summary, "rollback_readiness_summary")
    _require_fields(
        summary,
        ROLLBACK_SUMMARY_REQUIRED_FIELDS,
        "rollback_readiness_summary",
        errors,
    )
    _validate_allowed(
        summary.get("rollback_readiness_status"),
        ALLOWED_ROLLBACK_READINESS_STATUSES,
        "rollback_readiness_summary.rollback_readiness_status",
        errors,
    )
    if not isinstance(summary.get("rollback_plan_present"), bool):
        errors.append(
            _error(
                "invalid_rollback_plan_present",
                "rollback_readiness_summary.rollback_plan_present",
                summary.get("rollback_plan_present"),
            )
        )
    return errors


def _validate_regression_gate_summary_shape(
    summary: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(summary, "regression_gate_summary")
    _require_fields(
        summary,
        GATE_SUMMARY_REQUIRED_FIELDS,
        "regression_gate_summary",
        errors,
    )
    _validate_allowed(
        summary.get("gate_summary_status"),
        ALLOWED_GATE_SUMMARY_STATUSES,
        "regression_gate_summary.gate_summary_status",
        errors,
    )
    for bool_field in (
        "multi_point_regression_required",
        "protected_sample_point_gate_required",
        "gameplay_gate_regression_required",
        "calibration_sandbox_regression_required",
        "dry_run_regression_required",
        "all_required_gate_refs_present",
    ):
        if not isinstance(summary.get(bool_field), bool):
            errors.append(
                _error(
                    "invalid_regression_gate_summary_boolean",
                    f"regression_gate_summary.{bool_field}",
                    summary.get(bool_field),
                )
            )
    return errors


def _validate_operator_checklist_shape(items: list[Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(items, "operator_review_checklist")
    checklist_items = [_dict(item) for item in items]
    present_items = {str(item.get("checklist_item")) for item in checklist_items}
    for required_item in OPERATOR_CHECKLIST_ITEMS:
        if required_item not in present_items:
            errors.append(
                _error(
                    "missing_operator_checklist_item",
                    f"operator_review_checklist.{required_item}",
                    None,
                )
            )
    for index, item in enumerate(checklist_items):
        if item.get("checklist_item") not in OPERATOR_CHECKLIST_ITEMS:
            errors.append(
                _error(
                    "invalid_operator_checklist_item",
                    f"operator_review_checklist[{index}].checklist_item",
                    item.get("checklist_item"),
                )
            )
        _validate_allowed(
            item.get("status"),
            ALLOWED_CHECKLIST_STATUSES,
            f"operator_review_checklist[{index}].status",
            errors,
        )
        if not isinstance(item.get("required"), bool):
            errors.append(
                _error(
                    "invalid_operator_checklist_required",
                    f"operator_review_checklist[{index}].required",
                    item.get("required"),
                )
            )
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


def _validate_required_bool(
    payload: dict[str, Any],
    field: str,
    required_value: bool,
    errors: list[dict[str, Any]],
) -> None:
    if payload.get(field) is not required_value:
        errors.append(_error(f"{field}_must_be_{required_value}", field, payload.get(field)))


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
        "validation_version": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_VERSION
        ),
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
            if str(key) in FORBIDDEN_REVIEW_PACKET_TOKENS:
                errors.append(_error("forbidden_field_or_value", child_path, key))
            errors.extend(_forbidden_token_errors(nested, child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_REVIEW_PACKET_TOKENS:
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_BLUEPRINT_NAME
        ),
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _path_string(value: str | Path | None) -> str | None:
    if value is None:
        return None
    return str(Path(value))
