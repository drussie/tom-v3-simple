# Milestone 3C Agent Report - YOLO Detection Adapter Normalization Foundation

## Summary

Milestone 3C adds YOLO-like output normalization. It converts fake or serialized frame-level YOLO boxes into TOM v3-compatible ball/player detection payloads and adapter results without real inference or observation persistence.

## Files Created

- `packages/model_adapters/tom_v3_model_adapters/yolo_normalization.py`
- `tests/test_yolo_normalization.py`
- `docs/milestones/milestone_3c_yolo_detection_adapter_normalization.md`
- `docs/handoffs/milestone_3c_yolo_detection_adapter_normalization_handoff.md`
- `docs/agent_reports/milestone_3c_yolo_detection_adapter_normalization_report.md`
- `docs/model_adapters/yolo_detection_normalization_v0.md`

## Files Modified

- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/blueprints/tom_v3_blueprint_3_real_model_runtime_yolo_observation_adapter.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/model_adapters/yolo_model_registry_weights_v0.md`
- `packages/model_adapters/tom_v3_model_adapters/__init__.py`
- `packages/model_adapters/tom_v3_model_adapters/detection.py`

## Normalization Decisions

Normalization accepts dictionary-shaped frame results with `frame_number`, `timestamp_ms`, and `boxes`. It emits `NormalizedYoloDetection` payloads plus a `YoloNormalizationResult` summary.

## Class Mapping Decisions

Class mapping reuses the Milestone 3B validated class map. Matching works by source class id or normalized, case-insensitive source class name.

Near/far player labels are emitted only when class mapping explicitly targets them.

## Invalid Input Decisions

Unmapped classes are counted and skipped.

Invalid bboxes and non-numeric confidence values are skipped with warnings.

Out-of-range confidence values produce warnings but keep the mapped detection.

No silent bbox clamping is performed.

## Adapter Skeleton Decisions

`YoloDetectionAdapter` now exposes normalization-only methods while `run()` continues to raise the existing unavailable-runtime error. Real inference remains for a later milestone.

## Tests Run

- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`
- `python scripts/smoke_synthetic_viewer_data.py`
- `python -m apps.worker.cli yolo-runtime-probe`
- normalization smoke one-liner with fake YOLO boxes

## Validation Results

- `pytest -q`: passed, 94 tests.
- `ruff check .`: passed.
- Web lint/build/audit: passed, 0 reported production vulnerabilities.
- Alembic SQLite smoke upgrade: passed.
- Synthetic viewer smoke: passed.
- Runtime probe: passed in the base environment and reported optional runtime packages unavailable.
- Normalization smoke: passed; produced one `ball_detection` payload and one `player_detection` payload without inference or persistence.

## Known Limitations

- No real Ultralytics inference.
- No detection persistence from real YOLO outputs.
- Dict-shaped fake/serialized outputs are the supported 3C input contract.

## Non-Goals Preserved

- No persisted YOLO detections.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally, point, or scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 3D - YOLO Frame Inference / Observation Persistence.
