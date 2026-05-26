# TOM v3 Simple - Milestone 1D Detection Overlay / Visual Observation Layer

## Goal

Make persisted ball/player detection observations visually inspectable in the existing TOM v3 viewer.

Target flow:

```text
indexed media_asset
-> detection adapter run
-> persisted ball_detection / player_detection observations
-> viewer run payload
-> bbox overlay and selected observation context
```

## Scope

Milestone 1D adds:

- detection overlay viewer transform
- bbox extraction from persisted detection observation payloads
- coordinate-space overlay panel
- selected frame behavior for detection observations
- selected bbox highlighting
- detection timeline row
- safe empty states for missing media dimensions or missing bbox payloads
- docs and validation coverage

## Data Contract

The overlay uses persisted observations only:

- `observation_family = atomic`
- `observation_type = ball_detection` or `player_detection`
- `coordinate_space = image_pixels`
- bbox data from observation or atomic payload JSON

Frame selection uses `frame_start` / `frame_end` from the persisted observation. The overlay does not maintain a separate frontend-only timeline.

## Non-Goals

- No real YOLO inference.
- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No production streaming.
- No adjudication.

## Acceptance

Status: complete.

Milestone 1D is complete because:

- detection overlay transform exists
- detection overlay components exist
- overlay uses persisted ball_detection and player_detection observations
- bboxes are rendered using media dimensions and image-pixel coordinates
- selected detection observations highlight matching bboxes
- missing dimensions and missing bbox payloads are handled safely
- existing detail, lineage, artifact, and annotation panels continue to use the selected observation
- detection observations are visible in the timeline and observation list
- tests and build validation pass

## Ready For Next

Recommended next milestone: Milestone 1E - Detection Artifact / Frame Extraction Foundation.

Reason: detection bboxes are now visible on an honest coordinate canvas. The next useful step is extracting or serving actual frames/artifacts so the same persisted bboxes can be inspected over real imagery.
