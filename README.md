# TOM v3 Simple

TOM v3 Simple is a lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Observation-Only Boundary

TOM v3 Simple is not TOM v2.

It does not adjudicate truth. It records observations, lineage, artifacts, and annotations.

The core invariant:

> TOM v3 records what was observed, not what was proven.

## Current Status

Milestone 2D adds tracklet evidence export / review dataset artifacts on top of persisted ball/player detections and candidate tracklets:

- repo memory and architecture contracts
- FastAPI backend/API foundation
- SQLAlchemy observation store and Alembic migration
- central observation writer
- worker CLI and rich synthetic seeder
- viewer-ready synthetic baseline data
- Next.js visual evidence viewer foundation
- local setup, runbook, Makefile, and smoke validation
- real local media registration with ffprobe metadata extraction
- sha256 checksum persistence
- local storage copy/register modes
- centralized frame/time mapping utilities
- gameplay adapter interface
- fixture gameplay adapter for deterministic dev/test output
- TOM v1 gameplay adapter integration stub and portability assessment
- worker command to persist gameplay/non_gameplay/uncertain observations
- detection adapter interface
- fixture detector for deterministic ball/player dev/test output
- YOLO26 detection adapter unavailable stub and portability assessment
- worker command to persist ball_detection/player_detection atomic observations
- detection overlay transform and coordinate-space bbox panel
- selected detection highlighting in the viewer
- detection timeline row and safe missing-bbox states
- ffmpeg-backed frame artifact extraction
- local frame artifact metadata persisted as evidence artifacts
- viewer frame images behind persisted detection bboxes when available
- deterministic tracklet builder from persisted detections
- worker command to persist candidate tracklet and track point rows
- first-class tracklet and track point observation spine rows
- lineage from source detections to track points and from track points to tracklets
- dynamic tracklet evidence bundle API
- viewer panel for tracklet candidate, track point candidate, source detection, frame artifact, and lineage inspection
- structured tracklet query API
- annotation summaries for tracklet evidence bundles
- viewer review controls for annotating tracklet candidates, track point candidates, and source detections
- review dataset export service, API, and worker CLI for packaging candidate tracklet evidence as JSON artifacts

Portable TOM v1 detector assets/source and YOLO26 runtime/assets are not present in this repo state. No sophisticated tracking, pose processing, court homography, or real bounce detection is implemented yet.

## Repo Structure

```text
apps/
  api/       FastAPI backend foundation.
  worker/    Worker CLI and rich synthetic seeding entrypoint.
  web/       Visual evidence viewer foundation.
packages/
  schema/          Shared schema contracts.
  storage/         Storage adapters and persistence helpers.
  video/           ffprobe metadata and frame/time mapping utilities.
  model_adapters/  Gameplay and detection adapter interfaces and fixtures.
  observations/    Observation writer, lineage, and synthetic helpers.
  visualization/   Viewer-oriented utilities placeholder.
migrations/        Alembic database migrations.
scripts/           Local smoke and developer scripts.
tests/             Backend, worker, viewer, and integration tests.
docs/              Durable project memory and architecture contracts.
```

## Quickstart

Create a local environment:

```bash
conda create -n tom_v3 python=3.11 -y
conda activate tom_v3
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Install web dependencies:

```bash
cd apps/web
npm install
cd ../..
```

Set local defaults:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
export TOM_V3_CREATE_DB_ON_STARTUP=true
export NEXT_PUBLIC_TOM_V3_API_BASE_URL="http://127.0.0.1:8000"
```

Run migrations:

```bash
alembic upgrade head
```

Index a real local video:

```bash
python -m apps.worker.cli index-media \
  --source-path /path/to/video.mp4 \
  --copy-to-storage
```

The media indexing path uses `ffprobe`, calculates a sha256 checksum, optionally copies the source into `.data/media/{media_id}/`, and persists a `media_asset` with duration, FPS, frame count, dimensions, checksum, storage metadata, and a frame/time summary.

The same path is available through the API:

```bash
uvicorn apps.api.main:app --reload
curl -X POST http://127.0.0.1:8000/media/register-file \
  -H "Content-Type: application/json" \
  -d '{"source_path":"/path/to/video.mp4","copy_to_storage":true}'
```

Run the gameplay adapter fixture for indexed media:

```bash
python -m apps.worker.cli run-gameplay-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

Or index and run in one local command:

```bash
python -m apps.worker.cli index-and-run-gameplay \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

Open the returned `run_id` in the viewer:

```text
http://127.0.0.1:3000/runs/<RUN_ID>
```

Run the detection adapter fixture for indexed media:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --frame-sample-rate 30 \
  --max-frames 5 \
  --output-debug-artifact
```

Or index and run detection in one local command:

```bash
python -m apps.worker.cli index-and-run-detection \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

Extract frame artifacts for a detection run:

```bash
python -m apps.worker.cli extract-frame-artifacts \
  --run-id <DETECTION_RUN_ID> \
  --max-frames 2 \
  --output-root .data/artifacts
```

