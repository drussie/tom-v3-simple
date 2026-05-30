# Player-Anchored Hit Contact-Zone Tightening v0.2.4 Report

Status: implemented

## Summary

Implemented a focused candidate-quality repair on top of player-anchored hit recall v0.2.3.

The builder now:

- scores player-anchor ball candidates instead of blindly using a single closest point
- requires side-matched player contact-zone metadata for player-anchored hit candidates
- persists `player_anchor_contact_zone` details on candidates and diagnostics
- suppresses player-anchored hit candidates that overlap final bounce candidates
- records `overlap_suppression` diagnostics and summary counts

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

- `event_candidate_run_id`: `5280daf4-78f5-4d80-a011-fdac5d263d39`
- `hit_candidate`: 2
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 655
- `player_anchor_suppressed_overlap_count`: 1

The previous frame-34 player-anchored hit overlapping the frame-30 far-side bounce was suppressed
with `suppressed_by_bounce_candidate_overlap` and `open_court_landing_zone_anchor` diagnostics.

## Validation

Completed during implementation:

- `tests/test_hit_bounce_candidates.py`: 24 passed

Full repository validation should still be run before merge.

## Remaining Limitations

The contact-zone gate is still based on candidate court-template geometry and source projection
quality. It does not prove racket contact. Sparse trajectory segments can still leave true contacts
unrecoverable, and rejection diagnostics should be used to inspect missing candidates.

This repair does not add hit truth, bounce truth, in/out, score, rally/point logic, identity, or
adjudication.
