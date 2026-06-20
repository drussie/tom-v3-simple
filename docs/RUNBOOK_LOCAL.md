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

Blueprint 6 is complete and adds a media-centric replay/operator workstation route:

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

Replay overlays are observation evidence. They do not establish object state, player identity, movement analysis, or tennis events.

Open Stream Proxy Mode:

```text
http://127.0.0.1:3000/replay/<media_id>?mode=stream_proxy&detectionRunId=<run_id>&trackletRunId=<run_id>&poseRunId=<run_id>
```

Or print a helper URL:

```bash
make replay-open MEDIA_ID=<media_id> MODE=stream_proxy DETECTION_RUN_ID=<detection_run_id> TRACKLET_RUN_ID=<tracklet_run_id> POSE_RUN_ID=<pose_run_id>
```

Expected 6E Stream Proxy behavior:

- playback starts from the beginning as a video-as-live proxy
- future detection, tracklet, pose, and annotation evidence is hidden until playback reaches it
- the page shows live edge, operator time, lag, and available evidence counts
- pausing means the operator is reviewing paused proxy time
- Return to live edge jumps back to the latest available proxy time

Stream Proxy Mode still uses indexed local media and persisted observations. It is not real live stream ingestion.

Blueprint 6 is complete at this boundary. Future real live ingestion, new replay capabilities, or tennis-intelligence layers should begin as separate blueprints.

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

Candidate tracklets are temporal grouping evidence, not tennis events.

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

## 11. Optional YOLO / Pose Runtime

The fixture demo does not require YOLO or pose weights.

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

Run a real YOLO detection replay pass after a media asset exists:

```bash
make real-detection \
  MEDIA_ID=<media_id> \
  YOLO_WEIGHTS_PATH=./model_assets/yolo/<model>.pt \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=120
```

Equivalent worker command:

```bash
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

The command prints a replay URL:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>
```

Milestone 7B replay validation:

- the detection run selector should label the run as real model output
- fixture detection runs should remain labeled as fixture/demo evidence
- clicking a real detection bbox should show source runtime, model registry id, runtime config id, class id/label, frame/time owner, and evidence-only copy when available
- the detection timeline label should include the real model-output source label

Build candidate tracklets from a real detection run:

```bash
.venv/bin/python -m apps.worker.cli build-tracklets \
  --detection-run-id <real_detection_run_id> \
  --run-name real-detection-tracklet-candidates
```

The command prints a replay URL with both run ids:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<tracklet_run_id>
```

Milestone 7C replay validation:

- the tracklet run selector should label the run as real-detection-derived tracklet candidates
- selected tracklet details should show source detection run, source evidence type, source runtime, candidate status, and unverified identity status when available
- selected track point details should show the source detection observation id and source detection evidence metadata when available
- tracklet points and paths remain candidate temporal groupings and do not establish object paths

Run a real pose replay pass after a media asset exists. Crop-from-player-detection mode is preferred when a real detection run is available:

```bash
make real-pose \
  MEDIA_ID=<media_id> \
  SOURCE_DETECTION_RUN_ID=<real_detection_run_id> \
  POSE_WEIGHTS_PATH=./model_assets/pose/<pose_model>.pt \
  PYTHON=.venv/bin/python \
  MAX_FRAMES=120
```

Equivalent worker command:

```bash
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <real_detection_run_id> \
  --weights ./model_assets/pose/<pose_model>.pt \
  --mode crop_from_player_detection \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

The command prints a replay URL with `poseRunId`:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&poseRunId=<real_pose_run_id>
```

If a real-detection-derived tracklet run also exists, open:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<real_pose_run_id>
```

Milestone 7D replay validation:

- the pose run selector should label the run as real pose model output
- pose keypoints and skeletons should render through `poseRunId`
- selected pose details should show source runtime, model registry id, runtime config id, skeleton format, keypoint counts, and subject association candidate context when available
- crop-mode pose lineage should point back to source `player_detection` observations
- pose observations remain keypoint evidence and do not interpret movement, strokes, biomechanics, court position, or tennis events

If local weights are not available, skip the real smoke and rely on the fake real-detection tests. The default fixture demo and CI path must not require YOLO weights.

If local pose weights are not available, skip the real pose smoke and rely on the fake real-pose tests. The default fixture demo and CI path must not require pose weights.

Real YOLO detections are model-output observations. Real-detection-derived tracklets are candidate groupings from those observations. Real pose observations are keypoint evidence. These layers do not create movement interpretation, homography, events, scoring, or adjudication.

## 11A. TOM v1 Model Assets Bridge

The TOM v3 replay/evidence infrastructure is working, but fixture visual quality is not real tracking quality. Fixture ball/player overlays and fixture court lines prove the pipeline; they do not prove real perception quality.

TOM v1 model assets may be tested locally as TOM v3 observation sources. Model weights are local-only and ignored by git.

Expected local inventory:

```text
model_assets/tom_v1/best_ball_v2_1280.pt          # ball detector
model_assets/tom_v1/keypoints_model.pth           # court keypoints model, future adapter required
model_assets/tom_v1/view_classifier_gameplay.pt   # gameplay classifier, future adapter required
model_assets/tom_v1/yolo26n.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26s.pt                    # YOLO26 small variant
model_assets/tom_v1/yolo26x-pose.pt               # pose model
model_assets/tom_v1/yolo26x.pt                    # player/object detector
```

Immediate supported paths:

- likely usable now through existing TOM v3 real YOLO detection: `best_ball_v2_1280.pt`, `yolo26x.pt`, `yolo26n.pt`, `yolo26s.pt`
- likely usable now through existing TOM v3 real pose: `yolo26x-pose.pt`
- usable through the TOM v1 court keypoint adapter: `keypoints_model.pth`
- future TOM v1-specific adapter required: `view_classifier_gameplay.pt`

Probe optional runtime:

```bash
.venv/bin/python -m apps.worker.cli yolo-runtime-probe --device auto
```

If unavailable, install optional vision dependencies in a local optional environment. The default fixture demo and default CI still do not require Ultralytics, Torch, OpenCV, or model files.

Fixture-safe setup:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=30
```

Copy the `media_id` from the demo summary.

TOM v1 ball detection:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights model_assets/tom_v1/best_ball_v2_1280.pt \
  --model-name tom-v1-best-ball-v2-1280 \
  --model-version v1-local \
  --device auto \
  --imgsz 1280 \
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.10 \
  --allowed-root model_assets/tom_v1
```

TOM v1 player/object detection:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights model_assets/tom_v1/yolo26x.pt \
  --model-name tom-v1-yolo26x-player-detector \
  --model-version v1-local \
  --device auto \
  --imgsz 640 \
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25 \
  --allowed-root model_assets/tom_v1
```

Candidate tracklets from a real detection run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli build-tracklets \
  --detection-run-id <real_detection_run_id> \
  --run-name tom-v1-model-derived-tracklets
```

TOM v1 pose from the player detection run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --weights model_assets/tom_v1/yolo26x-pose.pt \
  --model-name tom-v1-yolo26x-pose \
  --model-version v1-local \
  --mode crop_from_player_detection \
  --device auto \
  --imgsz 640 \
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25 \
  --allowed-root model_assets/tom_v1
```

TOM v1 court keypoint probe:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli tom-v1-court-keypoints-probe \
  --weights model_assets/tom_v1/keypoints_model.pth \
  --allowed-root model_assets/tom_v1
```

Expected local format:

```text
load_strategy = torch_load_state_dict
recognized_architecture = torchvision_resnet50_fc28_xy224
raw_output_pair_count = 14
expected_adapter_status = ready
```

TOM v1 real court keypoints:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-court-keypoints \
  --media-id <media_id> \
  --weights model_assets/tom_v1/keypoints_model.pth \
  --model-name tom-v1-court-keypoints \
  --model-version v1-local \
  --device auto \
  --img-size 640 \
  --every-n-frames 30 \
  --max-frames 214 \
  --allowed-root model_assets/tom_v1 \
  --preprocessing-mode full_frame_resize_224 \
  --coordinate-interpretation output_as_pixels_224 \
  --viewer-base-url http://127.0.0.1:3000
```

This persists real model-output `court_keypoint_observation` rows and, when enough keypoints are present, derived `court_line_observation` candidates. The keypoints and lines are geometry evidence only, not court truth.

TOM v1 court keypoint calibration audit:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-court-keypoints \
  --media-id <media_id> \
  --weights model_assets/tom_v1/keypoints_model.pth \
  --model-name tom-v1-court-keypoints \
  --model-version v1-local \
  --device auto \
  --img-size 224 \
  --every-n-frames 30 \
  --max-frames 214 \
  --allowed-root model_assets/tom_v1 \
  --preprocessing-mode full_frame_resize_224 \
  --coordinate-interpretation output_as_pixels_224 \
  --emit-debug-artifacts \
  --viewer-base-url http://127.0.0.1:3000
```

Equivalent helper:

```bash
make tom-v1-court-keypoint-audit \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  MAX_FRAMES=214 \
  EVERY_N_FRAMES=30
```

The audit run records raw TOM v1 points, scaled image-space raw points, mapped TOM v3 points, inferred keypoints, preprocessing mode, and coordinate interpretation in the observation payload and optional debug artifacts. In replay, inspect raw `raw_0..raw_13` keypoints before mapped keypoints, derived lines, homography, or diagnostics. Current court/homography output is not trusted until this visual calibration is reviewed.

Homography and projection diagnostics from real court keypoints:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id <media_id> \
  --court-run-id <real_court_run_id>

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli build-projection-diagnostics \
  --media-id <media_id> \
  --homography-run-id <homography_run_id>
```

Replay with the real court run:

```text
/replay/<media_id>?courtRunId=<real_court_run_id>&homographyRunId=<homography_run_id>&projectionDiagnosticRunId=<projection_diagnostic_run_id>
```

Replay labels distinguish raw TOM v1 keypoint evidence, mapped TOM v3 keypoint evidence, `real court keypoint model output`, `derived court line candidate`, `homography candidate`, and `projection diagnostic`. These labels describe provenance and calibration context, not correctness.

Main tennis-player subject filter:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli select-main-player-subjects \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --run-name main-player-subject-filter-v0 \
  --frame-start 0 \
  --frame-end 214 \
  --max-frames 214
```

This persists at most two `main_player_subject_candidate` rows per frame: `near_player_candidate` and `far_player_candidate`. These rows are pose source candidates only. They do not identify players, mutate raw detections, or decide tennis events.

Main player track assignment:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli assign-main-player-tracks \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --run-name main-player-track-assignment-v01 \
  --frame-start 0 \
  --frame-end 214 \
  --max-frames 214 \
  --every-n-frames 1
```

This persists `main_player_track_candidate` rows for `near_player_track_candidate` and `far_player_track_candidate`, plus per-frame `main_player_track_assignment_candidate` rows. v0.1 locks each candidate visual track from plausible seeds, rejects large jumps or edge/wall candidates, and allows gaps instead of forcing a bad assignment. These are visual subject track candidates only. They do not confirm player identity, names, server/receiver role, side changes, or tennis truth.

TOM v1 pose from selected main subject candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --weights model_assets/tom_v1/yolo26x-pose.pt \
  --model-name tom-v1-yolo26x-pose \
  --model-version v1-local \
  --mode crop_from_player_detection \
  --device auto \
  --imgsz 640 \
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25 \
  --allowed-root model_assets/tom_v1
```

TOM v1 pose from main player track candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --source-track-run-id <main_player_track_run_id> \
  --weights model_assets/tom_v1/yolo26x-pose.pt \
  --model-name tom-v1-yolo26x-pose \
  --model-version v1-local \
  --mode crop_from_player_detection \
  --device auto \
  --imgsz 640 \
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25 \
  --allowed-root model_assets/tom_v1
```

Motion smoothing / stable replay candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli smooth-motion-candidates \
  --media-id <media_id> \
  --detection-run-id <player_or_ball_detection_run_id> \
  --tracklet-run-id <tracklet_run_id> \
  --main-player-track-run-id <main_player_track_run_id> \
  --pose-run-id <track_filtered_pose_run_id> \
  --run-name motion-smoothing-stable-replay-candidates-v0
```

This creates derived `smoothed_ball_position_candidate`,
`smoothed_main_player_box_candidate`, and `smoothed_pose_candidate` rows when the matching source
runs are supplied. These rows are replay smoothing candidates only. They do not mutate raw
detections, tracklets, main player track assignments, or pose observations, and they do not decide
bounce, hit, in/out, point, score, player identity, or court-space position.

Object-to-court projection candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli project-objects-to-court \
  --media-id <media_id> \
  --motion-smoothing-run-id <motion_smoothing_run_id> \
  --homography-run-id <homography_run_id> \
  --homography-max-gap-ms 1500 \
  --viewer-base-url http://127.0.0.1:3000
