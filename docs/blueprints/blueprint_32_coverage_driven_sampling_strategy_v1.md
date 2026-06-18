# Blueprint 32 Coverage-Driven Sampling Strategy v1

Status: complete

Blueprint 32 adds a versioned coverage-driven sampling strategy contract, profile builder,
structural validator, and report layer over the existing versioned dataset corpus. It helps TOM
describe structural evidence, provenance, review, and alignment coverage gaps for future controlled
dataset expansion.

This milestone is planning/provenance infrastructure only. It reads existing corpus, replay-index,
and regression-matrix artifacts, preserves replay and run-ID context, and emits structural coverage
candidates with planning labels such as `coverage_gap_present`, `requires_human_review`,
`distinct_second_point_needed`, `demo_stand_in_only`, and `structural_sampling_candidate`.

It does not ingest media, generate observations, create event candidates, create 3D candidates,
create training truth, create automatic labels, score correctness, infer expert interpretation,
resolve disagreement, rank reviewers, decide in/out, score, point winner, player identity, rally
state, server/receiver state, coaching/tactical conclusions, match outcomes, betting or prediction,
generalization claims, or adjudication.

## Commands

Export the frozen coverage sampling strategy contract:

```bash
.venv/bin/python -m apps.worker.cli export-coverage-sampling-strategy-contract \
  --output ".data/contracts/coverage_sampling_strategy_contract_v1.json" \
  --skip-create-db
```

Build a coverage sampling profile from the versioned dataset corpus manifest:

```bash
.venv/bin/python -m apps.worker.cli build-coverage-sampling-profile \
  --corpus-manifest ".data/exports/versioned_dataset_corpus_manifest.current.json" \
  --index ".data/manifests/multi_point_replay_index.json" \
  --matrix ".data/exports/multi_point_regression_matrix.current.json" \
  --output ".data/exports/coverage_sampling_profile.current.json" \
  --skip-create-db
```

Validate a coverage sampling profile structurally:

```bash
.venv/bin/python -m apps.worker.cli validate-coverage-sampling-profile \
  --contract ".data/contracts/coverage_sampling_strategy_contract_v1.json" \
  --profile ".data/exports/coverage_sampling_profile.current.json" \
  --observation-quality-taxonomy ".data/contracts/observation_quality_taxonomy_v1.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --multi-reviewer-schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --intennse-alignment-contract ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --dataset-corpus-contract ".data/contracts/versioned_dataset_corpus_contract_v1.json" \
  --output ".data/exports/coverage_sampling_profile.validation.json" \
  --skip-create-db
```

Build a structural coverage sampling report:

```bash
.venv/bin/python -m apps.worker.cli build-coverage-sampling-report \
  --contract ".data/contracts/coverage_sampling_strategy_contract_v1.json" \
  --profile ".data/exports/coverage_sampling_profile.current.json" \
  --observation-quality-taxonomy ".data/contracts/observation_quality_taxonomy_v1.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --multi-reviewer-schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --intennse-alignment-contract ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --dataset-corpus-contract ".data/contracts/versioned_dataset_corpus_contract_v1.json" \
  --output ".data/exports/coverage_sampling_report.current.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-coverage-sampling-strategy-contract PYTHON=.venv/bin/python
make tom-v1-build-coverage-sampling-profile PYTHON=.venv/bin/python
make tom-v1-validate-coverage-sampling-profile \
  PYTHON=.venv/bin/python \
  COVERAGE_SAMPLING_PROFILE=.data/exports/coverage_sampling_profile.current.json
make tom-v1-build-coverage-sampling-report \
  PYTHON=.venv/bin/python \
  COVERAGE_SAMPLING_PROFILE=.data/exports/coverage_sampling_profile.current.json
```

## Paths

Default local paths:

```text
.data/contracts/coverage_sampling_strategy_contract_v1.json
.data/exports/coverage_sampling_profile.current.json
.data/exports/coverage_sampling_profile.validation.json
.data/exports/coverage_sampling_report.current.json
```

The contract under `.data/contracts` is committed as the frozen v1 coverage sampling strategy
contract. Generated `.data/exports` coverage sampling profiles, validation outputs, and reports are
local outputs and should not be committed unless intentionally documented.

## Contract Shape

The contract records:

- `contract_type`: `coverage_sampling_strategy_contract`
- `contract_version`: `v1`
- `profile_type`: `coverage_sampling_profile`
- `profile_version`: `v1`
- `report_type`: `coverage_sampling_report`
- `report_version`: `v1`
- strategy scope
- source contract refs
- coverage axes
- coverage gap types
- sampling priority values
- sampling candidate fields
- allowed next-action values
- provenance requirements
- validation rules
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication/no-sampling-execution warnings

Referenced contract versions:

- `observation_quality_taxonomy_version`: `v1`
- `review_label_schema_version`: `v1`
- `reviewer_confidence_schema_version`: `v1`
- `multi_reviewer_disagreement_schema_version`: `v1`
- `intennse_label_alignment_contract_version`: `v1`
- `versioned_dataset_corpus_contract_version`: `v1`
- `multi_point_regression_matrix_version`: `v0`
- `point_manifest_version`: `v0`

## Profile Behavior

The profile builder reads the existing Blueprint 31 corpus manifest and optionally the Blueprint 24
replay index and Blueprint 25 regression matrix. It preserves:

- source corpus entry identity
- point manifest identity
- media identity
- replay URL
- event candidate, trajectory 3D, and camera geometry run IDs when present
- evidence availability
- profile counts
- provenance-only labels from the source corpus
- source warnings

Coverage gaps are structural planning context only. Missing optional observation-quality,
review-label, reviewer-confidence, multi-reviewer, disagreement-report, and INTENNSE-alignment refs
are coverage gaps, not errors.

## Validation Behavior

Validation checks contract shape, profile type/version, source paths, referenced Blueprint 26
through 31 contract versions when paths are available, candidate required fields, allowed coverage
axes, allowed gap types, allowed priority values, allowed next-action values, and forbidden fields.

Validation reports structural errors and coverage warnings only. It does not infer missing labels,
create labels, judge label validity, resolve disagreement, create truth, create training truth, or
execute sampling.

## Report Behavior

The report summarizes coverage axes, coverage gaps, sampling priorities, missing optional refs, and
structural candidate counts. Report language uses structural terms such as
`coverage_gap_present`, `missing_optional_ref`, `provenance_partial`, `requires_human_review`,
`distinct_second_point_needed`, `demo_stand_in_only`, and `structural_sampling_candidate`.

The report does not evaluate tennis quality, decide correctness, infer expert interpretation,
resolve disagreement, execute next actions, create labels, or adjudicate evidence.

## Boundaries

Blueprint 32 does not add or change:

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
- automatic corpus sampling execution
- automatic media ingestion
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
