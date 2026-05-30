# Hit/Bounce Physics Heuristic Repair v0.2

Status: implemented

Hit/Bounce Physics Heuristic Repair v0.2 improves the candidate-quality logic for
`hit_candidate` and `bounce_candidate` observations.

The repair remains candidate evidence only. It does not create hit truth, bounce truth, in/out
decisions, point or score logic, accepted/rejected lifecycle, or adjudication.

## Hit Candidate Logic

Hit candidates now prefer a player-proximate net-axis reversal:

```text
main-player projection near candidate time
+ court-y direction reversal across the candidate point
+ trajectory direction or speed-change support
-> hit_candidate
```

The first v0.2 implementation treats normalized `court_template_2d.court_y` as the net-axis. The
payload includes:

```json
{
  "net_axis_reversal": {
    "axis": "court_y",
    "vy_before": -0.045488,
    "vy_after": 0.044607,
    "reversal": true,
    "min_axis_delta": 0.015
  }
}
```

Reason codes can include:

- `near_main_player_projection`
- `net_axis_reversal`
- `trajectory_direction_change`
- `player_proximate_event_priority`
- `speed_change_candidate`
- `within_time_window`

## Bounce Candidate Logic

Bounce candidates now prefer image-space descending-to-ascending motion plus speed reduction away
from main-player projection candidates:

```text
away from main-player projection
+ source image-y proxy descends then ascends
+ court-template speed reduces after the candidate
+ inside or near the court template
-> bounce_candidate
```

The vertical signal is a camera-space image-y proxy, not true 3D ball height. The payload says that
explicitly:

```json
{
  "vertical_motion_proxy": {
    "proxy_type": "image_y_descending_to_ascending_v0",
    "descending_to_ascending": true,
    "proxy_warning": "image_y is camera-space proxy, not true ball height"
  },
  "speed_reduction": {
    "speed_reduction_fraction": 0.925587,
    "speed_reduced": true
  }
}
```

Reason codes can include:

- `descending_to_ascending_image_proxy`
- `speed_reduction_candidate`
- `away_from_main_player_projection`
- `inside_or_near_court_template`
- `trajectory_direction_change`
- `local_motion_discontinuity`

## Source Image Points

The builder resolves each trajectory point's source `ball_court_projection_candidate` and reads the
persisted `payload.image_point`. This keeps bounce proxy computation tied to the immutable source
projection evidence.

If source image points are unavailable, v0.2 does not create a high-confidence bounce candidate
from the vertical proxy path.

## CLI Thresholds

`build-hit-bounce-candidates` now supports:

```text
--hit-min-net-axis-delta-template 0.015
--bounce-min-image-y-delta-pixels 2.0
--bounce-min-speed-reduction-fraction 0.05
```

The Makefile helper exposes matching variables:

```text
HIT_MIN_NET_AXIS_DELTA_TEMPLATE
BOUNCE_MIN_IMAGE_Y_DELTA_PIXELS
BOUNCE_MIN_SPEED_REDUCTION_FRACTION
```

## Boundaries

The repaired candidates are still derived evidence. They are not confirmed hits, confirmed bounces,
in/out decisions, rally, point, score, player identity, accepted/rejected truth lifecycle, or
adjudication.