```

This creates derived `ball_court_projection_candidate` and
`main_player_court_projection_candidate` rows by projecting smoothed image-space candidates through
candidate homography rows into normalized `court_template_2d` coordinates. These projections are
candidate evidence only. They do not confirm ball location, player location, court truth, bounce,
hit, in/out, point, score, identity, or adjudication.

Ball trajectory court candidate:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli build-ball-court-trajectory \
  --media-id <media_id> \
  --court-projection-run-id <court_projection_run_id> \
  --max-gap-frames 6 \
  --max-gap-ms 250 \
  --min-points-per-segment 3 \
  --viewer-base-url http://127.0.0.1:3000
```

This creates derived `ball_trajectory_court_candidate` segment rows from ordered
`ball_court_projection_candidate` points. The trajectory includes velocity, direction, gap,
out-of-template, and homography carry-forward diagnostics. It is not bounce truth, hit truth,
in/out truth, rally/point/score logic, or adjudication.

Hit/bounce candidate evidence:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli build-hit-bounce-candidates \
  --media-id <media_id> \
  --ball-trajectory-run-id <ball_trajectory_run_id> \
  --court-projection-run-id <court_projection_run_id> \
  --hit-player-distance-max-template 0.18 \
  --bounce-player-distance-min-template 0.18 \
  --hit-min-direction-delta-degrees 25 \
  --bounce-min-direction-delta-degrees 20 \
  --hit-min-net-axis-delta-template 0.015 \
  --bounce-min-image-y-delta-pixels 2.0 \
  --bounce-min-speed-reduction-fraction 0.05 \
  --hit-player-time-window-ms 300 \
  --hit-contact-fallback-min-speed-delta-fraction 0.45 \
  --hit-contact-fallback-min-direction-delta-degrees 5.0 \
  --bounce-fallback-enabled \
  --bounce-fallback-min-speed-reduction-fraction 0.35 \
  --event-overlap-distance-template 0.08 \
  --net-axis-reversal-hit-enabled \
  --net-axis-reversal-lookback-ms 700 \
  --net-axis-reversal-lookahead-ms 700 \
  --net-axis-reversal-min-delta-template 0.015 \
  --net-axis-reversal-min-pre-post-gap-ms 60 \
  --net-axis-reversal-dedupe-distance-template 0.08 \
  --candidate-dedupe-ms 500 \
  --viewer-base-url http://127.0.0.1:3000
```

This creates derived `hit_candidate` and `bounce_candidate` rows from court-space trajectory
diagnostics and main-player projection proximity. The v0.2 repair prefers player-proximate
`court_y` net-axis reversal for hit candidates and image-y descending-to-ascending proxy plus speed
reduction for bounce candidates. The v0.2.1 repair also writes
`event_candidate_rejection_diagnostic` rows and a rejection-reason summary so missing candidate
contexts can be inspected. These are candidate markers and diagnostics only. They are not hit truth,
bounce truth, in/out truth, rally/point/score logic, or adjudication.

By default, this command prints compact operator JSON: run ids, replay URL, observation counts,
active versions, candidate-only warnings, and a deterministic `marker_summary` with one row per
final visible hit/bounce marker. It omits the full `observation_ids` list and nested
`candidate_summary` diagnostics unless requested.

Replay Marker Inspector v0 exposes the same compact marker information in the replay UI. Open a
replay with `eventCandidateRunId=<event_candidate_run_id>`, then click a `HIT CANDIDATE` or
`BOUNCE CANDIDATE` marker in the video overlay, mini-map, or event timeline. The side panel shows a
compact selected-marker card with source method, frame/time, confidence, marker-level arbitration
decision/reason, image/court coordinates, and candidate-only warnings.

Deep diagnostic output remains available:

```bash
make tom-v1-hit-bounce-candidates HIT_BOUNCE_VERBOSE=true
make tom-v1-hit-bounce-candidates INCLUDE_OBSERVATION_IDS=true
make tom-v1-hit-bounce-candidates DIAGNOSTIC_SUMMARY=full
make tom-v1-hit-bounce-candidates-verbose
```

These flags change CLI presentation only. They do not change persisted observations or candidate
decisions.

Generate a compact point evidence snapshot after a candidate run:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-point-evidence-snapshot \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>
```

The snapshot returns replay URL, source run ids, observation counts, active candidate versions,
final visible marker summary, candidate-only warnings, and known limitations. It is a report for
operator review and reproducibility only; it does not create hit truth, bounce truth, in/out, score,
or adjudication.

Generate a Blueprint 10 point candidate review evaluation after adding Blueprint 9 review
annotations:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-evaluate-point-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id>
```

Optional markdown output:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-evaluate-point-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  FORMAT=markdown \
  OUTPUT=tmp_reports/point_candidate_review_evaluation.md
```

The evaluation summarizes generated candidate markers and operator review metadata. It does not
compute precision/recall in v0, does not promote review labels into truth, and does not change
generated candidates, in/out, score, point state, or adjudication.

Declare Blueprint 11 camera/court geometry readiness for a point:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-declare-camera-geometry \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  COURT_RUN_ID=<court_run_id> \
  COURT_PROJECTION_RUN_ID=<court_projection_run_id> \
  HOMOGRAPHY_RUN_ID=<homography_run_id>
```

The output records `camera_geometry_evidence` with declared court dimensions, camera model,
geometry status, coordinate-system metadata, capabilities, and no-truth warnings. It does not
create 3D ball trajectories, change event candidates, decide in/out, score a point, or adjudicate
evidence. Subsequent point evidence snapshots include `camera_geometry_summary`, and point
candidate evaluations include `geometry_readiness`.

Build Blueprint 12 provisional 3D ball trajectory candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-build-3d-ball-trajectory-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  BALL_TRAJECTORY_RUN_ID=<ball_trajectory_run_id> \
  COURT_PROJECTION_RUN_ID=<court_projection_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

The default `HEIGHT_MODEL=none_unknown` derives metric court-plane x/y candidates from declared
court dimensions and leaves height unknown. It does not create true 3D reconstruction, verified
ball height, hit/bounce truth, in/out, score, or adjudication. Subsequent point evidence snapshots
include `trajectory_3d_summary`, and point candidate evaluations include
`trajectory_3d_readiness`.

Blueprint 8 freeze operator workflow:

1. Build or obtain the source perception, court, smoothing, projection, and trajectory runs.
2. Run `make tom-v1-hit-bounce-candidates`.
3. Open the replay URL in operator view.
4. Review final visible markers in the Event Candidate Review panel.
5. Click rows or markers to seek/select evidence.
6. Inspect source method, confidence, coordinates, and marker-level arbitration in Replay Marker
   Inspector.
7. Generate a point evidence snapshot for the reviewed run.
8. Generate a point candidate review evaluation when review annotations should be summarized.
9. Declare camera geometry evidence when future 3D readiness assumptions should be recorded.

The v0.2.2 side-zone sequence repair preserves the 2-hit / 2-bounce sample-point recall while adding
`court_side_zone`, `player_contact_zone`, `court_landing_zone`, `candidate_reclassification`, and
`candidate_sequence` diagnostics. CLI summaries now include raw candidate counts, final candidate
counts, reclassification counts, `sequence_prior_applied_count`, and
`physics_heuristic_version = v0.2.2`. The sequence pass is a candidate label repair only; it does
not create hit truth, bounce truth, in/out, score, or adjudication.

The v0.2.4 player-anchored contact-zone tightening repair adds `player_anchor_contact_zone` and
`overlap_suppression` diagnostics. Player-anchored hits that overlap final bounce/open-court
landing clusters are suppressed as diagnostics rather than emitted as final hit candidates.

The v0.2.5 net-axis reversal hit recall repair adds ball-first
`net_axis_reversal_hit_candidate_v025` candidates from court-template `court_y` direction reversal
without requiring player proximity. Player proximity is diagnostic/confidence support only for this
path. The repair keeps bounce-overlap protections and remains candidate evidence only, not hit
truth, bounce truth, in/out, score, or adjudication.

The v0.2.6 image-space net-axis hit recall repair adds
`image_space_net_axis_reversal_hit_candidate_v026` candidates from broadcast image-y direction
reversal. The axis method is explicitly labeled `broadcast_image_y_axis_fallback_v026` because this
is a hardcam image-space fallback for airborne hit-like candidates, not universal camera geometry.
Player proximity is not required for this path; it is diagnostic/confidence support only. The
repair can use `ball_court_projection_candidate.image_point` rows directly, so a short or gappy
projection span can recover a hit candidate even when it was not persisted as a trajectory segment.
It remains candidate evidence only, not hit truth, bounce truth, in/out, score, or adjudication.

The v0.2.7 image-space direction-change hit recall repair adds
`image_space_direction_change_hit_candidate_v027` candidates from full 2D broadcast image vector
angle changes. The direction method is
`broadcast_image_2d_vector_direction_change_v027`. Player proximity is not required; it is
diagnostic/confidence support only. Weak direction-change candidates immediately before bounce
candidates are suppressed as diagnostics to avoid restoring false open-court hit-over-bounce
markers. This remains candidate evidence only, not hit truth, bounce truth, in/out, score, or
adjudication.

Replay can show those candidates in two places:

- the normalized court mini-map, using candidate court-template coordinates
- the broadcast video overlay, using the source `ball_court_projection_candidate.image_point`

If an event candidate cannot resolve an image point, the replay API keeps the candidate available
for timeline/mini-map inspection and reports `image_marker_source = unavailable`.

Makefile helpers:

```bash
make tom-v1-yolo-probe PYTHON=.venv/bin/python
make tom-v1-ball-detection MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-player-detection MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-tracklets DETECTION_RUN_ID=<real_detection_run_id> PYTHON=.venv/bin/python
make tom-v1-main-subjects MEDIA_ID=<media_id> DETECTION_RUN_ID=<player_real_detection_run_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-main-player-tracks MEDIA_ID=<media_id> DETECTION_RUN_ID=<player_real_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-court-keypoints-probe PYTHON=.venv/bin/python
make tom-v1-court-keypoints MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=214 EVERY_N_FRAMES=30
make tom-v1-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-pose-main-subjects MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-pose-main-tracks MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> SOURCE_SUBJECT_RUN_ID=<main_subject_run_id> SOURCE_TRACK_RUN_ID=<main_player_track_run_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-motion-smoothing MEDIA_ID=<media_id> DETECTION_RUN_ID=<detection_run_id> TRACKLET_RUN_ID=<tracklet_run_id> MAIN_PLAYER_TRACK_RUN_ID=<main_player_track_run_id> POSE_RUN_ID=<pose_run_id> PYTHON=.venv/bin/python
make tom-v1-object-court-projection MEDIA_ID=<media_id> MOTION_SMOOTHING_RUN_ID=<motion_smoothing_run_id> HOMOGRAPHY_RUN_ID=<homography_run_id> PYTHON=.venv/bin/python
make tom-v1-ball-court-trajectory MEDIA_ID=<media_id> COURT_PROJECTION_RUN_ID=<court_projection_run_id> PYTHON=.venv/bin/python
make tom-v1-hit-bounce-candidates MEDIA_ID=<media_id> BALL_TRAJECTORY_RUN_ID=<ball_trajectory_run_id> COURT_PROJECTION_RUN_ID=<court_projection_run_id> PYTHON=.venv/bin/python
make tom-v1-point-evidence-snapshot MEDIA_ID=<media_id> EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> PYTHON=.venv/bin/python
```

The TOM v1 Makefile helpers pass `--allowed-root "$(TOM_V1_MODEL_ROOT)"` and default image sizes that match the local smoke path: 1280 for `best_ball_v2_1280.pt`, 640 for `yolo26x.pt`, 640 for `yolo26x-pose.pt`, and 224 fixed preprocessing for the recognized court keypoint state dict. Override with `IMG_SIZE=<value>` only when testing a deliberate alternate model input size. The court keypoint adapter records requested image size but uses the recognized 224x224 model input convention.

Class mapping warning:

The TOM v1 ball model may emit `class 0 = ball`. If real detection returns zero useful detections, lower the confidence threshold, inspect debug payloads/artifacts if available, check class names emitted by Ultralytics, and add an explicit class map only when the model output proves the mapping. Do not relabel unknown classes without evidence.

TOM v1-origin detections and poses are still model-output observations. They do not confirm ball path, player identity, court position, bounce/hit/in-out/rally/point/scoring, or official tennis truth.

Main player track replay:

```text
/replay/<media_id>?detectionRunId=<player_detection_run_id>&trackletRunId=<player_tracklet_run_id>&subjectRunId=<main_subject_run_id>&mainPlayerTrackRunId=<main_player_track_run_id>&poseRunId=<track_filtered_pose_run_id>
```

When `mainPlayerTrackRunId` is present, replay can show selectable `NEAR TRACK` and `FAR TRACK` candidate labels over accepted track assignments. The labels expose track candidate evidence; they are not player identities.

Replay display policy:

The replay workstation includes display modes for dense real detection/tracklet runs:

- Current only
- Short trail
- Full trail

Detection display defaults to current-only. Tracklet point display defaults to short-trail, and tracklet trail/path rendering is off by default. These are visual review controls only; they do not change persisted observations, candidate tracklets, or evidence semantics.

Replay view presets:

```text
/replay/<media_id>?motionSmoothingRunId=<run_id>&courtRunId=<run_id>&homographyRunId=<run_id>&courtProjectionRunId=<run_id>&ballTrajectoryRunId=<run_id>&eventCandidateRunId=<run_id>&viewPreset=operator
/replay/<media_id>?motionSmoothingRunId=<run_id>&courtRunId=<run_id>&homographyRunId=<run_id>&courtProjectionRunId=<run_id>&ballTrajectoryRunId=<run_id>&eventCandidateRunId=<run_id>&viewPreset=debug
```

`operator` is the default when `viewPreset` is omitted. It keeps the replay clean by showing stable
candidate layers and hiding raw/debug layers by default. Smoothed ball/player/pose candidates,
mapped court keypoints, court line evidence, court carry-forward, and the court projection mini-map
are enabled when their runs exist. Raw TOM v1 keypoints, homography overlays, projection
diagnostics, raw detection trails, raw pose, and camera/view evidence stay off unless explicitly
enabled.

`debug` enables raw/audit layers when their run ids exist. Selecting either preset only changes UI
layer toggles. It does not mutate persisted observations or change candidate evidence into truth.

When `eventCandidateRunId` is present, replay can show `HIT CANDIDATE` and `BOUNCE CANDIDATE`
markers on the normalized court mini-map and, when a source image point is available, on the
broadcast video. Labels must include `candidate`; they do not confirm hits, bounces, in/out,
points, or score.

Selected event-candidate evidence also exposes physics diagnostics when present:

- hit candidates: `net_axis_reversal`
- ball-first hit recall: `net_axis_reversal_recall`
- bounce candidates: `vertical_motion_proxy` and `speed_reduction`

Motion smoothing replay:

```text
/replay/<media_id>?motionSmoothingRunId=<motion_smoothing_run_id>
```

When `motionSmoothingRunId` is present, replay can show smoothed ball, smoothed main player box,
and smoothed pose candidate layers. Raw detections, raw tracklet points, and raw pose observations
remain available as audit layers. Smoothed overlays are derived candidate evidence, not object
truth or tennis-event interpretation.

## 11B. Court / Homography Decision Gate

Milestone 7E is docs/status only. It decides that court/camera/homography evidence should be implemented as future Blueprint 8 work, not inside Blueprint 7.

Read:

```text
docs/court/court_homography_evidence_decision_v0.md
docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md
```

There is no `make court`, no homography runtime, no schema migration, no replay court overlay, and no production court-space transform in 7E.

Future court evidence should remain observation-only:

```text
court keypoint evidence
-> court line evidence
-> camera/view evidence
-> homography candidate
-> projection diagnostic
```

Those records should not become bounce/hit/rally/point/scoring conclusions.

## 11C. Blueprint 7 Final Perception Orchestration

Blueprint 7 is complete. The final local path keeps the fixture-safe baseline separate from optional real runtime work.

Fixture-safe baseline:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
make completion-audit PYTHON=.venv/bin/python
```

