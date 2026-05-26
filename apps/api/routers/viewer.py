from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    EvidenceArtifact,
    HumanAnnotation,
    MediaAsset,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    Tracklet,
    TrackPoint,
)

from apps.api.db import get_session

router = APIRouter(prefix="/viewer", tags=["viewer"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/runs/{run_id}")
def get_viewer_run(run_id: str, session: SessionDep) -> dict[str, Any]:
    payload = build_viewer_run_payload(session, run_id)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="run not found")
    return payload


def build_viewer_run_payload(session: Session, run_id: str) -> dict[str, Any] | None:
    run = session.get(ProcessingRun, run_id)
    if run is None:
        return None

    media = session.get(MediaAsset, run.media_id)
    steps = session.scalars(
        select(ProcessingStep)
        .where(ProcessingStep.run_id == run_id)
        .order_by(ProcessingStep.step_name)
    ).all()
    observations = session.scalars(
        select(Observation)
        .where(Observation.run_id == run_id)
        .order_by(Observation.frame_start, Observation.observation_type, Observation.id)
    ).all()
    observation_ids = [observation.id for observation in observations]

    tracklets = session.scalars(
        select(Tracklet)
        .where(Tracklet.run_id == run_id)
        .order_by(Tracklet.track_family, Tracklet.subject_ref, Tracklet.frame_start)
    ).all()
    tracklet_ids = [tracklet.id for tracklet in tracklets]
    points_by_tracklet: dict[str, list[TrackPoint]] = {tracklet.id: [] for tracklet in tracklets}
    if tracklet_ids:
        points = session.scalars(
            select(TrackPoint)
            .where(TrackPoint.tracklet_id.in_(tracklet_ids))
            .order_by(TrackPoint.tracklet_id, TrackPoint.frame_number)
        ).all()
        for point in points:
            points_by_tracklet.setdefault(point.tracklet_id, []).append(point)

    lineage: list[ObservationLineage] = []
    if observation_ids:
        lineage = list(
            session.scalars(
                select(ObservationLineage)
                .where(
                    or_(
                        ObservationLineage.child_observation_id.in_(observation_ids),
                        ObservationLineage.parent_observation_id.in_(observation_ids),
                    )
                )
                .order_by(ObservationLineage.child_observation_id, ObservationLineage.created_at)
            ).all()
        )

    artifacts = session.scalars(
        select(EvidenceArtifact)
        .where(EvidenceArtifact.run_id == run_id)
        .order_by(EvidenceArtifact.frame_start, EvidenceArtifact.artifact_type)
    ).all()
    annotations: list[HumanAnnotation] = []
    if observation_ids:
        annotations = list(
            session.scalars(
                select(HumanAnnotation)
                .where(HumanAnnotation.observation_id.in_(observation_ids))
                .order_by(HumanAnnotation.created_at)
            ).all()
        )

    return {
        "run": _run_payload(run),
        "media": _media_payload(media) if media is not None else None,
        "steps": [_step_payload(step) for step in steps],
        "observations": [_observation_payload(observation) for observation in observations],
        "tracklets": [
            _tracklet_payload(tracklet, points_by_tracklet.get(tracklet.id, []))
            for tracklet in tracklets
        ],
        "lineage": [_lineage_payload(row) for row in lineage],
        "artifacts": [_artifact_payload(artifact) for artifact in artifacts],
        "annotations": [_annotation_payload(annotation) for annotation in annotations],
    }


def _dt(value: Any) -> str | None:
    return value.isoformat() if value is not None else None


def _run_payload(run: ProcessingRun) -> dict[str, Any]:
    return {
        "id": run.id,
        "media_id": run.media_id,
        "run_name": run.run_name,
        "run_status": run.run_status,
        "started_at": _dt(run.started_at),
        "completed_at": _dt(run.completed_at),
        "runtime_config_id": run.runtime_config_id,
        "metadata_jsonb": run.metadata_jsonb,
    }


def _media_payload(media: MediaAsset) -> dict[str, Any]:
    return {
        "id": media.id,
        "source_uri": media.source_uri,
        "media_type": media.media_type,
        "duration_ms": media.duration_ms,
        "frame_count": media.frame_count,
        "fps": media.fps,
        "width": media.width,
        "height": media.height,
        "checksum": media.checksum,
        "metadata_jsonb": media.metadata_jsonb,
        "created_at": _dt(media.created_at),
    }


def _step_payload(step: ProcessingStep) -> dict[str, Any]:
    return {
        "id": step.id,
        "run_id": step.run_id,
        "step_name": step.step_name,
        "step_status": step.step_status,
        "started_at": _dt(step.started_at),
        "completed_at": _dt(step.completed_at),
        "runtime_config_id": step.runtime_config_id,
        "metadata_jsonb": step.metadata_jsonb,
    }


def _observation_payload(observation: Observation) -> dict[str, Any]:
    return {
        "id": observation.id,
        "media_id": observation.media_id,
        "run_id": observation.run_id,
        "observation_family": observation.observation_family,
        "observation_type": observation.observation_type,
        "granularity": observation.granularity,
        "frame_start": observation.frame_start,
        "frame_end": observation.frame_end,
        "timestamp_start_ms": observation.timestamp_start_ms,
        "timestamp_end_ms": observation.timestamp_end_ms,
        "confidence": observation.confidence,
        "model_id": observation.model_id,
        "runtime_config_id": observation.runtime_config_id,
        "coordinate_space": observation.coordinate_space,
        "schema_version": observation.schema_version,
        "payload_jsonb": observation.payload_jsonb,
        "idempotency_key": observation.idempotency_key,
        "created_at": _dt(observation.created_at),
        "gameplay": _gameplay_payload(observation),
        "atomic": _atomic_payload(observation),
        "derived": _derived_payload(observation),
        "pose": _pose_payload(observation),
    }


def _gameplay_payload(observation: Observation) -> dict[str, Any] | None:
    detail = observation.gameplay_detail
    if detail is None:
        return None
    return {
        "observation_id": detail.observation_id,
        "view_state": detail.view_state,
        "view_state_subtype": detail.view_state_subtype,
        "payload_jsonb": detail.payload_jsonb,
    }


def _atomic_payload(observation: Observation) -> dict[str, Any] | None:
    detail = observation.atomic_detail
    if detail is None:
        return None
    return {
        "observation_id": detail.observation_id,
        "atomic_kind": detail.atomic_kind,
        "payload_jsonb": detail.payload_jsonb,
    }


def _derived_payload(observation: Observation) -> dict[str, Any] | None:
    detail = observation.derived_detail
    if detail is None:
        return None
    return {
        "observation_id": detail.observation_id,
        "derived_kind": detail.derived_kind,
        "derivation_payload_jsonb": detail.derivation_payload_jsonb,
    }


def _pose_payload(observation: Observation) -> dict[str, Any] | None:
    detail = observation.pose_detail
    if detail is None:
        return None
    return {
        "observation_id": detail.observation_id,
        "media_id": detail.media_id,
        "run_id": detail.run_id,
        "frame_number": detail.frame_number,
        "timestamp_ms": detail.timestamp_ms,
        "skeleton_format": detail.skeleton_format,
        "skeleton_version": detail.skeleton_version,
        "keypoint_schema_jsonb": detail.keypoint_schema_jsonb,
        "keypoints_jsonb": detail.keypoints_jsonb,
        "keypoint_count": detail.keypoint_count,
        "keypoints_present_count": detail.keypoints_present_count,
        "keypoints_missing_count": detail.keypoints_missing_count,
        "mean_keypoint_confidence": detail.mean_keypoint_confidence,
        "min_keypoint_confidence": detail.min_keypoint_confidence,
        "max_keypoint_confidence": detail.max_keypoint_confidence,
        "pose_confidence": detail.pose_confidence,
        "bbox_x": detail.bbox_x,
        "bbox_y": detail.bbox_y,
        "bbox_w": detail.bbox_w,
        "bbox_h": detail.bbox_h,
        "bbox_confidence": detail.bbox_confidence,
        "crop_x": detail.crop_x,
        "crop_y": detail.crop_y,
        "crop_w": detail.crop_w,
        "crop_h": detail.crop_h,
        "crop_source": detail.crop_source,
        "subject_ref_type": detail.subject_ref_type,
        "subject_detection_observation_id": detail.subject_detection_observation_id,
        "subject_tracklet_id": detail.subject_tracklet_id,
        "subject_track_point_id": detail.subject_track_point_id,
        "association_status": detail.association_status,
        "association_method": detail.association_method,
        "association_confidence": detail.association_confidence,
        "frame_time_owner": detail.frame_time_owner,
        "raw_model_payload_jsonb": detail.raw_model_payload_jsonb,
        "metadata_jsonb": detail.metadata_jsonb,
        "created_at": _dt(detail.created_at),
    }


def _tracklet_payload(tracklet: Tracklet, points: list[TrackPoint]) -> dict[str, Any]:
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
        "points": [_track_point_payload(point) for point in points],
    }


