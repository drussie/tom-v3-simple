# Codex Context For TOM v3

Before editing TOM v3, read:

- `docs/memory/PROJECT_STATE.md`
- `docs/memory/ARCHITECTURE_BOUNDARIES.md`
- `docs/memory/BLUEPRINT_LEDGER.md`
- `docs/memory/DECISIONS.md`
- `docs/memory/NEXT_ACTIONS.md`

## Default Codex Rules

- Create a branch for every task.
- Keep changes blueprint-scoped.
- Do not broaden scope.
- Do not modify runtime code unless the handoff explicitly asks for it.
- Do not modify model weights.
- Do not change frozen baselines unless explicitly requested.
- Do not introduce truth-adjudication language.
- Do not introduce production-readiness claims.
- Preserve provenance, confidence, source, frame/time, and lineage.
- Preserve controlled calibration governance boundaries.
- Run the appropriate validation gate before commit.
- For docs-only changes, at minimum run `git diff --check`.
- If runtime code changes, run the full relevant test/build gate.

## Required Final Report For Future Codex Tasks

- Branch
- Commit hash
- Files changed
- Commands run
- Validation results
- Boundary check
- Known risks
- Suggested memory update

## Blueprint 63 Boundary

This task is documentation-only.

Do not:

- Modify runtime code.
- Modify tests.
- Modify app UI.
- Modify schemas.
- Modify frozen baselines.
- Modify model weights.
- Delete unrelated backup files.
- Invent unverified blueprint history.
- Claim runtime application occurred.
- Claim production readiness.
- Claim classifier accuracy.
- Claim tennis truth.
