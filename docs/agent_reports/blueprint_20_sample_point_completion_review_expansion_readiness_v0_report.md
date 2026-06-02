# Blueprint 20 sample_point Completion Review / Expansion Readiness v0 Report

Status: implemented

Branch: `codex/blueprint-20-sample-point-completion-review-expansion-readiness-v0`

## Summary

Blueprint 20 adds a documentation and gate checkpoint for the current `sample_point` phase. It
records the sample profile, baseline gate state, expansion readiness verdict, and remaining
candidate-only boundaries before TOM v3 introduces a second point.

No event candidate logic, marker arbitration, 3D candidate generation, 3D diagnostics, review
annotations, replay UI, in/out, score, or adjudication logic was changed.

## Created

- `docs/reviews/sample_point_completion_review_v0.md`
- `docs/reviews/sample_point_expansion_readiness_v0.md`
- `docs/agent_reports/blueprint_20_sample_point_completion_review_expansion_readiness_v0_report.md`

## Updated

- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`

## Confirmed Sample Profile

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `event_candidate_run_id`: `1b946366-7ec1-426f-8b40-494535a9b3fb`
- `trajectory_3d_run_id`: `ea76ccab-c51d-4a63-9682-9fd0bbb83f14`
- `camera_geometry_id`: `5afa67fb-7f6e-41eb-b4aa-b1100a97ee97`
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

## Gates Run

Baseline verify:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

Point evidence snapshot:

- `marker_summary`: 6
- `trajectory_3d_summary`: available
- `event_candidate_3d_diagnostic_summary`: available
- `trajectory_3d_debug_review_summary`: present

Candidate evaluation:

- `final_marker_count`: 6
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `reviewed_final_markers`: 1
- `unreviewed_final_markers`: 5

Reviewed 3D debug dataset export:

- `event_marker_count`: 6
- `trajectory_3d_candidate_count`: 68
- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_review_count`: 1
- `not_truth`: true
- `not_training_truth`: true

## Readiness Verdict

The `sample_point` phase is ready for controlled second-point expansion.

This means the evidence/review/export/regression loop is stable enough to introduce one additional
point under the same candidate-only boundaries. It does not mean event candidates are truth, 3D is
solved, markers are fully correct, or scoring/in-out/adjudication is available.

## Boundaries Preserved

- no hit truth
- no bounce truth
- no in/out
- no score
- no point or rally state
- no player identity
- no training truth
- no accepted/rejected lifecycle
- no adjudication
- no mutation of existing candidate or review observations

## Validation

Sample gates:

```text
tom-v1-verify-reviewed-3d-debug-baseline
passed: ok=true, drift_detected=false, breaking_drift_detected=false

tom-v1-point-evidence-snapshot
passed: marker_summary=6, trajectory_3d_summary available

tom-v1-evaluate-point-candidates
passed: final_marker_count=6, hit_candidate=3, bounce_candidate=3

tom-v1-export-reviewed-3d-debug-dataset
passed: event_marker_count=6, trajectory_3d_candidate_count=68
```

Full validation:

```text
.venv/bin/python -m pytest -q
384 passed

ruff check .
passed

git diff --check
passed

cd apps/web && npm run lint
passed

cd apps/web && npm run build
passed

cd apps/web && npm audit --omit=dev
found 0 vulnerabilities
```

Fixture demo and audit:

```text
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_20_completion_fixture.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_20_completion_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```

## Recommended Next Step

Blueprint 21 - Second Point Ingestion / Evidence Replay Smoke v0.
