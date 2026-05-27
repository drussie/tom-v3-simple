from __future__ import annotations

from collections import Counter
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.pose import PoseQueryFilters, PoseQueryResponse, PoseQueryRow
from tom_v3_storage.db_models import EvidenceArtifact, HumanAnnotation, Observation, PoseObservation

from apps.api.routers.viewer import _observation_payload
from apps.api.services.annotation_review import annotation_label, summarize_annotations


def query_poses(session: Session, filters: PoseQueryFilters) -> PoseQueryResponse:
    stmt = (
        select(PoseObservation)
        .join(Observation, PoseObservation.observation_id == Observation.id)
        .where(Observation.observation_family == "pose")
        .order_by(PoseObservation.frame_number, PoseObservation.observation_id)
    )

    if filters.media_id is not None:
        stmt = stmt.where(PoseObservation.media_id == filters.media_id)
    if filters.run_id is not None:
        stmt = stmt.where(PoseObservation.run_id == filters.run_id)
    if filters.frame_start_gte is not None:
        stmt = stmt.where(PoseObservation.frame_number >= filters.frame_start_gte)
    if filters.frame_end_lte is not None:
        stmt = stmt.where(PoseObservation.frame_number <= filters.frame_end_lte)
    if filters.timestamp_start_gte is not None:
        stmt = stmt.where(PoseObservation.timestamp_ms >= filters.timestamp_start_gte)
    if filters.timestamp_end_lte is not None:
        stmt = stmt.where(PoseObservation.timestamp_ms <= filters.timestamp_end_lte)
    if filters.pose_confidence_min is not None:
        stmt = stmt.where(PoseObservation.pose_confidence >= filters.pose_confidence_min)
    if filters.pose_confidence_max is not None:
        stmt = stmt.where(PoseObservation.pose_confidence <= filters.pose_confidence_max)
    if filters.keypoints_missing_count_min is not None:
        stmt = stmt.where(
            PoseObservation.keypoints_missing_count >= filters.keypoints_missing_count_min
        )
    if filters.keypoints_missing_count_max is not None:
        stmt = stmt.where(
            PoseObservation.keypoints_missing_count <= filters.keypoints_missing_count_max
        )
    if filters.skeleton_format is not None:
        stmt = stmt.where(PoseObservation.skeleton_format == filters.skeleton_format)
    if filters.association_status is not None:
        stmt = stmt.where(PoseObservation.association_status == filters.association_status)
    if filters.association_method is not None:
        stmt = stmt.where(PoseObservation.association_method == filters.association_method)
    if filters.subject_ref_type is not None:
        stmt = stmt.where(PoseObservation.subject_ref_type == filters.subject_ref_type)
    if filters.subject_detection_observation_id is not None:
        stmt = stmt.where(
            PoseObservation.subject_detection_observation_id
            == filters.subject_detection_observation_id
        )
    if filters.subject_tracklet_id is not None:
        stmt = stmt.where(PoseObservation.subject_tracklet_id == filters.subject_tracklet_id)
    if filters.subject_track_point_id is not None:
        stmt = stmt.where(PoseObservation.subject_track_point_id == filters.subject_track_point_id)

    poses = list(session.scalars(stmt).all())
    observation_ids = [pose.observation_id for pose in poses]
    annotations_by_observation = _annotations_by_observation(session, observation_ids)
    artifacts_by_observation = _artifacts_by_observation(session, observation_ids)

    filtered = [
        pose
        for pose in poses
        if _matches_python_filters(
            pose=pose,
            filters=filters,
            annotations=annotations_by_observation.get(pose.observation_id, []),
        )
    ]

    count = len(filtered)
    paged = filtered[filters.offset : filters.offset + filters.limit]
    rows = [
        _query_row(
            pose=pose,
            annotations=annotations_by_observation.get(pose.observation_id, []),
            artifacts=artifacts_by_observation.get(pose.observation_id, []),
        )
        for pose in paged
    ]

    return PoseQueryResponse(
        count=count,
        poses=rows,
        filters_applied=filters.model_dump(exclude_none=True),
        summary=_summary(filtered, annotations_by_observation),
    )


