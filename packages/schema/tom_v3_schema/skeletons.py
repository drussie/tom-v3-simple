from __future__ import annotations

from typing import Any

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel

COCO17_FORMAT = "coco17"
COCO17_VERSION = "v1"

COCO17_KEYPOINT_NAMES = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

COCO17_SKELETON_EDGES = [
    ("nose", "left_eye"),
    ("nose", "right_eye"),
    ("left_eye", "left_ear"),
    ("right_eye", "right_ear"),
    ("left_shoulder", "right_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"),
    ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"),
    ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"),
    ("left_hip", "right_hip"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
]


class SkeletonRegistryError(ValueError):
    pass


class KeypointSchemaError(ValueError):
    pass


class SkeletonKeypointDefinition(TOMBaseModel):
    index: int
    name: str


class SkeletonDefinition(TOMBaseModel):
    skeleton_format: str
    skeleton_version: str
    keypoints: list[SkeletonKeypointDefinition]
    edges: list[tuple[str, str]] = Field(default_factory=list)

    def as_schema_json(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


COCO17_SKELETON = SkeletonDefinition(
    skeleton_format=COCO17_FORMAT,
    skeleton_version=COCO17_VERSION,
    keypoints=[
        SkeletonKeypointDefinition(index=index, name=name)
        for index, name in enumerate(COCO17_KEYPOINT_NAMES)
    ],
    edges=COCO17_SKELETON_EDGES,
)

SKELETON_REGISTRY: dict[tuple[str, str], SkeletonDefinition] = {
    (COCO17_FORMAT, COCO17_VERSION): COCO17_SKELETON,
}


def get_skeleton_definition(
    skeleton_format: str = COCO17_FORMAT,
    skeleton_version: str = COCO17_VERSION,
) -> SkeletonDefinition:
    try:
        return SKELETON_REGISTRY[(skeleton_format, skeleton_version)]
    except KeyError as exc:
        raise SkeletonRegistryError(
            f"unknown skeleton format/version: {skeleton_format}/{skeleton_version}"
        ) from exc


def skeleton_schema_json(
    skeleton_format: str = COCO17_FORMAT,
    skeleton_version: str = COCO17_VERSION,
) -> dict[str, Any]:
    return get_skeleton_definition(skeleton_format, skeleton_version).as_schema_json()


def validate_skeleton_definition(definition: SkeletonDefinition) -> SkeletonDefinition:
    seen_indices: set[int] = set()
    seen_names: set[str] = set()
    for expected_index, keypoint in enumerate(definition.keypoints):
        if keypoint.index != expected_index:
            raise SkeletonRegistryError(
                f"keypoint index mismatch for {keypoint.name}: "
                f"expected {expected_index}, got {keypoint.index}"
            )
        if keypoint.index in seen_indices:
            raise SkeletonRegistryError(f"duplicate keypoint index: {keypoint.index}")
        if keypoint.name in seen_names:
            raise SkeletonRegistryError(f"duplicate keypoint name: {keypoint.name}")
        seen_indices.add(keypoint.index)
        seen_names.add(keypoint.name)

    for start, end in definition.edges:
        if start not in seen_names or end not in seen_names:
            raise SkeletonRegistryError(
                f"skeleton edge references unknown keypoint: {start}->{end}"
            )

    return definition


def validate_keypoint_schema(
    keypoints: list[dict[str, Any]],
    skeleton_format: str = COCO17_FORMAT,
    skeleton_version: str = COCO17_VERSION,
) -> list[dict[str, Any]]:
    definition = validate_skeleton_definition(
        get_skeleton_definition(skeleton_format, skeleton_version)
    )
    expected = definition.keypoints
    if len(keypoints) != len(expected):
        raise KeypointSchemaError(
            f"expected {len(expected)} keypoints for {skeleton_format}/{skeleton_version}, "
            f"got {len(keypoints)}"
        )

    for expected_keypoint, keypoint in zip(expected, keypoints, strict=True):
        if keypoint.get("index") != expected_keypoint.index:
            raise KeypointSchemaError(
                f"keypoint index mismatch for {expected_keypoint.name}: "
                f"expected {expected_keypoint.index}, got {keypoint.get('index')}"
            )
        if keypoint.get("name") != expected_keypoint.name:
            raise KeypointSchemaError(
                f"keypoint name mismatch at index {expected_keypoint.index}: "
                f"expected {expected_keypoint.name}, got {keypoint.get('name')}"
            )

    return keypoints
