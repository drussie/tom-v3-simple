from __future__ import annotations

from tom_v3_model_adapters.pose_normalization import (
    FixturePoseAdapter,
    build_pose_adapter_result_from_normalized,
    normalize_pose_frame_result,
)
from tom_v3_schema.pose import PoseObservationCreate
from tom_v3_schema.skeletons import COCO17_KEYPOINT_NAMES


def raw_coco17_keypoints(
    *,
    missing_indices: set[int] | None = None,
    start_x: float = 500.0,
    start_y: float = 180.0,
) -> list[dict[str, object]]:
    missing_indices = missing_indices or set()
    keypoints: list[dict[str, object]] = []
    for index in range(17):
        if index in missing_indices:
            keypoints.append({"x": None, "y": None, "confidence": None})
        else:
            keypoints.append(
                {
                    "x": start_x + index * 8,
                    "y": start_y + index * 18,
                    "confidence": round(0.9 - index * 0.02, 3),
                }
            )
    return keypoints


def pose_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "bbox_xyxy": [480.0, 150.0, 660.0, 580.0],
        "bbox_confidence": 0.86,
        "pose_confidence": 0.82,
        "source_result_index": 0,
        "keypoints": raw_coco17_keypoints(),
    }
    payload.update(overrides)
    return payload


def frame_result(*poses: dict[str, object], **overrides: object) -> dict[str, object]:
    result: dict[str, object] = {
        "frame_number": 120,
        "timestamp_ms": 4000,
        "image_width": 1280,
        "image_height": 720,
        "poses": list(poses),
    }
    result.update(overrides)
    return result


def test_full_frame_fake_pose_normalizes_to_pose_create_payload() -> None:
    result = normalize_pose_frame_result(frame_result(pose_payload()))

    assert result.input_pose_count == 1
    assert result.normalized_pose_count == 1
    normalized = result.poses[0]
    pose_create = normalized.as_pose_observation_create()

    assert isinstance(pose_create, PoseObservationCreate)
    assert pose_create.frame_number == 120
    assert pose_create.timestamp_ms == 4000
    assert pose_create.skeleton_format == "coco17"
    assert pose_create.skeleton_version == "v1"
    assert pose_create.frame_time_owner == "media_indexing"


def test_coco17_keypoint_names_indices_and_normalized_coordinates() -> None:
    result = normalize_pose_frame_result(frame_result(pose_payload()))

    keypoints = result.poses[0].keypoints_jsonb
    assert [keypoint["name"] for keypoint in keypoints] == COCO17_KEYPOINT_NAMES
    assert [keypoint["index"] for keypoint in keypoints] == list(range(17))
    assert keypoints[0]["x"] == 500.0
    assert keypoints[0]["y"] == 180.0
    assert keypoints[0]["x_norm"] == round(500.0 / 1280, 6)
    assert keypoints[0]["y_norm"] == round(180.0 / 720, 6)


def test_missing_keypoints_remain_missing_evidence() -> None:
    keypoints = raw_coco17_keypoints(missing_indices={10})

    result = normalize_pose_frame_result(frame_result(pose_payload(keypoints=keypoints)))

    right_wrist = result.poses[0].keypoints_jsonb[10]
    assert right_wrist["name"] == "right_wrist"
    assert right_wrist["present"] is False
    assert right_wrist["x"] is None
    assert right_wrist["y"] is None
    assert right_wrist["confidence"] is None


def test_keypoint_summary_counts_present_and_missing_keypoints() -> None:
    keypoints = raw_coco17_keypoints(missing_indices={10, 15})

    result = normalize_pose_frame_result(frame_result(pose_payload(keypoints=keypoints)))
    pose = result.poses[0]

    assert pose.keypoint_count == 17
    assert pose.keypoints_present_count == 15
    assert pose.keypoints_missing_count == 2
    assert pose.mean_keypoint_confidence is not None
    assert pose.min_keypoint_confidence is not None
    assert pose.max_keypoint_confidence is not None


def test_pose_confidence_uses_provided_value() -> None:
    result = normalize_pose_frame_result(frame_result(pose_payload(pose_confidence=0.77)))

    assert result.poses[0].pose_confidence == 0.77


def test_pose_confidence_falls_back_to_mean_keypoint_confidence() -> None:
    payload = pose_payload()
    payload.pop("pose_confidence")

    result = normalize_pose_frame_result(frame_result(payload))
    pose = result.poses[0]

    assert pose.pose_confidence == pose.mean_keypoint_confidence


def test_bbox_xyxy_converts_to_bbox_fields() -> None:
    result = normalize_pose_frame_result(
        frame_result(pose_payload(bbox_xyxy=[10.0, 20.0, 30.0, 70.0]))
    )

    pose = result.poses[0]
    assert pose.bbox_x == 10.0
    assert pose.bbox_y == 20.0
    assert pose.bbox_w == 20.0
    assert pose.bbox_h == 50.0


