from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT,
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT,
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION,
    validate_review_guided_gameplay_calibration_evaluation_inputs,
    validate_review_guided_gameplay_calibration_evaluation_report,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    NON_CLAIMS as EVALUATION_SANDBOX_NON_CLAIMS,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    SANDBOX_WARNINGS as EVALUATION_SANDBOX_WARNINGS,
)
from apps.worker.services.review_guided_gameplay_calibration_evaluation_sandbox import (
    SOURCE_CONTRACT_REFS as EVALUATION_SANDBOX_SOURCE_CONTRACT_REFS,
)

REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_TYPE = (
    "review_guided_gameplay_calibration_sandbox_regression_contract"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE = (
    "review_guided_gameplay_calibration_sandbox_regression_baseline"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CURRENT_TYPE = (
    "review_guided_gameplay_calibration_sandbox_regression_current"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_TYPE = (
    "review_guided_gameplay_calibration_sandbox_regression_verification"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_TYPE = (
    "review_guided_gameplay_calibration_sandbox_regression_report"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BLUEPRINT = "blueprint_51"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BLUEPRINT_NAME = (
    "calibration_evaluation_sandbox_regression_gate_v1"
)

DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT = (
    ".data/contracts/review_guided_gameplay_calibration_sandbox_regression_contract_v1.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT = (
    ".data/baselines/review_guided_gameplay_calibration_sandbox.baseline.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CURRENT_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_sandbox.current.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_sandbox.regression.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_sandbox.report.json"
)

REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_GENERATED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

ALLOWED_VERIFICATION_STATUSES = {
    "baseline_missing",
    "baseline_invalid",
    "current_output_invalid",
    "completed",
    "drift_detected",
    "breaking_drift_detected",
    "verification_failed",
}
ALLOWED_DRIFT_SEVERITIES = {"info", "warning", "breaking"}

FORBIDDEN_CALIBRATION_SANDBOX_REGRESSION_TOKENS = {
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
    "threshold_changes_applied",
    "smoothing_changes_applied",
    "hysteresis_changes_applied",
    "runtime_config_updated",
    "model_weights_modified",
    "baseline_replaced",
}

REGRESSION_WARNINGS = {
    "baseline_is_not_truth": True,
    "sandbox_is_not_truth": True,
    "sandbox_is_not_accuracy_scoring": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "runtime_config_not_updated": True,
    "model_weights_not_modified": True,
    "baseline_not_replaced": True,
    "classifier_correctness_not_assessed": True,
    "generalization_not_claimed": True,
    "regression_gate_only": True,
    "structural_outputs_only": True,
    "offline_evaluation_only": True,
    "observation_only": True,
    "no_adjudication": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
}

NON_CLAIMS = {
    "not_point_detection": True,
    "not_scoring": True,
    "not_line_calling": True,
    "not_gameplay_ground_truth": True,
    "not_classifier_correctness_benchmark": True,
    "not_classifier_accuracy_benchmark": True,
    "not_generalization_claim": True,
    "not_production_readiness_claim": True,
    "not_training_label_source": True,
    "not_automatic_relabeling": True,
    "not_model_tuning": True,
    "not_runtime_calibration": True,
    "not_baseline_replacement": True,
}

SOURCE_CONTRACT_REFS = {
    "review_guided_gameplay_calibration_evaluation_sandbox_contract_version": (
        REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION
    ),
    **dict(EVALUATION_SANDBOX_SOURCE_CONTRACT_REFS),
}

BASELINE_REQUIRED_FIELDS = [
    "baseline_id",
    "baseline_version",
    "generated_at",
    "source_evaluation_input_path",
    "source_evaluation_report_path",
    "model_asset_ref",
    "model_asset_sha256",
    "current_threshold",
    "current_smoothing_window",
    "current_hysteresis_settings",
    "candidate_setting_count",
    "evaluated_candidate_count",
    "blocked_candidate_count",
    "ready_for_offline_evaluation_count",
    "blocked_missing_review_data_count",
    "blocked_insufficient_sample_size_count",
    "blocked_fixture_only_data_count",
    "blocked_no_human_review_count",
    "invalid_candidate_count",
    "not_applied_candidate_count",
    "drift_detected_count",
    "breaking_drift_detected_count",
    "human_review_required_count",
    "decision_support_status_distribution",
    "evaluation_status_distribution",
    "warning_categories",
    "non_claims",
]

SUMMARY_COMPARE_FIELDS = [
    ("source_contract_refs", "breaking"),
    ("model_asset_sha256", "breaking"),
    ("current_threshold", "breaking"),
    ("current_smoothing_window", "breaking"),
    ("current_hysteresis_settings", "breaking"),
    ("candidate_setting_count", "breaking"),
    ("evaluated_candidate_count", "breaking"),
    ("blocked_candidate_count", "breaking"),
    ("ready_for_offline_evaluation_count", "breaking"),
    ("blocked_missing_review_data_count", "breaking"),
    ("blocked_insufficient_sample_size_count", "breaking"),
    ("blocked_fixture_only_data_count", "breaking"),
    ("blocked_no_human_review_count", "breaking"),
    ("invalid_candidate_count", "breaking"),
    ("not_applied_candidate_count", "breaking"),
    ("drift_detected_count", "warning"),
    ("breaking_drift_detected_count", "breaking"),
    ("human_review_required_count", "warning"),
    ("decision_support_status_distribution", "breaking"),
    ("evaluation_status_distribution", "breaking"),
    ("warning_categories", "breaking"),
    ("non_claims", "breaking"),
    ("fixture_reuse_only", "breaking"),
    ("not_distinct_real_broadcast_corpus", "breaking"),
    ("does_not_claim_generalization", "breaking"),
]


def export_review_guided_gameplay_calibration_sandbox_regression_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = (
        exported_at or REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_EXPORTED_AT
    )
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_TYPE
        ),
        "contract_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
        ),
        "baseline_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE
        ),
        "baseline_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_VERSION
        ),
        "contract": contract,
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_review_guided_gameplay_calibration_sandbox_regression_baseline(
    *,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT
    ),
    source_evaluation_input_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT
    ),
    source_evaluation_report_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    source_evaluation_contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = (
        generated_at
        or REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_GENERATED_AT
    )
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    if errors:
        return _failed_result(
            status="baseline_invalid",
            errors=errors,
            output_path=output_path,
            result_key="baseline_output",
        )
    current_result = _build_current_summary(
        source_evaluation_input_path=source_evaluation_input_path,
        source_evaluation_report_path=source_evaluation_report_path,
        source_evaluation_contract_path=source_evaluation_contract_path,
        generated_at=generated_at,
    )
    if current_result.get("ok") is False:
        return _failed_result(
            status="current_output_invalid",
            errors=_list(current_result.get("errors")),
            output_path=output_path,
            result_key="baseline_output",
        )
    baseline = _baseline_from_current(
        current=_dict(current_result.get("current")),
        generated_at=generated_at,
    )
    baseline_errors = _validate_baseline_shape(baseline)
    if baseline_errors:
        return _failed_result(
            status="baseline_invalid",
            errors=baseline_errors,
            output_path=output_path,
            result_key="baseline_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "baseline_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE
        ),
        "baseline_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_VERSION
        ),
        "baseline_id": baseline["baseline_id"],
        "baseline": baseline,
        "summary": baseline["summary"],
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, baseline, result, "baseline_output")
    return result


