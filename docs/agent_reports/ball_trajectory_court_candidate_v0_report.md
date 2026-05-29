# Ball Trajectory Court Candidate v0 Report

## Summary

Implemented a derived court-space ball trajectory candidate layer from existing
`ball_court_projection_candidate` observations. The layer persists ordered trajectory segments with
gap, bounds, velocity, direction, and homography carry-forward diagnostics while preserving
observation-only semantics.

## Files Created

- `apps/worker/services/ball_court_trajectory.py`
- `docs/trajectory/ball_trajectory_court_candidate_v0.md`
- `docs/agent_reports/ball_trajectory_court_candidate_v0_report.md`
- `tests/test_ball_court_trajectory.py`

## Files Modified

- `Makefile`
- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/ReplayCourtProjectionMiniMap.tsx`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/replayTimeline.ts`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `packages/schema/tom_v3_schema/enums.py`
- `tests/test_replay_api.py`
- `tests/test_tom_v1_bridge_helpers.py`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/projection/object_to_court_projection_candidates_v0.md`

## Trajectory Method

The builder orders ball court projection candidates by media-owned timestamp, frame, and
observation id. It splits segments when frame or time gaps exceed configured thresholds and drops
segments shorter than `min_points_per_segment`. v0 does not interpolate, use a physics model, or
infer events.

## Observation Types Created

- `ball_trajectory_court_candidate`

The new rows use `observation_family = trajectory`, `granularity = segment`, and
`coordinate_space = court_template_2d`.

## Diagnostics

Each trajectory segment stores ordered points and per-step kinematic diagnostics:

- `dt_ms`
- `dx`
- `dy`
- `speed_template_units_per_second`
- `direction_angle_degrees`

Run and payload diagnostics include gap splits, dropped segments, out-of-template points, and
homography carry-forward counts.

## Replay / Mini-Map Behavior

Replay accepts `ballTrajectoryRunId` and exposes the `ball_court_trajectory` layer plus a
`ball_trajectory` timeline lane. The court projection mini-map draws a subtle trajectory candidate
path and keeps current ball/player projection candidates distinct.

## Validation Results

- `.venv/bin/python -m pytest -q` passed: 280 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed: 0 vulnerabilities.
- Fixture demo passed with `tmp_tom_v3_ball_trajectory_fixture.db`.
- Fixture completion audit passed with `tmp_tom_v3_ball_trajectory_fixture.db`.

## Local Smoke Result

Using `sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db`:

- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `fff6c194-d66e-4444-83a4-c53b9ef8903c`
- Source point count: 75
- Segment count before short-segment dropping: 11
- Persisted segment count: 7
- Dropped short segment count: 4
- Gap split count: 10
- Out-of-template point count: 4

Replay smoke loaded the existing local workstation with `ballTrajectoryRunId`, confirmed the ball
trajectory run selector and layer toggle were present, and confirmed the court projection mini-map
remained available with projection candidate evidence.

## Remaining Limitations

The trajectory is a court-template candidate sequence only. It does not smooth in court space,
interpolate missing points, classify bounces or hits, or decide in/out.

## Non-Goals Preserved

No bounce, hit, in/out, rally, point, score, player identity, scoreboard OCR, server/receiver logic,
accepted/rejected lifecycle, or adjudication was added.

## Push Status

Pending commit, tag, and push at report authoring time. Final response records the completed push.

## Recommended Next Step

Hit/Bounce Candidate Evidence v0.
