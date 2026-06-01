# Ball Trajectory 3D Candidate Evidence v0

`ball_trajectory_3d_candidate` rows are provisional geometry evidence derived from:

- `ball_trajectory_court_candidate` source points
- `ball_court_projection_candidate` source image points, when available
- `camera_geometry_evidence` declared court dimensions

## Coordinate Meaning

The v0 metric conversion is declared-assumption geometry:

```text
court_x_m = court_x * declared court width
court_y_m = court_y * declared court length
```

These coordinates are useful for future diagnostics, but they are not calibrated 3D truth.

## Height

Default:

```text
height_model = none_unknown
court_z_m = null
court_z_status = unknown
```

Optional placeholder:

```text
height_model = court_plane_placeholder
court_z_m = 0.0
court_z_status = court_plane_assumed
```

The placeholder mode means "on the declared court plane for diagnostic continuity." It does not mean
the ball was physically on the court or that a bounce occurred.

## Warnings

Every output carries:

- `trajectory_3d_candidate_only`
- `not_3d_truth`
- `not_camera_calibration_truth`
- `height_not_verified`
- `geometry_evidence_only`
- `does_not_change_event_candidates`
- `does_not_create_event_truth`
- `does_not_create_in_out`
- `does_not_create_score`
- `no_adjudication`

## Boundary

This layer does not create event truth, in/out, score, accepted/rejected lifecycle, automatic
correction, or adjudication. It is a read-only candidate evidence layer for future 3D-assisted
diagnostics.
