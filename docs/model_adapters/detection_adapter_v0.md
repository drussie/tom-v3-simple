# TOM v3 Simple - Detection Adapter v0

## Purpose

Detection Adapter v0 is the TOM v3 interface for ball/player detector output.

It turns detector output into persisted atomic observations:

```text
indexed media_asset
-> optional gameplay scope
-> detection adapter
-> ball_detection / player_detection observations
-> ObservationWriter
-> query API and viewer observation list/detail
```

Ball/player detections are observations. They are not tracking, identity assignment, bounce detection, or adjudication.

## Package

Adapter interface:

```text
packages/model_adapters/tom_v3_model_adapters/detection.py
```

Worker persistence service:

```text
apps/worker/services/detection_adapter.py
```

## Adapter Contract

Primary classes:

- `DetectionAdapterInput`
- `DetectionObservation`
- `DetectionAdapterResult`
- `BaseDetectionAdapter`
- `FixtureDetectionAdapter`
- `YoloDetectionAdapter`

Adapter input includes:

- media id
- source URI
- local path when available
- FPS
- frame count
- duration
- width and height
- runtime config payload
- frame/time summary from media indexing
- optional gameplay segments
- media metadata

Adapter output includes:

- adapter name and version
- detection observations
- optional artifact metadata
- diagnostics

## Frame/Time Rule

Media indexing owns frame/time.

Detection adapters must use indexed media FPS, frame count, duration, and frame/time summary. Every detection observation stores `frame_start`, `frame_end`, `timestamp_start_ms`, and `timestamp_end_ms` derived from TOM v3 media metadata.

## Fixture Adapter

`FixtureDetectionAdapter` is deterministic and development-only.

For sampled frames, it emits:

- one `ball_detection`
- one near-player-like `player_detection`
- one far-player-like `player_detection`

It supports:

- `frame_sample_rate`
- `max_frames`

The fixture payload marks itself as fixture output and includes `frame_time_owner: media_indexing`.

## YOLO Adapter Stub

`YoloDetectionAdapter` exists behind the same interface but intentionally raises a clear unavailable error when the runtime or model file is unavailable.

The current repo/environment does not contain:

- Ultralytics package
- YOLO26 model weights
- known ball/player model path

See:

```text
docs/model_adapters/yolo26_detection_adapter_assessment.md
```

## YOLO Runtime Probe

Milestone 3A adds an optional runtime environment probe without enabling real inference.

The base `tom_v3` environment does not require Ultralytics, Torch, or OpenCV. Optional runtime dependencies live in:

```text
requirements-yolo.txt
```

Probe the current environment:

```bash
python -m apps.worker.cli yolo-runtime-probe
```

The probe reports:

- Ultralytics availability/version
- Torch availability/version
- OpenCV availability/version
- CUDA availability
- MPS availability
- requested and resolved device
- missing optional packages

See:

```text
docs/model_adapters/yolo_runtime_environment_v0.md
```

Real YOLO detection persistence remains out of scope until a future Blueprint 3 milestone supplies validated model weights and runtime configuration.

Milestone 3B supplies the validated model weights and registry foundation, but still does not run inference:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name <model-name> \
  --model-version v0
```

The command creates or reuses a `model_registry` row with weights fingerprint and class map metadata. It does not create a `processing_run` or any detection observations.

## Persistence

The worker service creates:

- `runtime_config`
- `model_registry`
- `processing_run`
- `processing_step`
- one `observation` row per detection
- one typed `atomic_observation` row per detection

Ball detections write:

- `observation_family=atomic`
- `observation_type=ball_detection`
- `atomic_kind=ball_detection`
- `coordinate_space=image_pixels`

Player detections write:

- `observation_family=atomic`
- `observation_type=player_detection`
- `atomic_kind=player_detection`
- `coordinate_space=image_pixels`

Atomic payload includes:

- bbox
- center
- class label
- class id
- detector metadata
- `frame_time_owner=media_indexing`

If a gameplay run is supplied, detections are linked to overlapping gameplay/view-state observations with `scoped_by` lineage.

## Worker Commands

Run fixture detection on indexed media:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --frame-sample-rate 30 \
  --max-frames 5
```

Index a local file and run fixture detection:

```bash
python -m apps.worker.cli index-and-run-detection \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

Use a gameplay scope:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --gameplay-run-id <GAMEPLAY_RUN_ID>
```

The command prints:

- media id
- run id
- model id
- runtime config id
- processing step id
- detection count
- counts by label
- counts by observation type
- observation ids

## Query Examples

Query balls:

```json
{
  "run_id": "<DETECTION_RUN_ID>",
  "observation_type": "ball_detection"
}
```

Query players by confidence:

```json
{
  "run_id": "<DETECTION_RUN_ID>",
  "observation_type": "player_detection",
  "confidence_gte": 0.5
}
```

## Viewer Compatibility

The existing viewer route works unchanged:

```text
GET /viewer/runs/{run_id}
```

Detection observations appear in the observation list and detail panel with atomic payload JSON.

Milestone 1D adds visual overlay support for persisted detection observations. The viewer reads bbox payloads from `observation.payload_jsonb` or `observation.atomic.payload_jsonb`, scales them by media dimensions, and renders them in an `image_pixels` coordinate panel.

Milestone 1E adds optional frame artifact extraction. Extracted `frame_image` and `detection_frame_image` artifacts can be displayed behind the same persisted bbox overlay.

Milestone 2A adds candidate tracklet grouping from persisted detection observations. The tracklet builder consumes a detection run and writes tracklet/track point candidate observations plus tracklet/track point rows without mutating detection observations.

The overlay is a visual evidence layer only. It does not create temporal groupings, infer events, or alter the persisted observations.

## Out of Scope

- tracking
- pose detection
- court homography
- bounce detection
- hit detection
- rally segmentation
- point reconstruction
- production deployment
