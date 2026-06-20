# Calibration Candidate Decision Packet v1

Blueprint 52 creates a structural decision-support packet for calibration candidates.

The packet combines:

- Blueprint 49 calibration proposal items
- Blueprint 50 offline sandbox candidate evaluations
- Blueprint 51 sandbox regression verification
- optional Blueprint 48 review metrics, Blueprint 47 review-loop, Blueprint 46 corpus-run, and
  Blueprint 43 baseline context
- model asset reference and SHA provenance when available

Tracked artifact:

```text
.data/contracts/calibration_candidate_decision_packet_contract_v1.json
```

Generated local artifacts:

```text
.data/exports/calibration_candidate_decision_packet_inputs.current.json
.data/exports/calibration_candidate_decision_packet_inputs.validation.json
.data/exports/calibration_candidate_decision_packet.current.json
.data/exports/calibration_candidate_decision_packet.validation.json
.data/exports/calibration_candidate_decision_packet.report.json
```

Each candidate packet includes candidate type, candidate status, sandbox evaluation status,
sandbox regression status, baseline comparison status, review coverage status, decision-support
status, operator review status, blockers, risk flags, evidence refs, provenance status, and
warnings.

Every candidate remains `not_applied: true`, and candidate runtime status remains `not_applied`.
Operator next actions are review-support prompts only.

The packet is not runtime calibration. It does not prove gameplay truth, classifier correctness,
classifier accuracy, point detection, line calls, score, player identity, production readiness,
generalization, training truth, automatic relabeling, reviewer quality, or adjudication. It does
not modify model weights, thresholds, smoothing, hysteresis, runtime config, or baselines.
