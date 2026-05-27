# Milestone 6F - Blueprint 6 Completion Review

Status: COMPLETE

Date: 2026-05-27

## Mission

Close Blueprint 6 without adding new product capability.

Milestone 6F verifies and documents that TOM v3's visual replay/operator workstation is complete for indexed local media, persisted evidence overlays, evidence timeline navigation, and Stream Proxy Mode.

## Completion Summary

Blueprint 6 is complete.

TOM v3 can now:

- open indexed local media in `/replay/<media_id>`
- play video in Replay Mode
- play video in Stream Proxy Mode
- synchronize playback time to TOM media-owned timestamp/frame
- render persisted detection observation overlays
- render persisted tracklet candidate overlays
- render persisted pose keypoint overlays
- show evidence timeline lanes
- seek/select persisted evidence from timeline items
- select persisted evidence from overlay clicks
- hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it

## Non-Goals Preserved

Milestone 6F does not add:

- real live stream ingestion
- HLS/RTSP/HDMI/camera capture
- stream backend/session tables
- websocket live updates
- live model scheduling
- real pose inference
- movement interpretation
- homography
- bounce/hit/rally/point/scoring
- TOM v2-style adjudication

## Final Status Updates

This milestone marks Blueprint 6 COMPLETE in:

- `README.md`
- `docs/CONTROL_ROOM.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/blueprints/tom_v3_blueprint_6_visual_replay_live_observation_workstation.md`

## Validation Scope

Final validation covers:

- Python tests
- Ruff
- web lint/build/audit
- Alembic smoke
- synthetic viewer smoke
- fixture demo
- completion audit
- Replay Mode smoke notes
- Stream Proxy Mode smoke notes

## Recommended Next Step

Stop Blueprint 6. Use and demo the replay workstation.

Future work should begin as separate blueprints only if deliberately chosen.
