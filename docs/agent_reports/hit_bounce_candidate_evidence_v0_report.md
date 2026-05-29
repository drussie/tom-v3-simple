# Hit/Bounce Candidate Evidence v0 Report

## Summary

Implemented first-pass `hit_candidate` and `bounce_candidate` derived evidence from
`ball_trajectory_court_candidate` and `main_player_court_projection_candidate` rows.

## Files Created

- `apps/worker/services/hit_bounce_candidates.py`
- `docs/events/hit_bounce_candidate_evidence_v0.md`
- `docs/agent_reports/hit_bounce_candidate_evidence_v0_report.md`
- `tests/test_hit_bounce_candidates.py`

## Files Modified

- `Makefile`
- `apps/worker/cli.py`
- `packages/schema/tom_v3_schema/enums.py`
- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/replayTimeline.ts`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/components/ReplayCourtProjectionMiniMap.tsx`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/app/globals.css`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/trajectory/ball_trajectory_court_candidate_v0.md`
- `tests/test_tom_v1_bridge_helpers.py`

## Candidate Methods

Hit candidates use `trajectory_player_proximity_hit_candidate_v0`: local trajectory direction
change near a main-player court projection candidate within a time window.

Bounce candidates use `trajectory_shape_bounce_candidate_v0`: local trajectory direction change
away from main-player projection candidates and inside or near the court template.

Both methods use transparent deterministic scores and modest confidence caps.

## Observation Types

- `hit_candidate`
- `bounce_candidate`

Both use `observation_family = event_candidate`, `granularity = frame`, and
`coordinate_space = court_template_2d`.

## Lineage

Each candidate links to the source `ball_trajectory_court_candidate`; when available, it also links
to the source `ball_court_projection_candidate` and nearest
`main_player_court_projection_candidate`.

## Replay

Replay now accepts `eventCandidateRunId`, fetches `hit_candidates` and `bounce_candidates`, exposes
an `event_candidates` timeline lane, and renders candidate markers in the court projection mini-map.

## Validation Results

- `.venv/bin/python -m pytest -q` -> 286 passed
- `ruff check .` -> passed
- `cd apps/web && npm run lint` -> passed
- `cd apps/web && npm run build` -> passed
- `cd apps/web && npm audit --omit=dev` -> 0 vulnerabilities
- fixture demo -> passed
- fixture completion audit -> passed

## Local Smoke Result

Using `sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db`:

- media id: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- court projection run id: `82498799-490f-44df-9222-0157356c5ff7`
- ball trajectory run id: `2e16f3d1-e252-497a-b688-d81890645ab7`
- event candidate run id: `89079e62-e580-47f1-bce3-8370614f6ca1`
- output: 0 `hit_candidate`, 2 `bounce_candidate`
- evaluated trajectory points: 33
- trajectory segments: 7

Replay proxy/timeline checks returned the event-candidate payloads. Browser smoke confirmed the
replay page loads with the court projection mini-map, event-candidate layer control, and
`event_candidates` timeline lane.

## Remaining Limitations

- v0 has only 2D court-template trajectory; no ball height is modeled.
- candidates are heuristic, low-authority evidence markers.
- no rally ordering, alternation, point logic, in/out, or scoring is inferred.

## Non-Goals Preserved

- No hit truth
- No bounce truth
- No in/out
- No rally, point, or score
- No player identity
- No accepted/rejected lifecycle
- No adjudication

## Recommended Next Step

Blueprint 8 completion review or a focused candidate-quality audit over real local replay data.
