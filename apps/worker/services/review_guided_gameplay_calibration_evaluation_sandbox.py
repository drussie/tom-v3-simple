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
    DEFAULT_HYSTERESIS_ENTER,
    DEFAULT_HYSTERESIS_EXIT,
    DEFAULT_SMOOTHING_WINDOW,
    DEFAULT_THRESHOLD,
)
from apps.worker.services.real_broadcast_gameplay_gate_corpus_run import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
)
from apps.worker.services.real_broadcast_gameplay_review_loop import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT,
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT,
)
from apps.worker.services.real_broadcast_gameplay_review_metrics import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT,
)
from apps.worker.services.review_guided_gameplay_gate_calibration_proposal import (
    DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT,
    FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS,
    REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION,
)
from apps.worker.services.review_guided_gameplay_gate_calibration_proposal import (
    SOURCE_CONTRACT_REFS as CALIBRATION_PROPOSAL_SOURCE_CONTRACT_REFS,
)

REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_TYPE = (
    "review_guided_gameplay_calibration_evaluation_sandbox_contract"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE = (
    "review_guided_gameplay_calibration_evaluation_inputs"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE = (
    "review_guided_gameplay_calibration_evaluation_report"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_TYPE = (
    "review_guided_gameplay_calibration_evaluation_summary"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_BLUEPRINT = "blueprint_50"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_BLUEPRINT_NAME = (
    "review_guided_gameplay_calibration_evaluation_sandbox_v1"
)

DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT = (
    ".data/contracts/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_evaluation_inputs.current.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_evaluation_inputs.validation.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_evaluation_report.current.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VALIDATION_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_evaluation_report.validation.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_evaluation_summary.current.json"
)

REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

ALLOWED_CANDIDATE_TYPES = [
    "threshold_candidate",
    "smoothing_window_candidate",
    "hysteresis_candidate",
    "combined_candidate",
    "no_candidate",
    "not_applicable",
]

ALLOWED_CANDIDATE_STATUSES = [
    "ready_for_offline_evaluation",
    "blocked_missing_review_data",
    "blocked_insufficient_sample_size",
    "blocked_fixture_only_data",
    "blocked_no_human_review",
    "invalid_candidate",
    "informational_only",
    "not_applicable",
]

ALLOWED_EVALUATION_MODES = [
    "dry_run",
    "fixture_only",
    "structural_offline_evaluation",
    "baseline_comparison_only",
    "not_applicable",
]

ALLOWED_EVALUATION_STATUSES = [
    "evaluated_offline",
    "blocked_missing_review_data",
    "blocked_insufficient_sample_size",
    "blocked_fixture_only_data",
    "blocked_no_human_review",
    "blocked_invalid_candidate",
    "completed_with_warnings",
    "not_applicable",
]

ALLOWED_DECISION_SUPPORT_STATUSES = [
    "insufficient_data",
    "needs_more_human_review",
    "safe_for_future_manual_review",
    "unsafe_for_runtime_application",
    "informational_only",
    "not_applicable",
]

ALLOWED_DRIFT_SEVERITIES = ["info", "warning", "breaking"]

FORBIDDEN_EVALUATION_SANDBOX_TOKENS = {
    *FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS,
    "model_weights_modified",
    "runtime_config_updated",
    "baseline_replaced",
}

SANDBOX_WARNINGS = {
    "sandbox_is_not_truth": True,
    "sandbox_is_not_accuracy_scoring": True,
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
    "human_review_required": True,
    "classifier_correctness_not_assessed": True,
    "offline_evaluation_only": True,
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
    "review_guided_gameplay_calibration_proposal_contract_version": (
        REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION
    ),
    **dict(CALIBRATION_PROPOSAL_SOURCE_CONTRACT_REFS),
}

DRIFT_SUMMARY_FIELDS = [
    "entry_count",
    "gameplay_segment_candidate_count",
    "non_gameplay_segment_candidate_count",
    "uncertain_segment_count",
    "downstream_allowed_window_count",
    "downstream_blocked_window_count",
    "downstream_review_required_window_count",
    "perception_execution_window_count",
    "perception_skipped_window_count",
    "replay_timeline_entry_count",
    "review_dataset_entry_count",
    "status_distribution",
    "warning_categories",
]


def export_review_guided_gameplay_calibration_evaluation_sandbox_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_TYPE
        ),
        "contract_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION
        ),
        "evaluation_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
        "evaluation_report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
        "contract": contract,
        "warnings": dict(SANDBOX_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_review_guided_gameplay_calibration_evaluation_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    source_calibration_proposal_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT
    ),
    source_metrics_report_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT
    ),
    source_review_loop_report_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT
    ),
    source_review_bundle_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT
    ),
    source_corpus_run_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
    source_regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    current_threshold: float = DEFAULT_THRESHOLD,
    current_smoothing_window: int = DEFAULT_SMOOTHING_WINDOW,
    hysteresis_enter: float = DEFAULT_HYSTERESIS_ENTER,
    hysteresis_exit: float = DEFAULT_HYSTERESIS_EXIT,
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    proposal = _load_required_json(
        source_calibration_proposal_path,
        "review_guided_gameplay_calibration_proposal",
        errors,
    )
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if errors:
        return _failed_result(
            status="invalid_evaluation_input_sources",
            errors=errors,
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
            result_key="evaluation_inputs_output",
        )

    metrics_report = _load_optional_json(
        source_metrics_report_path,
        "real_broadcast_gameplay_review_metrics_report",
    )
    review_loop_report = _load_optional_json(
        source_review_loop_report_path,
        "real_broadcast_gameplay_review_loop_report",
    )
    review_bundle = _load_optional_json(
        source_review_bundle_path,
        "real_broadcast_gameplay_review_bundle",
    )
    corpus_run = _load_optional_json(
        source_corpus_run_path,
        "real_broadcast_gameplay_corpus_run",
    )
    regression_baseline = _load_optional_json(
        source_regression_baseline_path,
        "gameplay_gate_regression_baseline",
    )
    current_settings = _settings(
        proposal=proposal,
        regression_baseline=regression_baseline,
        current_threshold=current_threshold,
        current_smoothing_window=current_smoothing_window,
        hysteresis_enter=hysteresis_enter,
        hysteresis_exit=hysteresis_exit,
    )
    model_asset = _model_asset_from_sources(
        proposal=proposal,
        metrics_report=metrics_report,
        review_bundle=review_bundle,
        review_loop_report=review_loop_report,
        model_asset_path=model_asset_path,
    )
    review_metrics_summary = _review_metrics_summary(proposal, metrics_report)
    baseline_summary = _baseline_summary(regression_baseline)
    review_entries = [
        entry for entry in _list(review_bundle.get("entries")) if isinstance(entry, dict)
    ]
    source_context = _source_context(proposal=proposal, corpus_run=corpus_run)
    candidate_settings = _candidate_settings_from_proposal(
        proposal=proposal,
        review_metrics_summary=review_metrics_summary,
        source_context=source_context,
    )
    evaluation_input = {
        "evaluation_input_id": _stable_id(
            "review_guided_gameplay_calibration_evaluation_inputs_v1",
            str(source_calibration_proposal_path),
            candidate_settings,
            current_settings,
        ),
        "evaluation_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
        "evaluation_input_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_calibration_proposal_path": str(Path(source_calibration_proposal_path)),
        "source_metrics_report_path": (
            str(Path(source_metrics_report_path)) if source_metrics_report_path else None
        ),
        "source_review_loop_report_path": (
            str(Path(source_review_loop_report_path))
            if source_review_loop_report_path
            else None
        ),
        "source_review_bundle_path": (
            str(Path(source_review_bundle_path)) if source_review_bundle_path else None
        ),
        "source_corpus_run_path": (
            str(Path(source_corpus_run_path)) if source_corpus_run_path else None
        ),
        "source_regression_baseline_path": (
            str(Path(source_regression_baseline_path))
            if source_regression_baseline_path
            else None
        ),
        "model_asset_ref": model_asset.get("model_asset_ref"),
        "model_asset_sha256": model_asset.get("model_asset_sha256"),
        "model_asset_exists": model_asset.get("model_asset_exists"),
        "current_threshold": current_settings["threshold"],
        "current_smoothing_window": current_settings["smoothing_window"],
        "current_hysteresis_settings": current_settings["hysteresis_settings"],
        "candidate_settings": candidate_settings,
        "proposal_item_refs": _proposal_item_refs(proposal),
        "baseline_summary": baseline_summary,
        "review_metrics_summary": review_metrics_summary,
        "source_context": source_context,
        "review_bundle_summary": _review_bundle_summary(review_entries),
        "current_structural_summary": _current_structural_summary(
            baseline_summary=baseline_summary,
            review_entries=review_entries,
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _warnings_from_sources(
            proposal=proposal,
            metrics_report=metrics_report,
            review_loop_report=review_loop_report,
            review_bundle=review_bundle,
            corpus_run=corpus_run,
            regression_baseline=regression_baseline,
        ),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": True,
        "status": "completed",
        "evaluation_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
        "evaluation_input_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION
        ),
        "evaluation_input_id": evaluation_input["evaluation_input_id"],
        "candidate_setting_count": len(candidate_settings),
        "evaluation_inputs": evaluation_input,
        "warnings": evaluation_input["warnings"],
    }
    _write_json_if_requested(
        output_path,
        evaluation_input,
        result,
        "evaluation_inputs_output",
    )
    return result


