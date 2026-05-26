# TOM v3 Simple - Milestone 2C Handoff

## Mission

Implement the first query and review workflow for tracklet candidates.

## Required Outcome

```text
tracklet candidates
-> structured query
-> evidence bundle
-> review annotations
-> viewer review panel
```

## Required Boundaries

TOM v3 remains observation-only. Review labels are human annotations about persisted observations. They do not mutate source detections, track point candidates, tracklet candidates, lineage, or frame artifacts.

## Deliverables

- Tracklet query service.
- `POST /tracklets/query`.
- Evidence bundle annotation summaries.
- Viewer review controls for selected tracklet evidence.
- Tracklet query/review docs.
- Agent report.

## Recommended Next Handoff

Milestone 2D - Tracklet Evidence Export / Review Dataset Foundation.
