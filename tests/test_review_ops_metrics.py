from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_REPORT_TYPE,
    COVERAGE_SAMPLING_REPORT_VERSION,
    export_coverage_sampling_strategy_contract,
)
from apps.worker.services.intennse_label_alignment import (
    export_intennse_label_alignment_contract,
)
from apps.worker.services.many_point_ingestion_gate import (
    MANY_POINT_INGESTION_GATE_TYPE,
    MANY_POINT_INGESTION_GATE_VERSION,
    export_many_point_ingestion_gate_contract,
)
from apps.worker.services.multi_reviewer_disagreement import (
    export_multi_reviewer_disagreement_schema,
)
from apps.worker.services.observation_quality_taxonomy import (
    export_observation_quality_taxonomy,
)
from apps.worker.services.review_label_schema import export_review_label_schema
from apps.worker.services.review_ops_metrics import (
    ALLOWED_METRIC_STATUS_VALUES,
    DASHBOARD_CARD_IDS,
    FORBIDDEN_REVIEW_OPS_FIELDS,
    METRIC_GROUPS,
    REVIEW_OPS_DASHBOARD_DATA_TYPE,
    REVIEW_OPS_DASHBOARD_DATA_VERSION,
    REVIEW_OPS_METRICS_CONTRACT_TYPE,
    REVIEW_OPS_METRICS_CONTRACT_VERSION,
    REVIEW_OPS_METRICS_REPORT_TYPE,
    REVIEW_OPS_METRICS_REPORT_VERSION,
    REVIEW_OPS_WARNINGS,
    build_review_ops_dashboard_data,
    build_review_ops_metrics_report,
    export_review_ops_metrics_contract,
    validate_review_ops_metrics_report,
)
from apps.worker.services.reviewer_confidence_schema import (
    export_reviewer_confidence_schema,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    export_versioned_dataset_corpus_contract,
)


def test_export_review_ops_metrics_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "contracts" / "review_ops_metrics_contract_v1.json"

    result = export_review_ops_metrics_contract(output_path=output_path)

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == REVIEW_OPS_METRICS_CONTRACT_TYPE
    assert result["contract_version"] == REVIEW_OPS_METRICS_CONTRACT_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["report_type"] == REVIEW_OPS_METRICS_REPORT_TYPE
    assert contract["report_version"] == REVIEW_OPS_METRICS_REPORT_VERSION
    assert {item["key"] for item in contract["metric_groups"]} == set(METRIC_GROUPS)
    assert set(contract["dashboard_card_schema"]["allowed_card_ids"]) == set(
        DASHBOARD_CARD_IDS
    )
    assert set(contract["allowed_metric_status_values"]) == set(
        ALLOWED_METRIC_STATUS_VALUES
    )
    assert contract["source_contract_refs"] == {
        "observation_quality_taxonomy_version": "v1",
        "review_label_schema_version": "v1",
        "reviewer_confidence_schema_version": "v1",
        "multi_reviewer_disagreement_schema_version": "v1",
        "intennse_label_alignment_contract_version": "v1",
        "versioned_dataset_corpus_contract_version": "v1",
        "coverage_sampling_strategy_contract_version": "v1",
        "many_point_ingestion_gate_contract_version": "v1",
        "multi_point_regression_matrix_version": "v0",
        "point_manifest_version": "v0",
    }
    assert contract["metrics_scope"]["read_only"] is True
    assert contract["metrics_scope"]["label_creation_allowed"] is False
    assert contract["validation_rules"]["does_not_rank_reviewers"] is True
    assert contract["warnings"] == REVIEW_OPS_WARNINGS
    assert not FORBIDDEN_REVIEW_OPS_FIELDS & _walk_keys(contract)