def verify_review_guided_gameplay_calibration_sandbox_regression_baseline(
    *,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT
    ),
    baseline_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT
    ),
    source_evaluation_input_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT
    ),
    source_evaluation_report_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    source_evaluation_contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    current_output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CURRENT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT
    ),
    verified_at: datetime | None = None,
) -> dict[str, Any]:
    verified_at = verified_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    baseline = _load_baseline(baseline_path=baseline_path, errors=errors)
    if errors:
        missing_baseline = any(
            error.get("error_type") == "baseline_load_failed" for error in errors
        )
        status = "baseline_missing" if missing_baseline and not baseline else "baseline_invalid"
        verification = _verification_payload(
            status=status,
            baseline=baseline,
            current={},
            drift_items=errors,
            verified_at=verified_at,
        )
        return _write_verification(verification, output_path)

    current_result = _build_current_summary(
        source_evaluation_input_path=source_evaluation_input_path,
        source_evaluation_report_path=source_evaluation_report_path,
        source_evaluation_contract_path=source_evaluation_contract_path,
        generated_at=verified_at,
    )
    if current_result.get("ok") is False:
        verification = _verification_payload(
            status="current_output_invalid",
            baseline=baseline,
            current={},
            drift_items=_list(current_result.get("errors")),
            verified_at=verified_at,
        )
        return _write_verification(verification, output_path)

    current = _dict(current_result.get("current"))
    _write_json_if_requested(current_output_path, current, {}, "current_output")
    drift_items = _compare_summaries(
        baseline_summary=_dict(baseline.get("summary")),
        current_summary=_dict(current.get("summary")),
    )
    drift_detected = bool(drift_items)
    breaking_drift = any(item.get("severity") == "breaking" for item in drift_items)
    status = (
        "breaking_drift_detected"
        if breaking_drift
        else "drift_detected"
        if drift_detected
        else "completed"
    )
    verification = _verification_payload(
        status=status,
        baseline=baseline,
        current=current,
        drift_items=drift_items,
        verified_at=verified_at,
    )
    return _write_verification(verification, output_path)


