# Real Detection Replay v0

## Purpose

Milestone 7A adds a real YOLO detection replay command for indexed media.
Milestone 7B validates that the resulting real detection runs are clearly labeled and inspectable in the replay workstation.
Milestone 7C uses those persisted real detections as source observations for candidate tracklet generation.
Milestone 7D can use source `player_detection` observations from the real detection run as crop subjects for real pose replay.
Milestone 7F closes Blueprint 7 with the final perception orchestration path.

It runs optional Ultralytics YOLO detection over media-owned sampled frames, normalizes mapped model outputs into TOM atomic detection observations, persists them through the existing detection adapter path, and prints a replay workstation URL.

The command does not judge model correctness or tennis meaning.

## Command

```bash
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
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
--class-map-json
--plan-only
--viewer-base-url
```

Makefile helper:

```bash
make real-detection \
  MEDIA_ID=<media_id> \
  YOLO_WEIGHTS_PATH=./model_assets/yolo/<model>.pt \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=120
```

## Output Contract

Successful output includes:

```json
{
  "ok": true,
  "message": "real YOLO detection replay run complete",
  "media_id": "...",
  "detection_run_id": "...",
  "model_registry_id": "...",
  "runtime_config_id": "...",
  "observations": {
    "ball_detection": 0,
    "player_detection": 0,
    "total": 0
  },
  "replay_url": "http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<run_id>",
  "stream_proxy_replay_url": "http://127.0.0.1:3000/replay/<media_id>?mode=stream_proxy&detectionRunId=<run_id>",
  "run_label": "real YOLO detection run",
  "warnings": {
    "observation_only": true,
    "no_adjudication": true,
    "model_output_not_truth": true
  }
}
```

Failures return structured JSON with `ok: false`. Missing runtime, missing weights, missing media, and invalid class maps do not fall back to fixture detections.

## Frame / Time Ownership

YOLO does not create time.

Frame sampling is owned by indexed media metadata:

```text
media_asset
-> frame_count / fps / frame_time_index
-> sampled frame_number
-> timestamp_ms
-> frame image
-> YOLO model output
-> persisted observation at that frame/time
```

The runtime config records:

```json
{
  "frame_sampling": {
    "mode": "every_n_frames",
    "every_n_frames": 1,
    "frame_start": null,
    "frame_end": null,
    "max_frames": 120
  },
  "frame_time_owner": "media_indexing"
}
```

## Class Mapping

Default mapped classes:

```json
{
  "person": {
    "observation_type": "player_detection",
    "label": "player_unknown"
  },
  "sports ball": {
    "observation_type": "ball_detection",
    "label": "ball"
  },
  "tennis_ball": {
    "observation_type": "ball_detection",
    "label": "ball"
  },
  "ball": {
    "observation_type": "ball_detection",
    "label": "ball"
  },
  "player": {
    "observation_type": "player_detection",
    "label": "player_unknown"
  }
}
```

Unmapped classes are skipped and counted in the summary. The command does not infer near/far player role, player identity, ball path, or tennis events.

## Persistence

Mapped detections persist through the existing detection adapter path:

- `observation_family = atomic`
- `observation_type = ball_detection | player_detection`
- `coordinate_space = image_pixels`
- media-owned `frame_start`, `frame_end`, `timestamp_start_ms`, and `timestamp_end_ms`
- `model_id` from `model_registry`
- `runtime_config_id` from the real detection runtime config
- atomic typed detail row
- payload flags `real_model_output = true`, `source_runtime = ultralytics_yolo`, and `frame_time_owner = media_indexing`

Processing run name:

```text
real-yolo-detection-replay
```

Runtime config name:

```text
real-yolo-detection-replay-config
```

## Replay Integration

The Blueprint 6 replay workstation already accepts `detectionRunId`.

Open:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>
```

The detection overlay endpoint and timeline lane read the persisted atomic detection observations. No new replay UI capability is required for 7A.

Milestone 7B adds replay metadata that helps operators distinguish real model output from fixture demo evidence:

- replay-info detection run summaries include `evidence_source`, `source_label`, `source_runtime`, model metadata, runtime config id, and boolean `is_fixture` / `is_real_model_output` flags when available
- detection overlay payloads include optional source/runtime/model/config/class metadata
- detection timeline labels include the source label
- selected detection detail in the replay workstation shows model/runtime/config/class fields when present

Example real detection run metadata:

```json
{
  "run_name": "real-yolo-detection-replay",
  "evidence_source": "real_model_output",
  "source_label": "real model output",
  "source_runtime": "ultralytics_yolo",
  "is_fixture": false,
  "is_real_model_output": true
}
```

Example fixture detection run metadata:

```json
{
  "evidence_source": "fixture_demo",
  "source_label": "fixture evidence",
  "is_fixture": true,
  "is_real_model_output": false
}
```

These fields are operational display metadata. They do not alter the persisted observation contract and do not make model output official tennis meaning.

## Real Detection-Derived Tracklets

After a real detection run exists, build candidate tracklets from it with the existing tracklet builder:

```bash
.venv/bin/python -m apps.worker.cli build-tracklets \
  --detection-run-id <real_detection_run_id> \
  --run-name real-detection-tracklet-candidates
```

The command output includes a replay URL with both run ids:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<tracklet_run_id>
```

Tracklet runs derived from real model-output detections preserve:

- source detection run id
- source detection evidence source
- source runtime
- source detection observation ids on track points
- `tracked_from` lineage from detection observations to track point candidates
- `grouped_from` lineage from track point candidates to tracklet candidates

These tracklets are candidate temporal groupings. They do not establish player identity, ball path correctness, tennis events, or scoring.

## Real Pose Replay From Source Player Detections

After a real detection run exists, run real pose replay in crop mode:

```bash
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <real_detection_run_id> \
  --weights ./model_assets/pose/<pose_model>.pt \
  --mode crop_from_player_detection \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

The command output includes a replay URL with `poseRunId`:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&poseRunId=<pose_run_id>
```

Crop-mode pose observations preserve:

- source detection run id
- source player detection observation id
- source detection confidence as association context when available
- `pose_from_subject_detection_candidate` lineage from the detection observation to the pose observation
- full-frame image-pixel COCO17 keypoints
- `source_runtime = ultralytics_pose`

These pose observations are keypoint evidence only. They do not interpret movement, strokes, biomechanics, court position, tennis events, or scoring.

## Non-goals

7A/7B/7C/7D/7F do not add movement interpretation, stroke classification, homography, court-space reasoning, stream ingestion, live model scheduling, bounce/hit/rally/point/scoring, or adjudication.

Court/camera/homography evidence is deferred to Blueprint 8.
