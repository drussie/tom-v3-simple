# Pose Overlay Viewer v0

## Purpose

Pose Overlay Viewer v0 makes persisted `player_pose_observation` evidence visually inspectable in the existing Evidence Viewer.

The overlay answers:

```text
The database says this pose observation exists.
Where were the keypoint outputs observed?
```

It visualizes persisted keypoint evidence. It does not infer movement, subject identity, serve mechanics, hit events, rally state, point state, scoring, or adjudicated results.

## Data Source

The overlay uses the existing viewer route:

```text
GET /viewer/runs/{run_id}
```

Each viewer observation can now include a `pose` detail object when:

- `observation_family = pose`
- `observation_type = player_pose_observation`
- `coordinate_space = image_pixels`

The frontend reads:

- observation spine fields
- typed `pose_observation` fields
- COCO17 keypoints from `keypoints_jsonb`
- source association candidate fields when present

## Viewer Files

Primary files:

- `apps/api/routers/viewer.py`
- `apps/web/src/lib/poses.ts`
- `apps/web/src/components/PoseOverlayPanel.tsx`
- `apps/web/src/components/PoseOverlayCanvas.tsx`
- `apps/web/src/components/EvidenceViewer.tsx`

## Rendering Contract

Pose coordinates are persisted full-frame image-pixel coordinates.

The overlay uses media dimensions from `media_asset.width` and `media_asset.height`.

Rendering rules:

- Draw only keypoints with `present = true` and numeric `x/y`.
- Do not draw missing keypoints as present markers.
- Draw a COCO17 skeleton edge only when both endpoint keypoints are present.
- Draw the pose bbox when `bbox_x/y/w/h` are present and positive.
- Show low-confidence keypoints as low-confidence evidence, not as correctness decisions.
- Show missing keypoints in the keypoint table.

## Viewer Controls

The panel includes toggles for:

- pose observations
- skeleton edges
- keypoint labels
- low-confidence keypoints

Selecting a pose updates the existing observation selection so the detail, lineage, artifact, and annotation panels remain aligned.

## Detail Display

The selected pose panel shows:

- observation id
- skeleton format/version
- frame/time
- pose confidence
- keypoints present/missing
- mean keypoint confidence
- bbox
- frame time owner
- association status and method

Milestone 5B adds a short evidence note above these details: pose observations are keypoint evidence only and do not classify movement, actions, or biomechanics.

The keypoint table includes all persisted COCO17 keypoints with name, x/y, confidence, and present/missing status.

## Source Context

When source association candidate fields exist, the panel displays:

- subject ref type
- association status
- association method
- association confidence
- source player detection observation id
- source tracklet candidate id
- source track point candidate id

This is candidate context only. It does not establish player identity or movement meaning.

## Review and Export Context

Milestone 4E keeps pose review/export integration outside the overlay renderer:

- pose annotations are created through the generic annotation API
- selected pose annotations still appear in the existing annotation panel when present in the viewer payload
- pose evidence bundles and review dataset exports are available through the backend/API and worker CLI

The viewer does not convert pose review labels into movement conclusions.

## Known Limitations

- No real pose inference is added by this milestone.
- The pose review label form remains a future viewer enhancement; service/API support exists.
- Deeper source observation lookup remains in existing lineage/detail panels.
- No video playback pose overlay is implemented.

## Blueprint 4 Completion

Blueprint 4 closes with pose evidence visually inspectable in the existing Evidence Viewer. The overlay renders persisted keypoint evidence, skeleton edges, bbox context, keypoint confidence rows, and candidate source context. It does not infer movement, classify actions, or convert review labels into event conclusions.

## Product Polish

Milestone 5B keeps the same overlay but improves empty states and source context language. If no pose observations are available for a run, the viewer points to `run-pose-adapter` or `make demo`. Missing keypoints remain visible as missing evidence in the table and are not drawn as present markers.