def build_review_guided_gameplay_calibration_sandbox_regression_report(
    *,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_OUTPUT
    ),
    baseline_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_OUTPUT
    ),
    verification_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    _load_contract(contract_path=contract_path, errors=errors)
    baseline = _load_baseline(baseline_path=baseline_path, errors=errors)
    verification = _load_verification(verification_path=verification_path, errors=errors)
    if verification:
        errors.extend(_validate_verification_shape(verification))
    report = {
        "report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_TYPE,
        "report_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "baseline_path": str(Path(baseline_path)),
        "verification_path": str(Path(verification_path)),
        "baseline_id": baseline.get("baseline_id"),
        "verification_status": verification.get("status"),
        "drift_detected": verification.get("drift_detected"),
        "breaking_drift_detected": verification.get("breaking_drift_detected"),
        "drift_items": _list(verification.get("drift_items")),
        "summary": {
            "baseline_summary": _dict(verification.get("baseline_summary")),
            "current_summary": _dict(verification.get("current_summary")),
            "error_count": len(errors),
            "report_is_structural_only": True,
            "baseline_not_replaced": True,
            "threshold_changes_not_applied": True,
            "smoothing_changes_not_applied": True,
            "hysteresis_changes_not_applied": True,
            "runtime_config_not_updated": True,
            "model_weights_not_modified": True,
        },
        "errors": errors,
        "warnings": dict(REGRESSION_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": not errors,
        "status": "completed" if not errors else "verification_failed",
        "report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_REPORT_TYPE,
        "report_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
        ),
        "baseline_id": baseline.get("baseline_id"),
        "report": report,
        "warnings": dict(REGRESSION_WARNINGS),
    }
    _write_json_if_requested(output_path, report, result, "report_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_TYPE
        ),
        "contract_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "regression_scope": {
            "purpose": "calibration_evaluation_sandbox_structural_regression_protection",
            "freezes_evaluation_input_structure": True,
            "freezes_candidate_setting_semantics": True,
            "checks_candidate_settings_are_not_applied": True,
            "checks_blocked_candidate_handling": True,
            "checks_offline_evaluation_report_summaries": True,
            "checks_structural_drift_summaries": True,
            "checks_non_claim_guardrails": True,
            "checks_baseline_comparison_behavior": True,
            "checks_runtime_application_safety_guards": True,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "writes_runtime_config": False,
            "updates_model_assets": False,
            "replaces_existing_baselines": False,
            "scores_classifier_correctness": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "baseline_schema": {
            "baseline_type": (
                REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE
            ),
            "baseline_version": (
                REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_VERSION
            ),
            "required_fields": list(BASELINE_REQUIRED_FIELDS),
        },
        "verification_schema": {
            "verification_type": (
                REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_TYPE
            ),
            "allowed_statuses": sorted(ALLOWED_VERIFICATION_STATUSES),
            "allowed_result_fields": [
                "ok",
                "status",
                "baseline_id",
                "current_summary",
                "baseline_summary",
                "drift_detected",
                "breaking_drift_detected",
                "drift_items",
                "warnings",
                "baseline_is_not_truth",
                "sandbox_is_not_truth",
                "sandbox_is_not_accuracy_scoring",
                "threshold_changes_not_applied",
                "smoothing_changes_not_applied",
                "hysteresis_changes_not_applied",
                "runtime_config_not_updated",
                "model_weights_not_modified",
                "baseline_not_replaced",
                "classifier_correctness_not_assessed",
                "generalization_not_claimed",
            ],
        },
        "drift_detection_schema": {
            "allowed_severities": sorted(ALLOWED_DRIFT_SEVERITIES),
            "compares_source_contract_refs": True,
            "compares_model_asset_sha": True,
            "compares_threshold_smoothing_hysteresis_metadata": True,
            "compares_candidate_counts": True,
            "compares_blocked_candidate_counts": True,
            "compares_status_distributions": True,
            "compares_not_applied_counts": True,
            "compares_drift_counts": True,
            "compares_warning_categories": True,
            "compares_non_claims": True,
            "breaking_drift_is_structural_or_safety_guardrail_only": True,
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_source_evaluation_input_shape": True,
            "validate_source_evaluation_report_shape": True,
            "validate_baseline_shape": True,
            "validate_verification_report_shape": True,
            "validate_allowed_statuses": True,
            "validate_allowed_severities": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_exact_tokens": True,
            "report_structural_errors_only": True,
            "requires_candidate_settings_to_remain_not_applied": True,
            "requires_runtime_config_to_remain_unwritten": True,
            "requires_model_assets_to_remain_unmodified": True,
            "requires_existing_baselines_to_remain_unreplaced": True,
            "does_not_infer_tennis_meaning": True,
        },
        "provenance_requirements": {
            "source_evaluation_input_path_required": True,
            "source_evaluation_report_path_required": True,
            "model_asset_provenance_required": True,
            "current_gate_settings_recorded_as_read_only_context": True,
            "candidate_counts_recorded": True,
            "blocked_candidate_statuses_recorded": True,
            "decision_support_distribution_recorded": True,
            "evaluation_status_distribution_recorded": True,
            "warnings_preserved": True,
            "non_claims_preserved": True,
            "fixture_or_demo_reuse_marked_when_present": True,
        },
        "warnings": dict(REGRESSION_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }


