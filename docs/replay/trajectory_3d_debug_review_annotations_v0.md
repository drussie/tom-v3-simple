# Trajectory 3D Debug Review Annotations v0

The Replay Workstation 3D Debug View can now record compact operator review metadata for selected
3D debug evidence.

## Review Targets

- selected 3D candidate samples
- selected event-marker 3D diagnostic links
- missing 3D sample moments at current replay time

Review annotations persist separately from event candidate reviews. They are grouped in replay by
`trajectory_3d_candidate_id` and `event_candidate_3d_diagnostic_id`.

## Summary Surfaces

Replay overlay chunks, point evidence snapshots, and point candidate evaluations expose compact
3D debug review summaries with counts for sample reviews, diagnostic reviews, missing sample
notes, and review labels.

## Boundary

These reviews are not 3D truth, hit truth, bounce truth, in/out, score, or adjudication. They do
not change generated evidence.
