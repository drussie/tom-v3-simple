# Reviewer Confidence / Ambiguity Capture v1

The reviewer confidence and ambiguity schema is a versioned contract for human-provided review
metadata. It defines neutral values for confidence, ambiguity, ambiguity reasons, evidence
sufficiency, uncertainty notes, additional-review requests, review duration buckets, and review
context completeness.

It is not truth, training truth, 3D truth, scoring, player identity, point winner, in/out,
automatic confidence scoring, automatic ambiguity scoring, correctness validation, or adjudication.

## Build

```bash
make tom-v1-export-reviewer-confidence-schema \
  PYTHON=.venv/bin/python

make tom-v1-build-reviewer-confidence-template \
  PYTHON=.venv/bin/python
```

Validate a bundle:

```bash
make tom-v1-validate-reviewer-confidence-bundle \
  PYTHON=.venv/bin/python \
  REVIEWER_CONFIDENCE_BUNDLE=.data/exports/reviewer_confidence_ambiguity_template.current.json
```

Default paths:

```text
.data/contracts/reviewer_confidence_ambiguity_schema_v1.json
.data/exports/reviewer_confidence_ambiguity_template.current.json
.data/exports/reviewer_confidence_ambiguity.validation.json
```

## Expected Contract

- `schema_type`: `reviewer_confidence_ambiguity_schema`
- `schema_version`: `v1`
- neutral reviewer confidence, ambiguity, ambiguity reason, and evidence-sufficiency value sets
- metadata definitions are optional in v1
- metadata is human-provided only
- machine-inferred confidence and ambiguity are disabled
- explicit no-truth/no-adjudication warnings

## Validation Semantics

Validation checks shape, allowed metadata values, forbidden fields, optional Blueprint 27 label keys,
and human-only flags. It does not infer missing confidence, create labels, decide whether confidence
is appropriate, decide whether a human label is true or correct, or change existing review
annotation semantics.

## Caveat

A structurally valid bundle can still contain poor, incomplete, or inconsistent human review
metadata. Blueprint 28 validates the schema contract only, not review quality or tennis truth.
