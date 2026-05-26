# TOM v3 Simple - Milestone 1C Agent Report

## Summary

Status: complete.

Milestone 1C implements the TOM v3 detection adapter interface, fixture detector, YOLO unavailable stub, worker detection adapter service, CLI commands, persistence tests, query tests, viewer payload tests, and documentation. The fixture adapter writes `ball_detection` and `player_detection` atomic observations through the existing `ObservationWriter`.

## Files Created

- `apps/worker/services/detection_adapter.py`
- `docs/agent_reports/milestone_1c_yolo26_ball_player_observation_adapter_report.md`
- `docs/handoffs/milestone_1c_yolo26_ball_player_observation_adapter_handoff.md`
- `docs/milestones/milestone_1c_yolo26_ball_player_observation_adapter.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/model_adapters/yolo26_detection_adapter_assessment.md`
- `packages/model_adapters/tom_v3_model_adapters/detection.py`
- `tests/test_detection_adapter.py`

## Files Modified

- `Makefile`
- `README.md`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/dev/local_demo_runbook.md`
- `docs/media/media_indexing_v0.md`
- `packages/model_adapters/README.md`
- `packages/model_adapters/tom_v3_model_adapters/__init__.py`
- `packages/schema/tom_v3_schema/enums.py`

## YOLO26 Portability Assessment

YOLO26 runtime/assets are not available in this repo/environment.

Ultralytics is not installed in `.venv`, and no TOM v3-managed YOLO26 ball/player model file was found in this repo. Milestone 1C therefore does not claim real YOLO inference.

## Adapter Interface Decisions

The adapter seam lives in `tom_v3_model_adapters.detection`.

The interface is intentionally narrow:

- `DetectionAdapterInput`
- `DetectionObservation`
- `DetectionAdapterResult`
- `BaseDetectionAdapter`

Adapter output is detection evidence only. Persistence remains owned by TOM v3 worker services and `ObservationWriter`.

## Fixture Adapter Decisions

The fixture adapter deterministically samples indexed frames and emits:

- one ball-like detection
- one near-player-like detection
- one far-player-like detection

It supports `frame_sample_rate` and `max_frames`. It exists for tests and development and is clearly marked as fixture output, not real detection.

## YOLO Adapter Decisions

`YoloDetectionAdapter` exists as an explicit unavailable stub. It checks for Ultralytics and model path availability and raises a clear error when either is missing.

## Persistence Decisions

The detection adapter service creates:

- `runtime_config`
- `model_registry`
- `processing_run`
- `processing_step`
- `observation`
- `atomic_observation`

If a gameplay run is supplied, detection observations are lineage-linked to overlapping gameplay/view-state observations using `scoped_by`.

## Worker / API Decisions

Worker commands were added:

- `run-detection-adapter`
- `index-and-run-detection`

No API endpoint was added in 1C. Detection runs are worker-driven for now, using the same service the API could call later.

## Tests Run

Passed:

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `npm run lint` in `apps/web`
- `npm run build` in `apps/web`
- `npm audit --omit=dev` in `apps/web`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- generated a temporary 1-second MP4 with ffmpeg and ran `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_detection_adapter.db .venv/bin/python -m apps.worker.cli index-media --source-path tmp_detection_smoke/sample.mp4 --storage-root .data/media`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_detection_adapter.db .venv/bin/python -m apps.worker.cli run-gameplay-adapter --media-id 17271fa4-f5a1-4746-8720-37b2063080c6 --adapter fixture`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_detection_adapter.db .venv/bin/python -m apps.worker.cli run-detection-adapter --media-id 17271fa4-f5a1-4746-8720-37b2063080c6 --adapter fixture --frame-sample-rate 5 --max-frames 2 --gameplay-run-id 6315ae72-9f66-4855-b550-ca957f475975 --output-debug-artifact`
- queried `ball_detection` and `player_detection` observations for detection run `8bcfd1b5-454e-410d-898d-ad576298d8b2`
- inspected `build_viewer_run_payload` for detection run `8bcfd1b5-454e-410d-898d-ad576298d8b2`

## Validation Results

- Backend tests: 29 passed.
- Ruff: passed.
- Web lint/build/audit: passed with 0 production dependency vulnerabilities.
- Alembic SQLite smoke test: passed.
- Synthetic viewer smoke: passed.
- Real media indexing smoke: passed.
- Fixture gameplay adapter smoke: passed.
- Fixture detection adapter smoke: passed.
- Detection query inspection returned 2 `ball_detection` rows and 4 `player_detection` rows.
- Viewer payload inspection returned detection observation types and 6 debug artifact metadata rows.

## Known Limitations

- Real YOLO26 integration is not complete because runtime/assets are unavailable.
- Fixture output is deterministic and metadata-driven; it is not model inference.
- No API trigger was added for detection runs.
- No overlay renderer was added in 1C.
- No tracking, pose, homography, bounce, hit, rally, or point logic is present.

## Non-Goals Preserved

- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No streaming ingestion.
- No production deployment.
- No adjudication.

## Recommended Next Handoff

Milestone 1D - Detection Overlay / Visual Observation Layer.

Reason: detection observations are now persisted, queryable, and available in the viewer payload. The next useful step is displaying bbox evidence visually without adding tracking or higher-level interpretation.