Build candidate tracklets from a detection run:

```bash
python -m apps.worker.cli build-tracklets \
  --detection-run-id <DETECTION_RUN_ID> \
  --max-gap-frames 30
```

Seed synthetic evidence:

```bash
python -m apps.worker.cli seed-synthetic-run \
  --scenario baseline-tennis-clip \
  --source-uri file:///dev/synthetic-tennis-clip.mp4 \
  --run-name synthetic-baseline-run
```

Use the `run_id` from the seed output to verify:

```bash
python -m apps.worker.cli verify-synthetic-run --run-id <RUN_ID>
```

Start the API:

```bash
uvicorn apps.api.main:app --reload
```

Start the web viewer in another terminal:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open:

```text
http://127.0.0.1:3000/runs/<RUN_ID>
```

For a detection adapter run, the viewer shows a detection overlay. The panel uses persisted `image_pixels` bbox payloads and media dimensions; when frame artifacts exist, it displays the extracted frame image behind the bboxes. If no frame artifact is available, it displays an honest frame-space canvas.

For a tracklet builder run, the viewer shows candidate tracklet coverage rows, track point candidate observations, and lineage. Source detection observations remain linked through `observation_lineage` and `track_point.payload_jsonb.source_detection_observation_id`.

The tracklet evidence bundle endpoint exposes the cross-run evidence path:

```text
GET /tracklets/<TRACKLET_ID>/evidence-bundle
```

When a tracklet builder run is open in the viewer, selecting a tracklet loads that bundle and shows source detection evidence from the detection run.

Tracklet candidates can be queried with structured filters:

```bash
curl -X POST http://127.0.0.1:8000/tracklets/query \
  -H "Content-Type: application/json" \
  -d '{"track_family":"ball","min_track_points":2,"has_gaps":true}'
```

The viewer Tracklet Evidence panel can add review annotations to the selected tracklet candidate, track point candidate, or source detection observation. These annotations are persisted as `human_annotation` rows and do not mutate the underlying evidence.

Export candidate tracklet review evidence:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"track_family":"ball","has_annotation":true}' \
  --output-root .data/exports
```

Or export explicit tracklets:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --tracklet-id <TRACKLET_ID> \
  --output-root .data/exports
```

The export writes `.data/exports/tracklets/{export_id}/tracklet_review_dataset.json`, persists a `tracklet_review_dataset_export` evidence artifact with checksum, and includes candidate-only and no-adjudication warnings. Exports package evidence; they do not create adjudicated labels.

## Validation

Run the consolidated checks:

```bash
pytest -q
ruff check .
cd apps/web && npm run lint && npm run build && npm audit --omit=dev
```

Run the Milestone 0 smoke check:

```bash
python scripts/smoke_synthetic_viewer_data.py
```

The root `Makefile` wraps common commands:

```bash
make install
make web-install
make test
make lint
make migrate
make index-media SOURCE_PATH=/path/to/video.mp4
make run-gameplay MEDIA_ID=<media_id>
make index-and-run-gameplay SOURCE_PATH=/path/to/video.mp4
make run-detection MEDIA_ID=<media_id>
make index-and-run-detection SOURCE_PATH=/path/to/video.mp4
make extract-frame-artifacts RUN_ID=<detection_run_id>
make build-tracklets DETECTION_RUN_ID=<detection_run_id>
make seed
make smoke
make all-checks
```

## Docs Entrypoint

Start with [docs/CONTROL_ROOM_INDEX.md](docs/CONTROL_ROOM_INDEX.md).

Useful runbooks:

- [Local Environment Setup](docs/dev/local_environment_setup.md)
- [Local Demo Runbook](docs/dev/local_demo_runbook.md)
- [Media Indexing v0](docs/media/media_indexing_v0.md)
- [Frame Artifacts v0](docs/media/frame_artifacts_v0.md)
- [Gameplay Adapter v0](docs/model_adapters/gameplay_adapter_v0.md)
- [Detection Adapter v0](docs/model_adapters/detection_adapter_v0.md)
- [Detection Overlay Viewer v0](docs/web/detection_overlay_viewer_v0.md)
- [Frame Artifact Overlay v0](docs/web/frame_artifact_overlay_v0.md)
- [Tracklet Foundation v0](docs/tracklets/tracklet_foundation_v0.md)
- [Tracklet Evidence Bundle v0](docs/tracklets/tracklet_evidence_bundle_v0.md)
- [Tracklet Evidence Viewer v0](docs/web/tracklet_evidence_viewer_v0.md)
- [Tracklet Query v0](docs/tracklets/tracklet_query_v0.md)
- [Tracklet Review Annotations v0](docs/tracklets/tracklet_review_annotations_v0.md)
- [Tracklet Review Viewer v0](docs/web/tracklet_review_viewer_v0.md)
- [Repo Branch Hygiene](docs/dev/repo_branch_hygiene.md)
