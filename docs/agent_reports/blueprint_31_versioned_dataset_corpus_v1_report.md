# Blueprint 31 Versioned Dataset Corpus v1 Report

Status: implemented

Branch: `codex/blueprint-31-versioned-dataset-corpus-v1`

## Summary

Blueprint 31 adds a versioned dataset corpus contract, corpus manifest builder, structural corpus
manifest validator, and structural corpus report builder. The corpus layer packages existing TOM
point manifests, multi-point replay index rows, multi-point regression matrix rows, Blueprint 26
through 30 contract references, and future review/INTENNSE/export references into durable corpus
entries.

The implementation does not create training truth, automatic labels, correctness claims, in/out,
score, point winner, player identity, rally state, server/receiver state, event generation, 3D
generation, reviewer ranking, reviewer scoring, disagreement resolution, INTENNSE conclusions,
coaching/tactical conclusions, betting or prediction, generalization claims, or adjudication.

## Created

- `apps/worker/services/versioned_dataset_corpus.py`
- `tests/test_versioned_dataset_corpus.py`
- `docs/blueprints/blueprint_31_versioned_dataset_corpus_v1.md`
- `docs/reviews/versioned_dataset_corpus_v1.md`
- `docs/agent_reports/blueprint_31_versioned_dataset_corpus_v1_report.md`
- `.data/contracts/versioned_dataset_corpus_contract_v1.json`

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
python -m apps.worker.cli export-versioned-dataset-corpus-contract
python -m apps.worker.cli build-versioned-dataset-corpus-manifest
python -m apps.worker.cli validate-versioned-dataset-corpus-manifest
python -m apps.worker.cli build-versioned-dataset-corpus-report
```

Added Make targets:

```text
make tom-v1-export-versioned-dataset-corpus-contract
make tom-v1-build-versioned-dataset-corpus-manifest
make tom-v1-validate-versioned-dataset-corpus-manifest
make tom-v1-build-versioned-dataset-corpus-report
```

Default local paths:

```text
.data/contracts/versioned_dataset_corpus_contract_v1.json
.data/exports/versioned_dataset_corpus_manifest.current.json
.data/exports/versioned_dataset_corpus_manifest.validation.json
.data/exports/versioned_dataset_corpus_report.current.json
```

## Validation Semantics

The validator checks contract shape, manifest type/version, included contract refs, referenced
contract versions when paths are available, source index/matrix path existence, required corpus
entry fields, allowed split/status values, and forbidden fields. Missing optional review,
observation-quality, INTENNSE, disagreement, and dataset-export refs are reported as provenance
gaps.

Validation and reports are structural only. They do not infer missing labels, create labels, judge
correctness, create truth, create training truth, resolve disagreement, or adjudicate evidence.

## Boundary

The contract/manifest/validator/report are provenance and dataset-corpus structure only. They do
not generate evidence, mutate review metadata, change replay semantics, change protected
baselines, decide in/out, score, identify players, determine a winner, claim generalization, score
reviewers, resolve disagreement, produce INTENNSE coaching/tactical/match-outcome conclusions, or
adjudicate evidence.

## Validation

Focused Blueprint 31 checks:

```text
.venv/bin/python -m pytest -q tests/test_versioned_dataset_corpus.py
5 passed

ruff check apps/worker/services/versioned_dataset_corpus.py tests/test_versioned_dataset_corpus.py apps/worker/cli.py
passed
```

Full validation was run before the Blueprint 31 commit/tag. See the final handoff for the exact
test counts, protected gate outputs, post-Codex validator result, and generated-artifact status.
