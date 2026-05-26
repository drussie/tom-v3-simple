# TOM v3 Simple - Milestone 2C Tracklet Query and Review

## Goal

Milestone 2C makes tracklet candidates searchable and reviewable without mutating observations.

The target workflow is:

```text
tracklet candidates
-> structured query filters
-> review list
-> evidence bundle inspection
-> human annotations on tracklet / track point / source detection observations
-> review status visible
```

## In Scope

- `POST /tracklets/query`
- structured tracklet filters
- annotation summaries for tracklet evidence bundles
- review labels for tracklets, track points, and source detections
- viewer review controls in the Tracklet Evidence panel
- docs and tests

## Non-Goals

- No new tracking algorithm.
- No pose or court homography.
- No bounce or hit detection.
- No rally, point, or score reconstruction.
- No adjudication.

## Acceptance

Milestone 2C is complete when tracklet candidates can be filtered by run/source/type/frame/confidence/gap/point-count fields, review annotations can target candidate observations, and the viewer can add and display review annotations while preserving observation immutability.
