# TOM v3 Simple Observation Contract

TOM v3 Simple records evidence. It does not decide official tennis meaning.

## Frame And Time Ownership

Media indexing owns frame/time.

Adapters and fixture services must use media-owned frame numbers and timestamps. A model runtime should not invent independent TOM v3 time.

For frame observations:

```text
observation.frame_start = media-owned frame
observation.frame_end = same frame
observation.timestamp_start_ms = media-owned timestamp
observation.timestamp_end_ms = same timestamp
```

Pose observations also store:

```text
frame_time_owner = media_indexing
```

## Observation Spine

Every persisted evidence record has an `observation` spine row.

The spine stores family, type, media/run ownership, frame/time, confidence, model/runtime provenance, coordinate space, and a compact payload.

Typed rows store detailed payloads.

## Gameplay Observations

Gameplay observations store fixture or adapter view-state evidence such as gameplay, non-gameplay, or uncertain intervals.

They do not decide point state, rally state, or score.

## Atomic Detection Observations

Atomic detections store ball/player bbox and center evidence.

Examples:

- `ball_detection`
- `player_detection`

A detection observation means an adapter or fixture produced a detection-like output. It does not prove the object is correct or known.

## Tracklet Candidates

Tracklet candidates are temporal groupings of source detections.

They store candidate grouping metadata and lineage from track point candidates.

A tracklet candidate does not prove object identity or path correctness.

## Track Point Candidates

Track point candidates connect a source detection observation to a candidate tracklet at a frame/time.

They keep source detection id, bbox/center context, and candidate grouping metadata.

## Pose Observations

Pose observations store keypoint evidence for a person-like subject at a media-owned frame/time.

They use COCO17 keypoint names/indices in v0. Missing keypoints persist as missing evidence and are not inferred.

Pose observations do not identify a player, classify movement, or describe tennis actions.

## Court / Camera / Homography Evidence

Blueprint 8 uses `observation_family = court` for geometry evidence.

Current typed court observation types:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`
- `homography_candidate_observation`
- `projection_diagnostic_observation`

Court observations store geometry evidence at media-owned frame/time. Homography rows are candidates. Projection diagnostic rows diagnose court-template projection evidence only.

Court evidence does not decide in/out, bounce locations, player court position, ball court position, rally state, point state, or score.

## Lineage

Lineage records source relationships between observations.

Examples:

- `tracked_from`
- `grouped_from`
- `pose_from_subject_detection_candidate`
- `subject_context_candidate`
- `pose_from_track_point_candidate`
- `homography_from_court_keypoints_candidate`
- `homography_from_court_lines_candidate`
- `camera_context_for_homography_candidate`
- `projection_diagnostic_for_homography_candidate`

Lineage is source context. It does not certify correctness.

## Evidence Artifacts

Evidence artifacts store files or metadata connected to media, runs, or observations:

- frame images
- detection frame images
- debug JSON
- review export JSON

File-backed artifacts should include checksums where available.

## Human Annotations

Human annotations are review evidence.

They may include labels, notes, keypoint metadata, demo-seeded flags, and review-only flags.

Annotations do not mutate observations, source detections, tracklets, pose rows, or exports.

## Review Exports

Exports package evidence into TOM-native review datasets.

Current exports:

- tracklet review dataset
- pose review dataset

Future court review exports should package court keypoints, court lines, camera/view evidence, homography candidates, projection diagnostics, lineage, artifacts, and annotations without producing tennis-event conclusions.

Exports are portable evidence packages. They are not official tennis results.

## What Observations Do Not Mean

An observation does not mean:

- the output is correct
- identity is known
- a stroke happened
- a hit happened
- a bounce happened
- a rally or point exists
- a score exists
- the result is official
