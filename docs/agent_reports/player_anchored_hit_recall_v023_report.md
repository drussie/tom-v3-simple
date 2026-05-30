# Player-Anchored Hit Recall v0.2.3 Report

## Summary

Implemented a player-anchored hit recall pass for `build-hit-bounce-candidates`. The repair scans a
wider ball trajectory window around near/far main player court projections and emits
`hit_candidate` evidence when a candidate ball point near a player has a wide-window `court_y`
net-axis reversal.

All output remains candidate evidence only. No hit truth, bounce truth, in/out, score, rally/point
logic, identity, accepted/rejected lifecycle, or adjudication was added.

## Implementation

Changed:

- `apps/worker/services/hit_bounce_candidates.py`
- `apps/worker/cli.py`
- `Makefile`
- `apps/api/services/replay.py`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/types.ts`
- `tests/test_hit_bounce_candidates.py`

Added docs:

- `docs/events/player_anchored_hit_recall_v023.md`
- `docs/agent_reports/player_anchored_hit_recall_v023_report.md`

## Candidate Method

New method:

```text
player_anchored_net_axis_reversal_hit_candidate_v023
```

The pass evaluates:

- main player projection anchor
- nearest ball court trajectory point near the anchor
- incoming ball point within lookback
- outgoing ball point within lookahead
- wide-window `court_y` reversal
- player/ball distance in normalized template units

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

```text
event_candidate_run_id: 9ae5e4a3-346e-41a8-866c-cc29cc00d8e2
hit_candidate: 3
bounce_candidate: 2
event_candidate_rejection_diagnostic: 433
player_anchor_context_count: 405
player_anchor_candidate_count: 66
player_anchor_recovered_hit_count: 2
```

Old v0.2.2 local baseline:

```text
hit_candidate: 2
bounce_candidate: 2
event_candidate_rejection_diagnostic: 29
```

The repair recovered a far-player anchored hit at frame 34. It also preserved one pre-anchor
fallback candidate so the side-zone sequence pass could keep the earlier far-side landing candidate
as `bounce_candidate`.

## Diagnostics

Selected evidence and replay payloads expose `player_anchored_hit_recall`, including:

- anchor player observation id
- anchor track role candidate
- anchor ball frame/time
- incoming/outgoing frame/time
- lookback/lookahead windows
- distance threshold
- `vy_before` / `vy_after`
- net-axis reversal flag
- candidate-only warnings

Rejected anchor contexts are persisted as `event_candidate_rejection_diagnostic` rows with explicit
reason codes.

## Validation

Validation passed:

```text
.venv/bin/python -m pytest tests/test_hit_bounce_candidates.py -q
21 passed

.venv/bin/python -m pytest -q
301 passed

ruff check .
passed

cd apps/web
npm run lint
npm run build
npm audit --omit=dev
passed / found 0 vulnerabilities

DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_player_anchored_hit_recall_fixture.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_player_anchored_hit_recall_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```

Browser smoke against `event_candidate_run_id` `9ae5e4a3-346e-41a8-866c-cc29cc00d8e2` showed the
operator replay page loading with video, 5 event candidates, and visible `HIT CANDIDATE` /
`BOUNCE CANDIDATE` labels.

## Remaining Limitations

- The wider lookahead bridges sparse trajectory gaps, but it is still a heuristic over candidate
  projection evidence.
- `court_y` is treated as the current normalized template net-axis convention.
- Player anchors inherit main-player projection and homography candidate limitations.
- Candidate counts can change with threshold tuning; no candidate is truth.
