# Fixture Court Evidence Adapter v0

Milestone 8B makes the Blueprint 8 court schema operational with deterministic fixture evidence.

The adapter writes court geometry evidence into the existing observation spine:

```text
indexed media
-> fixture court evidence adapter
-> court_keypoint_observation
-> court_line_observation
-> camera_view_observation
-> processing run / step provenance
```

This is fixture evidence only. It is not a real court model, not a homography computation, and not tennis-event interpretation.

## Command

```bash
.venv/bin/python -m apps.worker.cli run-fixture-court \
  --media-id <media_id> \
  --frame-sample-rate 30 \
  --max-frames 30
```

Plan-only mode does not touch the database:

```bash
.venv/bin/python -m apps.worker.cli run-fixture-court \
  --media-id media-plan \
  --plan-only
```

The Makefile helper is:

```bash
make court-fixture MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=30
```

## Evidence Produced

For each sampled media-owned frame, the adapter writes:

- one `court_keypoint_observation`
- one `court_line_observation`
- one `camera_view_observation`

Frame/time is owned by media indexing:

```text
frame_number -> frame_to_timestamp_ms(media.fps, frame_number)
```

The adapter samples every `frame_sample_rate` frames up to `max_frames`.

## Fixture Geometry

Court keypoints are derived from the normalized v0 court template and projected into image pixels with margins:

```text
x = margin_x + template_x * (media.width - 2 * margin_x)
y = margin_y + template_y * (media.height - 2 * margin_y)
```

Fixture margins are:

- `margin_x = media.width * 0.15`
- `margin_y = media.height * 0.20`

Court lines connect the v0 template keypoints in image-pixel coordinates. Camera/view rows default to `broadcast_hardcam`, `stable`, and fixture confidence values.

## Camera / View Read Layer

Milestone 8C reads the `camera_view_observation` rows produced by this adapter through:

```text
GET /court/camera-view?media_id=<media_id>&run_id=<court_run_id>
GET /court/camera-view/summary?media_id=<media_id>&run_id=<court_run_id>
GET /court/camera-view/<camera_view_observation_id>/bundle
```

These APIs expose geometry context evidence only. They do not compute homography or confirm camera state.

## Provenance

The adapter creates:

- `model_registry` row for `fixture-court-evidence-adapter`
- `runtime_config` row for `fixture-court-evidence-config`
- `processing_run` row named `fixture-court-evidence`
- `processing_step` row named `fixture_court_evidence_adapter`

Every emitted observation has:

- `observation_family = court`
- `frame_time_owner = media_indexing`
- `fixture_court_evidence = true`
- `observation_only = true`
- `no_adjudication = true`
- `geometry_evidence_only = true`
- `not_real_court_model = true`

## Explicit Non-Goals

8B and 8C do not create:

- homography candidates
- projection diagnostics
- replay court overlays
- real court model inference
- real camera model inference
- ball/player court-space projection
- bounce, hit, in/out, rally, point, or scoring conclusions
