# Blueprint 51 - Calibration Evaluation Sandbox Regression Gate v1

Status: complete

## Goal

Blueprint 51 freezes the Blueprint 50 calibration evaluation sandbox as a structural regression
gate.

```text
BP50 evaluation inputs/report
-> BP51 regression contract
-> frozen calibration sandbox baseline
-> current structural summary
-> baseline verification
-> regression report
```

The gate compares provenance, candidate-setting semantics, blocked candidate handling, not-applied
counts, offline evaluation summaries, warning categories, non-claims, model asset SHA, and
read-only threshold/smoothing/hysteresis metadata. It does not apply calibration.

## Tracked Artifacts

```text
.data/contracts/review_guided_gameplay_calibration_sandbox_regression_contract_v1.json
.data/baselines/review_guided_gameplay_calibration_sandbox.baseline.json
```

Generated current summaries, verification reports, and regression reports live under
`.data/exports/` and remain local.

## Commands

```bash
make tom-v1-export-review-guided-gameplay-calibration-sandbox-regression-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-baseline \
  PYTHON=.venv/bin/python

make tom-v1-verify-review-guided-gameplay-calibration-sandbox-regression-baseline \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-report \
  PYTHON=.venv/bin/python
```

The default baseline is fixture-reuse-only because it reuses the existing local BP50 sandbox
fixtures. It is not a distinct real broadcast corpus and does not claim generalization.

## Boundaries

Blueprint 51 is regression protection only. It does not decide or infer in/out, score, point
winner, player identity, rally state, server/receiver state, line-call truth, point truth, event
truth, gameplay truth, classifier correctness, classifier accuracy, accepted/rejected lifecycle,
automatic relabeling, reviewer ranking or quality scoring, coaching/tactical conclusions,
betting/prediction outcomes, generalization, training truth, production truth, or adjudication.

It does not train, tune, or mutate model assets. It does not apply threshold, smoothing, or
hysteresis changes. It does not update runtime config and does not replace the gameplay regression
baseline.
