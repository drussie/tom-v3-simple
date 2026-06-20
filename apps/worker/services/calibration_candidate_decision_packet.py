from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION,
)
from apps.worker.services.review_guided_gameplay_calibration_sandbox_regression import (
    SOURCE_CONTRACT_REFS as CALIBRATION_SANDBOX_REGRESSION_SOURCE_CONTRACT_REFS,
)
from apps.worker.services.review_guided_gameplay_gate_calibration_proposal import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT,
)

CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_TYPE = (
    "calibration_candidate_decision_packet_contract"
)
CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION = "v1"
CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE = (
    "calibration_candidate_decision_packet_inputs"
)
CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_VERSION = "v1"
CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE = "calibration_candidate_decision_packet"
CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION = "v1"
CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_TYPE = (
    "calibration_candidate_decision_packet_report"
)
CALIBRATION_CANDIDATE_DECISION_PACKET_BLUEPRINT = "blueprint_52"
CALIBRATION_CANDIDATE_DECISION_PACKET_BLUEPRINT_NAME = (
    "calibration_candidate_decision_packet_v1"
)

DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT = (
    ".data/contracts/calibration_candidate_decision_packet_contract_v1.json"
)
DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_OUTPUT = (
    ".data/exports/calibration_candidate_decision_packet_inputs.current.json"
)
DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/calibration_candidate_decision_packet_inputs.validation.json"
)
DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT = (
    ".data/exports/calibration_candidate_decision_packet.current.json"
)
DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_VALIDATION_OUTPUT = (
    ".data/exports/calibration_candidate_decision_packet.validation.json"
)
DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_OUTPUT = (
    ".data/exports/calibration_candidate_decision_packet.report.json"
)

CALIBRATION_CANDIDATE_DECISION_PACKET_EXPORTED_AT = datetime(
    2026,
    6,
    20,
    0,
    0,
    tzinfo=UTC,
)

SOURCE_CONTRACT_REFS = {
    "review_guided_gameplay_calibration_sandbox_regression_contract_version": (
        REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
    ),
    **dict(CALIBRATION_SANDBOX_REGRESSION_SOURCE_CONTRACT_REFS),
}

ALLOWED_CANDIDATE_TYPES = [
    "threshold_candidate",
    "smoothing_window_candidate",
    "hysteresis_candidate",
    "combined_candidate",
    "no_candidate",
    "not_applicable",
]
ALLOWED_CANDIDATE_STATUSES = [
    "ready_for_operator_review",
    "blocked_missing_review_data",
    "blocked_insufficient_sample_size",
    "blocked_fixture_only_data",
    "blocked_no_human_review",
    "blocked_regression_drift",
    "blocked_invalid_candidate",
    "informational_only",
    "no_candidate",
    "not_applicable",
]
ALLOWED_SANDBOX_EVALUATION_STATUSES = [
    "evaluated_offline",
    "blocked_missing_review_data",
    "blocked_insufficient_sample_size",
    "blocked_fixture_only_data",
    "blocked_no_human_review",
    "blocked_invalid_candidate",
    "completed_with_warnings",
    "not_applicable",
]
ALLOWED_SANDBOX_REGRESSION_STATUSES = [
    "regression_gate_passed",
    "regression_gate_warning",
    "regression_gate_blocked",
    "regression_gate_missing",
    "not_applicable",
]
ALLOWED_BASELINE_COMPARISON_STATUSES = [
    "no_structural_drift",
    "structural_drift_warning",
    "breaking_structural_drift",
    "baseline_missing",
    "not_applicable",
]
ALLOWED_REVIEW_COVERAGE_STATUSES = [
    "sufficient_for_operator_review",
    "insufficient_review_data",
    "missing_required_review_fields",
    "fixture_only_review_data",
    "human_review_required",
    "not_applicable",
]
ALLOWED_DECISION_SUPPORT_STATUSES = [
    "ready_for_human_decision",
    "needs_more_human_review",
    "blocked_from_runtime_consideration",
    "safe_for_future_manual_review",
    "informational_only",
    "not_applicable",
]
ALLOWED_OPERATOR_REVIEW_STATUSES = [
    "not_reviewed_by_operator",
    "operator_review_needed",
    "operator_review_in_progress",
    "operator_review_completed_no_runtime_action",
    "not_applicable",
]
ALLOWED_RUNTIME_CHANGE_STATUSES = [
    "not_applied",
    "runtime_application_not_supported",
    "future_manual_change_required",
    "not_applicable",
]
ALLOWED_OPERATOR_NEXT_ACTION_TYPES = [
    "review_candidate_packet",
    "collect_more_human_review",
    "inspect_boundary_segments",
    "inspect_ambiguity_cluster",
    "inspect_regression_drift",
    "inspect_missing_review_fields",
    "prepare_offline_followup_experiment",
    "do_not_apply_runtime_change",
    "no_action",
    "not_applicable",
]

CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS = {
    "decision_packet_is_not_truth": True,
    "decision_packet_is_not_accuracy_scoring": True,
    "decision_packet_is_not_runtime_calibration": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "runtime_config_not_updated": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_operator_decision_required": True,
    "classifier_correctness_not_assessed": True,
    "structural_decision_support_only": True,
}

NON_CLAIMS = {
    "decision_packet_is_not_truth": True,
    "decision_packet_is_not_accuracy_scoring": True,
    "decision_packet_is_not_runtime_calibration": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "runtime_config_not_updated": True,
    "baseline_not_replaced": True,
    "automatic_relabeling_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_operator_decision_required": True,
}

FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS = {
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
}

PACKET_INPUT_REQUIRED_FIELDS = [
    "packet_input_id",
    "packet_input_type",
    "packet_input_version",
    "generated_at",
    "source_calibration_proposal_path",
    "source_sandbox_evaluation_report_path",
    "source_sandbox_regression_verification_path",
    "source_review_metrics_report_path",
    "source_review_loop_report_path",
    "source_corpus_run_path",
    "source_gameplay_gate_regression_baseline_path",
    "source_calibration_sandbox_baseline_path",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "proposal_summary",
    "sandbox_evaluation_summary",
    "sandbox_regression_summary",
    "review_metrics_summary",
    "blocked_candidate_summary",
    "candidate_inputs",
    "warnings",
    "non_claims",
]

DECISION_PACKET_REQUIRED_FIELDS = [
    "decision_packet_id",
    "decision_packet_type",
    "decision_packet_version",
    "generated_at",
    "source_packet_input_path",
    "model_asset_ref",
    "model_asset_sha256",
    "current_settings",
    "candidate_packets",
    "blocked_candidates",
    "required_human_review",
    "regression_gate_summary",
    "review_coverage_summary",
    "operator_next_actions",
    "summary",
    "warnings",
    "non_claims",
]

