from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.camera_geometry_calibration_provenance import (
    CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE,
    CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION,
    CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE,
    CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION,
    CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE,
    CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION,
    CAMERA_GEOMETRY_CALIBRATION_WARNINGS,
    CONFIDENCE_STATUS_VALUES,
    EVIDENCE_STATUS_VALUES,
    FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS,
    PROVENANCE_STATUS_VALUES,
    REVIEW_STATUS_VALUES,
    build_camera_geometry_calibration_profile,
    build_camera_geometry_calibration_report,
    export_camera_geometry_calibration_provenance_contract,
    validate_camera_geometry_calibration_profile,
)
from apps.worker.services.coverage_driven_sampling_strategy import (
    export_coverage_sampling_strategy_contract,
)
from apps.worker.services.intennse_label_alignment import (
    export_intennse_label_alignment_contract,
)
from apps.worker.services.label_feedback_evaluation import (
    LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
    LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
    export_label_feedback_evaluation_contract,
)
from apps.worker.services.many_point_ingestion_gate import (
    export_many_point_ingestion_gate_contract,
)
from apps.worker.services.multi_point_regression_matrix import (
    MULTI_POINT_REGRESSION_MATRIX_TYPE,
    MULTI_POINT_REGRESSION_MATRIX_VERSION,
)
from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_TYPE,
    MULTI_POINT_REPLAY_INDEX_VERSION,
)
from apps.worker.services.multi_reviewer_disagreement import (
    export_multi_reviewer_disagreement_schema,
)
from apps.worker.services.observation_quality_taxonomy import (
    export_observation_quality_taxonomy,
)
from apps.worker.services.review_label_schema import export_review_label_schema
from apps.worker.services.review_ops_metrics import export_review_ops_metrics_contract
from apps.worker.services.reviewer_confidence_schema import (
    export_reviewer_confidence_schema,
)
from apps.worker.services.versioned_dataset_corpus import (
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    export_versioned_dataset_corpus_contract,
)

PROTECTED_MEDIA_ID = "9518fb01-0da1-4344-9a84-ff88ec8e9b1e"
PROTECTED_EVENT_RUN_ID = "1b946366-7ec1-426f-8b40-494535a9b3fb"
PROTECTED_TRAJECTORY_RUN_ID = "ea76ccab-c51d-4a63-9682-9fd0bbb83f14"
PROTECTED_CAMERA_GEOMETRY_ID = "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97"


