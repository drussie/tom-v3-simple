# TOM v3 Simple - Milestone 2B Tracklet Viewer / Multi-Run Evidence Bundle

## Goal

Make tracklet candidate evidence inspectable across the tracklet builder run and the source detection run.

Target flow:

```text
tracklet candidate
-> track point candidates
-> source detection observations
-> frame artifacts
-> lineage
-> viewer drilldown
```

## Scope

Milestone 2B adds:

- dynamic tracklet evidence bundle service
- `GET /tracklets/{tracklet_id}/evidence-bundle`
- lineage-driven source detection lookup
- frame artifact matching for source detections
- viewer Tracklet Evidence panel
- source detection drilldown from selected track point
- docs and tests

## Acceptance

Status: complete when validation passes.

Milestone 2B is complete because:

- tracklet evidence bundle service exists
- evidence bundle endpoint exists
- bundle includes tracklet row and tracklet candidate observation
- bundle includes tracklet builder and source detection run metadata
- bundle includes track points and track point candidate observations
- bundle includes source detection observations
- bundle exposes `tracked_from` and `grouped_from` lineage
- bundle includes frame artifacts when available and succeeds when unavailable
- viewer can select a tracklet and display bundle evidence
- no new model intelligence or adjudication is added

## Ready For Next

Recommended next milestone: Milestone 2C - Tracklet Query and Review, unless real YOLO runtime/assets become available and the user chooses to prioritize that integration.
