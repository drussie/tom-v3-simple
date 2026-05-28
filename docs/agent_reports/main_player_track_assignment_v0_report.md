# Main Player Track Assignment v0 Report

## Summary

Implemented persistent candidate visual track assignment for the two primary tennis-player subjects. The new layer consumes `main_player_subject_candidate` rows, writes `main_player_track_candidate` and `main_player_track_assignment_candidate` observations, and allows real pose crop mode to consume `--source-track-run-id`.

## Files Created

- `apps/worker/services/main_player_track_assignment.py`
- `docs/perception/main_player_track_assignment_v0.md`
- `docs/agent_reports/main_player_track_assignment_v0_report.md`

## Files Modified

- `Makefile`
- `README.md`
- `apps/api/services/replay.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `apps/worker/services/real_pose_replay.py`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/perception/main_tennis_subject_filter_v0.md`
- `docs/perception/tom_v1_model_assets_bridge_v0.md`
- `packages/schema/tom_v3_schema/enums.py`
- `tests/test_main_subject_filter.py`
- `tests/test_tom_v1_bridge_helpers.py`

## Observation Types Added

- `main_player_track_candidate`
- `main_player_track_assignment_candidate`

Both are spine-only `tracking` observations. No migration or raw detection mutation was added.

## Design Summary

The v0 assignment groups role-consistent frame-local subject candidates into persistent visual track candidates:

- `near_player_candidate` -> `near_player_track_candidate_001`
- `far_player_candidate` -> `far_player_track_candidate_001`

Per-frame assignment candidates preserve the source subject candidate, source player detection, assignment score, continuity features, and track candidate id/role.

## Pose Integration

`run-real-pose` now accepts `--source-track-run-id`. When supplied, crop-mode pose uses only detections attached to `main_player_track_assignment_candidate` rows. Pose payloads and replay payloads include track candidate metadata.

## Lineage

Track assignment lineage preserves:

- `main_player_track_assignment_from_subject_candidate`
- `main_player_track_assignment_from_player_detection`
- `main_player_track_assignment_for_track_candidate`

Track-filtered pose lineage adds:

- `pose_from_main_player_track_assignment`
- `pose_from_main_player_track_candidate`

## CLI / Makefile Helpers

- `assign-main-player-tracks`
- `make tom-v1-main-player-tracks`
- `make tom-v1-pose-main-tracks`

## Validation Results

- `.venv/bin/python -m pytest tests/test_main_subject_filter.py tests/test_tom_v1_bridge_helpers.py -q` passed: 7 tests.
- `.venv/bin/python -m pytest -q` passed: 253 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed with `MAX_FRAMES=3`.
- Completion audit passed for the fixture demo database.
- Browser replay smoke passed against the TOM v1 bridge DB: the replay page loaded the track-filtered pose URL, showed nonzero detection/tracklet/pose evidence, listed main player track candidate context, and did not show the missing-timeline message.

## Local Smoke Result

Optional local TOM v1 bridge smoke was run against `sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db`.

Track assignment:

- `main_player_track_run_id`: `ec9c657d-bf58-4f52-9d28-188777bc126a`
- Source subject candidates considered: 428
- Track candidates: 2 total, one near-player candidate track and one far-player candidate track
- Assignment candidates: 428 total, 214 near-player assignments and 214 far-player assignments

Track-filtered TOM v1 pose:

- `pose_run_id`: `e436be74-7ce1-44b9-ac83-6abb8e668e1e`
- Pose observations: 424
- Lineage rows: 1696
- Frames considered: 214
- Pose source mode: `main_player_track_assignment_v0`

## Remaining Limitations

Main player tracks are candidate visual tracks only. They are not player identities, names, server/receiver roles, side assignments, accepted tracks, or tennis truth.

## Non-goals Preserved

- No raw detections were mutated or deleted.
- No player identity truth was added.
- No ball/player court-space projection was added.
- No bounce/hit/in-out/rally/point/scoring was added.
- No accepted/rejected lifecycle or adjudication was added.

## Recommended Next Step

Identity Architecture Contract v0: define `player_A` / `player_B`, scoreboard OCR evidence, server candidates, side assignments, and future TOM-derived score reconciliation on top of stable visual player track candidates.
