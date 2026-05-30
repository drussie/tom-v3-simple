# Player-Anchored Hit Recall v0.2.3

Status: implemented

This repair adds a player-anchored hit recall pass on top of the v0.2.2 hit/bounce candidate
builder.

The output remains candidate evidence only. It is not hit truth, bounce truth, in/out, rally,
point, score, player identity, accepted/rejected lifecycle, or adjudication.

## Recall Pass

The earlier local trajectory pass depends on adjacent trajectory triples:

```text
previous ball point -> current ball point -> next ball point
```

That can miss a visually obvious hit when the ball trajectory has a sparse gap near a main player.
v0.2.3 adds a second pass:

```text
main player court projection anchor
+ wider ball lookback/lookahead window
+ court_y net-axis reversal
+ player proximity
-> hit_candidate
```

The pass uses only persisted candidate evidence:

- `ball_trajectory_court_candidate`
- `main_player_court_projection_candidate`

It does not mutate source rows.

## Defaults

The default player-anchored recall thresholds are:

```text
player_anchored_hit_lookback_ms = 700
player_anchored_hit_lookahead_ms = 1300
player_anchored_hit_distance_max_template = 0.24
player_anchored_hit_min_net_axis_delta_template = 0.015
player_anchored_hit_min_pre_post_gap_ms = 60
```

The longer lookahead is bounded and exists to bridge sparse ball trajectory gaps around player
contact zones. It does not infer contact truth.

## Candidate Payload

Player-anchored hit candidates include:

```json
{
  "candidate_method": "player_anchored_net_axis_reversal_hit_candidate_v023",
  "player_anchored_hit_recall": {
    "anchor_track_role_candidate": "far_player_track_candidate",
    "anchor_ball_frame": 34,
    "incoming_frame": 30,
    "outgoing_frame": 66,
    "distance_template_units": 0.129729,
    "distance_threshold": 0.24,
    "vy_before": 0.015369,
    "vy_after": -0.029911,
    "net_axis_reversal": true,
    "not_hit_truth": true,
    "observation_only": true,
    "no_adjudication": true
  }
}
```

Rejected player anchors produce `event_candidate_rejection_diagnostic` observations with reasons
such as:

- `no_ball_point_near_player_anchor`
- `player_anchor_distance_too_large`
- `no_incoming_point_in_lookback_window`
- `no_outgoing_point_in_lookahead_window`
- `no_wide_window_net_axis_reversal`

## Dedupe And Sequence

v0.2.3 preserves one pre-anchor fallback candidate when a later player-anchored hit would otherwise
dedupe it. This allows the side-zone sequence pass to classify an earlier player-proximate landing
candidate as `bounce_candidate` while keeping the later player-anchored net-axis reversal as
`hit_candidate`.

This is a candidate-label repair. It is not a rally-order truth model.

## CLI

The existing command remains:

```bash
python -m apps.worker.cli build-hit-bounce-candidates \
  --media-id <media_id> \
  --ball-trajectory-run-id <ball_trajectory_run_id> \
  --court-projection-run-id <court_projection_run_id>
```

Optional player-anchored recall knobs:

```text
--player-anchored-hit-enabled / --no-player-anchored-hit-enabled
--player-anchored-hit-lookback-ms
--player-anchored-hit-lookahead-ms
--player-anchored-hit-distance-max-template
--player-anchored-hit-min-net-axis-delta-template
--player-anchored-hit-min-pre-post-gap-ms
```

The Makefile helper exposes matching variables:

```bash
make tom-v1-hit-bounce-candidates \
  PLAYER_ANCHORED_HIT_LOOKAHEAD_MS=1300
```

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `9ae5e4a3-346e-41a8-866c-cc29cc00d8e2`
- `hit_candidate`: 3
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 433
- `player_anchor_candidate_count`: 66
- `player_anchor_recovered_hit_count`: 2

The far-side player-anchored hit was recovered at frame 34 from a wide-window `court_y` reversal
between frames 30 and 66. The earlier far-side fallback remained available for side-zone sequence
classification as a `bounce_candidate`.

## Boundaries

Player-anchored hit recall improves candidate recall and diagnostics only. It does not add hit
truth, bounce truth, line calls, score, rally/point logic, identity, server/receiver logic,
accepted/rejected lifecycle, or adjudication.
