from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.coverage_driven_sampling_strategy import (
    COVERAGE_AXES,
    COVERAGE_GAP_TYPES,
    COVERAGE_SAMPLING_CONTRACT_TYPE,
    COVERAGE_SAMPLING_CONTRACT_VERSION,
    COVERAGE_SAMPLING_PROFILE_TYPE,
    COVERAGE_SAMPLING_PROFILE_VERSION,
    COVERAGE_SAMPLING_REPORT_TYPE,
    COVERAGE_SAMPLING_REPORT_VERSION,
    COVERAGE_SAMPLING_WARNINGS,
    FORBIDDEN_COVERAGE_SAMPLING_FIELDS,
    NEXT_ACTION_VALUES,
    SAMPLING_PRIORITY_VALUES,
    build_coverage_sampling_profile,
    build_coverage_sampling_report,
    export_coverage_sampling_strategy_contract,
    validate_coverage_sampling_profile,
)
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
    build_versioned_dataset_corpus_manifest,
    export_versioned_dataset_corpus_contract,
)

PROTECTED_MEDIA_ID = "9518fb01-0da1-4344-9a84-ff88ec8e9b1e"
PROTECTED_EVENT_RUN_ID = "1b946366-7ec1-426f-8b40-494535a9b3fb"
PROTECTED_TRAJECTORY_RUN_ID = "ea76ccab-c51d-4a63-9682-9fd0bbb83f14"
PROTECTED_CAMERA_GEOMETRY_ID = "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97"