def test_invalid_bbox_warns_but_keeps_valid_keypoints() -> None:
    result = normalize_pose_frame_result(
        frame_result(pose_payload(bbox_xyxy=[30.0, 70.0, 10.0, 20.0]))
    )

    assert result.normalized_pose_count == 1
    assert result.poses[0].bbox_x is None
    assert result.poses[0].bbox_w is None
    assert result.warnings[0]["warning_type"] == "invalid_bbox"


def test_invalid_keypoint_count_skips_pose_with_warning() -> None:
    result = normalize_pose_frame_result(
        frame_result(pose_payload(keypoints=raw_coco17_keypoints()[:-1]))
    )

    assert result.normalized_pose_count == 0
    assert result.skipped_pose_count == 1
    assert result.warnings[0]["warning_type"] == "invalid_keypoint_count"


def test_invalid_and_out_of_range_confidence_records_warnings() -> None:
    keypoints = raw_coco17_keypoints()
    keypoints[0]["confidence"] = 1.2
    keypoints[1]["confidence"] = "high"

    result = normalize_pose_frame_result(frame_result(pose_payload(keypoints=keypoints)))

    warning_types = [warning["warning_type"] for warning in result.warnings]
    assert "confidence_out_of_range" in warning_types
    assert "invalid_confidence" in warning_types
    assert result.normalized_pose_count == 1


def test_crop_local_keypoints_project_to_full_frame_coordinates() -> None:
    keypoints = raw_coco17_keypoints(start_x=10.0, start_y=20.0)

    result = normalize_pose_frame_result(
        frame_result(
            pose_payload(
                keypoints=keypoints,
                keypoint_coordinate_space="crop_pixels",
                crop={
                    "x": 100.0,
                    "y": 50.0,
                    "width": 300.0,
                    "height": 500.0,
                    "source": "player_detection",
                },
            )
        )
    )

    pose = result.poses[0]
    assert pose.crop_x == 100.0
    assert pose.crop_y == 50.0
    assert pose.crop_w == 300.0
    assert pose.crop_h == 500.0
    assert pose.crop_source == "player_detection"
    assert pose.keypoints_jsonb[0]["x"] == 110.0
    assert pose.keypoints_jsonb[0]["y"] == 70.0
    assert pose.metadata_jsonb["crop_local_keypoints"][0]["x"] == 10.0
    assert pose.metadata_jsonb["crop_local_keypoints"][0]["y"] == 20.0


def test_subject_association_defaults_to_unassociated_full_frame() -> None:
    result = normalize_pose_frame_result(frame_result(pose_payload()))

    pose = result.poses[0]
    assert pose.subject_ref_type == "none"
    assert pose.association_status == "unassociated"
    assert pose.association_method == "full_frame_pose"
    assert pose.association_confidence is None


def test_subject_association_candidate_fields_pass_through() -> None:
    result = normalize_pose_frame_result(
        frame_result(
            pose_payload(
                subject_context={
                    "subject_ref_type": "player_detection",
                    "subject_detection_observation_id": "obs-player-1",
                    "subject_tracklet_id": "tracklet-1",
                    "subject_track_point_id": "track-point-1",
                    "association_status": "candidate",
                    "association_method": "crop_from_player_detection",
                    "association_confidence": 0.86,
                }
            )
        )
    )

    pose = result.poses[0]
    assert pose.subject_ref_type == "player_detection"
    assert pose.subject_detection_observation_id == "obs-player-1"
    assert pose.subject_tracklet_id == "tracklet-1"
    assert pose.subject_track_point_id == "track-point-1"
    assert pose.association_status == "candidate"
    assert pose.association_method == "crop_from_player_detection"
    assert pose.association_confidence == 0.86


def test_adapter_skeleton_returns_pose_adapter_result_with_diagnostics() -> None:
    adapter = FixturePoseAdapter()
    normalization = adapter.normalize_frame_result(frame_result(pose_payload()))
    adapter_result = adapter.build_adapter_result_from_normalized(normalization)

    assert adapter_result.poses == normalization.poses
    assert adapter_result.diagnostics["input_pose_count"] == 1
    assert adapter_result.diagnostics["normalized_pose_count"] == 1
    assert adapter_result.diagnostics["note"] == "normalization only, no real pose inference"


def test_build_pose_adapter_result_from_normalized_function() -> None:
    normalization = normalize_pose_frame_result(frame_result(pose_payload()))

    adapter_result = build_pose_adapter_result_from_normalized(normalization)

    assert adapter_result.adapter_name == "fixture-pose-normalizer"
    assert adapter_result.adapter_version == "v0"
    assert adapter_result.poses[0].frame_time_owner == "media_indexing"


def test_unsupported_skeleton_skips_pose_with_warning() -> None:
    result = normalize_pose_frame_result(
        frame_result(pose_payload(), skeleton_format="unknown17", skeleton_version="v0")
    )

    assert result.poses == []
    assert result.skipped_pose_count == 1
    assert result.warnings[0]["warning_type"] == "unsupported_skeleton"
