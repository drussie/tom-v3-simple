# TOM v3 Simple - Milestone 1C YOLO26 Ball / Player Observation Adapter

## Goal

Implement the first ball/player detector adapter seam for TOM v3 Simple.

Target flow:

```text
indexed media_asset
-> optional gameplay scope
-> detection adapter
-> ball_detection / player_detection observations
-> ObservationWriter
-> query API and viewer observation detail
```

## Scope

Milestone 1C adds:

- detection adapter interface
- YOLO26/Ultralytics portability assessment
- YOLO unavailable stub when runtime/assets are unavailable
- deterministic fixture detector for tests and development
- worker detection adapter service
- worker `run-detection-adapter` command
- worker `index-and-run-detection` convenience command
- atomic observation persistence through `ObservationWriter`
- optional scoped lineage to gameplay observations
- query/viewer compatibility tests
- docs and runbook updates

## YOLO26 Status

YOLO26 runtime/assets were not available in this repo/environment.

The real YOLO adapter is therefore represented by a clear unavailable stub. The fixture adapter proves the TOM v3 persistence, query, and viewer path.

## Non-Goals

- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No streaming ingestion.
- No production deployment.
- No adjudication.

## Acceptance

Status: complete.

Milestone 1C is complete because:

- detection adapter interface exists
- YOLO26/Ultralytics portability assessment exists
- YOLO adapter stub exists with clear unavailable behavior
- fixture detection adapter exists
- detection adapter service creates model, config, run, and step records
- fixture output persists typed atomic observations through `ObservationWriter`
- fixture output includes ball_detection and player_detection observations
- detection timestamps derive from TOM v3 media frame/time utilities
- worker CLI command exists
- query API retrieves detection observations
- viewer payload includes detection observations
- tests cover adapter and persistence flow

## Ready For Next

Recommended next milestone: Milestone 1D - Detection Overlay / Visual Observation Layer.

Reason: detector observations are now queryable and present in the viewer payload. The next useful step is visualizing bbox evidence without adding tracking or higher-level interpretation.
