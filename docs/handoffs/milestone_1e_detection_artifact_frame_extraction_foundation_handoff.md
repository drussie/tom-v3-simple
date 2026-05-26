# TOM v3 Simple - Milestone 1E Handoff

## Detection Artifact / Frame Extraction Foundation

Repo: `drussie/tom-v3-simple`

Branch: `codex/m1e-detection-artifact-frame-extraction-foundation`

## Mission

Implement the first frame artifact extraction foundation so persisted detection observations can be inspected over real extracted frame imagery.

## Target Flow

```text
indexed media
-> detection run
-> persisted detection observations
-> selected detection frame
-> extracted frame image artifact
-> persisted evidence_artifact metadata
-> viewer frame image behind bbox overlay
```

## In Scope

- ffmpeg frame extraction primitive
- worker frame artifact extraction service
- worker `extract-frame-artifacts` command
- local artifact storage under `.data/artifacts`
- persisted `frame_image` and `detection_frame_image` artifact rows
- artifact content route for local development
- viewer frame artifact matching
- coordinate canvas fallback
- docs and tests

## Out of Scope

- Real YOLO inference.
- Tracking.
- Pose detection.
- Court homography.
- Bounce detection.
- Hit detection.
- Rally segmentation.
- Point reconstruction.
- Scoring.
- Production object storage.
- Streaming.
- Adjudication.

## Completion Notes

Frame artifacts make detection observations easier to inspect. They do not make detections correct, create tracks, or infer tennis events.
