# Frame Artifact Overlay v0

## Purpose

Frame Artifact Overlay v0 lets the visual evidence viewer display extracted frame images behind persisted detection bboxes when frame artifacts are available.

The viewer still renders bboxes from persisted observations. The frame image is supporting evidence, not a new observation interpretation.

## Matching Rules

For a selected detection observation, the viewer looks for frame artifacts in this order:

1. Targeted artifact:
   - `target_observation_id == selectedObservation.id`
   - `artifact_type in frame_image / detection_frame_image`
2. Same-frame artifact:
   - `artifact.frame_start == selectedFrame`
   - `artifact_type in frame_image / detection_frame_image`
3. Fallback:
   - render the `image_pixels` coordinate canvas

This allows a single shared frame artifact to support multiple detections on the same frame while still supporting observation-targeted artifacts.

## Rendering Behavior

When a frame artifact is available:

- the viewer loads it from `GET /artifacts/{artifact_id}/content`
- the image is rendered behind the bbox overlay
- bboxes remain scaled from persisted media dimensions and persisted bbox payloads
- the panel labels the artifact source

When no frame artifact is available:

- the viewer keeps the coordinate canvas fallback
- the viewer displays:

```text
No frame image artifact is available for this frame; showing image_pixels coordinate canvas.
```

## Files

- `apps/web/src/lib/detections.ts`
- `apps/web/src/components/DetectionOverlayPanel.tsx`
- `apps/web/src/components/DetectionOverlayCanvas.tsx`

## What The Frame Artifact Means

A frame artifact means:

```text
This image was extracted from this indexed media asset at this media-owned frame/timestamp.
```

It does not mean:

- the detection is correct
- the object is proven
- a track exists
- a bounce happened
- a hit happened

## Known Limitations

- The route serves local files for development only.
- Missing files render as image load failures in the browser, while metadata remains visible in the artifact panel.
- There is no video player overlay in this milestone.
