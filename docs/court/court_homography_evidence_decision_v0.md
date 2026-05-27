# Court / Homography Evidence Decision v0

## Decision

Court / camera / homography evidence should be deferred to Blueprint 8.

Blueprint 7 closes after real detection, real-detection-derived candidate tracklets, real pose keypoint evidence, this decision gate, and the 7F perception orchestration completion review.

## Rationale

Blueprint 7 activates real perception for the replay workstation. Real detections, candidate tracklets derived from real detections, and real pose keypoint observations are enough to make the workstation show model-output evidence over indexed media.

Court and homography work introduces a distinct geometry domain:

- court keypoint evidence
- court line evidence
- camera/view evidence
- homography candidates
- projection diagnostics
- optional court-space coordinate transform candidates

That domain needs its own schema design, confidence model, replay overlays, review labels, diagnostics, exports, and invariants. Implementing it inside Blueprint 7 would blur the boundary between perception evidence and later tennis-event layers.

## Boundary

Court evidence should mean:

```text
adapter or model output
-> media-owned frame/time
-> persisted court/camera/geometry observation
-> lineage and diagnostics
-> replayable evidence
```

Court evidence should not mean:

- bounce location
- hit event
- in/out conclusion
- player court-position conclusion
- ball court-position conclusion
- rally, point, or score
- adjudication

## Future Observation Family

Future Blueprint 8 should introduce or formalize:

```text
observation_family = court
```

Potential future observation types:

- `court_keypoint_observation`
- `court_line_observation`
- `camera_view_observation`
- `homography_candidate_observation`
- `projection_diagnostic_observation`

7E does not add these to code or database schema.

## Court Keypoint Observation Contract

Proposed future typed row:

```text
court_keypoint_observation
```

Fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `court_keypoint_schema`
- `keypoints_jsonb`
- `keypoint_count`
- `keypoints_present_count`
- `mean_keypoint_confidence`
- `coordinate_space = image_pixels`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `raw_model_payload_jsonb`
- `metadata_jsonb`
- `created_at`

Potential keypoint names:

- `near_left_baseline_corner`
- `near_right_baseline_corner`
- `far_left_baseline_corner`
- `far_right_baseline_corner`
- `left_net_post`
- `right_net_post`
- `service_line_t`
- `center_mark_near`
- `center_mark_far`

## Court Line Observation Contract

Proposed future typed row:

```text
court_line_observation
```

Fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `line_segments_jsonb`
- `line_class`
- `confidence`
- `coordinate_space = image_pixels`
- `model_id`
- `runtime_config_id`
- `frame_time_owner = media_indexing`
- `metadata_jsonb`

Potential line classes:

- `baseline_near`
- `baseline_far`
- `sideline_left`
- `sideline_right`
- `service_line_near`
- `service_line_far`
- `center_service_line`
- `net_line`

## Camera / View Observation Contract

Proposed future typed row:

```text
camera_view_observation
```

Fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `view_label`
- `view_confidence`
- `camera_motion_hint`
- `stability_score`
- `metadata_jsonb`

Potential labels:

- `broadcast_hardcam`
- `behind_baseline`
- `side_view`
- `closeup`
- `replay_overlay`
- `non_gameplay`
- `unknown`

## Homography Candidate Observation Contract

Proposed future typed row:

```text
homography_candidate_observation
```

Fields:

- `observation_id`
- `media_id`
- `run_id`
- `frame_number`
- `timestamp_ms`
- `source_court_keypoint_observation_id`
- `source_court_line_observation_id`
- `homography_matrix_jsonb`
- `source_coordinate_space = image_pixels`
- `target_coordinate_space = court_template_2d`
- `template_name`
- `template_version`
- `reprojection_error`
- `inlier_count`
- `confidence`
- `status = candidate`
- `frame_time_owner = media_indexing`
- `metadata_jsonb`

A homography candidate is a candidate coordinate transform derived from source court evidence. It is not a final court model.

## Future Lineage Contract

Potential lineage relationships:

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
homography_candidate_observation
-> projection_diagnostic_observation
relationship_type = projection_diagnostic_for_homography_candidate
```

Future projection evidence should remain candidate evidence:

```text
ball_detection observation
+ homography_candidate_observation
-> ball_court_projection_candidate
```

7E does not implement projection evidence.

## Future Replay Workstation Integration

Potential future overlay layers:

- Court keypoint overlay
- Court line overlay
- Homography candidate overlay
- Projection diagnostic overlay

Future UI labels:

- Court keypoint evidence
- Court line evidence
- Homography candidate
- Projection diagnostic

Avoid labels that imply a final court model, in/out result, bounce location, or court conclusion.

Suggested future controls:

- Show court evidence
- Show homography candidate
- Show projection diagnostics
- Confidence threshold
- Selected court evidence detail

Selected detail should show:

- observation id
- run id
- model/runtime/config
- frame/time
- source keypoints/lines
- matrix
- confidence
- reprojection error
- lineage
- annotations
- warning that this is candidate geometry evidence only

## Future Review Labels

Court keypoint review labels:

- `likely_good_court_keypoint`
- `bad_court_keypoint`
- `missing_court_keypoint`
- `wrong_court_keypoint_label`
- `uncertain_court_keypoint`

Court line review labels:

- `likely_good_court_line`
- `bad_court_line`
- `wrong_line_class`
- `line_occluded`
- `uncertain_court_line`

Homography review labels:

- `likely_good_homography_candidate`
- `bad_homography_candidate`
- `bad_projection`
- `unstable_camera_view`
- `insufficient_court_evidence`
- `uncertain_homography`

Annotations remain non-mutating review evidence.

## Future Exports

Potential TOM-native export record types:

- `court_keypoint_observation_review`
- `court_line_observation_review`
- `homography_candidate_review`
- `projection_diagnostic_review`

Exports should include:

- media/frame/time
- model/runtime/config
- source keypoints/lines
- homography candidate matrix
- diagnostics
- lineage
- artifacts
- annotations

## Risks And Tradeoffs

Risk: Court geometry can be mistaken for a final geometry model too early.

Mitigation: use candidate, evidence, and observation language; preserve review and lineage.

Risk: Homography quality depends on camera view.

Mitigation: persist camera/view evidence and confidence; avoid using geometry candidates on closeups and non-gameplay views.

Risk: Broadcast overlays and cuts can disrupt court inference.

Mitigation: make camera/view state explicit and preserve failure/uncertain states.

Risk: Projection into court space invites bounce/hit interpretation.

Mitigation: projection candidates are not bounce or hit events. Bounce/hit candidates require future separate blueprints.

Risk: Schema creep.

Mitigation: keep Blueprint 8 narrowly focused on court/camera/homography evidence.

Risk: Performance and visual clutter.

Mitigation: replay layers should be toggleable and confidence-filtered.

## 7E Non-Implementation Statement

7E adds no runtime, database migration, API endpoint, detector, court overlay, homography computation, coordinate transform service, tennis-event interpretation, or stream ingestion.

Milestone 7F preserves this boundary while marking Blueprint 7 complete. Court/camera/homography evidence remains a Blueprint 8 candidate, not a hidden extension of Blueprint 7.
