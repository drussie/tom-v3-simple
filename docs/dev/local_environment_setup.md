# Local Environment Setup

## Python Environment

Create and activate the recommended local Conda environment:

```bash
conda create -n tom_v3 python=3.11 -y
conda activate tom_v3
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

For existing virtualenv users, the same editable install works from any Python 3.11 environment:

```bash
python -m pip install -e ".[dev]"
```

## Web Dependencies

Install the web app dependencies:

```bash
cd apps/web
npm install
```

## Environment Variables

For fast local development, use SQLite:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
export TOM_V3_CREATE_DB_ON_STARTUP=true
export NEXT_PUBLIC_TOM_V3_API_BASE_URL="http://127.0.0.1:8000"
```

The same values are captured in `.env.example`.

## SQLite Database

SQLite is the default path for local smoke testing:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
alembic upgrade head
```

The worker CLI can also create tables for local development if migrations have not been run.

## Optional Postgres Database

The repository includes `docker-compose.yml` for local Postgres:

```bash
docker compose up -d postgres
export TOM_V3_DATABASE_URL="postgresql+psycopg://tom_v3:tom_v3@localhost:5432/tom_v3"
alembic upgrade head
```

Postgres is the intended development database target for richer integration checks. SQLite remains the quick local default.

## Common Commands

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

Use `RUN_ID` for run-specific verification:

```bash
make verify RUN_ID=<run_id>
```
