# Tracklet Evidence Bundle v0

## Purpose

The tracklet evidence bundle explains one tracklet candidate across the tracklet builder run and the source detection run.

It answers:

```text
The database says this tracklet candidate exists. Show the grouped track points, source detections, frame artifacts, and lineage.
```

## API

```text
GET /tracklets/{tracklet_id}/evidence-bundle
```

The endpoint is read-only and dynamic. It does not create a saved bundle table.

## Bundle Contents

The response includes:

- typed `tracklet` row
- tracklet candidate observation
- media asset
- tracklet builder run
- source detection run
- runtime config summaries
- model registry summaries
- track point rows
- track point candidate observations
- source detection observations
- frame artifacts matched to source detections
- `tracked_from` lineage rows
- `grouped_from` lineage rows
- available annotations
- annotation summaries for the tracklet, track points, source detections, and full bundle
- candidate-only summary

## Lineage Path

The bundle reconstructs:

```text
source detection observation
-> tracked_from
-> track point candidate observation
-> grouped_from
-> tracklet candidate observation
```

Sequence indexes are stored in lineage payload JSON because the lineage table does not currently have a dedicated `sequence_index` column.

## Artifact Matching

For each source detection, the bundle looks for:

1. targeted `frame_image` or `detection_frame_image` artifacts with `target_observation_id` equal to the source detection id
2. same-frame frame artifacts with matching media id and frame number
3. no artifact, in which case bbox/coordinate metadata remains available

Missing frame artifacts do not fail the bundle.

## Review Annotations

Milestone 2C adds annotation summaries to the bundle. Review annotations may target:

- the tracklet candidate observation
- track point candidate observations
- source detection observations

The bundle returns both the flat annotation list and per-target summaries so the viewer can show review state without mutating any evidence rows.

## Export Use

Milestone 2D review dataset exports package these dynamic bundles into local JSON artifacts. The export path may include or omit frame artifact metadata and annotations, but it does not persist a new saved bundle table.

## Non-Goals

- No new grouping algorithm.
- No multi-object tracker sophistication.
- No bounce or hit detection.
- No pose or court homography.
- No rally or point reconstruction.
- No adjudication.
