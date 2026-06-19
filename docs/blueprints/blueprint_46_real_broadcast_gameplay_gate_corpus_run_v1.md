# Blueprint 46 - Real Broadcast Gameplay Gate Corpus Run v1

Status: complete

## Goal

Blueprint 46 creates the first controlled real-broadcast gameplay gate corpus run surface.

```text
explicit local broadcast-style clips
-> gameplay segment gate
-> gameplay-gated routing
-> gameplay-gated perception execution planning
-> gameplay segment replay timeline
-> gameplay gate review dataset export
-> corpus run summary
-> human review readiness report
```

This moves the frozen BP38-BP45 gameplay pathway from fixture-only readiness into an explicit
operator-supplied corpus workflow. It remains structural and review-oriented.

## Tracked Artifact

```text
.data/contracts/real_broadcast_gameplay_corpus_run_contract_v1.json
```

Generated manifests, validation results, corpus run outputs, per-entry artifacts, and reports live
under `.data/exports/` and remain local unless a future milestone explicitly commits them.

## Commands

```bash
make tom-v1-export-real-broadcast-gameplay-corpus-run-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-real-broadcast-gameplay-corpus-manifest-template \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_CORPUS_MEDIA_PATH=/path/to/broadcast_clip.mp4 \
  REAL_BROADCAST_GAMEPLAY_CORPUS_CONTENT_TAG=live_gameplay

make tom-v1-validate-real-broadcast-gameplay-corpus-manifest \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE=dry_run

make tom-v1-run-real-broadcast-gameplay-corpus \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE=explicit_local_media_run

make tom-v1-build-real-broadcast-gameplay-corpus-report \
  PYTHON=.venv/bin/python
```

Default run mode is `dry_run`. Real local media processing requires an explicit manifest and an
explicit real-data run mode. TOM does not scan folders or ingest arbitrary media.

## Contract Summary

The contract records:

- allowed run modes: `dry_run`, `validate_only`, `fixture_only`,
  `structural_real_data_run`, and `explicit_local_media_run`
- allowed expected broadcast content tags, such as `live_gameplay`, `replay_package`,
  `commercial`, `broadcast_graphic`, `crowd_cutaway`, and `unknown`
- allowed requested structural steps
- disallowed steps such as creating truth, scoring points, identifying players, adjudicating,
  generating training labels, proving generalization, or calculating classifier accuracy
- source contract refs for BP38-BP45 and review/corpus/calibration contracts
- provenance requirements, warnings, and non-claims

Expected broadcast content tags are operator context only. They are not truth labels.

## Boundaries

Blueprint 46 does not add or infer:

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
- reviewer ranking or quality scoring
- coaching or tactical conclusions
- betting or prediction outputs
- generalization
- training truth
- production truth
- adjudication

The corpus run does not train a classifier, modify model assets, commit model weights, mutate
regression baselines, silently scan folders, or create tennis conclusions.
