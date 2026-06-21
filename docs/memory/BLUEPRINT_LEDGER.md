# TOM v3 Blueprint Ledger

## Ledger Rules

- Only record completed, verified work.
- Do not invent project history.
- Every new blueprint entry should include status, branch, commit, tag if applicable, files or areas
  changed, validation, decision, and follow-up.
- State clearly whether the blueprint is documentation-only, runtime-facing, replay-facing,
  review-facing, calibration-facing, governance-facing, execution-facing, or regression-gate-facing.
- If a detail is not verified from repo docs, git history, or the current handoff, write
  "not yet verified in repo memory v0" rather than inventing it.

## Initial Phase Summary

- BP1-37: TOM v3 evidence, replay, review, and 3D foundation.
- BP38-45: Gameplay gate pathway.
- BP46-54: Real broadcast gameplay review and calibration decision phase.
- BP55-73: Controlled runtime calibration governance through final-gate rerun request packet state.

## Current Chain

BP55 -> BP56 -> BP57 -> BP58 -> BP59 -> BP60 -> BP61 -> BP62 -> BP63 memory insert -> BP64 -> BP65 -> BP66 -> BP67 -> BP68 -> BP69 -> BP70 -> BP71 -> BP72 -> BP73.

## Detailed Entries

### Blueprint 62 - Controlled Runtime Calibration Application Execution v1

Status: Complete.

Branch: not yet verified in repo memory v0.

Commit: `33467c308b501b59784dc2da8b2ea5153723c33c`

Tag: `tom-v3-blueprint-62-controlled-runtime-calibration-application-execution-v1`

Classification: calibration-governance-facing, runtime-execution-facing, controlled-config-facing,
rollback-facing, post-apply-verification-facing.

Files or areas changed:

- Controlled runtime calibration application execution service.
- CLI commands and Make targets.
- Tracked BP62 contract and runtime-config target artifacts.
- Docs, runbook, agent report, and focused tests.
- Post-Codex validation coverage.

Validation: not yet verified in repo memory v0.

Decision: BP62 may execute a controlled runtime config update only through the BP62 service and only
when prior gate artifacts allow it. The committed frozen path remains blocked because no real BP61
operator signoff or selected candidate is present yet.

Runtime result: blocked safely; runtime target unchanged.

Follow-up: Completed by Blueprint 64.

### Blueprint 63 - TOM v3 Repo Memory Layer v0

Status: Complete when committed.

Branch: `codex/blueprint-63-tom-v3-repo-memory-layer-v0`

Commit: recorded by the blueprint commit and final report.

Tag: `tom-v3-blueprint-63-repo-memory-layer-v0`

Classification: documentation-only, codex-workflow-facing, memory-facing, no runtime mutation.

Files or areas changed:

- `docs/memory/`
- `docs/codex-workflow/handoffs/`
- `docs/codex-workflow/retros/`

Validation: docs-only validation with `git diff --check`, `ls docs/memory`, and `git status --short`.

Decision: Repo-local Markdown memory is the first operational memory layer for TOM v3.

Follow-up: Completed by Blueprint 64.

### Blueprint 64 - Controlled Runtime Calibration Application Execution Review Packet v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-64-controlled-runtime-calibration-application-execution-review-packet-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-64-controlled-runtime-calibration-application-execution-review-packet-v1`

Classification: calibration-governance-facing, review-facing, post-execution-verification-facing,
no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration application execution review packet service.
- CLI commands and Make targets.
- Tracked BP64 contract and frozen review packet artifacts.
- Generated `.data/exports/` reports for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 64 validation recorded by final report.

Decision: BP64 packages BP62 execution results for post-execution human review only. The committed
packet represents the safe blocked path because BP61/BP62 still lack real operator signoff and a
selected candidate.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Resolve real operator signoff and selected candidate context before any future
controlled runtime application retry.

### Blueprint 65 - Controlled Runtime Calibration Blocked Execution Resolution Packet v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-65-controlled-runtime-calibration-blocked-execution-resolution-packet-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-65-controlled-runtime-calibration-blocked-execution-resolution-packet-v1`

Classification: calibration-governance-facing, blocked-execution-resolution-facing,
no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration blocked execution resolution packet service.
- CLI commands and Make targets.
- Tracked BP65 contract and frozen resolution packet artifacts.
- Generated `.data/exports/` checklists and plans for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 65 validation recorded by final report.

