# Blueprint 25 Multi-Point Regression Matrix / Baseline Expansion v0 Report

Status: implemented

Branch: `codex/blueprint-25-multi-point-regression-matrix-baseline-expansion-v0`

## Summary

Blueprint 25 adds a read-only multi-point regression matrix over Blueprint 24 point-index rows and
Blueprint 23 point manifests. It builds current/baseline matrix artifacts, compares matrix drift,
and verifies a current matrix against a frozen baseline without creating observations, event
candidates, 3D candidates, truth, scoring, player identity, point winner, or adjudication.

## Created

- `apps/worker/services/multi_point_regression_matrix.py`
- `tests/test_multi_point_regression_matrix.py`
- `docs/blueprints/blueprint_25_multi_point_regression_matrix_baseline_expansion_v0.md`
- `docs/reviews/multi_point_regression_matrix_baseline_expansion_v0.md`
- `docs/agent_reports/blueprint_25_multi_point_regression_matrix_baseline_expansion_v0_report.md`

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
python -m apps.worker.cli build-multi-point-regression-matrix
python -m apps.worker.cli compare-multi-point-regression-matrix
python -m apps.worker.cli verify-multi-point-regression-matrix
```

Added Make targets:

```text
make tom-v1-build-multi-point-regression-matrix
make tom-v1-compare-multi-point-regression-matrix
make tom-v1-verify-multi-point-regression-matrix
```

Default local paths:

```text
.data/baselines/multi_point_regression_matrix.baseline.json
.data/exports/multi_point_regression_matrix.current.json
.data/exports/multi_point_regression_matrix.regression.json
.data/exports/multi_point_regression_matrix.regression.md
```

## Drift Semantics

The comparator reports drift for point presence, labels, replay/run context, evidence availability,
profile counts, point warnings, row warnings, summary counts, and matrix warning contract. Added
manifest-backed points are non-breaking unless strict mode is enabled. Protected sample-point row
changes and matrix contract failures are breaking.

Regression drift is not proof of correctness or incorrectness.

## Boundary

The matrix reads existing index/manifest JSON only. It does not generate evidence, mutate review
metadata, change protected baselines, decide in/out, score, identify players, determine a winner,
claim generalization, or adjudicate evidence.

## Validation

```text
.venv/bin/python -m pytest tests/test_multi_point_regression_matrix.py tests/test_multi_point_replay_index.py -q
7 passed

.venv/bin/python -m pytest -q
406 passed

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

Observed protected result:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

Multi-point replay index and regression matrix smoke:

```text
.venv/bin/python -m apps.worker.cli build-multi-point-replay-index \
  --manifest-root .data/manifests \
  --output /tmp/tom_v3_blueprint_25_replay_index.json \
  --skip-create-db
passed

.venv/bin/python -m apps.worker.cli build-multi-point-regression-matrix \
  --index /tmp/tom_v3_blueprint_25_replay_index.json \
  --output /tmp/tom_v3_blueprint_25_matrix.baseline.json \
  --skip-create-db
passed

.venv/bin/python -m apps.worker.cli build-multi-point-regression-matrix \
  --index /tmp/tom_v3_blueprint_25_replay_index.json \
  --output /tmp/tom_v3_blueprint_25_matrix.current.json \
  --skip-create-db
passed

.venv/bin/python -m apps.worker.cli compare-multi-point-regression-matrix \
  --baseline /tmp/tom_v3_blueprint_25_matrix.baseline.json \
  --current /tmp/tom_v3_blueprint_25_matrix.current.json \
  --output /tmp/tom_v3_blueprint_25_matrix.regression.json \
  --skip-create-db
passed

.venv/bin/python -m apps.worker.cli verify-multi-point-regression-matrix \
  --index /tmp/tom_v3_blueprint_25_replay_index.json \
  --baseline /tmp/tom_v3_blueprint_25_matrix.baseline.json \
  --current-output /tmp/tom_v3_blueprint_25_matrix.verify.current.json \
  --regression-output /tmp/tom_v3_blueprint_25_matrix.verify.regression.json \
  --regression-markdown-output /tmp/tom_v3_blueprint_25_matrix.verify.regression.md \
  --skip-create-db
passed
```

The local smoke discovered one deduplicated protected sample-point row and skipped two duplicate
manifest files for the same deterministic point identity. Matrix verify completed with no drift.

Fixture demo and audit:

```text
.venv/bin/python scripts/smoke_synthetic_viewer_data.py
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_25_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_25_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
