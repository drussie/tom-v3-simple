# Blueprint 39 - Gameplay-Gated Evidence Pipeline Routing v1

Status: implemented.

Blueprint 39 turns Blueprint 38 gameplay segment candidates into a structural downstream routing
plan. It records which downstream evidence stages may use gameplay-approved windows, which windows
are blocked or require review, and why each route decision exists.

## Scope

Blueprint 39 proves:

```text
gameplay segment candidates
-> allowed / blocked / review-required windows
-> downstream stage routing entries
-> skip reasons and override statuses
-> replay-visible routing timeline lane
-> structural routing report
```

The tracked contract lives at:

```text
.data/contracts/gameplay_gated_pipeline_routing_contract_v1.json
```

Generated local exports live at:

```text
.data/exports/gameplay_gated_routing_plan.current.json
.data/exports/gameplay_gated_routing_plan.validation.json
.data/exports/gameplay_gated_routing_report.current.json
```

## Commands

```bash
make tom-v1-export-gameplay-gated-routing-contract PYTHON=.venv/bin/python
make tom-v1-build-gameplay-gated-routing-plan \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS=.data/exports/gameplay_segment_candidates.current.json
make tom-v1-validate-gameplay-gated-routing-plan \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
make tom-v1-build-gameplay-gated-routing-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
```

## Boundary

This is a routing and planning layer only. The default routing mode is `dry_run`; it does not run
downstream detection, tracklet, pose, court, event, 3D, replay, or corpus jobs. It preserves
segment provenance and records structural decisions such as `allow_downstream_observation`,
`skip_non_gameplay`, and `require_human_review`.

Blueprint 39 does not decide tennis truth, in/out, score, point winner, player identity, rally
state, server/receiver state, line-call truth, point truth, event truth, marker arbitration,
accepted/rejected lifecycle, coaching/tactical conclusions, betting/prediction outcomes,
generalization, automatic correctness, training truth, production truth, or adjudication. It does
not mutate model assets, commit weights, silently ingest media, auto-discover media folders, run
heavy inference, or mutate protected regression baselines.
