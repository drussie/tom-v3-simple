# Blueprint 30 INTENNSE Label Alignment Contract v1 Report

Status: implemented

Branch: `codex/blueprint-30-intennse-label-alignment-contract-v1`

## Summary

Blueprint 30 adds a versioned INTENNSE label alignment contract, blank alignment bundle template,
structural alignment bundle validator, and structural alignment report builder. The contract
connects TOM observation evidence, structured review labels, reviewer confidence/ambiguity
metadata, multi-reviewer disagreement reports, replay context, and future INTENNSE expert
interpretation label references.

The implementation does not import INTENNSE labels, create TOM labels, infer expert
interpretation, judge correctness, resolve disagreement, infer truth, inspect video, create
observations, create event candidates, create 3D candidates, decide in/out, score, identify
players, determine winners, create coaching/tactical conclusions, claim generalization, or
adjudicate evidence.

## Created

- `apps/worker/services/intennse_label_alignment.py`
- `tests/test_intennse_label_alignment.py`
- `docs/blueprints/blueprint_30_intennse_label_alignment_contract_v1.md`
- `docs/reviews/intennse_label_alignment_contract_v1.md`
- `docs/agent_reports/blueprint_30_intennse_label_alignment_contract_v1_report.md`
- `.data/contracts/intennse_label_alignment_contract_v1.json`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `scripts/post_codex_validate.sh`
- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/BLUEPRINT_STATUS.md`

## CLI / Make Helpers

Added CLI commands:

```text
python -m apps.worker.cli export-intennse-label-alignment-contract
python -m apps.worker.cli build-intennse-alignment-template
python -m apps.worker.cli validate-intennse-alignment-bundle
python -m apps.worker.cli build-intennse-alignment-report
```

Added Make targets:

```text
make tom-v1-export-intennse-label-alignment-contract
make tom-v1-build-intennse-alignment-template
make tom-v1-validate-intennse-alignment-bundle
make tom-v1-build-intennse-alignment-report
```

Default local paths:

```text
.data/contracts/intennse_label_alignment_contract_v1.json
.data/exports/intennse_alignment_template.current.json
.data/exports/intennse_alignment_bundle.validation.json
.data/exports/intennse_alignment_report.current.json
```

## Validation Semantics

The validator checks contract shape, bundle type/version, TOM schema reference versions, referenced
TOM contract versions when paths are available, allowed alignment entities, allowed value sets,
forbidden fields, human-provided-only flags, and machine-inferred flags. INTENNSE references are
external placeholders in v1.

Validation and reports are structural only. They do not infer missing TOM labels, create INTENNSE
labels, validate correctness, resolve disagreement, decide whether an external interpretation is
true, or adjudicate evidence.

## Boundary

The contract/template/validator/report are provenance and review-support contracts only. They do
not generate evidence, mutate review metadata, change replay semantics, change protected baselines,
decide in/out, score, identify players, determine a winner, claim generalization, score reviewers,
resolve disagreement, produce INTENNSE coaching/tactical/match-outcome conclusions, or adjudicate
evidence.

## Validation

Focused Blueprint 30 checks:

```text
.venv/bin/python -m pytest tests/test_intennse_label_alignment.py -q
5 passed

ruff check apps/worker/services/intennse_label_alignment.py tests/test_intennse_label_alignment.py apps/worker/cli.py
passed
```

Full validation:

```text
.venv/bin/python -m pytest -q
432 passed

ruff check .
passed

git diff --check
passed

cd apps/web && npm run lint && npm run build && npm audit --omit=dev
passed; found 0 vulnerabilities
```

Blueprint 30 command smoke:

```text
make tom-v1-export-intennse-label-alignment-contract PYTHON=.venv/bin/python
passed

make tom-v1-build-intennse-alignment-template PYTHON=.venv/bin/python ...
passed

make tom-v1-validate-intennse-alignment-bundle \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
passed

make tom-v1-build-intennse-alignment-report \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
passed
```

Observed Blueprint 30 smoke output:

- `contract_type`: `intennse_label_alignment_contract`
- `contract_version`: `v1`
- `alignment_bundle_type`: `intennse_label_alignment_bundle`
- `alignment_bundle_version`: `v1`
- `alignment_entry_count`: 8
- `validation_type`: `intennse_alignment_bundle_validation`
- `status`: `valid`
- `error_count`: 0
- `structural_warning_count`: 0 for the sample-point template with an external INTENNSE ref
- `alignment_report_type`: `intennse_label_alignment_report`
- `alignment_report_version`: `v1`
- `summary.alignment_reference_present_count`: 8
- `summary.missing_tom_reference_count`: 0
- `summary.missing_intennse_reference_count`: 0

Blueprint 26 through Blueprint 29 temp-path contract smokes:

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

.venv/bin/python -m apps.worker.cli export-multi-reviewer-disagreement-schema \
  --output .data/tmp/multi_reviewer_disagreement_schema_v1.smoke.json \
  --skip-create-db
passed
```

Multi-point replay index and matrix gate:

```text
make tom-v1-build-multi-point-replay-index \
  PYTHON=.venv/bin/python \
  MULTI_POINT_REPLAY_INDEX_OUTPUT=.data/tmp/blueprint_30_multi_point_replay_index.json
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-multi-point-regression-matrix \
  PYTHON=.venv/bin/python \
  MULTI_POINT_REPLAY_INDEX_OUTPUT=.data/tmp/blueprint_30_multi_point_replay_index.json
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

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_30_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_30_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```

Post-Codex validation helper:

```text
scripts/post_codex_validate.sh \
  --branch codex/blueprint-30-intennse-label-alignment-contract-v1 \
  --expected-tag tom-v3-blueprint-30-intennse-label-alignment-contract-v1 \
  --python .venv/bin/python
passed; exit 0
```

Observed final helper status:

- post-Codex standard tests, ruff, diff check, web lint/build/audit passed
- post-Codex multi-point replay index and regression matrix gate passed
- post-Codex protected sample-point gate passed
- post-Codex BP26, BP27, BP28, BP29, and BP30 temp-path smokes passed
- final helper `git status --short`: only `tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`
