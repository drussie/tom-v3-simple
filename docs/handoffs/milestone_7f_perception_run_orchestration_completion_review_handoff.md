# TOM v3 - Milestone 7F Handoff

## Perception Run Orchestration and Completion Review

Repo: `drussie/tom-v3-simple`

Branch: `codex/m7f-perception-run-orchestration-completion-review`

Starting state: Milestone 7E Court / Homography Evidence Decision Gate completed and merged to `main`.

## Mission

Close Blueprint 7.

The target path is:

```text
Blueprint 7 real perception runtime
-> final orchestration runbook
-> final completion review
-> Blueprint 7 COMPLETE
-> Blueprint 8 boundary preserved
```

## Required Boundary

Use evidence language:

- real model output
- detection observation
- candidate tracklet
- track point candidate
- pose keypoint evidence
- perception run
- model registry
- runtime config
- persisted observation
- replay overlay
- evidence only
- non-adjudicative
- Blueprint 8 candidate

Do not add new runtime behavior, court/homography implementation, database schema, frontend features, bounce/hit/rally/point/scoring, movement/stroke interpretation, real stream ingestion, or adjudication.

## Validation Checklist

- Blueprint 7 completion review exists.
- Canonical docs mark Blueprint 7 COMPLETE.
- Final orchestration runbook is documented.
- Plan-only real detection and real pose commands pass.
- Full test/lint/build/smoke validation passes.
- Optional real runtime smoke is run only if local weights exist.
- Court/camera/homography remains deferred to Blueprint 8.

## Recommended Next Step

Stop Blueprint 7. Use/demo the real perception replay ladder when local weights are available.

Future work should begin as Blueprint 8 only if deliberately chosen.
