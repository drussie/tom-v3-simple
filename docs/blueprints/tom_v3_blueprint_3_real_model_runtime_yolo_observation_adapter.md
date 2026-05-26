# TOM v3 Blueprint 3 - Real Model Runtime / YOLO Observation Adapter

## Status

Status: in progress

Milestone 3A establishes the optional YOLO runtime environment boundary.

Milestone 3B establishes local weights validation and YOLO model registry metadata.

Real YOLO detection persistence is not implemented yet.

## Mission

Safely introduce real YOLO / Ultralytics runtime as a TOM v3 observation adapter that can later convert model outputs into persisted ball/player detection observations without changing downstream query, viewer, artifact, tracklet, review, or export contracts.

Blueprint 3 is about real model runtime and ball/player observation adapters.

Pose is out of scope for Blueprint 3 and should remain for a later blueprint.

## Starting Point

Blueprint 1 proved the media, observation store, viewer, detection overlay, and frame artifact loop.

Blueprint 2 proved candidate temporal evidence: persisted detections can become candidate tracklets with source lineage, evidence bundles, query/review flows, and review dataset exports.

## Blueprint 3 Direction

The intended path is:

```text
optional YOLO runtime
-> validated model weights/config
-> real detector adapter
-> persisted ball_detection / player_detection observations
-> existing viewer/query/artifact/tracklet/review/export contracts
```

Blueprint 3 should not require the base `tom_v3` environment to install Ultralytics or Torch.

## Milestone 3A Result

Milestone 3A adds:

- `requirements-yolo.txt`
- YOLO runtime import guard
- runtime availability probe
- device resolver for `auto`, `cpu`, `mps`, and `cuda`
- missing dependency diagnostics
- worker `yolo-runtime-probe`
- model weight ignore policy
- docs for `tom_v3_yolo`

## Milestone 3B Result

Milestone 3B adds:

- safe local weights path validation
- sha256 and file-size fingerprinting
- required checksum validation
- default ball/player class mapping
- optional model metadata probing
- `model_registry` registration/reuse for validated weights
- worker `register-yolo-model`

3B registers model asset metadata only. It does not run inference and does not persist detections.

## What Blueprint 3 Will Not Prove

Blueprint 3 does not prove that a detection is correct.

Blueprint 3 does not add:

- pose
- court homography
- bounce detection
- hit detection
- rally or point reconstruction
- scoring
- adjudication

## Invariant

A future YOLO detection means:

```text
The YOLO adapter produced a detection-like model output at a media-owned frame/time.
```

It does not mean:

```text
The object is proven.
The identity is known.
A bounce happened.
A hit happened.
A rally or point exists.
```

## Next Milestone

Recommended next milestone:

```text
Milestone 3C - YOLO Detection Adapter Normalization Foundation
```
