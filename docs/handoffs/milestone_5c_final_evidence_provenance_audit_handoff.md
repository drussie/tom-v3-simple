# TOM v3 Simple - Milestone 5C Handoff

## Final Evidence / Provenance Audit

Repo: `drussie/tom-v3-simple`

Branch: `codex/m5c-final-evidence-provenance-audit`

Starting state: Milestone 5B Viewer / Product Polish accepted and merged to main.

## Mission

Milestone 5C adds a final structural evidence/provenance audit for the completed local fixture demo path.

The target path is:

```text
local fixture demo state
-> completion audit
-> PASS / WARN / FAIL result
-> counts and diagnostics
-> provenance, lineage, target, and export integrity checks
```

## Implemented

- `run_completion_audit(session, media_id=None, demo_only=True, strict=False)`.
- Worker CLI `completion-audit`.
- Makefile `completion-audit`.
- Optional `TOM_V3_AUDIT_REQUIRED=true make completion-check` integration.
- Demo-only and all-data audit scopes.
- Strict mode for warning-as-failure behavior.
- Focused regression tests.
- `docs/PROVENANCE_AUDIT.md`.

## Validation Commands

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5c_check.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5c_check.db make completion-audit PYTHON=.venv/bin/python
pytest tests/test_completion_audit.py tests/test_local_demo.py -q
```

## Next Handoff

Recommended next milestone:

Milestone 5D - Docs / Control-Room Consolidation

## Boundaries

This milestone audits evidence structure only.

No real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, or adjudication was added.
