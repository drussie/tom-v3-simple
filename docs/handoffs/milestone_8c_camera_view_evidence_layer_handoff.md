# Milestone 8C Handoff - Camera / View Evidence Layer

## Starting State

Milestone 8B accepted and merged to main. Fixture court runs can persist court keypoint, court line, and camera/view observations.

## Mission

Make `camera_view_observation` rows operational as queryable, inspectable geometry context evidence without adding new writer behavior, homography computation, projection diagnostics, or replay overlays.

## Implemented Path

```text
run-fixture-court
-> camera_view_observation rows
-> query_camera_view_observations
-> summarize_camera_view_evidence
-> build_camera_view_evidence_bundle
-> /court/camera-view endpoints
```

## Validation Focus

- Query filters by media/run/time/frame/view/motion/confidence.
- Summary counts labels and motion hints.
- Summary computes basic confidence/stability/cut metrics.
- Bundle returns observation spine, typed camera detail, run/model/runtime context, artifacts, annotations, and lineage.
- Fixture court adapter behavior remains unchanged.

## Preserved Non-Goals

No homography computation, no projection diagnostics, no replay court overlay, no real camera/court model, no ball/player court projection, and no tennis-event interpretation.

## Next Handoff

Milestone 8D - Homography Candidate Persistence.
