# Milestone 3A - YOLO Runtime Environment / Runtime Probe Foundation

## Status

Status: complete

## Mission

Prepare TOM v3 for future real YOLO / Ultralytics model runtime work while keeping the base environment clean.

Milestone 3A adds an optional dependency path, runtime probe, device resolver, import guards, tests, and docs. It does not persist real YOLO detections.

## Implemented

- `requirements-yolo.txt` for optional runtime dependencies.
- `tom_v3_model_adapters.yolo_runtime` with:
  - `try_import_yolo_runtime`
  - `probe_yolo_runtime`
  - `resolve_yolo_device`
  - clear unavailable exceptions
- Worker command:

```bash
python -m apps.worker.cli yolo-runtime-probe
```

- Git ignore rules for model weights and runtime assets.
- Tests with mocked imports/devices.
- Blueprint 3 and YOLO runtime environment docs.

## Environment Strategy

Base environment:

```text
tom_v3
```

remains suitable for backend, worker, viewer, fixture adapters, tests, and local demo flows.

Optional model runtime environment:

```text
tom_v3_yolo
```

installs:

```bash
pip install -r requirements-yolo.txt
```

Torch can require platform-specific installation for CUDA/MPS.

## Out of Scope

- real YOLO detection persistence
- model weights loading
- pose
- homography
- bounce detection
- hit detection
- rally/point/scoring
- adjudication

## Next

Recommended next milestone:

```text
Milestone 3B - YOLO Model Registry and Weights Validation
```
