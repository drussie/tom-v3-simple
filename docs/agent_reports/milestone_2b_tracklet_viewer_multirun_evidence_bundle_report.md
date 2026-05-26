# TOM v3 Simple - Milestone 2B Agent Report

## Summary

Status: complete.

Milestone 2B adds the first dynamic tracklet evidence bundle and viewer inspection panel. A tracklet candidate can now be inspected across the tracklet builder run and source detection run, showing track point candidates, source detections, frame artifacts when available, and lineage rows that connect the evidence.

## Files Created

- `apps/api/routers/tracklets.py`
- `apps/api/services/tracklet_evidence_bundle.py`
- `apps/web/src/app/api/tracklets/[trackletId]/evidence-bundle/route.ts`
- `apps/web/src/components/TrackletEvidencePanel.tsx`
- `apps/web/src/lib/trackletEvidence.ts`
- `docs/agent_reports/milestone_2b_tracklet_viewer_multirun_evidence_bundle_report.md`
- `docs/blueprints/tom_v3_blueprint_2_temporal_evidence_tracklet_candidate_system.md`
- `docs/handoffs/milestone_2b_tracklet_viewer_multirun_evidence_bundle_handoff.md`
- `docs/milestones/milestone_2b_tracklet_viewer_multirun_evidence_bundle.md`
- `docs/tracklets/tracklet_evidence_bundle_v0.md`
- `docs/web/tracklet_evidence_viewer_v0.md`
- `tests/test_tracklet_evidence_bundle.py`

## Files Modified

- `README.md`
- `apps/api/main.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/api/backend_api_v0.md`
- `docs/dev/local_demo_runbook.md`
- `docs/tracklets/tracklet_foundation_v0.md`
- `docs/web/visual_evidence_viewer_v0.md`

## Evidence Bundle Decisions

- Evidence bundles are dynamic API responses, not persisted tables.
- The bundle is built from existing `tracklet`, `track_point`, `observation`, `observation_lineage`, artifact, run, model, and config rows.
- The bundle centers on one tracklet candidate id.
- Source detections are resolved through `tracked_from` lineage and track point payload metadata.
- Track points are linked to the tracklet through `grouped_from` lineage.

## Multi-Run Viewer Decisions

- The viewer remains opened on a single run URL.
- Opening a tracklet builder run shows existing tracklet rows and observations.
- Selecting a tracklet loads the multi-run evidence bundle in a focused panel.
- The panel shows source detection evidence from the detection run without building a full multi-run timeline.

## Artifact Matching Decisions

- Targeted `frame_image` and `detection_frame_image` artifacts are preferred.
- Same-frame frame artifacts are used as a fallback.
- Missing frame artifacts do not fail the bundle or the viewer panel.
- Local artifact content uses the existing `/artifacts/{artifact_id}/content` route.

## Lineage Display Decisions

- The bundle exposes raw lineage rows and per-track-point lineage references.
- The viewer shows `tracked_from` and `grouped_from` lineage ids for the selected track point.
- Source detection, track point candidate, and tracklet candidate ids remain visible.

## Known Limitations

- The viewer does not yet fuse source detection overlays and tracklet coverage into one multi-run timeline.
- The Tracklet Evidence panel reads annotations but does not add a new annotation workflow.
- Real YOLO26 runtime/assets remain unavailable in this repo state.

## Tests Run

- `.venv/bin/python -m pytest tests/test_tracklet_evidence_bundle.py tests/test_tracklet_builder.py -q`
- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- Local media/detection/frame-artifact/tracklet smoke path with a generated temporary video.
- Browser validation against `http://127.0.0.1:3000/runs/<tracklet_run_id>`.

## Validation Results

- Focused evidence bundle and tracklet tests: 11 passed.
- Full pytest suite: 44 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: 0 vulnerabilities.
- Alembic SQLite upgrade smoke test: passed.
- Synthetic viewer smoke script: passed.
- Local evidence path smoke: indexed media, ran fixture detection, extracted 2 frame artifacts, built 3 tracklet candidates, and loaded a bundle with 4 track points, 4 source detections, 2 frame artifacts, 4 `tracked_from` rows, and 4 `grouped_from` rows.
- Browser validation: passed. The tracklet builder run loaded the Tracklet Evidence panel, selected a tracklet candidate, displayed track point candidates, displayed source detection evidence, and showed `tracked_from` / `grouped_from` lineage labels without fetch errors.

## Non-Goals Preserved

- No new tracking algorithm was added.
- No pose detection was added.
- No court homography was added.
- No bounce detection was added.
- No hit detection was added.
- No rally or point reconstruction was added.
- No scoring was added.
- No real YOLO runtime integration was added.
- No adjudication was added.

## Recommended Next Handoff

Recommended next milestone: Milestone 2C - Tracklet Query and Review.

Reason: cross-run tracklet evidence is now inspectable. The next useful step is making candidate tracklets easier to search, compare, annotate, and review without adding model certainty.

If YOLO26 runtime/assets become available first, Milestone 2C could instead be Real YOLO Runtime Completion.
