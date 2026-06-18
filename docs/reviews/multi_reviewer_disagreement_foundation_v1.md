# Multi-Reviewer / Disagreement Foundation v1

The multi-reviewer disagreement schema is a versioned contract for comparing multiple
human-provided review bundles and reviewer confidence bundles. It defines pseudonymous reviewer
entries, review-set validation, structural disagreement dimensions, and a neutral disagreement
report shape.

It is not truth, training truth, 3D truth, scoring, player identity, point winner, in/out,
automatic labeling, reviewer ranking, reviewer quality scoring, correctness validation,
disagreement resolution, or adjudication.

## Build

```bash
make tom-v1-export-multi-reviewer-disagreement-schema \
  PYTHON=.venv/bin/python

make tom-v1-build-multi-reviewer-review-set-template \
  PYTHON=.venv/bin/python
```

Validate a review set:

```bash
make tom-v1-validate-multi-reviewer-review-set \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
```

Build a disagreement report:

```bash
make tom-v1-build-reviewer-disagreement-report \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
```

Default paths:

```text
.data/contracts/multi_reviewer_disagreement_schema_v1.json
.data/exports/multi_reviewer_review_set_template.current.json
.data/exports/multi_reviewer_review_set.validation.json
.data/exports/reviewer_disagreement_report.current.json
```

## Expected Contract

- `schema_type`: `multi_reviewer_disagreement_schema`
- `schema_version`: `v1`
- `review_set_type`: `multi_reviewer_review_set`
- `review_set_version`: `v1`
- pseudonymous reviewer identifiers only
- reviewer IDs required and unique within a review set
- referenced Blueprint 27 and Blueprint 28 bundles validated when paths are present
- missing bundle references are structural warnings
- explicit no-truth/no-adjudication/no-resolution warnings

## Validation Semantics

Validation checks structure, reviewer IDs, forbidden fields, disallowed reviewer identity fields,
human-only flags, and referenced bundle structure. It does not infer missing labels, create labels,
decide whether a reviewer is right, resolve disagreement, decide whether a label is true, or score
reviewers.

## Caveat

A structurally valid disagreement report can still reflect incomplete, conflicting, or poor human
review inputs. Blueprint 29 reports the structure of those inputs only.
