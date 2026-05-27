# Milestone 7D - Real Pose Runtime for Replay Workstation

## Status

Complete.

## Goal

Run optional real pose inference on indexed media and persist `player_pose_observation` rows that the replay workstation can render as pose keypoint evidence.

7D uses TOM v3's existing pose schema, COCO17 skeleton registry, pose normalization, pose persistence, lineage, and replay pose overlay path.

## What Changed

- Added `run-real-pose` worker CLI.
- Added `make real-pose`.
- Added an optional Ultralytics pose provider boundary and fake pose provider for default tests.
- Added a real pose replay service with plan-only, crop-from-player-detection, and full-frame modes.
- Reused local weights validation and optional runtime probe patterns.
- Registered pose model metadata separately from detection model metadata.
- Persisted real `player_pose_observation` rows through the existing pose contract.
- Stored real pose output source metadata, model registry id, runtime config id, COCO17 keypoint summaries, and media-owned frame/time.
- Linked crop-mode pose observations back to source `player_detection` observations through `pose_from_subject_detection_candidate` lineage.
- Exposed real pose source metadata in replay-info, pose overlay chunks, pose timeline items, and selected pose detail when available.

## Boundary

Pose observations are keypoint evidence from a configured model at a media-owned frame/time.

7D does not add movement interpretation, stroke classification, serve detection, split-step analysis, biomechanics conclusions, player identity resolution, court/homography evidence, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.

## Validation

Default tests use fake/stubbed pose output and do not require pose weights.

Optional local real pose smoke requires local pose weights and the optional runtime environment.
