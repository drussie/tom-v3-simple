# TOM v3 Simple - Milestone 1D Agent Report

## Summary

Status: complete.

Milestone 1D adds the first visual overlay layer for persisted ball/player detection observations. The existing viewer now extracts bbox payloads from `ball_detection` and `player_detection` atomic observations, renders them on an image-pixel coordinate panel, highlights the selected detection, and keeps the existing detail, lineage, artifact, and annotation panels synchronized with the selected observation.

## Files Created

- `apps/web/src/components/DetectionLegend.tsx`
- `apps/web/src/components/DetectionOverlayCanvas.tsx`
- `apps/web/src/components/DetectionOverlayPanel.tsx`
- `apps/web/src/lib/detections.ts`
- `docs/agent_reports/milestone_1d_detection_overlay_visual_observation_layer_report.md`
- `docs/handoffs/milestone_1d_detection_overlay_visual_observation_layer_handoff.md`
- `docs/milestones/milestone_1d_detection_overlay_visual_observation_layer.md`
- `docs/web/detection_overlay_viewer_v0.md`
- `tests/test_detection_overlay_contract.py`

## Files Modified

- `README.md`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/viewerData.ts`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/web/visual_evidence_viewer_v0.md`

## Overlay Data Decisions

- Detection overlay data is derived only from persisted viewer payload observations.
- Overlay items are extracted from `atomic` observations with `observation_type` of `ball_detection` or `player_detection`.
- Bbox and center payloads are accepted from either the observation spine payload or the typed atomic payload.
- Observations without bbox payloads are not invented into overlay items; they are counted as missing bbox observations.
- Frame selection uses persisted `frame_start` / `frame_end` values.

## Rendering Decisions

- The overlay uses an honest `image_pixels` coordinate canvas instead of requiring real frame extraction.
- Bboxes are scaled by persisted media `width` and `height`.
- Ball and player detections use distinct bbox styling and label text so color is not the only signal.
- The detection timeline row marks persisted detection frames without treating detections as candidates.

## Selection / Highlighting Decisions

- If the selected observation is a detection, the overlay shows all detections on that frame.
- The selected detection bbox is highlighted.
- Clicking a bbox updates the existing selected observation state.
- Existing detail, lineage, artifact, and annotation panels remain driven by the selected observation.

## Known Limitations

- No real video frame extraction is implemented.
- No video playback overlay is implemented.
- Real YOLO26 runtime/assets are still unavailable in this repo state.
- The overlay visualizes frame-level detections only; it does not create tracks.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- Local media fixture smoke with `index-media`
- Local detection fixture smoke with `run-detection-adapter`
- Viewer payload query smoke for ball/player detections
- Browser validation against `http://127.0.0.1:3000/runs/<DETECTION_RUN_ID>`

## Validation Results

- Pytest: 30 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Local media/detection fixture smoke: produced 2 ball detections and 4 player detections.
- Browser validation: overlay rendered one ball bbox and two player bboxes on the selected frame; clicking a player bbox updated the detail panel.

## Non-Goals Preserved

- No real YOLO inference was added.
- No tracking was added.
- No pose detection was added.
- No court homography was added.
- No bounce detection was added.
- No hit detection was added.
- No rally or point reconstruction was added.
- No scoring was added.
- No adjudication was added.

## Recommended Next Handoff

Recommended next milestone: Milestone 1E - Detection Artifact / Frame Extraction Foundation.

Reason: persisted detection bboxes are now visible on a coordinate canvas. The next high-leverage step is extracting or serving actual frame artifacts so detection observations can be inspected over real imagery without changing the observation-only model.
