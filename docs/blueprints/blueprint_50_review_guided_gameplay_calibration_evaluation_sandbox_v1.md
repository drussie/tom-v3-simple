# Blueprint 50 - Review-Guided Gameplay Calibration Evaluation Sandbox v1

Status: complete

## Goal

Blueprint 50 turns Blueprint 49 calibration proposal records into an offline-only evaluation
sandbox.

```text
BP49 calibration proposal
-> evaluation input snapshot
-> structural validation
-> offline sandbox report
-> report validation
-> summary
```

The milestone records candidate settings, read-only current gate settings, review coverage,
baseline comparison context, model asset provenance, fixture/data limitations, warnings, and
structural drift summaries without applying threshold, smoothing, hysteresis, model, label,
baseline, or runtime changes.

## Tracked Artifact

```text
.data/contracts/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.json
```

Generated evaluation inputs, validation results, sandbox reports, and summaries live under
`.data/exports/` and remain local unless a future milestone explicitly documents committing
reviewed fixtures.

## Commands

```bash
make tom-v1-export-review-guided-gameplay-calibration-evaluation-sandbox-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-evaluation-inputs \
  PYTHON=.venv/bin/python

make tom-v1-validate-review-guided-gameplay-calibration-evaluation-inputs \
  PYTHON=.venv/bin/python

make tom-v1-run-review-guided-gameplay-calibration-evaluation-sandbox \
  PYTHON=.venv/bin/python

make tom-v1-validate-review-guided-gameplay-calibration-evaluation-report \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-evaluation-summary \
  PYTHON=.venv/bin/python
```

The builders read existing BP49/BP48/BP47/BP46/BP43 artifacts when supplied. They do not run
inference, mutate model assets, mutate baselines, infer labels, alter thresholds, alter smoothing,
alter hysteresis, write runtime config, or score classifier correctness.

## Contract Summary

The contract records:

- source contract refs through BP49 and earlier gameplay path artifacts
- evaluation input, candidate setting, sandbox report, and summary schemas
- allowed candidate types, candidate statuses, evaluation modes, evaluation statuses, decision
  support statuses, and drift severities
- validation rules that reject unsupported values, exact forbidden tokens, runtime-changing fields,
  model mutation flags, and baseline replacement flags
- provenance requirements for calibration proposals, review metrics, review bundles, corpus runs,
  regression baselines, model asset refs, warnings, and non-claims

Candidate settings are sandbox records only. They must be `not_applied`, must not write runtime
config, must not mutate model assets, and must not replace regression baselines.

## Boundaries

Blueprint 50 does not add or infer:

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
- threshold, smoothing, hysteresis, baseline, model, or runtime config changes
- adjudication

The sandbox is decision-support plumbing for future human review only. It does not train a
classifier, modify model assets, commit model weights, mutate regression baselines, or create
tennis conclusions.
