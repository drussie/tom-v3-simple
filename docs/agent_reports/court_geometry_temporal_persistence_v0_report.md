# Court Geometry Temporal Persistence v0 Report

## Summary

Implemented replay/read-model temporal persistence for sparse court geometry evidence. Court keypoints, court lines, homography candidates, and projection diagnostics can now be carried forward for a bounded display window so replay overlays remain stable between sampled court observations.

## Files Created

- `docs/court/court_geometry_temporal_persistence_v0.md`
- `docs/agent_reports/court_geometry_temporal_persistence_v0_report.md`

## Files Modified

- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayCourtOverlay.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/app/globals.css`
- `tests/test_replay_api.py`
- `tests/test_tom_v1_bridge_helpers.py`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/court/tom_v1_court_keypoint_visual_calibration_audit_v0.md`
- `docs/court/homography_candidate_persistence_v0.md`
- `docs/court/projection_diagnostics_v0.md`

## Display Policy Decisions

- Used replay/API carry-forward, not new persisted observations.
- Defaulted court geometry temporal persistence to `carry_forward`.
- Added `court_persistence_max_gap_ms`, default `1500`.
- Applied the policy only to court geometry display layers: keypoints, lines, homography candidates, and projection diagnostics.
- Left camera/view evidence as context evidence with its existing time range.

## API / Query Params

- `court_temporal_persistence=off|carry_forward`
- `court_persistence_max_gap_ms=<int>`

## Payload Metadata

Court geometry overlays now include source observation, source frame/time, active display window, carry boundary, and explicit `not_court_truth` / `candidate_geometry_only` fields.

## UI Controls

Replay adds controls for:

- Court geometry temporal persistence
- Court carry-forward max gap

The court overlay displays a carried-forward candidate geometry badge when current active geometry is being displayed away from the source sample.

## Validation Results

- `.venv/bin/python -m pytest -q`: 266 passed.
- `ruff check .`: passed.
- `cd apps/web && npm run lint`: passed.
- `cd apps/web && npm run build`: passed.
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities.
- Fixture demo with `tmp_tom_v3_court_persistence_fixture.db`: passed.
- Completion audit with `tmp_tom_v3_court_persistence_fixture.db`: passed.

## Local Visual Smoke

- API/service smoke on `tmp_tom_v3_tom_v1_bridge.db` confirmed that a request between sampled court frames carries forward the prior court keypoint and line evidence. The carried item reported `active_from_ms=0`, `active_until_ms=1000`, `carried_forward=true`, and `carry_forward_boundary=next_observation_or_max_gap_ms`.
- Next proxy smoke confirmed `courtTemporalPersistence=carry_forward` returned a carried-forward court keypoint through `/api/replay/overlays`.
- Browser smoke confirmed the replay page exposes the court temporal persistence controls and renders raw/mapped court overlays for the existing real court run.
- Screenshot: `.data/artifacts/court-geometry-temporal-persistence-smoke.png`.
- Limitation: the in-app browser runtime did not allow setting video `currentTime` directly during smoke, so the dynamic carried-forward badge was verified through API/proxy metadata rather than browser time seeking.

## Remaining Limitations

- v0 uses max-gap and next-observation boundaries only.
- Camera-cut boundaries are reserved for a future real camera/view classifier or segment layer.
- Carry-forward is a display/read-model behavior only; it does not prove geometry correctness.

## Non-goals Preserved

- No court truth.
- No accepted/rejected court lifecycle.
- No ball/player court-space projection.
- No bounce/hit/in-out/rally/point/score.
- No player identity, scoreboard OCR, server/receiver logic, or adjudication.

## Push Status

Pending final commit, tag, and push.

## Recommended Next Step

Use the stable court overlay to visually review whether remaining geometry errors are from TOM v1 keypoint mapping, preprocessing, crop/letterbox assumptions, or homography fit.
