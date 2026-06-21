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
-> controlled runtime calibration explicit selected candidate artifact state
-> controlled runtime calibration human resolution input packet state
-> controlled runtime calibration human resolution provided packet state
-> controlled runtime calibration explicit human resolution record state
-> controlled runtime calibration human resolution completeness gate state
-> controlled runtime calibration final-gate rerun request packet state
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
- BP55-73: Controlled runtime calibration governance through final-gate rerun request packet state.

## Latest Completed Milestone

Blueprint 73 - Controlled Runtime Calibration Final Gate Rerun Request Packet v1

Status: Complete.

Commit: recorded by the Blueprint 73 commit.

Tag:
`tom-v3-blueprint-73-controlled-runtime-calibration-final-gate-rerun-request-packet-v1`

Implemented:

- Controlled runtime calibration final-gate rerun request packet service.
- CLI commands and Make targets.
- Focused tests.
- Docs, runbook, status, and report updates.
- Post-Codex validator updates.
- Tracked BP73 contract artifacts:
  - `.data/contracts/controlled_runtime_calibration_final_gate_rerun_request_packet_contract_v1.json`
  - `.data/contracts/controlled_runtime_calibration_final_gate_rerun_request_packet_v1.json`

Runtime result:

- The committed frozen BP73 request packet correctly represents the incomplete human resolution
  state after BP72, BP71, BP70, BP69, BP68, BP67, and BP66.
- There is still no real operator signoff or selected candidate in the frozen path.
- BP73 preserves one discovered candidate option as inventory only and does not select from it.
- BP73 records missing human inputs, final-gate rerun request blockers, prerequisites, future
  execution plan, and reexecution dependencies.
- Runtime target stayed unchanged before and after.
- Runtime target SHA before and after:
  `8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0`
- Final gate rerun request status:
  `final_gate_rerun_request_blocked_missing_human_resolution`
- Human resolution completeness gate status:
  `human_resolution_completeness_gate_not_ready`
- Human resolution record status: `human_resolution_record_pending_explicit_inputs`
- Human resolution provided status: `human_resolution_not_provided`
- Human resolution completeness status: `human_resolution_incomplete`
- Missing input status: `required_human_inputs_missing`
- Operator input completeness status: `operator_inputs_incomplete`
- Candidate input completeness status: `candidate_inputs_incomplete`
- Operator signoff status: `operator_signoff_required`
- Operator attestation status: `operator_attestation_required`
- Operator identity status: `operator_identity_required`
- Operator timestamp status: `operator_timestamp_required`
- Selected candidate status: `selected_candidate_required`
- Candidate selection validation status: `candidate_selection_pending_explicit_input`
- Candidate option count: 1
- Final gate rerun status: `final_gate_rerun_required`
- Final gate rerun readiness status: `final_gate_rerun_not_ready_missing_human_resolution`
- Final gate rerun execution status: `final_gate_rerun_not_executed`
- Reexecution readiness status: `reexecution_not_ready_blockers_unresolved`
- Runtime application status: `not_executed`
- Next action recommendations:
  `provide_operator_inputs`, `provide_selected_candidate_inputs`,
  `provide_operator_signoff_and_selected_candidate`, and `rerun_final_gate_after_human_resolution`

Final-gate rerun request packet test coverage:

- Current BP72/BP71/BP70/BP69/BP68/BP67/BP66 pending request-packet path.
- Blocker report, prerequisite report, execution plan, and reexecution dependency report generation.
- Future complete-human-resolution request readiness without final-gate execution or runtime
  mutation.

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
- BP68 - Controlled Runtime Calibration Explicit Selected Candidate Artifact
- BP69 - Controlled Runtime Calibration Human Resolution Input Packet
- BP70 - Controlled Runtime Calibration Human Resolution Provided Packet
- BP71 - Controlled Runtime Calibration Explicit Human Resolution Record
- BP72 - Controlled Runtime Calibration Human Resolution Completeness Gate
- BP73 - Controlled Runtime Calibration Final Gate Rerun Request Packet

## Next Regular Action

Provide real operator signoff identity, timestamp, attestation, scope acknowledgement, and an
explicit selected candidate ref with provenance, then rerun the BP72 completeness gate and create a
new BP73 request packet that becomes ready before rerunning the BP61 final gate in a future
blueprint. Do not attempt runtime application while the
BP61/BP62/BP64/BP65/BP66/BP67/BP68/BP69/BP70/BP71/BP72/BP73 chain remains blocked.

## Known Unrelated Working Tree Item

`tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`

Do not delete or modify that backup unless explicitly instructed.
