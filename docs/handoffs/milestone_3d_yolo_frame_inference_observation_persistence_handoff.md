# Milestone 3D Handoff - YOLO Frame Inference / Observation Persistence

## Starting State

Blueprints 1 and 2 are complete. Milestone 3C added YOLO-like output normalization but did not run frame inference or persist YOLO detections.

## Completed Work

Milestone 3D adds the first narrow YOLO frame inference bridge:

```text
indexed media
-> sampled media-owned frames
-> fake or real YOLO result provider
-> 3C normalization
-> DetectionAdapterResult
-> existing detection persistence
-> atomic ball/player observations
```

The adapter uses registered model metadata when supplied through `--model-registry-id`, validates registered weights and checksum before running, and persists mocked YOLO outputs through the same worker service as fixture detections.

## Important Files

- `packages/model_adapters/tom_v3_model_adapters/yolo_inference.py`
- `packages/model_adapters/tom_v3_model_adapters/detection.py`
- `apps/worker/services/detection_adapter.py`
- `apps/worker/cli.py`
- `tests/test_yolo_frame_inference.py`
- `docs/model_adapters/yolo_frame_inference_persistence_v0.md`

## Validation Focus

Use mocked providers in CI. Real Ultralytics, Torch, OpenCV, CUDA/MPS, and model weights remain optional.

Required checks:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
python -m apps.worker.cli yolo-runtime-probe
```

## Next Suggested Milestone

Milestone 3E - Real YOLO Runtime Local Smoke / Viewer Validation.

## Boundary

No YOLO tracking mode, no pose, no homography, no bounce/hit detection, no rally/point/scoring, and no adjudication were added.
