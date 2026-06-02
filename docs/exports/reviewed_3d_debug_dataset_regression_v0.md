# Reviewed 3D Debug Dataset Regression v0

The reviewed 3D debug dataset regression report compares a saved baseline export with a current
export from Blueprint 17.

## Inputs

- `baseline` reviewed 3D debug dataset JSON path
- `current` reviewed 3D debug dataset JSON path
- optional `strict` flag
- optional ID and float drift tolerances
- optional JSON or Markdown output path

## Drift Categories

- `top_level_drift`
- `summary_count_drift`
- `section_presence_drift`
- `event_marker_drift`
- `trajectory_3d_candidate_drift`
- `event_candidate_3d_diagnostic_drift`
- `trajectory_3d_debug_review_drift`
- `event_candidate_review_drift`
- `warning_drift`

## Status Values

- `completed`: no drift detected
- `completed_with_drift`: drift detected in non-strict mode
- `failed_regression`: drift detected in strict mode

## Warnings

Every report carries:

- `regression_report_only: true`
- `baseline_is_not_truth: true`
- `not_truth: true`
- `not_3d_truth: true`
- `not_training_truth: true`
- `does_not_change_event_candidates: true`
- `does_not_change_3d_candidates: true`
- `does_not_create_in_out: true`
- `does_not_create_score: true`
- `no_adjudication: true`

Baseline drift is a review signal, not an adjudication signal. The harness does not update source
evidence or decide tennis meaning.
