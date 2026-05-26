# TOM v3 Simple - Milestone 1F Agent Report

## Summary

Status: complete.

Milestone 1F adds a deterministic tracklet foundation that groups already-persisted `ball_detection` and `player_detection` observations into candidate temporal groupings. The worker creates a separate tracklet builder run, persists `tracklet` and `track_point` rows, links each track point back to its source detection observation, and keeps the result queryable and visible through the existing viewer payload.

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

- The first grouping algorithm is intentionally deterministic and simple.
- Ball detections are grouped into `ball` tracklet candidates in frame order.
- Player detections are grouped by persisted label when available: `near_player`, `far_player`, or `player_unknown`.
- A frame gap greater than `max_gap_frames` starts a new candidate tracklet.
- `max_center_distance_px` is stored in runtime configuration for the contract, but no sophisticated spatial association is implemented in this milestone.
- Every tracklet metadata payload records `track_status = candidate`, `identity_status = unverified`, and `frame_time_owner = media_indexing`.

## Persistence Decisions

- The tracklet builder creates its own `processing_run`, `processing_step`, `runtime_config`, and deterministic `model_registry` row.
- Source detection observations are not mutated.
- `tracklet` rows summarize the candidate grouping and include viewer-friendly coverage metadata.
- `track_point` rows carry the source detection frame, timestamp, bbox, center, confidence, and source observation metadata.
- Track point frame/time values come from the source detection observations, preserving the media-indexing ownership rule.

## Lineage / Source-Link Decisions

- `track_point.observation_id` references the source `ball_detection` or `player_detection` observation.
- `tracklet.observation_id` uses the first source detection as a representative source link.
- `track_point.payload_jsonb` also stores source observation id/type/label and frame-time ownership metadata.
- No `observation_lineage` rows are created because the current lineage table links observation spine rows, while tracklets and track points are separate tables. This limitation is documented in `docs/tracklets/tracklet_foundation_v0.md`.

## Viewer / Query Decisions

- Existing `GET /viewer/runs/{run_id}` can open a tracklet builder run and return tracklets plus track points.
- Tracklet coverage segments use `state = candidate`; the web CSS now styles that state in the timeline.
- Existing query filters can retrieve source observations by `tracklet_id` because track points reference detection observation ids.
- The viewer remains single-run oriented. It can inspect a tracklet run, but it does not yet present a combined detection-run plus tracklet-run evidence bundle.

## Known Limitations

- This is a baseline temporal grouping layer, not a sophisticated multi-object tracking system.
- Spatial association for generic player detections is conservative and intentionally limited.
- Tracklet-to-source provenance uses track point links and metadata, not `observation_lineage` rows.
- The viewer does not yet combine source detection overlays and tracklet coverage across multiple runs.
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

- Focused tracklet tests: 5 passed.
- Full pytest suite: 38 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Local media/detection/tracklet smoke: indexed a generated local video, created a fixture detection run, built 3 tracklet candidates, and persisted 12 track points.
- Viewer payload smoke: returned the tracklet builder run with 3 tracklets and 12 track points.

## Non-Goals Preserved

- No pose detection was added.
- No court homography was added.
- No bounce detection was added.
- No hit detection was added.
- No rally or point reconstruction was added.
- No scoring was added.
- No real YOLO runtime integration was added.
- No adjudication was added.

## Recommended Next Handoff

Recommended next milestone: Milestone 1G - Tracklet Viewer / Multi-Run Evidence Bundle.

Reason: candidate tracklets now exist, but the viewer is still centered on one run at a time. A multi-run evidence bundle would let the UI show source detection observations, frame artifacts, and tracklet coverage together without pretending the grouping is more certain than it is.

If YOLO26 runtime/assets become available first, Milestone 1G could instead be Real YOLO Runtime Completion.
