# Reviewed 3D Debug Dataset Export v0

The reviewed 3D debug dataset export is an offline package for analysis and curation. It turns
existing 3D debug evidence plus operator review metadata into deterministic JSON or Markdown.

## Inputs

- `media_id`
- `event_candidate_run_id`
- `trajectory_3d_run_id`
- `camera_geometry_id`

The export reads:

- final hit/bounce event marker observations
- `ball_trajectory_3d_candidate` rows
- `event_candidate_3d_diagnostic` rows
- `trajectory_3d_debug_review_annotation` rows
- `event_candidate_review_annotation` rows
- declared camera geometry evidence

## JSON Sections

- `summary`
- `camera_geometry_summary`
- `trajectory_3d_summary`
- `event_candidate_3d_diagnostic_summary`
- `trajectory_3d_debug_review_summary`
- `event_marker_summary`
- `trajectory_3d_candidates`
- `event_candidate_3d_diagnostics`
- `trajectory_3d_debug_reviews`
- `event_candidate_reviews`
- `warnings`

## Warnings

Every export carries:

- `dataset_export_only: true`
- `review_metadata_only: true`
- `not_truth: true`
- `not_3d_truth: true`
- `not_training_truth: true`
- `does_not_change_event_candidates: true`
- `does_not_change_3d_candidates: true`
- `does_not_create_in_out: true`
- `does_not_create_score: true`
- `no_adjudication: true`

Review labels are useful for offline review and future training preparation, but they are not
ground truth labels. The export does not change live TOM behavior.
