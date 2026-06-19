# Blueprint 44 - Gameplay Gate Review Dataset Export v1

Status: complete

## Goal

Blueprint 44 exports gameplay gate candidate segments and their structural context into a
reviewable dataset bundle.

```text
gameplay segment candidates
-> routing plan
-> perception execution plan
-> replay timeline
-> regression baseline context
-> review dataset export
-> human review bundle
```

The export is review infrastructure only. It gives operators replay URLs, timestamp windows,
source artifact paths, model asset provenance, gate configuration, regression context, and blank
human review metadata fields without creating review labels or tennis conclusions.

## Tracked Artifact

```text
.data/contracts/gameplay_gate_review_dataset_export_contract_v1.json
```

Generated dataset, validation, and report outputs live under `.data/exports/` and remain local.

## Commands

```bash
make tom-v1-export-gameplay-gate-review-dataset-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-gameplay-gate-review-dataset \
  PYTHON=.venv/bin/python

make tom-v1-validate-gameplay-gate-review-dataset \
  PYTHON=.venv/bin/python

make tom-v1-build-gameplay-gate-review-dataset-report \
  PYTHON=.venv/bin/python
```

The build command reads supplied gameplay segment, routing, execution, replay timeline, and
regression artifacts when present. When they are not supplied, it creates fixture-safe local
source artifacts under the configured work directory using existing BP38-BP41 structural builders.

## Review Entry Shape

Each dataset entry preserves:

- segment identity, timestamps, and frame bounds
- replay URL with segment query parameters
- gameplay and non-gameplay probability values from the source segment candidate
- raw, smoothed, segment, downstream gate, routing, and execution statuses
- replay timeline entry id when available
- regression baseline/verification context when available
- blank human review fields using neutral default values
- provenance status and no-truth warnings

## Boundaries

Blueprint 44 does not add or infer:

- in/out
- score
- point winner
- player identity
- rally state
- server/receiver state
- line-call truth
- point truth
- event truth
- classifier correctness
- accepted/rejected lifecycle
- automatic relabeling
- reviewer ranking or scoring
- coaching or tactical conclusions
- betting or prediction outputs
- generalization
- training truth
- production readiness
- adjudication

The export does not mutate model assets, commit weights, modify regression baselines, discover
media folders, create observations, run downstream perception jobs, or score the classifier.
