# TOM v3 Blueprint 4 - Pose Observation / Movement Evidence Layer

## Status

Status: in progress

Milestones 4A, 4B, and 4C are complete. They establish the pose runtime/schema foundation, pose adapter normalization foundation, and pose observation persistence/lineage foundation.

## Mission

Persist pose model output as replayable observation evidence, including keypoints, skeleton metadata, confidence, bbox context, model/runtime provenance, optional subject association, lineage, review annotations, and export compatibility, without interpreting tennis movement or events.

Blueprint 4 is about pose evidence as model output.

It is not about movement conclusions.

## Starting Point

Blueprint 1 proved the media, observation store, viewer, detection overlay, and frame artifact loop.

Blueprint 2 proved candidate temporal evidence: persisted detections can become candidate tracklets with lineage, evidence bundles, query/review flows, and review dataset exports.

Blueprint 3 proved optional real YOLO runtime: local weights can be validated and registered, YOLO-like output can be normalized, and YOLO-origin detections can persist through the existing detection pipeline.

## Blueprint 4 Direction

The intended path is:

```text
optional pose runtime
-> validated pose model metadata
-> pose adapter normalization
-> persisted pose_observation rows
-> pose viewer overlay
-> pose review / export compatibility
-> future movement evidence candidates
```

Pose observations must use media-owned frame/time. If a future pose observation is produced from a source detection crop or track point context, the pose frame/time still comes from the source TOM v3 observation.

## Milestone 4A Result

Milestone 4A adds:

- `pose_observation` typed table
- COCO17 skeleton registry
- keypoint schema validation helpers
- pose schema models
- fixture/synthetic pose insertion helper
- pose runtime config metadata contract
- pose model registry metadata contract
- tests for pose persistence, frame/time ownership, keypoint summaries, and queryability

4A does not add real pose inference, pose overlay rendering, movement interpretation, or event candidates.

## Milestone 4B Result

Milestone 4B adds:

- fake/serialized pose frame result input contract
- COCO17 keypoint normalization using the skeleton registry
- missing keypoint preservation
- keypoint summary and pose confidence handling
- bbox normalization with explicit invalid-bbox warnings
- crop-local to full-frame keypoint projection
- subject association candidate passthrough
- pose adapter result skeleton
- tests proving normalized output can instantiate `PoseObservationCreate`

4B does not add real pose inference, pose observation worker persistence, pose overlay rendering, movement interpretation, or event candidates.

## Milestone 4C Result

Milestone 4C adds:

- fixture pose worker persistence service
- worker `run-pose-adapter`
- pose `processing_run` and `processing_step` records
- normalized fixture pose persistence through `ObservationWriter`
- first-class `pose` observation spine rows
- typed `pose_observation` rows
- media-owned frame/time preservation
- source `player_detection` candidate lineage using `pose_from_subject_detection_candidate`
- reserved relationship names for candidate tracklet and track point pose context
- tests for unassociated poses, source detection lineage, invalid explicit source ids, and CLI behavior

4C does not add real pose inference, pose overlay rendering, movement interpretation, or event candidates.

## Milestone 4D Result

Milestone 4D adds:

- viewer payload serialization for typed pose details
- frontend pose observation types
- pose overlay extraction helpers
- COCO17 skeleton edge rendering
- present keypoint marker rendering from persisted image-pixel coordinates
- missing keypoint table display without drawing missing markers
- selected pose metadata and keypoint confidence detail
- source association candidate context display
- a pose observations timeline row

4D does not add real pose inference, movement interpretation, pose review/export integration, or event candidates.

## Observation Boundary

A pose observation means:

```text
A pose adapter produced keypoint evidence for a person-like subject at a media-owned frame/time.
```

It does not mean:

```text
The subject identity is known.
The player action is known.
A serve occurred.
A hit occurred.
A split-step occurred.
A biomechanical conclusion is valid.
A rally or point exists.
```

## Out of Scope For Blueprint 4A-4D

- real pose inference
- movement interpretation
- serve mechanics conclusions
- split-step conclusions
- biomechanics analysis
- court homography
- bounce or hit detection
- rally/point/scoring
- adjudication

## Next Milestone

Recommended next milestone:

```text
Milestone 4E - Pose Query / Review / Export Integration
```
