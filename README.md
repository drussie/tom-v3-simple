# TOM v3 Simple

TOM v3 Simple is a lightweight tennis video observation platform that accepts model output as operational evidence, persists every atomic observation — including gameplay/non-gameplay state — and makes the evidence queryable and visually replayable without adjudicating truth.

## Observation-Only Boundary

TOM v3 Simple is not TOM v2.

It does not adjudicate truth. It records observations, lineage, artifacts, and annotations.

The core invariant:

> TOM v3 records what was observed, not what was proven.

## Current Status

Blueprints 1, 2, and 3 are complete. Blueprint 4 is in progress with pose evidence schema, normalization, persistence, lineage, overlay viewer, query, review, and export foundations. TOM v3 Simple can build, inspect, query, review, and export candidate temporal evidence on top of persisted ball/player detections, has an optional YOLO / Ultralytics runtime path for ball/player observation adapters, and now has first-class pose observation review/export contracts:

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
- YOLO detection adapter guarded runtime path and YOLO26 portability assessment
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
- Blueprint 2 completion review and invariant audit
- optional `requirements-yolo.txt` dependency path for a separate `tom_v3_yolo` environment
- YOLO runtime probe and device resolver for Ultralytics, Torch, OpenCV, CUDA, and MPS diagnostics
- YOLO weights validation and model registry registration without inference
- YOLO-like output normalization into TOM v3-compatible detection payloads
- YOLO frame inference provider boundary and mocked YOLO detection persistence through the existing detection adapter path
- optional real-YOLO local smoke helper and viewer validation workflow
- Blueprint 3 completion review and runtime invariant audit
- Blueprint 4 pose observation schema foundation
- COCO17 skeleton registry and keypoint validation helpers
- typed `pose_observation` persistence with keypoint summary statistics
- fake/serialized pose output normalization into `PoseObservationCreate`-compatible payloads
- crop-local to full-frame pose keypoint projection
- synthetic/fake pose observation insertion for schema and persistence validation
- worker fixture pose persistence with processing run/step provenance
- source `player_detection` candidate lineage to pose observations
- pose overlay viewer for persisted COCO17 keypoint evidence
- selected pose metadata, source association candidate context, and keypoint confidence table
- pose-specific query API and evidence bundle service
- pose review labels with keypoint-level annotation metadata
- worker/API pose review dataset export as local TOM-native JSON artifacts
- model asset and weight ignore policy

Portable TOM v1 detector assets/source and YOLO26 model weights are not present in this repo state. Real YOLO inference now has a guarded frame-level provider path and optional local smoke workflow, but local runtime validation still requires optional YOLO packages and explicitly registered local weights. Pose currently has schema, normalization, persistence, lineage, overlay viewer, query, review, and export foundations only; no real pose runtime, movement interpretation, court homography, or real bounce detection is implemented yet.

Blueprint 2 did not add pose, homography, bounce detection, hit detection, rally/point reconstruction, scoring, identity proof, or adjudication.

Blueprint 3 did not add pose, homography, bounce detection, hit detection, rally/point reconstruction, scoring, identity proof, YOLO tracking mode, or adjudication.

Blueprint 4A/4B/4C/4D/4E did not add real pose inference, movement interpretation, serve/hit/split-step/biomechanics conclusions, homography, rally/point reconstruction, scoring, or adjudication.

Recommended next milestone: Milestone 4F - Blueprint 4 Completion Review / Pose Evidence Hardening.

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

Probe the optional YOLO runtime:

```bash
python -m apps.worker.cli yolo-runtime-probe
python -m apps.worker.cli yolo-runtime-probe --device cpu
```

For real YOLO runtime work, keep the base `tom_v3` environment clean and create a separate optional environment:

```bash
conda create -n tom_v3_yolo python=3.11 -y
conda activate tom_v3_yolo
python -m pip install --upgrade pip
pip install -e ".[dev]"
pip install -r requirements-yolo.txt
python -m apps.worker.cli yolo-runtime-probe
```

Model weights are local assets, not source code. The repo ignores `model_assets/`, `weights/`, `*.pt`, `*.pth`, `*.onnx`, and `*.engine`.

Validate and register local YOLO weights without running inference:

