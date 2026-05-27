# TOM v3 Replay Workstation

Blueprint 6 starts a new product layer on top of the completed TOM v3 Simple evidence platform.

Replay Mode is the first step:

```text
indexed video
-> browser playback
-> TOM media-owned timestamp/frame display
-> selected run context
-> future synchronized observation overlays
```

Milestone 6A proves video replay and frame/time synchronization only.

## What 6A Adds

- `GET /media/{media_id}/replay-info`
- `GET /media/{media_id}/video`
- backend frame/time mapping helpers
- `/replay/[mediaId]` frontend route
- HTML video playback for indexed local media
- current time, timestamp, and nearest frame display
- basic timeline/progress shell
- available run context grouped by evidence type
- overlay placeholder for future detection, tracklet, and pose playback layers

## What 6A Does Not Add

- detection overlay playback
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

In 6A, these only identify selected run context. They do not draw overlays yet.

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

## Boundary

The replay workstation displays synchronized evidence context. It does not decide tennis meaning.

Blueprint 6B can add detection observation overlay playback. Blueprint 6C can add tracklet and pose replay layers. Stream proxy mode remains future work.
