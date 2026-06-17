# Multi-Point Replay Navigation / Review Surface v0

The multi-point replay index is a local navigation artifact over existing point manifests. It lets
operators discover replayable manifest-backed points and open the Replay Workstation with preserved
run-ID context.

It is not a truth source, training source, event lifecycle, scoring layer, or adjudication layer.

## Build

```bash
make tom-v1-build-multi-point-replay-index \
  PYTHON=.venv/bin/python
```

Optional overrides:

```bash
POINT_MANIFEST_ROOT=.data/manifests
MULTI_POINT_REPLAY_INDEX_OUTPUT=.data/manifests/multi_point_replay_index.json
VIEWER_BASE_URL=http://127.0.0.1:3000
```

## Expected Output

```text
.data/manifests/multi_point_replay_index.json
```

Expected result fields:

- `ok`: true
- `status`: `completed`
- `index_type`: `multi_point_replay_index`
- `index_version`: `v0`
- `point_count`: number of valid point manifests discovered
- `points[]`: replayable manifest-backed points
- `warnings.navigation_only`: true
- `warnings.manifest_index_is_not_truth`: true
- `warnings.observation_only`: true
- `warnings.no_adjudication`: true

## Replay Review

The API route is:

```text
GET /replay/point-manifests
```

The web replay page keeps the existing route:

```text
/replay/<media_id>
```

Point links include these query parameters when present:

- `eventCandidateRunId`
- `trajectory3dRunId`
- `cameraGeometryId`

The navigator displays evidence availability and profile counts from manifests only. It does not
generate evidence, change review annotations, accept or reject markers, decide in/out, score, or
identify players.

## Labels

Labels are provenance-only:

- `protected_sample_point` is reserved for the known protected sample-point manifest/run context.
- `second_point_parity_stand_in` is emitted only when existing manifest path/source provenance
  indicates a second-point or sample-point stand-in context.

These labels do not imply correctness, representative coverage, or generalization.
