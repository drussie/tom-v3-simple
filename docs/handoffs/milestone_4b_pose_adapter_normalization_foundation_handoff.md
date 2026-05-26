# Milestone 4B Handoff - Pose Adapter Normalization Foundation

## Starting State

Milestone 4A created the pose observation typed table, COCO17 skeleton registry, keypoint validation, and synthetic pose insertion.

## Completed Work

- Added `tom_v3_model_adapters.pose_normalization`.
- Added `NormalizedPoseObservation`, `PoseNormalizationResult`, and `PoseAdapterResult`.
- Added `PoseNormalizationAdapter` and `FixturePoseAdapter` skeletons.
- Added full-frame pose normalization for fake/serialized pose frame results.
- Added COCO17 keypoint naming/index assignment from the skeleton registry.
- Added missing keypoint preservation.
- Added bbox conversion with invalid bbox warnings that keep valid keypoints.
- Added pose/keypoint/bbox confidence warning behavior.
- Added crop-local to full-frame keypoint projection.
- Added subject association candidate passthrough.
- Added focused tests for pose normalization and adapter diagnostics.
- Added docs for the normalization contract and updated project memory.

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
pytest tests/test_pose_normalization.py -q
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

Milestone 4C - Pose Observation Persistence and Lineage.
