# TOM v3 Simple - Milestone 1B TOM v1 Gameplay Detector Adapter

## Goal

Implement the first gameplay/view-state observation adapter seam for TOM v3 Simple.

Target flow:

```text
indexed media_asset
-> gameplay adapter
-> gameplay / non_gameplay / uncertain segments
-> ObservationWriter
-> gameplay_observation rows
-> viewer gameplay timeline band
```

## Scope

Milestone 1B adds:

- gameplay adapter interface
- TOM v1 portability assessment
- TOM v1 adapter stub when portable assets are unavailable
- deterministic fixture adapter for tests and development
- worker gameplay adapter service
- worker `run-gameplay-adapter` command
- worker `index-and-run-gameplay` convenience command
- gameplay observation persistence through `ObservationWriter`
- viewer compatibility tests
- docs and runbook updates

## TOM v1 Status

Portable TOM v1 detector source, weights, and callable entrypoint were not available in this repo/environment.

The real TOM v1 adapter is therefore represented by a clear integration stub. The fixture adapter proves the TOM v3 persistence and viewer path.

## Non-Goals

- No YOLO integration.
- No ball tracking.
- No player tracking.
- No pose tracking.
- No court homography.
- No bounce detection.
- No point/rally reconstruction.
- No scoring.
- No streaming ingestion.
- No production deployment.
- No adjudication.

## Acceptance

Status: complete.

Milestone 1B is complete because:

- gameplay adapter interface exists
- TOM v1 portability assessment exists
- TOM v1 adapter stub exists with clear unavailable behavior
- fixture gameplay adapter exists
- gameplay adapter service creates model, config, run, and step records
- fixture output persists typed gameplay observations through `ObservationWriter`
- labels include gameplay, non_gameplay, and uncertain
- segment timestamps derive from TOM v3 media frame/time utilities
- worker CLI command exists
- viewer payload includes gameplay observations from adapter runs
- tests cover adapter and persistence flow

## Ready For Next

Recommended next milestone: Milestone 1C - YOLO26 Ball/Player Observation Adapter.

Reason: the real media substrate and gameplay adapter seam now exist. Ball/player detection can be added as atomic observations while preserving the observation-only boundary.
