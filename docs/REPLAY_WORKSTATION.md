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

Milestone 7E decides that court/camera/homography evidence belongs in Blueprint 8. Blueprint 8E adds replay overlays for persisted court keypoint evidence, court line evidence, camera/view evidence, and homography candidates. Milestone 8F adds projection diagnostic replay payloads/details for persisted diagnostic observations. Object-to-Court Projection Candidates v0 adds derived ball and main-player court-template projection candidates through `courtProjectionRunId`; these remain evidence-only candidates, not court truth or tennis-event conclusions.

Milestone 7F closes Blueprint 7 with the final perception orchestration path:

```text
indexed media
-> optional real detection run
-> optional real-detection-derived candidate tracklets
-> optional real pose run
-> replay URL with detectionRunId, trackletRunId, and poseRunId
```

Blueprint 7 completes TOM v3's real perception runtime for the replay workstation. The workstation can render fixture evidence or optional real model-output evidence through the same detection, tracklet, pose, timeline, and selected-detail surfaces. Court/camera/homography evidence now proceeds in Blueprint 8.

Blueprint 8 has started with geometry evidence work. Milestone 8A adds court keypoint, court line, camera/view, homography candidate, and projection diagnostic storage contracts. Milestone 8B writes fixture court keypoint, line, and camera/view rows. Milestone 8C exposes camera/view rows through read-model APIs. Milestone 8D persists homography candidate rows with lineage from source court evidence. Milestone 8E renders those persisted court rows in the replay workstation through `courtRunId` and `homographyRunId`. Milestone 8F adds projection diagnostic rows and replay support through `projectionDiagnosticRunId`.

The TOM v1 court keypoint adapter can now write real model-output `court_keypoint_observation` rows through `courtRunId`. Replay labels distinguish fixture court evidence from real court keypoint model output and derived court line candidates. The court calibration audit adds separate raw TOM v1 keypoint and mapped TOM v3 keypoint toggles so `raw_0..raw_13` can be visually checked before trusting mapping or homography. Homography and projection diagnostic overlays built from those rows remain candidate geometry evidence and review diagnostics, not court truth.

Court geometry temporal persistence is now a replay/read-model display policy. `court_temporal_persistence=carry_forward` carries the latest court keypoint, court line, homography candidate, and projection diagnostic overlay forward until the next source observation or `court_persistence_max_gap_ms`. The default max gap is `1500` ms. Replay controls expose this policy and show a carried-forward candidate geometry badge when active geometry is displayed between source samples. This reduces flicker for sparse court runs without creating new observations or turning candidate geometry into court truth.

The TOM v1 model assets bridge does not add replay architecture. It lets local TOM v1 detector and pose weights be tested through the existing `detectionRunId`, `trackletRunId`, and `poseRunId` replay paths. If a TOM v1 smoke run succeeds, the replay workstation should label the resulting rows as real model-output observations, not fixture evidence or tracking truth.

The main tennis-player subject filter can reduce TOM v1 player-detection pose sources before replay. It persists `main_player_subject_candidate` rows for `near_player_candidate` and `far_player_candidate` source candidates, then real pose can consume that `source_subject_run_id`. Replay then shows cleaner pose evidence because pose was only run on selected candidates. This remains observation-only and does not confirm player identity.

Main player track assignment can further reduce frame-local subject noise by persisting `main_player_track_candidate` rows for `near_player_track_candidate` and `far_player_track_candidate`, plus per-frame `main_player_track_assignment_candidate` rows. Real pose can consume `source_track_run_id` so keypoint evidence is generated only from detections attached to those visual track candidates. Replay pose detail shows the track candidate id/role when available. These are still candidate visual tracks, not player identity truth.

Dense real model-output runs can produce visually noisy overlays. The replay workstation provides display-only controls for detection and tracklet evidence:

- Current only
- Short trail
- Full trail

Detection display defaults to current-only. Tracklet point display defaults to short-trail, and tracklet trail/path rendering is off by default. These controls reduce visual trails without mutating persisted observations, candidate tracklets, lineage, or evidence-only semantics.

