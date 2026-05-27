# TOM v3 Simple

TOM v3 Simple is a local observation/evidence platform for tennis video work.

It indexes media, persists model or fixture outputs as observations, preserves lineage, displays evidence in a viewer, supports review annotations, exports review datasets, and audits local demo provenance.

It is not TOM v2, and it does not decide official tennis meaning.

## Status

TOM v3 Simple Status: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. It can index local tennis video, run fixture gameplay/detection/pose paths, optionally run YOLO detection smoke when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render detection/tracklet/pose evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit.

The completed TOM v3 Simple baseline remains intentionally non-decisive about tennis meaning. The fixture path does not require real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, real stream ingestion, or TOM v2-style adjudication.

Blueprint 6 Status: COMPLETE

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Future real live ingestion and future tennis intelligence must begin as new blueprints.

Blueprint 7 Status: COMPLETE

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. TOM can now run optional real YOLO detection on indexed media, persist real ball/player detection observations, label and inspect real model-output detection evidence in replay, build candidate tracklets from real detection observations with lineage back to source detections, run optional real pose inference, persist COCO17 player pose observations, link pose evidence back to source player detections, and render detection, tracklet, and pose evidence in the replay workstation.

Blueprint 7 remains observation-only and non-adjudicative. It does not add court/homography implementation, bounce/hit/rally/point/scoring, movement/stroke interpretation, player identity conclusions, real stream ingestion, or TOM v2-style adjudication.

Court/camera/homography evidence now proceeds in Blueprint 8.

Blueprint 8 Status: IN PROGRESS

Blueprint 8 starts TOM v3's court/camera/homography evidence layer. Milestone 8A adds the schema and persistence contract for court keypoints, court lines, camera/view evidence, homography candidates, projection diagnostics, and a normalized court template registry. Milestone 8B adds a deterministic fixture court evidence adapter that writes court keypoint, court line, and camera/view observations with model/runtime/run provenance. Milestone 8C makes camera/view observations queryable and inspectable as geometry context evidence through summary and evidence-bundle read models. Milestone 8D persists homography candidate observations from court keypoint, court line, and camera/view source evidence with lineage.

8D is still geometry evidence only. Homography rows are candidates, not court truth. 8D does not add projection diagnostics, replay court overlays, real court model inference, ball/player court-space projection, bounce/hit/in-out/rally/point/scoring, real stream ingestion, or adjudication.

## What It Does

- Index local video media with frame/time metadata.
- Persist gameplay, detection, tracklet candidate, track point candidate, and pose observations.
- Preserve source relationships through observation lineage.
- Store frame images, debug files, and review exports as evidence artifacts.
- Show detections, tracklets, pose keypoints, lineage, artifacts, annotations, and exports in the local viewer.
- Export TOM-native pose and tracklet review datasets.
- Run a structural provenance audit for the fixture demo.
- Open indexed video in a replay/operator workstation with synchronized evidence overlays and timeline lanes.
- Run an optional real YOLO detection replay pass on indexed media when local runtime and weights exist.
- Distinguish fixture detection evidence from real model-output detection evidence in replay run selectors and selected detection detail.
- Build candidate tracklets from real model-output detection runs while preserving source detection lineage.
- Run an optional real pose replay pass on indexed media when local runtime and pose weights exist.
- Persist real `player_pose_observation` rows with COCO17 keypoints and source player detection lineage when available.
- Persist fixture court keypoint, court line, and camera/view observations for Blueprint 8 geometry evidence development.
- Query and inspect camera/view observations as geometry context evidence.
- Build homography candidate observations from persisted court evidence while preserving source lineage.
- Keep optional YOLO and pose runtimes separate from the default base environment.

## What It Does Not Do

- No scoring, point reconstruction, rally segmentation, hit detection, or bounce detection.
- No stroke classification, movement interpretation, or biomechanics conclusions.
- No confirmed homography, court truth, or court-space reasoning.
- No real court/camera model, projection diagnostics, replay court overlay, or ball/player court-space projection in Blueprint 8D.
- No movement interpretation from pose keypoints.
- No production deployment, auth, cloud workflow, real live stream ingestion, or multi-camera support.

Fixture output proves persistence, lineage, viewer, review, export, and audit plumbing. It is demo evidence only.

## Quickstart

Install Python dependencies:

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

Set a local database URL and run migrations:

```bash
export TOM_V3_DATABASE_URL="sqlite+pysqlite:///./tmp_tom_v3.db"
alembic upgrade head
```

Run the canonical fixture demo:

```bash
make demo
```

If your shell is not already using the TOM v3 Python environment:

```bash
make demo PYTHON=.venv/bin/python
```

Audit the demo:

```bash
make completion-audit
```

Run the local validation checklist:

```bash
make completion-check
```

## Open The Viewer

Start the API:

```bash
uvicorn apps.api.main:app --reload
```

Start the web app:

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open the viewer URLs printed by `make demo`:

```text
http://127.0.0.1:3000/runs/<run_id>
```

You can also print a helper URL:

```bash
make demo-open RUN_ID=<run_id>
```

## Optional YOLO

The default fixture demo does not require YOLO weights, Ultralytics, Torch, OpenCV, GPU runtime, or network access.

Probe the optional YOLO path:

```bash
make yolo-probe
```

Preview the optional local YOLO smoke path:

```bash
make yolo-smoke
```

Run a real detection replay pass after indexing media:

```bash
make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=./model_assets/yolo/<model>.pt PYTHON=.venv/bin/python
```

