from __future__ import annotations

from collections import Counter
from typing import Any

from tom_v3_storage.db_models import HumanAnnotation

TRACKLET_REVIEW_LABELS = [
    "likely_good_tracklet",
    "bad_tracklet",
    "identity_switch",
    "wrong_grouping",
    "fragmented_tracklet",
    "merged_multiple_objects",
    "uncertain",
]

TRACK_POINT_REVIEW_LABELS = [
    "wrong_point_assignment",
    "point_should_start_new_tracklet",
    "point_should_belong_to_previous_tracklet",
    "bad_source_detection",
    "missed_detection_nearby",
    "uncertain",
]

SOURCE_DETECTION_REVIEW_LABELS = [
    "bad_source_detection",
    "wrong_class_label",
    "bad_bbox",
    "duplicate_detection",
    "missed_ball_nearby",
    "uncertain",
]

POSE_REVIEW_LABELS = [
    "likely_good_pose",
    "bad_pose",
    "wrong_subject",
    "bad_skeleton",
    "uncertain",
    "missing_keypoint",
    "bad_keypoint",
    "low_confidence_but_visible",
    "keypoint_on_wrong_body_part",
    "keypoint_occluded",
    "uncertain_keypoint",
    "bad_source_detection",
    "bad_tracklet_context",
    "subject_association_uncertain",
]

REVIEW_LABELS = sorted(
    set(
        TRACKLET_REVIEW_LABELS
        + TRACK_POINT_REVIEW_LABELS
        + SOURCE_DETECTION_REVIEW_LABELS
        + POSE_REVIEW_LABELS
    )
)


def annotation_label(annotation: HumanAnnotation | dict[str, Any]) -> str:
    payload = (
        annotation.get("payload_jsonb", {})
        if isinstance(annotation, dict)
        else annotation.payload_jsonb
    )
    annotation_type = (
        annotation.get("annotation_type")
        if isinstance(annotation, dict)
        else annotation.annotation_type
    )
    label = payload.get("annotation_label") if isinstance(payload, dict) else None
    return label if isinstance(label, str) and label else str(annotation_type)


def summarize_annotations(
    annotations: list[HumanAnnotation] | list[dict[str, Any]],
) -> dict[str, Any]:
    labels = Counter(annotation_label(annotation) for annotation in annotations)
    latest = None
    for annotation in annotations:
        created_at = (
            annotation.get("created_at")
            if isinstance(annotation, dict)
            else annotation.created_at
        )
        if created_at is None:
            continue
        created_at_text = created_at if isinstance(created_at, str) else created_at.isoformat()
        latest = max(latest, created_at_text) if latest else created_at_text

    return {
        "count": len(annotations),
        "labels": dict(sorted(labels.items())),
        "latest_created_at": latest,
    }
