# Blueprint 23 Point Manifest / Evidence Provenance Contract v0

Status: complete

Blueprint 23 adds a point-level manifest contract for describing what evidence already exists for a
media-backed point. The manifest is a provenance record for replay, review, dataset export, and
future regression gates. It does not create truth, event generation, 3D generation, scoring, player
identity, or adjudication.

## Command

```bash
.venv/bin/python -m apps.worker.cli build-point-manifest \
  --media-id "9518fb01-0da1-4344-9a84-ff88ec8e9b1e" \
  --event-candidate-run-id "1b946366-7ec1-426f-8b40-494535a9b3fb" \
  --trajectory-3d-run-id "ea76ccab-c51d-4a63-9682-9fd0bbb83f14" \
  --camera-geometry-id "5afa67fb-7f6e-41eb-b4aa-b1100a97ee97"
```

Make helper:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-build-point-manifest \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

## Manifest Path

By default, the command writes:

```text
.data/manifests/<point_manifest_id>.json
```

The `point_manifest_id` is deterministic for:

- manifest type
- manifest version
- media ID
- event candidate run ID, when provided
- trajectory 3D run ID, when provided
- camera geometry ID, when provided

Override the path with:

```bash
POINT_MANIFEST_OUTPUT=.data/manifests/sample_point.point_manifest.json
```

Generated `.data` artifacts are local outputs and should not be committed.

## Contract

The manifest records:

- `manifest_type`: `point_evidence_provenance_manifest`
- `manifest_version`: `v0`
- deterministic `point_manifest_id`
- media source and stored URI/path provenance
- replay URL
- generated timestamp
- TOM project and Blueprint 23 provenance
- optional associated run IDs
- evidence availability booleans
- profile counts for event markers, 3D candidates, diagnostics, and review metadata
- boundary warnings

## Boundaries

Blueprint 23 does not add or change:

- in/out
- score
- point winner
- player identity
- rally state
- server or receiver state
- accepted/rejected lifecycle
- marker arbitration
- event generation
- 3D generation
- coaching or tactical conclusions
- adjudication
- betting or prediction
- generalization claims

The manifest is observation-only provenance. It can say that evidence rows exist, but it cannot say
that any row is correct.

## Protected sample_point Gate

Blueprint 23 preserves the existing `sample_point` reviewed 3D debug baseline gate:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Expected:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
