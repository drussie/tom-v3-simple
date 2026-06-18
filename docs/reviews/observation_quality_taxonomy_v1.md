# Observation Quality Taxonomy v1

The observation-quality taxonomy is a versioned vocabulary for describing review-support quality
dimensions on manifest-backed points. It gives future review/export/regression surfaces a stable
contract for quality metadata without creating truth.

It is not truth, training truth, 3D truth, scoring, player identity, point winner, in/out,
candidate generation, or adjudication.

## Build

```bash
make tom-v1-export-observation-quality-taxonomy \
  PYTHON=.venv/bin/python

make tom-v1-build-multi-point-replay-index \
  PYTHON=.venv/bin/python

make tom-v1-build-observation-quality-profile \
  PYTHON=.venv/bin/python
```

Default paths:

```text
.data/contracts/observation_quality_taxonomy_v1.json
.data/exports/observation_quality_profile.current.json
```

## Expected Contract

- `taxonomy_type`: `observation_quality_taxonomy`
- `taxonomy_version`: `v1`
- dimensions for media, visibility, replay context, evidence completeness, 3D readiness, review
  readiness, annotation readiness, and provenance completeness
- neutral allowed values including `unknown`, `unavailable`, `mixed`, `sufficient_for_review`,
  `insufficient_for_review`, and `needs_human_review`
- explicit warnings that taxonomy/profile data is observation-only and no-adjudication

## Profile Semantics

The profile reads existing replay index rows only. It copies point identity, replay URL, run IDs,
evidence availability, profile counts, and provenance-only labels from the index. Visual quality is
`unknown` when media/replay context exists because the profile does not inspect video. Missing
evidence is `unavailable`. Review-support fields can be marked `sufficient_for_review` only when
existing metadata is enough to open or identify the point for review.

## Caveat

The profile can say whether evidence context exists. It cannot say whether the evidence is correct,
complete, useful, or tennis-true without human review.
