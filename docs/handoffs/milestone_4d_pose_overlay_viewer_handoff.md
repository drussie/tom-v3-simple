# Milestone 4D Handoff - Pose Overlay Viewer

## Starting State

Milestone 4C persisted fixture pose observations through a worker processing-run path and added lineage to source player detections when candidate context was supplied.

## Mission

Make persisted pose evidence visually replayable in the existing Evidence Viewer.

## Required Work

- Include typed pose detail in the viewer payload.
- Add frontend pose types and overlay model helpers.
- Render COCO17 keypoints and skeleton edges from persisted coordinates.
- Show missing keypoints as missing evidence, not overlay markers.
- Show selected pose metadata and keypoint confidence detail.
- Show source association candidate context when present.
- Preserve the existing detection overlay.
- Update docs and tests.

## Non-Goals

- No real pose inference.
- No pose review UI.
- No pose export integration.
- No movement interpretation.
- No tennis-event candidates.
- No homography, bounce, hit, rally, point, scoring, or adjudication.

## Implemented Result

Milestone 4D adds a pose overlay panel to the existing Evidence Viewer. Persisted pose observations now appear in `/viewer/runs/{run_id}`, render as image-pixel keypoint evidence, and expose selected pose details, keypoint confidence rows, and source candidate context.

## Next Handoff

Milestone 4E - Pose Query / Review / Export Integration.
