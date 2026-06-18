# Blueprint 27 Structured Review Label Schema v1 Report

Status: implemented

Branch: `codex/blueprint-27-structured-review-label-schema-v1`

## Summary

Blueprint 27 adds a versioned structured review label schema, blank review-label bundle template,
and structural bundle validator for future human review workflows. It defines neutral label
families, label definitions, value sets, provenance requirements, validation rules, and explicit
warning contracts.

The implementation does not label automatically, infer truth, judge correctness, inspect video,
create observations, create event candidates, create 3D candidates, decide in/out, score, identify
players, determine winners, claim generalization, or adjudicate evidence.

## Created

- `apps/worker/services/review_label_schema.py`
- `tests/test_review_label_schema.py`
- `docs/blueprints/blueprint_27_structured_review_label_schema_v1.md`
- `docs/reviews/structured_review_label_schema_v1.md`
- `docs/agent_reports/blueprint_27_structured_review_label_schema_v1_report.md`

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
python -m apps.worker.cli export-review-label-schema
python -m apps.worker.cli build-review-label-template
python -m apps.worker.cli validate-review-label-bundle
```

Added Make targets:

```text
make tom-v1-export-review-label-schema
make tom-v1-build-review-label-template
make tom-v1-validate-review-label-bundle
```

Default local paths:

```text
.data/contracts/review_label_schema_v1.json
.data/exports/review_label_template.current.json
.data/exports/review_label_bundle.validation.json
```

## Validation Semantics

The validator checks schema shape, bundle type/version, known label keys, allowed values, forbidden
fields, and human-provided-only flags. It rejects forbidden decision fields such as score,
winner/player identity, server/receiver, accepted/rejected lifecycle, and adjudication fields.

Validation reports structural errors only. It does not infer missing labels, create labels, judge
truth, or decide whether a human label is correct.

## Boundary

The schema/template/validator are review-support contracts only. They do not generate evidence,
mutate review metadata, change replay semantics, change protected baselines, decide in/out, score,
identify players, determine a winner, claim generalization, or adjudicate evidence.

## Validation

```text
.venv/bin/python -m pytest tests/test_review_label_schema.py -q
5 passed

.venv/bin/python -m pytest -q
415 passed

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

Review-label command smoke:

```text
make tom-v1-export-review-label-schema PYTHON=.venv/bin/python
passed

make tom-v1-build-review-label-template PYTHON=.venv/bin/python ...
passed

make tom-v1-validate-review-label-bundle \
  PYTHON=.venv/bin/python \
  REVIEW_LABEL_BUNDLE=.data/exports/review_label_template.current.json
passed
```

Observed validation smoke:

- `schema_type`: `structured_review_label_schema`
- `schema_version`: `v1`
- `label_bundle_type`: `structured_review_label_bundle`
- `label_bundle_version`: `v1`
- `status`: `valid`
- `error_count`: 0
- template entries defaulted to `not_assessed`
- template entries carried `human_provided_only: true`
- template entries carried `machine_inferred: false`

Blueprint 26 taxonomy export smoke:

```text
make tom-v1-export-observation-quality-taxonomy PYTHON=.venv/bin/python
passed
```

Observed:

- `ok`: true
- `status`: `completed`
- `taxonomy_version`: `v1`

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

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_27_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_27_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
