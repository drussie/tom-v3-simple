from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

REGRESSION_TYPE = "reviewed_3d_debug_dataset_regression_report"
REGRESSION_VERSION = "v0"

REGRESSION_WARNINGS = {
    "regression_report_only": True,
    "baseline_is_not_truth": True,
    "not_truth": True,
    "not_3d_truth": True,
    "not_training_truth": True,
    "does_not_change_event_candidates": True,
    "does_not_change_3d_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}

COUNT_KEYS = (
    "event_marker_count",
    "trajectory_3d_candidate_count",
    "event_candidate_3d_diagnostic_count",
    "trajectory_3d_debug_review_count",
    "event_marker_review_count",
    "missing_3d_sample_note_count",
)

REQUIRED_SECTIONS = (
    "summary",
    "camera_geometry_summary",
    "trajectory_3d_summary",
    "event_candidate_3d_diagnostic_summary",
    "trajectory_3d_debug_review_summary",
    "event_marker_summary",
    "trajectory_3d_candidates",
    "event_candidate_3d_diagnostics",
    "trajectory_3d_debug_reviews",
    "event_candidate_reviews",
    "warnings",
)

TOP_LEVEL_COMPARE_KEYS = (
    "export_type",
    "export_version",
    "media_id",
    "event_candidate_run_id",
    "trajectory_3d_run_id",
    "camera_geometry_id",
)

ID_FIELD_NAMES = {
    "id",
    "media_id",
    "observation_id",
    "review_annotation_id",
    "event_observation_id",
    "source_observation_id",
    "nearest_3d_candidate_id",
    "trajectory_3d_candidate_id",
    "event_candidate_3d_diagnostic_id",
    "camera_geometry_id",
}


def compare_reviewed_3d_debug_dataset_exports(
    *,
    baseline_path: str,
    current_path: str,
    strict: bool = False,
    output_format: str = "json",
    output_path: str | None = None,
    allow_id_drift: bool = True,
    allow_float_drift: float = 0.000001,
) -> dict[str, Any]:
    """Compare two reviewed 3D debug dataset export JSON files.

    This is an offline regression/drift report. Baseline exports are comparison
    artifacts only; they are not truth and do not affect live evidence.
    """

    if output_format not in {"json", "markdown"}:
        return _failed(
            "unsupported_format",
            f"unsupported reviewed 3D debug dataset regression format: {output_format}",
        )

    baseline_loaded = _load_json_export(baseline_path, label="baseline")
    if baseline_loaded.get("ok") is False:
        return baseline_loaded
    current_loaded = _load_json_export(current_path, label="current")
    if current_loaded.get("ok") is False:
        return current_loaded

    baseline = _dict(baseline_loaded["data"])
    current = _dict(current_loaded["data"])

    drift = {
        "top_level_drift": _top_level_drift(
            baseline,
            current,
            allow_id_drift=allow_id_drift,
            allow_float_drift=allow_float_drift,
        ),
        "summary_count_drift": _summary_count_drift(baseline, current),
        "section_presence_drift": _section_presence_drift(baseline, current),
        "event_marker_drift": _list_drift(
            baseline_rows=_list(baseline.get("event_marker_summary")),
            current_rows=_list(current.get("event_marker_summary")),
            row_kind="event_marker",
            key_fn=_event_marker_key,
            allow_id_drift=allow_id_drift,
            allow_float_drift=allow_float_drift,
        ),
        "trajectory_3d_candidate_drift": _list_drift(
            baseline_rows=_list(baseline.get("trajectory_3d_candidates")),
            current_rows=_list(current.get("trajectory_3d_candidates")),
            row_kind="trajectory_3d_candidate",
            key_fn=_trajectory_3d_candidate_key,
            allow_id_drift=allow_id_drift,
            allow_float_drift=allow_float_drift,
        ),
        "event_candidate_3d_diagnostic_drift": _list_drift(
            baseline_rows=_list(baseline.get("event_candidate_3d_diagnostics")),
            current_rows=_list(current.get("event_candidate_3d_diagnostics")),
            row_kind="event_candidate_3d_diagnostic",
            key_fn=_event_candidate_3d_diagnostic_key,
            allow_id_drift=allow_id_drift,
            allow_float_drift=allow_float_drift,
        ),
        "trajectory_3d_debug_review_drift": _list_drift(
            baseline_rows=_list(baseline.get("trajectory_3d_debug_reviews")),
            current_rows=_list(current.get("trajectory_3d_debug_reviews")),
            row_kind="trajectory_3d_debug_review",
            key_fn=_trajectory_3d_debug_review_key,
            allow_id_drift=allow_id_drift,
            allow_float_drift=allow_float_drift,
        ),
        "event_candidate_review_drift": _list_drift(
            baseline_rows=_list(baseline.get("event_candidate_reviews")),
            current_rows=_list(current.get("event_candidate_reviews")),
            row_kind="event_candidate_review",
            key_fn=_event_candidate_review_key,
            allow_id_drift=allow_id_drift,
            allow_float_drift=allow_float_drift,
        ),
        "warning_drift": _warning_drift(baseline, current),
    }
    drift_detected = any(bool(items) for items in drift.values())
    breaking_drift_detected = bool(strict and drift_detected)

    result: dict[str, Any] = {
        "ok": not breaking_drift_detected,
        "status": (
            "failed_regression"
            if breaking_drift_detected
            else "completed_with_drift"
            if drift_detected
            else "completed"
        ),
        "regression_type": REGRESSION_TYPE,
        "regression_version": REGRESSION_VERSION,
        "baseline_path": str(Path(baseline_path)),
        "current_path": str(Path(current_path)),
        "comparison_config": {
            "strict": strict,
            "allow_id_drift": allow_id_drift,
            "allow_float_drift": allow_float_drift,
        },
        "summary": _report_summary(
            baseline,
            current,
            drift_detected=drift_detected,
            breaking_drift_detected=breaking_drift_detected,
        ),
        "drift": drift,
        "warnings": dict(REGRESSION_WARNINGS),
        "known_limitations": [
            "Regression drift is a difference between exports, not proof of incorrectness.",
            "The baseline export is not truth, 3D truth, or training truth.",
            "The report does not change live event candidates or 3D candidates.",
            "The report does not create in/out, score, point, or adjudication decisions.",
        ],
    }

    if output_format == "markdown":
        result["markdown"] = render_reviewed_3d_debug_dataset_regression_markdown(result)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(result["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["output_path"] = str(path)

    return result


def render_reviewed_3d_debug_dataset_regression_markdown(
    result: dict[str, Any],
) -> str:
    summary = _dict(result.get("summary"))
    drift = _dict(result.get("drift"))
    rows = [
        "# Reviewed 3D Debug Dataset Regression Report v0",
        "",
        f"Baseline path: `{result.get('baseline_path')}`  ",
        f"Current path: `{result.get('current_path')}`  ",
        f"Status: `{result.get('status')}`",
        "",
        "## Drift Status",
        "",
    ]
    if summary.get("drift_detected"):
        rows.append("Drift detected.")
    else:
        rows.append("No drift detected.")
    rows.extend(
        [
            "",
            "## Summary Counts",
            "",
            "| Field | Baseline | Current |",
            "|---|---:|---:|",
        ]
    )
    for key in COUNT_KEYS:
        rows.append(
            "| {field} | {baseline} | {current} |".format(
                field=key,
                baseline=summary.get(f"baseline_{key}", 0),
                current=summary.get(f"current_{key}", 0),
            )
        )
    rows.extend(
        [
            "",
            "## Drift Tables",
            "",
            "| Drift kind | Count |",
            "|---|---:|",
        ]
    )
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
            "- Baseline export is not truth.",
            "- Not truth, not 3D truth, and not training truth.",
            "- Does not change event candidates, 3D candidates, in/out, score, or adjudication.",
            "",
            "## Known Limitations",
            "",
        ]
    )
    for limitation in result.get("known_limitations", []):
        rows.append(f"- {limitation}")
    rows.append("")
    return "\n".join(rows)


def _load_json_export(path: str, *, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return _failed(f"missing_{label}_export", f"{label} export not found: {path}")
    except json.JSONDecodeError as exc:
        return _failed(
            f"invalid_{label}_json",
            f"{label} export is not valid JSON: {path}: {exc}",
        )
    if not isinstance(data, dict):
        return _failed(
            f"invalid_{label}_export",
            f"{label} export must be a JSON object: {path}",
        )
    return {"ok": True, "data": data}


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "regression_type": REGRESSION_TYPE,
        "regression_version": REGRESSION_VERSION,
        "warnings": dict(REGRESSION_WARNINGS),
    }


def _top_level_drift(
    baseline: dict[str, Any],
    current: dict[str, Any],
    *,
    allow_id_drift: bool,
    allow_float_drift: float,
) -> list[dict[str, Any]]:
    drift: list[dict[str, Any]] = []
    for key in TOP_LEVEL_COMPARE_KEYS:
        if allow_id_drift and key.endswith("_id"):
            continue
        baseline_value = baseline.get(key)
        current_value = current.get(key)
        if not _values_equal(baseline_value, current_value, allow_float_drift=allow_float_drift):
            drift.append(
                {
                    "field": key,
                    "baseline": baseline_value,
                    "current": current_value,
                }
            )
    return drift


def _summary_count_drift(
    baseline: dict[str, Any],
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    baseline_summary = _dict(baseline.get("summary"))
    current_summary = _dict(current.get("summary"))
    keys = sorted(set(COUNT_KEYS) | set(baseline_summary) | set(current_summary))
    drift: list[dict[str, Any]] = []
    for key in keys:
        baseline_value = baseline_summary.get(key)
        current_value = current_summary.get(key)
        if baseline_value != current_value:
            drift.append(
                {
                    "field": key,
                    "baseline": baseline_value,
                    "current": current_value,
                }
            )
    return drift


def _section_presence_drift(
    baseline: dict[str, Any],
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    drift: list[dict[str, Any]] = []
    for section in REQUIRED_SECTIONS:
        baseline_present = section in baseline
        current_present = section in current
        if baseline_present != current_present:
            drift.append(
                {
                    "section": section,
                    "baseline_present": baseline_present,
                    "current_present": current_present,
                }
            )
    return drift


def _warning_drift(
    baseline: dict[str, Any],
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    baseline_warnings = _dict(baseline.get("warnings"))
    current_warnings = _dict(current.get("warnings"))
    drift: list[dict[str, Any]] = []
    for key in sorted(set(baseline_warnings) | set(current_warnings)):
        baseline_value = baseline_warnings.get(key)
        current_value = current_warnings.get(key)
        if baseline_value != current_value:
            drift.append(
                {
                    "warning": key,
                    "baseline": baseline_value,
                    "current": current_value,
                }
            )
    return drift


def _list_drift(
    *,
    baseline_rows: list[Any],
    current_rows: list[Any],
    row_kind: str,
    key_fn: Any,
    allow_id_drift: bool,
    allow_float_drift: float,
) -> list[dict[str, Any]]:
    baseline_map = _stable_row_map(
        baseline_rows,
        key_fn=key_fn,
        allow_id_drift=allow_id_drift,
    )
    current_map = _stable_row_map(
        current_rows,
        key_fn=key_fn,
        allow_id_drift=allow_id_drift,
    )
    drift: list[dict[str, Any]] = []
    for key in sorted(set(baseline_map) - set(current_map)):
        drift.append({"kind": row_kind, "drift_type": "missing_in_current", "stable_key": key})
    for key in sorted(set(current_map) - set(baseline_map)):
        drift.append({"kind": row_kind, "drift_type": "added_in_current", "stable_key": key})
    for key in sorted(set(baseline_map) & set(current_map)):
        baseline_value = _canonical_row(
            baseline_map[key],
            allow_id_drift=allow_id_drift,
        )
        current_value = _canonical_row(
            current_map[key],
            allow_id_drift=allow_id_drift,
        )
        if _values_equal(
            baseline_value,
            current_value,
            allow_float_drift=allow_float_drift,
        ):
            continue
        drift.append(
            {
                "kind": row_kind,
                "drift_type": "changed",
                "stable_key": key,
                "changed_fields": _changed_fields(
                    baseline_value,
                    current_value,
                    allow_float_drift=allow_float_drift,
                ),
            }
        )
    return drift


def _stable_row_map(
    rows: list[Any],
    *,
    key_fn: Any,
    allow_id_drift: bool,
) -> dict[str, dict[str, Any]]:
    counts: dict[str, int] = {}
    mapped: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            key = f"invalid-row:{index}"
            mapped[key] = {"value": row}
            continue
        raw_key = key_fn(row, index, allow_id_drift)
        occurrence = counts.get(raw_key, 0)
        counts[raw_key] = occurrence + 1
        key = raw_key if occurrence == 0 else f"{raw_key}#duplicate-{occurrence + 1}"
        mapped[key] = row
    return mapped


def _event_marker_key(row: dict[str, Any], index: int, allow_id_drift: bool) -> str:
    return _key(
        "event_marker",
        row.get("candidate_type"),
        row.get("frame"),
        row.get("timestamp_ms"),
        row.get("source_method") or row.get("candidate_method") or row.get("source"),
        row.get("index") if row.get("index") is not None else index,
        row.get("observation_id") if not allow_id_drift else None,
    )


def _trajectory_3d_candidate_key(
    row: dict[str, Any],
    index: int,
    allow_id_drift: bool,
) -> str:
    return _key(
        "trajectory_3d_candidate",
        row.get("frame"),
        row.get("timestamp_ms"),
        row.get("projection_method"),
        row.get("source_observation_id") if not allow_id_drift else None,
        index if allow_id_drift else None,
    )


def _event_candidate_3d_diagnostic_key(
    row: dict[str, Any],
    index: int,
    allow_id_drift: bool,
) -> str:
    return _key(
        "event_candidate_3d_diagnostic",
        row.get("candidate_type"),
        row.get("frame"),
        row.get("timestamp_ms"),
        row.get("event_observation_id") if not allow_id_drift else None,
        index if allow_id_drift else None,
    )


def _trajectory_3d_debug_review_key(
    row: dict[str, Any],
    index: int,
    allow_id_drift: bool,
) -> str:
    return _key(
        "trajectory_3d_debug_review",
        row.get("annotation_kind"),
        row.get("review_label"),
        row.get("timestamp_ms"),
        row.get("trajectory_3d_candidate_id") if not allow_id_drift else None,
        row.get("event_candidate_3d_diagnostic_id") if not allow_id_drift else None,
        index if allow_id_drift else None,
    )


def _event_candidate_review_key(
    row: dict[str, Any],
    index: int,
    allow_id_drift: bool,
) -> str:
    return _key(
        "event_candidate_review",
        row.get("candidate_type"),
        row.get("review_label"),
        row.get("frame"),
        row.get("timestamp_ms"),
        row.get("observation_id") if not allow_id_drift else None,
        index if allow_id_drift else None,
    )


def _key(*parts: Any) -> str:
    return "|".join("" if part is None else str(part) for part in parts)


def _canonical_row(
    row: dict[str, Any],
    *,
    allow_id_drift: bool,
) -> dict[str, Any]:
    return _strip_id_like_fields(row) if allow_id_drift else row


def _strip_id_like_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _strip_id_like_fields(item)
            for key, item in value.items()
            if not _is_id_like_key(str(key))
        }
    if isinstance(value, list):
        return [_strip_id_like_fields(item) for item in value]
    return value


def _is_id_like_key(key: str) -> bool:
    return key in ID_FIELD_NAMES or key.endswith("_id") or key.endswith("_ids")


def _values_equal(
    baseline: Any,
    current: Any,
    *,
    allow_float_drift: float,
) -> bool:
    if isinstance(baseline, float) or isinstance(current, float):
        if not _is_number(baseline) or not _is_number(current):
            return baseline == current
        return math.isclose(
            float(baseline),
            float(current),
            rel_tol=0.0,
            abs_tol=allow_float_drift,
        )
    if isinstance(baseline, dict) and isinstance(current, dict):
        if set(baseline) != set(current):
            return False
        return all(
            _values_equal(
                baseline[key],
                current[key],
                allow_float_drift=allow_float_drift,
            )
            for key in baseline
        )
    if isinstance(baseline, list) and isinstance(current, list):
        if len(baseline) != len(current):
            return False
        return all(
            _values_equal(
                baseline_item,
                current_item,
                allow_float_drift=allow_float_drift,
            )
            for baseline_item, current_item in zip(baseline, current, strict=True)
        )
    return baseline == current


def _changed_fields(
    baseline: dict[str, Any],
    current: dict[str, Any],
    *,
    allow_float_drift: float,
) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    for key in sorted(set(baseline) | set(current)):
        baseline_value = baseline.get(key)
        current_value = current.get(key)
        if _values_equal(
            baseline_value,
            current_value,
            allow_float_drift=allow_float_drift,
        ):
            continue
        fields.append(
            {
                "field": key,
                "baseline": baseline_value,
                "current": current_value,
            }
        )
    return fields


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _report_summary(
    baseline: dict[str, Any],
    current: dict[str, Any],
    *,
    drift_detected: bool,
    breaking_drift_detected: bool,
) -> dict[str, Any]:
    baseline_summary = _dict(baseline.get("summary"))
    current_summary = _dict(current.get("summary"))
    summary: dict[str, Any] = {}
    for key in COUNT_KEYS:
        summary[f"baseline_{key}"] = baseline_summary.get(key, 0)
        summary[f"current_{key}"] = current_summary.get(key, 0)
    summary["drift_detected"] = drift_detected
    summary["breaking_drift_detected"] = breaking_drift_detected
    return summary


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
