# TOM v3 Simple - Milestone 1E Agent Report

## Summary

Status: complete.

Milestone 1E adds frame artifact extraction so persisted detection observations can be inspected over extracted frame imagery. The worker can extract frame images from indexed media, persist shared and detection-targeted `evidence_artifact` rows, and the viewer displays matching frame images behind the existing persisted bbox overlay when artifacts are available.

## Files Created

- `apps/worker/services/frame_artifacts.py`
- `docs/agent_reports/milestone_1e_detection_artifact_frame_extraction_foundation_report.md`
- `docs/handoffs/milestone_1e_detection_artifact_frame_extraction_foundation_handoff.md`
- `docs/media/frame_artifacts_v0.md`
- `docs/milestones/milestone_1e_detection_artifact_frame_extraction_foundation.md`
- `docs/web/frame_artifact_overlay_v0.md`
- `packages/video/tom_v3_video/frame_extract.py`
- `tests/test_frame_artifacts.py`

## Files Modified

- `Makefile`
- `README.md`
- `apps/api/routers/artifacts.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/DetectionOverlayCanvas.tsx`
- `apps/web/src/components/DetectionOverlayPanel.tsx`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/lib/detections.ts`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/api/backend_api_v0.md`
- `docs/dev/local_demo_runbook.md`
- `docs/media/media_indexing_v0.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/web/detection_overlay_viewer_v0.md`
- `docs/web/visual_evidence_viewer_v0.md`
- `packages/video/tom_v3_video/__init__.py`

## Frame Extraction Decisions

- Frame extraction lives in `tom_v3_video.frame_extract`.
- Extraction uses `ffmpeg` and seeks by timestamp derived from `frame_to_timestamp_ms(media_asset.fps, frame_number)`.
- Missing `ffmpeg` raises a clear actionable error.
- Existing frame image files are reused unless `--overwrite` is supplied.
- No fake frame image is created when extraction fails.

## Artifact Storage Decisions

- Local frame images are stored under `.data/artifacts/media/{media_id}/frames/`.
- One shared `frame_image` artifact is written per extracted frame.
- One targeted `detection_frame_image` artifact is written per target detection observation on that frame.
- Artifact metadata records frame number, timestamp, frame-time owner, extraction method/version, source media path, output path, image format, placeholder status, and checksum.
- Binary image data is not stored in the database.

## Viewer Integration Decisions

- The viewer uses existing `GET /viewer/runs/{run_id}` artifact metadata.
- A local development route, `GET /artifacts/{artifact_id}/content`, serves extracted frame files.
- The detection overlay first prefers artifacts targeted to the selected observation.
- It falls back to same-frame `frame_image` / `detection_frame_image` artifacts.
- Bboxes continue to come from persisted detection observations, not image analysis in the viewer.

## Fallback Behavior Decisions

- If no frame artifact exists, the coordinate canvas remains visible.
- The viewer explicitly says when it is showing the coordinate canvas because no frame image artifact is available.
- Missing media dimensions still produce a safe unavailable state.

## Known Limitations

- Artifact content serving is local-development only.
- No production object storage, CDN, or auth layer is implemented.
- No automatic extraction for every video frame is implemented.
- No video player overlay is implemented.
- Real YOLO26 runtime/assets remain unavailable in this repo state.

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
- Local frame artifact extraction smoke with `extract-frame-artifacts`
- Browser validation against `http://127.0.0.1:3000/runs/<DETECTION_RUN_ID>`

## Validation Results

- Pytest: 33 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Local media/detection/frame extraction smoke: extracted 2 frame images and persisted 8 frame artifact rows.
- Viewer payload smoke: returned 8 frame artifacts, including 2 shared artifacts and 6 targeted artifacts.
- Browser validation: frame artifact image loaded behind the overlay with natural width 160, 3 bboxes rendered on the selected frame, and artifact metadata visible in the side panel.

## Non-Goals Preserved

- No real YOLO inference was added.
- No tracking was added.
- No pose detection was added.
- No court homography was added.
- No bounce detection was added.
- No hit detection was added.
- No rally or point reconstruction was added.
- No scoring was added.
- No production object storage was added.
- No adjudication was added.

## Recommended Next Handoff

Recommended next milestone: Milestone 1F - Tracklet Foundation from Persisted Detections, unless YOLO26 runtime/assets become available and the user chooses to prioritize real detector integration.

Reason: frame-backed detection inspection is now available. If real YOLO remains unavailable, the next observation-platform step is explicitly-approved temporal grouping from persisted detections.
