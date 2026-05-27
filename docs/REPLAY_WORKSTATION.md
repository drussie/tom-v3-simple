# TOM v3 Replay Workstation

Blueprint 6 is complete.

It adds a visual replay/operator workstation on top of the completed TOM v3 Simple evidence platform.

Replay Mode is the first step:

```text
indexed video
-> browser playback
-> TOM media-owned timestamp/frame display
-> selected run context
-> synchronized detection observation overlays
-> synchronized tracklet candidate overlays
-> synchronized pose keypoint evidence overlays
-> evidence timeline lanes and click-to-seek scrubber
-> Stream Proxy Mode for video-as-live operation
```

Milestone 6A proved video replay and frame/time synchronization.

Milestone 6B adds detection overlay playback for persisted `ball_detection` and
`player_detection` observations.

Milestone 6C adds tracklet candidate and pose keypoint overlay playback.

Milestone 6D adds timeline lanes and evidence scrubbing across detection
observations, tracklet candidates, pose observations, and review annotations.

Milestone 6E adds Stream Proxy Mode over indexed local video.

Milestone 6F closes Blueprint 6 with a completion review and final status updates.

Blueprint 6 completes TOM v3's visual replay/operator workstation. TOM can now open an indexed video in Replay Mode or Stream Proxy Mode, play the video, synchronize persisted detection observations, candidate tracklets, and pose keypoint evidence over media-owned frame/time, render evidence timeline lanes, allow click-to-seek and click-to-select persisted observations, and hide future evidence in Stream Proxy Mode until the live-like proxy edge reaches it.

Blueprint 6 remains observation-only and non-adjudicative. It does not add real live TV/HLS/RTSP/HDMI ingestion, stream backend infrastructure, real pose inference, movement interpretation, homography, bounce/hit/rally/point/scoring, or TOM v2-style adjudication.

Blueprint 7 is complete. It adds real perception runtime for this workstation while keeping all outputs observation-only. Milestones 7A and 7B add optional real YOLO detection replay runs that persist model-output `ball_detection` and `player_detection` observations, then label and inspect those real runs through `detectionRunId`.

Milestone 7C builds candidate tracklets from real detection runs through the existing tracklet builder. These tracklets are real-detection-derived candidate evidence; they do not establish paths or identities.

Milestone 7D adds optional real pose replay runs that persist `player_pose_observation` keypoint evidence and render through `poseRunId`. Pose keypoints are evidence only and do not interpret movement, strokes, biomechanics, court position, or tennis events.

Milestone 7E decides that court/camera/homography evidence belongs in future Blueprint 8. The replay workstation does not yet implement court keypoint overlays, court line overlays, homography candidate overlays, projection diagnostics, or court-space coordinate transforms.

Milestone 7F closes Blueprint 7 with the final perception orchestration path:

```text
indexed media
-> optional real detection run
-> optional real-detection-derived candidate tracklets
-> optional real pose run
-> replay URL with detectionRunId, trackletRunId, and poseRunId
```

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. The workstation can render fixture evidence or optional real model-output evidence through the same detection, tracklet, pose, timeline, and selected-detail surfaces. Court/camera/homography evidence now proceeds in Blueprint 8.

Blueprint 8 has started with schema/contract work. Milestone 8A adds court keypoint, court line, camera/view, homography candidate, and projection diagnostic storage contracts, but it does not add replay court overlays yet.

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

- evidence lanes on the timeline
- live stream ingestion
- HLS/RTSP/HDMI capture
- new model runtime behavior
- tennis-event interpretation
- scoring or official results

## What 6C Adds

- `GET /replay/overlays` support for `layers=tracklets,pose`
- optional `tracklet_run_id` filtering
- optional `pose_run_id` and display-only `min_pose_confidence` filtering
- normalized tracklet candidate payloads with persisted track points
- normalized pose observation payloads with persisted keypoints and COCO17 edges
- replay layer toggles for detection observations, tracklet candidates, and pose observations
- tracklet and pose run selection with query parameter support
- candidate track point and selected candidate path rendering over replay video
- pose bbox, keypoint, and skeleton rendering over replay video
- click-to-select detection, tracklet, track point, and pose evidence details

Tracklet overlays are candidate temporal groupings. Pose overlays are keypoint
evidence. Neither layer confirms object identity, movement, or tennis events.

## What 6C Does Not Add

- stream proxy mode
- live stream ingestion
- new model runtime behavior
- tennis-event interpretation
- scoring or official results

## What 6D Adds

