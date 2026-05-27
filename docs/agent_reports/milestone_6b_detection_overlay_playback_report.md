# Milestone 6B - Detection Overlay Playback Report

## Summary

Milestone 6B adds synchronized detection observation overlays to the Replay Workstation.

The replay page now fetches persisted `ball_detection` and `player_detection`
observations by media/time window, renders their stored image-pixel bboxes over
the indexed video, supports detection layer controls and detection run selection,
and lets an operator click a bbox to inspect the selected persisted observation.

Detection boxes remain observation evidence only. No tennis-event interpretation
or adjudication was added.

## Files Created

- `apps/api/routers/replay.py`
- `apps/web/src/app/api/replay/overlays/route.ts`
- `apps/web/src/components/ReplayDetectionOverlay.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/replayOverlays.ts`
- `docs/milestones/milestone_6b_detection_overlay_playback.md`
- `docs/handoffs/milestone_6b_detection_overlay_playback_handoff.md`
- `docs/agent_reports/milestone_6b_detection_overlay_playback_report.md`

## Files Modified

- `README.md`
- `apps/api/main.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayVideoPlayer.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_blueprint_6_visual_replay_live_observation_workstation.md`
- `tests/test_replay_api.py`

## Backend Overlay Decisions

- Added `GET /replay/overlays`.
- Kept 6B scoped to `layers=detections`.
- Returned only persisted `ball_detection` and `player_detection` observations.
- Filtered by `media_id`, `start_ms`, `end_ms`, optional `detection_run_id`, and optional display-only `min_confidence`.
- Returned normalized dict payloads rather than raw ORM rows.
- Preserved `observation_only` and `no_adjudication` flags in the overlay response.

## Detection Payload Decisions

- Overlay items use `overlay_type = detection_bbox`.
- Bboxes are returned as `{x, y, w, h}` in original media image pixels.
- Payloads include observation id, run id, frame number, timestamp, observation type, label, confidence, source runtime, and `source_language = detection observation`.
- The service reads bbox data from atomic detail payloads when present and falls back to observation payloads.

## Coordinate Scaling Decisions

- Frontend scaling uses contained-video geometry so original image-pixel bboxes map correctly into the rendered video area.
- The helper accounts for letterboxing offsets when the video uses contained aspect-ratio display.
- Detection display hold is visual-only and does not alter persisted observations.

## Frontend Overlay Decisions

- `/replay/[mediaId]` now renders a client-side `ReplayWorkstation`.
- The workstation fetches 2-second overlay chunks and caches them by media/run/window.
- `detectionRunId` query parameter selects the detection run when valid.
- If exactly one detection run exists, the replay page auto-selects it.
- Tracklet and pose run ids are displayed as context only; their overlay playback remains deferred.

## Click / Select Decisions

- Detection bboxes render as clickable overlay buttons.
- Clicking a bbox selects the persisted detection observation and shows id, run id, label, confidence, frame, timestamp, bbox, source language, and a link to the source evidence run.
- The selected detail language says “Detection observation. Evidence only, not a confirmed object or tennis event.”

## Tests Run

- `.venv/bin/python -m pytest -q` - passed, 170 tests.
- `pytest -q` - did not collect repo tests because the shell resolved to a system Python 3.8 pytest with an incompatible global plugin; rerun through the project venv passed.
- `ruff check .` - passed.
- `cd apps/web && npm run lint` - passed.
- `cd apps/web && npm run build` - passed.
- `cd apps/web && npm audit --omit=dev` - passed, 0 vulnerabilities.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head` - passed.
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py` - passed.
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6b.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3` - passed.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6b.db make completion-audit PYTHON=.venv/bin/python` - passed.
- Browser smoke with local API/web servers - passed: replay page loaded the sample media, fetched 9 detection overlays, rendered current-frame bboxes, and clicking a bbox populated selected detection observation detail.

## Validation Results

Validation passed after the client overlay fetch was routed through a Next API proxy to avoid browser CORS issues.

The final demo media id was `783074bd-6044-47de-af50-079c23f63827`.
The final demo detection run id was `6e1fb1d7-8798-4ba1-926b-79e06affaf00`.
The completion audit returned `status = passed` with no warnings or failures.

## Known Limitations

- 6B displays detection observations only.
- Tracklet candidate replay, pose keypoint replay, and full evidence timeline lanes remain future Blueprint 6 work.
- Display hold makes sparse detections visible to operators but does not imply persistence changes.
- The replay layer is local indexed-file replay, not live stream ingestion.

## Non-Goals Preserved

- No tracklet overlay playback.
- No pose overlay playback.
- No live stream ingestion.
- No new model/runtime capability.
- No real pose inference.
- No movement interpretation.
- No stroke classification.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.

## Push Status

The branch is prepared for commit, tag, and remote push after this report is written.
The final assistant response records the actual pushed branch, commit SHA, and tag.

## Recommended Next Handoff

Milestone 6C - Tracklet / Pose Overlay Playback
