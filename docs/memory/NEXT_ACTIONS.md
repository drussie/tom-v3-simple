# TOM v3 Next Actions

## Current Next Action

- Use repo-local memory before every future Codex handoff.
- Future handoffs should instruct Codex to read `docs/memory/CODEX_CONTEXT.md` before editing.
- Future blueprints should update `PROJECT_STATE.md`, `BLUEPRINT_LEDGER.md`, `DECISIONS.md`, and
  `NEXT_ACTIONS.md` when project state changes.

## Immediate Next Regular Blueprint

After Blueprint 78:

- The blocked calibration pathway is frozen. The first valid option is to stop this blocked path.
- The second valid option is to start a new explicit human-resolution cycle.
- A new successful pathway requires real operator signoff with operator identity/reference,
  timestamp, attestation text, and explicit scope acknowledgement.
- A new successful pathway also requires explicit selected candidate context that references a
  frozen candidate config or controlled candidate artifact and includes selection provenance.
- Rerun the BP72 human resolution completeness gate only after real operator signoff material and
  selected candidate context exist.
- Rebuild BP73/BP74/BP75/BP76/BP77 only after BP72 reports readiness and each upstream artifact
  becomes non-blocked in order.
- Keep future runtime application blocked while the current BP61-BP78 chain reports the safe
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