Optional real detection replay:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<detection_model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Replay:

```text
/replay/<media_id>?detectionRunId=<real_detection_run_id>
```

Optional real-detection-derived candidate tracklets:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
.venv/bin/python -m apps.worker.cli build-tracklets \
  --detection-run-id <real_detection_run_id> \
  --run-name real-detection-tracklet-candidates
```

Replay:

```text
/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>
```

Optional real pose replay:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <real_detection_run_id> \
  --weights ./model_assets/pose/<pose_model>.pt \
  --mode crop_from_player_detection \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Replay:

```text
/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>&poseRunId=<real_pose_run_id>
```

Start the API and web app against the same database before opening replay URLs:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
.venv/bin/python -m uvicorn apps.api.main:app --reload
```

```bash
make web
```

Default validation does not require local weights. If local YOLO or pose weights are absent, skip optional real smokes and use the fixture-safe baseline plus plan-only command checks.

## 11D. Court Evidence Schema Contract

Blueprint 8 began with Milestone 8A schema/contract work.

Read:

```text
docs/court/court_evidence_schema_v0.md
docs/court/court_template_registry_v0.md
```

8A adds typed storage for:

```text
court_keypoint_observation
court_line_observation
camera_view_observation
homography_candidate_observation
projection_diagnostic_observation
```

Run schema/persistence tests:

```bash
.venv/bin/python -m pytest tests/test_court_schema.py tests/test_court_observation_persistence.py -q
```

## 11E. Fixture Court Evidence Adapter

Milestone 8B adds a deterministic fixture court evidence adapter. First index media through the fixture demo:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8b_court_fixture.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
```

Then run fixture court evidence for the resulting `media_id`:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8b_court_fixture.db \
.venv/bin/python -m apps.worker.cli run-fixture-court \
  --media-id <media_id> \
  --frame-sample-rate 30 \
  --max-frames 30
```

Or use:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8b_court_fixture.db \
make court-fixture MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=30
```

Plan-only mode:

```bash
.venv/bin/python -m apps.worker.cli run-fixture-court \
  --media-id media-plan \
  --plan-only
```

Expected output includes `court_run_id`, sampled frames, and positive counts for:

```text
court_keypoint_observation
court_line_observation
camera_view_observation
```

Fixture court evidence is the source input for homography candidate persistence and later replay overlays, but it is not a real court model.

## 11F. Camera / View Evidence Queries

Milestone 8C exposes fixture camera/view observations as read-only geometry context evidence.

After running `run-fixture-court`, start the API against the same database:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8b_court_fixture.db \
.venv/bin/python -m uvicorn apps.api.main:app --reload
```

Then query:

```text
GET /court/camera-view?media_id=<media_id>&run_id=<court_run_id>
GET /court/camera-view/summary?media_id=<media_id>&run_id=<court_run_id>
GET /court/camera-view/<camera_view_observation_id>/bundle
```

Expected results:

- camera/view rows return media-owned frame/time.
- summary counts `broadcast_hardcam` and `stable` fixture evidence.
- bundle includes observation spine, typed camera/view detail, run/model/runtime context, annotations, artifacts, and lineage arrays.

This is not a confirmed camera state and does not compute homography.

## 11G. Homography Candidate Persistence

Milestone 8D builds candidate homography observations from persisted court evidence.

After running `run-fixture-court`, build homography candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8b_court_fixture.db \
.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id <media_id> \
  --court-run-id <court_run_id>
```

Or use:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8b_court_fixture.db \
make homography-candidates \
  MEDIA_ID=<media_id> \
  COURT_RUN_ID=<court_run_id> \
  PYTHON=.venv/bin/python
```

Plan-only mode:

```bash
.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id media-plan \
  --court-run-id court-run-plan \
  --plan-only
```

Expected output includes `homography_run_id`, candidate counts, source counts, sampled frames, and a replay URL with `courtRunId` and `homographyRunId`.

Homography candidates are candidate geometry evidence only. 8D does not add projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, or adjudication.

## 11H. Court Overlay Replay Workstation

Milestone 8E renders persisted court evidence in the replay workstation.

After running `run-fixture-court` and `build-homography-candidates`, start the API and web app against the same database:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8e_fixture_demo.db \
.venv/bin/python -m uvicorn apps.api.main:app --reload
```

Second terminal:

```bash
make web
```

Open:

```text
http://127.0.0.1:3000/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>
```

Expected:

- court keypoint evidence can be displayed
- court line evidence can be displayed
- camera/view evidence is visible as replay context
- homography candidate geometry can be displayed from persisted candidate rows
- selected court evidence remains geometry evidence only
- no projection diagnostics, ball/player court-space projection, bounce, hit, line-call, rally, point, score, or adjudication is produced

## 11I. Projection Diagnostics / Court Review Export

Milestone 8F persists projection diagnostic observations from homography candidates and exports TOM-native court review datasets.

After running `run-fixture-court` and `build-homography-candidates`, build projection diagnostics:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_projection_diag.db \
.venv/bin/python -m apps.worker.cli build-projection-diagnostics \
  --media-id <media_id> \
  --homography-run-id <homography_run_id>
```

Or use:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_projection_diag.db \
make projection-diagnostics \
  MEDIA_ID=<media_id> \
  HOMOGRAPHY_RUN_ID=<homography_run_id> \
  PYTHON=.venv/bin/python
```

Plan-only mode:

```bash
.venv/bin/python -m apps.worker.cli build-projection-diagnostics \
  --media-id media-plan \
  --homography-run-id homography-run-plan \
  --plan-only
```

Expected output includes `projection_diagnostic_run_id`, diagnostic counts, source counts, sampled frames, and a replay URL with `projectionDiagnosticRunId`.

Export a court review dataset:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_projection_diag.db \
.venv/bin/python -m apps.worker.cli export-court-review-dataset \
  --media-id <media_id> \
  --court-run-id <court_run_id> \
  --homography-run-id <homography_run_id> \
  --projection-diagnostic-run-id <projection_diagnostic_run_id>
```

Or use:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_8f_projection_diag.db \
make court-review-export \
  MEDIA_ID=<media_id> \
  COURT_RUN_ID=<court_run_id> \
  HOMOGRAPHY_RUN_ID=<homography_run_id> \
  PROJECTION_DIAGNOSTIC_RUN_ID=<projection_diagnostic_run_id> \
  PYTHON=.venv/bin/python
```

Open replay with diagnostics:

```text
http://127.0.0.1:3000/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>&projectionDiagnosticRunId=<projection_diagnostic_run_id>
```

Projection diagnostics are review evidence for projected court template geometry. They do not project ball/player observations into court space and do not produce bounce, hit, line-call, rally, point, score, or adjudication.

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

To review sparse court geometry without flicker, open replay with temporal display persistence:

```text
/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>&projectionDiagnosticRunId=<projection_diagnostic_run_id>&courtTemporalPersistence=carry_forward&courtPersistenceMaxGapMs=1500
```

The Next replay page passes these settings to `GET /replay/overlays` as:

```text
court_temporal_persistence=carry_forward
court_persistence_max_gap_ms=1500
```

This is a display/read-model policy only. It carries candidate geometry forward for review and does not confirm a court model, in/out, bounce location, player court position, point, or score.

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
- Real pose replay is optional and locally gated by pose runtime and weights.
- Pose is keypoint evidence only, not movement interpretation.
- Tracklets are candidates, not official rallies or points.
- Homography candidates, projection diagnostics, and object-to-court projection candidates are
  evidence only, not final court models or object truth.
- Hit/bounce event candidates can be produced for review, but they remain candidate evidence only.
  Persistent replay markers are not hit truth, bounce truth, in/out, rally, point, score, or
  adjudication.
- Player-anchored hit recall is enabled by default for hit/bounce candidate builds. It uses near/far
  main player projection anchors plus a bounded wider ball trajectory window to recover additional
  `hit_candidate` evidence, and it remains candidate-only.
- Player-anchored hit contact-zone tightening suppresses anchored hits that overlap final
  bounce/open-court landing clusters. The diagnostics explain the suppression, but they do not
  create hit truth, bounce truth, in/out, score, or adjudication.
- Image-space net-axis hit recall uses a broadcast image-y fallback to improve airborne hit
  candidate recall. This is not true camera geometry, true ball height, hit truth, in/out, score,
  or adjudication.
- Local-evidence event type classification v0.2.8 is enabled by default for image-space
  direction-change event candidates. It can keep a direction change as `hit_candidate` or reclassify
  it to `bounce_candidate` based on local landing/contact evidence. A hit candidate does not
  require a prior bounce.
- Universal hit candidate validity guard v0.3.0 is enabled by default after all hit/bounce
  candidate classifiers. It evaluates every final hit-candidate source, records
  `universal_hit_validity_guard` metadata, can reclassify unsupported landing-like hits to
  `bounce_candidate`, and can suppress fly-through/no-event hits into diagnostics. v0.3.0 treats
  court-y/image-y reversal as hard support and generic image-direction changes as diagnostic support
  only. This is still candidate evidence only.
- Marker-level event arbitration v0.3.1 runs after the universal guard. It resolves visible
  co-located hit/bounce marker conflicts to the bounce marker unless the hit has strong independent
  contact evidence, and it suppresses transit/fly-through hit markers into diagnostics. It records
  `marker_level_arbitration`, keeps `hit_requires_prior_bounce = false`, and keeps
  `sequence_is_hard_gate = false`. This is marker-level candidate display arbitration only, not
  hit truth, bounce truth, in/out, score, or adjudication.
- Compact CLI + Marker Summary v0 changes default hit/bounce command output only. Full diagnostic
  data is still persisted and can be printed with verbose/debug flags.
- Replay Marker Inspector v0 and Event Candidate Review Panel v0 use `marker_summary` in replay so
  operators can review final visible hit/bounce markers, click rows to seek/select markers, and
  inspect compact candidate evidence without terminal JSON. This is display-only and does not
  create truth, in/out, score, or adjudication.
- Point Evidence Snapshot v0 can freeze a specific media/event-candidate run into a compact JSON or
  markdown report with replay URL, source run ids, counts, active versions, final markers, warnings,
  and known limitations. It is report-only and does not create truth, in/out, score, or
  adjudication.
- Blueprint 9 Manual Candidate Review Annotation v0 lets an operator mark selected event candidate
  markers as `useful`, `wrong`, `unclear`, or `needs_review`, and add missing-candidate notes at the
  current replay time. The annotations are review metadata only and do not change event candidate
  generation, marker counts, point evidence, in/out, score, accepted/rejected lifecycle, or
  adjudication.
- Blueprint 10 Benchmark / Evaluation Harness v0 summarizes generated point candidate markers and
  Blueprint 9 review annotations with `evaluate-point-candidates` and
  `tom-v1-evaluate-point-candidates`. It is a read-only review report; it does not compute
  precision/recall in v0, promote labels into truth, correct candidates, decide in/out, score a
  point, or adjudicate evidence.
- Blueprint 11 3D Readiness / Camera Geometry Evidence Layer v0 records declared camera/court
  geometry metadata and unknown intrinsics/extrinsics placeholders. It prepares TOM for future 3D
  evidence layers without creating 3D ball trajectories, 3D truth, event truth, in/out, score,
  accepted/rejected lifecycle, automatic correction, or adjudication.
- Blueprint 12 3D Ball Trajectory Candidate Evidence v0 records provisional metric court-plane
  x/y samples from existing ball trajectory candidates and declared camera geometry. Default height
  is unknown. It does not create true 3D reconstruction, verified ball height, event truth, in/out,
  score, accepted/rejected lifecycle, automatic correction, or adjudication.
- Blueprint 13 3D-Assisted Event Candidate Diagnostics v0 links final hit/bounce marker rows to
  nearby 3D trajectory candidate samples. It reports nearby sample counts, nearest metric x/y,
  height status, and conservative diagnostic labels. It does not change hit/bounce classification,
  marker counts, review annotations, in/out, score, or adjudication.
- Blueprint 8 Completion Review / Freeze v0 freezes the current evidence workstation as a
  documented, reproducible candidate-evidence milestone. It does not add tennis logic, truth,
  score, in/out, manual correction, accepted/rejected lifecycle, or adjudication.
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

Build 3D-assisted event candidate diagnostics:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-build-event-candidate-3d-diagnostics \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id>
```

