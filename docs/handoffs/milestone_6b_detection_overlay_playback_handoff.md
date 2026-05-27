# Milestone 6B Handoff - Detection Overlay Playback

## Starting State

Milestone 6A created the replay workstation foundation:

```text
indexed media
-> replay-info endpoint
-> local media video endpoint
-> /replay/<media_id>
-> HTML video player
-> current timestamp/frame display
-> timeline shell
-> available run context
```

## 6B Result

Milestone 6B adds detection overlay playback:

```text
current replay timestamp/frame
-> detection overlay chunk endpoint
-> persisted ball/player bbox overlays
-> detection layer toggle
-> detection run selection
-> click-to-select detection observation detail
```

## Implementation Notes

- Backend endpoint: `GET /replay/overlays`.
- Supported layer in 6B: `layers=detections`.
- Supported detection types: `ball_detection`, `player_detection`.
- Coordinates: original media `image_pixels`.
- Replay page route: `/replay/<media_id>`.
- Detection run selection: `?detectionRunId=<run_id>` or run selector.
- Display hold is visual only; persisted observations are not changed.

## Deferred

- Tracklet overlay playback.
- Pose overlay playback.
- Evidence timeline lanes.
- Live stream ingestion.
- Tennis-event interpretation.

## Next Recommended Handoff

Milestone 6C - Tracklet / Pose Overlay Playback
