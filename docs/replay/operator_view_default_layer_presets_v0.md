# Operator View Default Layer Presets v0

Status: implemented

This repair adds explicit replay layer presets so a URL with many run ids opens in a clean operator
view instead of a debug-heavy audit view.

## Presets

### Operator View

`viewPreset=operator` is the default when no preset is supplied.

Operator view prefers stable replay candidates and hides raw/debug geometry by default:

- smoothed ball candidate on when `motionSmoothingRunId` exists
- smoothed near/far player boxes on when `motionSmoothingRunId` exists
- smoothed pose candidates on when `motionSmoothingRunId` exists
- mapped TOM v3 court keypoints on when `courtRunId` exists
- court line evidence on when `courtRunId` exists
- court temporal persistence set to `carry_forward`
- court projection mini-map on when `courtProjectionRunId` exists
- raw detections, raw tracklets, raw poses, raw TOM v1 keypoints, homography overlays,
  projection diagnostics, and camera/view evidence off by default when stable candidate layers exist

Pose visual style defaults to `limbs_only`. Smoothed motion display defaults to `current_only`.

### Debug / Audit View

`viewPreset=debug` applies a deliberately busy audit preset:

- raw detection observations on when a detection run exists
- tracklets, trails, and raw pose on when those runs exist
- main-player track labels on when a track run exists
- raw TOM v1 court keypoints, mapped keypoints, court lines, camera/view evidence, homography
  candidates, and projection diagnostics on when their runs exist
- smoothed layers and court projection mini-map remain available when their runs exist

Operators can still manually toggle individual layers after applying either preset.

## URL Parameter

```text
/replay/<media_id>?viewPreset=operator
/replay/<media_id>?viewPreset=debug
```

If omitted, replay uses `operator`.

## Boundary

Presets are UI/read-model display policy only. They do not create, mutate, delete, accept, or reject
observations. They do not change model outputs, homography math, projection math, lineage, or truth
status. All visible layers remain persisted evidence or derived candidate evidence, not adjudication.

## Non-Goals

This repair does not add bounce, hit, in/out, rally, point, score, player identity, scoreboard OCR,
server/receiver logic, accepted/rejected lifecycle, or TOM v2-style adjudication.
