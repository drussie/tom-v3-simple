# Milestone 4D - Pose Overlay Viewer

## Status

Status: complete.

## Goal

Make persisted pose evidence visually inspectable in the existing Evidence Viewer without adding real pose inference or movement interpretation.

## What Changed

- Added pose detail serialization to the viewer run payload.
- Added frontend pose observation types.
- Added pose overlay extraction and COCO17 edge helpers.
- Added a Pose Overlay panel and canvas.
- Rendered present keypoints, skeleton edges, and pose bbox from persisted `pose_observation` rows.
- Added selected pose metadata, source association candidate context, and a 17-keypoint evidence table.
- Added a pose timeline row.
- Kept the existing detection overlay and viewer selection model intact.

## Evidence Boundary

A pose observation means a pose adapter produced keypoint evidence at a media-owned frame/time.

It does not mean subject identity, player action, serve mechanics, hit, rally, point, scoring, biomechanics, or movement conclusions are known.

## Validation

Focused pose persistence tests and web type checking validate that viewer payloads include pose detail and the frontend accepts the pose overlay contract.

## Next

Recommended next milestone: Milestone 4E - Pose Query / Review / Export Integration.
