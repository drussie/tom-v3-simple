# Milestone 3B Agent Report - YOLO Model Registry and Weights Validation

## Summary

Milestone 3B adds YOLO weights validation and model registry registration. It prepares TOM v3 for future real YOLO detection adapters without running inference, creating processing runs, or persisting detections.

## Files Created

- `packages/model_adapters/tom_v3_model_adapters/yolo_weights.py`
- `apps/worker/services/yolo_model_registry.py`
- `tests/test_yolo_model_registry.py`
- `docs/milestones/milestone_3b_yolo_model_registry_weights_validation.md`
- `docs/handoffs/milestone_3b_yolo_model_registry_weights_validation_handoff.md`
- `docs/agent_reports/milestone_3b_yolo_model_registry_weights_validation_report.md`
- `docs/model_adapters/yolo_model_registry_weights_v0.md`

## Files Modified

- `Makefile`
- `README.md`
- `apps/worker/cli.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/yolo_runtime_environment_v0.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/blueprints/tom_v3_blueprint_3_real_model_runtime_yolo_observation_adapter.md`
- `packages/model_adapters/tom_v3_model_adapters/__init__.py`

## Weights Validation Decisions

The validator accepts local filesystem weights only. It checks allowed roots, supported suffix, file existence, file type, non-empty size, sha256, and optional required sha256.

Default allowed roots are:

- `model_assets/yolo`
- `weights/yolo`

## Model Registry Decisions

Validated weights create or reuse a `model_registry` row with `model_family = detection` and metadata for runtime, task, weights path, sha256, size, class map, runtime probe, optional model probe, Blueprint 3, and Milestone 3B.

No schema migration was needed.

## Class Mapping Decisions

The default class map normalizes sports ball / tennis ball / ball to `ball_detection` and person / player to `player_detection` with `player_unknown` label. Near/far labels are only used when source classes explicitly map to them.

## Runtime / Model Probe Decisions

The optional model metadata probe loads only metadata when Ultralytics is available. If runtime packages are unavailable, registration still works with weights identity and class map metadata.

## Tests Run

- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`
- `python scripts/smoke_synthetic_viewer_data.py`
- `python -m apps.worker.cli yolo-runtime-probe`
- local temp weights `register-yolo-model` smoke

## Validation Results

- `pytest -q`: passed, 79 tests.
- `ruff check .`: passed.
- Web lint/build/audit: passed, 0 reported production vulnerabilities.
- Alembic SQLite smoke upgrade: passed.
- Synthetic viewer smoke: passed.
- Runtime probe: passed in the base environment and reported optional runtime packages unavailable.
- Temp weights registration smoke: passed; created a `model_registry` row with sha256 and file size, and did not run inference.

## Known Limitations

- Real YOLO inference is not implemented.
- The model metadata probe is optional and not required in CI.
- Remote weights, auto-download, and production object storage are out of scope.

## Non-Goals Preserved

- No real detection persistence.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally, point, or scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 3C - YOLO Detection Adapter Normalization Foundation.
