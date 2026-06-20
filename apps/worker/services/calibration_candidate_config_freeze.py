from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.calibration_candidate_decision_packet import (
    CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION,
    DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT,
    DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT,
)
from apps.worker.services.calibration_candidate_decision_packet import (
    SOURCE_CONTRACT_REFS as DECISION_PACKET_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.gameplay_gate_regression_baseline import (
    DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT,
)
from apps.worker.services.gameplay_segment_gate import (
    DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
)
from apps.worker.services.real_broadcast_gameplay_gate_corpus_run import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
)
from apps.worker.services.real_broadcast_gameplay_review_loop import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT,
)
from apps.worker.services.real_broadcast_gameplay_review_metrics import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT,
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_gate_calibration_proposal import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT,
)

CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_TYPE = (
    "calibration_candidate_config_freeze_contract"
)
CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION = "v1"
CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE = (
    "calibration_candidate_config_freeze_inputs"
)
CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_VERSION = "v1"
CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE = "calibration_candidate_config_freeze"
CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION = "v1"
CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE = (
    "calibration_candidate_manual_approval_packet"
)
CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VERSION = "v1"
CALIBRATION_CANDIDATE_CONFIG_FREEZE_REPORT_TYPE = (
    "calibration_candidate_config_freeze_report"
)
CALIBRATION_CANDIDATE_CONFIG_FREEZE_BLUEPRINT = "blueprint_53"
CALIBRATION_CANDIDATE_CONFIG_FREEZE_BLUEPRINT_NAME = (
    "candidate_config_freeze_manual_approval_packet_v1"
)

DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT = (
    ".data/contracts/calibration_candidate_config_freeze_contract_v1.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_ARTIFACT_OUTPUT = (
    ".data/contracts/calibration_candidate_config_freeze_v1.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUTS_OUTPUT = (
    ".data/exports/calibration_candidate_config_freeze_inputs.current.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/calibration_candidate_config_freeze_inputs.validation.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_OUTPUT = (
    ".data/exports/calibration_candidate_config_freeze.current.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_VALIDATION_OUTPUT = (
    ".data/exports/calibration_candidate_config_freeze.validation.json"
)
DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT = (
    ".data/exports/calibration_candidate_manual_approval_packet.current.json"
)
DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VALIDATION_OUTPUT = (
    ".data/exports/calibration_candidate_manual_approval_packet.validation.json"
)
DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_REPORT_OUTPUT = (
    ".data/exports/calibration_candidate_config_freeze.report.json"
)

CALIBRATION_CANDIDATE_CONFIG_FREEZE_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "calibration_candidate_decision_packet_contract_version": (
        CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION
    ),
    **dict(DECISION_PACKET_SOURCE_CONTRACT_REFS),
}

ALLOWED_CANDIDATE_TYPES = [
    "threshold_candidate",
    "smoothing_window_candidate",
    "hysteresis_candidate",
    "combined_candidate",
    "no_candidate",
    "not_applicable",
]
ALLOWED_CANDIDATE_CONFIG_STATUSES = [
    "frozen_for_manual_review",
    "blocked_missing_review_data",
    "blocked_regression_drift",
    "blocked_insufficient_sample_size",
    "blocked_fixture_only_data",
    "blocked_invalid_candidate",
    "informational_only",
    "no_candidate_selected",
    "not_applicable",
]
ALLOWED_MANUAL_APPROVAL_STATUSES = [
    "not_reviewed_by_operator",
    "operator_review_required",
    "operator_review_in_progress",
    "operator_review_completed_no_runtime_action",
    "blocked_from_manual_approval",
    "not_applicable",
]
ALLOWED_RUNTIME_APPLICATION_STATUSES = [
    "not_applied",
    "runtime_application_not_supported",
    "future_manual_application_required",
    "blocked_from_runtime_application",
    "not_applicable",
]
ALLOWED_APPROVAL_BLOCKERS = [
    "missing_operator_review",
    "missing_human_review_data",
    "insufficient_review_coverage",
    "regression_gate_warning",
    "regression_gate_blocked",
    "fixture_only_evidence",
    "missing_decision_packet",
    "missing_sandbox_evaluation",
    "missing_sandbox_regression",
    "invalid_candidate_config",
    "not_applicable",
]
ALLOWED_OPERATOR_CHECKLIST_ITEMS = [
    "reviewed_candidate_packet",
    "reviewed_review_coverage",
    "reviewed_sandbox_evaluation",
    "reviewed_sandbox_regression_gate",
    "reviewed_gameplay_regression_gate",
    "reviewed_non_claims",
    "confirmed_no_runtime_application",
    "confirmed_model_weights_unchanged",
    "confirmed_baselines_unchanged",
    "confirmed_human_approval_required",
]
ALLOWED_OPERATOR_NEXT_ACTION_TYPES = [
    "review_candidate_config_freeze",
    "collect_more_human_review",
    "inspect_regression_drift",
    "inspect_boundary_segments",
    "inspect_ambiguity_cluster",
    "inspect_missing_review_fields",
    "prepare_followup_real_data_review",
    "prepare_future_runtime_change_request",
    "do_not_apply_runtime_change",
    "no_action",
    "not_applicable",
]

CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS = {
    "candidate_config_freeze_is_not_truth": True,
    "candidate_config_freeze_is_not_accuracy_scoring": True,
    "candidate_config_freeze_is_not_runtime_calibration": True,
    "manual_approval_packet_is_not_runtime_config": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "runtime_config_not_updated": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_operator_approval_required": True,
    "classifier_correctness_not_assessed": True,
    "structural_manual_approval_support_only": True,
}
NON_CLAIMS = {
    "candidate_config_freeze_is_not_truth": True,
    "candidate_config_freeze_is_not_accuracy_scoring": True,
    "candidate_config_freeze_is_not_runtime_calibration": True,
    "manual_approval_packet_is_not_runtime_config": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "runtime_config_not_updated": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "automatic_approval_not_performed": True,
    "automatic_rejection_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_operator_approval_required": True,
}

FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS = {
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
    "runtime_config",
    "production_config",
}

