# Structured Review Label Schema v1

The structured review label schema is a versioned contract for human-provided review labels. It
defines neutral label families, allowed values, provenance requirements, and structural validation
rules for future review workflows.

It is not truth, training truth, 3D truth, scoring, player identity, point winner, in/out,
automatic labeling, correctness validation, or adjudication.

## Build

```bash
make tom-v1-export-review-label-schema \
  PYTHON=.venv/bin/python

make tom-v1-build-review-label-template \
  PYTHON=.venv/bin/python
```

Validate a bundle:

```bash
make tom-v1-validate-review-label-bundle \
  PYTHON=.venv/bin/python \
  REVIEW_LABEL_BUNDLE=.data/exports/review_label_template.current.json
```

Default paths:

```text
.data/contracts/review_label_schema_v1.json
.data/exports/review_label_template.current.json
.data/exports/review_label_bundle.validation.json
```

## Expected Contract

- `schema_type`: `structured_review_label_schema`
- `schema_version`: `v1`
- label families for visibility, replay readiness, observation quality, event-candidate context,
  3D trajectory context, provenance, and reviewer-note context
- neutral allowed values only
- all labels optional in v1
- all labels human-provided only
- machine-inferred labels disabled
- explicit no-truth/no-adjudication warnings

## Validation Semantics

Validation checks shape, known label keys, allowed values, forbidden fields, and human-only flags.
It does not infer missing labels, create labels, decide whether a label is true or correct, or
change existing review annotation semantics.

## Caveat

A structurally valid bundle can still contain poor or incomplete human review notes. Blueprint 27
only validates the schema contract, not review quality or tennis truth.
