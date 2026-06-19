# Real Broadcast Gameplay Gate Corpus Run v1

Blueprint 46 adds an explicit local-media corpus run layer over the frozen gameplay gate pathway.

The contract and runner support:

- explicit broadcast-style media entries
- expected broadcast context tags that are not truth labels
- dry-run and validate-only defaults
- fixture-only CI/demo runs
- explicit real local media modes that require an input manifest
- gameplay segment candidates, routing plans, execution plans, replay timelines, and review
  dataset exports as structural artifacts
- a corpus run summary and human review readiness report

The tracked contract is
`.data/contracts/real_broadcast_gameplay_corpus_run_contract_v1.json`.

Generated manifests, validations, per-entry artifacts, corpus run outputs, and reports live under
`.data/exports/`. They should remain local unless a future blueprint explicitly documents
committing a reviewed corpus fixture.

This review surface is not classifier scoring. It does not prove gameplay truth, classifier
accuracy, classifier correctness, point detection, line calls, score, player identity, production
readiness, generalization, training truth, or adjudication. It does not train or mutate the local
TOM v1 gameplay classifier asset.
