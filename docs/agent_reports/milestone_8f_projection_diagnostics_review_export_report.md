# Milestone 8F Agent Report - Projection Diagnostics / Review Export

## Summary

Milestone 8F adds projection diagnostic persistence and court review export support for Blueprint 8. TOM can now build `projection_diagnostic_observation` rows from homography candidate runs, preserve lineage from homography candidates to diagnostics, expose diagnostics through replay payloads/timeline/detail surfaces, and export a TOM-native court review dataset.

## Files Created

- `apps/worker/services/projection_diagnostic_builder.py`
- `apps/worker/services/court_review_export.py`
- `docs/court/projection_diagnostics_v0.md`
- `docs/court/court_review_export_v0.md`
- `docs/milestones/milestone_8f_projection_diagnostics_review_export.md`
- `docs/handoffs/milestone_8f_projection_diagnostics_review_export_handoff.md`
- `docs/agent_reports/milestone_8f_projection_diagnostics_review_export_report.md`
- `tests/test_projection_diagnostic_builder.py`

## Files Modified

- Worker CLI, Makefile, export schemas, replay API/router, replay tests, frontend replay types/API/helpers/workstation/timeline/court overlay/styles, and Blueprint 8 docs/status/runbook pages.

## Projection Diagnostic Builder Decisions

The builder reads persisted `homography_candidate_observation` rows and writes `projection_diagnostic_observation` rows through `ObservationWriter`. It creates dedicated model registry, runtime config, processing run, and processing step rows, and keeps diagnostic metadata explicitly observation-only, geometry-only, and not ball/player projection.

## Projection Method Decisions

For candidates with `matrix_direction = image_pixels_to_court_template_2d`, diagnostics use the stored inverse matrix to project normalized court template keypoints and lines back into image pixels. If only a template-to-image matrix is present, the builder uses that matrix directly. Missing usable matrices produce `insufficient_homography` diagnostic rows instead of crashing the whole run.

## Lineage Decisions

Each projection diagnostic links to its source homography candidate with `projection_diagnostic_for_homography_candidate`. No ball/player observations, tracklets, or pose observations are diagnostic parents.

## Review Export Decisions

`export-court-review-dataset` writes `court_review_dataset_v0` JSON under `.data/exports/court`, persists a `court_review_dataset_export` evidence artifact, and records query result memory. The export includes selected court keypoints, court lines, camera/view observations, homography candidates, projection diagnostics, lineage, artifacts, annotations, and evidence-only warnings.

## Replay Payload / Rendering Decisions

Replay overlays and timelines accept `projection_diagnostic_run_id`. The frontend accepts `projectionDiagnosticRunId`, includes projection diagnostic run summaries, renders projected template geometry from persisted diagnostic rows, and keeps labels as projection diagnostic evidence rather than final court geometry.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_fixture_demo.db make completion-audit PYTHON=.venv/bin/python`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_fixture_demo.db .venv/bin/python -m apps.worker.cli run-fixture-court --media-id dfc5ceed-250b-40e4-8873-120e4c499049 --frame-sample-rate 30 --max-frames 30`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_fixture_demo.db .venv/bin/python -m apps.worker.cli build-homography-candidates --media-id dfc5ceed-250b-40e4-8873-120e4c499049 --court-run-id 21e96e07-916a-48d6-85da-96c9991c34ab`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_fixture_demo.db .venv/bin/python -m apps.worker.cli build-projection-diagnostics --media-id dfc5ceed-250b-40e4-8873-120e4c499049 --homography-run-id ed593bf4-4c04-4351-b20b-eee58979901d`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_fixture_demo.db .venv/bin/python -m apps.worker.cli export-court-review-dataset --media-id dfc5ceed-250b-40e4-8873-120e4c499049 --court-run-id 21e96e07-916a-48d6-85da-96c9991c34ab --homography-run-id ed593bf4-4c04-4351-b20b-eee58979901d --projection-diagnostic-run-id 92fbbc77-0e9f-4e82-a6f7-e15caad72f48`
- `.venv/bin/python -m apps.worker.cli build-projection-diagnostics --media-id media-plan --homography-run-id homography-run-plan --plan-only`
- Browser replay smoke at `/replay/dfc5ceed-250b-40e4-8873-120e4c499049?courtRunId=21e96e07-916a-48d6-85da-96c9991c34ab&homographyRunId=ed593bf4-4c04-4351-b20b-eee58979901d&projectionDiagnosticRunId=92fbbc77-0e9f-4e82-a6f7-e15caad72f48`

## Validation Results

- Python tests: passed, 242 tests.
- Ruff: passed.
- Web lint/typecheck: passed after `next build` refreshed generated `.next/types` files.
- Web production build: passed.
- NPM audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo: passed.
- Completion audit: passed.
- Court fixture smoke: passed with 8 court keypoint, 8 court line, and 8 camera/view observations.
- Homography candidate smoke: passed with 8 candidate rows.
- Projection diagnostic smoke: passed with 8 diagnostic candidate rows.
- Court review export smoke: passed with 40 selected court observations and a persisted export artifact.
- Browser replay smoke: passed; replay page loaded with court keypoint, court line, camera/view, homography, and projection diagnostic evidence present.

## Known Limitations

- Court evidence remains fixture-generated unless a future real court adapter is added.
- Projection diagnostics compare projected template geometry for review; they are not final court model decisions.
- Diagnostic metrics are intentionally simple in v0.
- No ball/player court-space projection exists.

## Non-Goals Preserved

- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/scoring.
- No accepted/rejected court lifecycle.
- No real court model inference.
- No adjudication.

## Push Status

Commit prepared on `codex/m8f-projection-diagnostics-review-export`; final branch and tag push status is reported in the handoff response.

## Recommended Next Handoff

Milestone 8G - Blueprint 8 Completion Review