def _build_current_summary(
    *,
    source_evaluation_input_path: str | Path,
    source_evaluation_report_path: str | Path,
    source_evaluation_contract_path: str | Path,
    generated_at: datetime,
) -> dict[str, Any]:
    validation_errors = _validate_source_evaluation_outputs(
        source_evaluation_input_path=source_evaluation_input_path,
        source_evaluation_report_path=source_evaluation_report_path,
        source_evaluation_contract_path=source_evaluation_contract_path,
        validated_at=generated_at,
    )
    if validation_errors:
        return {"ok": False, "errors": validation_errors}
    inputs = _load_required_json(
        source_evaluation_input_path,
        "review_guided_gameplay_calibration_evaluation_inputs",
        [],
    )
    report = _load_required_json(
        source_evaluation_report_path,
        "review_guided_gameplay_calibration_evaluation_report",
        [],
    )
    summary = _summary_from_sources(
        inputs=inputs,
        report=report,
    )
    current = {
        "current_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CURRENT_TYPE,
        "current_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_evaluation_input_path": str(Path(source_evaluation_input_path)),
        "source_evaluation_report_path": str(Path(source_evaluation_report_path)),
        "source_evaluation_contract_path": str(Path(source_evaluation_contract_path)),
        "source_evaluation_input_id": inputs.get("evaluation_input_id"),
        "source_evaluation_report_id": report.get("evaluation_report_id"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "model_asset_ref": summary.get("model_asset_ref"),
        "model_asset_sha256": summary.get("model_asset_sha256"),
        "current_threshold": summary.get("current_threshold"),
        "current_smoothing_window": summary.get("current_smoothing_window"),
        "current_hysteresis_settings": summary.get("current_hysteresis_settings"),
        "summary": summary,
        "warnings": _regression_warnings(summary=summary),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    return {"ok": True, "current": current}


def _validate_source_evaluation_outputs(
    *,
    source_evaluation_input_path: str | Path,
    source_evaluation_report_path: str | Path,
    source_evaluation_contract_path: str | Path,
    validated_at: datetime,
) -> list[dict[str, Any]]:
    input_validation = validate_review_guided_gameplay_calibration_evaluation_inputs(
        evaluation_inputs_path=source_evaluation_input_path,
        contract_path=source_evaluation_contract_path,
        output_path=None,
        validated_at=validated_at,
    )
    report_validation = validate_review_guided_gameplay_calibration_evaluation_report(
        evaluation_report_path=source_evaluation_report_path,
        contract_path=source_evaluation_contract_path,
        output_path=None,
        validated_at=validated_at,
    )
    errors: list[dict[str, Any]] = []
    if input_validation.get("ok") is False:
        errors.append(
            _error(
                "source_evaluation_inputs_invalid",
                "source_evaluation_input_path",
                input_validation,
            )
        )
    if report_validation.get("ok") is False:
        errors.append(
            _error(
                "source_evaluation_report_invalid",
                "source_evaluation_report_path",
                report_validation,
            )
        )
    return errors


def _summary_from_sources(
    *,
    inputs: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, Any]:
    candidate_settings = [_dict(item) for item in _list(inputs.get("candidate_settings"))]
    candidate_evaluations = [
        _dict(item) for item in _list(report.get("candidate_evaluations"))
    ]
    blocked_candidates = [_dict(item) for item in _list(report.get("blocked_candidates"))]
    candidate_status_distribution = _count_by_field(candidate_settings, "candidate_status")
    evaluation_status_distribution = _count_by_field(
        candidate_evaluations,
        "evaluation_status",
    )
    decision_support_status_distribution = _count_by_field(
        candidate_evaluations,
        "decision_support_status",
    )
    settings = _dict(report.get("current_settings"))
    warnings = _merged_warnings(inputs=inputs, report=report)
    non_claims = {
        **dict(EVALUATION_SANDBOX_NON_CLAIMS),
        **_dict(inputs.get("non_claims")),
        **_dict(report.get("non_claims")),
        **dict(NON_CLAIMS),
    }
    fixture_reuse_only = _fixture_reuse_detected(
        inputs=inputs,
        report=report,
        warnings=warnings,
        candidate_status_distribution=candidate_status_distribution,
    )
    current_threshold = settings.get("threshold", inputs.get("current_threshold"))
    current_smoothing_window = settings.get(
        "smoothing_window",
        inputs.get("current_smoothing_window"),
    )
    current_hysteresis_settings = _dict(
        settings.get("hysteresis_settings", inputs.get("current_hysteresis_settings"))
    )
    summary = {
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "source_evaluation_input_id": inputs.get("evaluation_input_id"),
        "source_evaluation_report_id": report.get("evaluation_report_id"),
        "model_asset_ref": report.get("model_asset_ref", inputs.get("model_asset_ref")),
        "model_asset_sha256": report.get(
            "model_asset_sha256",
            inputs.get("model_asset_sha256"),
        ),
        "current_threshold": current_threshold,
        "current_smoothing_window": current_smoothing_window,
        "current_hysteresis_settings": current_hysteresis_settings,
        "candidate_setting_count": len(candidate_settings),
        "evaluated_candidate_count": sum(
            evaluation.get("evaluation_status")
            in {"evaluated_offline", "completed_with_warnings"}
            for evaluation in candidate_evaluations
        ),
        "blocked_candidate_count": len(blocked_candidates)
        or sum(
            str(evaluation.get("evaluation_status", "")).startswith("blocked_")
            for evaluation in candidate_evaluations
        ),
        "ready_for_offline_evaluation_count": candidate_status_distribution.get(
            "ready_for_offline_evaluation",
            0,
        ),
        "blocked_missing_review_data_count": candidate_status_distribution.get(
            "blocked_missing_review_data",
            0,
        ),
        "blocked_insufficient_sample_size_count": candidate_status_distribution.get(
            "blocked_insufficient_sample_size",
            0,
        ),
        "blocked_fixture_only_data_count": candidate_status_distribution.get(
            "blocked_fixture_only_data",
            0,
        ),
        "blocked_no_human_review_count": candidate_status_distribution.get(
            "blocked_no_human_review",
            0,
        ),
        "invalid_candidate_count": candidate_status_distribution.get(
            "invalid_candidate",
            0,
        )
        or evaluation_status_distribution.get("blocked_invalid_candidate", 0),
        "not_applied_candidate_count": sum(
            candidate.get("not_applied") is True for candidate in candidate_settings
        ),
        "drift_detected_count": sum(
            evaluation.get("drift_detected") is True for evaluation in candidate_evaluations
        ),
        "breaking_drift_detected_count": sum(
            evaluation.get("breaking_drift_detected") is True
            for evaluation in candidate_evaluations
        ),
        "human_review_required_count": sum(
            candidate.get("human_review_required") is True for candidate in candidate_settings
        ),
        "candidate_status_distribution": dict(candidate_status_distribution),
        "decision_support_status_distribution": dict(decision_support_status_distribution),
        "evaluation_status_distribution": dict(evaluation_status_distribution),
        "warning_categories": sorted(warnings.keys()),
        "non_claims": dict(sorted(non_claims.items())),
        "fixture_reuse_only": fixture_reuse_only,
        "not_distinct_real_broadcast_corpus": fixture_reuse_only,
        "does_not_claim_generalization": True,
        "baseline_is_not_truth": True,
        "sandbox_is_not_truth": True,
        "sandbox_is_not_accuracy_scoring": True,
        "threshold_changes_not_applied": True,
        "smoothing_changes_not_applied": True,
        "hysteresis_changes_not_applied": True,
        "runtime_config_not_updated": True,
        "model_weights_not_modified": True,
        "baseline_not_replaced": True,
        "classifier_correctness_not_assessed": True,
        "generalization_not_claimed": True,
    }
    return summary


def _baseline_from_current(
    *,
    current: dict[str, Any],
    generated_at: datetime,
) -> dict[str, Any]:
    summary = _dict(current.get("summary"))
    baseline_id = _stable_id(
        "review_guided_gameplay_calibration_sandbox_regression_baseline_v1",
        json.dumps(summary, sort_keys=True),
    )
    baseline = {
        "baseline_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE
        ),
        "baseline_id": baseline_id,
        "baseline_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_evaluation_input_path": current.get("source_evaluation_input_path"),
        "source_evaluation_report_path": current.get("source_evaluation_report_path"),
        "source_evaluation_contract_path": current.get("source_evaluation_contract_path"),
        "source_evaluation_input_id": current.get("source_evaluation_input_id"),
        "source_evaluation_report_id": current.get("source_evaluation_report_id"),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "model_asset_ref": summary.get("model_asset_ref"),
        "model_asset_sha256": summary.get("model_asset_sha256"),
        "current_threshold": summary.get("current_threshold"),
        "current_smoothing_window": summary.get("current_smoothing_window"),
        "current_hysteresis_settings": summary.get("current_hysteresis_settings"),
        "candidate_setting_count": summary.get("candidate_setting_count"),
        "evaluated_candidate_count": summary.get("evaluated_candidate_count"),
        "blocked_candidate_count": summary.get("blocked_candidate_count"),
        "ready_for_offline_evaluation_count": summary.get(
            "ready_for_offline_evaluation_count"
        ),
        "blocked_missing_review_data_count": summary.get(
            "blocked_missing_review_data_count"
        ),
        "blocked_insufficient_sample_size_count": summary.get(
            "blocked_insufficient_sample_size_count"
        ),
        "blocked_fixture_only_data_count": summary.get(
            "blocked_fixture_only_data_count"
        ),
        "blocked_no_human_review_count": summary.get("blocked_no_human_review_count"),
        "invalid_candidate_count": summary.get("invalid_candidate_count"),
        "not_applied_candidate_count": summary.get("not_applied_candidate_count"),
        "drift_detected_count": summary.get("drift_detected_count"),
        "breaking_drift_detected_count": summary.get("breaking_drift_detected_count"),
        "human_review_required_count": summary.get("human_review_required_count"),
        "decision_support_status_distribution": summary.get(
            "decision_support_status_distribution"
        ),
        "evaluation_status_distribution": summary.get("evaluation_status_distribution"),
        "warning_categories": summary.get("warning_categories"),
        "non_claims": summary.get("non_claims"),
        "fixture_reuse_only": summary.get("fixture_reuse_only") is True,
        "not_distinct_real_broadcast_corpus": (
            summary.get("not_distinct_real_broadcast_corpus") is True
        ),
        "does_not_claim_generalization": True,
        "summary": summary,
        "warnings": _regression_warnings(summary=summary),
        "tom_provenance": _tom_provenance(),
    }
    return baseline


def _compare_summaries(
    *,
    baseline_summary: dict[str, Any],
    current_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    drift_items: list[dict[str, Any]] = []
    for field, severity in SUMMARY_COMPARE_FIELDS:
        expected = baseline_summary.get(field)
        actual = current_summary.get(field)
        if expected == actual:
            continue
        drift_items.append(
            {
                "field": field,
                "expected": expected,
                "actual": actual,
                "severity": severity,
                "reason": "calibration_sandbox_structural_regression_mismatch",
            }
        )
    return drift_items


def _verification_payload(
    *,
    status: str,
    baseline: dict[str, Any],
    current: dict[str, Any],
    drift_items: list[dict[str, Any]],
    verified_at: datetime,
) -> dict[str, Any]:
    breaking = any(item.get("severity") == "breaking" for item in drift_items)
    return {
        "verification_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_VERIFICATION_TYPE
        ),
        "verification_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
        ),
        "verified_at": verified_at.isoformat(),
        "ok": status == "completed",
        "status": status,
        "baseline_id": baseline.get("baseline_id"),
        "current_summary": _dict(current.get("summary")),
        "baseline_summary": _dict(baseline.get("summary")),
        "drift_detected": bool(drift_items),
        "breaking_drift_detected": breaking,
        "drift_items": drift_items,
        "warnings": dict(REGRESSION_WARNINGS),
        "baseline_is_not_truth": True,
        "sandbox_is_not_truth": True,
        "sandbox_is_not_accuracy_scoring": True,
        "threshold_changes_not_applied": True,
        "smoothing_changes_not_applied": True,
        "hysteresis_changes_not_applied": True,
        "runtime_config_not_updated": True,
        "model_weights_not_modified": True,
        "baseline_not_replaced": True,
        "classifier_correctness_not_assessed": True,
        "generalization_not_claimed": True,
        "tom_provenance": _tom_provenance(),
    }


