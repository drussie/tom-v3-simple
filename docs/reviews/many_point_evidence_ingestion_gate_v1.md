# Many-Point Evidence Ingestion Gate v1

The many-point evidence ingestion gate contract defines how TOM validates and plans explicitly
provided local point/video paths before any optional indexing. It is a replay/evidence
provenance gate, not tennis interpretation.

It is not truth, training truth, scoring, player identity, point winner, in/out, automatic
labeling, correctness validation, reviewer scoring, disagreement resolution, INTENNSE conclusion,
coaching output, tactical output, match-outcome output, automatic media discovery, or adjudication.

## Build

```bash
make tom-v1-export-many-point-ingestion-gate-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-many-point-ingestion-manifest-template \
  PYTHON=.venv/bin/python
```

Validate an ingestion manifest:

```bash
make tom-v1-validate-many-point-ingestion-manifest \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
```

Build a dry-run plan and run the dry-run gate:

```bash
make tom-v1-build-many-point-ingestion-plan \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json

make tom-v1-run-many-point-ingestion-gate \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
```

Default paths:

```text
.data/contracts/many_point_ingestion_gate_contract_v1.json
.data/exports/many_point_ingestion_manifest.template.json
.data/exports/many_point_ingestion_manifest.validation.json
.data/exports/many_point_ingestion_plan.current.json
.data/exports/many_point_ingestion_gate.current.json
```

## Expected Contract

- `contract_type`: `many_point_ingestion_gate_contract`
- `contract_version`: `v1`
- `manifest_type`: `many_point_ingestion_manifest`
- `manifest_version`: `v1`
- `ingestion_gate_type`: `many_point_ingestion_gate_report`
- `ingestion_gate_version`: `v1`
- contract refs for Blueprints 26 through 32, Blueprint 25 matrix v0, and Blueprint 23 point manifests v0
- execution modes `dry_run`, `validate_only`, `index_only`, and `index_and_manifest`
- default execution mode `dry_run`
- allowed requested actions that do not include event generation, 3D generation, review-label creation, scoring, player identification, or truth creation
- explicit no-truth/no-adjudication/no-generalization warnings

## Validation Semantics

Validation checks manifest type/version, source contract refs, local media path presence,
file existence, checksums where available, duplicate path/checksum conflicts, requested actions,
expected media type, and forbidden fields.

Dry-run planning and dry-run gate reports do not persist media, point manifests, replay indexes,
corpus manifests, observations, candidates, or labels.

## Caveat

Using `demo_assets/sample_point.mp4` in the smoke path validates the gate mechanics only. It does
not prove that TOM has ingested many real distinct tennis points or generalized beyond protected
sample evidence.
