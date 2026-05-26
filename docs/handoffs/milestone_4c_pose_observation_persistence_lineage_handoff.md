# Milestone 4C Handoff - Pose Observation Persistence and Lineage

## Starting State

Milestone 4B completed pose normalization for fake or serialized pose model output. Normalized outputs were compatible with `PoseObservationCreate`, but there was no worker pose processing-run path.

## Mission

Bridge normalized pose payloads into TOM v3's durable observation store while preserving the observation-only boundary.

## Required Work

- Add a pose processing service.
- Create pose `processing_run` and `processing_step` rows.
- Persist fixture normalized pose payloads through `ObservationWriter`.
- Persist typed `pose_observation` rows.
- Preserve media-owned frame/time.
- Link pose observations to source `player_detection` observations when supplied.
- Optionally support candidate tracklet and track point context lineage.
- Add a worker CLI command if low risk.
- Update docs and tests.

## Non-Goals

- No real pose inference.
- No pose runtime weights.
- No pose overlay viewer.
- No movement interpretation.
- No tennis-event candidates.
- No homography, bounce, hit, rally, point, scoring, or adjudication.

## Implemented Result

Milestone 4C adds the worker fixture pose service and CLI command. Full-frame fixture poses persist unassociated pose evidence. Source-detection-linked fixture poses create `pose_from_subject_detection_candidate` lineage to source `player_detection` observations. Explicit invalid source ids fail clearly.

## Next Handoff

Milestone 4D - Pose Overlay Viewer.
