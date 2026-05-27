# TOM v3 Simple - Milestone 5D Handoff

## Docs / Control-Room Consolidation

Repo: `drussie/tom-v3-simple`

Branch: `codex/m5d-docs-control-room-consolidation`

Starting state: Milestone 5C Final Evidence / Provenance Audit accepted and merged to main.

## Mission

Milestone 5D consolidates repo memory into canonical current-state docs:

```text
README
-> RUNBOOK_LOCAL
-> CONTROL_ROOM
-> ARCHITECTURE
-> OBSERVATION_CONTRACT
-> BLUEPRINT_STATUS
-> KNOWN_LIMITATIONS
-> OPTIONAL_YOLO
-> EXPORTS
-> PROVENANCE_AUDIT
-> COMPLETION_CHECKLIST
```

## Result

The canonical docs now describe TOM v3 Simple as a local observation/evidence platform with a fixture demo, optional YOLO path, review exports, and provenance audit.

Milestone docs remain accessible as historical memory.

## Validation Commands

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5d_check.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5d_check.db make completion-audit PYTHON=.venv/bin/python
```

## Next Handoff

Recommended next milestone:

Milestone 5E - Final Completion Review

## Boundary

No new product capability was added. No real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or adjudication was added.
