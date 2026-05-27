# TOM v3 - Milestone 7D Handoff

## Real Pose Runtime for Replay Workstation

Repo: `drussie/tom-v3-simple`

Branch: `codex/m7d-real-pose-runtime-replay-workstation`

Starting state: Milestone 7C Real Detection Tracklet Generation accepted and merged to `main`.

## Mission

Add optional real pose runtime for the replay workstation while preserving TOM v3's observation-only boundary.

The target path is:

```text
indexed media
-> real detection run with player detections
-> run-real-pose
-> persisted real player_pose_observation rows
-> lineage to source player detections when available
-> replay workstation detection / tracklet / pose overlays
```

## Required Boundary

Use evidence language:

- pose observation
- keypoint evidence
- real model output
- source player detection
- subject association candidate
- COCO17 keypoints
- media-owned frame/time
- persisted evidence
- replay overlay

Do not add movement interpretation, stroke classification, serve detection, split-step analysis, biomechanics conclusions, court/homography, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Validation Checklist

- `run-real-pose` supports plan-only mode.
- Missing media, weights, runtime, and source detection runs fail clearly.
- Fake pose provider persists real-run-labeled pose observations without weights.
- Crop mode links pose observations to source player detections.
- Lineage from source player detections to pose observations exists.
- Replay-info labels real pose model-output runs.
- Replay overlay and timeline endpoints return real pose source metadata.
- Fixture pose behavior remains unchanged.
- Default tests pass without pose weights.

## Recommended Next Handoff

Milestone 7E - Court / Homography Evidence Decision Gate.
