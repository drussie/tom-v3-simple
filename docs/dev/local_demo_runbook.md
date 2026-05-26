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

## 12. Run Detection Adapter On Indexed Media

Milestone 1C adds a worker-driven ball/player detection adapter path.

Run the deterministic fixture detector:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --frame-sample-rate 30 \
  --max-frames 5
```

Or index and run detection in one command:

```bash
python -m apps.worker.cli index-and-run-detection \
  --source-path /path/to/video.mp4 \
  --adapter fixture
```

Use gameplay scope if you have a gameplay adapter run:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --gameplay-run-id <GAMEPLAY_RUN_ID>
```

Query ball detections:

```bash
curl -X POST http://127.0.0.1:8000/observations/query \
  -H 'Content-Type: application/json' \
  -d '{"run_id":"<DETECTION_RUN_ID>","observation_type":"ball_detection"}'
```

Query player detections:

```bash
curl -X POST http://127.0.0.1:8000/observations/query \
  -H 'Content-Type: application/json' \
  -d '{"run_id":"<DETECTION_RUN_ID>","observation_type":"player_detection"}'
```

The viewer can open the detection `run_id` and show ball/player detections in the observation list and detail panel.

Milestone 1D adds a detection overlay for the same detection `run_id`. The viewer now shows:

- a coordinate-space media/frame panel
- persisted ball/player bboxes scaled by media dimensions
- labels and confidence values
- selected detection highlighting
- safe empty states when media dimensions or bbox payloads are unavailable

Open:

```text
http://127.0.0.1:3000/runs/<DETECTION_RUN_ID>
```

Click a `ball_detection` or `player_detection` row in the observation list, or click a bbox in the overlay, to update the selected observation detail, lineage, artifact, and annotation panels.

The YOLO adapter is wired behind an optional frame-level runtime path as of Milestone 3D. Use the fixture adapter for base-environment demos; use `--adapter yolo` only after probing the optional runtime and registering local weights.

## 13. Extract Frame Artifacts For Detection Overlay

Milestone 1E adds frame artifact extraction so detection bboxes can be inspected over extracted frame imagery.

Run:

```bash
python -m apps.worker.cli extract-frame-artifacts \
  --run-id <DETECTION_RUN_ID> \
  --max-frames 2 \
  --output-root .data/artifacts
```

The command writes images under:

```text
.data/artifacts/media/{media_id}/frames/
```

It also persists `frame_image` and `detection_frame_image` evidence artifact rows.

Open:

```text
http://127.0.0.1:3000/runs/<DETECTION_RUN_ID>
```

Expected behavior:

- if extraction succeeded, the selected detection frame image appears behind the bbox overlay
- persisted bboxes still render from observation payloads
- the artifact panel shows frame artifact metadata for selected detection observations
- if extraction was not run, the coordinate canvas fallback still renders

`ffmpeg` is required for frame extraction. If it is unavailable, the command reports that `ffmpeg` must be installed.

## 14. Build Candidate Tracklets From Detection Observations

Milestone 2A adds candidate temporal grouping from persisted detection observations with first-class tracklet and track point observation rows.

Run:

```bash
python -m apps.worker.cli build-tracklets \
  --detection-run-id <DETECTION_RUN_ID> \
  --max-gap-frames 30
```

The command creates a new tracklet-builder run and prints a `tracklet_run_id`.

Open:

```text
http://127.0.0.1:3000/runs/<TRACKLET_RUN_ID>
```

Expected behavior:

- candidate ball/player tracklet coverage rows are visible
- track point candidate observations are present in the viewer payload
- each track point stores `source_detection_observation_id` in payload metadata
- lineage links source detections to track points and track points to tracklets
- `tracklet_id` queries return tracklet candidate and track point candidate observations

Example query:

```bash
curl -X POST http://127.0.0.1:8000/observations/query \
  -H 'Content-Type: application/json' \
  -d '{"tracklet_id":"<TRACKLET_ID>"}'
```

Tracklet builder output is candidate temporal grouping only. It does not establish identity, bounce, hit, rally, or point state.

## 15. Inspect A Tracklet Evidence Bundle

Milestone 2B adds a multi-run evidence bundle for a selected tracklet candidate.

After building tracklets, call:

```bash
curl http://127.0.0.1:8000/tracklets/<TRACKLET_ID>/evidence-bundle
```

The bundle includes:

- typed tracklet row and tracklet candidate observation
- track point rows and track point candidate observations
- source detection observations from the detection run
- frame artifacts when extraction has already run
- `tracked_from` and `grouped_from` lineage rows

Open the tracklet builder run:

```text
http://127.0.0.1:3000/runs/<TRACKLET_RUN_ID>
```

Expected behavior:

- selecting a tracklet loads the Tracklet Evidence panel
- track point candidates are listed
- selecting a track point shows its source detection evidence
- frame artifacts appear when available
- missing frame artifacts fall back to bbox/source metadata