FREEZE_INPUT_REQUIRED_FIELDS = [
    "freeze_input_id",
    "freeze_input_type",
    "freeze_input_version",
    "generated_at",
    "source_decision_packet_path",
    "source_sandbox_evaluation_report_path",
    "source_sandbox_regression_verification_path",
    "source_calibration_proposal_path",
    "source_review_metrics_report_path",
    "source_review_loop_report_path",
    "source_corpus_run_path",
    "source_gameplay_gate_regression_baseline_path",
    "source_calibration_sandbox_baseline_path",
    "model_asset_ref",
    "model_asset_sha256",
    "current_threshold",
    "current_smoothing_window",
    "current_hysteresis_settings",
    "current_settings",
    "candidate_packet_refs",
    "selected_candidate_packet_ref",
    "operator_context",
    "warnings",
    "non_claims",
]
FREEZE_REQUIRED_FIELDS = [
    "candidate_config_freeze_id",
    "candidate_config_freeze_type",
    "candidate_config_freeze_version",
    "generated_at",
    "source_freeze_input_path",
    "source_decision_packet_path",
    "selected_candidate_packet_ref",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "candidate_settings",
    "candidate_config_status",
    "manual_approval_status",
    "runtime_application_status",
    "not_applied",
    "approval_required",
    "approval_blockers",
    "required_preconditions",
    "supporting_evidence_refs",
    "regression_gate_summary",
    "review_coverage_summary",
    "risk_flags",
    "warnings",
    "non_claims",
]
MANUAL_APPROVAL_PACKET_REQUIRED_FIELDS = [
    "manual_approval_packet_id",
    "manual_approval_packet_type",
    "manual_approval_packet_version",
    "generated_at",
    "source_candidate_config_freeze_path",
    "operator_review_status",
    "approval_required",
    "runtime_application_status",
    "candidate_config_summary",
    "supporting_evidence_summary",
    "blockers",
    "operator_checklist",
    "operator_next_actions",
    "warnings",
    "non_claims",
]


