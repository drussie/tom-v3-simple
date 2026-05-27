# Milestone 6B - Detection Overlay Playback

## Status

Status: COMPLETE

## Mission

Add the first synchronized replay overlay layer:

```text
indexed video playback
-> current media-owned timestamp/frame
-> detection overlay chunk lookup
-> persisted ball/player bbox overlays
-> click-to-select detection observation detail
```

This milestone renders persisted `ball_detection` and `player_detection`
observations over replay video. It does not interpret tennis events.

## Implemented

- `GET /replay/overlays` for replay overlay chunks.
- Detection overlay payload service for media/time-window lookup.
- Detection run filtering with `detection_run_id`.
- Display-only `min_confidence` filtering.
- Normalized bbox payloads in `image_pixels` coordinate space.
- Replay page detection overlay chunk fetching and caching.
- Detection layer toggle and detection run selector.
- Contained-video coordinate scaling for overlay boxes.
- Click-to-select detection detail panel.
- Loaded-chunk detection timeline ticks.
- Backend tests for overlay endpoint behavior.

## Boundaries

6B does not add:

- tracklet overlay playback
- pose overlay playback
- live stream ingestion
- new model/runtime behavior
- homography
- bounce or hit detection
- rally/point/scoring
- adjudication

Detection boxes remain observation evidence, not confirmed tennis state.
