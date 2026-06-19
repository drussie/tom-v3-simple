# Label Feedback Loop into Evaluation Harness v1

Blueprint 35 adds a structural bridge from TOM review artifacts into the evaluation harness.

The bridge reads existing local artifacts where available:

- versioned dataset corpus manifest
- review-ops metrics report/dashboard data
- coverage sampling profile/report
- multi-point regression matrix
- frozen TOM contracts under `.data/contracts`

It then emits label-feedback evaluation inputs with structural signal types, statuses, and routing
actions. These actions are evaluation-harness routing metadata only: include a point as structural
context, flag a missing review artifact, preserve a regression-protected sample, or flag a
provenance gap.

The current sample/demo outputs are expected to show one protected sample-point feedback entry with
missing optional review-support refs. That is useful for harness wiring only; it is not proof of
many real points, model generalization, training truth, or label validity.

## Commands

```bash
make tom-v1-export-label-feedback-evaluation-contract PYTHON=.venv/bin/python

make tom-v1-build-label-feedback-evaluation-inputs PYTHON=.venv/bin/python

make tom-v1-validate-label-feedback-evaluation-inputs \
  PYTHON=.venv/bin/python \
  LABEL_FEEDBACK_EVALUATION_INPUTS=.data/exports/label_feedback_evaluation_inputs.current.json

make tom-v1-build-label-feedback-evaluation-report \
  PYTHON=.venv/bin/python \
  LABEL_FEEDBACK_EVALUATION_INPUTS=.data/exports/label_feedback_evaluation_inputs.current.json
```

## Outputs

- `.data/contracts/label_feedback_evaluation_contract_v1.json`
- `.data/exports/label_feedback_evaluation_inputs.current.json`
- `.data/exports/label_feedback_evaluation_inputs.validation.json`
- `.data/exports/label_feedback_evaluation_report.current.json`

Only the contract is committed. Generated exports remain ignored local outputs.

## Non-Goals

The feedback bridge does not create evidence, create labels, generate confidence scores, rank
reviewers, score reviewer quality, resolve disagreement, import INTENNSE conclusions, create
training truth, decide tennis outcomes, ingest media, execute sampling, retrain models, modify
evaluation baselines, or adjudicate evidence.
