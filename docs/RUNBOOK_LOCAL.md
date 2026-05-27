# TOM v3 Simple Local Runbook

This is the canonical local runbook for TOM v3 Simple.

It is written for a new developer who wants to prove the local observation loop without YOLO weights, real pose weights, GPU setup, or prior control-room context.

For the short current-status map, start with:

- [Control Room](CONTROL_ROOM.md)
- [Architecture](ARCHITECTURE.md)
- [Observation Contract](OBSERVATION_CONTRACT.md)
- [Blueprint Status](BLUEPRINT_STATUS.md)
- [Known Limitations](KNOWN_LIMITATIONS.md)
- [Optional YOLO](OPTIONAL_YOLO.md)
- [Exports](EXPORTS.md)
- [Completion Checklist](COMPLETION_CHECKLIST.md)

## 1. What TOM v3 Simple Is

TOM v3 Simple is a local observation platform for tennis video evidence.

It can:

- index local media
- persist gameplay, detection, tracklet, and pose observations
- preserve lineage between observations
- extract frame-backed artifacts
- show evidence in the viewer
- support review annotations
- export TOM-native review datasets

Core invariant:

```text
TOM v3 records evidence. It does not decide official tennis meaning.
```

## 2. What TOM v3 Simple Is Not

TOM v3 Simple does not:

- decide a point, score, rally, hit, bounce, serve, or stroke
- adjudicate observations into official results
- infer movement or biomechanics from pose
- identify a player as known
- require real YOLO or real pose inference for the fixture demo

Fixture outputs are demo evidence only. They prove the local persistence, viewer, review, lineage, and export plumbing.

## 3. Prerequisites

Create and activate the base environment:

```bash
conda create -n tom_v3 python=3.11 -y
conda activate tom_v3
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Install frontend dependencies:

```bash
cd apps/web
npm install
cd ../..
```

Set the local database URL:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
export TOM_V3_CREATE_DB_ON_STARTUP=true
```

Run migrations:

```bash
alembic upgrade head
```

The default fixture demo can generate a tiny synthetic placeholder media file with `ffmpeg` when no media path is supplied. To use your own media, set `DEMO_MEDIA_PATH`.

## 4. Run The Fixture Demo

The canonical demo command is:

```bash
make demo
```

If your shell's default `python` is not the TOM v3 environment, pass the interpreter explicitly:

```bash
make demo PYTHON=.venv/bin/python
```

To preview the plan without touching local data:

```bash
make demo-plan
```

The default media priority is:

1. `DEMO_MEDIA_PATH` if set and present
2. `demo_assets/tennis_fixture.mp4` if present
3. generated `.data/demo/media/synthetic_demo_media.mp4`

Use custom media:

```bash
DEMO_MEDIA_PATH=/path/to/video.mp4 make demo
```

Use a sample asset and isolated demo database:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
```

Then audit the same database:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point.db \
make completion-audit PYTHON=.venv/bin/python
```

Local video files under `demo_assets/` should not be committed unless intentionally tracked.

The demo runs this fixture-only path:

```text
resolve media
-> index media
-> run fixture gameplay adapter
-> run fixture detection adapter
-> extract frame artifacts
-> build candidate tracklets
-> run fixture pose adapter
-> seed review annotations
-> export pose review dataset
-> export tracklet review dataset
-> print summary
```

The printed JSON summary includes media id, run ids, observation counts, artifact counts, annotation count, export artifact ids, export paths, viewer URLs, and warnings.

Run the structural provenance audit after the demo:

```bash
make completion-audit
```

The audit checks media, processing runs/steps, observations, typed rows, lineage, artifacts, annotations, and review exports. It does not check model correctness or decide tennis meaning.

For the final checklist, see [Completion Checklist](COMPLETION_CHECKLIST.md).

## 5. Open The Viewer

Start the backend:

```bash
uvicorn apps.api.main:app --reload
```

