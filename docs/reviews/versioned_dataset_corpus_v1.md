# Versioned Dataset Corpus v1

The versioned dataset corpus contract packages existing TOM point manifests, replay index rows,
multi-point regression matrix rows, review-support contract refs, and future INTENNSE alignment
refs into a durable corpus manifest.

It is not truth, training truth, scoring, player identity, point winner, in/out, automatic
labeling, correctness validation, reviewer scoring, disagreement resolution, INTENNSE conclusion,
coaching output, tactical output, match-outcome output, or adjudication.

## Build

```bash
make tom-v1-export-versioned-dataset-corpus-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-versioned-dataset-corpus-manifest \
  PYTHON=.venv/bin/python
```

Validate a corpus manifest:

```bash
make tom-v1-validate-versioned-dataset-corpus-manifest \
  PYTHON=.venv/bin/python \
  DATASET_CORPUS_MANIFEST=.data/exports/versioned_dataset_corpus_manifest.current.json
```

Build a structural corpus report:

```bash
make tom-v1-build-versioned-dataset-corpus-report \
  PYTHON=.venv/bin/python \
  DATASET_CORPUS_MANIFEST=.data/exports/versioned_dataset_corpus_manifest.current.json
```

Default paths:

```text
.data/contracts/versioned_dataset_corpus_contract_v1.json
.data/exports/versioned_dataset_corpus_manifest.current.json
.data/exports/versioned_dataset_corpus_manifest.validation.json
.data/exports/versioned_dataset_corpus_report.current.json
```

## Expected Contract

- `contract_type`: `versioned_dataset_corpus_contract`
- `contract_version`: `v1`
- `corpus_manifest_type`: `versioned_dataset_corpus_manifest`
- `corpus_manifest_version`: `v1`
- contract refs for Blueprints 26 through 30, Blueprint 25 matrix v0, and Blueprint 23 point manifests v0
- corpus entities for point entries, evidence refs, replay refs, review refs, disagreement refs, INTENNSE refs, regression refs, and export refs
- allowed split values that do not include training truth assignments
- explicit no-truth/no-adjudication/no-training-truth warnings

## Validation Semantics

Validation checks structure, source index/matrix paths, allowed corpus split/status values,
forbidden fields, included contract refs, and referenced contract versions when paths are
available.

Missing optional review, observation-quality, disagreement, INTENNSE, and dataset-export refs are
provenance gaps. They are not labels, errors, or adjudications.

Validation does not infer missing labels, create labels, judge correctness, create truth, create
training truth, or resolve disagreement.

## Caveat

A structurally valid corpus manifest can still be incomplete. Blueprint 31 reports incomplete
review/INTENNSE/export provenance as structural context only.
