# Blueprint 40 - Gameplay-Gated Perception Execution Hook v1

Status: complete

## Goal

Create the first execution hook that consumes Blueprint 39 gameplay-gated routing plans and turns
them into perception-stage execution constraints without running heavy perception inference by
default.

## Flow

```text
gameplay-gated routing plan
-> allowed gameplay execution windows
-> skipped non-gameplay windows
-> review-required windows
-> perception execution entries
-> structural execution report
```

## Scope

Blueprint 40 adds:

- `apps.worker.services.gameplay_gated_perception_execution`
- `export-gameplay-gated-perception-execution-contract`
- `build-gameplay-gated-perception-execution-plan`
- `validate-gameplay-gated-perception-execution-plan`
- `build-gameplay-gated-perception-execution-report`
- `tom-v1-export-gameplay-gated-perception-execution-contract`
- `tom-v1-build-gameplay-gated-perception-execution-plan`
- `tom-v1-validate-gameplay-gated-perception-execution-plan`
- `tom-v1-build-gameplay-gated-perception-execution-report`
- `.data/contracts/gameplay_gated_perception_execution_contract_v1.json`

Generated execution plan, validation, and report artifacts are local outputs under
`.data/exports/` and are not committed.

## Contract

The contract records execution scope, source contract refs, Blueprint 39 routing-plan refs,
perception stage schema, execution plan schema, skipped window schema, execution summary schema,
validation rules, provenance requirements, and warning flags.

The default execution mode is `dry_run`. The hook records which perception stages may run on
gameplay-approved windows and which windows must be skipped or reviewed. It does not run GPU/model
inference, write observations, mutate model assets, mutate baselines, create labels, create
in/out, create score, identify players, determine winners, make line-call conclusions, make
training labels, claim production correctness, or adjudicate evidence.

## Validation

Validation checks:

- contract shape
- execution plan shape
- allowed execution modes
- allowed execution decisions
- allowed skip reasons
- allowed provenance statuses
- referenced Blueprint 39 routing plan/contract versions
- exact forbidden keys and values

Validation reports structural errors only.
