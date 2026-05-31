# Universal Hit Validity Guard Tightening v0.3.0

Status: implemented

This repair tightens the final universal hit-candidate guard introduced in v0.2.9. The v0.2.9
guard recorded metadata but kept every real sample hit candidate. v0.3.0 keeps the same
candidate-only boundary while making the guard corrective.

The repair does not add hit truth, bounce truth, in/out, score, rally/point logic, player identity,
an accepted/rejected lifecycle, or adjudication.

## Tightening

The guard now separates strong local event evidence from weak image-space transit evidence:

- hard reversal support means court-y net-axis reversal or image-y net-axis reversal
- image-space direction change alone is diagnostic, not hard reversal support
- fallback landing-like hit candidates can be reclassified to `bounce_candidate`
- midcourt image-direction-only transit candidates can be suppressed as rejection diagnostics

The guard remains a final display/evidence policy over candidates. It still does not require a prior
bounce before a hit candidate:

```json
{
  "hit_requires_prior_bounce": false,
  "sequence_is_hard_gate": false
}
```

## Decisions

For each final hit candidate draft, v0.3.0 records `universal_hit_validity_guard` metadata and
chooses:

- `keep_as_hit`
- `reclassify_to_bounce`
- `suppress_as_diagnostic`

Rejected diagnostics can include `fly_through_no_local_reversal`,
`transit_candidate_without_event_evidence`, and `suppressed_by_universal_hit_validity_guard`.

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `5bbbb6b8-fb06-4319-863f-e32675f48aba`
- `hit_candidate`: 5
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 869
- `physics_heuristic_version`: `v0.3.0`
- `universal_hit_validity_guard_decision_counts`: `{"keep_as_hit": 5, "reclassify_to_bounce": 1, "suppress_as_diagnostic": 1}`

Compared with v0.2.9, the real sample run changed from 7 hits and 2 bounces with all hits kept to
5 hits and 3 bounces, with one unsupported landing-like hit reclassified and one transit hit
suppressed into diagnostics.

## Boundaries

This is candidate-quality repair only. It improves review markers and diagnostics, but it does not
prove hit, bounce, in/out, point state, score, or adjudication.

## Follow-Up v0.3.1

Marker-Level Event Arbitration v0.3.1 runs after this universal guard and resolves visible marker
conflicts that require local marker context rather than only source-specific hit validation. It can
suppress co-located hit markers when a bounce marker is the better candidate explanation and can
suppress transit/fly-through hits into diagnostics. It still does not require a prior bounce before
a hit candidate, and sequence remains weak diagnostic context only.

See `docs/events/marker_level_event_arbitration_v031.md`.
