# Milestone 3A Handoff - YOLO Runtime Environment / Runtime Probe Foundation

## Summary

Milestone 3A starts Blueprint 3 by adding a safe optional YOLO runtime boundary.

The base TOM v3 environment remains lightweight. Real YOLO dependencies are optional and documented through `requirements-yolo.txt`.

## Completed

- Blueprint 3 doc created.
- Optional YOLO dependency file added.
- Runtime probe implemented.
- Device resolver implemented.
- Worker `yolo-runtime-probe` command added.
- Missing dependency diagnostics are structured and actionable.
- Model weight ignore rules added.
- Tests cover mocked runtime availability and device resolution.
- Docs explain `tom_v3_yolo` setup and the weights policy.

## Important Boundary

Milestone 3A does not run real YOLO inference and does not persist real YOLO detections.

The next milestone should validate model registry/weights metadata before real inference writes observations.

## Recommended Next Handoff

```text
Milestone 3B - YOLO Model Registry and Weights Validation
```
