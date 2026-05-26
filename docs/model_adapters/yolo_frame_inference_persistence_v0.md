# YOLO Frame Inference Persistence v0

## Purpose

Milestone 3D connects frame-level YOLO-like model output to the existing TOM v3 detection persistence contract.

The path is:

```text
indexed media
-> sampled media-owned frames
-> YOLO result provider
-> YOLO normalization
-> DetectionAdapterResult
-> existing detection persistence service
-> ball_detection / player_detection atomic observations
```

This milestone does not add YOLO tracking mode, tracklet creation inside the adapter, pose, homography, bounce/hit detection, rally/point/scoring, or adjudication.

Milestone 3F closes Blueprint 3 and confirms this persistence path as the completed real-model-runtime contract.

## Frame Ownership

Media indexing owns frame/time.

The YOLO adapter samples explicit frame numbers from indexed `media_asset.frame_count` using `frame_sample_rate` and `max_frames`. Timestamps are derived with TOM v3 frame/time utilities from indexed media FPS.

The adapter does not use model runtime timestamps as the source of TOM v3 frame/time.

## Provider Boundary

Frame inference is behind small provider interfaces:

- `YoloFrameSource`
- `YoloResultProvider`
- `FakeYoloResultProvider`
- `UltralyticsYoloResultProvider`

The fake provider is for deterministic tests and local contract checks. It does not pretend to be real model inference.

The Ultralytics provider is guarded by optional imports. Base TOM v3 imports do not require Ultralytics, Torch, or OpenCV.

## Real Provider Behavior

When optional runtime packages and registered weights are available, the real provider:

1. resolves the requested device,
2. loads the registered weights,
3. decodes the selected frame,
4. runs one-frame prediction,
5. converts Ultralytics boxes into the normalized frame-result shape,
6. passes the result through the 3C normalization utility.

Ultralytics result objects do not leave the provider boundary.

## Worker Command

Register weights first:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name <model-name> \
  --model-version v0 \
  --device cpu
```

Then run the YOLO adapter on indexed media:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter yolo \
  --model-registry-id <MODEL_REGISTRY_ID> \
  --device cpu \
  --image-size 640 \
  --confidence-threshold 0.25 \
  --iou-threshold 0.7 \
  --max-det 50 \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --output-debug-artifact
```

If runtime packages or weights are unavailable, the command fails clearly and does not fall back to fixture detections.

## Local Smoke Helper

Milestone 3E adds:

```bash
python -m apps.worker.cli smoke-real-yolo-local --plan-only
```

When runtime, weights, and media are available:

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

The helper probes runtime, validates/registers weights, indexes media, runs YOLO detection, extracts frame artifacts when detections exist, and optionally builds tracklets. Missing runtime/assets produce structured skipped output.

## Persisted Payload

Successful YOLO detections persist through the existing detection adapter service as atomic observations:

- `observation_family = atomic`
- `observation_type = ball_detection` or `player_detection`
- `coordinate_space = image_pixels`
- `frame_time_owner = media_indexing`

Payloads include:

- bbox
- center
- label
- confidence
- class id and class label
- `source_runtime = ultralytics_yolo`
- source result index
- model registry id when supplied
- runtime config id
- weights sha256 when supplied
- inference metadata such as image size, confidence threshold, IoU threshold, max detections, and device

The same observations are compatible with the existing detection overlay, frame artifact, tracklet builder, review, and export paths.

## Failure Behavior

The YOLO path fails without writing detection observations when it encounters:

- missing optional runtime packages
- unavailable device
- missing model registry row
- missing weights
- checksum mismatch
- model load failure
- prediction failure
- media local path or frame decode failure
- invalid result shape that cannot normalize into detections

When the worker run has already been created, the run and step are marked failed and the error is recorded in metadata.

## Debug Artifact

When `--output-debug-artifact` is enabled, detection debug artifact metadata includes:

- adapter and version
- bbox and center
- source runtime
- model registry id
- weights sha256
- inference settings
- normalization diagnostics

The debug artifact is intentionally small and does not store massive raw model output.

## Out of Scope

- optimized video-stream inference
- YOLO tracking mode
- tracklet generation inside YOLO
- pose
- court homography
- bounce or hit detection
- rally/point/scoring
- production GPU worker
- remote weight download
- adjudication

## Blueprint 3 Completion

Blueprint 3 completion is documented in:

```text
docs/blueprints/tom_v3_blueprint_3_completion_review.md
```

The completion review confirms that YOLO-origin detections remain normal TOM v3 atomic observations and that downstream viewer, frame artifact, tracklet, review, and export contracts do not require a YOLO-specific branch.