- `GET /replay/timeline`
- detection observation timeline ticks
- tracklet candidate timeline spans
- pose observation timeline ticks
- review annotation timeline markers when target frame/time is available
- frontend evidence timeline lanes
- current playback playhead over the lane stack
- click-to-seek for detection, tracklet, pose, and annotation timeline items
- click-to-select persisted evidence detail from timeline items

Timeline lanes are navigation aids over persisted evidence. They do not imply
object correctness, movement interpretation, tennis-event interpretation, or
official results.

## What 6D Does Not Add

- stream proxy mode
- live stream ingestion
- HLS/RTSP/HDMI capture
- new model runtime behavior
- tennis-event interpretation
- scoring or official results

## What 6E Adds

- Replay / Stream Proxy mode toggle
- `mode=stream_proxy` query parameter support
- video-as-live live edge that advances with playback
- future detection/tracklet/pose overlays hidden until available
- future timeline evidence hidden until available
- tracklet spans clipped to the currently available live-like edge
- available evidence counts
- paused review / lag indicator
- return-to-live-edge action
- `make replay-open MODE=stream_proxy ...` helper URL support

Stream Proxy Mode is a UI/operator mode over indexed local media. It does not
create backend stream sessions or ingest real streams.

## What 6E Does Not Add

- live stream ingestion
- HLS/RTSP/HDMI/camera capture
- websocket live updates
- model scheduling
- new model runtime behavior
- tennis-event interpretation
- scoring or official results

## What 6F Adds

- Blueprint 6 completion review
- final status updates marking Blueprint 6 complete
- final validation and smoke documentation
- explicit future blueprint boundary

6F is closeout only. It adds no new replay, stream, model, or tennis-intelligence capability.

## What 6F Does Not Add

- live stream ingestion
- HLS/RTSP/HDMI/camera capture
- stream backend/session tables
- websocket live updates
- model scheduling
- new model runtime behavior
- tennis-event interpretation
- scoring or official results

## Blueprint 7E Court / Homography Decision

7E is a documentation and architecture decision gate. It adds no replay runtime behavior.

Future Blueprint 8 replay layers may include:

- court keypoint evidence
- court line evidence
- homography candidate
- projection diagnostic

Future selected detail should show source court evidence, model/runtime/config, matrix and diagnostics when applicable, lineage, annotations, and candidate-only wording.

The replay workstation should avoid labels that imply final court geometry, in/out decisions, bounce locations, or official tennis results.

## Blueprint 7F Completion

7F is closeout only. It adds no new replay runtime behavior.

Final Blueprint 7 replay ladder:

```text
run-real-detection
-> /replay/<media_id>?detectionRunId=<real_detection_run_id>

build-tracklets
-> /replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>

run-real-pose
-> /replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>&poseRunId=<real_pose_run_id>
```

The replay workstation remains evidence-only: detection observations, candidate tracklets, track point candidates, and pose keypoint evidence do not become tennis events, player identities, court positions, or scoring.

## Blueprint 8A Court Schema Boundary

8A adds backend schema and persistence foundations for future replay court layers:

- court keypoint evidence
- court line evidence
- camera/view evidence
- homography candidate
- projection diagnostic

The replay workstation does not yet fetch or render these court layers. Future Blueprint 8 milestones should add court overlays deliberately, with labels that keep geometry evidence separate from bounce, hit, in/out, rally, point, and scoring conclusions.

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

Real YOLO detection replay runs appear in the same detection run group because they persist the same atomic observation contract. Run summaries can include optional source metadata so the UI can label:

- real YOLO detection runs as real model-output evidence
- fixture detection runs as fixture/demo evidence

The optional fields include `evidence_source`, `source_label`, `source_runtime`, `model_name`, `model_version`, `model_registry_id`, `runtime_config_id`, `is_fixture`, and `is_real_model_output`.

Real-detection-derived tracklet runs appear in the tracklet run group. Their optional metadata includes `evidence_source`, `source_label`, `source_detection_run_id`, `source_detection_evidence_source`, `source_detection_runtime`, and `is_real_detection_derived`.

Real pose replay runs appear in the pose run group. Their optional metadata includes `evidence_source = real_pose_model_output`, `source_label`, `source_runtime = ultralytics_pose`, `model_name`, `model_version`, `model_registry_id`, `runtime_config_id`, `is_fixture`, and `is_real_model_output`.

## Replay Overlay Chunks

`GET /replay/overlays` returns replay overlay data for a media/time window:

```text
GET /replay/overlays?media_id=<media_id>&start_ms=0&end_ms=2000&layers=detections,tracklets,pose&detection_run_id=<run_id>&tracklet_run_id=<run_id>&pose_run_id=<run_id>
```

