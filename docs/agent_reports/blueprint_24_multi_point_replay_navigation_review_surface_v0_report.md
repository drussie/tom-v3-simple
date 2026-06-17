# Blueprint 24 Multi-Point Replay Navigation / Review Surface v0 Report

Status: implemented

Branch: `codex/blueprint-24-multi-point-replay-navigation-review-surface-v0`

## Summary

Blueprint 24 adds a read-only multi-point replay index over existing Blueprint 23 point manifests.
The index becomes a navigation/review surface for manifest-backed points, preserving replay URLs
and associated run-ID context without creating new observations, event candidates, 3D candidates,
truth, scoring, player identity, point winner, or adjudication.

## Created

- `apps/worker/services/multi_point_replay_index.py`
- `tests/test_multi_point_replay_index.py`
- `apps/web/src/app/api/replay/point-manifests/route.ts`
- `docs/blueprints/blueprint_24_multi_point_replay_navigation_review_surface_v0.md`
- `docs/reviews/multi_point_replay_navigation_review_surface_v0.md`
- `docs/agent_reports/blueprint_24_multi_point_replay_navigation_review_surface_v0_report.md`

## Updated

- `apps/worker/cli.py`
- `Makefile`
- `apps/api/routers/replay.py`
- `apps/web/src/app/replay/[mediaId]/page.tsx`
- `apps/web/src/components/ReplayWorkstation.tsx`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/types.ts`
- `apps/web/src/app/globals.css`
- `docs/RUNBOOK_LOCAL.md`
- `docs/BLUEPRINT_PROGRESS.md`
- `docs/CONTROL_ROOM_INDEX.md`
- `docs/IMPLEMENTATION_LOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/BLUEPRINT_STATUS.md`

## CLI / Make Helper

Added CLI command:

```text
python -m apps.worker.cli build-multi-point-replay-index
```

Added Make target:

```text
make tom-v1-build-multi-point-replay-index
```

Default output:

```text
.data/manifests/multi_point_replay_index.json
```

## API / Web

Added API route:

```text
GET /replay/point-manifests
```

The Replay Workstation loads the index and renders a compact point navigator above the existing
replay grid. Point links continue to use `/replay/[mediaId]` and preserve
`eventCandidateRunId`, `trajectory3dRunId`, and `cameraGeometryId` query parameters when present.

## Boundary

The index reads existing point manifest JSON only. It does not generate evidence, mutate review
metadata, change the protected baseline, decide in/out, score, identify players, determine a
winner, or adjudicate evidence.

## Validation

```text
.venv/bin/python -m pytest tests/test_multi_point_replay_index.py -q
3 passed

.venv/bin/python -m pytest -q
402 passed

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

Observed protected result:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

Multi-point index CLI smoke:

```text
.venv/bin/python -m apps.worker.cli build-multi-point-replay-index \
  --manifest-root .data/manifests \
  --output /tmp/tom_v3_blueprint_24_multi_point_replay_index.json \
  --skip-create-db
passed
```

The local smoke discovered one deduplicated protected sample-point manifest and skipped duplicate
manifest files for the same deterministic point identity.

Fixture demo and audit:

```text
.venv/bin/python scripts/smoke_synthetic_viewer_data.py
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_24_fixture.db \
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
passed

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_24_fixture.db \
make completion-audit PYTHON=.venv/bin/python
passed
```
