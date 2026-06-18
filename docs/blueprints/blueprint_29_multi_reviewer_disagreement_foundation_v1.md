# Blueprint 29 Multi-Reviewer / Disagreement Foundation v1

Status: complete

Blueprint 29 adds a versioned multi-reviewer review-set schema and structural disagreement report.
It lets TOM represent multiple independent human reviewers, validate their referenced Blueprint 27
review-label bundles and Blueprint 28 reviewer confidence bundles, and report disagreement
structure without resolving it.

This milestone is a review-structure and reporting layer only. It does not decide which reviewer is
right, rank reviewers, score reviewer quality, resolve disagreement, infer truth, inspect video,
create observations, create event candidates, create 3D candidates, decide in/out, score, identify
players, determine point winners, claim generalization, or adjudicate evidence.

## Commands

Export the schema contract:

```bash
.venv/bin/python -m apps.worker.cli export-multi-reviewer-disagreement-schema \
  --output ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --skip-create-db
```

Build a blank multi-reviewer review-set template:

```bash
.venv/bin/python -m apps.worker.cli build-multi-reviewer-review-set-template \
  --point-manifest-id "<point_manifest_id>" \
  --media-id "<media_id>" \
  --replay-url "<replay_url>" \
  --reviewer-count 2 \
  --output ".data/exports/multi_reviewer_review_set_template.current.json" \
  --skip-create-db
```

Validate a multi-reviewer review set:

```bash
.venv/bin/python -m apps.worker.cli validate-multi-reviewer-review-set \
  --schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --review-set ".data/exports/multi_reviewer_review_set_template.current.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --output ".data/exports/multi_reviewer_review_set.validation.json" \
  --skip-create-db
```

Build a structural disagreement report:

```bash
.venv/bin/python -m apps.worker.cli build-reviewer-disagreement-report \
  --schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --review-set ".data/exports/multi_reviewer_review_set_template.current.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --output ".data/exports/reviewer_disagreement_report.current.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-multi-reviewer-disagreement-schema PYTHON=.venv/bin/python
make tom-v1-build-multi-reviewer-review-set-template PYTHON=.venv/bin/python
make tom-v1-validate-multi-reviewer-review-set \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
make tom-v1-build-reviewer-disagreement-report \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
```

## Paths

Default local paths:

```text
.data/contracts/multi_reviewer_disagreement_schema_v1.json
.data/exports/multi_reviewer_review_set_template.current.json
.data/exports/multi_reviewer_review_set.validation.json
.data/exports/reviewer_disagreement_report.current.json
```

Generated `.data/exports` artifacts are local outputs and should not be committed unless
intentionally documented. The v1 multi-reviewer disagreement schema contract is frozen as a
versioned contract artifact.

## Schema Contract

The schema records:

- `schema_type`: `multi_reviewer_disagreement_schema`
- `schema_version`: `v1`
- `review_set_type`: `multi_reviewer_review_set`
- `review_set_version`: `v1`
- reviewer identity policy
- reviewer entry definitions
- disagreement dimensions
- disagreement value sets
- provenance requirements
- validation rules
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication warnings

Reviewer identity is pseudonymous only. Allowed identity fields are:

- `reviewer_id`
- `reviewer_role`
- `reviewer_session_id`
- `reviewer_notes`

The schema does not require real names or email addresses and does not allow reviewer ranking,
reviewer reliability scoring, reviewer correctness scoring, or reviewer authority scoring.

## Validation Behavior

Validation checks:

- schema type and version
- review-set type and version
- reviewer ID presence and uniqueness
- forbidden fields
- disallowed reviewer identity fields
- human-provided-only and machine-inferred flags
- referenced Blueprint 27 review-label bundles when paths are present
- referenced Blueprint 28 confidence bundles when paths are present

Missing review-label or confidence bundle references are structural warnings in v1 so blank
templates can validate. Validation does not infer missing labels, create labels, judge correctness,
say which reviewer is right, resolve disagreement, decide truth, or score reviewers.

## Report Behavior

The disagreement report compares human-provided values across referenced bundles and reports
structural differences using neutral dimensions such as `label_value_disagreement`,
`confidence_disagreement`, `ambiguity_disagreement`, `evidence_sufficiency_disagreement`,
`missing_review_bundle`, `missing_confidence_bundle`, `reviewer_note_difference`,
`provenance_mismatch`, and `not_assessed_difference`.

Report notes use neutral terms such as `conflicting_human_inputs`, `missing_reviewer_input`, and
`needs_additional_review`. The report does not identify a correct reviewer and does not resolve the
conflict.

## Boundaries

Blueprint 29 does not add or change:

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
- automatic confidence scores
- reviewer ranking
- reviewer quality scoring
- disagreement resolution

The schema supports future multi-reviewer workflows, but it does not establish truth.
