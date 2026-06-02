from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apps.worker.services.reviewed_3d_debug_baseline import (
    BASELINE_MANIFEST_TYPE,
    build_reviewed_3d_debug_baseline_manifest,
    freeze_reviewed_3d_debug_baseline,
    verify_reviewed_3d_debug_baseline,
)
from apps.worker.services.reviewed_3d_debug_dataset_regression import (
    compare_reviewed_3d_debug_dataset_exports,
)


def test_baseline_manifest_generation_uses_expected_counts() -> None:
    manifest = build_reviewed_3d_debug_baseline_manifest(
        export_payload=_sample_export(),
        baseline_name="sample_point_reviewed_3d_debug_baseline_v0",
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_json_path=".data/baselines/baseline.json",
        baseline_markdown_path=".data/baselines/baseline.md",
    )

    assert manifest["manifest_type"] == BASELINE_MANIFEST_TYPE
    assert manifest["manifest_version"] == "v0"
    assert manifest["expected_summary"]["event_marker_count"] == 6
    assert manifest["expected_summary"]["trajectory_3d_candidate_count"] == 68
    assert manifest["expected_summary"]["event_candidate_3d_diagnostic_count"] == 6
    assert manifest["expected_summary"]["event_marker_review_count"] == 1
    assert manifest["warnings"]["baseline_is_not_truth"] is True
    assert manifest["warnings"]["not_training_truth"] is True
    assert "accepted_track" not in str(manifest)


