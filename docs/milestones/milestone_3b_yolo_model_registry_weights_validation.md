# Milestone 3B - YOLO Model Registry and Weights Validation

## Status

Status: complete

## Mission

Validate local YOLO weights and register model metadata before real YOLO inference is integrated.

The target flow is:

```text
configured weights path
-> safe path validation
-> sha256/file-size fingerprint
-> optional model metadata probe
-> model_registry row
-> no detections persisted
```

## Implemented

- YOLO weights validation utility.
- Safe local root checks for `model_assets/yolo` and `weights/yolo`.
- sha256 and file-size fingerprinting.
- Required sha256 validation.
- Default ball/player class mapping validation.
- Optional model metadata probe.
- Model registry helper for YOLO detection models.
- Worker command:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name <model-name> \
  --model-version v0
```

## Out of Scope

- real YOLO inference
- detection observation persistence
- pose
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

## Next

Recommended next milestone:

```text
Milestone 3C - YOLO Detection Adapter Normalization Foundation
```
