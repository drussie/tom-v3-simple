# TOM v3 Blueprint 7 - Real Perception Runtime For Replay Workstation

Status: COMPLETE

## Mission

Blueprint 7 runs real perception on indexed tennis video and persists model-output observations so the Blueprint 6 replay workstation displays real detection, candidate tracklet, and pose keypoint evidence over video playback.

The architecture remains observation-only and non-adjudicative. Real model output is persisted as evidence, not as official tennis meaning.

## Starting Point

TOM v3 Simple is complete, and Blueprint 6 is complete. The replay workstation can already open indexed video, synchronize media-owned frame/time, render persisted detection, tracklet, and pose overlays, show evidence timeline lanes, and simulate video-as-live Stream Proxy Mode.

Blueprint 7 begins from that replay surface and replaces fixture-only perception with optional real model-output runs.

## Milestone 7A

Milestone 7A adds a narrow real YOLO detection replay path:

```text
indexed video
-> optional YOLO runtime and local weights
-> media-owned frame sampling
-> real YOLO frame inference
-> explicit class mapping
-> persisted atomic ball/player detection observations
-> replay URL with detectionRunId
-> real detection overlays in the replay workstation
```

7A does not build real tracklets from real detections, real pose inference, homography, stream ingestion, or tennis-event interpretation.

## Milestone 7B

Milestone 7B validates real detection overlay use in the replay workstation:

```text
real YOLO detection run
-> replay-info source metadata
-> run selector labels for real model output vs fixture evidence
-> overlay payload source/runtime/model/config metadata
-> selected detection detail source context
-> timeline detection labels
```

7B does not create tracklets from real detections, add real pose inference, add court/homography evidence, improve model quality, ingest streams, or interpret tennis events.

## Milestone 7C

Milestone 7C builds candidate tracklets from real detection runs:

```text
real YOLO detection observations
-> existing candidate tracklet builder
-> real-detection-derived tracklet run metadata
-> track point candidates with source detection ids
-> lineage back to source real detections
-> replay URL with detectionRunId and trackletRunId
```

7C keeps tracklets as candidate temporal groupings. It does not add a new tracking model, smoothing/interpolation as evidence, real pose inference, court/homography evidence, stream ingestion, or tennis-event interpretation.

## Milestone 7D

Milestone 7D adds optional real pose replay runtime:

```text
indexed media
-> optional pose runtime and local weights
-> crop-from-player-detection or full-frame pose inference
-> normalized COCO17 keypoint evidence
-> persisted player_pose_observation rows
-> source player detection lineage when available
-> replay URL with poseRunId
```

7D keeps pose as keypoint evidence. It does not add movement interpretation, stroke classification, serve detection, biomechanics conclusions, court/homography evidence, stream ingestion, or tennis-event interpretation.

## Milestone 7E

Milestone 7E is a court/homography evidence decision gate:

```text
Blueprint 7 real perception runtime
-> court/camera/homography scope review
-> geometry evidence contract proposal
-> Blueprint 8 candidate
-> no runtime implementation
```

7E decides that court/camera/homography evidence should be future Blueprint 8 work. It does not add database schema, court runtime, homography computation, replay court overlays, production coordinate transforms, stream ingestion, or tennis-event interpretation.

## Milestone 7F

Milestone 7F closes Blueprint 7 with perception run orchestration and completion review:

```text
fixture-safe demo
-> optional real detection
-> optional real-detection-derived candidate tracklets
-> optional real pose
-> replay workstation URLs
-> Blueprint 8 court/homography boundary
```

7F adds final status updates, final runbook consolidation, completion review docs, and validation notes. It does not add new runtime behavior, API behavior, schema, frontend features, stream ingestion, court/homography implementation, or tennis-event interpretation.

Blueprint 7 Status: COMPLETE

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. TOM can now run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output detection evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation.

Blueprint 7 remains observation-only and non-adjudicative. It does not add court/homography implementation, bounce/hit/rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, or TOM v2-style adjudication.

Court/camera/homography evidence is deferred to Blueprint 8.

## Boundaries

Blueprint 7 does not add official tennis conclusions, TOM v2-style adjudication, accepted/rejected event lifecycles, bounce/hit detection, stroke classification, rally/point/scoring, player identity resolution, ball-path conclusions, movement interpretation from pose, court-space reasoning, court/homography runtime, or live stream ingestion.

Future real perception outputs remain observations and candidates until a separate blueprint deliberately defines a higher-level evidence layer.

## Fixture Path

The default fixture demo remains unchanged and CI-safe:

```text
make demo
make completion-audit
```

No YOLO weights, GPU, Torch, Ultralytics, OpenCV, or pose weights are required for default validation.

## Future Work

Remaining Blueprint 7 milestones: none.

Future work should begin as a separate blueprint:

- Blueprint 8 - Court / Camera / Homography Evidence Layer.
- Bounce / Hit Candidate Evidence.
- Movement / Stroke Evidence Candidates.
- Real Live Stream Ingestion.
- Product Deployment Blueprint.

Court/camera/homography evidence is now a Blueprint 8 candidate.