def test_freeze_baseline_writes_json_markdown_and_manifest(tmp_path) -> None:
    baseline_dir = tmp_path / "baselines"

    result = freeze_reviewed_3d_debug_baseline(
        session=_SentinelSession(),
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_dir=str(baseline_dir),
        exporter=_fake_exporter(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    json_path = baseline_dir / "reviewed_3d_debug_dataset_sample_point.baseline.json"
    markdown_path = baseline_dir / "reviewed_3d_debug_dataset_sample_point.baseline.md"
    manifest_path = baseline_dir / "reviewed_3d_debug_dataset_sample_point.baseline_manifest.json"
    assert json_path.is_file()
    assert markdown_path.is_file()
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["expected_summary"]["event_marker_count"] == 6
    assert manifest["baseline_paths"]["json"] == str(json_path)
    assert result["expected_summary"]["trajectory_3d_debug_review_count"] == 0


def test_verify_baseline_runs_export_and_compare_no_drift(tmp_path) -> None:
    baseline_path = tmp_path / "baselines" / "baseline.json"
    baseline_path.parent.mkdir(parents=True)
    baseline_path.write_text(json.dumps(_sample_export(), sort_keys=True), encoding="utf-8")
    current_output = tmp_path / "exports" / "current.json"
    regression_output = tmp_path / "exports" / "regression.json"

    result = verify_reviewed_3d_debug_baseline(
        session=_SentinelSession(),
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_path=str(baseline_path),
        current_output=str(current_output),
        regression_output=str(regression_output),
        exporter=_fake_exporter(),
        comparator=compare_reviewed_3d_debug_dataset_exports,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["regression_summary"]["drift_detected"] is False
    assert current_output.is_file()
    assert regression_output.is_file()
    assert (tmp_path / "exports" / "regression.md").is_file()
    assert result["warnings"]["baseline_is_not_truth"] is True


def test_verify_baseline_reports_drift_when_current_differs(tmp_path) -> None:
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(_sample_export(), sort_keys=True), encoding="utf-8")
    current_output = tmp_path / "current.json"
    regression_output = tmp_path / "regression.json"

    result = verify_reviewed_3d_debug_baseline(
        session=_SentinelSession(),
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_path=str(baseline_path),
        current_output=str(current_output),
        regression_output=str(regression_output),
        exporter=_fake_exporter(summary_overrides={"event_marker_count": 7}),
        comparator=compare_reviewed_3d_debug_dataset_exports,
    )

    assert result["ok"] is True
    assert result["status"] == "completed_with_drift"
    assert result["regression_summary"]["drift_detected"] is True


def test_verify_baseline_missing_baseline_produces_clear_error(tmp_path) -> None:
    result = verify_reviewed_3d_debug_baseline(
        session=_SentinelSession(),
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_path=str(tmp_path / "missing.json"),
    )

    assert result["ok"] is False
    assert result["status"] == "missing_baseline_export"
    assert "baseline export not found" in result["message"]
    assert result["warnings"]["baseline_is_not_truth"] is True


def test_verify_baseline_strict_mode_fails_on_drift(tmp_path) -> None:
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(_sample_export(), sort_keys=True), encoding="utf-8")

    result = verify_reviewed_3d_debug_baseline(
        session=_SentinelSession(),
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_path=str(baseline_path),
        current_output=str(tmp_path / "current.json"),
        regression_output=str(tmp_path / "regression.json"),
        strict=True,
        exporter=_fake_exporter(summary_overrides={"trajectory_3d_candidate_count": 67}),
        comparator=compare_reviewed_3d_debug_dataset_exports,
    )

    assert result["ok"] is False
    assert result["status"] == "failed_regression"
    assert result["regression_summary"]["breaking_drift_detected"] is True


def test_freeze_and_verify_do_not_require_db_mutation(tmp_path) -> None:
    session = _SentinelSession()
    baseline_dir = tmp_path / "baselines"

    freeze_reviewed_3d_debug_baseline(
        session=session,
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_dir=str(baseline_dir),
        exporter=_fake_exporter(),
    )
    verify_reviewed_3d_debug_baseline(
        session=session,
        media_id="media-1",
        event_candidate_run_id="event-run-1",
        trajectory_3d_run_id="trajectory-3d-run-1",
        camera_geometry_id="camera-geometry-1",
        baseline_path=str(baseline_dir / "reviewed_3d_debug_dataset_sample_point.baseline.json"),
        current_output=str(tmp_path / "exports" / "current.json"),
        regression_output=str(tmp_path / "exports" / "regression.json"),
        exporter=_fake_exporter(),
        comparator=compare_reviewed_3d_debug_dataset_exports,
    )

    assert session.mutated is False


class _SentinelSession:
    mutated = False


def _fake_exporter(summary_overrides: dict[str, int] | None = None):
    def _exporter(**kwargs: Any) -> dict[str, Any]:
        output_format = kwargs.get("output_format", "json")
        output_path = kwargs.get("output_path")
        payload = _sample_export()
        if summary_overrides:
            payload["summary"].update(summary_overrides)
        if output_path is not None:
            path = kwargs["output_path"]
            target = Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            if output_format == "markdown":
                target.write_text("# Reviewed 3D Debug Dataset Export v0\n", encoding="utf-8")
            else:
                target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        if output_format == "markdown":
            payload["markdown"] = "# Reviewed 3D Debug Dataset Export v0\n"
        payload["output_path"] = output_path
        return payload

    return _exporter


def _sample_export() -> dict[str, Any]:
    return {
        "ok": True,
        "status": "completed",
        "export_type": "reviewed_3d_debug_dataset_export",
        "export_version": "v0",
        "media_id": "media-1",
        "event_candidate_run_id": "event-run-1",
        "trajectory_3d_run_id": "trajectory-3d-run-1",
        "camera_geometry_id": "camera-geometry-1",
        "summary": {
            "event_marker_count": 6,
            "trajectory_3d_candidate_count": 68,
            "event_candidate_3d_diagnostic_count": 6,
            "event_marker_review_count": 1,
            "trajectory_3d_debug_review_count": 0,
            "missing_3d_sample_note_count": 0,
        },
        "event_marker_summary": [],
        "trajectory_3d_candidates": [],
        "event_candidate_3d_diagnostics": [],
        "trajectory_3d_debug_reviews": [],
        "event_candidate_reviews": [],
        "camera_geometry_summary": {},
        "trajectory_3d_summary": {},
        "event_candidate_3d_diagnostic_summary": {},
        "trajectory_3d_debug_review_summary": {},
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
