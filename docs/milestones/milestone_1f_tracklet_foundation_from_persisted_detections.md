# TOM v3 Simple - Milestone 1F Tracklet Foundation From Persisted Detections

## Goal

Create the first temporal grouping foundation from already-persisted detection observations.

Target flow:

```text
persisted ball/player detections
-> tracklet candidate builder
-> tracklet rows
-> track_point rows
-> explicit source links to detection observations
-> viewer/query inspection
```

## Scope

Milestone 1F adds:

- deterministic tracklet builder service
- worker `build-tracklets` command
- grouping for ball detections
- grouping for near-player, far-player, and player-unknown detections
- `tracklet` rows
- `track_point` rows
- source detection observation links through track points
- runtime config, model registry, processing run, and processing step records
- viewer/query compatibility tests
- docs and report

## Tracklet Meaning

A tracklet in TOM v3 means:

```text
A grouping algorithm associated these persisted detections over time.
```

It does not mean:

- the identity is proven
- the grouping is correct
- the object is definitely the ball/player
- a bounce happened
- a hit happened
- a rally or point state exists

## Non-Goals

- No real multi-object tracking sophistication.
- No Kalman filter.
- No optical flow.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No adjudication.

## Acceptance

Status: complete.

Milestone 1F is complete because:

- tracklet builder service exists
- worker `build-tracklets` command exists
- persisted detection observations can produce candidate tracklets
- ball detections produce ball tracklet candidates
- player detections produce near-player/far-player/player-unknown candidates
- tracklet rows are persisted
- track point rows are persisted
- track points reference source detection observation ids
- track point frame/time values come from source observations
- tracklet metadata marks candidate/unverified status
- processing run, step, runtime config, and model registry records are created
- tests cover grouping and persistence

## Ready For Next

Recommended next milestone: Milestone 1G - Tracklet Viewer / Multi-Run Evidence Bundle.

Reason: tracklet runs are now inspectable, but the viewer remains a single-run view. The next useful step is a bundled evidence view that can show source detection observations, frame artifacts, and tracklet candidates together.
