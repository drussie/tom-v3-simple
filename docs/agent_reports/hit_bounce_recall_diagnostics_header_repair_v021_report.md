# Hit/Bounce Recall Diagnostics + Header Layout Repair v0.2.1 Report

Status: implemented

Branch: `codex/hit-bounce-recall-diagnostics-header-repair-v021`

## Summary

This repair adds candidate rejection diagnostics, improves far-side hit recall with a bounded
player-proximate speed-change fallback, and repairs the Replay Workstation header layout collapse.

No event truth, in/out, score, rally/point logic, accepted/rejected lifecycle, or adjudication was
added.

## Event Candidate Changes

- Added `event_candidate_rejection_diagnostic` observations.
- Added rejection-reason summaries to processing run metadata and CLI output.
- Increased the default player projection time window to `300ms`.
- Added a bounded fallback hit method:
  `player_proximate_speed_reduction_hit_candidate_fallback_v021`.
- Kept bounce candidates on the image-y vertical proxy plus speed-reduction path, with a clearly
  labeled low-confidence fallback path available for missing/partial image proxy cases.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `0217bd29-f2db-471a-ba50-69a17612027e`
- `hit_candidate`: 2
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 29
- `evaluated_trajectory_points`: 33

The sample-point review target of 2 hit candidates and 2 bounce candidates was achieved.

## Rejection Summary

The local smoke run reported these rejection reasons:

- `deduped_lower_confidence`: 4
- `near_player_so_not_bounce`: 3
- `net_axis_delta_below_threshold`: 6
- `no_descending_to_ascending_proxy`: 12
- `no_net_axis_reversal`: 23
- `no_speed_reduction`: 21
- `player_too_far_for_hit`: 22

## Header Repair

Replay header changes:

- single flexible header column
- compact badge wrapping
- ellipsized `.replay-media-id`
- no character-by-character media-id wrapping

Browser smoke with the local replay URL confirmed:

- 4 event candidates visible as persistent video markers
- 2 `HIT CANDIDATE` labels
- 2 `BOUNCE CANDIDATE` labels
- `.replay-media-id` uses `white-space: nowrap`, `overflow: hidden`, and ellipsis
- the video starts near the top rather than below a collapsed vertical header

## Validation

Focused event-candidate tests:

```text
.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q
15 passed
```

Full validation:

```text
.venv/bin/python -m pytest -q
295 passed

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

## Remaining Limitations

Event candidates are still first-pass review markers. The far-side fallback improves recall for
sparse trajectory data, but it remains candidate evidence and should not be used as hit truth,
bounce truth, in/out, score, or adjudication.
