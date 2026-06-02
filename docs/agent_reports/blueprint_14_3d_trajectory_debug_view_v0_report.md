# Blueprint 14 3D Trajectory Debug View v0 Report

Implemented a display-only 3D trajectory debug view for Replay Workstation.

## Changes

- Added replay API `trajectory_3d_debug` payload.
- Added `trajectory3dRunId` query plumbing in the replay page and overlay fetch.
- Added TypeScript types for court dimensions, debug points, and debug payload.
- Added a side-panel SVG court-plane view showing candidate x/y samples and path.
- Added selected-marker nearest 3D sample highlighting from Blueprint 13 diagnostics.
- Added replay API tests for available and unavailable debug payload states.

## Validation Notes

Focused validation passed for 3D trajectory and 3D diagnostic replay paths:

```bash
.venv/bin/python -m pytest tests/test_ball_trajectory_3d_candidates.py tests/test_event_candidate_3d_diagnostics.py -q
cd apps/web && npm run lint
```

## Boundaries

This milestone did not change hit/bounce generation, marker arbitration, review annotations, source
evidence, snapshots, evaluation counts, in/out, score, truth lifecycle, or adjudication. Height
remains unknown in v0.
