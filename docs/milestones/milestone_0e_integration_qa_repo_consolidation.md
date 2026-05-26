# Milestone 0E - Integration / QA / Repo Consolidation

## Goal

Consolidate TOM v3 Simple Milestone 0 into a coherent, runnable foundation.

The target loop:

```text
clean repo -> local setup -> seed synthetic run -> start backend -> start web viewer -> inspect persisted synthetic evidence -> run validation
```

## Scope

Milestone 0E includes:

- local environment setup docs
- local demo runbook
- `.env.example`
- root Makefile for common commands
- integration smoke script
- integration smoke test
- README refresh
- project memory updates
- branch/default-branch hygiene guidance
- final Milestone 0 report and handoff

## What Was Validated

Validation covers:

- backend tests
- ruff linting
- web TypeScript lint
- web production build
- web dependency audit
- Alembic SQLite migration smoke test
- worker seed and verify flow
- synthetic viewer data smoke script
- Milestone 0 integration smoke test
- docs file listing
- git status

## What Remains Synthetic

Milestone 0E does not add real model intelligence.

The following remain synthetic or placeholder:

- media source files
- frame extraction
- model output
- tracking
- homography calculation
- bounce and hit candidates
- artifact files

## Ready For Next Milestone

The recommended next milestone is:

```text
Milestone 1A - Real Media Indexing + Video Upload/Registration
```

Real media indexing should come before model adapters because every future model run needs stable media, frame, timestamp, and artifact references.

## Acceptance Status

Status: complete.

Milestone 0E acceptance criteria are satisfied by:

- dev docs in `docs/dev`
- `.env.example`
- root `Makefile`
- smoke script in `scripts/smoke_synthetic_viewer_data.py`
- smoke test in `tests/test_milestone_0_integration.py`
- updated README and control-room docs
- branch/default-branch cleanup guidance in `docs/dev/repo_branch_hygiene.md`
- final agent report
