# Milestone 8C - Camera / View Evidence Layer

Status: IMPLEMENTED

Milestone 8C hardens camera/view evidence as a queryable geometry context layer.

## Delivered

```text
fixture court run
-> persisted camera_view_observation rows
-> camera/view query service
-> camera/view summary read model
-> camera/view evidence bundle
-> /court/camera-view API endpoints
```

## Scope

8C adds read/query visibility for camera/view evidence produced by 8B. It supports filters by media, run, time, frame, view label, motion hint, confidence, limit, and offset.

The summary read model counts view labels and motion hints, computes confidence/stability/cut metrics, and exposes candidate-only homography context hints.

The bundle exposes the observation spine, typed camera/view detail, media, run, model, runtime config, artifacts, annotations, and lineage context.

## Boundary

Camera/view observations are geometry context evidence only. They do not confirm the camera state or court geometry.

8C does not add homography computation, projection diagnostics, replay court overlays, real camera/court inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.
