# Blueprint 55 - Controlled Runtime Calibration Change Request v1

Status: complete

## Goal

Blueprint 55 creates the first controlled runtime calibration change-request mechanism for the
gameplay gate calibration pathway.

```text
BP54 decision phase freeze
-> BP55 change-request contract
-> change-request inputs
-> controlled change request
-> structural dry-run / rollback plan
-> change-request report
```

This is a request, validation, dry-run planning, and rollback-planning layer only. It does not
apply threshold, smoothing, or hysteresis changes; update runtime config; modify the TOM v1
gameplay classifier; update model weights; replace baselines; create production config; or perform
automatic approval or rejection.

## Tracked Artifacts

```text
.data/contracts/controlled_runtime_calibration_change_request_contract_v1.json
.data/contracts/controlled_runtime_calibration_change_request_v1.json
```

Generated inputs, validation results, dry-run outputs, and reports live under `.data/exports/` and
remain local.

## Commands

```bash
make tom-v1-export-controlled-runtime-calibration-change-request-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-controlled-runtime-calibration-change-request-inputs \
  PYTHON=.venv/bin/python

make tom-v1-validate-controlled-runtime-calibration-change-request-inputs \
  PYTHON=.venv/bin/python

make tom-v1-build-controlled-runtime-calibration-change-request \
  PYTHON=.venv/bin/python

make tom-v1-validate-controlled-runtime-calibration-change-request \
  PYTHON=.venv/bin/python

make tom-v1-build-controlled-runtime-calibration-change-request-dry-run \
  PYTHON=.venv/bin/python

make tom-v1-validate-controlled-runtime-calibration-change-request-dry-run \
  PYTHON=.venv/bin/python

make tom-v1-build-controlled-runtime-calibration-change-request-report \
  PYTHON=.venv/bin/python
```

## Current Request State

The committed change request records the current BP53 source state:

```text
candidate_config_status: no_candidate_selected
change_request_status: informational_only
approval_status: human_approval_required
runtime_application_status: not_applied
dry_run_required: true
rollback_plan_required: true
```

That state is intentionally conservative. It preserves a reviewable request contract and rollback
plan without selecting or applying any runtime calibration candidate.

## Boundaries

Blueprint 55 does not decide tennis truth, gameplay truth, line-call truth, in/out, score, point
winner, player identity, rally state, server/receiver state, event truth, reviewer quality,
classifier correctness, classifier accuracy, production readiness, or generalization.

It does not train or mutate the gameplay classifier, commit model weights, create labels, score the
classifier, alter thresholds, alter smoothing, alter hysteresis, update runtime config, replace
baselines, create production config, or perform automatic approval or rejection. Future runtime
application still requires a separate blueprint and explicit human approval.
