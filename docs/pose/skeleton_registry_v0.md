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

## Normalization Use

Milestone 4B uses this registry to assign COCO17 names and indices to fake/serialized pose keypoints during normalization. The normalizer skips a pose when keypoint count does not match the registered skeleton instead of silently padding or truncating.

## Blueprint 4 Completion

Blueprint 4 closes with COCO17 as the first supported skeleton contract. The registry is reused by normalization, persistence tests, viewer overlay helpers, and pose export so keypoint names, indices, and edges stay consistent across the pose evidence path.
