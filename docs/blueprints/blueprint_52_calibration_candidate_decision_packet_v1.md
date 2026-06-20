# Blueprint 52 - Calibration Candidate Decision Packet v1

Status: complete

## Goal

Blueprint 52 packages Blueprint 49 through Blueprint 51 calibration outputs into one
operator-facing decision-support packet.

```text
BP49 calibration proposal
-> BP50 offline sandbox report
-> BP51 sandbox regression verification
-> BP52 packet inputs
-> BP52 decision packet
-> BP52 packet report
```

The packet describes candidate settings, blockers, source artifacts, model asset provenance,
regression gate status, review coverage, and operator next actions. It keeps every candidate
marked `not_applied` and records `runtime_change_status: not_applied`.

## Tracked Artifacts

```text
.data/contracts/calibration_candidate_decision_packet_contract_v1.json
```

Generated packet inputs, validations, decision packets, and reports live under `.data/exports/`
and remain local.

## Commands

```bash
make tom-v1-export-calibration-candidate-decision-packet-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-calibration-candidate-decision-packet-inputs \
  PYTHON=.venv/bin/python

make tom-v1-validate-calibration-candidate-decision-packet-inputs \
  PYTHON=.venv/bin/python

make tom-v1-build-calibration-candidate-decision-packet \
  PYTHON=.venv/bin/python

make tom-v1-validate-calibration-candidate-decision-packet \
  PYTHON=.venv/bin/python

make tom-v1-build-calibration-candidate-decision-packet-report \
  PYTHON=.venv/bin/python
```

## Boundaries

Blueprint 52 is a decision packet only. It does not decide tennis truth, in/out, score, point
winner, player identity, rally state, server/receiver state, line-call truth, point truth, event
truth, gameplay truth, classifier correctness, classifier accuracy, accepted/rejected lifecycle,
automatic relabeling, reviewer ranking or quality scoring, coaching/tactical conclusions,
betting/prediction outcomes, generalization, automatic correctness, training truth, production
truth, or adjudication.

It does not apply threshold, smoothing, or hysteresis changes. It does not update runtime config,
modify model weights, replace baselines, or select a candidate for runtime use. A human operator
decision remains required for any future manual review workflow.
