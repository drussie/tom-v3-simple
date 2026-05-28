# Court Review Export v0

Milestone 8F adds a TOM-native court review dataset export for Blueprint 8 geometry evidence.

The export packages persisted court keypoints, court lines, camera/view observations, homography candidates, projection diagnostics, lineage, artifacts, and annotations for review. It does not create new geometry conclusions and does not mutate source observations.

## Command

```bash
.venv/bin/python -m apps.worker.cli export-court-review-dataset \
  --media-id <media_id> \
  --court-run-id <court_run_id> \
  --homography-run-id <homography_run_id> \
  --projection-diagnostic-run-id <projection_diagnostic_run_id>
```

The default export root is:

```text
.data/exports/court
```

The command writes a JSON artifact named:

```text
court_review_dataset.json
```

and stores an evidence artifact record with `artifact_type = court_review_dataset_export`.

## Export Shape

The JSON export uses:

```text
export_version = court_review_dataset_v0
```

Top-level sections include:

- media context
- processing runs
- model registry rows
- runtime config rows
- court keypoint observations
- court line observations
- camera/view observations
- homography candidate observations
- projection diagnostic observations
- lineage between selected court observations
- artifacts
- annotations
- evidence-only warnings

## Evidence Boundary

The export preserves these warnings:

- `geometry_evidence_only = true`
- `observation_only = true`
- `no_adjudication = true`
- `not_ball_player_projection = true`
- `no_tennis_event_interpretation = true`

The export is a review package. It is not a training format, an accepted court model, a line-call decision, or a tennis-event record.

## Run Selection

At least one run id is required:

- `court_run_id`
- `homography_run_id`
- `projection_diagnostic_run_id`

When supplied, `court_run_id` selects court keypoint, court line, and camera/view observations. `homography_run_id` selects homography candidates. `projection_diagnostic_run_id` selects projection diagnostics.

Lineage is included only for selected court observations in the exported dataset.

## Non-Goals

The review export does not add:

- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- accepted/rejected court lifecycle
- confirmed court model promotion
- production deployment
- adjudication
