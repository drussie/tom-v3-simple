# Blueprint 16 3D Debug Review Annotations v0 Report

## Summary

Blueprint 16 adds persistent review metadata for 3D Debug View evidence.

Implemented:

- `trajectory_3d_debug_review_annotation` persistence and migration
- `tom_v3_schema.trajectory_3d_debug_review` request/response models
- replay API GET/POST/PATCH endpoints for 3D debug reviews
- replay overlay `trajectory_3d_debug_review_summary`
- point evidence snapshot `trajectory_3d_debug_review_summary`
- point candidate evaluation `trajectory_3d_debug_reviews`
- Replay Workstation controls for 3D sample reviews, 3D diagnostic reviews, and missing 3D sample notes
- tests for create/update/reject/snapshot/evaluation/replay-summary behavior

## Boundary

This branch does not change hit/bounce candidate generation, marker arbitration, event reviews, 3D
candidate samples, 3D diagnostics, in/out, score, accepted/rejected lifecycle, or adjudication.

## Validation

Focused validation:

```bash
.venv/bin/python -m pytest tests/test_trajectory_3d_debug_review_annotations.py \
  tests/test_event_candidate_review_annotations.py \
  tests/test_ball_trajectory_3d_candidates.py \
  tests/test_event_candidate_3d_diagnostics.py \
  tests/test_point_candidate_evaluation.py -q
ruff check apps/api/services/trajectory_3d_debug_reviews.py apps/api/routers/replay.py
cd apps/web && npm run lint
```

Full validation should also run before final merge:

```bash
.venv/bin/python -m pytest -q
ruff check .
git diff --check
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
```
