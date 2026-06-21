# TOM v3 Decisions

## Decision 1: Keep TOM v3 Observation-First

Reason: TOM v3 is designed to safely store and review evidence before any future truth adjudication.

## Decision 2: Reviewed Datasets And Frozen Baselines Matter More Than Automatic Answers

Reason: They allow TOM to improve while preserving auditability and avoiding false truth claims.

## Decision 3: Replay Workstation Is A First-Class Evidence Interface

Reason: Tennis observation quality depends on visual verification and reviewable evidence.

## Decision 4: Memory Belongs In Repo Docs First

Reason: Codex can read repo-local Markdown directly. Obsidian or other knowledge-base tools can be
added later as a human strategic layer, but TOM should carry its own operational memory.

## Decision 5: Controlled Runtime Calibration Is A Chain, Not A One-Step Mutation

Reason: Runtime config changes must be backed by change request, dry run, review packet, human
approval gate, application plan, staging, final gate, execution, rollback, and post-application
verification.

## Decision 6: Model Weights Remain Protected Assets

Reason: Calibration governance may alter explicit runtime configuration only when authorized, but it
must not mutate the underlying classifier weights.

## Decision 7: A Blocked Controlled Execution Is A Valid Safe Outcome

Reason: BP62 can prove the execution mechanism exists while still refusing to apply a runtime config
change when final gate, operator signoff, or selected-candidate requirements are not met.

## Decision 8: Blocked Execution Resolution Packets Do Not Satisfy Blockers

Reason: BP65 may package missing operator signoff, missing selected candidate context, final-gate
rerun requirements, and future reexecution prerequisites, but it must not create those artifacts or
retry runtime application.

## Decision 9: Operator Signoff And Candidate Selection Must Be Explicit

Reason: BP66 may discover candidate option refs and validate packet structure, but candidate option
discovery is not selected candidate context, and validation success or Codex execution is not
operator signoff.

## Decision 10: Explicit Operator Signoff Artifacts Require Real Operator Input

Reason: BP67 may create a pending signoff artifact, requirements report, attestation template, and
readiness report, but those artifacts do not satisfy signoff without real operator identity,
timestamp, attestation text, scope acknowledgement, and selected candidate context.
