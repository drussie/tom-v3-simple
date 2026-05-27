# Milestone 6D Handoff - Timeline Lanes / Evidence Scrubber

Status: complete

## Starting Point

Milestone 6C added synchronized detection, tracklet candidate, and pose keypoint
overlay playback in the replay workstation.

## Completed in 6D

```text
indexed video playback
-> synchronized overlays
-> replay timeline endpoint
-> detection ticks
-> tracklet candidate spans
-> pose ticks
-> review annotation markers
-> click-to-seek/select persisted evidence
```

## Implementation Notes

- Backend timeline data is exposed through `GET /replay/timeline`.
- Timeline run filters mirror replay overlay run filters:
  `detection_run_id`, `tracklet_run_id`, and `pose_run_id`.
- Annotation markers are included when a review annotation can be mapped to a
  media-owned frame/time through either the annotation or its target
  observation.
- Frontend timeline lanes are fetched when selected runs change, not on every
  frame.
- Timeline item clicks create a seek request for `ReplayVideoPlayer` and update
  the selected evidence panel.

## Non-Goals Preserved

- no stream proxy mode
- no live stream ingestion
- no new model/runtime behavior
- no real pose inference
- no movement interpretation
- no homography
- no bounce/hit/rally/point/scoring
- no adjudication

## Recommended Next Handoff

Milestone 6E - Stream Proxy Mode
