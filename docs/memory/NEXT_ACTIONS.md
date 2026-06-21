# TOM v3 Next Actions

## Current Next Action

- Use repo-local memory before every future Codex handoff.
- Future handoffs should instruct Codex to read `docs/memory/CODEX_CONTEXT.md` before editing.
- Future blueprints should update `PROJECT_STATE.md`, `BLUEPRINT_LEDGER.md`, `DECISIONS.md`, and
  `NEXT_ACTIONS.md` when project state changes.

## Immediate Next Regular Blueprint

After Blueprint 65:

- Resolve the BP65 next-action recommendations before any future runtime application retry:
  `resolve_operator_signoff_before_reapplying`.
- Select explicit candidate context before rerunning the final gate.
- Rerun the BP61 final gate only after real operator signoff and selected candidate context exist.
- Keep future runtime application blocked while BP61/BP62/BP64/BP65 report the current safe
  blocked state.

## Open Follow-Ups

- Decide whether to mirror TOM strategic notes into an external Obsidian vault later.
- Add memory-update requirement to all future TOM handoffs.
- Consider a future docs check that verifies memory files exist and are referenced by Codex workflow
  docs.
- Consider adding a lightweight memory update checklist to `docs/codex-workflow`.
- Consider using `docs/codex-workflow/handoffs` and `docs/codex-workflow/retros` for future handoff
  and retro records.
- Consider adding a future phase-freeze/readiness blueprint after the BP64 blocked execution review
  packet if no operator signoff is ready yet.
