# Milestone 3B Handoff - YOLO Model Registry and Weights Validation

## Summary

Milestone 3B adds local YOLO weights validation and model registry registration without running inference.

## Completed

- Weights validation with safe roots, suffix checks, size checks, sha256, and optional required checksum.
- Default ball/player class mapping and validation.
- Optional model metadata probe when Ultralytics is available.
- Model registry helper that stores YOLO runtime, task, weights, class map, runtime probe, and milestone metadata.
- Worker command `register-yolo-model`.
- Tests and docs.

## Important Boundary

3B does not create processing runs or observations.

Real YOLO detection normalization and persistence should begin only after model weights are registered and runtime configuration is explicit.

## Recommended Next Handoff

```text
Milestone 3C - YOLO Detection Adapter Normalization Foundation
```
