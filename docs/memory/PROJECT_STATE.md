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
- BP55-68: Controlled runtime calibration governance through explicit selected candidate artifact
  state.

## Latest Completed Milestone

Blueprint 68 - Controlled Runtime Calibration Explicit Selected Candidate Artifact v1

Status: Complete.

Commit: recorded by the Blueprint 68 commit.

Tag:
`tom-v3-blueprint-68-controlled-runtime-calibration-explicit-selected-candidate-artifact-v1`

Implemented:

- Controlled runtime calibration explicit selected candidate artifact service.
- CLI commands and Make targets.
- Focused tests.
- Docs, runbook, status, and report updates.
- Post-Codex validator updates.
- Tracked BP68 contract artifacts:
  - `.data/contracts/controlled_runtime_calibration_explicit_selected_candidate_artifact_contract_v1.json`
  - `.data/contracts/controlled_runtime_calibration_explicit_selected_candidate_artifact_v1.json`

Runtime result:

- The committed frozen BP68 artifact correctly represents the pending explicit selected candidate
  state after BP67 and BP66.
- There is still no real operator signoff or selected candidate in the frozen path.
- BP68 preserves one discovered candidate option as inventory only and does not select from it.
- BP68 records candidate option inventory, selected candidate requirements, selected candidate
  readiness, final-gate rerun readiness, and reexecution readiness.
- Runtime target stayed unchanged before and after.
- Runtime target SHA before and after:
  `8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0`
- Selected candidate artifact status:
  `selected_candidate_artifact_created_pending_explicit_candidate_input`
- Selected candidate status: `selected_candidate_required`
- Candidate selection validation status: `candidate_selection_pending_explicit_input`
- Candidate option count: 1
- Operator signoff status: `operator_signoff_required`
- Final gate rerun status: `final_gate_rerun_required`
- Reexecution readiness status: `reexecution_not_ready_blockers_unresolved`
- Runtime application status: `not_executed`
- Next action recommendations:
  `provide_explicit_selected_candidate`, `provide_explicit_operator_signoff`, and
  `rerun_final_gate_after_signoff_and_candidate_selection`

Explicit selected candidate artifact test coverage:

- Current BP67/BP66 pending selected candidate path.
- Candidate option inventory, selection requirements, and readiness report generation.
- Invalid explicit selected candidate rejection.

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

## Next Regular Action

Provide real operator signoff identity, timestamp, attestation, scope acknowledgement, and an
explicit selected candidate ref with provenance, then rerun the BP61 final gate in a future
blueprint. Do not attempt runtime application while the BP61/BP62/BP64/BP65/BP66/BP67/BP68 chain
remains blocked.

## Known Unrelated Working Tree Item

`tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`

Do not delete or modify that backup unless explicitly instructed.
