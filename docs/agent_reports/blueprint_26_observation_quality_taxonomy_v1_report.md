# Blueprint 26 Observation Quality Taxonomy v1 Report

Status: implemented

Branch: `codex/blueprint-26-observation-quality-taxonomy-v1`

## Summary

Blueprint 26 adds a versioned observation-quality taxonomy contract and a conservative profile
builder over existing Blueprint 24 replay indexes. The taxonomy gives future review/export/gate
surfaces stable quality dimensions. The profile records only what can be known from existing index
metadata and marks visual or uncertain quality as requiring human review.

The implementation does not inspect video, create observations, create event candidates, create 3D
candidates, decide in/out, score, identify players, determine winners, claim generalization, or
adjudicate evidence.

## Created

- `apps/worker/services/observation_quality_taxonomy.py`
- `tests/test_observation_quality_taxonomy.py`
- `docs/blueprints/blueprint_26_observation_quality_taxonomy_v1.md`
- `docs/reviews/observation_quality_taxonomy_v1.md`
- `docs/agent_reports/blueprint_26_observation_quality_taxonomy_v1_report.md`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/BLUEPRINT_STATUS.md`

## CLI / Make Helpers

Added CLI commands:

```text
python -m apps.worker.cli export-observation-quality-taxonomy
python -m apps.worker.cli build-observation-quality-profile
```

Added Make targets:

```text
make tom-v1-export-observation-quality-taxonomy
make tom-v1-build-observation-quality-profile
```

Default local paths:

```text
.data/contracts/observation_quality_taxonomy_v1.json
.data/exports/observation_quality_profile.current.json
```

## Profile Semantics

The profile reads the multi-point replay index only. For each point it preserves manifest/media
identity, replay URL, source/storage media paths or URIs, associated run IDs, evidence
availability, profile counts, provenance-only labels, quality dimensions, and warnings.

Visual dimensions are `unknown` when media or replay context exists because the service does not
inspect video. Missing evidence is `unavailable`. Existing replay/provenance context can be marked
`sufficient_for_review` when the index already provides enough metadata to open or identify the
point for review.

## Boundary

The taxonomy and profile are review-support contracts only. They do not generate evidence, mutate
review metadata, change protected baselines, decide in/out, score, identify players, determine a
winner, claim generalization, or adjudicate evidence.

## Validation

```text
.venv/bin/python -m pytest tests/test_observation_quality_taxonomy.py -q
4 passed

.venv/bin/python -m pytest -q
410 passed

ruff check .
passed

git diff --check
passed

cd apps/web && npm run lint
passed

cd apps/web && npm run build
passed

cd apps/web && npm audit --omit=dev
found 0 vulnerabilities
```

Observation-quality command smoke:

```text
make tom-v1-export-observation-quality-taxonomy PYTHON=.venv/bin/python
passed

make tom-v1-build-multi-point-replay-index PYTHON=.venv/bin/python
passed

make tom-v1-build-observation-quality-profile PYTHON=.venv/bin/python
passed
```

Observed profile smoke:

- `profile_type`: `observation_quality_profile`
- `profile_version`: `v1`
- `point_count`: 1
- `summary.replay_available_count`: 1
- `summary.review_ready_count`: 1
- `summary.unknown_quality_count`: 1
- `summary.requires_human_review_count`: 1
- visual dimensions remained `unknown` and required human review
- replay/provenance completeness were `sufficient_for_review`

Multi-point matrix gate:

```text
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
passed
```

Observed:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
- `matrix_is_not_truth`: true

Protected sample-point baseline gate:

```text
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
passed
```

Observed:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

Fixture demo and audit:

```text
.venv/bin/python scripts/smoke_synthetic_viewer_data.py
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_26_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_26_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
