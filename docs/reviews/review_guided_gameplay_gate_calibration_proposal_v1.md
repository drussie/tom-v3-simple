# Review-Guided Gameplay Gate Calibration Proposal v1

Blueprint 49 adds a proposal-only planning layer over Blueprint 48 real-broadcast gameplay review
metrics.

The contract and builders support:

- calibration input snapshots from existing review metrics, review-loop, review-bundle, corpus,
  review-dataset, and regression-baseline artifacts
- read-only current threshold, smoothing window, and hysteresis settings
- model asset ref and sha256 provenance
- review coverage, missing review data, ambiguity flags, boundary cases, and fixture-only source
  context
- future-evaluation proposal items with allowed proposal types, statuses, evaluation actions, and
  risk flags
- validation that candidate settings remain not applied, do not write runtime config, do not
  affect baselines, and remain future-evaluation-only
- structural proposal reports for review planning

The tracked contract is
`.data/contracts/review_guided_gameplay_calibration_proposal_contract_v1.json`.

Generated calibration inputs, proposal validations, proposal JSON, and proposal reports live under
`.data/exports/`. They should remain local unless a future blueprint explicitly documents
committing reviewed fixture outputs.

This layer is not calibration execution. It does not prove gameplay truth, classifier accuracy,
classifier correctness, point detection, line calls, score, player identity, production readiness,
generalization, training truth, automatic relabeling, reviewer quality, or adjudication. It does
not train, tune, or mutate the local TOM v1 gameplay classifier asset and does not apply threshold,
smoothing, hysteresis, runtime config, or regression baseline changes.
