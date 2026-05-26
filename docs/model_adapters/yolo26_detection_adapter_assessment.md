# TOM v3 Simple - YOLO26 Detection Adapter Assessment

## Summary

Status: YOLO26 integration is not available in this repo/environment.

Milestone 1C therefore implements:

- a TOM v3 detection adapter interface
- a deterministic fixture detector for tests and development
- a `YoloDetectionAdapter` integration stub with a clear unavailable error
- docs describing what is needed for real YOLO/Ultralytics integration

It does not claim that real YOLO26 inference is running.

## Is YOLO26 Available?

No YOLO26 model file was found in `drussie/tom-v3-simple`.

Local workstation search found unrelated YOLO sample scripts and generic weights outside this repo, but no TOM v3-managed YOLO26 ball/player detector assets.

## Is Ultralytics Installed?

No. `.venv` does not currently have the `ultralytics` package installed.

## What Model Path Is Required?

Future real integration should accept:

```text
--model-path /path/to/yolo26-ball-player.pt
```

The model path should be recorded in:

- `runtime_config.payload_jsonb.model_path`
- `model_registry.metadata_jsonb.model_path`
- `model_registry.metadata_jsonb.weights_path`

## Is A Ball Model Available?

No TOM v3 ball model is available in this repo state.

## Is A Player Model Available?

No TOM v3 player model is available in this repo state.

## Combined Or Separate Detectors?

Recommended integration mode: start with one combined detector if available.

Expected class map:

```json
{
  "0": "ball",
  "1": "player"
}
```

If separate models are supplied later, keep the same TOM v3 adapter output contract and record model details in metadata.

## Runtime Input

The YOLO adapter should accept:

- local video path or extracted frames
- model path
- device
- image size
- confidence threshold
- frame sample rate
- max frames
- optional gameplay scope

## Runtime Output

The adapter must map runtime output to `DetectionObservation` values:

- label
- frame number
- timestamp
- confidence
- bbox
- center
- class id
- class label
- metadata

## GPU Requirement

Unknown for YOLO26 assets. TOM v3 should support CPU/MPS/CUDA configuration through runtime config, but 1C does not add runtime execution.

## Can It Run On CPU/MPS For Development?

Unknown until a real model and Ultralytics runtime are supplied.

The intended CLI surface already exposes:

```text
--device
--image-size
--confidence-threshold
```

## Class Mapping

Future YOLO output should map to TOM v3 observation types:

- `ball` -> `ball_detection`
- `player`, `near_player`, `far_player`, `player_unknown` -> `player_detection`

The adapter may use metadata to preserve raw class labels and any subject hints.

## Recommended Integration Mode

Keep TOM v3 stable and narrow:

```text
TOM v3 DetectionAdapter interface
-> YOLO/Ultralytics runtime
-> DetectionObservation values
-> ObservationWriter
-> atomic_observation rows
```

Do not make YOLO own persistence.
Do not add tracking in the detector adapter milestone.

## Current Developer Path

Use the fixture adapter:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

The fixture path proves persistence, queryability, and viewer compatibility without representing itself as real YOLO inference.
