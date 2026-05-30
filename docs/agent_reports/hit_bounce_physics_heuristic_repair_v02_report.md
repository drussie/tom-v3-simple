# Hit/Bounce Physics Heuristic Repair v0.2 Report

Status: implemented

## Summary

This repair changes event-candidate classification from generic 2D trajectory bends to
tennis-specific candidate heuristics:

- hit candidates prefer player-proximate court-y net-axis reversal
- bounce candidates prefer image-y descending-to-ascending proxy plus speed reduction
- source image points are loaded from persisted `ball_court_projection_candidate` rows
- selected replay evidence now exposes `net_axis_reversal`, `vertical_motion_proxy`, and
  `speed_reduction` diagnostics

The repair remains evidence-only and does not add hit truth, bounce truth, in/out, score, point
logic, or adjudication.

## Files Changed

- `apps/worker/services/hit_bounce_candidates.py`
- `apps/worker/cli.py`
- `apps/api/services/replay.py`
- `apps/web/src/lib/types.ts`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `Makefile`
- `tests/test_hit_bounce_candidates.py`
- `docs/events/hit_bounce_physics_heuristic_repair_v02.md`

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

- `event_candidate_run_id`: `d1f7b159-7260-4567-8943-cd641f7da528`
- `hit_candidate`: 1
- `bounce_candidate`: 2
- evaluated trajectory contexts: 33
- raw hit candidate drafts: 1
- raw bounce candidate drafts: 5
- deduped hit candidates: 1
- deduped bounce candidates: 2

Compared with the previous local run noted in the handoff, the hit count stayed at 1 and bounce
count increased from 1 to 2 because the repaired vertical-proxy plus speed-reduction gate surfaced
one additional candidate. This remains candidate evidence for review, not bounce truth.

## Diagnostics Observed

The hit candidate payload includes:

- `net_axis_reversal.axis = court_y`
- `net_axis_reversal.reversal = true`
- `near_main_player_projection`
- `net_axis_reversal`
- `player_proximate_event_priority`

The bounce candidate payloads include:

- `vertical_motion_proxy.descending_to_ascending = true`
- `vertical_motion_proxy.proxy_warning = image_y is camera-space proxy, not true ball height`
- `speed_reduction.speed_reduced = true`
- `away_from_main_player_projection`
- `inside_or_near_court_template`

## Remaining Limitations

- Image-y is only a camera-space proxy and is not true ball height.
- Court-y is treated as the first v0.2 net-axis convention for normalized template coordinates.
- Candidate counts can change as thresholds are tuned.
- Candidates are not adjudicated and do not decide in/out, hits, bounces, points, or score.
