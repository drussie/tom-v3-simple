# Object-to-Court Projection Candidates v0 Report

## Summary

Implemented derived candidate projection from smoothed image-space evidence into normalized
`court_template_2d` coordinates using existing homography candidate observations.

## Files Created

- `apps/worker/services/object_court_projection.py`
- `apps/web/src/components/ReplayCourtProjectionMiniMap.tsx`
- `docs/projection/object_to_court_projection_candidates_v0.md`
- `docs/agent_reports/object_to_court_projection_candidates_v0_report.md`
- `tests/test_object_court_projection.py`

## Files Modified

- `Makefile`
- `apps/api/routers/replay.py`
- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayEvidenceTimeline.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/replayOverlays.ts`
- `apps/web/src/lib/replayTimeline.ts`
- `apps/web/src/lib/types.ts`
- `apps/worker/cli.py`
- `packages/schema/tom_v3_schema/enums.py`
- `tests/test_replay_api.py`

## Projection Method

Ball candidates use smoothed ball center points. Main-player candidates use the bottom center of
smoothed main-player bboxes. Both are projected through image-pixels-to-court-template homography
candidates.

## Observation Types Created

- `ball_court_projection_candidate`
- `main_player_court_projection_candidate`

Both are generic observation-spine rows with `observation_family = projection` and
`coordinate_space = court_template_2d`.

## Lineage Implementation

Projection candidates link to source smoothed object observations and source homography candidates.
Relationship types:

- `projected_from_smoothed_ball_position`
- `projected_from_smoothed_main_player_box`
- `projected_with_homography_candidate`

## Replay / Mini-Map Behavior

Replay accepts `courtProjectionRunId`, exposes `ball_court_projection` and
`main_player_court_projection` overlay payloads, adds a `court_projection` timeline lane, and renders
current projection candidates in a normalized court-template mini-map panel.

## Validation Results

Validation passed:

- `.venv/bin/python -m pytest -q` -> 275 passed.
- `ruff check .` -> passed.
- `cd apps/web && npm run lint` -> passed.
- `cd apps/web && npm run build` -> passed.
- `cd apps/web && npm audit --omit=dev` -> 0 vulnerabilities.
- Fixture demo passed against `tmp_tom_v3_object_projection_fixture.db`.
- Completion audit passed against `tmp_tom_v3_object_projection_fixture.db`.

Focused validation also passed:

- `pytest tests/test_object_court_projection.py tests/test_replay_api.py::test_replay_overlay_and_timeline_return_court_projection_candidates -q`.

Local bridge smoke produced:

- `court_projection_run_id = 867f1016-72b1-468a-b40c-1b4b09f7a2f0`
- `ball_court_projection_candidate = 75`
- `main_player_court_projection_candidate = 405`
- skipped missing homography = 0
- skipped invalid projection = 0

Browser smoke opened the replay with `courtProjectionRunId` and confirmed the replay loaded court
projection candidate counts and the normalized mini-map panel without the missing-timeline warning.

## Known Limitations

- Projection uses candidate homography rows and remains sensitive to court keypoint/homography
  quality.
- Main-player projection uses bbox bottom-center as a candidate anchor, not a confirmed foot contact
  point.
- No trajectory grouping is persisted in v0.

## Non-Goals Preserved

No bounce, hit, in/out, rally, point, score, player identity, OCR, accepted/rejected lifecycle, or
adjudication was added.

## Push Status

Pending commit, tag, and push.

## Recommended Next Step

Ball Trajectory Court Candidate v0, followed by Hit/Bounce Candidate Evidence v0.
