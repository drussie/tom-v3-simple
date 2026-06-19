# Review Operations Metrics / Label Throughput Dashboard v1

Blueprint 34 adds a read-only operations visibility layer for TOM review progress.

The layer reads existing local artifacts where available:

- versioned dataset corpus manifest
- coverage sampling profile/report
- many-point ingestion gate report
- frozen TOM contracts under `.data/contracts`

It then emits structural counts and dashboard cards for review label coverage, confidence coverage,
multi-reviewer coverage, disagreement coverage, INTENNSE alignment coverage, provenance
completeness, ingestion readiness, coverage gaps, regression protection, and human review required
counts.

The report treats missing optional review, confidence, disagreement, INTENNSE, observation-quality,
and export refs as structural gaps. Those gaps do not mean a label is wrong. They do not rank
reviewers, resolve disagreement, or infer truth.

Current sample/demo outputs are expected to show one protected sample-point corpus entry with
missing optional review-support refs. That is useful for dashboard wiring only; it is not proof of
many real points, model generalization, training truth, or review correctness.

## Commands

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

## Outputs

- `.data/contracts/review_ops_metrics_contract_v1.json`
- `.data/exports/review_ops_metrics_report.current.json`
- `.data/exports/review_ops_metrics_report.validation.json`
- `.data/exports/review_ops_dashboard_data.current.json`

Only the contract is committed. Generated exports remain ignored local outputs.

## Non-Goals

The review-ops dashboard layer does not create evidence, labels, confidence scores, reviewer
scores, reviewer rankings, disagreement resolutions, INTENNSE conclusions, training truth, in/out,
score, point winner, player identity, event candidates, 3D candidates, sampling execution, media
ingestion, or adjudication.
