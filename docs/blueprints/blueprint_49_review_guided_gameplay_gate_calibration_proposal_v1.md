# Blueprint 49 - Review-Guided Gameplay Gate Calibration Proposal v1

Status: complete

## Goal

Blueprint 49 turns Blueprint 48 review metrics into a proposal-only calibration planning layer.

```text
BP48 review metrics report
-> calibration input snapshot
-> structural validation
-> future-evaluation proposal
-> proposal validation
-> proposal report
```

The milestone records review coverage, ambiguity, boundary cases, current gate settings, model
asset provenance, fixture/data limitations, and proposed future evaluation actions without
applying threshold, smoothing, hysteresis, model, label, baseline, or runtime changes.

## Tracked Artifact

```text
.data/contracts/review_guided_gameplay_calibration_proposal_contract_v1.json
```

Generated calibration inputs, validation results, proposal JSON, and proposal reports live under
`.data/exports/` and remain local unless a future milestone explicitly documents committing
reviewed fixtures.

## Commands

```bash
make tom-v1-export-review-guided-gameplay-calibration-proposal-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-inputs \
  PYTHON=.venv/bin/python

make tom-v1-validate-review-guided-gameplay-calibration-inputs \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-proposal \
  PYTHON=.venv/bin/python

make tom-v1-validate-review-guided-gameplay-calibration-proposal \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-proposal-report \
  PYTHON=.venv/bin/python
```

The builders read existing BP48/BP47/BP46/BP44/BP43 artifacts when supplied. They do not run
inference, mutate model assets, mutate baselines, infer labels, alter thresholds, alter smoothing,
alter hysteresis, or score classifier correctness.

## Contract Summary

The contract records:

- source contract refs through BP48 and earlier gameplay path artifacts
- calibration input and proposal schemas
- allowed proposal types, statuses, future evaluation actions, and risk flags
- validation rules that reject unsupported values, exact forbidden tokens, and runtime-changing
  candidate settings
- provenance requirements for source metrics, review bundles, corpus runs, regression baselines,
  model asset refs, warnings, and non-claims

Proposal items are future-evaluation planning records only. Candidate settings must be
`not_applied`, must not write runtime config, must not affect regression baselines, and must remain
future-evaluation-only.

## Boundaries

Blueprint 49 does not add or infer:

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
- threshold, smoothing, hysteresis, baseline, or model changes
- adjudication

The proposal layer is a review planning surface only. It does not train a classifier, modify model
assets, commit model weights, mutate regression baselines, or create tennis conclusions.
