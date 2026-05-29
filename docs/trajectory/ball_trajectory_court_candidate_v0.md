# Ball Trajectory Court Candidate v0

Status: implemented

Ball Trajectory Court Candidate v0 derives a court-template trajectory candidate from persisted
`ball_court_projection_candidate` observations.

The pipeline is:

```text
ball_court_projection_candidate rows
-> ordered media-frame sequence
-> gap-segmented trajectory candidate
-> velocity/direction/gap diagnostics
-> ball_trajectory_court_candidate
```

## Observation

The builder persists generic observation-spine rows:

- `observation_family = trajectory`
- `observation_type = ball_trajectory_court_candidate`
- `granularity = segment`
- `coordinate_space = court_template_2d`

The payload includes:

- `source_court_projection_run_id`
- `source_ball_court_projection_observation_ids`
- `trajectory_segment_index`
- start/end frame and timestamp
- ordered court-template points
- per-step kinematic diagnostics
- gap, bounds, and homography carry-forward diagnostics
- evidence-only warnings

## Segmentation

The v0 segmentation is deterministic:

- sort by `timestamp_ms`, `frame_number`, and `observation_id`
- split when frame gap or time gap exceeds configured thresholds
- drop segments shorter than `min_points_per_segment`
- do not interpolate
- do not apply a physics model

Defaults:

- `max_gap_frames = 6`
- `max_gap_ms = 250`
- `min_points_per_segment = 3`

## Diagnostics

For consecutive trajectory points, v0 computes:

- `dt_ms`
- `dx`
- `dy`
- `speed_template_units_per_second`
- `direction_angle_degrees`

The run also reports:

- source point count
- segment count
- dropped short segment count
- gap split count
- out-of-template count
- homography carried-forward count

These are trajectory diagnostics only. They are not event inference.

## Replay

Replay accepts:

```text
ballTrajectoryRunId=<ball_trajectory_run_id>
```

The replay overlay layer is:

```text
ball_court_trajectory
```

The court projection mini-map can draw a subtle `BALL TRAJECTORY CANDIDATE` path alongside current
ball and main-player projection candidates. The timeline includes a `ball_trajectory` lane.

Downstream event-candidate work may consume `ball_trajectory_court_candidate` rows to propose
`hit_candidate` and `bounce_candidate` markers. Those markers remain derived candidate evidence;
they do not convert the trajectory into bounce, hit, in/out, point, or score truth.

## Boundaries

The trajectory is derived candidate evidence. It is not:

- true ball position
- bounce truth
- hit truth
- in/out truth
- rally, point, or score logic
- adjudication

Raw detections, smoothed ball candidates, court projection candidates, and homography candidates are
not mutated.