Motion Smoothing / Stable Replay Candidates v0 adds derived replay candidate layers through
`motionSmoothingRunId`:

- `smoothed_ball_position_candidate`
- `smoothed_main_player_box_candidate`
- `smoothed_pose_candidate`

Replay can render smoothed ball, smoothed near/far main-player boxes, and smoothed pose skeletons by
default when a motion smoothing run is selected. Raw detection, tracklet, and pose evidence remains
available for audit. These layers are derived candidate evidence only; they do not establish ball
truth, pose truth, player identity, bounce, hit, in/out, point, score, or court-space position.

The smoothed motion display defaults to **Current only**. In that mode replay selects one current
smoothed ball candidate, one near-player box candidate, one far-player box candidate, and one
smoothed pose per active main-player track. Short-trail and full-trail/debug modes remain available
for audit when an operator intentionally wants to inspect neighboring smoothed candidates.

Pose overlays default to a limb-only visual style for both raw and smoothed pose evidence. Left-side
limbs render blue, right-side limbs render red, and neutral/cross-body lines stay subtle. Operators
can switch to `Limbs + joints` or `Joints only/debug` when they need to audit raw keypoint markers.
This is display-only styling; it does not classify strokes, body mechanics, hits, or tennis events.

Object-to-Court Projection Candidates v0 adds `courtProjectionRunId` replay support for derived
`ball_court_projection_candidate` and `main_player_court_projection_candidate` rows. Replay exposes
these through `ball_court_projection` and `main_player_court_projection` payloads, a
`court_projection` timeline lane, selected evidence details, and a normalized court-template
mini-map. The mini-map labels points as `BALL CANDIDATE`, `NEAR PLAYER CANDIDATE`, and
`FAR PLAYER CANDIDATE`. It intentionally does not draw those normalized template coordinates over
the broadcast video or present them as true object locations.

Operator View Default Layer Presets v0 adds a replay view preset control. `viewPreset=operator` is
the default and opens full replay URLs with stable candidate layers on and raw/debug layers off:
smoothed ball/player/pose, mapped court keypoints, court lines, court carry-forward, and the court
projection mini-map are visible when their runs exist. Raw TOM v1 court keypoints, homography
candidate overlays, projection diagnostics, camera/view evidence, raw detection trails, and raw pose
are kept off until the operator enables them. `viewPreset=debug` applies a busy audit preset with
raw/debug evidence visible when its run ids exist. Both presets are display policy only.

Ball Trajectory Court Candidate v0 adds `ballTrajectoryRunId` replay support for derived
`ball_trajectory_court_candidate` rows. Replay exposes these through the `ball_court_trajectory`
payload, a `ball_trajectory` timeline lane, selected evidence details, and a subtle trajectory path
inside the normalized court-template mini-map. The trajectory is a candidate sequence of projected
ball evidence; it does not imply bounce, hit, in/out, point, or score.

Hit/Bounce Candidate Evidence v0 adds `eventCandidateRunId` replay support for derived
`hit_candidate` and `bounce_candidate` rows. Replay exposes them in the `event_candidates` timeline
lane, the normalized court-template mini-map, selected evidence details, and as broadcast video
markers when the source ball court projection includes an image-space point. Video labels must say
`HIT CANDIDATE` or `BOUNCE CANDIDATE`; they do not confirm events or line calls.

Hit/Bounce Physics Heuristic Repair v0.2 adds selected-evidence diagnostics for
`net_axis_reversal`, `vertical_motion_proxy`, and `speed_reduction`. These explain why a candidate
was proposed; they do not make the candidate true.

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

Blueprint 8 replay layers now include:

- court keypoint evidence
- raw TOM v1 court keypoint evidence
- mapped TOM v3 court keypoint evidence
- court line evidence
- camera/view evidence
- homography candidate
- projection diagnostic

Selected detail should show source court evidence, model/runtime/config, matrix fields when applicable, lineage-oriented identifiers, annotations where available, and candidate-only wording.

The replay workstation should avoid labels that imply final court geometry, line-call decisions, bounce locations, or official tennis results.

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

## Blueprint 8 Court Evidence Boundary

