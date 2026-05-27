# Court Template Registry v0

Milestone 8A introduces the first court template registry for Blueprint 8 geometry evidence.

Milestone 8B uses this template registry to generate deterministic fixture court keypoint and line evidence in image-pixel coordinates.

## Template

```text
template_name = tennis_court_template_normalized_v0
template_version = v0
target_coordinate_space = court_template_2d
```

The v0 template is normalized, not real-dimensioned. It is meant to provide a stable target coordinate contract for future homography candidates and projection diagnostics.

## Keypoints

The v0 template uses the same keypoint names as `tennis_court_v0` court keypoint observations:

- `near_left_baseline_corner`
- `near_right_baseline_corner`
- `far_left_baseline_corner`
- `far_right_baseline_corner`
- `left_net_post`
- `right_net_post`
- `service_line_t_near_left`
- `service_line_t_near_right`
- `service_line_t_far_left`
- `service_line_t_far_right`
- `center_mark_near`
- `center_mark_far`

Normalized examples:

```text
near_left_baseline_corner = [0.0, 0.0]
near_right_baseline_corner = [1.0, 0.0]
far_left_baseline_corner = [0.0, 1.0]
far_right_baseline_corner = [1.0, 1.0]
```

## Lines

The v0 template defines:

- `baseline_near`
- `baseline_far`
- `sideline_left`
- `sideline_right`
- `service_line_near`
- `service_line_far`
- `center_service_line`
- `net_line`

`unknown_court_line` is valid for observations, but it is not a template line.

## Boundary

The template is a geometry evidence contract. It does not create in/out logic, bounce locations, player court-position conclusions, scoring, or adjudication.