```bash
mkdir -p model_assets/yolo
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name <model-name> \
  --model-version v0 \
  --device cpu
```

The command fingerprints the file, validates the class mapping, creates or reuses a `model_registry` row, and does not create processing runs or observations.

Normalize fake YOLO-like output without inference:

```bash
python - <<'PY'
from tom_v3_model_adapters.yolo_normalization import normalize_yolo_frame_result

result = normalize_yolo_frame_result({
    "frame_number": 120,
    "timestamp_ms": 4000,
    "boxes": [
        {"xyxy": [100, 200, 140, 240], "confidence": 0.91, "class_id": 32, "class_name": "sports ball"},
        {"xyxy": [500, 150, 700, 900], "confidence": 0.87, "class_id": 0, "class_name": "person"},
    ],
})
print(result.as_dict())
PY
```

Run the guarded YOLO detection path when optional runtime packages and registered weights are available:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter yolo \
  --model-registry-id <MODEL_REGISTRY_ID> \
  --device cpu \
  --image-size 640 \
  --confidence-threshold 0.25 \
  --iou-threshold 0.7 \
  --max-det 50 \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --output-debug-artifact
```

If runtime packages or weights are unavailable, the YOLO path fails clearly and does not fall back to fixture detections. Mocked provider tests cover persistence in the base environment without real Ultralytics or weights.

Plan or run the optional real-YOLO local smoke:

```bash
python -m apps.worker.cli smoke-real-yolo-local --plan-only

python -m apps.worker.cli smoke-real-yolo-local \
  --source-path <sample_video_path> \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name local-yolo-smoke \
  --model-version local-v0 \
  --device cpu \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --run-tracklets
```

Validate the pose schema foundation without real pose runtime:

```bash
pytest tests/test_pose_schema.py tests/test_pose_observation_persistence.py tests/test_pose_normalization.py -q
```

These focused tests create fixture pose model/runtime records, write a synthetic `player_pose_observation` spine row plus typed `pose_observation` row, normalize fake pose frame results into `PoseObservationCreate`-compatible payloads, and verify COCO17 keypoint summaries and media-owned frame/time. They do not run pose inference.

## 27. Validate Pose Persistence and Lineage

Milestone 4C adds worker pose persistence for normalized fixture output. It still does not run real pose inference.

Run focused persistence checks:

```bash
pytest tests/test_pose_persistence_lineage.py -q
```

Run the fixture pose worker command after indexing media:

```bash
python -m apps.worker.cli run-pose-adapter \
  --media-id <media_id> \
  --adapter fixture \
  --frame-sample-rate 30 \
  --max-frames 3
```

To link pose evidence to persisted source player detections:

```bash
python -m apps.worker.cli run-pose-adapter \
  --media-id <media_id> \
  --adapter fixture \
  --source-detection-run-id <detection_run_id> \
  --link-source-detections \
  --max-frames 3
```

Expected behavior:

- A pose `processing_run` and `processing_step` are created.
- `player_pose_observation` spine rows and typed `pose_observation` rows are persisted.
- Full-frame fixture poses remain unassociated.
- Source-detection-linked poses use `pose_from_subject_detection_candidate` lineage.
- Source-detection-linked poses copy source detection frame/time values.

This does not create movement conclusions, homography, bounce/hit/rally/point/scoring evidence, or adjudication.

## 28. Inspect Pose Overlay Evidence

Milestone 4D adds pose overlay rendering in the existing Evidence Viewer.

Open a pose run:

```text
http://127.0.0.1:3000/runs/<POSE_RUN_ID>
```

Expected behavior:

- pose observations appear in the observation list and timeline
- the Pose Overlay panel renders present COCO17 keypoints
- skeleton edges render only when both endpoint keypoints are present
- missing keypoints stay visible as missing evidence in the keypoint table
- selected pose metadata shows skeleton format, confidence summaries, bbox, and frame time owner
- source association candidate context appears when a pose was linked to source player detection evidence

The overlay visualizes persisted pose evidence. It does not infer subject identity, movement, serve mechanics, hit events, rally state, point state, scoring, or adjudicated outcomes.

## 29. Query, Review, and Export Pose Evidence

Milestone 4E adds pose-specific query filters, evidence bundles, generic review annotations, and TOM-native review dataset export.

Query persisted pose observations:

```bash
curl -X POST http://127.0.0.1:8000/pose/query \
  -H "Content-Type: application/json" \
  -d '{"run_id":"<pose_run_id>","keypoints_missing_count_min":1}'
