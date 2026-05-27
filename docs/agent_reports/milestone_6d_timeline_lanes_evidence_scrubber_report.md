# Milestone 6D Agent Report - Timeline Lanes / Evidence Scrubber

## Summary

Milestone 6D adds temporal navigation to the Blueprint 6 replay workstation. The
replay API now returns normalized evidence lanes for detection observations,
tracklet candidates, pose observations, and review annotations. The replay UI
renders those lanes with a current playhead, and timeline item clicks seek video
playback while selecting persisted evidence detail.

## Files Created

- `apps/web/src/app/api/replay/timeline/route.ts`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/lib/replayTimeline.ts`
- `docs/milestones/milestone_6d_timeline_lanes_evidence_scrubber.md`
- `docs/handoffs/milestone_6d_timeline_lanes_evidence_scrubber_handoff.md`
- `docs/agent_reports/milestone_6d_timeline_lanes_evidence_scrubber_report.md`

## Files Modified

- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/ReplayVideoPlayer.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `tests/test_replay_api.py`
- `README.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/CONTROL_ROOM.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CURRENT_STATE.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/blueprints/tom_v3_blueprint_6_visual_replay_live_observation_workstation.md`

## Backend Timeline Decisions

The timeline endpoint is separate from overlay chunks because it is selected-run
context that should be fetched when media/run selections change, not every
playback frame.

## Timeline Payload Decisions

Detection and pose observations are point-like timeline ticks. Tracklet
candidates are spans from persisted track point times. Review annotations are
included when they can be mapped to a target frame/time. All payloads keep
observation/evidence/candidate wording and include `observation_only` and
`no_adjudication` flags.

## Frontend Evidence Lane Decisions

The replay workstation now fetches `GET /replay/timeline` through a Next proxy
route. `ReplayEvidenceTimeline` renders lanes as simple HTML/CSS controls with a
playhead and empty states. Layer visibility dims lane context but keeps evidence
available for navigation.

## Click-To-Seek/Select Decisions

Timeline clicks create a seek request consumed by `ReplayVideoPlayer`, then
select a timeline-backed evidence detail. Overlay highlighting uses the same
observation/tracklet/pose identifiers, so highlighting catches up when the
overlay chunk for the seeked time loads.

## Tests Run

- `.venv/bin/python -m pytest tests/test_replay_api.py -q`
- `ruff check apps/api/services/replay.py apps/api/routers/replay.py tests/test_replay_api.py`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6d.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6d.db make completion-audit PYTHON=.venv/bin/python`
- Browser smoke on `/replay/<media_id>?detectionRunId=...&trackletRunId=...&poseRunId=...`

## Validation Results

- Focused replay API tests: 21 passed.
- Full Python suite: 180 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Demo smoke: passed with sample media and created detection, tracklet, pose, annotation, and export evidence.
- Completion audit: passed with `ok: true` and no warnings/failures.
- Browser smoke: replay page loaded video, overlay chunks, timeline lanes, review annotation markers, and click-to-seek/select behavior. A later detection timeline tick sought video playback to 2 seconds and selected the persisted detection detail.

## Known Limitations

- Timeline lanes are v0 navigation controls, not a full editor.
- Annotation markers require a media-owned frame/time on the annotation or its
  target observation.
- Stream proxy mode and live ingestion remain future work.

## Non-Goals Preserved

- No stream proxy mode.
- No live stream ingestion.
- No new model/runtime capability.
- No real pose inference.
- No movement interpretation.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.

## Push Status

- Branch: `codex/m6d-timeline-lanes-evidence-scrubber`
- Tag: `tom-v3-m6d-timeline-lanes-evidence-scrubber`
- Branch and tag push completed as part of milestone closeout.

## Recommended Next Handoff

Milestone 6E - Stream Proxy Mode