def validate_review_guided_gameplay_calibration_evaluation_inputs(
    *,
    evaluation_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(evaluation_inputs_path, "evaluation_inputs", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if inputs:
        errors.extend(_validate_evaluation_input_shape(inputs))
        errors.extend(_validate_source_contract_refs(inputs))
        errors.extend(_forbidden_token_errors(inputs, path="evaluation_inputs"))
    result = _validation_result(
        ok=not errors,
        validation_type="review_guided_gameplay_calibration_evaluation_inputs_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=evaluation_inputs_path,
        payload_type=inputs.get("evaluation_input_type") if inputs else None,
        payload_version=inputs.get("evaluation_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def run_review_guided_gameplay_calibration_evaluation_sandbox(
    *,
    evaluation_inputs_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    evaluation_mode: str = "structural_offline_evaluation",
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_review_guided_gameplay_calibration_evaluation_inputs(
        evaluation_inputs_path=evaluation_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_evaluation_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
            result_key="evaluation_report_output",
        )
    if evaluation_mode not in ALLOWED_EVALUATION_MODES:
        return _failed_result(
            status="invalid_evaluation_mode",
            errors=[_error("unsupported_evaluation_mode", "evaluation_mode", evaluation_mode)],
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
            result_key="evaluation_report_output",
        )

    inputs = _load_optional_json(evaluation_inputs_path, "evaluation_inputs")
    evaluations = [
        _candidate_evaluation(
            candidate=candidate,
            inputs=inputs,
            evaluation_mode=evaluation_mode,
        )
        for candidate in _list(inputs.get("candidate_settings"))
    ]
    blocked_candidates = [
        evaluation
        for evaluation in evaluations
        if str(evaluation.get("evaluation_status", "")).startswith("blocked_")
    ]
    report = {
        "evaluation_report_id": _stable_id(
            "review_guided_gameplay_calibration_evaluation_report_v1",
            str(evaluation_inputs_path),
            evaluations,
        ),
        "evaluation_report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
        "evaluation_report_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_evaluation_input_path": str(Path(evaluation_inputs_path)),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "model_asset_exists": inputs.get("model_asset_exists"),
        "current_settings": _current_settings_payload(inputs),
        "candidate_evaluations": evaluations,
        "blocked_candidates": blocked_candidates,
        "baseline_comparison_summary": _baseline_comparison_summary(evaluations),
        "review_coverage_summary": _dict(inputs.get("review_metrics_summary")),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _dict(inputs.get("warnings")) or dict(SANDBOX_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    errors = _validate_evaluation_report_shape(report)
    if errors:
        return _failed_result(
            status="invalid_evaluation_report",
            errors=errors,
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
            result_key="evaluation_report_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "evaluation_report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE,
        "evaluation_report_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION
        ),
        "evaluation_report_id": report["evaluation_report_id"],
        "candidate_evaluation_count": len(evaluations),
        "blocked_candidate_count": len(blocked_candidates),
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "evaluation_report_output")
    return result


def validate_review_guided_gameplay_calibration_evaluation_report(
    *,
    evaluation_report_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    report = _load_required_json(evaluation_report_path, "evaluation_report", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if report:
        errors.extend(_validate_evaluation_report_shape(report))
        errors.extend(_validate_source_contract_refs(report))
        errors.extend(_forbidden_token_errors(report, path="evaluation_report"))
    result = _validation_result(
        ok=not errors,
        validation_type="review_guided_gameplay_calibration_evaluation_report_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=evaluation_report_path,
        payload_type=report.get("evaluation_report_type") if report else None,
        payload_version=report.get("evaluation_report_version") if report else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_review_guided_gameplay_calibration_evaluation_summary(
    *,
    evaluation_report_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_review_guided_gameplay_calibration_evaluation_report(
        evaluation_report_path=evaluation_report_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_evaluation_report",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_TYPE,
            result_key="evaluation_summary_output",
        )
    report = _load_optional_json(evaluation_report_path, "evaluation_report")
    evaluations = _list(report.get("candidate_evaluations"))
    summary = {
        "summary_id": _stable_id(
            "review_guided_gameplay_calibration_evaluation_summary_v1",
            str(evaluation_report_path),
            report.get("baseline_comparison_summary"),
        ),
        "summary_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_TYPE,
        "summary_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_evaluation_report_path": str(Path(evaluation_report_path)),
        "evaluation_report_id": report.get("evaluation_report_id"),
        "candidate_evaluation_count": len(evaluations),
        "candidate_type_counts": _count_by_field(evaluations, "candidate_type"),
        "evaluation_status_counts": _count_by_field(evaluations, "evaluation_status"),
        "decision_support_status_counts": _count_by_field(
            evaluations,
            "decision_support_status",
        ),
        "blocked_candidate_count": len(_list(report.get("blocked_candidates"))),
        "baseline_comparison_summary": _dict(report.get("baseline_comparison_summary")),
        "review_coverage_summary": _dict(report.get("review_coverage_summary")),
        "validation_snapshot": validation,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _dict(report.get("warnings")) or dict(SANDBOX_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": True,
        "status": "completed",
        "summary_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_TYPE,
        "summary_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SUMMARY_VERSION,
        "summary_id": summary["summary_id"],
        "summary": summary,
        "warnings": summary["warnings"],
    }
    _write_json_if_requested(output_path, summary, result, "evaluation_summary_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_TYPE
        ),
        "contract_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION
        ),
        "exported_at": exported_at.isoformat(),
        "sandbox_scope": {
            "purpose": "review_guided_gameplay_calibration_evaluation_sandbox",
            "reads_calibration_proposal_when_supplied": True,
            "reads_review_metrics_when_supplied": True,
            "reads_review_loop_when_supplied": True,
            "reads_review_bundle_when_supplied": True,
            "builds_evaluation_inputs": True,
            "runs_offline_evaluation": True,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "updates_runtime_config": False,
            "updates_model": False,
            "trains_classifier": False,
            "calculates_classifier_accuracy": False,
            "creates_review_labels": False,
            "mutates_regression_baselines": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "evaluation_input_schema": {
            "evaluation_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE,
            "evaluation_input_version": (
                REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION
            ),
            "required_fields": [
                "evaluation_input_id",
                "evaluation_input_type",
                "evaluation_input_version",
                "generated_at",
                "source_calibration_proposal_path",
                "source_metrics_report_path",
                "source_review_loop_report_path",
                "source_review_bundle_path",
                "source_corpus_run_path",
                "source_regression_baseline_path",
                "model_asset_ref",
                "model_asset_sha256",
                "current_threshold",
                "current_smoothing_window",
                "current_hysteresis_settings",
                "candidate_settings",
                "proposal_item_refs",
                "baseline_summary",
                "review_metrics_summary",
                "warnings",
                "non_claims",
            ],
        },
        "candidate_setting_schema": {
            "allowed_candidate_types": list(ALLOWED_CANDIDATE_TYPES),
            "allowed_candidate_statuses": list(ALLOWED_CANDIDATE_STATUSES),
            "candidate_settings_must_be_not_applied": True,
            "required_fields": [
                "candidate_setting_id",
                "source_proposal_item_id",
                "candidate_type",
                "threshold_candidate",
                "smoothing_window_candidate",
                "hysteresis_candidate",
                "candidate_status",
                "not_applied",
                "evaluation_mode",
                "required_preconditions",
                "warnings",
            ],
        },
        "sandbox_evaluation_schema": {
            "allowed_evaluation_modes": list(ALLOWED_EVALUATION_MODES),
            "allowed_evaluation_statuses": list(ALLOWED_EVALUATION_STATUSES),
            "allowed_decision_support_statuses": list(ALLOWED_DECISION_SUPPORT_STATUSES),
            "allowed_drift_severities": list(ALLOWED_DRIFT_SEVERITIES),
            "required_fields": [
                "candidate_evaluation_id",
                "candidate_setting_id",
                "candidate_type",
                "evaluation_status",
                "evaluation_mode",
                "not_applied",
                "current_summary",
                "candidate_summary",
                "baseline_summary",
                "drift_detected",
                "breaking_drift_detected",
                "drift_items",
                "review_data_limitations",
                "human_review_required",
                "decision_support_status",
                "warnings",
            ],
        },
        "sandbox_report_schema": {
            "evaluation_report_type": (
                REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE
            ),
            "evaluation_report_version": (
                REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION
            ),
            "required_fields": [
                "evaluation_report_id",
                "evaluation_report_type",
                "evaluation_report_version",
                "generated_at",
                "source_evaluation_input_path",
                "model_asset_ref",
                "model_asset_sha256",
                "current_settings",
                "candidate_evaluations",
                "blocked_candidates",
                "baseline_comparison_summary",
                "review_coverage_summary",
                "warnings",
                "non_claims",
            ],
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_evaluation_input_shape": True,
            "validate_candidate_setting_shape": True,
            "validate_evaluation_report_shape": True,
            "validate_allowed_candidate_types": True,
            "validate_allowed_candidate_statuses": True,
            "validate_allowed_evaluation_modes": True,
            "validate_allowed_evaluation_statuses": True,
            "validate_allowed_decision_support_statuses": True,
            "validate_allowed_drift_severities": True,
            "validate_candidate_settings_are_not_applied": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_fields_and_values": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_accuracy": True,
            "does_not_auto_label_segments": True,
            "does_not_alter_thresholds": True,
            "does_not_alter_smoothing": True,
            "does_not_alter_hysteresis": True,
            "does_not_modify_existing_baselines": True,
            "does_not_modify_model_assets": True,
        },
        "provenance_requirements": {
            "source_calibration_proposal_path_recorded": True,
            "source_metrics_report_path_recorded_when_supplied": True,
            "source_review_loop_report_path_recorded_when_supplied": True,
            "source_review_bundle_path_recorded_when_supplied": True,
            "source_corpus_run_path_recorded_when_supplied": True,
            "source_regression_baseline_path_recorded_when_supplied": True,
            "model_asset_provenance_preserved": True,
            "current_gate_settings_recorded_as_read_only_context": True,
            "source_warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(SANDBOX_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _candidate_settings_from_proposal(
    *,
    proposal: dict[str, Any],
    review_metrics_summary: dict[str, Any],
    source_context: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        _candidate_setting_from_item(
            item=_dict(item),
            review_metrics_summary=review_metrics_summary,
            source_context=source_context,
        )
        for item in _list(proposal.get("proposal_items"))
    ]


def _candidate_setting_from_item(
    *,
    item: dict[str, Any],
    review_metrics_summary: dict[str, Any],
    source_context: dict[str, Any],
) -> dict[str, Any]:
    candidate = _dict(item.get("proposed_candidate_setting"))
    candidate_type = _candidate_type(candidate)
    candidate_status = _candidate_status(
        item=item,
        candidate_type=candidate_type,
        review_metrics_summary=review_metrics_summary,
        source_context=source_context,
    )
    payload = {
        "source_proposal_item_id": item.get("proposal_item_id"),
        "candidate_type": candidate_type,
        "threshold_candidate": (
            _float_or_none(candidate.get("candidate_value"))
            if candidate_type == "threshold_candidate"
            else None
        ),
        "smoothing_window_candidate": (
            _int_or_none(candidate.get("candidate_value"))
            if candidate_type == "smoothing_window_candidate"
            else None
        ),
        "hysteresis_candidate": (
            _dict(candidate.get("candidate_value"))
            if candidate_type == "hysteresis_candidate"
            else None
        ),
        "candidate_status": candidate_status,
        "not_applied": True,
        "evaluation_mode": _evaluation_mode_for_candidate(candidate_status),
        "required_preconditions": _list(item.get("required_preconditions")),
        "source_metric_group": item.get("source_metric_group"),
        "source_review_entry_refs": _list(item.get("source_review_entry_refs")),
        "source_segment_refs": _list(item.get("source_segment_refs")),
        "human_review_required": item.get("requires_human_review") is True,
        "writes_runtime_config": False,
        "mutates_model_assets": False,
        "replaces_regression_baseline": False,
        "warnings": dict(SANDBOX_WARNINGS),
    }
    return {
        "candidate_setting_id": _stable_id(
            "review_guided_gameplay_calibration_candidate_setting_v1",
            payload,
        ),
        **payload,
    }


def _candidate_type(candidate: dict[str, Any]) -> str:
    setting_type = _string_or_none(candidate.get("setting_type"))
    if setting_type in {
        "threshold_candidate",
        "smoothing_window_candidate",
        "hysteresis_candidate",
    }:
        return setting_type
    if setting_type == "combined_candidate":
        return "combined_candidate"
    if setting_type == "not_applicable":
        return "no_candidate"
    return "not_applicable"


def _candidate_status(
    *,
    item: dict[str, Any],
    candidate_type: str,
    review_metrics_summary: dict[str, Any],
    source_context: dict[str, Any],
) -> str:
    proposal_status = _string_or_none(item.get("proposal_status"))
    if candidate_type in {"no_candidate", "not_applicable"}:
        if proposal_status and proposal_status.startswith("blocked_"):
            return _blocked_status(proposal_status)
        return "informational_only"
    if proposal_status and proposal_status.startswith("blocked_"):
        return _blocked_status(proposal_status)
    if source_context.get("fixture_mode_used") is True:
        return "blocked_fixture_only_data"
    if _int(review_metrics_summary.get("unreviewed_entry_count")) > 0:
        return "blocked_no_human_review"
    if _int(review_metrics_summary.get("total_missing_review_field_count")) > 0:
        return "blocked_missing_review_data"
    if _int(review_metrics_summary.get("reviewed_entry_count")) <= 0:
        return "blocked_no_human_review"
    if proposal_status == "needs_additional_review":
        return "blocked_insufficient_sample_size"
    if proposal_status == "proposed_for_future_evaluation":
        return "ready_for_offline_evaluation"
    return "informational_only"


def _blocked_status(proposal_status: str) -> str:
    if proposal_status in ALLOWED_CANDIDATE_STATUSES:
        return proposal_status
    return "blocked_insufficient_sample_size"


def _evaluation_mode_for_candidate(candidate_status: str) -> str:
    if candidate_status == "ready_for_offline_evaluation":
        return "structural_offline_evaluation"
    if candidate_status == "blocked_fixture_only_data":
        return "fixture_only"
    if candidate_status.startswith("blocked_"):
        return "baseline_comparison_only"
    return "not_applicable"


def _candidate_evaluation(
    *,
    candidate: dict[str, Any],
    inputs: dict[str, Any],
    evaluation_mode: str,
) -> dict[str, Any]:
    candidate_status = _string_or_none(candidate.get("candidate_status"))
    current_summary = _dict(inputs.get("current_structural_summary"))
    baseline_summary = _dict(inputs.get("baseline_summary"))
    if candidate_status == "ready_for_offline_evaluation":
        candidate_summary = _simulate_candidate_summary(
            candidate=candidate,
            inputs=inputs,
        )
        drift_items = _drift_items(
            current_summary=current_summary,
            candidate_summary=candidate_summary,
            baseline_summary=baseline_summary,
        )
        evaluation_status = (
            "completed_with_warnings"
            if _requires_structural_warning(candidate)
            else "evaluated_offline"
        )
        decision_status = (
            "safe_for_future_manual_review"
            if not any(item.get("severity") == "breaking" for item in drift_items)
            else "unsafe_for_runtime_application"
        )
    elif candidate_status in {"informational_only", "not_applicable"}:
        candidate_summary = dict(current_summary)
        drift_items = []
        evaluation_status = "not_applicable"
        decision_status = "informational_only"
    else:
        candidate_summary = dict(current_summary)
        drift_items = []
        evaluation_status = _blocked_evaluation_status(candidate_status)
        decision_status = _blocked_decision_status(candidate_status)
    payload = {
        "candidate_setting_id": candidate.get("candidate_setting_id"),
        "candidate_type": candidate.get("candidate_type"),
        "evaluation_status": evaluation_status,
        "evaluation_mode": (
            evaluation_mode
            if candidate_status == "ready_for_offline_evaluation"
            else candidate.get("evaluation_mode")
        ),
        "not_applied": True,
        "current_summary": current_summary,
        "candidate_summary": candidate_summary,
        "baseline_summary": baseline_summary,
        "drift_detected": bool(drift_items),
        "breaking_drift_detected": any(
            item.get("severity") == "breaking" for item in drift_items
        ),
        "drift_items": drift_items,
        "review_data_limitations": _review_data_limitations(inputs, candidate),
        "human_review_required": candidate.get("human_review_required") is True,
        "decision_support_status": decision_status,
        "warnings": dict(SANDBOX_WARNINGS),
    }
    return {
        "candidate_evaluation_id": _stable_id(
            "review_guided_gameplay_calibration_candidate_evaluation_v1",
            payload,
        ),
        **payload,
    }


def _simulate_candidate_summary(
    *,
    candidate: dict[str, Any],
    inputs: dict[str, Any],
) -> dict[str, Any]:
    entries = _list(_dict(inputs.get("review_bundle_summary")).get("entries"))
    if not entries:
        return dict(_dict(inputs.get("current_structural_summary")))
    threshold = _float(candidate.get("threshold_candidate")) or _float(
        inputs.get("current_threshold")
    )
    hysteresis = _dict(candidate.get("hysteresis_candidate")) or _dict(
        inputs.get("current_hysteresis_settings")
    )
    exit_probability = _float(hysteresis.get("exit_gameplay_probability"))
    statuses = [
        _candidate_status_for_entry(entry, threshold, exit_probability)
        for entry in entries
    ]
    status_counts = dict(sorted(Counter(statuses).items()))
    gameplay_count = status_counts.get("gameplay_segment_candidate", 0)
    uncertain_count = status_counts.get("uncertain_segment", 0)
    non_gameplay_count = status_counts.get("non_gameplay_segment_candidate", 0)
    current_summary = _dict(inputs.get("current_structural_summary"))
    return {
        **current_summary,
        "entry_count": len(entries),
        "gameplay_segment_candidate_count": gameplay_count,
        "non_gameplay_segment_candidate_count": non_gameplay_count,
        "uncertain_segment_count": uncertain_count,
        "downstream_allowed_window_count": gameplay_count,
        "downstream_blocked_window_count": non_gameplay_count,
        "downstream_review_required_window_count": uncertain_count,
        "perception_execution_window_count": gameplay_count,
        "perception_skipped_window_count": non_gameplay_count,
        "review_dataset_entry_count": len(entries),
        "status_distribution": status_counts,
        "candidate_summary_is_structural_only": True,
        "classifier_correctness_not_assessed": True,
    }


def _candidate_status_for_entry(
    entry: Any,
    threshold: float,
    exit_probability: float,
) -> str:
    probability = _float(_dict(entry).get("gameplay_probability"))
    if probability >= threshold:
        return "gameplay_segment_candidate"
    if probability > exit_probability:
        return "uncertain_segment"
    return "non_gameplay_segment_candidate"


def _drift_items(
    *,
    current_summary: dict[str, Any],
    candidate_summary: dict[str, Any],
    baseline_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    items = []
    for field in DRIFT_SUMMARY_FIELDS:
        current_value = current_summary.get(field)
        candidate_value = candidate_summary.get(field)
        baseline_value = baseline_summary.get(field)
        if candidate_value == current_value and candidate_value == baseline_value:
            continue
        if candidate_value == current_value:
            continue
        items.append(
            {
                "field": field,
                "current_value": current_value,
                "candidate_value": candidate_value,
                "baseline_value": baseline_value,
                "severity": _drift_severity(field, current_value, candidate_value),
                "reason": "structural_drift_summary",
            }
        )
    return items


def _drift_severity(field: str, current_value: Any, candidate_value: Any) -> str:
    if field in {"status_distribution", "warning_categories"}:
        return "info"
    if current_value is None or candidate_value is None:
        return "warning"
    return "warning"


def _requires_structural_warning(candidate: dict[str, Any]) -> bool:
    return candidate.get("candidate_type") in {
        "smoothing_window_candidate",
        "hysteresis_candidate",
    }


def _blocked_evaluation_status(candidate_status: str | None) -> str:
    mapping = {
        "blocked_missing_review_data": "blocked_missing_review_data",
        "blocked_insufficient_sample_size": "blocked_insufficient_sample_size",
        "blocked_fixture_only_data": "blocked_fixture_only_data",
        "blocked_no_human_review": "blocked_no_human_review",
        "invalid_candidate": "blocked_invalid_candidate",
    }
    return mapping.get(str(candidate_status), "not_applicable")


def _blocked_decision_status(candidate_status: str | None) -> str:
    if candidate_status in {
        "blocked_missing_review_data",
        "blocked_no_human_review",
        "blocked_insufficient_sample_size",
    }:
        return "needs_more_human_review"
    if candidate_status == "blocked_fixture_only_data":
        return "insufficient_data"
    if candidate_status == "invalid_candidate":
        return "unsafe_for_runtime_application"
    return "not_applicable"


def _review_data_limitations(
    inputs: dict[str, Any],
    candidate: dict[str, Any],
) -> list[str]:
    limitations: list[str] = []
    review = _dict(inputs.get("review_metrics_summary"))
    source_context = _dict(inputs.get("source_context"))
    if _int(review.get("unreviewed_entry_count")) > 0:
        limitations.append("blocked_no_human_review")
    if _int(review.get("total_missing_review_field_count")) > 0:
        limitations.append("blocked_missing_review_data")
    if source_context.get("fixture_mode_used") is True:
        limitations.append("blocked_fixture_only_data")
    if candidate.get("candidate_type") in {
        "smoothing_window_candidate",
        "hysteresis_candidate",
    }:
        limitations.append("structural_offline_evaluation_requires_future_replay")
    return sorted(set(limitations))


def _baseline_comparison_summary(evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_evaluation_count": len(evaluations),
        "evaluated_offline_count": sum(
            1
            for evaluation in evaluations
            if evaluation.get("evaluation_status") == "evaluated_offline"
        ),
        "completed_with_warnings_count": sum(
            1
            for evaluation in evaluations
            if evaluation.get("evaluation_status") == "completed_with_warnings"
        ),
        "blocked_candidate_count": sum(
            1
            for evaluation in evaluations
            if str(evaluation.get("evaluation_status", "")).startswith("blocked_")
        ),
        "drift_detected_count": sum(
            1 for evaluation in evaluations if evaluation.get("drift_detected") is True
        ),
        "breaking_drift_detected_count": sum(
            1
            for evaluation in evaluations
            if evaluation.get("breaking_drift_detected") is True
        ),
        "threshold_changes_not_applied": True,
        "smoothing_changes_not_applied": True,
        "hysteresis_changes_not_applied": True,
        "runtime_config_not_updated": True,
        "baseline_not_replaced": True,
        "classifier_not_modified": True,
        "sandbox_is_not_truth": True,
        "sandbox_is_not_accuracy_scoring": True,
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if (
        contract.get("contract_type")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "sandbox_scope",
        "source_contract_refs",
        "evaluation_input_schema",
        "candidate_setting_schema",
        "sandbox_evaluation_schema",
        "sandbox_report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
        "non_claims",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    refs = _dict(contract.get("source_contract_refs"))
    for key, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(key) != expected:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _validate_evaluation_input_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if (
        inputs.get("evaluation_input_type")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_TYPE
    ):
        errors.append(
            _error(
                "invalid_evaluation_input_type",
                "evaluation_input_type",
                inputs.get("evaluation_input_type"),
            )
        )
    if (
        inputs.get("evaluation_input_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_evaluation_input_version",
                "evaluation_input_version",
                inputs.get("evaluation_input_version"),
            )
        )
    for field in (
        "evaluation_input_id",
        "generated_at",
        "source_calibration_proposal_path",
        "model_asset_ref",
        "model_asset_sha256",
        "current_threshold",
        "current_smoothing_window",
        "current_hysteresis_settings",
        "candidate_settings",
        "proposal_item_refs",
        "baseline_summary",
        "review_metrics_summary",
        "warnings",
        "non_claims",
    ):
        if field not in inputs:
            errors.append(_error("missing_evaluation_input_field", field, None))
    for candidate in _list(inputs.get("candidate_settings")):
        errors.extend(_validate_candidate_setting(_dict(candidate)))
    return errors


def _validate_candidate_setting(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for field in (
        "candidate_setting_id",
        "source_proposal_item_id",
        "candidate_type",
        "threshold_candidate",
        "smoothing_window_candidate",
        "hysteresis_candidate",
        "candidate_status",
        "not_applied",
        "evaluation_mode",
        "required_preconditions",
        "warnings",
    ):
        if field not in candidate:
            errors.append(_error("missing_candidate_setting_field", field, None))
    if candidate.get("candidate_type") not in ALLOWED_CANDIDATE_TYPES:
        errors.append(
            _error("unsupported_candidate_type", "candidate_type", candidate.get("candidate_type"))
        )
    if candidate.get("candidate_status") not in ALLOWED_CANDIDATE_STATUSES:
        errors.append(
            _error(
                "unsupported_candidate_status",
                "candidate_status",
                candidate.get("candidate_status"),
            )
        )
    if candidate.get("evaluation_mode") not in ALLOWED_EVALUATION_MODES:
        errors.append(
            _error(
                "unsupported_evaluation_mode",
                "evaluation_mode",
                candidate.get("evaluation_mode"),
            )
        )
    if candidate.get("not_applied") is not True:
        errors.append(
            _error(
                "candidate_setting_must_be_not_applied",
                "not_applied",
                candidate.get("not_applied"),
            )
        )
    if candidate.get("writes_runtime_config") is not False:
        errors.append(
            _error(
                "candidate_setting_must_not_write_runtime_config",
                "writes_runtime_config",
                candidate.get("writes_runtime_config"),
            )
        )
    if candidate.get("mutates_model_assets") is not False:
        errors.append(
            _error(
                "candidate_setting_must_not_mutate_model_assets",
                "mutates_model_assets",
                candidate.get("mutates_model_assets"),
            )
        )
    if candidate.get("replaces_regression_baseline") is not False:
        errors.append(
            _error(
                "candidate_setting_must_not_replace_baseline",
                "replaces_regression_baseline",
                candidate.get("replaces_regression_baseline"),
            )
        )
    return errors


def _validate_evaluation_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, path="evaluation_report")
    if (
        report.get("evaluation_report_type")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_TYPE
    ):
        errors.append(
            _error(
                "invalid_evaluation_report_type",
                "evaluation_report_type",
                report.get("evaluation_report_type"),
            )
        )
    if (
        report.get("evaluation_report_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_REPORT_VERSION
    ):
        errors.append(
            _error(
                "invalid_evaluation_report_version",
                "evaluation_report_version",
                report.get("evaluation_report_version"),
            )
        )
    for field in (
        "evaluation_report_id",
        "generated_at",
        "source_evaluation_input_path",
        "model_asset_ref",
        "model_asset_sha256",
        "current_settings",
        "candidate_evaluations",
        "blocked_candidates",
        "baseline_comparison_summary",
        "review_coverage_summary",
        "warnings",
        "non_claims",
    ):
        if field not in report:
            errors.append(_error("missing_evaluation_report_field", field, None))
    for evaluation in _list(report.get("candidate_evaluations")):
        errors.extend(_validate_candidate_evaluation(_dict(evaluation)))
    return errors


def _validate_candidate_evaluation(evaluation: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for field in (
        "candidate_evaluation_id",
        "candidate_setting_id",
        "candidate_type",
        "evaluation_status",
        "evaluation_mode",
        "not_applied",
        "current_summary",
        "candidate_summary",
        "baseline_summary",
        "drift_detected",
        "breaking_drift_detected",
        "drift_items",
        "review_data_limitations",
        "human_review_required",
        "decision_support_status",
        "warnings",
    ):
        if field not in evaluation:
            errors.append(_error("missing_candidate_evaluation_field", field, None))
    if evaluation.get("candidate_type") not in ALLOWED_CANDIDATE_TYPES:
        errors.append(
            _error(
                "unsupported_candidate_type",
                "candidate_type",
                evaluation.get("candidate_type"),
            )
        )
    if evaluation.get("evaluation_status") not in ALLOWED_EVALUATION_STATUSES:
        errors.append(
            _error(
                "unsupported_evaluation_status",
                "evaluation_status",
                evaluation.get("evaluation_status"),
            )
        )
    if evaluation.get("evaluation_mode") not in ALLOWED_EVALUATION_MODES:
        errors.append(
            _error(
                "unsupported_evaluation_mode",
                "evaluation_mode",
                evaluation.get("evaluation_mode"),
            )
        )
    if evaluation.get("decision_support_status") not in ALLOWED_DECISION_SUPPORT_STATUSES:
        errors.append(
            _error(
                "unsupported_decision_support_status",
                "decision_support_status",
                evaluation.get("decision_support_status"),
            )
        )
    if evaluation.get("not_applied") is not True:
        errors.append(
            _error(
                "candidate_evaluation_must_be_not_applied",
                "not_applied",
                evaluation.get("not_applied"),
            )
        )
    for item in _list(evaluation.get("drift_items")):
        severity = _dict(item).get("severity")
        if severity not in ALLOWED_DRIFT_SEVERITIES:
            errors.append(_error("unsupported_drift_severity", "drift_items.severity", severity))
    return errors


def _validate_source_contract_refs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    refs = _dict(payload.get("source_contract_refs"))
    errors = []
    for field, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(field) != expected:
            errors.append(_error("invalid_source_contract_ref", field, refs.get(field)))
    return errors


def _settings(
    *,
    proposal: dict[str, Any],
    regression_baseline: dict[str, Any],
    current_threshold: float,
    current_smoothing_window: int,
    hysteresis_enter: float,
    hysteresis_exit: float,
) -> dict[str, Any]:
    baseline_summary = _dict(regression_baseline.get("summary"))
    return {
        "threshold": proposal.get(
            "current_threshold",
            baseline_summary.get("threshold", current_threshold),
        ),
        "smoothing_window": proposal.get(
            "current_smoothing_window",
            baseline_summary.get("smoothing_window", current_smoothing_window),
        ),
        "hysteresis_settings": _dict(proposal.get("current_hysteresis_settings"))
        or _dict(baseline_summary.get("hysteresis_settings"))
        or {
            "enter_gameplay_probability": hysteresis_enter,
            "exit_gameplay_probability": hysteresis_exit,
        },
    }


def _current_settings_payload(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "threshold": inputs.get("current_threshold"),
        "smoothing_window": inputs.get("current_smoothing_window"),
        "hysteresis_settings": inputs.get("current_hysteresis_settings"),
        "read_only_context": True,
        "threshold_changes_not_applied": True,
        "smoothing_changes_not_applied": True,
        "hysteresis_changes_not_applied": True,
    }


def _baseline_summary(regression_baseline: dict[str, Any]) -> dict[str, Any]:
    summary = dict(_dict(regression_baseline.get("summary")))
    if not summary:
        return {
            "baseline_available": False,
            "baseline_is_not_truth": True,
        }
    summary["baseline_available"] = True
    summary["baseline_is_not_truth"] = True
    return summary


def _review_metrics_summary(
    proposal: dict[str, Any],
    metrics_report: dict[str, Any],
) -> dict[str, Any]:
    summary = dict(_dict(metrics_report.get("summary")))
    groups = _dict(metrics_report.get("metric_groups"))
    coverage = _dict(groups.get("review_coverage"))
    missing = _dict(groups.get("missing_review_fields"))
    proposal_summary = _dict(proposal.get("summary"))
    return {
        **summary,
        "review_bundle_entry_count": _int(coverage.get("review_bundle_entry_count")),
        "reviewed_entry_count": _int(coverage.get("reviewed_entry_count")),
        "unreviewed_entry_count": _int(coverage.get("unreviewed_entry_count")),
        "review_completion_rate": _float(coverage.get("review_completion_rate")),
        "review_pending_rate": _float(coverage.get("review_pending_rate")),
        "total_missing_review_field_count": _int(
            missing.get("total_missing_review_field_count")
        ),
        "proposal_item_count": _int(proposal_summary.get("proposal_item_count")),
        "blocked_item_count": _int(proposal_summary.get("blocked_item_count")),
        "review_metrics_are_operational_only": True,
        "classifier_correctness_not_assessed": True,
    }


def _source_context(
    *,
    proposal: dict[str, Any],
    corpus_run: dict[str, Any],
) -> dict[str, Any]:
    proposal_context = _dict(proposal.get("source_context"))
    entries = _list(corpus_run.get("entries"))
    return {
        **proposal_context,
        "source_corpus_run_supplied": bool(corpus_run),
        "corpus_run_mode": corpus_run.get("run_mode") or proposal_context.get("corpus_run_mode"),
        "fixture_only_entry_count": sum(
            1
            for entry in entries
            if _string_or_none(_dict(entry).get("run_mode")) == "fixture_only"
        ),
        "fixture_mode_used": _fixture_mode_used(corpus_run)
        or proposal_context.get("fixture_mode_used") is True,
    }


def _review_bundle_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "entry_count": len(entries),
        "entries": [
            {
                "review_entry_id": entry.get("review_entry_id"),
                "segment_id": entry.get("segment_id"),
                "gameplay_probability": entry.get("gameplay_probability"),
                "segment_status": entry.get("segment_status"),
                "routing_decision": entry.get("routing_decision"),
                "execution_decision": entry.get("execution_decision"),
            }
            for entry in entries
        ],
    }


def _current_structural_summary(
    *,
    baseline_summary: dict[str, Any],
    review_entries: list[dict[str, Any]],
) -> dict[str, Any]:
    if baseline_summary.get("baseline_available") is True:
        return dict(baseline_summary)
    status_counts = _count_by_field(review_entries, "segment_status")
    routing_counts = _count_by_field(review_entries, "routing_decision")
    execution_counts = _count_by_field(review_entries, "execution_decision")
    return {
        "entry_count": len(review_entries),
        "gameplay_segment_candidate_count": status_counts.get(
            "gameplay_segment_candidate",
            0,
        ),
        "non_gameplay_segment_candidate_count": status_counts.get(
            "non_gameplay_segment_candidate",
            0,
        ),
        "uncertain_segment_count": status_counts.get("uncertain_segment", 0),
        "downstream_allowed_window_count": routing_counts.get(
            "allow_downstream_observation",
            0,
        ),
        "downstream_blocked_window_count": routing_counts.get("skip_non_gameplay", 0),
        "downstream_review_required_window_count": routing_counts.get(
            "require_human_review",
            0,
        ),
        "perception_execution_window_count": execution_counts.get(
            "execute_on_gameplay_window",
            0,
        ),
        "perception_skipped_window_count": execution_counts.get(
            "skip_non_gameplay_window",
            0,
        ),
        "replay_timeline_entry_count": len(review_entries),
        "review_dataset_entry_count": len(review_entries),
        "status_distribution": status_counts,
        "warning_categories": [],
    }


def _model_asset_from_sources(
    *,
    proposal: dict[str, Any],
    metrics_report: dict[str, Any],
    review_bundle: dict[str, Any],
    review_loop_report: dict[str, Any],
    model_asset_path: str | Path,
) -> dict[str, Any]:
    for source in (proposal, metrics_report, review_bundle):
        if source.get("model_asset_ref"):
            return {
                "model_asset_ref": source.get("model_asset_ref"),
                "model_asset_sha256": source.get("model_asset_sha256"),
                "model_asset_exists": bool(source.get("model_asset_exists")),
            }
    report_model = _dict(review_loop_report.get("model_asset_provenance"))
    if report_model.get("model_asset_ref"):
        return {
            "model_asset_ref": report_model.get("model_asset_ref"),
            "model_asset_sha256": report_model.get("model_asset_sha256"),
            "model_asset_exists": bool(report_model.get("model_asset_exists")),
        }
    return _model_asset_ref(model_asset_path)


def _model_asset_ref(model_asset_path: str | Path) -> dict[str, Any]:
    path = Path(model_asset_path).expanduser()
    if not path.is_file():
        return {
            "model_asset_ref": str(model_asset_path),
            "model_asset_sha256": None,
            "model_asset_exists": False,
        }
    return {
        "model_asset_ref": str(model_asset_path),
        "model_asset_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "model_asset_exists": True,
    }


def _proposal_item_refs(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "proposal_item_id": _dict(item).get("proposal_item_id"),
            "proposal_type": _dict(item).get("proposal_type"),
            "proposal_status": _dict(item).get("proposal_status"),
        }
        for item in _list(proposal.get("proposal_items"))
    ]


def _warnings_from_sources(
    *,
    proposal: dict[str, Any],
    metrics_report: dict[str, Any],
    review_loop_report: dict[str, Any],
    review_bundle: dict[str, Any],
    corpus_run: dict[str, Any],
    regression_baseline: dict[str, Any],
) -> dict[str, Any]:
    return {
        **dict(SANDBOX_WARNINGS),
        **_dict(proposal.get("warnings")),
        **_dict(metrics_report.get("warnings")),
        **_dict(review_loop_report.get("warnings")),
        **_dict(review_bundle.get("warnings")),
        **_dict(corpus_run.get("warnings")),
        **_dict(regression_baseline.get("warnings")),
    }


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
        "validation_version": (
            REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_SANDBOX_CONTRACT_VERSION
        ),
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(SANDBOX_WARNINGS),
        "known_limitations": [
            "Validation checks structural shape, allowed values, source refs, "
            "candidate-setting not-applied semantics, and exact forbidden tokens.",
            "Validation does not infer review labels.",
            "Validation does not calculate classifier accuracy.",
            "Validation does not alter thresholds, smoothing, hysteresis, runtime config, "
            "baselines, or model assets.",
        ],
    }


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    return _load_required_json(
        contract_path,
        "review_guided_gameplay_calibration_evaluation_sandbox_contract",
        errors,
    )


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


def _load_optional_json(path: str | Path | None, label: str) -> dict[str, Any]:
    if path is None:
        return {}
    candidate = Path(path).expanduser()
    if not candidate.is_file():
        return {}
    result = _load_json(candidate, label=label)
    if result.get("ok") is False:
        return {}
    return _dict(result.get("data"))


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "status": "missing", "label": label, "path": str(path)}
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "status": "invalid_json",
            "label": label,
            "path": str(path),
            "message": str(exc),
        }
    if not isinstance(data, dict):
        return {"ok": False, "status": "not_object", "label": label, "path": str(path)}
    return {"ok": True, "status": "loaded", "label": label, "path": str(path), "data": data}


def _failed_result(
    *,
    status: str,
    errors: list[dict[str, Any]],
    output_path: str | Path | None,
    payload_type: str,
    result_key: str,
) -> dict[str, Any]:
    payload = {
        "payload_type": payload_type,
        "status": status,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(SANDBOX_WARNINGS),
    }
    result = {"ok": False, **payload}
    _write_json_if_requested(output_path, payload, result, result_key)
    return result


def _write_json_if_requested(
    output_path: str | Path | None,
    payload: dict[str, Any],
    result: dict[str, Any],
    result_key: str,
) -> None:
    if output_path is None:
        return
    path = Path(output_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result[result_key] = str(path)


def _forbidden_token_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    _collect_forbidden_token_errors(value=value, path=path, errors=errors)
    return errors


def _collect_forbidden_token_errors(
    *,
    value: Any,
    path: str,
    errors: list[dict[str, Any]],
) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_EVALUATION_SANDBOX_TOKENS:
                errors.append(_error("forbidden_field_or_value", f"{path}.{key_text}", key_text))
            _collect_forbidden_token_errors(
                value=nested,
                path=f"{path}.{key_text}",
                errors=errors,
            )
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _collect_forbidden_token_errors(
                value=nested,
                path=f"{path}[{index}]",
                errors=errors,
            )
    elif isinstance(value, str) and value in FORBIDDEN_EVALUATION_SANDBOX_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, value))


def _fixture_mode_used(corpus_run: dict[str, Any]) -> bool:
    if corpus_run.get("run_mode") == "fixture_only":
        return True
    if _dict(corpus_run.get("warnings")).get("fixture_mode_used") is True:
        return True
    return any(
        _dict(entry).get("run_mode") == "fixture_only"
        or _dict(entry).get("status") == "fixture_completed"
        for entry in _list(corpus_run.get("entries"))
    )


def _count_by_field(rows: list[Any], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(_dict(row).get(field)) for row in rows).items()))


def _stable_id(*parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "field": field, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "blueprint": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_BLUEPRINT,
        "blueprint_name": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EVALUATION_BLUEPRINT_NAME,
        "project_version": "0.0.0",
    }
