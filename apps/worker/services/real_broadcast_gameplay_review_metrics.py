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
from apps.worker.services.gameplay_segment_gate import DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH
from apps.worker.services.real_broadcast_gameplay_gate_corpus_run import (
    DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
)
from apps.worker.services.real_broadcast_gameplay_review_loop import (
    ALLOWED_AMBIGUITY_FLAGS,
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT,
    DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT,
    REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION,
)
from apps.worker.services.real_broadcast_gameplay_review_loop import (
    SOURCE_CONTRACT_REFS as REVIEW_LOOP_SOURCE_CONTRACT_REFS,
)

REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_TYPE = (
    "real_broadcast_gameplay_review_metrics_contract"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE = (
    "real_broadcast_gameplay_review_metrics_report"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE = (
    "real_broadcast_gameplay_review_qa_dashboard"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE = (
    "real_broadcast_gameplay_review_next_actions_report"
)
REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_VERSION = "v1"
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_BLUEPRINT = "blueprint_48"
REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_BLUEPRINT_NAME = (
    "real_broadcast_gameplay_review_metrics_dashboard_v1"
)

DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT = (
    ".data/contracts/real_broadcast_gameplay_review_metrics_contract_v1.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_metrics_report.current.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_VALIDATION_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_metrics_report.validation.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_qa_dashboard.current.json"
)
DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_OUTPUT = (
    ".data/exports/real_broadcast_gameplay_review_next_actions.current.json"
)

REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_EXPORTED_AT = datetime(
    2026,
    6,
    19,
    0,
    0,
    tzinfo=UTC,
)

METRIC_GROUPS = [
    "review_coverage",
    "segment_status_distribution",
    "downstream_gate_review_distribution",
    "confidence_distribution",
    "ambiguity_flag_distribution",
    "missing_review_fields",
    "review_readiness",
    "corpus_entry_coverage",
    "replay_context_coverage",
    "model_asset_provenance",
    "qa_warnings",
    "next_review_actions",
]

DASHBOARD_CARD_IDS = [
    "total_review_entries",
    "reviewed_entries",
    "unreviewed_entries",
    "needs_additional_review",
    "review_completion_rate",
    "reviewed_gameplay_candidate_segments",
    "reviewed_non_gameplay_candidate_segments",
    "reviewed_uncertain_segments",
    "downstream_allow_reviews",
    "downstream_block_reviews",
    "high_ambiguity_entries",
    "missing_review_fields",
    "human_review_required",
]

DASHBOARD_TABLE_IDS = [
    "review_coverage",
    "segment_status_distribution",
    "downstream_gate_review_distribution",
    "confidence_distribution",
    "ambiguity_flag_distribution",
    "missing_review_fields",
    "qa_warnings",
    "next_review_actions",
]

ALLOWED_NEXT_ACTION_TYPES = [
    "review_unreviewed_entries",
    "review_uncertain_segments",
    "review_high_ambiguity_entries",
    "complete_missing_review_fields",
    "inspect_classifier_boundary_cases",
    "inspect_broadcast_replay_possible_cases",
    "inspect_commercial_or_graphic_possible_cases",
    "prepare_human_review_batch",
    "not_applicable",
]

FORBIDDEN_REVIEW_METRICS_TOKENS = {
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
}

METRICS_WARNINGS = {
    "metrics_are_not_truth": True,
    "review_loop_is_not_truth": True,
    "gameplay_gate_is_not_truth": True,
    "classifier_correctness_not_assessed": True,
    "classifier_accuracy_not_assessed": True,
    "expected_tags_are_not_truth": True,
    "review_metadata_is_not_training_truth": True,
    "automatic_relabeling_not_performed": True,
    "threshold_changes_not_performed": True,
    "generalization_not_claimed": True,
    "production_readiness_not_claimed": True,
    "model_assets_are_not_mutated": True,
    "regression_baselines_are_not_mutated": True,
    "operations_visibility_only": True,
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
}

SOURCE_CONTRACT_REFS = {
    "real_broadcast_gameplay_review_loop_contract_version": (
        REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_CONTRACT_VERSION
    ),
    **dict(REVIEW_LOOP_SOURCE_CONTRACT_REFS),
}


def export_real_broadcast_gameplay_review_metrics_contract(
    *,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT
    ),
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    exported_at = exported_at or REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result = {
        "ok": True,
        "status": "completed",
        "contract_type": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION,
        "metrics_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE,
        "qa_dashboard_type": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
        "next_actions_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE,
        "contract": contract,
        "warnings": dict(METRICS_WARNINGS),
    }
    _write_json_if_requested(output_path, contract, result, "contract_output")
    return result


def build_real_broadcast_gameplay_review_metrics_report(
    *,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT,
    source_review_loop_report_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_LOOP_REPORT_OUTPUT
    ),
    source_review_bundle_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_BUNDLE_TEMPLATE_OUTPUT
    ),
    source_corpus_run_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_CORPUS_OUTPUT,
    source_review_dataset_path: str | Path | None = None,
    source_regression_baseline_path: str | Path | None = (
        DEFAULT_GAMEPLAY_GATE_REGRESSION_BASELINE_OUTPUT
    ),
    model_asset_path: str | Path = DEFAULT_GAMEPLAY_CLASSIFIER_ASSET_PATH,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT
    ),
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if errors:
        return _failed_result(
            status="invalid_metrics_contract",
            errors=errors,
            output_path=output_path,
            payload_type=REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE,
            result_key="metrics_report_output",
        )

    review_loop_report = _load_optional_json(
        source_review_loop_report_path,
        "real_broadcast_gameplay_review_loop_report",
    )
    review_bundle = _load_optional_json(
        source_review_bundle_path,
        "real_broadcast_gameplay_review_bundle",
    )
    corpus_run = _load_optional_json(source_corpus_run_path, "real_broadcast_gameplay_corpus_run")
    review_dataset = _load_optional_json(
        source_review_dataset_path,
        "gameplay_gate_review_dataset",
    )
    regression_baseline = _load_optional_json(
        source_regression_baseline_path,
        "gameplay_gate_regression_baseline",
    )

    entries = [entry for entry in _list(review_bundle.get("entries")) if isinstance(entry, dict)]
    report_summary = _dict(review_loop_report.get("summary"))
    metric_groups = _metric_groups(
        entries=entries,
        review_loop_report=review_loop_report,
        review_bundle=review_bundle,
        corpus_run=corpus_run,
        review_dataset=review_dataset,
        regression_baseline=regression_baseline,
        model_asset_path=model_asset_path,
    )
    metrics_report_id = _stable_id(
        "real_broadcast_gameplay_review_metrics_report_v1",
        str(source_review_loop_report_path),
        str(source_review_bundle_path),
        metric_groups,
    )
    report = {
        "metrics_report_id": metrics_report_id,
        "metrics_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE,
        "metrics_report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
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
        "source_review_dataset_path": (
            str(Path(source_review_dataset_path)) if source_review_dataset_path else None
        ),
        "source_regression_baseline_path": (
            str(Path(source_regression_baseline_path))
            if source_regression_baseline_path
            else None
        ),
        "model_asset_ref": _model_asset_from_sources(
            review_bundle=review_bundle,
            review_loop_report=review_loop_report,
            model_asset_path=model_asset_path,
        ).get("model_asset_ref"),
        "model_asset_sha256": _model_asset_from_sources(
            review_bundle=review_bundle,
            review_loop_report=review_loop_report,
            model_asset_path=model_asset_path,
        ).get("model_asset_sha256"),
        "model_asset_exists": _model_asset_from_sources(
            review_bundle=review_bundle,
            review_loop_report=review_loop_report,
            model_asset_path=model_asset_path,
        ).get("model_asset_exists"),
        "metric_groups": metric_groups,
        "summary": {
            **_dict(report_summary),
            "metrics_group_count": len(metric_groups),
            "review_bundle_entry_count": _get_nested_int(
                metric_groups,
                "review_coverage",
                "review_bundle_entry_count",
            ),
            "review_completion_rate": _get_nested_float(
                metric_groups,
                "review_coverage",
                "review_completion_rate",
            ),
            "metrics_are_not_truth": True,
            "classifier_correctness_not_assessed": True,
            "automatic_relabeling_not_performed": True,
            "threshold_changes_not_performed": True,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "warnings": _warnings_from_sources(
            review_loop_report=review_loop_report,
            review_bundle=review_bundle,
        ),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    result = {
        "ok": True,
        "status": "completed",
        "metrics_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE,
        "metrics_report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_VERSION,
        "metrics_report_id": metrics_report_id,
        "summary": report["summary"],
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "metrics_report_output")
    return result


def validate_real_broadcast_gameplay_review_metrics_report(
    *,
    metrics_report_path: str | Path,
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT,
    output_path: str | Path | None = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_VALIDATION_OUTPUT
    ),
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    validated_at = validated_at or datetime.now(UTC)
    errors: list[dict[str, Any]] = []
    contract = _load_contract(contract_path=contract_path, errors=errors)
    report = _load_required_json(metrics_report_path, "review_metrics_report", errors)
    if contract:
        errors.extend(_validate_contract_shape(contract))
    if report:
        errors.extend(_validate_metrics_report_shape(report))
        errors.extend(_validate_source_contract_refs(report))
        errors.extend(_forbidden_token_errors(report, path="metrics_report"))
    result = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "real_broadcast_gameplay_review_metrics_report_validation",
        "validation_version": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "metrics_report_path": str(Path(metrics_report_path)),
        "contract_type": contract.get("contract_type") if contract else None,
        "contract_version": contract.get("contract_version") if contract else None,
        "metrics_report_type": report.get("metrics_report_type") if report else None,
        "metrics_report_version": report.get("metrics_report_version") if report else None,
        "error_count": len(errors),
        "errors": errors,
        "warnings": dict(METRICS_WARNINGS),
        "known_limitations": [
            "Validation checks structural metrics shape, allowed metric groups, source refs, "
            "and exact forbidden tokens.",
            "Validation does not infer review labels.",
            "Validation does not calculate classifier accuracy.",
            "Validation does not alter thresholds or model assets.",
        ],
    }
    _write_json_if_requested(output_path, result, result, "validation_output")
    return result


def build_real_broadcast_gameplay_review_qa_dashboard(
    *,
    metrics_report_path: str | Path = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT
    ),
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_real_broadcast_gameplay_review_metrics_report(
        metrics_report_path=metrics_report_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_metrics_report",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
            result_key="dashboard_output",
        )
    report = _load_optional_json(metrics_report_path, "review_metrics_report")
    groups = _dict(report.get("metric_groups"))
    dashboard = {
        "dashboard_id": _stable_id(
            "real_broadcast_gameplay_review_qa_dashboard_v1",
            str(metrics_report_path),
            groups,
        ),
        "dashboard_type": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
        "dashboard_version": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_metrics_report_path": str(Path(metrics_report_path)),
        "cards": _dashboard_cards(groups),
        "tables": _dashboard_tables(groups),
        "validation_snapshot": validation,
        "warnings": _dict(report.get("warnings")) or dict(METRICS_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    dashboard_errors = _validate_dashboard_shape(dashboard)
    if dashboard_errors:
        return _failed_result(
            status="invalid_qa_dashboard",
            errors=dashboard_errors,
            output_path=output_path,
            payload_type=REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
            result_key="dashboard_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "dashboard_type": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
        "dashboard_version": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_VERSION,
        "dashboard_id": dashboard["dashboard_id"],
        "card_count": len(dashboard["cards"]),
        "table_count": len(dashboard["tables"]),
        "dashboard": dashboard,
        "warnings": dashboard["warnings"],
    }
    _write_json_if_requested(output_path, dashboard, result, "dashboard_output")
    return result


def build_real_broadcast_gameplay_review_next_actions_report(
    *,
    metrics_report_path: str | Path = (
        DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_OUTPUT
    ),
    contract_path: str | Path = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_OUTPUT,
    output_path: str | Path | None = DEFAULT_REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC)
    validation = validate_real_broadcast_gameplay_review_metrics_report(
        metrics_report_path=metrics_report_path,
        contract_path=contract_path,
        output_path=None,
        validated_at=generated_at,
    )
    if validation.get("ok") is False:
        return _failed_result(
            status="invalid_metrics_report",
            errors=_list(validation.get("errors")),
            output_path=output_path,
            payload_type=REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE,
            result_key="next_actions_output",
        )
    metrics_report = _load_optional_json(metrics_report_path, "review_metrics_report")
    groups = _dict(metrics_report.get("metric_groups"))
    actions = _next_actions(groups)
    report = {
        "next_actions_report_id": _stable_id(
            "real_broadcast_gameplay_review_next_actions_report_v1",
            str(metrics_report_path),
            actions,
        ),
        "next_actions_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE,
        "next_actions_report_version": (
            REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_VERSION
        ),
        "generated_at": generated_at.isoformat(),
        "source_metrics_report_path": str(Path(metrics_report_path)),
        "prioritized_actions": actions,
        "validation_snapshot": validation,
        "warnings": _dict(metrics_report.get("warnings")) or dict(METRICS_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
        "tom_provenance": _tom_provenance(),
    }
    action_errors = _validate_next_actions_shape(report)
    if action_errors:
        return _failed_result(
            status="invalid_next_actions_report",
            errors=action_errors,
            output_path=output_path,
            payload_type=REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE,
            result_key="next_actions_output",
        )
    result = {
        "ok": True,
        "status": "completed",
        "next_actions_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE,
        "next_actions_report_version": (
            REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_VERSION
        ),
        "next_actions_report_id": report["next_actions_report_id"],
        "action_count": len(actions),
        "report": report,
        "warnings": report["warnings"],
    }
    _write_json_if_requested(output_path, report, result, "next_actions_output")
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_TYPE,
        "contract_version": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "metrics_scope": {
            "purpose": "real_broadcast_gameplay_review_operations_visibility",
            "reads_review_loop_report_when_supplied": True,
            "reads_review_bundle_when_supplied": True,
            "reads_corpus_run_context_when_supplied": True,
            "builds_metrics_report": True,
            "builds_dashboard_ready_json": True,
            "builds_next_review_actions": True,
            "calculates_classifier_accuracy": False,
            "creates_review_labels": False,
            "automatic_relabeling_allowed": False,
            "threshold_changes_allowed": False,
            "smoothing_changes_allowed": False,
            "model_tuning_allowed": False,
            "mutates_model_assets": False,
            "mutates_regression_baselines": False,
        },
        "source_contract_refs": dict(SOURCE_CONTRACT_REFS),
        "metrics_report_schema": {
            "metrics_report_type": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE,
            "metrics_report_version": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_VERSION,
            "required_fields": [
                "metrics_report_id",
                "metrics_report_version",
                "generated_at",
                "source_review_loop_report_path",
                "source_review_bundle_path",
                "source_corpus_run_path",
                "source_review_dataset_path",
                "source_regression_baseline_path",
                "model_asset_ref",
                "model_asset_sha256",
                "metric_groups",
                "summary",
                "warnings",
                "non_claims",
            ],
        },
        "qa_dashboard_schema": {
            "dashboard_type": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE,
            "dashboard_version": REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_VERSION,
            "allowed_card_ids": list(DASHBOARD_CARD_IDS),
            "allowed_table_ids": list(DASHBOARD_TABLE_IDS),
        },
        "next_actions_schema": {
            "next_actions_report_type": (
                REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE
            ),
            "next_actions_report_version": (
                REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_VERSION
            ),
            "allowed_next_action_types": list(ALLOWED_NEXT_ACTION_TYPES),
        },
        "metric_groups": list(METRIC_GROUPS),
        "validation_rules": {
            "validate_contract_shape": True,
            "validate_metrics_report_shape": True,
            "validate_qa_dashboard_shape": True,
            "validate_next_actions_report_shape": True,
            "validate_allowed_metric_group_names": True,
            "validate_allowed_dashboard_card_names": True,
            "validate_allowed_next_action_types": True,
            "validate_referenced_contracts_when_available": True,
            "reject_forbidden_fields_and_values": True,
            "report_structural_errors_only": True,
            "does_not_infer_tennis_meaning": True,
            "does_not_calculate_classifier_accuracy": True,
            "does_not_auto_label_segments": True,
            "does_not_alter_thresholds": True,
            "does_not_modify_regression_baselines": True,
        },
        "provenance_requirements": {
            "source_review_loop_report_path_recorded_when_supplied": True,
            "source_review_bundle_path_recorded_when_supplied": True,
            "source_corpus_run_path_recorded_when_supplied": True,
            "source_review_dataset_path_recorded_when_supplied": True,
            "source_regression_baseline_path_recorded_when_supplied": True,
            "model_asset_provenance_preserved": True,
            "source_warnings_preserved": True,
            "non_claims_preserved": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(METRICS_WARNINGS),
        "non_claims": dict(NON_CLAIMS),
    }


def _metric_groups(
    *,
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
    review_bundle: dict[str, Any],
    corpus_run: dict[str, Any],
    review_dataset: dict[str, Any],
    regression_baseline: dict[str, Any],
    model_asset_path: str | Path,
) -> dict[str, Any]:
    review_coverage = _review_coverage(entries, review_loop_report)
    return {
        "review_coverage": review_coverage,
        "segment_status_distribution": _segment_status_distribution(
            entries,
            review_loop_report,
        ),
        "downstream_gate_review_distribution": _downstream_gate_review_distribution(
            entries,
            review_loop_report,
        ),
        "confidence_distribution": _confidence_distribution(entries, review_loop_report),
        "ambiguity_flag_distribution": _ambiguity_flag_distribution(
            entries,
            review_loop_report,
        ),
        "missing_review_fields": _missing_review_fields(entries, review_loop_report),
        "review_readiness": _review_readiness(entries, review_coverage),
        "corpus_entry_coverage": _corpus_entry_coverage(entries, corpus_run),
        "replay_context_coverage": _replay_context_coverage(entries, review_bundle),
        "model_asset_provenance": _model_asset_from_sources(
            review_bundle=review_bundle,
            review_loop_report=review_loop_report,
            model_asset_path=model_asset_path,
        ),
        "qa_warnings": _qa_warnings(
            review_loop_report=review_loop_report,
            review_bundle=review_bundle,
            review_dataset=review_dataset,
            regression_baseline=regression_baseline,
        ),
        "next_review_actions": _next_action_metrics(entries, review_coverage),
    }


def _review_coverage(
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
) -> dict[str, Any]:
    summary = _dict(review_loop_report.get("summary"))
    total = len(entries) or _int(summary.get("review_bundle_entry_count"))
    reviewed = (
        _reviewed_entry_count(entries)
        if entries
        else _int(summary.get("reviewed_entry_count"))
    )
    unreviewed = (
        _human_status_count(entries, "not_reviewed")
        if entries
        else _int(summary.get("unreviewed_entry_count"))
    )
    needs_more = (
        _needs_additional_review_count(entries)
        if entries
        else _int(summary.get("needs_additional_review_count"))
    )
    optional = _human_status_count(entries, "not_applicable") if entries else 0
    required = max(0, total - optional)
    missing = _missing_review_fields(entries, review_loop_report)
    return {
        "review_bundle_entry_count": total,
        "reviewed_entry_count": reviewed,
        "unreviewed_entry_count": unreviewed,
        "needs_additional_review_count": needs_more,
        "review_completion_rate": _rate(reviewed, total),
        "review_pending_rate": _rate(unreviewed, total),
        "review_required_count": required,
        "review_optional_count": optional,
        "missing_reviewer_id_count": _int(missing.get("missing_reviewer_id_count")),
        "missing_reviewed_at_count": _int(missing.get("missing_reviewed_at_count")),
        "missing_review_notes_count": _int(missing.get("missing_review_notes_count")),
        "rates_are_operational_completeness_only": True,
        "classifier_correctness_not_assessed": True,
    }


def _segment_status_distribution(
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
) -> dict[str, int]:
    if not entries:
        summary = _dict(review_loop_report.get("summary"))
        return {
            "reviewed_as_gameplay_candidate_count": _int(
                summary.get("reviewed_as_gameplay_candidate_count")
            ),
            "reviewed_as_non_gameplay_candidate_count": _int(
                summary.get("reviewed_as_non_gameplay_candidate_count")
            ),
            "reviewed_as_uncertain_count": _int(
                summary.get("reviewed_as_uncertain_count")
            ),
            "not_reviewed_count": _int(summary.get("unreviewed_entry_count")),
            "not_applicable_count": 0,
        }
    return {
        "reviewed_as_gameplay_candidate_count": _human_status_count(
            entries,
            "reviewed_as_gameplay_candidate",
        ),
        "reviewed_as_non_gameplay_candidate_count": _human_status_count(
            entries,
            "reviewed_as_non_gameplay_candidate",
        ),
        "reviewed_as_uncertain_count": _human_status_count(
            entries,
            "reviewed_as_uncertain",
        ),
        "not_reviewed_count": _human_status_count(entries, "not_reviewed"),
        "not_applicable_count": _human_status_count(entries, "not_applicable"),
    }


def _downstream_gate_review_distribution(
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
) -> dict[str, int]:
    if not entries:
        summary = _dict(review_loop_report.get("summary"))
        return {
            "reviewer_would_allow_downstream_observation_count": _int(
                summary.get("downstream_allow_review_count")
            ),
            "reviewer_would_block_downstream_observation_count": _int(
                summary.get("downstream_block_review_count")
            ),
            "reviewer_requests_additional_review_count": _int(
                summary.get("needs_additional_review_count")
            ),
            "no_review_decision_count": _int(summary.get("unreviewed_entry_count")),
        }
    return {
        "reviewer_would_allow_downstream_observation_count": _human_downstream_count(
            entries,
            "reviewer_would_allow_downstream_observation",
        ),
        "reviewer_would_block_downstream_observation_count": _human_downstream_count(
            entries,
            "reviewer_would_block_downstream_observation",
        ),
        "reviewer_requests_additional_review_count": _human_downstream_count(
            entries,
            "reviewer_requests_additional_review",
        ),
        "no_review_decision_count": _human_downstream_count(entries, "no_review_decision"),
    }


def _confidence_distribution(
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
) -> dict[str, int]:
    if not entries:
        distribution = _dict(
            _dict(review_loop_report.get("summary")).get("confidence_distribution")
        )
        return {
            "review_confidence_low_count": _int(distribution.get("low")),
            "review_confidence_medium_count": _int(distribution.get("medium")),
            "review_confidence_high_count": _int(distribution.get("high")),
            "review_confidence_not_assessed_count": _int(distribution.get("not_assessed")),
            "review_confidence_not_applicable_count": _int(distribution.get("not_applicable")),
        }
    return {
        "review_confidence_low_count": _human_confidence_count(entries, "low"),
        "review_confidence_medium_count": _human_confidence_count(entries, "medium"),
        "review_confidence_high_count": _human_confidence_count(entries, "high"),
        "review_confidence_not_assessed_count": _human_confidence_count(
            entries,
            "not_assessed",
        ),
        "review_confidence_not_applicable_count": _human_confidence_count(
            entries,
            "not_applicable",
        ),
    }


def _ambiguity_flag_distribution(
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
) -> dict[str, int]:
    source_counts = Counter(
        flag
        for entry in entries
        for flag in _string_list(_dict(entry.get("human_review")).get("ambiguity_flags"))
    )
    if not entries:
        source_counts = Counter(
            _dict(_dict(review_loop_report.get("summary")).get("ambiguity_flag_counts"))
        )
    return {
        f"{flag}_count": _int(source_counts.get(flag))
        for flag in sorted(ALLOWED_AMBIGUITY_FLAGS)
    }


def _missing_review_fields(
    entries: list[dict[str, Any]],
    review_loop_report: dict[str, Any],
) -> dict[str, int]:
    if not entries:
        counts = _dict(_dict(review_loop_report.get("summary")).get("missing_review_field_counts"))
        return {
            "missing_reviewer_id_count": _int(counts.get("reviewer_id")),
            "missing_reviewed_at_count": _int(counts.get("reviewed_at")),
            "missing_reviewed_segment_status_count": _int(
                counts.get("reviewed_segment_status")
            ),
            "missing_reviewed_downstream_gate_status_count": _int(
                counts.get("reviewed_downstream_gate_status")
            ),
            "missing_review_confidence_count": _int(counts.get("review_confidence")),
            "missing_review_source_count": _int(counts.get("review_source")),
            "missing_review_notes_count": 0,
            "total_missing_review_field_count": sum(_int(value) for value in counts.values()),
        }
    counts = Counter()
    for entry in entries:
        human = _dict(entry.get("human_review"))
        if _string_or_none(human.get("reviewer_id")) is None:
            counts["missing_reviewer_id_count"] += 1
        if _string_or_none(human.get("reviewed_at")) is None:
            counts["missing_reviewed_at_count"] += 1
        if human.get("reviewed_segment_status") == "not_reviewed":
            counts["missing_reviewed_segment_status_count"] += 1
        if human.get("reviewed_downstream_gate_status") == "no_review_decision":
            counts["missing_reviewed_downstream_gate_status_count"] += 1
        if human.get("review_confidence") == "not_assessed":
            counts["missing_review_confidence_count"] += 1
        if human.get("review_source") == "not_assessed":
            counts["missing_review_source_count"] += 1
        if _string_or_none(human.get("reviewer_notes")) is None:
            counts["missing_review_notes_count"] += 1
    counts["total_missing_review_field_count"] = sum(counts.values())
    return dict(sorted(counts.items()))


def _review_readiness(
    entries: list[dict[str, Any]],
    coverage: dict[str, Any],
) -> dict[str, Any]:
    replay_count = sum(
        1 for entry in entries if _string_or_none(entry.get("replay_url")) is not None
    )
    timestamp_count = sum(
        1
        for entry in entries
        if entry.get("segment_start_ms") is not None and entry.get("segment_end_ms") is not None
    )
    total = _int(coverage.get("review_bundle_entry_count"))
    return {
        "ready_for_human_review": total > 0 and replay_count == total,
        "human_review_required_count": _int(coverage.get("review_required_count")),
        "review_pending_count": _int(coverage.get("unreviewed_entry_count")),
        "entries_with_replay_url_count": replay_count,
        "entries_with_timestamp_context_count": timestamp_count,
        "review_readiness_is_not_correctness": True,
        "classifier_correctness_not_assessed": True,
    }


def _corpus_entry_coverage(
    entries: list[dict[str, Any]],
    corpus_run: dict[str, Any],
) -> dict[str, Any]:
    corpus_ids = {
        str(entry.get("corpus_entry_id"))
        for entry in entries
        if entry.get("corpus_entry_id")
    }
    source_label_counts = Counter(
        str(entry.get("source_label") or "not_applicable") for entry in entries
    )
    return {
        "corpus_entry_count": len(corpus_ids),
        "source_corpus_run_entry_count": len(_list(corpus_run.get("entries"))),
        "source_label_counts": dict(sorted(source_label_counts.items())),
        "corpus_run_status": corpus_run.get("status") or "not_supplied",
    }


def _replay_context_coverage(
    entries: list[dict[str, Any]],
    review_bundle: dict[str, Any],
) -> dict[str, Any]:
    total = len(entries)
    replay_count = sum(
        1 for entry in entries if _string_or_none(entry.get("replay_url")) is not None
    )
    timestamp_count = sum(
        1
        for entry in entries
        if entry.get("segment_start_ms") is not None and entry.get("segment_end_ms") is not None
    )
    return {
        "entry_count": total,
        "entries_with_replay_url_count": replay_count,
        "entries_missing_replay_url_count": max(0, total - replay_count),
        "entries_with_timestamp_context_count": timestamp_count,
        "entries_missing_timestamp_context_count": max(0, total - timestamp_count),
        "source_review_bundle_id": review_bundle.get("review_bundle_id"),
    }


def _qa_warnings(
    *,
    review_loop_report: dict[str, Any],
    review_bundle: dict[str, Any],
    review_dataset: dict[str, Any],
    regression_baseline: dict[str, Any],
) -> dict[str, Any]:
    warnings = {
        **dict(METRICS_WARNINGS),
        **_dict(review_loop_report.get("warnings")),
        **_dict(review_bundle.get("warnings")),
    }
    return {
        "warning_count": len(warnings),
        "warnings": warnings,
        "source_review_dataset_supplied": bool(review_dataset),
        "source_regression_baseline_supplied": bool(regression_baseline),
        "qa_warnings_are_operational_only": True,
    }


def _next_action_metrics(
    entries: list[dict[str, Any]],
    coverage: dict[str, Any],
) -> dict[str, int]:
    ambiguity_counts = Counter(
        flag
        for entry in entries
        for flag in _string_list(_dict(entry.get("human_review")).get("ambiguity_flags"))
    )
    uncertain_count = sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("reviewed_segment_status")
        == "reviewed_as_uncertain"
        or entry.get("segment_status") == "uncertain_segment"
    )
    return {
        "review_unreviewed_entries_count": _int(coverage.get("unreviewed_entry_count")),
        "review_uncertain_segments_count": uncertain_count,
        "review_high_ambiguity_entries_count": sum(
            1
            for entry in entries
            if _string_list(_dict(entry.get("human_review")).get("ambiguity_flags"))
        ),
        "complete_missing_review_fields_count": _int(
            coverage.get("missing_reviewer_id_count")
        )
        + _int(coverage.get("missing_reviewed_at_count"))
        + _int(coverage.get("missing_review_notes_count")),
        "inspect_classifier_boundary_cases_count": _int(
            ambiguity_counts.get("classifier_boundary_unclear")
        ),
        "inspect_broadcast_replay_possible_cases_count": _int(
            ambiguity_counts.get("broadcast_replay_possible")
        ),
        "inspect_commercial_or_graphic_possible_cases_count": _int(
            ambiguity_counts.get("commercial_or_graphic_possible")
        ),
        "prepare_human_review_batch_count": _int(coverage.get("unreviewed_entry_count")),
    }


def _dashboard_cards(groups: dict[str, Any]) -> list[dict[str, Any]]:
    coverage = _dict(groups.get("review_coverage"))
    segment = _dict(groups.get("segment_status_distribution"))
    downstream = _dict(groups.get("downstream_gate_review_distribution"))
    ambiguity = _dict(groups.get("next_review_actions"))
    missing = _dict(groups.get("missing_review_fields"))
    values = {
        "total_review_entries": coverage.get("review_bundle_entry_count"),
        "reviewed_entries": coverage.get("reviewed_entry_count"),
        "unreviewed_entries": coverage.get("unreviewed_entry_count"),
        "needs_additional_review": coverage.get("needs_additional_review_count"),
        "review_completion_rate": coverage.get("review_completion_rate"),
        "reviewed_gameplay_candidate_segments": segment.get(
            "reviewed_as_gameplay_candidate_count"
        ),
        "reviewed_non_gameplay_candidate_segments": segment.get(
            "reviewed_as_non_gameplay_candidate_count"
        ),
        "reviewed_uncertain_segments": segment.get("reviewed_as_uncertain_count"),
        "downstream_allow_reviews": downstream.get(
            "reviewer_would_allow_downstream_observation_count"
        ),
        "downstream_block_reviews": downstream.get(
            "reviewer_would_block_downstream_observation_count"
        ),
        "high_ambiguity_entries": ambiguity.get("review_high_ambiguity_entries_count"),
        "missing_review_fields": missing.get("total_missing_review_field_count"),
        "human_review_required": coverage.get("review_required_count"),
    }
    return [
        {
            "card_id": card_id,
            "label": card_id.replace("_", " "),
            "value": values.get(card_id, 0),
            "value_type": "rate" if card_id.endswith("_rate") else "count",
            "structural_only": True,
        }
        for card_id in DASHBOARD_CARD_IDS
    ]


def _dashboard_tables(groups: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "table_id": table_id,
            "title": table_id.replace("_", " "),
            "rows": _rows_from_mapping(_dict(groups.get(table_id))),
            "structural_only": True,
        }
        for table_id in DASHBOARD_TABLE_IDS
    ]


def _rows_from_mapping(mapping: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for key, value in sorted(mapping.items()):
        if isinstance(value, dict):
            value = len(value)
        elif isinstance(value, list):
            value = len(value)
        rows.append({"metric": key, "value": value})
    return rows


def _next_actions(groups: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = _dict(groups.get("next_review_actions"))
    actions: list[dict[str, Any]] = []
    action_specs = [
        ("review_unreviewed_entries", "review_unreviewed_entries_count"),
        ("review_uncertain_segments", "review_uncertain_segments_count"),
        ("review_high_ambiguity_entries", "review_high_ambiguity_entries_count"),
        ("complete_missing_review_fields", "complete_missing_review_fields_count"),
        ("inspect_classifier_boundary_cases", "inspect_classifier_boundary_cases_count"),
        (
            "inspect_broadcast_replay_possible_cases",
            "inspect_broadcast_replay_possible_cases_count",
        ),
        (
            "inspect_commercial_or_graphic_possible_cases",
            "inspect_commercial_or_graphic_possible_cases_count",
        ),
        ("prepare_human_review_batch", "prepare_human_review_batch_count"),
    ]
    for action_type, count_field in action_specs:
        count = _int(metrics.get(count_field))
        if count <= 0:
            continue
        actions.append(
            {
                "action_type": action_type,
                "display_order": len(actions) + 1,
                "title": action_type.replace("_", " "),
                "affected_entry_count": count,
                "reason": "human_review_metadata_gap",
                "changes_labels_or_thresholds": False,
                "review_operations_only": True,
            }
        )
    if not actions:
        actions.append(
            {
                "action_type": "not_applicable",
                "display_order": 1,
                "title": "not applicable",
                "affected_entry_count": 0,
                "reason": "no_review_operations_action_suggested",
                "changes_labels_or_thresholds": False,
                "review_operations_only": True,
            }
        )
    return actions


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(contract, path="contract")
    if contract.get("contract_type") != REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if (
        contract.get("contract_version")
        != REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_CONTRACT_VERSION
    ):
        errors.append(
            _error(
                "invalid_contract_version",
                "contract_version",
                contract.get("contract_version"),
            )
        )
    for section in (
        "metrics_scope",
        "source_contract_refs",
        "metrics_report_schema",
        "qa_dashboard_schema",
        "next_actions_schema",
        "metric_groups",
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


def _validate_metrics_report_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if report.get("metrics_report_type") != REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_TYPE:
        errors.append(
            _error(
                "invalid_metrics_report_type",
                "metrics_report_type",
                report.get("metrics_report_type"),
            )
        )
    if (
        report.get("metrics_report_version")
        != REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_REPORT_VERSION
    ):
        errors.append(
            _error(
                "invalid_metrics_report_version",
                "metrics_report_version",
                report.get("metrics_report_version"),
            )
        )
    for field in (
        "metrics_report_id",
        "metrics_report_version",
        "generated_at",
        "source_review_loop_report_path",
        "source_review_bundle_path",
        "source_corpus_run_path",
        "source_review_dataset_path",
        "source_regression_baseline_path",
        "model_asset_ref",
        "model_asset_sha256",
        "metric_groups",
        "summary",
        "warnings",
        "non_claims",
    ):
        if field not in report:
            errors.append(_error("missing_metrics_report_field", field, None))
    groups = _dict(report.get("metric_groups"))
    for group_name in groups:
        if group_name not in METRIC_GROUPS:
            errors.append(_error("unsupported_metric_group", "metric_groups", group_name))
    for group_name in METRIC_GROUPS:
        if group_name not in groups:
            errors.append(_error("missing_metric_group", f"metric_groups.{group_name}", None))
    return errors


def _validate_dashboard_shape(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(dashboard, path="qa_dashboard")
    if dashboard.get("dashboard_type") != REAL_BROADCAST_GAMEPLAY_REVIEW_QA_DASHBOARD_TYPE:
        errors.append(
            _error("invalid_dashboard_type", "dashboard_type", dashboard.get("dashboard_type"))
        )
    for card in _list(dashboard.get("cards")):
        card_id = _string_or_none(_dict(card).get("card_id"))
        if card_id not in DASHBOARD_CARD_IDS:
            errors.append(_error("unsupported_dashboard_card", "cards.card_id", card_id))
    for table in _list(dashboard.get("tables")):
        table_id = _string_or_none(_dict(table).get("table_id"))
        if table_id not in DASHBOARD_TABLE_IDS:
            errors.append(_error("unsupported_dashboard_table", "tables.table_id", table_id))
    return errors


def _validate_next_actions_shape(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_token_errors(report, path="next_actions_report")
    if (
        report.get("next_actions_report_type")
        != REAL_BROADCAST_GAMEPLAY_REVIEW_NEXT_ACTIONS_REPORT_TYPE
    ):
        errors.append(
            _error(
                "invalid_next_actions_report_type",
                "next_actions_report_type",
                report.get("next_actions_report_type"),
            )
        )
    for action in _list(report.get("prioritized_actions")):
        action_type = _string_or_none(_dict(action).get("action_type"))
        if action_type not in ALLOWED_NEXT_ACTION_TYPES:
            errors.append(_error("unsupported_next_action_type", "action_type", action_type))
    return errors


def _validate_source_contract_refs(report: dict[str, Any]) -> list[dict[str, Any]]:
    refs = _dict(report.get("source_contract_refs"))
    errors = []
    for field, expected in SOURCE_CONTRACT_REFS.items():
        if refs.get(field) != expected:
            errors.append(_error("invalid_source_contract_ref", field, refs.get(field)))
    return errors


def _model_asset_from_sources(
    *,
    review_bundle: dict[str, Any],
    review_loop_report: dict[str, Any],
    model_asset_path: str | Path,
) -> dict[str, Any]:
    report_model = _dict(review_loop_report.get("model_asset_provenance"))
    if review_bundle.get("model_asset_ref") or report_model.get("model_asset_ref"):
        return {
            "model_asset_ref": review_bundle.get("model_asset_ref")
            or report_model.get("model_asset_ref"),
            "model_asset_sha256": review_bundle.get("model_asset_sha256")
            or report_model.get("model_asset_sha256"),
            "model_asset_exists": bool(
                review_bundle.get("model_asset_exists") or report_model.get("model_asset_exists")
            ),
            "model_assets_are_not_mutated": True,
            "classifier_correctness_not_assessed": True,
        }
    return {
        **_model_asset_ref(model_asset_path),
        "model_assets_are_not_mutated": True,
        "classifier_correctness_not_assessed": True,
    }


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
    review_loop_report: dict[str, Any],
    review_bundle: dict[str, Any],
) -> dict[str, Any]:
    return {
        **dict(METRICS_WARNINGS),
        **_dict(review_loop_report.get("warnings")),
        **_dict(review_bundle.get("warnings")),
    }


def _reviewed_entry_count(entries: list[dict[str, Any]]) -> int:
    return sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("reviewed_segment_status")
        not in {"not_reviewed", "not_applicable"}
    )


def _human_status_count(entries: list[dict[str, Any]], status: str) -> int:
    return sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("reviewed_segment_status") == status
    )


def _human_downstream_count(entries: list[dict[str, Any]], status: str) -> int:
    return sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("reviewed_downstream_gate_status") == status
    )


def _human_confidence_count(entries: list[dict[str, Any]], confidence: str) -> int:
    return sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("review_confidence") == confidence
    )


def _needs_additional_review_count(entries: list[dict[str, Any]]) -> int:
    return sum(
        1
        for entry in entries
        if _dict(entry.get("human_review")).get("needs_additional_review") is True
        or _dict(entry.get("human_review")).get("reviewed_segment_status")
        == "needs_additional_review"
        or _dict(entry.get("human_review")).get("reviewed_downstream_gate_status")
        == "reviewer_requests_additional_review"
    )


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 6)


def _get_nested_int(mapping: dict[str, Any], section: str, field: str) -> int:
    return _int(_dict(mapping.get(section)).get(field))


def _get_nested_float(mapping: dict[str, Any], section: str, field: str) -> float:
    try:
        return float(_dict(mapping.get(section)).get(field) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _load_contract(
    *,
    contract_path: str | Path,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    return _load_required_json(
        contract_path,
        "real_broadcast_gameplay_review_metrics_contract",
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
        "warnings": dict(METRICS_WARNINGS),
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
            if key_text in FORBIDDEN_REVIEW_METRICS_TOKENS:
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
    elif isinstance(value, str) and value in FORBIDDEN_REVIEW_METRICS_TOKENS:
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


def _error(error_type: str, field: str, value: Any) -> dict[str, Any]:
    return {"error_type": error_type, "field": field, "value": value}


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "blueprint": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_BLUEPRINT,
        "blueprint_name": REAL_BROADCAST_GAMEPLAY_REVIEW_METRICS_BLUEPRINT_NAME,
        "project_version": "0.0.0",
    }
