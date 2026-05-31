# Marker-Level Event Arbitration v0.3.1

Status: implemented

This repair adds a marker-level arbitration pass after universal hit validity guard v0.3.0. The
v0.3.0 guard reduced generic false positives, but the visible replay still needed marker-level
conflict handling: a co-located hit/bounce pair should not remain as two strong visible markers
unless the hit has independent contact evidence, and a transit/fly-through hit marker should not
remain visible when it has no local event support.

The repair remains candidate evidence only. It does not add hit truth, bounce truth, in/out, score,
rally/point logic, player identity, an accepted/rejected lifecycle, or adjudication.

## Arbitration Rules

Marker-level arbitration runs over the final candidate drafts after the universal guard:

- `hit_candidate` and `bounce_candidate` markers in the same local time/space neighborhood are
  treated as a visible marker conflict.
- Co-located hit/bounce conflicts prefer the `bounce_candidate` unless the hit has strong
  independent contact evidence.
- Fly-through/transit hit markers without local reversal/contact/landing support are suppressed
  into `event_candidate_rejection_diagnostic` rows.
- Far-side recall candidates are preserved when they survive the marker-level checks.
- A hit candidate still does not require a prior bounce.
- Sequence remains weak diagnostic context only, not a hard gate.

The selected evidence payload can include `marker_level_arbitration` with a decision such as:

```json
{
  "version": "v0.3.1",
  "decision": "suppress_hit_keep_bounce",
  "reason": "co_located_hit_bounce_prefers_landing_evidence",
  "hit_requires_prior_bounce": false,
  "sequence_is_hard_gate": false
}
```

## Decisions

The pass records decision counts in the CLI summary and processing metadata:

- `keep_hit`
- `keep_bounce`
- `suppress_hit_keep_bounce`
- `suppress_as_diagnostic`

Suppressed diagnostics can include reason codes such as:

- `suppressed_by_marker_level_arbitration`
- `hit_bounce_conflict_resolved_to_bounce`
- `suppressed_hit_overlapping_bounce`
- `co_located_hit_bounce_prefers_landing_evidence`
- `fly_through_no_local_event`
- `transit_candidate_without_event_evidence`

## Local Smoke

Input:

- `media_id`: `9518fb01-0da1-4344-9a84-ff88ec8e9b1e`
- `court_projection_run_id`: `82498799-490f-44df-9222-0157356c5ff7`
- `ball_trajectory_run_id`: `2e16f3d1-e252-497a-b688-d81890645ab7`

Output:

- `event_candidate_run_id`: `609fe533-42cf-4f7f-98f0-330b0bc05b45`
- `physics_heuristic_version`: `v0.3.1`
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `event_candidate_rejection_diagnostic`: 871
- `marker_level_arbitration_decision_counts`:
  - `keep_bounce`: 3
  - `keep_hit`: 3
  - `suppress_as_diagnostic`: 1
  - `suppress_hit_keep_bounce`: 1
- `hit_bounce_conflicts_resolved_to_bounce`: 1
- `fly_through_hits_suppressed`: 1
- `far_side_hits_recovered`: 1
- `far_side_bounces_recovered`: 1
- `hit_requires_prior_bounce`: false
- `sequence_is_hard_gate`: false

Compared with the v0.3.0 smoke output, v0.3.1 keeps the far-side hit and far-side bounce, resolves
the far-side hit/bounce overlap to the bounce marker, and suppresses the lower/mid-court
fly-through hit into diagnostics.

## Boundaries

This repair changes candidate-marker arbitration and diagnostics only. It improves what operators
see in replay, but it does not prove contact, bounce, in/out, point state, score, or adjudication.
