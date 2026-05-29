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

Usable through the TOM v1 court keypoint adapter:

- `model_assets/tom_v1/keypoints_model.pth`

Requires future TOM v1-specific adapters:

- `model_assets/tom_v1/view_classifier_gameplay.pt`

Do not force `.pth` court keypoint or gameplay classifier assets through the YOLO detector path unless compatibility is proven. The court keypoint model is handled by `tom-v1-court-keypoints-probe` and `run-real-court-keypoints`.

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

This helper uses `best_ball_v2_1280.pt`, passes `--allowed-root model_assets/tom_v1`, and defaults to `--imgsz 1280`.

Player/object detection:

```bash
make tom-v1-player-detection \
  MEDIA_ID=<media_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=1 \
  YOLO_DEVICE=auto
```

This helper uses `yolo26x.pt`, passes `--allowed-root model_assets/tom_v1`, and defaults to `--imgsz 640`.

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

This helper uses `yolo26x-pose.pt`, passes `--allowed-root model_assets/tom_v1`, and defaults to `--imgsz 640`.

Court keypoint probe:

```bash
make tom-v1-court-keypoints-probe PYTHON=.venv/bin/python
```

Real court keypoints:

```bash
make tom-v1-court-keypoints \
  MEDIA_ID=<media_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=30
```

This helper uses `keypoints_model.pth`, passes `--allowed-root model_assets/tom_v1`, and writes real model-output `court_keypoint_observation` rows plus derived `court_line_observation` candidates when enough keypoints are present. The recognized TOM v1 keypoint state dict uses fixed 224x224 preprocessing and records requested image size as runtime metadata.

Main tennis-player subject filtering:

```bash
make tom-v1-main-subjects \
  MEDIA_ID=<media_id> \
  DETECTION_RUN_ID=<player_real_detection_run_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214
```

This helper selects at most two `main_player_subject_candidate` observations per frame: `near_player_candidate` and `far_player_candidate`. These are pose source candidates only, not identity truth.

Main player track assignment:

```bash
make tom-v1-main-player-tracks \
  MEDIA_ID=<media_id> \
  DETECTION_RUN_ID=<player_real_detection_run_id> \
  SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214
```

This helper groups frame-local subject candidates into `near_player_track_candidate` and `far_player_track_candidate` visual track candidates, with per-frame `main_player_track_assignment_candidate` evidence. These are still not identity truth.

The current assignment method is `main_player_track_assignment_v01`. It uses simple persistent-lock checks, rejects large jumps or edge/wall candidates, and may leave assignment gaps rather than passing an implausible subject to pose.

Pose from selected main subject candidates:

```bash
make tom-v1-pose-main-subjects \
  MEDIA_ID=<media_id> \
  SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> \
  SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214
```

Filtered pose mode preserves lineage from raw `player_detection` rows to `main_player_subject_candidate` rows and then to `player_pose_observation` rows.

Pose from main player track candidates:

```bash
make tom-v1-pose-main-tracks \
  MEDIA_ID=<media_id> \
  SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> \
  SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> \
  SOURCE_TRACK_RUN_ID=<main_player_track_run_id> \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=214
```

Track-filtered pose mode preserves track assignment metadata on pose observations, including `track_candidate_id`, `track_role_candidate`, and `track_assignment_observation_id`. It remains candidate visual subject evidence only.

Replay can show these track assignments with:

```text
/replay/<media_id>?detectionRunId=<player_detection_run_id>&trackletRunId=<player_tracklet_run_id>&subjectRunId=<main_subject_run_id>&mainPlayerTrackRunId=<main_player_track_run_id>&poseRunId=<track_filtered_pose_run_id>
```

The visible `NEAR TRACK` and `FAR TRACK` labels are candidate visual track labels. They are not player names, identity truth, or accepted tracks.

## Runtime / Replay Repair Notes

The TOM v3 real detection and real pose runtime bridge must omit optional Ultralytics arguments when they are unset. In particular, `imgsz`, `iou`, and `max_det` should not be forwarded as `None` because some Ultralytics versions treat `None` as an invalid explicit value rather than an omitted option.

The replay workstation also has visual display modes for dense real detection and tracklet runs:

- Current only
- Short trail
- Full trail

These modes only affect what is shown on screen. They do not change persisted observations, candidate tracklets, pose observations, or evidence-only semantics.

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
