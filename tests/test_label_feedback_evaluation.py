from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_SAMPLING_PROFILE_TYPE,
    COVERAGE_SAMPLING_PROFILE_VERSION,
    COVERAGE_SAMPLING_REPORT_TYPE,
    COVERAGE_SAMPLING_REPORT_VERSION,
    export_coverage_sampling_strategy_contract,
)
from apps.worker.services.intennse_label_alignment import (
    export_intennse_label_alignment_contract,
)
from apps.worker.services.label_feedback_evaluation import (
    EVALUATION_HARNESS_ACTIONS,
    EVALUATION_SIGNAL_STATUSES,
    EVALUATION_SIGNAL_TYPES,
    FORBIDDEN_LABEL_FEEDBACK_FIELDS,
    LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE,
    LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION,
    LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
    LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
    LABEL_FEEDBACK_EVALUATION_REPORT_TYPE,
    LABEL_FEEDBACK_EVALUATION_REPORT_VERSION,
    LABEL_FEEDBACK_WARNINGS,
    build_label_feedback_evaluation_inputs,
    build_label_feedback_evaluation_report,
    export_label_feedback_evaluation_contract,
    validate_label_feedback_evaluation_inputs,
)
from apps.worker.services.many_point_ingestion_gate import (
    export_many_point_ingestion_gate_contract,
)
from apps.worker.services.multi_point_regression_matrix import (
    MULTI_POINT_REGRESSION_MATRIX_TYPE,
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_reviewer_disagreement import (
    export_multi_reviewer_disagreement_schema,
)
from apps.worker.services.observation_quality_taxonomy import (
    export_observation_quality_taxonomy,
)
from apps.worker.services.review_label_schema import export_review_label_schema
from apps.worker.services.review_ops_metrics import (
    REVIEW_OPS_DASHBOARD_DATA_TYPE,
    REVIEW_OPS_DASHBOARD_DATA_VERSION,
    REVIEW_OPS_METRICS_REPORT_TYPE,
    REVIEW_OPS_METRICS_REPORT_VERSION,
    export_review_ops_metrics_contract,
)
from apps.worker.services.reviewer_confidence_schema import (
    export_reviewer_confidence_schema,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    export_versioned_dataset_corpus_contract,
)


def test_export_label_feedback_evaluation_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "contracts" / "label_feedback_evaluation_contract_v1.json"

    result = export_label_feedback_evaluation_contract(output_path=output_path)

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == LABEL_FEEDBACK_EVALUATION_CONTRACT_TYPE
    assert result["contract_version"] == LABEL_FEEDBACK_EVALUATION_CONTRACT_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["feedback_inputs_type"] == LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE
    assert contract["feedback_inputs_version"] == LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION
    assert contract["report_type"] == LABEL_FEEDBACK_EVALUATION_REPORT_TYPE
    assert contract["report_version"] == LABEL_FEEDBACK_EVALUATION_REPORT_VERSION
    assert set(contract["evaluation_signal_types"]) == set(EVALUATION_SIGNAL_TYPES)
    assert set(
        contract["evaluation_bridge_schema"]["allowed_evaluation_signal_statuses"]
    ) == set(EVALUATION_SIGNAL_STATUSES)
    assert set(
        contract["evaluation_bridge_schema"]["allowed_evaluation_harness_actions"]
    ) == set(EVALUATION_HARNESS_ACTIONS)
    assert contract["source_contract_refs"]["review_ops_metrics_contract_version"] == "v1"
    assert contract["feedback_scope"]["truth_creation_allowed"] is False
    assert contract["feedback_scope"]["model_retraining_allowed"] is False
    assert contract["warnings"] == LABEL_FEEDBACK_WARNINGS
    assert not FORBIDDEN_LABEL_FEEDBACK_FIELDS & _walk_keys(contract)


def test_build_label_feedback_evaluation_inputs_preserves_structural_context(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = build_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        review_ops_metrics_report_path=paths["review_ops_report"],
        review_ops_dashboard_data_path=paths["review_ops_dashboard"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        multi_point_regression_matrix_path=paths["regression_matrix"],
        output_path=paths["feedback_inputs"],
        generated_at=datetime(2026, 6, 18, 18, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["feedback_inputs_type"] == LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE
    assert result["feedback_entry_count"] == 1

    feedback_inputs = json.loads(paths["feedback_inputs"].read_text(encoding="utf-8"))
    entry = feedback_inputs["feedback_entries"][0]
    assert feedback_inputs["generated_at"] == "2026-06-18T18:00:00+00:00"
    assert entry["source_corpus_entry_id"] == "corpus_entry_v1_test"
    assert entry["point_manifest_id"] == "point_manifest_v0_test"
    assert entry["media_id"] == "media-test"
    assert entry["associated_run_ids"]["event_candidate_run_id"] == "event-run-test"
    assert entry["profile_counts"]["review_annotation_count"] == 4
    assert entry["evaluation_signal_type"] == "structural_review_missing"
    assert entry["evaluation_signal_status"] == "requires_human_review"
    assert entry["evaluation_harness_action"] == "flag_missing_review_artifact"
    assert "include_as_regression_context" in entry["evaluation_harness_actions"]
    assert "preserve_regression_protected_sample" in entry["evaluation_harness_actions"]
    assert entry["requires_human_review"] is True
    assert entry["coverage_gap_ref"]["coverage_gaps"] == ["missing_review_labels"]
    assert feedback_inputs["summary"]["review_artifact_missing_entries"] == 1
    assert feedback_inputs["summary"]["regression_context_available_entries"] == 1
    assert not FORBIDDEN_LABEL_FEEDBACK_FIELDS & _walk_keys(feedback_inputs)


def test_validate_label_feedback_evaluation_inputs_accepts_structural_bundle(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        review_ops_metrics_report_path=paths["review_ops_report"],
        review_ops_dashboard_data_path=paths["review_ops_dashboard"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        multi_point_regression_matrix_path=paths["regression_matrix"],
        output_path=paths["feedback_inputs"],
    )

    result = validate_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        feedback_inputs_path=paths["feedback_inputs"],
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        coverage_sampling_contract_path=paths["coverage_contract"],
        many_point_ingestion_contract_path=paths["ingestion_contract"],
        review_ops_metrics_contract_path=paths["review_ops_contract"],
        output_path=paths["validation"],
        validated_at=datetime(2026, 6, 18, 18, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T18:05:00+00:00"
    assert len(result["referenced_contract_validations"]) == 9
    assert all(item["ok"] is True for item in result["referenced_contract_validations"])
    assert {item["warning_type"] for item in result["structural_warnings"]} == {
        "requires_human_review"
    }


def test_validate_label_feedback_evaluation_inputs_rejects_forbidden_content(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        review_ops_metrics_report_path=paths["review_ops_report"],
        review_ops_dashboard_data_path=paths["review_ops_dashboard"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        multi_point_regression_matrix_path=paths["regression_matrix"],
        output_path=paths["feedback_inputs"],
    )
    feedback_inputs = json.loads(paths["feedback_inputs"].read_text(encoding="utf-8"))
    feedback_inputs["feedback_entries"][0]["score"] = "15-0"
    feedback_inputs["feedback_entries"][0]["evaluation_signal_type"] = "correct"
    _write_json(paths["feedback_inputs"], feedback_inputs)

    result = validate_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        feedback_inputs_path=paths["feedback_inputs"],
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        coverage_sampling_contract_path=paths["coverage_contract"],
        many_point_ingestion_contract_path=paths["ingestion_contract"],
        review_ops_metrics_contract_path=paths["review_ops_contract"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "forbidden_value" in error_types
    assert "invalid_evaluation_signal_type" in error_types


def test_build_label_feedback_evaluation_report_summarizes_structural_feedback(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        corpus_manifest_path=paths["corpus_manifest"],
        review_ops_metrics_report_path=paths["review_ops_report"],
        review_ops_dashboard_data_path=paths["review_ops_dashboard"],
        coverage_sampling_profile_path=paths["coverage_profile"],
        coverage_sampling_report_path=paths["coverage_report"],
        multi_point_regression_matrix_path=paths["regression_matrix"],
        output_path=paths["feedback_inputs"],
    )

    result = build_label_feedback_evaluation_report(
        contract_path=paths["label_feedback_contract"],
        feedback_inputs_path=paths["feedback_inputs"],
        output_path=paths["feedback_report"],
        generated_at=datetime(2026, 6, 18, 18, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == LABEL_FEEDBACK_EVALUATION_REPORT_TYPE
    assert result["report_version"] == LABEL_FEEDBACK_EVALUATION_REPORT_VERSION

    report = json.loads(paths["feedback_report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-18T18:10:00+00:00"
    assert report["summary"]["feedback_entry_count"] == 1
    assert report["summary"]["review_artifact_missing_count"] == 1
    assert report["summary"]["confidence_artifact_missing_count"] == 1
    assert report["summary"]["regression_context_available_entries"] == 1
    assert report["evaluation_harness_action_counts"][
        "preserve_regression_protected_sample"
    ] == 1
    assert {section["section_id"] for section in report["report_sections"]} >= {
        "structural_feedback_entry",
        "review_artifact_missing",
        "regression_context_available",
    }


def test_build_label_feedback_evaluation_inputs_treats_missing_sources_as_gaps(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = build_label_feedback_evaluation_inputs(
        contract_path=paths["label_feedback_contract"],
        corpus_manifest_path=tmp_path / "missing" / "corpus.json",
        review_ops_metrics_report_path=None,
        review_ops_dashboard_data_path=None,
        coverage_sampling_profile_path=None,
        coverage_sampling_report_path=None,
        multi_point_regression_matrix_path=None,
        output_path=None,
    )

    assert result["ok"] is True
    feedback_inputs = result["feedback_inputs"]
    assert feedback_inputs["feedback_entry_count"] == 0
    assert feedback_inputs["source_statuses"]["corpus_manifest"] == "missing"
    assert {warning["warning_type"] for warning in feedback_inputs["source_warnings"]} == {
        "source_path_missing",
        "source_not_supplied",
    }
    assert feedback_inputs["warnings"]["evaluation_actions_are_routing_only"] is True


def _paths(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "label_feedback_contract": tmp_path
        / "contracts"
        / "label_feedback_evaluation_contract_v1.json",
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
        "review_ops_contract": tmp_path
        / "contracts"
        / "review_ops_metrics_contract_v1.json",
        "corpus_manifest": tmp_path
        / "exports"
        / "versioned_dataset_corpus_manifest.current.json",
        "coverage_profile": tmp_path / "exports" / "coverage_sampling_profile.current.json",
        "coverage_report": tmp_path / "exports" / "coverage_sampling_report.current.json",
        "regression_matrix": tmp_path
        / "exports"
        / "multi_point_regression_matrix.current.json",
        "review_ops_report": tmp_path / "exports" / "review_ops_metrics_report.current.json",
        "review_ops_dashboard": tmp_path
        / "exports"
        / "review_ops_dashboard_data.current.json",
        "feedback_inputs": tmp_path
        / "exports"
        / "label_feedback_evaluation_inputs.current.json",
        "validation": tmp_path
        / "exports"
        / "label_feedback_evaluation_inputs.validation.json",
        "feedback_report": tmp_path
        / "exports"
        / "label_feedback_evaluation_report.current.json",
    }
    export_label_feedback_evaluation_contract(output_path=paths["label_feedback_contract"])
    export_observation_quality_taxonomy(output_path=paths["observation_quality_taxonomy"])
    export_review_label_schema(output_path=paths["review_label_schema"])
    export_reviewer_confidence_schema(output_path=paths["reviewer_confidence_schema"])
    export_multi_reviewer_disagreement_schema(output_path=paths["multi_reviewer_schema"])
    export_intennse_label_alignment_contract(output_path=paths["intennse_contract"])
    export_versioned_dataset_corpus_contract(output_path=paths["dataset_corpus_contract"])
    export_coverage_sampling_strategy_contract(output_path=paths["coverage_contract"])
    export_many_point_ingestion_gate_contract(output_path=paths["ingestion_contract"])
    export_review_ops_metrics_contract(output_path=paths["review_ops_contract"])
    _write_json(paths["corpus_manifest"], _corpus_manifest())
    _write_json(paths["coverage_profile"], _coverage_profile())
    _write_json(paths["coverage_report"], _coverage_report())
    _write_json(paths["regression_matrix"], _regression_matrix())
    _write_json(paths["review_ops_report"], _review_ops_report())
    _write_json(paths["review_ops_dashboard"], _review_ops_dashboard())
    return paths


def _corpus_manifest() -> dict[str, Any]:
    return {
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "corpus_entries": [
            {
                "corpus_entry_id": "corpus_entry_v1_test",
                "point_manifest_id": "point_manifest_v0_test",
                "point_manifest_path": ".data/manifests/point_manifest_v0_test.json",
                "media_id": "media-test",
                "replay_url": "http://127.0.0.1:3000/replay/media-test",
                "associated_run_ids": {
                    "event_candidate_run_id": "event-run-test",
                    "trajectory_3d_run_id": "trajectory-run-test",
                    "camera_geometry_id": "camera-test",
                },
                "labels": ["protected_sample_point"],
                "evidence_availability": {
                    "media_indexed": True,
                    "replay_available": True,
                    "event_candidates_available": True,
                    "trajectory_3d_candidates_available": True,
                    "review_annotations_available": True,
                },
                "profile_counts": {
                    "review_annotation_count": 4,
                    "event_marker_count": 6,
                },
                "review_label_bundle_refs": [],
                "reviewer_confidence_bundle_refs": [],
                "multi_reviewer_review_set_refs": [],
                "disagreement_report_refs": [],
                "intennse_alignment_refs": [],
                "observation_quality_profile_path": None,
                "provenance_status": "provenance_partial",
                "requires_human_review": "not_assessed",
                "provenance_gaps": ["missing_optional_review_ref"],
                "warnings": {
                    "corpus_entry_is_not_truth": True,
                    "review_support_only": True,
                },
            }
        ],
        "warnings": {"dataset_corpus_is_not_truth": True},
    }


def _coverage_profile() -> dict[str, Any]:
    return {
        "profile_type": COVERAGE_SAMPLING_PROFILE_TYPE,
        "profile_version": COVERAGE_SAMPLING_PROFILE_VERSION,
        "sampling_candidates": [
            {
                "source_corpus_entry_id": "corpus_entry_v1_test",
                "coverage_gaps": ["missing_review_labels"],
                "warnings": {"coverage_sampling_is_not_truth": True},
            }
        ],
        "coverage_gap_summary": {"missing_review_labels": 1},
        "warnings": {"coverage_sampling_is_not_truth": True},
    }


def _coverage_report() -> dict[str, Any]:
    return {
        "report_type": COVERAGE_SAMPLING_REPORT_TYPE,
        "report_version": COVERAGE_SAMPLING_REPORT_VERSION,
        "coverage_gap_summary": {"missing_review_labels": 1},
        "warnings": {"report_is_structural_only": True},
    }


def _regression_matrix() -> dict[str, Any]:
    return {
        "matrix_type": MULTI_POINT_REGRESSION_MATRIX_TYPE,
        "matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_count": 1,
        "points": [
            {
                "point_manifest_id": "point_manifest_v0_test",
                "media_id": "media-test",
                "labels": ["protected_sample_point"],
                "warnings": {"matrix_row_is_not_truth": True},
            }
        ],
        "warnings": {"matrix_is_not_truth": True},
    }


def _review_ops_report() -> dict[str, Any]:
    return {
        "report_type": REVIEW_OPS_METRICS_REPORT_TYPE,
        "report_version": REVIEW_OPS_METRICS_REPORT_VERSION,
        "entry_metrics": [
            {
                "corpus_entry_id": "corpus_entry_v1_test",
                "statuses": {
                    "review_label_bundle": "missing",
                    "reviewer_confidence_bundle": "missing",
                },
            }
        ],
        "summary": {"total_corpus_entries": 1},
        "warnings": {"review_ops_metrics_are_not_truth": True},
    }


def _review_ops_dashboard() -> dict[str, Any]:
    return {
        "dashboard_data_type": REVIEW_OPS_DASHBOARD_DATA_TYPE,
        "dashboard_data_version": REVIEW_OPS_DASHBOARD_DATA_VERSION,
        "cards": [{"card_id": "total_corpus_entries", "value": 1}],
        "warnings": {"read_only_dashboard_data": True},
    }


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
