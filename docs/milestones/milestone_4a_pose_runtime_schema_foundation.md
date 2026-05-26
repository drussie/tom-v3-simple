# Milestone 4A - Pose Runtime / Schema Foundation

## Status

Status: complete

## Purpose

Milestone 4A starts Blueprint 4 by adding the schema and helper contracts needed to persist pose evidence.

## Result

The repo now has:

- Blueprint 4 documentation
- COCO17 skeleton registry
- keypoint schema validation helpers
- pose schema models
- `pose_observation` typed table
- observation-writer support for pose typed rows
- synthetic fixture pose insertion helper
- tests for keypoint validation, typed-row persistence, media-owned frame/time, model metadata, runtime config metadata, and existing observation query compatibility

## Flow

```text
observation spine
-> pose_observation typed row
-> COCO17 keypoints JSON
-> keypoint summary columns
-> existing observation query path
```

## Non-Goals

- No real pose inference.
- No pose overlay viewer.
- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Next Milestone

Recommended next milestone:

```text
Milestone 4B - Pose Adapter Normalization Foundation
```
