# Blueprint 19 Reviewed 3D Debug Baseline Freeze v0

Blueprint 19 turns the Blueprint 17 export and Blueprint 18 regression report into a repeatable
local `sample_point` baseline gate.

The workflow freezes a reviewed 3D debug export profile locally, then verifies future current
exports against that baseline. It is a regression checkpoint only. It is not truth, not 3D truth,
not training truth, not scoring, not in/out, and not adjudication.

## Make Targets

Freeze the baseline:

```bash
make tom-v1-freeze-reviewed-3d-debug-baseline \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

Verify the baseline:

```bash
make tom-v1-verify-reviewed-3d-debug-baseline \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

## CLI Commands

```bash
.venv/bin/python -m apps.worker.cli freeze-reviewed-3d-debug-baseline \
  --media-id <media_id> \
  --event-candidate-run-id <event_candidate_run_id> \
  --trajectory-3d-run-id <trajectory_3d_run_id> \
  --camera-geometry-id <camera_geometry_id>
```

```bash
.venv/bin/python -m apps.worker.cli verify-reviewed-3d-debug-baseline \
  --baseline .data/baselines/reviewed_3d_debug_dataset_sample_point.baseline.json \
  --media-id <media_id> \
  --event-candidate-run-id <event_candidate_run_id> \
  --trajectory-3d-run-id <trajectory_3d_run_id> \
  --camera-geometry-id <camera_geometry_id>
```

## Manifest

The freeze command writes:

- baseline JSON export
- baseline Markdown export
- compact baseline manifest

The manifest includes:

- baseline name
- media/run/camera geometry IDs
- expected summary counts
- local baseline file paths
- not-truth warnings

## Boundaries

The baseline export is not truth. Drift is a difference between exports and needs human review. The
gate does not alter event candidates, marker arbitration, 3D candidates, diagnostics, review
annotations, point snapshots, evaluation reports, in/out, score, or adjudication.
