# Milestone 7A Agent Report - Real YOLO Detection Replay Run

## Summary

Milestone 7A starts Blueprint 7 by adding a real YOLO detection replay run path for indexed media. TOM can now validate optional YOLO runtime/weights, register model metadata, sample indexed frames, persist mapped real model output as atomic detection observations, and print a replay workstation URL using the real detection run id.

The fixture demo path remains unchanged and default validation does not require YOLO weights, GPU, Torch, Ultralytics, OpenCV, or real pose weights.

## Files Created

- `apps/worker/services/real_detection_replay.py`
- `tests/test_real_detection_replay.py`
- `docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md`
- `docs/perception/real_detection_replay_v0.md`
- `docs/milestones/milestone_7a_real_yolo_detection_replay_run.md`
- `docs/handoffs/milestone_7a_real_yolo_detection_replay_run_handoff.md`
- `docs/agent_reports/milestone_7a_real_yolo_detection_replay_run_report.md`

## Files Modified

- `Makefile`
- `README.md`
- `apps/worker/cli.py`
- `apps/worker/services/detection_adapter.py`
- `packages/model_adapters/tom_v3_model_adapters/detection.py`
- `packages/model_adapters/tom_v3_model_adapters/yolo_inference.py`
- `packages/model_adapters/tom_v3_model_adapters/yolo_normalization.py`
- `tests/test_yolo_frame_inference.py`
- `docs/CONTROL_ROOM.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CURRENT_STATE.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OPTIONAL_YOLO.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/REPLAY_WORKSTATION.md`

## Real Detection Command Decisions

The new command is:

```bash
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

It also supports plan-only output, model name/version, required sha256, `imgsz`, confidence, IoU, frame start/end, explicit class-map JSON, debug artifacts, and viewer base URL.

`make real-detection` wraps the command without changing `make demo`.

## Runtime / Weights Decisions

The service reuses existing YOLO runtime probing, device resolution, weights validation, and model registry helpers. Missing media, missing runtime, missing/invalid weights, and invalid class maps return `ok: false` structured errors. The command never falls back to fixture detections.

## Class Mapping Decisions

The default mapping uses the existing Blueprint 3 YOLO class mapping:

- `sports ball`, `tennis ball`, `ball` -> `ball_detection` / `ball`
- `person`, `player` -> `player_detection` / `player_unknown`

The 7A service also accepts shorthand JSON entries using `observation_type` and `label`, then normalizes them into the existing YOLO class-map contract.

Unmapped classes are skipped and counted.

## Persistence Decisions

Real detections persist through the existing detection adapter and `ObservationWriter` path:

- `observation_family = atomic`
- `observation_type = ball_detection | player_detection`
- media-owned frame/time values
- `coordinate_space = image_pixels`
- `model_id` and `runtime_config_id`
- atomic typed detail row
- `real_model_output = true`
- `source_runtime = ultralytics_yolo`
- `model_output_not_truth = true`

Processing run name is `real-yolo-detection-replay`.

## Replay Integration Decisions

No replay UI change was needed. The Blueprint 6 replay workstation already supports `detectionRunId`, `/media/{media_id}/replay-info`, `/replay/overlays`, and `/replay/timeline`. Real detection runs appear as detection runs because they persist the same atomic observation contract.

## Tests Run

Initial focused validation:

```bash
.venv/bin/python -m pytest tests/test_real_detection_replay.py tests/test_yolo_frame_inference.py tests/test_real_yolo_smoke.py tests/test_replay_api.py -q
ruff check apps/worker/services/real_detection_replay.py apps/worker/services/detection_adapter.py apps/worker/cli.py packages/model_adapters/tom_v3_model_adapters/yolo_inference.py packages/model_adapters/tom_v3_model_adapters/yolo_normalization.py tests/test_real_detection_replay.py tests/test_yolo_frame_inference.py
```

Final validation:

```bash
.venv/bin/python -m pytest -q
ruff check .
cd apps/web && npm run lint
cd apps/web && npm run build
cd apps/web && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head
.venv/bin/python scripts/smoke_synthetic_viewer_data.py
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7a_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_7a_fixture_demo.db make completion-audit PYTHON=.venv/bin/python
.venv/bin/python -m apps.worker.cli run-real-detection --media-id media-plan --weights model_assets/yolo/model.pt --plan-only
make real-detection MEDIA_ID=media-plan YOLO_WEIGHTS_PATH=model_assets/yolo/model.pt PYTHON=.venv/bin/python PLAN_ONLY=true MAX_FRAMES=120
```

## Validation Results

- Focused replay/YOLO tests: passed, 42 tests.
- Full Python suite: passed, 189 tests.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo smoke: passed.
- Completion audit on fixture demo DB: passed.
- `run-real-detection --plan-only`: passed.
- `make real-detection ... PLAN_ONLY=true`: passed.

## Optional Real YOLO Smoke Result

Not run. No local YOLO weights were present under `model_assets/` or `weights/`.

## Known Limitations

- Real YOLO detection quality depends on the local model, class mapping, confidence settings, device, and source video.
- 7A does not build tracklets from real detections.
- 7A does not add real pose inference.
- 7A does not add homography, court-space reasoning, stream ingestion, or tennis-event interpretation.

## Non-goals Preserved

No official tennis truth, TOM v2-style adjudication, accepted/rejected event lifecycle, bounce/hit detection, stroke classification, rally/point/scoring, confirmed player identity, confirmed ball path, real pose inference, homography, or stream ingestion was added.

## Push Status

Final branch and tag push status is reported in the assistant handoff after commit and push.

## Recommended Next Handoff

Milestone 7B - Real Detection Overlay Validation in Replay Workstation.
