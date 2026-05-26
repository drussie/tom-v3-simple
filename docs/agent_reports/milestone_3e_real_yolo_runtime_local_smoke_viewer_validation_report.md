# Milestone 3E Agent Report - Real YOLO Runtime Local Smoke / Viewer Validation

## Summary

Milestone 3E adds a safe optional real-YOLO local smoke foundation. It provides a smoke helper service, worker CLI command, script wrapper, tests, and docs for validating runtime probe, weights registration, media indexing, YOLO detection persistence, frame artifacts, viewer overlay, and optional tracklet compatibility.

## Files Created

- `apps/worker/services/real_yolo_smoke.py`
- `scripts/smoke_real_yolo_local.py`
- `tests/test_real_yolo_smoke.py`
- `docs/model_adapters/yolo_real_runtime_smoke_v0.md`
- `docs/milestones/milestone_3e_real_yolo_runtime_local_smoke_viewer_validation.md`
- `docs/handoffs/milestone_3e_real_yolo_runtime_local_smoke_viewer_validation_handoff.md`
- `docs/agent_reports/milestone_3e_real_yolo_runtime_local_smoke_viewer_validation_report.md`

## Files Modified

- `apps/worker/cli.py`
- `Makefile`
- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/dev/local_demo_runbook.md`
- `docs/model_adapters/yolo_runtime_environment_v0.md`
- `docs/model_adapters/yolo_model_registry_weights_v0.md`
- `docs/model_adapters/yolo_detection_normalization_v0.md`
- `docs/model_adapters/yolo_frame_inference_persistence_v0.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/web/detection_overlay_viewer_v0.md`
- `docs/tracklets/tracklet_foundation_v0.md`
- `docs/tracklets/tracklet_evidence_bundle_v0.md`
- `docs/blueprints/tom_v3_blueprint_3_real_model_runtime_yolo_observation_adapter.md`

## Smoke Flow Decisions

The smoke helper supports a `--plan-only` mode that requires no runtime packages or local assets. The executable path probes runtime first, validates weights, registers the model, indexes media, runs `--adapter yolo`, extracts frame artifacts when detections exist, and optionally runs the tracklet builder.

## Runtime / Weights Validation Decisions

Missing optional runtime packages produce structured `status = skipped` output. Missing weights and missing media also skip before creating runs or observations. The smoke path never falls back to fixture detections.

## Viewer Validation Decisions

No new viewer feature was added. YOLO-origin detections persist as ordinary atomic detection observations, so the existing detection overlay and frame artifact image layer remain the validation surface.

## Tracklet Compatibility Decisions

Tracklet compatibility is optional in the smoke helper through `--run-tracklets`. Tracklets are built only after a detection run and only by the existing tracklet builder.

## Tests Run

- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`
- `python scripts/smoke_synthetic_viewer_data.py`
- `python -m apps.worker.cli yolo-runtime-probe`
- `python -m apps.worker.cli smoke-real-yolo-local --plan-only`
- `python scripts/smoke_real_yolo_local.py --plan-only`
- `python -m apps.worker.cli smoke-real-yolo-local --source-path /tmp/missing.mp4 --weights-path model_assets/yolo/missing.pt`

## Validation Results

- Python tests: passed, `106 passed`.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: passed with `0 vulnerabilities`.
- Alembic smoke: passed on SQLite temp database.
- Synthetic viewer smoke: passed with `"ok": true`.
- YOLO runtime probe: command completed without crashing and reported optional packages unavailable in the base environment.
- Smoke plan-only command: passed through both worker CLI and script wrapper.
- Missing-runtime smoke command: returned structured `status = skipped` and `skip_reason = yolo_runtime_unavailable`.

## Known Limitations

- Real YOLO runtime smoke is local-only and depends on user-supplied weights/media.
- Default CI does not install Ultralytics, Torch, or OpenCV.
- The smoke helper does not download models.
- The smoke helper does not guarantee detections; output depends on model/video/classes.

## Non-Goals Preserved

- No YOLO tracking mode.
- No tracklets inside YOLO.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No production GPU worker.
- No remote or automatic weights download.
- No adjudication.

## Recommended Next Handoff

Milestone 3F - Blueprint 3 Completion Review / Real Model Runtime Hardening.
