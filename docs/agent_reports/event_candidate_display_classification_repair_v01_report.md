# Event Candidate Display + Classification Repair v0.1 Report

## Summary

Repaired event-candidate replay display and classification. Event candidate markers now remain
visible as persistent review pins on both the broadcast video and court projection mini-map, with
active/selected states. The candidate builder now prioritizes `hit_candidate` when a trajectory
change is near a main-player projection, and keeps `bounce_candidate` for away-from-player
trajectory changes.

## Files Created

- `docs/events/event_candidate_display_classification_repair_v01.md`
- `docs/agent_reports/event_candidate_display_classification_repair_v01_report.md`

## Files Modified

- `apps/worker/services/hit_bounce_candidates.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/ReplayCourtProjectionMiniMap.tsx`
- `apps/web/src/components/ReplayEventCandidateVideoOverlay.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/types.ts`
- `tests/test_hit_bounce_candidates.py`
- `tests/test_tom_v1_bridge_helpers.py`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/events/hit_bounce_candidate_evidence_v0.md`
- `docs/events/event_candidate_video_overlay_v01.md`

## Classification Repair

The builder now uses `classification_priority = hit_first_when_player_proximate`.

For each trajectory context:

- a player-proximate direction or speed change creates a `hit_candidate`
- the same context does not fall through as a `bounce_candidate`
- away-from-player direction changes can create `bounce_candidate`
- same-window conflict resolution prefers the hit candidate when player proximity exists

The payload now includes `player_proximity_gate` and `candidate_decision` diagnostics so review can
see why a marker became a hit or bounce candidate.

## Old vs New Local Counts

Using the bridge DB:

- old `event_candidate_run_id`: `1917963a-e82d-4486-9af2-8cd3b6aa3709`
- old output: `hit_candidate = 0`, `bounce_candidate = 2`
- new `event_candidate_run_id`: `b0f3c0e8-3615-47f5-9515-27361f4a1336`
- new output: `hit_candidate = 1`, `bounce_candidate = 1`

The near-player marker is now a `HIT CANDIDATE`. The away-from-player marker remains a
`BOUNCE CANDIDATE`.

## Display Persistence

The video overlay and mini-map now render all selected event candidates as persistent pins:

- inactive markers remain visible but subdued
- active markers highlight near the current replay timestamp
- selected markers receive the strongest outline
- labels still include `CANDIDATE`

## Validation Results

- Focused event/replay tests: 43 passed.
- Full Python tests: 289 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: passed with 0 vulnerabilities.
- Fixture demo: passed.
- Fixture completion audit: passed.

## Local Visual Smoke Result

Using `event_candidate_run_id = b0f3c0e8-3615-47f5-9515-27361f4a1336`, browser smoke confirmed:

- video overlay rendered two persistent markers
- court mini-map rendered two persistent markers
- the near-player marker rendered as active `HIT CANDIDATE`
- the away-from-player marker rendered as inactive `BOUNCE CANDIDATE`
- selecting the bounce marker populated selected evidence details with image point, court point,
  classification priority, player gate distance/threshold, candidate decision, source ids, and
  no-truth warnings

Screenshot:

```text
.data/artifacts/event-candidate-display-classification-repair-v01-smoke.png
```

## Remaining Limitations

- Hit/bounce classification still uses deterministic 2D court-template heuristics.
- There is no ball height, racket detection, player identity, rally state, or score context.
- Persistent pins are review markers only; they are not event truth.

## Non-Goals Preserved

- No hit truth.
- No bounce truth.
- No in/out.
- No point or score.
- No player identity, OCR, server/receiver logic, or adjudication.
