# Blueprint 26 Observation Quality Taxonomy v1

Status: complete

Blueprint 26 adds a versioned observation-quality taxonomy and a conservative profile builder over
existing Blueprint 24 multi-point replay indexes. The profile makes point manifests easier to use
for future review surfaces by describing which quality dimensions are known, unknown, unavailable,
or ready for human review.

This milestone is a contract and profiling layer only. It does not inspect video, create
observations, generate event candidates, generate 3D candidates, decide in/out, score, identify
players, determine point winners, claim generalization, or adjudicate evidence.

## Commands

Export the taxonomy contract:

```bash
.venv/bin/python -m apps.worker.cli export-observation-quality-taxonomy \
  --output ".data/contracts/observation_quality_taxonomy_v1.json" \
  --skip-create-db
```

Build a profile from the current multi-point replay index:

```bash
.venv/bin/python -m apps.worker.cli build-observation-quality-profile \
  --index ".data/manifests/multi_point_replay_index.json" \
  --output ".data/exports/observation_quality_profile.current.json" \
  --skip-create-db
```

Make helpers:

```bash
make tom-v1-export-observation-quality-taxonomy PYTHON=.venv/bin/python
make tom-v1-build-observation-quality-profile PYTHON=.venv/bin/python
```

## Paths

Default local paths:

```text
.data/contracts/observation_quality_taxonomy_v1.json
.data/exports/observation_quality_profile.current.json
```

Generated `.data` artifacts are local outputs and should not be committed unless intentionally
freezing a reviewed contract artifact.

## Taxonomy Contract

The taxonomy records:

- `taxonomy_type`: `observation_quality_taxonomy`
- `taxonomy_version`: `v1`
- exported timestamp
- dimension definitions
- allowed neutral values
- TOM/Blueprint provenance
- explicit no-truth/no-adjudication warnings

Dimensions:

- `media_quality`
- `camera_stability`
- `court_visibility`
- `ball_visibility`
- `player_visibility`
- `occlusion`
- `motion_blur`
- `lighting`
- `frame_continuity`
- `replay_context_completeness`
- `evidence_completeness`
- `calibration_readiness`
- `trajectory_3d_readiness`
- `review_readiness`
- `annotation_readiness`
- `provenance_completeness`

Allowed values are neutral review-support labels such as `unknown`, `unavailable`, `mixed`,
`sufficient_for_review`, `insufficient_for_review`, and `needs_human_review`.

## Profile Behavior

The profile reads an existing multi-point replay index only. For each point, it preserves:

- point manifest ID
- media ID
- provenance-only labels
- manifest path
- replay URL
- source/storage media paths or URIs when present
- associated run IDs
- evidence availability
- profile counts
- quality dimensions
- warning flags

Visual dimensions are `unknown` when media or replay context exists because the service does not
inspect video content. Missing evidence is `unavailable`. Replay/provenance completeness may be
`sufficient_for_review` when the index already carries enough metadata to open and review the
point. Quality dimensions that cannot be known from artifacts set `requires_human_review`.

## Summary

The profile summary records:

- `point_count`
- `replay_available_count`
- `review_ready_count`
- `unknown_quality_count`
- `requires_human_review_count`

These counts are review-support summaries only. They are not correctness metrics, scoring metrics,
or training labels.

## Boundaries

Blueprint 26 does not add or change:

- in/out
- score
- point winner
- player identity
- rally state
- server or receiver state
- accepted/rejected lifecycle
- marker arbitration
- event generation
- 3D generation
- coaching or tactical conclusions
- adjudication
- betting or prediction
- generalization claims

The taxonomy and profile support future review workflows, but they do not establish truth.
