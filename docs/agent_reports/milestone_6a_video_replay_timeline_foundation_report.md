# Milestone 6A Agent Report - Video Replay Timeline Foundation

## Summary

Milestone 6A starts Blueprint 6 and adds the replay workstation foundation.

TOM can now expose replay metadata for an indexed media asset, serve the local indexed media file to the browser, load that video in a `/replay/<media_id>` route, and display the current playback timestamp and nearest TOM frame from media-owned frame/time metadata.

This milestone does not add detection, tracklet, or pose overlay playback. It does not add live stream ingestion or tennis-event interpretation.

## Files Created

- `apps/api/services/replay.py`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayVideoPlayer.tsx`
- `apps/web/src/lib/replayTime.ts`
- `tests/test_replay_api.py`
- `docs/REPLAY_WORKSTATION.md`
- `docs/blueprints/tom_v3_blueprint_6_visual_replay_live_observation_workstation.md`
- `docs/milestones/milestone_6a_video_replay_timeline_foundation.md`
- `docs/handoffs/milestone_6a_video_replay_timeline_foundation_handoff.md`
- `docs/agent_reports/milestone_6a_video_replay_timeline_foundation_report.md`

## Files Modified

- `Makefile`
- `README.md`
- `apps/api/routers/media.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `apps/worker/services/local_demo.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CONTROL_ROOM.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/blueprints/tom_v3_simple_final_completion_review.md`

## Backend Replay-Info Decisions

`GET /media/{media_id}/replay-info` returns media metadata, `/media/{media_id}/video`, frame/time mode, frame-time index summary, observation-only flags, and available runs grouped by evidence type.

Available runs are grouped from persisted observations:

- detection: ball/player detection observations
- tracklet: tracklet candidate and track point candidate observations
- pose: player pose observations
- gameplay: view-state observations

## Video Serving Decisions

`GET /media/{media_id}/video` serves only local file-backed media referenced by the indexed media asset. It prefers stored URI/path metadata and returns `404` when no local video file is available.

This is local replay only, not stream ingestion.

## Frame / Time Mapping Decisions

6A uses indexed media metadata and a constant-frame-rate approximation:

```text
frame = round((timestamp_ms / 1000) * fps)
```

Frames are clamped to the indexed media frame range. The frontend labels the value as the nearest frame from media metadata.

## Frontend Replay Route Decisions

The new route is:

```text
/replay/<media_id>
```

It renders an HTML video player, current timestamp/frame telemetry, timeline/progress shell, media details, available run context, selected run context from optional query parameters, and a placeholder for future overlay layers.

## Tests Run

- `.venv/bin/python -m pytest tests/test_replay_api.py -q`
- `npm run lint`
- `ruff check apps/api/services/replay.py apps/api/routers/media.py tests/test_replay_api.py apps/worker/services/local_demo.py`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db make completion-audit PYTHON=.venv/bin/python`
- Browser replay smoke against `http://127.0.0.1:3000/replay/<media_id>`

## Validation Results

- Focused replay API tests: passed.
- Full Python suite: 164 passed.
- Ruff: passed.
- Web TypeScript lint: passed.
- Web production build: passed.
- npm audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Demo with `demo_assets/sample_point.mp4`: passed.
- Completion audit on demo state: passed.
- Browser replay smoke: page rendered, video metadata loaded from `/media/{media_id}/video`, and replay workstation text/run context appeared.

## Known Limitations

- 6A does not draw detection, tracklet, or pose overlays over video.
- 6A does not include evidence timeline lanes.
- Video serving is local file playback only.
- Live TV/stream proxy mode is future work.
- Frame/time mapping currently uses indexed constant-frame-rate metadata.

## Non-Goals Preserved

- No new model/runtime capability.
- No real pose inference.
- No detection/tracklet/pose overlay playback yet.
- No movement interpretation.
- No stroke classification.
- No homography or court-space reasoning.
- No bounce/hit/rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 6B - Detection Overlay Playback.
