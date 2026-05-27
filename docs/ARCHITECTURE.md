# TOM v3 Simple Architecture

This is a high-level architecture summary for the current TOM v3 Simple platform.

## Local Media

Media indexing creates a `media_asset` row for a local video. It records source URI, optional stored URI, checksum, FPS, frame count, dimensions, and a frame/time summary.

Media indexing owns frame/time. Downstream adapters use media-owned frame numbers and timestamps.

## Processing Runs And Steps

Each adapter, builder, export, or demo stage records provenance through:

- `processing_run`
- `processing_step`
- `runtime_config`
- `model_registry` where relevant

Runs identify the operation. Steps describe the phase inside that operation. Runtime configs preserve the settings used.

## Model Registry

The model registry stores model or fixture metadata. For YOLO, it stores local weights fingerprint and class mapping. For pose fixtures, it stores skeleton metadata.

Model registry rows are provenance records. They do not make output correct.

## Observation Spine

The `observation` table is the shared spine for evidence. It stores:

- media id
- run id
- family/type
- granularity
- frame/time range
- confidence
- model/runtime ids
- coordinate space
- payload summary

Typed tables add structured detail.

## Typed Observations

TOM v3 Simple currently has:

- gameplay observations
- atomic detection observations
- tracklet candidate rows
- track point candidate rows
- pose observations

Detection and pose rows use image-pixel coordinates. Tracklet and track point rows keep candidate grouping context.

## Lineage

`observation_lineage` records parent/child relationships:

- source detection -> track point candidate
- track point candidate -> tracklet candidate
- source player detection -> pose observation
- optional tracklet/track point context -> pose observation

Lineage explains source context. It does not validate correctness.

## Evidence Artifacts

`evidence_artifact` rows point to local frame images, debug JSON, and review exports. File-backed artifacts include checksums where available.

Artifacts support replay and review.

## Human Annotations

`human_annotation` rows attach review evidence to observations or artifacts. They do not mutate the original observation, tracklet, pose row, or export.

## Query And Export

Tracklet and pose query services expose structured filters.

Tracklet and pose review export services create TOM-native JSON files and persist export artifact metadata. Query-driven exports can create query result memory.

## Viewer

The Evidence Viewer reads backend payloads and displays:

- run evidence summary
- observations
- detection bboxes
- candidate tracklet evidence
- pose keypoint evidence
- lineage
- artifacts
- annotations
- review export metadata

The viewer presents evidence; it does not run models or infer tennis meaning.

## Fixture Demo

The local fixture demo exercises the platform end-to-end without optional model assets:

```text
media -> gameplay -> detections -> artifacts -> tracklets -> pose -> annotations -> exports -> audit
```

## Optional YOLO Path

YOLO runtime is optional. The base environment stays lightweight.

The optional path includes runtime probe, device resolver, local weights validation, model registration, YOLO-like output normalization, guarded frame inference, and detection persistence through the existing detection adapter contract.

YOLO-origin detections are still observations.