Start the frontend in another terminal:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open the viewer URLs from the demo summary:

```text
http://127.0.0.1:3000/runs/<detection_run_id>
http://127.0.0.1:3000/runs/<tracklet_run_id>
http://127.0.0.1:3000/runs/<pose_run_id>
```

You can also print a URL helper:

```bash
make demo-open RUN_ID=<run_id>
```

The viewer includes a run evidence summary, observation counts, lineage and annotation counts, and review export artifact summaries when the selected run payload includes them.

Viewer copy uses evidence and candidate wording. Fixture outputs are not presented as real tennis understanding.

## 5A. Open The Replay Workstation

Blueprint 6 adds a media-centric replay route:

```text
http://127.0.0.1:3000/replay/<media_id>
```

After `make demo`, use the `media_id` from the demo summary:

```bash
make replay-open MEDIA_ID=<media_id>
```

The replay route loads the indexed local video through the API and shows:

- current video time
- current timestamp in milliseconds
- nearest TOM frame from indexed media metadata
- fps and frame count
- basic timeline/progress shell
- available detection, tracklet, pose, and gameplay run context
- persisted detection observation overlays when a detection run is selected
- persisted tracklet candidate overlays when a tracklet run is selected
- persisted pose keypoint overlays when a pose run is selected

Optional context query parameters:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<run_id>&trackletRunId=<run_id>&poseRunId=<run_id>
```

`detectionRunId`, `trackletRunId`, and `poseRunId` select the persisted evidence runs to draw over the replay video.

Expected 6D replay behavior:

- video playback updates current TOM timestamp and nearest frame
- detection boxes appear near persisted detection timestamps
- tracklet candidate points and selected candidate paths appear near persisted track point timestamps
- pose keypoints and skeleton edges appear near persisted pose timestamps
- timeline lanes show detection observations, tracklet candidates, pose observations, and review annotations
- clicking a timeline item seeks playback and selects persisted evidence detail
- the detection layer can be hidden or shown
- the tracklet and pose layers can be hidden or shown
- clicking an overlay selects persisted evidence detail
- the selected detail panel shows observation id/run id, frame/time, confidence, and source context where available

Replay overlays are observation evidence. They are not confirmed objects, player identity, movement analysis, or tennis events.

## 6. Inspect Detections

Open:

```text
http://127.0.0.1:3000/runs/<detection_run_id>
```

Expected:

- persisted `ball_detection` and `player_detection` observations appear
- bbox overlays use stored image-pixel coordinates
- extracted frame artifacts appear behind bboxes when available
- selected observations show payload, artifacts, lineage, and annotations
- empty states explain how to create missing frame artifacts or detection evidence

Fixture detections are demo evidence only. They are not real model findings.

## 7. Inspect Tracklets

Open:

```text
http://127.0.0.1:3000/runs/<tracklet_run_id>
```

Expected:

- candidate tracklets appear as derived evidence
- track point candidates reference source detections
- lineage explains how persisted detections were grouped
- review annotations are shown as review evidence
- the tracklet panel uses candidate wording and describes source detection context

Candidate tracklets are not accepted tennis events.

## 8. Inspect Pose Observations

Open:

```text
http://127.0.0.1:3000/runs/<pose_run_id>
```

Expected:

- persisted `player_pose_observation` rows appear
- COCO17 keypoints and skeleton edges render from stored coordinates
- missing keypoints remain missing evidence
- source association fields use candidate language
- keypoint confidence rows are inspectable
- missing keypoints are listed as missing evidence and are not drawn as present markers

Fixture pose output is not real pose inference and does not interpret movement.

## 9. Add Or Inspect Review Annotations

The demo seeds a small set of review annotations:

- one detection annotation
- one tracklet annotation
- one pose keypoint annotation

They use:

```text
created_by = tom-v3-demo
```

Annotations are review evidence. They do not mutate observations, detections, tracklets, pose rows, or exports.

The viewer annotation panel shows keypoint metadata, notes, demo-seeded metadata, and review-only metadata when present.

Add a pose annotation through the generic annotation API:

```bash
curl -X POST http://127.0.0.1:8000/annotations \
  -H "Content-Type: application/json" \
  -d '{
    "observation_id":"<pose_observation_id>",
    "annotation_type":"bad_keypoint",
    "payload_jsonb":{
      "annotation_label":"bad_keypoint",
      "keypoint_name":"right_wrist",
      "keypoint_index":10
    },
    "created_by":"local-reviewer"
  }'
