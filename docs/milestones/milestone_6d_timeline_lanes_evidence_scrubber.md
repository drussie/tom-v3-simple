# Milestone 6D - Timeline Lanes / Evidence Scrubber

Status: complete

## Goal

Add temporal navigation to the Blueprint 6 replay workstation.

The milestone proves:

```text
indexed video
-> synchronized overlays
-> timeline lanes
-> click-to-seek evidence
-> click-to-inspect persisted observations
```

## Delivered

- `GET /replay/timeline`
- detection observation timeline ticks
- tracklet candidate timeline spans
- pose observation timeline ticks
- review annotation markers when target frame/time is available
- frontend evidence lane stack with current playhead
- click-to-seek/select behavior for timeline items
- selected detail display for timeline-selected evidence
- timeline empty states
- backend API tests for lanes, filters, flags, and missing media

## Evidence Boundary

Timeline lanes are navigation aids over persisted evidence. They do not classify
tennis actions, confirm object identity, reconstruct points, or adjudicate
official tennis meaning.

## Non-Goals Preserved

- no stream proxy mode
- no live stream ingestion
- no model/runtime expansion
- no real pose inference
- no movement interpretation
- no homography
- no bounce/hit/rally/point/scoring
- no adjudication

## Next Handoff

Milestone 6E - Stream Proxy Mode