def _matches_python_filters(
    *,
    pose: PoseObservation,
    filters: PoseQueryFilters,
    annotations: list[HumanAnnotation],
) -> bool:
    if filters.review_label is not None:
        labels = {annotation_label(annotation) for annotation in annotations}
        if filters.review_label not in labels:
            return False
    return True


def _query_row(
    *,
    pose: PoseObservation,
    annotations: list[HumanAnnotation],
    artifacts: list[EvidenceArtifact],
) -> PoseQueryRow:
    observation = pose.observation
    pose_payload = _observation_payload(observation)["pose"] or {}
    return PoseQueryRow(
        observation=_observation_payload(observation),
        pose=pose_payload,
        media_id=pose.media_id,
        run_id=pose.run_id,
        frame_number=pose.frame_number,
        timestamp_ms=pose.timestamp_ms,
        skeleton_format=pose.skeleton_format,
        skeleton_version=pose.skeleton_version,
        pose_confidence=pose.pose_confidence,
        keypoints_present_count=pose.keypoints_present_count,
        keypoints_missing_count=pose.keypoints_missing_count,
        subject_ref_type=pose.subject_ref_type,
        association_status=pose.association_status,
        association_method=pose.association_method,
        subject_detection_observation_id=pose.subject_detection_observation_id,
        subject_tracklet_id=pose.subject_tracklet_id,
        subject_track_point_id=pose.subject_track_point_id,
        annotation_summary=summarize_annotations(annotations),
        artifact_summary=_artifact_summary(artifacts),
        evidence_bundle_url=f"/pose-observations/{pose.observation_id}/evidence-bundle",
    )


def _summary(
    poses: list[PoseObservation],
    annotations_by_observation: dict[str, list[HumanAnnotation]],
) -> dict[str, Any]:
    return {
        "count": len(poses),
        "by_skeleton_format": dict(
            sorted(Counter(pose.skeleton_format for pose in poses).items())
        ),
        "by_association_status": dict(
            sorted(Counter(pose.association_status for pose in poses).items())
        ),
        "by_subject_ref_type": dict(
            sorted(Counter(pose.subject_ref_type for pose in poses).items())
        ),
        "by_annotation_label": _annotation_label_counts(poses, annotations_by_observation),
    }


def _annotations_by_observation(
    session: Session,
    observation_ids: list[str],
) -> dict[str, list[HumanAnnotation]]:
    if not observation_ids:
        return {}
    rows = session.scalars(
        select(HumanAnnotation)
        .where(HumanAnnotation.observation_id.in_(observation_ids))
        .order_by(HumanAnnotation.created_at, HumanAnnotation.id)
    ).all()
    grouped: dict[str, list[HumanAnnotation]] = {
        observation_id: [] for observation_id in observation_ids
    }
    for row in rows:
        if row.observation_id is not None:
            grouped.setdefault(row.observation_id, []).append(row)
    return grouped


def _artifacts_by_observation(
    session: Session,
    observation_ids: list[str],
) -> dict[str, list[EvidenceArtifact]]:
    if not observation_ids:
        return {}
    rows = session.scalars(
        select(EvidenceArtifact)
        .where(EvidenceArtifact.target_observation_id.in_(observation_ids))
        .order_by(EvidenceArtifact.created_at, EvidenceArtifact.id)
    ).all()
    grouped: dict[str, list[EvidenceArtifact]] = {
        observation_id: [] for observation_id in observation_ids
    }
    for row in rows:
        if row.target_observation_id is not None:
            grouped.setdefault(row.target_observation_id, []).append(row)
    return grouped


def _artifact_summary(artifacts: list[EvidenceArtifact]) -> dict[str, Any]:
    return {
        "count": len(artifacts),
        "artifact_types": dict(sorted(Counter(row.artifact_type for row in artifacts).items())),
    }


def _annotation_label_counts(
    poses: list[PoseObservation],
    annotations_by_observation: dict[str, list[HumanAnnotation]],
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for pose in poses:
        for annotation in annotations_by_observation.get(pose.observation_id, []):
            counts[annotation_label(annotation)] += 1
    return dict(sorted(counts.items()))
