# Motion Smoothing / Stable Replay Candidates v0

Status: implemented

This bridge creates derived replay-smoothing candidate evidence from already persisted raw
observations.

```text
raw ball_detection or track_point_candidate rows
-> smoothed_ball_position_candidate

main_player_track_assignment_candidate rows
-> smoothed_main_player_box_candidate

player_pose_observation rows
-> smoothed_pose_candidate
```

Raw observations remain immutable and inspectable. Smoothing is a derived read/replay aid and a
future input candidate for trajectory review. It is not ball truth, pose truth, player identity,
court-space reasoning, bounce/hit/in-out, point, or score.

Downstream object-to-court projection can consume these smoothed candidates as image-space source
evidence. That projection remains derived candidate evidence and does not change smoothing outputs
into object truth or tennis-event conclusions.

## Observation Types

### smoothed_ball_position_candidate

Family: `tracking`

The ball smoother prefers `track_point_candidate` rows from a selected ball tracklet run. If no
tracklet source is available, it can use raw `ball_detection` rows from a detection run.

The v0 method is `rolling_median_no_long_gap_interpolation_v0`:

- rolling median over a configurable frame window
- no synthetic points across long gaps
- source observation ids preserved in payload and lineage

### smoothed_main_player_box_candidate

Family: `tracking`

The player-box smoother consumes accepted `main_player_track_assignment_candidate` rows. It smooths
bbox center, width, and height independently per near/far visual track role.

The v0 method is `exponential_moving_average_bbox_v0`:

- per-track-role EMA
- configurable alpha
- reset after a configurable frame gap
- source track assignment preserved in payload and lineage

### smoothed_pose_candidate

Family: `pose`

The pose smoother consumes `player_pose_observation` rows, preferring pose observations that already
carry main-player track context.

The v0 method is `per_keypoint_ema_v0`:

- per-track-role or per-subject keypoint EMA
- only smooths present keypoints
- does not invent missing keypoints across gaps
- source pose observation preserved in payload and lineage

## CLI

```bash
.venv/bin/python -m apps.worker.cli smooth-motion-candidates \
  --media-id <media_id> \
  --detection-run-id <detection_run_id> \
  --tracklet-run-id <tracklet_run_id> \
  --main-player-track-run-id <main_player_track_run_id> \
  --pose-run-id <pose_run_id>
```

Inputs are optional by layer. If a pose run is missing, pose smoothing is skipped. If a main player
track run is missing, player-box smoothing is skipped. If a tracklet run is missing, ball smoothing
falls back to ball detections when a detection run is supplied.

The command returns `motion_smoothing_run_id` and a replay URL using:

```text
motionSmoothingRunId=<motion_smoothing_run_id>
```

## Replay

Replay supports these layers:

- `smoothed_ball`
- `smoothed_player_boxes`
- `smoothed_pose`

When a `motionSmoothingRunId` is selected, the workstation defaults the smoothed layers on and raw
detection/tracklet/pose layers off. Operators can still toggle raw evidence back on for audit.

The smoothed motion display mode defaults to `current_only`:

- one nearest current `smoothed_ball_position_candidate`
- at most one `smoothed_main_player_box_candidate` per near/far track role
- at most one `smoothed_pose_candidate` per track candidate/role

`short_trail` and `full_trail` remain debug display modes. They can show multiple neighboring
smoothed candidates, with labels reserved for the current selected candidate to reduce visual clutter.

Selected smoothed evidence shows:

- smoothing method
- source run ids where available
- source observation count
- track candidate id/role for player boxes and poses
- observation-only and no-adjudication warnings

## Lineage

Relationship types:

- `smoothed_from_ball_detection`
- `smoothed_from_track_point_candidate`
- `smoothed_from_main_player_track_assignment`
- `smoothed_from_pose_observation`

Lineage is source evidence context, not correctness proof.

## Non-Goals

This milestone does not add:

- bounce detection
- hit detection
- in/out decisions
- confirmed ball/player court-space projection truth
- player identity
- server/receiver logic
- scoreboard OCR
- rally/point/score logic
- accepted/rejected truth lifecycle
- adjudication
