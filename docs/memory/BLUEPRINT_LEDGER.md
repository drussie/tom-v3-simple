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
- BP55-62: Controlled runtime calibration governance and execution mechanism.

## Current Chain

BP55 -> BP56 -> BP57 -> BP58 -> BP59 -> BP60 -> BP61 -> BP62 -> BP63 memory insert -> BP64
next.

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

Follow-up: Resume with Blueprint 64 - Controlled Runtime Calibration Application Execution Review /
Post-Application Verification Packet v1.

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

Follow-up: Resume with Blueprint 64 - Controlled Runtime Calibration Application Execution Review /
Post-Application Verification Packet v1.
