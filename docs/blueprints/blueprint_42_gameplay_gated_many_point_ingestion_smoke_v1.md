# Blueprint 42 - Gameplay-Gated Many-Point Ingestion Smoke v1

Status: complete

## Goal

Blueprint 42 adds the first end-to-end structural smoke path that starts from an explicit
many-point media manifest and composes the gameplay gate contracts delivered in Blueprints 38-41.

```text
explicit smoke manifest
-> many-point ingestion gate dry run
-> gameplay segment candidates
-> gameplay-gated routing plan
-> gameplay-gated perception execution plan
-> gameplay segment replay timeline
-> structural smoke report
```

This is a smoke/integration workflow only. It is not point detection, scoring, line calling,
truth, adjudication, model correctness, or a generalization claim.

## Contract

The tracked contract is:

```text
.data/contracts/gameplay_gated_many_point_smoke_contract_v1.json
```

The contract defines:

- smoke scope and allowed smoke modes
- explicit manifest and entry schema
- requested smoke step schema
- smoke report schema
- referenced TOM contract versions
- structural validation rules
- provenance requirements
- no-truth/no-adjudication warnings

Default smoke mode is `fixture_only`, which uses the existing provenance fixture classifier path.
It does not run GPU/model inference by default and does not mutate `model_assets/`.

## Commands

```bash
make tom-v1-export-gameplay-gated-many-point-smoke-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-gameplay-gated-many-point-smoke-manifest-template \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_MEDIA_PATH=demo_assets/sample_point.mp4

make tom-v1-validate-gameplay-gated-many-point-smoke-manifest \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST=.data/exports/gameplay_gated_many_point_smoke_manifest.template.json

make tom-v1-run-gameplay-gated-many-point-smoke \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST=.data/exports/gameplay_gated_many_point_smoke_manifest.template.json

make tom-v1-build-gameplay-gated-many-point-smoke-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT=.data/exports/gameplay_gated_many_point_smoke.current.json
```

Generated reports and intermediate artifacts live under `.data/exports/` and are not committed.

## Boundaries

Blueprint 42 does not add or infer:

- in/out
- score
- point winner
- player identity
- rally state
- server/receiver state
- line-call truth
- point truth
- event truth
- accepted/rejected lifecycle
- marker arbitration
- coaching/tactical conclusions
- betting or prediction outputs
- training labels
- production readiness or generalization claims

If `demo_assets/sample_point.mp4` is reused more than once as a fixture stand-in, the manifest and
report explicitly include `fixture_reuse_only`, `not_distinct_real_points`, and
`does_not_claim_generalization`.
