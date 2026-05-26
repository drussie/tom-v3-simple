# Milestone 4C - Pose Observation Persistence and Lineage

## Status

Status: complete.

## Goal

Persist normalized pose payloads through a worker pose processing-run path and connect pose evidence to source subject evidence when candidate context is supplied.

## What Changed

- Added a fixture pose worker service.
- Added worker `run-pose-adapter`.
- Created pose `processing_run` and `processing_step` records.
- Persisted normalized pose payloads through `ObservationWriter`.
- Wrote first-class `pose` observation spine rows and typed `pose_observation` rows.
- Added lineage from source `player_detection` observations to pose observations.
- Added reserved relationship names for tracklet and track point pose context.
- Added tests for unassociated full-frame fixture poses, source detection lineage, invalid explicit source ids, and CLI smoke behavior.

## Evidence Boundary

A pose observation means a pose adapter produced keypoint evidence at a media-owned frame/time.

It does not mean subject identity, player action, serve mechanics, hit, rally, point, scoring, or movement conclusions are known.

## Validation

Focused pose persistence and lineage tests pass in the base environment without pose weights or real pose runtime.

## Next

Recommended next milestone: Milestone 4D - Pose Overlay Viewer.
