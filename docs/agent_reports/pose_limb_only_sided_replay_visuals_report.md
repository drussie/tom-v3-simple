# Pose Limb-Only Sided Replay Visuals Report

## Summary

Changed replay pose visualization for raw and smoothed pose overlays to default to limb-only
rendering. Joint markers are still available through an explicit debug style.

## Files Modified

- `apps/web/src/components/ReplayPoseOverlay.tsx`
- `apps/web/src/components/ReplaySmoothedMotionOverlay.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/app/globals.css`
- `docs/REPLAY_WORKSTATION.md`
- `docs/IMPLEMENTATION_LOG.md`
- `tests/test_tom_v1_bridge_helpers.py`

## Visual Style Implementation

Added `ReplayPoseVisualStyle`:

- `limbs_only`
- `limbs_and_joints`
- `joints_only`

`limbs_only` is the default. The workstation exposes this as `Pose visual style`.

## Raw Pose Behavior

Raw replay pose overlays render limb lines by default and hide joint dots. Debug modes can restore
joint markers without changing persisted pose observations.

## Smoothed Pose Behavior

Smoothed pose overlays use the same visual style setting as raw pose overlays. Smoothed replay can
therefore remain clean by default while still allowing keypoint marker audit when needed.

## Left / Right Styling

Pose edges where both endpoints are `left_*` render as left-side limbs. Edges where both endpoints
are `right_*` render as right-side limbs. Cross-body, torso-center, and head edges render as neutral.

## Non-Goals Preserved

No forehand/backhand classification, stroke detection, hit detection, bounce detection, in/out,
score, player identity, biomechanics truth, accepted/rejected lifecycle, or adjudication was added.
This is replay visualization only.

## Validation Results

- `.venv/bin/python -m pytest -q` passed: 269 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed against `tmp_tom_v3_pose_visuals_fixture.db`.
- Completion audit passed against `tmp_tom_v3_pose_visuals_fixture.db`.

## Visual Smoke Result

Loaded the local replay through `next start` on port 3001 and FastAPI on port 8001 with
`motionSmoothingRunId=d6e23e3d-daee-4c12-aa11-2d17eee15b58`.

Default state:

- `Pose visual style`: `limbs_only`
- smoothed pose lines: 16
- smoothed pose circles: 0
- left-side limb classes: 6
- right-side limb classes: 6
- neutral limb classes: 4

After switching to `Limbs + joints`, smoothed pose circles appeared again, confirming debug joint
markers remain available.

## Push Status

Branch `codex/pose-limb-only-sided-visuals` and tag
`tom-v3-pose-limb-only-sided-replay-visuals` pushed to origin.