def export_calibration_candidate_config_freeze_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or CALIBRATION_CANDIDATE_CONFIG_FREEZE_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_TYPE,
        "contract_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION,
        "contract": contract,
        "warnings": dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_calibration_candidate_config_freeze_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    source_decision_packet_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT
    ),
    source_sandbox_evaluation_report_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    source_sandbox_regression_verification_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT
    ),
    source_calibration_proposal_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT
    ),
    source_review_metrics_report_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT
    ),
    source_review_loop_report_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT
    ),
    source_corpus_run_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
    source_gameplay_gate_regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    source_calibration_sandbox_baseline_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT
    ),
    selected_candidate_packet_ref: str | None = None,
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    decision_packet = _load_required_json(
        source_decision_packet_path,
        "source_decision_packet",
        errors,
    )
    sandbox_evaluation_report = _load_required_json(
        source_sandbox_evaluation_report_path,
        "source_sandbox_evaluation_report",
        errors,
    )
    sandbox_regression_verification = _load_required_json(
        source_sandbox_regression_verification_path,
        "source_sandbox_regression_verification",
        errors,
    )
    calibration_proposal = _load_optional_json(source_calibration_proposal_path)
    review_metrics_report = _load_optional_json(source_review_metrics_report_path)
    review_loop_report = _load_optional_json(source_review_loop_report_path)
    corpus_run = _load_optional_json(source_corpus_run_path)
    gameplay_gate_regression_baseline = _load_optional_json(
        source_gameplay_gate_regression_baseline_path
    )
    calibration_sandbox_baseline = _load_optional_json(
        source_calibration_sandbox_baseline_path
    )
    errors.extend(
        _validate_source_artifacts(
            decision_packet=decision_packet,
            sandbox_evaluation_report=sandbox_evaluation_report,
            sandbox_regression_verification=sandbox_regression_verification,
        )
    )
    source_payloads = {
        "decision_packet": decision_packet,
        "sandbox_evaluation_report": sandbox_evaluation_report,
        "sandbox_regression_verification": sandbox_regression_verification,
        "calibration_proposal": calibration_proposal,
        "review_metrics_report": review_metrics_report,
        "review_loop_report": review_loop_report,
        "corpus_run": corpus_run,
        "gameplay_gate_regression_baseline": gameplay_gate_regression_baseline,
        "calibration_sandbox_baseline": calibration_sandbox_baseline,
    }
    errors.extend(_forbidden_token_errors(_source_scan_payload(source_payloads), "sources"))
    if errors:
        return _failed_result(
            status="invalid_freeze_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE,
            result_key="freeze_inputs_output",
        )

    model_asset_ref, model_asset_sha256 = _model_asset_identity(
        source_payloads=source_payloads,
        model_asset_path=model_asset_path,
    )
    selected_ref = _selected_candidate_ref(
        decision_packet=decision_packet,
        selected_candidate_packet_ref=selected_candidate_packet_ref,
    )
    current_settings = _current_settings(
        decision_packet=decision_packet,
        sandbox_evaluation_report=sandbox_evaluation_report,
        calibration_proposal=calibration_proposal,
    )
    freeze_inputs = {
        "freeze_input_id": _stable_id(
            "calibration_candidate_config_freeze_inputs_v1",
            source_decision_packet_path,
            source_sandbox_evaluation_report_path,
            source_sandbox_regression_verification_path,
            selected_ref.get("candidate_packet_id"),
            model_asset_sha256,
        ),
        "freeze_input_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE,
        "freeze_input_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_decision_packet_path": str(Path(source_decision_packet_path)),
        "source_sandbox_evaluation_report_path": str(
            Path(source_sandbox_evaluation_report_path)
        ),
        "source_sandbox_regression_verification_path": str(
            Path(source_sandbox_regression_verification_path)
        ),
        "source_calibration_proposal_path": _path_string(source_calibration_proposal_path),
        "source_review_metrics_report_path": _path_string(source_review_metrics_report_path),
        "source_review_loop_report_path": _path_string(source_review_loop_report_path),
        "source_corpus_run_path": _path_string(source_corpus_run_path),
        "source_gameplay_gate_regression_baseline_path": _path_string(
            source_gameplay_gate_regression_baseline_path
        ),
        "source_calibration_sandbox_baseline_path": _path_string(
            source_calibration_sandbox_baseline_path
        ),
        "source_decision_packet_contract_path": str(
            Path(DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT)
        ),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha256,
        "current_threshold": current_settings.get("current_threshold"),
        "current_smoothing_window": current_settings.get("current_smoothing_window"),
        "current_hysteresis_settings": _dict(
            current_settings.get("current_hysteresis_settings")
        ),
        "current_settings": current_settings,
        "candidate_packet_refs": _candidate_packet_refs(decision_packet),
        "selected_candidate_packet_ref": selected_ref or None,
        "operator_context": {
            "operator_review_required": bool(selected_ref),
            "human_operator_approval_required": True,
            "future_manual_review_candidate": bool(selected_ref),
            "structural_drift_summary": _regression_gate_summary(decision_packet),
            "classifier_correctness_not_assessed": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_freeze_inputs_shape(freeze_inputs)
    if validation_errors:
        return _failed_result(
            status="invalid_freeze_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE,
            result_key="freeze_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "freeze_input_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE,
        "freeze_input_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_VERSION,
        "freeze_input_id": freeze_inputs["freeze_input_id"],
        "freeze_inputs": freeze_inputs,
        "selected_candidate_packet_ref": freeze_inputs["selected_candidate_packet_ref"],
        "warnings": freeze_inputs["warnings"],
    }
    _write_json_if_requested(output_path, freeze_inputs, result, "freeze_inputs_output")
    return result


def validate_calibration_candidate_config_freeze_inputs(
    *,
    freeze_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    freeze_inputs = _load_required_json(freeze_inputs_path, "freeze_inputs", errors)
    if freeze_inputs:
        errors.extend(_validate_freeze_inputs_shape(freeze_inputs))
    result = _validation_result(
        ok=not errors,
        validation_type="calibration_candidate_config_freeze_inputs_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=freeze_inputs_path,
        payload_type=freeze_inputs.get("freeze_input_type") if freeze_inputs else None,
        payload_version=(
            freeze_inputs.get("freeze_input_version") if freeze_inputs else None
        ),
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_calibration_candidate_config_freeze(
    *,
    freeze_inputs_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_calibration_candidate_config_freeze_inputs(
        freeze_inputs_path=freeze_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_freeze_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE,
            result_key="candidate_config_freeze_output",
        )
    freeze_inputs = _dict(_load_json(freeze_inputs_path, label="freeze_inputs").get("data"))
    selected_ref = _dict(freeze_inputs.get("selected_candidate_packet_ref"))
    selected_candidate = _candidate_ref_by_id(
        freeze_inputs=freeze_inputs,
        candidate_packet_id=selected_ref.get("candidate_packet_id"),
    )
    candidate_config_status = _candidate_config_status(selected_candidate)
    approval_required = bool(selected_candidate)
    approval_blockers = _approval_blockers(
        selected_candidate=selected_candidate,
        freeze_inputs=freeze_inputs,
        candidate_config_status=candidate_config_status,
    )
    freeze = {
        "candidate_config_freeze_id": _stable_id(
            "calibration_candidate_config_freeze_v1",
            freeze_inputs.get("freeze_input_id"),
            selected_ref.get("candidate_packet_id"),
            freeze_inputs.get("model_asset_sha256"),
        ),
        "candidate_config_freeze_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE,
        "candidate_config_freeze_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_freeze_input_path": str(Path(freeze_inputs_path)),
        "freeze_input_id": freeze_inputs.get("freeze_input_id"),
        "source_decision_packet_path": freeze_inputs.get("source_decision_packet_path"),
        "selected_candidate_packet_ref": selected_ref or None,
        "model_asset_ref": freeze_inputs.get("model_asset_ref"),
        "model_asset_sha256": freeze_inputs.get("model_asset_sha256"),
        "current_settings": _dict(freeze_inputs.get("current_settings")),
        "candidate_settings": _candidate_settings(selected_candidate),
        "candidate_config_status": candidate_config_status,
        "manual_approval_status": _manual_approval_status(
            candidate_config_status=candidate_config_status,
            selected_candidate=selected_candidate,
        ),
        "runtime_application_status": "not_applied",
        "not_applied": True,
        "approval_required": approval_required,
        "approval_blockers": approval_blockers,
        "required_preconditions": _required_preconditions(
            selected_candidate=selected_candidate,
            approval_required=approval_required,
        ),
        "supporting_evidence_refs": _supporting_evidence_refs(
            freeze_inputs=freeze_inputs,
            selected_candidate=selected_candidate,
        ),
        "regression_gate_summary": _regression_gate_summary_from_inputs(freeze_inputs),
        "review_coverage_summary": _review_coverage_summary_from_inputs(freeze_inputs),
        "risk_flags": _risk_flags(
            selected_candidate=selected_candidate,
            approval_blockers=approval_blockers,
            candidate_config_status=candidate_config_status,
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(freeze_inputs.get("warnings")),
            **dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_candidate_config_freeze_shape(freeze)
    if validation_errors:
        return _failed_result(
            status="invalid_candidate_config_freeze",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE,
            result_key="candidate_config_freeze_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "candidate_config_freeze_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE,
        "candidate_config_freeze_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION,
        "candidate_config_freeze_id": freeze["candidate_config_freeze_id"],
        "candidate_config_freeze": freeze,
        "candidate_config_status": freeze["candidate_config_status"],
        "runtime_application_status": freeze["runtime_application_status"],
        "approval_required": freeze["approval_required"],
        "not_applied": freeze["not_applied"],
        "warnings": freeze["warnings"],
    }
    _write_json_if_requested(output_path, freeze, result, "candidate_config_freeze_output")
    return result


def validate_calibration_candidate_config_freeze(
    *,
    candidate_config_freeze_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    freeze = _load_required_json(
        candidate_config_freeze_path,
        "candidate_config_freeze",
        errors,
    )
    if freeze:
        errors.extend(_validate_candidate_config_freeze_shape(freeze))
    result = _validation_result(
        ok=not errors,
        validation_type="calibration_candidate_config_freeze_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=candidate_config_freeze_path,
        payload_type=freeze.get("candidate_config_freeze_type") if freeze else None,
        payload_version=freeze.get("candidate_config_freeze_version") if freeze else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_calibration_candidate_manual_approval_packet(
    *,
    candidate_config_freeze_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_calibration_candidate_config_freeze(
        candidate_config_freeze_path=candidate_config_freeze_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_candidate_config_freeze",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE,
            result_key="manual_approval_packet_output",
        )
    freeze = _dict(
        _load_json(
            candidate_config_freeze_path,
            label="candidate_config_freeze",
        ).get("data")
    )
    operator_next_actions = _operator_next_actions(freeze)
    packet = {
        "manual_approval_packet_id": _stable_id(
            "calibration_candidate_manual_approval_packet_v1",
            freeze.get("candidate_config_freeze_id"),
            freeze.get("candidate_config_status"),
            freeze.get("model_asset_sha256"),
        ),
        "manual_approval_packet_type": CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE,
        "manual_approval_packet_version": (
            CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_candidate_config_freeze_path": str(Path(candidate_config_freeze_path)),
        "candidate_config_freeze_id": freeze.get("candidate_config_freeze_id"),
        "operator_review_status": freeze.get("manual_approval_status"),
        "approval_required": freeze.get("approval_required") is True,
        "runtime_application_status": "not_applied",
        "candidate_config_summary": _candidate_config_summary(freeze),
        "supporting_evidence_summary": _supporting_evidence_summary(freeze),
        "blockers": _list(freeze.get("approval_blockers")),
        "operator_checklist": _operator_checklist(freeze),
        "operator_next_actions": operator_next_actions,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(freeze.get("warnings")),
            **dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_manual_approval_packet_shape(packet)
    if validation_errors:
        return _failed_result(
            status="invalid_manual_approval_packet",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE,
            result_key="manual_approval_packet_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "manual_approval_packet_type": CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE,
        "manual_approval_packet_version": (
            CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VERSION
        ),
        "manual_approval_packet_id": packet["manual_approval_packet_id"],
        "manual_approval_packet": packet,
        "runtime_application_status": packet["runtime_application_status"],
        "approval_required": packet["approval_required"],
        "warnings": packet["warnings"],
    }
    _write_json_if_requested(output_path, packet, result, "manual_approval_packet_output")
    return result


def validate_calibration_candidate_manual_approval_packet(
    *,
    manual_approval_packet_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    packet = _load_required_json(
        manual_approval_packet_path,
        "manual_approval_packet",
        errors,
    )
    if packet:
        errors.extend(_validate_manual_approval_packet_shape(packet))
    result = _validation_result(
        ok=not errors,
        validation_type="calibration_candidate_manual_approval_packet_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=manual_approval_packet_path,
        payload_type=packet.get("manual_approval_packet_type") if packet else None,
        payload_version=packet.get("manual_approval_packet_version") if packet else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_calibration_candidate_config_freeze_report(
    *,
    candidate_config_freeze_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_OUTPUT
    ),
    manual_approval_packet_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_CONFIG_FREEZE_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    freeze_validation = validate_calibration_candidate_config_freeze(
        candidate_config_freeze_path=candidate_config_freeze_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    packet_validation: dict[str, Any] | None = None
    manual_packet: dict[str, Any] = {}
    if manual_approval_packet_path:
        packet_validation = validate_calibration_candidate_manual_approval_packet(
            manual_approval_packet_path=manual_approval_packet_path,
            contract_path=contract_path,
            output_path=None,
            validated_at=generated_at,
        )
        manual_packet = _dict(
            _load_json(
                manual_approval_packet_path,
                label="manual_approval_packet",
            ).get("data")
        )
    freeze = _dict(
        _load_json(
            candidate_config_freeze_path,
            label="candidate_config_freeze",
        ).get("data")
    )
    report = {
        "report_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_REPORT_TYPE,
        "report_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_candidate_config_freeze_path": str(Path(candidate_config_freeze_path)),
        "source_manual_approval_packet_path": _path_string(manual_approval_packet_path),
        "candidate_config_freeze_id": freeze.get("candidate_config_freeze_id"),
        "manual_approval_packet_id": manual_packet.get("manual_approval_packet_id"),
        "candidate_config_summary": _candidate_config_summary(freeze),
        "manual_approval_summary": {
            "operator_review_status": manual_packet.get("operator_review_status"),
            "approval_required": manual_packet.get("approval_required") is True,
            "runtime_application_status": "not_applied",
            "blocker_count": len(_list(manual_packet.get("blockers"))),
            "operator_next_action_count": len(
                _list(manual_packet.get("operator_next_actions"))
            ),
        },
        "structural_drift_summary": _dict(freeze.get("regression_gate_summary")),
        "review_coverage_summary": _dict(freeze.get("review_coverage_summary")),
        "blockers": _list(freeze.get("approval_blockers")),
        "risk_flags": _list(freeze.get("risk_flags")),
        "freeze_validation_snapshot": freeze_validation,
        "manual_approval_validation_snapshot": packet_validation,
        "warnings": {
            **_dict(freeze.get("warnings")),
            **dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result_errors = _list(freeze_validation.get("errors"))
    if packet_validation:
        result_errors.extend(_list(packet_validation.get("errors")))
    result_errors.extend(_forbidden_token_errors(report, "report"))
    result = {
        "ok": not result_errors,
        "status": "completed" if not result_errors else "invalid_freeze_report",
        "report_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_REPORT_TYPE,
        "report_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION,
        "candidate_config_freeze_id": freeze.get("candidate_config_freeze_id"),
        "report": report,
        "errors": result_errors,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_TYPE,
        "contract_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "freeze_scope": {
            "purpose": "candidate_config_freeze_manual_approval_support",
            "packages_decision_packet": True,
            "packages_sandbox_evaluation": True,
            "packages_regression_gate_result": True,
            "supports_manual_operator_review": True,
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
        "freeze_input_schema": {
            "freeze_input_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE,
            "freeze_input_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_VERSION,
            "required_fields": list(FREEZE_INPUT_REQUIRED_FIELDS),
        },
        "candidate_config_schema": {
            "candidate_config_freeze_type": CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE,
            "candidate_config_freeze_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION,
            "required_fields": list(FREEZE_REQUIRED_FIELDS),
            "allowed_candidate_types": list(ALLOWED_CANDIDATE_TYPES),
            "allowed_candidate_config_statuses": list(
                ALLOWED_CANDIDATE_CONFIG_STATUSES
            ),
            "allowed_manual_approval_statuses": list(ALLOWED_MANUAL_APPROVAL_STATUSES),
            "allowed_runtime_application_statuses": list(
                ALLOWED_RUNTIME_APPLICATION_STATUSES
            ),
            "allowed_approval_blockers": list(ALLOWED_APPROVAL_BLOCKERS),
            "requires_not_applied": True,
        },
        "manual_approval_packet_schema": {
            "manual_approval_packet_type": (
                CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE
            ),
            "manual_approval_packet_version": (
                CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VERSION
            ),
            "required_fields": list(MANUAL_APPROVAL_PACKET_REQUIRED_FIELDS),
            "allowed_operator_checklist_items": list(ALLOWED_OPERATOR_CHECKLIST_ITEMS),
            "allowed_operator_next_action_types": list(
                ALLOWED_OPERATOR_NEXT_ACTION_TYPES
            ),
        },
        "operator_approval_schema": {
            "human_operator_approval_required": True,
            "automatic_approval_allowed": False,
            "automatic_rejection_allowed": False,
            "future_manual_application_phase_required": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_freeze_input_shape": True,
            "validate_candidate_config_freeze_shape": True,
            "validate_manual_approval_packet_shape": True,
            "validate_allowed_statuses": True,
            "validate_allowed_blockers": True,
            "validate_allowed_checklist_items": True,
            "validate_allowed_operator_next_action_types": True,
            "validate_not_applied": True,
            "validate_runtime_application_status": True,
            "validate_approval_required": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_errors_only": True,
        },
        "provenance_requirements": {
            "source_decision_packet_path_required": True,
            "source_sandbox_evaluation_report_path_required": True,
            "source_sandbox_regression_verification_path_required": True,
            "model_asset_ref_required": True,
            "model_asset_sha256_when_available": True,
            "source_contract_refs_required": True,
            "source_warnings_preserved": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _selected_candidate_ref(
    *,
    decision_packet: dict[str, Any],
    selected_candidate_packet_ref: str | None,
) -> dict[str, Any]:
    candidates = [_dict(item) for item in _list(decision_packet.get("candidate_packets"))]
    if selected_candidate_packet_ref:
        for candidate in candidates:
            if selected_candidate_packet_ref in {
                str(candidate.get("candidate_packet_id")),
                str(candidate.get("candidate_setting_id")),
                str(candidate.get("source_proposal_item_id")),
            }:
                return _candidate_ref(candidate)
        return {}
    for candidate in candidates:
        if candidate.get("decision_support_status") == "ready_for_human_decision":
            return _candidate_ref(candidate)
    return {}


def _candidate_ref(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_packet_id": candidate.get("candidate_packet_id"),
        "candidate_setting_id": candidate.get("candidate_setting_id"),
        "source_proposal_item_id": candidate.get("source_proposal_item_id"),
        "candidate_type": candidate.get("candidate_type"),
        "candidate_status": candidate.get("candidate_status"),
        "decision_support_status": candidate.get("decision_support_status"),
        "operator_review_status": candidate.get("operator_review_status"),
        "runtime_change_status": candidate.get("runtime_change_status"),
        "not_applied": candidate.get("not_applied") is True,
    }


def _candidate_packet_refs(decision_packet: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            **_candidate_ref(_dict(candidate)),
            "candidate_setting_summary": _dict(
                _dict(candidate).get("candidate_setting_summary")
            ),
            "blockers": _list(_dict(candidate).get("blockers")),
            "risk_flags": _list(_dict(candidate).get("risk_flags")),
            "required_preconditions": _list(
                _dict(candidate).get("required_preconditions")
            ),
            "evidence_refs": _dict(_dict(candidate).get("evidence_refs")),
        }
        for candidate in _list(decision_packet.get("candidate_packets"))
    ]


def _candidate_ref_by_id(
    *,
    freeze_inputs: dict[str, Any],
    candidate_packet_id: Any,
) -> dict[str, Any]:
    if not candidate_packet_id:
        return {}
    for candidate in _list(freeze_inputs.get("candidate_packet_refs")):
        candidate_ref = _dict(candidate)
        if candidate_ref.get("candidate_packet_id") == candidate_packet_id:
            return candidate_ref
    return {}


def _candidate_config_status(candidate: dict[str, Any]) -> str:
    if not candidate:
        return "no_candidate_selected"
    candidate_status = str(candidate.get("candidate_status") or "")
    decision_support_status = str(candidate.get("decision_support_status") or "")
    if candidate_status == "ready_for_operator_review" and (
        decision_support_status == "ready_for_human_decision"
    ):
        return "frozen_for_manual_review"
    if candidate_status in {
        "blocked_missing_review_data",
        "blocked_regression_drift",
        "blocked_insufficient_sample_size",
        "blocked_fixture_only_data",
        "blocked_invalid_candidate",
        "informational_only",
        "not_applicable",
    }:
        return candidate_status
    if candidate_status == "blocked_no_human_review":
        return "blocked_missing_review_data"
    if candidate_status == "no_candidate":
        return "no_candidate_selected"
    return "informational_only"


def _manual_approval_status(
    *,
    candidate_config_status: str,
    selected_candidate: dict[str, Any],
) -> str:
    if not selected_candidate:
        return "not_applicable"
    if candidate_config_status == "frozen_for_manual_review":
        return "operator_review_required"
    if candidate_config_status.startswith("blocked_"):
        return "blocked_from_manual_approval"
    return "not_reviewed_by_operator"


def _candidate_settings(candidate: dict[str, Any]) -> dict[str, Any]:
    summary = _dict(candidate.get("candidate_setting_summary"))
    candidate_type = str(candidate.get("candidate_type") or "not_applicable")
    candidate_value = summary.get("candidate_value")
    candidate_threshold = summary.get("threshold_candidate")
    candidate_smoothing_window = summary.get("smoothing_window_candidate")
    candidate_hysteresis_settings = _dict(summary.get("hysteresis_candidate"))
    if candidate_type == "threshold_candidate" and candidate_threshold is None:
        candidate_threshold = candidate_value
    if candidate_type == "smoothing_window_candidate" and candidate_smoothing_window is None:
        candidate_smoothing_window = candidate_value
    if candidate_type == "hysteresis_candidate" and not candidate_hysteresis_settings:
        candidate_hysteresis_settings = _dict(candidate_value)
    return {
        "candidate_threshold": candidate_threshold,
        "candidate_smoothing_window": candidate_smoothing_window,
        "candidate_hysteresis_settings": candidate_hysteresis_settings,
        "candidate_type": candidate_type,
        "candidate_source": {
            "candidate_packet_id": candidate.get("candidate_packet_id"),
            "candidate_setting_id": candidate.get("candidate_setting_id"),
            "source_proposal_item_id": candidate.get("source_proposal_item_id"),
        },
        "candidate_notes": [
            "candidate_settings_are_frozen_for_manual_review_only",
            "not_applied",
        ],
        "not_applied": True,
        "writes_runtime_configuration": False,
        "affects_regression_baselines": False,
    }


def _approval_blockers(
    *,
    selected_candidate: dict[str, Any],
    freeze_inputs: dict[str, Any],
    candidate_config_status: str,
) -> list[str]:
    if not selected_candidate:
        return ["not_applicable"]
    blockers = {"missing_operator_review"}
    candidate_blockers = {
        str(item)
        for item in _list(selected_candidate.get("blockers"))
        + _list(selected_candidate.get("risk_flags"))
    }
    coverage = _dict(freeze_inputs.get("operator_context")).get("structural_drift_summary")
    if candidate_config_status == "blocked_missing_review_data":
        blockers.add("missing_human_review_data")
    if "insufficient_review_coverage" in candidate_blockers:
        blockers.add("insufficient_review_coverage")
    if "human_review_required" in candidate_blockers:
        blockers.add("missing_human_review_data")
    if "missing_required_review_fields" in candidate_blockers:
        blockers.add("missing_human_review_data")
    if "fixture_only_review_data" in candidate_blockers or (
        candidate_config_status == "blocked_fixture_only_data"
    ):
        blockers.add("fixture_only_evidence")
    if _dict(coverage).get("sandbox_regression_status") == "regression_gate_warning":
        blockers.add("regression_gate_warning")
    if _dict(coverage).get("sandbox_regression_status") == "regression_gate_blocked":
        blockers.add("regression_gate_blocked")
    if candidate_config_status == "blocked_invalid_candidate":
        blockers.add("invalid_candidate_config")
    return sorted(blockers)


def _required_preconditions(
    *,
    selected_candidate: dict[str, Any],
    approval_required: bool,
) -> list[str]:
    preconditions = {
        "reviewed_candidate_packet",
        "reviewed_review_coverage",
        "reviewed_sandbox_evaluation",
        "reviewed_sandbox_regression_gate",
        "reviewed_gameplay_regression_gate",
        "reviewed_non_claims",
        "confirmed_no_runtime_application",
        "confirmed_model_weights_unchanged",
        "confirmed_baselines_unchanged",
        "confirmed_human_approval_required",
    }
    if approval_required:
        preconditions.update(str(item) for item in _list(selected_candidate.get("blockers")))
    return sorted(preconditions)


def _supporting_evidence_refs(
    *,
    freeze_inputs: dict[str, Any],
    selected_candidate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "source_decision_packet_path": freeze_inputs.get("source_decision_packet_path"),
        "source_sandbox_evaluation_report_path": freeze_inputs.get(
            "source_sandbox_evaluation_report_path"
        ),
        "source_sandbox_regression_verification_path": freeze_inputs.get(
            "source_sandbox_regression_verification_path"
        ),
        "source_calibration_proposal_path": freeze_inputs.get(
            "source_calibration_proposal_path"
        ),
        "source_review_metrics_report_path": freeze_inputs.get(
            "source_review_metrics_report_path"
        ),
        "source_review_loop_report_path": freeze_inputs.get(
            "source_review_loop_report_path"
        ),
        "source_corpus_run_path": freeze_inputs.get("source_corpus_run_path"),
        "source_gameplay_gate_regression_baseline_path": freeze_inputs.get(
            "source_gameplay_gate_regression_baseline_path"
        ),
        "source_calibration_sandbox_baseline_path": freeze_inputs.get(
            "source_calibration_sandbox_baseline_path"
        ),
        "candidate_packet_ref": _candidate_ref(selected_candidate)
        if selected_candidate
        else None,
        "candidate_evidence_refs": _dict(selected_candidate.get("evidence_refs")),
    }


def _risk_flags(
    *,
    selected_candidate: dict[str, Any],
    approval_blockers: list[str],
    candidate_config_status: str,
) -> list[str]:
    flags = {
        "not_applied",
        "runtime_application_status_not_applied",
        "human_operator_approval_required",
        candidate_config_status,
        *approval_blockers,
        *[str(item) for item in _list(selected_candidate.get("risk_flags"))],
    }
    return sorted(flag for flag in flags if flag)


def _operator_next_actions(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    action_types = {"do_not_apply_runtime_change"}
    if freeze.get("approval_required") is True:
        action_types.add("review_candidate_config_freeze")
        action_types.add("prepare_future_runtime_change_request")
    blockers = set(_list(freeze.get("approval_blockers")))
    if blockers & {"missing_human_review_data", "insufficient_review_coverage"}:
        action_types.add("collect_more_human_review")
    if "regression_gate_warning" in blockers or "regression_gate_blocked" in blockers:
        action_types.add("inspect_regression_drift")
    if "fixture_only_evidence" in blockers:
        action_types.add("prepare_followup_real_data_review")
    if "missing_human_review_data" in blockers:
        action_types.add("inspect_missing_review_fields")
    if not action_types:
        action_types.add("no_action")
    return [
        {
            "action_type": action_type,
            "operator_review_required": action_type
            not in {"do_not_apply_runtime_change", "no_action", "not_applicable"},
            "runtime_application_status": "not_applied",
        }
        for action_type in sorted(action_types)
    ]


def _operator_checklist(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "checklist_item": item,
            "required": freeze.get("approval_required") is True,
            "operator_review_status": freeze.get("manual_approval_status"),
            "runtime_application_status": "not_applied",
        }
        for item in ALLOWED_OPERATOR_CHECKLIST_ITEMS
    ]


def _candidate_config_summary(freeze: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_config_freeze_id": freeze.get("candidate_config_freeze_id"),
        "candidate_config_status": freeze.get("candidate_config_status"),
        "manual_approval_status": freeze.get("manual_approval_status"),
        "runtime_application_status": "not_applied",
        "approval_required": freeze.get("approval_required") is True,
        "not_applied": freeze.get("not_applied") is True,
        "candidate_type": _dict(freeze.get("candidate_settings")).get("candidate_type"),
        "approval_blocker_count": len(_list(freeze.get("approval_blockers"))),
        "risk_flag_count": len(_list(freeze.get("risk_flags"))),
        "classifier_correctness_not_assessed": True,
    }


def _supporting_evidence_summary(freeze: dict[str, Any]) -> dict[str, Any]:
    refs = _dict(freeze.get("supporting_evidence_refs"))
    return {
        "source_decision_packet_path": refs.get("source_decision_packet_path"),
        "source_sandbox_evaluation_report_path": refs.get(
            "source_sandbox_evaluation_report_path"
        ),
        "source_sandbox_regression_verification_path": refs.get(
            "source_sandbox_regression_verification_path"
        ),
        "model_asset_ref": freeze.get("model_asset_ref"),
        "model_asset_sha256": freeze.get("model_asset_sha256"),
        "baseline_not_replaced": True,
        "model_weights_not_modified": True,
    }


def _current_settings(
    *,
    decision_packet: dict[str, Any],
    sandbox_evaluation_report: dict[str, Any],
    calibration_proposal: dict[str, Any],
) -> dict[str, Any]:
    current = _dict(decision_packet.get("current_settings"))
    evaluation_current = _dict(sandbox_evaluation_report.get("current_settings"))
    return {
        "current_threshold": current.get("current_threshold")
        or evaluation_current.get("current_threshold")
        or calibration_proposal.get("current_threshold"),
        "current_smoothing_window": current.get("current_smoothing_window")
        or evaluation_current.get("current_smoothing_window")
        or calibration_proposal.get("current_smoothing_window"),
        "current_hysteresis_settings": _dict(
            current.get("current_hysteresis_settings")
        )
        or _dict(evaluation_current.get("current_hysteresis_settings"))
        or _dict(calibration_proposal.get("current_hysteresis_settings")),
        "runtime_application_status": "not_applied",
    }


def _regression_gate_summary(decision_packet: dict[str, Any]) -> dict[str, Any]:
    return {
        **_dict(decision_packet.get("regression_gate_summary")),
        "runtime_application_status": "not_applied",
        "baseline_not_replaced": True,
        "classifier_correctness_not_assessed": True,
    }


def _regression_gate_summary_from_inputs(freeze_inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        **_dict(_dict(freeze_inputs.get("operator_context")).get("structural_drift_summary")),
        "runtime_application_status": "not_applied",
        "baseline_not_replaced": True,
        "classifier_correctness_not_assessed": True,
    }


def _review_coverage_summary_from_inputs(freeze_inputs: dict[str, Any]) -> dict[str, Any]:
    candidates = [_dict(item) for item in _list(freeze_inputs.get("candidate_packet_refs"))]
    return {
        "candidate_packet_count": len(candidates),
        "operator_review_required_count": sum(
            1
            for candidate in candidates
            if candidate.get("operator_review_status") == "operator_review_needed"
        ),
        "ready_for_human_decision_count": sum(
            1
            for candidate in candidates
            if candidate.get("decision_support_status") == "ready_for_human_decision"
        ),
        "candidate_status_counts": _count_by_field(candidates, "candidate_status"),
        "decision_support_status_counts": _count_by_field(
            candidates,
            "decision_support_status",
        ),
        "human_operator_approval_required": True,
    }


def _model_asset_identity(
    *,
    source_payloads: dict[str, dict[str, Any]],
    model_asset_path: str | Path,
) -> tuple[str, str | None]:
    for payload in source_payloads.values():
        if not payload:
            continue
        model_ref = payload.get("model_asset_ref")
        model_sha = payload.get("model_asset_sha256")
        if model_ref:
            return str(model_ref), str(model_sha) if model_sha else None
    model_path = Path(model_asset_path)
    if model_path.exists() and model_path.is_file():
        digest = hashlib.sha256(model_path.read_bytes()).hexdigest()
        return str(model_asset_path), digest
    return str(model_asset_path), None


def _merged_warnings(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    warnings = dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS)
    for payload in source_payloads.values():
        warnings.update(_dict(payload.get("warnings")))
    warnings.update(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS)
    return warnings


def _validate_source_artifacts(
    *,
    decision_packet: dict[str, Any],
    sandbox_evaluation_report: dict[str, Any],
    sandbox_regression_verification: dict[str, Any],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not _list(decision_packet.get("candidate_packets")):
        errors.append(_error("missing_candidate_packets", "source_decision_packet", None))
    if "candidate_evaluations" not in sandbox_evaluation_report:
        errors.append(
            _error(
                "missing_candidate_evaluations",
                "source_sandbox_evaluation_report",
                None,
            )
        )
    if sandbox_regression_verification.get("status") is None:
        errors.append(
            _error(
                "missing_sandbox_regression_status",
                "source_sandbox_regression_verification.status",
                None,
            )
        )
    return errors


def _validate_freeze_inputs_shape(freeze_inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(freeze_inputs, "freeze_inputs")
    if freeze_inputs.get("freeze_input_type") != CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_TYPE:
        errors.append(
            _error(
                "invalid_freeze_input_type",
                "freeze_input_type",
                freeze_inputs.get("freeze_input_type"),
            )
        )
    if (
        freeze_inputs.get("freeze_input_version")
        != CALIBRATION_CANDIDATE_CONFIG_FREEZE_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_freeze_input_version",
                "freeze_input_version",
                freeze_inputs.get("freeze_input_version"),
            )
        )
    for field in FREEZE_INPUT_REQUIRED_FIELDS:
        if field not in freeze_inputs:
            errors.append(_error("missing_freeze_input_field", field, None))
    errors.extend(_source_contract_ref_errors(_dict(freeze_inputs.get("source_contract_refs"))))
    errors.extend(_required_flag_errors(_dict(freeze_inputs.get("warnings")), "warnings"))
    errors.extend(_required_flag_errors(_dict(freeze_inputs.get("non_claims")), "non_claims"))
    for candidate in _list(freeze_inputs.get("candidate_packet_refs")):
        candidate_ref = _dict(candidate)
        if candidate_ref.get("runtime_change_status") != "not_applied":
            errors.append(
                _error(
                    "candidate_packet_ref_must_remain_not_applied",
                    "candidate_packet_refs.runtime_change_status",
                    candidate_ref.get("runtime_change_status"),
                )
            )
        if candidate_ref.get("not_applied") is not True:
            errors.append(
                _error(
                    "candidate_packet_ref_must_remain_not_applied",
                    "candidate_packet_refs.not_applied",
                    candidate_ref.get("not_applied"),
                )
            )
    return errors


def _validate_candidate_config_freeze_shape(freeze: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(freeze, "candidate_config_freeze")
    if freeze.get("candidate_config_freeze_type") != CALIBRATION_CANDIDATE_CONFIG_FREEZE_TYPE:
        errors.append(
            _error(
                "invalid_candidate_config_freeze_type",
                "candidate_config_freeze_type",
                freeze.get("candidate_config_freeze_type"),
            )
        )
    if (
        freeze.get("candidate_config_freeze_version")
        != CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION
    ):
        errors.append(
            _error(
                "invalid_candidate_config_freeze_version",
                "candidate_config_freeze_version",
                freeze.get("candidate_config_freeze_version"),
            )
        )
    for field in FREEZE_REQUIRED_FIELDS:
        if field not in freeze:
            errors.append(_error("missing_candidate_config_freeze_field", field, None))
    if freeze.get("candidate_config_status") not in ALLOWED_CANDIDATE_CONFIG_STATUSES:
        errors.append(
            _error(
                "invalid_candidate_config_status",
                "candidate_config_status",
                freeze.get("candidate_config_status"),
            )
        )
    if freeze.get("manual_approval_status") not in ALLOWED_MANUAL_APPROVAL_STATUSES:
        errors.append(
            _error(
                "invalid_manual_approval_status",
                "manual_approval_status",
                freeze.get("manual_approval_status"),
            )
        )
    if freeze.get("runtime_application_status") != "not_applied":
        errors.append(
            _error(
                "runtime_application_status_must_remain_not_applied",
                "runtime_application_status",
                freeze.get("runtime_application_status"),
            )
        )
    if freeze.get("not_applied") is not True:
        errors.append(
            _error("candidate_config_must_remain_not_applied", "not_applied", None)
        )
    if (
        freeze.get("candidate_config_status") != "no_candidate_selected"
        and freeze.get("approval_required") is not True
    ):
        errors.append(
            _error(
                "approval_required_for_selected_candidate",
                "approval_required",
                freeze.get("approval_required"),
            )
        )
    errors.extend(_allowed_list_errors("approval_blockers", freeze, ALLOWED_APPROVAL_BLOCKERS))
    errors.extend(_source_contract_ref_errors(_dict(freeze.get("source_contract_refs"))))
    errors.extend(_required_flag_errors(_dict(freeze.get("warnings")), "warnings"))
    errors.extend(_required_flag_errors(_dict(freeze.get("non_claims")), "non_claims"))
    candidate_settings = _dict(freeze.get("candidate_settings"))
    if candidate_settings.get("candidate_type") not in ALLOWED_CANDIDATE_TYPES:
        errors.append(
            _error(
                "invalid_candidate_type",
                "candidate_settings.candidate_type",
                candidate_settings.get("candidate_type"),
            )
        )
    if candidate_settings.get("not_applied") is not True:
        errors.append(
            _error(
                "candidate_settings_must_remain_not_applied",
                "candidate_settings.not_applied",
                candidate_settings.get("not_applied"),
            )
        )
    return errors


def _validate_manual_approval_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(packet, "manual_approval_packet")
    if (
        packet.get("manual_approval_packet_type")
        != CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_TYPE
    ):
        errors.append(
            _error(
                "invalid_manual_approval_packet_type",
                "manual_approval_packet_type",
                packet.get("manual_approval_packet_type"),
            )
        )
    if (
        packet.get("manual_approval_packet_version")
        != CALIBRATION_CANDIDATE_MANUAL_APPROVAL_PACKET_VERSION
    ):
        errors.append(
            _error(
                "invalid_manual_approval_packet_version",
                "manual_approval_packet_version",
                packet.get("manual_approval_packet_version"),
            )
        )
    for field in MANUAL_APPROVAL_PACKET_REQUIRED_FIELDS:
        if field not in packet:
            errors.append(_error("missing_manual_approval_packet_field", field, None))
    if packet.get("operator_review_status") not in ALLOWED_MANUAL_APPROVAL_STATUSES:
        errors.append(
            _error(
                "invalid_operator_review_status",
                "operator_review_status",
                packet.get("operator_review_status"),
            )
        )
    if packet.get("runtime_application_status") != "not_applied":
        errors.append(
            _error(
                "runtime_application_status_must_remain_not_applied",
                "runtime_application_status",
                packet.get("runtime_application_status"),
            )
        )
    errors.extend(_allowed_list_errors("blockers", packet, ALLOWED_APPROVAL_BLOCKERS))
    for checklist_item in _list(packet.get("operator_checklist")):
        item = _dict(checklist_item).get("checklist_item")
        if item not in ALLOWED_OPERATOR_CHECKLIST_ITEMS:
            errors.append(_error("invalid_operator_checklist_item", "checklist_item", item))
        if _dict(checklist_item).get("runtime_application_status") != "not_applied":
            errors.append(
                _error(
                    "checklist_runtime_status_must_remain_not_applied",
                    "operator_checklist.runtime_application_status",
                    _dict(checklist_item).get("runtime_application_status"),
                )
            )
    for action in _list(packet.get("operator_next_actions")):
        action_type = _dict(action).get("action_type")
        if action_type not in ALLOWED_OPERATOR_NEXT_ACTION_TYPES:
            errors.append(_error("invalid_operator_next_action_type", "action_type", action_type))
        if _dict(action).get("runtime_application_status") != "not_applied":
            errors.append(
                _error(
                    "operator_next_action_status_must_remain_not_applied",
                    "operator_next_actions.runtime_application_status",
                    _dict(action).get("runtime_application_status"),
                )
            )
    errors.extend(_source_contract_ref_errors(_dict(packet.get("source_contract_refs"))))
    errors.extend(_required_flag_errors(_dict(packet.get("warnings")), "warnings"))
    errors.extend(_required_flag_errors(_dict(packet.get("non_claims")), "non_claims"))
    return errors


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    if contract.get("contract_type") != CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != CALIBRATION_CANDIDATE_CONFIG_FREEZE_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    errors.extend(_source_contract_ref_errors(_dict(contract.get("source_contract_refs"))))
    errors.extend(_required_flag_errors(_dict(contract.get("warnings")), "warnings"))
    errors.extend(_required_flag_errors(_dict(contract.get("non_claims")), "non_claims"))
    return errors


def _allowed_list_errors(
    field: str,
    payload: dict[str, Any],
    allowed: list[str],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for value in _list(payload.get(field)):
        if value not in allowed:
            errors.append(_error(f"invalid_{field}_value", field, value))
    return errors


def _source_contract_ref_errors(refs: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(key) != expected:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _required_flag_errors(payload: dict[str, Any], path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key in NON_CLAIMS:
        if payload.get(key) is not True:
            errors.append(_error("missing_required_non_claim", f"{path}.{key}", payload.get(key)))
    return errors


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(contract_path, label="config_freeze_contract")
    if loaded.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", loaded))
        return {}
    contract = _dict(loaded.get("data"))
    errors.extend(_validate_contract_shape(contract))
    return contract


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
) -> dict[str, Any]:
    return {
        "ok": ok,
        "status": "valid" if ok else "invalid",
        "validation_type": validation_type,
        "validation_version": CALIBRATION_CANDIDATE_CONFIG_FREEZE_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _failed_result(
    *,
    status: str,
    errors: list[dict[str, Any]],
    output_path: str | Path | None,
    payload_type: str,
    result_key: str,
) -> dict[str, Any]:
    payload = {
        "ok": False,
        "status": status,
        "payload_type": payload_type,
        "errors": errors,
        "warnings": dict(CALIBRATION_CANDIDATE_CONFIG_FREEZE_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }
    _write_json_if_requested(output_path, payload, payload, result_key)
    return payload


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
    if result:
        result[result_key] = str(path)


def _load_required_json(
    path: str | Path | None,
    label: str,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    if path is None:
        errors.append(_error("missing_required_path", label, None))
        return {}
    result = _load_json(path, label=label)
    if result.get("ok") is False:
        errors.append(_error("json_load_failed", label, result))
        return {}
    return _dict(result.get("data"))


def _load_optional_json(path: str | Path | None) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {}
    result = _load_json(path, label="optional_source")
    if result.get("ok") is False:
        return {}
    return _dict(result.get("data"))


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "status": "missing_file", "label": label, "path": str(path)}
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(path),
            "error": str(exc),
        }
    if not isinstance(data, dict):
        return {"ok": False, "status": "invalid_json_shape", "label": label}
    return {"ok": True, "status": "loaded", "label": label, "data": data}


def _source_scan_payload(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "source_ids": {
            name: {
                "keys": sorted(payload.keys()),
                "warnings": _dict(payload.get("warnings")),
                "non_claims": _dict(payload.get("non_claims")),
            }
            for name, payload in source_payloads.items()
            if payload
        }
    }


def _forbidden_token_errors(value: Any, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}" if path else key_text
            if key_text in FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS:
                errors.append(_error("forbidden_field_or_value", nested_path, key_text))
            errors.extend(_forbidden_token_errors(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif (
        isinstance(value, str)
        and value in FORBIDDEN_CALIBRATION_CANDIDATE_CONFIG_FREEZE_TOKENS
    ):
        errors.append(_error("forbidden_field_or_value", path, value))
    return errors


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        "::".join(str(part) for part in parts).encode("utf-8")
    ).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _count_by_field(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field)) for row in rows).items()))


def _path_string(path: str | Path | Any | None) -> str | None:
    if path is None or not str(path).strip():
        return None
    return str(Path(str(path)))


def _tom_provenance() -> dict[str, Any]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": CALIBRATION_CANDIDATE_CONFIG_FREEZE_BLUEPRINT,
        "blueprint_name": CALIBRATION_CANDIDATE_CONFIG_FREEZE_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "path": path,
        "value": value,
    }
