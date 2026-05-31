# Event Candidate Review Panel v0 Report

## Summary

Implemented a compact Event Candidate Review panel in replay. The panel lists final visible
hit/bounce markers from `marker_summary` in chronological order and lets operators click a row to
seek/select that marker. The existing Replay Marker Inspector then shows the selected marker's
compact evidence.

## UI Behavior

- Added `ReplayEventCandidateReviewPanel`.
- Rows show marker number, type, frame/time, source method, confidence, and arbitration decision.
- Row clicks reuse the existing event-candidate timeline selection path when available.
- Selected rows are visually highlighted.
- Empty state explains that an `eventCandidateRunId` is needed.
- Candidate-only warnings remain visible in the review workflow.

## Boundary

This milestone does not change hit/bounce generation, trajectory generation, marker-level
arbitration, persisted source observations, truth status, in/out, score, player identity,
accepted/rejected lifecycle, or adjudication.

## Validation

Implemented and ran validation:

- `.venv/bin/python -m pytest -q`: passed, 326 tests
- `ruff check .`: passed
- `git diff --check`: passed
- `cd apps/web && npm run lint`: passed
- `cd apps/web && npm run build`: passed
- `cd apps/web && npm audit --omit=dev`: passed, 0 vulnerabilities
- fixture `make demo`: passed
- fixture `make completion-audit`: passed

Local bridge smoke produced event candidate run `06d51d3e-dde5-45cc-821a-ba2260f3ddcb`
with 6 final visible markers: 3 `hit_candidate` and 3 `bounce_candidate` rows.

Browser DOM smoke confirmed the replay renders:

- Event Candidate Review panel
- 6 review rows
- 6 video marker controls
- row click selection for the first `HIT CANDIDATE`
- one highlighted selected row
- Replay Marker Inspector updated with the selected marker evidence
