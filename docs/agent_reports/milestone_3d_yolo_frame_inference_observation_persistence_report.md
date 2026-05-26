# Milestone 3D Agent Report - YOLO Frame Inference / Observation Persistence

## Summary

Milestone 3D adds the first frame-level YOLO inference bridge into TOM v3 observation persistence. YOLO-style frame outputs now pass through provider interfaces, 3C normalization, and the existing worker detection adapter service to persist atomic `ball_detection` and `player_detection` observations.

The base environment still does not require Ultralytics, Torch, OpenCV, real weights, CUDA, or MPS.

## Files Created

- `packages/model_adapters/tom_v3_model_adapters/yolo_inference.py`
- `tests/test_yolo_frame_inference.py`
- `docs/model_adapters/yolo_frame_inference_persistence_v0.md`
- `docs/milestones/milestone_3d_yolo_frame_inference_observation_persistence.md`
- `docs/handoffs/milestone_3d_yolo_frame_inference_observation_persistence_handoff.md`
- `docs/agent_reports/milestone_3d_yolo_frame_inference_observation_persistence_report.md`

## Files Modified

- `packages/model_adapters/tom_v3_model_adapters/detection.py`
- `packages/model_adapters/tom_v3_model_adapters/__init__.py`
- `apps/worker/services/detection_adapter.py`
- `apps/worker/cli.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/model_adapters/yolo_detection_normalization_v0.md`
- `docs/model_adapters/yolo_model_registry_weights_v0.md`
- `docs/blueprints/tom_v3_blueprint_3_real_model_runtime_yolo_observation_adapter.md`

## Frame Inference Decisions

Frame inference is frame-first rather than video-stream-first.

The adapter samples explicit frame numbers from indexed media metadata and derives timestamps through TOM v3 frame/time utilities. This preserves the Milestone 1A invariant that media indexing owns frame/time.

## Provider / Fake-Provider Decisions

The provider boundary has two implementations:

- `FakeYoloResultProvider` for deterministic tests and base-environment persistence coverage.
- `UltralyticsYoloResultProvider` behind guarded imports for optional local real runtime use.

Ultralytics result objects are converted into the serialized frame-result shape before normalization.

## Persistence Decisions

The YOLO adapter returns the existing `DetectionAdapterResult` shape.

The worker service persists YOLO-origin detections through the same `ObservationWriter` path as fixture detections. Payloads include bbox, center, label, confidence, class metadata, `source_runtime`, model registry id, weights sha256, inference settings, and `frame_time_owner = media_indexing`.

No tracklets are created inside the YOLO adapter.

## Failure Behavior Decisions

Missing runtime, missing weights, checksum mismatch, missing model registry, device errors, model load errors, prediction errors, or frame decoding errors fail clearly.

If the worker run has already started, run and step metadata record the error and no detection observations are persisted. The YOLO path does not fall back to fixture detections.

## Tests Run

- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`
- `python scripts/smoke_synthetic_viewer_data.py`
- `python -m apps.worker.cli yolo-runtime-probe`

## Validation Results

- Python tests: passed, `100 passed`.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: passed with `0 vulnerabilities`.
- Alembic smoke: passed on SQLite temp database.
- Synthetic viewer smoke: passed with `"ok": true`.
- YOLO runtime probe: command completed without crashing and reported optional packages unavailable in the base environment with install guidance.

## Known Limitations

- Real local Ultralytics smoke was not made a CI requirement.
- Frame loading for real runtime uses a simple OpenCV source, not optimized streaming.
- The adapter does not copy or archive raw YOLO outputs as large artifacts.
- Real YOLO quality depends on local weights and class mapping supplied outside git.

## Non-Goals Preserved

- No YOLO tracking mode.
- No tracklet generation inside YOLO.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 3E - Real YOLO Runtime Local Smoke / Viewer Validation.
