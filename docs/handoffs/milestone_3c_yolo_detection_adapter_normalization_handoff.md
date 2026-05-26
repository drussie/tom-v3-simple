# Milestone 3C Handoff - YOLO Detection Adapter Normalization Foundation

## Summary

Milestone 3C adds normalization for YOLO-like frame outputs.

It converts fake/serialized boxes into TOM v3-compatible detection payloads and adapter results without loading a real model or persisting detections.

## Completed

- Class-name and class-id mapping.
- `xyxy` to bbox/center conversion.
- Confidence validation and warnings.
- Unmapped class accounting.
- Invalid bbox handling.
- Normalized detection payload dataclasses.
- Adapter result conversion.
- YOLO adapter skeleton normalization methods.
- Tests and docs.

## Important Boundary

3C does not run full-media inference and does not write observations.

## Recommended Next Handoff

```text
Milestone 3D - YOLO Frame Inference / Observation Persistence
```