def test_export_coverage_sampling_strategy_contract_writes_stable_contract(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "contracts" / "coverage_sampling_strategy_contract_v1.json"

    result = export_coverage_sampling_strategy_contract(output_path=output_path)

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["contract_type"] == COVERAGE_SAMPLING_CONTRACT_TYPE
    assert result["contract_version"] == COVERAGE_SAMPLING_CONTRACT_VERSION
    assert result["profile_type"] == COVERAGE_SAMPLING_PROFILE_TYPE
    assert result["profile_version"] == COVERAGE_SAMPLING_PROFILE_VERSION
    assert output_path.is_file()

    contract = json.loads(output_path.read_text(encoding="utf-8"))
    assert contract["exported_at"] == "2026-06-18T00:00:00+00:00"
    assert contract["source_contract_refs"] == {
        "observation_quality_taxonomy_version": "v1",
        "review_label_schema_version": "v1",
        "reviewer_confidence_schema_version": "v1",
        "multi_reviewer_disagreement_schema_version": "v1",
        "intennse_label_alignment_contract_version": "v1",
        "versioned_dataset_corpus_contract_version": "v1",
        "multi_point_regression_matrix_version": "v0",
        "point_manifest_version": "v0",
    }
    assert {item["key"] for item in contract["coverage_axes"]} == set(COVERAGE_AXES)
    assert {item["key"] for item in contract["coverage_gap_types"]} == set(
        COVERAGE_GAP_TYPES
    )
    assert set(contract["sampling_priority_values"]) == set(SAMPLING_PRIORITY_VALUES)
    assert set(contract["allowed_next_action_values"]) == set(NEXT_ACTION_VALUES)
    assert contract["strategy_scope"]["sampling_execution_allowed"] is False
    assert contract["validation_rules"]["does_not_execute_sampling"] is True
    assert contract["warnings"] == COVERAGE_SAMPLING_WARNINGS
    assert not FORBIDDEN_COVERAGE_SAMPLING_FIELDS & _walk_keys(contract)


def test_build_coverage_sampling_profile_identifies_structural_gaps(
    tmp_path: Path,
) -> None:
    artifacts = _build_corpus_artifacts(tmp_path, include_second_point=True)
    output_path = tmp_path / "exports" / "coverage_sampling_profile.current.json"

    result = build_coverage_sampling_profile(
        source_corpus_manifest_path=artifacts["corpus_manifest"],
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=output_path,
        generated_at=datetime(2026, 6, 18, 15, 0, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["profile_type"] == COVERAGE_SAMPLING_PROFILE_TYPE
    assert result["profile_version"] == COVERAGE_SAMPLING_PROFILE_VERSION
    assert result["sampling_candidate_count"] == 2
    assert output_path.is_file()

    profile = json.loads(output_path.read_text(encoding="utf-8"))
    assert profile["generated_at"] == "2026-06-18T15:00:00+00:00"
    assert profile["source_corpus_manifest_path"] == str(artifacts["corpus_manifest"])
    assert profile["source_index_path"] == str(artifacts["index"])
    assert profile["source_matrix_path"] == str(artifacts["matrix"])
    assert profile["coverage_gap_summary"]["missing_review_labels"] == 2
    assert profile["coverage_gap_summary"]["missing_intennse_alignment"] == 2
    assert profile["coverage_gap_summary"]["demo_stand_in_only"] == 1
    assert profile["priority_summary"]["high"] == 1
    assert profile["priority_summary"]["medium"] == 1

    protected_candidate = profile["sampling_candidates"][0]
    assert protected_candidate["labels"] == ["protected_sample_point"]
    assert protected_candidate["sampling_priority"] == "medium"
    assert protected_candidate["suggested_next_action"] == "add_human_review_labels"
    assert protected_candidate["associated_run_ids"]["event_candidate_run_id"] == (
        PROTECTED_EVENT_RUN_ID
    )
    assert protected_candidate["coverage_axes"]["regression_protection_coverage"] == (
        "covered"
    )

    second_candidate = profile["sampling_candidates"][1]
    assert second_candidate["labels"] == ["second_point_parity_stand_in"]
    assert second_candidate["sampling_priority"] == "high"
    assert second_candidate["suggested_next_action"] == "collect_additional_point_candidate"
    assert "missing_event_candidates" in second_candidate["coverage_gaps"]
    assert "demo_stand_in_only" in second_candidate["coverage_gaps"]
    assert second_candidate["warnings"]["demo_stand_in_only"] is True
    assert not FORBIDDEN_COVERAGE_SAMPLING_FIELDS & _walk_keys(profile)


def test_coverage_sampling_profile_marks_single_point_only(
    tmp_path: Path,
) -> None:
    artifacts = _build_corpus_artifacts(tmp_path, include_second_point=False)

    result = build_coverage_sampling_profile(
        source_corpus_manifest_path=artifacts["corpus_manifest"],
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=None,
    )

    assert result["ok"] is True
    profile = result["profile"]
    candidate = profile["sampling_candidates"][0]
    assert "single_point_only" in candidate["coverage_gaps"]
    assert candidate["sampling_priority"] == "high"
    assert candidate["suggested_next_action"] == "collect_distinct_second_point"
    assert profile["known_limitations"][0]["limitation_type"] == "single_point_only"


def test_validate_coverage_sampling_profile_reports_coverage_gaps(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    artifacts = _build_corpus_artifacts(tmp_path, include_second_point=True)
    profile_path = tmp_path / "exports" / "coverage_sampling_profile.current.json"
    build_coverage_sampling_profile(
        source_corpus_manifest_path=artifacts["corpus_manifest"],
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=profile_path,
    )

    result = validate_coverage_sampling_profile(
        contract_path=paths["coverage_sampling_contract"],
        profile_path=profile_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        output_path=tmp_path / "exports" / "coverage_sampling.validation.json",
        validated_at=datetime(2026, 6, 18, 15, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "valid"
    assert result["error_count"] == 0
    assert result["validated_at"] == "2026-06-18T15:05:00+00:00"
    assert len(result["referenced_contract_validations"]) == 6
    assert all(item["ok"] is True for item in result["referenced_contract_validations"])
    assert {item["warning_type"] for item in result["structural_warnings"]} == {
        "coverage_gap_present"
    }
    assert result["known_limitations"][6] == "Validation does not execute sampling."


def test_validate_coverage_sampling_profile_rejects_forbidden_fields(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    artifacts = _build_corpus_artifacts(tmp_path, include_second_point=False)
    profile_path = tmp_path / "exports" / "invalid_coverage_sampling_profile.json"
    build_coverage_sampling_profile(
        source_corpus_manifest_path=artifacts["corpus_manifest"],
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=profile_path,
    )
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["sampling_candidates"][0]["score"] = "15-0"
    profile["sampling_candidates"][0]["sampling_priority"] = "urgent"
    profile["sampling_candidates"][0]["suggested_next_action"] = "ingest_media_now"
    _write_json(profile_path, profile)

    result = validate_coverage_sampling_profile(
        contract_path=paths["coverage_sampling_contract"],
        profile_path=profile_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        output_path=None,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid"
    error_types = {error["error_type"] for error in result["errors"]}
    assert "forbidden_field" in error_types
    assert "invalid_sampling_priority" in error_types
    assert "invalid_suggested_next_action" in error_types
    assert result["warnings"]["does_not_execute_sampling"] is True


def test_build_coverage_sampling_report_summarizes_structure_only(
    tmp_path: Path,
) -> None:
    paths = _contract_paths(tmp_path)
    artifacts = _build_corpus_artifacts(tmp_path, include_second_point=True)
    profile_path = tmp_path / "exports" / "coverage_sampling_profile.current.json"
    report_path = tmp_path / "exports" / "coverage_sampling_report.current.json"
    build_coverage_sampling_profile(
        source_corpus_manifest_path=artifacts["corpus_manifest"],
        source_index_path=artifacts["index"],
        source_matrix_path=artifacts["matrix"],
        output_path=profile_path,
    )

    result = build_coverage_sampling_report(
        contract_path=paths["coverage_sampling_contract"],
        profile_path=profile_path,
        observation_quality_taxonomy_path=paths["observation_quality_taxonomy"],
        review_label_schema_path=paths["review_label_schema"],
        reviewer_confidence_schema_path=paths["reviewer_confidence_schema"],
        multi_reviewer_schema_path=paths["multi_reviewer_schema"],
        intennse_alignment_contract_path=paths["intennse_contract"],
        dataset_corpus_contract_path=paths["dataset_corpus_contract"],
        output_path=report_path,
        generated_at=datetime(2026, 6, 18, 15, 10, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["report_type"] == COVERAGE_SAMPLING_REPORT_TYPE
    assert result["report_version"] == COVERAGE_SAMPLING_REPORT_VERSION
    assert result["summary"]["sampling_candidate_count"] == 2
    assert result["summary"]["coverage_gap_present_count"] == 2
    assert result["summary"]["demo_stand_in_only_count"] == 1
    assert report_path.is_file()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["generated_at"] == "2026-06-18T15:10:00+00:00"
    assert report["warnings"]["report_is_structural_only"] is True
    assert report["warnings"]["does_not_execute_next_actions"] is True
    assert {item["coverage_gap_type"] for item in report["missing_optional_refs"]} >= {
        "missing_review_labels",
        "missing_reviewer_confidence",
        "missing_intennse_alignment",
    }
    assert not FORBIDDEN_COVERAGE_SAMPLING_FIELDS & _walk_keys(report)


def _build_corpus_artifacts(tmp_path: Path, *, include_second_point: bool) -> dict[str, Path]:
    manifest_root = tmp_path / "manifests"
    _seed_point_manifests(manifest_root, include_second_point=include_second_point)
    index_path = tmp_path / "exports" / "multi_point_replay_index.json"
    matrix_path = tmp_path / "exports" / "multi_point_regression_matrix.current.json"
    corpus_path = tmp_path / "exports" / "versioned_dataset_corpus_manifest.current.json"
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
    corpus_result = build_versioned_dataset_corpus_manifest(
        source_index_path=index_path,
        source_matrix_path=matrix_path,
        output_path=corpus_path,
        generated_at=datetime(2026, 6, 18, 14, 0, tzinfo=UTC),
    )
    assert corpus_result["ok"] is True
    return {"index": index_path, "matrix": matrix_path, "corpus_manifest": corpus_path}


def _seed_point_manifests(manifest_root: Path, *, include_second_point: bool) -> None:
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
    if include_second_point:
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
        "coverage_sampling_contract": tmp_path
        / "contracts"
        / "coverage_sampling_strategy_contract_v1.json",
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
    export_coverage_sampling_strategy_contract(
        output_path=paths["coverage_sampling_contract"]
    )
    export_versioned_dataset_corpus_contract(
        output_path=paths["dataset_corpus_contract"]
    )
    export_intennse_label_alignment_contract(output_path=paths["intennse_contract"])
    export_observation_quality_taxonomy(output_path=paths["observation_quality_taxonomy"])
    export_review_label_schema(output_path=paths["review_label_schema"])
    export_reviewer_confidence_schema(output_path=paths["reviewer_confidence_schema"])
    export_multi_reviewer_disagreement_schema(output_path=paths["multi_reviewer_schema"])
    return paths


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
