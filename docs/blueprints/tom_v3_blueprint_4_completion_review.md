# TOM v3 Blueprint 4 Completion Review

## Verdict

Blueprint 4 Status: COMPLETE

Blueprint 4 is complete enough to close. It proved that TOM v3 can persist pose model output as observation evidence using a first-class pose observation schema, COCO17 skeleton registry, keypoint validation, normalization, processing-run persistence, source-evidence lineage, viewer overlay, pose-specific query filters, review annotation support, evidence bundles, and TOM-native review dataset export.

Blueprint 4 did not add real pose inference, movement interpretation, stroke classification, serve/hit/split-step/biomechanics analysis, homography, bounce detection, hit detection, rally/point/scoring, or adjudication.

## What Blueprint 4 Proves

Blueprint 4 proves this path:

```text
pose schema
-> skeleton registry
-> fake / serialized pose normalization
-> fixture pose processing run
-> persisted pose observation
-> source candidate lineage
-> viewer overlay
-> pose query
-> review annotation support
-> TOM-native review export
```

The path is durable and observation-only. A pose row records keypoint evidence at a media-owned frame/time. It does not identify a player, interpret movement, or create tennis-event conclusions.

## What Blueprint 4 Does Not Prove

Blueprint 4 does not prove that pose keypoints are correct.

It does not prove identity, player action, serve mechanics, split-step timing, biomechanics, homography, bounce, hit, rally state, point state, score state, or any official result. It does not load a real pose model or run Ultralytics pose inference.

## Completion Questions

1. Is Blueprint 4 complete enough to close?
   Yes. The schema, normalization, persistence, lineage, viewer, query, review, export, docs, and tests are in place for fixture/fake pose evidence.

2. What exactly does Blueprint 4 prove?
   It proves TOM v3 can store, replay, inspect, query, annotate, and export pose keypoint evidence as observations.

3. What does Blueprint 4 intentionally not prove?
   It does not prove keypoint correctness, subject identity, movement meaning, tennis events, scoring, or any official result.

4. Does pose remain observation-only?
   Yes. Pose data is stored as keypoint evidence with source/runtime/provenance context.

5. Does the pose schema preserve media-owned frame/time?
   Yes. Pose frame/time fields mirror the observation spine and use `frame_time_owner = media_indexing`.

6. Does the COCO17 skeleton registry define keypoints and edges consistently?
   Yes. The registry defines 17 named keypoints, ordered indices, and edges that reference valid names.

7. Do pose observations store full keypoint evidence?
   Yes. The typed row stores full `keypoints_jsonb`; the observation payload stores a compact summary.

8. Do pose observations support missing keypoints without inference?
   Yes. Missing keypoints persist as `present = false` with null coordinates.

9. Does pose normalization avoid smoothing/repairing/interpreting keypoints?
   Yes. The normalizer validates and transforms coordinates only. It does not smooth, repair, or interpret movement.

10. Does crop projection preserve full-frame image-pixel coordinates?
    Yes. Crop-local coordinates are projected by adding crop origin, and crop-local values are preserved in metadata.

11. Does pose persistence create processing_run and processing_step provenance?
    Yes. The fixture pose worker path creates both.

12. Does pose persistence write through ObservationWriter?
    Yes. The service writes observation spine rows and typed pose rows through `ObservationWriter`.

13. Does pose lineage link to source player_detection where supplied?
    Yes. It writes `pose_from_subject_detection_candidate` lineage from source player detections.

14. Does pose lineage support tracklet/track point context where supplied?
    Yes. Candidate tracklet and track point context lineage is supported and tested.

15. Does the viewer render pose evidence without movement interpretation?
    Yes. It renders persisted keypoints, skeleton edges, bbox context, and candidate source context only.

16. Does the viewer show keypoint evidence and missing keypoints correctly?
    Yes. Present keypoints render; missing keypoints appear in the table and are not drawn as present markers.

17. Does pose query support typed pose filters?
    Yes. Filters include run/media/frame/time, confidence, missing count, skeleton format, and association fields.

18. Does pose evidence bundle expose pose/source/lineage/artifact/annotation context?
    Yes. The bundle composes those rows without creating new state.

19. Do pose annotations remain non-mutating review evidence?
    Yes. Pose annotations use `human_annotation` and do not mutate pose/source observations.

20. Does pose export preserve TOM-native keypoint evidence, lineage, context, annotations, and artifacts?
    Yes. Export records include full keypoints, subject context, lineage, artifacts, annotations, warnings, artifact metadata, and query result memory where applicable.

