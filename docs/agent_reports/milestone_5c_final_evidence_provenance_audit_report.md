# Milestone 5C Agent Report - Final Evidence / Provenance Audit

## Summary

Implemented the TOM v3 Simple completion/provenance audit layer. The audit checks local demo evidence structure across media, processing runs/steps, observations, typed rows, candidate tracklets, pose observations, lineage, artifacts, annotations, and review exports. It reports `passed`, `warning`, or `failed` JSON without judging model correctness.

## Files Created

- `apps/worker/services/completion_audit.py`
- `tests/test_completion_audit.py`
- `docs/PROVENANCE_AUDIT.md`
- `docs/milestones/milestone_5c_final_evidence_provenance_audit.md`
- `docs/handoffs/milestone_5c_final_evidence_provenance_audit_handoff.md`
- `docs/agent_reports/milestone_5c_final_evidence_provenance_audit_report.md`

## Files Modified

- `apps/worker/cli.py`
- `Makefile`
- `README.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/blueprints/tom_v3_blueprint_5_simple_completion_product_hardening.md`

## Audit Design Decisions

- The audit is a worker service so tests, CLI, and Makefile all use one implementation.
- `demo_only=True` scopes to media marked with `tom_v3_demo = true`.
- `--no-demo-only` audits all local rows and can be used for broader local checks.
- `--media-id` narrows the audit to one media row.
- Audit checks are structural and do not mutate evidence.

## PASS/WARN/FAIL Decisions

- Fail-severity checks make `status = failed`.
- Warning-severity checks make `status = warning` unless strict mode promotes them to command failure.
- `status = passed` requires all required and warning checks to pass.
- The JSON result includes `observation_only = true` and `no_adjudication = true`.

## Demo Completeness Decisions

The demo completeness check requires demo media, fixture detection/tracklet/pose runs, detections, tracklets, track points, pose observations, artifacts, annotations, and pose/tracklet review export artifacts.

If demo media is absent, demo-only audit fails with a clear `Run make demo first` message.

## CLI/Makefile Decisions

- Added `python -m apps.worker.cli completion-audit`.
- Added `make completion-audit`.
- `make completion-check` keeps the lightweight validation path and documents the audit command by default.
- `TOM_V3_AUDIT_REQUIRED=true make completion-check` includes the audit for callers that already created demo data.

## Tests Run

- `pytest -q` - passed, 159 tests.
- `ruff check .` - passed.
- `cd apps/web && npm run lint` - passed.
- `cd apps/web && npm run build` - passed.
- `cd apps/web && npm audit --omit=dev` - passed, 0 vulnerabilities.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head` - passed.
- `python scripts/smoke_synthetic_viewer_data.py` - passed.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5c_check.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3` - passed.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5c_check.db make completion-audit PYTHON=.venv/bin/python` - passed with `status = passed`.
- `pytest tests/test_completion_audit.py tests/test_local_demo.py -q` - passed, 12 tests.

## Validation Results

Full Python, Ruff, web lint/build/audit, Alembic smoke, synthetic viewer smoke, and demo plus provenance audit smoke all passed.

## Known Limitations

- The audit is local-database oriented and does not replace production observability.
- It checks file existence for local file-backed frame/export artifacts only.
- It does not evaluate model output quality.

## Non-Goals Preserved

- No new model/runtime capability.
- No real pose inference.
- No movement interpretation.
- No stroke classification.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 5D - Docs / Control-Room Consolidation
