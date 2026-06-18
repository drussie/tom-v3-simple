# INTENNSE Label Alignment Contract v1

The INTENNSE label alignment contract is a versioned bridge contract for future alignment between
TOM evidence/review/provenance structures and external INTENNSE expert interpretation label
references.

It is not truth, training truth, scoring, player identity, point winner, in/out, automatic
labeling, correctness validation, disagreement resolution, coaching output, tactical output,
match-outcome output, or adjudication.

## Build

```bash
make tom-v1-export-intennse-label-alignment-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-intennse-alignment-template \
  PYTHON=.venv/bin/python
```

Validate an alignment bundle:

```bash
make tom-v1-validate-intennse-alignment-bundle \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
```

Build an alignment report:

```bash
make tom-v1-build-intennse-alignment-report \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
```

Default paths:

```text
.data/contracts/intennse_label_alignment_contract_v1.json
.data/exports/intennse_alignment_template.current.json
.data/exports/intennse_alignment_bundle.validation.json
.data/exports/intennse_alignment_report.current.json
```

## Expected Contract

- `contract_type`: `intennse_label_alignment_contract`
- `contract_version`: `v1`
- `alignment_bundle_type`: `intennse_label_alignment_bundle`
- `alignment_bundle_version`: `v1`
- TOM schema refs for Blueprint 26 through Blueprint 29
- alignment entities for point manifest, replay context, observation quality, review labels,
  reviewer confidence, multi-reviewer disagreement, expert interpretation placeholders, and
  dataset export alignment
- explicit no-truth/no-adjudication/no-import warnings

## Validation Semantics

Validation checks structure, allowed entities, allowed values, forbidden fields, human-only flags,
and referenced TOM contract versions when paths are available. It treats INTENNSE references as
external placeholders unless a future local fixture is explicitly supplied.

Validation does not infer missing TOM labels, create INTENNSE labels, judge expert interpretation,
resolve disagreement, validate correctness, or create truth.

## Caveat

A structurally valid alignment bundle can still be incomplete. Blueprint 30 reports missing TOM
or INTENNSE references as provenance issues only.