The evidence bundle is read-only and descriptive. It does not establish a confirmed track, identity, bounce, hit, rally, or point state.

## 16. Query And Review Tracklet Candidates

Milestone 2C adds structured tracklet candidate query:

```bash
curl -X POST http://127.0.0.1:8000/tracklets/query \
  -H 'Content-Type: application/json' \
  -d '{
    "source_detection_run_id": "<DETECTION_RUN_ID>",
    "track_family": "ball",
    "min_track_points": 2,
    "has_gaps": true,
    "limit": 50
  }'
```

The response includes candidate summaries, annotation summaries, and evidence bundle URLs.

To add a review annotation through the API:

```bash
curl -X POST http://127.0.0.1:8000/annotations \
  -H 'Content-Type: application/json' \
  -d '{
    "observation_id": "<TRACKLET_OR_POINT_OR_SOURCE_OBSERVATION_ID>",
    "annotation_type": "bad_tracklet",
    "payload_jsonb": {
      "annotation_label": "bad_tracklet",
      "notes": "Review note from local demo.",
      "review_context": "tracklet_evidence_bundle",
      "review_status": "reviewed"
    },
    "created_by": "local-reviewer"
  }'
```

In the viewer, open the tracklet builder run:

```text
http://127.0.0.1:3000/runs/<TRACKLET_RUN_ID>
```

Expected behavior:

- selecting a tracklet loads the Tracklet Evidence panel
- annotation summaries are visible
- the Tracklet Review form can target the selected tracklet candidate, track point candidate, or source detection
- saving a review annotation refreshes the evidence bundle

Review annotations are additional evidence. They do not mutate candidate observations or source detections.

## 17. Export Tracklet Review Dataset

Milestone 2D adds a portable JSON export for candidate tracklet review evidence.

Export by query:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"has_annotation":true}' \
  --output-root .data/exports \
  --format json
```

Export one selected tracklet:

```bash
python -m apps.worker.cli export-tracklet-review-dataset \
  --tracklet-id <TRACKLET_ID> \
  --output-root .data/exports
```

The command prints:

- `export_id`
- `artifact_id`
- export file path and URI
- checksum
- selected tracklet ids
- optional `query_result_id`
- candidate-only warning fields

The JSON file is written under:

```text
.data/exports/tracklets/{export_id}/tracklet_review_dataset.json
```

Expected behavior:

- export JSON exists
- `tracklet_review_dataset_export` evidence artifact row exists
- query exports create a `query_result` row
- export includes tracklet evidence bundles, lineage, frame artifact metadata, and annotations when requested
- export warnings state that candidate evidence and annotations are not adjudicated labels

## 18. Blueprint 2 Full Local Smoke Path

Blueprint 2 is complete when this local fixture/dev path works without real YOLO:

```text
index media
-> run fixture detection adapter
-> extract frame artifacts
-> build candidate tracklets
-> query tracklets
-> inspect evidence bundle
-> add review annotation
-> export review dataset
-> inspect output artifact
```

Recommended command sequence:

```bash
python -m apps.worker.cli index-media --source-path /path/to/video.mp4
python -m apps.worker.cli run-detection-adapter --media-id <MEDIA_ID> --adapter fixture --frame-sample-rate 5 --max-frames 4 --output-debug-artifact
python -m apps.worker.cli extract-frame-artifacts --run-id <DETECTION_RUN_ID> --max-frames 2 --output-root .data/artifacts
python -m apps.worker.cli build-tracklets --detection-run-id <DETECTION_RUN_ID> --max-gap-frames 30
```

Then:

```bash
curl -X POST http://127.0.0.1:8000/tracklets/query \
  -H 'Content-Type: application/json' \
  -d '{"source_detection_run_id":"<DETECTION_RUN_ID>","limit":50}'

curl http://127.0.0.1:8000/tracklets/<TRACKLET_ID>/evidence-bundle

curl -X POST http://127.0.0.1:8000/annotations \
  -H 'Content-Type: application/json' \
  -d '{"observation_id":"<TRACKLET_OBSERVATION_ID>","annotation_type":"bad_tracklet","payload_jsonb":{"annotation_label":"bad_tracklet","review_context":"blueprint_2_smoke","review_status":"reviewed"},"created_by":"local-reviewer"}'

python -m apps.worker.cli export-tracklet-review-dataset \
  --query-json '{"has_annotation":true}' \
  --output-root .data/exports \
  --format json
