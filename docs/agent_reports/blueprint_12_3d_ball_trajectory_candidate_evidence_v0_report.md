# Blueprint 12 3D Ball Trajectory Candidate Evidence v0 Report

## Summary

Blueprint 12 adds provisional 3D ball trajectory candidate evidence. It persists metric court-plane
x/y candidate samples from existing `ball_trajectory_court_candidate` points and Blueprint 11
camera geometry declarations. Default v0 keeps height unknown.

## Added

- `ball_trajectory_3d_candidate` persistence table and migration
- `tom_v3_schema.ball_trajectory_3d` contract
- `build-3d-ball-trajectory-candidates` worker CLI command
- `tom-v1-build-3d-ball-trajectory-candidates` Make helper
- replay info `trajectory_3d_summary`
- replay side-panel 3D trajectory candidate summary
- point evidence snapshot `trajectory_3d_summary`
- point candidate evaluation `trajectory_3d_readiness`
- tests for persistence, height-model validation, snapshot/evaluation/replay integration, and
  boundaries

## Boundary

No true 3D reconstruction was added. No verified ball height was added. Hit/bounce candidate
generation, marker arbitration, review annotations, source observations, in/out, score, point
state, accepted/rejected lifecycle, and adjudication were not changed.

## Validation Notes

Local bridge smoke built 3D trajectory candidates for media
`9518fb01-0da1-4344-9a84-ff88ec8e9b1e` from ball trajectory run
`2e16f3d1-e252-497a-b688-d81890645ab7`, court projection run
`82498799-490f-44df-9222-0157356c5ff7`, and camera geometry
`5afa67fb-7f6e-41eb-b4aa-b1100a97ee97`.

- `trajectory_3d_run_id`: `4cb10f39-8873-4939-a654-33de05d6901f`
- `source_trajectory_points`: 68
- `trajectory_3d_candidate_count`: 68
- `height_model`: `none_unknown`
- `known_height_count`: 0
- `unknown_height_count`: 68
- `court_plane_xy_metric_count`: 68
- `velocity_candidate_count`: 51

Snapshot and evaluation smoke runs found the 3D trajectory summary/readiness and preserved the
existing event candidate counts:

- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- `final_marker_count`: 6

The evaluation summary reported 3D trajectory candidates available, height candidates unavailable,
true 3D reconstruction unavailable, and 3D ball trajectory truth unavailable.

Validation passed:

- `.venv/bin/python -m pytest -q` (`350 passed`)
- `ruff check .`
- `git diff --check`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- fixture `make demo`
- fixture `make completion-audit`
- Alembic upgrade through `0006_ball_trajectory_3d_candidate`
