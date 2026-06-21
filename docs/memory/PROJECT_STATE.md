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
- BP55-62: Controlled runtime calibration governance through application execution mechanism.

## Latest Completed Milestone

Blueprint 62 - Controlled Runtime Calibration Application Execution v1

Status: Complete.

Commit: `33467c308b501b59784dc2da8b2ea5153723c33c`

Tag: `tom-v3-blueprint-62-controlled-runtime-calibration-application-execution-v1`

Implemented:

- Controlled runtime calibration application execution service.
- CLI commands and Make targets.
- Focused tests.
- Docs, runbook, status, and report updates.
- Post-Codex validator updates.
- Tracked BP62 contract artifacts:
  - `.data/contracts/controlled_runtime_calibration_application_execution_contract_v1.json`
  - `.data/contracts/controlled_runtime_calibration_application_execution_v1.json`
  - `.data/contracts/controlled_runtime_calibration_application_rollback_package_v1.json`
  - `.data/contracts/controlled_runtime_calibration_applied_runtime_config_v1.json`

Runtime result:

- The committed frozen BP62 path correctly blocks application because BP61 final gate is still
  blocked.
- There is no real operator signoff or selected candidate in the frozen path yet.
- Runtime target stayed unchanged before and after.
- Runtime target SHA before and after:
  `8052301c40dee448f858a3a7c64ae7805d3e7839fbbe35305044e1775f0f8fd0`

Success-path test coverage:

- The success-path test verifies controlled application only through BP62 execution.
- It includes atomic write, readback, and rollback coverage.
- Tested delta:
  - threshold `0.55 -> 0.62`
  - smoothing `3 -> 5`
  - hysteresis `0.6/0.45 -> 0.67/0.5`

## Controlled Calibration Chain

- BP55 - Controlled Runtime Calibration Change Request
- BP56 - Controlled Runtime Calibration Dry-Run Execution
- BP57 - Controlled Runtime Calibration Dry-Run Review Packet
- BP58 - Controlled Runtime Calibration Human Approval Gate
- BP59 - Controlled Runtime Calibration Application Plan
- BP60 - Controlled Runtime Calibration Runtime Application Staging
- BP61 - Controlled Runtime Calibration Pre-Application Final Gate
- BP62 - Controlled Runtime Calibration Application Execution

## Next Regular Action

After this documentation-only memory insert, resume with:

Blueprint 64 - Controlled Runtime Calibration Application Execution Review / Post-Application
Verification Packet v1

## Known Unrelated Working Tree Item

`tmp_tom_v3_tom_v1_bridge.before_review_annotation.bak`

Do not delete or modify that backup unless explicitly instructed.
