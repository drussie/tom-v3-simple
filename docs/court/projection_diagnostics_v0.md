# Projection Diagnostics v0

Milestone 8F adds projection diagnostic observations for Blueprint 8 court geometry evidence.

Projection diagnostics are review evidence. They project the normalized court template back into image-pixel space from a persisted homography candidate so an operator can inspect how the candidate geometry lines up with observed court evidence.

They do not confirm a court model, project ball/player observations into court space, decide line calls, infer bounce/hit events, or add adjudication.

Projection diagnostics can now be built from homography candidates whose source court keypoints came from the TOM v1 real court keypoint adapter. Those diagnostics are still review evidence. A better-looking projection is not a verified court, and a poor projection should be treated as evidence of model, mapping, preprocessing, or fit uncertainty.

## Flow

```text
indexed media
-> run-fixture-court
-> build-homography-candidates
-> homography_candidate_observation rows
-> build-projection-diagnostics
-> projection_diagnostic_observation rows
-> lineage from homography candidate
```

## Builder

The worker command is:

```bash
.venv/bin/python -m apps.worker.cli build-projection-diagnostics \
  --media-id <media_id> \
  --homography-run-id <homography_run_id>
```

Plan-only mode:

```bash
.venv/bin/python -m apps.worker.cli build-projection-diagnostics \
  --media-id media-plan \
  --homography-run-id homography-run-plan \
  --plan-only
```

The builder validates media and homography run existence, reads persisted `homography_candidate_observation` rows, projects the court template into image pixels, persists `projection_diagnostic_observation` rows through `ObservationWriter`, and writes lineage from the source homography candidate.

## Projection Method

Homography candidates usually store:

```text
matrix_direction = image_pixels_to_court_template_2d
```

For diagnostics, the builder uses `inverse_homography_matrix_jsonb` to map template coordinates back into image pixels.

If a candidate uses:

```text
matrix_direction = court_template_2d_to_image_pixels
```

the builder can use `homography_matrix_jsonb` directly.

If no usable matrix exists, the diagnostic row is written with `status = insufficient_homography`.

## Payload Contract

Projection diagnostic rows use:

```text
observation_family = court
observation_type = projection_diagnostic_observation
coordinate_space = image_pixels
frame_time_owner = media_indexing
```

The typed detail includes:

- `source_homography_candidate_observation_id`
- `projected_template_keypoints_jsonb`
- `projected_template_lines_jsonb`
- `diagnostic_metrics_jsonb`
- `status`
- `confidence`
- `model_id`
- `runtime_config_id`

Projected keypoint records include template and image coordinates:

```json
{
  "name": "near_left_baseline_corner",
  "template_x": 0.0,
  "template_y": 0.0,
  "image_x": 192.0,
  "image_y": 216.0,
  "valid": true
}
```

Projected line records include projected image endpoints:

```json
{
  "line_class": "baseline_near",
  "start_keypoint": "near_left_baseline_corner",
  "end_keypoint": "near_right_baseline_corner",
  "x1": 192.0,
  "y1": 216.0,
  "x2": 1728.0,
  "y2": 216.0,
  "valid": true
}
```

## Metrics

The v0 diagnostic metrics are intentionally simple:

- source homography status
- projected keypoint and line counts
- source point and line counts
- source reprojection error metrics
- source homography confidence
- optional line-count delta
- `diagnostic_method = template_projection_diagnostic_v0`

These metrics are diagnostic context only. They do not establish geometry correctness.

## Lineage

Every diagnostic row links back to its source homography candidate:

```text
homography_candidate_observation
-> projection_diagnostic_observation
relationship_type = projection_diagnostic_for_homography_candidate
```

Lineage payloads preserve:

- `geometry_evidence_only = true`
- `diagnostic_candidate = true`
- `observation_only = true`
- `no_adjudication = true`
- `not_ball_player_projection = true`

No ball/player detections, tracklets, or pose observations are source parents for projection diagnostics.

## Replay Support

8F adds replay overlay payload support for `projectionDiagnosticRunId`.

The replay workstation can display projected template keypoints and lines as projection diagnostic evidence when that run is supplied:

```text
/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>&projectionDiagnosticRunId=<projection_diagnostic_run_id>
```

This overlay is display-only. It does not write diagnostic rows from the frontend and does not project objects into court space.

## Non-Goals

8F does not add:

- ball/player court-space projection
- tracklet court-space projection
- bounce/hit/in-out/rally/point/scoring
- accepted/rejected court lifecycle
- confirmed court model
- real court model inference
- real stream ingestion
- adjudication
