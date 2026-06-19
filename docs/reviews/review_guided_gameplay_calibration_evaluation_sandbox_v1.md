# Review-Guided Gameplay Calibration Evaluation Sandbox v1

Blueprint 50 adds an offline-only evaluation sandbox over Blueprint 49 calibration proposals.

The contract and builders support:

- evaluation input snapshots from existing calibration proposals, review metrics, review-loop,
  review-bundle, corpus-run, and regression-baseline artifacts
- read-only current threshold, smoothing window, and hysteresis settings
- model asset ref and sha256 provenance
- candidate settings derived from proposal items, with explicit blocked/ready/informational status
- structural offline sandbox reports with drift summaries and review-data limitations
- report validation and compact summaries for future review workflows
- validation that candidates remain not applied, do not write runtime config, do not mutate model
  assets, and do not replace baselines

The tracked contract is
`.data/contracts/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.json`.

Generated evaluation inputs, validation snapshots, sandbox reports, and summaries live under
`.data/exports/`. They should remain local unless a future blueprint explicitly documents
committing reviewed fixture outputs.

This layer is not calibration application. It does not prove gameplay truth, classifier accuracy,
classifier correctness, point detection, line calls, score, player identity, production readiness,
generalization, training truth, automatic relabeling, reviewer quality, or adjudication. It does
not train, tune, or mutate the local TOM v1 gameplay classifier asset and does not apply threshold,
smoothing, hysteresis, runtime config, or regression baseline changes.
