# Milestone 7A - Real YOLO Detection Replay Run

Status: COMPLETE

## Summary

Milestone 7A starts Blueprint 7 by adding a real YOLO detection replay command for indexed media. The command validates optional YOLO runtime/weights, registers model metadata, samples media-owned frames, persists mapped real model outputs as atomic `ball_detection` and `player_detection` observations, and prints a replay URL using the real detection run id.

## Proof Path

```text
indexed media
-> optional YOLO runtime/weights validation
-> explicit class mapping
-> media-owned frame sampling
-> YOLO frame inference
-> atomic detection observation persistence
-> replay URL with detectionRunId
-> Blueprint 6 replay overlays
```

## Commands

Plan:

```bash
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
  --plan-only
```

Run:

```bash
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Makefile helper:

```bash
make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=./model_assets/yolo/<model>.pt PYTHON=.venv/bin/python
```

## What Was Added

- `apps.worker.services.real_detection_replay`
- worker CLI `run-real-detection`
- Makefile `real-detection`
- frame start/end support in shared YOLO frame sampling
- `real_model_output` and `model_output_not_truth` payload flags for YOLO-origin detections
- fake-runtime tests that persist real-run-labeled atomic observations without YOLO weights
- Blueprint 7 and real detection replay docs

## What Was Not Added

- no tracklet generation from real detections
- no real pose inference
- no court/homography implementation
- no stream ingestion
- no tennis-event interpretation
- no official tennis results or adjudication
