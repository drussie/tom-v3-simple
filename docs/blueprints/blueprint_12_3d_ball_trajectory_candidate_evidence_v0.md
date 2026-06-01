# Blueprint 12 - 3D Ball Trajectory Candidate Evidence v0

Blueprint 12 adds an optional 3D ball trajectory candidate evidence layer.

```text
ball_trajectory_court_candidate
+ camera_geometry_evidence
-> ball_trajectory_3d_candidate
-> replay / snapshot / evaluation readiness summaries
```

This is not true 3D reconstruction. It is provisional geometry evidence that records what TOM can
derive from declared court/camera assumptions.

## What It Persists

The `ball_trajectory_3d_candidate` table stores one row per source trajectory point:

- source media, ball trajectory run, court projection run, and camera geometry ids
- frame and timestamp
- source image point when available
- normalized court x/y from the 2D trajectory point
- metric court-plane `court_x_m` / `court_y_m` from declared court dimensions
- `court_z_m` and `court_z_status`
- height model and diagnostics
- velocity candidates in meters/second when adjacent points are available
- candidate-only warnings

Default v0 behavior uses `height_model = none_unknown`, so `court_z_m` remains null and
`court_z_status = unknown`.

An explicit `court_plane_placeholder` mode can write `court_z_m = 0.0`, but this is only a court
plane placeholder. It is not actual ball height.

## CLI

```bash
.venv/bin/python -m apps.worker.cli build-3d-ball-trajectory-candidates \
  --media-id <media_id> \
  --ball-trajectory-run-id <ball_trajectory_run_id> \
  --court-projection-run-id <court_projection_run_id> \
  --camera-geometry-id <camera_geometry_id> \
  --height-model none_unknown
```

Make helper:

```bash
make tom-v1-build-3d-ball-trajectory-candidates \
  MEDIA_ID=<media_id> \
  BALL_TRAJECTORY_RUN_ID=<ball_trajectory_run_id> \
  COURT_PROJECTION_RUN_ID=<court_projection_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

## Replay / Snapshot / Evaluation

Replay info includes `trajectory_3d_summary` and an available-runs group for 3D trajectory
candidate evidence. The UI shows a compact side-panel summary only. Blueprint 12 intentionally does
not add 3D rendering, fake arcs, or Three.js.

Point evidence snapshots include `trajectory_3d_summary`.

Point candidate evaluations include `trajectory_3d_readiness`.

## Boundary

3D ball trajectory candidates are derived evidence only.

They are not:

- true 3D reconstruction
- verified ball height
- hit truth
- bounce truth
- in/out
- score
- adjudication

Blueprint 12 does not change hit/bounce candidate generation, marker arbitration, review
annotations, source evidence, event counts, or replay marker placement.