def test_export_camera_geometry_calibration_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = (
        tmp_path
        / "contracts"
        / "camera_geometry_calibration_provenance_contract_v1.json"
    )

    result = export_camera_geometry_calibration_provenance_contract(
        output_path=output_path,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == CAMERA_GEOMETRY_CALIBRATION_CONTRACT_TYPE
    assert result["contract_version"] == CAMERA_GEOMETRY_CALIBRATION_CONTRACT_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["profile_type"] == CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE
    assert contract["profile_version"] == CAMERA_GEOMETRY_CALIBRATION_PROFILE_VERSION
    assert contract["report_type"] == CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE
    assert contract["report_version"] == CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION
    assert contract["source_contract_refs"]["label_feedback_evaluation_contract_version"] == (
        "v1"
    )
    assert set(
        contract["evidence_confidence_semantics"]["confidence_status_values"]
    ) == set(CONFIDENCE_STATUS_VALUES)
    assert set(contract["evidence_confidence_semantics"]["evidence_status_values"]) == set(
        EVIDENCE_STATUS_VALUES
    )
    assert set(
        contract["evidence_confidence_semantics"]["provenance_status_values"]
    ) == set(PROVENANCE_STATUS_VALUES)
    assert set(contract["evidence_confidence_semantics"]["review_status_values"]) == set(
        REVIEW_STATUS_VALUES
    )
    assert contract["calibration_scope"]["read_only"] is True
    assert contract["calibration_scope"]["homography_generation_allowed"] is False
    assert contract["validation_rules"]["does_not_create_calibration_truth"] is True
    assert contract["warnings"] == CAMERA_GEOMETRY_CALIBRATION_WARNINGS
    assert not FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS & _walk_keys(contract)


def test_build_camera_geometry_calibration_profile_preserves_provenance(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)

    result = build_camera_geometry_calibration_profile(
        contract_path=paths["camera_calibration_contract"],
        replay_index_path=paths["replay_index"],
        regression_matrix_path=paths["regression_matrix"],
        corpus_manifest_path=paths["corpus_manifest"],
        label_feedback_inputs_path=paths["label_feedback_inputs"],
        output_path=paths["profile"],
        generated_at=datetime(2026, 6, 18, 19, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["profile_type"] == CAMERA_GEOMETRY_CALIBRATION_PROFILE_TYPE
    assert result["calibration_profile_count"] == 2

    profile = json.loads(paths["profile"].read_text(encoding="utf-8"))
    protected = profile["camera_geometry_profiles"][0]
    second = profile["camera_geometry_profiles"][1]
    assert profile["generated_at"] == "2026-06-18T19:00:00+00:00"
    assert protected["media_id"] == PROTECTED_MEDIA_ID
    assert protected["camera_geometry_id"] == PROTECTED_CAMERA_GEOMETRY_ID
    assert protected["trajectory_3d_run_id"] == PROTECTED_TRAJECTORY_RUN_ID
    assert protected["associated_run_ids"]["event_candidate_run_id"] == (
        PROTECTED_EVENT_RUN_ID
    )
    assert protected["calibration_confidence_status"] == "regression_protected_context"
    assert protected["calibration_evidence_status"] == "evidence_partial"
    assert protected["calibration_provenance_status"] == "provenance_partial"
    assert protected["calibration_review_status"] == "review_ready"
    assert protected["requires_human_calibration_review"] is True
    assert protected["evidence_availability"]["camera_geometry_available"] is True
    assert protected["evidence_availability"]["projection_diagnostics_available"] is False
    assert protected["warnings"]["missing_projection_diagnostics"] is True

    assert second["media_id"] == "second-point-media-id"
    assert second["camera_geometry_id"] is None
    assert second["calibration_evidence_status"] == "missing_camera_geometry"
    assert second["calibration_confidence_status"] == "evidence_missing"
    assert second["requires_human_calibration_review"] is True

    assert profile["summary"]["calibration_profile_count"] == 2
    assert profile["summary"]["camera_geometry_evidence_present_count"] == 1
    assert profile["summary"]["camera_geometry_evidence_missing_count"] == 1
    assert profile["summary"]["missing_projection_diagnostics_count"] == 2
    assert profile["summary"]["regression_protected_context_count"] == 1
    assert profile["warnings"]["profile_uses_existing_artifacts_only"] is True
    assert not FORBIDDEN_CAMERA_GEOMETRY_CALIBRATION_FIELDS & _walk_keys(profile)


def test_validate_camera_geometry_calibration_profile_accepts_structural_profile(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_camera_geometry_calibration_profile(
        contract_path=paths["camera_calibration_contract"],
        replay_index_path=paths["replay_index"],
        regression_matrix_path=paths["regression_matrix"],
        corpus_manifest_path=paths["corpus_manifest"],
        label_feedback_inputs_path=paths["label_feedback_inputs"],
        output_path=paths["profile"],
    )

    result = validate_camera_geometry_calibration_profile(
        contract_path=paths["camera_calibration_contract"],
        profile_path=paths["profile"],
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        coverage_sampling_contract_path=paths["coverage_contract"],
        many_point_ingestion_contract_path=paths["ingestion_contract"],
        review_ops_metrics_contract_path=paths["review_ops_contract"],
        label_feedback_contract_path=paths["label_feedback_contract"],
        output_path=paths["validation"],
        validated_at=datetime(2026, 6, 18, 19, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T19:05:00+00:00"
    assert len(result["referenced_contract_validations"]) == 10
    assert all(item["ok"] is True for item in result["referenced_contract_validations"])
    warning_types = {item["warning_type"] for item in result["structural_warnings"]}
    assert "requires_human_calibration_review" in warning_types
    assert "missing_projection_diagnostics" in warning_types


def test_validate_camera_geometry_calibration_profile_rejects_forbidden_content(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_camera_geometry_calibration_profile(
        contract_path=paths["camera_calibration_contract"],
        replay_index_path=paths["replay_index"],
        regression_matrix_path=paths["regression_matrix"],
        corpus_manifest_path=paths["corpus_manifest"],
        label_feedback_inputs_path=paths["label_feedback_inputs"],
        output_path=paths["profile"],
    )
    profile = json.loads(paths["profile"].read_text(encoding="utf-8"))
    profile["camera_geometry_profiles"][0]["score"] = "15-0"
    profile["camera_geometry_profiles"][0]["calibration_confidence_status"] = "truth"
    _write_json(paths["profile"], profile)

    result = validate_camera_geometry_calibration_profile(
        contract_path=paths["camera_calibration_contract"],
        profile_path=paths["profile"],
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        coverage_sampling_contract_path=paths["coverage_contract"],
        many_point_ingestion_contract_path=paths["ingestion_contract"],
        review_ops_metrics_contract_path=paths["review_ops_contract"],
        label_feedback_contract_path=paths["label_feedback_contract"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "forbidden_value" in error_types
    assert "invalid_calibration_confidence_status" in error_types


def test_build_camera_geometry_calibration_report_summarizes_structure_only(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    build_camera_geometry_calibration_profile(
        contract_path=paths["camera_calibration_contract"],
        replay_index_path=paths["replay_index"],
        regression_matrix_path=paths["regression_matrix"],
        corpus_manifest_path=paths["corpus_manifest"],
        label_feedback_inputs_path=paths["label_feedback_inputs"],
        output_path=paths["profile"],
    )

    result = build_camera_geometry_calibration_report(
        contract_path=paths["camera_calibration_contract"],
        profile_path=paths["profile"],
        output_path=paths["report"],
        generated_at=datetime(2026, 6, 18, 19, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == CAMERA_GEOMETRY_CALIBRATION_REPORT_TYPE
    assert result["report_version"] == CAMERA_GEOMETRY_CALIBRATION_REPORT_VERSION

    report = json.loads(paths["report"].read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-18T19:10:00+00:00"
    assert report["summary"]["calibration_profile_count"] == 2
    assert report["summary"]["calibration_review_needed_count"] == 2
    assert report["summary"]["human_review_ready_count"] == 1
    assert report["summary"]["regression_protected_context_count"] == 1
    assert report["warnings"]["report_is_structural_only"] is True
    assert {section["section_id"] for section in report["report_sections"]} >= {
        "camera_geometry_evidence_present",
        "projection_diagnostics_present",
        "calibration_review_needed",
        "human_review_ready",
        "regression_protected_context",
        "structural_confidence_only",
    }


def _paths(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "camera_calibration_contract": tmp_path
        / "contracts"
        / "camera_geometry_calibration_provenance_contract_v1.json",
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
        "review_ops_contract": tmp_path / "contracts" / "review_ops_metrics_contract_v1.json",
        "label_feedback_contract": tmp_path
        / "contracts"
        / "label_feedback_evaluation_contract_v1.json",
        "replay_index": tmp_path / "manifests" / "multi_point_replay_index.json",
        "regression_matrix": tmp_path
        / "exports"
        / "multi_point_regression_matrix.current.json",
        "corpus_manifest": tmp_path
        / "exports"
        / "versioned_dataset_corpus_manifest.current.json",
        "label_feedback_inputs": tmp_path
        / "exports"
        / "label_feedback_evaluation_inputs.current.json",
        "profile": tmp_path
        / "exports"
        / "camera_geometry_calibration_profile.current.json",
        "validation": tmp_path
        / "exports"
        / "camera_geometry_calibration_profile.validation.json",
        "report": tmp_path
        / "exports"
        / "camera_geometry_calibration_report.current.json",
    }
    export_camera_geometry_calibration_provenance_contract(
        output_path=paths["camera_calibration_contract"],
    )
    export_observation_quality_taxonomy(output_path=paths["observation_quality_taxonomy"])
    export_review_label_schema(output_path=paths["review_label_schema"])
    export_reviewer_confidence_schema(output_path=paths["reviewer_confidence_schema"])
    export_multi_reviewer_disagreement_schema(output_path=paths["multi_reviewer_schema"])
    export_intennse_label_alignment_contract(output_path=paths["intennse_contract"])
    export_versioned_dataset_corpus_contract(output_path=paths["dataset_corpus_contract"])
    export_coverage_sampling_strategy_contract(output_path=paths["coverage_contract"])
    export_many_point_ingestion_gate_contract(output_path=paths["ingestion_contract"])
    export_review_ops_metrics_contract(output_path=paths["review_ops_contract"])
    export_label_feedback_evaluation_contract(output_path=paths["label_feedback_contract"])
    _write_json(paths["replay_index"], _replay_index())
    _write_json(paths["regression_matrix"], _regression_matrix())
    _write_json(paths["corpus_manifest"], _corpus_manifest())
    _write_json(paths["label_feedback_inputs"], _label_feedback_inputs())
    return paths


def _replay_index() -> dict[str, Any]:
    return {
        "index_type": MULTI_POINT_REPLAY_INDEX_TYPE,
        "index_version": MULTI_POINT_REPLAY_INDEX_VERSION,
        "point_count": 2,
        "points": [_protected_point(), _second_point()],
        "warnings": {"navigation_only": True},
    }


def _regression_matrix() -> dict[str, Any]:
    return {
        "matrix_type": MULTI_POINT_REGRESSION_MATRIX_TYPE,
        "matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "point_count": 2,
        "points": [_protected_point(), _second_point()],
        "warnings": {"matrix_is_not_truth": True},
    }


def _corpus_manifest() -> dict[str, Any]:
    protected = {
        **_protected_point(),
        "corpus_entry_id": "corpus_entry_v1_protected",
        "point_manifest_path": ".data/manifests/protected.point_manifest.json",
        "provenance_status": "provenance_partial",
        "provenance_gaps": ["missing_optional_review_ref"],
    }
    second = {
        **_second_point(),
        "corpus_entry_id": "corpus_entry_v1_second",
        "point_manifest_path": ".data/manifests/second.point_manifest.json",
        "provenance_status": "provenance_partial",
        "provenance_gaps": ["missing_camera_geometry"],
    }
    return {
        "corpus_manifest_type": DATASET_CORPUS_MANIFEST_TYPE,
        "corpus_manifest_version": DATASET_CORPUS_MANIFEST_VERSION,
        "corpus_entries": [protected, second],
        "warnings": {"dataset_corpus_is_not_truth": True},
    }


def _label_feedback_inputs() -> dict[str, Any]:
    return {
        "feedback_inputs_type": LABEL_FEEDBACK_EVALUATION_INPUTS_TYPE,
        "feedback_inputs_version": LABEL_FEEDBACK_EVALUATION_INPUTS_VERSION,
        "feedback_entries": [
            {
                "feedback_entry_id": "feedback_entry_v1_protected",
                "point_manifest_id": "point_manifest_v0_protected",
                "media_id": PROTECTED_MEDIA_ID,
                "review_label_bundle_refs": [],
                "reviewer_confidence_bundle_refs": [],
                "multi_reviewer_review_set_refs": [],
                "disagreement_report_refs": [],
                "evaluation_signal_type": "structural_review_missing",
                "evaluation_signal_status": "requires_human_review",
                "evaluation_harness_actions": ["flag_missing_review_artifact"],
                "requires_human_review": True,
            }
        ],
        "warnings": {"label_feedback_evaluation_is_not_truth": True},
    }


def _protected_point() -> dict[str, Any]:
    return {
        "point_manifest_id": "point_manifest_v0_protected",
        "media_id": PROTECTED_MEDIA_ID,
        "manifest_path": ".data/manifests/protected.point_manifest.json",
        "replay_url": f"http://127.0.0.1:3000/replay/{PROTECTED_MEDIA_ID}",
        "source_media_path": "/data/sample_point.mp4",
        "source_uri": "file:///data/sample_point.mp4",
        "stored_path": "/stored/sample_point.mp4",
        "stored_uri": "file:///stored/sample_point.mp4",
        "associated_run_ids": {
            "event_candidate_run_id": PROTECTED_EVENT_RUN_ID,
            "trajectory_3d_run_id": PROTECTED_TRAJECTORY_RUN_ID,
            "camera_geometry_id": PROTECTED_CAMERA_GEOMETRY_ID,
        },
        "evidence_availability": {
            "media_indexed": True,
            "replay_available": True,
            "event_candidates_available": True,
            "trajectory_3d_candidates_available": True,
            "event_candidate_3d_diagnostics_available": True,
            "review_annotations_available": True,
        },
        "profile_counts": {
            "event_marker_count": 6,
            "event_candidate_3d_diagnostic_count": 6,
            "trajectory_3d_candidate_count": 68,
            "review_annotation_count": 4,
        },
        "labels": ["protected_sample_point"],
        "warnings": {"manifest_is_not_truth": True},
    }


def _second_point() -> dict[str, Any]:
    return {
        "point_manifest_id": "point_manifest_v0_second",
        "media_id": "second-point-media-id",
        "manifest_path": ".data/manifests/second.point_manifest.json",
        "replay_url": "http://127.0.0.1:3000/replay/second-point-media-id",
        "associated_run_ids": {},
        "evidence_availability": {
            "media_indexed": True,
            "replay_available": True,
            "event_candidates_available": False,
            "trajectory_3d_candidates_available": False,
            "review_annotations_available": False,
        },
        "profile_counts": {
            "event_marker_count": 0,
            "trajectory_3d_candidate_count": 0,
            "review_annotation_count": 0,
        },
        "labels": ["second_point_parity_stand_in"],
        "warnings": {"not_generalization_claim": True},
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
