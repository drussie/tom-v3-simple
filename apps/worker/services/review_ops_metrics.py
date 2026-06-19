from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_CONTRACT_TYPE,
    COVERAGE_SAMPLING_CONTRACT_VERSION,
    COVERAGE_SAMPLING_PROFILE_TYPE,
    COVERAGE_SAMPLING_PROFILE_VERSION,
    COVERAGE_SAMPLING_REPORT_TYPE,
    COVERAGE_SAMPLING_REPORT_VERSION,
    DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT,
    DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT,
)
from apps.worker.services.intennse_label_alignment import (
    DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT,
    INTENNSE_ALIGNMENT_CONTRACT_TYPE,
    INTENNSE_ALIGNMENT_CONTRACT_VERSION,
)
from apps.worker.services.many_point_ingestion_gate import (
    DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT,
    DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT,
    MANY_POINT_INGESTION_CONTRACT_TYPE,
    MANY_POINT_INGESTION_CONTRACT_VERSION,
    MANY_POINT_INGESTION_GATE_TYPE,
    MANY_POINT_INGESTION_GATE_VERSION,
)
from apps.worker.services.multi_point_regression_matrix import (
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_reviewer_disagreement import (
    DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    MULTI_REVIEWER_SCHEMA_TYPE,
    MULTI_REVIEWER_SCHEMA_VERSION,
)
from apps.worker.services.observation_quality_taxonomy import (
    DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT,
    OBSERVATION_QUALITY_TAXONOMY_TYPE,
    OBSERVATION_QUALITY_TAXONOMY_VERSION,
)
from apps.worker.services.point_manifest import POINT_MANIFEST_VERSION
from apps.worker.services.review_label_schema import (
    DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    REVIEW_LABEL_SCHEMA_TYPE,
    REVIEW_LABEL_SCHEMA_VERSION,
)
from apps.worker.services.reviewer_confidence_schema import (
    DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT,
    REVIEWER_CONFIDENCE_SCHEMA_TYPE,
    REVIEWER_CONFIDENCE_SCHEMA_VERSION,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_CONTRACT_TYPE,
    DATASET_CORPUS_CONTRACT_VERSION,
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT,
    DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
)

REVIEW_OPS_METRICS_CONTRACT_TYPE = "review_ops_metrics_contract"
REVIEW_OPS_METRICS_CONTRACT_VERSION = "v1"
REVIEW_OPS_METRICS_REPORT_TYPE = "review_ops_metrics_report"
REVIEW_OPS_METRICS_REPORT_VERSION = "v1"
REVIEW_OPS_DASHBOARD_DATA_TYPE = "review_ops_dashboard_data"
REVIEW_OPS_DASHBOARD_DATA_VERSION = "v1"
REVIEW_OPS_BLUEPRINT = "blueprint_34"
REVIEW_OPS_BLUEPRINT_NAME = "review_ops_metrics_dashboard_v1"

DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT = (
    ".data/contracts/review_ops_metrics_contract_v1.json"
)
DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT = (
    ".data/exports/review_ops_metrics_report.current.json"
)
DEFAULT_REVIEW_OPS_METRICS_VALIDATION_OUTPUT = (
    ".data/exports/review_ops_metrics_report.validation.json"
)
DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT = (
    ".data/exports/review_ops_dashboard_data.current.json"
)

CONTRACT_EXPORTED_AT = datetime(2026, 6, 18, 0, 0, tzinfo=UTC)

METRIC_GROUPS = [
    "corpus_entry_counts",
    "review_label_coverage",
    "reviewer_confidence_coverage",
    "multi_reviewer_coverage",
    "disagreement_report_coverage",
    "intennse_alignment_coverage",
    "observation_quality_coverage",
    "provenance_completeness",
    "ingestion_gate_readiness",
    "coverage_sampling_gaps",
    "regression_protection_coverage",
    "missing_optional_refs",
    "human_review_required_counts",
]

DASHBOARD_CARD_IDS = [
    "total_corpus_entries",
    "replay_available_entries",
    "entries_with_point_manifest",
    "entries_with_review_label_bundle",
    "entries_with_reviewer_confidence_bundle",
    "entries_with_multi_reviewer_review",
    "entries_with_disagreement_report",
    "entries_with_intennse_alignment",
    "entries_with_provenance_partial",
    "entries_requiring_human_review",
    "regression_protected_entries",
    "ingestion_ready_entries",
    "coverage_gap_counts",
]

ALLOWED_METRIC_STATUS_VALUES = [
    "not_assessed",
    "present",
    "missing",
    "partial",
    "not_applicable",
    "requires_human_review",
    "provenance_present",
    "provenance_partial",
    "provenance_missing",
    "coverage_gap_present",
    "structurally_ready",
    "structurally_blocked",
]

FORBIDDEN_REVIEW_OPS_FIELDS = {
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
    "tactical_recommendation",
    "coaching_recommendation",
    "betting_prediction",
    "match_outcome",
    "reviewer_score",
    "reviewer_rank",
    "quality_score",
    "training_truth",
    "model_ready_truth",
    "disagreement_resolution",
}

FORBIDDEN_METRIC_STATUS_TERMS = FORBIDDEN_REVIEW_OPS_FIELDS | {"true", "false", "resolved"}

REVIEW_OPS_WARNINGS = {
    "review_ops_metrics_are_not_truth": True,
    "operations_visibility_only": True,
    "read_only_dashboard_data": True,
    "provenance_only": True,
    "observation_only": True,
    "review_support_only": True,
    "no_adjudication": True,
    "does_not_create_labels": True,
    "does_not_create_review_labels": True,
    "does_not_create_confidence_scores": True,
    "does_not_rank_reviewers": True,
    "does_not_score_reviewers": True,
    "does_not_resolve_disagreement": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_determine_winner": True,
    "does_not_identify_players": True,
    "does_not_ingest_media": True,
    "does_not_execute_sampling": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_claim_generalization": True,
}

CARD_WARNINGS = {
    "card_is_structural_count_only": True,
    "card_does_not_judge_correctness": True,
    "card_does_not_create_labels": True,
    "no_adjudication": True,
}


def export_review_ops_metrics_contract(
    *,
    output_path: str | Path | None = DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
    exported_at: datetime | None = None,
) -> dict[str, Any]:
    """Export the frozen review-ops metrics contract."""

    exported_at = exported_at or CONTRACT_EXPORTED_AT
    contract = _contract_payload(exported_at=exported_at)
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "contract_type": REVIEW_OPS_METRICS_CONTRACT_TYPE,
        "contract_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
        "report_type": REVIEW_OPS_METRICS_REPORT_TYPE,
        "report_version": REVIEW_OPS_METRICS_REPORT_VERSION,
        "dashboard_data_type": REVIEW_OPS_DASHBOARD_DATA_TYPE,
        "dashboard_data_version": REVIEW_OPS_DASHBOARD_DATA_VERSION,
        "contract": contract,
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(contract, indent=2, sort_keys=True), encoding="utf-8")
        result["contract_output"] = str(path)
    return result


