# Universal Hit Candidate Validity Guard v0.2.9 Report

## Summary

Implemented a final post-generation guard for all `hit_candidate` sources. The guard adds
`universal_hit_validity_guard` payload metadata, updates replay selected evidence, and can
reclassify unsupported landing-like hits to `bounce_candidate` or suppress fly-through/no-event hits
as rejection diagnostics.

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

- `event_candidate_run_id`: `ac6486bd-d4d0-4d60-88ea-b9790fe3a01f`
- `hit_candidate`: 7
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 868
- universal guard evaluated 7 hit candidates
- universal guard kept 7, reclassified 0, suppressed 0

## Validation

Completed validation:

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
