# TOM v3 Blueprint 2 - Temporal Evidence Tracklet Candidate System

## Mission

Blueprint 2 creates a lightweight temporal evidence layer that groups persisted detection observations into candidate tracklets, persists every track point with source links, and makes those temporal groupings queryable and visually replayable without adjudicating correctness.

## Current Status

Status: in progress.

- Milestone 2A made tracklet candidates and track point candidates first-class observations.
- Milestone 2A added lineage from source detections to track points and from track points to tracklets.
- Milestone 2B adds a dynamic multi-run evidence bundle so the viewer can inspect tracklet evidence alongside source detection evidence.

## Core Flow

```text
source detection run
-> ball/player detection observations
-> tracklet builder run
-> tracklet candidate observations
-> track point candidate observations
-> lineage across observations
-> tracklet evidence bundle
-> viewer inspection
```

## Core Rule

Tracklet evidence is descriptive. It records that a grouping algorithm associated persisted detections over time.

It does not prove object identity, object path, bounce, hit, rally, point state, or score.

## Milestone Path

- 2A: Tracklet candidate observation spine and lineage.
- 2B: Tracklet viewer / multi-run evidence bundle.
- 2C: Tracklet query and review, unless real YOLO runtime work is prioritized.
