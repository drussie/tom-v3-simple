# Milestone 4E Handoff - Pose Query / Review / Export Integration

## Starting State

Milestone 4D made persisted pose observations visible in the existing Evidence Viewer with COCO17 keypoint and skeleton overlays.

## Mission

Make pose observations searchable, reviewable, and exportable while preserving the observation-only pose evidence contract.

## Implemented Result

Milestone 4E adds:

- `POST /pose/query`
- `GET /pose-observations/{pose_observation_id}/evidence-bundle`
- `POST /pose/export-review-dataset`
- worker `export-pose-review-dataset`
- `PoseQueryFilters` / `PoseQueryResponse`
- `PoseReviewDatasetExportRequest` / `PoseReviewDatasetExportResponse`
- `pose_review_dataset_export` evidence artifacts
- query result rows for query/run/media-based exports
- pose review labels and keypoint-level annotation metadata support

## Review Labels

Supported/documented pose labels include:

- `likely_good_pose`
- `bad_pose`
- `wrong_subject`
- `bad_skeleton`
- `uncertain`
- `missing_keypoint`
- `bad_keypoint`
- `low_confidence_but_visible`
- `keypoint_on_wrong_body_part`
- `keypoint_occluded`
- `uncertain_keypoint`
- `bad_source_detection`
- `bad_tracklet_context`
- `subject_association_uncertain`

Keypoint-level annotation metadata is stored in `human_annotation.payload_jsonb`, for example:

```json
{
  "annotation_label": "bad_keypoint",
  "keypoint_name": "right_wrist",
  "keypoint_index": 10
}
```

## Non-Goals Preserved

- No real pose inference.
- No movement interpretation.
- No tennis-event candidates.
- No serve, hit, split-step, or biomechanics conclusions.
- No homography, bounce, hit, rally, point, scoring, or adjudication.

## Next Handoff

Milestone 4F - Blueprint 4 Completion Review / Pose Evidence Hardening.
