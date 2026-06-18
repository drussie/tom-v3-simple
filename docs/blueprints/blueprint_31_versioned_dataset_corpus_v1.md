# Blueprint 31 Versioned Dataset Corpus v1

Status: complete

Blueprint 31 adds a versioned dataset corpus contract and manifest/report layer over existing TOM
evidence, provenance, review, reviewer-confidence, multi-reviewer disagreement, INTENNSE alignment,
and regression structures.

This milestone is a dataset-corpus foundation only. It packages existing TOM artifacts into
versioned corpus entries, preserves replay and run-ID context, reports structural provenance gaps,
and keeps protected sample-point evidence marked as regression-protected when inferable from
existing manifest labels.

It does not create training truth, automatic review labels, automatic correctness claims, in/out,
score, point winner, player identity, rally state, server/receiver state, reviewer ranking,
reviewer scoring, disagreement resolution, INTENNSE conclusions, coaching/tactical conclusions,
betting or prediction, generalization claims, or adjudication.

## Commands

Export the frozen corpus contract:

```bash
.venv/bin/python -m apps.worker.cli export-versioned-dataset-corpus-contract \
  --output ".data/contracts/versioned_dataset_corpus_contract_v1.json" \
  --skip-create-db
```

Build a corpus manifest from the existing multi-point replay index and regression matrix:

```bash
.venv/bin/python -m apps.worker.cli build-versioned-dataset-corpus-manifest \
  --index ".data/manifests/multi_point_replay_index.json" \
  --matrix ".data/exports/multi_point_regression_matrix.current.json" \
  --output ".data/exports/versioned_dataset_corpus_manifest.current.json" \
  --skip-create-db
```

Validate a corpus manifest structurally:

```bash
.venv/bin/python -m apps.worker.cli validate-versioned-dataset-corpus-manifest \
  --contract ".data/contracts/versioned_dataset_corpus_contract_v1.json" \
  --manifest ".data/exports/versioned_dataset_corpus_manifest.current.json" \
  --observation-quality-taxonomy ".data/contracts/observation_quality_taxonomy_v1.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --multi-reviewer-schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --intennse-alignment-contract ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --output ".data/exports/versioned_dataset_corpus_manifest.validation.json" \
  --skip-create-db
```

Build a structural corpus report:

```bash
.venv/bin/python -m apps.worker.cli build-versioned-dataset-corpus-report \
  --contract ".data/contracts/versioned_dataset_corpus_contract_v1.json" \
  --manifest ".data/exports/versioned_dataset_corpus_manifest.current.json" \
  --observation-quality-taxonomy ".data/contracts/observation_quality_taxonomy_v1.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --multi-reviewer-schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --intennse-alignment-contract ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --output ".data/exports/versioned_dataset_corpus_report.current.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-versioned-dataset-corpus-contract PYTHON=.venv/bin/python
make tom-v1-build-versioned-dataset-corpus-manifest PYTHON=.venv/bin/python
make tom-v1-validate-versioned-dataset-corpus-manifest \
  PYTHON=.venv/bin/python \
  DATASET_CORPUS_MANIFEST=.data/exports/versioned_dataset_corpus_manifest.current.json
make tom-v1-build-versioned-dataset-corpus-report \
  PYTHON=.venv/bin/python \
  DATASET_CORPUS_MANIFEST=.data/exports/versioned_dataset_corpus_manifest.current.json
```

## Paths

Default local paths:

```text
.data/contracts/versioned_dataset_corpus_contract_v1.json
.data/exports/versioned_dataset_corpus_manifest.current.json
.data/exports/versioned_dataset_corpus_manifest.validation.json
.data/exports/versioned_dataset_corpus_report.current.json
```

The contract under `.data/contracts` is committed as the frozen v1 corpus contract. Generated
`.data/exports` corpus manifests, validation outputs, and reports are local outputs and should not
be committed unless intentionally documented.

## Contract Shape

The contract records:

- `contract_type`: `versioned_dataset_corpus_contract`
- `contract_version`: `v1`
- `corpus_manifest_type`: `versioned_dataset_corpus_manifest`
- `corpus_manifest_version`: `v1`
- corpus scope
- corpus entities
- corpus entry fields
- corpus split policy
- corpus versioning policy
- provenance requirements
- included contract refs
- corpus value sets
- validation rules
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication warnings

Referenced contract versions:

- `observation_quality_taxonomy_version`: `v1`
- `review_label_schema_version`: `v1`
- `reviewer_confidence_schema_version`: `v1`
- `multi_reviewer_disagreement_schema_version`: `v1`
- `intennse_label_alignment_contract_version`: `v1`
- `multi_point_regression_matrix_version`: `v0`
- `point_manifest_version`: `v0`

Allowed corpus split values are `unassigned`, `holdout_candidate`, `review_candidate`,
`regression_protected`, and `not_applicable`. The current generated manifest uses
`regression_protected` for protected sample-point entries and `unassigned` for other entries. Split
metadata is not training truth.

## Manifest Behavior

The manifest builder reads the existing Blueprint 24 replay index and Blueprint 25 regression
matrix. It preserves:

- point manifest identity
- media identity
- replay URL
- event candidate, trajectory 3D, and camera geometry run IDs when present
- source/stored media references when present
- point manifest path
- source index and source matrix paths
- evidence availability
- profile counts
- source warnings
- provenance-only labels from existing manifests/indexes/matrices

Missing optional observation-quality, review-label, reviewer-confidence, multi-reviewer,
disagreement-report, INTENNSE-alignment, and dataset-export refs are recorded as provenance gaps,
not errors.

## Validation Behavior

Validation checks contract shape, corpus manifest type/version, included contract refs, source
index/matrix path existence, entry required fields, allowed split/status values, referenced
Blueprint 26 through 30 contract versions when paths are available, and forbidden fields.

Validation reports structural errors and provenance warnings only. It does not infer missing
labels, create labels, judge label correctness, resolve disagreement, create truth, or create
training truth.

## Report Behavior

The report summarizes corpus entries, evidence availability, provenance completeness, missing
optional refs, and review-readiness signals using structural language such as
`corpus_entry_present`, `missing_optional_review_ref`, `provenance_partial`,
`requires_human_review`, and `regression_protected_entry`.

The report does not evaluate tennis quality, decide correctness, infer expert interpretation,
resolve disagreement, create labels, or adjudicate evidence.

## Boundaries

Blueprint 31 does not add or change:

- in/out
- score
- point winner
- player identity
- rally state
- server or receiver state
- accepted/rejected lifecycle
- marker arbitration
- event generation
- 3D generation
- coaching or tactical conclusions
- INTENNSE tactical conclusions
- INTENNSE coaching conclusions
- INTENNSE match outcome conclusions
- adjudication
- betting or prediction
- generalization claims
- automatic correctness claims
- automatic review labels
- automatic truth labels
- automatic confidence scores
- reviewer ranking
- reviewer quality scoring
- disagreement resolution
- training truth
