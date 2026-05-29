# Object-to-Court Projection Candidates v0

Status: implemented

This bridge creates derived court-template coordinate candidates from existing image-space
evidence and existing homography candidates.

```text
smoothed_ball_position_candidate
+ homography_candidate_observation
-> ball_court_projection_candidate

smoothed_main_player_box_candidate
+ homography_candidate_observation
-> main_player_court_projection_candidate
```

Raw detections, smoothed candidates, player track assignments, court keypoints, homography
candidates, and projection diagnostics remain immutable. The new rows are derived candidate
evidence only.

## Coordinate Space

The v0 target coordinate space is `court_template_2d` using the existing normalized tennis court
template semantics. Coordinates are stored as normalized template points and must not be read as
true ball or player positions.

## Projection Method

Ball projection uses the smoothed ball image center:

```text
projection_method = homography_image_pixels_to_court_template_2d_v0
```

Main-player projection uses the bottom center of the smoothed main-player bbox:

```text
projection_method = bbox_bottom_center_homography_projection_v0
```

The bbox bottom center is only a candidate image anchor. It is not a confirmed foot contact point or
player position truth.

## Homography Matching

For each source object candidate, v0 chooses a homography candidate using:

1. exact frame match
2. latest prior homography within `homography_max_gap_ms`
3. nearest homography within `homography_max_gap_ms`
4. skip if no usable candidate exists

The default max gap is `1500` ms. Payloads preserve `homography_match_policy`,
`homography_time_delta_ms`, and `homography_carried_forward`.

## CLI

```bash
.venv/bin/python -m apps.worker.cli project-objects-to-court \
  --media-id <media_id> \
  --motion-smoothing-run-id <motion_smoothing_run_id> \
  --homography-run-id <homography_run_id> \
  --homography-max-gap-ms 1500
```

Makefile helper:

```bash
make tom-v1-object-court-projection \
  MEDIA_ID=<media_id> \
  MOTION_SMOOTHING_RUN_ID=<motion_smoothing_run_id> \
  HOMOGRAPHY_RUN_ID=<homography_run_id> \
  PYTHON=.venv/bin/python
```

The command returns `court_projection_run_id` and a replay URL with:

```text
courtProjectionRunId=<court_projection_run_id>
```

## Replay

Replay supports:

- `courtProjectionRunId`
- `ball_court_projection`
- `main_player_court_projection`
- a `court_projection` timeline lane
- a normalized court-template mini-map panel

The mini-map labels points as `BALL CANDIDATE`, `NEAR PLAYER CANDIDATE`, and
`FAR PLAYER CANDIDATE`. It intentionally does not draw these court-template coordinates over the
broadcast video.

Operator view presets keep the mini-map visible when `courtProjectionRunId` is present while hiding
homography and projection-diagnostic debug overlays by default. Debug/audit view can re-enable those
raw geometry layers for inspection.

## Lineage

Relationship types:

- `projected_from_smoothed_ball_position`
- `projected_from_smoothed_main_player_box`
- `projected_with_homography_candidate`

Lineage records the source evidence used for projection. It is not correctness proof.

## Non-Goals

This milestone does not add:

- bounce detection
- hit detection
- in/out decisions
- rally, point, or score logic
- player identity
- scoreboard OCR
- server/receiver logic
- accepted/rejected court or projection lifecycle
- adjudication

Court projection candidates are prerequisites for future event-candidate work, not event truth.

Ball Trajectory Court Candidate v0 consumes `ball_court_projection_candidate` rows to build
`ball_trajectory_court_candidate` segments with velocity, direction, gap, and carry-forward
diagnostics. That downstream layer remains candidate evidence; it does not infer bounce, hit,
in/out, point, or score.
