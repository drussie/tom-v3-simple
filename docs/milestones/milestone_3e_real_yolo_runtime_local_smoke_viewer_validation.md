# Milestone 3E - Real YOLO Runtime Local Smoke / Viewer Validation

## Status

Status: implemented

## Goal

Create a safe, optional local smoke path for real YOLO runtime validation without requiring YOLO dependencies or weights in the default test suite.

## Implemented

- Local smoke helper service.
- Worker CLI command `smoke-real-yolo-local`.
- Script wrapper `scripts/smoke_real_yolo_local.py`.
- Plan-only mode for docs and dry runs.
- Structured skip behavior for missing runtime or missing weights.
- Real smoke sequence for runtime probe, model registration, media indexing, YOLO detection, frame artifact extraction, and optional tracklet building.
- Tests for smoke plan and skip behavior without real Ultralytics or weights.
- Runbook and model-adapter docs for viewer validation and Blueprint 2 compatibility.

## Smoke Command

```bash
python -m apps.worker.cli smoke-real-yolo-local --plan-only
```

When local runtime assets are available:

```bash
python -m apps.worker.cli smoke-real-yolo-local \
  --source-path <sample_video_path> \
  --weights-path model_assets/yolo/<weights_file>.pt \
  --model-name local-yolo-smoke \
  --model-version local-v0 \
  --device cpu \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --run-tracklets
```

## Non-Goals

- No YOLO tracking mode.
- No tracklet generation inside YOLO.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No production GPU worker.
- No remote or automatic weight download.
- No adjudication.
