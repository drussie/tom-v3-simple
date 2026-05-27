# Pose Query / Review / Export v0

## Purpose

Milestone 4E makes persisted pose evidence searchable, reviewable, and exportable.

The layer packages pose observations and review evidence for later inspection or training-dataset preparation. It does not interpret movement or tennis events.

## Query

API:

```http
POST /pose/query
```

Worker/service schema:

```text
PoseQueryFilters
```

Supported filters:

- `media_id`
- `run_id`
- `frame_start_gte`
- `frame_end_lte`
- `timestamp_start_gte`
- `timestamp_end_lte`
- `pose_confidence_min`
- `pose_confidence_max`
- `keypoints_missing_count_min`
- `keypoints_missing_count_max`
- `skeleton_format`
- `association_status`
- `association_method`
- `subject_ref_type`
- `subject_detection_observation_id`
- `subject_tracklet_id`
- `subject_track_point_id`
- `review_label`
- `limit`
- `offset`

Each query row includes the observation spine, typed pose detail, source association ids, annotation summary, artifact summary, and an evidence bundle URL.

## Evidence Bundle

API:

```http
GET /pose-observations/{pose_observation_id}/evidence-bundle
```

Bundle content:

- pose observation spine and typed `pose_observation` detail
- media and pose processing run summary
- model registry and runtime config summary
- source player detection when present
- source tracklet / track point candidate context when present
- lineage rows
- artifacts linked to the pose or source context
- annotations linked to the pose or source context
- annotation summary

The bundle uses source association candidate wording. It does not identify a subject or infer an action.

## Review Annotations

Pose reviews use the existing `human_annotation` table and generic annotation API.

Target:

```text
human_annotation.observation_id = pose observation id
```

Supported/documented labels:

```text
likely_good_pose
bad_pose
wrong_subject
bad_skeleton
uncertain
missing_keypoint
bad_keypoint
low_confidence_but_visible
keypoint_on_wrong_body_part
keypoint_occluded
uncertain_keypoint
bad_source_detection
bad_tracklet_context
subject_association_uncertain
```

Keypoint-level review metadata is stored in `payload_jsonb`:

```json
{
  "annotation_label": "bad_keypoint",
  "keypoint_name": "right_wrist",
  "keypoint_index": 10
}
```

Annotations are separate evidence records. They do not mutate the pose observation, source detection, tracklet, or track point.

Milestone 5B makes this visible in the viewer annotation panel. Keypoint-level metadata such as `keypoint_name` and `keypoint_index` is shown when present, along with notes, creator, frame range, demo-seeded metadata, and review-only metadata.

## Export

API:

```http
POST /pose/export-review-dataset
```

Worker CLI:

```bash
python -m apps.worker.cli export-pose-review-dataset \
  --run-id <pose_run_id> \
  --output-root .data/exports
```

Selected ids:

```bash
python -m apps.worker.cli export-pose-review-dataset \
  --pose-observation-id <pose_observation_id> \
  --output-root .data/exports
```

Query export:

```bash
python -m apps.worker.cli export-pose-review-dataset \
  --query-json '{"association_status":"candidate","keypoints_missing_count_min":1}' \
  --output-root .data/exports
```

The export writes:

```text
.data/exports/pose/{export_id}/pose_review_dataset.json
```

It also creates an `evidence_artifact` row:

```text
artifact_type = pose_review_dataset_export
checksum = sha256 of the JSON export
metadata_jsonb.export_version = pose_review_dataset_v0
```

For run/media/query-based exports, a `query_result` row records the selection and export artifact id.

Milestone 5B surfaces review dataset export artifacts in the run summary when those artifacts are present in the viewer payload. The export service and file format are unchanged.

## Export Record Shape

Each record includes:

- `record_type = pose_observation_review`
- media frame/time context
- pose observation id, run id, model id, runtime config id
- skeleton format/version
- bbox context
- full keypoint JSON
- keypoint present/missing counts and confidence summary
- subject association candidate context
- lineage rows
- artifacts
- annotations

Required warning fields:

```json
{
  "pose_evidence_only": true,
  "annotations_are_reviews_only": true,
  "no_movement_interpretation": true,
  "no_adjudication": true
}
```

## Non-Goals

- No real pose inference.
- No movement interpretation.
- No serve, hit, split-step, or biomechanics conclusions.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.
- No conversion to a third-party pose training format in v0.

## Blueprint 4 Completion

Blueprint 4 closes with pose evidence searchable, reviewable, and exportable. Query, evidence bundle, annotation, and export flows preserve TOM-native keypoint evidence, source candidate context, lineage, artifacts, and annotations without mutating observations or creating movement/event conclusions.
