# Milestone 3E Handoff - Real YOLO Runtime Local Smoke / Viewer Validation

## Starting State

Milestone 3D added guarded YOLO frame inference and persistence with fake-provider tests. Real local runtime smoke remained optional and manual.

## Completed Work

Milestone 3E adds the local smoke validation foundation:

```text
runtime probe
-> weights registration
-> media indexing
-> YOLO detection adapter run
-> frame artifact extraction
-> viewer validation
-> optional tracklet builder
-> evidence bundle inspection
```

The smoke path is optional and skipped gracefully when runtime packages, weights, or source media are unavailable.

## Primary Files

- `apps/worker/services/real_yolo_smoke.py`
- `scripts/smoke_real_yolo_local.py`
- `apps/worker/cli.py`
- `tests/test_real_yolo_smoke.py`
- `docs/model_adapters/yolo_real_runtime_smoke_v0.md`

## Commands

Plan only:

```bash
python -m apps.worker.cli smoke-real-yolo-local --plan-only
```

Local smoke:

```bash
python -m apps.worker.cli smoke-real-yolo-local \
  --source-path <sample_video_path> \
  --weights-path model_assets/yolo/<weights_file>.pt \
  --model-name local-yolo-smoke \
  --model-version local-v0 \
  --device cpu \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --run-tracklets
```

## Validation

Default validation does not require real YOLO:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
python -m apps.worker.cli yolo-runtime-probe
```

## Next Suggested Milestone

Milestone 3F - Blueprint 3 Completion Review / Real Model Runtime Hardening.
