# Milestone 0D Agent Report - Visual Evidence Viewer Foundation

## Summary

Status: complete.

Milestone 0D implemented the first visual evidence viewer foundation for TOM v3 Simple. The viewer loads persisted run data through backend/API contracts and renders synthetic evidence without adding real ML or a frontend-only evidence model.

## Files Created

- `apps/api/routers/viewer.py`
- `apps/web/next-env.d.ts`
- `apps/web/next.config.mjs`
- `apps/web/package-lock.json`
- `apps/web/package.json`
- `apps/web/tsconfig.json`
- `apps/web/src/app/globals.css`
- `apps/web/src/app/layout.tsx`
- `apps/web/src/app/page.tsx`
- `apps/web/src/app/runs/[runId]/page.tsx`
- `apps/web/src/components/AnnotationPanel.tsx`
- `apps/web/src/components/ArtifactPanel.tsx`
- `apps/web/src/components/CandidateMarkers.tsx`
- `apps/web/src/components/EvidenceViewer.tsx`
- `apps/web/src/components/LineagePanel.tsx`
- `apps/web/src/components/ObservationDetailPanel.tsx`
- `apps/web/src/components/ObservationList.tsx`
- `apps/web/src/components/RunLauncher.tsx`
- `apps/web/src/components/Timeline.tsx`
- `apps/web/src/components/TimelineBand.tsx`
- `apps/web/src/components/TrackCoverageRows.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/timeline.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/viewerData.ts`
- `tests/test_viewer_api.py`
- `docs/milestones/milestone_0d_visual_evidence_viewer_foundation.md`
- `docs/handoffs/milestone_0d_visual_evidence_viewer_foundation_handoff.md`
- `docs/agent_reports/milestone_0d_visual_evidence_viewer_foundation_report.md`
- `docs/web/visual_evidence_viewer_v0.md`

## Files Modified

- `.gitignore`
- `README.md`
- `apps/api/main.py`
- `apps/web/README.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/api/backend_api_v0.md`
- `docs/milestones/milestone_0_observation_store_visual_foundation.md`

## Frontend Decisions

- The web app uses Next.js and React under `apps/web`.
- `npm run lint` runs TypeScript checks.
- `npm run build` runs a production Next.js build.
- The app renders an operational evidence workspace rather than a landing page.
- The annotation panel is present but read-only in v0.

## API/Data-Loading Decisions

- Added `GET /viewer/runs/{run_id}` as a thin read model over existing persisted rows.
- The endpoint returns run, media, steps, observations, tracklets/points, lineage, artifacts, and annotations.
- The viewer page fetches this endpoint by run id.
- Track coverage rows are built from persisted tracklet metadata.
- Candidate markers are built from persisted derived observations.

## Timeline/Rendering Decisions

- Timeline range is computed from evidence frames with padding.
- Gameplay bands render from typed gameplay observations.
- Ball and player coverage rows render from tracklet `coverage_segments`.
- Homography availability renders from `homography_placeholder` observations.
- Candidate markers are clickable and update detail, lineage, and artifact panels.
- Missingness and low-confidence regions are visible timeline states.

## Known Limitations

- No actual video playback yet.
- No artifact files are generated; placeholder artifact URIs are displayed as metadata.
- Annotation creation is not wired in the web UI yet.
- No dedicated frontend unit test or E2E harness is configured.
- The viewer is optimized around the baseline synthetic scenario shape.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `.venv/bin/ruff check .`
- `apps/web: npm run lint`
- `apps/web: npm run build`
- `apps/web: npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db .venv/bin/python -m apps.worker.cli seed-synthetic-run --scenario baseline-tennis-clip --source-uri file:///dev/synthetic-tennis-clip.mp4 --run-name synthetic-baseline-run`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_viewer_seed.db .venv/bin/python -m apps.worker.cli verify-synthetic-run --run-id 9f83bcab-483a-4f13-b1e5-3b917379885a`
- Browser check at `http://127.0.0.1:3010/runs/9f83bcab-483a-4f13-b1e5-3b917379885a`
- `find docs -maxdepth 3 -type f | sort`
- `git status --short`

## Validation Results

- Pytest passed: 8 tests.
- Ruff passed.
- TypeScript lint passed.
- Next.js production build passed.
- `npm audit --omit=dev` found 0 vulnerabilities.
- Alembic upgrade smoke test passed against SQLite.
- Worker CLI seed and verify smoke test passed; verifier returned `ok: true`.
- Browser check confirmed required viewer rows and candidate marker buttons, and selecting the tracking-gap marker updated the detail panel.

## Non-goals Preserved

- No YOLO integration was added.
- No TOM v1 integration was added.
- No real video processing was added.
- No real tracking implementation was added.
- No real homography calculation was added.
- No real bounce detection was added.
- No production auth was added.
- No deployment work was added.
- No adjudication system was added.

## Recommended Next Handoff

Milestone 0E - Integration / QA / Repo Consolidation.