8A adds backend schema and persistence foundations for future replay court layers:

- court keypoint evidence
- court line evidence
- camera/view evidence
- homography candidate
- projection diagnostic

8B adds fixture production of court keypoint, court line, and camera/view evidence through `run-fixture-court`. 8C adds backend camera/view query, summary, and evidence-bundle APIs under `/court/camera-view` so future homography work can inspect view context. 8D adds `build-homography-candidates` to persist candidate transform evidence and source lineage. 8E adds replay overlay payloads, court layer toggles, selected evidence detail, and timeline lanes for persisted court evidence. 8F adds `build-projection-diagnostics` and replay support for persisted projection diagnostic observations.

The replay workstation fetches and renders court layers as geometry evidence only. Projection diagnostics are review evidence for projected court template geometry; they remain separate from ball/player court projection, bounce, hit, line-call, rally, point, and scoring conclusions.

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

Court keypoint payloads from the TOM v1 adapter also include `raw_tom_v1_keypoints`, `mapped_keypoints`, `preprocessing_mode`, `coordinate_interpretation`, `mapping_version`, `inferred_tom_v3_keypoints`, and an uncalibrated mapping warning. These are calibration/debug fields, not correctness claims.

Real-detection-derived tracklet runs appear in the tracklet run group. Their optional metadata includes `evidence_source`, `source_label`, `source_detection_run_id`, `source_detection_evidence_source`, `source_detection_runtime`, and `is_real_detection_derived`.

Real pose replay runs appear in the pose run group. Their optional metadata includes `evidence_source = real_pose_model_output`, `source_label`, `source_runtime = ultralytics_pose`, `model_name`, `model_version`, `model_registry_id`, `runtime_config_id`, `is_fixture`, and `is_real_model_output`.

## Replay Overlay Chunks

`GET /replay/overlays` returns replay overlay data for a media/time window:

```text
GET /replay/overlays?media_id=<media_id>&start_ms=0&end_ms=2000&layers=detections,tracklets,pose,court_keypoints,court_lines,camera_view,homography_candidates,projection_diagnostics,ball_court_projection,main_player_court_projection&detection_run_id=<run_id>&tracklet_run_id=<run_id>&pose_run_id=<run_id>&court_run_id=<run_id>&homography_run_id=<run_id>&projection_diagnostic_run_id=<run_id>&court_projection_run_id=<run_id>
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
  "projection_diagnostics": [
    {
      "overlay_type": "projection_diagnostic",
      "observation_id": "...",
      "run_id": "...",
      "frame_number": 30,
      "timestamp_ms": 1000,
      "source_homography_candidate_observation_id": "...",
      "projected_template_keypoints": [],
      "projected_template_lines": [],
      "diagnostic_metrics": {},
      "status": "diagnostic_candidate",
      "geometry_evidence_only": true,
      "not_ball_player_projection": true
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
GET /replay/timeline?media_id=<media_id>&detection_run_id=<run_id>&tracklet_run_id=<run_id>&pose_run_id=<run_id>&court_run_id=<run_id>&homography_run_id=<run_id>&projection_diagnostic_run_id=<run_id>&court_projection_run_id=<run_id>
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
    { "lane_type": "projection_diagnostics", "label": "Projection diagnostics", "items": [] },
    { "lane_type": "court_projection", "label": "Court projection candidates", "items": [] },
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
?detectionRunId=<run_id>&trackletRunId=<run_id>&poseRunId=<run_id>&courtRunId=<run_id>&homographyRunId=<run_id>&projectionDiagnosticRunId=<run_id>&courtProjectionRunId=<run_id>&ballTrajectoryRunId=<run_id>&viewPreset=operator
```

`detectionRunId`, `trackletRunId`, `poseRunId`, `courtRunId`, `homographyRunId`,
`projectionDiagnosticRunId`, `courtProjectionRunId`, and `ballTrajectoryRunId` select the persisted
evidence runs used for replay overlay playback. `viewPreset=operator|debug` selects the initial
replay layer preset; operator is the default when the parameter is omitted.

Open Stream Proxy Mode:

