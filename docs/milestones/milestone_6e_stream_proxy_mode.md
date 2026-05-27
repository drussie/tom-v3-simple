# Milestone 6E - Stream Proxy Mode

Status: COMPLETE

Milestone 6E adds a live-like operator mode to the replay workstation without adding stream ingestion.

## Proof Path

```text
indexed video replay
-> Replay / Stream Proxy mode toggle
-> video-as-live live edge
-> future overlay filtering
-> future timeline filtering
-> available evidence counts
-> pause/review state
-> return-to-live-edge action
```

## What Changed

- `/replay/<media_id>` accepts `mode=stream_proxy`.
- The replay workstation can switch between Replay Mode and Stream Proxy Mode.
- Stream Proxy Mode starts at media time zero.
- The live-like edge advances only as playback reaches media time.
- Future detection, tracklet, pose, and annotation timeline evidence is hidden until the live-like edge reaches it.
- Future detection, tracklet, and pose overlays are hidden until available.
- Native video seeking is clamped to the current live-like edge.
- The workstation shows live edge, operator time, lag, available evidence counts, and paused-review state.
- The workstation can return to the current live-like edge.

## Boundaries

Stream Proxy Mode is a UI/operator behavior over indexed local media and already-persisted evidence. It is not real live ingestion.

Milestone 6E does not add HLS, RTSP, HDMI capture, webcam ingestion, websocket updates, model scheduling, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or adjudication.

## Validation

Validation results are recorded in `docs/agent_reports/milestone_6e_stream_proxy_mode_report.md`.
