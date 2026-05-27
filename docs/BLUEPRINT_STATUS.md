# TOM v3 Simple Blueprint Status

## Overview

- Blueprint 1: COMPLETE
- Blueprint 2: COMPLETE
- Blueprint 3: COMPLETE
- Blueprint 4: COMPLETE
- Blueprint 5: COMPLETE
- Blueprint 6: COMPLETE
- Blueprint 7: COMPLETE
- Blueprint 8: IN PROGRESS
- TOM v3 Simple: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. Blueprint 6 is complete as the visual replay/operator workstation layer. Blueprint 7 is complete as the real perception runtime layer for optional real detection, real-detection-derived candidate tracklets, and optional real pose keypoint evidence. Blueprint 8 is in progress with court/camera/homography schema contracts, fixture court evidence persistence, and camera/view evidence query/bundle read models.

## Blueprint 1 - Media, Observation Store, Viewer Foundation

Status: COMPLETE

Proved:

```text
real media
-> indexed media asset
-> observation store
-> queryable evidence
-> visual evidence viewer
-> frame-backed detection evidence
```

Did not add:

- candidate tracklet review/export completion
- optional real YOLO runtime
- pose evidence
- tennis-event interpretation
- scoring
- adjudication

## Blueprint 2 - Temporal Evidence Tracklet Candidate System

Status: COMPLETE

Proved:

```text
persisted detections
-> candidate tracklets
-> track point candidates
-> lineage to source detections
-> multi-run evidence bundle
-> query
-> review annotation
-> exportable review dataset
```

Did not add:

- pose
- homography
- bounce or hit detection
- rally/point/scoring
- identity proof
- adjudication

## Blueprint 3 - Optional YOLO Runtime / Detection Observation Adapter

Status: COMPLETE

Proved:

```text
optional YOLO runtime
-> runtime probe / device resolver
-> local weights validation
-> model_registry metadata
-> YOLO-like normalization
-> guarded frame inference provider
-> existing detection adapter persistence
-> atomic ball/player observations
-> existing viewer, frame artifact, tracklet, review, and export paths
```

Did not add:

- YOLO tracking mode
- pose
- homography
- bounce or hit detection
- rally/point/scoring
- identity proof
- adjudication

## Blueprint 4 - Pose Observation / Movement Evidence Layer

Status: COMPLETE

Proved:

```text
pose schema
-> COCO17 skeleton registry
-> fake / serialized pose normalization
-> fixture pose processing run
-> persisted pose observation
-> source candidate lineage
-> pose overlay viewer
-> pose query
-> review annotation support
-> TOM-native pose review export
```

Did not add:

- real pose inference
- movement interpretation
- stroke classification
- serve/hit/split-step/biomechanics conclusions
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

## Blueprint 5 - Simple Completion / Product Hardening

Status: COMPLETE

Completed:

- 5A: canonical local fixture demo and runbook
- 5B: viewer/product polish
- 5C: final evidence/provenance audit
- 5D: docs/control-room consolidation
- 5E: final completion review

Final proof path:

```text
fixture demo
-> viewer inspection
-> review annotations
-> exports
-> provenance audit
-> canonical docs
-> final completion review
```

Blueprint 5 proved that TOM v3 Simple can be run, inspected, audited, explained, and demoed locally without adding tennis interpretation capability.

Blueprint 5 did not add real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, streaming, or adjudication.

## Blueprint 6 - Visual Replay / Live Observation Workstation

Status: COMPLETE

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Milestone 6A proved:

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

Milestone 6A did not add:

- detection overlay playback
- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6B proved:

```text
indexed video playback
-> current TOM timestamp/frame
-> detection overlay chunk endpoint
-> persisted ball/player bbox overlays
-> detection layer toggle
-> detection run selection
-> click-to-select detection observation detail
```

Milestone 6B did not add:

- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6C proved:

```text
indexed video playback
-> current TOM timestamp/frame
-> detection overlay chunks
-> tracklet candidate overlay chunks
-> pose keypoint overlay chunks
-> synchronized bbox / point / skeleton rendering
-> click-to-select persisted evidence details
```

Milestone 6C did not add:

- stream proxy mode
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6D proved:

```text
indexed video playback
-> synchronized detection / tracklet / pose overlays
-> replay timeline endpoint
-> evidence lanes
-> detection ticks
-> tracklet candidate spans
-> pose ticks
-> review annotation markers
-> click-to-seek/select persisted evidence
```

Milestone 6D did not add:

- stream proxy mode
- live stream ingestion
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6E proved:

```text
indexed video playback
-> Replay / Stream Proxy mode toggle
-> video-as-live live edge
-> hidden future overlays
-> hidden future timeline evidence
-> operator pause/review state
-> return-to-live-edge control
```

