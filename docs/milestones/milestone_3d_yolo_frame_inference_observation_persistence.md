# Milestone 3D - YOLO Frame Inference / Observation Persistence

## Status

Status: implemented

## Goal

Connect frame-level YOLO inference output to persisted TOM v3 detection observations without changing downstream query, viewer, artifact, tracklet, review, or export contracts.

## Implemented

- Frame inference provider interface.
- Metadata-only frame source for deterministic fake-provider tests.
- OpenCV frame source for optional real runtime use.
- Fake YOLO result provider for tests.
- Guarded Ultralytics result provider.
- Explicit media-owned frame sampling.
- YOLO adapter `run()` implementation that uses 3C normalization.
- Existing worker detection adapter persistence path for YOLO output.
- `--model-registry-id`, `--iou-threshold`, and `--max-det` worker options.
- Registered model metadata and weights checksum validation before YOLO runs.
- Persisted atomic `ball_detection` and `player_detection` observations from mocked YOLO output.
- Clear failed-run behavior without fixture fallback.
- Docs and tests for the frame inference/persistence path.

## Contract

YOLO frame inference writes the same observation shape as fixture detection:

```text
observation_family = atomic
observation_type = ball_detection | player_detection
granularity = frame
coordinate_space = image_pixels
frame_time_owner = media_indexing
```

Payloads carry bbox, center, label, confidence, class metadata, source runtime, model registry id when supplied, weights sha256 when supplied, and inference settings.

## Non-Goals

- No optimized video-stream inference.
- No YOLO tracking mode.
- No tracklets inside the YOLO adapter.
- No pose.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Validation

Primary validation is through mocked YOLO providers, not real weights:

```bash
pytest -q tests/test_yolo_frame_inference.py
```

Optional local runtime validation requires a separate YOLO environment and registered local weights.
