# Blueprint 17 Reviewed 3D Debug Dataset Export v0 Report

Status: implemented

Branch: `codex/blueprint-17-reviewed-3d-debug-dataset-export-v0`

## Summary

Blueprint 17 adds a read-only reviewed 3D debug dataset export path. The exporter packages existing
event markers, 3D ball trajectory candidates, camera geometry context, event-candidate 3D
diagnostics, event-marker review annotations, and 3D debug review annotations into deterministic JSON
or Markdown artifacts for offline review.

No live event candidates, 3D candidates, review annotations, in/out state, score, accepted/rejected
lifecycle, or adjudication are changed.

## Implementation

Created:

- `apps/worker/services/reviewed_3d_debug_dataset_export.py`
- `docs/blueprints/blueprint_17_reviewed_3d_debug_dataset_export_v0.md`
- `docs/exports/reviewed_3d_debug_dataset_export_v0.md`
- `tests/test_reviewed_3d_debug_dataset_export.py`

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
python -m apps.worker.cli export-reviewed-3d-debug-dataset
```

Added Make target:

```text
make tom-v1-export-reviewed-3d-debug-dataset
```

Required inputs:

- `MEDIA_ID`
- `EVENT_CANDIDATE_RUN_ID`
- `TRAJECTORY_3D_RUN_ID`
- `CAMERA_GEOMETRY_ID`

Supported output formats:

- `json`
- `markdown`

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

Outputs:

- `.data/exports/reviewed_3d_debug_dataset_sample_point.json`
- `.data/exports/reviewed_3d_debug_dataset_sample_point.md`

JSON smoke summary:

- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_count`: 6
- `event_marker_review_count`: 1
- `missing_3d_sample_note_count`: 0
- `trajectory_3d_candidate_count`: 68
- `trajectory_3d_debug_review_count`: 0

The local export validates as JSON and carries the required read-only warnings:

- `dataset_export_only`
- `review_metadata_only`
- `not_truth`
- `not_3d_truth`
- `not_training_truth`
- `does_not_change_event_candidates`
- `does_not_change_3d_candidates`
- `does_not_create_in_out`
- `does_not_create_score`
- `no_adjudication`

## Validation

Focused tests:

```text
.venv/bin/python -m pytest tests/test_reviewed_3d_debug_dataset_export.py -q
4 passed
```

Related 3D debug tests:

```text
.venv/bin/python -m pytest tests/test_reviewed_3d_debug_dataset_export.py tests/test_trajectory_3d_debug_review_annotations.py tests/test_event_candidate_3d_diagnostics.py tests/test_ball_trajectory_3d_candidates.py -q
21 passed
```

Full validation:

```text
.venv/bin/python -m pytest -q
364 passed

ruff check .
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

The current local sample export has event-marker review metadata but no persisted
`trajectory_3d_debug_review_annotation` rows for that specific 3D trajectory run. The exporter still
includes the 3D debug review section, and tests cover populated 3D debug review annotations.

The artifact is an offline review dataset export only. It is not hit truth, bounce truth, 3D truth,
training truth, in/out, score, or adjudication.
