# Image-Space Direction-Change Hit Recall v0.2.7 Report

Status: implemented

## Summary

Added `image_space_direction_change_hit_candidate_v027`, a full 2D broadcast-image recall pass for
airborne hit-like candidates. The pass uses incoming/anchor/outgoing image vectors and persists
`image_space_direction_change_recall` diagnostics. Player proximity remains optional diagnostic
support (`player_proximity_required = false`).

The repair also keeps the v0.2.4-v0.2.6 false hit-over-bounce protections: weak image-space
direction-change hits immediately before a bounce are suppressed as rejection diagnostics rather
than emitted as final hit markers.

## Local Smoke

Command:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-hit-bounce-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  BALL_TRAJECTORY_RUN_ID=2e16f3d1-e252-497a-b688-d81890645ab7 \
  COURT_PROJECTION_RUN_ID=82498799-490f-44df-9222-0157356c5ff7
```

Result:

- new `event_candidate_run_id`: `9a67e173-dbe5-4644-bc0c-233b46fc2fd5`
- old v0.2.6 profile: 4 `hit_candidate`, 2 `bounce_candidate`
- new v0.2.7 profile: 5 `hit_candidate`, 2 `bounce_candidate`
- image-space direction source points: 75
- image-space direction candidates: 43
- image-space direction final recovered hits: 1
- image-space direction overlap suppressions: 1

The recovered final image-space direction-change hit is at frame 164. The final event list keeps
the existing v0.2.6 hits and bounces, adds the frame 164 direction-change hit, and suppresses the
weak frame 77 pre-bounce direction-change candidate.

## Validation

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q` passed: 36 tests.
- `.venv/bin/python -m pytest -q` passed: 316 tests.
- `ruff check .` passed.
- `cd apps/web && npm run lint` passed.
- `cd apps/web && npm run build` passed.
- `cd apps/web && npm audit --omit=dev` passed with 0 vulnerabilities.
- Fixture demo passed against `tmp_tom_v3_image_space_direction_change_hit_recall_fixture.db`.
- Fixture completion audit passed against `tmp_tom_v3_image_space_direction_change_hit_recall_fixture.db`.

Browser smoke loaded the replay page for
`event_candidate_run_id = 9a67e173-dbe5-4644-bc0c-233b46fc2fd5`. The replay showed 7 event
candidates in the operator view: 5 `HIT CANDIDATE` markers and 2 `BOUNCE CANDIDATE` markers, with
the court projection mini-map still labeled as derived candidate evidence only.

## Remaining Limitations

This recall path is deliberately image-space and heuristic. It improves recall for a visible
airborne direction change, but it is not calibrated 3D ball motion, not hit truth, not bounce truth,
not in/out, and not scoring or adjudication evidence.
