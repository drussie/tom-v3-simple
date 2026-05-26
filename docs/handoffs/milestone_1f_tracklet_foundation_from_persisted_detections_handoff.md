# TOM v3 Simple - Milestone 1F Handoff

## Tracklet Foundation From Persisted Detections

Repo: `drussie/tom-v3-simple`

Branch: `codex/m1f-tracklet-foundation-from-persisted-detections`

## Mission

Implement the first tracklet foundation for TOM v3 Simple by grouping persisted detection observations into explicit candidate temporal groupings.

## Target Flow

```text
persisted ball/player detections
-> tracklet builder
-> tracklet rows
-> track_point rows
-> source links to detection observations
-> viewer/query support
```

## In Scope

- Tracklet builder service.
- Deterministic frame-gap grouping policy.
- Ball tracklet candidates.
- Player tracklet candidates by label where available.
- Tracklet and track point persistence.
- Runtime config, model registry, processing run, and processing step records.
- Worker `build-tracklets` command.
- Viewer/query compatibility.
- Tests and docs.

## Out of Scope

- Sophisticated tracking.
- Optical flow.
- Pose detection.
- Court homography.
- Bounce detection.
- Hit detection.
- Rally segmentation.
- Point reconstruction.
- Scoring.
- Adjudication.

## Completion Notes

The tracklet builder creates candidate temporal groupings from persisted detections. It does not prove identity, correctness, bounce, hit, rally, or point state.
