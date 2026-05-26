# TOM v3 Simple Web

Milestone 0D adds the first visual evidence viewer for TOM v3 Simple.

The app loads viewer-ready run data from the TOM v3 backend and renders:

- gameplay, non-gameplay, and uncertain view-state bands
- ball, near-player, and far-player track coverage rows
- homography valid/missing intervals
- candidate markers
- observation detail, lineage, artifact, and annotation panels

The viewer does not create a separate frontend-only evidence model. It consumes persisted
observations, tracklets, lineage rows, artifacts, and annotations from the backend.

## Local Development

Start the backend with a database that has a seeded synthetic run, then run:

```bash
cd apps/web
npm install
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/runs/<run_id>
```

For a local synthetic run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db \
python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip
```
