# Review-Guided Gameplay Calibration Sandbox Regression Gate v1

Blueprint 51 adds a durable regression gate for the Blueprint 50 offline calibration evaluation
sandbox.

The contract and baseline protect:

- source contract references through BP50 and earlier gameplay path artifacts
- evaluation input/report structural summaries
- candidate-setting and candidate-evaluation not-applied semantics
- blocked candidate counts and status distributions
- model asset SHA provenance
- read-only threshold, smoothing, and hysteresis metadata
- warning categories and non-claims
- fixture/demo reuse markers

Tracked artifacts:

```text
.data/contracts/review_guided_gameplay_calibration_sandbox_regression_contract_v1.json
.data/baselines/review_guided_gameplay_calibration_sandbox.baseline.json
```

Generated current summaries and reports live under `.data/exports/`.

The gate is not runtime calibration. It does not prove gameplay truth, classifier correctness,
classifier accuracy, point detection, line calls, score, player identity, production readiness,
generalization, training truth, automatic relabeling, reviewer quality, or adjudication. It does
not modify model weights, thresholds, smoothing, hysteresis, runtime config, or the gameplay gate
regression baseline.
