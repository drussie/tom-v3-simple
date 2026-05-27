# Real Pose Replay v0

## Purpose

Milestone 7D adds an optional real pose replay command for indexed media.

It runs an Ultralytics pose model over media-owned frames or crops from persisted `player_detection` observations, normalizes model keypoints into TOM's COCO17 pose contract, persists `player_pose_observation` rows, and prints a replay workstation URL with `poseRunId`.

Pose output remains keypoint evidence. It is not movement, stroke, biomechanics, court, or tennis-event interpretation.

Milestone 7F closes Blueprint 7 with real detection, real-detection-derived candidate tracklets, and optional real pose replay documented as the final perception ladder. Court/camera/homography evidence remains future Blueprint 8 work.

## Command

Preferred crop-from-player-detection mode:

```bash
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --weights ./model_assets/pose/<pose_model>.pt \
  --source-detection-run-id <real_detection_run_id> \
  --mode crop_from_player_detection \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Full-frame mode is available for runs without a source detection run:

```bash
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --weights ./model_assets/pose/<pose_model>.pt \
  --mode full_frame \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Useful options:

```text
--model-name
--model-version
--required-sha256
--device auto|cpu|mps|cuda
--imgsz
--conf
--iou
--frame-start
--frame-end
--fallback-to-full-frame
--plan-only
--viewer-base-url
```

Makefile helper:

```bash
make real-pose \
  MEDIA_ID=<media_id> \
  SOURCE_DETECTION_RUN_ID=<real_detection_run_id> \
  POSE_WEIGHTS_PATH=./model_assets/pose/<pose_model>.pt \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=120
```

## Output Contract

Successful output includes:

```json
{
  "ok": true,
  "message": "real pose replay run complete",
  "media_id": "...",
  "pose_run_id": "...",
  "source_detection_run_id": "...",
  "model_registry_id": "...",
  "runtime_config_id": "...",
  "observations": {
    "player_pose_observation": 12,
    "total": 12
  },
  "replay_url": "http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<source_detection_run_id>&poseRunId=<pose_run_id>",
  "run_label": "real pose model output run",
  "warnings": {
    "observation_only": true,
    "no_adjudication": true,
    "pose_keypoints_not_movement_interpretation": true,
    "model_output_not_truth": true,
    "no_fixture_fallback": true
  }
}
```

Failures return structured JSON with `ok: false`. Missing runtime, missing weights, missing media, and missing source detection runs in crop mode do not fall back to fixture pose output.

## Runtime And Weights

The real pose path reuses the optional Ultralytics runtime boundary:

- optional runtime probe
- device resolver
- local weight file validation
- sha256 and file size recording
- model registry metadata
- runtime config metadata

Pose weights are local assets and should remain outside git.

The pose model registry row records:

```json
{
  "model_family": "pose",
  "model_runtime": "ultralytics",
  "model_task": "pose",
  "source_runtime": "ultralytics_pose",
  "skeleton_format": "coco17",
  "skeleton_version": "v1",
  "real_model_output": true,
  "model_output_not_truth": true
}
```

## Frame / Time Ownership

Pose inference does not create time.

Crop-from-player-detection mode uses the source detection observation:

```text
source player_detection observation
-> frame_start / timestamp_start_ms
-> crop image
-> pose model output
-> projected full-frame keypoints
-> persisted pose observation at the source media-owned frame/time
```

Full-frame mode samples indexed media frames:

```text
media_asset
-> frame_count / fps / frame_time_index
-> sampled frame_number
-> timestamp_ms
-> frame image
-> pose model output
-> persisted pose observation at that frame/time
```

Persisted pose payloads record:

```json
{
  "frame_time_owner": "media_indexing",
  "source_runtime": "ultralytics_pose",
  "real_model_output": true,
  "model_output_not_truth": true
}
```

## Crop Mode

Crop mode is preferred when a real detection run is available.

For each selected source `player_detection` observation:

```text
player_detection bbox
-> cropped image region
-> pose model
-> crop-local keypoints
-> full-frame image-pixel keypoints
-> player_pose_observation
-> lineage to source player_detection
```

The pose observation keeps subject association candidate metadata:

```json
{
  "subject_ref_type": "player_detection",
  "subject_detection_observation_id": "...",
  "association_status": "candidate",
  "association_method": "crop_from_player_detection"
}
```

Lineage uses:

```text
pose_from_subject_detection_candidate
```

This lineage is provenance. It does not establish player identity, body state, movement, or tennis meaning.

## Persistence

Real pose replay persists through the existing pose observation contract:

- `observation_family = pose`
- `observation_type = player_pose_observation`
- `coordinate_space = image_pixels`
- media-owned frame/time
- `model_id` from the pose `model_registry` row
- `runtime_config_id` from the real pose runtime config
- typed `pose_observation` row
- COCO17 keypoint schema and keypoint rows
- keypoint present/missing counts and confidence summaries
- optional crop projection metadata
- optional source detection association candidate metadata

Processing run name:

```text
real-pose-replay
```

Runtime config name:

```text
real-pose-replay-config
```

## Replay Integration

The Blueprint 6 replay workstation already accepts `poseRunId`.

Open:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&poseRunId=<real_pose_run_id>
```

If real-detection-derived tracklets are available:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<real_pose_run_id>
```

Replay-info pose run summaries can label real pose model-output runs with:

- `evidence_source = real_pose_model_output`
- `source_label = real pose model output`
- `source_runtime = ultralytics_pose`
- model name/version
- model registry id
- runtime config id
- `is_real_model_output = true`

Pose overlay chunks and pose timeline items include the same optional source metadata when available.

Selected pose detail can show source runtime, model registry id, runtime config id, skeleton format/version, keypoint counts, pose confidence, and subject association candidate context.

## Non-goals

7D and 7F do not add movement interpretation, stroke classification, serve detection, split-step analysis, biomechanics conclusions, court/homography evidence, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.
