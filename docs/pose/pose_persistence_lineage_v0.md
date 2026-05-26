# Pose Persistence and Lineage v0

## Purpose

Milestone 4C connects normalized pose payloads to durable TOM v3 observations.

The worker pose service creates a pose processing run, persists normalized fixture pose evidence through `ObservationWriter`, and records lineage to source subject evidence when a candidate source is supplied.

This remains observation evidence only. It does not run real pose inference or interpret movement.

## Worker Service

Location:

```text
apps/worker/services/pose_adapter.py
```

Primary entrypoint:

```text
run_pose_adapter(...)
```

The service:

- loads the indexed media asset
- creates a fixture pose model registry row when needed
- creates a pose runtime config
- creates a `processing_run`
- creates a `processing_step`
- normalizes fixture pose frame results with the 4B pose normalizer
- writes `observation_family = pose` spine rows
- writes typed `pose_observation` rows
- writes source-context lineage rows when supplied
- marks run and step completed or failed

## CLI

Worker command:

```bash
python -m apps.worker.cli run-pose-adapter \
  --media-id <media_id> \
  --adapter fixture \
  --frame-sample-rate 30 \
  --max-frames 3
```

Linked source detection mode:

```bash
python -m apps.worker.cli run-pose-adapter \
  --media-id <media_id> \
  --adapter fixture \
  --source-detection-run-id <detection_run_id> \
  --link-source-detections \
  --max-frames 3
```

The CLI returns:

- `pose_run_id`
- `processing_step_id`
- `pose_observation_count`
- `lineage_count`
- `model_id`
- `runtime_config_id`
- persisted pose observation ids

## Observation Writes

Each persisted pose has:

```text
observation_family = pose
observation_type = player_pose_observation
granularity = frame
coordinate_space = image_pixels
frame_time_owner = media_indexing
```

The observation payload stores a compact pose summary:

- skeleton format/version
- keypoint count and present/missing count
- keypoint confidence summary
- pose confidence
- bbox context
- subject association candidate fields
- source runtime `fixture_pose`
- `normalization_only = true`
- lineage summary

The typed `pose_observation` row stores full keypoint JSON and source association fields.

## Source Detection Lineage

When a normalized pose contains `subject_detection_observation_id`, the service validates that the source exists and is a `player_detection` observation.

It then writes:

```text
parent_observation_id = source player_detection observation
child_observation_id = pose observation
relationship_type = pose_from_subject_detection_candidate
```

For source-detection-linked fixture mode:

```text
pose.frame_number = source_detection.frame_start
pose.timestamp_ms = source_detection.timestamp_start_ms
```

## Tracklet Context Lineage

When a pose includes a candidate tracklet context:

```text
relationship_type = subject_context_candidate
```

When a pose includes a candidate track point context:

```text
relationship_type = pose_from_track_point_candidate
```

Explicit invalid source ids fail clearly. The service does not create placeholder source rows.

## Unassociated Fixture Poses

Full-frame fixture poses default to:

```text
subject_ref_type = none
association_status = unassociated
association_method = full_frame_pose
```

These poses may have no lineage. That is expected for unassociated full-frame evidence.

## Viewer Use

Milestone 4D makes persisted pose rows visible in the existing Evidence Viewer:

- pose rows appear in the observation list and timeline
- COCO17 keypoints and skeleton edges render from persisted image-pixel coordinates
- selected pose detail shows keypoint summary and bbox context
- source association candidate fields are displayed when present
- existing lineage panels still show persisted `observation_lineage` rows

The viewer displays candidate source context. It does not identify a player or interpret movement.

## Non-Goals

- No real pose inference.
- No pose model loading.
- No movement interpretation.
- No serve, hit, split-step, or biomechanics conclusions.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.
