# Milestone 0B - Backend / API Foundation

## Goal

Implement the first backend/API foundation for TOM v3 Simple:

```text
media -> processing run -> persisted observations -> lineage -> query API
```

This milestone makes the observation store real without adding real ML, video processing, bounce logic, or a frontend evidence viewer.

## Scope

Milestone 0B includes:

- FastAPI backend skeleton
- configuration management
- database connection
- Alembic migrations
- SQLAlchemy storage models
- Pydantic request/response schemas
- media registration API
- model registry API
- runtime config API
- processing run and processing step APIs
- observation spine model
- typed observation extension models
- observation writer service
- observation query endpoint
- observation detail endpoint
- lineage endpoint
- artifact metadata endpoint
- annotation endpoint
- synthetic/dev observation insertion support
- backend tests
- docs updates and agent report

## Non-goals

- No YOLO integration.
- No TOM v1 gameplay detector integration.
- No real video processing.
- No real bounce detection.
- No real tracking implementation.
- No frontend evidence viewer.
- No streaming ingestion.
- No production auth.
- No cloud deployment.
- No advanced analytics.
- No TOM v2 adjudication.

## Acceptance Status

Status: complete.

Milestone 0B acceptance criteria are satisfied by:

- backend app in `apps/api`
- schema contracts in `packages/schema`
- observation writer and synthetic helper in `packages/observations`
- storage models in `packages/storage`
- Alembic migration in `migrations/versions/0001_observation_store.py`
- backend tests in `tests/test_backend_api.py`
- API and database docs in `docs/api` and `docs/schema`

## Next Handoff

Milestone 0C - Worker + Synthetic Observation Seeder.
