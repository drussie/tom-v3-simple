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
-> controlled runtime calibration final-gate rerun execution blocked-result state
-> controlled runtime calibration reexecution request packet state
-> controlled runtime calibration reexecution execution blocked-result state
-> controlled runtime calibration post-reexecution verification not-available packet state
-> controlled runtime calibration blocked pathway phase-freeze state
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
- BP55-78: Controlled runtime calibration governance through blocked pathway phase-freeze state.

## Latest Completed Milestone

Blueprint 78 - Controlled Runtime Calibration Blocked Pathway Phase Freeze v1

Status: Complete.

Commit: recorded by the Blueprint 78 commit.

Tag:
`tom-v3-blueprint-78-controlled-runtime-calibration-blocked-pathway-phase-freeze-v1`

Implemented:

- Controlled runtime calibration blocked pathway phase-freeze service.
- CLI commands and Make targets.
- Focused tests.
- Docs, runbook, status, and report updates.
- Post-Codex validator updates.
- Tracked BP78 contract artifacts:
  - `.data/contracts/controlled_runtime_calibration_blocked_pathway_phase_freeze_contract_v1.json`
  - `.data/contracts/controlled_runtime_calibration_blocked_pathway_phase_freeze_v1.json`

Runtime result:

- The committed frozen BP78 blocked pathway phase-freeze correctly records that the current
  controlled calibration pathway is complete for the blocked/no-human-resolution path only.
- Successful runtime calibration remains incomplete.
- There is still no real operator signoff or selected candidate in the frozen path.
- BP78 preserves the one discovered candidate option from upstream inventory only and does not
  select from it.
- BP78 records blocked pathway completion, unresolved human inputs, runtime non-mutation evidence,
  successful-pathway remaining work, and future-unblock readiness.
- Runtime target stayed unchanged before and after.
- Runtime target SHA before and after:
  `8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0`
- Blocked pathway phase-freeze status:
  `blocked_pathway_phase_freeze_completed`
- Blocked pathway completion status: `complete_for_blocked_pathway`
- Successful pathway completion status:
  `incomplete_pending_explicit_human_resolution`
- Successful calibration application status: `not_completed`
- Human resolution status: `human_resolution_missing`
- Operator signoff status: `operator_signoff_required`
- Selected candidate status: `selected_candidate_required`
- Final gate rerun status: `final_gate_rerun_not_performed`
- Reexecution status: `reexecution_not_performed`
- Post-reexecution verification status:
  `post_reexecution_verification_not_available`
- Final gate rerun result status: `final_gate_rerun_result_not_available`
- Candidate option count: 1
- Runtime application status: `not_executed`
- Runtime config changed: `false`
- Mutation status: `no_runtime_mutation_due_to_blocker`
- Next action recommendations:
  `stop_blocked_calibration_pathway`, `provide_operator_signoff_and_selected_candidate`,
  `successful_pathway_requires_new_human_resolution_cycle`,
  `rerun_final_gate_after_human_resolution`, and `no_runtime_action_recommended`.

Blocked pathway phase-freeze test coverage:

- Current BP77/BP76/BP75/BP74/BP73/BP72/BP71/BP70/BP69/BP68/BP67/BP66 pending blocked path.
- Blocked pathway completion, unresolved human inputs, runtime non-mutation evidence,
  successful-pathway remaining work, and future-unblock readiness report generation.
- Rejection of fabricated successful runtime calibration completion while human resolution is
  missing.

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
- BP74 - Controlled Runtime Calibration Final Gate Rerun Execution Blocked Result
- BP75 - Controlled Runtime Calibration Reexecution Request Packet
- BP76 - Controlled Runtime Calibration Reexecution Execution Blocked Result
- BP77 - Controlled Runtime Calibration Post-Reexecution Verification Not Available Packet
- BP78 - Controlled Runtime Calibration Blocked Pathway Phase Freeze

## Next Regular Action

The blocked calibration pathway is frozen. Either stop this blocked pathway, or start a new
explicit human-resolution cycle with real operator signoff identity, timestamp, attestation, scope
acknowledgement, and an explicit selected candidate ref with provenance. Only after that cycle can
the project rerun BP72 and rebuild ready/non-blocked BP73/BP74/BP75/BP76/BP77 outputs. Do not
attempt runtime application while the current BP61-BP78 chain remains blocked.

## Known Unrelated Working Tree Item

`tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`

Do not delete or modify that backup unless explicitly instructed.
