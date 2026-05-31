# Replay Marker Inspector v0 Report

## Summary

Implemented a compact replay Marker Inspector for final visible hit/bounce candidate markers. The
inspector uses replay API `marker_summary` rows and selected event marker payloads to show source
method, frame/time, confidence, coordinates, and marker-level arbitration decisions without forcing
operators to inspect terminal JSON.

## API Behavior

- Added replay `marker_summary` to timeline responses.
- Added replay `marker_summary` to event overlay responses.
- Marker rows are sorted by timestamp, frame, candidate type, and observation id.
- Marker rows include final hit/bounce candidates only, not rejection diagnostics.
- Event candidate overlay/timeline payloads now expose original candidate type/method when present.

## UI Behavior

- Added `ReplayMarkerInspector`.
- Empty state invites the operator to click a hit or bounce marker.
- Selected marker state shows marker type, frame/time, source method, confidence, marker
  arbitration decision/reason, image coordinates, court coordinates, and candidate-only warning.
- Full selected evidence diagnostics remain available below the compact inspector.

## Validation

Implemented and ran validation:

- `.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py::test_replay_marker_summary_exposes_compact_final_markers tests/test_hit_bounce_candidates.py::test_event_candidate_replay_payloads_are_exposed -q`: passed
- `.venv/bin/python -m pytest -q`: passed, 326 tests
- `ruff check .`: passed
- `cd apps/web && npm run lint`: passed
- `cd apps/web && npm run build`: passed
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities
- fixture `make demo`: passed
- fixture `make completion-audit`: passed

Local bridge smoke produced event candidate run `64328e05-5f32-44b1-a98f-d7d731dfb150`
with 6 final visible markers: 3 `hit_candidate` and 3 `bounce_candidate` rows. A browser DOM
smoke confirmed the replay renders the Marker Inspector card, 6 video marker controls, and 6
mini-map event marker groups for that run.

## Boundaries

This milestone does not change hit/bounce generation, classification, marker-level arbitration,
persisted source evidence, truth status, in/out, score, player identity, accepted/rejected
lifecycle, or adjudication.
