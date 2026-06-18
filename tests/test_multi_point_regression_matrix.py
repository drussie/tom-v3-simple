from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.multi_point_regression_matrix import (
    MULTI_POINT_REGRESSION_MATRIX_TYPE,
    build_multi_point_regression_matrix,
    compare_multi_point_regression_matrices,
    verify_multi_point_regression_matrix,
)
from apps.worker.services.multi_point_replay_index import build_multi_point_replay_index
from apps.worker.services.point_manifest import POINT_MANIFEST_TYPE, POINT_MANIFEST_WARNINGS

PROTECTED_MEDIA_ID = "9518fb01-0da1-4344-9a84-ff88ec8e9b1e"
PROTECTED_EVENT_RUN_ID = "1b946366-7ec1-426f-8b40-494535a9b3fb"
PROTECTED_TRAJECTORY_RUN_ID = "ea76ccab-c51d-4a63-9682-9fd0bbb83f14"
PROTECTED_CAMERA_GEOMETRY_ID = "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97"
FORBIDDEN_DECISION_KEYS = {
    "in_out",
    "score",
    "point_winner",
    "player_identity",
    "rally_state",
    "server_state",
    "receiver_state",
}


def test_multi_point_regression_matrix_builds_from_replay_index(tmp_path: Path) -> None:
    manifest_root = tmp_path / "manifests"
    index_path = tmp_path / "exports" / "multi_point_replay_index.json"
    matrix_path = tmp_path / "exports" / "multi_point_matrix.current.json"
    _seed_point_manifests(manifest_root, include_second_point=True)

    index_result = build_multi_point_replay_index(
        manifest_root=manifest_root,
        output_path=index_path,
        generated_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
    )
    assert index_result["ok"] is True

    result = build_multi_point_regression_matrix(
        source_index_path=index_path,
        output_path=matrix_path,
        generated_at=datetime(2026, 6, 17, 12, 5, tzinfo=UTC),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["matrix_type"] == MULTI_POINT_REGRESSION_MATRIX_TYPE
    assert result["point_count"] == 2
    assert matrix_path.is_file()

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    assert matrix["generated_at"] == "2026-06-17T12:05:00+00:00"
    assert matrix["source_index_path"] == str(index_path)
    assert matrix["source_index_skipped_manifest_count"] == 1
    assert matrix["summary"] == {
        "point_count": 2,
        "protected_sample_point_count": 1,
        "second_point_parity_stand_in_count": 1,
        "replay_available_count": 2,
        "event_candidates_available_count": 1,
        "trajectory_3d_candidates_available_count": 1,
        "review_annotations_available_count": 1,
        "trajectory_3d_debug_reviews_available_count": 0,
    }
    assert matrix["warnings"]["matrix_is_not_truth"] is True
    assert matrix["warnings"]["baseline_is_not_truth"] is True
    assert matrix["warnings"]["regression_report_only"] is True
    assert matrix["warnings"]["no_adjudication"] is True

    protected_row = matrix["points"][0]
    assert protected_row["labels"] == ["protected_sample_point"]
    assert protected_row["associated_run_ids"]["event_candidate_run_id"] == PROTECTED_EVENT_RUN_ID
    assert protected_row["matrix_row_warnings"]["manifest_file_available"] is True
    assert protected_row["matrix_row_warnings"]["manifest_identity_matches_index"] is True
    assert protected_row["warnings"]["manifest_is_not_truth"] is True

    second_row = matrix["points"][1]
    assert second_row["labels"] == ["second_point_parity_stand_in"]
    assert second_row["evidence_availability"]["event_candidates_available"] is False
    assert not FORBIDDEN_DECISION_KEYS & _walk_keys(matrix)


def test_multi_point_regression_compare_treats_added_points_as_non_breaking(
    tmp_path: Path,
) -> None:
    baseline_path = _build_matrix(
        tmp_path / "baseline",
        include_second_point=False,
        output_name="baseline.json",
    )
    current_path = _build_matrix(
        tmp_path / "current",
        include_second_point=True,
        output_name="current.json",
    )

    result = compare_multi_point_regression_matrices(
        baseline_path=baseline_path,
        current_path=current_path,
        output_path=tmp_path / "regression.json",
    )

    assert result["ok"] is True
    assert result["status"] == "completed_with_drift"
    assert result["summary"]["drift_detected"] is True
    assert result["summary"]["breaking_drift_detected"] is False
    added = result["drift"]["point_presence_drift"][0]
    assert added["drift_type"] == "added_in_current"
    assert added["breaking"] is False
    assert result["warnings"]["not_generalization_claim"] is True

    strict_result = compare_multi_point_regression_matrices(
        baseline_path=baseline_path,
        current_path=current_path,
        strict=True,
    )
    assert strict_result["ok"] is False
    assert strict_result["summary"]["breaking_drift_detected"] is True


def test_multi_point_regression_compare_marks_protected_count_drift_breaking(
    tmp_path: Path,
) -> None:
    baseline_path = _build_matrix(
        tmp_path / "baseline",
        include_second_point=False,
        output_name="baseline.json",
    )
    current_path = _build_matrix(
        tmp_path / "current",
        include_second_point=False,
        output_name="current.json",
    )
    current = json.loads(current_path.read_text(encoding="utf-8"))
    current["points"][0]["profile_counts"]["event_marker_count"] = 1
    current_path.write_text(json.dumps(current, indent=2, sort_keys=True), encoding="utf-8")

    result = compare_multi_point_regression_matrices(
        baseline_path=baseline_path,
        current_path=current_path,
    )

    assert result["ok"] is False
    assert result["status"] == "failed_regression"
    assert result["summary"]["drift_detected"] is True
    assert result["summary"]["breaking_drift_detected"] is True
    drift = result["drift"]["profile_count_drift"][0]
    assert drift["field"] == "profile_counts"
    assert drift["breaking"] is True


def test_multi_point_regression_verify_writes_current_and_reports(
    tmp_path: Path,
) -> None:
    baseline_path = _build_matrix(
        tmp_path / "baseline",
        include_second_point=False,
        output_name="baseline.json",
    )
    index_path = _build_index(
        tmp_path / "current",
        include_second_point=False,
        output_name="index.json",
    )
    current_output = tmp_path / "outputs" / "current.json"
    regression_output = tmp_path / "outputs" / "regression.json"
    markdown_output = tmp_path / "outputs" / "regression.md"

    result = verify_multi_point_regression_matrix(
        source_index_path=index_path,
        baseline_path=baseline_path,
        current_output=current_output,
        regression_output=regression_output,
        regression_markdown_output=markdown_output,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert current_output.is_file()
    assert regression_output.is_file()
    assert markdown_output.is_file()
    assert result["regression_summary"]["drift_detected"] is False
    assert result["warnings"]["regression_report_only"] is True


def _build_matrix(root: Path, *, include_second_point: bool, output_name: str) -> Path:
    index_path = _build_index(
        root,
        include_second_point=include_second_point,
        output_name="index.json",
    )
    matrix_path = root / output_name
    result = build_multi_point_regression_matrix(
        source_index_path=index_path,
        output_path=matrix_path,
        generated_at=datetime(2026, 6, 17, 12, 5, tzinfo=UTC),
    )
    assert result["ok"] is True
    return matrix_path


def _build_index(root: Path, *, include_second_point: bool, output_name: str) -> Path:
    manifest_root = root / "manifests"
    _seed_point_manifests(manifest_root, include_second_point=include_second_point)
    index_path = root / output_name
    result = build_multi_point_replay_index(
        manifest_root=manifest_root,
        output_path=index_path,
        generated_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
    )
    assert result["ok"] is True
    return index_path


def _seed_point_manifests(manifest_root: Path, *, include_second_point: bool) -> None:
    _write_json(
        manifest_root / "sample_point.point_manifest.json",
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
            profile_counts={
                "event_marker_count": 2,
                "trajectory_3d_candidate_count": 12,
                "review_annotation_count": 3,
            },
        ),
    )
    _write_json(
        manifest_root / "zzz_duplicate_sample_point.point_manifest.json",
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
            profile_counts={
                "event_marker_count": 2,
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
                profile_counts={
                    "event_marker_count": 0,
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
    profile_counts: dict[str, int],
) -> dict[str, Any]:
    counts = {
        "event_marker_count": 0,
        "hit_candidate_count": 0,
        "bounce_candidate_count": 0,
        "event_candidate_observation_count": 0,
        "event_candidate_rejection_diagnostic_count": 0,
        "trajectory_3d_candidate_count": 0,
        "event_candidate_3d_diagnostic_count": 0,
        "event_marker_review_count": 0,
        "trajectory_3d_debug_review_count": 0,
        "human_annotation_count": 0,
        "review_annotation_count": 0,
        **profile_counts,
    }
    return {
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": "v0",
        "point_manifest_id": point_manifest_id,
        "media_id": media_id,
        "source_media_path": source_media_path,
        "source_uri": f"file://{source_media_path}",
        "stored_path": source_media_path,
        "stored_uri": f"file://{source_media_path}",
        "replay_url": replay_url,
        "generated_at": "2026-06-17T12:00:00+00:00",
        "tom_provenance": {
            "project": "tom-v3-simple",
            "project_version": "0.0.0",
            "blueprint": "blueprint_23",
        },
        "associated_run_ids": associated_run_ids,
        "evidence_availability": {
            "media_indexed": True,
            "replay_available": True,
            "event_candidates_available": counts["event_marker_count"] > 0,
            "trajectory_3d_candidates_available": counts["trajectory_3d_candidate_count"] > 0,
            "event_candidate_3d_diagnostics_available": False,
            "review_annotations_available": counts["review_annotation_count"] > 0,
            "trajectory_3d_debug_reviews_available": False,
        },
        "profile_counts": counts,
        "warnings": dict(POINT_MANIFEST_WARNINGS),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_walk_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_walk_keys(item))
        return keys
    return set()
