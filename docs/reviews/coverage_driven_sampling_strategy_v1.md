# Coverage-Driven Sampling Strategy v1

The coverage-driven sampling strategy contract defines how TOM describes structural evidence,
provenance, review, and alignment coverage gaps for future controlled corpus expansion.

It is not truth, training truth, scoring, player identity, point winner, in/out, automatic
labeling, correctness validation, reviewer scoring, disagreement resolution, INTENNSE conclusion,
coaching output, tactical output, match-outcome output, sampling execution, media ingestion, or
adjudication.

## Build

```bash
make tom-v1-export-coverage-sampling-strategy-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-coverage-sampling-profile \
  PYTHON=.venv/bin/python
```

Validate a coverage sampling profile:

```bash
make tom-v1-validate-coverage-sampling-profile \
  PYTHON=.venv/bin/python \
  COVERAGE_SAMPLING_PROFILE=.data/exports/coverage_sampling_profile.current.json
```

Build a structural coverage sampling report:

```bash
make tom-v1-build-coverage-sampling-report \
  PYTHON=.venv/bin/python \
  COVERAGE_SAMPLING_PROFILE=.data/exports/coverage_sampling_profile.current.json
```

Default paths:

```text
.data/contracts/coverage_sampling_strategy_contract_v1.json
.data/exports/coverage_sampling_profile.current.json
.data/exports/coverage_sampling_profile.validation.json
.data/exports/coverage_sampling_report.current.json
```

## Expected Contract

- `contract_type`: `coverage_sampling_strategy_contract`
- `contract_version`: `v1`
- `profile_type`: `coverage_sampling_profile`
- `profile_version`: `v1`
- `report_type`: `coverage_sampling_report`
- `report_version`: `v1`
- contract refs for Blueprints 26 through 31, Blueprint 25 matrix v0, and Blueprint 23 point manifests v0
- coverage axes for media, replay, point manifests, event candidates, 3D candidates, review refs, provenance, regression protection, second-point distinctness, and evidence diversity
- allowed priority values that are structural planning hints only
- allowed next-action values that do not execute ingestion, sampling, or evidence generation
- explicit no-truth/no-adjudication/no-training-truth warnings

## Validation Semantics

Validation checks structure, source corpus/index/matrix paths, allowed coverage axes, allowed gap
types, allowed priority values, allowed next-action values, forbidden fields, included contract
refs, and referenced contract versions when paths are available.

Missing optional review, observation-quality, disagreement, INTENNSE, and dataset-export refs are
coverage gaps. They are not labels, errors, adjudications, or proof of dataset readiness.

Validation does not infer missing labels, create labels, judge correctness, create truth, create
training truth, resolve disagreement, execute sampling, or ingest media.

## Caveat

A structurally valid coverage sampling profile can still describe an incomplete corpus. Blueprint
32 reports incomplete evidence/review/INTENNSE provenance as planning context only.
