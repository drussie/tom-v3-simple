# TOM v3 Simple - Milestone 1D Handoff

## Detection Overlay / Visual Observation Layer

Repo: `drussie/tom-v3-simple`

Branch: `codex/m1d-detection-overlay-visual-observation-layer`

## Mission

Implement the first visual overlay layer for persisted detection observations in TOM v3 Simple.

Milestone 1C added ball/player detection observations. Milestone 1D makes those observations visible by rendering bbox overlays in the existing visual evidence viewer.

## Target Flow

```text
indexed media
-> detection run
-> persisted ball/player detection observations
-> viewer run payload
-> bbox overlay / frame-space visualization
-> selected observation context
```

## In Scope

- Viewer data transform for detection observations.
- Bbox extraction from observation and atomic payloads.
- Detection overlay component.
- Selected frame handling.
- Selected observation highlighting.
- Detection timeline/list integration.
- Media/frame placeholder panel using image-pixel coordinates.
- Safe handling for missing dimensions or missing bbox payloads.
- Tests, docs, and agent report.

## Out of Scope

- Real YOLO inference.
- Tracking.
- Pose detection.
- Court homography.
- Bounce detection.
- Hit detection.
- Rally segmentation.
- Point reconstruction.
- Scoring.
- Production streaming.
- Adjudication.

## Completion Notes

The overlay should show that a model/adapter emitted a detection observation at a frame and bbox. It must not imply that the object was proven correct or that a track or event exists.