Decision: BP65 packages the current blocked BP64/BP62 execution state into resolution requirements
only. It does not create operator signoff, select a candidate, rerun the final gate, or retry
application execution.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Collect real operator signoff and selected candidate context, then rerun the final gate
in a future blueprint before any future application attempt.

### Blueprint 66 - Controlled Runtime Calibration Operator Signoff Candidate Selection Packet v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-66-controlled-runtime-calibration-operator-signoff-candidate-selection-packet-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-66-controlled-runtime-calibration-operator-signoff-candidate-selection-packet-v1`

Classification: calibration-governance-facing, operator-resolution-facing, candidate-selection-state-facing,
no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration operator signoff candidate selection packet service.
- CLI commands and Make targets.
- Tracked BP66 contract and frozen packet artifacts.
- Generated `.data/exports/` signoff requirements, candidate option, candidate validation, and
  readiness reports for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 66 validation recorded by final report.

Decision: BP66 records whether explicit operator signoff and selected candidate refs exist, but it
does not infer either one from available candidate options, Codex execution, validation success, or
branch state.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff and explicit selected candidate context, then rerun the
final gate in a future blueprint before any future application attempt.

### Blueprint 67 - Controlled Runtime Calibration Explicit Operator Signoff Artifact v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-67-controlled-runtime-calibration-explicit-operator-signoff-artifact-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-67-controlled-runtime-calibration-explicit-operator-signoff-artifact-v1`

Classification: calibration-governance-facing, operator-resolution-facing,
explicit-signoff-artifact-facing, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration explicit operator signoff artifact service.
- CLI commands and Make targets.
- Tracked BP67 contract and frozen signoff artifact.
- Generated `.data/exports/` inputs, validations, requirements report, attestation template, and
  readiness report for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 67 validation recorded by final report.

Decision: BP67 records whether explicit operator signoff material exists, but it does not create
signoff from Codex execution, validation success, branch state, or tags. It keeps operator identity,
operator timestamp, attestation, selected candidate, final-gate rerun, and runtime application
pending until explicit human-resolution input exists.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, then rerun the final gate in a future blueprint before any
future application attempt.

### Blueprint 73 - Controlled Runtime Calibration Final Gate Rerun Request Packet v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-73-controlled-runtime-calibration-final-gate-rerun-request-packet-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-73-controlled-runtime-calibration-final-gate-rerun-request-packet-v1`

Classification: calibration-governance-facing, final-gate-rerun-request-facing,
human-resolution-dependent, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration final-gate rerun request packet service.
- CLI commands and Make targets.
- Tracked BP73 contract and frozen request packet artifacts.
- Generated `.data/exports/` blocker, prerequisite, execution-plan, and reexecution-dependency
  reports for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 73 validation recorded by final report.

Decision: BP73 creates a request packet for a future final-gate rerun, but it does not infer
operator signoff, selected candidate, or human resolution from BP72 pending state, candidate option
discovery, a single available option, Codex execution, validation success, branch state, commits,
or tags.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, rerun the BP72 completeness gate, then create a ready BP73
request packet before rerunning the final gate in a future blueprint.

### Blueprint 72 - Controlled Runtime Calibration Human Resolution Completeness Gate v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-72-controlled-runtime-calibration-human-resolution-completeness-gate-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-72-controlled-runtime-calibration-human-resolution-completeness-gate-v1`

Classification: calibration-governance-facing, human-resolution-completeness-facing,
final-gate-readiness-facing, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration human resolution completeness gate service.
- CLI commands and Make targets.
- Tracked BP72 contract and frozen gate artifacts.
- Generated `.data/exports/` inputs, validations, missing-input matrix, operator completeness,
  candidate completeness, final-gate readiness, and reexecution readiness reports for local review
  only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 72 validation recorded by final report.

Decision: BP72 determines whether the BP71 explicit human resolution record is complete enough to
prepare a future final-gate rerun, but it does not create operator signoff, infer candidate
selection from candidate option discovery, infer human resolution, rerun the final gate, or execute
runtime application.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, rerun the BP72 completeness gate, then rerun the BP61
final gate in a future blueprint before any future application attempt.