Expected output includes `diagnostic_type=event_candidate_3d_diagnostic_evidence`,
`diagnostic_version=v0`, one diagnostic per final marker when markers exist, and warnings that the
diagnostics are not truth, not 3D truth, not in/out, not score, and not adjudication.

Open the Blueprint 14 3D Debug View by adding the selected 3D trajectory candidate run:

```text
http://127.0.0.1:3000/replay/<media_id>?eventCandidateRunId=<event_candidate_run_id>&trajectory3dRunId=<trajectory_3d_run_id>
```

The Replay Workstation side panel shows a display-only court-plane debug view of existing 3D
candidate samples. It can highlight the nearest 3D diagnostic sample for a selected marker when
Blueprint 13 diagnostics exist. Height remains unknown in v0, and the view does not change
hit/bounce candidates, in/out, score, or adjudication.

Blueprint 15 adds selection and timeline coupling to that same panel:

- current replay time highlights the nearest 3D candidate sample
- samples within the local ±250ms window are emphasized
- clicking a 3D sample requests replay seek to that sample timestamp
- clicked sample metadata is shown in the panel
- selected hit/bounce markers still highlight linked 3D diagnostic samples when available

The 3D panel requests seek through existing replay controls. It does not own playback time or
change generated evidence.

Blueprint 16 adds 3D debug review annotations to the same panel:

- click a 3D sample and save a useful/wrong/unclear/needs-review/bad-position review
- select a marker with a 3D diagnostic and save a useful/wrong/unclear/needs-review/bad-link review
- add a missing 3D sample note at current replay time

These reviews persist as `trajectory_3d_debug_review_annotation` metadata. They do not change
candidate counts, event marker review counts, 3D samples, 3D diagnostics, in/out, score, or
adjudication.

Export reviewed 3D debug evidence for offline analysis:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-export-reviewed-3d-debug-dataset \
  PYTHON=.venv/bin/python \
  MEDIA_ID=<media_id> \
  EVENT_CANDIDATE_RUN_ID=<event_candidate_run_id> \
  TRAJECTORY_3D_RUN_ID=<trajectory_3d_run_id> \
  CAMERA_GEOMETRY_ID=<camera_geometry_id> \
  FORMAT=json \
  OUTPUT=.data/exports/reviewed_3d_debug_dataset.json
```

Use `FORMAT=markdown` for a compact human-readable report. The export is read-only dataset
metadata. Review labels are not truth, not 3D truth, and not training truth.

Compare a current reviewed 3D debug dataset export with a saved baseline export:

```bash
.venv/bin/python -m apps.worker.cli compare-reviewed-3d-debug-dataset \
  --baseline .data/exports/reviewed_3d_debug_dataset_sample_point.baseline.json \
  --current .data/exports/reviewed_3d_debug_dataset_sample_point.current.json \
  --format json \
  --output .data/exports/reviewed_3d_debug_dataset_sample_point.regression.json
```

Or use the Make helper:

```bash
make tom-v1-compare-reviewed-3d-debug-dataset \
  BASELINE=.data/exports/reviewed_3d_debug_dataset_sample_point.baseline.json \
  CURRENT=.data/exports/reviewed_3d_debug_dataset_sample_point.current.json \
  FORMAT=json \
  OUTPUT=.data/exports/reviewed_3d_debug_dataset_sample_point.regression.json
```

Use `STRICT=true` to return `failed_regression` when drift is detected. Baseline exports are
comparison references only; they are not truth or training truth, and drift does not change live TOM
behavior.

Freeze the current sample-point reviewed 3D debug export as a local baseline:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-freeze-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Verify the current sample-point export against the local baseline:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

The gate writes local `.data/baselines` and `.data/exports` files. These are generated regression
artifacts. The baseline is not truth, and drift requires human review before any follow-up work.

## sample_point Expansion Readiness Gate

Use this gate before introducing a controlled second point. It verifies the current `sample_point`
profile, then records the point snapshot, point candidate evaluation, and reviewed 3D debug export.
The gate is evidence-only: it does not create truth, training truth, in/out, score, or adjudication.

Verify the reviewed 3D debug baseline:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Expected:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true

## Calibration Evaluation Sandbox Regression Gate

Use this after Blueprint 50 evaluation inputs and reports have been built. The gate freezes and
verifies structural sandbox behavior only. It does not apply threshold, smoothing, hysteresis, model,
runtime config, or baseline changes.

Build the tracked contract and frozen baseline:

```bash
make tom-v1-export-review-guided-gameplay-calibration-sandbox-regression-contract \
  PYTHON=.venv/bin/python

make tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-baseline \
  PYTHON=.venv/bin/python
```

Verify the baseline:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-review-guided-gameplay-calibration-sandbox-regression-baseline \
  PYTHON=.venv/bin/python
```

Expected:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
- `sandbox_is_not_truth`: true
- `sandbox_is_not_accuracy_scoring`: true
- `threshold_changes_not_applied`: true
- `smoothing_changes_not_applied`: true
- `hysteresis_changes_not_applied`: true
- `runtime_config_not_updated`: true
- `model_weights_not_modified`: true
- `baseline_not_replaced`: true
- `classifier_correctness_not_assessed`: true
- `generalization_not_claimed`: true

Build the local regression report if needed:

```bash
make tom-v1-build-review-guided-gameplay-calibration-sandbox-regression-report \
  PYTHON=.venv/bin/python
```

The tracked baseline currently marks fixture/demo reuse only. It is not a distinct real broadcast
corpus and does not claim generalization.

## Calibration Candidate Decision Packet

Use this after Blueprint 49 proposal, Blueprint 50 sandbox evaluation, and Blueprint 51 sandbox
regression verification outputs have been built. The packet packages prior calibration evidence
for operator review only. It keeps candidates marked `not_applied` and keeps
`runtime_change_status` as `not_applied`.

Build the tracked contract:

```bash
make tom-v1-export-calibration-candidate-decision-packet-contract \
  PYTHON=.venv/bin/python
```

Build and validate packet inputs:

```bash
make tom-v1-build-calibration-candidate-decision-packet-inputs \
  PYTHON=.venv/bin/python

make tom-v1-validate-calibration-candidate-decision-packet-inputs \
  PYTHON=.venv/bin/python
```

Build and validate the decision packet:

```bash
make tom-v1-build-calibration-candidate-decision-packet \
  PYTHON=.venv/bin/python

make tom-v1-validate-calibration-candidate-decision-packet \
  PYTHON=.venv/bin/python
```

Build the operator report:

```bash
make tom-v1-build-calibration-candidate-decision-packet-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/calibration_candidate_decision_packet_contract_v1.json`. Generated packet inputs,
validations, decision packets, and reports live under `.data/exports/` and should stay local.

The decision packet does not apply threshold, smoothing, or hysteresis changes, update runtime
config, mutate model weights, replace baselines, create review labels, infer tennis truth, score
classifier correctness, or select candidates for runtime use. Human operator decision remains
required for future manual review.

## Gameplay-Gated Perception Execution Hook

Use this after the Blueprint 38 gameplay segment gate and Blueprint 39 routing plan are available.
The execution hook is structural by default: it records which perception stages should run on
gameplay-approved windows and which windows should be skipped or reviewed. It does not run heavy
perception inference, write observations by default, create tennis truth, or adjudicate evidence.

Export the tracked contract:

```bash
make tom-v1-export-gameplay-gated-perception-execution-contract \
  PYTHON=.venv/bin/python
```

Build a gameplay-gated perception execution plan from a Blueprint 39 routing plan:

```bash
make tom-v1-build-gameplay-gated-perception-execution-plan \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
```

Validate the plan:

```bash
make tom-v1-validate-gameplay-gated-perception-execution-plan \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN=.data/exports/gameplay_gated_perception_execution_plan.current.json \
  GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
```

Build the report:

```bash
make tom-v1-build-gameplay-gated-perception-execution-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_PERCEPTION_EXECUTION_PLAN=.data/exports/gameplay_gated_perception_execution_plan.current.json \
  GAMEPLAY_GATED_PERCEPTION_EXECUTION_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
```

Expected:

- `ok`: true
- `status`: `completed` or `valid`
- `execution_mode`: `dry_run`
- `perception_jobs_executed`: false
- `gpu_or_model_inference_executed`: false
- `observations_written`: false
- skipped and review-required windows are preserved with reasons

## Gameplay Segment Replay Timeline / Operator Review

Use this after the Blueprint 38 gameplay segment gate, Blueprint 39 routing plan, and Blueprint 40
execution plan are available. The replay/review surface is structural by default: it records
timeline lanes and review metadata templates for operator inspection. It does not run inference,
write observations, persist review notes, decide classifier correctness, create tennis truth, or
adjudicate evidence.

Export the tracked contract:

```bash
make tom-v1-export-gameplay-segment-replay-review-contract \
  PYTHON=.venv/bin/python
```

Build a gameplay segment replay timeline:

```bash
make tom-v1-build-gameplay-segment-replay-timeline \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS=.data/exports/gameplay_segment_candidates.current.json \
  GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json \
  GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN=.data/exports/gameplay_gated_perception_execution_plan.current.json
```

Validate the timeline:

```bash
make tom-v1-validate-gameplay-segment-replay-timeline \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_REPLAY_TIMELINE=.data/exports/gameplay_segment_replay_timeline.current.json \
  GAMEPLAY_SEGMENT_REPLAY_REVIEW_GAMEPLAY_SEGMENTS=.data/exports/gameplay_segment_candidates.current.json \
  GAMEPLAY_SEGMENT_REPLAY_REVIEW_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json \
  GAMEPLAY_SEGMENT_REPLAY_REVIEW_EXECUTION_PLAN=.data/exports/gameplay_gated_perception_execution_plan.current.json
```

Build a review template:

```bash
make tom-v1-build-gameplay-segment-review-template \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_REPLAY_TIMELINE=.data/exports/gameplay_segment_replay_timeline.current.json
```

Validate the review bundle:

```bash
make tom-v1-validate-gameplay-segment-review-bundle \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_REPLAY_TIMELINE=.data/exports/gameplay_segment_replay_timeline.current.json \
  GAMEPLAY_SEGMENT_REVIEW_BUNDLE=.data/exports/gameplay_segment_review_template.current.json
```

Build the review report:

```bash
make tom-v1-build-gameplay-segment-review-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_REPLAY_TIMELINE=.data/exports/gameplay_segment_replay_timeline.current.json \
  GAMEPLAY_SEGMENT_REVIEW_BUNDLE=.data/exports/gameplay_segment_review_template.current.json
```

Expected:

- `ok`: true
- `status`: `completed` or `valid`
- timeline lanes include gameplay candidate, non-gameplay candidate, uncertain, downstream, and
  perception execution/skipped windows when source artifacts are supplied
