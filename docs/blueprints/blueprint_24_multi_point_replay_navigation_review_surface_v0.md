# Blueprint 24 Multi-Point Replay Navigation / Review Surface v0

Status: complete

Blueprint 24 makes Blueprint 23 point manifests usable as replay navigation units. It discovers
existing point manifest JSON files, builds a local multi-point replay index, exposes that index to
the replay API, and renders manifest-backed point navigation in the Replay Workstation.

This milestone is a navigation/review surface only. It does not create observations, event
candidates, 3D candidates, labels, review lifecycle decisions, truth, scoring, player identity, or
adjudication.

## Command

```bash
.venv/bin/python -m apps.worker.cli build-multi-point-replay-index \
  --manifest-root ".data/manifests" \
  --output ".data/manifests/multi_point_replay_index.json"
```

Make helper:

```bash
make tom-v1-build-multi-point-replay-index \
  PYTHON=.venv/bin/python
```

## Index Path

By default, the command writes:

```text
.data/manifests/multi_point_replay_index.json
```

Generated `.data` artifacts are local outputs and should not be committed.

## Index Contract

The index records:

- `index_type`: `multi_point_replay_index`
- `index_version`: `v0`
- generation timestamp
- source manifest roots
- point count
- manifest-backed `points[]`
- skipped non-point manifest files
- TOM project and Blueprint 24 provenance
- explicit no-truth/no-adjudication warnings

Each point records:

- `point_manifest_id`
- `media_id`
- source manifest path
- replay URL
- media source/storage URI and path fields when present
- associated run IDs
- evidence availability booleans
- profile counts
- manifest warning flags
- provenance-only labels such as `protected_sample_point` or
  `second_point_parity_stand_in` when inferable from existing manifest provenance

Replay URLs preserve `eventCandidateRunId`, `trajectory3dRunId`, and `cameraGeometryId` query
parameters when those IDs exist in the manifest.

## API and Replay Surface

The replay API exposes:

```text
GET /replay/point-manifests
```

The Replay Workstation loads the index opportunistically and renders a compact point navigator
above the existing replay grid. Existing `/replay/[mediaId]` behavior remains unchanged; selecting
a point navigates to the same replay route with preserved run-ID query parameters.

## Boundaries

Blueprint 24 does not add or change:

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

The index can say that manifests and evidence profiles exist. It cannot say that any observation,
candidate, review annotation, or manifest is correct.

## Protected sample_point Gate

Blueprint 24 preserves the existing `sample_point` reviewed 3D debug baseline gate:

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
