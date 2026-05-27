# Milestone 6C Handoff - Tracklet / Pose Overlay Playback

## Status

Complete.

## Implemented Path

```text
video replay
-> overlay chunk lookup
-> detection bbox overlays
-> tracklet candidate point/path overlays
-> pose keypoint/skeleton overlays
-> click-to-select persisted evidence details
```

## Key Decisions

- `/replay/overlays` remains the single replay overlay endpoint.
- `layers=detections,tracklets,pose` selects which evidence families are returned.
- Tracklet payloads include persisted points only; no interpolation or smoothing is performed.
- Pose payloads include persisted keypoints and COCO17 registry edges; missing keypoints are not drawn as present.
- Frontend coordinate scaling reuses the contained-video mapping from 6B.
- Display holds remain visual-only and do not alter persisted observations.

## Still Deferred

- Full evidence timeline lanes.
- Stream proxy mode or live ingestion.
- Annotated clip export.
- Any tennis-event interpretation.

## Recommended Next Milestone

Milestone 6D - Timeline Lanes / Evidence Scrubber.
