# Milestone 8B - Court Keypoint / Line Evidence Adapter

Status: COMPLETE

Milestone 8B adds a deterministic fixture court evidence adapter that writes court keypoint, court line, and camera/view observations into the 8A schema.

## Proved

```text
indexed media
-> fixture court evidence adapter
-> model registry / runtime config
-> processing run / step
-> media-owned frame sampling
-> court_keypoint_observation
-> court_line_observation
-> camera_view_observation
```

The adapter is available through:

```bash
.venv/bin/python -m apps.worker.cli run-fixture-court --media-id <media_id>
make court-fixture MEDIA_ID=<media_id>
```

Plan-only mode is available and does not touch the database.

## Boundaries Preserved

8B does not add homography computation, projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or TOM v2-style adjudication.

Court evidence remains fixture geometry evidence, not a confirmed court model.
