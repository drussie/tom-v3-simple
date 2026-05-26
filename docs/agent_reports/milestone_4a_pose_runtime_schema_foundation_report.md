# Milestone 4A Agent Report - Pose Runtime / Schema Foundation

## Summary

Milestone 4A starts Blueprint 4 by adding first-class pose observation schema, COCO17 skeleton metadata, keypoint validation, typed pose persistence, and synthetic fixture pose insertion. It does not add real pose inference or movement interpretation.

## Files Created

- `packages/schema/tom_v3_schema/skeletons.py`
- `packages/schema/tom_v3_schema/pose.py`
- `packages/observations/tom_v3_observations/pose.py`
- `migrations/versions/0002_pose_observation.py`
- `tests/test_pose_schema.py`
- `tests/test_pose_observation_persistence.py`
- `docs/blueprints/tom_v3_blueprint_4_pose_observation_movement_evidence_layer.md`
- `docs/pose/skeleton_registry_v0.md`
- `docs/pose/pose_observation_schema_v0.md`
- `docs/pose/pose_runtime_config_v0.md`
- `docs/milestones/milestone_4a_pose_runtime_schema_foundation.md`
- `docs/handoffs/milestone_4a_pose_runtime_schema_foundation_handoff.md`
- `docs/agent_reports/milestone_4a_pose_runtime_schema_foundation_report.md`

## Files Modified

- `packages/storage/tom_v3_storage/db_models.py`
- `packages/schema/tom_v3_schema/observations.py`
- `packages/observations/tom_v3_observations/writer.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/blueprints/tom_v3_blueprint_3_completion_review.md`

## Schema Decisions

Pose observations use the existing observation spine plus a new typed `pose_observation` table. Keypoints are stored as JSON in v0, with summary columns for count, present/missing counts, confidence statistics, pose confidence, bbox context, and subject association candidate fields.

## Skeleton Registry Decisions

COCO17 is the first skeleton format. The registry stores keypoint names, indices, and skeleton edges, and validation ensures keypoint payloads match the registered format/version.

## Pose Observation Persistence Decisions

`ObservationWriter` now supports one pose typed extension when `observation_family = pose`. The synthetic helper creates model/runtime/run/step records, writes the observation spine row, and writes the typed pose row with `frame_time_owner = media_indexing`.

## Model Registry / Runtime Config Decisions

Milestone 4A defines fixture pose model metadata and a pose runtime config shape. Real pose weights and runtime probing are deferred.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `npm run lint` in `apps/web`
- `npm run build` in `apps/web`
- `npm audit --omit=dev` in `apps/web`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `.venv/bin/python -m pytest tests/test_pose_schema.py tests/test_pose_observation_persistence.py -q`

## Validation Results

- Full Python suite: 120 passed.
- Ruff: passed.
- Web lint: passed.
- Web production build: passed.
- Web npm audit: 0 vulnerabilities.
- Alembic smoke: passed, including `0002_pose_observation`.
- Synthetic viewer smoke: passed.
- Focused pose schema/persistence tests: 14 passed.

## Known Limitations

- No real pose runtime or adapter exists yet.
- No pose overlay viewer exists yet.
- Pose-specific query API filters are deferred.
- Source detection/tracklet association lineage is documented for future work but not implemented in 4A fixture data.

## Non-Goals Preserved

- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 4B - Pose Adapter Normalization Foundation.