def _track_point_payload(point: TrackPoint) -> dict[str, Any]:
    return {
        "id": point.id,
        "tracklet_id": point.tracklet_id,
        "observation_id": point.observation_id,
        "frame_number": point.frame_number,
        "timestamp_ms": point.timestamp_ms,
        "x": point.x,
        "y": point.y,
        "width": point.width,
        "height": point.height,
        "confidence": point.confidence,
        "payload_jsonb": point.payload_jsonb,
    }


def _lineage_payload(row: ObservationLineage) -> dict[str, Any]:
    return {
        "id": row.id,
        "child_observation_id": row.child_observation_id,
        "parent_observation_id": row.parent_observation_id,
        "relationship_type": row.relationship_type,
        "processing_step_id": row.processing_step_id,
        "payload_jsonb": row.payload_jsonb,
        "created_at": _dt(row.created_at),
    }


def _artifact_payload(artifact: EvidenceArtifact) -> dict[str, Any]:
    return {
        "id": artifact.id,
        "media_id": artifact.media_id,
        "run_id": artifact.run_id,
        "target_observation_id": artifact.target_observation_id,
        "artifact_type": artifact.artifact_type,
        "uri": artifact.uri,
        "frame_start": artifact.frame_start,
        "frame_end": artifact.frame_end,
        "timestamp_start_ms": artifact.timestamp_start_ms,
        "timestamp_end_ms": artifact.timestamp_end_ms,
        "checksum": artifact.checksum,
        "metadata_jsonb": artifact.metadata_jsonb,
        "created_at": _dt(artifact.created_at),
    }


def _annotation_payload(annotation: HumanAnnotation) -> dict[str, Any]:
    return {
        "id": annotation.id,
        "media_id": annotation.media_id,
        "observation_id": annotation.observation_id,
        "evidence_artifact_id": annotation.evidence_artifact_id,
        "frame_start": annotation.frame_start,
        "frame_end": annotation.frame_end,
        "timestamp_start_ms": annotation.timestamp_start_ms,
        "timestamp_end_ms": annotation.timestamp_end_ms,
        "annotation_type": annotation.annotation_type,
        "payload_jsonb": annotation.payload_jsonb,
        "created_by": annotation.created_by,
        "created_at": _dt(annotation.created_at),
    }
