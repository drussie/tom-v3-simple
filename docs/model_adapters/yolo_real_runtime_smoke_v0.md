# YOLO Real Runtime Smoke v0

## Purpose

Milestone 3E documents and scripts the optional local real-YOLO smoke path.

The goal is to validate the runtime path created by Milestones 3A through 3D:

```text
tom_v3_yolo environment
-> runtime probe
-> registered local weights
-> indexed media
-> YOLO detection adapter run
-> persisted detection observations
-> frame artifacts
-> viewer overlay
-> optional tracklet builder
-> evidence bundle
```

This smoke path validates workflow and compatibility. It does not add new model intelligence.

Milestone 3F closes Blueprint 3 and treats this smoke path as the local validation surface for real YOLO runtime work.

## Optional Environment

Create a separate environment for real YOLO runtime work:

```bash
conda create -n tom_v3_yolo python=3.11 -y
conda activate tom_v3_yolo

python -m pip install --upgrade pip
pip install -e ".[dev]"
pip install -r requirements-yolo.txt
```

The base `tom_v3` environment should remain lightweight and should not require Ultralytics, Torch, or OpenCV.

## Runtime Probe

```bash
python -m apps.worker.cli yolo-runtime-probe --device auto
python -m apps.worker.cli yolo-runtime-probe --device cpu
```

Expected behavior:

- no crash
- optional package availability is reported
- requested and resolved device are reported
- missing packages produce a clear install hint

## Weights

Place local weights under an ignored model asset path:

```text
model_assets/yolo/<weights_file>.pt
weights/yolo/<weights_file>.pt
```

Do not commit weights.

Register weights:

```bash
python -m apps.worker.cli register-yolo-model \
  --weights-path model_assets/yolo/<weights_file>.pt \
  --model-name local-yolo-smoke \
  --model-version local-v0 \
  --device cpu
```

The command returns `model_registry_id`, sha256, file size, and class mapping metadata. It does not create a processing run or observations.

## Run YOLO Detection

Index media:

```bash
python -m apps.worker.cli index-media \
  --source-path <sample_video_path>
```

Run the YOLO adapter:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <media_id> \
  --adapter yolo \
  --model-registry-id <model_registry_id> \
  --device cpu \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --output-debug-artifact
```

Expected when runtime, weights, and media are available:

- the processing run completes
- `ball_detection` and/or `player_detection` observations may be persisted depending on model output and class map
- payloads carry `source_runtime = ultralytics_yolo`
- payloads carry `frame_time_owner = media_indexing`
- payloads carry model registry id and weights sha256 when supplied

Expected when unavailable:

- clear structured error or skipped smoke result
- no fixture fallback
- no fake detections written as real YOLO output

## Smoke Helper

Plan the local smoke without touching assets:

```bash
python -m apps.worker.cli smoke-real-yolo-local --plan-only
```

Run it when runtime, weights, and media are available:

```bash
python -m apps.worker.cli smoke-real-yolo-local \
  --source-path <sample_video_path> \
  --weights-path model_assets/yolo/<weights_file>.pt \
  --model-name local-yolo-smoke \
  --model-version local-v0 \
  --device cpu \
  --frame-sample-rate 30 \
  --max-frames 3 \
  --output-root .data/artifacts \
  --run-tracklets
```

Equivalent script:

```bash
python scripts/smoke_real_yolo_local.py --plan-only
```

The helper:

- probes runtime
- validates weights
- registers the model
- indexes media
- runs the YOLO adapter
- extracts frame artifacts when detections exist
- optionally builds tracklets
- prints a JSON summary

Missing runtime, weights, or source media produce structured `status = skipped` output. The helper never falls back to the fixture adapter.

## Viewer Validation

Start API and web, then open:

```text
http://127.0.0.1:3000/runs/<detection_run_id>
```

Expected:

- detection overlay uses persisted bbox observations
- selected detections show bbox, confidence, class metadata, model/runtime metadata, and frame/time metadata
- frame imagery appears behind bboxes after `extract-frame-artifacts`
- coordinate canvas fallback remains available when frame artifacts are missing

No separate YOLO viewer is required.

## Tracklet Compatibility

Build candidate tracklets from the YOLO detection run:

```bash
python -m apps.worker.cli build-tracklets \
  --detection-run-id <detection_run_id> \
  --max-gap-frames 30
```

Then inspect:

```text
GET /tracklets/<tracklet_id>/evidence-bundle
```

This proves Blueprint 3 can feed the Blueprint 2 temporal evidence layer. Tracklets remain candidate groupings built after detection; YOLO tracking mode is not used.

## Observation Boundary

A YOLO detection means the YOLO adapter produced a detection-like model output at a media-owned frame/time.

It does not mean the detection is correct, the object is proven, identity is known, a bounce or hit happened, a rally/point exists, or a score is known.

## Out of Scope

- YOLO tracking mode
- tracklets inside the YOLO adapter
- pose
- court homography
- bounce or hit detection
- rally/point/scoring
- production GPU worker
- remote or automatic weights download
- adjudication

## Blueprint 3 Completion

Blueprint 3 is complete as of Milestone 3F. The real local smoke remains optional and local-gated; base TOM v3 validation continues to run without real YOLO dependencies or weights.

See:

```text
docs/blueprints/tom_v3_blueprint_3_completion_review.md
```
