from __future__ import annotations

import pytest
from pydantic import ValidationError
from tom_v3_schema.court import (
    COURT_KEYPOINT_NAMES,
    COURT_LINE_CLASSES,
    COURT_TEMPLATE_COORDINATE_SPACE,
    COURT_TEMPLATE_NAME,
    COURT_TEMPLATE_VERSION,
    CameraViewObservationCreate,
    CourtKeypointObservationCreate,
    CourtLineObservationCreate,
    HomographyCandidateObservationCreate,
    ProjectionDiagnosticObservationCreate,
    court_template_schema_json,
    get_court_template,
)


def court_keypoints() -> list[dict[str, object]]:
    keypoints: list[dict[str, object]] = []
    for index, name in enumerate(COURT_KEYPOINT_NAMES):
        if name == "far_right_baseline_corner":
            keypoints.append(
                {
                    "name": name,
                    "x": None,
                    "y": None,
                    "confidence": 0.12,
                    "present": False,
                    "visibility": "occluded",
                    "source_index": index,
                }
            )
        else:
            keypoints.append(
                {
                    "name": name,
                    "x": 100.0 + index * 10.0,
                    "y": 200.0 + index * 5.0,
                    "confidence": 0.8,
                    "present": True,
                    "visibility": "visible",
                    "source_index": index,
                }
            )
    return keypoints


def test_court_template_registry_has_expected_v0_keypoints_and_lines() -> None:
    template = get_court_template()

    assert template.template_name == COURT_TEMPLATE_NAME
    assert template.template_version == COURT_TEMPLATE_VERSION
    assert template.target_coordinate_space == COURT_TEMPLATE_COORDINATE_SPACE
    assert [keypoint.name for keypoint in template.keypoints] == COURT_KEYPOINT_NAMES
    assert {line.line_class for line in template.lines} == set(COURT_LINE_CLASSES) - {
        "unknown_court_line"
    }
    schema = court_template_schema_json()
    assert schema["template_name"] == COURT_TEMPLATE_NAME


def test_court_keypoint_schema_validates_present_and_missing_keypoints() -> None:
    observation = CourtKeypointObservationCreate(
        frame_number=30,
        timestamp_ms=1000,
        keypoints_jsonb=court_keypoints(),
    )

    assert observation.court_keypoint_schema == "tennis_court_v0"
    assert observation.schema_version == "v0"
    assert observation.keypoint_count == len(COURT_KEYPOINT_NAMES)
    assert observation.keypoints_present_count == len(COURT_KEYPOINT_NAMES) - 1
    assert observation.keypoints_missing_count == 1
    assert observation.frame_time_owner == "media_indexing"
    assert observation.metadata_jsonb["geometry_evidence_only"] is True


def test_court_keypoint_schema_rejects_wrong_order() -> None:
    keypoints = court_keypoints()
    keypoints[0]["name"] = "wrong_keypoint"

    with pytest.raises(ValidationError):
        CourtKeypointObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            keypoints_jsonb=keypoints,
        )


def test_court_line_schema_validates_segments_and_summarizes_confidence() -> None:
    observation = CourtLineObservationCreate(
        frame_number=30,
        timestamp_ms=1000,
        line_segments_jsonb=[
            {
                "line_class": "baseline_near",
                "x1": 188.2,
                "y1": 646.3,
                "x2": 1092.7,
                "y2": 642.9,
                "confidence": 0.84,
                "visibility": "partial",
            },
            {
                "line_class": "net_line",
                "x1": 190.0,
                "y1": 360.0,
                "x2": 1090.0,
                "y2": 361.0,
                "confidence": 0.76,
                "visibility": "visible",
            },
        ],
    )

    assert observation.line_count == 2
    assert observation.line_classes_jsonb == ["baseline_near", "net_line"]
    assert observation.mean_line_confidence == 0.8
    assert observation.metadata_jsonb["no_adjudication"] is True


def test_court_line_schema_rejects_unknown_line_class() -> None:
    with pytest.raises(ValidationError):
        CourtLineObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            line_segments_jsonb=[
                {
                    "line_class": "confirmed_sideline",
                    "x1": 0.0,
                    "y1": 0.0,
                    "x2": 1.0,
                    "y2": 1.0,
                    "visibility": "visible",
                }
            ],
        )


def test_camera_view_schema_validates_labels() -> None:
    observation = CameraViewObservationCreate(
        frame_number=90,
        timestamp_ms=3000,
        view_label="broadcast_hardcam",
        view_confidence=0.91,
        camera_motion_hint="stable",
        stability_score=0.88,
        cut_likelihood=0.04,
    )

    assert observation.frame_start == 90
    assert observation.frame_end == 90
    assert observation.timestamp_start_ms == 3000
    assert observation.timestamp_end_ms == 3000
    assert observation.metadata_jsonb["geometry_evidence_only"] is True


def test_homography_schema_validates_matrix_status_and_coordinate_spaces() -> None:
    observation = HomographyCandidateObservationCreate(
        frame_number=90,
        timestamp_ms=3000,
        homography_matrix_jsonb=[
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        inverse_homography_matrix_jsonb=[
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        inlier_count=8,
        source_point_count=12,
        confidence=0.72,
    )

    assert observation.status == "candidate"
    assert observation.target_coordinate_space == "court_template_2d"
    assert observation.matrix_direction == "image_pixels_to_court_template_2d"
    assert observation.metadata_jsonb["geometry_evidence_only"] is True


def test_homography_schema_rejects_candidate_without_matrix() -> None:
    with pytest.raises(ValidationError):
        HomographyCandidateObservationCreate(
            frame_number=90,
            timestamp_ms=3000,
            status="candidate",
        )


def test_projection_diagnostic_schema_is_diagnostic_not_ball_player_projection() -> None:
    observation = ProjectionDiagnosticObservationCreate(
        frame_number=90,
        timestamp_ms=3000,
        source_homography_candidate_observation_id="homography-observation-id",
        projected_template_keypoints_jsonb=[
            {"name": "near_left_baseline_corner", "x": 100.0, "y": 640.0}
        ],
        diagnostic_metrics_jsonb={"mean_projection_error": 2.4},
        confidence=0.7,
    )

    assert observation.status == "diagnostic_candidate"
    assert observation.metadata_jsonb["not_ball_player_projection"] is True
    assert observation.frame_time_owner == "media_indexing"