def build_review_ops_metrics_report(
    *,
    contract_path: str | Path = DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
    corpus_manifest_path: str | Path | None = DEFAULT_DATASET_CORPUS_MANIFEST_OUTPUT,
    coverage_sampling_profile_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_PROFILE_OUTPUT
    ),
    coverage_sampling_report_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_REPORT_OUTPUT
    ),
    many_point_ingestion_gate_path: str | Path | None = (
        DEFAULT_MANY_POINT_INGESTION_GATE_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a read-only structural review operations metrics report."""

    generated_at = generated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="review_ops_metrics_contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    contract = _dict(contract_loaded["data"])
    contract_errors = _validate_contract_shape(contract)
    if contract_errors:
        return {
            "ok": False,
            "status": "invalid_review_ops_metrics_contract",
            "error_count": len(contract_errors),
            "errors": contract_errors,
            "warnings": dict(REVIEW_OPS_WARNINGS),
        }

    corpus_source = _load_optional_json(
        corpus_manifest_path,
        label="corpus_manifest",
        type_field="corpus_manifest_type",
        expected_type=DATASET_CORPUS_MANIFEST_TYPE,
        version_field="corpus_manifest_version",
        expected_version=DATASET_CORPUS_MANIFEST_VERSION,
    )
    coverage_profile_source = _load_optional_json(
        coverage_sampling_profile_path,
        label="coverage_sampling_profile",
        type_field="profile_type",
        expected_type=COVERAGE_SAMPLING_PROFILE_TYPE,
        version_field="profile_version",
        expected_version=COVERAGE_SAMPLING_PROFILE_VERSION,
    )
    coverage_report_source = _load_optional_json(
        coverage_sampling_report_path,
        label="coverage_sampling_report",
        type_field="report_type",
        expected_type=COVERAGE_SAMPLING_REPORT_TYPE,
        version_field="report_version",
        expected_version=COVERAGE_SAMPLING_REPORT_VERSION,
    )
    ingestion_gate_source = _load_optional_json(
        many_point_ingestion_gate_path,
        label="many_point_ingestion_gate",
        type_field="ingestion_gate_type",
        expected_type=MANY_POINT_INGESTION_GATE_TYPE,
        version_field="ingestion_gate_version",
        expected_version=MANY_POINT_INGESTION_GATE_VERSION,
    )
    sources = {
        "corpus_manifest": corpus_source,
        "coverage_sampling_profile": coverage_profile_source,
        "coverage_sampling_report": coverage_report_source,
        "many_point_ingestion_gate": ingestion_gate_source,
    }
    entries = _corpus_entries(_dict(corpus_source.get("data")))
    source_warnings = _source_warnings(sources)
    entry_metrics = [
        _entry_metrics(entry=entry, corpus_present=corpus_source.get("present") is True)
        for entry in entries
    ]
    counts = _summary_counts(
        entries=entries,
        entry_metrics=entry_metrics,
        coverage_profile=_dict(coverage_profile_source.get("data")),
        coverage_report=_dict(coverage_report_source.get("data")),
        ingestion_gate=_dict(ingestion_gate_source.get("data")),
    )
    metric_groups = _metric_groups(
        counts=counts,
        coverage_profile=_dict(coverage_profile_source.get("data")),
        coverage_report=_dict(coverage_report_source.get("data")),
        ingestion_gate=_dict(ingestion_gate_source.get("data")),
    )
    dashboard_cards = _dashboard_cards(counts=counts)
    report = {
        "report_type": REVIEW_OPS_METRICS_REPORT_TYPE,
        "report_version": REVIEW_OPS_METRICS_REPORT_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_paths": {
            "contract_path": str(Path(contract_path)),
            "corpus_manifest_path": _path_or_none(corpus_manifest_path),
            "coverage_sampling_profile_path": _path_or_none(coverage_sampling_profile_path),
            "coverage_sampling_report_path": _path_or_none(coverage_sampling_report_path),
            "many_point_ingestion_gate_path": _path_or_none(many_point_ingestion_gate_path),
        },
        "source_statuses": _source_statuses(sources),
        "source_contract_versions": _source_contract_refs(),
        "corpus_entry_count": len(entries),
        "entry_metrics": entry_metrics,
        "metric_groups": metric_groups,
        "dashboard_cards": dashboard_cards,
        "summary": counts,
        "coverage_gap_counts": _coverage_gap_counts(
            _dict(coverage_profile_source.get("data")),
            _dict(coverage_report_source.get("data")),
        ),
        "missing_optional_refs": _missing_optional_refs(entries=entries),
        "source_warnings": source_warnings,
        "known_limitations": _known_limitations(
            entry_count=len(entries),
            source_warnings=source_warnings,
        ),
        "validation_summary": {
            "status": "not_assessed",
            "structural_error_count": 0,
            "structural_warning_count": len(source_warnings),
            "validation_does_not_create_labels": True,
        },
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(REVIEW_OPS_WARNINGS),
            "report_is_structural_counts_only": True,
            "missing_optional_refs_are_gaps": True,
            "dashboard_data_is_read_only": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "report_type": REVIEW_OPS_METRICS_REPORT_TYPE,
        "report_version": REVIEW_OPS_METRICS_REPORT_VERSION,
        "corpus_entry_count": len(entries),
        "dashboard_card_count": len(dashboard_cards),
        "summary": counts,
        "report": report,
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        result["report_output"] = str(path)
    return result


def validate_review_ops_metrics_report(
    *,
    contract_path: str | Path = DEFAULT_REVIEW_OPS_METRICS_CONTRACT_OUTPUT,
    report_path: str | Path,
    observation_quality_taxonomy_path: str | Path | None = (
        DEFAULT_OBSERVATION_QUALITY_TAXONOMY_OUTPUT
    ),
    review_label_schema_path: str | Path | None = DEFAULT_REVIEW_LABEL_SCHEMA_OUTPUT,
    reviewer_confidence_schema_path: str | Path | None = (
        DEFAULT_REVIEWER_CONFIDENCE_SCHEMA_OUTPUT
    ),
    multi_reviewer_schema_path: str | Path | None = DEFAULT_MULTI_REVIEWER_SCHEMA_OUTPUT,
    intennse_alignment_contract_path: str | Path | None = (
        DEFAULT_INTENNSE_ALIGNMENT_CONTRACT_OUTPUT
    ),
    dataset_corpus_contract_path: str | Path | None = (
        DEFAULT_DATASET_CORPUS_CONTRACT_OUTPUT
    ),
    coverage_sampling_contract_path: str | Path | None = (
        DEFAULT_COVERAGE_SAMPLING_CONTRACT_OUTPUT
    ),
    many_point_ingestion_contract_path: str | Path | None = (
        DEFAULT_MANY_POINT_INGESTION_CONTRACT_OUTPUT
    ),
    output_path: str | Path | None = DEFAULT_REVIEW_OPS_METRICS_VALIDATION_OUTPUT,
    validated_at: datetime | None = None,
) -> dict[str, Any]:
    """Validate a review-ops report structurally without interpreting labels."""

    validated_at = validated_at or datetime.now(UTC)
    contract_loaded = _load_json(contract_path, label="review_ops_metrics_contract")
    if contract_loaded.get("ok") is False:
        return contract_loaded
    report_loaded = _load_json(report_path, label="review_ops_metrics_report")
    if report_loaded.get("ok") is False:
        return report_loaded

    contract = _dict(contract_loaded["data"])
    report = _dict(report_loaded["data"])
    errors = _validate_contract_shape(contract)
    structural_warnings: list[dict[str, Any]] = []
    contract_validations: list[dict[str, Any]] = []
    if not errors:
        contract_result = _validate_referenced_contracts(
            observation_quality_taxonomy_path=observation_quality_taxonomy_path,
            review_label_schema_path=review_label_schema_path,
            reviewer_confidence_schema_path=reviewer_confidence_schema_path,
            multi_reviewer_schema_path=multi_reviewer_schema_path,
            intennse_alignment_contract_path=intennse_alignment_contract_path,
            dataset_corpus_contract_path=dataset_corpus_contract_path,
            coverage_sampling_contract_path=coverage_sampling_contract_path,
            many_point_ingestion_contract_path=many_point_ingestion_contract_path,
        )
        errors.extend(_list(contract_result.get("errors")))
        structural_warnings.extend(_list(contract_result.get("structural_warnings")))
        contract_validations.extend(_list(contract_result.get("validations")))
        report_result = _validate_report_shape(report=report)
        errors.extend(_list(report_result.get("errors")))
        structural_warnings.extend(_list(report_result.get("structural_warnings")))

    result: dict[str, Any] = {
        "ok": not errors,
        "status": "valid" if not errors else "invalid",
        "validation_type": "review_ops_metrics_report_validation",
        "validation_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
        "validated_at": validated_at.isoformat(),
        "contract_path": str(Path(contract_path)),
        "report_path": str(Path(report_path)),
        "contract_type": REVIEW_OPS_METRICS_CONTRACT_TYPE,
        "contract_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
        "report_type": REVIEW_OPS_METRICS_REPORT_TYPE,
        "report_version": REVIEW_OPS_METRICS_REPORT_VERSION,
        "error_count": len(errors),
        "errors": errors,
        "structural_warning_count": len(structural_warnings),
        "structural_warnings": structural_warnings,
        "referenced_contract_validations": contract_validations,
        "warnings": dict(REVIEW_OPS_WARNINGS),
        "known_limitations": [
            "Validation checks contract, report, dashboard-card, and status shape only.",
            "Validation reports missing optional review and alignment artifacts as gaps.",
            "Validation does not infer missing labels.",
            "Validation does not create labels.",
            "Validation does not judge correctness.",
            "Validation does not rank reviewers.",
            "Validation does not resolve reviewer disagreement.",
            "Validation does not create training truth.",
        ],
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["validation_output"] = str(path)
    return result


def build_review_ops_dashboard_data(
    *,
    report_path: str | Path = DEFAULT_REVIEW_OPS_METRICS_REPORT_OUTPUT,
    output_path: str | Path | None = DEFAULT_REVIEW_OPS_DASHBOARD_DATA_OUTPUT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build read-only JSON data suitable for a review-ops dashboard."""

    generated_at = generated_at or datetime.now(UTC)
    report_loaded = _load_json(report_path, label="review_ops_metrics_report")
    if report_loaded.get("ok") is False:
        return report_loaded
    report = _dict(report_loaded["data"])
    data = {
        "dashboard_data_type": REVIEW_OPS_DASHBOARD_DATA_TYPE,
        "dashboard_data_version": REVIEW_OPS_DASHBOARD_DATA_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_report_path": str(Path(report_path)),
        "source_paths": _dict(report.get("source_paths")),
        "cards": _list(report.get("dashboard_cards")),
        "metric_groups": _list(report.get("metric_groups")),
        "summary": _dict(report.get("summary")),
        "coverage_gap_counts": _dict(report.get("coverage_gap_counts")),
        "missing_optional_refs": _dict(report.get("missing_optional_refs")),
        "source_warnings": _list(report.get("source_warnings")),
        "read_only": True,
        "tom_provenance": _tom_provenance(),
        "warnings": {
            **dict(REVIEW_OPS_WARNINGS),
            "dashboard_data_does_not_mutate_sources": True,
            "dashboard_data_does_not_create_labels": True,
        },
    }
    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "dashboard_data_type": REVIEW_OPS_DASHBOARD_DATA_TYPE,
        "dashboard_data_version": REVIEW_OPS_DASHBOARD_DATA_VERSION,
        "card_count": len(data["cards"]),
        "dashboard_data": data,
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        result["dashboard_data_output"] = str(path)
    return result


def _contract_payload(*, exported_at: datetime) -> dict[str, Any]:
    return {
        "contract_type": REVIEW_OPS_METRICS_CONTRACT_TYPE,
        "contract_version": REVIEW_OPS_METRICS_CONTRACT_VERSION,
        "exported_at": exported_at.isoformat(),
        "report_type": REVIEW_OPS_METRICS_REPORT_TYPE,
        "report_version": REVIEW_OPS_METRICS_REPORT_VERSION,
        "dashboard_data_type": REVIEW_OPS_DASHBOARD_DATA_TYPE,
        "dashboard_data_version": REVIEW_OPS_DASHBOARD_DATA_VERSION,
        "metrics_scope": {
            "purpose": (
                "Summarize structural review operations progress, coverage gaps, "
                "provenance completeness, and dashboard-ready counts."
            ),
            "operations_visibility_only": True,
            "read_only": True,
            "label_creation_allowed": False,
            "confidence_score_generation_allowed": False,
            "reviewer_ranking_allowed": False,
            "reviewer_quality_scoring_allowed": False,
            "disagreement_resolution_allowed": False,
            "truth_inference_allowed": False,
            "training_truth_allowed": False,
            "media_ingestion_allowed": False,
            "sampling_execution_allowed": False,
            "event_generation_allowed": False,
            "three_d_generation_allowed": False,
            "generalization_claim_allowed": False,
        },
        "source_contract_refs": _source_contract_refs(),
        "metric_groups": [_metric_group_definition(group) for group in METRIC_GROUPS],
        "allowed_metric_status_values": list(ALLOWED_METRIC_STATUS_VALUES),
        "forbidden_metric_status_terms": sorted(FORBIDDEN_METRIC_STATUS_TERMS),
        "dashboard_card_schema": {
            "required_fields": [
                "card_id",
                "label",
                "value",
                "status",
                "metric_group",
                "warnings",
            ],
            "allowed_card_ids": list(DASHBOARD_CARD_IDS),
            "allowed_status_values": list(ALLOWED_METRIC_STATUS_VALUES),
            "read_only": True,
        },
        "report_schema": {
            "required_fields": [
                "report_type",
                "report_version",
                "generated_at",
                "source_paths",
                "source_contract_versions",
                "corpus_entry_count",
                "metric_groups",
                "dashboard_cards",
                "warnings",
                "validation_summary",
            ],
            "metric_groups_required": list(METRIC_GROUPS),
            "dashboard_cards_required": list(DASHBOARD_CARD_IDS),
            "structural_counts_only": True,
        },
        "provenance_requirements": {
            "source_paths_preserved": True,
            "source_contract_versions_preserved": True,
            "missing_optional_refs_reported_as_gaps": True,
            "source_warnings_preserved_when_available": True,
            "dashboard_cards_preserve_source_metric_group": True,
        },
        "validation_rules": {
            "structural_validation_only": True,
            "contract_shape_validated": True,
            "report_shape_validated": True,
            "dashboard_card_schema_validated": True,
            "allowed_status_values_only": True,
            "referenced_contract_versions_validated_when_paths_available": True,
            "missing_optional_refs_are_structural_warnings": True,
            "does_not_infer_missing_labels": True,
            "does_not_create_labels": True,
            "does_not_create_confidence_scores": True,
            "does_not_rank_reviewers": True,
            "does_not_score_reviewers": True,
            "does_not_resolve_disagreement": True,
            "does_not_create_truth": True,
            "does_not_create_training_truth": True,
            "does_not_ingest_media": True,
            "does_not_execute_sampling": True,
            "forbidden_fields": sorted(FORBIDDEN_REVIEW_OPS_FIELDS),
        },
        "tom_provenance": _tom_provenance(),
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }


def _source_contract_refs() -> dict[str, str]:
    return {
        "observation_quality_taxonomy_version": OBSERVATION_QUALITY_TAXONOMY_VERSION,
        "review_label_schema_version": REVIEW_LABEL_SCHEMA_VERSION,
        "reviewer_confidence_schema_version": REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        "multi_reviewer_disagreement_schema_version": MULTI_REVIEWER_SCHEMA_VERSION,
        "intennse_label_alignment_contract_version": INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        "versioned_dataset_corpus_contract_version": DATASET_CORPUS_CONTRACT_VERSION,
        "coverage_sampling_strategy_contract_version": COVERAGE_SAMPLING_CONTRACT_VERSION,
        "many_point_ingestion_gate_contract_version": MANY_POINT_INGESTION_CONTRACT_VERSION,
        "multi_point_regression_matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_manifest_version": POINT_MANIFEST_VERSION,
    }


def _metric_group_definition(group: str) -> dict[str, Any]:
    return {
        "key": group,
        "allowed_status_values": list(ALLOWED_METRIC_STATUS_VALUES),
        "structural_counts_only": True,
        "read_only": True,
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }


def _corpus_entries(corpus_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    entries = corpus_manifest.get("corpus_entries")
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def _entry_metrics(*, entry: dict[str, Any], corpus_present: bool) -> dict[str, Any]:
    evidence = _bool_dict(entry.get("evidence_availability"))
    labels = _string_list(entry.get("labels"))
    review_label_refs = _list(entry.get("review_label_bundle_refs"))
    confidence_refs = _list(entry.get("reviewer_confidence_bundle_refs"))
    multi_reviewer_refs = _list(entry.get("multi_reviewer_review_set_refs"))
    disagreement_refs = _list(entry.get("disagreement_report_refs"))
    intennse_refs = _list(entry.get("intennse_alignment_refs"))
    quality_profile = _string_or_none(entry.get("observation_quality_profile_path"))
    provenance_status = _string_or_none(entry.get("provenance_status")) or "not_assessed"
    requires_human_review = _requires_human_review(
        entry=entry,
        review_label_refs=review_label_refs,
        confidence_refs=confidence_refs,
    )
    readiness = _ingestion_readiness(entry=entry, evidence=evidence)
    return {
        "corpus_entry_id": _string_or_none(entry.get("corpus_entry_id")),
        "point_manifest_id": _string_or_none(entry.get("point_manifest_id")),
        "media_id": _string_or_none(entry.get("media_id")),
        "labels": labels,
        "statuses": {
            "corpus_entry": "present" if corpus_present else "missing",
            "replay": _present_if(
                evidence.get("replay_available") is True
                or _string_or_none(entry.get("replay_url")) is not None
            ),
            "point_manifest": _present_if(
                _string_or_none(entry.get("point_manifest_id")) is not None
            ),
            "review_label_bundle": _present_if(bool(review_label_refs)),
            "reviewer_confidence_bundle": _present_if(bool(confidence_refs)),
            "multi_reviewer_review": _present_if(bool(multi_reviewer_refs)),
            "disagreement_report": _present_if(bool(disagreement_refs)),
            "intennse_alignment": _present_if(bool(intennse_refs)),
            "observation_quality_profile": _present_if(quality_profile is not None),
            "provenance": _provenance_status(provenance_status),
            "human_review": (
                "requires_human_review" if requires_human_review else "not_assessed"
            ),
            "ingestion_readiness": readiness,
            "regression_protection": (
                "present" if "protected_sample_point" in labels else "not_applicable"
            ),
        },
        "source_warnings": _bool_dict(entry.get("warnings")),
        "warnings": {
            **dict(CARD_WARNINGS),
            "entry_metrics_are_structural_only": True,
            "missing_review_label_bundle": not bool(review_label_refs),
            "missing_reviewer_confidence_bundle": not bool(confidence_refs),
        },
    }


def _summary_counts(
    *,
    entries: list[dict[str, Any]],
    entry_metrics: list[dict[str, Any]],
    coverage_profile: dict[str, Any],
    coverage_report: dict[str, Any],
    ingestion_gate: dict[str, Any],
) -> dict[str, int]:
    counts = {
        "total_corpus_entries": len(entries),
        "replay_available_entries": 0,
        "entries_with_point_manifest": 0,
        "entries_with_review_label_bundle": 0,
        "entries_with_reviewer_confidence_bundle": 0,
        "entries_with_multi_reviewer_review": 0,
        "entries_with_disagreement_report": 0,
        "entries_with_intennse_alignment": 0,
        "entries_with_observation_quality_profile": 0,
        "entries_with_provenance_partial": 0,
        "entries_with_provenance_present": 0,
        "entries_requiring_human_review": 0,
        "regression_protected_entries": 0,
        "ingestion_ready_entries": 0,
        "coverage_gap_counts": sum(
            _coverage_gap_counts(coverage_profile, coverage_report).values()
        ),
        "ingestion_gate_entries": int(ingestion_gate.get("entry_count") or 0),
        "ingestion_gate_indexed_entries": int(ingestion_gate.get("indexed_entry_count") or 0),
    }
    for metric in entry_metrics:
        statuses = _dict(metric.get("statuses"))
        counts["replay_available_entries"] += statuses.get("replay") == "present"
        counts["entries_with_point_manifest"] += statuses.get("point_manifest") == "present"
        counts["entries_with_review_label_bundle"] += (
            statuses.get("review_label_bundle") == "present"
        )
        counts["entries_with_reviewer_confidence_bundle"] += (
            statuses.get("reviewer_confidence_bundle") == "present"
        )
        counts["entries_with_multi_reviewer_review"] += (
            statuses.get("multi_reviewer_review") == "present"
        )
        counts["entries_with_disagreement_report"] += (
            statuses.get("disagreement_report") == "present"
        )
        counts["entries_with_intennse_alignment"] += (
            statuses.get("intennse_alignment") == "present"
        )
        counts["entries_with_observation_quality_profile"] += (
            statuses.get("observation_quality_profile") == "present"
        )
        counts["entries_with_provenance_partial"] += (
            statuses.get("provenance") == "provenance_partial"
        )
        counts["entries_with_provenance_present"] += (
            statuses.get("provenance") == "provenance_present"
        )
        counts["entries_requiring_human_review"] += (
            statuses.get("human_review") == "requires_human_review"
        )
        counts["regression_protected_entries"] += (
            statuses.get("regression_protection") == "present"
        )
        counts["ingestion_ready_entries"] += (
            statuses.get("ingestion_readiness") == "structurally_ready"
        )
    return {key: int(value) for key, value in counts.items()}


def _metric_groups(
    *,
    counts: dict[str, int],
    coverage_profile: dict[str, Any],
    coverage_report: dict[str, Any],
    ingestion_gate: dict[str, Any],
) -> list[dict[str, Any]]:
    gap_counts = _coverage_gap_counts(coverage_profile, coverage_report)
    groups = [
        _group(
            "corpus_entry_counts",
            {
                "total_corpus_entries": counts["total_corpus_entries"],
                "replay_available_entries": counts["replay_available_entries"],
                "entries_with_point_manifest": counts["entries_with_point_manifest"],
            },
            _status_for_count(counts["total_corpus_entries"]),
        ),
        _coverage_group(
            "review_label_coverage",
            "entries_with_review_label_bundle",
            counts,
        ),
        _coverage_group(
            "reviewer_confidence_coverage",
            "entries_with_reviewer_confidence_bundle",
            counts,
        ),
        _coverage_group(
            "multi_reviewer_coverage",
            "entries_with_multi_reviewer_review",
            counts,
        ),
        _coverage_group(
            "disagreement_report_coverage",
            "entries_with_disagreement_report",
            counts,
        ),
        _coverage_group(
            "intennse_alignment_coverage",
            "entries_with_intennse_alignment",
            counts,
        ),
        _coverage_group(
            "observation_quality_coverage",
            "entries_with_observation_quality_profile",
            counts,
        ),
        _group(
            "provenance_completeness",
            {
                "entries_with_provenance_present": counts[
                    "entries_with_provenance_present"
                ],
                "entries_with_provenance_partial": counts[
                    "entries_with_provenance_partial"
                ],
            },
            (
                "provenance_present"
                if counts["entries_with_provenance_present"] == counts[
                    "total_corpus_entries"
                ]
                and counts["total_corpus_entries"]
                else "provenance_partial"
                if counts["entries_with_provenance_partial"]
                else "not_assessed"
            ),
        ),
        _group(
            "ingestion_gate_readiness",
            {
                "ingestion_ready_entries": counts["ingestion_ready_entries"],
                "ingestion_gate_entries": counts["ingestion_gate_entries"],
                "ingestion_gate_indexed_entries": counts[
                    "ingestion_gate_indexed_entries"
                ],
                "ingestion_gate_dry_run": ingestion_gate.get("mode") == "dry_run",
            },
            _coverage_status(counts["ingestion_ready_entries"], counts["total_corpus_entries"]),
        ),
        _group(
            "coverage_sampling_gaps",
            dict(gap_counts),
            "coverage_gap_present" if gap_counts else "not_applicable",
        ),
        _group(
            "regression_protection_coverage",
            {"regression_protected_entries": counts["regression_protected_entries"]},
            _coverage_status(
                counts["regression_protected_entries"],
                counts["total_corpus_entries"],
            ),
        ),
        _group(
            "missing_optional_refs",
            {
                "missing_review_label_refs": counts["total_corpus_entries"]
                - counts["entries_with_review_label_bundle"],
                "missing_reviewer_confidence_refs": counts["total_corpus_entries"]
                - counts["entries_with_reviewer_confidence_bundle"],
                "missing_multi_reviewer_refs": counts["total_corpus_entries"]
                - counts["entries_with_multi_reviewer_review"],
                "missing_disagreement_refs": counts["total_corpus_entries"]
                - counts["entries_with_disagreement_report"],
                "missing_intennse_alignment_refs": counts["total_corpus_entries"]
                - counts["entries_with_intennse_alignment"],
            },
            "coverage_gap_present"
            if counts["total_corpus_entries"]
            and counts["entries_with_review_label_bundle"] < counts["total_corpus_entries"]
            else "not_applicable",
        ),
        _group(
            "human_review_required_counts",
            {"entries_requiring_human_review": counts["entries_requiring_human_review"]},
            "requires_human_review"
            if counts["entries_requiring_human_review"]
            else "not_assessed",
        ),
    ]
    return groups


def _coverage_group(
    group_id: str,
    count_key: str,
    counts: dict[str, int],
) -> dict[str, Any]:
    total = counts["total_corpus_entries"]
    present = counts[count_key]
    return _group(
        group_id,
        {
            count_key: present,
            "missing_entry_count": max(total - present, 0),
        },
        _coverage_status(present, total),
    )


def _group(group_id: str, metrics: dict[str, Any], status: str) -> dict[str, Any]:
    return {
        "group_id": group_id,
        "status": status,
        "metrics": metrics,
        "structural_counts_only": True,
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }


def _dashboard_cards(*, counts: dict[str, int]) -> list[dict[str, Any]]:
    total = counts["total_corpus_entries"]
    return [
        _card("total_corpus_entries", "Total corpus entries", total, _status_for_count(total)),
        _card(
            "replay_available_entries",
            "Replay available entries",
            counts["replay_available_entries"],
            _coverage_status(counts["replay_available_entries"], total),
        ),
        _card(
            "entries_with_point_manifest",
            "Entries with point manifest",
            counts["entries_with_point_manifest"],
            _coverage_status(counts["entries_with_point_manifest"], total),
        ),
        _card(
            "entries_with_review_label_bundle",
            "Entries with review label bundle",
            counts["entries_with_review_label_bundle"],
            _coverage_status(counts["entries_with_review_label_bundle"], total),
        ),
        _card(
            "entries_with_reviewer_confidence_bundle",
            "Entries with reviewer confidence bundle",
            counts["entries_with_reviewer_confidence_bundle"],
            _coverage_status(counts["entries_with_reviewer_confidence_bundle"], total),
        ),
        _card(
            "entries_with_multi_reviewer_review",
            "Entries with multi-reviewer review",
            counts["entries_with_multi_reviewer_review"],
            _coverage_status(counts["entries_with_multi_reviewer_review"], total),
        ),
        _card(
            "entries_with_disagreement_report",
            "Entries with disagreement report",
            counts["entries_with_disagreement_report"],
            _coverage_status(counts["entries_with_disagreement_report"], total),
        ),
        _card(
            "entries_with_intennse_alignment",
            "Entries with INTENNSE alignment",
            counts["entries_with_intennse_alignment"],
            _coverage_status(counts["entries_with_intennse_alignment"], total),
        ),
        _card(
            "entries_with_provenance_partial",
            "Entries with partial provenance",
            counts["entries_with_provenance_partial"],
            "provenance_partial"
            if counts["entries_with_provenance_partial"]
            else "not_applicable",
            metric_group="provenance_completeness",
        ),
        _card(
            "entries_requiring_human_review",
            "Entries requiring human review",
            counts["entries_requiring_human_review"],
            "requires_human_review"
            if counts["entries_requiring_human_review"]
            else "not_assessed",
            metric_group="human_review_required_counts",
        ),
        _card(
            "regression_protected_entries",
            "Regression protected entries",
            counts["regression_protected_entries"],
            _coverage_status(counts["regression_protected_entries"], total),
            metric_group="regression_protection_coverage",
        ),
        _card(
            "ingestion_ready_entries",
            "Ingestion ready entries",
            counts["ingestion_ready_entries"],
            _coverage_status(counts["ingestion_ready_entries"], total),
            metric_group="ingestion_gate_readiness",
        ),
        _card(
            "coverage_gap_counts",
            "Coverage gap counts",
            counts["coverage_gap_counts"],
            "coverage_gap_present" if counts["coverage_gap_counts"] else "not_applicable",
            metric_group="coverage_sampling_gaps",
        ),
    ]


def _card(
    card_id: str,
    label: str,
    value: int,
    status: str,
    *,
    metric_group: str | None = None,
) -> dict[str, Any]:
    return {
        "card_id": card_id,
        "label": label,
        "value": int(value),
        "status": status,
        "metric_group": metric_group or _card_group(card_id),
        "warnings": dict(CARD_WARNINGS),
    }


def _card_group(card_id: str) -> str:
    if card_id in {
        "total_corpus_entries",
        "replay_available_entries",
        "entries_with_point_manifest",
    }:
        return "corpus_entry_counts"
    if card_id == "entries_with_review_label_bundle":
        return "review_label_coverage"
    if card_id == "entries_with_reviewer_confidence_bundle":
        return "reviewer_confidence_coverage"
    if card_id == "entries_with_multi_reviewer_review":
        return "multi_reviewer_coverage"
    if card_id == "entries_with_disagreement_report":
        return "disagreement_report_coverage"
    if card_id == "entries_with_intennse_alignment":
        return "intennse_alignment_coverage"
    return "corpus_entry_counts"


def _coverage_gap_counts(
    coverage_profile: dict[str, Any],
    coverage_report: dict[str, Any],
) -> dict[str, int]:
    source = _dict(coverage_profile.get("coverage_gap_summary")) or _dict(
        coverage_report.get("coverage_gap_summary")
    )
    return {str(key): int(value) for key, value in source.items() if _is_int_like(value)}


def _missing_optional_refs(*, entries: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter()
    for entry in entries:
        if not _list(entry.get("review_label_bundle_refs")):
            counts["review_label_bundle_refs"] += 1
        if not _list(entry.get("reviewer_confidence_bundle_refs")):
            counts["reviewer_confidence_bundle_refs"] += 1
        if not _list(entry.get("multi_reviewer_review_set_refs")):
            counts["multi_reviewer_review_set_refs"] += 1
        if not _list(entry.get("disagreement_report_refs")):
            counts["disagreement_report_refs"] += 1
        if not _list(entry.get("intennse_alignment_refs")):
            counts["intennse_alignment_refs"] += 1
        if _string_or_none(entry.get("observation_quality_profile_path")) is None:
            counts["observation_quality_profile_path"] += 1
        for gap in _string_list(entry.get("provenance_gaps")):
            counts[gap] += 1
    return dict(sorted(counts.items()))


def _requires_human_review(
    *,
    entry: dict[str, Any],
    review_label_refs: list[Any],
    confidence_refs: list[Any],
) -> bool:
    return (
        entry.get("requires_human_review") == "required"
        or not review_label_refs
        or not confidence_refs
    )


def _ingestion_readiness(*, entry: dict[str, Any], evidence: dict[str, bool]) -> str:
    if (
        evidence.get("media_indexed") is True
        and (
            evidence.get("replay_available") is True
            or _string_or_none(entry.get("replay_url")) is not None
        )
        and _string_or_none(entry.get("point_manifest_id")) is not None
    ):
        return "structurally_ready"
    return "structurally_blocked"


def _present_if(value: bool) -> str:
    return "present" if value else "missing"


def _status_for_count(value: int) -> str:
    return "present" if value else "missing"


def _coverage_status(present: int, total: int) -> str:
    if total <= 0:
        return "missing"
    if present <= 0:
        return "missing"
    if present == total:
        return "present"
    return "partial"


def _provenance_status(status: str) -> str:
    if status in {"provenance_present", "provenance_partial", "provenance_missing"}:
        return status
    if status == "present":
        return "provenance_present"
    if status == "partial":
        return "provenance_partial"
    if status == "missing":
        return "provenance_missing"
    return "not_assessed"


def _known_limitations(
    *,
    entry_count: int,
    source_warnings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    limitations = [
        {
            "limitation_type": "structural_metrics_only",
            "description": "Metrics report artifact presence and gaps only.",
            "not_generalization_claim": True,
        }
    ]
    if entry_count <= 1:
        limitations.append(
            {
                "limitation_type": "demo_or_single_point_limited",
                "description": "Current corpus size does not prove many real points.",
                "not_generalization_claim": True,
            }
        )
    if source_warnings:
        limitations.append(
            {
                "limitation_type": "source_gap_present",
                "description": "At least one optional source was missing or structurally partial.",
                "not_generalization_claim": True,
            }
        )
    return limitations


def _validate_contract_shape(contract: dict[str, Any]) -> list[dict[str, Any]]:
    errors = _forbidden_field_errors(contract, path="contract")
    if contract.get("contract_type") != REVIEW_OPS_METRICS_CONTRACT_TYPE:
        errors.append(
            _error("invalid_contract_type", "contract_type", contract.get("contract_type"))
        )
    if contract.get("contract_version") != REVIEW_OPS_METRICS_CONTRACT_VERSION:
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
        "metric_groups",
        "dashboard_card_schema",
        "report_schema",
        "validation_rules",
        "provenance_requirements",
        "warnings",
    ):
        if section not in contract:
            errors.append(_error("missing_contract_section", section, None))
    if errors:
        return errors

    errors.extend(_source_contract_ref_errors(_dict(contract.get("source_contract_refs"))))
    contract_groups = {
        item.get("key")
        for item in _list(contract.get("metric_groups"))
        if isinstance(item, dict)
    }
    if set(contract_groups) != set(METRIC_GROUPS):
        errors.append(
            _error(
                "invalid_metric_groups",
                "metric_groups",
                sorted(set(METRIC_GROUPS) ^ set(contract_groups)),
            )
        )
    card_schema = _dict(contract.get("dashboard_card_schema"))
    if set(_string_list(card_schema.get("allowed_card_ids"))) != set(DASHBOARD_CARD_IDS):
        errors.append(
            _error(
                "invalid_dashboard_card_ids",
                "dashboard_card_schema.allowed_card_ids",
                card_schema.get("allowed_card_ids"),
            )
        )
    if set(_string_list(contract.get("allowed_metric_status_values"))) != set(
        ALLOWED_METRIC_STATUS_VALUES
    ):
        errors.append(
            _error(
                "invalid_allowed_metric_status_values",
                "allowed_metric_status_values",
                contract.get("allowed_metric_status_values"),
            )
        )
    rules = _dict(contract.get("validation_rules"))
    for rule in (
        "structural_validation_only",
        "contract_shape_validated",
        "report_shape_validated",
        "dashboard_card_schema_validated",
        "allowed_status_values_only",
        "referenced_contract_versions_validated_when_paths_available",
        "does_not_infer_missing_labels",
        "does_not_create_labels",
        "does_not_create_confidence_scores",
        "does_not_rank_reviewers",
        "does_not_score_reviewers",
        "does_not_resolve_disagreement",
        "does_not_create_truth",
        "does_not_create_training_truth",
        "does_not_ingest_media",
        "does_not_execute_sampling",
    ):
        if rules.get(rule) is not True:
            errors.append(
                _error("invalid_validation_rule", f"validation_rules.{rule}", rules.get(rule))
            )
    return errors


def _validate_report_shape(*, report: dict[str, Any]) -> dict[str, Any]:
    errors = _forbidden_field_errors(report, path="review_ops_metrics_report")
    structural_warnings: list[dict[str, Any]] = []
    if report.get("report_type") != REVIEW_OPS_METRICS_REPORT_TYPE:
        errors.append(_error("invalid_report_type", "report_type", report.get("report_type")))
    if report.get("report_version") != REVIEW_OPS_METRICS_REPORT_VERSION:
        errors.append(
            _error("invalid_report_version", "report_version", report.get("report_version"))
        )
    errors.extend(
        _source_contract_ref_errors(_dict(report.get("source_contract_versions")))
    )
    for field in (
        "generated_at",
        "source_paths",
        "corpus_entry_count",
        "metric_groups",
        "dashboard_cards",
        "warnings",
        "validation_summary",
    ):
        if field not in report:
            errors.append(_error("missing_report_field", field, None))
    groups = _list(report.get("metric_groups"))
    group_ids = {item.get("group_id") for item in groups if isinstance(item, dict)}
    if group_ids != set(METRIC_GROUPS):
        errors.append(
            _error("invalid_report_metric_groups", "metric_groups", sorted(group_ids))
        )
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            errors.append(
                _error("metric_group_must_be_object", f"metric_groups[{index}]", group)
            )
            continue
        status = _string_or_none(group.get("status"))
        if status not in ALLOWED_METRIC_STATUS_VALUES:
            errors.append(
                _error(
                    "invalid_metric_group_status",
                    f"metric_groups[{index}].status",
                    status,
                )
            )
    cards = _list(report.get("dashboard_cards"))
    card_ids = {item.get("card_id") for item in cards if isinstance(item, dict)}
    if card_ids != set(DASHBOARD_CARD_IDS):
        errors.append(
            _error("invalid_dashboard_cards", "dashboard_cards", sorted(card_ids))
        )
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            errors.append(
                _error(
                    "dashboard_card_must_be_object",
                    f"dashboard_cards[{index}]",
                    card,
                )
            )
            continue
        card_result = _validate_dashboard_card(card=card, path=f"dashboard_cards[{index}]")
        errors.extend(_list(card_result.get("errors")))
    if _list(report.get("source_warnings")):
        structural_warnings.append(
            {
                "warning_type": "source_gap_present",
                "path": "source_warnings",
                "structural_only": True,
            }
        )
    missing_optional = _dict(report.get("missing_optional_refs"))
    if any(int(value) > 0 for value in missing_optional.values() if _is_int_like(value)):
        structural_warnings.append(
            {
                "warning_type": "missing_optional_refs",
                "path": "missing_optional_refs",
                "structural_only": True,
            }
        )
    return {"errors": errors, "structural_warnings": structural_warnings}


def _validate_dashboard_card(*, card: dict[str, Any], path: str) -> dict[str, Any]:
    errors = _forbidden_field_errors(card, path=path)
    for field in ("card_id", "label", "value", "status", "metric_group", "warnings"):
        if field not in card:
            errors.append(_error("missing_dashboard_card_field", f"{path}.{field}", None))
    if _string_or_none(card.get("card_id")) not in DASHBOARD_CARD_IDS:
        errors.append(
            _error("invalid_dashboard_card_id", f"{path}.card_id", card.get("card_id"))
        )
    status = _string_or_none(card.get("status"))
    if status not in ALLOWED_METRIC_STATUS_VALUES:
        errors.append(_error("invalid_dashboard_card_status", f"{path}.status", status))
    if status in FORBIDDEN_METRIC_STATUS_TERMS:
        errors.append(_error("forbidden_dashboard_card_status", f"{path}.status", status))
    if _string_or_none(card.get("metric_group")) not in METRIC_GROUPS:
        errors.append(
            _error(
                "invalid_dashboard_card_metric_group",
                f"{path}.metric_group",
                card.get("metric_group"),
            )
        )
    return {"errors": errors}


def _validate_referenced_contracts(
    *,
    observation_quality_taxonomy_path: str | Path | None,
    review_label_schema_path: str | Path | None,
    reviewer_confidence_schema_path: str | Path | None,
    multi_reviewer_schema_path: str | Path | None,
    intennse_alignment_contract_path: str | Path | None,
    dataset_corpus_contract_path: str | Path | None,
    coverage_sampling_contract_path: str | Path | None,
    many_point_ingestion_contract_path: str | Path | None,
) -> dict[str, Any]:
    specs = [
        (
            "observation_quality_taxonomy",
            observation_quality_taxonomy_path,
            "taxonomy_type",
            OBSERVATION_QUALITY_TAXONOMY_TYPE,
            "taxonomy_version",
            OBSERVATION_QUALITY_TAXONOMY_VERSION,
        ),
        (
            "review_label_schema",
            review_label_schema_path,
            "schema_type",
            REVIEW_LABEL_SCHEMA_TYPE,
            "schema_version",
            REVIEW_LABEL_SCHEMA_VERSION,
        ),
        (
            "reviewer_confidence_schema",
            reviewer_confidence_schema_path,
            "schema_type",
            REVIEWER_CONFIDENCE_SCHEMA_TYPE,
            "schema_version",
            REVIEWER_CONFIDENCE_SCHEMA_VERSION,
        ),
        (
            "multi_reviewer_disagreement_schema",
            multi_reviewer_schema_path,
            "schema_type",
            MULTI_REVIEWER_SCHEMA_TYPE,
            "schema_version",
            MULTI_REVIEWER_SCHEMA_VERSION,
        ),
        (
            "intennse_alignment_contract",
            intennse_alignment_contract_path,
            "contract_type",
            INTENNSE_ALIGNMENT_CONTRACT_TYPE,
            "contract_version",
            INTENNSE_ALIGNMENT_CONTRACT_VERSION,
        ),
        (
            "versioned_dataset_corpus_contract",
            dataset_corpus_contract_path,
            "contract_type",
            DATASET_CORPUS_CONTRACT_TYPE,
            "contract_version",
            DATASET_CORPUS_CONTRACT_VERSION,
        ),
        (
            "coverage_sampling_strategy_contract",
            coverage_sampling_contract_path,
            "contract_type",
            COVERAGE_SAMPLING_CONTRACT_TYPE,
            "contract_version",
            COVERAGE_SAMPLING_CONTRACT_VERSION,
        ),
        (
            "many_point_ingestion_gate_contract",
            many_point_ingestion_contract_path,
            "contract_type",
            MANY_POINT_INGESTION_CONTRACT_TYPE,
            "contract_version",
            MANY_POINT_INGESTION_CONTRACT_VERSION,
        ),
    ]
    errors: list[dict[str, Any]] = []
    structural_warnings: list[dict[str, Any]] = []
    validations: list[dict[str, Any]] = []
    for label, path, type_field, expected_type, version_field, expected_version in specs:
        validation = _validate_contract_file(
            label=label,
            path=path,
            type_field=type_field,
            expected_type=expected_type,
            version_field=version_field,
            expected_version=expected_version,
        )
        validations.append(validation)
        if validation.get("ok") is False:
            if validation.get("missing") is True:
                structural_warnings.append(
                    {
                        "warning_type": "missing_referenced_contract",
                        "label": label,
                        "path": _path_or_none(path),
                        "structural_only": True,
                    }
                )
            else:
                errors.append(
                    _error("invalid_referenced_contract", label, validation)
                )
    return {
        "errors": errors,
        "structural_warnings": structural_warnings,
        "validations": validations,
    }


def _validate_contract_file(
    *,
    label: str,
    path: str | Path | None,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {"ok": False, "label": label, "path": None, "missing": True}
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return {"ok": False, "label": label, "path": str(file_path), "missing": True}
    loaded = _load_json(file_path, label=label)
    if loaded.get("ok") is False:
        return {"ok": False, "label": label, "path": str(file_path), "error": loaded}
    data = _dict(loaded.get("data"))
    return {
        "ok": data.get(type_field) == expected_type
        and data.get(version_field) == expected_version,
        "label": label,
        "path": str(file_path),
        "type_field": type_field,
        "type_value": data.get(type_field),
        "expected_type": expected_type,
        "version_field": version_field,
        "version_value": data.get(version_field),
        "expected_version": expected_version,
    }


def _source_contract_ref_errors(refs: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    expected = _source_contract_refs()
    for key, value in expected.items():
        if refs.get(key) != value:
            errors.append(_error("invalid_source_contract_ref", key, refs.get(key)))
    return errors


def _load_optional_json(
    path: str | Path | None,
    *,
    label: str,
    type_field: str,
    expected_type: str,
    version_field: str,
    expected_version: str,
) -> dict[str, Any]:
    if path is None or not str(path).strip():
        return {"ok": True, "present": False, "data": {}, "warning": "source_not_supplied"}
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return {
            "ok": True,
            "present": False,
            "data": {},
            "warning": "source_path_missing",
            "path": str(file_path),
        }
    loaded = _load_json(file_path, label=label)
    if loaded.get("ok") is False:
        return {
            "ok": True,
            "present": False,
            "data": {},
            "warning": "source_unreadable",
            "path": str(file_path),
            "load_error": loaded,
        }
    data = _dict(loaded["data"])
    if data.get(type_field) != expected_type or data.get(version_field) != expected_version:
        return {
            "ok": True,
            "present": False,
            "data": data,
            "warning": "source_shape_mismatch",
            "path": str(file_path),
            "type_value": data.get(type_field),
            "version_value": data.get(version_field),
        }
    return {"ok": True, "present": True, "data": data, "path": str(file_path)}


def _source_statuses(sources: dict[str, dict[str, Any]]) -> dict[str, str]:
    return {
        label: "present" if source.get("present") is True else "missing"
        for label, source in sources.items()
    }


def _source_warnings(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for label, source in sources.items():
        warning = source.get("warning")
        if warning:
            warnings.append(
                {
                    "warning_type": str(warning),
                    "source_label": label,
                    "path": source.get("path"),
                    "structural_only": True,
                }
            )
    return warnings


def _load_json(path: str | Path, *, label: str) -> dict[str, Any]:
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        return _failed("source_file_not_found", f"{label} not found: {file_path}")
    try:
        return {"ok": True, "data": json.loads(file_path.read_text(encoding="utf-8"))}
    except json.JSONDecodeError as exc:
        return _failed("invalid_json", f"{label} is not valid JSON: {exc}")


def _failed(error_type: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": error_type,
        "error_type": error_type,
        "message": message,
        "warnings": dict(REVIEW_OPS_WARNINGS),
    }


def _forbidden_field_errors(value: Any, *, path: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            if key in FORBIDDEN_REVIEW_OPS_FIELDS:
                errors.append(_error("forbidden_field", nested_path, key))
            errors.extend(_forbidden_field_errors(nested, path=nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_field_errors(nested, path=f"{path}[{index}]"))
    return errors


def _error(error_type: str, path: str, value: Any) -> dict[str, Any]:
    return {
        "error_type": error_type,
        "path": path,
        "value": value,
        "structural_only": True,
    }


def _path_or_none(path: str | Path | None) -> str | None:
    if path is None or not str(path).strip():
        return None
    return str(Path(path))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _bool_dict(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        return {}
    return {str(key): bool(item) for key, item in value.items() if isinstance(item, bool)}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None and str(item).strip()]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _is_int_like(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _tom_provenance() -> dict[str, str]:
    return {
        "project": "tom-v3-simple",
        "project_version": "0.0.0",
        "blueprint": REVIEW_OPS_BLUEPRINT,
        "blueprint_name": REVIEW_OPS_BLUEPRINT_NAME,
    }
