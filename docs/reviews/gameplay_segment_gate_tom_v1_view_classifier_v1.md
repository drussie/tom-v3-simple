# Gameplay Segment Gate / TOM v1 View Classifier Integration v1 Review

Status: complete.

Blueprint 38 adds a gameplay segment gate service, contract, classifier asset inspection, candidate
segment export, validator, report builder, CLI commands, Make targets, focused tests, and
post-Codex smoke coverage. The gate is driven by explicit media input and records the local TOM v1
gameplay classifier asset path, size, sha256, classifier ref, threshold, smoothing window,
hysteresis settings, inference mode, warnings, candidate segment statuses, and replay timeline
items.

## Review Notes

- Contract: `.data/contracts/gameplay_segment_gate_contract_v1.json`
- Local classifier asset: `model_assets/tom_v1/view_classifier_gameplay.pt`
- Asset inspection export: `.data/exports/gameplay_classifier_asset_inspection.current.json`
- Candidate export: `.data/exports/gameplay_segment_candidates.current.json`
- Candidate validation: `.data/exports/gameplay_segment_candidates.validation.json`
- Report export: `.data/exports/gameplay_segment_report.current.json`
- Default inference mode: `provenance_fixture`
- Default threshold: `0.55`
- Default smoothing window: `3`
- Default hysteresis: enter `0.60`, exit `0.45`

## Non-Goals

Blueprint 38 does not create tennis truth, in/out, score, point winners, player identity,
server/receiver state, rally state, line-call truth, point truth, event truth, accepted/rejected
lifecycle, marker arbitration, coaching/tactical conclusions, betting/prediction outcomes,
automatic correctness, training truth, production truth, or adjudication. It does not mutate or
commit the local model asset and does not run downstream detection, tracklet, pose, court, event,
or 3D jobs.
