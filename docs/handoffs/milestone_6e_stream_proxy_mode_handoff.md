# TOM v3 - Milestone 6E Handoff

## Stream Proxy Mode

Starting state: Milestone 6D Timeline Lanes / Evidence Scrubber accepted and merged to main.

Status: COMPLETE.

Milestone 6E added Stream Proxy Mode to the replay workstation.

## Completed Flow

```text
indexed video file
-> replay workstation
-> mode toggle: Replay / Stream Proxy
-> Stream Proxy starts at t=0
-> live-like edge advances with playback
-> future overlays hidden until available
-> future timeline evidence hidden until available
-> pause/review state
-> return-to-live-edge action
```

## Implementation Notes

- Frontend-only operator mode; no backend stream session state was added.
- `mode=stream_proxy` is supported on `/replay/<media_id>`.
- `make replay-open` can print replay URLs with `MODE=stream_proxy` and selected run IDs.
- Detection, tracklet, pose, and annotation evidence remain persisted evidence records.
- Stream Proxy Mode hides future evidence; it does not change persisted observations.

## Non-Goals Preserved

- No real live stream ingestion.
- No HLS/RTSP/HDMI/camera capture.
- No websocket live updates.
- No model scheduling.
- No tennis-event interpretation.
- No homography, bounce, hit, rally, point, scoring, or adjudication.

## Recommended Next Handoff

Milestone 6F - Operator Review Workflow Hardening.
