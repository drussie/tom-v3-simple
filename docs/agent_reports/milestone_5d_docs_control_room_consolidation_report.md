# Milestone 5D Agent Report - Docs / Control-Room Consolidation

## Summary

Milestone 5D consolidates TOM v3 Simple repo memory into a concise canonical documentation set. The new docs explain what the platform is, what it is not, how to run and audit the local demo, how evidence is stored, what optional YOLO means, how exports work, and what remains out of scope.

## Files Created

- `docs/CONTROL_ROOM.md`
- `docs/ARCHITECTURE.md`
- `docs/OBSERVATION_CONTRACT.md`
- `docs/BLUEPRINT_STATUS.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/OPTIONAL_YOLO.md`
- `docs/EXPORTS.md`
- `docs/COMPLETION_CHECKLIST.md`
- `docs/milestones/milestone_5d_docs_control_room_consolidation.md`
- `docs/handoffs/milestone_5d_docs_control_room_consolidation_handoff.md`
- `docs/agent_reports/milestone_5d_docs_control_room_consolidation_report.md`

## Files Modified

- `README.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/blueprints/tom_v3_blueprint_5_simple_completion_product_hardening.md`
- `docs/dev/local_demo_runbook.md`

## Canonical Docs Decisions

The canonical docs are current-state summaries, not milestone archaeology. Milestone docs remain historical memory and are still linked from the control-room index.

## Control-Room Decisions

`docs/CONTROL_ROOM.md` is now the short canonical repo-memory/status document. `docs/CONTROL_ROOM_INDEX.md` remains the full index of canonical docs, historical docs, handoffs, and agent reports.

## Known Limitations Decisions

Known limitations are explicit and grouped by model/runtime, evidence, product, tennis-understanding, and export/data constraints.

## Optional YOLO Documentation Decisions

YOLO is documented as optional, locally gated, and separate from the default fixture demo. YOLO-origin detections are described as observations only.

## Validation Results

- `pytest -q`: passed, 159 tests.
- `ruff check .`: passed.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`: passed.
- `python scripts/smoke_synthetic_viewer_data.py`: passed.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5d_check.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`: passed.
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_5d_check.db make completion-audit PYTHON=.venv/bin/python`: passed.

## Non-Goals Preserved

- No new product capability.
- No new backend logic.
- No new frontend logic.
- No new database schema.
- No real pose inference.
- No movement interpretation.
- No stroke classification.
- No homography.
- No bounce/hit/rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 5E - Final Completion Review
