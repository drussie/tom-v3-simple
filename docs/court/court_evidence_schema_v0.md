# Court Evidence Schema v0

Milestone 8A starts Blueprint 8 with schema and persistence contracts. Milestone 8B uses this schema through a deterministic fixture court evidence adapter. Milestone 8C exposes camera/view rows as read models. Milestone 8D persists homography candidate rows from source court evidence.

Blueprint 8 court evidence uses the existing TOM observation spine:

```text
observation row
-> typed court evidence row
-> optional lineage rows
-> optional artifacts / annotations
```

No parallel evidence store is introduced.

## Observation Family

```text
observation_family = court
```

Typed court observation types:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`
- `homography_candidate_observation`
- `projection_diagnostic_observation`

All court observations preserve:

- media-owned frame/time
- `frame_time_owner = media_indexing`
- `observation_only = true`
- `no_adjudication = true`
- `geometry_evidence_only = true`

## Court Keypoint Observation

Table:

```text
court_keypoint_observation
```

Key fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `court_keypoint_schema = tennis_court_v0`
- `schema_version = v0`
- `keypoints_jsonb`
- `keypoint_count`
- `keypoints_present_count`
- `keypoints_missing_count`
- `mean_keypoint_confidence`
- `min_keypoint_confidence`
- `max_keypoint_confidence`
- `coordinate_space = image_pixels`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `raw_model_payload_jsonb`
- `metadata_jsonb`

V0 keypoint names:

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

Keypoints may be present or missing. Missing keypoints remain missing evidence and are not inferred.

## Court Line Observation

Table:

```text
court_line_observation
```

Key fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `line_segments_jsonb`
- `line_classes_jsonb`
- `line_count`
- `mean_line_confidence`
- `coordinate_space = image_pixels`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `raw_model_payload_jsonb`
- `metadata_jsonb`

V0 line classes:

- `baseline_near`
- `baseline_far`
- `sideline_left`
- `sideline_right`
- `service_line_near`
- `service_line_far`
- `center_service_line`
- `net_line`
- `unknown_court_line`

Visibility values:

- `visible`
- `partial`
- `occluded`
- `inferred_by_adapter`
- `unknown`

## Camera / View Observation

Table:

```text
camera_view_observation
```

Key fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `frame_start`
- `frame_end`
- `timestamp_start_ms`
- `timestamp_end_ms`
- `view_label`
- `view_confidence`
- `camera_motion_hint`
- `stability_score`
- `cut_likelihood`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `metadata_jsonb`

V0 view labels:

- `broadcast_hardcam`
- `behind_baseline`
- `side_view`
- `closeup`
- `replay_overlay`
- `non_gameplay`
- `unknown`

Camera motion hints:

- `stable`
- `panning`
- `zooming`
- `camera_cut`
- `unknown`

## Homography Candidate Observation

Table:

```text
homography_candidate_observation
```

Key fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `source_court_keypoint_observation_id`
- `source_court_line_observation_id`
- `source_camera_view_observation_id`
- `homography_matrix_jsonb`
- `inverse_homography_matrix_jsonb`
- `source_coordinate_space = image_pixels`
- `target_coordinate_space = court_template_2d`
- `matrix_direction`
- `template_name`
- `template_version`
- `reprojection_error_mean`
- `reprojection_error_median`
- `reprojection_error_max`
- `inlier_count`
- `outlier_count`
- `source_point_count`
- `source_line_count`
- `confidence`
- `status`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `metadata_jsonb`

V0 candidate statuses:

- `candidate`
- `insufficient_source_evidence`
- `adapter_failed`
- `not_computed`

There is no accepted, rejected, or verified status.

Matrix directions:

- `image_pixels_to_court_template_2d`
- `court_template_2d_to_image_pixels`

## Projection Diagnostic Observation

Table:

```text
projection_diagnostic_observation
```

Key fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `source_homography_candidate_observation_id`
- `projected_template_keypoints_jsonb`
- `projected_template_lines_jsonb`
- `diagnostic_metrics_jsonb`
- `overlay_artifact_id`
- `confidence`
- `status`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `metadata_jsonb`

V0 diagnostic statuses:

- `diagnostic_candidate`
- `insufficient_homography`
- `adapter_failed`
- `not_computed`

Projection diagnostics are for court template evidence only. They do not project ball/player detections into court space.

## Lineage Contract

V0 relationship types:

- `homography_from_court_keypoints_candidate`
- `homography_from_court_lines_candidate`
- `camera_context_for_homography_candidate`
- `projection_diagnostic_for_homography_candidate`

Lineage examples:

```text
court_keypoint_observation
-> homography_candidate_observation
relationship_type = homography_from_court_keypoints_candidate
```

```text
court_line_observation
-> homography_candidate_observation
relationship_type = homography_from_court_lines_candidate
```

```text
camera_view_observation
-> homography_candidate_observation
relationship_type = camera_context_for_homography_candidate
```

```text
homography_candidate_observation
-> projection_diagnostic_observation
relationship_type = projection_diagnostic_for_homography_candidate
```

## Review Labels

Future review labels may include:

- `likely_good_court_keypoint`
- `bad_court_keypoint`
- `missing_court_keypoint`
- `wrong_court_keypoint_label`
- `uncertain_court_keypoint`
- `likely_good_court_line`
- `bad_court_line`
- `wrong_line_class`
- `line_occluded`
- `uncertain_court_line`
- `likely_good_homography_candidate`
- `bad_homography_candidate`
- `bad_projection`
- `unstable_camera_view`
- `insufficient_court_evidence`
- `uncertain_homography`

Annotations remain non-mutating review evidence.

## Export Contract

Future TOM-native court review exports should include:

- media/frame/time
- model/runtime/config
- source keypoints/lines/camera evidence
- homography candidate matrix
- projection diagnostics
- lineage
- artifacts
- annotations

No export should promote court evidence into bounce, hit, in/out, rally, point, or scoring conclusions.

## Camera / View Read Layer

8C exposes `camera_view_observation` rows through read-only query, summary, and evidence-bundle services. The summary can count view labels and camera motion hints and report confidence/stability/cut metrics.

Camera/view summaries are geometry context evidence. They do not confirm camera state or homography validity.

## Non-goals

8B writes fixture `court_keypoint_observation`, `court_line_observation`, and `camera_view_observation` rows with `fixture_court_evidence = true` and `not_real_court_model = true`. 8C exposes camera/view rows through read models.

8D writes `homography_candidate_observation` rows from persisted court keypoint evidence and optional court line/camera-view context. These candidates preserve source lineage and remain candidate geometry evidence.

8D does not add a real court/runtime model, projection diagnostics, replay court overlay, ball/player court projection, stream ingestion, or tennis-event interpretation.
