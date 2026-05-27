# Milestone 8E Agent Report - Court Overlay in Replay Workstation

## Summary

Milestone 8E renders persisted court geometry evidence in the replay workstation. Court keypoint, court line, camera/view, and homography candidate evidence can now be fetched through replay payloads, shown on the video/timeline, and inspected through selected evidence detail.

## Files Created

- `apps/web/src/components/ReplayCourtOverlay.tsx`
- `docs/court/court_replay_overlay_v0.md`
- `docs/milestones/milestone_8e_court_overlay_replay_workstation.md`
- `docs/handoffs/milestone_8e_court_overlay_replay_workstation_handoff.md`
- `docs/agent_reports/milestone_8e_court_overlay_replay_workstation_report.md`

## Files Modified

- Replay API service/router, replay tests, frontend replay types/API/helpers/workstation/timeline/styles, and Blueprint 8 docs/status/runbook pages.

## Replay Overlay API Decisions

`/replay/overlays` now accepts `court_run_id` and `homography_run_id` while preserving the existing detection, tracklet, and pose filters. Court payloads are additive: `court_keypoints`, `court_lines`, `camera_view`, and `homography_candidates`.

## Court Overlay Rendering Decisions

Court keypoints and court lines render from persisted image-pixel coordinates. Camera/view evidence renders as an inspectable badge and timeline lane. Homography candidate geometry renders by projecting normalized court template geometry through the stored inverse matrix when available.

## Homography Display-Only Projection Decisions

The frontend projection is display-only and writes no observations. It does not create projection diagnostics and does not project ball/player detections into court space.

## Layer Toggle / Detail Decisions

The workstation adds independent court keypoint, court line, camera/view, and homography candidate toggles plus run selectors. Selected detail panels use candidate/evidence-only wording and avoid court truth, in/out, bounce, point, or score language.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8e_fixture_demo.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8e_fixture_demo.db make completion-audit PYTHON=.venv/bin/python`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8e_fixture_demo.db .venv/bin/python -m apps.worker.cli run-fixture-court --media-id <media_id> --frame-sample-rate 30 --max-frames 30`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8e_fixture_demo.db .venv/bin/python -m apps.worker.cli build-homography-candidates --media-id <media_id> --court-run-id <court_run_id>`
- Browser/manual replay smoke at `/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>`

## Validation Results

- Python tests: passed, 235 tests.
- Ruff: passed.
- Web lint/typecheck: passed.
- Web production build: passed.
- NPM audit: passed, 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Fixture demo: passed.
- Completion audit: passed.
- Court fixture smoke: passed with court keypoint, court line, and camera/view observations.
- Homography candidate smoke: passed with candidate rows and source counts.
- Browser/manual replay smoke: passed; court keypoints, court lines, camera/view evidence, homography candidate overlay, timeline lanes, layer toggles, and selected homography detail were visible and evidence-only.

## Known Limitations

- Court evidence is fixture-generated unless future real court adapters are added.
- Homography candidate rendering depends on candidate matrix quality.
- No projection diagnostics exist yet.
- No ball/player court-space projection exists.

## Non-Goals Preserved

- No projection diagnostics.
- No real court model inference.
- No ball/player court projection.
- No bounce/hit/in-out/rally/point/scoring.
- No adjudication.

## Push Status

Commit prepared on `codex/m8e-court-overlay-replay-workstation`; final branch and tag push status is reported in the handoff response.

## Recommended Next Handoff

Milestone 8F - Projection Diagnostics / Review Export
