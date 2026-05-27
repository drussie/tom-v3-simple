# Milestone 8E Handoff - Court Overlay in Replay Workstation

## Result

Milestone 8E is complete.

TOM can now open the replay workstation with:

```text
/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>
```

and display persisted court keypoint evidence, court line evidence, camera/view evidence, and homography candidate geometry overlays.

## Implemented

- Replay API court run and homography run filters.
- Replay-info court and homography run summaries.
- Court keypoint, court line, camera/view, and homography candidate overlay payloads.
- Court evidence timeline lanes.
- Frontend court overlay component.
- Court layer toggles and selected evidence detail.
- Documentation and tests for court replay overlays.

## Still Deferred

- Projection diagnostics.
- Ball/player court-space projection.
- Real court/camera model inference.
- Bounce/hit/in-out/rally/point/scoring.
- Real stream ingestion.
- Adjudication.

## Recommended Next Handoff

Milestone 8F - Projection Diagnostics / Review Export
