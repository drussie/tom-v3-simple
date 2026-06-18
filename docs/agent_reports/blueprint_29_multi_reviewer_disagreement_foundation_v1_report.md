# Blueprint 29 Multi-Reviewer / Disagreement Foundation v1 Report

Status: implemented

Branch: `codex/blueprint-29-multi-reviewer-disagreement-foundation-v1`

## Summary

Blueprint 29 adds a versioned multi-reviewer disagreement schema, blank review-set template,
structural review-set validator, and structural disagreement report builder. It composes Blueprint
27 structured review-label bundles and Blueprint 28 reviewer confidence bundles when paths are
available.

The implementation does not rank reviewers, score reviewer quality, resolve disagreement, infer
truth, judge correctness, inspect video, create observations, create event candidates, create 3D
candidates, decide in/out, score, identify players, determine winners, claim generalization, or
adjudicate evidence.

## Created

- `apps/worker/services/multi_reviewer_disagreement.py`
- `tests/test_multi_reviewer_disagreement.py`
- `docs/blueprints/blueprint_29_multi_reviewer_disagreement_foundation_v1.md`
- `docs/reviews/multi_reviewer_disagreement_foundation_v1.md`
- `docs/agent_reports/blueprint_29_multi_reviewer_disagreement_foundation_v1_report.md`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/BLUEPRINT_STATUS.md`

## CLI / Make Helpers

Added CLI commands:

```text
python -m apps.worker.cli export-multi-reviewer-disagreement-schema
python -m apps.worker.cli build-multi-reviewer-review-set-template
python -m apps.worker.cli validate-multi-reviewer-review-set
python -m apps.worker.cli build-reviewer-disagreement-report
```

Added Make targets:

```text
make tom-v1-export-multi-reviewer-disagreement-schema
make tom-v1-build-multi-reviewer-review-set-template
make tom-v1-validate-multi-reviewer-review-set
make tom-v1-build-reviewer-disagreement-report
```

Default local paths:

```text
.data/contracts/multi_reviewer_disagreement_schema_v1.json
.data/exports/multi_reviewer_review_set_template.current.json
.data/exports/multi_reviewer_review_set.validation.json
.data/exports/reviewer_disagreement_report.current.json
```

## Validation Semantics

The validator checks schema shape, review-set type/version, reviewer ID presence and uniqueness,
forbidden fields, disallowed reviewer identity fields, human-provided-only flags, and referenced
Blueprint 27/28 bundle structure when paths are present. Missing bundle refs are structural
warnings, not errors, for blank templates.

Validation and reports are structural only. They do not infer missing labels, create labels, say
which reviewer is right, resolve disagreement, decide whether a human label is true, or score
reviewers.

## Boundary

The schema/template/validator/report are review-support contracts only. They do not generate
evidence, mutate review metadata, change replay semantics, change protected baselines, decide
in/out, score, identify players, determine a winner, claim generalization, rank reviewers, score
reviewer quality, or adjudicate evidence.

## Validation

```text
.venv/bin/python -m pytest tests/test_multi_reviewer_disagreement.py -q
6 passed

.venv/bin/python -m pytest -q
427 passed

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

Multi-reviewer command smoke:

```text
make tom-v1-export-multi-reviewer-disagreement-schema PYTHON=.venv/bin/python
passed

make tom-v1-build-multi-reviewer-review-set-template PYTHON=.venv/bin/python ...
passed

make tom-v1-validate-multi-reviewer-review-set \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
passed

make tom-v1-build-reviewer-disagreement-report \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
passed
```

Observed validation/report smoke:

- `schema_type`: `multi_reviewer_disagreement_schema`
- `schema_version`: `v1`
- `review_set_type`: `multi_reviewer_review_set`
- `review_set_version`: `v1`
- `status`: `valid`
- `error_count`: 0
- `structural_warning_count`: 4 for blank-template missing bundle refs
- `disagreement_report_type`: `reviewer_disagreement_report`
- `disagreement_report_version`: `v1`
- `comparison_group_count`: 9
- `summary.disagreement_observed_count`: 0 for the blank template
- `summary.missing_input_count`: 9 for the blank template
- `summary.requires_additional_review_count`: 9 for the blank template

Blueprint 26, Blueprint 27, and Blueprint 28 temp-path contract smokes:

```text
.venv/bin/python -m apps.worker.cli export-observation-quality-taxonomy \
  --output .data/tmp/observation_quality_taxonomy_v1.smoke.json \
  --skip-create-db
passed

.venv/bin/python -m apps.worker.cli export-review-label-schema \
  --output .data/tmp/review_label_schema_v1.smoke.json \
  --skip-create-db
passed

.venv/bin/python -m apps.worker.cli export-reviewer-confidence-schema \
  --output .data/tmp/reviewer_confidence_ambiguity_schema_v1.smoke.json \
  --skip-create-db
passed
```

Multi-point matrix gate:

```text
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
passed
```

Observed:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
- `matrix_is_not_truth`: true

Protected sample-point baseline gate:

```text
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
passed
```

Observed:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

Fixture demo and audit:

```text
.venv/bin/python scripts/smoke_synthetic_viewer_data.py
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_29_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_29_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```

Post-Codex validation helper is run after commit/tag creation because Blueprint 29 requires
passing the expected tag into the helper.