```

## 10. Export Review Datasets

The demo creates at least:

- a pose review dataset export
- a tracklet review dataset export

Export files are written under:

```text
.data/exports/
```

Export a pose review dataset manually:

```bash
python -m apps.worker.cli export-pose-review-dataset \
  --run-id <pose_run_id> \
  --output-root .data/exports
```

Export a tracklet review dataset manually:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"tracklet_run_id":"<tracklet_run_id>","limit":500}' \
  --output-root .data/exports
```

The exports are TOM-native JSON review datasets. They are not official labels or adjudicated results.

## 11. Optional YOLO Runtime

The fixture demo does not require YOLO.

Probe the optional runtime:

```bash
make yolo-probe
```

Preview the real-YOLO smoke plan:

```bash
make yolo-smoke
```

Real YOLO smoke requires:

- optional YOLO dependencies installed from `requirements-yolo.txt`
- local model weights outside git
- model registration through `register-yolo-model`
- local media

YOLO smoke remains separate from `make demo`. A YOLO smoke failure must not block the fixture demo.

## 12. Optional Custom Media

Use a local video:

```bash
DEMO_MEDIA_PATH=/path/to/video.mp4 make demo
```

Or pass it directly:

```bash
python -m apps.worker.cli run-demo --source-path /path/to/video.mp4
```

If neither custom media nor `demo_assets/tennis_fixture.mp4` exists, the demo generates synthetic placeholder media and marks it with:

```text
synthetic_demo_media = true
```

Synthetic placeholder media is not tennis footage.

## 13. Troubleshooting

If imports fail, install the editable package:

```bash
pip install -e ".[dev]"
```

If migrations are missing:

```bash
alembic upgrade head
```

If the generated media fallback fails, install `ffmpeg` or set `DEMO_MEDIA_PATH`:

```bash
DEMO_MEDIA_PATH=/path/to/video.mp4 make demo
```

If the frontend cannot reach the backend:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

If you want a fresh demo database without deleting existing data:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo.db make demo
```

The `demo-reset` target is intentionally non-destructive:

```bash
make demo-reset
```

If the provenance audit reports no demo media:

```bash
make demo
make completion-audit
```

To audit all local rows instead of only demo-marked media:

```bash
python -m apps.worker.cli completion-audit --no-demo-only
```

## 14. Known Limitations

- Fixture detection and pose output are deterministic demo evidence.
- Real YOLO runtime is optional and locally gated.
- Real pose inference is not implemented.
- Pose is keypoint evidence only, not movement interpretation.
- Tracklets are candidates, not official rallies or points.
- No homography, bounce, hit, rally, point, score, or adjudication is produced.
- Cloud deployment, auth, production streaming, and multi-camera reasoning are out of scope.

## 15. Completion Checklist

Run the local demo:

```bash
make demo
```

Run validation:

```bash
pytest -q
ruff check .
python scripts/smoke_synthetic_viewer_data.py
```

Run the provenance audit after `make demo`:

```bash
make completion-audit
```

Run web validation:

```bash
cd apps/web
npm run lint
npm run build
npm audit --omit=dev
```

Run migration smoke:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_migration_check.db alembic upgrade head
```

Expected result:

- fixture demo completes without YOLO or real pose weights
- viewer URLs are printed
- review exports are written
- observations remain evidence only
- no tennis-event interpretation appears
