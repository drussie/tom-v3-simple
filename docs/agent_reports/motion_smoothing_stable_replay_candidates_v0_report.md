# Motion Smoothing / Stable Replay Candidates v0 Report

## Summary

Added a derived motion-smoothing candidate layer for replay-ready ball, main-player box, and pose
overlays. Raw evidence remains unchanged and inspectable.

## Files Created

- `apps/worker/services/motion_smoothing.py`
- `apps/web/src/components/ReplaySmoothedMotionOverlay.tsx`
- `docs/motion/motion_smoothing_stable_replay_candidates_v0.md`
- `docs/agent_reports/motion_smoothing_stable_replay_candidates_v0_report.md`
- `tests/test_motion_smoothing.py`

## Files Modified

- `packages/schema/tom_v3_schema/enums.py`
- `apps/worker/cli.py`
- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/replayTimeline.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/app/globals.css`
- `Makefile`
- `tests/test_replay_api.py`
- `tests/test_tom_v1_bridge_helpers.py`
- `docs/RUNBOOK_LOCAL.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/perception/tom_v1_model_assets_bridge_v0.md`

## Smoothing Method Summary

- Ball: rolling median over a short frame window, without interpolation over long gaps.
- Player boxes: per-role EMA over accepted main-player track assignment bboxes.
- Pose: per-subject/keypoint EMA over present keypoints only.

## Observation Types Created

- `smoothed_ball_position_candidate`
- `smoothed_main_player_box_candidate`
- `smoothed_pose_candidate`

All carry `smoothed_candidate_only`, `observation_only`, `no_adjudication`, and not-truth metadata.

## Replay Layers Added

- `smoothed_ball`
- `smoothed_player_boxes`
- `smoothed_pose`
- timeline lane: `smoothed_motion`

When a smoothing run is selected, replay defaults to smoothed ball, smoothed player boxes, and
smoothed pose while keeping raw evidence available through toggles.

## Lineage Decisions

Smoothed observations link back to source observations with:

- `smoothed_from_ball_detection`
- `smoothed_from_track_point_candidate`
- `smoothed_from_main_player_track_assignment`
- `smoothed_from_pose_observation`

## Validation Results

- `.venv/bin/python -m pytest -q` passed: 269 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed against `tmp_tom_v3_motion_smoothing_fixture.db`.
- Completion audit passed against `tmp_tom_v3_motion_smoothing_fixture.db`.

## Local Smoke Result

Using `tmp_tom_v3_tom_v1_bridge.db`, `make tom-v1-motion-smoothing` completed for media
`9518fb01-0da1-4344-9a84-ff88ec8e9b1e`.

- `motion_smoothing_run_id`: `7cb26de6-e3eb-43a9-a415-bcf9706b3f9a`
- `smoothed_ball_position_candidate`: 75
- `smoothed_main_player_box_candidate`: 405
- `smoothed_pose_candidate`: 401
- Total smoothed observations: 881

Browser replay smoke loaded the run through the Next proxy and API with smoothed ball, player-box,
and pose layers selected by default. The visible replay state showed smoothed candidates and the
`smoothed_motion` timeline lane.

## Known Limitations

- Ball smoothing is deterministic and simple; it does not infer trajectory physics.
- Player-box smoothing depends on accepted main-player track assignment candidates.
- Pose smoothing does not fill missing keypoints across gaps.
- Replay smoothing improves display stability but does not prove tracking correctness.

## Non-Goals Preserved

No bounce/hit/in-out, rally/point/score, player identity, scoreboard OCR, server/receiver logic,
court-space projection, accepted/rejected lifecycle, or adjudication was added.

## Push Status

Pending final commit/tag/push.

## Recommended Next Step

Object-to-Court Projection Candidate v0.
