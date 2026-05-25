# Milestone 0B Handoff - Backend / API Foundation

## Repo

- Repo: drussie/tom-v3-simple
- Branch: codex/m0b-backend-api

## Mission

Implement the first backend/API foundation for TOM v3 Simple.

TOM v3 Simple is:

> A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Boundary

TOM v3 is observation-only.

Core invariant:

> TOM v3 records what was observed, not what was proven.

Human review creates `human_annotation` records. It does not mutate observations.

## Result

Status: complete.

Milestone 0B created:

- FastAPI app in `apps/api`.
- Pydantic schema contracts in `packages/schema/tom_v3_schema`.
- SQLAlchemy models in `packages/storage/tom_v3_storage/db_models.py`.
- Alembic migration in `migrations/versions/0001_observation_store.py`.
- Central observation writer in `packages/observations/tom_v3_observations/writer.py`.
- Synthetic/dev insertion helper in `packages/observations/tom_v3_observations/synthetic.py`.
- Tests in `tests/test_backend_api.py`.
- API and database schema docs.

## API Surface

Implemented:

- `GET /health`
- `POST /media`
- `GET /media/{media_id}`
- `POST /models`
- `GET /models/{model_id}`
- `POST /runtime-configs`
- `GET /runtime-configs/{runtime_config_id}`
- `POST /media/{media_id}/runs`
- `GET /runs/{run_id}`
- `POST /runs/{run_id}/steps`
- `GET /runs/{run_id}/steps`
- `POST /observations`
- `POST /observations/batch`
- `POST /observations/query`
- `GET /observations/{observation_id}`
- `GET /observations/{observation_id}/lineage`
- `GET /observations/{observation_id}/artifacts`
- `GET /observations/{observation_id}/annotations`
- `POST /artifacts`
- `GET /artifacts/{artifact_id}`
- `POST /annotations`
- `POST /dev/synthetic-run`

## Validation

Completed:

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`

## Known Gaps

- The synthetic/dev API path is intentionally small and API-local.
- No worker exists yet.
- No frontend viewer exists yet.
- No real model integration exists yet.
- Postgres is the intended database target, while tests use SQLite for milestone speed.

## Recommended Next Handoff

Milestone 0C - Worker + Synthetic Observation Seeder.

Suggested focus:

- Create a worker entrypoint that uses the same observation writer.
- Move synthetic seeding into worker-owned dev tooling.
- Generate richer synthetic observations and artifacts.
- Keep real ML integration out of scope until the synthetic loop is stable.
