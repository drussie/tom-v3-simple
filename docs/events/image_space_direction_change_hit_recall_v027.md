# Image-Space Direction-Change Hit Recall v0.2.7

Status: implemented

This repair adds a full 2D broadcast-image direction-change recall path for airborne hit-like
candidate events. It remains candidate evidence only: it is not hit truth, bounce truth, in/out,
rally, point, score, player identity, accepted/rejected lifecycle, or adjudication.

## Repair Goal

v0.2.6 used broadcast `image_y` reversal as a hardcam near/far-axis fallback. That recovered one
far-side hit, but another visually obvious far-side contact/reversal did not produce a clean
image-y sign change.

v0.2.7 adds:

- `image_space_direction_change_hit_candidate_v027`
- `broadcast_image_2d_vector_direction_change_v027`
- image-space direction diagnostics under `image_space_direction_change_recall`
- rejected-context diagnostics with `diagnostic_source = image_space_direction_change_hit_recall`
- a weak pre-bounce suppression guard so open-court bounce candidates are not relabeled as hits

## Recall Rule

For each anchor point with `ball_court_projection_candidate.image_point` evidence, the repair
searches for incoming and outgoing image points within the configured windows:

```text
image_space_direction_change_lookback_ms = 700
image_space_direction_change_lookahead_ms = 700
image_space_direction_change_min_pre_post_gap_ms = 60
image_space_direction_change_min_vector_pixels = 8.0
image_space_direction_change_min_delta_degrees = 45.0
```

The image vectors are:

```text
incoming_vector = anchor_image_point - incoming_image_point
outgoing_vector = outgoing_image_point - anchor_image_point
```

A hit candidate can be proposed when both vectors are long enough and the angle between them is at
least the configured threshold. Player proximity is not required; nearest-player information is
recorded only as diagnostic/confidence support.

## Payload

Candidate payloads include:

```json
{
  "image_space_direction_change_recall": {
    "candidate_method": "image_space_direction_change_hit_candidate_v027",
    "image_direction_change_method": "broadcast_image_2d_vector_direction_change_v027",
    "player_proximity_required": false,
    "incoming_frame": 162,
    "anchor_frame": 164,
    "outgoing_frame": 185,
    "dx_before": 15.351288,
    "dy_before": 26.199326,
    "dx_after": 195.282196,
    "dy_after": 34.330551,
    "image_direction_delta_degrees": 49.66147,
    "court_projection_warning": "hit candidate uses image-space direction change because airborne hits may not project cleanly to court plane"
  }
}
```

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `9a67e173-dbe5-4644-bc0c-233b46fc2fd5`
- `hit_candidate`: 5
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 870
- `image_direction_change_source_point_count`: 75
- `image_direction_change_candidate_count`: 43
- `image_direction_change_recovered_hit_count`: 1
- `image_direction_change_suppressed_overlap_count`: 1

The recovered final hit was emitted at frame 164 with
`candidate_method = image_space_direction_change_hit_candidate_v027`. A weak direction-change
candidate immediately before the frame 81 bounce was suppressed as an overlap diagnostic, so the
old false hit-over-bounce behavior stayed suppressed.

## Boundaries

This is a recall heuristic for operator review. A 2D image direction change can come from camera
perspective, detection gaps, occlusion, projection artifacts, or a real hit-like event. It does not
prove racket contact and does not establish bounce truth, in/out, scoring, rally/point state,
player identity, accepted/rejected lifecycle, or adjudication.
