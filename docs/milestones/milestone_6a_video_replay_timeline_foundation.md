# Milestone 6A - Video Replay Timeline Foundation

## Status

Status: complete

## Goal

Create the foundation for the TOM v3 replay workstation:

```text
indexed media asset
-> browser-usable video URL
-> replay info payload
-> frontend replay route
-> HTML video player
-> current timestamp/frame display
-> timeline shell
```

## Implementation

Milestone 6A adds:

- replay info backend service and endpoint
- local media video endpoint for browser playback
- constant-frame-rate frame/time mapping helpers using indexed media metadata
- frontend `/replay/[mediaId]` route
- `ReplayVideoPlayer` component with native video controls
- current time, timestamp, nearest frame, fps, and frame count display
- overlay placeholder for future layers
- available run context grouped by detection, tracklet, pose, and gameplay evidence
- `make replay-open MEDIA_ID=<media_id>`

## Validation

Focused coverage includes:

- replay info returns media metadata, video URL, observation-only flags, and grouped runs
- video endpoint serves local indexed media and returns 404 for unavailable files
- timestamp/frame mapping clamps to media frame range
- replay route and player pass TypeScript validation

## Non-Goals Preserved

Milestone 6A does not add detection, tracklet, or pose overlay playback. It does not add stream ingestion, new model runtime behavior, tennis-event interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Next Handoff

Recommended next handoff:

Milestone 6B - Detection Overlay Playback
