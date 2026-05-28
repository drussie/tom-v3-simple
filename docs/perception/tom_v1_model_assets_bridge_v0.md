# TOM v1 Model Assets Bridge v0

This note defines the local bridge between TOM v1 model assets and TOM v3's observation-only real perception replay paths.

The goal is practical and narrow:

```text
local TOM v1 model files
-> optional TOM v3 real detection / real pose commands
-> persisted observations
-> candidate tracklets when requested
-> replay workstation inspection
```

It does not replace TOM v3 architecture with TOM v1 code, and it does not claim tracking quality is solved.

## Current Reality

TOM v3 replay and evidence infrastructure is working. The replay workstation can display fixture/demo detections, candidate tracklets, pose, court keypoints, court lines, camera/view evidence, homography candidates, and projection diagnostics.

The fixture visual quality is not real tracking quality:

- fixture ball/player overlays are deterministic demo evidence
- fixture court lines are static and can be visually wrong for real footage
- sparse fixture evidence can flicker
- TOM v1 perception assets may perform better on local video than the fixture path

This bridge lets those TOM v1 local assets be tested as TOM v3 observation sources while preserving the TOM v3 evidence contract.

## Local Model Inventory

Expected local files:

```text
model_assets/tom_v1/best_ball_v2_1280.pt          # ball detector
model_assets/tom_v1/keypoints_model.pth           # court keypoints model, future adapter required
model_assets/tom_v1/view_classifier_gameplay.pt   # gameplay classifier, future adapter required
model_assets/tom_v1/yolo26n.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26s.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26x-pose.pt               # pose model
model_assets/tom_v1/yolo26x.pt                    # player/object detector
```

These files are local assets. They must not be committed, uploaded, or treated as source code.

## Guardrails

The repository ignores local model/runtime assets:

```text
model_assets/
*.pt
*.pth
*.onnx
*.engine
*.torchscript
```

No default CI path requires TOM v1 assets, Ultralytics, Torch, OpenCV, or GPU runtime.

## Supported Now

Likely usable through the existing TOM v3 real YOLO detection path:

- `model_assets/tom_v1/best_ball_v2_1280.pt`
- `model_assets/tom_v1/yolo26x.pt`
- `model_assets/tom_v1/yolo26n.pt`
- `model_assets/tom_v1/yolo26s.pt`

Likely usable through the existing TOM v3 real pose path:

- `model_assets/tom_v1/yolo26x-pose.pt`

Requires future TOM v1-specific adapters:

- `model_assets/tom_v1/keypoints_model.pth`
- `model_assets/tom_v1/view_classifier_gameplay.pt`

Do not force `.pth` court keypoint or gameplay classifier assets through the YOLO detector path unless compatibility is proven.

## Runtime Probe

Probe optional runtime support:

```bash
.venv/bin/python -m apps.worker.cli yolo-runtime-probe --device auto
```

Or:

```bash
make tom-v1-yolo-probe PYTHON=.venv/bin/python
```

If the probe reports missing optional packages, install them only in a local optional environment:

```bash
.venv/bin/python -m pip install ultralytics
```

The project also documents the optional YOLO environment in `requirements-yolo.txt`. This remains separate from default CI.

## Smoke Commands

Ball detection:

```bash
make tom-v1-ball-detection \
  MEDIA_ID=<media_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=1 \
  YOLO_DEVICE=auto
```

Player/object detection:

```bash
make tom-v1-player-detection \
  MEDIA_ID=<media_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=1 \
  YOLO_DEVICE=auto
```

Candidate tracklets from one real detection run:

```bash
make tom-v1-tracklets \
  DETECTION_RUN_ID=<real_detection_run_id> \
  PYTHON=.venv/bin/python
```

Pose from the player detection run:

```bash
make tom-v1-pose \
  MEDIA_ID=<media_id> \
  SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=1 \
  YOLO_DEVICE=auto
```

## Class Mapping Risk

The first real issue may be class mapping.

The TOM v1 ball detector may emit:

```text
class 0 = ball
```

The TOM v3 real detection path maps YOLO outputs into `ball_detection` and `player_detection` observations using explicit class-map rules. If a TOM v1 model returns zero useful detections:

1. Lower the confidence threshold.
2. Inspect debug payloads or artifacts if enabled.
3. Check the class names emitted by Ultralytics.
4. Add an explicit class map only if the CLI/runtime output proves the mapping.

Do not relabel unknown classes without evidence.

## Semantics

TOM v1-origin detections and poses are model-output evidence. Candidate tracklets from those detections are candidate temporal groupings.

They do not establish:

- confirmed ball path
- confirmed player identity
- confirmed court position
- bounce/hit/in-out/rally/point/scoring
- official tennis truth
- adjudicated events

The purpose of this bridge is to make better local perception assets testable inside TOM v3's observation/replay system.
