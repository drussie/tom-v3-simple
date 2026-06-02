# sample_point Expansion Readiness v0

## Verdict

TOM v3 is ready for controlled second-point expansion after Blueprint 20, provided the second point
is introduced as a new evidence sample and not as a claim of multi-point generalization.

The readiness verdict is intentionally conservative:

- ready for one additional point smoke
- not ready for dataset-level benchmark claims
- not ready for hit/bounce truth
- not ready for in/out, score, or adjudication
- not ready for training labels
- not ready for verified 3D reconstruction

## Required Pre-Expansion Gate

Before adding a second point, run the existing sample-point gate:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

The gate should report:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

If drift appears, stop and review the drift before introducing new media.

## What Expansion May Do

Blueprint 21 may:

- ingest one additional point
- run the existing evidence pipeline on that point
- open the replay for visual smoke
- record point-specific run IDs and counts
- produce a point evidence snapshot
- produce a candidate evaluation report
- export reviewed 3D debug evidence if the needed runs exist
- compare the second point against its own future baseline once reviewed

## What Expansion Must Not Do

Blueprint 21 must not:

- tune sample-point candidate logic just to fit the new point
- mix sample-point and second-point markers into a single truth set
- call reviewed metadata truth
- introduce in/out, score, point outcome, or adjudication
- infer player identity, server/receiver state, or scoreboard state
- treat provisional 3D candidates as verified 3D reconstruction
- create training labels from candidate exports

## Readiness Rationale

The sample-point evidence loop is ready for controlled expansion because:

- final event marker counts are reproducible
- point snapshot and evaluation reports are available
- operator review metadata is preserved without mutating candidates
- provisional 3D candidates and diagnostics are exported in a deterministic reviewed dataset format
- export-to-export regression detects drift
- a local baseline gate verifies the frozen sample profile
- candidate-only, not-truth, and no-adjudication warnings are preserved

## Remaining Risk

The largest risks for the second point are evidence quality and overinterpretation:

- sample-point still contains one reviewed wrong `bounce_candidate`
- most event markers remain unreviewed
- all 68 provisional 3D trajectory samples have unknown height
- declared camera/court geometry is evidence only
- no true 3D reconstruction is available
- no event marker is accepted or rejected as truth

These risks are acceptable for a controlled smoke, but they are not acceptable for benchmark,
training, or adjudication claims.

## Recommended Next Milestone

Blueprint 21 - Second Point Ingestion / Evidence Replay Smoke v0.

The next step should be one additional point, introduced carefully under the existing candidate-only
contract.
