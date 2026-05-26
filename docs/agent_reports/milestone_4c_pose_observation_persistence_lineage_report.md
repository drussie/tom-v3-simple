# Milestone 4C Agent Report - Pose Observation Persistence and Lineage

## Summary

Milestone 4C persists normalized fixture pose observations through a worker pose processing-run path. Pose evidence now has run/step provenance, typed pose rows, media-owned frame/time, and lineage to source `player_detection` observations when candidate subject context is supplied.

## Files Created

- `apps/worker/services/pose_adapter.py`
- `tests/test_pose_persistence_lineage.py`
- `docs/pose/pose_persistence_lineage_v0.md`
- `docs/milestones/milestone_4c_pose_observation_persistence_lineage.md`
- `docs/handoffs/milestone_4c_pose_observation_persistence_lineage_handoff.md`
- `docs/agent_reports/milestone_4c_pose_observation_persistence_lineage_report.md`

## Files Modified

- `apps/worker/cli.py`
- `Makefile`
- `packages/schema/tom_v3_schema/enums.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/blueprints/tom_v3_blueprint_4_pose_observation_movement_evidence_layer.md`
- `docs/pose/pose_observation_schema_v0.md`
- `docs/pose/pose_adapter_normalization_v0.md`
- `docs/pose/pose_runtime_config_v0.md`

## Persistence Decisions

The worker service creates a fixture pose model registry row, runtime config, `processing_run`, and `processing_step`, then writes pose observations through `ObservationWriter`. The observation spine stores compact pose summaries; the typed row stores full COCO17 keypoint evidence.

## Lineage Decisions

Source `player_detection` observations link to pose observations with `pose_from_subject_detection_candidate`. Candidate tracklet and track point context link with `subject_context_candidate` and `pose_from_track_point_candidate`. Invalid explicit source ids fail clearly.

## Source Association Decisions

Full-frame fixture poses remain unassociated. Source-detection-linked fixture poses copy source frame/time and carry candidate association fields without proving identity.

## CLI/Service Decisions

Added `python -m apps.worker.cli run-pose-adapter` for fixture pose persistence. The command supports unassociated full-frame fixture mode and source detection linked mode through `--source-detection-run-id` plus `--link-source-detections`.

## Tests Run

- `.venv/bin/python -m pytest tests/test_pose_persistence_lineage.py -q`
- `.venv/bin/python -m pytest tests/test_pose_schema.py tests/test_pose_observation_persistence.py tests/test_pose_normalization.py tests/test_pose_persistence_lineage.py -q`
- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `.venv/bin/python -m apps.worker.cli run-pose-adapter --help`
- `make -n run-pose MEDIA_ID=media-1 SOURCE_DETECTION_RUN_ID=run-1 LINK_SOURCE_DETECTIONS=true`

## Validation Results

Full repository validation passed in the base environment:

- `141 passed`
- Ruff passed
- web lint/build passed
- web audit found 0 vulnerabilities
- Alembic upgraded through head on SQLite
- synthetic viewer smoke returned `ok = true`

## Known Limitations

- No real pose inference.
- No pose overlay viewer.
- No pose-specific API evidence bundle yet; existing observation detail/query paths expose the persisted pose rows.
- Tracklet/track point pose context lineage is supported by service-level frame results and tests, but not yet driven by a local fixture CLI mode.

## Non-Goals Preserved

No movement interpretation, tennis-event inference, serve/hit/split-step/biomechanics analysis, homography, bounce, hit, rally, point, score, or adjudication was added.

## Recommended Next Handoff

Milestone 4D - Pose Overlay Viewer.
