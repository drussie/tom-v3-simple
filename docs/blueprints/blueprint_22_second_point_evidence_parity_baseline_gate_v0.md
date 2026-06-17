# Blueprint 22 Second Point Evidence Parity / Protected Baseline Gate v0

Status: complete

Blueprint 22 converts the Blueprint 21 second-point ingestion smoke into a protected evidence
parity checkpoint. It indexes one operator-provided local media file, returns a Replay Workstation
URL, records which evidence layers are currently available for that media asset, and writes a local
baseline manifest for the second-point profile.

This is not broad scaling, multi-point generalization, truth validation, line calling, scoring, or
adjudication.

## Command

```bash
.venv/bin/python -m apps.worker.cli build-second-point-evidence-parity \
  --media-path "/absolute/path/to/second_point.mp4" \
  --run-name "second-point-evidence-parity-v0" \
  --viewer-base-url "http://127.0.0.1:3000"
```

Make helper:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_parity.db \
make tom-v1-build-second-point-evidence-parity \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/second_point.mp4
```

The command validates the media path and fails clearly for missing or nonexistent input:

- `missing_second_point_media_path`
- `second_point_media_path_not_found`

## Baseline Manifest

By default, the command writes:

```text
.data/baselines/second_point_evidence_parity.baseline_manifest.json
```

Generated `.data` artifacts are local outputs and should not be committed.

The manifest records:

- `media_id`
- `source_media_path`
- `replay_url`
- second-point profile booleans
- second-point evidence counts
- candidate-only / not-truth / no-adjudication warnings

## Profile Semantics

The second-point profile reports current evidence availability:

- `media_indexed`
- `replay_available`
- `event_candidates_available`
- `trajectory_3d_candidates_available`
- `review_annotations_available`
- `baseline_available`

For v0, it is valid for the second point to have only media/replay parity. A lack of event
candidates or 3D candidates is not a failure unless a future command claims those layers exist.

## Protected sample_point Gate

Blueprint 22 must preserve the existing `sample_point` reviewed 3D debug baseline gate:

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

## Boundaries

Blueprint 22 does not add or change:

- event candidate generation
- marker arbitration
- 3D candidate generation
- 3D diagnostics
- review annotation semantics
- sample-point baseline data
- truth
- in/out
- score
- point winner
- player identity
- adjudication

The second-point manifest is a protected evidence checkpoint only. It is candidate-only,
observation-only, not truth, and not a generalization claim.
