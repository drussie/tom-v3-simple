# TOM v3 Next Actions

## Current Next Action

- Use repo-local memory before every future Codex handoff.
- Future handoffs should instruct Codex to read `docs/memory/CODEX_CONTEXT.md` before editing.
- Future blueprints should update `PROJECT_STATE.md`, `BLUEPRINT_LEDGER.md`, `DECISIONS.md`, and
  `NEXT_ACTIONS.md` when project state changes.

## Immediate Next Regular Blueprint

After Blueprint 77:

- Decide whether to freeze the current blocked pathway after the BP77 not-available packet.
- Resolve the BP77/BP76/BP75/BP74/BP73/BP72 next-action recommendations before any future runtime
  application retry:
  `provide_human_resolution_inputs`, `provide_operator_inputs`, `provide_selected_candidate_inputs`,
  `provide_operator_signoff_and_selected_candidate`, and
  `rerun_final_gate_after_human_resolution`.
- Provide real operator signoff with operator identity/reference, timestamp, attestation text, and
  explicit scope acknowledgement.
- Provide explicit selected candidate context that references a frozen candidate config or
  controlled candidate artifact and includes selection provenance.
- Rerun the BP72 human resolution completeness gate after real operator signoff material and
  selected candidate context exist.
- Rebuild the BP73 final-gate rerun request packet after BP72 reports readiness.
- Produce a non-blocked BP74/future final-gate rerun execution result only after BP72 reports
  readiness and BP73 records a ready request for a future final-gate rerun.
- Rebuild a non-blocked BP75/future reexecution request packet only after BP74/future output
  includes an explicit final-gate rerun result.
- Rebuild a non-blocked BP76/future reexecution execution result only after BP75/future output
  records a ready reexecution request after the final-gate rerun result.
- Rebuild BP77 only after a future BP76 output includes explicit runtime reexecution output.
- Rerun the BP61 final gate only after human resolution is complete and the controlled rerun request
  execution-result path, reexecution request path, and reexecution execution-result path are ready.
- Keep future runtime application blocked while the
  BP61/BP62/BP64/BP65/BP66/BP67/BP68/BP69/BP70/BP71/BP72/BP73/BP74/BP75/BP76/BP77 chain reports
  the current safe blocked state.

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
