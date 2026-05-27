# Pose Observation Schema v0

## Purpose

Milestone 4A adds first-class pose observation persistence. Milestone 4B adds normalization that can produce `PoseObservationCreate`-compatible payloads from fake or serialized pose frame results. Milestone 4C adds a worker pose processing-run path that persists normalized fixture poses and source candidate lineage.

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

Milestone 4C persists candidate associations to source `player_detection` observations when supplied. Candidate tracklet and track point association fields are supported by the schema and reserved for later fixture/runtime paths.

Source detection linkage uses:

```text
player_detection observation -> player_pose_observation
relationship_type = pose_from_subject_detection_candidate
```

## Queryability

Pose observations are queryable through the existing observation query path by media id, run id, frame range, confidence, family, and type.

Milestone 4E adds pose-specific filters through `POST /pose/query` for:

- frame/time range
- pose confidence range
- missing keypoint count range
- skeleton format
- association status and method
- subject reference type
- source detection, tracklet, and track point candidate ids
- review label

Each query row includes the observation spine, typed pose detail, annotation summary, artifact summary, and evidence bundle URL.

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

## Worker Persistence Compatibility

Worker `run-pose-adapter` writes normalized fixture poses through `ObservationWriter`:

```bash
python -m apps.worker.cli run-pose-adapter --media-id <media_id> --adapter fixture
```

Source-detection-linked fixture mode copies frame/time from source `player_detection` observations and records lineage without proving identity.

## Viewer Compatibility

Milestone 4D exposes typed pose detail through `GET /viewer/runs/{run_id}`.

The Evidence Viewer uses:

- `keypoints_jsonb` for COCO17 keypoint markers
- `skeleton_format` / `skeleton_version` for skeleton display
- bbox fields for optional pose bbox display
- keypoint summary fields for selected pose detail
- subject association candidate fields for source context display

The viewer renders only present keypoints with numeric coordinates. Missing keypoints remain visible in the keypoint table and are not drawn as present markers.

## Review and Export

Milestone 4E uses the existing `human_annotation` table for pose review annotations. Keypoint-level review metadata is stored in annotation payload JSON with fields such as `keypoint_name` and `keypoint_index`.

Pose review dataset export writes TOM-native JSON under `.data/exports/pose/{export_id}/pose_review_dataset.json` and records an `evidence_artifact` row with checksum and export metadata.

## Non-Goals

Pose observations do not infer movement, tennis actions, biomechanics, rally state, point state, or scoring.
