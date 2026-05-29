# Operator View Default Layer Presets v0 Report

## Summary

Implemented replay layer presets so full replay URLs default to a clean operator view while keeping a
manual debug/audit preset and all individual layer toggles available.

## Files Created

- `docs/replay/operator_view_default_layer_presets_v0.md`
- `docs/agent_reports/operator_view_default_layer_presets_v0_report.md`

## Files Modified

- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/projection/object_to_court_projection_candidates_v0.md`
- `tests/test_tom_v1_bridge_helpers.py`

## Preset Implementation

Added `ReplayLayerPreset = "operator" | "debug"`, `viewPreset` URL parsing, and a deterministic
`applyLayerPreset(...)` helper. Operator is the default. Debug is selected with `viewPreset=debug`.

## Default Operator Behavior

Operator view turns on stable candidate layers when their runs exist: smoothed ball/player/pose,
mapped court keypoints, court lines, court carry-forward, and court projection mini-map. It keeps raw
TOM v1 court keypoints, homography overlays, projection diagnostics, camera/view evidence, raw
pose, raw detections, and raw tracklet trails off by default when the stable candidate layer is
available.

## Debug Behavior

Debug / audit view enables raw evidence and geometry debug layers when their runs exist, including
raw detections, tracklets/trails, raw pose, main-player tracks, raw TOM v1 court keypoints,
homography candidates, projection diagnostics, and camera/view evidence.

## Manual Overrides

Changing the preset applies a known layer configuration. After that, individual layer toggles remain
manual controls and do not change persisted evidence.

## Tests Run

- `.venv/bin/python -m pytest tests/test_tom_v1_bridge_helpers.py -q`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- `DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_operator_preset_fixture.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3`
- `TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_operator_preset_fixture.db make completion-audit PYTHON=.venv/bin/python`

## Validation Results

- Focused frontend/helper regression: passed.
- Full Python suite: `275 passed`.
- Ruff: passed.
- Web lint: passed.
- Web build: passed.
- Web production dependency audit: passed, `0 vulnerabilities`.
- Fixture demo smoke: passed.
- Fixture completion audit: passed.

## Visual Smoke Result

Local replay smoke used the clutter-prone URL with `motionSmoothingRunId`, `courtRunId`,
`homographyRunId`, and `courtProjectionRunId`.

Default/operator result:

- preset = `operator`
- raw TOM v1 court keypoints off
- mapped TOM v3 court keypoints on
- court lines on
- homography candidates off
- projection diagnostics off
- smoothed ball/player/pose on
- smoothed display = `current_only`
- pose visual style = `limbs_only`
- court projection mini-map on
- no missing-timeline warning

Debug result with `viewPreset=debug`:

- preset = `debug`
- raw TOM v1 court keypoints on
- mapped court keypoints on
- court lines on
- homography candidates on
- smoothed layers and mini-map still available
- no missing-timeline warning

## Remaining Limitations

The preset is display policy only. It does not infer operator intent beyond the selected preset and
it does not save user-specific preferences.

## Non-Goals Preserved

No bounce, hit, in/out, rally, point, score, player identity, scoreboard OCR, server/receiver logic,
accepted/rejected lifecycle, or adjudication was added.

## Push Status

Pending at report authoring. The final handoff response records the pushed branch and tag status.

## Recommended Next Step

Ball Trajectory Court Candidate v0, followed by Hit/Bounce Candidate Evidence v0.
