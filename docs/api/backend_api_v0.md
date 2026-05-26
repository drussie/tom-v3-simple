# Backend API v0

## Purpose

Backend API v0 provides the first TOM v3 Simple persistence and query surface for media, processing runs, observations, lineage, evidence artifacts, and human annotations.

The API records observations and evidence. It does not resolve final tennis outcomes.

## Run Locally

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
TOM_V3_CREATE_DB_ON_STARTUP=true .venv/bin/uvicorn apps.api.main:app --reload
```

For migration-managed local Postgres:

```bash
docker compose up -d postgres
TOM_V3_DATABASE_URL=postgresql+psycopg://tom_v3:tom_v3@localhost:5432/tom_v3 .venv/bin/alembic upgrade head
```

## Health

- `GET /health`

Returns:

```json
{"status": "ok"}
```

## Media

- `POST /media`
- `POST /media/register-file`
- `GET /media/{media_id}`

`POST /media` registers metadata manually.

`POST /media/register-file` indexes a real local media file. It runs ffprobe, calculates sha256, optionally copies the file into local TOM v3 storage, persists a `media_asset`, and stores the frame/time summary in `metadata_jsonb`.

Example:

```json
{
  "source_path": "/path/to/video.mp4",
  "copy_to_storage": true,
  "media_name": "practice clip",
  "storage_root": ".data/media"
}
```

The response is a `media_asset` record with duration, frame count, FPS, dimensions, checksum, and media indexing metadata.

## Models and Runtime Configs

- `POST /models`
- `GET /models/{model_id}`
- `POST /runtime-configs`
- `GET /runtime-configs/{runtime_config_id}`

Synthetic/dev models are valid model registry entries.

## Runs and Steps

- `POST /media/{media_id}/runs`
- `GET /runs/{run_id}`
- `POST /runs/{run_id}/steps`
- `GET /runs/{run_id}/steps`

Run and step status values:

- queued
- running
- completed
- failed
- partial

## Observations

- `POST /observations`
- `POST /observations/batch`
- `POST /observations/query`
- `GET /observations/{observation_id}`
- `GET /observations/{observation_id}/lineage`
- `GET /observations/{observation_id}/artifacts`
- `GET /observations/{observation_id}/annotations`

All observation writes go through the central observation writer.

Supported typed extensions:

- `gameplay`
- `atomic`
- `derived`

Minimum query filters:

- `media_id`
- `run_id`
- `observation_family`
- `observation_type`
- `frame_start_gte`
- `frame_end_lte`
- `timestamp_start_gte`
- `timestamp_end_lte`
- `confidence_gte`
- `confidence_lte`
- `gameplay_label`
- `tracklet_id`

## Artifacts

- `POST /artifacts`
- `GET /artifacts/{artifact_id}`
- `GET /artifacts/{artifact_id}/content`

Artifacts are metadata records in v0. They may point to placeholder URIs.

`GET /artifacts/{artifact_id}/content` serves local artifact files for development inspection, such as extracted frame images from Milestone 1E. This is not a production object storage or auth design.

## Annotations

- `POST /annotations`
- `GET /observations/{observation_id}/annotations`

Annotations do not mutate observations.

## Dev Synthetic Path

- `POST /dev/synthetic-run`

This dev-only endpoint reuses the shared worker/seeding library and creates:

- media asset
- runtime config
- synthetic model registry entry
- processing run
- processing steps
- gameplay, non_gameplay, and uncertain observations
- atomic ball observations
- atomic near-player and far-player observations
- tracklets and track points
- homography placeholder observations
- derived bounce_candidate, hit_candidate, and tracking_gap_candidate placeholders
- lineage links
- evidence artifact placeholders

This endpoint proves backend persistence and uses the same shared synthetic seed function as the worker CLI. It is still dev-only.

## Viewer Composition

- `GET /viewer/runs/{run_id}`

This endpoint composes existing persisted rows for the visual evidence viewer:

- run metadata
- media metadata
- processing steps
- observations with typed gameplay, atomic, or derived detail
- tracklets and track points
- lineage rows
- evidence artifact metadata
- human annotations

The endpoint is a read model over stored evidence. It does not create observations or add new interpretation logic.
