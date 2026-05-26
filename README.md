# TOM v3 Simple

TOM v3 Simple is a lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Observation-Only Boundary

TOM v3 Simple is not TOM v2.

It does not adjudicate truth. It records observations, lineage, artifacts, and annotations.

The core invariant:

> TOM v3 records what was observed, not what was proven.

## Core Pillars

1. Observation Store
2. Lineage / Evidence Index
3. Visual Evidence Viewer

## Current Milestone

Current phase: Milestone 0D - Visual Evidence Viewer Foundation.

Milestone 0A created the repo-backed memory, architecture documentation, schema direction, and handoff structure future agents should follow.

Milestone 0B adds the first FastAPI backend, SQLAlchemy storage models, Alembic migration, schema contracts, observation writer, query API, and synthetic/dev insertion path.

Milestone 0C adds the first worker CLI and a rich synthetic observation seeding flow that feeds the future visual evidence viewer without real model integration.

Milestone 0D adds the first web viewer that loads persisted run evidence through backend/API contracts and renders timeline rows, candidate markers, detail, lineage, and artifact panels.

No real model pipeline, YOLO integration, TOM v1 integration, real bounce detection, real tracking implementation, or production viewer deployment is implemented yet.

## Docs Entrypoint

Start with [docs/CONTROL_ROOM_INDEX.md](docs/CONTROL_ROOM_INDEX.md).

## Basic Repo Structure

```text
apps/
  api/       FastAPI backend foundation.
  worker/    Worker CLI and rich synthetic seeding entrypoint.
  web/       Visual evidence viewer foundation.
packages/
  schema/          Shared schema contracts.
  storage/         Storage adapters and persistence helpers.
  video/           Media indexing and video utilities.
  observations/    Observation vocabulary and helpers.
  visualization/   Viewer-oriented utilities.
migrations/        Alembic database migrations.
tests/             Backend API and observation writer tests.
docs/              Durable project memory and architecture contracts.
```

## Backend Quickstart

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
```

Optional local Postgres:

```bash
docker compose up -d postgres
TOM_V3_DATABASE_URL=postgresql+psycopg://tom_v3:tom_v3@localhost:5432/tom_v3 .venv/bin/alembic upgrade head
```
