from __future__ import annotations

import copy
import json

from apps.worker.services.reviewed_3d_debug_dataset_regression import (
    compare_reviewed_3d_debug_dataset_exports,
)


def test_identical_reviewed_3d_debug_exports_return_no_drift(tmp_path) -> None:
    baseline_path = _write_export(tmp_path / "baseline.json", _sample_export())
    current_path = _write_export(tmp_path / "current.json", _sample_export())

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["regression_type"] == "reviewed_3d_debug_dataset_regression_report"
    assert result["regression_version"] == "v0"
    assert result["summary"]["drift_detected"] is False
    assert result["summary"]["baseline_event_marker_count"] == 2
    assert result["summary"]["current_event_marker_count"] == 2
    assert result["summary"]["baseline_trajectory_3d_candidate_count"] == 2
    assert result["summary"]["current_trajectory_3d_candidate_count"] == 2
    assert result["summary"]["baseline_event_candidate_3d_diagnostic_count"] == 1
    assert result["summary"]["current_event_candidate_3d_diagnostic_count"] == 1
    assert result["warnings"]["baseline_is_not_truth"] is True
    assert result["warnings"]["not_training_truth"] is True
    assert "accepted_track" not in str(result)


def test_summary_count_drift_is_reported(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["summary"]["event_marker_count"] = 3
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert result["ok"] is True
    assert result["status"] == "completed_with_drift"
    assert result["summary"]["drift_detected"] is True
    assert result["drift"]["summary_count_drift"] == [
        {"field": "event_marker_count", "baseline": 2, "current": 3}
    ]


def test_missing_section_drift_is_reported(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    del current["trajectory_3d_candidates"]
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert {
        "section": "trajectory_3d_candidates",
        "baseline_present": True,
        "current_present": False,
    } in result["drift"]["section_presence_drift"]


def test_event_marker_drift_is_reported(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["event_marker_summary"][0]["confidence"] = 0.72
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    drift = result["drift"]["event_marker_drift"]
    assert drift[0]["drift_type"] == "changed"
    assert drift[0]["changed_fields"] == [
        {"field": "confidence", "baseline": 0.7, "current": 0.72}
    ]


def test_trajectory_3d_candidate_drift_is_reported(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["trajectory_3d_candidates"][1]["court_y_m"] = 7.7
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    drift = result["drift"]["trajectory_3d_candidate_drift"]
    assert drift[0]["drift_type"] == "changed"
    assert drift[0]["changed_fields"] == [
        {"field": "court_y_m", "baseline": 7.6, "current": 7.7}
    ]


def test_event_candidate_3d_diagnostic_drift_is_reported(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["event_candidate_3d_diagnostics"][0]["diagnostic_label"] = "changed"
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    drift = result["drift"]["event_candidate_3d_diagnostic_drift"]
    assert drift[0]["drift_type"] == "changed"
    assert drift[0]["changed_fields"] == [
        {"field": "diagnostic_label", "baseline": "height_unknown", "current": "changed"}
    ]


def test_debug_review_drift_is_reported(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["trajectory_3d_debug_reviews"][0]["review_label"] = "needs_review"
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert result["drift"]["trajectory_3d_debug_review_drift"][0]["drift_type"] == (
        "missing_in_current"
    )
    assert result["drift"]["trajectory_3d_debug_review_drift"][1]["drift_type"] == (
        "added_in_current"
    )


def test_strict_mode_fails_on_breaking_drift(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["summary"]["trajectory_3d_candidate_count"] = 1
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
        strict=True,
    )

    assert result["ok"] is False
    assert result["status"] == "failed_regression"
    assert result["summary"]["breaking_drift_detected"] is True


def test_non_strict_mode_reports_completed_with_drift(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["warnings"]["not_3d_truth"] = False
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert result["ok"] is True
    assert result["status"] == "completed_with_drift"
    assert result["drift"]["warning_drift"] == [
        {"warning": "not_3d_truth", "baseline": True, "current": False}
    ]


def test_unsupported_format_is_rejected(tmp_path) -> None:
    baseline_path = _write_export(tmp_path / "baseline.json", _sample_export())
    current_path = _write_export(tmp_path / "current.json", _sample_export())

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
        output_format="csv",
    )

    assert result["ok"] is False
    assert result["status"] == "unsupported_format"
    assert result["warnings"]["baseline_is_not_truth"] is True


def test_output_file_writing_creates_parent_directory(tmp_path) -> None:
    baseline_path = _write_export(tmp_path / "baseline.json", _sample_export())
    current_path = _write_export(tmp_path / "current.json", _sample_export())
    output_path = tmp_path / "nested" / "regression" / "report.md"

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
        output_format="markdown",
        output_path=str(output_path),
    )

    assert result["ok"] is True
    assert result["output_path"] == str(output_path)
    assert output_path.read_text(encoding="utf-8") == result["markdown"]
    assert "# Reviewed 3D Debug Dataset Regression Report v0" in result["markdown"]
    assert "No drift detected." in result["markdown"]


def test_id_drift_is_allowed_by_default(tmp_path) -> None:
    baseline = _sample_export()
    current = _sample_export()
    current["event_marker_summary"][0]["observation_id"] = "new-hit-id"
    current["trajectory_3d_candidates"][0]["id"] = "new-3d-candidate-id"
    current["trajectory_3d_candidates"][0]["source_observation_id"] = "new-source-id"
    baseline_path = _write_export(tmp_path / "baseline.json", baseline)
    current_path = _write_export(tmp_path / "current.json", current)

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["summary"]["drift_detected"] is False


def test_comparison_does_not_mutate_input_files(tmp_path) -> None:
    baseline_path = _write_export(tmp_path / "baseline.json", _sample_export())
    current_path = _write_export(tmp_path / "current.json", _sample_export())
    baseline_before = baseline_path.read_text(encoding="utf-8")
    current_before = current_path.read_text(encoding="utf-8")

    result = compare_reviewed_3d_debug_dataset_exports(
        baseline_path=str(baseline_path),
        current_path=str(current_path),
    )

    assert result["ok"] is True
    assert baseline_path.read_text(encoding="utf-8") == baseline_before
    assert current_path.read_text(encoding="utf-8") == current_before


def _write_export(path, payload: dict[str, object]):
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _sample_export() -> dict[str, object]:
    return copy.deepcopy(
        {
            "ok": True,
            "status": "completed",
            "export_type": "reviewed_3d_debug_dataset_export",
            "export_version": "v0",
            "media_id": "media-1",
            "event_candidate_run_id": "event-run-1",
            "trajectory_3d_run_id": "trajectory-3d-run-1",
            "camera_geometry_id": "camera-geometry-1",
            "summary": {
                "event_marker_count": 2,
                "trajectory_3d_candidate_count": 2,
                "event_candidate_3d_diagnostic_count": 1,
                "trajectory_3d_debug_review_count": 1,
                "event_marker_review_count": 1,
                "missing_3d_sample_note_count": 0,
            },
            "camera_geometry_summary": {"camera_model": "homography_backed_court_plane"},
            "trajectory_3d_summary": {"candidate_count": 2},
            "event_candidate_3d_diagnostic_summary": {"diagnostic_count": 1},
            "trajectory_3d_debug_review_summary": {"total_reviews": 1},
            "event_marker_summary": [
                {
                    "index": 1,
                    "observation_id": "hit-1",
                    "candidate_type": "hit_candidate",
                    "source_method": "marker_level_arbitration_v0",
                    "frame": 12,
                    "timestamp_ms": 400,
                    "confidence": 0.7,
                },
                {
                    "index": 2,
                    "observation_id": "bounce-1",
                    "candidate_type": "bounce_candidate",
                    "source_method": "marker_level_arbitration_v0",
                    "frame": 30,
                    "timestamp_ms": 1000,
                    "confidence": 0.5,
                },
            ],
            "trajectory_3d_candidates": [
                {
                    "id": "trajectory-3d-candidate-1",
                    "source_observation_id": "projection-1",
                    "frame": 12,
                    "timestamp_ms": 400,
                    "projection_method": "declared_camera_geometry_v0",
                    "court_x_m": 3.1,
                    "court_y_m": 7.2,
                    "court_z_m": None,
                    "court_z_status": "unknown",
                },
                {
                    "id": "trajectory-3d-candidate-2",
                    "source_observation_id": "projection-2",
                    "frame": 30,
                    "timestamp_ms": 1000,
                    "projection_method": "declared_camera_geometry_v0",
                    "court_x_m": 3.2,
                    "court_y_m": 7.6,
                    "court_z_m": None,
                    "court_z_status": "unknown",
                },
            ],
            "event_candidate_3d_diagnostics": [
                {
                    "id": "diagnostic-1",
                    "event_observation_id": "hit-1",
                    "candidate_type": "hit_candidate",
                    "frame": 12,
                    "timestamp_ms": 400,
                    "diagnostic_label": "height_unknown",
                    "height_status": "height_unknown",
                }
            ],
            "trajectory_3d_debug_reviews": [
                {
                    "id": "review-1",
                    "annotation_kind": "trajectory_3d_sample_review",
                    "review_label": "useful",
                    "trajectory_3d_candidate_id": "trajectory-3d-candidate-1",
                    "event_candidate_3d_diagnostic_id": "diagnostic-1",
                    "timestamp_ms": 400,
                }
            ],
            "event_candidate_reviews": [
                {
                    "id": "event-review-1",
                    "observation_id": "hit-1",
                    "candidate_type": "hit_candidate",
                    "review_label": "useful",
                    "frame": 12,
                    "timestamp_ms": 400,
                }
            ],
            "warnings": {
                "dataset_export_only": True,
                "review_metadata_only": True,
                "not_truth": True,
                "not_3d_truth": True,
                "not_training_truth": True,
                "does_not_change_event_candidates": True,
                "does_not_change_3d_candidates": True,
                "does_not_create_in_out": True,
                "does_not_create_score": True,
                "no_adjudication": True,
            },
        }
    )
