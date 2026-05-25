# Worker

Worker entrypoints for TOM v3 Simple.

Milestone 0C adds a synthetic observation seeder that creates viewer-ready evidence without real model integration.

Run locally against SQLite:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db \
python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip
```

Verify a seeded run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_worker_seed.db \
python -m apps.worker.cli verify-synthetic-run --run-id <run_id>
```