Milestone 6E did not add:

- real live stream ingestion
- HLS/RTSP/HDMI/camera capture
- websocket live updates
- model scheduling
- model/runtime expansion
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Milestone 6F proved:

```text
Replay Mode
-> Stream Proxy Mode
-> synchronized detection / tracklet / pose evidence overlays
-> evidence timeline lanes
-> click-to-seek/select persisted evidence
-> hidden future evidence in Stream Proxy Mode
-> Blueprint 6 completion review
```

Milestone 6F did not add:

- real live stream ingestion
- HLS/RTSP/HDMI/camera capture
- stream backend/session tables
- websocket live updates
- live model scheduling
- real pose inference
- tennis-event interpretation
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Future real live ingestion and future tennis intelligence must begin as new blueprints.

## Blueprint 7 - Real Perception Runtime For Replay Workstation

Status: COMPLETE

Blueprint 7 mission:

```text
indexed video
-> real perception runtime
-> persisted model-output observations
-> replay workstation overlays
```

Milestone 7A proved:

```text
indexed media
-> optional YOLO runtime and local weights
-> media-owned frame sampling
-> explicit class mapping
-> real YOLO frame inference
-> persisted atomic ball/player detection observations
-> replay URL with real detectionRunId
```

Milestone 7B validates:

```text
real YOLO detection run
-> replay-info available run source metadata
-> real-vs-fixture run selector labels
-> overlay payload source/runtime/model/config metadata
-> selected detection detail source context
-> timeline detection source labels
```

Milestone 7C proves:

```text
real model-output detection observations
-> candidate tracklet builder
-> real-detection-derived tracklet run
-> track point candidates
-> lineage to source detections
-> replay URL with detectionRunId and trackletRunId
```

Milestone 7D proves:

```text
indexed media
-> optional pose runtime and local weights
-> crop-from-player-detection or full-frame pose inference
-> normalized COCO17 keypoint evidence
-> persisted player_pose_observation rows
-> lineage to source player detections when available
-> replay URL with poseRunId
```

Milestone 7E decides:

```text
court / camera / homography scope review
-> geometry evidence contract proposal
-> Blueprint 8 candidate
-> implementation deferred
```

Milestone 7F closes Blueprint 7:

```text
real perception ladder
-> final orchestration runbook
-> completion review
-> Blueprint 8 boundary preserved
```

Blueprint 7 Status: COMPLETE

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. TOM can now run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output detection evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation.

Blueprint 7 remains observation-only and non-adjudicative. It does not add court/homography implementation, bounce/hit/rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, or TOM v2-style adjudication.

Milestones 7A/7B/7C/7D/7E/7F do not add:

- movement interpretation or biomechanics conclusions
- homography or court-space reasoning
- court/camera/homography runtime
- stream ingestion
- bounce or hit detection
- rally/point/scoring
- identity resolution or ball-path conclusions
- adjudication

Court/camera/homography runtime work is future Blueprint 8 milestone work.

Remaining Blueprint 7 milestones: none.

## Blueprint 8 - Court / Camera / Homography Evidence Layer

Status: IN PROGRESS

Blueprint 8 mission:

```text
indexed video
-> court / camera evidence
-> homography candidates
-> projection diagnostics
-> replayable geometry evidence
```

Milestone 8A proves:

```text
observation spine
-> court keypoint typed rows
-> court line typed rows
-> camera/view typed rows
-> homography candidate typed rows
-> projection diagnostic typed rows
-> lineage-ready geometry evidence
```

8A adds schema contracts, typed storage tables, migration, a normalized court template registry, observation writer support, lineage relationship constants, and fake persistence tests.

Milestone 8B proves:

```text
indexed media
-> fixture court evidence adapter
-> media-owned frame sampling
-> court keypoint observations
-> court line observations
-> camera/view observations
-> model/runtime/run/step provenance
```

8B adds worker `run-fixture-court`, Makefile `court-fixture`, deterministic fixture geometry, and adapter persistence tests.

Milestone 8C proves:

```text
fixture camera/view observations
-> camera/view query service
-> camera/view summary read model
-> camera/view evidence bundle
-> /court/camera-view API
```

8C adds read-only query, summary, and bundle access for camera/view geometry context evidence. It does not create new camera/view rows beyond the 8B fixture adapter path.

8C does not add:

- real camera/view model
- homography computation
- projection diagnostics
- replay court overlay
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

8B does not add:

- real court keypoint detector
- real court line detector
- homography computation
- projection diagnostics
- replay court overlay
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication

8A does not add:

- real court keypoint detector
- real court line detector
- homography computation
- replay court overlay
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- stream ingestion
- adjudication
