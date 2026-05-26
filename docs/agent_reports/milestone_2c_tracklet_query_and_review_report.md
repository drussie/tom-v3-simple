# TOM v3 Simple - Milestone 2C Agent Report

## Summary

Status: complete.

Milestone 2C adds structured tracklet candidate query and a basic review workflow. Candidate tracklets can be filtered through `POST /tracklets/query`, evidence bundles now expose annotation summaries, and the viewer can add review annotations to selected tracklet, track point, or source detection observations.

## Files Created

- `apps/api/services/annotation_review.py`
- `apps/api/services/tracklet_query.py`
- `apps/web/src/app/api/annotations/route.ts`
- `docs/agent_reports/milestone_2c_tracklet_query_and_review_report.md`
- `docs/handoffs/milestone_2c_tracklet_query_and_review_handoff.md`
- `docs/milestones/milestone_2c_tracklet_query_and_review.md`
- `docs/tracklets/tracklet_query_v0.md`
- `docs/tracklets/tracklet_review_annotations_v0.md`
- `docs/web/tracklet_review_viewer_v0.md`
- `packages/schema/tom_v3_schema/tracklets.py`
- `tests/test_tracklet_query_review.py`

## Files Modified

- `README.md`
- `apps/api/routers/tracklets.py`
- `apps/api/services/tracklet_evidence_bundle.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/components/TrackletEvidencePanel.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/api/backend_api_v0.md`
- `docs/dev/local_demo_runbook.md`
- `docs/tracklets/tracklet_evidence_bundle_v0.md`
- `docs/tracklets/tracklet_foundation_v0.md`
- `docs/web/tracklet_evidence_viewer_v0.md`

## Tracklet Query Decisions

- Tracklet query uses structured filters only.
- The endpoint returns dynamic summaries and does not persist saved query results in 2C.
- Metadata-backed filters such as source detection run, gap count, track status, and identity status are evaluated against existing tracklet/observation payloads.

## Review / Annotation Decisions

- Review labels reuse the existing `human_annotation` table.
- Review annotations target observation ids for tracklets, track points, or source detections.
- Annotation labels are documented and surfaced in the viewer without adding an enum migration.

## Viewer Review Decisions

- Review controls live in the Tracklet Evidence panel.
- The viewer posts through a local Next.js proxy route to avoid browser CORS issues.
- After an annotation is saved, the selected evidence bundle refreshes.

## Known Limitations

- No production review queue or reviewer identity system exists.
- Query results are not saved to `query_result`.
- The viewer does not yet provide a dedicated tracklet search page.

## Tests Run

- `.venv/bin/python -m pytest tests/test_tracklet_query_review.py tests/test_tracklet_evidence_bundle.py tests/test_tracklet_builder.py -q`
- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- Local media/detection/frame-artifact/tracklet/query/review smoke path with a generated temporary video.
- Browser validation against `http://127.0.0.1:3000/runs/<tracklet_run_id>`.

## Validation Results

- Focused query/review, evidence bundle, and tracklet tests: 15 passed.
- Full pytest suite: 48 passed.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- npm audit: 0 vulnerabilities.
- Alembic SQLite upgrade smoke test: passed.
- Synthetic viewer smoke script: passed.
- Local evidence path smoke: indexed media, ran fixture detection, extracted 2 frame artifacts, built 3 tracklet candidates, queried a ball candidate by source run/family/point count/gap filters, loaded its evidence bundle, added a `bad_tracklet` annotation, and queried it back by review label.
- Browser validation: passed. The Tracklet Evidence panel displayed review controls, saved a review annotation through the web proxy, refreshed the bundle, and showed the annotation summary.

## Non-Goals Preserved

- No new tracking algorithm was added.
- No pose detection was added.
- No court homography was added.
- No bounce detection was added.
- No hit detection was added.
- No rally or point reconstruction was added.
- No scoring was added.
- No real YOLO runtime integration was added.
- No adjudication was added.

## Recommended Next Handoff

Recommended next milestone: Milestone 2D - Tracklet Evidence Export / Review Dataset Foundation.

Reason: query and review annotations now make candidate tracklets usable for human review. The next useful step is exporting reviewed evidence into a reusable dataset/report shape without adding model certainty.
