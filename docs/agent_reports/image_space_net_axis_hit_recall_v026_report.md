# Image-Space Net-Axis Hit Recall v0.2.6 Report

Status: implemented

## Summary

Added an image-space hit recall pass that detects broadcast image-y direction reversal for airborne
hit-like candidate events. The pass is explicitly labeled
`broadcast_image_y_axis_fallback_v026`, does not require player proximity, and persists
`image_space_net_axis_reversal_recall` diagnostics on candidates and rejection diagnostics.

## Local Smoke

Command:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-hit-bounce-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  BALL_TRAJECTORY_RUN_ID=2e16f3d1-e252-497a-b688-d81890645ab7 \
  COURT_PROJECTION_RUN_ID=82498799-490f-44df-9222-0157356c5ff7
```

Result:

- new `event_candidate_run_id`: `d33a959b-462d-4b2e-8eed-d715565ed2c7`
- old v0.2.5 profile: 3 `hit_candidate`, 2 `bounce_candidate`
- new v0.2.6 profile: 4 `hit_candidate`, 2 `bounce_candidate`
- image-space source points evaluated: 75
- image-space reversal candidates: 12
- image-space recovered final hits: 1
- image-space overlap suppressions: 0

The recovered image-space hit is at frame 54. Its recall payload uses incoming frame 34, anchor
frame 54, and outgoing frame 66 with image-axis deltas `-79.576702` and `94.3381`.

## Validation

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q` passed: 31 tests.
- `.venv/bin/python -m pytest -q` passed: 311 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed against `tmp_tom_v3_image_space_net_axis_hit_recall_fixture.db`.
- Fixture completion audit passed against `tmp_tom_v3_image_space_net_axis_hit_recall_fixture.db`.

Browser smoke loaded the replay page for the new event candidate run. The initial DOM snapshot did
not include active marker labels because playback starts away from the candidate timestamps, but the
replay payload and focused tests verify that image-space recall diagnostics are exposed for selected
event candidate evidence. A direct `/replay/overlays` smoke for the new run returned 4 hit
candidates and 2 bounce candidates, including the frame 54 image-space recall hit with
`image_marker_source: source_ball_court_projection_image_point`.

## Remaining Limitations

The v0.2.6 image axis is a broadcast-view fallback. It improves recall for this hardcam sample, but
it is not true camera geometry, not true ball height, and not contact truth. Future work should
derive the image near/far axis from calibrated court geometry or camera/view evidence when
available.
