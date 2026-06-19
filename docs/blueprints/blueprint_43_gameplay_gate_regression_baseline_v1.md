# Blueprint 43 - Gameplay Gate Regression Baseline v1

Status: complete

## Goal

Blueprint 43 freezes a structural regression baseline for the gameplay gate stack added in
Blueprints 38-42.

```text
explicit fixture smoke manifest
-> gameplay-gated many-point smoke
-> structural output summary
-> frozen regression baseline
-> verification report
```

The baseline is a regression checkpoint only. It preserves the expected shape of the local
fixture-safe gameplay gate path without creating classifier correctness, point detection,
line-call, scoring, production readiness, training-label, or generalization claims.

## Tracked Artifacts

```text
.data/contracts/gameplay_gate_regression_baseline_contract_v1.json
.data/baselines/gameplay_gate_regression.baseline.json
```

Generated verification and report outputs live under `.data/exports/` and remain local.

## Commands

```bash
make tom-v1-export-gameplay-gate-regression-baseline-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-gameplay-gate-regression-baseline \
  PYTHON=.venv/bin/python

make tom-v1-verify-gameplay-gate-regression-baseline \
  PYTHON=.venv/bin/python

make tom-v1-build-gameplay-gate-regression-report \
  PYTHON=.venv/bin/python
```

The verification gate reports `ok`, `status`, `drift_detected`, `breaking_drift_detected`,
`baseline_is_not_truth`, `gameplay_gate_is_not_truth`,
`classifier_correctness_not_assessed`, and `generalization_not_claimed`.

## Frozen Profile

The committed baseline records structural values from the fixture-only BP42 path:

- model asset existence and SHA-256 fingerprint
- source contract version refs
- threshold, smoothing, and hysteresis settings
- smoke entry count
- gameplay, non-gameplay, and uncertain segment counts
- downstream allowed, blocked, and review-required window counts
- perception execution and skipped window counts
- replay timeline entry count
- warning categories and smoke status distribution

## Boundaries

Blueprint 43 does not add or infer:

- in/out
- score
- point winner
- player identity
- rally state
- server/receiver state
- line-call truth
- point truth
- event truth
- classifier correctness
- accepted/rejected lifecycle
- coaching or tactical conclusions
- betting or prediction outputs
- generalization
- training truth
- production readiness
- adjudication

The gate does not mutate model assets, commit weights, discover media folders, run GPU/model
inference by default, or mutate protected sample-point baselines.
