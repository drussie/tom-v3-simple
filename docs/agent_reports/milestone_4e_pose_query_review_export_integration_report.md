# Milestone 4E Agent Report - Pose Query / Review / Export Integration

## Summary

Milestone 4E makes persisted pose observations searchable, reviewable through the generic annotation path, and exportable as TOM-native review dataset artifacts. Pose review evidence now includes query filters, evidence bundles, keypoint-level annotation metadata, local JSON exports, evidence artifact metadata, and query result memory.

## Files Created

- `apps/api/routers/pose.py`
- `apps/api/services/pose_query.py`
- `apps/api/services/pose_evidence_bundle.py`
- `apps/api/services/pose_review_export.py`
- `tests/test_pose_query_review_export.py`
- `docs/pose/pose_query_review_export_v0.md`
- `docs/milestones/milestone_4e_pose_query_review_export_integration.md`
- `docs/handoffs/milestone_4e_pose_query_review_export_integration_handoff.md`
- `docs/agent_reports/milestone_4e_pose_query_review_export_integration_report.md`

## Files Modified

- `apps/api/main.py`
- `apps/api/services/annotation_review.py`
- `apps/worker/cli.py`
- `packages/schema/tom_v3_schema/pose.py`
- `packages/schema/tom_v3_schema/exports.py`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `README.md`
- `docs/dev/local_demo_runbook.md`
- `docs/pose/pose_observation_schema_v0.md`
- `docs/pose/pose_persistence_lineage_v0.md`
- `docs/web/pose_overlay_viewer_v0.md`
- `docs/blueprints/tom_v3_blueprint_4_pose_observation_movement_evidence_layer.md`

## Query Decisions

Pose query uses a pose-specific service for filters that require typed `pose_observation` fields, including confidence ranges, missing keypoint counts, skeleton format, and source association fields. Annotation label filtering is applied through the existing annotation summary helper.

## Evidence Bundle Decisions

The pose evidence bundle is a service/API composition over existing rows. It includes pose detail, observation spine data, run/model/config summaries, lineage, source detection or tracklet context when present, artifacts, and annotations. It does not add new tables.

## Review Annotation Decisions

Pose review uses the existing `human_annotation` table and generic annotation API. Pose labels are documented and added to the shared label vocabulary. Keypoint-level metadata is stored in annotation payload JSON with `keypoint_name` and `keypoint_index`.

## Export Decisions

The pose review dataset export follows the tracklet export pattern: local JSON file, checksum, `evidence_artifact` row, and optional `query_result` row. The export is TOM-native and preserves keypoints, source context, lineage, artifacts, and annotations.

## Tests Run

- `.venv/bin/pytest tests/test_pose_query_review_export.py -q`
- `.venv/bin/pytest tests/test_pose_schema.py tests/test_pose_observation_persistence.py tests/test_pose_normalization.py tests/test_pose_persistence_lineage.py tests/test_pose_query_review_export.py -q`
- `.venv/bin/pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`

## Validation Results

- Focused pose query/review/export tests passed: `5 passed`.
- Focused Blueprint 4 pose tests passed: `41 passed`.
- Full Python suite passed: `147 passed`.
- Ruff passed.
- Web lint/build passed.
- Web audit found 0 vulnerabilities.
- Alembic upgraded through head on SQLite.
- Synthetic viewer smoke returned `ok = true`.

## Known Limitations

- No pose review UI form was added; the generic API path supports pose annotations, while the current viewer annotation panel remains display-oriented.
- Export format is TOM-native JSON only.
- Query/export pagination is intentionally simple for v0.
- No real pose inference is included.

## Non-Goals Preserved

No movement interpretation, tennis-event inference, serve/hit/split-step/biomechanics analysis, homography, bounce, hit, rally, point, score, or adjudication was added.

## Recommended Next Handoff

Milestone 4F - Blueprint 4 Completion Review / Pose Evidence Hardening.