```

Open a pose evidence bundle:

```text
GET /pose-observations/<pose_observation_id>/evidence-bundle
```

Add a pose review annotation through the generic annotation API:

```json
{
  "observation_id": "<pose_observation_id>",
  "annotation_type": "bad_keypoint",
  "payload_jsonb": {
    "annotation_label": "bad_keypoint",
    "keypoint_name": "right_wrist",
    "keypoint_index": 10
  },
  "created_by": "local-reviewer"
}
```

Export pose review evidence:

```bash
python -m apps.worker.cli export-pose-review-dataset \
  --run-id <pose_run_id> \
  --output-root .data/exports
```

Expected behavior:

- pose query returns persisted `player_pose_observation` rows
- evidence bundle includes pose detail, lineage, source candidate context, artifacts, and annotations
- annotations are stored separately from pose observations
- export writes `.data/exports/pose/<export_id>/pose_review_dataset.json`
- export creates a `pose_review_dataset_export` evidence artifact with checksum metadata
- no real pose inference or movement interpretation is added

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
make run-pose MEDIA_ID=<media_id>
make seed
make smoke
make yolo-runtime-probe
make register-yolo-model WEIGHTS_PATH=model_assets/yolo/<model>.pt MODEL_NAME=<model-name>
make smoke-real-yolo-local SOURCE_PATH=/path/to/video.mp4 WEIGHTS_PATH=model_assets/yolo/<model>.pt MODEL_NAME=local-yolo-smoke RUN_TRACKLETS=true
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
- [YOLO Runtime Environment v0](docs/model_adapters/yolo_runtime_environment_v0.md)
- [YOLO Model Registry and Weights v0](docs/model_adapters/yolo_model_registry_weights_v0.md)
- [YOLO Detection Normalization v0](docs/model_adapters/yolo_detection_normalization_v0.md)
- [YOLO Frame Inference Persistence v0](docs/model_adapters/yolo_frame_inference_persistence_v0.md)
- [YOLO Real Runtime Smoke v0](docs/model_adapters/yolo_real_runtime_smoke_v0.md)
- [Blueprint 3 Completion Review](docs/blueprints/tom_v3_blueprint_3_completion_review.md)
- [Blueprint 4 - Pose Observation / Movement Evidence Layer](docs/blueprints/tom_v3_blueprint_4_pose_observation_movement_evidence_layer.md)
- [Skeleton Registry v0](docs/pose/skeleton_registry_v0.md)
- [Pose Observation Schema v0](docs/pose/pose_observation_schema_v0.md)
- [Pose Runtime Config v0](docs/pose/pose_runtime_config_v0.md)
- [Pose Adapter Normalization v0](docs/pose/pose_adapter_normalization_v0.md)
- [Pose Persistence and Lineage v0](docs/pose/pose_persistence_lineage_v0.md)
- [Pose Overlay Viewer v0](docs/web/pose_overlay_viewer_v0.md)
- [Pose Query / Review / Export v0](docs/pose/pose_query_review_export_v0.md)
- [Detection Overlay Viewer v0](docs/web/detection_overlay_viewer_v0.md)
- [Frame Artifact Overlay v0](docs/web/frame_artifact_overlay_v0.md)
- [Tracklet Foundation v0](docs/tracklets/tracklet_foundation_v0.md)
- [Tracklet Evidence Bundle v0](docs/tracklets/tracklet_evidence_bundle_v0.md)
- [Tracklet Evidence Viewer v0](docs/web/tracklet_evidence_viewer_v0.md)
- [Tracklet Query v0](docs/tracklets/tracklet_query_v0.md)
- [Tracklet Review Annotations v0](docs/tracklets/tracklet_review_annotations_v0.md)
- [Tracklet Review Viewer v0](docs/web/tracklet_review_viewer_v0.md)
- [Repo Branch Hygiene](docs/dev/repo_branch_hygiene.md)
