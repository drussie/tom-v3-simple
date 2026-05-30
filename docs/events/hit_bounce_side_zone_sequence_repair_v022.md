# Hit/Bounce Side-Zone + Sequence Classification Repair v0.2.2

Status: implemented

This repair adds a side-zone and sequence classification pass on top of the v0.2.1 hit/bounce
candidate builder.

The output remains candidate evidence only. It is not hit truth, bounce truth, in/out, rally,
point, score, player identity, accepted/rejected lifecycle, or adjudication.

## Classification Pass

v0.2.2 first keeps the existing physics candidate generation and recall diagnostics, then applies a
deterministic review pass over deduped event candidates ordered by media time.

The pass adds:

- `court_side_zone`
- `player_contact_zone`
- `court_landing_zone`
- `candidate_reclassification`
- `candidate_sequence`

The current court convention is documented in each payload as:

```text
court_y_low_near_high_far_v022
```

This treats lower normalized `court_y` as the near side and higher normalized `court_y` as the far
side for candidate classification diagnostics.

## Reclassification Rules

The repair uses a simple alternating event prior:

```text
hit_candidate -> bounce_candidate -> hit_candidate -> bounce_candidate
```

The prior is not tennis truth. It is a candidate review heuristic used only after the physics pass
has proposed candidate events.

Two bounded reclassifications are supported:

- a `hit_candidate` can become a `bounce_candidate` when it is better explained as a court landing
  zone candidate and the sequence expects a bounce
- a `bounce_candidate` can become a `hit_candidate` when it falls in a player contact zone and the
  sequence or side-zone context supports a hit

Payloads preserve the original candidate type and method, for example:

```json
{
  "candidate_reclassification": {
    "original_candidate_type": "hit_candidate",
    "final_candidate_type": "bounce_candidate",
    "reason": "court_landing_zone_over_player_contact_zone",
    "reclassified": true
  }
}
```

## CLI Summary

`build-hit-bounce-candidates` now reports v0.2.2 side-zone sequence fields:

```json
{
  "raw_hit_candidate_count": 3,
  "raw_bounce_candidate_count": 5,
  "reclassified_hit_to_bounce_count": 1,
  "reclassified_bounce_to_hit_count": 1,
  "final_hit_candidate_count": 2,
  "final_bounce_candidate_count": 2,
  "sequence_prior_applied_count": 2,
  "physics_heuristic_version": "v0.2.2"
}
```

The raw counts describe candidates before sequence reclassification. Final counts describe persisted
`hit_candidate` and `bounce_candidate` rows.

## Replay

Replay selected evidence exposes the new diagnostics so an operator can see why an event marker was
kept or reclassified. Video and mini-map labels still say `HIT CANDIDATE` and `BOUNCE CANDIDATE`.
They never imply hit truth, bounce truth, in/out, point, score, or adjudication.

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
- `reclassified_hit_to_bounce_count`: 1
- `reclassified_bounce_to_hit_count`: 1
- `sequence_prior_applied_count`: 2

The sample-point visual target was achieved: the far-side triangle-like raw candidate is now a
`BOUNCE CANDIDATE`, and the near-side right circle-like raw candidate is now a `HIT CANDIDATE`.

## Boundaries

This repair improves candidate label quality and diagnostics only. It does not add event truth,
line calls, score, rally/point logic, identity, server/receiver logic, or adjudication.
