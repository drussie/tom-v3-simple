# Universal Hit Candidate Validity Guard v0.2.9

Status: implemented

This repair adds a final candidate-only validity guard after the existing hit/bounce candidate
classifiers and overlap suppressors. The guard applies to every remaining `hit_candidate` source:
local/player-proximate hits, player-anchored hits, court-y net-axis reversal hits, image-y
net-axis reversal hits, image-space direction-change hits, and fallback hits.

The guard does not create hit truth, bounce truth, in/out, point state, score, player identity,
an accepted/rejected lifecycle, or adjudication.

## Decisions

For each final hit candidate draft, the guard records `universal_hit_validity_guard` metadata and
chooses one display/evidence outcome:

- keep as `hit_candidate`
- reclassify to `bounce_candidate` when the candidate is landing-like and lacks reversal/contact
  support
- suppress to `event_candidate_rejection_diagnostic` when the candidate looks like fly-through or
  transit evidence with no local event support

The guard is intentionally not a sequence gate. A hit candidate still does not require a prior
bounce:

```json
{
  "hit_requires_prior_bounce": false,
  "sequence_is_hard_gate": false
}
```

## Payload

Final hit and reclassified bounce candidates can include:

```json
{
  "universal_hit_validity_guard": {
    "guard_version": "v0.2.9",
    "classification_priority": "universal_hit_candidate_validity_guard",
    "applied": true,
    "source_candidate_type": "hit_candidate",
    "source_candidate_method": "image_space_direction_change_hit_candidate_v027",
    "final_decision": "keep_as_hit",
    "assessment": {
      "reversal_support": true,
      "contact_support": false,
      "strong_contact_support": false,
      "landing_zone_support": true,
      "local_image_direction_support": true,
      "bounce_like_landing_zone": false,
      "fly_through_candidate": false
    },
    "hit_requires_prior_bounce": false,
    "sequence_is_hard_gate": false,
    "candidate_only": true,
    "not_hit_truth": true,
    "not_bounce_truth": true,
    "not_in_out_truth": true,
    "no_adjudication": true
  }
}
```

Suppressed candidates become diagnostics with rejection reasons such as
`suppressed_by_universal_hit_validity_guard`, `fly_through_no_local_reversal`, and
`transit_candidate_without_event_evidence`.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `ac6486bd-d4d0-4d60-88ea-b9790fe3a01f`
- `hit_candidate`: 7
- `bounce_candidate`: 2
- `event_candidate_rejection_diagnostic`: 868
- `hit_candidates_evaluated_by_guard`: 7
- `hit_candidates_kept_by_guard`: 7
- `hit_candidates_reclassified_to_bounce_by_guard`: 0
- `hit_candidates_suppressed_by_guard`: 0

The smoke run preserved the existing sample-point hit/bounce candidates and added guard diagnostics
to each final hit. Synthetic tests cover bounce-like hit reclassification and fly-through
suppression.

## Boundaries

This guard improves candidate quality and explainability. It is not hit truth, bounce truth, in/out,
score, rally/point logic, or adjudication.
