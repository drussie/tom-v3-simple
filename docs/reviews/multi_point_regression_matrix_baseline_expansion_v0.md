# Multi-Point Regression Matrix / Baseline Expansion v0

The multi-point regression matrix is a local comparison artifact over manifest-backed replay
points. It lets TOM compare evidence availability, profile counts, replay URLs, run IDs, labels,
and warning contracts over time.

It is not truth, training truth, 3D truth, scoring, player identity, point winner, in/out, or
adjudication.

## Build

```bash
make tom-v1-build-multi-point-replay-index \
  PYTHON=.venv/bin/python

make tom-v1-build-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
```

Optional output override:

```bash
MULTI_POINT_REGRESSION_MATRIX_OUTPUT=.data/baselines/multi_point_regression_matrix.baseline.json
```

## Verify

```bash
make tom-v1-verify-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
```

Default paths:

```text
.data/baselines/multi_point_regression_matrix.baseline.json
.data/exports/multi_point_regression_matrix.current.json
.data/exports/multi_point_regression_matrix.regression.json
.data/exports/multi_point_regression_matrix.regression.md
```

## Expected Result

- `ok`: true when no breaking drift is detected
- `status`: `completed`, `completed_with_drift`, or `failed_regression`
- `matrix_type`: `multi_point_evidence_regression_matrix`
- `matrix_version`: `v0`
- `summary.drift_detected`: boolean
- `summary.breaking_drift_detected`: boolean
- `warnings.matrix_is_not_truth`: true
- `warnings.baseline_is_not_truth`: true
- `warnings.regression_report_only`: true
- `warnings.no_adjudication`: true

## Drift Semantics

Non-breaking by default:

- added manifest-backed points
- additive count increases outside protected sample-point regression
- non-protected drift when not in strict mode

Breaking:

- protected sample-point point removal or protected row changes
- required matrix warning missing or false
- invalid matrix type or version
- strict-mode drift

Regression drift is a difference between local matrix artifacts. It does not prove correctness or
incorrectness.

## Caveat

The repo may only contain the protected sample-point manifest and demo or stand-in manifests unless
a real second-point clip has been supplied. This matrix supports multiple point rows structurally,
but it does not claim TOM generalizes to multiple real tennis points.
