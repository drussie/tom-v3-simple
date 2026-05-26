# TOM v3 Blueprint 2 - Temporal Evidence Tracklet Candidate System

## Mission

Blueprint 2 creates a lightweight temporal evidence layer that groups persisted detection observations into candidate tracklets, persists every track point with source links, and makes those temporal groupings queryable and visually replayable without adjudicating correctness.

## Current Status

Status: complete.

- Milestone 2A made tracklet candidates and track point candidates first-class observations.
- Milestone 2A added lineage from source detections to track points and from track points to tracklets.
- Milestone 2B added a dynamic multi-run evidence bundle so the viewer can inspect tracklet evidence alongside source detection evidence.
- Milestone 2C added structured tracklet query and human review annotations.
- Milestone 2D added reusable review dataset exports.
- Milestone 2E completed the invariant audit and closeout review.

## Completion Statement

Blueprint 2 proved that TOM v3 can compose persisted atomic detections into candidate temporal evidence, persist tracklet and track point observations with lineage to source detections, inspect that evidence across runs, review it with non-mutating annotations, query it through structured filters, and export it as a review dataset artifact without adjudicating correctness.

Blueprint 2 did not add pose, homography, bounce, hit, rally, point, scoring, identity proof, or truth promotion.

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
-> structured query
-> review annotation
-> review dataset export
```

## Core Rule

Tracklet evidence is descriptive. It records that a grouping algorithm associated persisted detections over time.

It does not prove object identity, object path, bounce, hit, rally, point state, or score.

## Milestone Path

- 2A: Tracklet candidate observation spine and lineage.
- 2B: Tracklet viewer / multi-run evidence bundle.
- 2C: Tracklet query and review.
- 2D: Tracklet evidence export / review dataset foundation.
- 2E: Blueprint 2 completion review / temporal evidence hardening.

## Naming Note

The original implementation branch and some historical references use `1F` for the tracklet foundation work. That work is canonically Milestone 2A because temporal grouping begins Blueprint 2.
