# Blueprint 32 Coverage-Driven Sampling Strategy v1 Report

Status: implemented

Branch: `codex/blueprint-32-coverage-driven-sampling-strategy-v1`

## Summary

Blueprint 32 adds a versioned coverage-driven sampling strategy contract, coverage profile builder,
structural profile validator, and structural coverage report builder. The coverage layer reads the
existing Blueprint 31 dataset corpus manifest and preserves point manifest identity, media identity,
replay URLs, run IDs, evidence availability, profile counts, source warnings, and provenance-only
labels while describing coverage gaps for future controlled evidence expansion.

The implementation does not ingest media, execute sampling, generate observations, create event
candidates, create 3D candidates, create training truth, create automatic labels, score
correctness, infer expert interpretation, resolve disagreement, rank reviewers, decide in/out,
score, point winner, player identity, rally state, server/receiver state, coaching/tactical
conclusions, match outcomes, betting or prediction, generalization claims, or adjudication.

## Created

- `apps/worker/services/coverage_driven_sampling_strategy.py`
- `tests/test_coverage_driven_sampling_strategy.py`
- `docs/blueprints/blueprint_32_coverage_driven_sampling_strategy_v1.md`
- `docs/reviews/coverage_driven_sampling_strategy_v1.md`
- `docs/agent_reports/blueprint_32_coverage_driven_sampling_strategy_v1_report.md`
- `.data/contracts/coverage_sampling_strategy_contract_v1.json`

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
python -m apps.worker.cli export-coverage-sampling-strategy-contract
python -m apps.worker.cli build-coverage-sampling-profile
python -m apps.worker.cli validate-coverage-sampling-profile
python -m apps.worker.cli build-coverage-sampling-report
```

Added Make targets:

```text
make tom-v1-export-coverage-sampling-strategy-contract
make tom-v1-build-coverage-sampling-profile
make tom-v1-validate-coverage-sampling-profile
make tom-v1-build-coverage-sampling-report
```

Default local paths:

```text
.data/contracts/coverage_sampling_strategy_contract_v1.json
.data/exports/coverage_sampling_profile.current.json
.data/exports/coverage_sampling_profile.validation.json
.data/exports/coverage_sampling_report.current.json
```

## Validation Semantics

The validator checks contract shape, profile type/version, included contract refs, referenced
contract versions when paths are available, source path existence, required candidate fields,
allowed coverage axes, allowed gap types, allowed priority values, allowed next-action values, and
forbidden fields. Missing optional review, observation-quality, INTENNSE, disagreement, and export
refs are reported as coverage gaps.

Validation and reports are structural only. They do not infer missing labels, create labels, judge
correctness, create truth, create training truth, resolve disagreement, execute sampling, ingest
media, or adjudicate evidence.

## Boundary

The contract/profile/validator/report are planning and provenance structure only. They do not
generate evidence, mutate review metadata, change replay semantics, change protected baselines,
decide in/out, score, identify players, determine a winner, claim generalization, score reviewers,
resolve disagreement, produce INTENNSE coaching/tactical/match-outcome conclusions, execute
sampling, ingest media, or adjudicate evidence.

## Validation

Focused Blueprint 32 checks:

```text
.venv/bin/python -m pytest -q tests/test_coverage_driven_sampling_strategy.py
6 passed

ruff check apps/worker/services/coverage_driven_sampling_strategy.py tests/test_coverage_driven_sampling_strategy.py apps/worker/cli.py
passed
```

Full validation was run before the Blueprint 32 commit/tag. See the final handoff for the exact
test counts, protected gate outputs, post-Codex validator result, and generated-artifact status.
