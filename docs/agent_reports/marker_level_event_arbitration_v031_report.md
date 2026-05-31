# Marker-Level Event Arbitration v0.3.1 Report

## Summary

Implemented marker-level event arbitration v0.3.1 on top of the universal hit validity guard. The
repair handles visible marker conflicts after candidate generation: co-located hit/bounce markers
prefer the bounce unless the hit has strong independent contact evidence, and fly-through/transit
hits with no local event support are suppressed into diagnostics.

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

- `event_candidate_run_id`: `609fe533-42cf-4f7f-98f0-330b0bc05b45`
- `physics_heuristic_version`: `v0.3.1`
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- marker-level arbitration kept 3 hits and 3 bounces
- marker-level arbitration suppressed 1 fly-through hit
- marker-level arbitration resolved 1 co-located hit/bounce conflict to the bounce marker
- far-side hit recovered/preserved: frame 54
- far-side bounce recovered/preserved: frame 30
- `hit_requires_prior_bounce`: false
- `sequence_is_hard_gate`: false

The v0.3.0 baseline produced 5 hits and 3 bounces. v0.3.1 produced 3 hits and 3 bounces by removing
the two visible false positives that should not remain as hit markers.

## Replay Details

Replay event candidate payloads now expose `marker_level_arbitration` so selected evidence can show
the arbitration decision, reason, and the no-prior-bounce/no-hard-sequence flags.

Browser/API smoke against the real bridge DB loaded the replay for
`event_candidate_run_id = 609fe533-42cf-4f7f-98f0-330b0bc05b45` on an alternate local port. The
page rendered `HIT CANDIDATE` and `BOUNCE CANDIDATE` text, and the overlay API returned 6 final
event markers: 3 hits, 3 bounces, and `marker_level_arbitration` metadata on all 6.

## Validation

Completed validation:

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q`: 44 passed
- `.venv/bin/python -m pytest -q`: 324 passed
- `ruff check .`: passed
- `git diff --check`: passed
- `cd apps/web && npm run lint`: passed
- `cd apps/web && npm run build`: passed
- `cd apps/web && npm audit --omit=dev`: 0 vulnerabilities
- fixture `make demo`: passed
- fixture `make completion-audit`: passed

## Boundaries

The repair remains candidate evidence only. It does not add hit truth, bounce truth, in/out,
scoring, rally/point logic, player identity, accepted/rejected lifecycle, or adjudication.
