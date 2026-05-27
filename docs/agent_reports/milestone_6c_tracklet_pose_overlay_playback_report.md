# Milestone 6C Agent Report - Tracklet / Pose Overlay Playback

## Summary

Milestone 6C extends the replay workstation from detection-only playback to synchronized detection, tracklet candidate, and pose keypoint evidence playback. Persisted candidate track points/paths and persisted pose keypoints/skeletons now render over indexed video using TOM media-owned frame/time.

## Files Created

- `apps/web/src/components/ReplayTrackletOverlay.tsx`
- `apps/web/src/components/ReplayPoseOverlay.tsx`
- `docs/milestones/milestone_6c_tracklet_pose_overlay_playback.md`
- `docs/handoffs/milestone_6c_tracklet_pose_overlay_playback_handoff.md`
- `docs/agent_reports/milestone_6c_tracklet_pose_overlay_playback_report.md`

## Files Modified

- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/app/globals.css`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/types.ts`
- `tests/test_replay_api.py`
- README and Blueprint 6 docs/control-room/runbook/status docs

## Backend Overlay Decisions

- Kept `/replay/overlays` as the single replay overlay endpoint.
- Extended `layers` to support `detections`, `tracklets`, and `pose`.
- Added optional `tracklet_run_id`, `pose_run_id`, and display-only `min_pose_confidence` filters.
- Returned normalized dict payloads rather than ORM rows.

## Tracklet Payload Decisions

- Tracklet overlays are candidate temporal groupings.
- Payloads include persisted `Tracklet` rows and their persisted `TrackPoint` rows.
- No interpolation, smoothing, or missing point inference is performed.
- Candidate and unverified status language is preserved in the payload.

## Pose Payload Decisions

- Pose overlays are persisted keypoint evidence.
- Payloads include pose bbox context, persisted keypoints, summary counts, subject association candidate context, and COCO17 edges from the skeleton registry.
- Missing keypoints remain in the payload but are not rendered as present overlay points.

## Coordinate Scaling Decisions

- Reused 6B contained-video coordinate mapping.
- Added point scaling for track points and pose keypoints.
- Source coordinates remain original media image pixels.

## Frontend Overlay Decisions

- Added separate SVG overlay layers for tracklet candidates and pose observations.
- Detection, tracklet, and pose layers can be toggled independently.
- Detection, tracklet, and pose runs are selected from replay-info or URL query params.
- Selected tracklets show candidate paths; active track points and poses use a visual display hold only.

## Click / Select Decisions

- Bboxes select detection observations.
- Track points select track point candidate detail.
- Candidate paths/ticks select tracklet candidate detail.
- Pose skeletons/keypoints select pose observation detail.
- Detail copy uses evidence/candidate wording and avoids identity or event claims.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6c.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6c.db make completion-audit PYTHON=.venv/bin/python`
- Browser smoke against `/replay/<media_id>?detectionRunId=...&trackletRunId=...&poseRunId=...`

## Validation Results

- Python tests: 175 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Demo smoke: passed.
- Completion audit: passed.
- Browser smoke: replay page loaded with detection, tracklet, and pose controls; DOM showed detection boxes, tracklet points, pose keypoints, and pose edges; clicking a pose overlay selected the pose observation detail panel.

## Known Limitations

- Full evidence timeline lanes and a richer scrubber are deferred to 6D.
- Replay remains local indexed file playback, not stream ingestion.
- Tracklet paths are persisted candidate evidence only.
- Pose skeletons are persisted keypoint evidence only.
- Sparse fixture observations use display holds for visual inspection; persisted observations are not changed.

## Non-goals Preserved

- No stream proxy mode.
- No live stream ingestion.
- No real pose inference.
- No movement interpretation.
- No stroke, serve, hit, split-step, or biomechanics conclusions.
- No homography, bounce, rally, point, scoring, or adjudication.

## Push Status

Final branch and tag push are performed after this report is committed. Required targets:

- branch: `codex/m6c-tracklet-pose-overlay-playback`
- tag: `tom-v3-m6c-tracklet-pose-overlay-playback`

## Recommended Next Handoff

Milestone 6D - Timeline Lanes / Evidence Scrubber.
