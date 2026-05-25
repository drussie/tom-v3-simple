# API

FastAPI backend foundation for TOM v3 Simple.

Milestone 0B implements:

- `/health`
- media registration
- model registry records
- runtime config records
- processing runs and steps
- single and batch observation writes through the central observation writer
- observation query/detail/lineage/artifact/annotation endpoints
- artifact metadata records
- human annotation records
- dev-only synthetic persistence path at `/dev/synthetic-run`

Run locally:

```bash
TOM_V3_CREATE_DB_ON_STARTUP=true .venv/bin/uvicorn apps.api.main:app --reload
```
