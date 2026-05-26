# Milestone 4D Agent Report - Pose Overlay Viewer

## Summary

Milestone 4D makes persisted pose observations visually inspectable in the existing Evidence Viewer. The viewer now receives typed pose detail, renders COCO17 keypoint evidence and skeleton edges, shows pose metadata and keypoint confidence rows, and surfaces source association candidate context without adding movement interpretation.

## Files Created

- `apps/web/src/lib/poses.ts`
- `apps/web/src/components/PoseOverlayCanvas.tsx`
- `apps/web/src/components/PoseOverlayPanel.tsx`
- `docs/web/pose_overlay_viewer_v0.md`
- `docs/milestones/milestone_4d_pose_overlay_viewer.md`
- `docs/handoffs/milestone_4d_pose_overlay_viewer_handoff.md`
- `docs/agent_reports/milestone_4d_pose_overlay_viewer_report.md`

## Files Modified

- `apps/api/routers/viewer.py`
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/viewerData.ts`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/components/ObservationDetailPanel.tsx`
- `apps/web/src/app/globals.css`
- `tests/test_pose_persistence_lineage.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/pose/pose_observation_schema_v0.md`
- `docs/pose/pose_persistence_lineage_v0.md`
- `docs/web/detection_overlay_viewer_v0.md`
- `docs/blueprints/tom_v3_blueprint_4_pose_observation_movement_evidence_layer.md`

## Viewer Payload Decisions

The existing `GET /viewer/runs/{run_id}` payload now includes a `pose` detail object for `player_pose_observation` rows. No pose-specific viewer API was added.

## Overlay Rendering Decisions

The pose overlay uses persisted full-frame image-pixel coordinates and media dimensions. Missing keypoints are not drawn. Skeleton edges render only when both endpoint keypoints are present.

## Keypoint/Skeleton Display Decisions

The frontend mirrors the COCO17 skeleton edge list from the schema registry. The selected pose panel shows all 17 keypoint rows, including missing keypoints.

## Source Context Display Decisions

The panel displays persisted source association candidate fields. It does not claim source identity or movement meaning.

## Tests Run

- `.venv/bin/python -m pytest tests/test_pose_persistence_lineage.py -q`
- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- Browser smoke against a fixture pose run at `/runs/<pose_run_id>`

## Validation Results

- `142 passed`
- Ruff passed
- web lint/build passed
- web audit found 0 vulnerabilities
- Alembic upgraded through head on SQLite
- synthetic viewer smoke returned `ok = true`
- browser smoke confirmed Pose Overlay, Keypoint Evidence, `coco17/v1`, missing keypoint text, and unassociated pose context render

## Known Limitations

- No real pose inference.
- No pose review UI.
- No pose export integration.
- No video playback pose overlay.
- Source context displays persisted candidate ids; richer source evidence drill-down remains a future viewer enhancement.

## Non-Goals Preserved

No movement interpretation, tennis-event inference, serve/hit/split-step/biomechanics analysis, homography, bounce, hit, rally, point, score, or adjudication was added.

## Recommended Next Handoff

Milestone 4E - Pose Query / Review / Export Integration.
