# Tracklet Query v0

## Purpose

Tracklet Query v0 provides structured filters for candidate tracklets.

It answers:

```text
Show me candidate tracklets that match these review filters.
```

## API

```text
POST /tracklets/query
```

Example:

```json
{
  "source_detection_run_id": "...",
  "track_family": "ball",
  "min_track_points": 2,
  "has_gaps": true,
  "confidence_gte": 0.5,
  "limit": 50
}
```

## Supported Filters

- `media_id`
- `tracklet_run_id`
- `source_detection_run_id`
- `track_family`
- `subject_ref`
- `track_status`
- `identity_status`
- `frame_start_gte`
- `frame_end_lte`
- `timestamp_start_gte`
- `timestamp_end_lte`
- `confidence_gte`
- `confidence_lte`
- `min_track_points`
- `max_track_points`
- `gap_count_gte`
- `gap_count_lte`
- `has_gaps`
- `review_label`
- `has_annotation`
- `annotation_label`
- `limit`
- `offset`

## Response

The response includes:

- total count
- tracklet summaries
- candidate observation summaries
- frame/timestamp ranges
- source detection run id
- track point count
- gap count
- annotation summary
- evidence bundle URL
- summary counts by family, subject, annotation label, and gap state

## Rule

Tracklet query returns candidate evidence for review. It does not rank correctness or adjudicate track quality.
