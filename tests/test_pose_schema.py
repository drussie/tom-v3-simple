from __future__ import annotations

import pytest
from tom_v3_observations.pose import fixture_coco17_keypoints
from tom_v3_schema.pose import PoseObservationCreate, summarize_pose_keypoints
from tom_v3_schema.skeletons import (
    COCO17_KEYPOINT_NAMES,
    KeypointSchemaError,
    SkeletonDefinition,
    SkeletonKeypointDefinition,
    SkeletonRegistryError,
    get_skeleton_definition,
    validate_keypoint_schema,
    validate_skeleton_definition,
)


def test_coco17_skeleton_registry_exists() -> None:
    skeleton = get_skeleton_definition("coco17", "v1")

    assert skeleton.skeleton_format == "coco17"
    assert skeleton.skeleton_version == "v1"
    assert len(skeleton.keypoints) == 17
    assert [keypoint.name for keypoint in skeleton.keypoints] == COCO17_KEYPOINT_NAMES


def test_coco17_edges_reference_valid_keypoints() -> None:
    skeleton = validate_skeleton_definition(get_skeleton_definition("coco17", "v1"))
    names = {keypoint.name for keypoint in skeleton.keypoints}

    assert skeleton.edges
    assert all(start in names and end in names for start, end in skeleton.edges)


def test_skeleton_validation_fails_for_bad_edge() -> None:
    skeleton = SkeletonDefinition(
        skeleton_format="bad17",
        skeleton_version="v0",
        keypoints=[SkeletonKeypointDefinition(index=0, name="nose")],
        edges=[("nose", "missing")],
    )

    with pytest.raises(SkeletonRegistryError, match="unknown keypoint"):
        validate_skeleton_definition(skeleton)


def test_keypoint_schema_validation_passes_for_fixture_keypoints() -> None:
    keypoints = fixture_coco17_keypoints()

    validated = validate_keypoint_schema(keypoints, "coco17", "v1")

    assert validated == keypoints


def test_keypoint_schema_validation_fails_for_wrong_count() -> None:
    keypoints = fixture_coco17_keypoints()[:-1]

    with pytest.raises(KeypointSchemaError, match="expected 17 keypoints"):
        validate_keypoint_schema(keypoints, "coco17", "v1")


def test_keypoint_schema_validation_fails_for_bad_name_or_index() -> None:
    keypoints = fixture_coco17_keypoints()
    keypoints[5] = {**keypoints[5], "name": "wrong_shoulder"}

    with pytest.raises(KeypointSchemaError, match="keypoint name mismatch"):
        validate_keypoint_schema(keypoints, "coco17", "v1")


def test_pose_observation_create_computes_keypoint_summary() -> None:
    keypoints = fixture_coco17_keypoints()

    pose = PoseObservationCreate(
        frame_number=12,
        timestamp_ms=400,
        keypoints_jsonb=keypoints,
        pose_confidence=0.82,
    )
    summary = summarize_pose_keypoints(keypoints)

    assert pose.keypoint_count == 17
    assert pose.keypoints_present_count == 15
    assert pose.keypoints_missing_count == 2
    assert pose.mean_keypoint_confidence == summary.mean_keypoint_confidence
    assert pose.frame_time_owner == "media_indexing"
