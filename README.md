# TOM v3 Simple

TOM v3 Simple is a lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Observation-Only Boundary

TOM v3 Simple is not TOM v2.

It does not adjudicate truth. It records observations, lineage, artifacts, and annotations.

The core invariant:

> TOM v3 records what was observed, not what was proven.

## Current Status

Milestone 0E consolidates the Milestone 0 foundation:

- repo memory and architecture contracts
- FastAPI backend/API foundation
- SQLAlchemy observation store and Alembic migration
- central observation writer
- worker CLI and rich synthetic seeder
- viewer-ready synthetic baseline data
- Next.js visual evidence viewer foundation
- local setup, runbook, Makefile, and smoke validation

No real model pipeline, YOLO integration, TOM v1 integration, real video processing, real tracking, real homography calculation, or real bounce detection is implemented yet.

## Repo Structure

```text
apps/
  api/       FastAPI backend foundation.
  worker/    Worker CLI and rich synthetic seeding entrypoint.
  web/       Visual evidence viewer foundation.
packages/
  schema/          Shared schema contracts.
  storage/         Storage adapters and persistence helpers.
  video/           Media indexing and video utilities placeholder.
  observations/    Observation writer, lineage, and synthetic helpers.
  visualization/   Viewer-oriented utilities placeholder.
migrations/        Alembic database migrations.
scripts/           Local smoke and developer scripts.
tests/             Backend, worker, viewer, and integration tests.
docs/              Durable project memory and architecture contracts.
```

## Quickstart

Create a local environment:

```bash
conda create -n tom_v3 python=3.11 -y
conda activate tom_v3
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Install web dependencies:

```bash
cd apps/web
npm install
cd ../..
```

Set local defaults:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
export TOM_V3_CREATE_DB_ON_STARTUP=true
export NEXT_PUBLIC_TOM_V3_API_BASE_URL="http://127.0.0.1:8000"
```

Run migrations:

```bash
alembic upgrade head
```

Seed synthetic evidence:

```bash
python -m apps.worker.cli seed-synthetic-run \
  --scenario baseline-tennis-clip \
  --source-uri file:///dev/synthetic-tennis-clip.mp4 \
  --run-name synthetic-baseline-run
```

Use the `run_id` from the seed output to verify:

```bash
python -m apps.worker.cli verify-synthetic-run --run-id <RUN_ID>
```

Start the API:

```bash
uvicorn apps.api.main:app --reload
```

Start the web viewer in another terminal:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/runs/<RUN_ID>
```

## Validation

Run the consolidated checks:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
```

Run the Milestone 0 smoke check:

```bash
python scripts/smoke_synthetic_viewer_data.py
```

The root `Makefile` wraps common commands:

```bash
make install
make web-install
make test
make lint
make migrate
make seed
make smoke
make all-checks
```

## Docs Entrypoint

Start with [docs/CONTROL_ROOM_INDEX.md](docs/CONTROL_ROOM_INDEX.md).

Useful runbooks:

- [Local Environment Setup](docs/dev/local_environment_setup.md)
- [Local Demo Runbook](docs/dev/local_demo_runbook.md)
- [Repo Branch Hygiene](docs/dev/repo_branch_hygiene.md)
