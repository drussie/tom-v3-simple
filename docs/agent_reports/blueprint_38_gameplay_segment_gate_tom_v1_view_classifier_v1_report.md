# Blueprint 38 Agent Report - Gameplay Segment Gate / TOM v1 View Classifier Integration v1

## Summary

Implemented Blueprint 38 as a candidate-only gameplay segment gate around the existing local TOM
v1 gameplay classifier asset. The new service exports a stable gate contract, inspects and hashes
the local classifier asset when present, builds explicit-media candidate segment artifacts with
temporal smoothing and hysteresis metadata, validates contract/candidate shape, and emits a
structural report plus replay timeline lane data for future downstream gate use.

## Added

- `apps.worker.services.gameplay_segment_gate`
- Worker CLI commands:
  - `export-gameplay-segment-gate-contract`
  - `inspect-gameplay-classifier-asset`
  - `build-gameplay-segment-candidates`
  - `validate-gameplay-segment-candidates`
  - `build-gameplay-segment-report`
- Make targets:
  - `tom-v1-export-gameplay-segment-gate-contract`
  - `tom-v1-inspect-gameplay-classifier-asset`
  - `tom-v1-build-gameplay-segment-candidates`
  - `tom-v1-validate-gameplay-segment-candidates`
  - `tom-v1-build-gameplay-segment-report`
- Tracked gate contract:
  - `.data/contracts/gameplay_segment_gate_contract_v1.json`
- Focused tests:
  - `tests/test_gameplay_segment_gate.py`
- Post-Codex validation smokes for BP38.

## Boundary

Blueprint 38 creates candidate segment artifacts and structural downstream gate statuses only. It
does not create truth, scoring, point winners, player identity, line calls, event labels, point
labels, review lifecycle decisions, marker arbitration, downstream perception jobs, model
training, model asset mutations, regression baseline mutations, generalization claims, automatic
correctness claims, or adjudication.
