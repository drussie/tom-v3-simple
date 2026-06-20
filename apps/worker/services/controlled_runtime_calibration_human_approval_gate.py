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
    CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION,
    DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_OUTPUT,
)
from apps.worker.services.controlled_runtime_calibration_dry_run_review_packet import (
    SOURCE_CONTRACT_REFS as DRY_RUN_REVIEW_PACKET_SOURCE_CONTRACT_REFS,
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

CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_TYPE = (
    "controlled_runtime_calibration_human_approval_gate_contract"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE = (
    "controlled_runtime_calibration_human_approval_gate_inputs"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE = (
    "controlled_runtime_calibration_human_approval_gate"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION = "v1"
CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_TYPE = (
    "controlled_runtime_calibration_operator_signoff_record"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_SUMMARY_TYPE = (
    "controlled_runtime_calibration_human_approval_summary"
)
CONTROLLED_RUNTIME_CALIBRATION_FUTURE_APPLICATION_READINESS_REPORT_TYPE = (
    "controlled_runtime_calibration_future_application_readiness_report"
)
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_BLUEPRINT = "blueprint_58"
CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_BLUEPRINT_NAME = (
    "controlled_runtime_calibration_human_approval_gate_v1"
)

DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_human_approval_gate_contract_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUTS_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_human_approval_gate_inputs.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_human_approval_gate_inputs.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT = (
    ".data/contracts/controlled_runtime_calibration_human_approval_gate_v1.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VALIDATION_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_human_approval_gate.validation.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_SUMMARY_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_human_approval_summary.current.json"
)
DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FUTURE_APPLICATION_READINESS_REPORT_OUTPUT = (
    ".data/exports/controlled_runtime_calibration_future_application_readiness_report.current.json"
)

CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "controlled_runtime_calibration_dry_run_review_packet_contract_version": (
        CONTROLLED_RUNTIME_CALIBRATION_DRY_RUN_REVIEW_PACKET_CONTRACT_VERSION
    ),
    **dict(DRY_RUN_REVIEW_PACKET_SOURCE_CONTRACT_REFS),
}

ALLOWED_APPROVAL_GATE_STATUSES = [
    "approval_gate_created",
    "approval_gate_created_with_warnings",
    "approval_gate_blocked_missing_review_packet",
    "approval_gate_blocked_missing_change_request",
    "approval_gate_blocked_missing_candidate_config",
    "approval_gate_blocked_missing_rollback_readiness",
    "approval_gate_blocked_missing_regression_gate",
    "approval_gate_blocked_unresolved_blockers",
    "approval_gate_blocked_breaking_structural_change",
    "approval_gate_waiting_for_operator_signoff",
    "approval_gate_human_signoff_recorded_no_runtime_action",
    "approval_gate_informational_only",
    "not_applicable",
]
ALLOWED_OPERATOR_SIGNOFF_STATUSES = [
    "operator_signoff_required",
    "operator_signoff_pending",
    "operator_signoff_recorded_no_runtime_action",
    "operator_signoff_blocked",
    "operator_signoff_not_applicable",
]
ALLOWED_FUTURE_APPLICATION_READINESS_STATUSES = [
    "future_application_not_ready",
    "future_application_blocked",
    "future_application_ready_for_separate_change_request",
    "future_application_requires_new_blueprint",
    "future_application_not_applicable",
]
ALLOWED_BLOCKER_SUMMARY_STATUSES = [
    "no_unresolved_blockers_reported",
    "unresolved_blockers_reported",
    "blocker_summary_missing",
    "blocker_summary_incomplete",
    "blocker_summary_blocked",
    "not_applicable",
]
ALLOWED_WARNING_SUMMARY_STATUSES = [
    "no_warnings_reported",
    "warnings_reported",
    "warning_summary_missing",
    "warning_summary_incomplete",
    "not_applicable",
]
ALLOWED_SIGNOFF_SCOPES = [
    "review_packet_acknowledgement",
    "future_application_readiness_acknowledgement",
    "blocker_resolution_acknowledgement",
    "no_runtime_action_acknowledgement",
    "not_applicable",
]
ALLOWED_SIGNOFF_RECORD_STATUSES = [
    "signoff_recorded_no_runtime_action",
    "signoff_required",
    "signoff_pending",
    "signoff_blocked",
    "signoff_not_applicable",
]

APPROVAL_GATE_INPUT_REQUIRED_FIELDS = [
    "approval_gate_input_id",
    "approval_gate_input_type",
    "approval_gate_input_version",
    "generated_at",
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
    "operator_signoff_context",
    "blocker_resolution_context",
    "future_application_context",
    "warnings",
    "non_claims",
]
APPROVAL_GATE_REQUIRED_FIELDS = [
    "approval_gate_id",
    "approval_gate_type",
    "approval_gate_version",
    "generated_at",
    "source_approval_gate_input_path",
    "source_dry_run_review_packet_path",
    "source_change_request_path",
    "selected_candidate_config_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "candidate_settings",
    "dry_run_review_packet_status",
    "structural_summary_status",
    "rollback_readiness_status",
    "regression_gate_summary_status",
    "blocker_summary_status",
    "warning_summary_status",
    "operator_signoff_status",
    "approval_gate_status",
    "future_application_readiness_status",
    "runtime_application_status",
    "mutation_status",
    "production_config_status",
    "baseline_update_status",
    "model_update_status",
    "future_blueprint_required_for_runtime_application",
    "human_operator_signoff_required",
    "human_approval_gate_record",
    "operator_signoff_record",
    "blocker_resolution_summary",
    "future_application_requirements",
    "warnings",
    "non_claims",
]
OPERATOR_SIGNOFF_REQUIRED_FIELDS = [
    "operator_signoff_id",
    "operator_signoff_type",
    "operator_signoff_version",
    "generated_at",
    "operator_identity_ref",
    "source_review_packet_ref",
    "source_change_request_ref",
    "selected_candidate_config_ref",
    "signoff_scope",
    "signoff_status",
    "signoff_notes",
    "runtime_application_status",
    "mutation_status",
    "warnings",
    "non_claims",
]
BLOCKER_RESOLUTION_SUMMARY_REQUIRED_FIELDS = [
    "blocker_summary_status",
    "unresolved_blocker_count",
    "unresolved_blockers",
    "operator_review_required",
    "runtime_application_status",
    "mutation_status",
    "warnings",
]
FUTURE_APPLICATION_READINESS_REQUIRED_FIELDS = [
    "future_application_readiness_status",
    "future_blueprint_required_for_runtime_application",
    "runtime_application_status",
    "mutation_status",
    "requirements",
    "missing_requirements",
    "warnings",
]

NON_CLAIMS = {
    "approval_gate_is_not_truth": True,
    "approval_gate_is_not_accuracy_scoring": True,
    "approval_gate_is_not_runtime_calibration": True,
    "approval_gate_is_not_runtime_application": True,
    "human_signoff_is_not_runtime_application": True,
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
    "controlled_human_approval_gate": True,
    "human_operator_signoff_required": True,
    "no_runtime_mutation": True,
    "runtime_application_status_not_applied": True,
    "production_config_not_created": True,
    "baseline_not_replaced": True,
    "model_weights_not_modified": True,
    "future_blueprint_required_for_runtime_application": True,
    "future_application_readiness": True,
    "review_support_only": True,
    "provenance_only": True,
    "classifier_correctness_not_assessed": True,
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
FORBIDDEN_APPROVAL_GATE_TOKENS = {
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


def export_controlled_runtime_calibration_human_approval_gate_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at or CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_EXPORTED_AT
    )
    contract = _contract_payload(exported_at=exported_at)
    errors = _validate_contract_shape(contract)
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_contract",
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION
        ),
        "contract": contract,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_controlled_runtime_calibration_human_approval_gate_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
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
    operator_identity_ref: str | None = None,
    operator_review_timestamp: str | None = None,
    signoff_scope: str = "no_runtime_action_acknowledgement",
    signoff_status: str = "signoff_required",
    signoff_notes: str | None = None,
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_result(
            status="invalid_approval_gate_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE,
            result_key="approval_gate_inputs_output",
        )

    source_payloads = {
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
    review_packet = source_payloads["dry_run_review_packet"]
    change_request = source_payloads["change_request"]
    candidate_config_freeze = source_payloads["candidate_config_freeze"]
    selected_candidate_ref = (
        _dict(review_packet.get("selected_candidate_config_ref"))
        or _dict(change_request.get("selected_candidate_config_ref"))
        or _dict(candidate_config_freeze.get("selected_candidate_config_ref"))
    )
    inputs = {
        "approval_gate_input_id": _stable_id(
            "controlled_runtime_calibration_human_approval_gate_inputs_v1",
            _path_string(source_dry_run_review_packet_path),
            review_packet.get("review_packet_id"),
            change_request.get("change_request_id"),
            selected_candidate_ref,
            _sha256_path(model_asset_path),
            signoff_status,
        ),
        "approval_gate_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE
        ),
        "approval_gate_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
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
        "operator_identity_ref": operator_identity_ref,
        "operator_review_timestamp": operator_review_timestamp,
        "operator_signoff_context": {
            "human_operator_signoff_required": True,
            "operator_identity_ref": operator_identity_ref,
            "operator_review_timestamp": operator_review_timestamp,
            "signoff_scope": signoff_scope,
            "signoff_status": signoff_status,
            "signoff_notes": signoff_notes,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "blocker_resolution_context": {
            "source_blocker_summary": _dict(review_packet.get("blocker_summary")),
            "blocker_summary_status": _blocker_summary_status(
                _dict(review_packet.get("blocker_summary"))
            ),
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "future_application_context": {
            "future_blueprint_required_for_runtime_application": True,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
            "production_config_status": "not_created",
            "baseline_update_status": "not_replaced",
            "model_update_status": "not_modified",
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
            status="invalid_approval_gate_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE,
            result_key="approval_gate_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "approval_gate_input_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE
        ),
        "approval_gate_input_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_VERSION
        ),
        "approval_gate_input_id": inputs["approval_gate_input_id"],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "human_operator_signoff_required": True,
        "approval_gate_inputs": inputs,
        "warnings": inputs["warnings"],
    }
    _write_json_if_requested(
        output_path,
        inputs,
        result,
        "approval_gate_inputs_output",
    )
    return result


def validate_controlled_runtime_calibration_human_approval_gate_inputs(
    *,
    approval_gate_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(
        approval_gate_inputs_path,
        "approval_gate_inputs",
        errors,
    )
    if inputs:
        errors.extend(_validate_inputs_shape(inputs))
    result = _validation_result(
        ok=not errors,
        validation_type=(
            "controlled_runtime_calibration_human_approval_gate_inputs_validation"
        ),
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=approval_gate_inputs_path,
        payload_type=inputs.get("approval_gate_input_type") if inputs else None,
        payload_version=inputs.get("approval_gate_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_human_approval_gate(
    *,
    approval_gate_inputs_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_human_approval_gate_inputs(
        approval_gate_inputs_path=approval_gate_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_approval_gate_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE,
            result_key="approval_gate_output",
        )

    inputs = _dict(
        _load_json(approval_gate_inputs_path, label="approval_gate_inputs").get("data")
    )
    review_packet = _load_optional_json(inputs.get("source_dry_run_review_packet_path"))
    change_request = _load_optional_json(inputs.get("source_change_request_path"))
    candidate_config_freeze = _load_optional_json(
        inputs.get("source_candidate_config_freeze_path")
    )
    selected_candidate_ref = (
        _dict(review_packet.get("selected_candidate_config_ref"))
        or _dict(inputs.get("selected_candidate_config_ref"))
        or _dict(change_request.get("selected_candidate_config_ref"))
        or _dict(candidate_config_freeze.get("selected_candidate_config_ref"))
    )
    blocker_summary = _blocker_resolution_summary(
        review_packet=review_packet,
        inputs=inputs,
        selected_candidate_ref=selected_candidate_ref,
    )
    warning_summary = _warning_summary(
        {
            **_dict(inputs.get("warnings")),
            **_dict(review_packet.get("warnings")),
            **dict(WARNINGS),
        }
    )
    signoff_record = _operator_signoff_record(
        inputs=inputs,
        review_packet=review_packet,
        selected_candidate_ref=selected_candidate_ref,
        generated_at=generated_at,
        blocker_summary=blocker_summary,
    )
    operator_status = _operator_signoff_status(signoff_record, blocker_summary)
    readiness = _future_application_readiness(
        review_packet=review_packet,
        selected_candidate_ref=selected_candidate_ref,
        blocker_summary=blocker_summary,
        operator_signoff_status=operator_status,
    )
    approval_gate_status = _approval_gate_status(
        review_packet=review_packet,
        selected_candidate_ref=selected_candidate_ref,
        blocker_summary=blocker_summary,
        operator_signoff_status=operator_status,
        readiness_status=readiness["future_application_readiness_status"],
    )
    structural_summary = _dict(review_packet.get("structural_comparison_summary"))
    rollback_summary = _dict(review_packet.get("rollback_readiness_summary"))
    gate_summary = _dict(review_packet.get("regression_gate_summary"))
    gate = {
        "approval_gate_id": _stable_id(
            "controlled_runtime_calibration_human_approval_gate_v1",
            inputs.get("approval_gate_input_id"),
            review_packet.get("review_packet_id"),
            change_request.get("change_request_id"),
            selected_candidate_ref,
            operator_status,
            approval_gate_status,
        ),
        "approval_gate_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE,
        "approval_gate_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_approval_gate_input_path": str(Path(approval_gate_inputs_path)),
        "source_dry_run_review_packet_path": inputs.get(
            "source_dry_run_review_packet_path"
        ),
        "source_change_request_path": inputs.get("source_change_request_path"),
        "selected_candidate_config_ref": selected_candidate_ref,
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "current_settings": (
            _dict(review_packet.get("current_settings"))
            or _dict(change_request.get("current_settings"))
        ),
        "candidate_settings": (
            _dict(review_packet.get("candidate_settings"))
            or _dict(change_request.get("requested_candidate_settings"))
            or _dict(candidate_config_freeze.get("candidate_settings"))
        ),
        "dry_run_review_packet_status": review_packet.get(
            "review_packet_status", "not_applicable"
        ),
        "structural_summary_status": structural_summary.get(
            "summary_status", "not_applicable"
        ),
        "rollback_readiness_status": rollback_summary.get(
            "rollback_readiness_status", "not_applicable"
        ),
        "regression_gate_summary_status": gate_summary.get(
            "gate_summary_status", "not_applicable"
        ),
        "blocker_summary_status": blocker_summary["blocker_summary_status"],
        "warning_summary_status": warning_summary["warning_summary_status"],
        "operator_signoff_status": operator_status,
        "approval_gate_status": approval_gate_status,
        "future_application_readiness_status": readiness[
            "future_application_readiness_status"
        ],
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_blueprint_required_for_runtime_application": True,
        "human_operator_signoff_required": True,
        "human_approval_gate_record": {
            "source_review_packet_ref": _review_packet_ref(review_packet),
            "source_change_request_ref": _change_request_ref(change_request, inputs),
            "dry_run_results_reviewed": bool(review_packet),
            "structural_comparison_summary_present": bool(structural_summary),
            "rollback_readiness_summary_present": bool(rollback_summary),
            "regression_gate_refs_present": (
                gate_summary.get("gate_summary_status") == "gate_refs_present"
            ),
            "unresolved_blockers_present": (
                blocker_summary["unresolved_blocker_count"] > 0
            ),
            "warnings_present": warning_summary["warning_count"] > 0,
            "human_operator_signoff_required": True,
            "runtime_application_allowed_in_this_blueprint": False,
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
            "future_blueprint_required_for_runtime_application": True,
        },
        "operator_signoff_record": signoff_record,
        "blocker_resolution_summary": blocker_summary,
        "future_application_requirements": readiness,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(inputs.get("warnings")),
            **_dict(review_packet.get("warnings")),
            **dict(WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_gate_shape(gate)
    if validation_errors:
        return _failed_result(
            status="invalid_approval_gate",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE,
            result_key="approval_gate_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "approval_gate_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE,
        "approval_gate_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
        ),
        "approval_gate_id": gate["approval_gate_id"],
        "approval_gate_status": gate["approval_gate_status"],
        "operator_signoff_status": gate["operator_signoff_status"],
        "future_application_readiness_status": gate[
            "future_application_readiness_status"
        ],
        "runtime_application_status": gate["runtime_application_status"],
        "mutation_status": gate["mutation_status"],
        "production_config_status": gate["production_config_status"],
        "baseline_update_status": gate["baseline_update_status"],
        "model_update_status": gate["model_update_status"],
        "human_operator_signoff_required": gate["human_operator_signoff_required"],
        "future_blueprint_required_for_runtime_application": gate[
            "future_blueprint_required_for_runtime_application"
        ],
        "approval_gate": gate,
        "warnings": gate["warnings"],
    }
    _write_json_if_requested(output_path, gate, result, "approval_gate_output")
    return result


def validate_controlled_runtime_calibration_human_approval_gate(
    *,
    approval_gate_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    gate = _load_required_json(approval_gate_path, "approval_gate", errors)
    if gate:
        errors.extend(_validate_gate_shape(gate))
    result = _validation_result(
        ok=not errors,
        validation_type="controlled_runtime_calibration_human_approval_gate_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=approval_gate_path,
        payload_type=gate.get("approval_gate_type") if gate else None,
        payload_version=gate.get("approval_gate_version") if gate else None,
        errors=errors,
        extra={
            "approval_gate_status": gate.get("approval_gate_status")
            if gate
            else None,
            "operator_signoff_status": gate.get("operator_signoff_status")
            if gate
            else None,
            "future_application_readiness_status": gate.get(
                "future_application_readiness_status"
            )
            if gate
            else None,
            "runtime_application_status": gate.get("runtime_application_status")
            if gate
            else None,
            "mutation_status": gate.get("mutation_status") if gate else None,
            "production_config_status": gate.get("production_config_status")
            if gate
            else None,
            "baseline_update_status": gate.get("baseline_update_status")
            if gate
            else None,
            "model_update_status": gate.get("model_update_status")
            if gate
            else None,
            "human_operator_signoff_required": gate.get(
                "human_operator_signoff_required"
            )
            if gate
            else None,
            "future_blueprint_required_for_runtime_application": gate.get(
                "future_blueprint_required_for_runtime_application"
            )
            if gate
            else None,
        },
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_controlled_runtime_calibration_human_approval_summary(
    *,
    approval_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_SUMMARY_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_human_approval_gate(
        approval_gate_path=approval_gate_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_approval_gate",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_SUMMARY_TYPE,
            result_key="summary_output",
        )
    gate = _dict(_load_json(approval_gate_path, label="approval_gate").get("data"))
    summary = {
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_SUMMARY_TYPE,
        "summary_version": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_approval_gate_path": str(Path(approval_gate_path)),
        "approval_gate_id": gate.get("approval_gate_id"),
        "approval_gate_status": gate.get("approval_gate_status"),
        "operator_signoff_status": gate.get("operator_signoff_status"),
        "future_application_readiness_status": gate.get(
            "future_application_readiness_status"
        ),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "human_operator_signoff_required": True,
        "future_blueprint_required_for_runtime_application": True,
        "blocker_resolution_summary": _dict(gate.get("blocker_resolution_summary")),
        "future_application_requirements": _dict(
            gate.get("future_application_requirements")
        ),
        "validation_snapshot": validation,
        "warnings": {
            **_dict(gate.get("warnings")),
            **dict(WARNINGS),
            "summary_is_review_only": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _forbidden_token_errors(summary, "approval_summary")
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_approval_summary",
        "summary_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_SUMMARY_TYPE,
        "summary_version": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION,
        "approval_gate_id": gate.get("approval_gate_id"),
        "error_count": len(errors),
        "errors": errors,
        "summary": summary,
        "warnings": summary["warnings"],
    }
    _write_json_if_requested(output_path, summary, result, "summary_output")
    return result


def build_controlled_runtime_calibration_future_application_readiness_report(
    *,
    approval_gate_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CONTROLLED_RUNTIME_CALIBRATION_FUTURE_APPLICATION_READINESS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_controlled_runtime_calibration_human_approval_gate(
        approval_gate_path=approval_gate_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_approval_gate",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=(
                CONTROLLED_RUNTIME_CALIBRATION_FUTURE_APPLICATION_READINESS_REPORT_TYPE
            ),
            result_key="readiness_report_output",
        )
    gate = _dict(_load_json(approval_gate_path, label="approval_gate").get("data"))
    readiness = _dict(gate.get("future_application_requirements"))
    report = {
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FUTURE_APPLICATION_READINESS_REPORT_TYPE
        ),
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_approval_gate_path": str(Path(approval_gate_path)),
        "approval_gate_id": gate.get("approval_gate_id"),
        "approval_gate_status": gate.get("approval_gate_status"),
        "operator_signoff_status": gate.get("operator_signoff_status"),
        "future_application_readiness_status": readiness.get(
            "future_application_readiness_status"
        ),
        "future_blueprint_required_for_runtime_application": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "production_config_status": "not_created",
        "baseline_update_status": "not_replaced",
        "model_update_status": "not_modified",
        "future_application_requirements": readiness,
        "warnings": {
            **_dict(gate.get("warnings")),
            **dict(WARNINGS),
            "future_application_readiness_report": True,
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_future_application_readiness_shape(readiness)
    errors.extend(_forbidden_token_errors(report, "future_application_readiness_report"))
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "invalid_readiness_report",
        "report_type": (
            CONTROLLED_RUNTIME_CALIBRATION_FUTURE_APPLICATION_READINESS_REPORT_TYPE
        ),
        "report_version": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION,
        "approval_gate_id": gate.get("approval_gate_id"),
        "future_application_readiness_status": readiness.get(
            "future_application_readiness_status"
        ),
        "error_count": len(errors),
        "errors": errors,
        "readiness_report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "readiness_report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_TYPE
        ),
        "contract_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "approval_gate_scope": {
            "purpose": "controlled_runtime_calibration_human_approval_gate",
            "consumes_dry_run_review_packet": True,
            "records_operator_signoff_state": True,
            "records_blocker_context": True,
            "records_future_application_readiness": True,
            "requires_human_operator_signoff": True,
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
        "approval_gate_input_schema": {
            "approval_gate_input_type": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE
            ),
            "approval_gate_input_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_VERSION
            ),
            "required_fields": list(APPROVAL_GATE_INPUT_REQUIRED_FIELDS),
        },
        "approval_gate_schema": {
            "approval_gate_type": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE,
            "approval_gate_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
            ),
            "required_fields": list(APPROVAL_GATE_REQUIRED_FIELDS),
            "allowed_approval_gate_statuses": list(ALLOWED_APPROVAL_GATE_STATUSES),
            "allowed_operator_signoff_statuses": list(
                ALLOWED_OPERATOR_SIGNOFF_STATUSES
            ),
            "allowed_future_application_readiness_statuses": list(
                ALLOWED_FUTURE_APPLICATION_READINESS_STATUSES
            ),
            "required_runtime_application_status": "not_applied",
            "required_mutation_status": "no_runtime_mutation",
            "required_production_config_status": "not_created",
            "required_baseline_update_status": "not_replaced",
            "required_model_update_status": "not_modified",
            "human_operator_signoff_required": True,
            "future_blueprint_required_for_runtime_application": True,
        },
        "operator_signoff_schema": {
            "operator_signoff_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_TYPE,
            "operator_signoff_version": (
                CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
            ),
            "required_fields": list(OPERATOR_SIGNOFF_REQUIRED_FIELDS),
            "allowed_signoff_scopes": list(ALLOWED_SIGNOFF_SCOPES),
            "allowed_signoff_statuses": list(ALLOWED_SIGNOFF_RECORD_STATUSES),
            "runtime_application_status": "not_applied",
            "mutation_status": "no_runtime_mutation",
        },
        "blocker_resolution_schema": {
            "required_fields": list(BLOCKER_RESOLUTION_SUMMARY_REQUIRED_FIELDS),
            "allowed_blocker_summary_statuses": list(
                ALLOWED_BLOCKER_SUMMARY_STATUSES
            ),
        },
        "future_application_readiness_schema": {
            "required_fields": list(FUTURE_APPLICATION_READINESS_REQUIRED_FIELDS),
            "allowed_future_application_readiness_statuses": list(
                ALLOWED_FUTURE_APPLICATION_READINESS_STATUSES
            ),
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_approval_gate_input_shape": True,
            "validate_approval_gate_shape": True,
            "validate_operator_signoff_record_shape": True,
            "validate_blocker_resolution_summary_shape": True,
            "validate_future_application_readiness_shape": True,
            "validate_allowed_statuses_and_scopes": True,
            "validate_required_no_mutation_statuses": True,
            "validate_human_operator_signoff_required": True,
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
            "source_dry_run_review_packet_path_recorded": True,
            "source_dry_run_execution_report_path_recorded_when_available": True,
            "source_change_request_path_recorded": True,
            "source_candidate_config_freeze_path_recorded_when_available": True,
            "source_manual_approval_packet_path_recorded_when_available": True,
            "model_asset_ref_required": True,
            "model_asset_sha256_when_available": True,
            "operator_signoff_context_recorded": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _blocker_resolution_summary(
    *,
    review_packet: dict[str, Any],
    inputs: dict[str, Any],
    selected_candidate_ref: dict[str, Any],
) -> dict[str, Any]:
    source_blocker_summary = _dict(review_packet.get("blocker_summary"))
    blockers = set(str(item) for item in _list(source_blocker_summary.get("blockers")))
    source_presence = _dict(inputs.get("source_artifact_presence"))
    if not _source_present(source_presence, "dry_run_review_packet"):
        blockers.add("missing_dry_run_review_packet")
    if not _source_present(source_presence, "change_request"):
        blockers.add("missing_change_request")
    if not selected_candidate_ref:
        blockers.add("missing_candidate_config")
    if _dict(review_packet.get("rollback_readiness_summary")).get(
        "rollback_readiness_status"
    ) not in {"rollback_ready_for_future_phase_review", None}:
        blockers.add("rollback_readiness_incomplete")
    if _dict(review_packet.get("regression_gate_summary")).get(
        "gate_summary_status"
    ) not in {"gate_refs_present", None}:
        blockers.add("regression_gate_incomplete")
    if _dict(review_packet.get("structural_comparison_summary")).get(
        "summary_status"
    ) == "breaking_structural_change_observed":
        blockers.add("breaking_structural_change_observed")
    status = _blocker_status_for_count(len(blockers), review_packet)
    return {
        "blocker_summary_status": status,
        "unresolved_blocker_count": len(blockers),
        "unresolved_blockers": sorted(blockers),
        "operator_review_required": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "human_operator_signoff_required": True,
            "runtime_application_status_not_applied": True,
        },
    }


def _blocker_summary_status(blocker_summary: dict[str, Any]) -> str:
    if not blocker_summary:
        return "blocker_summary_missing"
    blocker_count = int(blocker_summary.get("blocker_count", 0) or 0)
    if blocker_count:
        return "unresolved_blockers_reported"
    return "no_unresolved_blockers_reported"


def _blocker_status_for_count(count: int, review_packet: dict[str, Any]) -> str:
    if not review_packet:
        return "blocker_summary_blocked"
    if count:
        return "unresolved_blockers_reported"
    return "no_unresolved_blockers_reported"


def _warning_summary(warnings: dict[str, Any]) -> dict[str, Any]:
    warning_keys = sorted(str(key) for key, value in warnings.items() if value)
    return {
        "warning_summary_status": (
            "warnings_reported" if warning_keys else "no_warnings_reported"
        ),
        "warning_count": len(warning_keys),
        "warning_keys": warning_keys,
        "human_operator_signoff_required": True,
        "warnings": {
            "inspect_warnings": True,
            "approval_gate_is_not_truth": True,
        },
    }


def _operator_signoff_record(
    *,
    inputs: dict[str, Any],
    review_packet: dict[str, Any],
    selected_candidate_ref: dict[str, Any],
    generated_at: datetime,
    blocker_summary: dict[str, Any],
) -> dict[str, Any]:
    context = _dict(inputs.get("operator_signoff_context"))
    requested_status = str(context.get("signoff_status") or "signoff_required")
    if blocker_summary.get("unresolved_blocker_count", 0) and requested_status in {
        "signoff_recorded_no_runtime_action",
    }:
        signoff_status = "signoff_blocked"
    elif requested_status in ALLOWED_SIGNOFF_RECORD_STATUSES:
        signoff_status = requested_status
    else:
        signoff_status = "signoff_required"
    return {
        "operator_signoff_id": _stable_id(
            "controlled_runtime_calibration_operator_signoff_record_v1",
            inputs.get("approval_gate_input_id"),
            review_packet.get("review_packet_id"),
            selected_candidate_ref,
            signoff_status,
            context.get("operator_identity_ref"),
        ),
        "operator_signoff_type": CONTROLLED_RUNTIME_CALIBRATION_OPERATOR_SIGNOFF_TYPE,
        "operator_signoff_version": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
        ),
        "generated_at": (
            context.get("operator_review_timestamp") or generated_at.isoformat()
        ),
        "operator_identity_ref": context.get("operator_identity_ref"),
        "source_review_packet_ref": _review_packet_ref(review_packet),
        "source_change_request_ref": {
            "change_request_id": inputs.get("change_request_id"),
            "source_change_request_path": inputs.get("source_change_request_path"),
        },
        "selected_candidate_config_ref": selected_candidate_ref,
        "signoff_scope": context.get("signoff_scope")
        if context.get("signoff_scope") in ALLOWED_SIGNOFF_SCOPES
        else "no_runtime_action_acknowledgement",
        "signoff_status": signoff_status,
        "signoff_notes": context.get("signoff_notes"),
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "warnings": {
            "operator_signoff_recorded_no_runtime_action": (
                signoff_status == "signoff_recorded_no_runtime_action"
            ),
            "human_operator_signoff_required": True,
            "runtime_application_status_not_applied": True,
        },
        "non_claims": dict(NON_CLAIMS),
    }


def _operator_signoff_status(
    signoff_record: dict[str, Any],
    blocker_summary: dict[str, Any],
) -> str:
    signoff_status = signoff_record.get("signoff_status")
    if blocker_summary.get("unresolved_blocker_count", 0) and signoff_status in {
        "signoff_recorded_no_runtime_action",
    }:
        return "operator_signoff_blocked"
    if signoff_status == "signoff_recorded_no_runtime_action":
        return "operator_signoff_recorded_no_runtime_action"
    if signoff_status == "signoff_pending":
        return "operator_signoff_pending"
    if signoff_status == "signoff_blocked":
        return "operator_signoff_blocked"
    if signoff_status == "signoff_not_applicable":
        return "operator_signoff_not_applicable"
    return "operator_signoff_required"


def _future_application_readiness(
    *,
    review_packet: dict[str, Any],
    selected_candidate_ref: dict[str, Any],
    blocker_summary: dict[str, Any],
    operator_signoff_status: str,
) -> dict[str, Any]:
    requirements = [
        _requirement(
            "explicit_human_signoff_artifact",
            operator_signoff_status == "operator_signoff_recorded_no_runtime_action",
        ),
        _requirement("selected_candidate_config_freeze_ref", bool(selected_candidate_ref)),
        _requirement(
            "controlled_change_request_ref",
            bool(review_packet.get("source_change_request_path")),
        ),
        _requirement(
            "dry_run_execution_report_ref",
            bool(review_packet.get("source_dry_run_execution_report_path")),
        ),
        _requirement("dry_run_review_packet_ref", bool(review_packet)),
        _requirement(
            "rollback_readiness_ref",
            _dict(review_packet.get("rollback_readiness_summary")).get(
                "rollback_readiness_status"
            )
            == "rollback_ready_for_future_phase_review",
        ),
        _requirement(
            "all_required_regression_gates_passing",
            _dict(review_packet.get("regression_gate_summary")).get(
                "gate_summary_status"
            )
            == "gate_refs_present",
        ),
        _requirement(
            "no_unresolved_blockers",
            blocker_summary.get("unresolved_blocker_count", 0) == 0,
        ),
        _requirement(
            "explicit_rollback_plan",
            _dict(review_packet.get("rollback_readiness_summary")).get(
                "rollback_plan_present"
            )
            is True,
        ),
        _requirement("explicit_runtime_config_change_proposal", False),
        _requirement("dry_run_to_runtime_comparison_plan", False),
        _requirement("post_application_review_plan", False),
        _requirement("post_application_regression_gate", False),
        _requirement("future_baseline_candidate_policy", False),
        _requirement("explicit_no_truth_no_accuracy_claim_statement", True),
    ]
    missing_requirements = [
        str(item["requirement"]) for item in requirements if item["status"] != "present"
    ]
    if not review_packet:
        readiness_status = "future_application_blocked"
    elif not selected_candidate_ref:
        readiness_status = "future_application_not_applicable"
    elif blocker_summary.get("unresolved_blocker_count", 0):
        readiness_status = "future_application_blocked"
    elif operator_signoff_status != "operator_signoff_recorded_no_runtime_action":
        readiness_status = "future_application_not_ready"
    elif missing_requirements:
        readiness_status = "future_application_requires_new_blueprint"
    else:
        readiness_status = "future_application_ready_for_separate_change_request"
    return {
        "future_application_readiness_status": readiness_status,
        "future_blueprint_required_for_runtime_application": True,
        "runtime_application_status": "not_applied",
        "mutation_status": "no_runtime_mutation",
        "requirements": requirements,
        "missing_requirements": missing_requirements,
        "warnings": {
            "future_blueprint_required_for_runtime_application": True,
            "future_application_readiness": True,
            "runtime_application_status_not_applied": True,
        },
    }


def _requirement(name: str, present: bool) -> dict[str, Any]:
    return {
        "requirement": name,
        "status": "present" if present else "missing",
        "runtime_application_status": "not_applied",
        "warnings": {"future_blueprint_required_for_runtime_application": True},
    }


def _approval_gate_status(
    *,
    review_packet: dict[str, Any],
    selected_candidate_ref: dict[str, Any],
    blocker_summary: dict[str, Any],
    operator_signoff_status: str,
    readiness_status: str,
) -> str:
    blockers = set(str(item) for item in _list(blocker_summary.get("unresolved_blockers")))
    if "missing_dry_run_review_packet" in blockers:
        return "approval_gate_blocked_missing_review_packet"
    if "missing_change_request" in blockers:
        return "approval_gate_blocked_missing_change_request"
    if "missing_candidate_config" in blockers and not review_packet:
        return "approval_gate_blocked_missing_candidate_config"
    if "rollback_readiness_incomplete" in blockers:
        return "approval_gate_blocked_missing_rollback_readiness"
    if "regression_gate_incomplete" in blockers:
        return "approval_gate_blocked_missing_regression_gate"
    if "breaking_structural_change_observed" in blockers:
        return "approval_gate_blocked_breaking_structural_change"
    if not selected_candidate_ref:
        return "approval_gate_informational_only"
    if blockers:
        return "approval_gate_blocked_unresolved_blockers"
    if operator_signoff_status != "operator_signoff_recorded_no_runtime_action":
        return "approval_gate_waiting_for_operator_signoff"
    if readiness_status == "future_application_ready_for_separate_change_request":
        return "approval_gate_human_signoff_recorded_no_runtime_action"
    return "approval_gate_created_with_warnings"


def _review_packet_ref(review_packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_packet_id": review_packet.get("review_packet_id"),
        "review_packet_status": review_packet.get("review_packet_status"),
        "source_dry_run_review_packet_path": review_packet.get(
            "source_review_packet_input_path"
        ),
    }


def _change_request_ref(
    change_request: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    return {
        "change_request_id": change_request.get("change_request_id")
        or inputs.get("change_request_id"),
        "source_change_request_path": inputs.get("source_change_request_path"),
    }


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
        != CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_TYPE
    ):
        errors.append(_error("invalid_contract_type", "contract_type", None))
    if (
        contract.get("contract_version")
        != CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_CONTRACT_VERSION
    ):
        errors.append(_error("invalid_contract_version", "contract_version", None))
    for section in (
        "approval_gate_scope",
        "source_contract_refs",
        "approval_gate_input_schema",
        "approval_gate_schema",
        "operator_signoff_schema",
        "blocker_resolution_schema",
        "future_application_readiness_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    return errors


def _validate_inputs_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(inputs, "approval_gate_inputs")
    _require_fields(
        inputs,
        APPROVAL_GATE_INPUT_REQUIRED_FIELDS,
        "approval_gate_inputs",
        errors,
    )
    if (
        inputs.get("approval_gate_input_type")
        != CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_approval_gate_input_type",
                "approval_gate_input_type",
                inputs.get("approval_gate_input_type"),
            )
        )
    if (
        inputs.get("approval_gate_input_version")
        != CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_approval_gate_input_version",
                "approval_gate_input_version",
                inputs.get("approval_gate_input_version"),
            )
        )
    context = _dict(inputs.get("operator_signoff_context"))
    _validate_allowed(
        context.get("signoff_scope"),
        ALLOWED_SIGNOFF_SCOPES,
        "operator_signoff_context.signoff_scope",
        errors,
    )
    _validate_allowed(
        context.get("signoff_status"),
        ALLOWED_SIGNOFF_RECORD_STATUSES,
        "operator_signoff_context.signoff_status",
        errors,
    )
    _validate_non_claims(inputs, errors, path="approval_gate_inputs.non_claims")
    return errors


def _validate_gate_shape(gate: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(gate, "approval_gate")
    _require_fields(gate, APPROVAL_GATE_REQUIRED_FIELDS, "approval_gate", errors)
    if gate.get("approval_gate_type") != CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_TYPE:
        errors.append(
            _error(
                "invalid_approval_gate_type",
                "approval_gate_type",
                gate.get("approval_gate_type"),
            )
        )
    if (
        gate.get("approval_gate_version")
        != CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
    ):
        errors.append(
            _error(
                "invalid_approval_gate_version",
                "approval_gate_version",
                gate.get("approval_gate_version"),
            )
        )
    _validate_required_status(
        gate,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
        errors,
    )
    _validate_required_status(
        gate,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_required_status(
        gate,
        "production_config_status",
        "not_created",
        ["not_created", "not_applicable"],
        errors,
    )
    _validate_required_status(
        gate,
        "baseline_update_status",
        "not_replaced",
        ["not_replaced", "not_applicable"],
        errors,
    )
    _validate_required_status(
        gate,
        "model_update_status",
        "not_modified",
        ["not_modified", "not_applicable"],
        errors,
    )
    _validate_required_bool(
        gate,
        "future_blueprint_required_for_runtime_application",
        True,
        errors,
    )
    _validate_required_bool(
        gate,
        "human_operator_signoff_required",
        True,
        errors,
    )
    _validate_allowed(
        gate.get("approval_gate_status"),
        ALLOWED_APPROVAL_GATE_STATUSES,
        "approval_gate_status",
        errors,
    )
    _validate_allowed(
        gate.get("operator_signoff_status"),
        ALLOWED_OPERATOR_SIGNOFF_STATUSES,
        "operator_signoff_status",
        errors,
    )
    _validate_allowed(
        gate.get("future_application_readiness_status"),
        ALLOWED_FUTURE_APPLICATION_READINESS_STATUSES,
        "future_application_readiness_status",
        errors,
    )
    _validate_allowed(
        gate.get("blocker_summary_status"),
        ALLOWED_BLOCKER_SUMMARY_STATUSES,
        "blocker_summary_status",
        errors,
    )
    _validate_allowed(
        gate.get("warning_summary_status"),
        ALLOWED_WARNING_SUMMARY_STATUSES,
        "warning_summary_status",
        errors,
    )
    errors.extend(
        _validate_operator_signoff_shape(_dict(gate.get("operator_signoff_record")))
    )
    errors.extend(
        _validate_blocker_resolution_shape(
            _dict(gate.get("blocker_resolution_summary"))
        )
    )
    errors.extend(
        _validate_future_application_readiness_shape(
            _dict(gate.get("future_application_requirements"))
        )
    )
    _validate_non_claims(gate, errors, path="approval_gate.non_claims")
    return errors


def _validate_operator_signoff_shape(record: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(record, "operator_signoff_record")
    _require_fields(
        record,
        OPERATOR_SIGNOFF_REQUIRED_FIELDS,
        "operator_signoff_record",
        errors,
    )
    _validate_allowed(
        record.get("signoff_scope"),
        ALLOWED_SIGNOFF_SCOPES,
        "operator_signoff_record.signoff_scope",
        errors,
    )
    _validate_allowed(
        record.get("signoff_status"),
        ALLOWED_SIGNOFF_RECORD_STATUSES,
        "operator_signoff_record.signoff_status",
        errors,
    )
    _validate_required_status(
        record,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
        errors,
    )
    _validate_required_status(
        record,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
    )
    _validate_non_claims(record, errors, path="operator_signoff_record.non_claims")
    return errors


def _validate_blocker_resolution_shape(
    summary: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(summary, "blocker_resolution_summary")
    _require_fields(
        summary,
        BLOCKER_RESOLUTION_SUMMARY_REQUIRED_FIELDS,
        "blocker_resolution_summary",
        errors,
    )
    _validate_allowed(
        summary.get("blocker_summary_status"),
        ALLOWED_BLOCKER_SUMMARY_STATUSES,
        "blocker_resolution_summary.blocker_summary_status",
        errors,
    )
    if not isinstance(summary.get("unresolved_blocker_count"), int):
        errors.append(
            _error(
                "invalid_unresolved_blocker_count",
                "blocker_resolution_summary.unresolved_blocker_count",
                summary.get("unresolved_blocker_count"),
            )
        )
    return errors


def _validate_future_application_readiness_shape(
    readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(readiness, "future_application_readiness")
    _require_fields(
        readiness,
        FUTURE_APPLICATION_READINESS_REQUIRED_FIELDS,
        "future_application_readiness",
        errors,
    )
    _validate_allowed(
        readiness.get("future_application_readiness_status"),
        ALLOWED_FUTURE_APPLICATION_READINESS_STATUSES,
        "future_application_readiness.future_application_readiness_status",
        errors,
    )
    _validate_required_bool(
        readiness,
        "future_blueprint_required_for_runtime_application",
        True,
        errors,
    )
    _validate_required_status(
        readiness,
        "runtime_application_status",
        "not_applied",
        ["not_applied", "not_applicable"],
        errors,
    )
    _validate_required_status(
        readiness,
        "mutation_status",
        "no_runtime_mutation",
        ["no_runtime_mutation", "not_applicable"],
        errors,
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
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_VERSION
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
            if str(key) in FORBIDDEN_APPROVAL_GATE_TOKENS:
                errors.append(_error("forbidden_field_or_value", child_path, key))
            errors.extend(_forbidden_token_errors(nested, child_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str) and value in FORBIDDEN_APPROVAL_GATE_TOKENS:
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
        "blueprint": CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_BLUEPRINT,
        "blueprint_name": (
            CONTROLLED_RUNTIME_CALIBRATION_HUMAN_APPROVAL_GATE_BLUEPRINT_NAME
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
