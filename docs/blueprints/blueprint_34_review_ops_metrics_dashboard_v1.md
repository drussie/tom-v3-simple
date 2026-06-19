# Blueprint 34 - Review Operations Metrics / Label Throughput Dashboard v1

Status: complete

## Goal

Create a review-operations metrics contract and read-only dashboard data layer that summarizes
structural TOM review progress without changing evidence, labels, truth, scoring, ingestion, or
sampling behavior.

This milestone is operations visibility only. TOM reports whether review-support artifacts are
present, missing, partial, or structurally ready. TOM does not decide whether any label is correct,
rank reviewers, score reviewer quality, resolve disagreement, infer tennis truth, or create
review labels.

## Added

- `apps.worker.services.review_ops_metrics`
- `export-review-ops-metrics-contract`
- `build-review-ops-metrics-report`
- `validate-review-ops-metrics-report`
- `build-review-ops-dashboard-data`
- `tom-v1-export-review-ops-metrics-contract`
- `tom-v1-build-review-ops-metrics-report`
- `tom-v1-validate-review-ops-metrics-report`
- `tom-v1-build-review-ops-dashboard-data`
- `.data/contracts/review_ops_metrics_contract_v1.json`

Generated report/dashboard artifacts are written under `.data/exports/` and remain local ignored
outputs.

## Contract

The contract records:

- metrics scope
- source contract refs for Blueprints 26 through 33 plus point manifests and the multi-point matrix
- metric groups
- dashboard card schema
- report schema
- allowed structural metric statuses
- provenance requirements
- validation rules
- no-truth/no-adjudication warnings

## Metric Groups

The report summarizes structural counts for:

- corpus entry counts
- review label coverage
- reviewer confidence coverage
- multi-reviewer coverage
- disagreement report coverage
- INTENNSE alignment coverage
- observation quality coverage
- provenance completeness
- ingestion gate readiness
- coverage sampling gaps
- regression protection coverage
- missing optional refs
- human review required counts

## Dashboard Data

`build-review-ops-dashboard-data` reads a review-ops metrics report and writes dashboard-ready JSON
cards, metric groups, source paths, warnings, and summary counts. The output is read-only and does
not mutate DB rows, media, evidence, labels, review bundles, or source artifacts.

## Boundaries

Blueprint 34 does not add:

- in/out
- score
- point winner
- player identity
- rally state
- server/receiver state
- accepted/rejected lifecycle
- marker arbitration
- event generation
- 3D generation
- automatic correctness claims
- automatic review labels
- automatic confidence scores
- reviewer ranking
- reviewer quality scoring
- disagreement resolution
- INTENNSE coaching/tactical/match conclusions
- training truth
- automatic media ingestion
- automatic sampling execution

## Validation

Required local smokes:

```bash
make tom-v1-export-review-ops-metrics-contract PYTHON=.venv/bin/python

make tom-v1-build-review-ops-metrics-report PYTHON=.venv/bin/python

make tom-v1-validate-review-ops-metrics-report \
  PYTHON=.venv/bin/python \
  REVIEW_OPS_METRICS_REPORT=.data/exports/review_ops_metrics_report.current.json

make tom-v1-build-review-ops-dashboard-data \
  PYTHON=.venv/bin/python \
  REVIEW_OPS_METRICS_REPORT=.data/exports/review_ops_metrics_report.current.json
```

Expected:

- `ok`: true
- `status`: `completed` for export/report/dashboard commands
- `status`: `valid` for validation
- `report_type`: `review_ops_metrics_report`
- `dashboard_data_type`: `review_ops_dashboard_data`
- `warnings.review_ops_metrics_are_not_truth`: true
- `warnings.read_only_dashboard_data`: true
