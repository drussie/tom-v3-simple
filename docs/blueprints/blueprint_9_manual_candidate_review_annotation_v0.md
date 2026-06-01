# Blueprint 9 - Manual Candidate Review Annotation v0

Blueprint 9 adds operator review metadata for event candidate markers.

It does not change generated hit/bounce evidence. It does not create accepted/rejected truth. It is a review and annotation layer for later evaluation work.

## Scope

This milestone adds:

- `event_candidate_review_annotation` persistence
- replay API endpoints for list/create/update/delete review annotations
- marker-level review controls in the Replay Marker Inspector
- review badges and summary counts in the Event Candidate Review panel
- missing-candidate notes at the current replay time
- point evidence snapshot `review_summary` and `review_annotations`

Supported marker review labels:

- `useful`
- `wrong`
- `unclear`
- `needs_review`

Supported missing-candidate note labels:

- `missing_hit_candidate`
- `missing_bounce_candidate`
- `missing_event_candidate`

## Contract

Review annotations are metadata only.

They preserve:

- source event candidate observations
- event candidate counts
- marker-level arbitration output
- source run provenance

They explicitly do not add:

- hit truth
- bounce truth
- in/out
- score
- rally or point state
- accepted/rejected lifecycle
- adjudication

## API

List reviews:

```bash
GET /replay/{media_id}/event-candidate-reviews?event_candidate_run_id=<run_id>
```

Create a marker review:

```json
{
  "event_candidate_run_id": "...",
  "observation_id": "...",
  "annotation_kind": "candidate_marker_review",
  "review_label": "useful",
  "note": "Operator note"
}
```

Create a missing-candidate note:

```json
{
  "event_candidate_run_id": "...",
  "annotation_kind": "missing_candidate_note",
  "review_label": "missing_bounce_candidate",
  "frame": 42,
  "timestamp_ms": 1400,
  "note": "Possible unmarked bounce here"
}
```

Update and delete:

```bash
PATCH /replay/{media_id}/event-candidate-reviews/{review_id}
DELETE /replay/{media_id}/event-candidate-reviews/{review_id}
```

## Replay Behavior

When `eventCandidateRunId` is present, Replay loads review annotations for that run.

The Event Candidate Review panel shows summary counts and per-marker badges. The Marker Inspector lets the operator save or clear a marker review without mutating the underlying `hit_candidate` or `bounce_candidate` observation.

The Missing Candidate Note panel records a review note at the current frame/time. These notes are separate from generated markers and are intended for later benchmark/evaluation design.

## Snapshot Behavior

Point evidence snapshots include:

- `review_summary`
- `review_annotations`

The snapshot still reports generated candidate counts exactly as generated. Review labels never change `hit_candidate`, `bounce_candidate`, marker summary, or arbitration output.
