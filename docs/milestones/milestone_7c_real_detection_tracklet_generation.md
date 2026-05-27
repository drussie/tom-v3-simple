# Milestone 7C - Real Detection Tracklet Generation

## Status

Complete.

## Goal

Build candidate tracklets from real YOLO detection replay runs using the existing tracklet builder.

7C does not add a new tracking model. It applies TOM v3's existing deterministic candidate grouping to persisted real model-output `ball_detection` and `player_detection` observations.

## What Changed

- `build-tracklets` can build candidate tracklets from real detection runs.
- Source detection run validation checks that the run contains atomic ball/player detections with media-owned frame/time.
- Tracklet run, runtime config, processing step, tracklet observations, track points, and lineage now preserve source detection evidence metadata.
- Replay-info can label real-detection-derived tracklet runs.
- Replay tracklet overlays and track point overlays expose source detection evidence metadata.
- Selected tracklet and track point details in the replay workstation show source detection run/runtime/evidence context when available.
- `build-tracklets` output includes a replay URL with both `detectionRunId` and `trackletRunId`.

## Boundary

Tracklets remain candidate temporal groupings. They do not establish identity, ball path correctness, tennis events, or scoring.

7C does not add real pose inference, court/homography, bounce/hit/rally/point/scoring, real stream ingestion, or adjudication.
