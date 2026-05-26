# Milestone 2D Handoff - Tracklet Evidence Export / Review Dataset Foundation

## Starting State

Milestone 2C added structured tracklet query, review labels, annotations on tracklet/track point/source detection observations, annotation summaries in evidence bundles, and viewer review controls.

## Mission

Package selected candidate tracklet evidence into durable local export artifacts without mutating observations or converting review annotations into adjudicated results.

## Required Work

- Build a tracklet review dataset export service.
- Support export by explicit tracklet ids.
- Support export by query filters through the existing tracklet query service.
- Include tracklet evidence bundle contents, annotations, frame artifact metadata, lineage, and provenance.
- Write JSON to `.data/exports/tracklets/{export_id}/tracklet_review_dataset.json`.
- Persist a `tracklet_review_dataset_export` evidence artifact with checksum.
- Persist a `query_result` row for query-based exports when practical.
- Add worker CLI command `export-tracklet-review-dataset`.
- Add API endpoint `POST /tracklets/export-review-dataset` if low risk.
- Update docs and tests.

## Non-Goals

- No model training.
- No generated label source.
- No pose, homography, bounce, hit, rally, point, or scoring logic.
- No production storage/auth.
- No adjudication.

## Validation

Run:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
```

Also run a local evidence path and export:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"has_annotation":true}' \
  --output-root .data/exports \
  --format json
```

## Completion State

Milestone 2D is implemented on `codex/m2d-tracklet-evidence-export-review-dataset`.

Recommended next handoff: Milestone 2E - Blueprint 2 Completion Review / Temporal Evidence Hardening.
