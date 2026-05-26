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

Milestone 1E adds frame artifact support. When a matching `frame_image` or `detection_frame_image` artifact exists, the viewer displays that extracted image behind the same persisted bboxes.

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

Extract frame artifacts:

```bash
python -m apps.worker.cli extract-frame-artifacts \
  --run-id <DETECTION_RUN_ID> \
  --max-frames 2
```

Refresh the viewer to see frame imagery behind bbox overlays.

## Known Limitations

- No video playback overlay is implemented.
- Real YOLO runtime validation is optional and local-only; fixture detection remains the default base-environment demo path.
- Detection observations are not converted into tracks.
- The overlay visualizes only frame-level bbox observations.
- Frame artifact serving is local-development only.

Blueprint 3 completion confirms that YOLO-origin detections use this same overlay path; there is no separate YOLO viewer.

Milestone 4D adds a separate pose overlay panel to the same Evidence Viewer. Detection overlays continue to render persisted bbox observations; pose overlays render persisted `player_pose_observation` keypoint evidence. Neither overlay interprets tennis events or adjudicates correctness.
