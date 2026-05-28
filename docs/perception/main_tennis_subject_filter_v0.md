# Main Tennis Player Subject Filter v0

This document describes the TOM v3 main tennis-player subject filter.

The filter is a candidate selection layer:

```text
real player_detection observations
-> main_tennis_subject_filter_v0
-> main_player_subject_candidate observations
-> optional real pose crop mode
```

It does not confirm identity. It does not mutate raw detections. It does not decide tennis events.

## Purpose

TOM v1 player/object detection can emit many `player_detection` observations in a broadcast frame, including tennis players, ball kids, line judges, chair-side people, and background spectators.

Running pose inference on every human-like detection creates noisy replay evidence. The filter selects at most two pose source candidates per frame:

- `near_player_candidate`
- `far_player_candidate`

These are `main_player_subject_candidate` observations under the existing observation spine. They are candidate subject evidence only.

## Observation Contract

Each selected candidate is persisted as:

```text
observation_family = tracking
observation_type = main_player_subject_candidate
granularity = frame
coordinate_space = image_pixels
```

The payload includes:

```json
{
  "subject_role_candidate": "near_player_candidate",
  "source_detection_observation_id": "...",
  "source_detection_run_id": "...",
  "frame_number": 0,
  "timestamp_ms": 0,
  "selection_method": "main_tennis_subject_filter_v0",
  "selection_score": 0.82,
  "selection_features": {
    "bbox_area_ratio": 0.05,
    "bbox_center_x": 0.49,
    "bbox_center_y": 0.72,
    "court_region_hint": "near_court_center"
  },
  "candidate_subject_only": true,
  "not_identity_truth": true,
  "observation_only": true,
  "no_adjudication": true,
  "raw_detection_not_mutated": true
}
```

## Lineage

The filter writes lineage:

```text
player_detection
-> main_player_subject_candidate
relationship_type = main_subject_candidate_from_player_detection
```

When real pose consumes a subject run, pose lineage becomes:

```text
player_detection
-> player_pose_observation
relationship_type = pose_from_subject_detection_candidate

main_player_subject_candidate
-> player_pose_observation
relationship_type = pose_from_main_subject_candidate
```

This preserves the raw source detection and the selection step without promoting either into truth.

## Heuristic v0

The v0 filter uses image-relative bounding box features:

- bbox center x/y
- bbox area ratio
- source detection confidence
- central-court preference
- near-player lower-half preference
- far-player upper/mid-court preference
- edge penalties
- tiny-box exclusion

Thresholds are stored in runtime config so future versions can tune them without changing persisted raw detections.

## CLI

```bash
.venv/bin/python -m apps.worker.cli select-main-player-subjects \
  --media-id <media_id> \
  --source-detection-run-id <player_detection_run_id> \
  --run-name main-player-subject-filter-v0 \
  --max-frames 214 \
  --frame-start 0 \
  --frame-end 214
```

The command outputs a `main_subject_run_id`.

## Pose Integration

Filtered pose mode:

```bash
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <player_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --weights model_assets/tom_v1/yolo26x-pose.pt \
  --model-name tom-v1-yolo26x-pose \
  --model-version v1-local \
  --mode crop_from_player_detection \
  --imgsz 640 \
  --allowed-root model_assets/tom_v1
```

If `--source-subject-run-id` is omitted, the previous broad crop-from-player-detection behavior remains available.

## Boundaries

The filter does not add:

- confirmed player identity
- tennis-event interpretation
- bounce/hit/in-out logic
- court-space projection
- accepted/rejected lifecycle
- mutation or deletion of raw detections

Raw `player_detection` observations remain persisted and inspectable.
