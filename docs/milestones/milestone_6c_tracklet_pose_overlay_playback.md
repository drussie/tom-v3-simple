# Milestone 6C - Tracklet / Pose Overlay Playback

Status: complete

## Summary

Milestone 6C extends the Blueprint 6 replay workstation from detection-only playback to all three TOM v3 Simple evidence layers:

```text
indexed video
-> current media-owned frame/time
-> persisted detection observations
-> persisted tracklet candidates / track points
-> persisted pose observations / keypoint evidence
-> synchronized replay overlays
-> click-to-inspect evidence
```

## What Was Added

- Replay overlay API support for `layers=tracklets,pose`.
- `tracklet_run_id`, `pose_run_id`, and display-only `min_pose_confidence` overlay filters.
- Normalized tracklet candidate payloads with persisted track point coordinates and source detection ids.
- Normalized pose overlay payloads with persisted keypoints, COCO17 edges, bbox context, and subject association candidate fields.
- Replay UI layer toggles for detections, tracklet candidates, and pose observations.
- Tracklet and pose run selection from replay info / query params.
- Candidate track point rendering and selected candidate path rendering over video.
- Pose bbox, present keypoint, and skeleton edge rendering over video.
- Click-to-select detail for detections, tracklet candidates, track point candidates, and pose observations.

## Boundaries Preserved

Tracklets remain candidate temporal groupings. Pose overlays remain keypoint evidence. This milestone does not add stream ingestion, full timeline lanes, real pose inference, homography, bounce/hit/rally/point/scoring, or adjudication.

## Next Handoff

Recommended next milestone: Milestone 6D - Timeline Lanes / Evidence Scrubber.
