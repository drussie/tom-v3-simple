# Homography Candidate Persistence v0

Milestone 8D adds homography candidate persistence for Blueprint 8.

The 8D flow is:

```text
indexed media
-> run-fixture-court
-> persisted court keypoint observations
-> persisted court line observations
-> persisted camera/view observations
-> build-homography-candidates
-> homography_candidate_observation rows
-> source court evidence lineage
```

The same persistence path can also consume real model-output `court_keypoint_observation` rows from the TOM v1 court keypoint adapter. In that case, homography metadata preserves source provenance such as `source_court_evidence_source = real_model_output` and `source_court_keypoint_real_model_output = true`. The calibration audit also preserves source preprocessing mode, coordinate interpretation, mapping version, and `source_court_keypoint_uncalibrated_mapping`.

Homography candidates are candidate geometry evidence. They are not confirmed court models, true transforms, in/out decisions, bounce locations, hit events, rally state, point reconstruction, or score evidence.

## Command

```bash
.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id <media_id> \
  --court-run-id <court_run_id>
```

Optional controls:

- `--run-name`
- `--frame-start`
- `--frame-end`
- `--min-keypoint-confidence`
- `--viewer-base-url`
- `--plan-only`

Makefile helper:

```bash
make homography-candidates \
  MEDIA_ID=<media_id> \
  COURT_RUN_ID=<court_run_id> \
  PYTHON=.venv/bin/python
```

## Builder Strategy

The v0 builder consumes persisted `court_keypoint_observation` rows from a source court run. For each usable frame, it:

- finds keypoints present in both the source observation and the normalized court template registry
- requires at least four usable source point pairs
- computes a candidate image-pixels-to-court-template transform
- stores matrix direction as `image_pixels_to_court_template_2d`
- stores the normalized template name/version
- computes keypoint reprojection metrics
- uses a bounded builder confidence score
- links optional source `court_line_observation` and `camera_view_observation` rows from the same frame when present

The v0 matrix method is a lightweight axis-aligned affine fit. It can be used with fixture or real keypoint rows, but it is still intentionally labeled as candidate geometry, not a confirmed court model. If real keypoints produce a poor overlay, treat that as model/mapping/fit uncertainty.

## Persisted Observation

The observation spine uses:

```text
observation_family = court
observation_type = homography_candidate_observation
granularity = frame
coordinate_space = court_template_2d
frame_time_owner = media_indexing
```

Typed rows include:

- source court keypoint observation id
- source court line observation id when available
- source camera/view observation id when available
- homography matrix
- inverse homography matrix when computable
- source and target coordinate spaces
- matrix direction
- template name/version
- reprojection error mean/median/max
- inlier/outlier counts
- source point and line counts
- confidence
- status `candidate`
- geometry-evidence-only metadata

## Lineage

For each persisted candidate, 8D writes lineage rows:

```text
court_keypoint_observation
-> homography_candidate_observation
relationship_type = homography_from_court_keypoints_candidate

court_line_observation
-> homography_candidate_observation
relationship_type = homography_from_court_lines_candidate

camera_view_observation
-> homography_candidate_observation
relationship_type = camera_context_for_homography_candidate
```

Lineage payloads preserve:

- `candidate_geometry = true`
- `geometry_evidence_only = true`
- `observation_only = true`
- `no_adjudication = true`

## Processing Provenance

The builder creates:

- model registry row: `fixture-homography-candidate-builder`
- runtime config row: `homography-candidate-builder-config`
- processing run row
- processing step row

Run and step metadata report source counts, candidate counts, insufficient-source-evidence counts, sampled frames, and evidence-only warnings.

## Output

The CLI returns JSON with:

- `homography_run_id`
- `model_registry_id`
- `runtime_config_id`
- `processing_step_id`
- candidate counts
- source counts
- sampled frames
- replay URL with `courtRunId` and `homographyRunId`
- warnings that the output is candidate geometry evidence only

The replay URL is consumed by Milestone 8E court overlays. 8D itself does not add replay court overlays.

Milestone 8F consumes persisted homography candidate rows as source evidence for projection diagnostics. A homography candidate remains a candidate coordinate transform even when a diagnostic row or review export references it. 8F does not change homography candidate semantics and does not use the candidate to create ball/player court-space projections.

## Non-Goals

8D does not add:

- projection diagnostics
- replay court overlays
- real court model inference
- ball/player court-space projection
- bounce/hit/in-out/rally/point/scoring
- real stream ingestion
- adjudication
