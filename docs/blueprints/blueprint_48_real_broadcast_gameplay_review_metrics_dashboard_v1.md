# Blueprint 48 - Real Broadcast Gameplay Review Metrics / QA Dashboard v1

Status: complete

## Goal

Blueprint 48 summarizes the Blueprint 47 real-broadcast gameplay review loop into
dashboard-ready review operations metrics.

```text
BP47 review bundle/report
-> BP48 metrics contract
-> review metrics report
-> QA dashboard data
-> next-review actions report
```

This milestone makes review progress, ambiguity, missing fields, replay context, model asset
provenance, and next-review priorities visible without turning review metadata into truth,
classifier scoring, automatic relabeling, or model tuning.

## Tracked Artifact

```text
.data/contracts/real_broadcast_gameplay_review_metrics_contract_v1.json
```

Generated metrics reports, validation outputs, QA dashboard data, and next-actions reports live
under `.data/exports/` and remain local unless a future milestone explicitly documents committing
review operations fixtures.

## Commands

```bash
make tom-v1-export-real-broadcast-gameplay-review-metrics-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-review-metrics-report \
  PYTHON=.venv/bin/python

make tom-v1-validate-real-broadcast-gameplay-review-metrics-report \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-review-qa-dashboard \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-review-next-actions-report \
  PYTHON=.venv/bin/python
```

The metrics builder reads existing BP47/BP46/BP44/BP43 artifacts when supplied. It does not run
inference, mutate model assets, mutate baselines, infer labels, change thresholds, or score
classifier correctness.

## Contract Summary

The contract records:

- source contract refs through the BP47 review loop and earlier gameplay path artifacts
- allowed metric groups for coverage, status distribution, downstream review decisions,
  confidence distribution, ambiguity flags, missing fields, readiness, corpus coverage, replay
  context, model asset provenance, QA warnings, and next-review actions
- dashboard card and table identifiers
- allowed next-review action types
- structural validation rules
- provenance requirements for source paths, model asset refs, warnings, and non-claims

Metrics are operational completeness and review workflow visibility only.

## Boundaries

Blueprint 48 does not add or infer:

- in/out
- score
- point winner
- player identity
- rally state
- server/receiver state
- line-call truth
- point truth
- event truth
- gameplay truth
- classifier correctness or accuracy
- accepted/rejected lifecycle
- automatic relabeling
- reviewer ranking or quality scoring
- coaching or tactical conclusions
- betting or prediction outputs
- generalization
- training truth
- production truth
- threshold, smoothing, or model changes
- adjudication

The dashboard data is a review surface input only. It does not train a classifier, modify model
assets, commit model weights, mutate regression baselines, or create tennis conclusions.
