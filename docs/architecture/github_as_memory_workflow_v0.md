# GitHub-as-Memory Workflow v0

## Purpose

GitHub is the durable memory for TOM v3 Simple.

The repo should carry the current state, architecture contracts, milestone plans, handoffs, implementation logs, and agent reports so future Codex agents can continue without losing project intent.

## Operating Model

- GitHub = durable memory
- Architectural Control Room = milestone designer/reviewer
- Codex agents = bounded implementers
- Repo docs = shared project reference
- Branches/PRs = agent work isolation
- Agent reports = memory bridge
- Implementation logs = milestone history

## Recommended Agent Roles

1. Architecture / Schema Agent
2. Backend / API Agent
3. Worker / Pipeline Agent
4. Web / Visual Evidence Viewer Agent
5. QA / Integration / Docs Agent

## Recommended Branch Pattern

```text
codex/m0a-repo-memory-architecture-schema
codex/m0b-backend-api
codex/m0c-worker-synthetic-pipeline
codex/m0d-web-visual-evidence-viewer
codex/m0e-qa-integration-docs
```

## Required Agent Report

Every agent must write an agent report.

Agent reports should include:

- summary
- files created
- files modified
- decisions made
- non-goals preserved
- validation run
- known gaps
- recommended next handoff

## Handoff Discipline

Each milestone branch should leave behind enough documentation for the next branch to begin safely.

Before finishing, an agent should update:

- `docs/CURRENT_STATE.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/IMPLEMENTATION_LOG.md`
- relevant milestone docs
- relevant handoff docs
- relevant agent report

## Branch and PR Discipline

Agents should work on bounded branches and keep PR descriptions aligned with milestone acceptance criteria.

For M0A, the branch is:

```text
codex/m0a-repo-memory-architecture-schema
```
