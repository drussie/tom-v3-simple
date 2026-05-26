# Milestone 2D Agent Report - Tracklet Evidence Export / Review Dataset Foundation

## Summary

Status: complete.

Milestone 2D adds a review dataset export foundation for candidate tracklet evidence. Exports can be selected by explicit tracklet ids or by structured tracklet query filters, then written as local JSON artifacts with persisted `evidence_artifact` metadata and optional `query_result` memory.

## Files Created

- `apps/api/services/tracklet_review_export.py`
- `docs/agent_reports/milestone_2d_tracklet_evidence_export_review_dataset_report.md`
- `docs/handoffs/milestone_2d_tracklet_evidence_export_review_dataset_handoff.md`
- `docs/milestones/milestone_2d_tracklet_evidence_export_review_dataset.md`
- `docs/tracklets/tracklet_review_dataset_export_v0.md`
- `packages/schema/tom_v3_schema/exports.py`
- `tests/test_tracklet_review_export.py`

## Files Modified

- `README.md`
- `apps/api/routers/tracklets.py`
- `apps/worker/cli.py`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/api/backend_api_v0.md`
- `docs/dev/local_demo_runbook.md`
- `docs/tracklets/tracklet_evidence_bundle_v0.md`
- `docs/tracklets/tracklet_query_v0.md`
- `docs/tracklets/tracklet_review_annotations_v0.md`

## Export Format Decisions

- Export format is JSON only for v0.
- The top-level object is `tracklet_review_dataset_export`.
- Exports contain tracklet evidence bundle data rather than a new export-specific evidence model.
- Required warning fields are included in the JSON payload and export artifact metadata.
- Export JSON is written to local filesystem storage and not stored in Postgres.

## Artifact Storage Decisions

- Export files are written under `.data/exports/tracklets/{export_id}/tracklet_review_dataset.json`.
- Each export persists an `evidence_artifact` row with `artifact_type = tracklet_review_dataset_export`.
- The export artifact stores a checksum, export id, tracklet ids, query spec, and warning metadata.
- Current schema requires `evidence_artifact.media_id`, so multi-media exports record `media_scope` and attach to one represented media id.

## Query/Result Decisions

- Query-based exports reuse `query_tracklets`.
- Query-based exports persist a `query_result` row with selected tracklet ids, selected tracklet observation ids, and export artifact metadata.
- Direct tracklet-id exports do not create `query_result` rows.

## Known Limitations

- JSONL is not implemented in v0.
- Export does not copy frame image files; it references existing artifact metadata and URIs.
- API export writes to a server-local path from `output_root`, which is suitable for local/dev use only.
- Multi-media export artifact rows attach to one media id because the current artifact schema requires it.

## Tests Run

- `pytest -q tests/test_tracklet_review_export.py tests/test_tracklet_query_review.py tests/test_tracklet_evidence_bundle.py`
- `pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head`
- `python scripts/smoke_synthetic_viewer_data.py`
- Local evidence path with generated temporary video: `index-media`, `run-detection-adapter`, `extract-frame-artifacts`, `build-tracklets`, annotation insertion, and `export-tracklet-review-dataset --query-json '{"has_annotation":true}'`.

## Validation Results

- Targeted export/query/evidence bundle tests: passed.
- Full test suite: 54 passed.
- Ruff: passed.
- Web lint/build/audit: passed.
- Alembic smoke test: passed.
- Synthetic viewer smoke: passed.
- Local export smoke: passed. Export JSON existed, export artifact metadata was persisted, query result id was returned, and the export carried candidate-only/no-adjudication warning fields.

## Non-Goals Preserved

- No pose detection.
- No court homography.
- No bounce detection.
- No hit detection.
- No rally, point, or scoring logic.
- No real YOLO runtime integration.
- No adjudication.

## Recommended Next Handoff

Milestone 2E - Blueprint 2 Completion Review / Temporal Evidence Hardening.
