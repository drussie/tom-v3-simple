# second_point Ingestion Smoke v0

The `second_point` smoke is a single additional evidence sample used to confirm that TOM v3 can
index another local point/video and open it in Replay Workstation.

It is not a multi-point benchmark. It is not a generalization claim. It is not truth.

## Smoke Command

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_smoke.db \
make tom-v1-ingest-second-point-smoke \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/second_point.mp4
```

The media path must be supplied by the operator and must not be committed to Git.

## Successful Smoke Output

The command returns:

- `ok`: true
- `status`: `completed`
- `smoke_type`: `second_point_ingestion_evidence_replay_smoke`
- `smoke_version`: `v0`
- `media_id`
- `media_metadata`
- `replay_url`
- warnings preserving candidate-only, observation-only, not-truth, and no-adjudication boundaries

## Valid Empty Evidence State

For Blueprint 21, the second point may have:

- no detection run
- no motion smoothing run
- no court projection run
- no event candidate run
- no trajectory 3D run
- no review annotations

Replay should still load the media and handle missing event/3D candidates gracefully.

## sample_point Baseline

The original `sample_point` remains the protected baseline. The second point smoke must not change:

- `sample_point` media/runs
- `sample_point` event marker counts
- `sample_point` reviewed 3D debug baseline export
- `sample_point` baseline manifest
- `sample_point` regression semantics

Before using the second point for any follow-up milestone, the `sample_point` baseline gate must
still report no drift.

## Next Step

The next milestone may run existing candidate-generation paths on the second point, but only after
ingestion/replay is stable. That future work must still remain candidate-only and observation-only.
