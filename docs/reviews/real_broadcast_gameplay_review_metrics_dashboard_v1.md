# Real Broadcast Gameplay Review Metrics / QA Dashboard v1

Blueprint 48 adds a metrics and QA dashboard layer over Blueprint 47 real-broadcast gameplay
review loop outputs.

The contract and builders support:

- reviewed vs unreviewed operational coverage metrics
- reviewed segment status distributions
- downstream allow/block/additional-review decision counts
- reviewer confidence distributions
- ambiguity flag counts
- missing human review field counts
- review readiness and replay context coverage
- source corpus entry coverage and model asset provenance
- dashboard-ready cards/tables
- next-review action suggestions for review operations only

The tracked contract is
`.data/contracts/real_broadcast_gameplay_review_metrics_contract_v1.json`.

Generated metrics reports, validations, QA dashboard JSON, and next-actions reports live under
`.data/exports/`. They should remain local unless a future blueprint explicitly documents
committing reviewed fixture outputs.

This metrics layer is not classifier scoring. It does not prove gameplay truth, classifier
accuracy, classifier correctness, point detection, line calls, score, player identity, production
readiness, generalization, training truth, automatic relabeling, reviewer quality, or
adjudication. It does not train or mutate the local TOM v1 gameplay classifier asset.