- review entries default to `not_reviewed`
- review statuses are human metadata only
- generated `.data/exports/` files stay local and untracked

## Gameplay-Gated Many-Point Ingestion Smoke

Use this after the Blueprint 38-41 contracts are available. The smoke workflow reads explicit
media entries, runs the many-point ingestion gate in dry-run mode, and builds gameplay-gated
structural artifacts for each entry. It does not auto-discover folders, run GPU/model inference by
default, write observations, mutate model assets, mutate baselines, create labels, decide tennis
truth, or adjudicate evidence.

Export the tracked contract:

```bash
make tom-v1-export-gameplay-gated-many-point-smoke-contract \
  PYTHON=.venv/bin/python
```

Build an explicit smoke manifest:

```bash
make tom-v1-build-gameplay-gated-many-point-smoke-manifest-template \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_MEDIA_PATH=demo_assets/sample_point.mp4
```

Validate the smoke manifest:

```bash
make tom-v1-validate-gameplay-gated-many-point-smoke-manifest \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST=.data/exports/gameplay_gated_many_point_smoke_manifest.template.json
```

Run the structural smoke:

```bash
make tom-v1-run-gameplay-gated-many-point-smoke \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_MANIFEST=.data/exports/gameplay_gated_many_point_smoke_manifest.template.json
```

Build the smoke report:

```bash
make tom-v1-build-gameplay-gated-many-point-smoke-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_MANY_POINT_SMOKE_REPORT=.data/exports/gameplay_gated_many_point_smoke.current.json
```

If `demo_assets/sample_point.mp4` is reused more than once as a fixture stand-in, generated
manifests and reports must preserve `fixture_reuse_only`, `not_distinct_real_points`, and
`does_not_claim_generalization`.

## Gameplay Gate Regression Baseline

Use this after the Blueprint 38-42 contracts are available. The regression gate freezes a
fixture-safe structural summary for the gameplay gate stack and verifies future runs against that
baseline. It does not prove classifier correctness, point detection, line calls, score, player
identity, production readiness, training truth, generalization, or adjudication.

Export the tracked contract:

```bash
make tom-v1-export-gameplay-gate-regression-baseline-contract \
  PYTHON=.venv/bin/python
```

Build the tracked baseline:

```bash
make tom-v1-build-gameplay-gate-regression-baseline \
  PYTHON=.venv/bin/python
```

Verify the current fixture-safe gameplay gate profile:

```bash
make tom-v1-verify-gameplay-gate-regression-baseline \
  PYTHON=.venv/bin/python
```

Build a local verification report:

```bash
make tom-v1-build-gameplay-gate-regression-report \
  PYTHON=.venv/bin/python
```

The protected success shape is `ok=true`, `status=completed`, `drift_detected=false`,
`breaking_drift_detected=false`, `baseline_is_not_truth=true`, and
`gameplay_gate_is_not_truth=true`.

## Gameplay Gate Review Dataset Export

Use this after the Blueprint 38-43 contracts and regression baseline are available. The review
dataset export turns gameplay segment candidates, routing context, perception execution context,
replay timeline context, and regression context into a local human-review bundle. It does not
create labels, prove classifier correctness, detect points, call lines, score, identify players,
relabel automatically, claim generalization, or adjudicate evidence.

Export the tracked contract:

```bash
make tom-v1-export-gameplay-gate-review-dataset-contract \
  PYTHON=.venv/bin/python
```

Build a local review dataset:

```bash
make tom-v1-build-gameplay-gate-review-dataset \
  PYTHON=.venv/bin/python
```

Validate the local review dataset:

```bash
make tom-v1-validate-gameplay-gate-review-dataset \
  PYTHON=.venv/bin/python
```

Build a local structural report:

```bash
make tom-v1-build-gameplay-gate-review-dataset-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/gameplay_gate_review_dataset_export_contract_v1.json`. Generated dataset,
validation, report, and intermediate source artifacts live under `.data/exports/` and should stay
local unless a future milestone explicitly documents committing them.

## Gameplay Gate Pathway Completion Freeze

Use this after the Blueprint 38-44 gameplay pathway is complete. The freeze records completed
gameplay milestones, frozen gameplay contracts, the protected gameplay regression baseline,
required gates, model asset guardrails, non-claims, limitations, and the recommended Blueprint 46
controlled real broadcast corpus run. It does not add gameplay capability, run model inference,
create labels, prove classifier correctness/accuracy, mutate model assets, claim generalization,
or adjudicate evidence.

Build the tracked freeze manifest:

```bash
make tom-v1-build-gameplay-gate-pathway-completion-freeze \
  PYTHON=.venv/bin/python
```

Validate the freeze:

```bash
make tom-v1-validate-gameplay-gate-pathway-completion-freeze \
  PYTHON=.venv/bin/python
```

Build the local next-phase readiness report:

```bash
make tom-v1-build-gameplay-gate-next-phase-readiness-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/gameplay_gate_pathway_completion_freeze_v1.json`. Generated validation and
readiness report files live under `.data/exports/` and should stay local unless a future milestone
explicitly documents committing them.

## Real Broadcast Gameplay Gate Corpus Run

Blueprint 46 runs explicit local broadcast-style media entries through the frozen gameplay gate
pathway. It supports real local media supplied by the operator, but the default mode is `dry_run`.
TOM does not scan folders, ingest arbitrary media, train the gameplay classifier, modify model
assets, create labels, score classifier accuracy, prove generalization, decide tennis truth, or
adjudicate evidence.

Export the tracked contract:

```bash
make tom-v1-export-real-broadcast-gameplay-corpus-run-contract \
  PYTHON=.venv/bin/python
```

Build an explicit manifest template:

```bash
make tom-v1-build-real-broadcast-gameplay-corpus-manifest-template \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_CORPUS_MEDIA_PATH=/path/to/broadcast_clip.mp4 \
  REAL_BROADCAST_GAMEPLAY_CORPUS_SOURCE_LABEL=local_broadcast_clip \
  REAL_BROADCAST_GAMEPLAY_CORPUS_CONTENT_TAG=live_gameplay
```

Validate the manifest in the intended mode:

```bash
make tom-v1-validate-real-broadcast-gameplay-corpus-manifest \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE=dry_run
```

Run the corpus path only after the manifest is explicit:

```bash
make tom-v1-run-real-broadcast-gameplay-corpus \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_CORPUS_RUN_MODE=explicit_local_media_run
```

Build the human-review readiness report:

```bash
make tom-v1-build-real-broadcast-gameplay-corpus-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/real_broadcast_gameplay_corpus_run_contract_v1.json`. Generated manifests,
validations, corpus run outputs, per-entry artifacts, and readiness reports live under
`.data/exports/` and should stay local unless a future milestone explicitly documents committing
reviewed corpus fixtures.

## Real Broadcast Gameplay Review Loop

Blueprint 47 builds a human review metadata loop over Blueprint 46 corpus run outputs and
Blueprint 44 review dataset entries. It reads existing artifacts, preserves replay URLs,
timestamps, classifier probabilities, statuses, routing/execution context, baseline context, and
expected broadcast tags, then emits a review bundle template. It does not infer labels, score the
classifier, relabel automatically, decide tennis truth, mutate model assets, or mutate baselines.

Export the tracked contract:

```bash
make tom-v1-export-real-broadcast-gameplay-review-loop-contract \
  PYTHON=.venv/bin/python
```

Build a review bundle template from the latest local BP46 corpus run:

```bash
make tom-v1-build-real-broadcast-gameplay-review-bundle-template \
  PYTHON=.venv/bin/python \
  REAL_BROADCAST_GAMEPLAY_REVIEW_SOURCE_CORPUS_RUN=.data/exports/real_broadcast_gameplay_corpus_run.current.json
```

Validate a review bundle:

```bash
make tom-v1-validate-real-broadcast-gameplay-review-bundle \
  PYTHON=.venv/bin/python
```

Build review metadata coverage and distribution reporting:

```bash
make tom-v1-build-real-broadcast-gameplay-review-loop-report \
  PYTHON=.venv/bin/python
```

Build the human review readiness report:

```bash
make tom-v1-build-real-broadcast-gameplay-human-review-readiness-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/real_broadcast_gameplay_review_loop_contract_v1.json`. Generated review bundles,
validations, review-loop reports, and readiness reports live under `.data/exports/` and should
stay local unless a future milestone explicitly documents committing reviewed fixtures.

Human review fields are metadata only. They do not create training truth, gameplay truth,
classifier correctness, classifier accuracy, accepted/rejected lifecycle, automatic relabeling,
reviewer scoring, production readiness, generalization, or adjudication.

## Real Broadcast Gameplay Review Metrics / QA Dashboard

Blueprint 48 summarizes Blueprint 47 review loop outputs into review operations metrics,
dashboard-ready QA data, and next-review actions. It reads existing artifacts and does not infer
labels, score the classifier, relabel automatically, change thresholds, tune models, decide
tennis truth, mutate model assets, or mutate baselines.

Export the tracked contract:

```bash
make tom-v1-export-real-broadcast-gameplay-review-metrics-contract \
  PYTHON=.venv/bin/python
```

Build the review metrics report from the latest local BP47/BP46 outputs:

```bash
make tom-v1-build-real-broadcast-gameplay-review-metrics-report \
  PYTHON=.venv/bin/python
```

Validate the metrics report:

```bash
make tom-v1-validate-real-broadcast-gameplay-review-metrics-report \
  PYTHON=.venv/bin/python
```

Build dashboard-ready QA data:

```bash
make tom-v1-build-real-broadcast-gameplay-review-qa-dashboard \
  PYTHON=.venv/bin/python
```

Build next-review actions:

```bash
make tom-v1-build-real-broadcast-gameplay-review-next-actions-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/real_broadcast_gameplay_review_metrics_contract_v1.json`. Generated metrics
reports, validations, QA dashboard data, and next-actions reports live under `.data/exports/` and
should stay local unless a future milestone explicitly documents committing reviewed fixtures.

Metrics are operational visibility only. They do not create training truth, gameplay truth,
classifier correctness, classifier accuracy, accepted/rejected lifecycle, automatic relabeling,
reviewer scoring, production readiness, generalization, threshold changes, model tuning, or
adjudication.

## Review-Guided Gameplay Gate Calibration Proposal

Blueprint 49 summarizes Blueprint 48 review metrics into calibration inputs and proposal-only
future-evaluation records. It reads existing artifacts and does not infer labels, score the
classifier, relabel automatically, change thresholds, smoothing, hysteresis, runtime config, tune
models, decide tennis truth, mutate model assets, or mutate baselines.

Export the tracked contract:

```bash
make tom-v1-export-review-guided-gameplay-calibration-proposal-contract \
  PYTHON=.venv/bin/python
```

Build calibration inputs from the latest local BP48/BP47/BP46 outputs:

```bash
make tom-v1-build-review-guided-gameplay-calibration-inputs \
  PYTHON=.venv/bin/python
```

Validate the calibration inputs:

```bash
make tom-v1-validate-review-guided-gameplay-calibration-inputs \
  PYTHON=.venv/bin/python
```

Build the future-evaluation proposal:

```bash
make tom-v1-build-review-guided-gameplay-calibration-proposal \
  PYTHON=.venv/bin/python
```

Validate the proposal:

```bash
make tom-v1-validate-review-guided-gameplay-calibration-proposal \
  PYTHON=.venv/bin/python
```

Build the proposal report:

```bash
make tom-v1-build-review-guided-gameplay-calibration-proposal-report \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/review_guided_gameplay_calibration_proposal_contract_v1.json`. Generated
calibration inputs, validations, proposal JSON, and proposal reports live under `.data/exports/`
and should stay local unless a future milestone explicitly documents committing reviewed fixtures.

Proposal items are planning records only. They do not create training truth, gameplay truth,
classifier correctness, classifier accuracy, accepted/rejected lifecycle, automatic relabeling,
reviewer scoring, production readiness, generalization, threshold changes, smoothing changes,
hysteresis changes, runtime changes, model tuning, or adjudication.

## Review-Guided Gameplay Calibration Evaluation Sandbox

Blueprint 50 evaluates Blueprint 49 proposal candidates in an offline sandbox. It reads existing
artifacts and does not infer labels, score the classifier, relabel automatically, change
thresholds, smoothing, hysteresis, runtime config, tune models, decide tennis truth, mutate model
assets, or mutate baselines.

Export the tracked contract:

```bash
make tom-v1-export-review-guided-gameplay-calibration-evaluation-sandbox-contract \
  PYTHON=.venv/bin/python
```

Build evaluation inputs from the latest local BP49/BP48/BP47/BP46 outputs:

```bash
make tom-v1-build-review-guided-gameplay-calibration-evaluation-inputs \
  PYTHON=.venv/bin/python
```

Validate the evaluation inputs:

```bash
make tom-v1-validate-review-guided-gameplay-calibration-evaluation-inputs \
  PYTHON=.venv/bin/python
```

Run the offline-only sandbox:

