# Blueprint 35 - Label Feedback Loop into Evaluation Harness v1

Status: complete

## Goal

Create a label-feedback evaluation bridge that turns existing TOM review/corpus/coverage/metrics
artifacts into structural evaluation harness inputs.

This milestone is feedback-loop infrastructure only. It routes evidence-aware review structure into
evaluation coverage and regression diagnostics. TOM does not decide candidate validity, create truth
labels, create review labels, rank reviewers, score reviewer quality, resolve disagreement, retrain
models, or produce tennis conclusions.

## Added

- `apps.worker.services.label_feedback_evaluation`
- `export-label-feedback-evaluation-contract`
- `build-label-feedback-evaluation-inputs`
- `validate-label-feedback-evaluation-inputs`
- `build-label-feedback-evaluation-report`
- `tom-v1-export-label-feedback-evaluation-contract`
- `tom-v1-build-label-feedback-evaluation-inputs`
- `tom-v1-validate-label-feedback-evaluation-inputs`
- `tom-v1-build-label-feedback-evaluation-report`
- `.data/contracts/label_feedback_evaluation_contract_v1.json`

Generated feedback inputs, validations, and reports are written under `.data/exports/` and remain
local ignored outputs.

## Contract

The contract records:

- feedback scope
- source contract refs for Blueprints 26 through 34 plus point manifests and the multi-point matrix
- feedback input entities and entry fields
- evaluation bridge schema
- allowed evaluation signal types
- allowed evaluation signal statuses
- allowed evaluation harness routing actions
- provenance requirements
- validation rules
- no-truth/no-adjudication warnings

## Feedback Inputs

`build-label-feedback-evaluation-inputs` reads available local artifacts:

- versioned dataset corpus manifest
- review-ops metrics report
- review-ops dashboard data
- coverage sampling profile/report
- multi-point regression matrix

It emits one structural feedback entry per corpus entry. Entries preserve replay URLs, run IDs,
evidence availability, profile counts, provenance status, coverage gaps, review artifact refs, and
regression context. Missing review artifacts become gaps and routing actions, not label decisions.

## Report

`build-label-feedback-evaluation-report` summarizes:

- structural feedback entries
- review artifact gaps
- confidence artifact gaps
- disagreement context availability
- INTENNSE alignment gaps
- provenance gaps
- coverage gaps
- regression-protected entries
- structural evaluation routing actions

## Boundaries

Blueprint 35 does not add:

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
- automatic review labels
- automatic confidence scores
- reviewer ranking
- reviewer quality scoring
- disagreement resolution
- INTENNSE coaching/tactical/match conclusions
- training truth
- model retraining
- evaluation pass/fail from human labels
- automatic media ingestion
- automatic sampling execution
- adjudication

## Validation

Required local smokes:

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

Expected:

- `ok`: true
- `status`: `completed` for export/input/report commands
- `status`: `valid` for validation
- `contract_type`: `label_feedback_evaluation_contract`
- `feedback_inputs_type`: `label_feedback_evaluation_inputs`
- `report_type`: `label_feedback_evaluation_report`
- `warnings.label_feedback_evaluation_is_not_truth`: true
- `warnings.evaluation_bridge_is_structural_only`: true
