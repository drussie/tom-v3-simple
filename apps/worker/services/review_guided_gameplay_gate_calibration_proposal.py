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
from apps.worker.services.gameplay_gate_review_dataset_export import (
    DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT,
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
    REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION,
)
from apps.worker.services.real_broadcast_gameplay_review_metrics import (
    SOURCE_CONTRACT_REFS as REVIEW_METRICS_SOURCE_CONTRACT_REFS,
)

REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_TYPE = (
    "review_guided_gameplay_calibration_proposal_contract"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE = (
    "review_guided_gameplay_calibration_inputs"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE = (
    "review_guided_gameplay_calibration_proposal"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_TYPE = (
    "review_guided_gameplay_calibration_proposal_report"
)
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_VERSION = "v1"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_BLUEPRINT = "blueprint_49"
REVIEW_GUIDED_GAMEPLAY_CALIBRATION_BLUEPRINT_NAME = (
    "review_guided_gameplay_gate_calibration_proposal_v1"
)

DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT = (
    ".data/contracts/review_guided_gameplay_calibration_proposal_contract_v1.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_inputs.current.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_VALIDATION_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_inputs.validation.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_proposal.current.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VALIDATION_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_proposal.validation.json"
)
DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_OUTPUT = (
    ".data/exports/review_guided_gameplay_calibration_proposal_report.current.json"
)

REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

ALLOWED_PROPOSAL_TYPES = [
    "threshold_review_candidate",
    "smoothing_window_review_candidate",
    "hysteresis_review_candidate",
    "classifier_boundary_case_review",
    "ambiguity_cluster_review",
    "broadcast_replay_confusion_review",
    "commercial_or_graphic_confusion_review",
    "uncertain_segment_review",
    "missing_review_data_blocker",
    "human_review_batch_candidate",
    "no_calibration_action",
    "not_applicable",
]

ALLOWED_PROPOSAL_STATUSES = [
    "proposed_for_future_evaluation",
    "blocked_missing_review_data",
    "blocked_insufficient_sample_size",
    "blocked_fixture_only_data",
    "blocked_no_human_review",
    "needs_additional_review",
    "informational_only",
    "not_applicable",
]

ALLOWED_EVALUATION_ACTIONS = [
    "evaluate_threshold_candidate_later",
    "evaluate_smoothing_candidate_later",
    "evaluate_hysteresis_candidate_later",
    "collect_more_human_review",
    "inspect_boundary_segments",
    "inspect_ambiguity_cluster",
    "prepare_review_batch",
    "no_action",
    "not_applicable",
]

ALLOWED_RISK_FLAGS = [
    "human_review_required",
    "insufficient_review_coverage",
    "fixture_only_source",
    "missing_review_fields",
    "boundary_case_possible",
    "ambiguity_cluster_present",
    "broadcast_replay_possible",
    "commercial_or_graphic_possible",
    "threshold_candidate_not_applied",
    "smoothing_candidate_not_applied",
    "hysteresis_candidate_not_applied",
    "model_asset_not_modified",
    "regression_baseline_not_modified",
    "not_applicable",
]

FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS = {
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
}

CALIBRATION_WARNINGS = {
    "calibration_proposal_is_not_truth": True,
    "calibration_proposal_is_not_accuracy_scoring": True,
    "threshold_changes_not_applied": True,
    "smoothing_changes_not_applied": True,
    "hysteresis_changes_not_applied": True,
    "classifier_not_modified": True,
    "model_weights_not_modified": True,
    "automatic_relabeling_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "human_review_required": True,
    "classifier_correctness_not_assessed": True,
    "classifier_accuracy_not_assessed": True,
    "model_assets_are_not_mutated": True,
    "regression_baselines_are_not_mutated": True,
    "future_evaluation_proposals_only": True,
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
}

SOURCE_CONTRACT_REFS = {
    "real_broadcast_gameplay_review_metrics_contract_version": (
        REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION
    ),
    **dict(REVIEW_METRICS_SOURCE_CONTRACT_REFS),
}


def export_review_guided_gameplay_calibration_proposal_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or REVIEW_GUIDED_GAMEPLAY_CALIBRATION_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_TYPE,
        "contract_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION,
        "calibration_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE,
        "calibration_proposal_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
        "contract": contract,
        "warnings": dict(CALIBRATION_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_review_guided_gameplay_calibration_inputs(
    *,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT
    ),
    source_metrics_report_path: str | Path = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT
    ),
    source_review_loop_report_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT
    ),
    source_review_bundle_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT
    ),
    source_review_dataset_path: str | Path | None = DEFAULT_GAMEPLAY_GATE_REVIEW_DATASET_OUTPUT,
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
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    metrics_report = _load_required_json(
        source_metrics_report_path,
        "real_broadcast_gameplay_review_metrics_report",
        errors,
    )
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if errors:
        return _failed_result(
            status="invalid_calibration_input_sources",
            errors=errors,
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE,
            result_key="calibration_inputs_output",
        )

    review_loop_report = _load_optional_json(
        source_review_loop_report_path,
        "real_broadcast_gameplay_review_loop_report",
    )
    review_bundle = _load_optional_json(
        source_review_bundle_path,
        "real_broadcast_gameplay_review_bundle",
    )
    review_dataset = _load_optional_json(
        source_review_dataset_path,
        "gameplay_gate_review_dataset",
    )
    corpus_run = _load_optional_json(
        source_corpus_run_path,
        "real_broadcast_gameplay_corpus_run",
    )
    regression_baseline = _load_optional_json(
        source_regression_baseline_path,
        "gameplay_gate_regression_baseline",
    )

    entries = [entry for entry in _list(review_bundle.get("entries")) if isinstance(entry, dict)]
    groups = _dict(metrics_report.get("metric_groups"))
    settings = _settings(
        current_threshold=current_threshold,
        current_smoothing_window=current_smoothing_window,
        hysteresis_enter=hysteresis_enter,
        hysteresis_exit=hysteresis_exit,
        regression_baseline=regression_baseline,
    )
    model_asset = _model_asset_from_sources(
        metrics_report=metrics_report,
        review_bundle=review_bundle,
        review_loop_report=review_loop_report,
        model_asset_path=model_asset_path,
    )
    calibration_input = {
        "calibration_input_id": _stable_id(
            "review_guided_gameplay_calibration_inputs_v1",
            str(source_metrics_report_path),
            groups,
            settings,
        ),
        "calibration_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE,
        "calibration_input_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_metrics_report_path": str(Path(source_metrics_report_path)),
        "source_review_loop_report_path": (
            str(Path(source_review_loop_report_path))
            if source_review_loop_report_path
            else None
        ),
        "source_review_bundle_path": (
            str(Path(source_review_bundle_path)) if source_review_bundle_path else None
        ),
        "source_review_dataset_path": (
            str(Path(source_review_dataset_path)) if source_review_dataset_path else None
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
        "current_threshold": settings["current_threshold"],
        "current_smoothing_window": settings["current_smoothing_window"],
        "current_hysteresis_settings": settings["current_hysteresis_settings"],
        "review_metrics_summary": _review_metrics_summary(groups, metrics_report),
        "ambiguity_summary": _ambiguity_summary(groups, entries),
        "boundary_case_summary": _boundary_case_summary(groups, entries),
        "missing_review_summary": _missing_review_summary(groups),
        "source_context": _source_context(
            review_dataset=review_dataset,
            corpus_run=corpus_run,
            regression_baseline=regression_baseline,
        ),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _warnings_from_sources(
            metrics_report=metrics_report,
            review_loop_report=review_loop_report,
            review_bundle=review_bundle,
            corpus_run=corpus_run,
        ),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": True,
        "status": "completed",
        "calibration_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE,
        "calibration_input_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION,
        "calibration_input_id": calibration_input["calibration_input_id"],
        "summary": calibration_input["review_metrics_summary"],
        "calibration_inputs": calibration_input,
        "warnings": calibration_input["warnings"],
    }
    _write_json_if_requested(
        output_path,
        calibration_input,
        result,
        "calibration_inputs_output",
    )
    return result


def validate_review_guided_gameplay_calibration_inputs(
    *,
    calibration_inputs_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    inputs = _load_required_json(calibration_inputs_path, "calibration_inputs", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if inputs:
        errors.extend(_validate_calibration_input_shape(inputs))
        errors.extend(_validate_source_contract_refs(inputs))
        errors.extend(_forbidden_token_errors(inputs, path="calibration_inputs"))
    result = _validation_result(
        ok=not errors,
        validation_type="review_guided_gameplay_calibration_inputs_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=calibration_inputs_path,
        payload_type=inputs.get("calibration_input_type") if inputs else None,
        payload_version=inputs.get("calibration_input_version") if inputs else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_review_guided_gameplay_calibration_proposal(
    *,
    calibration_inputs_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUTS_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_review_guided_gameplay_calibration_inputs(
        calibration_inputs_path=calibration_inputs_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_calibration_inputs",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
            result_key="calibration_proposal_output",
        )

    inputs = _load_optional_json(calibration_inputs_path, "calibration_inputs")
    proposal_items = _proposal_items(inputs)
    blocked_items = [
        item
        for item in proposal_items
        if str(item.get("proposal_status", "")).startswith("blocked_")
    ]
    proposal = {
        "proposal_id": _stable_id(
            "review_guided_gameplay_calibration_proposal_v1",
            str(calibration_inputs_path),
            proposal_items,
        ),
        "proposal_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
        "proposal_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_calibration_input_path": str(Path(calibration_inputs_path)),
        "model_asset_ref": inputs.get("model_asset_ref"),
        "model_asset_sha256": inputs.get("model_asset_sha256"),
        "model_asset_exists": inputs.get("model_asset_exists"),
        "current_threshold": inputs.get("current_threshold"),
        "current_smoothing_window": inputs.get("current_smoothing_window"),
        "current_hysteresis_settings": inputs.get("current_hysteresis_settings"),
        "proposal_items": proposal_items,
        "blocked_items": blocked_items,
        "summary": _proposal_summary(proposal_items, blocked_items),
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _dict(inputs.get("warnings")) or dict(CALIBRATION_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    proposal["summary"]["threshold_changes_not_applied"] = True
    proposal["summary"]["smoothing_changes_not_applied"] = True
    proposal["summary"]["hysteresis_changes_not_applied"] = True
    proposal["summary"]["classifier_not_modified"] = True
    proposal_errors = _validate_calibration_proposal_shape(proposal)
    if proposal_errors:
        return _failed_result(
            status="invalid_calibration_proposal",
            errors=proposal_errors,
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
            result_key="calibration_proposal_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "proposal_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
        "proposal_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VERSION,
        "proposal_id": proposal["proposal_id"],
        "proposal_item_count": len(proposal_items),
        "blocked_item_count": len(blocked_items),
        "proposal": proposal,
        "warnings": proposal["warnings"],
    }
    _write_json_if_requested(
        output_path,
        proposal,
        result,
        "calibration_proposal_output",
    )
    return result


def validate_review_guided_gameplay_calibration_proposal(
    *,
    calibration_proposal_path: str | Path,
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    proposal = _load_required_json(calibration_proposal_path, "calibration_proposal", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if proposal:
        errors.extend(_validate_calibration_proposal_shape(proposal))
        errors.extend(_validate_source_contract_refs(proposal))
        errors.extend(_forbidden_token_errors(proposal, path="calibration_proposal"))
    result = _validation_result(
        ok=not errors,
        validation_type="review_guided_gameplay_calibration_proposal_validation",
        validated_at=validated_at,
        contract_path=contract_path,
        payload_path=calibration_proposal_path,
        payload_type=proposal.get("proposal_type") if proposal else None,
        payload_version=proposal.get("proposal_version") if proposal else None,
        errors=errors,
    )
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_review_guided_gameplay_calibration_proposal_report(
    *,
    calibration_proposal_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_OUTPUT
    ),
    contract_path: str | Path = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = (
        DEFAULT_REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_review_guided_gameplay_calibration_proposal(
        calibration_proposal_path=calibration_proposal_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_calibration_proposal",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_TYPE,
            result_key="calibration_proposal_report_output",
        )
    proposal = _load_optional_json(calibration_proposal_path, "calibration_proposal")
    report = {
        "report_id": _stable_id(
            "review_guided_gameplay_calibration_proposal_report_v1",
            str(calibration_proposal_path),
            proposal.get("summary"),
        ),
        "report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_TYPE,
        "report_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_calibration_proposal_path": str(Path(calibration_proposal_path)),
        "proposal_id": proposal.get("proposal_id"),
        "proposal_summary": _dict(proposal.get("summary")),
        "proposal_type_counts": _count_by_field(
            _list(proposal.get("proposal_items")),
            "proposal_type",
        ),
        "proposal_status_counts": _count_by_field(
            _list(proposal.get("proposal_items")),
            "proposal_status",
        ),
        "blocked_item_count": len(_list(proposal.get("blocked_items"))),
        "validation_snapshot": validation,
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _dict(proposal.get("warnings")) or dict(CALIBRATION_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": True,
        "status": "completed",
        "report_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_TYPE,
        "report_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_REPORT_VERSION,
        "report_id": report["report_id"],
        "summary": report["proposal_summary"],
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(
        output_path,
        report,
        result,
        "calibration_proposal_report_output",
    )
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_TYPE,
        "contract_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "proposal_scope": {
            "purpose": "review_guided_gameplay_gate_calibration_proposal",
            "reads_review_metrics_when_supplied": True,
            "reads_review_loop_when_supplied": True,
            "reads_review_bundle_when_supplied": True,
            "builds_calibration_inputs": True,
            "builds_future_evaluation_proposals": True,
            "applies_threshold_changes": False,
            "applies_smoothing_changes": False,
            "applies_hysteresis_changes": False,
            "updates_model": False,
            "trains_classifier": False,
            "calculates_classifier_accuracy": False,
            "creates_review_labels": False,
            "mutates_regression_baselines": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "calibration_input_schema": {
            "calibration_input_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE,
            "calibration_input_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION,
            "required_fields": [
                "calibration_input_id",
                "calibration_input_type",
                "calibration_input_version",
                "generated_at",
                "source_metrics_report_path",
                "source_review_loop_report_path",
                "source_review_bundle_path",
                "source_review_dataset_path",
                "source_corpus_run_path",
                "source_regression_baseline_path",
                "model_asset_ref",
                "model_asset_sha256",
                "current_threshold",
                "current_smoothing_window",
                "current_hysteresis_settings",
                "review_metrics_summary",
                "ambiguity_summary",
                "boundary_case_summary",
                "missing_review_summary",
                "source_context",
                "source_contract_refs",
                "warnings",
                "non_claims",
                "tom_provenance",
            ],
        },
        "calibration_proposal_schema": {
            "proposal_type": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE,
            "proposal_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VERSION,
            "required_fields": [
                "proposal_id",
                "proposal_type",
                "proposal_version",
                "generated_at",
                "source_calibration_input_path",
                "model_asset_ref",
                "model_asset_sha256",
                "current_threshold",
                "current_smoothing_window",
                "current_hysteresis_settings",
                "proposal_items",
                "blocked_items",
                "summary",
                "source_contract_refs",
                "warnings",
                "non_claims",
                "tom_provenance",
            ],
        },
        "proposal_item_schema": {
            "allowed_proposal_types": list(ALLOWED_PROPOSAL_TYPES),
            "allowed_proposal_statuses": list(ALLOWED_PROPOSAL_STATUSES),
            "allowed_proposed_evaluation_actions": list(ALLOWED_EVALUATION_ACTIONS),
            "allowed_risk_flags": list(ALLOWED_RISK_FLAGS),
            "candidate_settings_are_future_evaluation_only": True,
            "candidate_settings_must_be_not_applied": True,
            "required_fields": [
                "proposal_item_id",
                "proposal_type",
                "proposal_status",
                "source_metric_group",
                "source_review_entry_refs",
                "source_segment_refs",
                "observed_review_pattern",
                "proposed_evaluation_action",
                "proposed_candidate_setting",
                "requires_human_review",
                "required_preconditions",
                "risk_flags",
                "provenance_status",
                "warnings",
            ],
        },
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_calibration_input_shape": True,
            "validate_calibration_proposal_shape": True,
            "validate_allowed_proposal_types": True,
            "validate_allowed_statuses": True,
            "validate_allowed_evaluation_actions": True,
            "validate_allowed_risk_flags": True,
            "validate_candidate_settings_are_not_applied": True,
            "validate_candidate_settings_are_future_evaluation_only": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_fields_and_values": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_accuracy": True,
            "does_not_auto_label_segments": True,
            "does_not_alter_thresholds": True,
            "does_not_alter_smoothing": True,
            "does_not_alter_hysteresis": True,
            "does_not_modify_regression_baselines": True,
            "does_not_modify_model_assets": True,
        },
        "provenance_requirements": {
            "source_metrics_report_path_recorded": True,
            "source_review_loop_report_path_recorded_when_supplied": True,
            "source_review_bundle_path_recorded_when_supplied": True,
            "source_review_dataset_path_recorded_when_supplied": True,
            "source_corpus_run_path_recorded_when_supplied": True,
            "source_regression_baseline_path_recorded_when_supplied": True,
            "model_asset_provenance_preserved": True,
            "current_gate_settings_recorded_as_read_only_context": True,
            "source_warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(CALIBRATION_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _settings(
    *,
    current_threshold: float,
    current_smoothing_window: int,
    hysteresis_enter: float,
    hysteresis_exit: float,
    regression_baseline: dict[str, Any],
) -> dict[str, Any]:
    baseline_summary = _dict(regression_baseline.get("summary"))
    return {
        "current_threshold": baseline_summary.get("threshold", current_threshold),
        "current_smoothing_window": baseline_summary.get(
            "smoothing_window",
            current_smoothing_window,
        ),
        "current_hysteresis_settings": _dict(
            baseline_summary.get("hysteresis_settings")
        )
        or {
            "enter_gameplay_probability": hysteresis_enter,
            "exit_gameplay_probability": hysteresis_exit,
        },
    }


def _review_metrics_summary(
    groups: dict[str, Any],
    metrics_report: dict[str, Any],
) -> dict[str, Any]:
    coverage = _dict(groups.get("review_coverage"))
    segment = _dict(groups.get("segment_status_distribution"))
    downstream = _dict(groups.get("downstream_gate_review_distribution"))
    next_actions = _dict(groups.get("next_review_actions"))
    return {
        "metrics_report_id": metrics_report.get("metrics_report_id"),
        "review_bundle_entry_count": _int(coverage.get("review_bundle_entry_count")),
        "reviewed_entry_count": _int(coverage.get("reviewed_entry_count")),
        "unreviewed_entry_count": _int(coverage.get("unreviewed_entry_count")),
        "needs_additional_review_count": _int(
            coverage.get("needs_additional_review_count")
        ),
        "review_completion_rate": _float(coverage.get("review_completion_rate")),
        "review_pending_rate": _float(coverage.get("review_pending_rate")),
        "reviewed_as_uncertain_count": _int(
            segment.get("reviewed_as_uncertain_count")
        ),
        "downstream_allow_review_count": _int(
            downstream.get("reviewer_would_allow_downstream_observation_count")
        ),
        "downstream_block_review_count": _int(
            downstream.get("reviewer_would_block_downstream_observation_count")
        ),
        "boundary_case_candidate_count": _int(
            next_actions.get("inspect_classifier_boundary_cases_count")
        ),
        "review_metrics_are_operational_only": True,
        "classifier_correctness_not_assessed": True,
    }


def _ambiguity_summary(
    groups: dict[str, Any],
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    ambiguity = _dict(groups.get("ambiguity_flag_distribution"))
    non_zero = {
        key: value
        for key, value in sorted(ambiguity.items())
        if key.endswith("_count") and _int(value) > 0
    }
    return {
        "ambiguity_flag_counts": non_zero,
        "high_ambiguity_entry_count": _int(
            _dict(groups.get("next_review_actions")).get(
                "review_high_ambiguity_entries_count"
            )
        ),
        "classifier_boundary_unclear_count": _int(
            ambiguity.get("classifier_boundary_unclear_count")
        ),
        "broadcast_replay_possible_count": _int(
            ambiguity.get("broadcast_replay_possible_count")
        ),
        "commercial_or_graphic_possible_count": _int(
            ambiguity.get("commercial_or_graphic_possible_count")
        ),
        "source_review_entry_refs": _entry_refs(
            entries,
            lambda entry: bool(
                _string_list(_dict(entry.get("human_review")).get("ambiguity_flags"))
            ),
        ),
        "ambiguity_summary_is_not_truth": True,
    }


def _boundary_case_summary(
    groups: dict[str, Any],
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    next_actions = _dict(groups.get("next_review_actions"))
    return {
        "classifier_boundary_case_count": _int(
            next_actions.get("inspect_classifier_boundary_cases_count")
        ),
        "uncertain_segment_count": _int(
            next_actions.get("review_uncertain_segments_count")
        ),
        "source_review_entry_refs": _entry_refs(
            entries,
            lambda entry: _is_boundary_or_uncertain_entry(entry),
        ),
        "boundary_case_summary_is_not_accuracy_scoring": True,
    }


def _missing_review_summary(groups: dict[str, Any]) -> dict[str, Any]:
    missing = _dict(groups.get("missing_review_fields"))
    coverage = _dict(groups.get("review_coverage"))
    return {
        "total_missing_review_field_count": _int(
            missing.get("total_missing_review_field_count")
        ),
        "missing_reviewer_id_count": _int(missing.get("missing_reviewer_id_count")),
        "missing_reviewed_at_count": _int(missing.get("missing_reviewed_at_count")),
        "missing_review_notes_count": _int(missing.get("missing_review_notes_count")),
        "unreviewed_entry_count": _int(coverage.get("unreviewed_entry_count")),
        "human_review_required_count": _int(coverage.get("review_required_count")),
        "missing_review_data_blocks_calibration": _int(
            missing.get("total_missing_review_field_count")
        )
        > 0
        or _int(coverage.get("unreviewed_entry_count")) > 0,
    }


def _source_context(
    *,
    review_dataset: dict[str, Any],
    corpus_run: dict[str, Any],
    regression_baseline: dict[str, Any],
) -> dict[str, Any]:
    entries = _list(corpus_run.get("entries"))
    return {
        "source_review_dataset_supplied": bool(review_dataset),
        "source_corpus_run_supplied": bool(corpus_run),
        "source_regression_baseline_supplied": bool(regression_baseline),
        "corpus_run_mode": corpus_run.get("run_mode"),
        "corpus_run_status": corpus_run.get("status") or corpus_run.get("report_type"),
        "fixture_only_entry_count": sum(
            1
            for entry in entries
            if _string_or_none(_dict(entry).get("run_mode")) == "fixture_only"
        ),
        "fixture_mode_used": _fixture_mode_used(corpus_run),
    }


def _proposal_items(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    review_summary = _dict(inputs.get("review_metrics_summary"))
    ambiguity = _dict(inputs.get("ambiguity_summary"))
    boundary = _dict(inputs.get("boundary_case_summary"))
    missing = _dict(inputs.get("missing_review_summary"))
    source_context = _dict(inputs.get("source_context"))
    current_threshold = _float(inputs.get("current_threshold"))
    current_smoothing = _int(inputs.get("current_smoothing_window"))
    current_hysteresis = _dict(inputs.get("current_hysteresis_settings"))

    if _int(missing.get("total_missing_review_field_count")) > 0:
        items.append(
            _proposal_item(
                proposal_type="missing_review_data_blocker",
                proposal_status="blocked_missing_review_data",
                source_metric_group="missing_review_fields",
                source_review_entry_refs=[],
                source_segment_refs=[],
                observed_review_pattern="missing_human_review_metadata",
                proposed_evaluation_action="collect_more_human_review",
                proposed_candidate_setting=_candidate_setting("not_applicable", None),
                requires_human_review=True,
                required_preconditions=[
                    "complete_required_human_review_fields",
                    "rebuild_review_metrics_report",
                ],
                risk_flags=[
                    "human_review_required",
                    "missing_review_fields",
                    "insufficient_review_coverage",
                ],
            )
        )

    if _int(review_summary.get("unreviewed_entry_count")) > 0:
        items.append(
            _proposal_item(
                proposal_type="human_review_batch_candidate",
                proposal_status="blocked_no_human_review",
                source_metric_group="review_coverage",
                source_review_entry_refs=[],
                source_segment_refs=[],
                observed_review_pattern="unreviewed_entries_present",
                proposed_evaluation_action="prepare_review_batch",
                proposed_candidate_setting=_candidate_setting("not_applicable", None),
                requires_human_review=True,
                required_preconditions=[
                    "complete_human_review_batch",
                    "rebuild_review_loop_report",
                ],
                risk_flags=["human_review_required", "insufficient_review_coverage"],
            )
        )

    if _int(boundary.get("classifier_boundary_case_count")) > 0:
        refs = _list(boundary.get("source_review_entry_refs"))
        items.append(
            _proposal_item(
                proposal_type="threshold_review_candidate",
                proposal_status="proposed_for_future_evaluation",
                source_metric_group="next_review_actions",
                source_review_entry_refs=refs,
                source_segment_refs=_segment_refs(refs),
                observed_review_pattern="classifier_boundary_case_review",
                proposed_evaluation_action="evaluate_threshold_candidate_later",
                proposed_candidate_setting=_candidate_setting(
                    "threshold_candidate",
                    current_threshold,
                ),
                requires_human_review=True,
                required_preconditions=[
                    "complete_human_review_for_boundary_cases",
                    "run_offline_calibration_evaluation",
                ],
                risk_flags=[
                    "human_review_required",
                    "boundary_case_possible",
                    "threshold_candidate_not_applied",
                ],
            )
        )

    if _int(boundary.get("uncertain_segment_count")) > 0:
        refs = _list(boundary.get("source_review_entry_refs"))
        items.append(
            _proposal_item(
                proposal_type="smoothing_window_review_candidate",
                proposal_status="needs_additional_review",
                source_metric_group="next_review_actions",
                source_review_entry_refs=refs,
                source_segment_refs=_segment_refs(refs),
                observed_review_pattern="uncertain_segment_review",
                proposed_evaluation_action="evaluate_smoothing_candidate_later",
                proposed_candidate_setting=_candidate_setting(
                    "smoothing_window_candidate",
                    max(1, current_smoothing),
                ),
                requires_human_review=True,
                required_preconditions=[
                    "review_uncertain_segments",
                    "compare_future_offline_smoothing_candidates",
                ],
                risk_flags=[
                    "human_review_required",
                    "boundary_case_possible",
                    "smoothing_candidate_not_applied",
                ],
            )
        )

    if _int(ambiguity.get("high_ambiguity_entry_count")) > 0:
        refs = _list(ambiguity.get("source_review_entry_refs"))
        items.append(
            _proposal_item(
                proposal_type="ambiguity_cluster_review",
                proposal_status="needs_additional_review",
                source_metric_group="ambiguity_flag_distribution",
                source_review_entry_refs=refs,
                source_segment_refs=_segment_refs(refs),
                observed_review_pattern="ambiguity_cluster_review",
                proposed_evaluation_action="inspect_ambiguity_cluster",
                proposed_candidate_setting=_candidate_setting("not_applicable", None),
                requires_human_review=True,
                required_preconditions=["inspect_ambiguity_cluster"],
                risk_flags=["human_review_required", "ambiguity_cluster_present"],
            )
        )

    if _int(ambiguity.get("broadcast_replay_possible_count")) > 0:
        refs = _list(ambiguity.get("source_review_entry_refs"))
        items.append(
            _proposal_item(
                proposal_type="broadcast_replay_confusion_review",
                proposal_status="proposed_for_future_evaluation",
                source_metric_group="ambiguity_flag_distribution",
                source_review_entry_refs=refs,
                source_segment_refs=_segment_refs(refs),
                observed_review_pattern="broadcast_replay_confusion_review",
                proposed_evaluation_action="evaluate_hysteresis_candidate_later",
                proposed_candidate_setting=_candidate_setting(
                    "hysteresis_candidate",
                    current_hysteresis,
                ),
                requires_human_review=True,
                required_preconditions=["review_broadcast_replay_possible_segments"],
                risk_flags=[
                    "human_review_required",
                    "broadcast_replay_possible",
                    "hysteresis_candidate_not_applied",
                ],
            )
        )

    if _int(ambiguity.get("commercial_or_graphic_possible_count")) > 0:
        refs = _list(ambiguity.get("source_review_entry_refs"))
        items.append(
            _proposal_item(
                proposal_type="commercial_or_graphic_confusion_review",
                proposal_status="proposed_for_future_evaluation",
                source_metric_group="ambiguity_flag_distribution",
                source_review_entry_refs=refs,
                source_segment_refs=_segment_refs(refs),
                observed_review_pattern="commercial_or_graphic_confusion_review",
                proposed_evaluation_action="inspect_ambiguity_cluster",
                proposed_candidate_setting=_candidate_setting("not_applicable", None),
                requires_human_review=True,
                required_preconditions=["review_commercial_or_graphic_possible_segments"],
                risk_flags=[
                    "human_review_required",
                    "commercial_or_graphic_possible",
                ],
            )
        )

    if source_context.get("fixture_mode_used") is True:
        items.append(
            _proposal_item(
                proposal_type="no_calibration_action",
                proposal_status="blocked_fixture_only_data",
                source_metric_group="source_context",
                source_review_entry_refs=[],
                source_segment_refs=[],
                observed_review_pattern="fixture_only_source_context",
                proposed_evaluation_action="no_action",
                proposed_candidate_setting=_candidate_setting("not_applicable", None),
                requires_human_review=True,
                required_preconditions=[
                    "use_explicit_real_broadcast_review_data_before_calibration_evaluation"
                ],
                risk_flags=["fixture_only_source", "human_review_required"],
            )
        )

    if not items:
        items.append(
            _proposal_item(
                proposal_type="no_calibration_action",
                proposal_status="informational_only",
                source_metric_group="review_metrics_summary",
                source_review_entry_refs=[],
                source_segment_refs=[],
                observed_review_pattern="no_structural_calibration_signal",
                proposed_evaluation_action="no_action",
                proposed_candidate_setting=_candidate_setting("not_applicable", None),
                requires_human_review=False,
                required_preconditions=[],
                risk_flags=["not_applicable"],
            )
        )
    return items


def _proposal_item(
    *,
    proposal_type: str,
    proposal_status: str,
    source_metric_group: str,
    source_review_entry_refs: list[Any],
    source_segment_refs: list[Any],
    observed_review_pattern: str,
    proposed_evaluation_action: str,
    proposed_candidate_setting: dict[str, Any],
    requires_human_review: bool,
    required_preconditions: list[str],
    risk_flags: list[str],
) -> dict[str, Any]:
    payload = {
        "proposal_type": proposal_type,
        "proposal_status": proposal_status,
        "source_metric_group": source_metric_group,
        "source_review_entry_refs": source_review_entry_refs,
        "source_segment_refs": source_segment_refs,
        "observed_review_pattern": observed_review_pattern,
        "proposed_evaluation_action": proposed_evaluation_action,
        "proposed_candidate_setting": proposed_candidate_setting,
        "requires_human_review": requires_human_review,
        "required_preconditions": required_preconditions,
        "risk_flags": sorted(set(risk_flags)),
        "provenance_status": "derived_from_review_operations_metrics",
        "warnings": dict(CALIBRATION_WARNINGS),
    }
    return {"proposal_item_id": _stable_id("proposal_item", payload), **payload}


def _candidate_setting(setting_type: str, value: Any) -> dict[str, Any]:
    return {
        "setting_type": setting_type,
        "candidate_value": value,
        "not_applied": True,
        "writes_runtime_config": False,
        "affects_regression_baselines": False,
        "future_evaluation_only": True,
    }


def _proposal_summary(
    proposal_items: list[dict[str, Any]],
    blocked_items: list[dict[str, Any]],
) -> dict[str, Any]:
    type_counts = _count_by_field(proposal_items, "proposal_type")
    status_counts = _count_by_field(proposal_items, "proposal_status")
    return {
        "proposal_item_count": len(proposal_items),
        "blocked_item_count": len(blocked_items),
        "proposal_type_counts": type_counts,
        "proposal_status_counts": status_counts,
        "future_evaluation_candidate_count": sum(
            1
            for item in proposal_items
            if item.get("proposal_status") == "proposed_for_future_evaluation"
        ),
        "no_runtime_changes_applied": True,
        "candidate_settings_not_applied": all(
            _dict(item.get("proposed_candidate_setting")).get("not_applied") is True
            for item in proposal_items
        ),
        "calibration_proposal_is_not_truth": True,
        "calibration_proposal_is_not_accuracy_scoring": True,
    }


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if (
        contract.get("contract_type")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_TYPE
    ):
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "proposal_scope",
        "source_contract_refs",
        "calibration_input_schema",
        "calibration_proposal_schema",
        "proposal_item_schema",
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


def _validate_calibration_input_shape(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if inputs.get("calibration_input_type") != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_TYPE:
        errors.append(
            _error(
                "invalid_calibration_input_type",
                "calibration_input_type",
                inputs.get("calibration_input_type"),
            )
        )
    if (
        inputs.get("calibration_input_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_INPUT_VERSION
    ):
        errors.append(
            _error(
                "invalid_calibration_input_version",
                "calibration_input_version",
                inputs.get("calibration_input_version"),
            )
        )
    for field in (
        "calibration_input_id",
        "generated_at",
        "source_metrics_report_path",
        "model_asset_ref",
        "model_asset_sha256",
        "current_threshold",
        "current_smoothing_window",
        "current_hysteresis_settings",
        "review_metrics_summary",
        "ambiguity_summary",
        "boundary_case_summary",
        "missing_review_summary",
        "source_context",
        "source_contract_refs",
        "warnings",
        "non_claims",
        "tom_provenance",
    ):
        if field not in inputs:
            errors.append(_error("missing_calibration_input_field", field, None))
    return errors


def _validate_calibration_proposal_shape(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(proposal, path="calibration_proposal")
    if proposal.get("proposal_type") != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_TYPE:
        errors.append(
            _error(
                "invalid_proposal_type",
                "proposal_type",
                proposal.get("proposal_type"),
            )
        )
    if (
        proposal.get("proposal_version")
        != REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_VERSION
    ):
        errors.append(
            _error(
                "invalid_proposal_version",
                "proposal_version",
                proposal.get("proposal_version"),
            )
        )
    for field in (
        "proposal_id",
        "generated_at",
        "source_calibration_input_path",
        "model_asset_ref",
        "model_asset_sha256",
        "current_threshold",
        "current_smoothing_window",
        "current_hysteresis_settings",
        "proposal_items",
        "blocked_items",
        "summary",
        "source_contract_refs",
        "warnings",
        "non_claims",
        "tom_provenance",
    ):
        if field not in proposal:
            errors.append(_error("missing_calibration_proposal_field", field, None))
    for item in _list(proposal.get("proposal_items")):
        errors.extend(_validate_proposal_item(_dict(item)))
    return errors


def _validate_proposal_item(item: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for field in (
        "proposal_item_id",
        "proposal_type",
        "proposal_status",
        "source_metric_group",
        "source_review_entry_refs",
        "source_segment_refs",
        "observed_review_pattern",
        "proposed_evaluation_action",
        "proposed_candidate_setting",
        "requires_human_review",
        "required_preconditions",
        "risk_flags",
        "provenance_status",
        "warnings",
    ):
        if field not in item:
            errors.append(_error("missing_proposal_item_field", field, None))
    if item.get("proposal_type") not in ALLOWED_PROPOSAL_TYPES:
        errors.append(
            _error("unsupported_proposal_type", "proposal_type", item.get("proposal_type"))
        )
    if item.get("proposal_status") not in ALLOWED_PROPOSAL_STATUSES:
        errors.append(
            _error(
                "unsupported_proposal_status",
                "proposal_status",
                item.get("proposal_status"),
            )
        )
    if item.get("proposed_evaluation_action") not in ALLOWED_EVALUATION_ACTIONS:
        errors.append(
            _error(
                "unsupported_evaluation_action",
                "proposed_evaluation_action",
                item.get("proposed_evaluation_action"),
            )
        )
    for flag in _string_list(item.get("risk_flags")):
        if flag not in ALLOWED_RISK_FLAGS:
            errors.append(_error("unsupported_risk_flag", "risk_flags", flag))
    candidate = _dict(item.get("proposed_candidate_setting"))
    if candidate.get("not_applied") is not True:
        errors.append(
            _error(
                "candidate_setting_must_be_not_applied",
                "proposed_candidate_setting.not_applied",
                candidate.get("not_applied"),
            )
        )
    if candidate.get("writes_runtime_config") is not False:
        errors.append(
            _error(
                "candidate_setting_must_not_write_runtime_config",
                "proposed_candidate_setting.writes_runtime_config",
                candidate.get("writes_runtime_config"),
            )
        )
    if candidate.get("affects_regression_baselines") is not False:
        errors.append(
            _error(
                "candidate_setting_must_not_affect_baselines",
                "proposed_candidate_setting.affects_regression_baselines",
                candidate.get("affects_regression_baselines"),
            )
        )
    if candidate.get("future_evaluation_only") is not True:
        errors.append(
            _error(
                "candidate_setting_must_be_future_evaluation_only",
                "proposed_candidate_setting.future_evaluation_only",
                candidate.get("future_evaluation_only"),
            )
        )
    return errors


def _validate_source_contract_refs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    refs = _dict(payload.get("source_contract_refs"))
    errors = []
    for field, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(field) != expected:
            errors.append(_error("invalid_source_contract_ref", field, refs.get(field)))
    return errors


def _model_asset_from_sources(
    *,
    metrics_report: dict[str, Any],
    review_bundle: dict[str, Any],
    review_loop_report: dict[str, Any],
    model_asset_path: str | Path,
) -> dict[str, Any]:
    if metrics_report.get("model_asset_ref"):
        return {
            "model_asset_ref": metrics_report.get("model_asset_ref"),
            "model_asset_sha256": metrics_report.get("model_asset_sha256"),
            "model_asset_exists": bool(metrics_report.get("model_asset_exists")),
        }
    if review_bundle.get("model_asset_ref"):
        return {
            "model_asset_ref": review_bundle.get("model_asset_ref"),
            "model_asset_sha256": review_bundle.get("model_asset_sha256"),
            "model_asset_exists": bool(review_bundle.get("model_asset_exists")),
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
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "model_asset_ref": str(model_asset_path),
        "model_asset_sha256": digest,
        "model_asset_exists": True,
    }


def _warnings_from_sources(
    *,
    metrics_report: dict[str, Any],
    review_loop_report: dict[str, Any],
    review_bundle: dict[str, Any],
    corpus_run: dict[str, Any],
) -> dict[str, Any]:
    return {
        **dict(CALIBRATION_WARNINGS),
        **_dict(metrics_report.get("warnings")),
        **_dict(review_loop_report.get("warnings")),
        **_dict(review_bundle.get("warnings")),
        **_dict(corpus_run.get("warnings")),
    }


def _entry_refs(
    entries: list[dict[str, Any]],
    predicate: Any,
) -> list[dict[str, Any]]:
    refs = []
    for entry in entries:
        if not predicate(entry):
            continue
        refs.append(
            {
                "review_entry_id": entry.get("review_entry_id"),
                "corpus_entry_id": entry.get("corpus_entry_id"),
                "segment_id": entry.get("segment_id"),
                "replay_url": entry.get("replay_url"),
            }
        )
    return refs


def _segment_refs(review_entry_refs: list[Any]) -> list[dict[str, Any]]:
    refs = []
    for ref in review_entry_refs:
        ref_dict = _dict(ref)
        if ref_dict.get("segment_id") is None:
            continue
        refs.append(
            {
                "segment_id": ref_dict.get("segment_id"),
                "review_entry_id": ref_dict.get("review_entry_id"),
            }
        )
    return refs


def _is_boundary_or_uncertain_entry(entry: dict[str, Any]) -> bool:
    human = _dict(entry.get("human_review"))
    flags = set(_string_list(human.get("ambiguity_flags")))
    return (
        "classifier_boundary_unclear" in flags
        or human.get("reviewed_segment_status") == "reviewed_as_uncertain"
        or entry.get("segment_status") == "uncertain_segment"
    )


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
        "validation_version": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_PROPOSAL_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "payload_path": str(Path(payload_path)),
        "payload_type": payload_type,
        "payload_version": payload_version,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(CALIBRATION_WARNINGS),
        "known_limitations": [
            "Validation checks structural proposal shape, allowed values, source refs, "
            "candidate-setting not-applied semantics, and exact forbidden tokens.",
            "Validation does not infer review labels.",
            "Validation does not calculate classifier accuracy.",
            "Validation does not alter thresholds, smoothing, hysteresis, baselines, "
            "or model assets.",
        ],
    }


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    return _load_required_json(
        contract_path,
        "review_guided_gameplay_calibration_proposal_contract",
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
        "warnings": dict(CALIBRATION_WARNINGS),
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
            if key_text in FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS:
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
    elif isinstance(value, str) and value in FORBIDDEN_CALIBRATION_PROPOSAL_TOKENS:
        errors.append(_error("forbidden_field_or_value", path, value))


def _stable_id(*parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if value is None:
        return []
    return [str(value)]


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "field": field, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "blueprint": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_BLUEPRINT,
        "blueprint_name": REVIEW_GUIDED_GAMEPLAY_CALIBRATION_BLUEPRINT_NAME,
        "project_version": "0.0.0",
    }
