# Milestone 7F - Perception Run Orchestration and Completion Review

## Status

Complete.

## Goal

Close Blueprint 7 by consolidating the real perception run sequence, documenting the final local orchestration path, marking Blueprint 7 complete, and preserving the Blueprint 8 boundary for court/camera/homography evidence.

## Final Orchestration Sequence

Fixture-safe baseline:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3

TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
make completion-audit PYTHON=.venv/bin/python
```

Optional real detection:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<detection_model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Optional candidate tracklets from real detections:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_blueprint_7_demo.db \
.venv/bin/python -m apps.worker.cli build-tracklets \
  --detection-run-id <real_detection_run_id> \
  --run-name real-detection-tracklet-candidates
```

Optional real pose:

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

Replay URL with all available real perception runs:

```text
/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>&poseRunId=<real_pose_run_id>
```

## What Changed

- Added Blueprint 7 completion review.
- Added Milestone 7F closeout documentation.
- Updated canonical docs to mark Blueprint 7 COMPLETE.
- Consolidated the final real perception run ladder.
- Documented optional runtime smoke policy.
- Reaffirmed that court/camera/homography belongs in Blueprint 8.

## Boundary

7F adds no runtime behavior, API behavior, database schema, frontend feature, court/homography implementation, event interpretation, stream ingestion, or adjudication.

Blueprint 7 is closed.
