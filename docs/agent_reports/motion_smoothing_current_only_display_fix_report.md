# Motion Smoothing Replay Current-Only Display Fix Report

## Summary

Repaired the smoothed motion replay display policy so default replay shows current candidates instead
of all smoothed candidates in the active hold window.

## Root Cause

The smoothed overlay helpers treated every candidate within the replay hold window as active. That
made a single replay frame show several nearby `SMOOTH BALL`, `SMOOTH NEAR`, and `SMOOTH FAR`
items. The behavior is useful for debug trail modes, but it was wrong for the default smoothed replay
view.

## Files Modified

- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/components/ReplaySmoothedMotionOverlay.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `docs/REPLAY_WORKSTATION.md`
- `docs/motion/motion_smoothing_stable_replay_candidates_v0.md`
- `docs/IMPLEMENTATION_LOG.md`
- `tests/test_tom_v1_bridge_helpers.py`

## Current-Only Selection Behavior

- Smoothed ball: selects exactly one nearest current candidate.
- Smoothed player boxes: selects at most one candidate per near/far track role.
- Smoothed pose: selects at most one candidate per track candidate or role.
- Tie-breaking prefers exact current frame, nearest timestamp, higher confidence, then deterministic
  observation id ordering.

## Display Modes

The workstation now exposes one shared smoothed motion display mode:

- `Current only`
- `Short trail`
- `Full trail`

`Current only` is the default whenever a `motionSmoothingRunId` is selected. Short/full trail modes
remain available for intentional debug review, with labels de-cluttered around the current candidate.

## Non-Goals Preserved

No bounce/hit/in-out, rally/point/score, player identity, scoreboard OCR, server/receiver logic,
court-space projection, accepted/rejected lifecycle, or adjudication was added. Raw and smoothed
candidate observations remain immutable evidence.

## Validation Results

- `.venv/bin/python -m pytest -q` passed: 269 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed against `tmp_tom_v3_motion_smoothing_display_fix_fixture.db`.
- Completion audit passed against `tmp_tom_v3_motion_smoothing_display_fix_fixture.db`.

## Visual Smoke Result

Loaded the local bridge replay through `next start` on port 3001 and FastAPI on port 8001 using
motion smoothing run `d6e23e3d-daee-4c12-aa11-2d17eee15b58`.

The smoothed motion control reported `current_only`. At the loaded replay frame the DOM contained:

- smoothed ball markers: 0
- smoothed player boxes: 1
- smoothed poses: 1
- smoothed box labels: `SMOOTH NEAR`

That confirms the default display no longer renders several neighboring smoothed candidates as a
stacked trail in the current view.

## Push Status

Branch `codex/motion-smoothing-replay-current-only-fix` and tag
`tom-v3-motion-smoothing-current-only-display-fix` pushed to origin.
