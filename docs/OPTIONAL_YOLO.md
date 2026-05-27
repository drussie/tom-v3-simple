# Optional YOLO Runtime

YOLO is optional in TOM v3 Simple.

The default fixture demo does not require Ultralytics, Torch, OpenCV, YOLO weights, GPU runtime, or network access.

## Base Environment

The base `tom_v3` environment remains lightweight. It can run:

```bash
make demo
make completion-audit
pytest -q
```

without YOLO packages.

## Runtime Probe

Probe optional dependencies:

```bash
make yolo-probe
```

Equivalent:

```bash
python -m apps.worker.cli yolo-runtime-probe --device auto
python -m apps.worker.cli yolo-runtime-probe --device cpu
```

The probe reports package availability and resolved device information. Missing optional packages should produce clear diagnostics.

## Optional Environment

Recommended optional setup:

```bash
conda create -n tom_v3_yolo python=3.11 -y
conda activate tom_v3_yolo
python -m pip install --upgrade pip
pip install -e ".[dev]"
pip install -r requirements-yolo.txt
```

## Weights Policy

Model weights are local assets, not source code.

The repo ignores local weight/runtime paths such as:

```text
model_assets/
weights/
*.pt
*.pth
*.onnx
*.engine
```

Do not commit YOLO weights unless the project explicitly changes that policy.

## Register Weights

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<model>.pt \
  --model-name local-yolo-smoke \
  --model-version local-v0 \
  --device cpu
```

Registration validates the local path, records sha256/file size, validates class mapping, and creates or reuses a `model_registry` row. It does not create observations.

## Smoke Path

Preview the smoke path:

```bash
make yolo-smoke
```

Run it when runtime, weights, and media are present:

```bash
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

YOLO smoke remains separate from `make demo`.

## Real Detection Replay

Milestone 7A adds a replay-oriented real detection command:

```bash
python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights model_assets/yolo/<model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Makefile helper:

```bash
make real-detection MEDIA_ID=<media_id> YOLO_WEIGHTS_PATH=model_assets/yolo/<model>.pt
```

This command validates optional runtime and weights, registers model metadata, samples indexed media frames, persists mapped `ball_detection` / `player_detection` observations, and prints a replay URL with `detectionRunId`.

It does not fall back to fixture detections.

The replay workstation labels these runs as real model-output evidence when source metadata is available. Selected detection detail can show source runtime, model registry id, runtime config id, class id/label, and media-owned frame/time context. Fixture detection runs remain labeled as fixture/demo evidence.

## Blueprint 7 Completion Path

Blueprint 7 is complete. Optional YOLO detection is the first step in the real perception replay ladder:

```text
run-real-detection
-> real detection observations
-> optional real-detection-derived candidate tracklets
-> optional real pose keypoint evidence
-> replay workstation overlays
```

`run-real-detection` requires local YOLO runtime and weights. `run-real-pose` requires local pose runtime and weights. The default fixture demo, default CI, and completion audit do not require either set of weights.

Court/camera/homography evidence is not part of Blueprint 7 and is deferred to Blueprint 8.

## Common Failure Modes

- Ultralytics missing.
- Torch missing.
- OpenCV missing.
- Requested device unavailable.
- Weights path missing or outside allowed roots.
- Checksum mismatch.
- Model load failure.
- Prediction failure.
- Media path missing.

Failures should be clear and should not fall back to fixture detections.

## What YOLO Detections Mean

A YOLO-origin detection means the YOLO adapter produced a detection-like model output at a media-owned frame/time and TOM v3 persisted it through the existing detection observation contract.

It does not mean:

- the object is correct
- identity is known
- a tennis action happened
- a rally or point exists
- a score exists

Real model output is useful replay evidence, but model quality depends on the local weights, class mapping, source media, device, and thresholds.
