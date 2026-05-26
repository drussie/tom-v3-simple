# TOM v3 Simple - Milestone 1E Detection Artifact / Frame Extraction Foundation

## Goal

Add frame image artifacts so persisted detection observations can be inspected over real extracted frame imagery.

Target flow:

```text
indexed media
-> detection run
-> persisted detection observations
-> selected detection frame
-> extracted frame image artifact
-> evidence_artifact metadata
-> viewer displays frame image behind bbox overlay
```

## Scope

Milestone 1E adds:

- ffmpeg-based frame extraction service
- local frame artifact storage under `.data/artifacts`
- worker `extract-frame-artifacts` command
- `evidence_artifact` rows for shared frame images and detection-targeted frame images
- local artifact content route
- viewer frame artifact matching and image display
- coordinate canvas fallback when no frame artifact exists
- tests and docs

## Frame/Time Ownership

Frame extraction uses TOM v3 media indexing:

- `media_asset.fps`
- `frame_to_timestamp_ms`
- `metadata_jsonb.frame_time_index`

Frame artifact metadata stores `frame_time_owner = media_indexing`.

## Non-Goals

- No real YOLO inference.
- No automatic extraction for every video frame.
- No tracking.
- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally segmentation.
- No point reconstruction.
- No scoring.
- No production object storage.
- No adjudication.

## Acceptance

Status: complete.

Milestone 1E is complete because:

- frame extraction service exists
- missing ffmpeg failure is clear and actionable
- worker `extract-frame-artifacts` command exists
- frame artifacts are written to local `.data` storage
- `evidence_artifact` rows are persisted for extracted frames
- metadata includes media id, frame number, timestamp, frame-time owner, extraction method/version, and URI
- frame artifacts can target selected detection observations
- same-frame artifacts can support detections on the same frame
- viewer displays frame artifact imagery behind detection bboxes when available
- viewer falls back to the coordinate canvas when no frame artifact exists
- tests and validation pass

## Ready For Next

Recommended next milestone: Milestone 1F - Tracklet Foundation from Persisted Detections, unless YOLO26 runtime/assets become available and the user wants to prioritize real detector integration.

Reason: frame-backed detection inspection is now in place. If real YOLO remains unavailable, the next platform step is explicitly-approved temporal grouping from persisted detections.
