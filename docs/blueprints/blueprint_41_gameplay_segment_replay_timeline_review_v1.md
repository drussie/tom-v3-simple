# Blueprint 41 - Gameplay Segment Replay Timeline / Operator Review v1

Status: complete

## Purpose

Blueprint 41 makes Blueprint 38 gameplay segment candidates, Blueprint 39 routing windows, and
Blueprint 40 perception execution windows visible as replay-review timeline artifacts. The
timeline is an operator review surface only: it helps a human inspect candidate gameplay,
non-gameplay, uncertain, allowed, blocked, review-required, executed, and skipped windows without
creating tennis truth.

## Added

- `apps.worker.services.gameplay_segment_replay_review`
- `export-gameplay-segment-replay-review-contract`
- `build-gameplay-segment-replay-timeline`
- `validate-gameplay-segment-replay-timeline`
- `build-gameplay-segment-review-template`
- `validate-gameplay-segment-review-bundle`
- `build-gameplay-segment-review-report`
- `tom-v1-export-gameplay-segment-replay-review-contract`
- `tom-v1-build-gameplay-segment-replay-timeline`
- `tom-v1-validate-gameplay-segment-replay-timeline`
- `tom-v1-build-gameplay-segment-review-template`
- `tom-v1-validate-gameplay-segment-review-bundle`
- `tom-v1-build-gameplay-segment-review-report`
- `.data/contracts/gameplay_segment_replay_review_contract_v1.json`

Generated timeline, template, validation, and report artifacts live under `.data/exports/` and
remain local/untracked by default.

## Contract

The tracked contract defines replay review scope, source contract refs, timeline lane schema,
review template schema, review bundle schema, validation rules, provenance requirements, and
warnings. It references Blueprint 38, Blueprint 39, and Blueprint 40 contract versions.

Allowed lane types include gameplay candidate, non-gameplay candidate, uncertain segment,
downstream allowed, downstream blocked, downstream review required, perception execution window,
and perception skipped window.

Allowed review statuses are human metadata only:

- `not_reviewed`
- `review_optional`
- `review_needed`
- `reviewed_as_gameplay_candidate`
- `reviewed_as_non_gameplay_candidate`
- `reviewed_as_uncertain`
- `needs_additional_review`
- `not_applicable`

## Boundary

Blueprint 41 does not decide in/out, score, point winner, player identity, rally state,
server/receiver state, line-call truth, point truth, event truth, classifier correctness,
accepted/rejected lifecycle, marker arbitration, coaching/tactical conclusions, betting
prediction, generalization, training truth, production truth, or adjudication. It does not run
GPU/model inference, write observations, mutate model assets, or mutate regression baselines.
