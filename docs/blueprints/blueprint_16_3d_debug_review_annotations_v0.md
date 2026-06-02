# Blueprint 16 3D Debug Review Annotations v0

Blueprint 16 adds operator review metadata for the Replay Workstation 3D Debug View.

## Scope

Operators can review:

- selected `ball_trajectory_3d_candidate` samples
- selected marker-linked `event_candidate_3d_diagnostic` rows
- missing 3D sample moments at the current replay time

Supported labels are review labels only:

- `useful`
- `wrong`
- `unclear`
- `needs_review`
- `missing_3d_sample`
- `bad_3d_position`
- `bad_diagnostic_link`

The persistence table is `trajectory_3d_debug_review_annotation`.

## Replay

Replay exposes:

- GET/POST/PATCH API endpoints under `/replay/{media_id}/trajectory-3d-debug-reviews`
- compact `trajectory_3d_debug_review_summary` payloads
- 3D sample review controls in the 3D Debug View
- 3D diagnostic review controls for selected marker-linked diagnostics
- missing 3D sample notes at current replay time

## Boundary

3D debug reviews are operator metadata only. They do not mutate 3D candidate samples, 3D
diagnostics, hit/bounce event candidates, marker arbitration, in/out, score, or adjudication.
