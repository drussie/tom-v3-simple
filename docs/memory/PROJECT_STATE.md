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
- BP55-65: Controlled runtime calibration governance through blocked execution resolution packet.

## Latest Completed Milestone

Blueprint 65 - Controlled Runtime Calibration Blocked Execution Resolution Packet v1

Status: Complete.

Commit: recorded by the Blueprint 65 commit.

Tag: `tom-v3-blueprint-65-controlled-runtime-calibration-blocked-execution-resolution-packet-v1`

Implemented:

- Controlled runtime calibration blocked execution resolution packet service.
- CLI commands and Make targets.
- Focused tests.
- Docs, runbook, status, and report updates.
- Post-Codex validator updates.
- Tracked BP65 contract artifacts:
  - `.data/contracts/controlled_runtime_calibration_blocked_execution_resolution_packet_contract_v1.json`
  - `.data/contracts/controlled_runtime_calibration_blocked_execution_resolution_packet_v1.json`

Runtime result:

- The committed frozen BP65 packet correctly represents the blocked BP64/BP62 execution review.
- There is still no real operator signoff or selected candidate in the frozen path.
- BP65 packages the required future operator signoff, selected candidate context, final-gate rerun,
  and future reexecution prerequisites.
- Runtime target stayed unchanged before and after.
- Runtime target SHA before and after:
  `8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0`
- Resolution packet status: `resolution_packet_created_for_blocked_execution`
- Application outcome status: `application_blocked_safely_before_runtime_mutation`
- Next action recommendations:
  `resolve_operator_signoff_before_reapplying`, `select_candidate_before_reapplying`, and
  `rerun_final_gate_after_resolution`

Resolution-packet test coverage:

- Current BP64 blocked execution review path.
- Blocker checklist, operator action plan, candidate requirements, final-gate rerun plan, and
  reexecution readiness plan generation.
- Forbidden token rejection.

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

## Next Regular Action

Use the BP65 resolution packet to collect real operator signoff, select an explicit candidate, and
rerun the final gate before any future controlled runtime application retry. Do not attempt runtime
application while the BP61/BP62/BP64/BP65 chain remains blocked.

## Known Unrelated Working Tree Item

`tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`

Do not delete or modify that backup unless explicitly instructed.