def test_build_review_ops_metrics_report_counts_structural_gaps(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = build_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        many_point_ingestion_gate_path=paths["ingestion_gate"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 18, 17, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == REVIEW_OPS_METRICS_REPORT_TYPE
    assert result["report_version"] == REVIEW_OPS_METRICS_REPORT_VERSION
    assert result["corpus_entry_count"] == 1

    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-18T17:00:00+00:00"
    assert report["summary"]["total_corpus_entries"] == 1
    assert report["summary"]["replay_available_entries"] == 1
    assert report["summary"]["entries_with_point_manifest"] == 1
    assert report["summary"]["entries_with_review_label_bundle"] == 0
    assert report["summary"]["entries_with_reviewer_confidence_bundle"] == 0
    assert report["summary"]["entries_requiring_human_review"] == 1
    assert report["summary"]["regression_protected_entries"] == 1
    assert report["summary"]["ingestion_ready_entries"] == 1
    assert report["coverage_gap_counts"]["missing_review_labels"] == 1
    assert {card["card_id"] for card in report["dashboard_cards"]} == set(
        DASHBOARD_CARD_IDS
    )
    review_card = _card(report, "entries_with_review_label_bundle")
    assert review_card["status"] == "missing"
    assert _card(report, "entries_requiring_human_review")["status"] == (
        "requires_human_review"
    )
    assert report["known_limitations"][1]["limitation_type"] == "demo_or_single_point_limited"
    assert not FORBIDDEN_REVIEW_OPS_FIELDS & _walk_keys(report)


def test_validate_review_ops_metrics_report_accepts_structural_report(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        many_point_ingestion_gate_path=paths["ingestion_gate"],
        output_path=paths["report"],
    )

    result = validate_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        report_path=paths["report"],
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        coverage_sampling_contract_path=paths["coverage_contract"],
        many_point_ingestion_contract_path=paths["ingestion_contract"],
        output_path=paths["validation"],
        validated_at=datetime(2026, 6, 18, 17, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T17:05:00+00:00"
    assert len(result["referenced_contract_validations"]) == 8
    assert all(item["ok"] is True for item in result["referenced_contract_validations"])
    assert {item["warning_type"] for item in result["structural_warnings"]} == {
        "missing_optional_refs"
    }


def test_validate_review_ops_metrics_report_rejects_forbidden_fields(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        many_point_ingestion_gate_path=paths["ingestion_gate"],
        output_path=paths["report"],
    )
    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    report["dashboard_cards"][0]["status"] = "correct"
    report["score"] = "15-0"
    _write_json(paths["report"], report)

    result = validate_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        report_path=paths["report"],
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        coverage_sampling_contract_path=paths["coverage_contract"],
        many_point_ingestion_contract_path=paths["ingestion_contract"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "invalid_dashboard_card_status" in error_types
    assert "forbidden_dashboard_card_status" in error_types


def test_build_review_ops_dashboard_data_is_read_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        many_point_ingestion_gate_path=paths["ingestion_gate"],
        output_path=paths["report"],
    )

    result = build_review_ops_dashboard_data(
        report_path=paths["report"],
        output_path=paths["dashboard_data"],
        generated_at=datetime(2026, 6, 18, 17, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["dashboard_data_type"] == REVIEW_OPS_DASHBOARD_DATA_TYPE
    assert result["dashboard_data_version"] == REVIEW_OPS_DASHBOARD_DATA_VERSION
    assert result["card_count"] == len(DASHBOARD_CARD_IDS)
    dashboard_data = json.loads(paths["dashboard_data"].read_text(encoding="utf-8"))
    assert dashboard_data["generated_at"] == "2026-06-18T17:10:00+00:00"
    assert dashboard_data["read_only"] is True
    assert dashboard_data["cards"][0]["card_id"] == "total_corpus_entries"
    assert dashboard_data["warnings"]["dashboard_data_does_not_create_labels"] is True


def test_build_review_ops_metrics_report_treats_missing_sources_as_gaps(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = build_review_ops_metrics_report(
        contract_path=paths["review_ops_contract"],
        corpus_manifest_path=tmp_path / "missing" / "corpus.json",
        coverage_sampling_profile_path=tmp_path / "missing" / "coverage.json",
        coverage_sampling_report_path=None,
        many_point_ingestion_gate_path=None,
        output_path=None,
    )

    assert result["ok"] is True
    report = result["report"]
    assert report["corpus_entry_count"] == 0
    assert report["source_statuses"]["corpus_manifest"] == "missing"
    assert {warning["warning_type"] for warning in report["source_warnings"]} == {
        "source_path_missing",
        "source_not_supplied",
    }
    assert report["warnings"]["dashboard_data_is_read_only"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "review_ops_contract": tmp_path
        / "contracts"
        / "review_ops_metrics_contract_v1.json",
        "observation_quality_taxonomy": tmp_path
        / "contracts"
        / "observation_quality_taxonomy_v1.json",
        "review_label_schema": tmp_path / "contracts" / "review_label_schema_v1.json",
        "reviewer_confidence_schema": tmp_path
        / "contracts"
        / "reviewer_confidence_ambiguity_schema_v1.json",
        "multi_reviewer_schema": tmp_path
        / "contracts"
        / "multi_reviewer_disagreement_schema_v1.json",
        "intennse_contract": tmp_path
        / "contracts"
        / "intennse_label_alignment_contract_v1.json",
        "dataset_corpus_contract": tmp_path
        / "contracts"
        / "versioned_dataset_corpus_contract_v1.json",
        "coverage_contract": tmp_path
        / "contracts"
        / "coverage_sampling_strategy_contract_v1.json",
        "ingestion_contract": tmp_path
        / "contracts"
        / "many_point_ingestion_gate_contract_v1.json",
        "corpus_manifest": tmp_path
        / "exports"
        / "versioned_dataset_corpus_manifest.current.json",
        "coverage_profile": tmp_path / "exports" / "coverage_sampling_profile.current.json",
        "coverage_report": tmp_path / "exports" / "coverage_sampling_report.current.json",
        "ingestion_gate": tmp_path / "exports" / "many_point_ingestion_gate.current.json",
        "report": tmp_path / "exports" / "review_ops_metrics_report.current.json",
        "validation": tmp_path / "exports" / "review_ops_metrics_report.validation.json",
        "dashboard_data": tmp_path / "exports" / "review_ops_dashboard_data.current.json",
    }
    export_review_ops_metrics_contract(output_path=paths["review_ops_contract"])
    export_observation_quality_taxonomy(output_path=paths["observation_quality_taxonomy"])
    export_review_label_schema(output_path=paths["review_label_schema"])
    export_reviewer_confidence_schema(output_path=paths["reviewer_confidence_schema"])
    export_multi_reviewer_disagreement_schema(output_path=paths["multi_reviewer_schema"])
    export_intennse_label_alignment_contract(output_path=paths["intennse_contract"])
    export_versioned_dataset_corpus_contract(output_path=paths["dataset_corpus_contract"])
    export_coverage_sampling_strategy_contract(output_path=paths["coverage_contract"])
    export_many_point_ingestion_gate_contract(output_path=paths["ingestion_contract"])
    _write_json(paths["corpus_manifest"], _corpus_manifest())
    _write_json(paths["coverage_profile"], _coverage_profile())
    _write_json(paths["coverage_report"], _coverage_report())
    _write_json(paths["ingestion_gate"], _ingestion_gate())
    return paths


def _corpus_manifest() -> dict[str, Any]:
    return {
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "contract_type": "versioned_dataset_corpus_contract",
        "contract_version": "v1",
        "corpus_entries": [
            {
                "corpus_entry_id": "corpus_entry_v1_test",
                "point_manifest_id": "point_manifest_v0_test",
                "media_id": "media-test",
                "replay_url": "http://127.0.0.1:3000/replay/media-test",
                "labels": ["protected_sample_point"],
                "evidence_availability": {
                    "media_indexed": True,
                    "replay_available": True,
                    "event_candidates_available": True,
                    "trajectory_3d_candidates_available": True,
                    "review_annotations_available": True,
                },
                "review_label_bundle_refs": [],
                "reviewer_confidence_bundle_refs": [],
                "multi_reviewer_review_set_refs": [],
                "disagreement_report_refs": [],
                "intennse_alignment_refs": [],
                "observation_quality_profile_path": None,
                "provenance_status": "provenance_partial",
                "requires_human_review": "not_assessed",
                "provenance_gaps": [
                    "missing_optional_review_ref",
                    "missing_optional_intennse_alignment_ref",
                ],
                "warnings": {
                    "corpus_entry_is_not_truth": True,
                    "review_support_only": True,
                },
            }
        ],
        "source_contract_versions": {
            "observation_quality_taxonomy_version": "v1",
            "review_label_schema_version": "v1",
            "reviewer_confidence_schema_version": "v1",
            "multi_reviewer_disagreement_schema_version": "v1",
            "intennse_label_alignment_contract_version": "v1",
            "multi_point_regression_matrix_version": "v0",
            "point_manifest_version": "v0",
        },
        "warnings": {"dataset_corpus_is_not_truth": True},
    }


def _coverage_profile() -> dict[str, Any]:
    return {
        "profile_type": "coverage_sampling_profile",
        "profile_version": "v1",
        "coverage_gap_summary": {
            "missing_review_labels": 1,
            "missing_reviewer_confidence": 1,
        },
        "warnings": {"coverage_sampling_is_not_truth": True},
    }


def _coverage_report() -> dict[str, Any]:
    return {
        "report_type": COVERAGE_SAMPLING_REPORT_TYPE,
        "report_version": COVERAGE_SAMPLING_REPORT_VERSION,
        "coverage_gap_summary": {"missing_review_labels": 1},
        "warnings": {"report_is_structural_only": True},
    }


def _ingestion_gate() -> dict[str, Any]:
    return {
        "ingestion_gate_type": MANY_POINT_INGESTION_GATE_TYPE,
        "ingestion_gate_version": MANY_POINT_INGESTION_GATE_VERSION,
        "mode": "dry_run",
        "entry_count": 1,
        "indexed_entry_count": 0,
        "warnings": {"writes_media_or_manifest_state": False},
    }


def _card(report: dict[str, Any], card_id: str) -> dict[str, Any]:
    return next(card for card in report["dashboard_cards"] if card["card_id"] == card_id)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_walk_keys(nested))
    return keys
