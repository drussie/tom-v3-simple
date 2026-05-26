# Milestone 0E Agent Report - Integration / QA / Repo Consolidation

## Summary

Status: complete.

Milestone 0E consolidated TOM v3 Simple Milestone 0 into a runnable local foundation. The repo now has setup docs, demo docs, common commands, a synthetic viewer smoke script, integration smoke coverage, updated project memory, and branch/default-branch guidance.

## Files Created

- `.env.example`
- `Makefile`
- `docs/dev/local_environment_setup.md`
- `docs/dev/local_demo_runbook.md`
- `docs/dev/repo_branch_hygiene.md`
- `docs/milestones/milestone_0e_integration_qa_repo_consolidation.md`
- `docs/handoffs/milestone_0e_integration_qa_repo_consolidation_handoff.md`
- `docs/agent_reports/milestone_0e_integration_qa_repo_consolidation_report.md`
- `scripts/smoke_synthetic_viewer_data.py`
- `tests/test_milestone_0_integration.py`

## Files Modified

- `README.md`
- `apps/api/routers/viewer.py`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/milestones/milestone_0_observation_store_visual_foundation.md`

## Integration Decisions

- The smoke script seeds a synthetic run, verifies it, builds the backend viewer read model, and checks expected view states, tracks, gaps, homography placeholders, candidates, lineage, and artifacts.
- The viewer API composition logic is exposed as `build_viewer_run_payload` so the endpoint, script, and tests exercise the same read model.
- The integration test uses a temporary SQLite database to keep the smoke gate fast and deterministic.

## Developer Setup Decisions

- SQLite is documented as the default fast local path.
- Postgres remains documented as the optional migration-managed local database.
- The root Makefile wraps common backend, worker, web, and validation commands.
- `.env.example` captures the shared local defaults.
- Web dependency installation remains explicit under `apps/web`.

## Validation Results

Final validation commands:

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db .venv/bin/python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip --source-uri file:///dev/synthetic-tennis-clip.mp4 --run-name synthetic-baseline-run`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db .venv/bin/python -m apps.worker.cli verify-synthetic-run --run-id <RUN_ID>`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `make smoke PYTHON=.venv/bin/python`
- `find docs -maxdepth 3 -type f | sort`
- `git status --short`

Results:

- Pytest passed: 9 tests.
- Ruff passed.
- Web lint passed.
- Web build passed.
- Web audit found 0 vulnerabilities.
- Alembic SQLite smoke test passed.
- Worker seed and verify passed with verifier `ok: true`.
- Synthetic viewer smoke script passed with smoke `ok: true`.

## Branch/Default-Branch Status

GitHub reports the current default branch as:

```text
codex/m0a-repo-memory-architecture-schema
```

Remote `main` does not currently exist.

The GitHub CLI is installed locally but not authenticated, so the default branch was not changed by this milestone.

Exact cleanup steps are documented in:

```text
docs/dev/repo_branch_hygiene.md
```

Recommended final state:

```text
main = consolidated Milestone 0 baseline
default branch = main
```

## Known Limitations

- No real media file is indexed yet.
- No video upload flow exists yet.
- No real model output is ingested yet.
- No artifact files are generated.
- No Postgres-backed automated integration test exists yet.
- Web annotation creation remains future work.

## Non-goals Preserved

- No YOLO integration was added.
- No TOM v1 integration was added.
- No real video decoding was added.
- No real ffprobe media indexing was added.
- No real tracking implementation was added.
- No real homography calculation was added.
- No real bounce detection was added.
- No streaming ingestion was added.
- No production auth was added.
- No deployment work was added.
- No adjudication system was added.

## Recommended Next Handoff

Milestone 1A - Real Media Indexing + Video Upload/Registration.

This is the better next milestone before a TOM v1 gameplay detector adapter because every future model adapter needs reliable media registration, frame count, FPS, timestamps, dimensions, checksums, and artifact paths. Once that substrate is real, TOM v1 gameplay classification can be wrapped behind the TOM v3 observation interface cleanly.