The response includes selected overlay families:

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
      "source_language": "detection observation",
      "evidence_source": "real_model_output",
      "source_runtime": "ultralytics_yolo",
      "real_model_output": true,
      "model_output_not_truth": true
    }
  ],
  "tracklets": [
    {
      "overlay_type": "tracklet_candidate",
      "tracklet_id": "...",
      "track_status": "candidate",
      "identity_status": "unverified",
      "source_detection_run_id": "...",
      "source_detection_evidence_source": "real_model_output",
      "source_detection_runtime": "ultralytics_yolo",
      "points": []
    }
  ],
  "poses": [
    {
      "overlay_type": "pose_skeleton",
      "observation_id": "...",
      "skeleton_format": "coco17",
      "keypoints": [],
      "edges": [],
      "evidence_source": "real_pose_model_output",
      "source_runtime": "ultralytics_pose",
      "real_model_output": true,
      "model_output_not_truth": true
    }
  ],
  "observation_only": true,
  "no_adjudication": true
}
```

For real YOLO detection replay, pass the printed `detectionRunId`:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>
```

The boxes remain detection observations. They do not establish ball/player state or tennis-event conclusions.

The endpoint preserves media-owned frame/time and image-pixel coordinates.
`min_confidence` affects only the returned display payload; it does not mutate
observations.

For 7B, selected detection detail shows source/runtime/model/config/class context when those fields exist. This is operator provenance, not a model-correctness claim.

For 7C, selected tracklet and track point details show source detection run, source evidence type, and source runtime when those fields exist. This is source context for candidate temporal grouping; it does not claim path correctness.

For 7D, selected pose detail shows source runtime, model registry id, model name/version, runtime config id, skeleton format/version, keypoint counts, pose confidence, and subject association candidate context when those fields exist. This is keypoint evidence context, not movement interpretation.

## Replay Timeline

`GET /replay/timeline` returns normalized evidence lanes for the selected media
and optional run filters:

```text
GET /replay/timeline?media_id=<media_id>&detection_run_id=<run_id>&tracklet_run_id=<run_id>&pose_run_id=<run_id>
```

The response includes:

```json
{
  "media_id": "...",
  "duration_ms": 7133,
  "frame_count": 214,
  "fps": 30.0,
  "observation_only": true,
  "no_adjudication": true,
  "lanes": [
    { "lane_type": "detections", "label": "Detection observations", "items": [] },
    { "lane_type": "tracklets", "label": "Tracklet candidates", "items": [] },
    { "lane_type": "pose", "label": "Pose observations", "items": [] },
    { "lane_type": "annotations", "label": "Review annotations", "items": [] }
  ]
}
```

Point-like items use `timestamp_ms`; tracklet candidate items use
`timestamp_start_ms` and `timestamp_end_ms`. Clicking an item in the replay
workstation seeks the video to the item time and selects the corresponding
evidence detail.

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

`detectionRunId`, `trackletRunId`, and `poseRunId` select the persisted evidence
runs used for replay overlay playback.

Open Stream Proxy Mode:

```text
?mode=stream_proxy&detectionRunId=<run_id>&trackletRunId=<run_id>&poseRunId=<run_id>
```

In Stream Proxy Mode, future evidence is not rendered in overlays or timeline
lanes until playback reaches that media-owned time.

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

For overlay playback, open:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<pose_run_id>
```

For optional real YOLO detection plus real-detection-derived tracklet replay:

```bash
.venv/bin/python -m apps.worker.cli run-real-detection \
  --media-id <media_id> \
  --weights ./model_assets/yolo/<model>.pt \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto

.venv/bin/python -m apps.worker.cli build-tracklets \
  --detection-run-id <real_detection_run_id> \
  --run-name real-detection-tracklet-candidates
```

Open the replay URL from the `build-tracklets` output:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>
```

For optional real pose replay:

```bash
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <real_detection_run_id> \
  --weights ./model_assets/pose/<pose_model>.pt \
  --mode crop_from_player_detection \
  --every-n-frames 1 \
  --max-frames 120 \
  --device auto
```

Open the replay URL from the `run-real-pose` output:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&poseRunId=<real_pose_run_id>
```

If a tracklet run exists too:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<real_detection_run_id>&trackletRunId=<real_tracklet_run_id>&poseRunId=<real_pose_run_id>
```

For Stream Proxy Mode, open:

```text
http://127.0.0.1:3000/replay/<media_id>?mode=stream_proxy&detectionRunId=<detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<pose_run_id>
```

## Boundary

The replay workstation displays synchronized evidence context. It does not decide tennis meaning.

Stream Proxy Mode is live-like local replay only. Real live ingestion remains future work.

Future real live ingestion and future tennis intelligence must begin as new blueprints.
