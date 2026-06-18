from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.worker.services.multi_point_replay_index import (
    MULTI_POINT_REPLAY_INDEX_OUTPUT,
    MULTI_POINT_REPLAY_INDEX_TYPE,
    MULTI_POINT_REPLAY_INDEX_VERSION,
)
from apps.worker.services.point_manifest import (
    POINT_MANIFEST_TYPE,
    POINT_MANIFEST_VERSION,
    POINT_MANIFEST_WARNINGS,
)

MULTI_POINT_REGRESSION_MATRIX_TYPE = "multi_point_evidence_regression_matrix"
MULTI_POINT_REGRESSION_MATRIX_VERSION = "v0"
MULTI_POINT_REGRESSION_MATRIX_BLUEPRINT = "blueprint_25"
MULTI_POINT_REGRESSION_MATRIX_BLUEPRINT_NAME = (
    "multi_point_regression_matrix_baseline_expansion_v0"
)
DEFAULT_MULTI_POINT_REGRESSION_MATRIX_BASELINE = (
    ".data/baselines/multi_point_regression_matrix.baseline.json"
)
DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT = (
    ".data/exports/multi_point_regression_matrix.current.json"
)
DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION = (
    ".data/exports/multi_point_regression_matrix.regression.json"
)
DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN = (
    ".data/exports/multi_point_regression_matrix.regression.md"
)

MATRIX_WARNINGS = {
    "matrix_is_not_truth": True,
    "baseline_is_not_truth": True,
    "regression_report_only": True,
    "observation_only": True,
    "navigation_only": True,
    "no_adjudication": True,
    "does_not_create_observations": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "does_not_identify_players": True,
    "does_not_determine_winner": True,
    "not_generalization_claim": True,
}

MATRIX_ROW_WARNINGS = {
    "matrix_row_is_not_truth": True,
    "observation_only": True,
    "navigation_only": True,
    "no_adjudication": True,
    "does_not_create_observations": True,
    "does_not_create_event_candidates": True,
    "does_not_create_3d_candidates": True,
}

SUMMARY_AVAILABILITY_FIELDS = (
    "replay_available",
    "event_candidates_available",
    "trajectory_3d_candidates_available",
    "review_annotations_available",
    "trajectory_3d_debug_reviews_available",
)

MATRIX_REQUIRED_SECTIONS = (
    "matrix_type",
    "matrix_version",
    "source_index_path",
    "point_count",
    "points",
    "summary",
    "warnings",
)


