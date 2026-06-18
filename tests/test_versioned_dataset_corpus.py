from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from apps.worker.services.intennse_label_alignment import (
    export_intennse_label_alignment_contract,
)
from apps.worker.services.multi_point_regression_matrix import (
    build_multi_point_regression_matrix,
)
from apps.worker.services.multi_point_replay_index import build_multi_point_replay_index
from apps.worker.services.multi_reviewer_disagreement import (
    export_multi_reviewer_disagreement_schema,
)
from apps.worker.services.observation_quality_taxonomy import (
    export_observation_quality_taxonomy,
)
from apps.worker.services.point_manifest import (
    POINT_MANIFEST_TYPE,
    POINT_MANIFEST_VERSION,
    POINT_MANIFEST_WARNINGS,
)
from apps.worker.services.review_label_schema import export_review_label_schema
from apps.worker.services.reviewer_confidence_schema import (
    export_reviewer_confidence_schema,
)
from apps.worker.services.versioned_dataset_corpus import (
    CORPUS_ENTITIES,
    CORPUS_ENTRY_STATUS_VALUES,
    CORPUS_SPLIT_VALUES,
    DATASET_CORPUS_CONTRACT_TYPE,
    DATASET_CORPUS_CONTRACT_VERSION,
    DATASET_CORPUS_MANIFEST_TYPE,
    DATASET_CORPUS_MANIFEST_VERSION,
    DATASET_CORPUS_REPORT_TYPE,
    DATASET_CORPUS_REPORT_VERSION,
    DATASET_CORPUS_WARNINGS,
    FORBIDDEN_DATASET_CORPUS_FIELDS,
    PROVENANCE_STATUS_VALUES,
    build_versioned_dataset_corpus_manifest,
    build_versioned_dataset_corpus_report,
    export_versioned_dataset_corpus_contract,
    validate_versioned_dataset_corpus_manifest,
)

PROTECTED_MEDIA_ID = "9518fb01-0da1-4344-9a84-ff88ec8e9b1e"
PROTECTED_EVENT_RUN_ID = "1b946366-7ec1-426f-8b40-494535a9b3fb"
PROTECTED_TRAJECTORY_RUN_ID = "ea76ccab-c51d-4a63-9682-9fd0bbb83f14"
PROTECTED_CAMERA_GEOMETRY_ID = "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97"


def test_export_versioned_dataset_corpus_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "contracts" / "versioned_dataset_corpus_contract_v1.json"

    result = export_versioned_dataset_corpus_contract(output_path=output_path)

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == DATASET_CORPUS_CONTRACT_TYPE
    assert result["contract_version"] == DATASET_CORPUS_CONTRACT_VERSION
    assert result["corpus_manifest_type"] == DATASET_CORPUS_MANIFEST_TYPE
    assert result["corpus_manifest_version"] == DATASET_CORPUS_MANIFEST_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["included_contract_refs"] == {
        "observation_quality_taxonomy_version": "v1",
        "review_label_schema_version": "v1",
        "reviewer_confidence_schema_version": "v1",
        "multi_reviewer_disagreement_schema_version": "v1",
        "intennse_label_alignment_contract_version": "v1",
        "multi_point_regression_matrix_version": "v0",
        "point_manifest_version": "v0",
    }
    assert {item["key"] for item in contract["corpus_entities"]} == {
        entity["key"] for entity in CORPUS_ENTITIES
    }
    assert set(_value_set(contract, "corpus_split_values")) == set(CORPUS_SPLIT_VALUES)
    assert not {"train", "test", "validation"} & set(
        _value_set(contract, "corpus_split_values")
    )
    assert set(_value_set(contract, "corpus_entry_status_values")) == set(
        CORPUS_ENTRY_STATUS_VALUES
    )
    assert set(_value_set(contract, "provenance_status_values")) == set(
        PROVENANCE_STATUS_VALUES
    )
    assert contract["validation_rules"]["structural_validation_only"] is True
    assert contract["validation_rules"]["does_not_create_training_truth"] is True
    assert contract["warnings"] == DATASET_CORPUS_WARNINGS
    assert not FORBIDDEN_DATASET_CORPUS_FIELDS & _walk_keys(contract)


