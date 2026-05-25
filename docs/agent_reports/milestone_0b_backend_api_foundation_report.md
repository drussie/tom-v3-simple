# Milestone 0B Agent Report - Backend / API Foundation

## Summary

Status: complete.

Milestone 0B implemented the first backend/API foundation for TOM v3 Simple: FastAPI app, database models, Alembic migration, schema contracts, central observation writer, query/detail APIs, lineage/artifact/annotation APIs, a dev synthetic insertion path, and tests.

## Files Created

- `.gitignore`
- `pyproject.toml`
- `docker-compose.yml`
- `alembic.ini`
- `apps/__init__.py`
- `apps/api/__init__.py`
- `apps/api/config.py`
- `apps/api/db.py`
- `apps/api/main.py`
- `apps/api/routers/`
- `apps/api/services/`
- `packages/schema/tom_v3_schema/`
- `packages/storage/tom_v3_storage/`
- `packages/observations/tom_v3_observations/`
- `migrations/env.py`
- `migrations/versions/0001_observation_store.py`
- `tests/test_backend_api.py`
- `docs/milestones/milestone_0b_backend_api_foundation.md`
- `docs/handoffs/milestone_0b_backend_api_foundation_handoff.md`
- `docs/api/backend_api_v0.md`
- `docs/schema/database_schema_v0.md`

## Files Modified

- `README.md`
- `apps/api/README.md`
- `packages/schema/README.md`
- `packages/storage/README.md`
- `packages/observations/README.md`
- `migrations/README.md`
- `tests/README.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/milestones/milestone_0_observation_store_visual_foundation.md`

## Database Decisions

- SQLAlchemy 2.x models define the storage contract.
- Alembic owns the initial migration.
- Postgres is the intended local/dev database target.
- SQLite is used in tests for fast milestone validation.
- JSON payload columns use SQLAlchemy JSON with a Postgres JSONB variant.
- `observation` is the central append-only spine.
- `idempotency_key` has a unique index to support safe retries.

## API Decisions

- FastAPI is the backend app.
- Pydantic v2 schemas live in `packages/schema`.
- Initial API route groups cover media, registry/config, runs/steps, observations, artifacts, annotations, and dev support.
- `POST /media` registers metadata only in v0.
- `POST /dev/synthetic-run` is clearly dev-only and proves persistence without real model integration.

## Observation Writer Decisions

- Single and batch observation endpoints write through the central `ObservationWriter`.
- The writer inserts the observation spine row, typed extension row, lineage rows, and artifact records.
- Duplicate `idempotency_key` writes return the existing observation detail instead of inserting a duplicate.
- Human review is represented by `human_annotation` records and does not mutate observations.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`

## Validation Results

- Pytest passed: 3 tests.
- Ruff passed.
- Alembic upgrade smoke test passed against SQLite.
- Final docs/file listing and git status were checked before commit.

## Known Gaps

- No worker exists yet.
- No frontend evidence viewer exists yet.
- No real video processing exists yet.
- No real model integration exists yet.
- Optional architecture tables `frame_index`, `pose_observation`, `court_observation`, and `homography_observation` are not implemented in 0B.
- Tests use SQLite; future integration work should add Postgres-backed checks when practical.

## Non-goals Preserved

- No YOLO integration was added.
- No TOM v1 integration was added.
- No real detector pipeline was added.
- No real bounce logic was added.
- No frontend evidence viewer was added.
- No adjudication system was added.

## Recommended Next Handoff

Milestone 0C - Worker + Synthetic Observation Seeder.

The next agent should create a worker entrypoint and richer synthetic seeding flow that reuses the central observation writer and feeds the existing API/query foundation.