21. Is real pose inference still out of scope?
    Yes.

22. Is movement interpretation still out of scope?
    Yes.

23. Is homography still out of scope?
    Yes.

24. Is bounce/hit/rally/point/scoring still out of scope?
    Yes.

25. Is the next blueprint boundary clear?
    Yes. Recommended next blueprint: Blueprint 5 - TOM v3 Simple Completion / Product Hardening.

## Invariant Audit

| Invariant | Status | Coverage |
| --- | --- | --- |
| COCO17 skeleton registry has 17 keypoints | Covered | `tests/test_pose_schema.py::test_coco17_skeleton_registry_exists` |
| COCO17 skeleton edges reference valid keypoints | Covered | `tests/test_pose_schema.py::test_coco17_edges_reference_valid_keypoints` |
| Pose keypoint schema validation rejects wrong count | Covered | `tests/test_pose_schema.py::test_keypoint_schema_validation_fails_for_wrong_count` |
| Pose keypoint schema validation rejects wrong name/index | Covered | `tests/test_pose_schema.py::test_keypoint_schema_validation_fails_for_bad_name_or_index` |
| Pose observation table exists | Covered | `tests/test_pose_observation_persistence.py::test_pose_observation_table_exists` |
| Pose observation has observation spine row | Covered | `tests/test_pose_observation_persistence.py::test_synthetic_pose_observation_persists_typed_row_and_spine` |
| `observation_family = pose` | Covered | `tests/test_pose_observation_persistence.py::test_synthetic_pose_observation_persists_typed_row_and_spine` and `tests/test_pose_persistence_lineage.py::test_pose_processing_service_persists_unassociated_fixture_poses` |
| `observation_type = player_pose_observation` | Covered | `tests/test_pose_observation_persistence.py::test_synthetic_pose_observation_persists_typed_row_and_spine` |
| `frame_time_owner = media_indexing` | Covered | `tests/test_pose_observation_persistence.py::test_synthetic_pose_observation_persists_typed_row_and_spine` |
| Pose frame/time equals observation frame/time | Covered | `tests/test_pose_observation_persistence.py::test_synthetic_pose_observation_persists_typed_row_and_spine` and `tests/test_pose_persistence_lineage.py::test_pose_processing_service_links_to_source_player_detection` |
| Missing keypoints persist as `present = false` | Covered | `tests/test_pose_normalization.py::test_missing_keypoints_remain_missing_evidence` |
| Pose normalization assigns COCO17 names/indices | Covered | `tests/test_pose_normalization.py::test_full_frame_pose_normalizes_to_pose_create_compatible_payload` |
| Pose normalization computes x_norm/y_norm | Covered | `tests/test_pose_normalization.py::test_full_frame_pose_normalizes_to_pose_create_compatible_payload` |
| Pose normalization handles invalid bbox without crashing | Covered | `tests/test_pose_normalization.py::test_invalid_bbox_records_warning_but_keeps_keypoints` |
| Pose normalization skips invalid keypoint count | Covered | `tests/test_pose_normalization.py::test_invalid_keypoint_count_skips_pose_with_warning` |
| Pose normalization supports crop-to-full-frame projection | Covered | `tests/test_pose_normalization.py::test_crop_local_keypoints_project_to_full_frame_coordinates` |
| Pose normalization supports subject association candidate passthrough | Covered | `tests/test_pose_normalization.py::test_subject_association_candidate_fields_pass_through` |
| Pose processing service creates processing_run | Covered | `tests/test_pose_persistence_lineage.py::test_pose_processing_service_persists_unassociated_fixture_poses` |
| Pose processing service creates processing_step | Covered | `tests/test_pose_persistence_lineage.py::test_pose_processing_service_persists_unassociated_fixture_poses` |
| Pose processing service persists typed pose rows via ObservationWriter | Covered | `tests/test_pose_persistence_lineage.py::test_pose_processing_service_persists_unassociated_fixture_poses` |
| Unassociated full-frame pose persists with no lineage | Covered | `tests/test_pose_persistence_lineage.py::test_pose_processing_service_persists_unassociated_fixture_poses` |
| Source player_detection linked pose creates `pose_from_subject_detection_candidate` lineage | Covered | `tests/test_pose_persistence_lineage.py::test_pose_processing_service_links_to_source_player_detection` |
| Tracklet / track_point context lineage is supported | Covered | `tests/test_pose_persistence_lineage.py::test_pose_processing_service_links_candidate_tracklet_and_track_point_context` |
| Invalid explicit source id fails clearly | Covered | `tests/test_pose_persistence_lineage.py::test_invalid_explicit_source_detection_id_fails_without_pose_rows` |
| Viewer payload includes pose detail | Covered | `tests/test_pose_persistence_lineage.py::test_viewer_payload_includes_pose_detail_for_overlay` |
| Pose overlay extracts present keypoints | Covered | `apps/web/src/lib/poses.ts` and Milestone 4D viewer contract validation |
| Missing keypoints are not rendered as present markers | Covered | `apps/web/src/lib/poses.ts`, `apps/web/src/components/PoseOverlayCanvas.tsx`, and Milestone 4D viewer contract validation |
| Skeleton edges render only when both endpoints are present | Covered | `apps/web/src/lib/poses.ts`, `apps/web/src/components/PoseOverlayCanvas.tsx`, and Milestone 4D viewer contract validation |
| Keypoint table includes all 17 keypoints | Covered | `apps/web/src/components/PoseOverlayPanel.tsx` and Milestone 4D viewer contract validation |
| Source association context uses candidate/evidence language | Covered | `apps/web/src/components/PoseOverlayPanel.tsx` and docs review |
| Pose query filters by run/media/frame/confidence/missing count/skeleton/association | Covered | `tests/test_pose_query_review_export.py::test_pose_query_filters_and_annotation_summary` |
| Pose evidence bundle includes pose, source context, lineage, artifacts, annotations | Covered | `tests/test_pose_query_review_export.py::test_pose_evidence_bundle_includes_lineage_source_and_annotation` |
| Pose annotations do not mutate pose observations | Covered | `tests/test_pose_query_review_export.py::test_pose_annotation_does_not_mutate_pose_observation` |
| Keypoint-level annotation metadata is supported | Covered | `tests/test_pose_query_review_export.py::test_pose_annotation_does_not_mutate_pose_observation` |
| Pose review export includes keypoints | Covered | `tests/test_pose_query_review_export.py::test_pose_review_export_creates_artifact_query_result_and_tom_native_json` |
| Pose review export includes subject context | Covered | `tests/test_pose_query_review_export.py::test_pose_review_export_creates_artifact_query_result_and_tom_native_json` |
| Pose review export includes lineage | Covered | `tests/test_pose_query_review_export.py::test_pose_review_export_creates_artifact_query_result_and_tom_native_json` |
| Pose review export includes annotations | Covered | `tests/test_pose_query_review_export.py::test_pose_review_export_creates_artifact_query_result_and_tom_native_json` |
| Pose review export creates evidence_artifact row | Covered | `tests/test_pose_query_review_export.py::test_pose_review_export_creates_artifact_query_result_and_tom_native_json` |
| Pose review export can create query_result memory | Covered | `tests/test_pose_query_review_export.py::test_pose_review_export_creates_artifact_query_result_and_tom_native_json` |
| Docs avoid movement/event claims | Covered by review | 4F docs, runbook, and pose docs describe pose as evidence only and preserve the non-goal boundary |

