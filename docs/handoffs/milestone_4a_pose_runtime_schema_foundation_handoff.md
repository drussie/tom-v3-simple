# Milestone 4A Handoff - Pose Runtime / Schema Foundation

## Starting State

Blueprints 1, 2, and 3 were complete.

Blueprint 4 started with no pose schema, runtime config contract, or typed pose persistence table.

## Completed Work

- Added Blueprint 4 doc.
- Added COCO17 skeleton registry and validation helpers.
- Added pose keypoint and pose observation schema helpers.
- Added `pose_observation` SQLAlchemy model and Alembic migration.
- Extended `ObservationWriter` and observation detail read models for pose typed rows.
- Added synthetic fixture pose insertion helper.
- Added tests for skeleton validation, pose persistence, queryability, model metadata, runtime config metadata, frame/time ownership, and unassociated subject mode.
- Added docs for pose schema, skeleton registry, and runtime config.

## Validation

Run:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint
cd apps/web && npm run build
cd apps/web && npm audit --omit=dev
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
python scripts/smoke_synthetic_viewer_data.py
```

Focused checks:

```bash
pytest tests/test_pose_schema.py tests/test_pose_observation_persistence.py -q
```

## Non-Goals Preserved

- No real pose inference.
- No pose overlay viewer.
- No movement interpretation.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 4B - Pose Adapter Normalization Foundation.