```

Expected behavior:

- tracklet query returns candidate tracklets
- evidence bundle reconstructs source detection to track point to tracklet lineage
- annotation persists as review evidence
- export JSON exists
- export artifact metadata exists
- export warnings preserve candidate-only and no-adjudication semantics

This flow is fixture/dev evidence unless a future real model adapter is supplied. It does not require real YOLO and does not add pose, homography, bounce, hit, rally, point, scoring, or adjudication.

## 19. Optional YOLO Runtime Probe

Milestone 3A starts Blueprint 3 by adding a runtime probe for a separate optional YOLO environment. The base `tom_v3` environment should continue to run without Ultralytics, Torch, or OpenCV installed.

Probe the current environment:

```bash
python -m apps.worker.cli yolo-runtime-probe
```

Expected base behavior:

- the command returns JSON
- missing optional packages are reported in `missing_packages`
- `status` is `unavailable` when YOLO runtime packages are absent
- the command does not import heavy YOLO dependencies at normal app startup

Create the optional YOLO environment only when working on real runtime milestones:

```bash
conda create -n tom_v3_yolo python=3.11 -y
conda activate tom_v3_yolo
python -m pip install --upgrade pip
pip install -e ".[dev]"
pip install -r requirements-yolo.txt
python -m apps.worker.cli yolo-runtime-probe
```

Torch installation can be platform-specific. If CUDA or MPS support is needed, follow the Torch installation guidance for the target machine before running the probe.

Device examples:

```bash
python -m apps.worker.cli yolo-runtime-probe --device cpu
python -m apps.worker.cli yolo-runtime-probe --device mps
python -m apps.worker.cli yolo-runtime-probe --device cuda:0
python -m apps.worker.cli yolo-runtime-probe --device auto --no-mps
```

Milestone 3A does not persist real YOLO detections. It only validates runtime availability, device resolution, and optional dependency boundaries.

## 20. Register Local YOLO Weights

Milestone 3B adds local weights validation and model registry metadata. This still does not run inference or persist detections.

Allowed local development roots:

```text
model_assets/yolo/
weights/yolo/
```

Example local smoke file:

```bash
mkdir -p model_assets/yolo
python - <<'PY'
from pathlib import Path
p = Path("model_assets/yolo/test_fake_model.pt")
p.write_bytes(b"fake-yolo-weights-for-registry-smoke")
print(p)
PY
```

Register the weights metadata:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/test_fake_model.pt \
  --model-name fake-yolo-registry-smoke \
  --model-version test-v0 \
  --device cpu
```

Expected behavior:

- command prints `model_registry_id`
- output includes `weights_sha256` and `weights_size_bytes`
- output includes the default ball/player `class_map`
- no processing run is created
- no observations are created

Optional checksum enforcement:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/test_fake_model.pt \
  --model-name fake-yolo-registry-smoke \
  --model-version test-v0 \
  --required-sha256 <EXPECTED_SHA256>
```

Checksum mismatch produces a structured error and does not create a registry row.

## 21. Normalize Fake YOLO Output

Milestone 3C adds normalization for YOLO-like output dictionaries. This is a pure adapter-layer check; it does not load a model, run inference, create processing runs, or persist observations.

Run a local normalization smoke:

```bash
python - <<'PY'
from tom_v3_model_adapters.yolo_normalization import normalize_yolo_frame_result
from tom_v3_model_adapters.yolo_weights import default_yolo_class_mapping

result = normalize_yolo_frame_result(
    {
        "frame_number": 120,
        "timestamp_ms": 4000,
        "image_width": 1920,
        "image_height": 1080,
        "boxes": [
            {
                "xyxy": [100, 200, 140, 240],
                "confidence": 0.91,
                "class_id": 32,
                "class_name": "sports ball",
                "source_result_index": 0,
            },
            {
                "xyxy": [500, 150, 700, 900],
                "confidence": 0.87,
                "class_id": 0,
                "class_name": "person",
                "source_result_index": 1,
            },
        ],
    },
    class_mapping=default_yolo_class_mapping(),
)
print(result.as_dict())
PY
```

Expected behavior:

- one `ball_detection` normalized payload
- one `player_detection` normalized payload
- bbox converted from `xyxy` to `x/y/width/height`
- center calculated
- `frame_time_owner = media_indexing`
- `source_runtime = ultralytics_yolo`
- no model inference
- no observations persisted

## 22. Run YOLO Frame Inference Persistence

Milestone 3D connects the YOLO adapter to the existing detection persistence path.

The base environment test path uses mocked providers. Real local runtime use requires:

- optional `tom_v3_yolo` environment
- Ultralytics/Torch/OpenCV availability from `yolo-runtime-probe`
- a registered local model weights row
- an indexed media asset

Register weights as shown in section 20, then run:

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

Expected behavior when optional runtime and weights are available:

- a detection processing run is created
- YOLO-origin `ball_detection` and/or `player_detection` observations are persisted
- payloads include bbox, center, label, confidence, source runtime, model registry id, weights sha256, and media-owned frame/time metadata
- the existing detection viewer can inspect the run

Expected behavior when runtime or weights are unavailable:

- the command fails clearly
- the run/step is marked failed when created
- no fixture detections are persisted as a fallback

This path does not create tracklets. Build candidate tracklets explicitly with `build-tracklets` after reviewing a detection run.
