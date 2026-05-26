# YOLO Runtime Environment v0

## Purpose

Milestone 3A adds a safe optional YOLO runtime environment boundary for TOM v3.

The base environment stays lightweight:

```text
tom_v3
-> backend
-> worker
-> viewer
-> fixture adapters
-> tests
-> no required Ultralytics/Torch/OpenCV install
```

Real model work should use a separate optional environment:

```text
tom_v3_yolo
-> base TOM v3 dev install
-> requirements-yolo.txt
-> local model weights outside git
```

## Install

```bash
conda create -n tom_v3_yolo python=3.11 -y
conda activate tom_v3_yolo
python -m pip install --upgrade pip
pip install -e ".[dev]"
pip install -r requirements-yolo.txt
```

`requirements-yolo.txt` currently contains:

```text
ultralytics
opencv-python-headless
```

Torch may be installed as part of Ultralytics, but CUDA/MPS setups can require platform-specific Torch installation.

## Runtime Probe

Run:

```bash
python -m apps.worker.cli yolo-runtime-probe
```

Useful variants:

```bash
python -m apps.worker.cli yolo-runtime-probe --device cpu
python -m apps.worker.cli yolo-runtime-probe --device mps
python -m apps.worker.cli yolo-runtime-probe --device cuda:0
python -m apps.worker.cli yolo-runtime-probe --device auto --no-mps
```

The probe returns JSON with:

- Python version
- Ultralytics availability/version
- Torch availability/version
- OpenCV availability/version
- CUDA availability
- MPS availability
- requested device
- resolved device
- missing packages
- install hint

If optional runtime packages are missing, the probe reports `status = unavailable` and does not crash.

## Device Resolution

`resolve_yolo_device()` follows these rules:

- `auto`: prefer `cuda:0`, then `mps` when allowed, then `cpu`
- `cpu`: always allowed
- `mps`: requires Torch MPS availability
- `cuda`, `cuda:0`, or `0`: requires Torch CUDA availability

Unavailable explicit devices raise a clear `YoloDeviceUnavailable` message.

## Import Boundary

`tom_v3_model_adapters.yolo_runtime` does not import Ultralytics, Torch, or OpenCV at module import time. It uses guarded optional imports inside the probe.

Normal API, worker, viewer, and test imports must continue working without YOLO runtime packages installed.

## Weights Policy

Model weights are local model assets, not source code.

The repo ignores:

```text
model_assets/
weights/
*.pt
*.pth
*.onnx
*.engine
```

Future milestones should record weight path, checksum, runtime versions, class map, and adapter config before running real inference.

Milestone 3B adds that first registration layer. See:

```text
docs/model_adapters/yolo_model_registry_weights_v0.md
```

Milestone 3E adds the optional local real-YOLO smoke workflow. See:

```text
docs/model_adapters/yolo_real_runtime_smoke_v0.md
```

## Out of Scope

Milestone 3A did not add:

- real YOLO inference
- real detection persistence
- model weight validation
- pose
- homography
- bounce detection
- hit detection
- rally/point/scoring
- adjudication
