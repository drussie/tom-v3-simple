# Point Evidence Snapshot v0 Report

## Summary

Implemented Point Evidence Snapshot v0 for compact point/run reporting. The new worker command
reads an existing event candidate run and returns a durable snapshot with replay URL, source run
ids, observation counts, active versions, final marker summary, warnings, and known limitations.

## Commands

- `python -m apps.worker.cli build-point-evidence-snapshot`
- `make tom-v1-point-evidence-snapshot`

Supported output:

- JSON by default
- Markdown report body with `--format markdown`
- optional file write with `--output`

## Boundary

The snapshot is report-only. It does not change hit/bounce generation, marker-level arbitration,
replay marker behavior, persisted source observations, truth status, score, in/out,
accepted/rejected lifecycle, or adjudication.

## Validation

- `.venv/bin/python -m pytest -q`: passed, 328 tests.
- `ruff check .`: passed.
- `git diff --check`: passed.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities.
- Fixture demo passed with `tmp_tom_v3_point_evidence_snapshot_fixture.db`.
- Fixture completion audit passed with `tmp_tom_v3_point_evidence_snapshot_fixture.db`.

## Local Smoke

Ran `make tom-v1-point-evidence-snapshot` against the existing bridge DB with:

- media: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- event candidate run: `06d51d3e-dde5-45cc-821a-ba2260f3ddcb`

Snapshot output reported:

- `snapshot_type`: `point_evidence_snapshot`
- `snapshot_version`: `v0`
- final visible marker count: 6
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- `total`: 877

The active versions included physics heuristic `v0.3.1`, marker-level arbitration `v0.3.1`,
and universal hit validity guard `v0.3.0`. Markdown export also succeeded at
`.data/exports/point_evidence_snapshot_smoke.md`.