No new implementation tests were added in 4F. The existing 4A-4E test suite already covers the requested schema, normalization, persistence, lineage, query, review, export, and viewer payload contracts. The frontend overlay drawing invariants are covered by the 4D viewer contract, code paths, web build, and synthetic viewer smoke; a dedicated frontend unit-test runner remains a future hardening option.

## Runbook Result

The local runbook now describes the complete Blueprint 4 fixture path:

```text
index media
-> run fixture detection adapter
-> run fixture pose adapter
-> optionally link pose to source player detections
-> open viewer
-> inspect pose overlay and keypoint table
-> query pose observations
-> add review annotations through the generic annotation API
-> export TOM-native pose review dataset
-> inspect JSON export and artifact metadata
```

This path does not require real pose weights or Ultralytics pose runtime.

## Remaining Limitations

- Real pose model loading and inference are not implemented.
- Pose review labels can be written through the generic annotation API; a richer pose review UI is future work.
- Export format is TOM-native JSON only.
- Viewer overlay is 2D image-pixel evidence, not video tracking or movement analysis.
- No third-party pose training export format is produced.

## Next Blueprint Recommendation

Blueprint 5 has now started.

Recommended next blueprint from 4F was:

```text
Blueprint 5 - TOM v3 Simple Completion / Product Hardening
```

Milestone 5A establishes the canonical local fixture demo and runbook path. Blueprint 5 should remain a lightweight completion/product hardening pass unless the project explicitly chooses to add real pose inference next.
