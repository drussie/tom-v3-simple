# Local-Evidence Event-Type Classification v0.2.8

Status: implemented

This repair classifies image-space direction-change candidates by local evidence before assigning
them to `hit_candidate` or `bounce_candidate`. It remains candidate evidence only: it is not hit
truth, bounce truth, in/out, rally, point, score, player identity, accepted/rejected lifecycle, or
adjudication.

## Correction

A hit candidate does not require a prior bounce. Volleys, overheads, block volleys, swinging
volleys, short hops, and serve-and-volley patterns can all create hit-like ball direction changes
without a prior court bounce.

Sequence is now weak diagnostic context only:

```json
{
  "sequence_context_model": "optional_bounce_between_hits_v0",
  "sequence_prior_strength": "weak",
  "sequence_is_hard_gate": false,
  "hit_requires_prior_bounce": false
}
```

## Local Evidence Model

Image-space direction changes can be hit-like, bounce-like, or diagnostic-only. v0.2.8 adds
`local_evidence_event_type` to final event candidate payloads when this classifier handles an
image-space direction-change candidate.

Hit-like candidates are kept as `hit_candidate` when the direction change is strong and not in an
obvious court landing zone. Reason codes include:

- `image_space_direction_change`
- `hit_like_direction_change`
- `player_proximity_not_required`
- `no_bounce_required_for_hit`
- `airborne_hit_projection_warning`

Bounce-like candidates are reclassified to `bounce_candidate` when the direction change lands
inside/near the court plane, is away from clear player-contact support, and is not in the
midcourt/net transition zone. Reason codes include:

- `bounce_like_court_landing_zone`
- `court_plane_landing_candidate`
- `away_from_player_contact_zone`
- `direction_change_reclassified_to_bounce_candidate`

## Payload

Example payload fragment:

```json
{
  "local_evidence_event_type": {
    "classifier_version": "v0.2.8",
    "source_candidate_method": "image_space_direction_change_hit_candidate_v027",
    "selected_candidate_type": "bounce_candidate",
    "original_candidate_type": "hit_candidate",
    "sequence_is_hard_gate": false,
    "hit_requires_prior_bounce": false,
    "bounce_like_court_landing_zone": true,
    "hit_like_airborne_direction_change": false,
    "inside_or_near_court": true,
    "player_contact_support": false,
    "classification_reason": "direction_change_in_court_landing_zone_without_contact_support"
  }
}
```

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `2a5f4dc8-91fd-481c-91d1-c1f5ee5c3a17`
- `hit_candidate`: 7
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 868
- `direction_change_candidates_classified`: 2
- `direction_change_kept_as_hit_count`: 1
- `direction_change_reclassified_to_bounce_count`: 1
- `sequence_is_hard_gate`: false
- `hit_requires_prior_bounce`: false

The image-space direction-change candidate at frame 77 was reclassified to
`bounce_candidate`. The image-space direction-change candidate at frame 164 remained a
`hit_candidate` because local evidence treated it as a strong midcourt/airborne-style direction
change, not an obvious court landing-zone marker.

## Boundaries

This repair improves candidate labeling for operator review. It does not prove contact, bounce,
in/out, point state, score, or player identity. It does not create an accepted/rejected lifecycle
and does not adjudicate tennis events.

Follow-up v0.2.9 adds a universal final guard across all hit-candidate sources. The v0.2.8 local
classifier remains the image-space direction-change classifier, while v0.2.9 records
`universal_hit_validity_guard` metadata after all source-specific classifiers have run.