```bash
make tom-v1-run-review-guided-gameplay-calibration-evaluation-sandbox \
  PYTHON=.venv/bin/python
```

Validate the sandbox report:

```bash
make tom-v1-validate-review-guided-gameplay-calibration-evaluation-report \
  PYTHON=.venv/bin/python
```

Build the sandbox summary:

```bash
make tom-v1-build-review-guided-gameplay-calibration-evaluation-summary \
  PYTHON=.venv/bin/python
```

The tracked artifact is
`.data/contracts/review_guided_gameplay_calibration_evaluation_sandbox_contract_v1.json`.
Generated evaluation inputs, validations, sandbox reports, and summaries live under
`.data/exports/` and should stay local unless a future milestone explicitly documents committing
reviewed fixtures.

Evaluation candidates are sandbox records only. They do not create training truth, gameplay truth,
classifier correctness, classifier accuracy, accepted/rejected lifecycle, automatic relabeling,
reviewer scoring, production readiness, generalization, threshold changes, smoothing changes,
hysteresis changes, runtime changes, model tuning, baseline replacement, or adjudication.

## Camera Geometry Calibration Provenance

Blueprint 36 builds a structural camera geometry / calibration provenance profile from existing
point manifests, replay indexes, regression matrices, corpus entries, and label-feedback inputs.
It does not generate camera geometry, homography, projection diagnostics, event candidates, 3D
candidates, labels, truth, scoring, or adjudication.

Export the tracked contract:

```bash
make tom-v1-export-camera-geometry-calibration-provenance-contract \
  PYTHON=.venv/bin/python
```

Build the current profile:

```bash
make tom-v1-build-camera-geometry-calibration-profile \
  PYTHON=.venv/bin/python
```

Validate the profile:

```bash
make tom-v1-validate-camera-geometry-calibration-profile \
  PYTHON=.venv/bin/python \
  CAMERA_GEOMETRY_CALIBRATION_PROFILE=.data/exports/camera_geometry_calibration_profile.current.json
```

Build the report:

```bash
make tom-v1-build-camera-geometry-calibration-report \
  PYTHON=.venv/bin/python \
  CAMERA_GEOMETRY_CALIBRATION_PROFILE=.data/exports/camera_geometry_calibration_profile.current.json
```

Tracked contract:

```text
.data/contracts/camera_geometry_calibration_provenance_contract_v1.json
```

Generated outputs:

```text
.data/exports/camera_geometry_calibration_profile.current.json
.data/exports/camera_geometry_calibration_profile.validation.json
.data/exports/camera_geometry_calibration_report.current.json
```

Expected protected-sample interpretation:

- camera geometry evidence may be present through `camera_geometry_id`
- replay context may be present through the manifest-backed replay URL
- missing court keypoints, homography candidates, or projection diagnostics are review gaps
- `requires_human_calibration_review` can be true while TOM still makes no calibration claim
- `regression_protected_context` preserves baseline context only and is not a correctness finding

## TOM v3 Expansion Completion Freeze

Blueprint 37 freezes the completed BP22 through BP36 expansion as a tracked provenance/readiness
manifest. It records frozen contract refs, protected baseline refs, required regression gates,
capability summary, non-claims, known limitations, and the recommended first next phase. It does
not create evidence, ingest media, execute sampling, create labels, mutate baselines, retrain
models, wire gameplay classification, decide in/out, score, identify players, determine winners,
or adjudicate evidence.

Build the tracked freeze manifest:

```bash
make tom-v1-build-tom-v3-expansion-completion-freeze \
  PYTHON=.venv/bin/python
```

Validate the freeze:

```bash
make tom-v1-validate-tom-v3-expansion-completion-freeze \
  PYTHON=.venv/bin/python \
  TOM_V3_EXPANSION_COMPLETION_FREEZE=.data/contracts/tom_v3_expansion_completion_freeze_v1.json
```

Build the next-phase readiness report:

```bash
make tom-v1-build-tom-v3-next-phase-readiness-report \
  PYTHON=.venv/bin/python \
  TOM_V3_EXPANSION_COMPLETION_FREEZE=.data/contracts/tom_v3_expansion_completion_freeze_v1.json
```

Default paths:

```text
.data/contracts/tom_v3_expansion_completion_freeze_v1.json
.data/exports/tom_v3_expansion_completion_freeze.validation.json
.data/exports/tom_v3_next_phase_readiness_report.current.json
```

Expected:

- `ok`: true for freeze build, freeze validation, and readiness report
- `freeze_type`: `tom_v3_expansion_completion_freeze`
- `freeze_version`: `v1`
- `report_type`: `tom_v3_next_phase_readiness_report`
- `report_version`: `v1`
- `completed_blueprint_count`: 15
- `frozen_contract_count`: 11
- `tracked_exports`: `[]` in validation
- next phase recommends Gameplay Segment Gate / TOM v1 View Classifier Integration v1
- `model_assets/tom_v1/view_classifier_gameplay.pt` is recorded as the existing classifier asset,
  but not wired by Blueprint 37

## Gameplay Segment Gate

Blueprint 38 adds a candidate-only gameplay segment gate around the existing local TOM v1 gameplay
classifier asset. It records classifier asset provenance, builds explicit-media gameplay
suitability candidate segments, validates the artifact, and emits a replay timeline lane
structure for future downstream gating. It does not decide tennis truth, score, player identity,
line calls, point state, automatic correctness, or adjudication.

Export the tracked gate contract:

```bash
make tom-v1-export-gameplay-segment-gate-contract \
  PYTHON=.venv/bin/python
```

Inspect the local classifier asset:

```bash
make tom-v1-inspect-gameplay-classifier-asset \
  PYTHON=.venv/bin/python
```

Build candidate segments from explicit media input:

```bash
make tom-v1-build-gameplay-segment-candidates \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_MEDIA_PATH=demo_assets/sample_point.mp4 \
  GAMEPLAY_SEGMENT_MEDIA_ID=sample_point_gameplay_segment_gate_smoke
```

Validate the candidate artifact:

```bash
make tom-v1-validate-gameplay-segment-candidates \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_CANDIDATES=.data/exports/gameplay_segment_candidates.current.json
```

Build the structural report:

```bash
make tom-v1-build-gameplay-segment-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_SEGMENT_CANDIDATES=.data/exports/gameplay_segment_candidates.current.json
```

Default paths:

```text
.data/contracts/gameplay_segment_gate_contract_v1.json
.data/exports/gameplay_classifier_asset_inspection.current.json
.data/exports/gameplay_segment_candidates.current.json
.data/exports/gameplay_segment_candidates.validation.json
.data/exports/gameplay_segment_report.current.json
```

Expected:

- `ok`: true for contract export, asset inspection, candidate build, validation, and report
- `contract_type`: `gameplay_segment_gate_contract`
- `output_type`: `gameplay_segment_candidates`
- `report_type`: `gameplay_segment_gate_report`
- `model_asset_path`: `model_assets/tom_v1/view_classifier_gameplay.pt`
- model asset hash is present when the local asset exists
- generated `.data/exports/` files stay local and untracked
- model weights stay ignored and unmodified

## Gameplay-Gated Pipeline Routing

Blueprint 39 turns Blueprint 38 gameplay segment candidates into a structural routing plan for
future downstream evidence workflows. The default mode is `dry_run`; it records allowed, blocked,
and review-required routes without running detection, tracklet, pose, court, event, 3D, replay, or
corpus jobs.

Export the tracked routing contract:

```bash
make tom-v1-export-gameplay-gated-routing-contract \
  PYTHON=.venv/bin/python
```

Build a routing plan from gameplay segment candidates:

```bash
make tom-v1-build-gameplay-gated-routing-plan \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_ROUTING_GAMEPLAY_SEGMENTS=.data/exports/gameplay_segment_candidates.current.json
```

Validate the routing plan:

```bash
make tom-v1-validate-gameplay-gated-routing-plan \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
```

Build the structural routing report:

```bash
make tom-v1-build-gameplay-gated-routing-report \
  PYTHON=.venv/bin/python \
  GAMEPLAY_GATED_ROUTING_PLAN=.data/exports/gameplay_gated_routing_plan.current.json
```

Default paths:

```text
.data/contracts/gameplay_gated_pipeline_routing_contract_v1.json
.data/exports/gameplay_gated_routing_plan.current.json
.data/exports/gameplay_gated_routing_plan.validation.json
.data/exports/gameplay_gated_routing_report.current.json
```

Expected:

- `ok`: true for contract export, routing plan build, plan validation, and report
- `contract_type`: `gameplay_gated_pipeline_routing_contract`
- `plan_type`: `gameplay_gated_pipeline_routing_plan`
- `report_type`: `gameplay_gated_pipeline_routing_report`
- `routing_mode`: `dry_run`
- downstream jobs executed: false
- generated `.data/exports/` files stay local and untracked

## Point Manifest / Evidence Provenance Contract

Use this when an indexed point needs a durable provenance record for replay/review surfaces,
dataset exports, or regression gates. The manifest describes existing evidence only. It does not
generate event candidates, run marker arbitration, create 3D candidates, create reviews, decide
truth, identify players, determine a winner, score a point, or adjudicate in/out.

Build a point manifest:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-build-point-manifest \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Only `MEDIA_ID` is required. The event candidate, trajectory 3D, and camera geometry IDs narrow
the manifest to known evidence runs when available.

Default generated manifest:

```text
.data/manifests/<point_manifest_id>.json
```

Override the manifest path if needed:

```bash
POINT_MANIFEST_OUTPUT=.data/manifests/sample_point.point_manifest.json
```

Expected:

- `ok`: true
- `status`: `completed`
- `manifest_type`: `point_evidence_provenance_manifest`
- `manifest_version`: `v0`
- `point_manifest_id`: present and deterministic for the supplied IDs
- `replay_url`: present
- `evidence_availability.media_indexed`: true
- `evidence_availability.replay_available`: true
- `profile_counts`: present
- `warnings.manifest_is_not_truth`: true
- `warnings.observation_only`: true
- `warnings.no_adjudication`: true
- `warnings.does_not_create_in_out`: true
- `warnings.does_not_create_score`: true
- `warnings.does_not_identify_players`: true
- `warnings.does_not_determine_winner`: true
- `warnings.not_generalization_claim`: true

Generated `.data` manifests are local outputs and should not be committed.

## Multi-Point Replay Navigation / Review Surface

Use this after point manifests exist locally. The index discovers valid point manifests and builds a
replay navigation artifact for manifest-backed points. It describes existing manifests only. It
does not generate observations, event candidates, 3D candidates, review lifecycle decisions, truth,
score, player identity, point winner, in/out, or adjudication.

Build the multi-point replay index:

```bash
make tom-v1-build-multi-point-replay-index \
  PYTHON=.venv/bin/python
```

Optional overrides:

```bash
POINT_MANIFEST_ROOT=.data/manifests
MULTI_POINT_REPLAY_INDEX_OUTPUT=.data/manifests/multi_point_replay_index.json
VIEWER_BASE_URL=http://127.0.0.1:3000
```

Default generated index:

```text
.data/manifests/multi_point_replay_index.json
```

Expected:

- `ok`: true
- `status`: `completed`
- `index_type`: `multi_point_replay_index`
- `index_version`: `v0`
- `point_count`: number of valid point manifests discovered
- `points[]`: manifest-backed replay points
- `warnings.navigation_only`: true
- `warnings.manifest_index_is_not_truth`: true
- `warnings.observation_only`: true
- `warnings.no_adjudication`: true

The replay API exposes the same index at:

```text
GET /replay/point-manifests
```

The Replay Workstation keeps existing `/replay/<media_id>` semantics. Point links preserve
`eventCandidateRunId`, `trajectory3dRunId`, and `cameraGeometryId` query parameters when present.

## Multi-Point Regression Matrix / Baseline Expansion

Use this after a Blueprint 24 multi-point replay index exists. The matrix compares
manifest-backed evidence profiles over time. It protects regression contracts only. It does not
generate observations, event candidates, 3D candidates, labels, truth, score, point winner, player
identity, in/out, generalization, or adjudication.

Build a current matrix:

```bash
make tom-v1-build-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
```

Optional baseline build:

```bash
MULTI_POINT_REGRESSION_MATRIX_OUTPUT=.data/baselines/multi_point_regression_matrix.baseline.json \
make tom-v1-build-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
```

Verify current matrix against the frozen baseline:

```bash
make tom-v1-verify-multi-point-regression-matrix \
  PYTHON=.venv/bin/python
```

Default paths:

```text
.data/baselines/multi_point_regression_matrix.baseline.json
.data/exports/multi_point_regression_matrix.current.json
.data/exports/multi_point_regression_matrix.regression.json
.data/exports/multi_point_regression_matrix.regression.md
```

Expected:

- `ok`: true when no breaking drift is detected
- `status`: `completed`, `completed_with_drift`, or `failed_regression`
- `matrix_type`: `multi_point_evidence_regression_matrix`
- `matrix_version`: `v0`
- `warnings.matrix_is_not_truth`: true
- `warnings.baseline_is_not_truth`: true
- `warnings.regression_report_only`: true
- `warnings.no_adjudication`: true

