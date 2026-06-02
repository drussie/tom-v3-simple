from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from apps.worker.services.reviewed_3d_debug_dataset_export import (
    export_reviewed_3d_debug_dataset,
)
from apps.worker.services.reviewed_3d_debug_dataset_regression import (
    compare_reviewed_3d_debug_dataset_exports,
)

BASELINE_MANIFEST_TYPE = "reviewed_3d_debug_baseline_manifest"
BASELINE_MANIFEST_VERSION = "v0"
DEFAULT_BASELINE_NAME = "sample_point_reviewed_3d_debug_baseline_v0"
DEFAULT_BASELINE_FILE_STEM = "reviewed_3d_debug_dataset_sample_point"

BASELINE_WARNINGS = {
    "baseline_is_not_truth": True,
    "dataset_export_only": True,
    "not_truth": True,
    "not_3d_truth": True,
    "not_training_truth": True,
    "no_adjudication": True,
}


def freeze_reviewed_3d_debug_baseline(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str,
    baseline_dir: str = ".data/baselines",
    baseline_name: str = DEFAULT_BASELINE_NAME,
    file_stem: str = DEFAULT_BASELINE_FILE_STEM,
    viewer_base_url: str = "http://127.0.0.1:3000",
    exporter: Callable[..., dict[str, Any]] = export_reviewed_3d_debug_dataset,
) -> dict[str, Any]:
    """Write a local reviewed 3D debug baseline export and manifest."""

    baseline_root = Path(baseline_dir)
    baseline_json_path = baseline_root / f"{file_stem}.baseline.json"
    baseline_markdown_path = baseline_root / f"{file_stem}.baseline.md"
    manifest_path = baseline_root / f"{file_stem}.baseline_manifest.json"

    json_export = exporter(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
        viewer_base_url=viewer_base_url,
        output_format="json",
        output_path=str(baseline_json_path),
    )
    if json_export.get("ok") is False:
        return _failed(
            "baseline_json_export_failed",
            "failed to write baseline JSON export",
            details=json_export,
        )

    markdown_export = exporter(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
        viewer_base_url=viewer_base_url,
        output_format="markdown",
        output_path=str(baseline_markdown_path),
    )
    if markdown_export.get("ok") is False:
        return _failed(
            "baseline_markdown_export_failed",
            "failed to write baseline Markdown export",
            details=markdown_export,
        )

    manifest = build_reviewed_3d_debug_baseline_manifest(
        export_payload=json_export,
        baseline_name=baseline_name,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
        baseline_json_path=str(baseline_json_path),
        baseline_markdown_path=str(baseline_markdown_path),
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    return {
        "ok": True,
        "status": "completed",
        "baseline_type": "reviewed_3d_debug_baseline_freeze",
        "baseline_version": "v0",
        "baseline_name": baseline_name,
        "media_id": media_id,
        "event_candidate_run_id": event_candidate_run_id,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "camera_geometry_id": camera_geometry_id,
        "baseline_paths": {
            "json": str(baseline_json_path),
            "markdown": str(baseline_markdown_path),
            "manifest": str(manifest_path),
        },
        "expected_summary": manifest["expected_summary"],
        "manifest": manifest,
        "warnings": dict(BASELINE_WARNINGS),
    }


def verify_reviewed_3d_debug_baseline(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str,
    baseline_path: str,
    current_output: str = ".data/exports/reviewed_3d_debug_dataset_sample_point.current.json",
    regression_output: str = ".data/exports/reviewed_3d_debug_dataset_sample_point.regression.json",
    regression_markdown_output: str | None = None,
    strict: bool = False,
    viewer_base_url: str = "http://127.0.0.1:3000",
    exporter: Callable[..., dict[str, Any]] = export_reviewed_3d_debug_dataset,
    comparator: Callable[..., dict[str, Any]] = compare_reviewed_3d_debug_dataset_exports,
) -> dict[str, Any]:
    """Export the current reviewed 3D debug dataset and compare it to a baseline."""

    baseline = Path(baseline_path)
    if not baseline.is_file():
        return _failed(
            "missing_baseline_export",
            f"baseline export not found: {baseline_path}",
        )

    current_export = exporter(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
        viewer_base_url=viewer_base_url,
        output_format="json",
        output_path=current_output,
    )
    if current_export.get("ok") is False:
        return _failed(
            "current_export_failed",
            "failed to write current reviewed 3D debug export",
            details=current_export,
        )

    regression = comparator(
        baseline_path=baseline_path,
        current_path=current_output,
        strict=strict,
        output_format="json",
        output_path=regression_output,
    )
    markdown_path = regression_markdown_output or _markdown_path_for(regression_output)
    regression_markdown = comparator(
        baseline_path=baseline_path,
        current_path=current_output,
        strict=False,
        output_format="markdown",
        output_path=markdown_path,
    )

    result_ok = bool(regression.get("ok") is not False)
    return {
        "ok": result_ok,
        "status": regression.get("status", "failed_regression"),
        "baseline_gate_type": "reviewed_3d_debug_baseline_regression_gate",
        "baseline_gate_version": "v0",
        "media_id": media_id,
        "event_candidate_run_id": event_candidate_run_id,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "camera_geometry_id": camera_geometry_id,
        "baseline_path": baseline_path,
        "current_output": current_output,
        "regression_output": regression_output,
        "regression_markdown_output": markdown_path,
        "regression_summary": regression.get("summary", {}),
        "drift": regression.get("drift", {}),
        "regression": regression,
        "regression_markdown_status": regression_markdown.get("status"),
        "warnings": dict(BASELINE_WARNINGS),
    }


def build_reviewed_3d_debug_baseline_manifest(
    *,
    export_payload: dict[str, Any],
    baseline_name: str,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str,
    baseline_json_path: str,
    baseline_markdown_path: str,
) -> dict[str, Any]:
    return {
        "manifest_type": BASELINE_MANIFEST_TYPE,
        "manifest_version": BASELINE_MANIFEST_VERSION,
        "baseline_name": baseline_name,
        "media_id": media_id,
        "event_candidate_run_id": event_candidate_run_id,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "camera_geometry_id": camera_geometry_id,
        "expected_summary": dict(_dict(export_payload.get("summary"))),
        "baseline_paths": {
            "json": baseline_json_path,
            "markdown": baseline_markdown_path,
        },
        "warnings": dict(BASELINE_WARNINGS),
    }


def _failed(
    status: str,
    message: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(BASELINE_WARNINGS),
    }
    if details is not None:
        result["details"] = details
    return result


def _markdown_path_for(path: str) -> str:
    candidate = Path(path)
    if candidate.suffix:
        return str(candidate.with_suffix(".md"))
    return f"{path}.md"


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
