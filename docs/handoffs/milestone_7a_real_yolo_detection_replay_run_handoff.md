# Milestone 7A Handoff - Real YOLO Detection Replay Run

## Status

Milestone 7A is complete.

Blueprint 7 has started with a narrow real YOLO detection replay path.

## Implemented

- `run-real-detection` worker CLI
- `make real-detection`
- real detection replay service with plan mode
- runtime probe and weights validation reuse
- model registry reuse
- explicit YOLO class mapping, including shorthand JSON support
- media-owned frame sampling with optional start/end bounds
- real YOLO output persistence as atomic detection observations
- replay URL output with `detectionRunId`
- tests using fake YOLO frame output, no runtime/weights required

## Run

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_real_perception.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
```

Then:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_real_perception.db \
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Open the printed replay URL.

## Boundaries

The real detection run persists model output as observation evidence only. It does not create confirmed balls, confirmed players, tracklets, pose, homography, events, scoring, or adjudication.

## Recommended Next Handoff

Milestone 7B - Real Detection Overlay Validation in Replay Workstation.
