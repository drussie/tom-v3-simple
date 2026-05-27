# TOM v3 Simple Blueprint Status

## Overview

- Blueprint 1: COMPLETE
- Blueprint 2: COMPLETE
- Blueprint 3: COMPLETE
- Blueprint 4: COMPLETE
- Blueprint 5: COMPLETE
- Blueprint 6: IN PROGRESS
- TOM v3 Simple: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. Blueprint 6 has started as the visual replay/operator layer.

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

Status: IN PROGRESS

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