Additional manifest-backed points are additive and non-breaking unless strict mode is enabled.
Protected sample-point regressions and matrix contract failures are breaking. Drift is a local
artifact difference only; it is not proof of correctness or tennis truth.

## Observation Quality Taxonomy / Profile

Use this after a Blueprint 24 multi-point replay index exists. The taxonomy defines neutral
review-support quality dimensions. The profile reads the replay index and marks what is known,
unknown, unavailable, or needs human review from existing artifacts only. It does not inspect video,
generate observations, create event candidates, create 3D candidates, decide in/out, score, identify
players, determine a winner, or adjudicate evidence.

Export the taxonomy contract:

```bash
make tom-v1-export-observation-quality-taxonomy \
  PYTHON=.venv/bin/python
```

Build a current profile:

```bash
make tom-v1-build-observation-quality-profile \
  PYTHON=.venv/bin/python
```

Default paths:

```text
.data/contracts/observation_quality_taxonomy_v1.json
.data/exports/observation_quality_profile.current.json
```

Expected:

- `ok`: true
- `taxonomy_type`: `observation_quality_taxonomy`
- `taxonomy_version`: `v1`
- `profile_type`: `observation_quality_profile`
- `profile_version`: `v1`
- `warnings.taxonomy_is_not_truth`: true
- `warnings.observation_quality_is_not_adjudication`: true
- `warnings.no_adjudication`: true

Visual quality dimensions default to `unknown` when media/replay context exists because the profile
does not inspect video content. Missing evidence is `unavailable`. `requires_human_review` marks
dimensions that cannot be determined from the existing provenance artifacts.

## Structured Review Label Schema

Use this to export the human-review label schema, create a blank label bundle template, and validate
bundle structure. This is label-structure support only. It does not create labels automatically,
judge correctness, decide in/out, score, identify players, determine a winner, or adjudicate
evidence.

Export the schema contract:

```bash
make tom-v1-export-review-label-schema \
  PYTHON=.venv/bin/python
```

Build a blank template:

```bash
make tom-v1-build-review-label-template \
  PYTHON=.venv/bin/python
```

Validate a bundle:

```bash
make tom-v1-validate-review-label-bundle \
  PYTHON=.venv/bin/python \
  REVIEW_LABEL_BUNDLE=.data/exports/review_label_template.current.json
```

Default paths:

```text
.data/contracts/review_label_schema_v1.json
.data/exports/review_label_template.current.json
.data/exports/review_label_bundle.validation.json
```

Expected:

- `ok`: true for schema export and valid bundle validation
- `schema_type`: `structured_review_label_schema`
- `schema_version`: `v1`
- `label_bundle_type`: `structured_review_label_bundle`
- `label_bundle_version`: `v1`
- `warnings.label_is_not_truth`: true
- `warnings.human_review_only`: true
- `warnings.no_adjudication`: true

Validation checks shape, label keys, allowed values, forbidden fields, and human-only flags. It does
not infer missing labels, create labels, validate correctness, or decide truth.

## Reviewer Confidence / Ambiguity Capture

Use this to export the human-review confidence and ambiguity metadata schema, create a blank
confidence bundle template, and validate bundle structure. This is review metadata support only. It
does not score confidence automatically, infer truth, judge correctness, decide in/out, score,
identify players, determine a winner, or adjudicate evidence.

Export the schema contract:

```bash
make tom-v1-export-reviewer-confidence-schema \
  PYTHON=.venv/bin/python
```

Build a blank template:

```bash
make tom-v1-build-reviewer-confidence-template \
  PYTHON=.venv/bin/python
```

Validate a bundle:

```bash
make tom-v1-validate-reviewer-confidence-bundle \
  PYTHON=.venv/bin/python \
  REVIEWER_CONFIDENCE_BUNDLE=.data/exports/reviewer_confidence_ambiguity_template.current.json
```

Run the post-Codex validation helper:

```bash
make tom-v1-post-codex-validate \
  PYTHON=.venv/bin/python \
  EXPECTED_BRANCH=codex/blueprint-28-reviewer-confidence-ambiguity-capture-v1
```

Default paths:

```text
.data/contracts/reviewer_confidence_ambiguity_schema_v1.json
.data/exports/reviewer_confidence_ambiguity_template.current.json
.data/exports/reviewer_confidence_ambiguity.validation.json
.data/tmp/post_codex_validate/
```

Expected:

- `ok`: true for schema export and valid bundle validation
- `schema_type`: `reviewer_confidence_ambiguity_schema`
- `schema_version`: `v1`
- `confidence_bundle_type`: `reviewer_confidence_ambiguity_bundle`
- `confidence_bundle_version`: `v1`
- `warnings.confidence_is_not_truth`: true
- `warnings.ambiguity_is_not_truth`: true
- `warnings.human_review_only`: true
- `warnings.no_adjudication`: true

Validation checks shape, allowed metadata values, optional Blueprint 27 label keys, forbidden
fields, and human-only flags. It does not infer missing confidence or ambiguity, create labels,
validate correctness, decide whether confidence is appropriate, or decide truth.

## Multi-Reviewer / Disagreement Foundation

Use this to export the multi-reviewer disagreement schema, create a blank review-set template,
validate review-set structure, and build a structural disagreement report. This is review structure
support only. It does not rank reviewers, score reviewer quality, resolve disagreement, infer truth,
decide in/out, score, identify players, determine a winner, or adjudicate evidence.

Export the schema contract:

```bash
make tom-v1-export-multi-reviewer-disagreement-schema \
  PYTHON=.venv/bin/python
```

Build a blank review-set template:

```bash
make tom-v1-build-multi-reviewer-review-set-template \
  PYTHON=.venv/bin/python
```

Validate a review set:

```bash
make tom-v1-validate-multi-reviewer-review-set \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
```

Build a disagreement report:

```bash
make tom-v1-build-reviewer-disagreement-report \
  PYTHON=.venv/bin/python \
  MULTI_REVIEWER_REVIEW_SET=.data/exports/multi_reviewer_review_set_template.current.json
```

Default paths:

```text
.data/contracts/multi_reviewer_disagreement_schema_v1.json
.data/exports/multi_reviewer_review_set_template.current.json
.data/exports/multi_reviewer_review_set.validation.json
.data/exports/reviewer_disagreement_report.current.json
```

Expected:

- `ok`: true for schema export and valid review-set validation
- `schema_type`: `multi_reviewer_disagreement_schema`
- `schema_version`: `v1`
- `review_set_type`: `multi_reviewer_review_set`
- `review_set_version`: `v1`
- `disagreement_report_type`: `reviewer_disagreement_report`
- `disagreement_report_version`: `v1`
- `warnings.disagreement_is_not_truth`: true
- `warnings.does_not_resolve_disagreement`: true
- `warnings.does_not_score_reviewers`: true
- `warnings.no_adjudication`: true

Validation checks shape, reviewer IDs, forbidden fields, disallowed reviewer identity fields,
human-only flags, and referenced Blueprint 27/28 bundle structure when paths are present. It does
not infer missing labels, create labels, decide whether a reviewer is right, resolve disagreement,
or score reviewers.

## INTENNSE Label Alignment Contract

Use this to export the INTENNSE label alignment contract, create a blank alignment bundle template,
validate alignment bundle structure, and build a structural alignment report. This is a provenance
bridge foundation only. It does not import INTENNSE labels, create TOM labels, infer expert
interpretation, judge correctness, resolve disagreement, decide truth, decide in/out, score,
identify players, determine a winner, produce coaching or tactical conclusions, or adjudicate
evidence.

Export the contract:

```bash
make tom-v1-export-intennse-label-alignment-contract \
  PYTHON=.venv/bin/python
```

Build a blank alignment template:

```bash
make tom-v1-build-intennse-alignment-template \
  PYTHON=.venv/bin/python
```

Validate an alignment bundle:

```bash
make tom-v1-validate-intennse-alignment-bundle \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
```

Build an alignment report:

```bash
make tom-v1-build-intennse-alignment-report \
  PYTHON=.venv/bin/python \
  INTENNSE_ALIGNMENT_BUNDLE=.data/exports/intennse_alignment_template.current.json
```

Default paths:

```text
.data/contracts/intennse_label_alignment_contract_v1.json
.data/exports/intennse_alignment_template.current.json
.data/exports/intennse_alignment_bundle.validation.json
.data/exports/intennse_alignment_report.current.json
```

Expected:

- `ok`: true for contract export and valid alignment bundle validation
- `contract_type`: `intennse_label_alignment_contract`
- `contract_version`: `v1`
- `alignment_bundle_type`: `intennse_label_alignment_bundle`
- `alignment_bundle_version`: `v1`
- `alignment_report_type`: `intennse_label_alignment_report`
- `alignment_report_version`: `v1`
- `warnings.alignment_is_not_truth`: true
- `warnings.does_not_import_intennse_truth`: true
- `warnings.does_not_create_intennse_labels`: true
- `warnings.does_not_resolve_disagreement`: true
- `warnings.no_adjudication`: true

Validation checks contract shape, TOM contract references, allowed alignment entities, allowed
values, forbidden fields, and human-only flags. INTENNSE refs are external placeholders in v1.
Missing TOM or INTENNSE refs are reported as structural/provenance context only.

## Versioned Dataset Corpus

Use this to export the dataset corpus contract, package existing point manifests/replay-index rows
and regression-matrix rows into corpus entries, validate corpus structure, and build a structural
corpus report. This is a dataset-corpus foundation only. It does not create training truth,
automatic labels, correctness claims, in/out, score, player identity, point winner, reviewer
ranking, reviewer scoring, disagreement resolution, INTENNSE conclusions, coaching/tactical
conclusions, or adjudication.

Export the contract:

```bash
make tom-v1-export-versioned-dataset-corpus-contract \
  PYTHON=.venv/bin/python
```

Build the corpus manifest:

```bash
make tom-v1-build-versioned-dataset-corpus-manifest \
  PYTHON=.venv/bin/python
```

Validate a corpus manifest:

```bash
make tom-v1-validate-versioned-dataset-corpus-manifest \
  PYTHON=.venv/bin/python \
  DATASET_CORPUS_MANIFEST=.data/exports/versioned_dataset_corpus_manifest.current.json
```

Build a structural corpus report:

```bash
make tom-v1-build-versioned-dataset-corpus-report \
  PYTHON=.venv/bin/python \
  DATASET_CORPUS_MANIFEST=.data/exports/versioned_dataset_corpus_manifest.current.json
```

Default paths:

```text
.data/contracts/versioned_dataset_corpus_contract_v1.json
.data/exports/versioned_dataset_corpus_manifest.current.json
.data/exports/versioned_dataset_corpus_manifest.validation.json
.data/exports/versioned_dataset_corpus_report.current.json
```

Expected:

- `ok`: true for contract export and valid corpus manifest validation
- `contract_type`: `versioned_dataset_corpus_contract`
- `contract_version`: `v1`
- `corpus_manifest_type`: `versioned_dataset_corpus_manifest`
- `corpus_manifest_version`: `v1`
- `corpus_report_type`: `versioned_dataset_corpus_report`
- `corpus_report_version`: `v1`
- `warnings.dataset_corpus_is_not_truth`: true
- `warnings.dataset_corpus_is_not_training_truth`: true
- `warnings.does_not_create_labels`: true
- `warnings.does_not_resolve_disagreement`: true
- `warnings.no_adjudication`: true

Validation checks contract shape, included contract refs, referenced Blueprint 26 through 30
contract versions when paths are available, source index/matrix paths, required corpus entry
fields, allowed split/status values, and forbidden fields. Missing optional review,
observation-quality, disagreement, INTENNSE, and dataset-export refs are provenance gaps only.

## Coverage-Driven Sampling Strategy

Use this to export the coverage sampling strategy contract, build a structural coverage profile
from the versioned dataset corpus, validate profile structure, and build a structural coverage
report. This is planning/provenance infrastructure only. It does not execute sampling, ingest
media, create observations, create labels, create training truth, score correctness, claim
generalization, resolve disagreement, produce tennis conclusions, or adjudicate evidence.

Export the contract:

```bash
make tom-v1-export-coverage-sampling-strategy-contract \
  PYTHON=.venv/bin/python
```

Build the coverage sampling profile:

```bash
make tom-v1-build-coverage-sampling-profile \
  PYTHON=.venv/bin/python
```

Validate a coverage sampling profile:

```bash
make tom-v1-validate-coverage-sampling-profile \
  PYTHON=.venv/bin/python \
  COVERAGE_SAMPLING_PROFILE=.data/exports/coverage_sampling_profile.current.json
```

Build a structural coverage sampling report:

```bash
make tom-v1-build-coverage-sampling-report \
  PYTHON=.venv/bin/python \
  COVERAGE_SAMPLING_PROFILE=.data/exports/coverage_sampling_profile.current.json
```

Default paths:

