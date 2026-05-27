# Pose Adapter Normalization v0

## Purpose

Milestone 4B adds normalization for fake or serialized pose model output.

The normalizer converts model-shaped pose output into `PoseObservationCreate`-compatible payloads. Milestone 4C uses this normalizer from a fixture worker persistence path. The normalizer itself does not run a pose model, render a pose overlay, or interpret movement.

## Location

```text
packages/model_adapters/tom_v3_model_adapters/pose_normalization.py
```

## Input Shape

The v0 fake frame result shape is:

```json
{
  "frame_number": 120,
  "timestamp_ms": 4000,
  "image_width": 1280,
  "image_height": 720,
  "poses": [
    {
      "bbox_xyxy": [480.0, 150.0, 660.0, 580.0],
      "bbox_confidence": 0.86,
      "pose_confidence": 0.82,
      "source_result_index": 0,
      "keypoints": [
        {"x": 500.0, "y": 180.0, "confidence": 0.9}
      ]
    }
  ]
}
```

The keypoint list must match the COCO17 count in v0.

## Output Shape

The output is a `NormalizedPoseObservation` with the same fields required by `PoseObservationCreate`:

- frame number and timestamp
- skeleton format/version
- keypoint schema JSON
- named keypoints JSON
- keypoint count, present/missing count, and confidence summary
- pose confidence
- bbox fields
- crop fields when crop projection is used
- subject association candidate fields
- `frame_time_owner = media_indexing`
- raw model payload and normalization metadata

## Keypoint Rules

- Names and indices come from the COCO17 skeleton registry.
- `x` and `y` are stored in full-frame image pixels.
- `x_norm` and `y_norm` are computed from image width/height when available.
- Missing keypoints are preserved with `present = false`.
- Missing keypoints are not inferred, padded, smoothed, or repaired.
- Wrong keypoint count skips the pose and records `invalid_keypoint_count`.
- Non-numeric coordinates mark the keypoint missing and record `invalid_keypoint_coordinate`.

## Bbox Rules

Input bbox is `bbox_xyxy`.

Output bbox fields are:

```text
bbox_x = x1
bbox_y = y1
bbox_w = x2 - x1
bbox_h = y2 - y1
```

If keypoints are valid but bbox is invalid, the pose is kept with null bbox fields and an `invalid_bbox` warning. This preserves keypoint evidence without pretending the bbox context is usable.

## Confidence Rules

- Provided `pose_confidence` is copied.
- Missing `pose_confidence` falls back to the mean present keypoint confidence.
- Null keypoint confidence is allowed.
- Non-numeric confidence records `invalid_confidence`.
- Confidence outside `0..1` records `confidence_out_of_range`.
- No confidence is clamped.

## Crop Projection

If `keypoint_coordinate_space = crop_pixels`, v0 projects crop-local keypoints to full-frame coordinates:

```text
full_frame_x = crop.x + crop_keypoint_x
full_frame_y = crop.y + crop_keypoint_y
```

The output stores `crop_x`, `crop_y`, `crop_w`, `crop_h`, and `crop_source`. Crop-local keypoints are retained in `metadata_jsonb.crop_local_keypoints`.

## Subject Association

Full-frame normalization defaults to:

```text
subject_ref_type = none
association_status = unassociated
association_method = full_frame_pose
```

Input `subject_context` can pass through candidate association fields for a player detection, tracklet, or track point. These fields are context only; they do not establish identity.

Milestone 4C persists source `player_detection` candidate context as observation lineage:

```text
relationship_type = pose_from_subject_detection_candidate
```

## Adapter Skeleton

The module includes:

- `PoseNormalizationAdapter`
- `FixturePoseAdapter`
- `PoseNormalizationResult`
- `PoseAdapterResult`

Diagnostics include counts, warnings, and the note:

```text
normalization only, no real pose inference
```

## Worker Persistence

The normalized output can be persisted by worker `run-pose-adapter`. Full-frame fixture mode remains unassociated. Source-detection-linked fixture mode uses persisted `player_detection` observations as candidate subject context and preserves their frame/time values.

## Non-Goals

- No real pose inference.
- No pose model loading.
- No pose overlay viewer.
- No movement interpretation.
- No serve, hit, split-step, or biomechanics conclusions.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.

## Blueprint 4 Completion

Blueprint 4 closes with this normalizer as the bridge from fake/serialized pose model output into TOM v3 pose evidence. It prepares persistence-ready payloads, but it still does not load a pose model, smooth keypoints, repair missing keypoints, or interpret movement.
