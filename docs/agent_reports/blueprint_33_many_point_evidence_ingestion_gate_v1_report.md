# Blueprint 33 Many-Point Evidence Ingestion Gate v1 Report

Status: implemented

Branch: `codex/blueprint-33-many-point-evidence-ingestion-gate-v1`

## Summary

Blueprint 33 adds a many-point evidence ingestion gate contract, manifest template builder,
structural manifest validator, dry-run plan builder, and gate runner. The gate validates explicit
local media paths, checks file existence, computes checksums where available, detects duplicate
paths/checksums, and reports what would happen before any optional indexing.

The implementation does not discover media automatically, silently ingest media, generate
observations, create event candidates, create 3D candidates, create review labels, create training
truth, score correctness, infer expert interpretation, resolve disagreement, rank reviewers,
decide in/out, score, point winner, player identity, rally state, server/receiver state,
coaching/tactical conclusions, match outcomes, betting or prediction, generalization claims, or
adjudication.

## Created

- `apps/worker/services/many_point_ingestion_gate.py`
- `tests/test_many_point_ingestion_gate.py`
- `docs/blueprints/blueprint_33_many_point_evidence_ingestion_gate_v1.md`
- `docs/reviews/many_point_evidence_ingestion_gate_v1.md`
- `docs/agent_reports/blueprint_33_many_point_evidence_ingestion_gate_v1_report.md`
- `.data/contracts/many_point_ingestion_gate_contract_v1.json`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `scripts/post_codex_validate.sh`
- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/BLUEPRINT_STATUS.md`

## CLI / Make Helpers

Added CLI commands:

```text
python -m apps.worker.cli export-many-point-ingestion-gate-contract
python -m apps.worker.cli build-many-point-ingestion-manifest-template
python -m apps.worker.cli validate-many-point-ingestion-manifest
python -m apps.worker.cli build-many-point-ingestion-plan
python -m apps.worker.cli run-many-point-ingestion-gate
```

Added Make targets:

```text
make tom-v1-export-many-point-ingestion-gate-contract
make tom-v1-build-many-point-ingestion-manifest-template
make tom-v1-validate-many-point-ingestion-manifest
make tom-v1-build-many-point-ingestion-plan
make tom-v1-run-many-point-ingestion-gate
```

Default local paths:

```text
.data/contracts/many_point_ingestion_gate_contract_v1.json
.data/exports/many_point_ingestion_manifest.template.json
.data/exports/many_point_ingestion_manifest.validation.json
.data/exports/many_point_ingestion_plan.current.json
.data/exports/many_point_ingestion_gate.current.json
```

## Validation Semantics

The validator checks contract shape, manifest type/version, included contract refs, required
entry fields, local path existence, allowed requested actions, duplicate media policy, expected
media type, and forbidden fields. Duplicate path/checksum conflicts are rejected unless explicitly
allowed per entry.

Dry-run planning and dry-run gate reports are structural only. They do not index media, build
point manifests, refresh replay indexes, refresh corpus manifests, create labels, create truth,
run event generation, run 3D generation, or adjudicate evidence.

## Boundary

The contract/template/validator/plan/gate are controlled ingestion infrastructure only. They do
not mutate protected baselines, change replay semantics, generate evidence, decide in/out, score,
identify players, determine a winner, claim generalization, score reviewers, resolve
disagreement, produce INTENNSE coaching/tactical/match-outcome conclusions, create training truth,
or adjudicate evidence.

## Validation

Focused Blueprint 33 checks:

```text
.venv/bin/python -m pytest -q tests/test_many_point_ingestion_gate.py
6 passed

ruff check apps/worker/services/many_point_ingestion_gate.py tests/test_many_point_ingestion_gate.py apps/worker/cli.py
passed
```

Full validation was run before the Blueprint 33 commit/tag. See the final handoff for the exact
test counts, protected gate outputs, post-Codex validator result, and generated-artifact status.