def _write_verification(
    verification: dict[str, Any],
    output_path: str | Path | None,
) -> dict[str, Any]:
    result = dict(verification)
    _write_json_if_requested(output_path, verification, result, "verification_output")
    return result


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if (
        contract.get("contract_type")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "regression_scope",
        "source_contract_refs",
        "baseline_schema",
        "verification_schema",
        "drift_detection_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    errors.extend(_source_contract_ref_errors(_dict(contract.get("source_contract_refs"))))
    return errors


def _validate_baseline_shape(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(baseline, path="baseline")
    if (
        baseline.get("baseline_type")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_TYPE
    ):
        errors.append(
            _error(
                "invalid_baseline_type",
                "baseline_type",
                baseline.get("baseline_type"),
            )
        )
    if (
        baseline.get("baseline_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BASELINE_VERSION
    ):
        errors.append(
            _error(
                "invalid_baseline_version",
                "baseline_version",
                baseline.get("baseline_version"),
            )
        )
    for field in BASELINE_REQUIRED_FIELDS:
        if field not in baseline:
            errors.append(_error("missing_baseline_field", field, None))
    errors.extend(_source_contract_ref_errors(_dict(baseline.get("source_contract_refs"))))
    errors.extend(_required_safety_flag_errors(_dict(baseline.get("summary")), "summary"))
    errors.extend(_required_safety_flag_errors(_dict(baseline.get("warnings")), "warnings"))
    for field in (
        "candidate_setting_count",
        "evaluated_candidate_count",
        "blocked_candidate_count",
        "ready_for_offline_evaluation_count",
        "blocked_missing_review_data_count",
        "blocked_insufficient_sample_size_count",
        "blocked_fixture_only_data_count",
        "blocked_no_human_review_count",
        "invalid_candidate_count",
        "not_applied_candidate_count",
        "drift_detected_count",
        "breaking_drift_detected_count",
        "human_review_required_count",
    ):
        if field in baseline and _int(baseline.get(field)) < 0:
            errors.append(_error("negative_count", field, baseline.get(field)))
    if baseline.get("not_applied_candidate_count") != baseline.get(
        "candidate_setting_count"
    ):
        errors.append(
            _error(
                "candidate_settings_must_remain_not_applied",
                "not_applied_candidate_count",
                baseline.get("not_applied_candidate_count"),
            )
        )
    return errors


def _validate_verification_shape(verification: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(verification, path="verification")
    if verification.get("status") not in ALLOWED_VERIFICATION_STATUSES:
        errors.append(
            _error("invalid_verification_status", "status", verification.get("status"))
        )
    for item in _list(verification.get("drift_items")):
        if not isinstance(item, dict):
            errors.append(_error("invalid_drift_item", "drift_items", item))
            continue
        if item.get("severity") not in ALLOWED_DRIFT_SEVERITIES:
            errors.append(_error("invalid_drift_severity", "drift_items.severity", item))
    errors.extend(_required_safety_flag_errors(verification, "verification"))
    return errors


def _source_contract_ref_errors(refs: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for key, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(key) != expected:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _required_safety_flag_errors(payload: dict[str, Any], path: str) -> list[dict[str, Any]]:
    errors = []
    for key in (
        "baseline_is_not_truth",
        "sandbox_is_not_truth",
        "sandbox_is_not_accuracy_scoring",
        "threshold_changes_not_applied",
        "smoothing_changes_not_applied",
        "hysteresis_changes_not_applied",
        "runtime_config_not_updated",
        "model_weights_not_modified",
        "baseline_not_replaced",
        "classifier_correctness_not_assessed",
        "generalization_not_claimed",
    ):
        if payload.get(key) is not True:
            errors.append(_error("missing_safety_guardrail", f"{path}.{key}", payload.get(key)))
    return errors


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(contract_path, label="calibration_sandbox_regression_contract")
    if loaded.get("ok") is False:
        errors.append(_error("contract_load_failed", "contract_path", loaded))
        return {}
    contract = _dict(loaded.get("data"))
    errors.extend(_validate_contract_shape(contract))
    return contract


def _load_baseline(
    *,
    baseline_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(baseline_path, label="calibration_sandbox_regression_baseline")
    if loaded.get("ok") is False:
        errors.append(_error("baseline_load_failed", "baseline_path", loaded))
        return {}
    baseline = _dict(loaded.get("data"))
    errors.extend(_validate_baseline_shape(baseline))
    return baseline


def _load_verification(
    *,
    verification_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    loaded = _load_json(verification_path, label="calibration_sandbox_regression_verification")
    if loaded.get("ok") is False:
        errors.append(_error("verification_load_failed", "verification_path", loaded))
        return {}
    return _dict(loaded.get("data"))


def _merged_warnings(
    *,
    inputs: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, Any]:
    baseline_comparison = _dict(report.get("baseline_comparison_summary"))
    warning_flags = {
        key: value
        for key, value in baseline_comparison.items()
        if key.endswith("_not_applied")
        or key.endswith("_not_updated")
        or key.endswith("_not_replaced")
        or key in {"sandbox_is_not_truth", "sandbox_is_not_accuracy_scoring"}
    }
    return {
        **dict(EVALUATION_SANDBOX_WARNINGS),
        **_dict(inputs.get("warnings")),
        **_dict(report.get("warnings")),
        **warning_flags,
        **dict(REGRESSION_WARNINGS),
    }


def _fixture_reuse_detected(
    *,
    inputs: dict[str, Any],
    report: dict[str, Any],
    warnings: dict[str, Any],
    candidate_status_distribution: dict[str, int],
) -> bool:
    source_context = _dict(inputs.get("source_context"))
    if source_context.get("fixture_mode_used") is True:
        return True
    if warnings.get("fixture_reuse_only") is True:
        return True
    if warnings.get("fixture_mode_available") is True:
        return True
    if candidate_status_distribution.get("blocked_fixture_only_data", 0) > 0:
        return True
    report_mode = str(report.get("evaluation_mode") or "")
    return report_mode == "fixture_only"


def _regression_warnings(*, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **dict(REGRESSION_WARNINGS),
        "fixture_reuse_only": summary.get("fixture_reuse_only") is True,
        "not_distinct_real_broadcast_corpus": (
            summary.get("not_distinct_real_broadcast_corpus") is True
        ),
        "does_not_claim_generalization": True,
    }


def _count_by_field(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field)) for row in rows).items()))


def _failed_result(
    *,
    status: str,
    errors: list[dict[str, Any]],
    output_path: str | Path | None,
    result_key: str,
) -> dict[str, Any]:
    payload = {
        "ok": False,
        "status": status,
        "errors": errors,
        "warnings": dict(REGRESSION_WARNINGS),
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


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            nested_path = f"{path}.{key_text}" if path else key_text
            if key_text in FORBIDDEN_CALIBRATION_SANDBOX_REGRESSION_TOKENS:
                errors.append(_error("forbidden_field_or_value", nested_path, key_text))
            errors.extend(_forbidden_token_errors(nested, path=nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_token_errors(nested, path=f"{path}[{index}]"))
    elif (
        isinstance(value, str)
        and value in FORBIDDEN_CALIBRATION_SANDBOX_REGRESSION_TOKENS
    ):
        errors.append(_error("forbidden_field_or_value", path, value))
    return errors


def _stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256(
        "::".join(str(part) for part in parts).encode("utf-8")
    ).hexdigest()[:24]
    return f"{prefix}_{digest}"


def _tom_provenance() -> dict[str, Any]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BLUEPRINT,
        "blueprint_name": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_SANDBOX_REGRESSION_BLUEPRINT_NAME
        ),
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
        "structural_only": True,
    }
