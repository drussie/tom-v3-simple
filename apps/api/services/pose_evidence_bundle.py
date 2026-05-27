from __future__ import annotations

from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    EvidenceArtifact,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    PoseObservation,
    ProcessingRun,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)

from apps.api.routers.viewer import (
    _annotation_payload,
    _artifact_payload,
    _lineage_payload,
    _media_payload,
    _observation_payload,
    _run_payload,
)
from apps.api.services.annotation_review import summarize_annotations


def get_pose_evidence_bundle(
    session: Session,
    pose_observation_id: str,
) -> dict[str, Any] | None:
    observation = session.get(Observation, pose_observation_id)
    if observation is None or observation.pose_detail is None:
        return None

    pose = observation.pose_detail
    media = session.get(MediaAsset, observation.media_id)
    run = session.get(ProcessingRun, observation.run_id)
    runtime_config = (
        session.get(RuntimeConfig, observation.runtime_config_id)
        if observation.runtime_config_id
        else None
    )
    model = session.get(ModelRegistry, observation.model_id) if observation.model_id else None

    source_detection = _source_detection(session, pose)
    tracklet = session.get(Tracklet, pose.subject_tracklet_id) if pose.subject_tracklet_id else None
    track_point = (
        session.get(TrackPoint, pose.subject_track_point_id)
        if pose.subject_track_point_id
        else None
    )
    context_observation_ids = _context_observation_ids(
        pose_observation_id=observation.id,
        source_detection=source_detection,
        tracklet=tracklet,
        track_point=track_point,
    )
    lineage = _lineage_rows(session, observation.id, context_observation_ids)
    artifacts = _artifacts(session, context_observation_ids)
    annotations = _annotations(session, context_observation_ids)
    pose_annotations = [
        annotation for annotation in annotations if annotation.observation_id == observation.id
    ]

    return {
        "pose_observation": {
            "observation": _observation_payload(observation),
            "pose": _observation_payload(observation)["pose"],
            "annotations": [_annotation_payload(annotation) for annotation in pose_annotations],
            "annotation_summary": summarize_annotations(pose_annotations),
        },
        "media": _media_payload(media) if media is not None else None,
        "run": _run_payload(run) if run is not None else None,
        "runtime_config": _runtime_config_payload(runtime_config),
        "model_registry": _model_payload(model),
        "source_context": {
            "source_detection": (
                _observation_payload(source_detection) if source_detection is not None else None
            ),
            "tracklet": _tracklet_payload(tracklet),
            "track_point": _track_point_payload(track_point),
            "subject_ref_type": pose.subject_ref_type,
            "association_status": pose.association_status,
            "association_method": pose.association_method,
            "association_confidence": pose.association_confidence,
        },
        "lineage": [_lineage_payload(row) for row in lineage],
        "artifacts": [_artifact_payload(artifact) for artifact in artifacts],
        "annotations": [_annotation_payload(annotation) for annotation in annotations],
        "annotation_summary": summarize_annotations(annotations),
        "summary": {
            "pose_observation_id": observation.id,
            "frame_number": pose.frame_number,
            "timestamp_ms": pose.timestamp_ms,
            "keypoint_count": pose.keypoint_count,
            "keypoints_present_count": pose.keypoints_present_count,
            "keypoints_missing_count": pose.keypoints_missing_count,
            "pose_confidence": pose.pose_confidence,
            "lineage_count": len(lineage),
            "annotation_count": len(annotations),
            "artifact_count": len(artifacts),
            "observation_only": True,
            "no_movement_interpretation": True,
            "no_adjudication": True,
        },
    }


def _source_detection(session: Session, pose: PoseObservation) -> Observation | None:
    if pose.subject_detection_observation_id is None:
        return None
    return session.get(Observation, pose.subject_detection_observation_id)


def _context_observation_ids(
    *,
    pose_observation_id: str,
    source_detection: Observation | None,
    tracklet: Tracklet | None,
    track_point: TrackPoint | None,
) -> list[str]:
    ids = [pose_observation_id]
    if source_detection is not None:
        ids.append(source_detection.id)
    if tracklet is not None and tracklet.observation_id:
        ids.append(tracklet.observation_id)
    if track_point is not None and track_point.observation_id:
        ids.append(track_point.observation_id)
    return sorted(set(ids))


def _lineage_rows(
    session: Session,
    pose_observation_id: str,
    context_observation_ids: list[str],
) -> list[ObservationLineage]:
    rows = session.scalars(
        select(ObservationLineage)
        .where(
            or_(
                ObservationLineage.child_observation_id == pose_observation_id,
                ObservationLineage.parent_observation_id == pose_observation_id,
                ObservationLineage.child_observation_id.in_(context_observation_ids),
                ObservationLineage.parent_observation_id.in_(context_observation_ids),
            )
        )
        .order_by(ObservationLineage.created_at, ObservationLineage.id)
    ).all()
    return list(rows)


def _artifacts(session: Session, observation_ids: list[str]) -> list[EvidenceArtifact]:
    rows = session.scalars(
        select(EvidenceArtifact)
        .where(EvidenceArtifact.target_observation_id.in_(observation_ids))
        .order_by(EvidenceArtifact.frame_start, EvidenceArtifact.artifact_type, EvidenceArtifact.id)
    ).all()
    return list(rows)


def _annotations(session: Session, observation_ids: list[str]) -> list[HumanAnnotation]:
    rows = session.scalars(
        select(HumanAnnotation)
        .where(HumanAnnotation.observation_id.in_(observation_ids))
        .order_by(HumanAnnotation.created_at, HumanAnnotation.id)
    ).all()
    return list(rows)


def _runtime_config_payload(runtime_config: RuntimeConfig | None) -> dict[str, Any] | None:
    if runtime_config is None:
        return None
    return {
        "id": runtime_config.id,
        "config_name": runtime_config.config_name,
        "config_version": runtime_config.config_version,
        "payload_jsonb": runtime_config.payload_jsonb,
        "created_at": runtime_config.created_at.isoformat()
        if runtime_config.created_at is not None
        else None,
    }


def _model_payload(model: ModelRegistry | None) -> dict[str, Any] | None:
    if model is None:
        return None
    return {
        "id": model.id,
        "name": model.name,
        "version": model.version,
        "model_family": model.model_family,
        "source": model.source,
        "metadata_jsonb": model.metadata_jsonb,
        "created_at": model.created_at.isoformat() if model.created_at is not None else None,
    }


def _tracklet_payload(tracklet: Tracklet | None) -> dict[str, Any] | None:
    if tracklet is None:
        return None
    return {
        "id": tracklet.id,
        "media_id": tracklet.media_id,
        "run_id": tracklet.run_id,
        "track_family": tracklet.track_family,
        "subject_ref": tracklet.subject_ref,
        "frame_start": tracklet.frame_start,
        "frame_end": tracklet.frame_end,
        "confidence": tracklet.confidence,
        "observation_id": tracklet.observation_id,
        "metadata_jsonb": tracklet.metadata_jsonb,
    }


def _track_point_payload(track_point: TrackPoint | None) -> dict[str, Any] | None:
    if track_point is None:
        return None
    return {
        "id": track_point.id,
        "tracklet_id": track_point.tracklet_id,
        "observation_id": track_point.observation_id,
        "frame_number": track_point.frame_number,
        "timestamp_ms": track_point.timestamp_ms,
        "x": track_point.x,
        "y": track_point.y,
        "width": track_point.width,
        "height": track_point.height,
        "confidence": track_point.confidence,
        "payload_jsonb": track_point.payload_jsonb,
    }
