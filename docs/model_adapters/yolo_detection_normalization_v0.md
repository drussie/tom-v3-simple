# YOLO Detection Normalization v0

## Purpose

Milestone 3C normalizes YOLO-like frame outputs into TOM v3-compatible detection payloads.

This is not real model inference and does not persist observations.

## Input Shape

```json
{
  "frame_number": 120,
  "timestamp_ms": 4000,
  "image_width": 1920,
  "image_height": 1080,
  "boxes": [
    {
      "xyxy": [100.0, 200.0, 140.0, 240.0],
      "confidence": 0.91,
      "class_id": 32,
      "class_name": "sports ball",
      "source_result_index": 0
    }
  ]
}
```

## Output

Each mapped box becomes a `NormalizedYoloDetection` with:

- `observation_type`: `ball_detection` or `player_detection`
- `target_label`: `ball`, `player_unknown`, `near_player`, or `far_player`
- `frame_number`
- `timestamp_ms`
- `confidence`
- bbox as `x/y/width/height`
- center as `x/y`
- class id/name metadata
- `coordinate_space = image_pixels`
- `frame_time_owner = media_indexing`
- `source_runtime = ultralytics_yolo`

The summary includes:

- `input_box_count`
- `mapped_detection_count`
- `unmapped_detection_count`
- `unmapped_classes`
- `warnings`

## Class Mapping

Normalization uses the Milestone 3B class mapping helper.

Default name mappings include:

- `sports ball`, `tennis ball`, `ball` -> `ball_detection` / `ball`
- `person`, `player` -> `player_detection` / `player_unknown`
- `near_player` -> `player_detection` / `near_player`
- `far_player` -> `player_detection` / `far_player`

Class name matching is case-insensitive and normalizes simple separators.

Class id mapping is supported through `source_class_ids`.

Near/far player labels appear only when explicitly mapped by source class name or id.

## Bbox Conversion

Input:

```text
[x1, y1, x2, y2]
```

Output:

```text
x = x1
y = y1
width = x2 - x1
height = y2 - y1
center.x = x1 + width / 2
center.y = y1 + height / 2
```

Invalid boxes are skipped and recorded in `warnings`.

No silent clamping is performed in v0.

## Confidence

Confidence must be numeric.

Non-numeric confidence skips the box and records a warning.

Confidence outside `0..1` records a warning but the mapped detection is kept.

## Unmapped Classes

Unmapped boxes are counted and reported, but no detection payload is emitted for them.

3C does not persist unmapped classes as observations.

## Adapter Integration

Milestone 3C introduced normalization-only methods:

- `normalize_frame_result`
- `normalize_results`
- `build_adapter_result_from_normalized`

Milestone 3D connects `run()` to frame-level YOLO inference behind guarded provider interfaces. Tests use a fake provider; real runtime use still requires optional Ultralytics/OpenCV dependencies and registered local weights.

Milestone 3E adds a local smoke helper for validating that optional real runtime path when local weights and sample media are available.

Milestone 3F closes Blueprint 3 and records the normalization invariant audit in:

```text
docs/blueprints/tom_v3_blueprint_3_completion_review.md
```

## Persistence Compatibility

Normalized payloads include the fields expected by existing detection persistence and viewer overlay contracts:

- bbox
- center
- label
- class id
- class label
- confidence
- `coordinate_space = image_pixels`
- `frame_time_owner = media_indexing`

Milestone 3D uses this normalization output before writing `ball_detection` and `player_detection` observations through the existing detection persistence path.

## Out of Scope

- optimized full-video YOLO inference
- YOLO tracking mode
- tracklets
- pose
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication
