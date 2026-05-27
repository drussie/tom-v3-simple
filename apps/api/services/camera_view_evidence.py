from __future__ import annotations

from collections import Counter
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from tom_v3_schema.court import (
    CameraViewEvidenceSummary,
    CameraViewQueryFilters,
    CameraViewQueryResponse,
    CameraViewQueryRow,
)
from tom_v3_storage.db_models import (
    CameraViewObservation,
    EvidenceArtifact,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    RuntimeConfig,
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

CAMERA_VIEW_WARNINGS = {
    "camera_view_evidence_only": True,
    "not_confirmed_camera_state": True,
    "no_homography_decision": True,
    "no_tennis_event_interpretation": True,
    "no_adjudication": True,
}

USEFUL_HOMOGRAPHY_CONTEXT_VIEW_LABELS = ["broadcast_hardcam", "behind_baseline"]
UNSTABLE_CAMERA_MOTION_HINTS = {"panning", "zooming", "camera_cut", "unknown"}


class CameraViewEvidenceError(ValueError):
    def __init__(self, message: str, *, status_code: int = 400) -> None:
        super().__init__(message)
        self.status_code = status_code


def query_camera_view_observations(
    session: Session,
    filters: CameraViewQueryFilters,
) -> CameraViewQueryResponse:
    _require_media(session, filters.media_id)
    query = _filtered_camera_view_query(filters)
    total = session.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = session.scalars(
        query.order_by(CameraViewObservation.frame_number, CameraViewObservation.observation_id)
        .offset(filters.offset)
        .limit(filters.limit)
    ).all()

    return CameraViewQueryResponse(
        media_id=filters.media_id,
        run_id=filters.run_id,
        total=total,
        limit=filters.limit,
        offset=filters.offset,
        items=[_camera_view_row(row) for row in rows],
        warnings=dict(CAMERA_VIEW_WARNINGS),
    )


def summarize_camera_view_evidence(
    session: Session,
    filters: CameraViewQueryFilters,
) -> CameraViewEvidenceSummary:
    _require_media(session, filters.media_id)
    query = _filtered_camera_view_query(filters)
    rows = list(
        session.scalars(
            query.order_by(CameraViewObservation.frame_number, CameraViewObservation.observation_id)
        ).all()
    )
    labels = Counter(row.view_label for row in rows)
    motion_hints = Counter(row.camera_motion_hint or "unknown" for row in rows)
    frame_values = [value for row in rows for value in (row.frame_start, row.frame_end)]
    time_values = [
        value for row in rows for value in (row.timestamp_start_ms, row.timestamp_end_ms)
    ]

    return CameraViewEvidenceSummary(
        media_id=filters.media_id,
        run_id=filters.run_id,
        camera_view_observation_count=len(rows),
        labels=dict(sorted(labels.items())),
        motion_hints=dict(sorted(motion_hints.items())),
        time_range={
            "start_ms": min(time_values) if time_values else None,
            "end_ms": max(time_values) if time_values else None,
        },
        frame_range={
            "start": min(frame_values) if frame_values else None,
            "end": max(frame_values) if frame_values else None,
        },
        mean_view_confidence=_mean(row.view_confidence for row in rows),
        mean_stability_score=_mean(row.stability_score for row in rows),
        max_cut_likelihood=_max(row.cut_likelihood for row in rows),
        homography_context={
            "candidate_context_only": True,
            "likely_useful_view_labels": USEFUL_HOMOGRAPHY_CONTEXT_VIEW_LABELS,
            "observed_useful_view_count": sum(
                count
                for label, count in labels.items()
                if label in USEFUL_HOMOGRAPHY_CONTEXT_VIEW_LABELS
            ),
            "observed_unstable_count": sum(
                count
                for hint, count in motion_hints.items()
                if hint in UNSTABLE_CAMERA_MOTION_HINTS
            ),
        },
        warnings=dict(CAMERA_VIEW_WARNINGS),
    )


def build_camera_view_evidence_bundle(
    session: Session,
    observation_id: str,
) -> dict[str, Any] | None:
    observation = session.get(Observation, observation_id)
    if observation is None:
        return None
    if observation.camera_view_detail is None:
        raise CameraViewEvidenceError(
            "observation is not a camera_view_observation",
            status_code=400,
        )

    camera_view = observation.camera_view_detail
    media = session.get(MediaAsset, observation.media_id)
    run = session.get(ProcessingRun, observation.run_id)
    runtime_config = (
        session.get(RuntimeConfig, observation.runtime_config_id)
        if observation.runtime_config_id
        else None
    )
    model = session.get(ModelRegistry, observation.model_id) if observation.model_id else None
    lineage = _lineage_rows(session, observation.id)
    artifacts = _artifacts(session, observation.id)
    annotations = _annotations(session, observation.id)

    return {
        "camera_view_observation": {
            "observation": _observation_payload(observation),
            "camera_view": _camera_view_payload(camera_view),
            "annotations": [_annotation_payload(annotation) for annotation in annotations],
            "annotation_summary": summarize_annotations(annotations),
        },
        "media": _media_payload(media) if media is not None else None,
        "run": _run_payload(run) if run is not None else None,
        "runtime_config": _runtime_config_payload(runtime_config),
        "model_registry": _model_payload(model),
        "lineage": [_lineage_payload(row) for row in lineage],
        "artifacts": [_artifact_payload(artifact) for artifact in artifacts],
        "annotations": [_annotation_payload(annotation) for annotation in annotations],
        "annotation_summary": summarize_annotations(annotations),
        "summary": {
            "observation_id": observation.id,
            "frame_number": camera_view.frame_number,
            "timestamp_ms": camera_view.timestamp_ms,
            "view_label": camera_view.view_label,
            "view_confidence": camera_view.view_confidence,
            "camera_motion_hint": camera_view.camera_motion_hint,
            "stability_score": camera_view.stability_score,
            "cut_likelihood": camera_view.cut_likelihood,
            "lineage_count": len(lineage),
            "annotation_count": len(annotations),
            "artifact_count": len(artifacts),
            "camera_view_evidence_only": True,
            "not_confirmed_camera_state": True,
            "no_homography_decision": True,
            "no_tennis_event_interpretation": True,
            "no_adjudication": True,
        },
        "warnings": dict(CAMERA_VIEW_WARNINGS),
    }


def _require_media(session: Session, media_id: str) -> MediaAsset:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise CameraViewEvidenceError(
            f"media asset not found: {media_id}",
            status_code=404,
        )
    return media


def _filtered_camera_view_query(filters: CameraViewQueryFilters):
    query = (
        select(CameraViewObservation)
        .join(Observation, Observation.id == CameraViewObservation.observation_id)
        .where(
            CameraViewObservation.media_id == filters.media_id,
            Observation.observation_family == "court",
            Observation.observation_type == "camera_view_observation",
        )
    )
    if filters.run_id is not None:
        query = query.where(CameraViewObservation.run_id == filters.run_id)
    if filters.start_ms is not None:
        query = query.where(CameraViewObservation.timestamp_ms >= filters.start_ms)
    if filters.end_ms is not None:
        query = query.where(CameraViewObservation.timestamp_ms <= filters.end_ms)
    if filters.frame_start is not None:
        query = query.where(CameraViewObservation.frame_number >= filters.frame_start)
    if filters.frame_end is not None:
        query = query.where(CameraViewObservation.frame_number <= filters.frame_end)
    if filters.view_label is not None:
        query = query.where(CameraViewObservation.view_label == filters.view_label)
    if filters.camera_motion_hint is not None:
        query = query.where(CameraViewObservation.camera_motion_hint == filters.camera_motion_hint)
    if filters.min_view_confidence is not None:
        query = query.where(
            CameraViewObservation.view_confidence >= filters.min_view_confidence
        )
    return query


def _camera_view_row(row: CameraViewObservation) -> CameraViewQueryRow:
    metadata = row.metadata_jsonb or {}
    return CameraViewQueryRow(
        observation_id=row.observation_id,
        media_id=row.media_id,
        run_id=row.run_id,
        frame_number=row.frame_number,
        timestamp_ms=row.timestamp_ms,
        frame_start=row.frame_start,
        frame_end=row.frame_end,
        timestamp_start_ms=row.timestamp_start_ms,
        timestamp_end_ms=row.timestamp_end_ms,
        view_label=row.view_label,
        view_confidence=row.view_confidence,
        camera_motion_hint=row.camera_motion_hint,
        stability_score=row.stability_score,
        cut_likelihood=row.cut_likelihood,
        model_id=row.model_id,
        runtime_config_id=row.runtime_config_id,
        frame_time_owner=row.frame_time_owner,
        metadata_jsonb=metadata,
        created_at=row.created_at,
        fixture_camera_view_evidence=bool(metadata.get("fixture_camera_view_evidence")),
        observation_only=bool(metadata.get("observation_only", True)),
        no_adjudication=bool(metadata.get("no_adjudication", True)),
        geometry_evidence_only=bool(metadata.get("geometry_evidence_only", True)),
    )


def _camera_view_payload(row: CameraViewObservation) -> dict[str, Any]:
    return {
        "observation_id": row.observation_id,
        "media_id": row.media_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "frame_start": row.frame_start,
        "frame_end": row.frame_end,
        "timestamp_start_ms": row.timestamp_start_ms,
        "timestamp_end_ms": row.timestamp_end_ms,
        "view_label": row.view_label,
        "view_confidence": row.view_confidence,
        "camera_motion_hint": row.camera_motion_hint,
        "stability_score": row.stability_score,
        "cut_likelihood": row.cut_likelihood,
        "model_id": row.model_id,
        "runtime_config_id": row.runtime_config_id,
        "frame_time_owner": row.frame_time_owner,
        "metadata_jsonb": row.metadata_jsonb,
        "created_at": row.created_at.isoformat() if row.created_at is not None else None,
    }


def _lineage_rows(session: Session, observation_id: str) -> list[ObservationLineage]:
    rows = session.scalars(
        select(ObservationLineage)
        .where(
            or_(
                ObservationLineage.child_observation_id == observation_id,
                ObservationLineage.parent_observation_id == observation_id,
            )
        )
        .order_by(ObservationLineage.created_at, ObservationLineage.id)
    ).all()
    return list(rows)


def _artifacts(session: Session, observation_id: str) -> list[EvidenceArtifact]:
    rows = session.scalars(
        select(EvidenceArtifact)
        .where(EvidenceArtifact.target_observation_id == observation_id)
        .order_by(EvidenceArtifact.frame_start, EvidenceArtifact.artifact_type, EvidenceArtifact.id)
    ).all()
    return list(rows)


def _annotations(session: Session, observation_id: str) -> list[HumanAnnotation]:
    rows = session.scalars(
        select(HumanAnnotation)
        .where(HumanAnnotation.observation_id == observation_id)
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


def _mean(values: Any) -> float | None:
    numeric_values = [float(value) for value in values if value is not None]
    if not numeric_values:
        return None
    return round(sum(numeric_values) / len(numeric_values), 6)


def _max(values: Any) -> float | None:
    numeric_values = [float(value) for value in values if value is not None]
    if not numeric_values:
        return None
    return max(numeric_values)
