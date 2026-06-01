# Event Candidate 3D Diagnostics v0

`event_candidate_3d_diagnostic` is a typed diagnostic table that links final hit/bounce candidate
markers to nearby provisional 3D ball trajectory samples.

The table is intentionally separate from `observation`. It does not mutate event candidate rows or
3D trajectory candidate rows.

## Fields

The diagnostic stores:

- `event_candidate_run_id`
- `event_observation_id`
- `candidate_type`
- `trajectory_3d_run_id`
- `camera_geometry_id`
- marker frame/time
- nearest 3D candidate id/frame/time
- nearest metric court-plane x/y/z, when available
- height status
- diagnostic status/label
- local pre/post/window sample counts
- local velocity/speed/direction diagnostics
- warnings and metadata

## Conservative v0 Behavior

If no nearby 3D samples exist, diagnostics use:

- `diagnostic_status = insufficient_3d_evidence`
- `diagnostic_label = insufficient_evidence`

If nearby samples exist but height is unknown, diagnostics use:

- `diagnostic_status = height_unknown`
- `diagnostic_label = neutral_context`

This is expected with Blueprint 12 `none_unknown` height model.

## Boundary

These rows are diagnostic context only. They do not change event candidate classification, marker
counts, review annotations, in/out, score, or adjudication.
