# Milestone 4B - Pose Adapter Normalization Foundation

## Status

Status: complete

## Purpose

Milestone 4B makes fake or serialized pose model output compatible with TOM v3's pose observation schema.

## Result

The repo now has:

- pose normalization module
- fake/serialized pose frame result input contract
- COCO17 keypoint normalization using the 4A skeleton registry
- missing keypoint preservation
- keypoint summary computation
- bbox normalization with explicit invalid-bbox behavior
- confidence handling and warnings
- crop-local to full-frame projection
- subject association candidate passthrough
- pose adapter result skeleton
- tests for normalization, warnings, adapter diagnostics, and `PoseObservationCreate` compatibility

## Flow

```text
fake / serialized pose model output
-> COCO17 skeleton validation
-> normalized keypoint evidence
-> bbox / crop / subject context
-> PoseObservationCreate-compatible payload
-> PoseAdapterResult
```

## Non-Goals

- No real pose inference.
- No pose model loading.
- No pose observation worker pipeline.
- No pose overlay viewer.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Next Milestone

Recommended next milestone:

```text
Milestone 4C - Pose Observation Persistence and Lineage
```
