# Milestone 8F Handoff - Projection Diagnostics / Review Export

## Result

Milestone 8F is complete.

TOM can now build projection diagnostic observations from homography candidate runs and export a TOM-native court review dataset.

## Implemented

- Projection diagnostic builder service.
- Worker `build-projection-diagnostics` CLI.
- Makefile `projection-diagnostics` helper.
- Projection diagnostic persistence through `ObservationWriter`.
- Lineage from homography candidates to projection diagnostics.
- Replay payload and workstation support for `projectionDiagnosticRunId`.
- Court review export service and `export-court-review-dataset` CLI.
- Makefile `court-review-export` helper.
- Documentation and tests for diagnostics, replay payloads, and exports.

## Still Deferred

- Ball/player court-space projection.
- Tracklet court-space projection.
- Bounce/hit/in-out/rally/point/scoring.
- Real court/camera model inference.
- Accepted/rejected court lifecycle.
- Real stream ingestion.
- Adjudication.

## Recommended Next Handoff

Milestone 8G - Blueprint 8 Completion Review
