# Blueprint 27 Structured Review Label Schema v1

Status: complete

Blueprint 27 adds a versioned schema for human-provided review labels. It defines neutral label
families, label definitions, value sets, provenance requirements, validation rules, and explicit
warnings so future review workflows can collect structured labels without creating truth.

This milestone is a schema and structural-validation layer only. It does not label automatically,
judge whether a label is correct, inspect video, create observations, generate event candidates,
generate 3D candidates, decide in/out, score, identify players, determine point winners, claim
generalization, or adjudicate evidence.

## Commands

Export the schema contract:

```bash
.venv/bin/python -m apps.worker.cli export-review-label-schema \
  --output ".data/contracts/review_label_schema_v1.json" \
  --skip-create-db
```

Build a blank review-label template:

```bash
.venv/bin/python -m apps.worker.cli build-review-label-template \
  --point-manifest-id "<point_manifest_id>" \
  --media-id "<media_id>" \
  --replay-url "<replay_url>" \
  --output ".data/exports/review_label_template.current.json" \
  --skip-create-db
```

Validate a review-label bundle:

```bash
.venv/bin/python -m apps.worker.cli validate-review-label-bundle \
  --schema ".data/contracts/review_label_schema_v1.json" \
  --bundle ".data/exports/review_label_template.current.json" \
  --output ".data/exports/review_label_bundle.validation.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-review-label-schema PYTHON=.venv/bin/python
make tom-v1-build-review-label-template PYTHON=.venv/bin/python
make tom-v1-validate-review-label-bundle \
  PYTHON=.venv/bin/python \
  REVIEW_LABEL_BUNDLE=.data/exports/review_label_template.current.json
```

## Paths

Default local paths:

```text
.data/contracts/review_label_schema_v1.json
.data/exports/review_label_template.current.json
.data/exports/review_label_bundle.validation.json
```

Generated `.data` artifacts are local outputs and should not be committed unless intentionally
freezing a reviewed contract artifact.

## Schema Contract

The schema records:

- `schema_type`: `structured_review_label_schema`
- `schema_version`: `v1`
- exported timestamp
- `label_families`
- `label_definitions`
- `value_sets`
- `provenance_requirements`
- `validation_rules`
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication warnings

Label families:

- `evidence_visibility_review`
- `replay_review_readiness`
- `observation_quality_review`
- `event_candidate_review_context`
- `trajectory_3d_review_context`
- `provenance_review`
- `reviewer_note_context`

Allowed values are neutral review labels such as `not_assessed`, `unknown`, `unavailable`,
`visible`, `partially_visible`, `obscured`, `ambiguous`, `needs_human_review`,
`sufficient_for_review`, `insufficient_for_review`, `evidence_present`, `evidence_missing`,
`provenance_present`, `provenance_missing`, `reviewer_note_present`, `reviewer_note_missing`, and
`not_applicable`.

Forbidden labels and fields include in/out, score, winner, player identity, server/receiver,
accepted/rejected lifecycle, correctness labels, and adjudication fields.

## Template Behavior

The template builder emits a blank structured review bundle. Entries default to `not_assessed`,
carry `human_provided_only: true`, and carry `machine_inferred: false`. The template does not
complete a review and does not infer labels from evidence.

## Validation Behavior

Validation checks:

- schema type and version
- required schema sections
- label bundle type and version
- known label keys
- allowed label values
- forbidden structural fields
- human-provided-only and machine-inferred flags

Validation does not infer missing labels, create labels, judge correctness, or decide truth. Empty
label-entry lists are structurally valid because all label definitions are optional in v1.

## Boundaries

Blueprint 27 does not add or change:

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
- adjudication
- betting or prediction
- generalization claims
- automatic correctness claims
- automatic review labels
- automatic truth labels

The schema supports future human review workflows, but it does not establish truth.