def test_build_versioned_dataset_corpus_manifest_preserves_point_provenance(
    tmp_path: Path,
) -> None:
    artifacts = _build_source_artifacts(tmp_path)
    output_path = tmp_path / "exports" / "versioned_dataset_corpus_manifest.current.json"

    result = build_versioned_dataset_corpus_manifest(
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=output_path,
        generated_at=datetime(2026, 6, 18, 14, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["corpus_manifest_type"] == DATASET_CORPUS_MANIFEST_TYPE
    assert result["corpus_manifest_version"] == DATASET_CORPUS_MANIFEST_VERSION
    assert result["point_count"] == 2
    assert output_path.is_file()

    manifest = json.loads(output_path.read_text(encoding="utf-8"))
    assert manifest["generated_at"] == "2026-06-18T14:00:00+00:00"
    assert manifest["source_index_path"] == str(artifacts["index"])
    assert manifest["source_matrix_path"] == str(artifacts["matrix"])
    assert manifest["summary"]["regression_protected_entry_count"] == 1
    assert manifest["summary"]["unassigned_entry_count"] == 1
    assert manifest["warnings"]["dataset_corpus_is_not_training_truth"] is True

    protected_entry = manifest["corpus_entries"][0]
    assert protected_entry["labels"] == ["protected_sample_point"]
    assert protected_entry["corpus_split"] == "regression_protected"
    assert protected_entry["associated_run_ids"]["event_candidate_run_id"] == (
        PROTECTED_EVENT_RUN_ID
    )
    replay_params = parse_qs(urlparse(protected_entry["replay_url"]).query)
    assert replay_params["eventCandidateRunId"] == [PROTECTED_EVENT_RUN_ID]
    assert replay_params["trajectory3dRunId"] == [PROTECTED_TRAJECTORY_RUN_ID]
    assert replay_params["cameraGeometryId"] == [PROTECTED_CAMERA_GEOMETRY_ID]
    assert "missing_optional_review_ref" in protected_entry["provenance_gaps"]
    assert protected_entry["warnings"]["regression_protected_entry"] is True

    second_entry = manifest["corpus_entries"][1]
    assert second_entry["labels"] == ["second_point_parity_stand_in"]
    assert second_entry["corpus_split"] == "unassigned"
    assert second_entry["evidence_availability"]["event_candidates_available"] is False
    assert second_entry["warnings"]["not_generalization_claim"] is True
    assert not FORBIDDEN_DATASET_CORPUS_FIELDS & _walk_keys(manifest)


def test_validate_versioned_dataset_corpus_manifest_reports_optional_ref_gaps(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    artifacts = _build_source_artifacts(tmp_path)
    manifest_path = tmp_path / "exports" / "versioned_dataset_corpus_manifest.current.json"
    build_versioned_dataset_corpus_manifest(
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=manifest_path,
    )

    result = validate_versioned_dataset_corpus_manifest(
        contract_path=paths["dataset_corpus_contract"],
        manifest_path=manifest_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        output_path=tmp_path / "exports" / "versioned_dataset_corpus.validation.json",
        validated_at=datetime(2026, 6, 18, 14, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T14:05:00+00:00"
    assert len(result["referenced_contract_validations"]) == 5
    assert all(item["ok"] is True for item in result["referenced_contract_validations"])
    warning_types = {item["warning_type"] for item in result["structural_warnings"]}
    assert "missing_optional_review_ref" in warning_types
    assert "missing_optional_intennse_alignment_ref" in warning_types
    assert "missing_optional_dataset_export_ref" in warning_types
    assert result["known_limitations"][0].startswith("Validation checks corpus structure")


def test_validate_versioned_dataset_corpus_manifest_rejects_forbidden_fields(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    artifacts = _build_source_artifacts(tmp_path)
    manifest_path = tmp_path / "exports" / "invalid_corpus_manifest.json"
    build_versioned_dataset_corpus_manifest(
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=manifest_path,
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["corpus_entries"][0]["score"] = "15-0"
    manifest["corpus_entries"][0]["corpus_split"] = "train"
    _write_json(manifest_path, manifest)

    result = validate_versioned_dataset_corpus_manifest(
        contract_path=paths["dataset_corpus_contract"],
        manifest_path=manifest_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "invalid_corpus_split" in error_types
    assert result["warnings"]["does_not_create_labels"] is True


def test_build_versioned_dataset_corpus_report_summarizes_structure_only(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    artifacts = _build_source_artifacts(tmp_path)
    manifest_path = tmp_path / "exports" / "versioned_dataset_corpus_manifest.current.json"
    report_path = tmp_path / "exports" / "versioned_dataset_corpus_report.current.json"
    build_versioned_dataset_corpus_manifest(
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=manifest_path,
    )

    result = build_versioned_dataset_corpus_report(
        contract_path=paths["dataset_corpus_contract"],
        manifest_path=manifest_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        output_path=report_path,
        generated_at=datetime(2026, 6, 18, 14, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["corpus_report_type"] == DATASET_CORPUS_REPORT_TYPE
    assert result["corpus_report_version"] == DATASET_CORPUS_REPORT_VERSION
    assert result["summary"]["corpus_entry_count"] == 2
    assert result["summary"]["regression_protected_entry_count"] == 1
    assert result["summary"]["missing_optional_review_ref_count"] == 2
    assert report_path.is_file()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-18T14:10:00+00:00"
    assert report["coverage"]["structural_coverage_only"] is True
    assert report["warnings"]["report_is_structural_only"] is True
    assert report["warnings"]["does_not_evaluate_tennis_quality"] is True
    assert {item["issue_type"] for item in report["provenance_issues"]} >= {
        "missing_optional_review_ref",
        "missing_optional_intennse_alignment_ref",
    }
    assert not FORBIDDEN_DATASET_CORPUS_FIELDS & _walk_keys(report)


def _build_source_artifacts(tmp_path: Path) -> dict[str, Path]:
    manifest_root = tmp_path / "manifests"
    _seed_point_manifests(manifest_root)
    index_path = tmp_path / "exports" / "multi_point_replay_index.json"
    matrix_path = tmp_path / "exports" / "multi_point_regression_matrix.current.json"
    index_result = build_multi_point_replay_index(
        manifest_root=manifest_root,
        output_path=index_path,
        generated_at=datetime(2026, 6, 18, 13, 30, tzinfo=UTC),
    )
    assert index_result["ok"] is True
    matrix_result = build_multi_point_regression_matrix(
        source_index_path=index_path,
        output_path=matrix_path,
        generated_at=datetime(2026, 6, 18, 13, 35, tzinfo=UTC),
    )
    assert matrix_result["ok"] is True
    return {"index": index_path, "matrix": matrix_path}


def _seed_point_manifests(manifest_root: Path) -> None:
    _write_json(
        manifest_root / "sample_point.blueprint_23.point_manifest.json",
        _point_manifest(
            point_manifest_id="point_manifest_v0_protected",
            media_id=PROTECTED_MEDIA_ID,
            source_media_path="/data/sample_point.mp4",
            replay_url=f"http://viewer.example/replay/{PROTECTED_MEDIA_ID}",
            associated_run_ids={
                "event_candidate_run_id": PROTECTED_EVENT_RUN_ID,
                "trajectory_3d_run_id": PROTECTED_TRAJECTORY_RUN_ID,
                "camera_geometry_id": PROTECTED_CAMERA_GEOMETRY_ID,
            },
            evidence_availability={
                "media_indexed": True,
                "replay_available": True,
                "event_candidates_available": True,
                "trajectory_3d_candidates_available": True,
                "event_candidate_3d_diagnostics_available": True,
                "review_annotations_available": True,
                "trajectory_3d_debug_reviews_available": False,
            },
            profile_counts={
                "event_marker_count": 2,
                "hit_candidate_count": 1,
                "bounce_candidate_count": 1,
                "event_candidate_observation_count": 2,
                "trajectory_3d_candidate_count": 12,
                "review_annotation_count": 3,
            },
        ),
    )
    _write_json(
        manifest_root / "second_point" / "sample_point.stand_in.point_manifest.json",
        _point_manifest(
            point_manifest_id="point_manifest_v0_second",
            media_id="second-point-media-id",
            source_media_path="/demo_assets/sample_point.mp4",
            replay_url="http://viewer.example/replay/second-point-media-id",
            associated_run_ids={},
            evidence_availability={
                "media_indexed": True,
                "replay_available": True,
                "event_candidates_available": False,
                "trajectory_3d_candidates_available": False,
                "event_candidate_3d_diagnostics_available": False,
                "review_annotations_available": False,
                "trajectory_3d_debug_reviews_available": False,
            },
            profile_counts={
                "event_marker_count": 0,
                "hit_candidate_count": 0,
                "bounce_candidate_count": 0,
                "event_candidate_observation_count": 0,
                "trajectory_3d_candidate_count": 0,
                "review_annotation_count": 0,
            },
        ),
    )


def _point_manifest(
    *,
    point_manifest_id: str,
    media_id: str,
    source_media_path: str,
    replay_url: str,
    associated_run_ids: dict[str, str],
    evidence_availability: dict[str, bool],
    profile_counts: dict[str, int],
) -> dict[str, Any]:
    return {
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": POINT_MANIFEST_VERSION,
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "source_media_path": source_media_path,
        "source_uri": f"file://{source_media_path}",
        "stored_uri": f"file://{source_media_path}",
        "replay_url": replay_url,
        "associated_run_ids": associated_run_ids,
        "evidence_availability": evidence_availability,
        "profile_counts": profile_counts,
        "warnings": dict(POINT_MANIFEST_WARNINGS),
    }


def _contract_paths(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "dataset_corpus_contract": tmp_path
        / "contracts"
        / "versioned_dataset_corpus_contract_v1.json",
        "intennse_contract": tmp_path
        / "contracts"
        / "intennse_label_alignment_contract_v1.json",
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
    }
    export_versioned_dataset_corpus_contract(
        output_path=paths["dataset_corpus_contract"]
    )
    export_intennse_label_alignment_contract(output_path=paths["intennse_contract"])
    export_observation_quality_taxonomy(output_path=paths["observation_quality_taxonomy"])
    export_review_label_schema(output_path=paths["review_label_schema"])
    export_reviewer_confidence_schema(output_path=paths["reviewer_confidence_schema"])
    export_multi_reviewer_disagreement_schema(output_path=paths["multi_reviewer_schema"])
    return paths


def _value_set(contract: dict[str, Any], key: str) -> list[str]:
    for item in contract["corpus_value_sets"]:
        if item["key"] == key:
            return item["allowed_values"]
    raise AssertionError(f"missing value set {key}")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_walk_keys(item))
    return keys
