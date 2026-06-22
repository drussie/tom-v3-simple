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

## Decision 11: Explicit Selected Candidate Artifacts Require Human Selection Input

Reason: BP68 may preserve candidate option inventory and create a pending selected candidate
artifact, requirements report, and readiness report, but candidate option discovery, a single
available option, validation success, branch state, commit state, and tags do not satisfy explicit
candidate selection.

## Decision 12: Human Resolution Input Packets Require Explicit Human Inputs

Reason: BP69 may combine operator signoff requirements and selected candidate requirements into a
single pending packet and template, but that packet does not resolve blockers without real operator
identity, timestamp, attestation, scope acknowledgement, selected candidate ref, selected candidate
provenance, selection reason, selection timestamp, and operator reference.

## Decision 13: Human Resolution Provided Packets Still Require Real Human Inputs

Reason: BP70 may record whether the BP69 human-resolution inputs have been supplied, but it must
keep human resolution not provided until real operator identity, timestamp, attestation, scope
acknowledgement, selected candidate ref, selected candidate provenance, selection reason, selection
timestamp, and operator reference are explicitly supplied through controlled input fields.

## Decision 14: Explicit Human Resolution Records Require Real Controlled Inputs

Reason: BP71 may define a durable record for explicit human resolution fields, but it must keep the
record pending until real operator identity, timestamp, attestation, scope acknowledgement, selected
candidate ref, selected candidate provenance, selection reason, selection timestamp, and operator
reference are supplied through controlled input fields.

## Decision 15: Human Resolution Completeness Gates Do Not Resolve Missing Inputs

Reason: BP72 may determine whether a BP71 explicit human resolution record is complete enough to
prepare a future final-gate rerun, but it must keep the gate not ready until real operator signoff
material and real selected candidate material are supplied. Candidate option discovery, validation
success, branch state, commits, and tags do not satisfy the completeness gate.

## Decision 16: Final Gate Rerun Request Packets Do Not Execute Final Gates

Reason: BP73 may create a formal request packet for a future final-gate rerun, but it must keep the
request blocked until BP72 reports complete human resolution. The request packet does not infer
operator signoff, selected candidate, or human resolution; it does not rerun the final gate, mutate
runtime config, create production config, modify model weights, or replace baselines.

## Decision 17: Final Gate Rerun Execution Results Do Not Force Reruns

Reason: BP74 may create an execution-result artifact from BP73, but when BP73 remains blocked by
incomplete human resolution it must record a blocked, non-executed result. It does not infer
operator signoff, selected candidate, or human resolution; it does not execute a final-gate rerun,
mutate runtime config, create production config, modify model weights, or replace baselines.

## Decision 18: Reexecution Request Packets Do Not Execute Runtime Application

Reason: BP75 may create a reexecution request packet from BP74, but it must keep the request
blocked until an explicit final-gate rerun result exists after complete human resolution. It does
not infer operator signoff, selected candidate, human resolution, or final-gate result; it does not
execute runtime application, mutate runtime config, create production config, modify model weights,
or replace baselines.

## Decision 19: Reexecution Execution Results Do Not Force Runtime Execution

Reason: BP76 may create a reexecution execution blocked-result artifact from BP75, but it must keep
execution blocked while BP75 is blocked by the missing final-gate rerun result. It does not infer
operator signoff, selected candidate, human resolution, final-gate result, or reexecution approval;
it does not execute runtime reexecution or runtime application, mutate runtime config, create
production config, modify model weights, or replace baselines.

## Decision 20: Post-Reexecution Verification Requires Runtime Reexecution Output

Reason: BP77 may create a post-reexecution verification not-available packet from BP76, but it must
keep verification unavailable while BP76 records that runtime reexecution was not performed. It
does not infer post-reexecution verification, runtime reexecution output, final-gate result, human
resolution, selected candidate, operator signoff, or reexecution approval; it does not execute
runtime reexecution or runtime application, mutate runtime config, create production config, modify
model weights, or replace baselines.
