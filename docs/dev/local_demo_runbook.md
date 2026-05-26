# Local Demo Runbook

This runbook exercises the Milestone 0 loop:

```text
synthetic seed -> persisted observations -> backend API -> visual evidence viewer
```

## 1. Activate Environment

```bash
conda activate tom_v3
```

Or activate any Python 3.11 environment where `pip install -e ".[dev]"` has been run.

## 2. Configure Local Database

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
export TOM_V3_CREATE_DB_ON_STARTUP=true
```

## 3. Run Migrations

```bash
alembic upgrade head
```

## 4. Seed Synthetic Evidence

```bash
python -m apps.worker.cli seed-synthetic-run \
  --scenario baseline-tennis-clip \
  --source-uri file:///dev/synthetic-tennis-clip.mp4 \
  --run-name synthetic-baseline-run
```

The seed command prints JSON. Use the `run_id` value from that output.

## 5. Verify Seeded Evidence

```bash
python -m apps.worker.cli verify-synthetic-run --run-id <RUN_ID>
```

The verifier should return `"ok": true`.

## 6. Start Backend

```bash
uvicorn apps.api.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

## 7. Start Frontend

In a separate terminal:

```bash
cd apps/web
npm install
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

The viewer will be available at:

```text
http://127.0.0.1:3000
```

## 8. Open the Viewer

Open:

```text
http://127.0.0.1:3000/runs/<RUN_ID>
```

The viewer should show:

- media metadata
- gameplay, non_gameplay, and uncertain bands
- ball, near-player, and far-player track coverage rows
- homography valid/missing ranges
- candidate markers
- observation detail
- lineage and artifact panels

## 9. One-Command Smoke Check

The integration smoke script seeds a temporary run and validates the viewer read model:

```bash
python scripts/smoke_synthetic_viewer_data.py
```

## 10. Index a Real Local Video

Milestone 1A adds real media registration:

```bash
python -m apps.worker.cli index-media \
  --source-path /path/to/video.mp4 \
  --copy-to-storage \
  --storage-root .data/media
```

The command prints a `media_id`, stored URI, checksum, ffprobe metadata, and frame/time summary.

The API equivalent is:

```bash
curl -X POST http://127.0.0.1:8000/media/register-file \
  -H 'Content-Type: application/json' \
  -d '{
    "source_path": "/path/to/video.mp4",
    "copy_to_storage": true,
    "storage_root": ".data/media"
  }'
```

## 11. Run Gameplay Adapter On Indexed Media

Milestone 1B adds a worker-driven gameplay adapter path.

Run the deterministic fixture adapter:

```bash
python -m apps.worker.cli run-gameplay-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture
```

Or index and run in one command:

```bash
python -m apps.worker.cli index-and-run-gameplay \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

The command prints a `run_id`. Start the backend and web app, then open:

```text
http://127.0.0.1:3000/runs/<RUN_ID>
```

The viewer should show the gameplay/non_gameplay/uncertain band from persisted gameplay observations.

The real TOM v1 detector is not wired in this repo state. `--adapter tom-v1` is present as an integration stub and reports that portable TOM v1 assets/source are unavailable.
