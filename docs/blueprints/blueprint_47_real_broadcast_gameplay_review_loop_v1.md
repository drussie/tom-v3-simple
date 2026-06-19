# Blueprint 47 - Real Broadcast Gameplay Review Loop v1

Status: complete

## Goal

Blueprint 47 creates the first structured human review loop over real-broadcast gameplay gate
corpus outputs.

```text
BP46 corpus run outputs
-> gameplay gate review dataset entries
-> review bundle template
-> filled human review metadata
-> bundle validation
-> review-loop report
-> human review readiness report
```

This milestone makes BP46 reviewable by operators without turning review metadata into truth,
classifier scoring, or automatic relabeling.

## Tracked Artifact

```text
.data/contracts/real_broadcast_gameplay_review_loop_contract_v1.json
```

Generated review bundle templates, validations, review-loop reports, and human review readiness
reports live under `.data/exports/` and remain local unless a future milestone explicitly commits
a reviewed fixture.

## Commands

```bash
make tom-v1-export-real-broadcast-gameplay-review-loop-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-review-bundle-template \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_CORPUS_RUN=.data/exports/real_broadcast_gameplay_corpus_run.current.json

make tom-v1-validate-real-broadcast-gameplay-review-bundle \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-review-loop-report \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-human-review-readiness-report \
  PYTHON=.venv/bin/python
```

The bundle builder reads existing BP46/BP44 artifacts. It does not run inference, mutate model
assets, mutate baselines, infer labels, or score classifier correctness.

## Contract Summary

The contract records:

- BP46 corpus run and BP44 review dataset source refs
- BP38-BP45 gameplay path contract refs plus existing review/corpus/ops refs
- review bundle, entry, validation, report, and readiness payload requirements
- allowed reviewed segment statuses, downstream gate review statuses, confidence values,
  ambiguity flags, and review source values
- required warnings and non-claims for review metadata only
- forbidden exact fields/values that would imply truth, adjudication, scoring, reviewer ranking,
  classifier accuracy, production readiness, or automatic relabeling

Human review values are metadata. They do not modify source artifacts or create labels.

## Boundaries

Blueprint 47 does not add or infer:

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
- adjudication

The review loop does not train a classifier, modify model assets, commit model weights, mutate
regression baselines, or create tennis conclusions.
