# Milestone 0D - Visual Evidence Viewer Foundation

## Goal

Build the first TOM v3 Simple frontend surface that can load a persisted run and show the evidence behind observations.

The target loop:

```text
persisted synthetic run -> backend viewer read model -> timeline / detail / lineage / artifact panels
```

## Scope

Milestone 0D includes:

- Next.js / React app under `apps/web`
- backend API client
- run loading by run id
- viewer read model endpoint over persisted backend rows
- gameplay/non_gameplay/uncertain timeline band
- ball, near-player, and far-player track coverage rows
- homography valid/missing row
- candidate marker row
- observation list
- observation detail panel
- lineage panel
- artifact panel
- annotation panel foundation
- docs updates and agent report

## Non-goals

- No real video processing.
- No YOLO integration.
- No TOM v1 gameplay detector integration.
- No real tracking implementation.
- No real homography calculation.
- No real bounce detection.
- No streaming viewer.
- No production auth.
- No cloud deployment.
- No TOM v2 adjudication.

## Acceptance Status

Status: complete.

Milestone 0D acceptance criteria are satisfied by:

- web app in `apps/web`
- viewer page at `/runs/{run_id}`
- TOM v3 API client in `apps/web/src/lib/api.ts`
- viewer data transforms in `apps/web/src/lib/viewerData.ts`
- timeline and panel components in `apps/web/src/components`
- backend viewer endpoint in `apps/api/routers/viewer.py`
- viewer endpoint tests in `tests/test_viewer_api.py`
- updated project memory docs

## Local Demo Flow

Seed a synthetic run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db \
.venv/bin/python -m apps.worker.cli seed-synthetic-run \
  --scenario baseline-tennis-clip \
  --source-uri file:///dev/synthetic-tennis-clip.mp4 \
  --run-name synthetic-baseline-run
```

Start the backend against the same database:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db \
TOM_V3_CREATE_DB_ON_STARTUP=true \
.venv/bin/uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

Start the frontend:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/runs/<run_id>
```

## Next Handoff

Milestone 0E - Integration / QA / Repo Consolidation.
