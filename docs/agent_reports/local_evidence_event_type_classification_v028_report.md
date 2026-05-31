# Local-Evidence Event-Type Classification v0.2.8 Report

## Summary

Implemented a local-evidence classifier for image-space direction-change event candidates. Sequence
metadata is now explicitly weak diagnostic context and does not require hit/bounce alternation.

## Changes

- Added `local_evidence_event_type` payloads for image-space direction-change candidates.
- Added `local_evidence_direction_change_bounce_candidate_v028` for direction-change candidates
  reclassified to `bounce_candidate`.
- Updated final event candidate classification priority to
  `local_evidence_event_type_classification`.
- Updated replay API, timeline payloads, TypeScript types, and selected evidence details to expose
  local evidence classification.
- Added tests for no-bounce-required hits, hit-after-hit sequencing, landing-zone reclassification,
  and replay payload exposure.

## Local Smoke

Source runs:

- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

New run:

- `event_candidate_run_id`: `2a5f4dc8-91fd-481c-91d1-c1f5ee5c3a17`

Counts:

- old v0.2.7 baseline: 5 hit, 2 bounce, 870 diagnostics
- new v0.2.8 smoke: 7 hit, 2 bounce, 868 diagnostics
- direction-change classified: 2
- direction-change kept as hit: 1
- direction-change reclassified to bounce: 1

## Notes

The remaining bottom-right player-anchored marker stayed a `hit_candidate` because its local
payload has strong near-player contact-zone support; it was not a bounce-like image-space
direction-change candidate. The repair now exposes enough local evidence and rejection diagnostics
to review that case without relying on a hard sequence rule.

## Validation

Validation runs:

```bash
.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q
.venv/bin/python -m pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_local_evidence_event_type_fixture.db make demo PYTHON=.venv/bin/python MAX_FRAMES=3
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_local_evidence_event_type_fixture.db make completion-audit PYTHON=.venv/bin/python
```

Result:

```text
hit/bounce service tests: 38 passed
full pytest: 318 passed
ruff: passed
web lint/build/audit: passed, 0 vulnerabilities
fixture demo/audit: passed
```

## Boundaries

This repair remains candidate-only. It does not add hit truth, bounce truth, in/out, score,
rally/point logic, player identity, accepted/rejected lifecycle, or adjudication.
