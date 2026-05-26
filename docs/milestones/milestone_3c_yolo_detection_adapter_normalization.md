# Milestone 3C - YOLO Detection Adapter Normalization Foundation

## Status

Status: complete

## Mission

Normalize YOLO-like output into TOM v3-compatible detection payloads without real model inference or persistence.

The target flow is:

```text
YOLO-like result object
-> class mapping
-> bbox/center/confidence normalization
-> TOM v3 detection payloads
-> persistence-ready adapter result
```

## Implemented

- `tom_v3_model_adapters.yolo_normalization`.
- `NormalizedYoloDetection`.
- `YoloNormalizationResult`.
- `normalize_yolo_frame_result`.
- `normalize_yolo_results`.
- `build_detection_adapter_result_from_normalized`.
- YOLO adapter skeleton normalization methods.
- Tests for class mapping, bbox conversion, invalid input, summary counts, and adapter result compatibility.

## Out of Scope

- real YOLO inference
- persisted YOLO detections
- tracklet generation
- pose
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

## Next

Recommended next milestone:

```text
Milestone 3D - YOLO Frame Inference / Observation Persistence
```