### Blueprint 69 - Controlled Runtime Calibration Human Resolution Input Packet v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-69-controlled-runtime-calibration-human-resolution-input-packet-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-69-controlled-runtime-calibration-human-resolution-input-packet-v1`

Classification: calibration-governance-facing, human-resolution-input-facing,
operator-resolution-facing, candidate-selection-state-facing, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration human resolution input packet service.
- CLI commands and Make targets.
- Tracked BP69 contract and frozen packet artifacts.
- Generated `.data/exports/` inputs, validations, requirements report, input template, readiness
  report, and final-gate rerun prerequisite report for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 69 validation recorded by final report.

Decision: BP69 records whether explicit operator signoff material and explicit selected candidate
material exist together, but it does not infer either one from candidate option discovery, a single
available option, Codex execution, validation success, branch state, commits, or tags.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, then rerun the final gate in a future blueprint before any
future application attempt.

### Blueprint 68 - Controlled Runtime Calibration Explicit Selected Candidate Artifact v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-68-controlled-runtime-calibration-explicit-selected-candidate-artifact-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-68-controlled-runtime-calibration-explicit-selected-candidate-artifact-v1`

Classification: calibration-governance-facing, candidate-selection-state-facing,
explicit-selected-candidate-artifact-facing, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration explicit selected candidate artifact service.
- CLI commands and Make targets.
- Tracked BP68 contract and frozen selected candidate artifact.
- Generated `.data/exports/` inputs, validations, inventory report, requirements report, and
  readiness report for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 68 validation recorded by final report.

Decision: BP68 records whether explicit selected candidate material exists, but it does not infer a
selection from candidate option discovery, Codex execution, validation success, branch state, or
tags. It keeps selected candidate, operator signoff, final-gate rerun, and runtime application
pending until explicit human-resolution input exists.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, then rerun the final gate in a future blueprint before any
future application attempt.

### Blueprint 70 - Controlled Runtime Calibration Human Resolution Provided Packet v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-70-controlled-runtime-calibration-human-resolution-provided-packet-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-70-controlled-runtime-calibration-human-resolution-provided-packet-v1`

Classification: calibration-governance-facing, human-resolution-provided-facing,
operator-resolution-facing, candidate-selection-state-facing, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration human resolution provided packet service.
- CLI commands and Make targets.
- Tracked BP70 contract and frozen packet artifacts.
- Generated `.data/exports/` inputs, validations, missing-input report, completeness report,
  final-gate readiness report, and reexecution readiness report for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 70 validation recorded by final report.

Decision: BP70 records whether explicit operator signoff material and explicit selected candidate
material have actually been supplied, but it does not infer either one from BP69 pending artifacts,
candidate option discovery, a single available option, Codex execution, validation success, branch
state, commits, or tags.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, then rerun the final gate in a future blueprint before any
future application attempt.

### Blueprint 71 - Controlled Runtime Calibration Explicit Human Resolution Record v1

Status: Complete after this blueprint commit.

Branch:
`codex/blueprint-71-controlled-runtime-calibration-explicit-human-resolution-record-v1`

Commit: recorded by the blueprint commit and final report.

Tag:
`tom-v3-blueprint-71-controlled-runtime-calibration-explicit-human-resolution-record-v1`

Classification: calibration-governance-facing, explicit-human-resolution-record-facing,
operator-resolution-facing, candidate-selection-state-facing, no-runtime-mutation.

Files or areas changed:

- Controlled runtime calibration explicit human resolution record service.
- CLI commands and Make targets.
- Tracked BP71 contract and frozen record artifacts.
- Generated `.data/exports/` inputs, validations, missing-input report, completeness report,
  final-gate readiness report, and reexecution readiness report for local review only.
- Focused tests.
- Docs, runbook, agent report, status docs, and repo memory updates.
- Post-Codex validation coverage.

Validation: full Blueprint 71 validation recorded by final report.

Decision: BP71 records whether explicit human resolution fields exist in a durable record, but it
does not infer operator signoff, selected candidate, or human resolution from BP70 pending state,
candidate option discovery, a single available option, Codex execution, validation success, branch
state, commits, or tags.

Runtime result: blocked safely; runtime target unchanged before and after.

Follow-up: Provide real operator signoff identity, timestamp, attestation, scope acknowledgement,
and explicit selected candidate context, then rerun the final gate in a future blueprint before any
future application attempt.
