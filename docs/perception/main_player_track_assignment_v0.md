# Main Player Track Assignment v0.1

This document describes the TOM v3 main player track assignment repair bridge.

## Purpose

TOM v1 player detection can produce many `player_detection` observations in a broadcast frame. The main tennis-player subject filter reduces that set to frame-local `near_player_candidate` and `far_player_candidate` rows, but those rows can still briefly jump to a ball kid, line judge, or wall-side person.

Main player track assignment v0.1 adds persistent candidate visual tracks for the two primary tennis-player subjects:

- `near_player_track_candidate`
- `far_player_track_candidate`

These are candidate visual tracks only. They are not player identity truth, player names, server/receiver conclusions, side-change logic, or accepted tracks.

## Evidence Flow

```text
real player detections
-> main_player_subject_candidate rows
-> main_player_track_candidate rows
-> main_player_track_assignment_candidate rows
-> run-real-pose --source-track-run-id
-> player_pose_observation rows linked to accepted track assignment candidates
```

Raw `player_detection` observations remain persisted and inspectable. The assignment layer does not mutate or delete detections.

## Observation Types

`main_player_track_candidate`

Track-level candidate observation under `observation_family = tracking`. It summarizes one candidate visual track over a frame range and includes:

- `track_role_candidate`
- `track_candidate_id`
- source detection and subject run ids
- frame/time range
- assignment score summary
- `candidate_track_only`
- `not_identity_truth`
- `observation_only`
- `no_adjudication`

`main_player_track_assignment_candidate`

Per-frame assignment observation under `observation_family = tracking`. It links one accepted frame-local subject candidate and source detection to a persistent track candidate.

## Lineage

The assignment preserves:

```text
player_detection
-> main_player_subject_candidate
-> main_player_track_assignment_candidate
-> player_pose_observation
```

Per-frame assignments also link to the track-level candidate observation. Pose rows generated with `--source-track-run-id` include track metadata such as `track_candidate_id`, `track_role_candidate`, and `track_assignment_observation_id`.

## v0.1 Locking Heuristic

v0.1 keeps the near/far role split from the subject filter, then adds a light persistent track lock:

- seed each role from a strong, plausible, non-edge candidate
- compare later candidates to the previous accepted assignment
- reject large normalized center jumps
- reject large bbox-area changes
- apply an edge/wall penalty, especially for upper-right or wall-side far-player candidates
- allow gaps instead of forcing an assignment every frame

This is still a candidate source selector for cleaner pose. It is not a tracker truth engine.

The current method identifier is `main_player_track_assignment_v01`. The default run name is `main-player-track-assignment-v01`.

## Replay Labels

Replay overlay payloads can expose `main_player_track_assignment_candidate` rows through the `main_player_tracks` layer. When `mainPlayerTrackRunId=<run_id>` is present, the workstation can show selectable labels:

- `NEAR TRACK`
- `FAR TRACK`

The selected detail panel shows the track candidate id, role candidate, assignment score, assignment method, source subject candidate observation id, source detection observation id, and evidence-only warnings.

These visible labels are candidate labels only. They do not identify players.

## Runbook

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli assign-main-player-tracks \
  --media-id <media_id> \
  --source-detection-run-id <player_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --run-name main-player-track-assignment-v01 \
  --max-frames 214 \
  --every-n-frames 1
```

Then run pose from those candidate tracks:

```bash
TOM_V3_DATABASE_URL=sqlite+pysqlite:///./tmp_tom_v3_tom_v1_bridge.db \
.venv/bin/python -m apps.worker.cli run-real-pose \
  --media-id <media_id> \
  --source-detection-run-id <player_detection_run_id> \
  --source-subject-run-id <main_subject_run_id> \
  --source-track-run-id <main_player_track_run_id> \
  --weights model_assets/tom_v1/yolo26x-pose.pt \
  --model-name tom-v1-yolo26x-pose \
  --model-version v1-local \
  --mode crop_from_player_detection \
  --device auto \
  --imgsz 640 \
  --every-n-frames 1 \
  --max-frames 214 \
  --conf 0.25 \
  --allowed-root model_assets/tom_v1
```

Open replay with:

```text
/replay/<media_id>?detectionRunId=<player_detection_run_id>&trackletRunId=<player_tracklet_run_id>&subjectRunId=<main_subject_run_id>&mainPlayerTrackRunId=<main_player_track_run_id>&poseRunId=<track_filtered_pose_run_id>
```

## Non-goals

- no confirmed player identity
- no player names
- no server/receiver truth
- no scoreboard OCR
- no side-change identity logic
- no bounce/hit/in-out/rally/point/scoring
- no ball/player court-space projection
- no accepted/rejected lifecycle
- no raw detection mutation
