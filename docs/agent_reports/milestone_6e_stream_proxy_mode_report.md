# Milestone 6E - Stream Proxy Mode Agent Report

## Summary

Milestone 6E adds Stream Proxy Mode to the replay workstation. The mode makes an indexed local video behave like a live-like source: playback starts at zero, the available evidence edge advances with playback, future overlays and timeline items stay hidden, and the operator can pause/review or return to the current live-like edge.

## Files Created

- `docs/milestones/milestone_6e_stream_proxy_mode.md`
- `docs/handoffs/milestone_6e_stream_proxy_mode_handoff.md`
- `docs/agent_reports/milestone_6e_stream_proxy_mode_report.md`

## Files Modified

- `Makefile`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/components/ReplayVideoPlayer.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/replayTimeline.ts`
- `apps/web/src/lib/types.ts`
- docs and control-room files listed in the final validation summary

## Stream Proxy Decisions

Stream Proxy Mode is implemented as frontend operator behavior over existing replay APIs. The backend still returns persisted replay information, overlay chunks, and timeline lanes. The UI filters evidence by the current live-like edge instead of introducing stream session state.

## Future Evidence Decisions

Future detections, poses, and annotations are hidden until their media timestamp is available. Tracklet candidates are visible only from their persisted start time, and their displayed span/points are clipped to the live-like edge so the UI does not reveal future path evidence.

## Operator Review Decisions

Native video seeking is clamped to the current live-like edge in Stream Proxy Mode. The operator can review earlier media time, see a lag indicator, and use Return to live edge to jump back to the latest available proxy time.

## Tests Run

- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db .venv/bin/alembic upgrade head`
- `.venv/bin/python scripts/smoke_synthetic_viewer_data.py`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6e.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6e.db make completion-audit PYTHON=.venv/bin/python`
- Browser smoke of `/replay/<media_id>?mode=stream_proxy&detectionRunId=<id>&trackletRunId=<id>&poseRunId=<id>`

## Validation Results

- Python tests: 180 passed.
- Ruff: passed.
- Web TypeScript lint: passed.
- Web production build: passed.
- Web audit: 0 vulnerabilities.
- Alembic smoke: passed.
- Synthetic viewer smoke: passed.
- Demo smoke: passed using `demo_assets/sample_point.mp4`.
- Completion audit: passed with `observation_only=true` and `no_adjudication=true`.
- Browser smoke: passed; Stream Proxy Mode loaded, showed live-edge UI, rendered initial available overlays, and hid future timeline evidence with available/future counts.

## Known Limitations

- Stream Proxy Mode is not real stream ingestion.
- The live-like edge advances only through local video playback.
- There is no backend stream session, websocket update feed, model scheduler, or capture infrastructure.
- There is no dedicated frontend unit-test runner; frontend coverage is through TypeScript build and browser smoke.

## Non-Goals Preserved

- No real pose inference.
- No movement interpretation.
- No stroke, serve, hit, bounce, rally, point, scoring, or homography logic.
- No live stream ingestion or production streaming protocol support.
- No adjudication or official tennis result layer.

## Push Status

Branch `codex/m6e-stream-proxy-mode` and tag `tom-v3-m6e-stream-proxy-mode` were pushed to origin after validation.

## Recommended Next Handoff

Milestone 6F - Operator Review Workflow Hardening.
