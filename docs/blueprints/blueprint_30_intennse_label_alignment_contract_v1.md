# Blueprint 30 INTENNSE Label Alignment Contract v1

Status: complete

Blueprint 30 adds a versioned INTENNSE label alignment contract. It defines how future INTENNSE
expert interpretation label references can align with TOM observation evidence, structured review
labels, reviewer confidence/ambiguity metadata, multi-reviewer disagreement structure, replay
context, and dataset exports.

This milestone is a contract and provenance foundation only. It does not import INTENNSE labels,
create TOM labels, infer expert interpretation, judge correctness, resolve disagreement, create
truth, decide in/out, score, identify players, determine point winners, produce coaching or
tactical conclusions, claim generalization, or adjudicate evidence.

## Commands

Export the alignment contract:

```bash
.venv/bin/python -m apps.worker.cli export-intennse-label-alignment-contract \
  --output ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --skip-create-db
```

Build a blank alignment bundle template:

```bash
.venv/bin/python -m apps.worker.cli build-intennse-alignment-template \
  --point-manifest-id "<point_manifest_id>" \
  --media-id "<media_id>" \
  --replay-url "<replay_url>" \
  --intennse-label-bundle-ref "<external_intennse_ref>" \
  --intennse-schema-version "<external_schema_version>" \
  --output ".data/exports/intennse_alignment_template.current.json" \
  --skip-create-db
```

Validate an alignment bundle:

```bash
.venv/bin/python -m apps.worker.cli validate-intennse-alignment-bundle \
  --contract ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --bundle ".data/exports/intennse_alignment_template.current.json" \
  --observation-quality-taxonomy ".data/contracts/observation_quality_taxonomy_v1.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --multi-reviewer-schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --output ".data/exports/intennse_alignment_bundle.validation.json" \
  --skip-create-db
```

Build a structural alignment report:

```bash
.venv/bin/python -m apps.worker.cli build-intennse-alignment-report \
  --contract ".data/contracts/intennse_label_alignment_contract_v1.json" \
  --bundle ".data/exports/intennse_alignment_template.current.json" \
  --observation-quality-taxonomy ".data/contracts/observation_quality_taxonomy_v1.json" \
  --review-label-schema ".data/contracts/review_label_schema_v1.json" \
  --reviewer-confidence-schema ".data/contracts/reviewer_confidence_ambiguity_schema_v1.json" \
  --multi-reviewer-schema ".data/contracts/multi_reviewer_disagreement_schema_v1.json" \
  --output ".data/exports/intennse_alignment_report.current.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-intennse-label-alignment-contract PYTHON=.venv/bin/python
make tom-v1-build-intennse-alignment-template PYTHON=.venv/bin/python
make tom-v1-validate-intennse-alignment-bundle \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
make tom-v1-build-intennse-alignment-report \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
```

## Paths

Default local paths:

```text
.data/contracts/intennse_label_alignment_contract_v1.json
.data/exports/intennse_alignment_template.current.json
.data/exports/intennse_alignment_bundle.validation.json
.data/exports/intennse_alignment_report.current.json
```

The contract under `.data/contracts` is committed as the frozen v1 contract. Generated
`.data/exports` artifacts are local outputs and should not be committed unless intentionally
documented.

## Contract Shape

The contract records:

- `contract_type`: `intennse_label_alignment_contract`
- `contract_version`: `v1`
- `tom_schema_refs` for Blueprint 26, 27, 28, and 29 contracts
- INTENNSE alignment scope
- alignment entities
- alignment fields
- alignment value sets
- provenance requirements
- validation rules
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication warnings

Supported alignment entities are:

- `point_manifest_alignment`
- `replay_context_alignment`
- `observation_quality_alignment`
- `review_label_alignment`
- `reviewer_confidence_alignment`
- `multi_reviewer_disagreement_alignment`
- `expert_interpretation_placeholder`
- `dataset_export_alignment`

Supported alignment statuses include `not_assessed`, `aligned_by_reference`,
`partially_aligned`, `not_aligned`, `missing_tom_context`, `missing_intennse_context`,
`requires_human_alignment_review`, and `not_applicable`.

## Validation Behavior

Validation checks:

- contract type and version
- alignment bundle type and version
- TOM schema reference versions
- referenced TOM contract versions when paths are available
- allowed alignment entities
- allowed alignment and provenance status values
- forbidden fields
- human-provided-only and machine-inferred flags

INTENNSE references are treated as external placeholders in v1. Validation reports structural
errors and provenance warnings only. It does not infer missing TOM labels, create INTENNSE labels,
judge expert interpretation, resolve disagreement, create truth, or adjudicate evidence.

## Report Behavior

The alignment report summarizes reference presence and provenance issues with neutral terms such
as `alignment_reference_present`, `missing_intennse_reference`, `missing_tom_reference`,
`requires_human_alignment_review`, and `provenance_partial`.

Missing TOM context and missing INTENNSE context are provenance issues only. The report does not
decide whether an external interpretation is correct, does not import labels, and does not resolve
reviewer disagreement.

## Boundaries

Blueprint 30 does not add or change:

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

The contract supports future TOM/INTENNSE bridge work, but it does not establish truth.
