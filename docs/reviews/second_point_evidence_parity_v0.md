# second_point Evidence Parity v0

The `second_point` evidence parity checkpoint is a controlled step beyond `sample_point`. It proves
that one additional operator-provided media asset can be indexed, opened in replay, and represented
by a local evidence-profile manifest.

It does not prove that TOM has generalized to multiple points. It does not create or validate
hit/bounce truth, in/out, score, player identity, tactical meaning, or adjudication.

## Local Command

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_parity.db \
make tom-v1-build-second-point-evidence-parity \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/second_point.mp4
```

Default manifest output:

```text
.data/baselines/second_point_evidence_parity.baseline_manifest.json
```

## Expected v0 Profile

A valid v0 result may initially contain:

- `media_indexed`: true
- `replay_available`: true
- `event_candidates_available`: false
- `trajectory_3d_candidates_available`: false
- `review_annotations_available`: false
- `baseline_available`: true

Empty event or 3D evidence layers are acceptable for this parity checkpoint. They should be reported
honestly rather than filled with synthetic candidate evidence.

## Review Rules

Before using the second point for candidate-generation work:

1. Re-run the protected `sample_point` baseline gate.
2. Confirm the second-point replay URL opens without crashing.
3. Confirm the second-point manifest reflects the evidence layers that actually exist.
4. Keep all labels candidate-only and observation-only.

## Non-Goals

This checkpoint does not add:

- multi-point benchmark metrics
- hit/bounce truth
- in/out decisions
- scoring
- accepted/rejected lifecycle
- player identity
- coaching or tactical conclusions
- adjudication
