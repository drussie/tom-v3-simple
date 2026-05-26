# YOLO Model Registry and Weights v0

## Purpose

Milestone 3B validates local YOLO model weights and records reproducible model metadata before real inference is introduced.

This milestone does not run YOLO inference and does not persist detections.

## Local Weights Policy

Weights are local model assets, not source code.

Allowed local development roots:

```text
model_assets/yolo/
weights/yolo/
```

Allowed suffixes:

```text
.pt
.pth
.onnx
.engine
```

The repo ignores model asset paths and weight formats. Do not commit weights.

## Validation

The validator checks:

- path resolves under an allowed root
- path exists
- path is a file
- file is non-empty
- suffix is supported
- sha256 matches `--required-sha256` when provided

Valid weights produce:

- resolved path
- file size
- sha256
- validation status

Missing, unsafe, empty, directory, unsupported suffix, or checksum-mismatched weights fail clearly.

## Register Weights

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name <model-name> \
  --model-version v0 \
  --device cpu
```

Optional checksum:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name <model-name> \
  --model-version v0 \
  --required-sha256 <EXPECTED_SHA256>
```

## Registry Metadata

The model registry row uses:

```text
model_family = detection
source = tom_v3_model_adapters.yolo_weights
```

`metadata_jsonb` includes:

- `model_runtime = ultralytics`
- `model_task = detect`
- model name/version
- weights path and resolved path
- weights sha256
- weights size bytes
- class map
- optional class names
- runtime package versions from the runtime probe
- optional model metadata probe output
- `blueprint = 3`
- `milestone = 3B`
- `no_detection_persistence = true`

If a row with the same model name, version, weights sha256, and class map already exists, the helper reuses it.

## Default Class Map

Default mapping:

```json
{
  "ball": {
    "source_class_names": ["sports ball", "tennis ball", "ball"],
    "source_class_ids": [],
    "target_observation_type": "ball_detection",
    "target_label": "ball"
  },
  "player": {
    "source_class_names": ["person", "player"],
    "source_class_ids": [],
    "target_observation_type": "player_detection",
    "target_label": "player_unknown"
  },
  "near_player": {
    "source_class_names": ["near_player"],
    "source_class_ids": [],
    "target_observation_type": "player_detection",
    "target_label": "near_player"
  },
  "far_player": {
    "source_class_names": ["far_player"],
    "source_class_ids": [],
    "target_observation_type": "player_detection",
    "target_label": "far_player"
  }
}
```

The class map only describes how future model outputs should normalize into TOM v3 observation types and labels.

It does not infer near/far player status unless the source class explicitly maps that way.

## Optional Metadata Probe

When `--probe-model` is supplied and Ultralytics is available, the helper attempts to load the model metadata enough to capture:

- model class
- task
- class names
- number of classes
- Ultralytics/Torch versions

If runtime packages are unavailable, registration can still proceed with weights identity and class map metadata.

## Future Runtime Config Preview

Future real inference runtime config should include:

```json
{
  "model_registry_id": "<MODEL_REGISTRY_ID>",
  "weights_path": "model_assets/yolo/model.pt",
  "required_sha256": "<sha256>",
  "device": "cpu",
  "imgsz": 640,
  "conf": 0.25,
  "iou": 0.7,
  "max_det": 300,
  "class_mapping": {}
}
```

## Normalization Next Step

Milestone 3C uses this class map to normalize YOLO-like frame results into TOM v3-compatible detection payloads. See:

```text
docs/model_adapters/yolo_detection_normalization_v0.md
```

## Out of Scope

- real YOLO inference
- detection observation persistence
- pose
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication
