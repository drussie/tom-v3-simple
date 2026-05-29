# Event Candidate Video Overlay v0.1 Report

## Summary

Added broadcast-video markers for existing `hit_candidate` and `bounce_candidate` replay evidence.
The repair resolves event candidate image positions from each candidate's source
`ball_court_projection_candidate` and renders labeled video overlay markers in addition to the
existing court mini-map and timeline surfaces.

## Files Created

- `apps/web/src/components/ReplayEventCandidateVideoOverlay.tsx`
- `docs/events/event_candidate_video_overlay_v01.md`
- `docs/agent_reports/event_candidate_video_overlay_v01_report.md`

## Files Modified

- `apps/api/services/replay.py`
- `apps/web/src/app/globals.css`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `tests/test_hit_bounce_candidates.py`
- `tests/test_tom_v1_bridge_helpers.py`
- `docs/REPLAY_WORKSTATION.md`
- `docs/RUNBOOK_LOCAL.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/events/hit_bounce_candidate_evidence_v0.md`

## Image Point Resolution

Replay resolves video marker coordinates through:

```text
event candidate payload.source_ball_court_projection_observation_id
-> source ball_court_projection_candidate.payload.image_point
```

Resolved payloads use `image_marker_source = source_ball_court_projection_image_point`.
If an image point is missing, the API returns `image_point = null` and
`image_marker_source = unavailable` without failing.

## Video Overlay Behavior

`ReplayEventCandidateVideoOverlay` draws event candidate markers over the broadcast video:

- `HIT CANDIDATE` uses a triangle marker.
- `BOUNCE CANDIDATE` uses a ring marker.
- Both include short crosshair ticks and selectable labels.
- Labels always include `CANDIDATE`.

The existing `Show hit/bounce event candidates` layer toggle controls the video markers, mini-map
markers, and timeline lane.

## Mini-Map Behavior

The court projection mini-map is preserved. It continues to render event candidates in normalized
court-template space while the new video overlay renders image-space markers.

## Tests Run

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py tests/test_tom_v1_bridge_helpers.py -q`
- `.venv/bin/python -m pytest tests/test_replay_api.py -q`
- `.venv/bin/python -m pytest -q`
- `ruff check .`
- `cd apps/web && npm run lint`
- `cd apps/web && npm run build`
- `cd apps/web && npm audit --omit=dev`
- fixture demo smoke
- fixture completion audit smoke

## Validation Results

- Focused event/helper tests: 9 passed.
- Replay API tests: 32 passed.
- Full Python tests: 287 passed.
- Ruff: passed.
- Web lint/build/audit: passed, 0 npm vulnerabilities.
- Fixture demo/audit: passed.

## Local Visual Smoke Result

Using `event_candidate_run_id = 1917963a-e82d-4486-9af2-8cd3b6aa3709`, the Next replay proxy
returned a `bounce_candidate` payload with:

- `image_point = { "x": 787.143005, "y": 755.09375 }`
- `image_marker_source = source_ball_court_projection_image_point`

Browser smoke confirmed:

- one broadcast-video `BOUNCE CANDIDATE` marker was rendered
- selecting the marker opened the selected evidence panel
- selected evidence displayed the image point, marker source, and no-truth warnings

## Known Limitations

- The video marker depends on the source ball court projection preserving `image_point`.
- There is no inverse-homography fallback in v0.1.
- Markers appear near candidate timestamps; they are not persistent truth pins.

## Non-Goals Preserved

- No hit truth.
- No bounce truth.
- No in/out.
- No rally, point, or score.
- No identity, OCR, or server/receiver logic.
- No accepted/rejected lifecycle or adjudication.
