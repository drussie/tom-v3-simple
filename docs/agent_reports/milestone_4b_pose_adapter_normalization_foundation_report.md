# Milestone 4B Agent Report - Pose Adapter Normalization Foundation

## Summary

Milestone 4B adds pose output normalization for fake/serialized pose frame results. It converts COCO17-shaped keypoint output into `PoseObservationCreate`-compatible payloads, including bbox context, crop projection, subject association candidate fields, confidence summaries, and adapter diagnostics. It does not add real pose inference or movement interpretation.

## Files Created

- `packages/model_adapters/tom_v3_model_adapters/pose_normalization.py`
- `tests/test_pose_normalization.py`
- `docs/pose/pose_adapter_normalization_v0.md`
- `docs/milestones/milestone_4b_pose_adapter_normalization_foundation.md`
- `docs/handoffs/milestone_4b_pose_adapter_normalization_foundation_handoff.md`
- `docs/agent_reports/milestone_4b_pose_adapter_normalization_foundation_report.md`

## Files Modified

- `packages/model_adapters/tom_v3_model_adapters/__init__.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/pose/pose_observation_schema_v0.md`
- `docs/pose/skeleton_registry_v0.md`
- `docs/pose/pose_runtime_config_v0.md`
- `docs/blueprints/tom_v3_blueprint_4_pose_observation_movement_evidence_layer.md`

## Normalization Decisions

The normalizer accepts dict-shaped frame results with `poses`, assigns COCO17 names/indices from the skeleton registry, and emits `NormalizedPoseObservation` objects that can instantiate `PoseObservationCreate`.

## Keypoint Handling Decisions

Keypoints must match the COCO17 count in v0. Missing keypoints are preserved with `present = false`. Invalid keypoint count skips the pose. Non-numeric coordinates mark the keypoint missing and record a warning.

## Bbox / Confidence Decisions

`bbox_xyxy` converts to typed bbox fields. Invalid bbox does not discard otherwise valid keypoints; bbox fields are set to null and an `invalid_bbox` warning is recorded. Provided pose confidence is copied, missing pose confidence falls back to mean keypoint confidence, and confidence values outside `0..1` warn without clamping.

## Crop Projection Decision

Crop-local projection is implemented for `keypoint_coordinate_space = crop_pixels`. Full-frame coordinates are computed by adding the crop origin, crop fields are stored, and crop-local keypoints are retained in normalization metadata.

## Subject Association Decision

Full-frame poses default to unassociated evidence. Input `subject_context` can pass through candidate association fields for player detection, tracklet, or track point context without claiming subject identity.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `npm run lint` in `apps/web`
- `npm run build` in `apps/web`
- `npm audit --omit=dev` in `apps/web`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `.venv/bin/python -m pytest tests/test_pose_normalization.py -q`
- `.venv/bin/python -m pytest tests/test_pose_schema.py tests/test_pose_observation_persistence.py -q`

## Validation Results

- Full Python suite: 136 passed.
- Ruff: passed.
- Web lint: passed.
- Web production build: passed.
- Web npm audit: 0 vulnerabilities.
- Alembic smoke: passed, including `0002_pose_observation`.
- Synthetic viewer smoke: passed.
- Focused pose normalization tests: 16 passed.
- Focused 4A pose schema/persistence tests: included in full suite and focused checks.

## Known Limitations

- No real pose runtime exists yet.
- No pose processing run/worker persistence pipeline exists yet.
- No pose overlay viewer exists yet.
- Pose export/review integration remains future work.

## Non-Goals Preserved

- No movement interpretation.
- No serve, split-step, or biomechanics conclusions.
- No homography.
- No bounce or hit detection.
- No rally/point/scoring.
- No adjudication.

## Recommended Next Handoff

Milestone 4C - Pose Observation Persistence and Lineage.
