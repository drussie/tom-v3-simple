# Pose Observation Schema v0

## Purpose

Milestone 4A adds first-class pose observation persistence. Milestone 4B adds normalization that can produce `PoseObservationCreate`-compatible payloads from fake or serialized pose frame results.

Pose observations use the central observation spine plus a typed `pose_observation` row.

## Observation Spine

Each pose observation writes:

```text
observation_family = pose
observation_type = player_pose_observation
granularity = frame
coordinate_space = image_pixels
```

Frame/time fields are media-owned:

```text
frame_start = frame_number
frame_end = frame_number
timestamp_start_ms = timestamp_ms
timestamp_end_ms = timestamp_ms
```

## Typed Row

The typed `pose_observation` row stores:

- media/run ids
- frame number and timestamp
- skeleton format/version
- keypoint schema JSON
- keypoints JSON
- keypoint count and present/missing counts
- mean/min/max keypoint confidence
- pose confidence
- bbox context
- optional crop context
- optional subject association candidate fields
- `frame_time_owner = media_indexing`
- raw model payload metadata

## Keypoint JSON

Persisted keypoints use JSON:

```json
{
  "index": 0,
  "name": "nose",
  "x": 642.3,
  "y": 210.7,
  "x_norm": 0.5018,
  "y_norm": 0.2926,
  "confidence": 0.88,
  "present": true,
  "visibility": null
}
```

Missing keypoints are recorded explicitly:

```json
{
  "index": 10,
  "name": "right_wrist",
  "x": null,
  "y": null,
  "x_norm": null,
  "y_norm": null,
  "confidence": null,
  "present": false,
  "visibility": null
}
```

Missing keypoints are not inferred.

## Subject Association

Milestone 4A supports unassociated pose evidence:

```text
subject_ref_type = none
association_status = unassociated
association_method = full_frame_pose
```

Future milestones may use candidate associations to player detections, tracklets, or track points.

## Queryability

Pose observations are queryable through the existing observation query path by media id, run id, frame range, confidence, family, and type.

Future pose-specific filters may add keypoint missing count, skeleton format, and association status.

## Normalization Compatibility

The Milestone 4B pose normalizer emits the same fields used by this schema:

- COCO17 `keypoints_jsonb`
- keypoint summary counts and confidence statistics
- pose confidence
- bbox fields
- crop fields when crop projection is used
- subject association candidate fields
- raw model payload and normalization metadata

Invalid bbox input does not discard valid keypoints; bbox fields are stored as null and a normalization warning is reported.

## Non-Goals

Pose observations do not infer movement, tennis actions, biomechanics, rally state, point state, or scoring.
