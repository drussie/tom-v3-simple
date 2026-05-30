# Image-Space Net-Axis Hit Recall v0.2.6

Status: implemented

This repair adds an image-space hit-candidate recall path for airborne visual events where
court-plane homography can distort the ball's apparent net-axis motion. The output remains
candidate evidence only: it is not hit truth, bounce truth, in/out, rally, point, score, player
identity, accepted/rejected lifecycle, or adjudication.

## Repair Goal

v0.2.5 recovered ball-first hit candidates from `court_y` reversal in court-template space. That
works when the projected court-space ball path is meaningful, but a hit usually happens in the air,
not on the court plane. For far-side contacts, the projected `court_y` path can be sparse or
distorted even when the broadcast video shows a clear direction reversal.

v0.2.6 adds:

- `image_space_net_axis_reversal_hit_candidate_v026`
- `broadcast_image_y_axis_fallback_v026`
- image-space reversal diagnostics under `image_space_net_axis_reversal_recall`
- direct use of `ball_court_projection_candidate.image_point` rows for the recall pass
- persisted diagnostics for rejected image-space recall contexts

## Recall Rule

The first implementation uses broadcast image `y` as a pragmatic near/far-axis fallback:

```text
image_space_net_axis_lookback_ms = 700
image_space_net_axis_lookahead_ms = 700
image_space_net_axis_min_pre_post_gap_ms = 60
image_space_net_axis_min_delta_pixels = 4.0
```

For each image-space anchor point, the repair searches for incoming and outgoing ball projection
points within the configured windows. A hit candidate can be proposed when:

- incoming, anchor, and outgoing image points exist
- the pre/post image-axis deltas exceed the minimum pixel delta
- the sign of image-axis motion reverses

Player proximity is not required. If a near/far main-player projection is found, it is recorded as
diagnostic and confidence support only.

Example payload field:

```json
{
  "image_space_net_axis_reversal_recall": {
    "candidate_method": "image_space_net_axis_reversal_hit_candidate_v026",
    "image_axis_method": "broadcast_image_y_axis_fallback_v026",
    "player_proximity_required": false,
    "incoming_frame": 34,
    "anchor_frame": 54,
    "outgoing_frame": 66,
    "image_axis_before": -79.576702,
    "image_axis_after": 94.3381,
    "image_axis_reversal": true,
    "court_projection_warning": "hit candidate uses image-space motion because airborne hits may not project cleanly to court plane"
  }
}
```

## Source Points

The image-space recall pass reads `ball_court_projection_candidate` rows from the court projection
run when available. This allows recall from short or gappy projection spans that were not persisted
as `ball_trajectory_court_candidate` segments. Candidates still link to the source ball projection
observation. If the anchor point did not come from a trajectory observation, the trajectory
observation id is recorded as `null` rather than fabricating lineage.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `d33a959b-462d-4b2e-8eed-d715565ed2c7`
- `hit_candidate`: 4
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 796
- `image_net_axis_reversal_source_point_count`: 75
- `image_net_axis_reversal_candidate_count`: 12
- `image_net_axis_reversal_recovered_hit_count`: 1

The added recovered hit was emitted at frame 54 with `candidate_method =
image_space_net_axis_reversal_hit_candidate_v026`, using incoming frame 34 and outgoing frame 66 in
image space. Existing good bounce candidates remained present.

## Boundaries

This repair improves candidate recall and diagnostics only. Broadcast `image_y` is a camera-space
fallback, not universal court geometry or true ball height. An image-space reversal can be caused
by camera perspective, detection gaps, projection artifacts, or a real hit-like event. It does not
prove racket contact and does not establish bounce truth, in/out, score, rally/point state, player
identity, accepted/rejected lifecycle, or adjudication.
