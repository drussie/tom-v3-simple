# Main Player Track Assignment v0.1 Replay Labels Report

## Summary

Main Player Track Assignment v0.1 repairs the v0 behavior by making near/far visual track candidates visible in replay and by adding a lightweight persistent-lock assignment heuristic. The branch keeps the evidence-only boundary: track labels are candidate visual tracks, not player identities.

## Files Created

- `apps/web/src/components/ReplayMainPlayerTrackOverlay.tsx`
- `docs/agent_reports/main_player_track_assignment_v01_replay_labels_report.md`

## Files Modified

- `Makefile`
- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/replayTimeline.ts`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `apps/worker/services/main_player_track_assignment.py`
- `apps/worker/services/real_pose_replay.py`
- `tests/test_main_subject_filter.py`
- `tests/test_replay_api.py`
- `tests/test_tom_v1_bridge_helpers.py`
- `docs/perception/main_player_track_assignment_v0.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/perception/tom_v1_model_assets_bridge_v0.md`

## Root Cause

The v0 track assignment mostly grouped frame-local `near_player_candidate` and `far_player_candidate` rows into two tracks. If the subject filter briefly selected an upper-edge ball kid or wall-side person, v0 could still persist that assignment and pass it to pose. Replay also had no dedicated `main_player_tracks` overlay layer, so the new track evidence was present but visually unclear.

## Visual Label Implementation

Replay overlay and timeline APIs now accept `main_player_track_run_id` and return `main_player_tracks` payloads for `main_player_track_assignment_candidate` observations. The replay workstation accepts `mainPlayerTrackRunId`, enables the main player track layer by default when a run is selected, and draws selectable `NEAR TRACK` / `FAR TRACK` labels from current active assignments.

The selected evidence panel shows track candidate id, role candidate, assignment score, method, source subject candidate observation id, source detection observation id, track lock state, and candidate-only warnings.

## Track Assignment / Locking Changes

The assignment method is now `main_player_track_assignment_v01`. For each role, v0.1 selects a plausible seed and then applies continuity checks across frames. It rejects assignments with large normalized center jumps, large bbox-area changes, or strong edge/wall penalties unless continuity is already strong. Rejected frames become gaps instead of forced pose sources.

## Tests Run

- `.venv/bin/python -m pytest tests/test_main_subject_filter.py tests/test_replay_api.py tests/test_tom_v1_bridge_helpers.py -q`
- `ruff check apps/worker/services/main_player_track_assignment.py apps/worker/services/real_pose_replay.py apps/api/services/replay.py apps/api/routers/replay.py tests/test_main_subject_filter.py tests/test_replay_api.py`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`

## Validation Results

- Full Python test suite: 256 passed.
- Ruff: passed.
- Web lint/typecheck: passed.
- Web production build: passed.
- Web audit: 0 vulnerabilities.

## Local Smoke Result

Using the TOM v1 bridge database, v0.1 produced:

- `main_player_track_run_id`: `e2ebf81a-a804-4f16-86e4-5faaed51f05d`
- near-player assignments: 214
- far-player assignments: 191
- total assignments: 405
- source subject candidates considered: 428

The reduced far-player assignment count confirms v0.1 left implausible far-role frames as gaps rather than forcing every frame into the far track.

Track-filtered pose from the new run completed:

- `pose_run_id`: `b9c942f1-972e-4994-a0ac-f466b7e0c35a`
- pose observations: 401
- source player detections considered: 405

Replay proxy and browser smoke confirmed that `main_player_tracks` payloads load, the timeline includes the main player track lane, and visible `NEAR TRACK` / `FAR TRACK` labels are present without the missing-timeline message.

## Known Limitations

- v0.1 is still a heuristic visual track candidate layer.
- Track gaps are expected when the best candidate is implausible.
- A difficult frame can still produce a wrong temporary visual assignment.
- Track labels are not player names, identity truth, side assignment, server/receiver state, or accepted tracks.

## Non-goals Preserved

- No player names.
- No confirmed player identity.
- No scoreboard OCR.
- No server/receiver truth.
- No side-change identity logic.
- No bounce/hit/in-out/rally/point/scoring.
- No ball/player court-space projection.
- No raw detection mutation or deletion.
- No adjudication or accepted/rejected lifecycle.

## Push Status

Pending final validation, commit, tag, and push.

## Recommended Next Step

After this repair is accepted, the next architecture step should be Identity Architecture Contract v0, defining future `player_A` / `player_B`, scoreboard OCR evidence, server candidates, side assignments, and score reconciliation without treating visual track candidates as identity truth.
