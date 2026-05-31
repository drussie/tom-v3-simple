# Universal Hit Validity Guard Tightening v0.3.0 Report

## Summary

Implemented v0.3.0 tightening for the universal hit-candidate guard. The repair changes the guard
from a metadata-only pass in the real sample run into an active candidate-quality filter that can
reclassify landing-like fallback hits and suppress image-direction-only transit hits.

## Local Smoke

Command:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-hit-bounce-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  BALL_TRAJECTORY_RUN_ID=2e16f3d1-e252-497a-b688-d81890645ab7 \
  COURT_PROJECTION_RUN_ID=82498799-490f-44df-9222-0157356c5ff7
```

Result:

- `event_candidate_run_id`: `5bbbb6b8-fb06-4319-863f-e32675f48aba`
- `physics_heuristic_version`: `v0.3.0`
- `hit_candidate`: 5
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 869
- universal guard evaluated 7 hit candidates
- universal guard kept 5, reclassified 1, suppressed 1
- `hit_requires_prior_bounce`: false
- `sequence_is_hard_gate`: false

The previous v0.2.9 run produced 7 hits, 2 bounces, and `{"keep_as_hit": 7}`. The repaired run
produced `{"keep_as_hit": 5, "reclassify_to_bounce": 1, "suppress_as_diagnostic": 1}`.

## Validation

Completed validation:

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q`: 41 passed
- `.venv/bin/python -m pytest -q`: 321 passed
- `ruff check .`: passed
- `cd apps/web && npm run lint`: passed
- `cd apps/web && npm run build`: passed
- `cd apps/web && npm audit --omit=dev`: 0 vulnerabilities
- fixture `make demo`: passed
- fixture `make completion-audit`: passed

## Boundaries

The repair remains candidate evidence only. It does not add hit truth, bounce truth, in/out,
scoring, rally/point logic, player identity, accepted/rejected lifecycle, or adjudication.
