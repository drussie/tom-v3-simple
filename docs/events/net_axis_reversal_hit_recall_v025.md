# Net-Axis Reversal Hit Recall v0.2.5

Status: implemented

This repair adds a ball-first hit-candidate recall path for sparse event contexts. The output remains
candidate evidence only: it is not hit truth, bounce truth, in/out, rally, point, score, player
identity, accepted/rejected lifecycle, or adjudication.

## Repair Goal

Earlier repairs recovered hits primarily from player-proximate contact zones. That protects against
open-court false hits, but it can miss a plausible hit when the player projection is absent,
time-shifted, or too noisy while the ball trajectory itself clearly reverses along the net axis.

v0.2.5 adds:

- `net_axis_reversal_hit_candidate_v025`
- configurable lookback/lookahead windows around each ball trajectory point
- a `court_y` net-axis reversal gate that does not require player proximity
- optional nearest-player diagnostics and confidence support when player projections are available
- weak-overlap suppression so ball-first recall does not erase protected bounce candidates

## Recall Rule

For each ball trajectory anchor point, the repair searches for incoming and outgoing ball points
within the configured windows:

```text
net_axis_reversal_lookback_ms = 700
net_axis_reversal_lookahead_ms = 700
net_axis_reversal_min_pre_post_gap_ms = 60
net_axis_reversal_min_delta_template = 0.015
```

A hit candidate can be proposed when:

- the incoming and outgoing `court_y` deltas exceed the minimum axis delta
- the sign of `court_y` motion reverses
- the anchor point is inside or near the court template

Player proximity is not required. If a near/far main-player projection is found, it is recorded as
diagnostic and confidence support only.

Example payload field:

```json
{
  "net_axis_reversal_recall": {
    "version": "v0.2.5",
    "player_proximity_required": false,
    "incoming_frame": 81,
    "anchor_frame": 93,
    "outgoing_frame": 109,
    "lookback_ms": 700,
    "lookahead_ms": 700,
    "nearest_player_found": true
  }
}
```

## Bounce Protection

The v0.2.4 contact-zone tightening remains in place. Ball-first net-axis reversal hits do not
automatically suppress nearby bounce candidates. Weak ball-first hits that overlap a bounce in both
time and court-template position can be suppressed with `suppressed_by_bounce_candidate_overlap`
diagnostics.

This keeps the false open-court hit-over-bounce protection while allowing an additional recalled
hit candidate when the ball trajectory supports it.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `6f432ec3-25f7-4ebf-87c9-3a3caf5afea4`
- `hit_candidate`: 3
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 722
- `net_axis_reversal_recovered_hit_count`: 1
- `player_anchor_suppressed_overlap_count`: 1

The added recalled hit was emitted with `candidate_method =
net_axis_reversal_hit_candidate_v025` and `player_proximity_required = false`. The two bounce
candidates remained present.

## Boundaries

This repair improves candidate recall and diagnostics only. A net-axis reversal can be caused by
projection error, sparse trajectory segmentation, camera effects, or a real hit-like event. It does
not prove racket contact and does not establish bounce truth, in/out, score, rally/point state,
player identity, accepted/rejected lifecycle, or adjudication.
