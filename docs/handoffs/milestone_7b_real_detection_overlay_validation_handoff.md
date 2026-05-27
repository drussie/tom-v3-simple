# TOM v3 - Milestone 7B Handoff

## Real Detection Overlay Validation in Replay Workstation

Repo: `drussie/tom-v3-simple`

Branch: `codex/m7b-real-detection-overlay-validation`

Starting state: Milestone 7A Real YOLO Detection Replay Run accepted and merged to `main`.

## Mission

Validate and polish real detection replay in the workstation.

The target operator question is:

```text
Am I looking at fixture demo evidence or actual model output from the video?
```

7B answers this with replay-info source metadata, clearer detection run labels, detection overlay payload metadata, selected detection detail fields, and tests that do not require local YOLO weights.

## Required Boundary

Use evidence language:

- real model output
- detection observation
- real YOLO detection run
- fixture detection run
- model-output evidence
- model registry
- runtime config
- source runtime
- frame/time owner

Do not add tennis-event interpretation, real pose inference, homography, real stream ingestion, or tracklets from real detections.

## Validation Checklist

- Default Python tests pass without YOLO weights.
- Replay-info labels real detection runs as real model-output evidence.
- Fixture detection runs remain fixture/demo evidence.
- Detection overlays expose source/runtime/model/config/class metadata when available.
- Selected detection detail shows that model output is evidence only.
- Fixture demo and completion audit still pass.
- Optional real YOLO smoke is run only if local weights exist.

## Recommended Next Handoff

Milestone 7C - Real Detection Tracklet Generation.
