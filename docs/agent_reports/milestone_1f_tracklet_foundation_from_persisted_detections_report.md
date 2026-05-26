# TOM v3 Simple - Milestone 2A Tracklet Repair Agent Report

## Summary

Status: complete.

This branch now implements Milestone 2A - Tracklet Candidate Foundation from Persisted Detections, even though the branch name remains `codex/m1f-tracklet-foundation-from-persisted-detections`.

The original 1F scaffold created `tracklet` and `track_point` rows, but those rows pointed their `observation_id` fields directly at source detection observations and did not create `observation_lineage` rows. The 2A repair makes tracklets and track points first-class TOM v3 observations:

- Each tracklet candidate gets a new observation spine row.
- Each track point candidate gets a new observation spine row.
- `tracklet.observation_id` points to the tracklet candidate observation.
- `track_point.observation_id` points to the track point candidate observation.
- Source detection observations remain immutable and are linked through payload metadata plus `observation_lineage`.

## Files Created

- `apps/worker/services/tracklet_builder.py`
- `docs/agent_reports/milestone_1f_tracklet_foundation_from_persisted_detections_report.md`
- `docs/handoffs/milestone_1f_tracklet_foundation_from_persisted_detections_handoff.md`
- `docs/milestones/milestone_1f_tracklet_foundation_from_persisted_detections.md`
- `docs/tracklets/tracklet_foundation_v0.md`
- `tests/test_tracklet_builder.py`

## Files Modified

- `Makefile`
- `README.md`
- `apps/web/src/app/globals.css`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/web/visual_evidence_viewer_v0.md`

## Tracklet Grouping Decisions

- The first grouping algorithm remains deterministic and simple.
- Ball detections are grouped into `ball` tracklet candidates in frame order.
- Player detections are grouped by persisted label when available: `near_player`, `far_player`, or `player_unknown`.
- A frame gap greater than `max_gap_frames` starts a new candidate tracklet.
- `max_center_distance_px` is stored in runtime configuration for the contract, but no sophisticated spatial association is implemented in this milestone.
- Every tracklet and track point records `track_status = candidate`, `identity_status = unverified`, and `frame_time_owner = media_indexing`.

## Persistence Decisions

- The tracklet builder creates its own `processing_run`, `processing_step`, `runtime_config`, and deterministic `model_registry` row.
- Source detection observations are not mutated.
- Each tracklet candidate creates a new `observation` row with `observation_family = track` and `observation_type = ball_tracklet_candidate | player_tracklet_candidate`.
- Each track point candidate creates a new `observation` row with `observation_family = track` and `observation_type = track_point_candidate`.
- `tracklet.observation_id` points to the tracklet candidate observation.
- `track_point.observation_id` points to the track point candidate observation.
- Source detection observation ids are stored in `track_point.payload_jsonb.source_detection_observation_id` and track point observation payloads.
- Track point frame/time values come from the source detection observations, preserving the media-indexing ownership rule.

## Lineage / Source-Link Decisions

- For each source detection, the builder creates a `tracked_from` lineage row:
  - parent: source detection observation
  - child: track point candidate observation
- For each track point, the builder creates a `grouped_from` lineage row:
  - parent: track point candidate observation
  - child: tracklet candidate observation
- The current schema does not have `observation_lineage.sequence_index`, so sequence indexes are stored in lineage `payload_jsonb`.
- Querying by `tracklet_id` now returns the tracklet candidate observation and track point candidate observations. Source detection observations are reachable through lineage and source ids in payload metadata.

## Viewer / Query Decisions

- Existing `GET /viewer/runs/{run_id}` can open a tracklet builder run and return candidate track observations, tracklets, track points, and lineage.
- Tracklet coverage segments use `state = candidate`; the web CSS styles that state in the timeline.
- Existing query filters can retrieve tracklet candidate and track point candidate observations by `tracklet_id`.
- The viewer remains single-run oriented. It can inspect a tracklet run, but it does not yet present a combined detection-run plus tracklet-run evidence bundle.

## Known Limitations

- This is a baseline temporal grouping layer, not a sophisticated multi-object tracking system.
- Spatial association for generic player detections is conservative and intentionally limited.
- Source detection ids are stored in payload metadata because `track_point` does not yet have a dedicated `source_detection_observation_id` column.
- The viewer does not yet combine source detection overlays, frame artifacts, and tracklet coverage across multiple runs.
- Real YOLO26 runtime/assets remain unavailable in this repo state.

## Tests Run

- `.venv/bin/python -m pytest tests/test_tracklet_builder.py -q`
- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- Local media fixture smoke with `index-media`
- Local detection fixture smoke with `run-detection-adapter`
- Local tracklet builder smoke with `build-tracklets`
- Viewer payload smoke for the tracklet builder run

## Validation Results

- Focused tracklet tests: 7 passed.
- Full pytest suite: 40 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Local media/detection/tracklet smoke: indexed a generated local video, created a fixture detection run, built 3 tracklet candidates, persisted 12 track points, and created 15 track observation rows.
- Lineage smoke: created 12 `tracked_from` rows and 12 `grouped_from` rows.
- Viewer payload smoke: returned the tracklet builder run with 3 tracklets and 12 track points.

## Non-Goals Preserved

- No pose detection was added.
- No court homography was added.
- No bounce detection was added.
- No hit detection was added.
- No rally or point reconstruction was added.
- No scoring was added.
- No real YOLO runtime integration was added.
- No complex tracker logic was added.
- No adjudication was added.

## Recommended Next Handoff

Recommended next milestone: Milestone 2B - Tracklet Viewer / Multi-Run Evidence Bundle.

Reason: candidate tracklets and track point observations now have first-class observation spine rows and lineage. The next useful step is a bundled evidence view that can show source detection observations, frame artifacts, track point candidate observations, and tracklet candidate observations together without elevating the grouping beyond candidate evidence.

If YOLO26 runtime/assets become available first, Milestone 2B could instead be Real YOLO Runtime Completion.
