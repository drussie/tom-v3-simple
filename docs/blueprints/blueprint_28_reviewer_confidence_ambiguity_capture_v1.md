# Blueprint 28 Reviewer Confidence / Ambiguity Capture v1

Status: complete

Blueprint 28 adds a versioned schema for human-provided reviewer confidence, ambiguity, and
evidence-sufficiency metadata. It defines neutral metadata keys, allowed value sets, provenance
requirements, validation rules, templates, and explicit warnings so future review workflows can
capture reviewer uncertainty without creating truth.

This milestone is a metadata contract and structural-validation layer only. It does not score
confidence automatically, judge whether confidence is appropriate, decide whether a human label is
correct, inspect video, create observations, generate event candidates, generate 3D candidates,
decide in/out, score, identify players, determine point winners, claim generalization, or
adjudicate evidence.

## Commands

Export the schema contract:

```bash
.venv/bin/python -m apps.worker.cli export-reviewer-confidence-schema \
  --output ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --skip-create-db
```

Build a blank reviewer-confidence template:

```bash
.venv/bin/python -m apps.worker.cli build-reviewer-confidence-template \
  --point-manifest-id "<point_manifest_id>" \
  --media-id "<media_id>" \
  --replay-url "<replay_url>" \
  --output ".data/exports/reviewer_confidence_ambiguity_template.current.json" \
  --skip-create-db
```

Validate a reviewer-confidence bundle:

```bash
.venv/bin/python -m apps.worker.cli validate-reviewer-confidence-bundle \
  --schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --bundle ".data/exports/reviewer_confidence_ambiguity_template.current.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --output ".data/exports/reviewer_confidence_ambiguity.validation.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-reviewer-confidence-schema PYTHON=.venv/bin/python
make tom-v1-build-reviewer-confidence-template PYTHON=.venv/bin/python
make tom-v1-validate-reviewer-confidence-bundle \
  PYTHON=.venv/bin/python \
  REVIEWER_CONFIDENCE_BUNDLE=.data/exports/reviewer_confidence_ambiguity_template.current.json
```

Post-Codex validation helper:

```bash
make tom-v1-post-codex-validate \
  PYTHON=.venv/bin/python \
  EXPECTED_BRANCH=codex/blueprint-28-reviewer-confidence-ambiguity-capture-v1
```

The helper is validation-only. It does not merge, commit, tag, push, clean files, or mutate frozen
tracked contracts. Temporary validation artifacts are written under `.data/tmp/post_codex_validate`.

## Paths

Default local paths:

```text
.data/contracts/reviewer_confidence_ambiguity_schema_v1.json
.data/exports/reviewer_confidence_ambiguity_template.current.json
.data/exports/reviewer_confidence_ambiguity.validation.json
```

Generated `.data` artifacts are local outputs and should not be committed unless intentionally
freezing a reviewed contract artifact. The v1 reviewer confidence schema contract is frozen as a
versioned contract artifact.

## Schema Contract

The schema records:

- `schema_type`: `reviewer_confidence_ambiguity_schema`
- `schema_version`: `v1`
- exported timestamp
- confidence value sets
- ambiguity level and ambiguity reason value sets
- evidence sufficiency value sets
- metadata definitions
- provenance requirements
- validation rules
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication warnings

Metadata definitions:

- `reviewer_confidence`
- `ambiguity_level`
- `ambiguity_reasons`
- `evidence_sufficiency`
- `reviewer_uncertainty_note`
- `requires_additional_review`
- `reviewer_time_spent_bucket`
- `review_context_complete`

All metadata definitions are optional in v1, human-provided only, and not machine inferred.

## Template Behavior

The template builder emits a blank reviewer confidence bundle with one placeholder confidence entry
per Blueprint 27 structured review label key. Entries default to `not_assessed`, carry
`human_provided_only: true`, and carry `machine_inferred: false`. The template does not complete a
review and does not infer confidence, ambiguity, or evidence sufficiency from evidence.

## Validation Behavior

Validation checks:

- schema type and version
- required schema sections
- confidence bundle type and version
- allowed metadata keys and values
- optional Blueprint 27 `label_key` values when a review-label schema path is supplied
- forbidden structural fields
- human-provided-only and machine-inferred flags

Validation does not infer missing confidence, create labels, judge correctness, decide whether
confidence is appropriate, or decide truth. Empty confidence-entry lists are structurally valid
because all metadata definitions are optional in v1.

## Boundaries

Blueprint 28 does not add or change:

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
- automatic confidence scoring
- automatic ambiguity scoring
- automatic truth labels

The schema supports future human review workflows, but it does not establish truth.
