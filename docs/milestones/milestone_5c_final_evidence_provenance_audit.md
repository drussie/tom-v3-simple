# Milestone 5C - Final Evidence / Provenance Audit

Status: complete

## Goal

Add a final structural audit layer for TOM v3 Simple local demo evidence.

The audit answers whether persisted demo evidence is internally coherent across media, runs, steps, observations, typed rows, lineage, artifacts, annotations, and exports.

It does not judge model correctness or tennis meaning.

## Implemented

- Completion audit service in `apps/worker/services/completion_audit.py`.
- Worker CLI command:

```bash
python -m apps.worker.cli completion-audit --demo-only
```

- Makefile target:

```bash
make completion-audit
```

- PASS/WARN/FAIL-style JSON with summary counts, checks, warnings, failures, and observation-only flags.
- Demo completeness check for the canonical fixture demo path.
- Tests for passing demo audit, empty demo state, empty all-data mode, broken observation refs, broken typed-row refs, broken lineage refs, broken artifact targets, broken annotation targets, and CLI handler output.
- Provenance audit docs in `docs/PROVENANCE_AUDIT.md`.

## Result

After `make demo`, `make completion-audit` verifies the fixture demo state and returns `status = passed` when the evidence loop is structurally complete.

The audit catches missing or broken references without creating new observations or mutating existing evidence.

## Non-Goals Preserved

- No new model/runtime capability.
- No real pose inference.
- No movement interpretation.
- No stroke classification.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.
