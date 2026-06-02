# Blueprint 15 3D Debug Selection / Timeline Coupling v0 Report

Implemented display-only selection and timeline coupling for the Replay Workstation 3D Debug View.

## Changes

- Added current-time nearest 3D sample highlighting.
- Added local ±250ms time-window emphasis.
- Added click/keyboard selection for 3D candidate samples.
- Clicking a sample requests replay seek through the existing seek request path.
- Added selected 3D sample metadata.
- Preserved selected-marker nearest diagnostic sample highlighting.
- Added a compact legend for all/local/current/marker-linked sample states.

## Validation Notes

Focused checks passed:

```bash
.venv/bin/python -m pytest tests/test_ball_trajectory_3d_candidates.py tests/test_event_candidate_3d_diagnostics.py -q
cd apps/web && npm run lint
git diff --check
```

Full validation is recorded in the final handoff report for this branch.

## Boundaries

This milestone changed display interaction only. It did not change event candidate generation,
marker arbitration, review annotations, source evidence, snapshots, evaluation counts, in/out,
score, truth lifecycle, or adjudication.
