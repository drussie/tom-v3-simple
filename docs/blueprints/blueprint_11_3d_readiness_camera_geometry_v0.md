# Blueprint 11 - 3D Readiness / Camera Geometry Evidence Layer v0

Blueprint 11 adds persistent camera/court geometry evidence so future 3D work has explicit
assumptions to inspect.

This is not 3D reconstruction.

It records:

- declared court model and dimensions
- camera model/status declarations
- unknown intrinsics/extrinsics placeholders
- optional court, homography, and court-projection run linkage
- world-coordinate convention metadata
- capability flags that keep true 3D unavailable

## Command

```bash
.venv/bin/python -m apps.worker.cli declare-camera-geometry \
  --media-id <media_id> \
  --court-run-id <court_run_id> \
  --court-projection-run-id <court_projection_run_id> \
  --homography-run-id <homography_run_id> \
  --court-model itf_standard_tennis_court \
  --camera-model homography_backed_court_plane \
  --geometry-status declared \
  --viewer-base-url http://127.0.0.1:3000
```

Make helper:

```bash
make tom-v1-declare-camera-geometry \
  MEDIA_ID=<media_id> \
  COURT_RUN_ID=<court_run_id> \
  COURT_PROJECTION_RUN_ID=<court_projection_run_id> \
  HOMOGRAPHY_RUN_ID=<homography_run_id>
```

## Geometry Status

Allowed status values:

- `declared`
- `partial`
- `estimated`
- `unknown`
- `invalid`

Truth-like labels such as `true_camera_pose`, `calibrated_truth`, or `verified_3d` are rejected.

## Boundary

Camera geometry evidence is declared or estimated metadata. It is not 3D truth, does not produce
3D ball trajectories, does not change hit/bounce candidates, does not decide in/out, does not score
a point, and does not adjudicate evidence.

