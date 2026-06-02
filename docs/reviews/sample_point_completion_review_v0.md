# sample_point Completion Review v0

Blueprint 20 freezes the current `sample_point` evidence/review/export/regression profile before
TOM v3 expands to a second point.

This is a completion review, not a feature milestone. It does not change candidate generation,
marker arbitration, 3D candidate generation, 3D diagnostics, review annotations, replay UI,
in/out, score, point state, or adjudication.

## Sample Context

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `event_candidate_run_id`: `1b946366-7ec1-426f-8b40-494535a9b3fb`
- `trajectory_3d_run_id`: `ea76ccab-c51d-4a63-9682-9fd0bbb83f14`
- `camera_geometry_id`: `5afa67fb-7f6e-41eb-b4aa-b1100a97ee97`
- `motion_smoothing_run_id`: `d6e23e3d-daee-4c12-aa11-2d17eee15b58`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

## Architecture Summary

Blueprints 8 through 19 established the current evidence loop:

```text
real image-space evidence
-> smoothed candidate overlays
-> court projection candidates
-> ball trajectory court candidates
-> hit/bounce event candidates
-> marker arbitration
-> event marker review annotations
-> point evidence snapshot/evaluation
-> declared camera/court geometry evidence
-> 3D trajectory candidate diagnostics
-> 3D Debug View review annotations
-> reviewed 3D debug dataset export
-> export regression report
-> local sample-point baseline gate
```

Every layer remains candidate evidence. The pipeline records review and diagnostic metadata but does
not promote any marker, trajectory, projection, or baseline into truth.

## Current Sample Profile

The Blueprint 20 gate run confirmed:

- `final_marker_count`: 6
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- `trajectory_3d_candidate_count`: 68
- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_review_count`: 1
- `trajectory_3d_debug_review_count`: 0
- `missing_3d_sample_note_count`: 0
- `height_model`: `none_unknown`
- `known_height_count`: 0
- `unknown_height_count`: 68
- `true_3d_reconstruction_available`: false

The one event marker review marks a `bounce_candidate` at frame 77 / `2567ms` as `wrong`, with the
operator note that the real bounce happens shortly after and is also found. That review is metadata
only. It does not change the live candidate run.

## Baseline Gate State

The reviewed 3D debug baseline gate passed:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
- baseline/current `event_marker_count`: 6
- baseline/current `trajectory_3d_candidate_count`: 68
- baseline/current `event_candidate_3d_diagnostic_count`: 6
- baseline/current `event_marker_review_count`: 1
- baseline/current `trajectory_3d_debug_review_count`: 0
- baseline/current `missing_3d_sample_note_count`: 0

This means the local export profile is stable against the frozen baseline. It does not mean the
markers are correct, complete, or suitable as truth labels.

## Stable For Expansion

The following are stable enough to carry into one controlled second-point smoke:

- run ID driven replay assembly
- operator/debug presets
- smoothed motion overlays
- court projection mini-map
- event candidate video and mini-map markers
- event marker review annotations
- point evidence snapshot and candidate evaluation reports
- declared camera/court geometry evidence metadata
- provisional 3D trajectory candidates with unknown height
- event candidate 3D diagnostics
- reviewed 3D debug dataset export
- reviewed 3D debug dataset regression
- sample-point baseline verification

## Not Stable As Truth

The following are explicitly not stable as truth:

- hit/bounce correctness
- marker completeness
- 3D ball reconstruction
- ball height
- in/out
- score
- point outcome
- rally state
- player identity
- server/receiver state
- training labels
- accepted/rejected lifecycle

## Expansion Criteria

Before any second-point work is considered comparable, TOM v3 should require:

1. The sample-point baseline gate still passes with no drift.
2. The new point is introduced as a separate evidence sample, not as a generalization claim.
3. The new point preserves candidate-only warnings across candidate, review, export, and regression
   outputs.
4. The new point records its own media/run IDs, marker counts, review state, and baseline readiness.
5. Any new visual or diagnostic issue is handled as a repair, not as hidden truth correction.

## Completion Verdict

The `sample_point` phase is complete as an observation-only evidence/review/export/regression loop.
It is ready for controlled second-point expansion under the same candidate-only boundaries.

This verdict does not assert truth, scoring, in/out, 3D reconstruction, or adjudication.
