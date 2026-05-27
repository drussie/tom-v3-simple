# TOM v3 Blueprint 7 Completion Review

## Status

Blueprint 7 Status: COMPLETE

## Completion Verdict

Blueprint 7 is complete enough to stop.

It completes TOM v3's real perception runtime for the replay workstation. TOM can now run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output detection evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation.

Blueprint 7 remains observation-only and non-adjudicative. It does not add court/homography implementation, bounce/hit/rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, or TOM v2-style adjudication.

Court/camera/homography evidence is deferred to Blueprint 8.

## Final Perception Ladder

```text
indexed media
-> optional real YOLO detection run
-> real ball/player detection observations
-> replay detection overlays
-> candidate tracklets from real detections
-> source detection lineage
-> optional real pose run
-> COCO17 player pose observations
-> source player detection lineage when available
-> replay detection / tracklet / pose overlays
```

## Completion Review Questions

### 1. Is Blueprint 7 complete enough to stop?

Yes. Blueprint 7 has delivered the planned real perception replay ladder through detection observations, real-detection-derived candidate tracklets, and real pose keypoint evidence. The remaining court/camera/homography work is explicitly deferred to Blueprint 8.

### 2. What does TOM v3 real perception support now?

TOM v3 supports optional real YOLO detection replay, candidate tracklet generation from real detection observations, and optional real pose replay. All outputs persist as observations or candidate evidence with media-owned frame/time, model/runtime metadata, and replay workstation integration.

### 3. What does `run-real-detection` do?

`run-real-detection` validates optional runtime and weights, samples indexed media frames, maps model output classes into TOM detection observation types, persists `ball_detection` and `player_detection` observations, records model/runtime metadata, and prints a replay URL with `detectionRunId`.

### 4. What does real detection replay show?

The replay workstation can show real model-output detection bounding boxes over video playback, label real detection runs separately from fixture runs, expose model/runtime/config/class context, and keep the evidence-only boundary visible.

### 5. What does real-detection-derived tracklet generation do?

The existing tracklet builder can consume a real detection run and create candidate tracklets plus track point candidates. It does not introduce a new tracking model or path correctness claim.

### 6. What lineage is preserved from track points to real detections?

Track point candidates preserve source detection observation ids and lineage back to the real detection observations that produced them. Replay payloads and selected detail panels can show source detection run/runtime/evidence metadata when available.

### 7. What does `run-real-pose` do?

`run-real-pose` validates optional pose runtime and local weights, runs crop-from-player-detection or full-frame pose inference, normalizes COCO17 keypoints, persists `player_pose_observation` rows, records model/runtime metadata, and prints a replay URL with `poseRunId`.

### 8. How are pose observations linked to source player detections?

In crop-from-player-detection mode, pose observations use source `player_detection` frame/time, keep subject association candidate metadata, and write `pose_from_subject_detection_candidate` lineage back to the source player detection observation.

### 9. What does the replay workstation show now?

The replay workstation can show persisted detection overlays, candidate tracklet points/paths, pose keypoint/skeleton overlays, evidence timeline lanes, click-to-seek, click-to-select, and Stream Proxy Mode. Blueprint 7 adds source-aware real detection, tracklet, and pose run metadata to that existing workstation.

### 10. What remains fixture/demo only?

The default `make demo` path remains fixture-safe and does not require YOLO or pose weights. Fixture gameplay, fixture detections, fixture pose observations, seeded annotations, and exports remain deterministic demo evidence for local validation.

### 11. What requires local optional weights?

Real detection replay requires local YOLO detection weights and optional runtime dependencies. Real pose replay requires local pose weights and optional runtime dependencies. Default CI and fixture demo do not require these weights.

### 12. What does default CI require?

Default CI requires the base TOM v3 development environment, Python dependencies, web dependencies, migrations, and fixture/synthetic assets. It does not require YOLO weights, pose weights, GPU runtime, Ultralytics, Torch, OpenCV, or network access.

### 13. What does Blueprint 7 intentionally not do?

Blueprint 7 does not add court/homography implementation, bounce detection, hit detection, rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, production deployment, or TOM v2-style adjudication.

### 14. Why is court/homography deferred to Blueprint 8?

Court/camera/homography is a distinct geometry evidence layer. It needs its own evidence family, schema contracts, confidence model, replay overlays, diagnostics, exports, and review workflow. Keeping it out of Blueprint 7 prevents perception runtime closeout from drifting into court-space or tennis-event interpretation.

### 15. What future blueprint candidates remain?

Future candidates include Blueprint 8 for court/camera/homography evidence, bounce/hit candidate evidence, movement/stroke evidence candidates, real stream ingestion, product deployment, and model-quality/evaluation workflows.

## Final Validation Summary

Final validation is recorded in the Milestone 7F agent report.

## Non-goals Preserved

Blueprint 7 closes without adding court/homography runtime, database migrations for court evidence, court overlays, bounce/hit/rally/point/scoring, movement/stroke interpretation, real stream ingestion, or adjudication.