```text
.data/contracts/coverage_sampling_strategy_contract_v1.json
.data/exports/coverage_sampling_profile.current.json
.data/exports/coverage_sampling_profile.validation.json
.data/exports/coverage_sampling_report.current.json
```

Expected:

- `ok`: true for contract export and valid coverage sampling profile validation
- `contract_type`: `coverage_sampling_strategy_contract`
- `contract_version`: `v1`
- `profile_type`: `coverage_sampling_profile`
- `profile_version`: `v1`
- `report_type`: `coverage_sampling_report`
- `report_version`: `v1`
- `warnings.coverage_sampling_is_not_truth`: true
- `warnings.coverage_sampling_is_not_training_truth`: true
- `warnings.does_not_execute_sampling`: true
- `warnings.does_not_ingest_media`: true
- `warnings.does_not_create_labels`: true
- `warnings.no_adjudication`: true

Validation checks contract shape, profile type/version, referenced Blueprint 26 through 31
contract versions when paths are available, source corpus/index/matrix paths, required candidate
fields, allowed coverage axes, allowed gap types, allowed priority values, allowed next-action
values, and forbidden fields. Missing optional review, observation-quality, disagreement,
INTENNSE, and export refs are coverage gaps only.

## Many-Point Evidence Ingestion Gate

Use this to export the many-point ingestion gate contract, build an explicit local-media manifest
template, validate the manifest, build a dry-run plan, and run the dry-run gate. This is controlled
ingestion infrastructure only. It does not discover media automatically, silently ingest media,
create observations, create event candidates, create 3D candidates, create review labels, create
training truth, score correctness, claim generalization, produce tennis conclusions, or adjudicate
evidence.

Export the contract:

```bash
make tom-v1-export-many-point-ingestion-gate-contract \
  PYTHON=.venv/bin/python
```

Build a manifest template using an explicit local path:

```bash
make tom-v1-build-many-point-ingestion-manifest-template \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MEDIA_PATH=demo_assets/sample_point.mp4
```

Validate the manifest:

```bash
make tom-v1-validate-many-point-ingestion-manifest \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
```

Build the dry-run plan:

```bash
make tom-v1-build-many-point-ingestion-plan \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
```

Run the dry-run gate:

```bash
make tom-v1-run-many-point-ingestion-gate \
  PYTHON=.venv/bin/python \
  MANY_POINT_INGESTION_MANIFEST=.data/exports/many_point_ingestion_manifest.template.json
```

Default paths:

```text
.data/contracts/many_point_ingestion_gate_contract_v1.json
.data/exports/many_point_ingestion_manifest.template.json
.data/exports/many_point_ingestion_manifest.validation.json
.data/exports/many_point_ingestion_plan.current.json
.data/exports/many_point_ingestion_gate.current.json
```

Expected:

- `ok`: true for contract export, manifest validation, plan build, and dry-run gate
- `contract_type`: `many_point_ingestion_gate_contract`
- `contract_version`: `v1`
- `manifest_type`: `many_point_ingestion_manifest`
- `manifest_version`: `v1`
- `ingestion_gate_type`: `many_point_ingestion_gate_report`
- `ingestion_gate_version`: `v1`
- `mode`: `dry_run`
- `indexed_entry_count`: 0 in dry-run mode
- `warnings.ingestion_gate_is_not_truth`: true
- `warnings.does_not_create_event_candidates`: true
- `warnings.does_not_create_3d_candidates`: true
- `warnings.does_not_create_review_labels`: true
- `warnings.does_not_claim_generalization`: true
- `warnings.no_adjudication`: true

Validation checks manifest type/version, source contract refs, local media path presence, file
existence, duplicate path/checksum conflicts, allowed requested actions, expected media type, and
forbidden fields. Demo asset smokes validate gate mechanics only; they do not prove many real
distinct tennis points were ingested.

## Review Operations Metrics / Label Throughput Dashboard

Use this to export the review-ops metrics contract, build a structural operations report, validate
the report, and build read-only dashboard JSON. This is operations visibility only. It does not
create evidence, create review labels, generate confidence scores, rank reviewers, score reviewer
quality, resolve disagreement, infer tennis truth, ingest media, execute sampling, or adjudicate
evidence.

Export the contract:

```bash
make tom-v1-export-review-ops-metrics-contract \
  PYTHON=.venv/bin/python
```

Build the report from current local corpus/coverage/ingestion artifacts:

```bash
make tom-v1-build-review-ops-metrics-report \
  PYTHON=.venv/bin/python
```

Validate the report:

```bash
make tom-v1-validate-review-ops-metrics-report \
  PYTHON=.venv/bin/python \
  REVIEW_OPS_METRICS_REPORT=.data/exports/review_ops_metrics_report.current.json
```

Build dashboard data:

```bash
make tom-v1-build-review-ops-dashboard-data \
  PYTHON=.venv/bin/python \
  REVIEW_OPS_METRICS_REPORT=.data/exports/review_ops_metrics_report.current.json
```

Default paths:

```text
.data/contracts/review_ops_metrics_contract_v1.json
.data/exports/review_ops_metrics_report.current.json
.data/exports/review_ops_metrics_report.validation.json
.data/exports/review_ops_dashboard_data.current.json
```

Expected:

- `ok`: true for contract export, report build, validation, and dashboard-data build
- `contract_type`: `review_ops_metrics_contract`
- `contract_version`: `v1`
- `report_type`: `review_ops_metrics_report`
- `report_version`: `v1`
- `dashboard_data_type`: `review_ops_dashboard_data`
- `dashboard_data_version`: `v1`

## Label Feedback Loop into Evaluation Harness

Use this to export the label-feedback evaluation contract, build structural feedback inputs,
validate them, and build an evaluation report. This is evaluation-routing infrastructure only. It
does not create labels, generate confidence scores, rank reviewers, resolve disagreement, infer
truth, modify baselines, retrain models, ingest media, execute sampling, or adjudicate evidence.

Export the contract:

```bash
make tom-v1-export-label-feedback-evaluation-contract \
  PYTHON=.venv/bin/python
```

Build feedback inputs from current local corpus/review-ops/coverage/regression artifacts:

```bash
make tom-v1-build-label-feedback-evaluation-inputs \
  PYTHON=.venv/bin/python
```

Validate feedback inputs:

```bash
make tom-v1-validate-label-feedback-evaluation-inputs \
  PYTHON=.venv/bin/python \
  LABEL_FEEDBACK_EVALUATION_INPUTS=.data/exports/label_feedback_evaluation_inputs.current.json
```

Build the evaluation report:

```bash
make tom-v1-build-label-feedback-evaluation-report \
  PYTHON=.venv/bin/python \
  LABEL_FEEDBACK_EVALUATION_INPUTS=.data/exports/label_feedback_evaluation_inputs.current.json
```

Default paths:

```text
.data/contracts/label_feedback_evaluation_contract_v1.json
.data/exports/label_feedback_evaluation_inputs.current.json
.data/exports/label_feedback_evaluation_inputs.validation.json
.data/exports/label_feedback_evaluation_report.current.json
```

Expected:

- `ok`: true for contract export, input build, validation, and report build
- `contract_type`: `label_feedback_evaluation_contract`
- `contract_version`: `v1`
- `feedback_inputs_type`: `label_feedback_evaluation_inputs`
- `feedback_inputs_version`: `v1`
- `report_type`: `label_feedback_evaluation_report`
- `report_version`: `v1`
- `dashboard_card_count`: 13
- `warnings.review_ops_metrics_are_not_truth`: true
- `warnings.read_only_dashboard_data`: true
- missing optional review/INTENNSE refs are structural gaps, not correctness findings

Validation checks contract shape, report shape, dashboard-card schema, allowed structural status
values, referenced contract versions, and forbidden fields. It does not infer missing labels,
create labels, judge correctness, rank reviewers, score reviewer quality, resolve disagreement, or
create training truth.

Build the point evidence snapshot:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-point-evidence-snapshot \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb
```

Expected:

- `marker_summary`: 6
- `trajectory_3d_summary`: available
- `event_candidate_3d_diagnostic_summary`: available
- `trajectory_3d_debug_review_summary`: present
- warnings preserve candidate-only, not-truth, and no-adjudication boundaries

Evaluate point candidates:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-evaluate-point-candidates \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb
```

Expected:

- `final_marker_count`: 6
- `hit_candidate`: 3
- `bounce_candidate`: 3
- `trajectory_3d_readiness`: available
- `event_candidate_3d_diagnostics`: available
- reviewed event-marker count remains 1

Export the reviewed 3D debug dataset:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-export-reviewed-3d-debug-dataset \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97 \
  FORMAT=json \
  OUTPUT=.data/exports/reviewed_3d_debug_dataset_sample_point.current.json
```

Expected:

- `event_marker_count`: 6
- `trajectory_3d_candidate_count`: 68
- `event_candidate_3d_diagnostic_count`: 6
- `event_marker_review_count`: 1
- `not_truth`: true
- `not_training_truth`: true

Then run the normal validation suite:

```bash
.venv/bin/python -m pytest -q
ruff check .
git diff --check
cd apps/web
npm run lint
npm run build
npm audit --omit=dev
cd ../..
```

Only proceed to a second point if the baseline gate passes and the validation suite is clean.

## Second Point Ingestion / Replay Smoke

Use this smoke after the `sample_point` expansion readiness gate passes. The second point is a
single additional evidence sample only. It is not a generalization claim, benchmark, truth source,
or event-generation milestone.

Ingest one local second-point video:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_smoke.db \
make tom-v1-ingest-second-point-smoke \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/second_point.mp4
```

Optional generated manifest:

```bash
SECOND_POINT_MANIFEST_OUTPUT=.data/second_point/second_point_smoke_manifest.json
```

Expected:

- `ok`: true
- `status`: `completed`
- `smoke_type`: `second_point_ingestion_evidence_replay_smoke`
- `media_id`: present
- `replay_url`: present
- `not_truth`: true
- `not_generalization_claim`: true
- `does_not_change_sample_point`: true

Missing media path returns `missing_second_point_media_path`. A nonexistent file returns
`second_point_media_path_not_found`.

Open the returned `replay_url`. For Blueprint 21 it is valid if the replay shows only indexed video
playback and no event/3D candidate layers. Missing event candidates, missing 3D candidates, and no
review annotations should not crash replay.

After the smoke, verify `sample_point` remains protected:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

## Second Point Evidence Parity / Protected Baseline Gate

Use this after the second-point ingestion smoke is available and the protected `sample_point`
baseline gate passes. The parity command records media/replay availability and the current evidence
profile for one second-point media asset. It does not generate hit/bounce candidates, marker
arbitration, 3D candidates, 3D diagnostics, truth, in/out, score, or adjudication.

Build a second-point evidence parity manifest:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_parity.db \
make tom-v1-build-second-point-evidence-parity \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/second_point.mp4
```

Default generated manifest:

```text
.data/baselines/second_point_evidence_parity.baseline_manifest.json
```

Override the manifest path if needed:

```bash
SECOND_POINT_BASELINE_MANIFEST_OUTPUT=.data/baselines/my_second_point.baseline_manifest.json
```

Expected:

- `ok`: true
- `status`: `completed`
- `parity_type`: `second_point_evidence_parity_baseline`
- `media_id`: present
- `replay_url`: present
- `second_point_profile.media_indexed`: true
- `second_point_profile.replay_available`: true
- `second_point_profile.baseline_available`: true
- `not_truth`: true
- `not_generalization_claim`: true
- `does_not_change_sample_point`: true

For v0, it is acceptable for `event_candidates_available`,
`trajectory_3d_candidates_available`, and `review_annotations_available` to be false. That means
the second point has media/replay parity only; it is not a failure unless a future command claims
those evidence layers exist.

If no real second-point file is available, validate the negative path:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_second_point_parity.db \
make tom-v1-build-second-point-evidence-parity \
  PYTHON=.venv/bin/python \
  SECOND_POINT_MEDIA_PATH=/absolute/path/to/missing.mp4
```

Expected:

- `ok`: false
- `status`: `second_point_media_path_not_found`

For command validation only, an operator may explicitly pass `demo_assets/sample_point.mp4`. Any
report using that stand-in must state that it is not a real second-point review and not proof of
generalization.

After parity, verify `sample_point` remains protected:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
make tom-v1-verify-reviewed-3d-debug-baseline \
  PYTHON=.venv/bin/python \
  MEDIA_ID=9518fb01-0da1-4344-9a84-ff88ec8e9b1e \
  EVENT_CANDIDATE_RUN_ID=1b946366-7ec1-426f-8b40-494535a9b3fb \
  TRAJECTORY_3D_RUN_ID=ea76ccab-c51d-4a63-9682-9fd0bbb83f14 \
  CAMERA_GEOMETRY_ID=5afa67fb-7f6e-41eb-b4aa-b1100a97ee97
```

Expected:

- `ok`: true
- `status`: `completed`
- `drift_detected`: false
- `breaking_drift_detected`: false
- `baseline_is_not_truth`: true
