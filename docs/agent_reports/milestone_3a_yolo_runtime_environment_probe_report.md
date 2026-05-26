# Milestone 3A Agent Report - YOLO Runtime Environment / Runtime Probe Foundation

## Summary

Milestone 3A starts Blueprint 3 with an optional YOLO runtime environment foundation. The base `tom_v3` environment remains clean; YOLO dependencies are optional, probed at runtime, and documented for a separate `tom_v3_yolo` environment.

## Files Created

- `requirements-yolo.txt`
- `packages/model_adapters/tom_v3_model_adapters/yolo_runtime.py`
- `tests/test_yolo_runtime.py`
- `docs/blueprints/tom_v3_blueprint_3_real_model_runtime_yolo_observation_adapter.md`
- `docs/milestones/milestone_3a_yolo_runtime_environment_probe.md`
- `docs/handoffs/milestone_3a_yolo_runtime_environment_probe_handoff.md`
- `docs/model_adapters/yolo_runtime_environment_v0.md`
- `docs/agent_reports/milestone_3a_yolo_runtime_environment_probe_report.md`

## Files Modified

- `.gitignore`
- `Makefile`
- `apps/worker/cli.py`
- `packages/model_adapters/tom_v3_model_adapters/__init__.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/detection_adapter_v0.md`

## Environment Strategy Decisions

The base environment does not require Ultralytics, Torch, or OpenCV. YOLO runtime dependencies live in `requirements-yolo.txt` for a separate optional `tom_v3_yolo` environment.

## Runtime Probe Decisions

`probe_yolo_runtime()` safely imports optional runtime packages inside the probe call, reports structured availability diagnostics, and returns `status = unavailable` when optional packages or requested devices are missing.

## Device Resolver Decisions

`resolve_yolo_device()` supports `auto`, `cpu`, `mps`, `cuda`, `cuda:0`, and `0`. Auto prefers CUDA, then MPS when allowed, then CPU. Explicit unavailable GPU/MPS requests raise `YoloDeviceUnavailable`.

## Dependency / Weights Policy

Model weights remain outside git. `.gitignore` now excludes `model_assets/`, `weights/`, `*.pt`, `*.pth`, `*.onnx`, and `*.engine`.

## Tests Run

- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`
- `python scripts/smoke_synthetic_viewer_data.py`
- `python -m apps.worker.cli yolo-runtime-probe`
- `make yolo-runtime-probe PYTHON=.venv/bin/python`

## Validation Results

- `pytest -q`: passed, 65 tests.
- `ruff check .`: passed.
- Web lint/build/audit: passed, 0 reported production vulnerabilities.
- Alembic SQLite smoke upgrade: passed.
- Synthetic viewer smoke: passed.
- Base environment YOLO runtime probe: passed without crashing; reported optional packages unavailable and resolved `auto` to `cpu`.
- Makefile YOLO runtime probe wrapper: passed.

## Known Limitations

- Real YOLO inference is not implemented in 3A.
- YOLO model weights are not validated yet.
- Torch installation remains platform-specific for CUDA/MPS.

## Non-Goals Preserved

- No real detection persistence.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally, point, or scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 3B - YOLO Model Registry and Weights Validation.
