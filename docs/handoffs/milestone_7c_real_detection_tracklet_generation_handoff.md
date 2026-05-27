# TOM v3 - Milestone 7C Handoff

## Real Detection Tracklet Generation

Repo: `drussie/tom-v3-simple`

Branch: `codex/m7c-real-detection-tracklet-generation`

Starting state: Milestone 7B Real Detection Overlay Validation accepted and merged to `main`.

## Mission

Build candidate tracklets from real detection runs while preserving TOM v3's observation-only boundary.

The target path is:

```text
indexed media
-> run-real-detection
-> persisted real detection observations
-> build-tracklets
-> real-detection-derived candidate tracklets
-> replay workstation detection + tracklet overlays
```

## Required Boundary

Use candidate/evidence language:

- real-detection-derived tracklet
- candidate tracklet
- track point candidate
- source detection observation
- lineage
- model-output detection
- candidate temporal grouping
- unverified identity

Do not add real pose inference, court/homography, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Validation Checklist

- Build tracklets from fake real model-output detection observations.
- Track points preserve source detection observation ids.
- Lineage from source real detections to track points exists.
- Replay-info labels real-detection-derived tracklet runs.
- Replay tracklet overlays include source detection evidence metadata.
- Fixture-derived tracklet behavior remains unchanged.
- Default tests pass without YOLO weights.

## Recommended Next Handoff

Milestone 7D - Real Pose Runtime for Replay Workstation.
