# TOM v3 Blueprint 6 - Visual Replay / Live Observation Workstation

## Status

Status: IN PROGRESS

Milestone 6A started Blueprint 6. Milestone 6B added detection overlay playback.
Milestone 6C adds tracklet candidate and pose keypoint overlay playback.
Milestone 6D adds timeline lanes and evidence scrubbing.

TOM v3 Simple is complete. Blueprint 6 is a new product layer that turns the local evidence platform into a replay/operator workstation.

## Mission

Build a visual workstation for synchronized video replay and persisted TOM evidence.

Initial mode:

```text
indexed local video
-> replay route
-> synchronized frame/time display
-> selected run context
-> persisted detection observation overlays
-> persisted tracklet candidate overlays
-> persisted pose keypoint overlays
-> evidence timeline lanes
-> click-to-seek persisted evidence
```

Future modes may explore stream proxy workflows, but production live ingestion is not part of 6A, 6B, 6C, or 6D.

## Milestone Plan

- 6A: Video Replay Timeline Foundation
- 6B: Detection Overlay Playback
- 6C: Tracklet / Pose Replay Layers
- 6D: Evidence Timeline Lanes
- 6E: Operator Review Workflow Hardening

The plan is intentionally incremental. Each milestone should preserve TOM's observation-only boundary.

## 6A Proof

Milestone 6A proves:

```text
indexed media asset
-> browser-usable local video URL
-> replay info payload
-> frontend replay route
-> HTML video player
-> current TOM timestamp/frame display
-> timeline shell
-> available run context
```

## 6A Non-Goals

Milestone 6A does not add:

- detection overlay playback
- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- HLS/RTSP/HDMI capture
- model/runtime expansion
- tennis-event interpretation
- homography or court-space reasoning
- bounce/hit/rally/point/scoring

## 6B Proof

Milestone 6B proves:

```text
indexed video playback
-> current replay timestamp/frame
-> detection overlay chunk lookup
-> persisted ball/player bbox overlays
-> click-to-select detection observation detail
```

## 6B Non-Goals

Milestone 6B does not add:

- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- model/runtime expansion
- tennis-event interpretation
- homography or court-space reasoning
- bounce/hit/rally/point/scoring

## 6C Proof

Milestone 6C proves:

```text
indexed video playback
-> current replay timestamp/frame
-> tracklet candidate overlay chunk lookup
-> pose observation overlay chunk lookup
-> persisted candidate track points/paths
-> persisted pose keypoints/skeletons
-> click-to-select evidence detail
```

## 6C Non-Goals

Milestone 6C does not add:

- stream proxy mode
- live stream ingestion
- model/runtime expansion
- tennis-event interpretation
- homography or court-space reasoning
- bounce/hit/rally/point/scoring

## 6D Proof

Milestone 6D proves:

```text
indexed video playback
-> synchronized detection / tracklet / pose overlays
-> replay timeline endpoint
-> detection ticks
-> tracklet candidate spans
-> pose ticks
-> review annotation markers
-> click timeline item to seek/select evidence
```

## 6D Non-Goals

Milestone 6D does not add:

- stream proxy mode
- live stream ingestion
- model/runtime expansion
- tennis-event interpretation
- homography or court-space reasoning
- bounce/hit/rally/point/scoring

## Product Boundary

The replay workstation presents synchronized evidence. It does not decide official tennis meaning.

Use words like:

- replay workstation
- video replay
- observation overlay
- synchronized evidence
- media-owned frame/time
- current frame
- persisted evidence
- operator view

Avoid words that imply a final tennis decision.
