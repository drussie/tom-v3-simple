# TOM v3 Project State

TOM v3 is an observation-first tennis evidence platform.

Its current purpose is to store, index, replay, export, and review tennis evidence while preserving
uncertainty, provenance, confidence, source, frame/time, lineage, and review status. TOM v3 does not
claim tennis truth by default, and it must not silently become a truth-adjudication system.

## Current Architecture

The current architecture grows through this evidence and review chain:

```text
video/media
-> observations
-> evidence persistence
-> replay workstation
-> review annotations
-> point evidence snapshots
-> evaluation harness
-> camera geometry evidence
-> 3D trajectory diagnostics
-> gameplay gate
-> real-broadcast review
-> calibration decision support
-> controlled runtime calibration governance
-> controlled runtime calibration execution mechanism
-> controlled runtime calibration post-execution review
-> controlled runtime calibration blocked-execution resolution requirements
-> controlled runtime calibration operator signoff / candidate selection packet state
-> controlled runtime calibration explicit operator signoff artifact state
```

The current principle is to expand safely from reviewed sample evidence toward broader replay,
runtime capability, controlled calibration, and post-application review without losing provenance or
auditability.

The current risk is convenience work that turns TOM into a truth engine or an uncontrolled runtime
mutation system. Runtime changes must remain explicitly governed.

## Completed Blueprint Areas

- BP1-37: TOM v3 evidence, replay, review, and 3D foundation.
- BP38-45: Gameplay gate pathway.
- BP46-54: Real broadcast gameplay review and calibration decision phase.
- BP55-67: Controlled runtime calibration governance through explicit operator signoff artifact
  state.

## Latest Completed Milestone

Blueprint 67 - Controlled Runtime Calibration Explicit Operator Signoff Artifact v1

Status: Complete.

Commit: recorded by the Blueprint 67 commit.

Tag:
`tom-v3-blueprint-67-controlled-runtime-calibration-explicit-operator-signoff-artifact-v1`

Implemented:

- Controlled runtime calibration explicit operator signoff artifact service.
- CLI commands and Make targets.
- Focused tests.
- Docs, runbook, status, and report updates.
- Post-Codex validator updates.
- Tracked BP67 contract artifacts:
  - `.data/contracts/controlled_runtime_calibration_explicit_operator_signoff_artifact_contract_v1.json`
  - `.data/contracts/controlled_runtime_calibration_explicit_operator_signoff_artifact_v1.json`

Runtime result:

- The committed frozen BP67 artifact correctly represents the pending explicit operator signoff,
  operator identity, operator timestamp, operator attestation, and selected candidate state after
  BP66.
- There is still no real operator signoff or selected candidate in the frozen path.
- BP67 creates a pending artifact and attestation template but does not satisfy signoff.
- BP67 records operator signoff requirements, attestation requirements, signoff readiness,
  final-gate rerun readiness, and reexecution readiness.
- Runtime target stayed unchanged before and after.
- Runtime target SHA before and after:
  `8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0`
- Signoff artifact status: `signoff_artifact_created_pending_explicit_operator_input`
- Operator signoff status: `operator_signoff_required`
- Operator attestation status: `operator_attestation_required`
- Operator identity status: `operator_identity_required`
- Operator timestamp status: `operator_timestamp_required`
- Candidate selection status: `selected_candidate_required`
- Final gate rerun status: `final_gate_rerun_required`
- Reexecution readiness status: `reexecution_not_ready_blockers_unresolved`
- Runtime application status: `not_executed`
- Next action recommendations:
  `provide_explicit_operator_signoff`, `provide_operator_identity_and_attestation`,
  `provide_selected_candidate`, and
  `rerun_final_gate_after_signoff_and_candidate_selection`

Explicit operator signoff artifact test coverage:

- Current BP66 pending operator signoff / selected candidate path.
- Operator signoff requirements, attestation template, and readiness report generation.
- Incomplete explicit operator signoff rejection.

## Controlled Calibration Chain

- BP55 - Controlled Runtime Calibration Change Request
- BP56 - Controlled Runtime Calibration Dry-Run Execution
- BP57 - Controlled Runtime Calibration Dry-Run Review Packet
- BP58 - Controlled Runtime Calibration Human Approval Gate
- BP59 - Controlled Runtime Calibration Application Plan
- BP60 - Controlled Runtime Calibration Runtime Application Staging
- BP61 - Controlled Runtime Calibration Pre-Application Final Gate
- BP62 - Controlled Runtime Calibration Application Execution
- BP63 - TOM v3 Repo Memory Layer
- BP64 - Controlled Runtime Calibration Application Execution Review Packet
- BP65 - Controlled Runtime Calibration Blocked Execution Resolution Packet
- BP66 - Controlled Runtime Calibration Operator Signoff Candidate Selection Packet
- BP67 - Controlled Runtime Calibration Explicit Operator Signoff Artifact

## Next Regular Action

Use the BP67 artifact/template to collect real operator signoff identity, timestamp, attestation,
scope acknowledgement, and an explicit selected candidate ref, then rerun the BP61 final gate in a
future blueprint. Do not attempt runtime application while the BP61/BP62/BP64/BP65/BP66/BP67 chain
remains blocked.

## Known Unrelated Working Tree Item

`tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`

Do not delete or modify that backup unless explicitly instructed.
