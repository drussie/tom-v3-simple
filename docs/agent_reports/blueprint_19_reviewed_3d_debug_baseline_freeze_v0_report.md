# Blueprint 19 Reviewed 3D Debug Baseline Freeze v0 Report

Status: implemented

Branch: `codex/blueprint-19-reviewed-3d-debug-baseline-freeze-v0`

## Summary

Blueprint 19 adds a local sample-point reviewed 3D debug baseline freeze and regression gate. It
wraps the Blueprint 17 exporter and Blueprint 18 regression harness into repeatable Make/CLI
workflows.

The baseline is not truth, not 3D truth, and not training truth. The gate detects export drift for
human review and does not change live event candidates, marker arbitration, 3D candidates, 3D
diagnostics, review annotations, in/out, score, or adjudication.

## Implementation

Created:

- `apps/worker/services/reviewed_3d_debug_baseline.py`
- `docs/baselines/sample_point_reviewed_3d_debug_baseline_v0.md`
- `docs/blueprints/blueprint_19_reviewed_3d_debug_baseline_freeze_v0.md`
- `tests/test_reviewed_3d_debug_baseline.py`

Updated:

- `apps/worker/cli.py`
- `Makefile`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`

## CLI / Make Helper

Added CLI commands:

```text
python -m apps.worker.cli freeze-reviewed-3d-debug-baseline
python -m apps.worker.cli verify-reviewed-3d-debug-baseline
```

Added Make targets:

```text
make tom-v1-freeze-reviewed-3d-debug-baseline
make tom-v1-verify-reviewed-3d-debug-baseline
```

## Manifest

The baseline manifest includes:

- `manifest_type`: `reviewed_3d_debug_baseline_manifest`
- `manifest_version`: `v0`
- `baseline_name`: `sample_point_reviewed_3d_debug_baseline_v0`
- media/run/camera geometry IDs
- expected summary counts
- baseline JSON/Markdown paths
- not-truth warnings

## Local Smoke

Database:

```text
sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db
```

Inputs:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `event_candidate_run_id`: `1b946366-7ec1-426f-8b40-494535a9b3fb`
- `trajectory_3d_run_id`: `ea76ccab-c51d-4a63-9682-9fd0bbb83f14`
- `camera_geometry_id`: `5afa67fb-7f6e-41eb-b4aa-b1100a97ee97`

Freeze outputs:

- `.data/baselines/reviewed_3d_debug_dataset_sample_point.baseline.json`
- `.data/baselines/reviewed_3d_debug_dataset_sample_point.baseline.md`
- `.data/baselines/reviewed_3d_debug_dataset_sample_point.baseline_manifest.json`

Verify outputs:

- `.data/exports/reviewed_3d_debug_dataset_sample_point.current.json`
- `.data/exports/reviewed_3d_debug_dataset_sample_point.regression.json`
- `.data/exports/reviewed_3d_debug_dataset_sample_point.regression.md`

Manifest / gate summary:

- `event_marker_count`: 6
- `trajectory_3d_candidate_count`: 68
- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_review_count`: 1
- `trajectory_3d_debug_review_count`: 0
- `missing_3d_sample_note_count`: 0
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false

Generated baseline and regression JSON files validate with `json.tool`.

## Validation

Focused tests:

```text
.venv/bin/python -m pytest tests/test_reviewed_3d_debug_baseline.py tests/test_reviewed_3d_debug_dataset_regression.py -q
20 passed
```

Full validation:

```text
.venv/bin/python -m pytest -q
384 passed

ruff check .
passed

git diff --check
passed

cd apps/web && npm run lint
passed

cd apps/web && npm run build
passed

cd apps/web && npm audit --omit=dev
found 0 vulnerabilities
```

Fixture demo and audit:

```text
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

make completion-audit PYTHON=.venv/bin/python
passed
```

## Remaining Limitations

This is a local regression checkpoint around one sample point. It detects drift from a frozen export
profile but does not prove correctness. Drift requires human review.

The gate compares generated export files. It does not create new event candidates, 3D candidates,
review annotations, in/out, score, or adjudication.
