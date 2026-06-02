# Sample Point Reviewed 3D Debug Baseline v0

This baseline workflow freezes the current sample-point reviewed 3D debug dataset export profile as
a local regression reference.

The baseline is not truth, not 3D truth, and not training truth. It exists to detect export drift
before future pipeline work expands beyond the current `sample_point` context.

## Sample Context

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `event_candidate_run_id`: `1b946366-7ec1-426f-8b40-494535a9b3fb`
- `trajectory_3d_run_id`: `ea76ccab-c51d-4a63-9682-9fd0bbb83f14`
- `camera_geometry_id`: `5afa67fb-7f6e-41eb-b4aa-b1100a97ee97`

## Expected Summary

- `event_marker_count`: 6
- `trajectory_3d_candidate_count`: 68
- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_review_count`: 1
- `trajectory_3d_debug_review_count`: 0
- `missing_3d_sample_note_count`: 0

## Freeze

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-freeze-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Generated local files:

- `.data/baselines/reviewed_3d_debug_dataset_sample_point.baseline.json`
- `.data/baselines/reviewed_3d_debug_dataset_sample_point.baseline.md`
- `.data/baselines/reviewed_3d_debug_dataset_sample_point.baseline_manifest.json`

## Verify

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Expected no-drift status:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
- `not_truth`: true
- `not_training_truth`: true

Drift requires human review. The gate does not update live TOM evidence.
