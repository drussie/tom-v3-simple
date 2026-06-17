# Blueprint 23 Point Manifest / Evidence Provenance Contract v0 Report

Status: implemented

Branch: `codex/blueprint-23-point-manifest-evidence-provenance-contract-v0`

## Summary

Blueprint 23 adds a point-level manifest/provenance contract. The new service reads existing media,
event candidate, 3D candidate, diagnostic, and review metadata rows, writes one JSON manifest, and
returns a compact CLI result with the same manifest payload.

This milestone does not run candidate generation, marker arbitration, 3D generation, review
creation, truth, in/out, score, player identity, point winner, or adjudication.

## Created

- `apps/worker/services/point_manifest.py`
- `tests/test_point_manifest.py`
- `docs/blueprints/blueprint_23_point_manifest_evidence_provenance_contract_v0.md`
- `docs/reviews/point_manifest_evidence_provenance_contract_v0.md`
- `docs/agent_reports/blueprint_23_point_manifest_evidence_provenance_contract_v0_report.md`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/BLUEPRINT_STATUS.md`

## CLI / Make Helper

Added CLI command:

```text
python -m apps.worker.cli build-point-manifest
```

Added Make target:

```text
make tom-v1-build-point-manifest
```

Default output:

```text
.data/manifests/<point_manifest_id>.json
```

The `point_manifest_id` is deterministic over manifest type/version, media ID, and any associated
run IDs supplied to the command.

## Protected sample_point Gate

The protected `sample_point` baseline gate remains required and unchanged:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

## Local Manifest Smoke

The sample-point manifest command produced:

- `point_manifest_id`: `point_manifest_v0_690dfd41205609e0caca1263`
- `event_marker_count`: 6
- `hit_candidate_count`: 3
- `bounce_candidate_count`: 3
- `event_candidate_observation_count`: 877
- `event_candidate_rejection_diagnostic_count`: 871
- `trajectory_3d_candidate_count`: 68
- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_review_count`: 1
- `trajectory_3d_debug_review_count`: 0
- `human_annotation_count`: 3
- `review_annotation_count`: 4
- `manifest_is_not_truth`: true
- `observation_only`: true
- `no_adjudication`: true

## Validation

```text
.venv/bin/python -m pytest tests/test_point_manifest.py -q
5 passed

.venv/bin/python -m pytest -q
399 passed

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

Protected baseline gate:

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

Manifest Make target:

```text
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-build-point-manifest \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
passed
```

Fixture demo and audit:

```text
.venv/bin/python scripts/smoke_synthetic_viewer_data.py
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_23_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_23_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
