# Skeleton Registry v0

## Purpose

Milestone 4A adds a central skeleton registry for pose observations.

The registry is intended to be reused by future pose adapter normalization, viewer overlays, review tools, and exports.

## Location

```text
packages/schema/tom_v3_schema/skeletons.py
```

## COCO17

The first supported skeleton is:

```text
skeleton_format = coco17
skeleton_version = v1
```

Keypoint names:

```text
nose
left_eye
right_eye
left_ear
right_ear
left_shoulder
right_shoulder
left_elbow
right_elbow
left_wrist
right_wrist
left_hip
right_hip
left_knee
right_knee
left_ankle
right_ankle
```

## Validation

The registry validates:

- skeleton format/version exists
- keypoint indices are contiguous and ordered
- keypoint names align with indices
- skeleton edges reference known keypoint names
- pose keypoint payloads have the expected count, names, and indices

## Contract

The skeleton registry describes the shape of model output evidence. It does not interpret actions, movement, skill, or biomechanics.
