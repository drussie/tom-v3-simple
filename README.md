# TOM v3 Simple

TOM v3 Simple is a local observation/evidence platform for tennis video work.

It indexes media, persists model or fixture outputs as observations, preserves lineage, displays evidence in a viewer, supports review annotations, exports review datasets, and audits local demo provenance.

It is not TOM v2, and it does not decide official tennis meaning.

## Status

TOM v3 Simple Status: COMPLETE

TOM v3 Simple is complete as a lightweight local observation/evidence platform. It can index local tennis video, run fixture gameplay/detection/pose paths, optionally run YOLO detection smoke when local runtime and weights exist, persist observations and typed evidence rows, build candidate tracklets, preserve lineage/provenance, render detection/tracklet/pose evidence in the viewer, seed and display review annotations, export TOM-native review datasets, and run a structural completion audit.

It remains intentionally non-decisive about tennis meaning. It does not include real pose inference, movement interpretation, stroke classification, homography, bounce/hit/rally/point/scoring, production deployment, auth, real stream ingestion, or TOM v2-style adjudication.

Blueprint 6 Status: COMPLETE

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Future real live ingestion and future tennis intelligence must begin as new blueprints.

Blueprint 7 Status: IN PROGRESS

Blueprint 7 starts TOM v3's real perception runtime for the replay workstation. Milestones 7A and 7B add a real YOLO detection replay run that samples indexed media frames, persists mapped real model output as atomic `ball_detection` and `player_detection` observations, and labels those real detection runs clearly in the replay workstation with source/runtime/model/config context.

Blueprint 7 remains observation-only. Real model output is evidence, not confirmed tennis state.

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
- Keep optional YOLO runtime separate from the default base environment.

## What It Does Not Do

- No scoring, point reconstruction, rally segmentation, hit detection, or bounce detection.
- No stroke classification, movement interpretation, or biomechanics conclusions.
- No homography or court-space reasoning.
- No real pose inference in TOM v3 Simple.
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
- [Completion Checklist](docs/COMPLETION_CHECKLIST.md)
- [Final Completion Review](docs/blueprints/tom_v3_simple_final_completion_review.md)
- [Blueprint 6 Completion Review](docs/blueprints/tom_v3_blueprint_6_completion_review.md)
- [Blueprint 7 - Real Perception Runtime](docs/blueprints/tom_v3_blueprint_7_real_perception_runtime_for_replay_workstation.md)
- [Control Room Index](docs/CONTROL_ROOM_INDEX.md)

## Current State

Blueprints 1, 2, 3, 4, 5, and 6 are complete. TOM v3 Simple is complete as a lightweight local platform, Blueprint 6 is complete as the visual replay/operator workstation layer, and Blueprint 7 is in progress with real YOLO detection replay and replay-workstation source validation.

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
-> replay workstation detection overlays
```

Future real tracklets, real pose, real live ingestion, and new tennis-intelligence work should start as separate blueprints.
