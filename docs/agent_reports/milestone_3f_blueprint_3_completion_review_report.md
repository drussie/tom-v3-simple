# Milestone 3F Agent Report - Blueprint 3 Completion Review / Real Model Runtime Hardening

## Summary

Milestone 3F closes Blueprint 3 with a completion review, invariant audit, documentation cleanup, runbook clarification, validation pass, and next-blueprint recommendation.

No new inference behavior was added.

## Files Created

- `docs/blueprints/tom_v3_blueprint_3_completion_review.md`
- `docs/milestones/milestone_3f_blueprint_3_completion_review.md`
- `docs/handoffs/milestone_3f_blueprint_3_completion_review_handoff.md`
- `docs/agent_reports/milestone_3f_blueprint_3_completion_review_report.md`

## Files Modified

- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/dev/local_demo_runbook.md`
- `docs/blueprints/tom_v3_blueprint_3_real_model_runtime_yolo_observation_adapter.md`
- `docs/model_adapters/yolo_runtime_environment_v0.md`
- `docs/model_adapters/yolo_model_registry_weights_v0.md`
- `docs/model_adapters/yolo_detection_normalization_v0.md`
- `docs/model_adapters/yolo_frame_inference_persistence_v0.md`
- `docs/model_adapters/yolo_real_runtime_smoke_v0.md`
- `docs/model_adapters/detection_adapter_v0.md`
- `docs/web/detection_overlay_viewer_v0.md`
- `docs/tracklets/tracklet_foundation_v0.md`
- `docs/tracklets/tracklet_evidence_bundle_v0.md`

## Blueprint 3 Completion Verdict

Blueprint 3 is complete.

It proves that TOM v3 can safely introduce optional real YOLO / Ultralytics runtime, keep the base environment lightweight, validate and register local weights, normalize YOLO-like outputs, persist YOLO-origin detection observations through the existing detection pipeline, validate the local smoke/viewer path, and keep Blueprint 2 tracklet/review/export contracts unchanged.

## Invariant Audit Results

The audit found that existing 3A-3E tests cover the requested runtime, registry, normalization, persistence, failure, smoke, and viewer invariants.

No new code-path tests were added because no uncovered behavior gap was found.

Key coverage:

- Runtime probe and device resolver: `tests/test_yolo_runtime.py`
- Weights validation and model registry: `tests/test_yolo_model_registry.py`
- Normalization and class mapping: `tests/test_yolo_normalization.py`
- YOLO frame persistence and failure behavior: `tests/test_yolo_frame_inference.py`
- Real local smoke planning and skip behavior: `tests/test_real_yolo_smoke.py`

## Runtime / Weights Validation Results

Blueprint 3 preserves a strict optional-runtime boundary:

- base `tom_v3` does not require Ultralytics, Torch, or OpenCV;
- `tom_v3_yolo` remains optional;
- model weights are ignored by git;
- local weights are validated and fingerprinted before registration;
- checksum mismatches and unsafe paths fail before registry creation;
- real detection runs require registered weights or an explicit model path;
- failed YOLO runs do not fall back to fixture detections.

## Smoke / Runbook Validation Results

The runbook now describes the complete Blueprint 3 local path:

```text
tom_v3_yolo setup
-> yolo-runtime-probe
-> register-yolo-model
-> index-media
-> run-detection-adapter --adapter yolo
-> extract-frame-artifacts
-> open viewer
-> optional build-tracklets
-> evidence bundle / review / export
```

Real local YOLO smoke remains optional and skipped gracefully when runtime packages, weights, or sample media are unavailable.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `git diff --check`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `.venv/bin/python -m apps.worker.cli yolo-runtime-probe`
- `.venv/bin/python -m apps.worker.cli smoke-real-yolo-local --plan-only`

## Validation Results

- Python tests: passed, `106 passed`.
- Ruff: passed.
- Whitespace check: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: passed with `0 vulnerabilities`.
- Alembic SQLite smoke upgrade: passed.
- Synthetic viewer smoke: passed with `"ok": true`.
- YOLO runtime probe: command completed without crashing and reported optional packages unavailable in the base environment.
- Smoke plan-only command: passed and returned the expected observation-only / no-fallback warning fields.

Note: bare `pytest` on this host resolves to an old system Python 3.8 entrypoint with a plugin mismatch, so validation used the repo virtualenv explicitly. This is the same test suite and avoids host-global pytest contamination.

## Non-Goals Preserved

- No YOLO tracking mode.
- No tracklets inside the YOLO adapter.
- No pose.
- No court homography.
- No bounce or hit detection.
- No rally, point, or scoring.
- No production GPU worker.
- No remote or automatic weights download.
- No adjudication.

## Known Limitations

- Real local YOLO validation depends on user-supplied runtime packages, weights, and sample media.
- CI intentionally remains lightweight and does not install YOLO runtime packages.
- Real model output quality depends on local weights and class mapping.
- Frame-level inference is not optimized streaming inference.

## Recommended Next Blueprint

Blueprint 4 - Pose Observation / Movement Evidence Layer.

Pose should remain outside Blueprint 3 and should use the same observation-only design: model outputs are persisted as evidence, not adjudicated results.
