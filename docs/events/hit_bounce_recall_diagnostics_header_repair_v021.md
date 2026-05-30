# Hit/Bounce Recall Diagnostics + Header Layout Repair v0.2.1

Status: implemented

This repair improves first-pass `hit_candidate` / `bounce_candidate` recall diagnostics and fixes a
Replay Workstation header layout collapse.

The event outputs remain candidate evidence only. They are not hit truth, bounce truth, in/out,
rally, point, score, player identity, accepted/rejected lifecycle, or adjudication.

## Candidate Recall

v0.2.1 keeps the v0.2 physics preference:

- hit candidates prefer player-proximate net-axis reversal
- bounce candidates prefer image-y descending-to-ascending proxy plus speed reduction away from
  main-player projections

It adds a bounded far-side hit fallback for player-proximate speed-change contexts. This recovers
contact-like events where sparse projected trajectory points show strong speed change near a player
but no reliable `court_y` reversal.

Fallback hit candidates are labeled with:

- `candidate_method = player_proximate_speed_reduction_hit_candidate_fallback_v021`
- `player_proximate_speed_change_fallback`
- `net_axis_reversal_not_required_for_fallback`

The fallback is still a `hit_candidate`, not hit truth.

## Rejection Diagnostics

The builder now persists `event_candidate_rejection_diagnostic` observations for evaluated
trajectory contexts that do not become candidates or are removed by dedupe/conflict handling.

Diagnostics include:

- frame and timestamp
- court point and source image point when available
- nearest main-player projection and time delta
- net-axis reversal result
- image-y vertical proxy result
- speed-reduction result
- candidate decision
- explicit rejection reasons

Reason codes include:

- `no_nearest_player_in_time_window`
- `player_too_far_for_hit`
- `no_net_axis_reversal`
- `net_axis_delta_below_threshold`
- `no_descending_to_ascending_proxy`
- `no_speed_reduction`
- `near_player_so_not_bounce`
- `deduped_lower_confidence`
- `suppressed_by_hit_candidate`

CLI output includes a rejection-reason summary so missing far-side candidates can be explained
without treating the event layer as truth.

## Header Layout

The replay header now uses a single flexible column, compact badge wrapping, and an ellipsized media
id. The media id should not wrap one character per line, and the video should start near the top of
the page on desktop and narrow layouts.

## CLI

`build-hit-bounce-candidates` now supports:

```text
--hit-player-time-window-ms 300
--hit-contact-fallback-min-speed-delta-fraction 0.45
--hit-contact-fallback-min-direction-delta-degrees 5.0
--bounce-fallback-enabled / --no-bounce-fallback-enabled
--bounce-fallback-min-speed-reduction-fraction 0.35
```

The Makefile helper exposes matching variables:

```text
HIT_PLAYER_TIME_WINDOW_MS
HIT_CONTACT_FALLBACK_MIN_SPEED_DELTA_FRACTION
HIT_CONTACT_FALLBACK_MIN_DIRECTION_DELTA_DEGREES
BOUNCE_FALLBACK_ENABLED
BOUNCE_FALLBACK_MIN_SPEED_REDUCTION_FRACTION
```

## Boundaries

The repair improves recall and diagnostic visibility only. It does not add accepted/rejected event
truth, in/out calls, scoring, point logic, player identity, server/receiver logic, or adjudication.