```text
?mode=stream_proxy&detectionRunId=<run_id>&trackletRunId=<run_id>&poseRunId=<run_id>&courtRunId=<run_id>&homographyRunId=<run_id>&projectionDiagnosticRunId=<run_id>&courtProjectionRunId=<run_id>&ballTrajectoryRunId=<run_id>
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

For TOM v1 filtered pose replay, first run the main subject filter:

```bash
.venv/bin/python -m apps.worker.cli select-main-player-subjects \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --max-frames 214
```

Then run pose with `--source-subject-run-id <main_subject_run_id>`. Raw detections remain inspectable; the subject run only controls pose source selection.

For TOM v1 main player track-filtered pose replay, assign visual track candidates after the subject filter:

```bash
.venv/bin/python -m apps.worker.cli assign-main-player-tracks \
  --media-id <media_id> \
  --source-detection-run-id <player_real_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --max-frames 214
```

Then run pose with `--source-track-run-id <main_player_track_run_id>` in addition to the detection and subject run ids. Replay pose details show the candidate visual track context when present. This does not confirm player names, identity, side, server/receiver role, or tennis events.

Open track-filtered replay with the track run selected:

```text
http://127.0.0.1:3000/replay/<media_id>?detectionRunId=<player_detection_run_id>&trackletRunId=<player_tracklet_run_id>&subjectRunId=<main_subject_run_id>&mainPlayerTrackRunId=<main_player_track_run_id>&poseRunId=<track_filtered_pose_run_id>
```

When `mainPlayerTrackRunId` is present, the workstation can draw selectable `NEAR TRACK` and `FAR TRACK` candidate labels from `main_player_track_assignment_candidate` rows. Selecting a label shows track candidate id, role candidate, assignment score, source subject candidate id, source detection id, and evidence-only warnings. These labels are candidate visual track labels, not player names or identity truth.

For court geometry evidence replay:

```bash
.venv/bin/python -m apps.worker.cli run-fixture-court \
  --media-id <media_id> \
  --frame-sample-rate 30 \
  --max-frames 30

.venv/bin/python -m apps.worker.cli build-homography-candidates \
  --media-id <media_id> \
  --court-run-id <court_run_id>

.venv/bin/python -m apps.worker.cli build-projection-diagnostics \
  --media-id <media_id> \
  --homography-run-id <homography_run_id>
```

Open:

```text
http://127.0.0.1:3000/replay/<media_id>?courtRunId=<court_run_id>&homographyRunId=<homography_run_id>&projectionDiagnosticRunId=<projection_diagnostic_run_id>
```

Projection diagnostics display projected court template evidence only. They do not project ball/player observations into court space.

For court projection, trajectory, and first-pass event-candidate replay:

```text
http://127.0.0.1:3000/replay/<media_id>?courtProjectionRunId=<court_projection_run_id>&ballTrajectoryRunId=<ball_trajectory_run_id>&eventCandidateRunId=<event_candidate_run_id>&viewPreset=operator
```

The court projection mini-map can show current ball/player projection candidates, a
`BALL TRAJECTORY CANDIDATE` path, and `HIT CANDIDATE` / `BOUNCE CANDIDATE` markers. Event candidate
markers also appear on the broadcast video when replay can resolve the source image point. Event
candidate markers remain visible as persistent review pins, with active and selected states, so
operators can review the full point without missing sparse markers. Both surfaces are derived
diagnostics only. They are not hit truth, bounce truth, in/out, point, score, or adjudication.

Event candidate selected evidence shows the v0.2 physics fields when available: player-proximate
net-axis reversal for hit candidates, and image-y descending-to-ascending proxy plus speed
reduction for bounce candidates.

For Stream Proxy Mode, open:

```text
http://127.0.0.1:3000/replay/<media_id>?mode=stream_proxy&detectionRunId=<detection_run_id>&trackletRunId=<tracklet_run_id>&poseRunId=<pose_run_id>
```

## Boundary

The replay workstation displays synchronized evidence context. It does not decide tennis meaning.

Stream Proxy Mode is live-like local replay only. Real live ingestion remains future work.

Future real live ingestion and future tennis intelligence must begin as new blueprints.
