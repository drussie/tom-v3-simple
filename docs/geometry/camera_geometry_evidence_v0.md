# Camera Geometry Evidence v0

Camera Geometry Evidence v0 is TOM v3's first explicit 3D-readiness contract.

The record lives in `camera_geometry_evidence` and can be linked to:

- `media_id`
- `court_run_id`
- `court_projection_run_id`
- `homography_run_id`
- `geometry_run_id`

## Declared ITF Court Dimensions

When `court_model=itf_standard_tennis_court`, TOM stores these declared dimensions in meters:

- court length: 23.77
- singles width: 8.23
- doubles width: 10.97
- net height center: 0.914
- net height posts: 1.07

These constants are declared geometry metadata, not verified geometry for a specific video.

## Coordinate Convention

The v0 world-coordinate convention is explicit:

- `court_x`: left/right across the declared court
- `court_y`: near/far along the declared court
- `court_z`: meters above the declared court plane
- `z_axis`: positive up from the court plane
- `origin`: declared near-left doubles corner

The convention prepares future 3D layers, but v0 does not create 3D ball trajectories.

## Integrations

Replay info exposes a compact `camera_geometry_summary` when geometry exists.

Point evidence snapshots include `camera_geometry_summary`.

Point candidate evaluations include `geometry_readiness`.

All integrations are read-only and do not change generated candidate evidence or review labels.

## Boundary

This layer is geometry evidence only. It is not camera calibration truth, 3D reconstruction, hit
truth, bounce truth, in/out, score, point state, accepted/rejected lifecycle, or adjudication.

