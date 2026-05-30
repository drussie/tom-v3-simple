# Hit/Bounce Side-Zone + Sequence Classification Repair v0.2.2 Report

Status: implemented

Branch: `codex/hit-bounce-side-zone-sequence-repair-v022`

## Summary

This repair adds side-zone, contact-zone, landing-zone, and sequence diagnostics to the
hit/bounce candidate builder. It preserves the v0.2.1 recall target while repairing two visible
classification errors in the sample point.

No hit truth, bounce truth, in/out decision, score, rally/point logic, accepted/rejected lifecycle,
or adjudication was added.

## Candidate Changes

- Added a side-zone sequence pass after candidate generation, dedupe, and hit-over-bounce conflict
  suppression.
- Added `court_side_zone` diagnostics with the `court_y_low_near_high_far_v022` convention.
- Added `player_contact_zone` and `court_landing_zone` diagnostics.
- Added `candidate_reclassification` payloads preserving original candidate type/method.
- Added `candidate_sequence` payloads with expected next candidate type and sequence-prior status.
- Updated event payload classification priority to `side_zone_sequence_candidate_prior`.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `fb997b06-2111-42c3-8708-0ace111a3a73`
- `hit_candidate`: 2
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 29
- `raw_hit_candidate_count`: 3
- `raw_bounce_candidate_count`: 5
- `reclassified_hit_to_bounce_count`: 1
- `reclassified_bounce_to_hit_count`: 1
- `final_hit_candidate_count`: 2
- `final_bounce_candidate_count`: 2
- `sequence_prior_applied_count`: 2
- `physics_heuristic_version`: `v0.2.2`

## Visual Classification Result

The sample point now preserves four visible event candidate markers:

- near-side contact marker: `HIT CANDIDATE`
- far-side landing marker: `BOUNCE CANDIDATE`
- near-side landing marker: `BOUNCE CANDIDATE`
- near-side right contact marker: `HIT CANDIDATE`

These are still candidate markers, not event truth.

## Validation

Focused event-candidate tests:

```text
.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q
16 passed
```

Focused lint:

```text
ruff check apps/worker/services/hit_bounce_candidates.py apps/api/services/replay.py tests/test_hit_bounce_candidates.py
passed
```

Full validation:

```text
.venv/bin/python -m pytest -q
296 passed

ruff check .
passed

cd apps/web && npm run lint
passed

cd apps/web && npm run build
passed

cd apps/web && npm audit --omit=dev
found 0 vulnerabilities
```

Fixture demo/audit:

```text
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

make completion-audit PYTHON=.venv/bin/python
passed
```

Browser smoke with the fresh local replay run confirmed:

- 4 event candidates loaded
- video overlay labels include 2 `HIT CANDIDATE` and 2 `BOUNCE CANDIDATE` markers
- mini-map labels include the same candidate set
- `.replay-media-id` remains nowrap/ellipsis instead of character-wrapping

## Remaining Limitations

The sequence prior is a bounded candidate-review heuristic. It can help classify sparse visual
markers for operator review, but it does not prove contact, bounce, in/out, point outcome, or score.
