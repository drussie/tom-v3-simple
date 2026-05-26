# Detection Overlay Viewer v0

## Purpose

Detection Overlay Viewer v0 makes persisted `ball_detection` and `player_detection` observations visually inspectable in the existing visual evidence viewer.

The overlay answers:

```text
The database says this detection observation exists.
Where was it observed?
```

The overlay is a visualization of persisted observation payloads. It does not create tracks, infer bounces, or decide whether a detection is correct.

## Data Source

The overlay uses the existing viewer route:

```text
GET /viewer/runs/{run_id}
```

It extracts detections from persisted observations where:

- `observation_family = atomic`
- `observation_type = ball_detection` or `player_detection`
- `coordinate_space = image_pixels`

The bbox payload may come from either:

- `observation.payload_jsonb.bbox`
- `observation.atomic.payload_jsonb.bbox`

The transform is tolerant of both locations because the observation spine and typed atomic extension both carry detection metadata.

## Viewer Files

Primary files:

- `apps/web/src/lib/detections.ts`
- `apps/web/src/components/DetectionOverlayPanel.tsx`
- `apps/web/src/components/DetectionOverlayCanvas.tsx`
- `apps/web/src/components/DetectionLegend.tsx`
- `apps/web/src/components/EvidenceViewer.tsx`

## Rendering Contract

The overlay uses media dimensions from the persisted `media_asset`:

- `width`
- `height`

Each bbox is scaled as:

```text
left = bbox.x / media.width
top = bbox.y / media.height
width = bbox.width / media.width
height = bbox.height / media.height
```

The coordinate panel is an honest frame-space visualization. If no real frame image is available, the viewer shows an `image_pixels` coordinate canvas instead of pretending a frame was extracted.

## Selection Behavior

When the selected observation is a detection:

- selected frame = `observation.frame_start`
- all detections on that frame are shown
- the selected detection bbox is highlighted

When the selected observation is not a detection:

- the overlay defaults to the first detection frame in the run

Selecting a bbox updates the existing observation selection, so the detail, lineage, artifact, and annotation panels continue to reflect the selected observation.

## Safe Empty States

The overlay does not invent detections.

It shows a safe unavailable state when:

- media dimensions are missing
- no persisted detection observations include bbox payloads

It also reports how many detection observations are missing bbox payloads.

## Local Flow

Index a video:

```bash
python -m apps.worker.cli index-media --source-path /path/to/video.mp4 --copy-to-storage
```

Run fixture detection:

```bash
python -m apps.worker.cli run-detection-adapter \
  --media-id <MEDIA_ID> \
  --adapter fixture \
  --frame-sample-rate 30 \
  --max-frames 5 \
  --output-debug-artifact
```

Start the backend and web app, then open:

```text
http://127.0.0.1:3000/runs/<DETECTION_RUN_ID>
```

## Known Limitations

- No frame extraction pipeline is implemented.
- No video playback overlay is implemented.
- No real YOLO26 inference is implemented in this repo state.
- Detection observations are not converted into tracks.
- The overlay visualizes only frame-level bbox observations.
