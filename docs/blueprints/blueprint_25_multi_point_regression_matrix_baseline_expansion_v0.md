# Blueprint 25 Multi-Point Regression Matrix / Baseline Expansion v0

Status: complete

Blueprint 25 turns manifest-backed replay points into a read-only regression matrix. The matrix
reads a Blueprint 24 multi-point replay index, verifies associated Blueprint 23 point manifests
where available, preserves replay/run/evidence/profile/warning context, and compares baseline and
current matrices over time.

This milestone is a regression-protection layer only. It does not create observations, event
candidates, 3D candidates, labels, truth, scoring, player identity, point winner, or adjudication.

## Commands

Build a current matrix:

```bash
.venv/bin/python -m apps.worker.cli build-multi-point-regression-matrix \
  --index ".data/manifests/multi_point_replay_index.json" \
  --output ".data/exports/multi_point_regression_matrix.current.json" \
  --skip-create-db
```

Compare matrices:

```bash
.venv/bin/python -m apps.worker.cli compare-multi-point-regression-matrix \
  --baseline ".data/baselines/multi_point_regression_matrix.baseline.json" \
  --current ".data/exports/multi_point_regression_matrix.current.json" \
  --output ".data/exports/multi_point_regression_matrix.regression.json" \
  --skip-create-db
```

Verify current matrix against a frozen baseline:

```bash
.venv/bin/python -m apps.worker.cli verify-multi-point-regression-matrix \
  --index ".data/manifests/multi_point_replay_index.json" \
  --baseline ".data/baselines/multi_point_regression_matrix.baseline.json" \
  --current-output ".data/exports/multi_point_regression_matrix.current.json" \
  --regression-output ".data/exports/multi_point_regression_matrix.regression.json" \
  --regression-markdown-output ".data/exports/multi_point_regression_matrix.regression.md" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-build-multi-point-regression-matrix PYTHON=.venv/bin/python
make tom-v1-verify-multi-point-regression-matrix PYTHON=.venv/bin/python
```

## Paths

Default local paths:

```text
.data/baselines/multi_point_regression_matrix.baseline.json
.data/exports/multi_point_regression_matrix.current.json
.data/exports/multi_point_regression_matrix.regression.json
.data/exports/multi_point_regression_matrix.regression.md
```

Generated `.data` artifacts are local outputs and should not be committed.

## Matrix Contract

The matrix records:

- `matrix_type`: `multi_point_evidence_regression_matrix`
- `matrix_version`: `v0`
- source Blueprint 24 index path and provenance
- skipped duplicate/non-current manifest details inherited from the source index
- point count
- manifest-backed point rows
- summary counts
- explicit no-truth/no-adjudication warnings

Each point row records:

- `point_manifest_id`
- `media_id`
- provenance-only labels
- manifest path
- replay URL
- associated run IDs
- evidence availability
- profile counts
- point warnings
- matrix row warnings, including manifest file availability and manifest/index identity match

## Comparison Behavior

Comparison reports drift in:

- point presence
- point labels
- replay URL and run-ID context
- evidence availability booleans
- profile counts
- warning presence
- row warning presence
- summary counts
- matrix warning contract

Additional manifest-backed points are additive and non-breaking by default. Strict mode can treat
additive/non-protected drift as breaking. Protected sample-point regressions and contract-breaking
warning/type/version failures are breaking.

Regression drift is not proof that any observation, candidate, review annotation, manifest, or
matrix is correct or incorrect.

## Boundaries

Blueprint 25 does not add or change:

- in/out
- score
- point winner
- player identity
- rally state
- server or receiver state
- accepted/rejected lifecycle
- marker arbitration
- event generation
- 3D generation
- coaching or tactical conclusions
- adjudication
- betting or prediction
- generalization claims

The matrix supports multiple points structurally, including demo or stand-in manifests, but it does
not claim real multi-point tennis generalization.

## Protected sample_point Gate

Blueprint 25 preserves the existing `sample_point` reviewed 3D debug baseline gate:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Expected:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
