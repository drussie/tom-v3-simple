# Gameplay-Gated Perception Execution Hook v1

Status: complete

Blueprint 40 turns Blueprint 39 routing rows into perception-stage execution constraints. It
preserves allowed gameplay windows, skipped non-gameplay windows, review-required windows, skip
reasons, routing warnings, segment warnings, and provenance refs.

The hook is structural by default. `dry_run` and `plan_only` do not run perception jobs or write
observations. `fixture_execution_only` can attach non-mutating fixture output refs for allowed
windows, but those refs are placeholders and do not represent model inference.

Boundary:

- no tennis truth
- no in/out
- no score
- no point winner
- no player identity
- no line-call conclusion
- no accepted/rejected lifecycle
- no marker arbitration
- no coaching/tactical conclusion
- no betting/prediction
- no generalization claim
- no training truth
- no adjudication

Generated execution artifacts live under `.data/exports/`. The tracked contract lives at
`.data/contracts/gameplay_gated_perception_execution_contract_v1.json`.
