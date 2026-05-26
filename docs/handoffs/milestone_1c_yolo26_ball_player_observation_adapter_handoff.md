# TOM v3 Simple - Milestone 1C Handoff

## Summary

Milestone 1C adds the ball/player detection adapter seam and the first persisted detection adapter path.

YOLO26/Ultralytics runtime and TOM v3-managed model assets were not available in this repo/environment, so the milestone uses:

- `BaseDetectionAdapter` as the TOM v3 contract
- `FixtureDetectionAdapter` for deterministic dev/test output
- `YoloDetectionAdapter` as a clear unavailable runtime/assets stub
- worker service and CLI commands that persist atomic observations through `ObservationWriter`

## Implemented

- `packages/model_adapters/tom_v3_model_adapters/detection.py`
- `apps/worker/services/detection_adapter.py`
- `python -m apps.worker.cli run-detection-adapter`
- `python -m apps.worker.cli index-and-run-detection`
- tests in `tests/test_detection_adapter.py`
- detection adapter docs and YOLO26 portability assessment

## Core Contract

Ball/player detections are observations.

Each detection writes:

- `observation_family=atomic`
- `observation_type=ball_detection` or `player_detection`
- `granularity=frame`
- media/run/model/config ids
- frame and timestamp scope
- confidence
- coordinate space `image_pixels`
- typed `atomic_observation`

Media indexing owns frame/time. The fixture adapter derives timestamps from indexed media FPS using TOM v3 video utilities.

## Worker Commands

Run detection on indexed media:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

Index and run:

```bash
python -m apps.worker.cli index-and-run-detection \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

With gameplay scope:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --gameplay-run-id <GAMEPLAY_RUN_ID>
```

## YOLO Integration Status

Real YOLO26 integration remains blocked until Ultralytics/runtime support and TOM v3-managed model assets are supplied.

See:

```text
docs/model_adapters/yolo26_detection_adapter_assessment.md
```

## Recommended Next Handoff

Milestone 1D - Detection Overlay / Visual Observation Layer.

If real YOLO assets become available first, an alternate handoff can complete `YoloDetectionAdapter.run()` without changing the TOM v3 persistence contract.
