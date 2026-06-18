# Blueprint 28 Reviewer Confidence / Ambiguity Capture v1 Report

Status: implemented

Branch: `codex/blueprint-28-reviewer-confidence-ambiguity-capture-v1`

## Summary

Blueprint 28 adds a versioned reviewer confidence and ambiguity metadata schema, blank bundle
template, structural bundle validator, and validation-only post-Codex helper. The schema defines
neutral confidence, ambiguity, ambiguity reason, evidence-sufficiency, review-context, and
additional-review metadata for future human review workflows.

The implementation does not score confidence automatically, infer truth, judge correctness, inspect
video, create observations, create event candidates, create 3D candidates, decide in/out, score,
identify players, determine winners, claim generalization, or adjudicate evidence.

## Created

- `apps/worker/services/reviewer_confidence_schema.py`
- `tests/test_reviewer_confidence_schema.py`
- `scripts/post_codex_validate.sh`
- `docs/blueprints/blueprint_28_reviewer_confidence_ambiguity_capture_v1.md`
- `docs/reviews/reviewer_confidence_ambiguity_capture_v1.md`
- `docs/agent_reports/blueprint_28_reviewer_confidence_ambiguity_capture_v1_report.md`

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
python -m apps.worker.cli export-reviewer-confidence-schema
python -m apps.worker.cli build-reviewer-confidence-template
python -m apps.worker.cli validate-reviewer-confidence-bundle
```

Added Make targets:

```text
make tom-v1-export-reviewer-confidence-schema
make tom-v1-build-reviewer-confidence-template
make tom-v1-validate-reviewer-confidence-bundle
make tom-v1-post-codex-validate
```

Default local paths:

```text
.data/contracts/reviewer_confidence_ambiguity_schema_v1.json
.data/exports/reviewer_confidence_ambiguity_template.current.json
.data/exports/reviewer_confidence_ambiguity.validation.json
```

## Validation Semantics

The validator checks schema shape, bundle type/version, metadata keys, allowed values, optional
Blueprint 27 label keys, forbidden fields, and human-provided-only flags. It rejects forbidden
decision fields such as score, winner/player identity, server/receiver, accepted/rejected
lifecycle, correctness fields, and adjudication fields.

Validation reports structural errors only. It does not infer missing confidence, create labels,
judge truth, decide whether confidence is appropriate, or decide whether a human label is correct.

## Boundary

The schema/template/validator are review-support contracts only. They do not generate evidence,
mutate review metadata, change replay semantics, change protected baselines, decide in/out, score,
identify players, determine a winner, claim generalization, score confidence automatically, or
adjudicate evidence.

## Validation

```text
.venv/bin/python -m pytest tests/test_reviewer_confidence_schema.py -q
6 passed

.venv/bin/python -m pytest -q
421 passed

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

Reviewer confidence command smoke:

```text
make tom-v1-export-reviewer-confidence-schema PYTHON=.venv/bin/python
passed

make tom-v1-build-reviewer-confidence-template PYTHON=.venv/bin/python ...
passed

make tom-v1-validate-reviewer-confidence-bundle \
  PYTHON=.venv/bin/python \
  REVIEWER_CONFIDENCE_BUNDLE=.data/exports/reviewer_confidence_ambiguity_template.current.json
passed
```

Observed validation smoke:

- `schema_type`: `reviewer_confidence_ambiguity_schema`
- `schema_version`: `v1`
- `confidence_bundle_type`: `reviewer_confidence_ambiguity_bundle`
- `confidence_bundle_version`: `v1`
- `status`: `valid`
- `error_count`: 0
- template entries defaulted to `not_assessed`
- template entries carried `human_provided_only: true`
- template entries carried `machine_inferred: false`

Blueprint 26 taxonomy and Blueprint 27 review-label schema temp-path smokes:

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

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_28_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_28_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```

Post-Codex validation helper:

```text
make tom-v1-post-codex-validate \
  PYTHON=.venv/bin/python \
  EXPECTED_BRANCH=codex/blueprint-28-reviewer-confidence-ambiguity-capture-v1
passed
```
