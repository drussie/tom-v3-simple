# Net-Axis Reversal Hit Recall v0.2.5 Report

Status: implemented

## Summary

Implemented a focused hit-candidate recall repair on top of the v0.2.4 contact-zone tightening.

The builder now:

- proposes `net_axis_reversal_hit_candidate_v025` from ball-first `court_y` direction reversals
- does not require player proximity for this recall path
- records nearest-player data as diagnostic/confidence support when available
- persists `net_axis_reversal_recall` metadata on candidates and diagnostics
- exposes the recall metadata in replay selected evidence
- preserves bounce-overlap protections so weak ball-first hits do not erase bounce candidates

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

- `event_candidate_run_id`: `6f432ec3-25f7-4ebf-87c9-3a3caf5afea4`
- `hit_candidate`: 3
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 722
- `net_axis_reversal_candidate_count`: 11
- `net_axis_reversal_recovered_hit_count`: 1
- `net_axis_reversal_suppressed_overlap_count`: 0
- `player_anchor_suppressed_overlap_count`: 1

Compared with the v0.2.4 2-hit / 2-bounce baseline, v0.2.5 recovered one extra ball-first
net-axis reversal hit while preserving the two bounce candidates.

## Validation

Completed:

- `.venv/bin/python -m pytest -q`: 308 passed
- `ruff check .`: passed
- `cd apps/web && npm run lint`: passed
- `cd apps/web && npm run build`: passed
- `cd apps/web && npm audit --omit=dev`: 0 vulnerabilities
- fixture `make demo`: passed
- fixture `make completion-audit`: passed

Browser smoke loaded the replay with
`eventCandidateRunId=6f432ec3-25f7-4ebf-87c9-3a3caf5afea4`, showed three
`HIT CANDIDATE` markers and two `BOUNCE CANDIDATE` markers, and selected the recovered frame-93 hit
with `player_proximity_required = false` in the reversal-recall details.

## Remaining Limitations

Ball-first net-axis reversal improves recall but does not prove racket contact. Player proximity is
diagnostic support for this path, not a truth requirement. The output remains candidate evidence and
does not add hit truth, bounce truth, in/out, score, rally/point logic, identity, or adjudication.
