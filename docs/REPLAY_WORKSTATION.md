# TOM v3 Replay Workstation

Blueprint 6 starts a new product layer on top of the completed TOM v3 Simple evidence platform.

Replay Mode is the first step:

```text
indexed video
-> browser playback
-> TOM media-owned timestamp/frame display
-> selected run context
-> synchronized detection observation overlays
-> future tracklet/pose replay layers
```

Milestone 6A proved video replay and frame/time synchronization.

Milestone 6B adds detection overlay playback for persisted `ball_detection` and
`player_detection` observations.

## What 6A Added

- `GET /media/{media_id}/replay-info`
- `GET /media/{media_id}/video`
- backend frame/time mapping helpers
- `/replay/[mediaId]` frontend route
- HTML video playback for indexed local media
- current time, timestamp, and nearest frame display
- basic timeline/progress shell
- available run context grouped by evidence type
- overlay placeholder for future detection, tracklet, and pose playback layers

## What 6B Adds

- `GET /replay/overlays`
- detection overlay chunks for media/time windows
- optional detection run filtering
- optional display-only confidence filtering
- normalized bbox payloads in original image-pixel coordinates
- replay detection layer toggle
- detection run selection and `detectionRunId` query support
- bbox rendering over the replay video
- display hold for sparse frame observations
- click-to-select detection observation details
- detection timeline ticks for the loaded overlay chunk

Detection overlays are persisted observation evidence. They do not confirm object
identity or tennis meaning.

## What 6B Does Not Add

- tracklet overlay playback
- pose overlay playback
- evidence lanes on the timeline
- live stream ingestion
- HLS/RTSP/HDMI capture
- new model runtime behavior
- tennis-event interpretation
- scoring or official results

## Backend Replay Info

`GET /media/{media_id}/replay-info` returns:

```json
{
  "media_id": "...",
  "video_url": "/media/{media_id}/video",
  "width": 1920,
  "height": 1080,
  "duration_ms": 7133,
  "fps": 30.0,
  "frame_count": 214,
  "frame_time_mode": "indexed",
  "available_runs": {
    "detection": [],
    "tracklet": [],
    "pose": [],
    "gameplay": []
  },
  "observation_only": true,
  "no_adjudication": true
}
```

Available runs are grouped from persisted observations:

- detection: `ball_detection`, `player_detection`
- tracklet: tracklet candidate and track point candidate observations
- pose: `player_pose_observation`
- gameplay: `view_state`

## Detection Overlay Chunks

`GET /replay/overlays` returns replay overlay data for a media/time window:

```text
GET /replay/overlays?media_id=<media_id>&start_ms=0&end_ms=2000&layers=detections&detection_run_id=<run_id>
```

The 6B response includes detection bbox items only:

```json
{
  "media_id": "...",
  "start_ms": 0,
  "end_ms": 2000,
  "coordinate_space": "image_pixels",
  "detections": [
    {
      "overlay_type": "detection_bbox",
      "observation_id": "...",
      "run_id": "...",
      "frame_number": 30,
      "timestamp_ms": 1000,
      "observation_type": "ball_detection",
      "label": "ball",
      "confidence": 0.82,
      "bbox": { "x": 511, "y": 280, "w": 18, "h": 18 },
      "source_language": "detection observation"
    }
  ],
  "tracklets": [],
  "poses": [],
  "observation_only": true,
  "no_adjudication": true
}
```

The endpoint preserves media-owned frame/time and image-pixel coordinates.
`min_confidence` affects only the returned display payload; it does not mutate
observations.

## Video Serving

`GET /media/{media_id}/video` serves the indexed local video file for browser playback.

The endpoint uses the media asset's stored local path or stored file URI first, then falls back to source local file references. It does not accept arbitrary file paths from the request.

If the local file is unavailable, the endpoint returns `404`.

This is local file replay, not streaming infrastructure.

## Frame / Time Mapping

6A uses indexed media metadata:

```text
timestamp_ms -> nearest frame
frame -> timestamp_ms
currentTime seconds -> nearest frame
```

For constant-frame-rate media, the mapping is:

```text
frame = round((timestamp_ms / 1000) * fps)
```

The frame value is clamped to:

```text
0 <= frame <= frame_count - 1
```

The replay page labels this as the nearest frame from media metadata.

## Frontend Route

Open:

```text
http://127.0.0.1:3000/replay/<media_id>
```

Optional context query parameters:

```text
?detectionRunId=<run_id>&trackletRunId=<run_id>&poseRunId=<run_id>
```

In 6B, `detectionRunId` selects the detection observation run used for bbox
overlay playback. Tracklet and pose query parameters still provide context only.

## Local Demo Flow

Run a fixture demo:

```bash
DEMO_MEDIA_PATH=demo_assets/sample_point.mp4 \
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db \
make demo PYTHON=.venv/bin/python MAX_FRAMES=3
```

Start the API and web app:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_demo_sample_point_6a.db \
.venv/bin/python -m uvicorn apps.api.main:app --reload
```

```bash
cd apps/web
NEXT_PUBLIC_TOM_V3_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open the replay URL from the demo summary or:

```bash
make replay-open MEDIA_ID=<media_id>
```

For detection overlay playback, open:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<detection_run_id>
```

## Boundary

The replay workstation displays synchronized evidence context. It does not decide tennis meaning.

Blueprint 6C can add tracklet and pose replay layers. Stream proxy mode remains future work.