Real YOLO smoke requires a separate optional runtime environment, local weights outside git, and model registration. See [OPTIONAL_YOLO.md](docs/OPTIONAL_YOLO.md).

When a real detection run is selected in the replay workstation, the UI labels it as real model-output evidence and shows available source runtime, model registry, runtime config, class, frame/time owner, and evidence-only metadata. Fixture runs remain labeled as fixture/demo evidence.

Build candidate tracklets from a real detection run:

```bash
make build-tracklets DETECTION_RUN_ID=<real_detection_run_id> RUN_NAME=real-detection-tracklet-candidates PYTHON=.venv/bin/python
```

The output includes a replay URL with `detectionRunId` and `trackletRunId`. Tracklets remain candidate temporal groupings, not object identity or path conclusions.

Run a real pose replay pass after indexing media and, preferably, after a real detection run:

```bash
make real-pose \
  MEDIA_ID=<media_id> \
  SOURCE_DETECTION_RUN_ID=<real_detection_run_id> \
  POSE_WEIGHTS_PATH=./model_assets/pose/<pose_model>.pt \
  PYTHON=.venv/bin/python
```

Real pose output persists `player_pose_observation` keypoint evidence and can be opened with `poseRunId`. It does not interpret movement, strokes, biomechanics, court position, or tennis events.

## Important Docs

- [Local Runbook](docs/RUNBOOK_LOCAL.md)
- [Control Room](docs/CONTROL_ROOM.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Observation Contract](docs/OBSERVATION_CONTRACT.md)
- [Blueprint Status](docs/BLUEPRINT_STATUS.md)
- [Known Limitations](docs/KNOWN_LIMITATIONS.md)
- [Optional YOLO](docs/OPTIONAL_YOLO.md)
- [Exports](docs/EXPORTS.md)
- [Provenance Audit](docs/PROVENANCE_AUDIT.md)
- [Replay Workstation](docs/REPLAY_WORKSTATION.md)
- [Real Detection Replay](docs/perception/real_detection_replay_v0.md)
- [Real Pose Replay](docs/perception/real_pose_replay_v0.md)
- [Court / Homography Decision](docs/court/court_homography_evidence_decision_v0.md)
- [Court Evidence Schema](docs/court/court_evidence_schema_v0.md)
- [Court Template Registry](docs/court/court_template_registry_v0.md)
- [Camera / View Evidence Layer](docs/court/camera_view_evidence_layer_v0.md)
- [Homography Candidate Persistence](docs/court/homography_candidate_persistence_v0.md)
- [Completion Checklist](docs/COMPLETION_CHECKLIST.md)
- [Final Completion Review](docs/blueprints/tom_v3_simple_final_completion_review.md)
- [Blueprint 6 Completion Review](docs/blueprints/tom_v3_blueprint_6_completion_review.md)
- [Blueprint 7 - Real Perception Runtime](docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md)
- [Blueprint 7 Completion Review](docs/blueprints/tom_v3_blueprint_7_completion_review.md)
- [Blueprint 8 - Court / Camera / Homography Evidence](docs/blueprints/tom_v3_blueprint_8_court_camera_homography_evidence_layer_candidate.md)
- [Control Room Index](docs/CONTROL_ROOM_INDEX.md)

## Current State

Blueprints 1, 2, 3, 4, 5, 6, and 7 are complete. TOM v3 Simple is complete as a lightweight local platform, Blueprint 6 is complete as the visual replay/operator workstation layer, Blueprint 7 is complete as the real perception runtime layer for optional real detection, real-detection-derived candidate tracklets, and optional real pose replay, and Blueprint 8 is in progress with court/camera/homography schema contracts, fixture court evidence, camera/view evidence query/bundle read models, and homography candidate persistence.

Current TOM v3 Simple path:

```text
media
-> fixture gameplay observations
-> fixture detections
-> frame artifacts
-> candidate tracklets
-> fixture pose observations
-> review annotations
-> TOM-native exports
-> viewer URLs
-> provenance audit
```

Replay workstation foundation:

```text
indexed media
-> /media/<media_id>/replay-info
-> /media/<media_id>/video
-> /replay/<media_id>
-> current timestamp/frame display
-> persisted detection observation overlays
-> persisted tracklet candidate overlays
-> persisted pose keypoint evidence overlays
-> evidence timeline lanes and click-to-seek scrubber
-> Stream Proxy Mode for video-as-live review
```

Open a replay URL after running the demo:

```bash
make replay-open MEDIA_ID=<media_id>
```

Open overlay playback with:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<pose_run_id>
```

Open Stream Proxy Mode with:

```text
http://127.0.0.1:3000/replay/<media_id>?mode=stream_proxy&detectionRunId=<detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<pose_run_id>
```

Replay overlays and timeline lanes render persisted evidence only: detection observations, tracklet candidates, pose keypoint evidence, and review annotation markers. Stream Proxy Mode hides future evidence until playback reaches it. Real live stream ingestion and tennis-event interpretation remain future work.

Real detection replay path:

```text
indexed media
-> optional YOLO runtime and local weights
-> run-real-detection
-> real model-output ball/player detection observations
-> optional candidate tracklets from real detections
-> optional real pose keypoint observations
-> replay workstation evidence overlays
```

Court/camera/homography evidence now has an 8A schema/persistence foundation, an 8B fixture court evidence adapter, 8C camera/view query, summary, and bundle read models, and 8D homography candidate persistence with source evidence lineage. Real court inference, projection diagnostics, replay overlays, and ball/player court projections are future Blueprint 8 work. Future real live ingestion, movement/stroke evidence, and new tennis-intelligence work should start as separate blueprints.
