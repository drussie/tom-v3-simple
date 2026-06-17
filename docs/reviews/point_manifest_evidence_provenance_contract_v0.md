# Point Manifest Evidence Provenance Contract v0

The point manifest is a durable, point-level provenance record. It describes media storage,
Replay Workstation links, optional associated evidence run IDs, evidence availability, profile
counts, and boundary warnings.

It is not a baseline truth record, adjudication layer, scoring layer, player identity layer, or
training-label source.

## Command

```bash
make tom-v1-build-point-manifest \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

Only `MEDIA_ID` is required. The run IDs narrow the manifest to known evidence runs when they are
available.

Default output:

```text
.data/manifests/<point_manifest_id>.json
```

## Required Semantics

- `media_indexed` means the media row exists.
- `replay_available` means TOM can form a Replay Workstation URL for the media ID.
- Candidate booleans mean candidate rows are present, not correct.
- Review booleans mean review metadata rows are present, not truth.
- 3D booleans mean provisional 3D/debug rows are present, not 3D truth.

## Warnings

The manifest must carry these true warnings:

- `baseline_is_not_truth`
- `manifest_is_not_truth`
- `observation_only`
- `no_adjudication`
- `not_training_truth`
- `not_3d_truth`
- `does_not_create_in_out`
- `does_not_create_score`
- `does_not_identify_players`
- `does_not_determine_winner`
- `not_generalization_claim`

## Use

Use the manifest as shared provenance for replay/review surfaces, sample-point and second-point
artifacts, dataset exports, and regression gates. Do not use it as a tennis conclusion.