CANDIDATE_PACKET_REQUIRED_FIELDS = [
    "candidate_packet_id",
    "candidate_setting_id",
    "source_proposal_item_id",
    "candidate_type",
    "candidate_setting_summary",
    "candidate_status",
    "sandbox_evaluation_status",
    "sandbox_regression_status",
    "baseline_comparison_status",
    "review_coverage_status",
    "decision_support_status",
    "operator_review_status",
    "not_applied",
    "runtime_change_status",
    "required_preconditions",
    "blockers",
    "risk_flags",
    "evidence_refs",
    "provenance_status",
    "warnings",
]


def export_calibration_candidate_decision_packet_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or CALIBRATION_CANDIDATE_DECISION_PACKET_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_TYPE,
        "contract_version": CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION,
        "contract": contract,
        "warnings": dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_calibration_candidate_decision_packet_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT
    ),
    source_calibration_proposal_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT
    ),
    source_sandbox_evaluation_report_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    source_sandbox_regression_verification_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT
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
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    proposal = _load_required_json(
        source_calibration_proposal_path,
        "source_calibration_proposal",
        errors,
    )
    evaluation_report = _load_required_json(
        source_sandbox_evaluation_report_path,
        "source_sandbox_evaluation_report",
        errors,
    )
    regression_verification = _load_required_json(
        source_sandbox_regression_verification_path,
        "source_sandbox_regression_verification",
        errors,
    )
    metrics_report = _load_optional_json(source_review_metrics_report_path)
    review_loop_report = _load_optional_json(source_review_loop_report_path)
    corpus_run = _load_optional_json(source_corpus_run_path)
    regression_baseline = _load_optional_json(source_gameplay_gate_regression_baseline_path)
    calibration_sandbox_baseline = _load_optional_json(
        source_calibration_sandbox_baseline_path
    )
    evaluation_inputs = _load_optional_json(evaluation_report.get("source_evaluation_input_path"))

    errors.extend(_validate_source_artifacts(proposal, evaluation_report, regression_verification))
    source_payloads = {
        "proposal": proposal,
        "evaluation_report": evaluation_report,
        "regression_verification": regression_verification,
        "metrics_report": metrics_report,
        "review_loop_report": review_loop_report,
        "corpus_run": corpus_run,
        "regression_baseline": regression_baseline,
        "calibration_sandbox_baseline": calibration_sandbox_baseline,
        "evaluation_inputs": evaluation_inputs,
    }
    errors.extend(_forbidden_token_errors(_source_summary_scan_payload(source_payloads), "sources"))
    if errors:
        return _failed_result(
            status="invalid_packet_inputs",
            errors=errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE,
            result_key="packet_inputs_output",
        )

    current_settings = _current_settings(
        proposal=proposal,
        evaluation_report=evaluation_report,
        evaluation_inputs=evaluation_inputs,
    )
    model_asset_ref, model_asset_sha256 = _model_asset_identity(
        source_payloads=source_payloads,
        model_asset_path=model_asset_path,
    )
    candidate_inputs = _candidate_inputs(
        proposal=proposal,
        evaluation_report=evaluation_report,
        evaluation_inputs=evaluation_inputs,
    )
    packet_inputs = {
        "packet_input_id": _stable_id(
            "calibration_candidate_decision_packet_inputs_v1",
            source_calibration_proposal_path,
            source_sandbox_evaluation_report_path,
            source_sandbox_regression_verification_path,
            model_asset_sha256,
        ),
        "packet_input_type": CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE,
        "packet_input_version": CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_calibration_proposal_path": str(Path(source_calibration_proposal_path)),
        "source_sandbox_evaluation_report_path": str(
            Path(source_sandbox_evaluation_report_path)
        ),
        "source_sandbox_regression_verification_path": str(
            Path(source_sandbox_regression_verification_path)
        ),
        "source_review_metrics_report_path": _path_string(source_review_metrics_report_path),
        "source_review_loop_report_path": _path_string(source_review_loop_report_path),
        "source_corpus_run_path": _path_string(source_corpus_run_path),
        "source_gameplay_gate_regression_baseline_path": _path_string(
            source_gameplay_gate_regression_baseline_path
        ),
        "source_calibration_sandbox_baseline_path": _path_string(
            source_calibration_sandbox_baseline_path
        ),
        "source_evaluation_input_path": _path_string(
            evaluation_report.get("source_evaluation_input_path")
        ),
        "model_asset_ref": model_asset_ref,
        "model_asset_sha256": model_asset_sha256,
        "current_settings": current_settings,
        "proposal_summary": _proposal_summary(proposal),
        "sandbox_evaluation_summary": _sandbox_evaluation_summary(evaluation_report),
        "sandbox_regression_summary": _sandbox_regression_summary(regression_verification),
        "review_metrics_summary": _review_metrics_summary(metrics_report),
        "blocked_candidate_summary": _blocked_candidate_summary(
            proposal=proposal,
            evaluation_report=evaluation_report,
        ),
        "candidate_inputs": candidate_inputs,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _merged_warnings(source_payloads),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_packet_input_shape(packet_inputs)
    if validation_errors:
        return _failed_result(
            status="invalid_packet_inputs",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE,
            result_key="packet_inputs_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "packet_input_type": CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE,
        "packet_input_version": CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_VERSION,
        "packet_input_id": packet_inputs["packet_input_id"],
        "packet_inputs": packet_inputs,
        "warnings": packet_inputs["warnings"],
    }
    _write_json_if_requested(output_path, packet_inputs, result, "packet_inputs_output")
    return result


def validate_calibration_candidate_decision_packet_inputs(
    *,
    packet_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    packet_inputs = _load_required_json(packet_inputs_path, "packet_inputs", errors)
    if packet_inputs:
        errors.extend(_validate_packet_input_shape(packet_inputs))
    result = _validation_result(
        ok=not errors,
        validation_type="calibration_candidate_decision_packet_inputs_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=packet_inputs_path,
        payload_type=packet_inputs.get("packet_input_type") if packet_inputs else None,
        payload_version=packet_inputs.get("packet_input_version") if packet_inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_calibration_candidate_decision_packet(
    *,
    packet_inputs_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_calibration_candidate_decision_packet_inputs(
        packet_inputs_path=packet_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_packet_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE,
            result_key="decision_packet_output",
        )
    packet_inputs = _dict(_load_json(packet_inputs_path, label="packet_inputs").get("data"))
    candidate_packets = [
        _candidate_packet(
            candidate_input=_dict(candidate_input),
            packet_inputs=packet_inputs,
            generated_at=generated_at,
        )
        for candidate_input in _list(packet_inputs.get("candidate_inputs"))
    ]
    blocked_candidates = [
        candidate
        for candidate in candidate_packets
        if str(candidate.get("candidate_status")).startswith("blocked_")
    ]
    operator_next_actions = _operator_next_actions(candidate_packets)
    packet = {
        "decision_packet_id": _stable_id(
            "calibration_candidate_decision_packet_v1",
            packet_inputs.get("packet_input_id"),
            len(candidate_packets),
            packet_inputs.get("model_asset_sha256"),
        ),
        "decision_packet_type": CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE,
        "decision_packet_version": CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_packet_input_path": str(Path(packet_inputs_path)),
        "packet_input_id": packet_inputs.get("packet_input_id"),
        "model_asset_ref": packet_inputs.get("model_asset_ref"),
        "model_asset_sha256": packet_inputs.get("model_asset_sha256"),
        "current_settings": _dict(packet_inputs.get("current_settings")),
        "candidate_packets": candidate_packets,
        "blocked_candidates": blocked_candidates,
        "required_human_review": _required_human_review(candidate_packets),
        "regression_gate_summary": _regression_gate_summary(packet_inputs),
        "review_coverage_summary": _review_coverage_summary(packet_inputs),
        "operator_next_actions": operator_next_actions,
        "summary": _decision_packet_summary(
            candidate_packets=candidate_packets,
            packet_inputs=packet_inputs,
            operator_next_actions=operator_next_actions,
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": {
            **_dict(packet_inputs.get("warnings")),
            **dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    validation_errors = _validate_decision_packet_shape(packet)
    if validation_errors:
        return _failed_result(
            status="invalid_decision_packet",
            errors=validation_errors,
            output_path=output_path,
            payload_type=CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE,
            result_key="decision_packet_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "decision_packet_type": CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE,
        "decision_packet_version": CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION,
        "decision_packet_id": packet["decision_packet_id"],
        "decision_packet": packet,
        "warnings": packet["warnings"],
    }
    _write_json_if_requested(output_path, packet, result, "decision_packet_output")
    return result


def validate_calibration_candidate_decision_packet(
    *,
    decision_packet_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    decision_packet = _load_required_json(decision_packet_path, "decision_packet", errors)
    if decision_packet:
        errors.extend(_validate_decision_packet_shape(decision_packet))
    result = _validation_result(
        ok=not errors,
        validation_type="calibration_candidate_decision_packet_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=decision_packet_path,
        payload_type=(
            decision_packet.get("decision_packet_type") if decision_packet else None
        ),
        payload_version=(
            decision_packet.get("decision_packet_version") if decision_packet else None
        ),
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_calibration_candidate_decision_packet_report(
    *,
    decision_packet_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_calibration_candidate_decision_packet(
        decision_packet_path=decision_packet_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    decision_packet = _dict(
        _load_json(decision_packet_path, label="decision_packet").get("data")
    )
    report = {
        "report_type": CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_TYPE,
        "report_version": CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_decision_packet_path": str(Path(decision_packet_path)),
        "decision_packet_id": decision_packet.get("decision_packet_id"),
        "decision_packet_summary": _dict(decision_packet.get("summary")),
        "structural_drift_summary": _dict(
            decision_packet.get("regression_gate_summary")
        ),
        "operator_review_needed": decision_packet.get("required_human_review") is True,
        "candidate_packet_summaries": [
            _candidate_report_summary(_dict(candidate))
            for candidate in _list(decision_packet.get("candidate_packets"))
        ],
        "operator_next_actions": _list(decision_packet.get("operator_next_actions")),
        "validation_snapshot": validation,
        "warnings": {
            **_dict(decision_packet.get("warnings")),
            **dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
        },
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _forbidden_token_errors(report, "report")
    result_errors = _list(validation.get("errors")) + errors
    result = {
        "ok": not result_errors,
        "status": "completed" if not result_errors else "invalid_decision_packet_report",
        "report_type": CALIBRATION_CANDIDATE_DECISION_PACKET_REPORT_TYPE,
        "report_version": CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION,
        "decision_packet_id": decision_packet.get("decision_packet_id"),
        "report": report,
        "errors": result_errors,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_TYPE,
        "contract_version": CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "packet_scope": {
            "purpose": "operator_facing_calibration_candidate_decision_packet",
            "packages_prior_calibration_evidence": True,
            "supports_human_operator_review": True,
            "updates_runtime_config": False,
            "updates_model_weights": False,
            "mutates_regression_baselines": False,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "auto_selects_candidates": False,
            "creates_review_labels": False,
            "calculates_classifier_correctness": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "packet_input_schema": {
            "packet_input_type": CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE,
            "packet_input_version": CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_VERSION,
            "required_fields": list(PACKET_INPUT_REQUIRED_FIELDS),
        },
        "decision_packet_schema": {
            "decision_packet_type": CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE,
            "decision_packet_version": CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION,
            "required_fields": list(DECISION_PACKET_REQUIRED_FIELDS),
        },
        "candidate_packet_schema": {
            "required_fields": list(CANDIDATE_PACKET_REQUIRED_FIELDS),
            "allowed_candidate_types": list(ALLOWED_CANDIDATE_TYPES),
            "allowed_candidate_statuses": list(ALLOWED_CANDIDATE_STATUSES),
            "allowed_sandbox_evaluation_statuses": list(
                ALLOWED_SANDBOX_EVALUATION_STATUSES
            ),
            "allowed_sandbox_regression_statuses": list(
                ALLOWED_SANDBOX_REGRESSION_STATUSES
            ),
            "allowed_baseline_comparison_statuses": list(
                ALLOWED_BASELINE_COMPARISON_STATUSES
            ),
            "allowed_review_coverage_statuses": list(ALLOWED_REVIEW_COVERAGE_STATUSES),
            "allowed_decision_support_statuses": list(ALLOWED_DECISION_SUPPORT_STATUSES),
            "allowed_operator_review_statuses": list(ALLOWED_OPERATOR_REVIEW_STATUSES),
            "allowed_runtime_change_statuses": list(ALLOWED_RUNTIME_CHANGE_STATUSES),
            "requires_not_applied": True,
        },
        "operator_action_schema": {
            "allowed_operator_next_action_types": list(ALLOWED_OPERATOR_NEXT_ACTION_TYPES),
            "requires_human_operator_decision": True,
        },
        "validation_rules": {
            "validate_source_contract_refs": True,
            "validate_allowed_statuses": True,
            "validate_candidate_not_applied": True,
            "validate_runtime_change_status": True,
            "reject_forbidden_exact_tokens": True,
            "structural_validation_only": True,
        },
        "provenance_requirements": {
            "source_artifact_paths_required": True,
            "model_asset_ref_required": True,
            "model_asset_sha256_when_available": True,
            "source_contract_refs_required": True,
            "tom_provenance_required": True,
        },
        "warnings": dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_inputs(
    *,
    proposal: dict[str, Any],
    evaluation_report: dict[str, Any],
    evaluation_inputs: dict[str, Any],
) -> list[dict[str, Any]]:
    proposal_items = [_dict(item) for item in _list(proposal.get("proposal_items"))]
    proposal_by_id = {
        str(item.get("proposal_item_id")): item
        for item in proposal_items
        if item.get("proposal_item_id")
    }
    candidate_settings = [
        _dict(item) for item in _list(evaluation_inputs.get("candidate_settings"))
    ]
    settings_by_id = {
        str(item.get("candidate_setting_id")): item
        for item in candidate_settings
        if item.get("candidate_setting_id")
    }
    evaluations = [
        _dict(item) for item in _list(evaluation_report.get("candidate_evaluations"))
    ]
    if not evaluations:
        evaluations = [_fallback_evaluation_for_proposal_item(item) for item in proposal_items]
    candidate_inputs: list[dict[str, Any]] = []
    for index, evaluation in enumerate(evaluations):
        setting = settings_by_id.get(str(evaluation.get("candidate_setting_id")), {})
        proposal_item = proposal_by_id.get(str(setting.get("source_proposal_item_id")), {})
        if not proposal_item and index < len(proposal_items):
            proposal_item = proposal_items[index]
        candidate_setting = _dict(proposal_item.get("proposed_candidate_setting"))
        candidate_inputs.append(
            {
                "candidate_input_id": _stable_id(
                    "calibration_candidate_decision_packet_candidate_input_v1",
                    evaluation.get("candidate_evaluation_id"),
                    evaluation.get("candidate_setting_id"),
                    proposal_item.get("proposal_item_id"),
                ),
                "candidate_evaluation": evaluation,
                "candidate_setting": setting,
                "proposal_item": proposal_item,
                "candidate_setting_summary": {
                    "setting_type": _candidate_type(
                        evaluation=evaluation,
                        candidate_setting=setting,
                        proposal_item=proposal_item,
                    ),
                    "candidate_value": candidate_setting.get("candidate_value"),
                    "threshold_candidate": setting.get("threshold_candidate"),
                    "smoothing_window_candidate": setting.get("smoothing_window_candidate"),
                    "hysteresis_candidate": setting.get("hysteresis_candidate"),
                    "future_manual_review_candidate": True,
                    "not_applied": True,
                    "writes_runtime_config": False,
                    "affects_regression_baselines": False,
                },
                "warnings": _candidate_warnings(
                    proposal_item=proposal_item,
                    setting=setting,
                    evaluation=evaluation,
                ),
            }
        )
    return candidate_inputs


def _candidate_packet(
    *,
    candidate_input: dict[str, Any],
    packet_inputs: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    evaluation = _dict(candidate_input.get("candidate_evaluation"))
    setting = _dict(candidate_input.get("candidate_setting"))
    proposal_item = _dict(candidate_input.get("proposal_item"))
    candidate_type = _candidate_type(
        evaluation=evaluation,
        candidate_setting=setting,
        proposal_item=proposal_item,
    )
    candidate_status = _candidate_status(
        evaluation=evaluation,
        setting=setting,
        proposal_item=proposal_item,
        packet_inputs=packet_inputs,
        candidate_type=candidate_type,
    )
    sandbox_regression_status = _sandbox_regression_status(packet_inputs)
    baseline_comparison_status = _baseline_comparison_status(packet_inputs)
    review_coverage_status = _review_coverage_status(
        evaluation=evaluation,
        setting=setting,
        proposal_item=proposal_item,
        packet_inputs=packet_inputs,
    )
    decision_support_status = _decision_support_status(
        candidate_status=candidate_status,
        sandbox_regression_status=sandbox_regression_status,
        review_coverage_status=review_coverage_status,
    )
    operator_review_status = _operator_review_status(
        candidate_status=candidate_status,
        decision_support_status=decision_support_status,
    )
    blockers = _candidate_blockers(
        candidate_status=candidate_status,
        review_coverage_status=review_coverage_status,
        sandbox_regression_status=sandbox_regression_status,
        proposal_item=proposal_item,
        setting=setting,
    )
    warnings = {
        **_dict(candidate_input.get("warnings")),
        **dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
    }
    return {
        "candidate_packet_id": _stable_id(
            "calibration_candidate_decision_packet_candidate_v1",
            candidate_input.get("candidate_input_id"),
            generated_at.isoformat(),
        ),
        "candidate_setting_id": _candidate_setting_id(
            evaluation=evaluation,
            setting=setting,
            proposal_item=proposal_item,
        ),
        "source_proposal_item_id": proposal_item.get("proposal_item_id"),
        "candidate_type": candidate_type,
        "candidate_setting_summary": _dict(
            candidate_input.get("candidate_setting_summary")
        ),
        "candidate_status": candidate_status,
        "sandbox_evaluation_status": _sandbox_evaluation_status(evaluation=evaluation),
        "sandbox_regression_status": sandbox_regression_status,
        "baseline_comparison_status": baseline_comparison_status,
        "review_coverage_status": review_coverage_status,
        "decision_support_status": decision_support_status,
        "operator_review_status": operator_review_status,
        "not_applied": True,
        "runtime_change_status": "not_applied",
        "required_preconditions": sorted(
            {
                *[str(item) for item in _list(setting.get("required_preconditions"))],
                *[
                    str(item)
                    for item in _list(proposal_item.get("required_preconditions"))
                ],
            }
        ),
        "blockers": blockers,
        "risk_flags": _risk_flags(
            candidate_status=candidate_status,
            review_coverage_status=review_coverage_status,
            proposal_item=proposal_item,
            setting=setting,
        ),
        "evidence_refs": {
            "candidate_evaluation_id": evaluation.get("candidate_evaluation_id"),
            "source_metric_group": (
                setting.get("source_metric_group")
                or proposal_item.get("source_metric_group")
            ),
            "source_review_entry_refs": _list(setting.get("source_review_entry_refs"))
            or _list(proposal_item.get("source_review_entry_refs")),
            "source_segment_refs": _list(setting.get("source_segment_refs"))
            or _list(proposal_item.get("source_segment_refs")),
            "source_paths": {
                "packet_inputs": packet_inputs.get("packet_input_id"),
                "calibration_proposal": packet_inputs.get(
                    "source_calibration_proposal_path"
                ),
                "sandbox_evaluation_report": packet_inputs.get(
                    "source_sandbox_evaluation_report_path"
                ),
                "sandbox_regression_verification": packet_inputs.get(
                    "source_sandbox_regression_verification_path"
                ),
            },
        },
        "provenance_status": _provenance_status(
            proposal_item=proposal_item,
            setting=setting,
            evaluation=evaluation,
        ),
        "warnings": warnings,
    }


def _candidate_status(
    *,
    evaluation: dict[str, Any],
    setting: dict[str, Any],
    proposal_item: dict[str, Any],
    packet_inputs: dict[str, Any],
    candidate_type: str,
) -> str:
    regression_status = _sandbox_regression_status(packet_inputs)
    if regression_status == "regression_gate_blocked":
        return "blocked_regression_drift"
    if candidate_type in {"no_candidate", "not_applicable"}:
        source_status = (
            evaluation.get("evaluation_status")
            or setting.get("candidate_status")
            or proposal_item.get("proposal_status")
        )
        return _mapped_blocked_status(source_status) or "no_candidate"
    source_status = (
        evaluation.get("evaluation_status")
        or setting.get("candidate_status")
        or proposal_item.get("proposal_status")
    )
    mapped = _mapped_blocked_status(source_status)
    if mapped:
        return mapped
    decision_status = str(evaluation.get("decision_support_status") or "")
    if decision_status == "informational_only":
        return "informational_only"
    if decision_status == "needs_more_human_review":
        return "blocked_no_human_review"
    if source_status in {"evaluated_offline", "completed_with_warnings"}:
        return "ready_for_operator_review"
    if source_status in {"needs_additional_review", "proposed_for_future_evaluation"}:
        return "ready_for_operator_review"
    return "informational_only"


def _mapped_blocked_status(value: Any) -> str | None:
    text = str(value or "")
    if text in {
        "blocked_missing_review_data",
        "blocked_insufficient_sample_size",
        "blocked_fixture_only_data",
        "blocked_no_human_review",
        "blocked_invalid_candidate",
    }:
        return text
    if text in {"invalid_candidate", "invalid"}:
        return "blocked_invalid_candidate"
    if text in {"fixture_only", "insufficient_data"}:
        return "blocked_fixture_only_data"
    return None


def _candidate_type(
    *,
    evaluation: dict[str, Any],
    candidate_setting: dict[str, Any],
    proposal_item: dict[str, Any],
) -> str:
    for value in (
        evaluation.get("candidate_type"),
        candidate_setting.get("candidate_type"),
        _dict(proposal_item.get("proposed_candidate_setting")).get("setting_type"),
    ):
        text = str(value or "")
        if text in ALLOWED_CANDIDATE_TYPES:
            return text
    return "not_applicable"


def _sandbox_evaluation_status(*, evaluation: dict[str, Any]) -> str:
    status = str(evaluation.get("evaluation_status") or "")
    if status in ALLOWED_SANDBOX_EVALUATION_STATUSES:
        return status
    if status in {"needs_additional_review", "proposed_for_future_evaluation"}:
        return "completed_with_warnings"
    if not status:
        return "not_applicable"
    return "blocked_invalid_candidate"


def _sandbox_regression_status(packet_inputs: dict[str, Any]) -> str:
    summary = _dict(packet_inputs.get("sandbox_regression_summary"))
    status = str(summary.get("status") or "")
    if not status or status in {"baseline_missing", "baseline_invalid"}:
        return "regression_gate_missing"
    if status == "completed" and summary.get("drift_detected") is not True:
        return "regression_gate_passed"
    if status == "drift_detected" and summary.get("breaking_drift_detected") is not True:
        return "regression_gate_warning"
    return "regression_gate_blocked"


def _baseline_comparison_status(packet_inputs: dict[str, Any]) -> str:
    summary = _dict(packet_inputs.get("sandbox_regression_summary"))
    status = str(summary.get("status") or "")
    if not status or status in {"baseline_missing", "baseline_invalid"}:
        return "baseline_missing"
    if summary.get("breaking_drift_detected") is True:
        return "breaking_structural_drift"
    if summary.get("drift_detected") is True:
        return "structural_drift_warning"
    return "no_structural_drift"


def _review_coverage_status(
    *,
    evaluation: dict[str, Any],
    setting: dict[str, Any],
    proposal_item: dict[str, Any],
    packet_inputs: dict[str, Any],
) -> str:
    values = {
        str(evaluation.get("evaluation_status") or ""),
        str(setting.get("candidate_status") or ""),
        str(proposal_item.get("proposal_status") or ""),
    }
    if "blocked_missing_review_data" in values:
        return "missing_required_review_fields"
    if "blocked_fixture_only_data" in values:
        return "fixture_only_review_data"
    if "blocked_insufficient_sample_size" in values:
        return "insufficient_review_data"
    if "blocked_no_human_review" in values:
        return "human_review_required"
    metrics_summary = _dict(packet_inputs.get("review_metrics_summary"))
    if metrics_summary.get("fixture_mode_used") is True:
        return "fixture_only_review_data"
    if _int(metrics_summary.get("reviewed_entry_count")) <= 0:
        return "human_review_required"
    return "sufficient_for_operator_review"


def _decision_support_status(
    *,
    candidate_status: str,
    sandbox_regression_status: str,
    review_coverage_status: str,
) -> str:
    if sandbox_regression_status == "regression_gate_blocked":
        return "blocked_from_runtime_consideration"
    if candidate_status in {"no_candidate", "not_applicable"}:
        return "not_applicable"
    if candidate_status.startswith("blocked_"):
        if candidate_status in {
            "blocked_missing_review_data",
            "blocked_no_human_review",
            "blocked_insufficient_sample_size",
        }:
            return "needs_more_human_review"
        return "blocked_from_runtime_consideration"
    if review_coverage_status in {
        "missing_required_review_fields",
        "human_review_required",
        "insufficient_review_data",
    }:
        return "needs_more_human_review"
    if candidate_status == "informational_only":
        return "informational_only"
    return "ready_for_human_decision"


def _operator_review_status(*, candidate_status: str, decision_support_status: str) -> str:
    if candidate_status in {"no_candidate", "not_applicable"}:
        return "not_applicable"
    if decision_support_status in {
        "ready_for_human_decision",
        "needs_more_human_review",
        "safe_for_future_manual_review",
    }:
        return "operator_review_needed"
    return "not_reviewed_by_operator"


def _candidate_blockers(
    *,
    candidate_status: str,
    review_coverage_status: str,
    sandbox_regression_status: str,
    proposal_item: dict[str, Any],
    setting: dict[str, Any],
) -> list[str]:
    blockers = {
        str(item)
        for item in [
            candidate_status if candidate_status.startswith("blocked_") else "",
            review_coverage_status
            if review_coverage_status != "sufficient_for_operator_review"
            else "",
            sandbox_regression_status
            if sandbox_regression_status == "regression_gate_blocked"
            else "",
        ]
        if item
    }
    blockers.update(str(item) for item in _list(proposal_item.get("risk_flags")))
    blockers.update(str(item) for item in _list(setting.get("risk_flags")))
    return sorted(blockers)


def _risk_flags(
    *,
    candidate_status: str,
    review_coverage_status: str,
    proposal_item: dict[str, Any],
    setting: dict[str, Any],
) -> list[str]:
    flags = {
        "not_applied",
        "runtime_change_status_not_applied",
        *[str(item) for item in _list(proposal_item.get("risk_flags"))],
        *[str(item) for item in _list(setting.get("risk_flags"))],
    }
    if candidate_status.startswith("blocked_"):
        flags.add(candidate_status)
    if review_coverage_status != "sufficient_for_operator_review":
        flags.add(review_coverage_status)
    return sorted(flags)


def _operator_next_actions(candidate_packets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    action_types: set[str] = {"do_not_apply_runtime_change"}
    for candidate in candidate_packets:
        status = str(candidate.get("candidate_status") or "")
        coverage = str(candidate.get("review_coverage_status") or "")
        if candidate.get("decision_support_status") == "ready_for_human_decision":
            action_types.add("review_candidate_packet")
        if status in {"blocked_no_human_review", "blocked_insufficient_sample_size"}:
            action_types.add("collect_more_human_review")
        if coverage == "missing_required_review_fields":
            action_types.add("inspect_missing_review_fields")
        if coverage == "fixture_only_review_data":
            action_types.add("prepare_offline_followup_experiment")
        if candidate.get("sandbox_regression_status") == "regression_gate_blocked":
            action_types.add("inspect_regression_drift")
    if not candidate_packets:
        action_types.add("no_action")
    return [
        {
            "action_type": action_type,
            "operator_review_needed": action_type
            not in {"do_not_apply_runtime_change", "no_action", "not_applicable"},
            "runtime_change_status": "not_applied",
        }
        for action_type in sorted(action_types)
    ]


def _required_human_review(candidate_packets: list[dict[str, Any]]) -> bool:
    return any(
        candidate.get("operator_review_status") == "operator_review_needed"
        or candidate.get("decision_support_status") in {
            "ready_for_human_decision",
            "needs_more_human_review",
        }
        for candidate in candidate_packets
    )


def _decision_packet_summary(
    *,
    candidate_packets: list[dict[str, Any]],
    packet_inputs: dict[str, Any],
    operator_next_actions: list[dict[str, Any]],
) -> dict[str, Any]:
    status_counts = _count_by_field(candidate_packets, "candidate_status")
    return {
        "candidate_packet_count": len(candidate_packets),
        "blocked_candidate_count": sum(
            count for status, count in status_counts.items() if status.startswith("blocked_")
        ),
        "ready_for_operator_review_count": status_counts.get(
            "ready_for_operator_review",
            0,
        ),
        "operator_review_needed_count": _count_by_field(
            candidate_packets,
            "operator_review_status",
        ).get("operator_review_needed", 0),
        "candidate_status_counts": status_counts,
        "candidate_type_counts": _count_by_field(candidate_packets, "candidate_type"),
        "decision_support_status_counts": _count_by_field(
            candidate_packets,
            "decision_support_status",
        ),
        "regression_gate_status": _sandbox_regression_status(packet_inputs),
        "operator_next_action_count": len(operator_next_actions),
        "not_applied_candidate_count": sum(
            1 for candidate in candidate_packets if candidate.get("not_applied") is True
        ),
        "runtime_change_status": "not_applied",
        "human_operator_decision_required": True,
        "classifier_correctness_not_assessed": True,
        "decision_packet_is_not_truth": True,
    }


def _proposal_summary(proposal: dict[str, Any]) -> dict[str, Any]:
    proposal_items = [_dict(item) for item in _list(proposal.get("proposal_items"))]
    return {
        "proposal_id": proposal.get("proposal_id"),
        "proposal_item_count": len(proposal_items),
        "blocked_item_count": len(_list(proposal.get("blocked_items"))),
        "proposal_status_counts": _count_by_field(proposal_items, "proposal_status"),
        "proposal_type_counts": _count_by_field(proposal_items, "proposal_type"),
    }


def _sandbox_evaluation_summary(report: dict[str, Any]) -> dict[str, Any]:
    evaluations = [_dict(item) for item in _list(report.get("candidate_evaluations"))]
    return {
        "evaluation_report_id": report.get("evaluation_report_id"),
        "candidate_evaluation_count": len(evaluations),
        "evaluation_status_counts": _count_by_field(evaluations, "evaluation_status"),
        "decision_support_status_counts": _count_by_field(
            evaluations,
            "decision_support_status",
        ),
        "blocked_candidate_count": len(_list(report.get("blocked_candidates"))),
        "baseline_comparison_summary": _dict(report.get("baseline_comparison_summary")),
        "review_coverage_summary": _dict(report.get("review_coverage_summary")),
    }


def _sandbox_regression_summary(verification: dict[str, Any]) -> dict[str, Any]:
    return {
        "baseline_id": verification.get("baseline_id"),
        "status": verification.get("status"),
        "drift_detected": verification.get("drift_detected") is True,
        "breaking_drift_detected": verification.get("breaking_drift_detected") is True,
        "drift_item_count": len(_list(verification.get("drift_items"))),
        "baseline_is_not_truth": verification.get("baseline_is_not_truth") is True,
        "baseline_not_replaced": verification.get("baseline_not_replaced") is True,
        "classifier_correctness_not_assessed": (
            verification.get("classifier_correctness_not_assessed") is True
        ),
    }


def _review_metrics_summary(metrics_report: dict[str, Any]) -> dict[str, Any]:
    summary = _dict(metrics_report.get("summary"))
    review_coverage = _dict(metrics_report.get("review_coverage_summary"))
    source_context = _dict(metrics_report.get("source_context"))
    return {
        "metrics_report_id": metrics_report.get("metrics_report_id"),
        "entry_count": _int(summary.get("entry_count")),
        "reviewed_entry_count": _int(
            summary.get("reviewed_entry_count")
            or review_coverage.get("reviewed_entry_count")
        ),
        "unreviewed_entry_count": _int(
            summary.get("unreviewed_entry_count")
            or review_coverage.get("unreviewed_entry_count")
        ),
        "missing_required_review_field_count": _int(
            summary.get("missing_required_review_field_count")
            or review_coverage.get("missing_required_review_field_count")
        ),
        "fixture_mode_used": source_context.get("fixture_mode_used") is True
        or _dict(metrics_report.get("warnings")).get("fixture_mode_used") is True,
    }


def _blocked_candidate_summary(
    *,
    proposal: dict[str, Any],
    evaluation_report: dict[str, Any],
) -> dict[str, Any]:
    blocked_items = [_dict(item) for item in _list(proposal.get("blocked_items"))]
    blocked_evaluations = [
        _dict(item) for item in _list(evaluation_report.get("blocked_candidates"))
    ]
    return {
        "proposal_blocked_item_count": len(blocked_items),
        "evaluation_blocked_candidate_count": len(blocked_evaluations),
        "proposal_blocked_status_counts": _count_by_field(
            blocked_items,
            "proposal_status",
        ),
        "evaluation_blocked_status_counts": _count_by_field(
            blocked_evaluations,
            "evaluation_status",
        ),
    }


def _regression_gate_summary(packet_inputs: dict[str, Any]) -> dict[str, Any]:
    summary = _dict(packet_inputs.get("sandbox_regression_summary"))
    return {
        **summary,
        "sandbox_regression_status": _sandbox_regression_status(packet_inputs),
        "baseline_comparison_status": _baseline_comparison_status(packet_inputs),
        "runtime_change_status": "not_applied",
        "baseline_not_replaced": True,
    }


def _review_coverage_summary(packet_inputs: dict[str, Any]) -> dict[str, Any]:
    metrics = _dict(packet_inputs.get("review_metrics_summary"))
    evaluation = _dict(packet_inputs.get("sandbox_evaluation_summary"))
    return {
        **metrics,
        "sandbox_review_coverage_summary": _dict(
            evaluation.get("review_coverage_summary")
        ),
        "human_operator_decision_required": True,
    }


def _current_settings(
    *,
    proposal: dict[str, Any],
    evaluation_report: dict[str, Any],
    evaluation_inputs: dict[str, Any],
) -> dict[str, Any]:
    current = _dict(evaluation_report.get("current_settings"))
    return {
        "current_threshold": current.get("current_threshold")
        or evaluation_inputs.get("current_threshold")
        or proposal.get("current_threshold"),
        "current_smoothing_window": current.get("current_smoothing_window")
        or evaluation_inputs.get("current_smoothing_window")
        or proposal.get("current_smoothing_window"),
        "current_hysteresis_settings": _dict(
            current.get("current_hysteresis_settings")
        )
        or _dict(evaluation_inputs.get("current_hysteresis_settings"))
        or _dict(proposal.get("current_hysteresis_settings")),
        "runtime_change_status": "not_applied",
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


def _candidate_warnings(
    *,
    proposal_item: dict[str, Any],
    setting: dict[str, Any],
    evaluation: dict[str, Any],
) -> dict[str, Any]:
    return {
        **_dict(proposal_item.get("warnings")),
        **_dict(setting.get("warnings")),
        **_dict(evaluation.get("warnings")),
        **dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
    }


def _merged_warnings(source_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    warnings = dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS)
    for payload in source_payloads.values():
        warnings.update(_dict(payload.get("warnings")))
    warnings.update(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS)
    return warnings


def _candidate_report_summary(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_packet_id": candidate.get("candidate_packet_id"),
        "candidate_setting_id": candidate.get("candidate_setting_id"),
        "source_proposal_item_id": candidate.get("source_proposal_item_id"),
        "candidate_type": candidate.get("candidate_type"),
        "candidate_status": candidate.get("candidate_status"),
        "decision_support_status": candidate.get("decision_support_status"),
        "operator_review_status": candidate.get("operator_review_status"),
        "not_applied": candidate.get("not_applied") is True,
        "runtime_change_status": candidate.get("runtime_change_status"),
        "blocker_count": len(_list(candidate.get("blockers"))),
        "risk_flags": _list(candidate.get("risk_flags")),
    }


def _candidate_setting_id(
    *,
    evaluation: dict[str, Any],
    setting: dict[str, Any],
    proposal_item: dict[str, Any],
) -> str:
    value = (
        evaluation.get("candidate_setting_id")
        or setting.get("candidate_setting_id")
        or proposal_item.get("proposal_item_id")
    )
    return str(value or "not_applicable")


def _provenance_status(
    *,
    proposal_item: dict[str, Any],
    setting: dict[str, Any],
    evaluation: dict[str, Any],
) -> str:
    if proposal_item and setting and evaluation:
        return "source_artifacts_available"
    if proposal_item or setting or evaluation:
        return "source_context_partial"
    return "source_context_missing"


def _fallback_evaluation_for_proposal_item(proposal_item: dict[str, Any]) -> dict[str, Any]:
    candidate_setting = _dict(proposal_item.get("proposed_candidate_setting"))
    return {
        "candidate_evaluation_id": _stable_id(
            "calibration_candidate_decision_packet_fallback_evaluation_v1",
            proposal_item.get("proposal_item_id"),
        ),
        "candidate_setting_id": proposal_item.get("proposal_item_id"),
        "candidate_type": candidate_setting.get("setting_type") or "not_applicable",
        "evaluation_status": proposal_item.get("proposal_status") or "not_applicable",
        "decision_support_status": "needs_more_human_review",
    }


def _source_summary_scan_payload(
    source_payloads: dict[str, dict[str, Any]],
) -> dict[str, Any]:
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


def _validate_source_artifacts(
    proposal: dict[str, Any],
    evaluation_report: dict[str, Any],
    regression_verification: dict[str, Any],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not _list(proposal.get("proposal_items")):
        errors.append(_error("missing_proposal_items", "source_calibration_proposal", None))
    if "candidate_evaluations" not in evaluation_report:
        errors.append(
            _error(
                "missing_candidate_evaluations",
                "source_sandbox_evaluation_report",
                None,
            )
        )
    if regression_verification.get("status") is None:
        errors.append(
            _error(
                "missing_regression_verification_status",
                "source_sandbox_regression_verification.status",
                None,
            )
        )
    return errors


def _validate_packet_input_shape(packet_inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(packet_inputs, "packet_inputs")
    if (
        packet_inputs.get("packet_input_type")
        != CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_packet_input_type",
                "packet_input_type",
                packet_inputs.get("packet_input_type"),
            )
        )
    if (
        packet_inputs.get("packet_input_version")
        != CALIBRATION_CANDIDATE_DECISION_PACKET_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_packet_input_version",
                "packet_input_version",
                packet_inputs.get("packet_input_version"),
            )
        )
    for field in PACKET_INPUT_REQUIRED_FIELDS:
        if field not in packet_inputs:
            errors.append(_error("missing_packet_input_field", field, None))
    errors.extend(_source_contract_ref_errors(_dict(packet_inputs.get("source_contract_refs"))))
    errors.extend(_required_flag_errors(_dict(packet_inputs.get("warnings")), "warnings"))
    errors.extend(_required_flag_errors(_dict(packet_inputs.get("non_claims")), "non_claims"))
    for candidate_input in _list(packet_inputs.get("candidate_inputs")):
        if not isinstance(candidate_input, dict):
            errors.append(_error("invalid_candidate_input", "candidate_inputs", candidate_input))
    return errors


def _validate_decision_packet_shape(packet: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(packet, "decision_packet")
    if packet.get("decision_packet_type") != CALIBRATION_CANDIDATE_DECISION_PACKET_TYPE:
        errors.append(
            _error(
                "invalid_decision_packet_type",
                "decision_packet_type",
                packet.get("decision_packet_type"),
            )
        )
    if packet.get("decision_packet_version") != CALIBRATION_CANDIDATE_DECISION_PACKET_VERSION:
        errors.append(
            _error(
                "invalid_decision_packet_version",
                "decision_packet_version",
                packet.get("decision_packet_version"),
            )
        )
    for field in DECISION_PACKET_REQUIRED_FIELDS:
        if field not in packet:
            errors.append(_error("missing_decision_packet_field", field, None))
    errors.extend(_source_contract_ref_errors(_dict(packet.get("source_contract_refs"))))
    errors.extend(_required_flag_errors(_dict(packet.get("warnings")), "warnings"))
    errors.extend(_required_flag_errors(_dict(packet.get("non_claims")), "non_claims"))
    candidate_packets = _list(packet.get("candidate_packets"))
    blocked_candidates = _list(packet.get("blocked_candidates"))
    for candidate in candidate_packets:
        if not isinstance(candidate, dict):
            errors.append(_error("invalid_candidate_packet", "candidate_packets", candidate))
            continue
        errors.extend(_validate_candidate_packet_shape(candidate))
    blocked_ids = {
        str(_dict(candidate).get("candidate_packet_id"))
        for candidate in blocked_candidates
    }
    for candidate in candidate_packets:
        if not isinstance(candidate, dict):
            continue
        status = str(candidate.get("candidate_status") or "")
        if (
            status.startswith("blocked_")
            and str(candidate.get("candidate_packet_id")) not in blocked_ids
        ):
            errors.append(
                _error(
                    "blocked_candidate_missing_from_summary",
                    "blocked_candidates",
                    candidate.get("candidate_packet_id"),
                )
            )
    for action in _list(packet.get("operator_next_actions")):
        action_type = _dict(action).get("action_type")
        if action_type not in ALLOWED_OPERATOR_NEXT_ACTION_TYPES:
            errors.append(_error("invalid_operator_action_type", "action_type", action_type))
        if _dict(action).get("runtime_change_status") != "not_applied":
            errors.append(
                _error(
                    "operator_action_runtime_status_must_remain_not_applied",
                    "runtime_change_status",
                    _dict(action).get("runtime_change_status"),
                )
            )
    return errors


def _validate_candidate_packet_shape(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for field in CANDIDATE_PACKET_REQUIRED_FIELDS:
        if field not in candidate:
            errors.append(_error("missing_candidate_packet_field", field, None))
    if candidate.get("candidate_type") not in ALLOWED_CANDIDATE_TYPES:
        errors.append(
            _error("invalid_candidate_type", "candidate_type", candidate.get("candidate_type"))
        )
    if candidate.get("candidate_status") not in ALLOWED_CANDIDATE_STATUSES:
        errors.append(
            _error(
                "invalid_candidate_status",
                "candidate_status",
                candidate.get("candidate_status"),
            )
        )
    if candidate.get("sandbox_evaluation_status") not in ALLOWED_SANDBOX_EVALUATION_STATUSES:
        errors.append(
            _error(
                "invalid_sandbox_evaluation_status",
                "sandbox_evaluation_status",
                candidate.get("sandbox_evaluation_status"),
            )
        )
    if candidate.get("sandbox_regression_status") not in ALLOWED_SANDBOX_REGRESSION_STATUSES:
        errors.append(
            _error(
                "invalid_sandbox_regression_status",
                "sandbox_regression_status",
                candidate.get("sandbox_regression_status"),
            )
        )
    if candidate.get("baseline_comparison_status") not in ALLOWED_BASELINE_COMPARISON_STATUSES:
        errors.append(
            _error(
                "invalid_baseline_comparison_status",
                "baseline_comparison_status",
                candidate.get("baseline_comparison_status"),
            )
        )
    if candidate.get("review_coverage_status") not in ALLOWED_REVIEW_COVERAGE_STATUSES:
        errors.append(
            _error(
                "invalid_review_coverage_status",
                "review_coverage_status",
                candidate.get("review_coverage_status"),
            )
        )
    if candidate.get("decision_support_status") not in ALLOWED_DECISION_SUPPORT_STATUSES:
        errors.append(
            _error(
                "invalid_decision_support_status",
                "decision_support_status",
                candidate.get("decision_support_status"),
            )
        )
    if candidate.get("operator_review_status") not in ALLOWED_OPERATOR_REVIEW_STATUSES:
        errors.append(
            _error(
                "invalid_operator_review_status",
                "operator_review_status",
                candidate.get("operator_review_status"),
            )
        )
    if candidate.get("runtime_change_status") not in {
        "not_applied",
        "runtime_application_not_supported",
    }:
        errors.append(
            _error(
                "invalid_runtime_change_status",
                "runtime_change_status",
                candidate.get("runtime_change_status"),
            )
        )
    if candidate.get("not_applied") is not True:
        errors.append(
            _error("candidate_must_remain_not_applied", "not_applied", candidate.get("not_applied"))
        )
    return errors


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, "contract")
    if contract.get("contract_type") != CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != CALIBRATION_CANDIDATE_DECISION_PACKET_CONTRACT_VERSION
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
    loaded = _load_json(contract_path, label="decision_packet_contract")
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
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
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
        "warnings": dict(CALIBRATION_CANDIDATE_DECISION_PACKET_WARNINGS),
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


def _forbidden_token_errors(value: Any, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}" if path else key_text
            if key_text in FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS:
                errors.append(_error("forbidden_field_or_value", nested_path, key_text))
            errors.extend(_forbidden_token_errors(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, f"{path}[{index}]"))
    elif (
        isinstance(value, str)
        and value in FORBIDDEN_CALIBRATION_CANDIDATE_DECISION_PACKET_TOKENS
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
        "blueprint": CALIBRATION_CANDIDATE_DECISION_PACKET_BLUEPRINT,
        "blueprint_name": CALIBRATION_CANDIDATE_DECISION_PACKET_BLUEPRINT_NAME,
    }


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "path": path,
        "value": value,
    }
