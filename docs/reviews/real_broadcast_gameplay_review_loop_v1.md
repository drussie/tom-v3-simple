# Real Broadcast Gameplay Review Loop v1

Blueprint 47 adds a human review metadata loop over Blueprint 46 real-broadcast gameplay corpus
outputs.

The contract and builder support:

- review bundle templates from BP46 corpus run outputs and BP44 review dataset entries
- preserved replay URLs, segment timestamps, classifier probabilities, segment statuses, routing
  decisions, execution decisions, baseline context, and expected broadcast context tags
- blank or not-assessed human review fields
- allowed reviewed segment statuses, downstream gate review statuses, confidence values,
  ambiguity flags, and review sources
- structural bundle validation
- review-loop coverage reports and human review readiness reports

The tracked contract is
`.data/contracts/real_broadcast_gameplay_review_loop_contract_v1.json`.

Generated review bundles, validations, and reports live under `.data/exports/`. They should remain
local unless a future blueprint explicitly documents committing a reviewed fixture.

This review loop is not classifier scoring. It does not prove gameplay truth, classifier accuracy,
classifier correctness, point detection, line calls, score, player identity, production readiness,
generalization, training truth, automatic relabeling, reviewer quality, or adjudication. It does
not train or mutate the local TOM v1 gameplay classifier asset.
