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
- future TOM v1-specific adapter required: `keypoints_model.pth`, `view_classifier_gameplay.pt`

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
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.10
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
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25
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
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25
```

Makefile helpers:

```bash
make tom-v1-yolo-probe PYTHON=.venv/bin/python
make tom-v1-ball-detection MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-player-detection MEDIA_ID=<media_id> PYTHON=.venv/bin/python MAX_FRAMES=214
make tom-v1-tracklets DETECTION_RUN_ID=<real_detection_run_id> PYTHON=.venv/bin/python
make tom-v1-pose MEDIA_ID=<media_id> SOURCE_DETECTION_RUN_ID=<player_real_detection_run_id> PYTHON=.venv/bin/python MAX_FRAMES=214
```

Class mapping warning:

The TOM v1 ball model may emit `class 0 = ball`. If real detection returns zero useful detections, lower the confidence threshold, inspect debug payloads/artifacts if available, check class names emitted by Ultralytics, and add an explicit class map only when the model output proves the mapping. Do not relabel unknown classes without evidence.

TOM v1-origin detections and poses are still model-output observations. They do not confirm ball path, player identity, court position, bounce/hit/in-out/rally/point/scoring, or official tennis truth.

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

Blueprint 8 has started. Milestone 8A is schema/contract only.

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
- Homography candidates and projection diagnostics are geometry evidence only, not final court models.
- No ball/player court-space projection, bounce, hit, rally, point, score, or adjudication is produced.
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
