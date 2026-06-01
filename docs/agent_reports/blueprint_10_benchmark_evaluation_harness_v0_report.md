# Blueprint 10 Benchmark / Evaluation Harness v0 Report

## Summary

Blueprint 10 adds a read-only point candidate evaluation harness. It summarizes final hit/bounce
candidate markers and Blueprint 9 review annotation metadata without changing generated evidence.

## Added

- `evaluate-point-candidates` worker CLI command
- `tom-v1-evaluate-point-candidates` Make helper
- JSON output by default
- optional markdown output through `--format markdown`
- optional output file writing through `--output`
- service tests covering reviewed markers, missing-candidate notes, zero-marker runs, markdown
  output, and prohibited metric terminology

## Boundary

The harness reports candidate evidence and operator review metadata only. It does not create hit
truth, bounce truth, in/out, score, point state, player identity, accepted/rejected lifecycle,
automatic correction, or adjudication.

## Validation Notes

Local bridge smoke:

- media: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- event candidate run: `1b946366-7ec1-426f-8b40-494535a9b3fb`
- final marker count: 6
- reviewed final markers: 1
- unreviewed final markers: 5
- reviewed-only wrong fraction: 1.0
- rejection diagnostics: 871

Validation:

- `tests/test_point_candidate_evaluation.py`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `git diff --check`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- fixture `make demo`
- fixture `make completion-audit`
