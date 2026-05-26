# Milestone 0E Handoff - Integration / QA / Repo Consolidation

## Repo

- Repo: drussie/tom-v3-simple
- Branch: codex/m0e-integration-qa-repo-consolidation

## Mission

Consolidate TOM v3 Simple Milestone 0 into a coherent, runnable foundation.

TOM v3 Simple is:

> A lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation - including gameplay/non-gameplay state - and makes the evidence queryable and visually replayable without adjudicating truth.

## Boundary

TOM v3 is observation-only.

Core invariant:

> TOM v3 records what was observed, not what was proven.

Milestone 0E does not add real ML, real video processing, real tracking, real homography calculation, real bounce logic, production auth, or deployment.

## Result

Status: complete.

Milestone 0E created:

- local environment setup doc
- local demo runbook
- branch/default-branch hygiene doc
- `.env.example`
- root Makefile
- synthetic viewer data smoke script
- Milestone 0 integration smoke test
- updated README and durable project memory
- final Milestone 0E agent report

## Local Run Path

Set up:

```bash
conda create -n tom_v3 python=3.11 -y
conda activate tom_v3
python -m pip install --upgrade pip
pip install -e ".[dev]"
cd apps/web && npm install && cd ../..
```

Run:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
export TOM_V3_CREATE_DB_ON_STARTUP=true
alembic upgrade head
python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip
uvicorn apps.api.main:app --reload
```

Then start the web app:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open `/runs/<RUN_ID>`.

## Branch/Default Branch Status

GitHub reports the default branch as:

```text
codex/m0a-repo-memory-architecture-schema
```

Remote `main` does not currently exist.

The exact cleanup steps are documented in:

```text
docs/dev/repo_branch_hygiene.md
```

The GitHub CLI was available locally but not authenticated, so default-branch mutation was not performed by this milestone.

## Recommended Next Handoff

Milestone 1A - Real Media Indexing + Video Upload/Registration.

This should come before TOM v1 gameplay detector adapter work because real model adapters need stable media and frame/time indexing first.
