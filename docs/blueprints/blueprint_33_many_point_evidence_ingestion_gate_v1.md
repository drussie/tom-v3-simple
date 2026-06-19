# Blueprint 33 Many-Point Evidence Ingestion Gate v1

Status: complete

Blueprint 33 adds a controlled many-point evidence ingestion gate contract, explicit ingestion
manifest template, structural manifest validator, dry-run plan builder, and gate report. It lets
TOM validate and plan multiple explicitly supplied local point/video paths and, only in explicit
write modes, index them as replayable evidence assets.

This milestone is an ingestion gate only. It does not discover media automatically, silently ingest
media, run tennis interpretation, create event candidates, create 3D candidates, create review
labels, create training truth, decide correctness, decide in/out, score, identify players,
determine a winner, claim generalization, or adjudicate evidence.

Demo assets such as `demo_assets/sample_point.mp4` may be used for smokes. That proves only the
gate structure and local replay-readiness path; it does not prove many real distinct tennis points
were ingested.

## Commands

Export the frozen many-point ingestion gate contract:

```bash
.venv/bin/python -m apps.worker.cli export-many-point-ingestion-gate-contract \
  --output ".data/contracts/many_point_ingestion_gate_contract_v1.json" \
  --skip-create-db
```

Build an ingestion manifest template from explicit local media paths:

```bash
.venv/bin/python -m apps.worker.cli build-many-point-ingestion-manifest-template \
  --local-media-path "demo_assets/sample_point.mp4" \
  --source-label "demo_local_point_video" \
  --output ".data/exports/many_point_ingestion_manifest.template.json" \
  --skip-create-db
```

Validate a manifest structurally:

```bash
.venv/bin/python -m apps.worker.cli validate-many-point-ingestion-manifest \
  --contract ".data/contracts/many_point_ingestion_gate_contract_v1.json" \
  --manifest ".data/exports/many_point_ingestion_manifest.template.json" \
  --output ".data/exports/many_point_ingestion_manifest.validation.json" \
  --skip-create-db
```

Build a dry-run ingestion plan:

```bash
.venv/bin/python -m apps.worker.cli build-many-point-ingestion-plan \
  --contract ".data/contracts/many_point_ingestion_gate_contract_v1.json" \
  --manifest ".data/exports/many_point_ingestion_manifest.template.json" \
  --mode dry_run \
  --output ".data/exports/many_point_ingestion_plan.current.json" \
  --skip-create-db
```

Run the ingestion gate in dry-run mode:

```bash
.venv/bin/python -m apps.worker.cli run-many-point-ingestion-gate \
  --contract ".data/contracts/many_point_ingestion_gate_contract_v1.json" \
  --manifest ".data/exports/many_point_ingestion_manifest.template.json" \
  --mode dry_run \
  --output ".data/exports/many_point_ingestion_gate.current.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-many-point-ingestion-gate-contract PYTHON=.venv/bin/python
make tom-v1-build-many-point-ingestion-manifest-template PYTHON=.venv/bin/python
make tom-v1-validate-many-point-ingestion-manifest \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
make tom-v1-build-many-point-ingestion-plan \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
make tom-v1-run-many-point-ingestion-gate \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
```

## Paths

Default local paths:

```text
.data/contracts/many_point_ingestion_gate_contract_v1.json
.data/exports/many_point_ingestion_manifest.template.json
.data/exports/many_point_ingestion_manifest.validation.json
.data/exports/many_point_ingestion_plan.current.json
.data/exports/many_point_ingestion_gate.current.json
```

The contract under `.data/contracts` is committed as the frozen v1 ingestion gate contract.
Generated `.data/exports` ingestion manifests, validations, plans, and reports are local outputs
and should not be committed unless intentionally documented.

## Contract Shape

The contract records:

- `contract_type`: `many_point_ingestion_gate_contract`
- `contract_version`: `v1`
- `manifest_type`: `many_point_ingestion_manifest`
- `manifest_version`: `v1`
- `ingestion_gate_type`: `many_point_ingestion_gate_report`
- `ingestion_gate_version`: `v1`
- ingestion scope
- source contract refs
- ingestion manifest schema
- ingestion entry fields
- requested action values
- disallowed requested action values
- execution modes
- output contracts
- provenance requirements
- validation rules
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication/no-generalization warnings

Referenced contract versions:

- `observation_quality_taxonomy_version`: `v1`
- `review_label_schema_version`: `v1`
- `reviewer_confidence_schema_version`: `v1`
- `multi_reviewer_disagreement_schema_version`: `v1`
- `intennse_label_alignment_contract_version`: `v1`
- `versioned_dataset_corpus_contract_version`: `v1`
- `coverage_sampling_strategy_contract_version`: `v1`
- `multi_point_regression_matrix_version`: `v0`
- `point_manifest_version`: `v0`

## Manifest Behavior

The manifest supports explicit entries with local media paths, source labels, optional external
reference IDs, optional intended point IDs, collection notes, expected media type, duplicate-media
policy, requested actions, and warnings.

Allowed requested actions are:

- `validate_path`
- `index_media`
- `build_replay_url`
- `build_point_manifest`
- `include_in_multi_point_index`
- `include_in_dataset_corpus_manifest`

Disallowed requested actions such as event generation, marker arbitration, 3D generation, review
label creation, truth creation, scoring, and player identification are rejected structurally.

## Gate Behavior

`dry_run` and `validate_only` validate local paths, compute checksums when files exist, detect
duplicates by path/checksum, and emit replay-intent records without persisting new media.

`index_only` and `index_and_manifest` are explicit write modes. They use the existing safe media
indexing behavior. `index_and_manifest` can also build point manifests and refresh downstream
index/corpus outputs when requested and when required source artifacts exist.

No mode runs event generation, marker arbitration, 3D generation, review-label creation, scoring,
truth creation, or adjudication.

## Boundaries

Blueprint 33 does not add or change:

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
- automatic media discovery outside explicit user input
- automatic corpus sampling execution
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
