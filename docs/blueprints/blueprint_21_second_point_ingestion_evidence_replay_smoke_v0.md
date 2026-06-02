# Blueprint 21 Second Point Ingestion / Evidence Replay Smoke v0

Blueprint 21 introduces one additional local point/video as a controlled evidence sample.

This is not multi-point generalization. It is not truth, not benchmark scoring, not in/out, and not
adjudication. The milestone only proves that TOM v3 can index one second media asset and open it in
the existing Replay Workstation without disturbing the protected `sample_point` baseline.

## Pipeline

```text
SECOND_POINT_MEDIA_PATH
-> existing media indexing/probe/storage path
-> new media_id
-> Replay Workstation URL
-> second_point smoke summary
```

The command does not run detection, smoothing, projection, event-candidate, 3D-candidate, or review
generation logic. Those future steps must remain separate milestones after ingestion/replay is
stable.

## CLI

```bash
.venv/bin/python -m apps.worker.cli ingest-second-point-smoke \
  --media-path "/absolute/path/to/second_point.mp4" \
  --run-name "second-point-ingestion-smoke-v0" \
  --viewer-base-url "http://127.0.0.1:3000"
```

Missing media path returns:

```json
{
  "ok": false,
  "status": "missing_second_point_media_path"
}
```

A nonexistent media path returns:

```json
{
  "ok": false,
  "status": "second_point_media_path_not_found"
}
```

Successful output includes:

- `media_id`
- media metadata
- `replay_url`
- candidate-only / observation-only / not-truth warnings
- `not_generalization_claim`
- `does_not_change_sample_point`

## Make Target

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_smoke.db \
make tom-v1-ingest-second-point-smoke \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/second_point.mp4
```

Optional manifest output:

```bash
SECOND_POINT_MANIFEST_OUTPUT=.data/second_point/second_point_smoke_manifest.json
```

The manifest is generated local data and should not be committed.

## Replay Expectations

The returned Replay Workstation URL may initially show:

- indexed video playback
- media timeline
- no event candidates
- no 3D candidates
- no review annotations

That is a valid Blueprint 21 outcome. Candidate generation for the second point is deliberately out
of scope.

## sample_point Protection

After adding the second point smoke path, the `sample_point` reviewed 3D debug baseline gate must
still pass with no drift:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

## Boundaries

Blueprint 21 does not add:

- event candidate logic
- marker arbitration logic
- hit/bounce generation
- 3D candidate generation
- 3D diagnostics
- verified height
- truth promotion
- accepted/rejected lifecycle
- in/out
- score
- point winner
- rally/server/player identity
- adjudication