def build_multi_point_regression_matrix(
    *,
    source_index_path: str | Path = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    output_path: str | Path | None = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a read-only regression matrix from a Blueprint 24 replay index."""

    loaded_index = _load_json(source_index_path, label="source_index")
    if loaded_index.get("ok") is False:
        return loaded_index
    source_index = _dict(loaded_index["data"])
    validation = _validate_source_index(source_index)
    if validation is not None:
        return validation

    generated_at = generated_at or datetime.now(UTC)
    points = [
        _matrix_point_from_index_point(point)
        for point in _list(source_index.get("points"))
        if isinstance(point, dict)
    ]
    summary = _matrix_summary(points)
    matrix: dict[str, Any] = {
        "matrix_type": MULTI_POINT_REGRESSION_MATRIX_TYPE,
        "matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "generated_at": generated_at.isoformat(),
        "source_index_path": str(Path(source_index_path)),
        "source_index_type": source_index.get("index_type"),
        "source_index_version": source_index.get("index_version"),
        "source_index_generated_at": source_index.get("generated_at"),
        "source_index_skipped_manifest_count": int(
            source_index.get("skipped_manifest_count") or 0
        ),
        "source_index_skipped_manifests": _list(source_index.get("skipped_manifests")),
        "point_count": len(points),
        "points": points,
        "summary": summary,
        "tom_provenance": {
            "project": "tom-v3-simple",
            "project_version": "0.0.0",
            "blueprint": MULTI_POINT_REGRESSION_MATRIX_BLUEPRINT,
            "blueprint_name": MULTI_POINT_REGRESSION_MATRIX_BLUEPRINT_NAME,
        },
        "warnings": dict(MATRIX_WARNINGS),
    }

    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "matrix_type": MULTI_POINT_REGRESSION_MATRIX_TYPE,
        "matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "source_index_path": str(Path(source_index_path)),
        "point_count": len(points),
        "summary": summary,
        "matrix": matrix,
        "warnings": dict(MATRIX_WARNINGS),
    }
    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(matrix, indent=2, sort_keys=True), encoding="utf-8")
        result["matrix_output"] = str(path)
    return result


def compare_multi_point_regression_matrices(
    *,
    baseline_path: str | Path,
    current_path: str | Path,
    strict: bool = False,
    output_format: str = "json",
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Compare two multi-point regression matrices without adjudicating evidence."""

    if output_format not in {"json", "markdown"}:
        return _failed(
            "unsupported_format",
            f"unsupported multi-point regression matrix format: {output_format}",
        )

    baseline_loaded = _load_json(baseline_path, label="baseline")
    if baseline_loaded.get("ok") is False:
        return baseline_loaded
    current_loaded = _load_json(current_path, label="current")
    if current_loaded.get("ok") is False:
        return current_loaded

    baseline = _dict(baseline_loaded["data"])
    current = _dict(current_loaded["data"])
    drift = _matrix_drift(baseline=baseline, current=current, strict=strict)
    drift_detected = any(bool(items) for items in drift.values())
    breaking_drift_detected = any(
        item.get("breaking") is True
        for items in drift.values()
        for item in items
        if isinstance(item, dict)
    )

    result: dict[str, Any] = {
        "ok": not breaking_drift_detected,
        "status": (
            "failed_regression"
            if breaking_drift_detected
            else "completed_with_drift"
            if drift_detected
            else "completed"
        ),
        "regression_type": "multi_point_regression_matrix_report",
        "regression_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "baseline_path": str(Path(baseline_path)),
        "current_path": str(Path(current_path)),
        "comparison_config": {"strict": strict},
        "summary": _comparison_summary(
            baseline=baseline,
            current=current,
            drift_detected=drift_detected,
            breaking_drift_detected=breaking_drift_detected,
        ),
        "drift": drift,
        "warnings": dict(MATRIX_WARNINGS),
        "known_limitations": [
            "Regression drift is a matrix difference, not proof of incorrectness.",
            "The baseline matrix is not truth, 3D truth, or training truth.",
            "The report does not change live observations, event candidates, or 3D candidates.",
            (
                "The report does not create in/out, score, point winner, player identity, "
                "or adjudication decisions."
            ),
            (
                "Additional manifest-backed points are additive structure only and not a "
                "generalization claim."
            ),
        ],
    }

    if output_format == "markdown":
        result["markdown"] = render_multi_point_regression_matrix_markdown(result)

    if output_path is not None and str(output_path).strip():
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(result["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["output_path"] = str(path)

    return result


def verify_multi_point_regression_matrix(
    *,
    source_index_path: str | Path = MULTI_POINT_REPLAY_INDEX_OUTPUT,
    baseline_path: str | Path = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_BASELINE,
    current_output: str | Path = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_CURRENT,
    regression_output: str | Path = DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION,
    regression_markdown_output: str | Path = (
        DEFAULT_MULTI_POINT_REGRESSION_MATRIX_REGRESSION_MARKDOWN
    ),
    strict: bool = False,
) -> dict[str, Any]:
    baseline = Path(baseline_path).expanduser()
    if not baseline.is_file():
        return _failed(
            "missing_baseline_matrix",
            f"baseline matrix not found: {baseline_path}",
        )

    current = build_multi_point_regression_matrix(
        source_index_path=source_index_path,
        output_path=current_output,
    )
    if current.get("ok") is False:
        return _failed(
            "current_matrix_build_failed",
            "failed to build current multi-point regression matrix",
            details=current,
        )

    regression = compare_multi_point_regression_matrices(
        baseline_path=baseline_path,
        current_path=current_output,
        strict=strict,
        output_format="json",
        output_path=regression_output,
    )
    regression_markdown = compare_multi_point_regression_matrices(
        baseline_path=baseline_path,
        current_path=current_output,
        strict=False,
        output_format="markdown",
        output_path=regression_markdown_output,
    )
    return {
        "ok": regression.get("ok") is not False,
        "status": regression.get("status", "failed_regression"),
        "baseline_gate_type": "multi_point_regression_matrix_gate",
        "baseline_gate_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "source_index_path": str(Path(source_index_path)),
        "baseline_path": str(Path(baseline_path)),
        "current_output": str(Path(current_output)),
        "regression_output": str(Path(regression_output)),
        "regression_markdown_output": str(Path(regression_markdown_output)),
        "matrix_summary": current.get("summary", {}),
        "regression_summary": regression.get("summary", {}),
        "drift": regression.get("drift", {}),
        "regression": regression,
        "regression_markdown_status": regression_markdown.get("status"),
        "warnings": dict(MATRIX_WARNINGS),
    }


def render_multi_point_regression_matrix_markdown(result: dict[str, Any]) -> str:
    summary = _dict(result.get("summary"))
    drift = _dict(result.get("drift"))
    rows = [
        "# Multi-Point Regression Matrix Report v0",
        "",
        f"Baseline path: `{result.get('baseline_path')}`  ",
        f"Current path: `{result.get('current_path')}`  ",
        f"Status: `{result.get('status')}`",
        "",
        "## Drift Status",
        "",
        "Drift detected." if summary.get("drift_detected") else "No drift detected.",
        "",
        "## Summary",
        "",
        "| Field | Baseline | Current |",
        "|---|---:|---:|",
    ]
    for key in sorted(
        key.removeprefix("baseline_")
        for key in summary
        if key.startswith("baseline_")
    ):
        rows.append(
            "| {field} | {baseline} | {current} |".format(
                field=key,
                baseline=summary.get(f"baseline_{key}", 0),
                current=summary.get(f"current_{key}", 0),
            )
        )
    rows.extend(["", "## Drift Tables", "", "| Drift kind | Count |", "|---|---:|"])
    for key in sorted(drift):
        items = drift.get(key)
        count = len(items) if isinstance(items, list) else 0
        rows.append(f"| {key} | {count} |")
    rows.extend(["", "## Details", ""])
    for key in sorted(drift):
        items = drift.get(key)
        if not isinstance(items, list) or not items:
            continue
        rows.append(f"### {key}")
        rows.append("")
        for item in items[:10]:
            rows.append(f"- `{json.dumps(item, sort_keys=True)}`")
        if len(items) > 10:
            rows.append(f"- ... {len(items) - 10} more drift rows")
        rows.append("")
    rows.extend(
        [
            "## Warnings",
            "",
            "- Regression report only.",
            "- Matrix and baseline are not truth.",
            "- Observation-only and navigation-only.",
            (
                "- Does not create observations, event candidates, 3D candidates, in/out, "
                "score, player identity, winner, or adjudication."
            ),
            "- Not a generalization claim.",
            "",
            "## Known Limitations",
            "",
        ]
    )
    for limitation in result.get("known_limitations", []):
        rows.append(f"- {limitation}")
    rows.append("")
    return "\n".join(rows)


def _validate_source_index(source_index: dict[str, Any]) -> dict[str, Any] | None:
    if source_index.get("index_type") != MULTI_POINT_REPLAY_INDEX_TYPE:
        return _failed(
            "invalid_source_index_type",
            f"source index must have index_type {MULTI_POINT_REPLAY_INDEX_TYPE}",
        )
    if source_index.get("index_version") != MULTI_POINT_REPLAY_INDEX_VERSION:
        return _failed(
            "unsupported_source_index_version",
            f"source index must have index_version {MULTI_POINT_REPLAY_INDEX_VERSION}",
        )
    return None


def _matrix_point_from_index_point(point: dict[str, Any]) -> dict[str, Any]:
    manifest_path = _string_or_none(point.get("manifest_path"))
    manifest = _load_point_manifest(manifest_path)
    row_warnings = {
        **dict(MATRIX_ROW_WARNINGS),
        "manifest_file_available": manifest.get("ok") is True,
        "manifest_identity_matches_index": _manifest_identity_matches_index(
            manifest=_dict(manifest.get("data")),
            point=point,
        ),
    }
    return {
        "point_manifest_id": _string_or_none(point.get("point_manifest_id")),
        "media_id": _string_or_none(point.get("media_id")),
        "labels": sorted(_string_list(point.get("labels"))),
        "manifest_path": manifest_path,
        "replay_url": _string_or_none(point.get("replay_url")),
        "associated_run_ids": _string_dict(point.get("associated_run_ids")),
        "evidence_availability": _bool_dict(point.get("evidence_availability")),
        "profile_counts": _int_dict(point.get("profile_counts")),
        "warnings": {
            **dict(POINT_MANIFEST_WARNINGS),
            **_bool_dict(point.get("warnings")),
        },
        "matrix_row_warnings": row_warnings,
    }


def _load_point_manifest(manifest_path: str | None) -> dict[str, Any]:
    if manifest_path is None:
        return {"ok": False, "status": "missing_manifest_path"}
    loaded = _load_json(manifest_path, label="point_manifest", fail_as_result=False)
    if loaded.get("ok") is False:
        return loaded
    manifest = _dict(loaded["data"])
    if manifest.get("manifest_type") != POINT_MANIFEST_TYPE:
        return {"ok": False, "status": "invalid_point_manifest_type", "data": manifest}
    if manifest.get("manifest_version") != POINT_MANIFEST_VERSION:
        return {"ok": False, "status": "unsupported_point_manifest_version", "data": manifest}
    return {"ok": True, "status": "loaded", "data": manifest}


def _manifest_identity_matches_index(
    *,
    manifest: dict[str, Any],
    point: dict[str, Any],
) -> bool:
    if not manifest:
        return False
    for key in ("point_manifest_id", "media_id"):
        if manifest.get(key) != point.get(key):
            return False
    manifest_runs = _string_dict(manifest.get("associated_run_ids"))
    index_runs = _string_dict(point.get("associated_run_ids"))
    return manifest_runs == index_runs


def _matrix_summary(points: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "point_count": len(points),
        "protected_sample_point_count": 0,
        "second_point_parity_stand_in_count": 0,
    }
    for field in SUMMARY_AVAILABILITY_FIELDS:
        summary[f"{field}_count"] = 0
    for point in points:
        labels = set(_string_list(point.get("labels")))
        if "protected_sample_point" in labels:
            summary["protected_sample_point_count"] += 1
        if "second_point_parity_stand_in" in labels:
            summary["second_point_parity_stand_in_count"] += 1
        availability = _bool_dict(point.get("evidence_availability"))
        for field in SUMMARY_AVAILABILITY_FIELDS:
            if availability.get(field) is True:
                summary[f"{field}_count"] += 1
    return summary


def _matrix_drift(
    *,
    baseline: dict[str, Any],
    current: dict[str, Any],
    strict: bool,
) -> dict[str, list[dict[str, Any]]]:
    baseline_points = _point_map(_list(baseline.get("points")))
    current_points = _point_map(_list(current.get("points")))
    drift: dict[str, list[dict[str, Any]]] = {
        "contract_drift": _contract_drift(baseline=baseline, current=current),
        "point_presence_drift": [],
        "point_label_drift": [],
        "replay_context_drift": [],
        "evidence_availability_drift": [],
        "profile_count_drift": [],
        "warning_drift": [],
        "matrix_row_warning_drift": [],
        "summary_drift": _summary_drift(
            baseline=_dict(baseline.get("summary")),
            current=_dict(current.get("summary")),
            strict=strict,
        ),
        "matrix_warning_drift": _top_level_warning_drift(
            baseline=_dict(baseline.get("warnings")),
            current=_dict(current.get("warnings")),
            strict=strict,
        ),
    }
    for key in sorted(set(baseline_points) - set(current_points)):
        point = baseline_points[key]
        protected = _is_protected_point(point)
        drift["point_presence_drift"].append(
            {
                "drift_type": "missing_in_current",
                "stable_key": key,
                "point_manifest_id": point.get("point_manifest_id"),
                "media_id": point.get("media_id"),
                "breaking": protected or strict,
            }
        )
    for key in sorted(set(current_points) - set(baseline_points)):
        point = current_points[key]
        drift["point_presence_drift"].append(
            {
                "drift_type": "added_in_current",
                "stable_key": key,
                "point_manifest_id": point.get("point_manifest_id"),
                "media_id": point.get("media_id"),
                "breaking": strict,
            }
        )
    for key in sorted(set(baseline_points) & set(current_points)):
        baseline_point = baseline_points[key]
        current_point = current_points[key]
        protected = _is_protected_point(baseline_point) or _is_protected_point(current_point)
        _append_point_field_drift(
            drift["point_label_drift"],
            stable_key=key,
            field="labels",
            baseline_value=sorted(_string_list(baseline_point.get("labels"))),
            current_value=sorted(_string_list(current_point.get("labels"))),
            breaking=protected or strict,
        )
        _append_point_field_drift(
            drift["replay_context_drift"],
            stable_key=key,
            field="replay_url",
            baseline_value=baseline_point.get("replay_url"),
            current_value=current_point.get("replay_url"),
            breaking=protected or strict,
        )
        _append_point_field_drift(
            drift["replay_context_drift"],
            stable_key=key,
            field="associated_run_ids",
            baseline_value=_string_dict(baseline_point.get("associated_run_ids")),
            current_value=_string_dict(current_point.get("associated_run_ids")),
            breaking=protected or strict,
        )
        _append_point_field_drift(
            drift["evidence_availability_drift"],
            stable_key=key,
            field="evidence_availability",
            baseline_value=_bool_dict(baseline_point.get("evidence_availability")),
            current_value=_bool_dict(current_point.get("evidence_availability")),
            breaking=protected or strict,
        )
        _append_point_field_drift(
            drift["profile_count_drift"],
            stable_key=key,
            field="profile_counts",
            baseline_value=_int_dict(baseline_point.get("profile_counts")),
            current_value=_int_dict(current_point.get("profile_counts")),
            breaking=protected or strict,
        )
        _append_point_field_drift(
            drift["warning_drift"],
            stable_key=key,
            field="warnings",
            baseline_value=_bool_dict(baseline_point.get("warnings")),
            current_value=_bool_dict(current_point.get("warnings")),
            breaking=protected or strict,
        )
        _append_point_field_drift(
            drift["matrix_row_warning_drift"],
            stable_key=key,
            field="matrix_row_warnings",
            baseline_value=_bool_dict(baseline_point.get("matrix_row_warnings")),
            current_value=_bool_dict(current_point.get("matrix_row_warnings")),
            breaking=protected or strict,
        )
    return drift


def _contract_drift(
    *,
    baseline: dict[str, Any],
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    drift: list[dict[str, Any]] = []
    for matrix, label in ((baseline, "baseline"), (current, "current")):
        if matrix.get("matrix_type") != MULTI_POINT_REGRESSION_MATRIX_TYPE:
            drift.append(
                {
                    "drift_type": "invalid_matrix_type",
                    "matrix": label,
                    "value": matrix.get("matrix_type"),
                    "breaking": True,
                }
            )
        if matrix.get("matrix_version") != MULTI_POINT_REGRESSION_MATRIX_VERSION:
            drift.append(
                {
                    "drift_type": "invalid_matrix_version",
                    "matrix": label,
                    "value": matrix.get("matrix_version"),
                    "breaking": True,
                }
            )
        for section in MATRIX_REQUIRED_SECTIONS:
            if section not in matrix:
                drift.append(
                    {
                        "drift_type": "missing_required_section",
                        "matrix": label,
                        "section": section,
                        "breaking": True,
                    }
                )
        warnings = _bool_dict(matrix.get("warnings"))
        for warning, expected in MATRIX_WARNINGS.items():
            if warnings.get(warning) is not expected:
                drift.append(
                    {
                        "drift_type": "required_warning_missing_or_false",
                        "matrix": label,
                        "warning": warning,
                        "value": warnings.get(warning),
                        "breaking": True,
                    }
                )
    return drift


def _summary_drift(
    *,
    baseline: dict[str, Any],
    current: dict[str, Any],
    strict: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(set(baseline) | set(current)):
        baseline_value = baseline.get(key)
        current_value = current.get(key)
        if baseline_value == current_value:
            continue
        breaking = strict or (
            key == "protected_sample_point_count"
            and _int_or_zero(current_value) < _int_or_zero(baseline_value)
        )
        rows.append(
            {
                "field": key,
                "baseline": baseline_value,
                "current": current_value,
                "breaking": breaking,
            }
        )
    return rows


def _top_level_warning_drift(
    *,
    baseline: dict[str, Any],
    current: dict[str, Any],
    strict: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(set(baseline) | set(current)):
        baseline_value = baseline.get(key)
        current_value = current.get(key)
        if baseline_value == current_value:
            continue
        rows.append(
            {
                "warning": key,
                "baseline": baseline_value,
                "current": current_value,
                "breaking": strict or key in MATRIX_WARNINGS,
            }
        )
    return rows


def _append_point_field_drift(
    rows: list[dict[str, Any]],
    *,
    stable_key: str,
    field: str,
    baseline_value: Any,
    current_value: Any,
    breaking: bool,
) -> None:
    if baseline_value == current_value:
        return
    rows.append(
        {
            "stable_key": stable_key,
            "field": field,
            "baseline": baseline_value,
            "current": current_value,
            "breaking": breaking,
        }
    )


def _comparison_summary(
    *,
    baseline: dict[str, Any],
    current: dict[str, Any],
    drift_detected: bool,
    breaking_drift_detected: bool,
) -> dict[str, Any]:
    baseline_summary = _dict(baseline.get("summary"))
    current_summary = _dict(current.get("summary"))
    summary: dict[str, Any] = {}
    for key in sorted(set(baseline_summary) | set(current_summary)):
        summary[f"baseline_{key}"] = baseline_summary.get(key, 0)
        summary[f"current_{key}"] = current_summary.get(key, 0)
    summary["drift_detected"] = drift_detected
    summary["breaking_drift_detected"] = breaking_drift_detected
    return summary


def _point_map(points: list[Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for index, point in enumerate(points):
        if not isinstance(point, dict):
            continue
        key = _point_key(point)
        mapped[key if key not in mapped else f"{key}#duplicate-{index + 1}"] = point
    return mapped


def _point_key(point: dict[str, Any]) -> str:
    return "|".join(
        str(point.get(key) or "")
        for key in ("point_manifest_id", "media_id")
    )


def _is_protected_point(point: dict[str, Any]) -> bool:
    return "protected_sample_point" in set(_string_list(point.get("labels")))


def _load_json(
    path: str | Path,
    *,
    label: str,
    fail_as_result: bool = True,
) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError:
        status = f"missing_{label}_json"
        message = f"{label} JSON not found: {path}"
        return _failed(status, message) if fail_as_result else {"ok": False, "status": status}
    except json.JSONDecodeError as exc:
        status = f"invalid_{label}_json"
        message = f"{label} JSON is not valid: {path}: {exc}"
        return _failed(status, message) if fail_as_result else {"ok": False, "status": status}
    if not isinstance(data, dict):
        status = f"invalid_{label}_json"
        message = f"{label} JSON must be an object: {path}"
        return _failed(status, message) if fail_as_result else {"ok": False, "status": status}
    return {"ok": True, "data": data}


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
        "matrix_type": MULTI_POINT_REGRESSION_MATRIX_TYPE,
        "matrix_version": MULTI_POINT_REGRESSION_MATRIX_VERSION,
        "warnings": dict(MATRIX_WARNINGS),
    }
    if details is not None:
        result["details"] = details
    return result


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _string_dict(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): item
        for key, item in value.items()
        if isinstance(item, str) and item
    }


def _bool_dict(value: object) -> dict[str, bool]:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items() if isinstance(item, bool)}


def _int_dict(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    counts: dict[str, int] = {}
    for key, item in value.items():
        if isinstance(item, bool):
            continue
        if isinstance(item, int):
            counts[str(key)] = item
    return counts


def _int_or_zero(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
