# Blueprint 18 Reviewed 3D Debug Dataset Regression v0 Report

Status: implemented

Branch: `codex/blueprint-18-reviewed-3d-debug-dataset-regression-v0`

## Summary

Blueprint 18 adds a read-only regression harness for Blueprint 17 reviewed 3D debug dataset exports.
It compares a saved baseline export with a current export and reports deterministic drift without
treating the baseline as truth.

No live event candidates, marker arbitration, 3D candidates, 3D diagnostics, review annotations,
in/out, score, accepted/rejected lifecycle, or adjudication are changed.

## Implementation

Created:

- `apps/worker/services/reviewed_3d_debug_dataset_regression.py`
- `docs/blueprints/blueprint_18_reviewed_3d_debug_dataset_regression_v0.md`
- `docs/exports/reviewed_3d_debug_dataset_regression_v0.md`
- `tests/test_reviewed_3d_debug_dataset_regression.py`

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

Added:

```text
python -m apps.worker.cli compare-reviewed-3d-debug-dataset
```

Added Make target:

```text
make tom-v1-compare-reviewed-3d-debug-dataset
```

Required inputs:

- `BASELINE`
- `CURRENT`

Supported output formats:

- `json`
- `markdown`

Optional controls:

- `STRICT`
- `ALLOW_ID_DRIFT`
- `ALLOW_FLOAT_DRIFT`

## Drift Coverage

The report compares:

- top-level export metadata
- summary counts
- required section presence
- warnings
- event marker rows
- 3D trajectory candidate rows
- event-candidate 3D diagnostic rows
- 3D debug review rows
- event candidate review rows

ID-like fields are ignored by default so regenerated UUIDs do not create drift by themselves.

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

Generated exports:

- `.data/exports/reviewed_3d_debug_dataset_sample_point.baseline.json`
- `.data/exports/reviewed_3d_debug_dataset_sample_point.current.json`

Generated regression reports:

- `.data/exports/reviewed_3d_debug_dataset_sample_point.regression.json`
- `.data/exports/reviewed_3d_debug_dataset_sample_point.regression.md`

No-drift JSON smoke summary:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `baseline_event_marker_count`: 6
- `current_event_marker_count`: 6
- `baseline_trajectory_3d_candidate_count`: 68
- `current_trajectory_3d_candidate_count`: 68
- `baseline_event_candidate_3d_diagnostic_count`: 6
- `current_event_candidate_3d_diagnostic_count`: 6
- `baseline_event_marker_review_count`: 1
- `current_event_marker_review_count`: 1
- `baseline_trajectory_3d_debug_review_count`: 0
- `current_trajectory_3d_debug_review_count`: 0

The JSON report validates with `json.tool`.

## Drift Test Result

Focused tests cover count drift, missing sections, marker drift, 3D candidate drift, diagnostic
drift, 3D debug review drift, strict mode failure, non-strict drift reporting, output writing,
warnings, ID drift tolerance, and input-file immutability.

```text
.venv/bin/python -m pytest tests/test_reviewed_3d_debug_dataset_regression.py -q
13 passed
```

## Validation

Full validation:

```text
.venv/bin/python -m pytest -q
377 passed

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

Regression drift is a difference between two exports, not proof that either export is correct or
incorrect. The baseline export is not truth, not 3D truth, and not training truth.

The harness compares already-exported files. It does not create new event candidates, 3D candidates,
review annotations, in/out, score, or adjudication.
