# Tracklet Review Annotations v0

## Purpose

Tracklet review annotations let humans mark observations for review without changing the observations themselves.

Annotations may target:

- tracklet candidate observations
- track point candidate observations
- source detection observations

## Storage

Review labels use the existing `human_annotation` table.

Recommended payload:

```json
{
  "annotation_label": "bad_tracklet",
  "notes": "Track jumps to another object around frame 120.",
  "review_context": "tracklet_evidence_bundle",
  "review_status": "reviewed",
  "target_kind": "tracklet_candidate",
  "created_from_view": "tracklet_evidence_panel"
}
```

## Tracklet Labels

- `likely_good_tracklet`
- `bad_tracklet`
- `identity_switch`
- `wrong_grouping`
- `fragmented_tracklet`
- `merged_multiple_objects`
- `uncertain`

## Track Point Labels

- `wrong_point_assignment`
- `point_should_start_new_tracklet`
- `point_should_belong_to_previous_tracklet`
- `bad_source_detection`
- `missed_detection_nearby`
- `uncertain`

## Source Detection Labels

- `bad_source_detection`
- `wrong_class_label`
- `bad_bbox`
- `duplicate_detection`
- `missed_ball_nearby`
- `uncertain`

## Immutability

Annotations do not mutate source detections, track point candidates, tracklet candidates, lineage, or frame artifacts. They are additional review evidence.

## Export Behavior

Milestone 2D review dataset exports include annotations by default.

Exported annotations remain review evidence. They are not converted into adjudicated labels, and the export carries explicit candidate-only and no-adjudication warnings.
