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

FRAME_ARTIFACT_TYPES = {"frame_image", "detection_frame_image"}


def build_tracklet_evidence_bundle(
    session: Session,
    tracklet_id: str,
) -> dict[str, Any] | None:
    tracklet = session.get(Tracklet, tracklet_id)
    if tracklet is None:
        return None

    media = session.get(MediaAsset, tracklet.media_id)
    tracklet_run = session.get(ProcessingRun, tracklet.run_id)
    tracklet_observation = (
        session.get(Observation, tracklet.observation_id)
        if tracklet.observation_id is not None
        else None
    )
    track_points = _track_points(session, tracklet.id)
    track_point_observations = _observations_by_id(
        session, [point.observation_id for point in track_points if point.observation_id]
    )
    lineage = _lineage_for_tracklet(
        session=session,
        tracklet_observation_id=tracklet.observation_id,
        track_point_observation_ids=list(track_point_observations),
    )
    source_detections = _source_detections(session, lineage, track_points)
    source_detection_run_id = _source_detection_run_id(tracklet, source_detections)
    source_detection_run = (
        session.get(ProcessingRun, source_detection_run_id)
        if source_detection_run_id is not None
        else None
    )
    artifacts_by_source_detection = _frame_artifacts_by_source_detection(
        session=session,
        media_id=tracklet.media_id,
        source_detections=list(source_detections.values()),
    )
    observation_ids = _annotation_observation_ids(
        tracklet_observation=tracklet_observation,
        track_point_observations=track_point_observations,
        source_detections=source_detections,
    )
    annotations = _annotations(session, observation_ids)
    annotations_by_observation = _annotations_by_observation(annotations)

    source_detection_payloads = [
        {
            "observation": _observation_payload(observation),
            "frame_artifacts": [
                _artifact_payload(artifact)
                for artifact in artifacts_by_source_detection.get(observation.id, [])
            ],
            "annotations": [
                _annotation_payload(annotation) for annotation in observation_annotations
            ],
            "annotation_summary": summarize_annotations(observation_annotations),
        }
        for observation in sorted(
            source_detections.values(),
            key=lambda row: (row.frame_start or 0, row.observation_type, row.id),
        )
        for observation_annotations in [annotations_by_observation.get(observation.id, [])]
    ]

    return {
        "tracklet": {
            "typed": _tracklet_payload(tracklet),
            "observation": (
                _observation_payload(tracklet_observation)
                if tracklet_observation is not None
                else None
            ),
            "annotations": [
                _annotation_payload(annotation)
                for annotation in annotations_by_observation.get(tracklet.observation_id or "", [])
            ],
            "annotation_summary": summarize_annotations(
                annotations_by_observation.get(tracklet.observation_id or "", [])
            ),
        },
        "media": _media_payload(media) if media is not None else None,
        "runs": {
            "tracklet_run": _run_payload(tracklet_run) if tracklet_run is not None else None,
            "source_detection_run": (
                _run_payload(source_detection_run)
                if source_detection_run is not None
                else None
            ),
        },
        "runtime_configs": {
            "tracklet_runtime_config": _runtime_config_payload(
                _runtime_config(session, tracklet_run)
            ),
            "source_detection_runtime_config": _runtime_config_payload(
                _runtime_config(session, source_detection_run)
            ),
        },
        "model_registry": {
            "tracklet_builder_model": _model_payload(
                _model(session, tracklet_observation.model_id if tracklet_observation else None)
            ),
            "source_detection_model": _model_payload(
                _first_model(session, source_detections.values())
            ),
        },
        "track_points": [
            _track_point_bundle_payload(
                point=point,
                point_observation=track_point_observations.get(point.observation_id or ""),
                source_detection=source_detections.get(
                    str(point.payload_jsonb.get("source_detection_observation_id", ""))
                ),
                tracked_from=_tracked_from_lineage(lineage, point),
                grouped_from=_grouped_from_lineage(lineage, point),
                frame_artifacts=artifacts_by_source_detection.get(
                    str(point.payload_jsonb.get("source_detection_observation_id", "")),
                    [],
                ),
                annotations=annotations_by_observation.get(point.observation_id or "", []),
            )
            for point in track_points
        ],
        "source_detections": source_detection_payloads,
        "frame_artifacts": [
            _artifact_payload(artifact)
            for artifacts in artifacts_by_source_detection.values()
            for artifact in artifacts
        ],
        "lineage": [_lineage_payload(row) for row in lineage],
        "annotations": [_annotation_payload(annotation) for annotation in annotations],
        "annotation_summary": {
            "tracklet": summarize_annotations(
                annotations_by_observation.get(tracklet.observation_id or "", [])
            ),
            "track_points": summarize_annotations(
                [
                    annotation
                    for point in track_points
                    for annotation in annotations_by_observation.get(point.observation_id or "", [])
                ]
            ),
            "source_detections": summarize_annotations(
                [
                    annotation
                    for source_id in source_detections
                    for annotation in annotations_by_observation.get(source_id, [])
                ]
            ),
            "all": summarize_annotations(annotations),
        },
        "summary": _summary_payload(
            tracklet=tracklet,
            tracklet_observation=tracklet_observation,
            track_point_count=len(track_points),
            source_detection_count=len(source_detections),
        ),
    }


def _track_points(session: Session, tracklet_id: str) -> list[TrackPoint]:
    return list(
        session.scalars(
            select(TrackPoint)
            .where(TrackPoint.tracklet_id == tracklet_id)
            .order_by(TrackPoint.frame_number, TrackPoint.id)
        ).all()
    )


def _observations_by_id(session: Session, ids: list[str]) -> dict[str, Observation]:
    if not ids:
        return {}
    return {
        row.id: row
        for row in session.scalars(select(Observation).where(Observation.id.in_(ids))).all()
    }


def _lineage_for_tracklet(
    session: Session,
    tracklet_observation_id: str | None,
    track_point_observation_ids: list[str],
) -> list[ObservationLineage]:
    ids = set(track_point_observation_ids)
    if tracklet_observation_id is not None:
        ids.add(tracklet_observation_id)
    if not ids:
        return []
    return list(
        session.scalars(
            select(ObservationLineage)
            .where(
                or_(
                    ObservationLineage.child_observation_id.in_(ids),
                    ObservationLineage.parent_observation_id.in_(ids),
                )
            )
            .order_by(
                ObservationLineage.relationship_type,
                ObservationLineage.created_at,
            )
        ).all()
    )


def _source_detections(
    session: Session,
    lineage: list[ObservationLineage],
    track_points: list[TrackPoint],
) -> dict[str, Observation]:
    source_ids = {
        row.parent_observation_id
        for row in lineage
        if row.relationship_type == "tracked_from"
    }
    source_ids.update(
        str(source_id)
        for point in track_points
        if (source_id := point.payload_jsonb.get("source_detection_observation_id"))
    )
    return _observations_by_id(session, sorted(source_ids))


def _source_detection_run_id(
    tracklet: Tracklet,
    source_detections: dict[str, Observation],
) -> str | None:
    metadata_run_id = tracklet.metadata_jsonb.get("source_detection_run_id")
    if isinstance(metadata_run_id, str) and metadata_run_id:
        return metadata_run_id
    first_source = next(iter(source_detections.values()), None)
    return first_source.run_id if first_source is not None else None


def _frame_artifacts_by_source_detection(
    session: Session,
    media_id: str,
    source_detections: list[Observation],
) -> dict[str, list[EvidenceArtifact]]:
    if not source_detections:
        return {}
    source_ids = [observation.id for observation in source_detections]
    frames = sorted(
        {
            observation.frame_start
            for observation in source_detections
            if observation.frame_start is not None
        }
    )
    targeted = list(
        session.scalars(
            select(EvidenceArtifact).where(
                EvidenceArtifact.target_observation_id.in_(source_ids),
                EvidenceArtifact.artifact_type.in_(sorted(FRAME_ARTIFACT_TYPES)),
            )
        ).all()
    )
    same_frame: list[EvidenceArtifact] = []
    if frames:
        same_frame = list(
            session.scalars(
                select(EvidenceArtifact).where(
                    EvidenceArtifact.media_id == media_id,
                    EvidenceArtifact.frame_start.in_(frames),
                    EvidenceArtifact.artifact_type.in_(sorted(FRAME_ARTIFACT_TYPES)),
                )
            ).all()
        )

    artifacts_by_id: dict[str, list[EvidenceArtifact]] = {source_id: [] for source_id in source_ids}
    targeted_by_source: dict[str, list[EvidenceArtifact]] = {}
    for artifact in targeted:
        if artifact.target_observation_id is not None:
            targeted_by_source.setdefault(artifact.target_observation_id, []).append(artifact)

    same_frame_by_frame: dict[int, list[EvidenceArtifact]] = {}
    for artifact in same_frame:
        if artifact.frame_start is not None:
            same_frame_by_frame.setdefault(artifact.frame_start, []).append(artifact)

    for observation in source_detections:
        artifacts = targeted_by_source.get(observation.id, [])
        if not artifacts and observation.frame_start is not None:
            artifacts = same_frame_by_frame.get(observation.frame_start, [])
        artifacts_by_id[observation.id] = _dedupe_artifacts(artifacts)
    return artifacts_by_id


def _dedupe_artifacts(artifacts: list[EvidenceArtifact]) -> list[EvidenceArtifact]:
    deduped: dict[str, EvidenceArtifact] = {}
    for artifact in artifacts:
        deduped[artifact.id] = artifact
    return sorted(
        deduped.values(),
        key=lambda row: (
            row.target_observation_id is None,
            row.frame_start or -1,
            row.artifact_type,
            row.id,
        ),
    )


def _annotation_observation_ids(
    tracklet_observation: Observation | None,
    track_point_observations: dict[str, Observation],
    source_detections: dict[str, Observation],
) -> list[str]:
    ids: list[str] = []
    if tracklet_observation is not None:
        ids.append(tracklet_observation.id)
    ids.extend(track_point_observations)
    ids.extend(source_detections)
    return sorted(set(ids))


def _annotations(session: Session, observation_ids: list[str]) -> list[HumanAnnotation]:
    if not observation_ids:
        return []
    return list(
        session.scalars(
            select(HumanAnnotation)
            .where(HumanAnnotation.observation_id.in_(observation_ids))
            .order_by(HumanAnnotation.created_at)
        ).all()
    )


def _annotations_by_observation(
    annotations: list[HumanAnnotation],
) -> dict[str, list[HumanAnnotation]]:
    grouped: dict[str, list[HumanAnnotation]] = {}
    for annotation in annotations:
        if annotation.observation_id is not None:
            grouped.setdefault(annotation.observation_id, []).append(annotation)
    return grouped


def _runtime_config(
    session: Session,
    run: ProcessingRun | None,
) -> RuntimeConfig | None:
    if run is None or run.runtime_config_id is None:
        return None
    return session.get(RuntimeConfig, run.runtime_config_id)


def _model(session: Session, model_id: str | None) -> ModelRegistry | None:
    if model_id is None:
        return None
    return session.get(ModelRegistry, model_id)


def _first_model(
    session: Session,
    observations: Any,
) -> ModelRegistry | None:
    for observation in observations:
        if observation.model_id is not None:
            return session.get(ModelRegistry, observation.model_id)
    return None


def _runtime_config_payload(config: RuntimeConfig | None) -> dict[str, Any] | None:
    if config is None:
        return None
    return {
        "id": config.id,
        "config_name": config.config_name,
        "config_version": config.config_version,
        "payload_jsonb": config.payload_jsonb,
        "created_at": config.created_at.isoformat() if config.created_at else None,
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
        "created_at": model.created_at.isoformat() if model.created_at else None,
    }


def _tracklet_payload(tracklet: Tracklet) -> dict[str, Any]:
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


def _track_point_bundle_payload(
    point: TrackPoint,
    point_observation: Observation | None,
    source_detection: Observation | None,
    tracked_from: ObservationLineage | None,
    grouped_from: ObservationLineage | None,
    frame_artifacts: list[EvidenceArtifact],
    annotations: list[HumanAnnotation],
) -> dict[str, Any]:
    return {
        "typed": _track_point_payload(point),
        "observation": (
            _observation_payload(point_observation)
            if point_observation is not None
            else None
        ),
        "sequence_index": point.payload_jsonb.get("sequence_index"),
        "frame_number": point.frame_number,
        "timestamp_ms": point.timestamp_ms,
        "bbox": point.payload_jsonb.get("bbox"),
        "center": point.payload_jsonb.get("center"),
        "source_detection_observation_id": point.payload_jsonb.get(
            "source_detection_observation_id"
        ),
        "source_detection": (
            _observation_payload(source_detection)
            if source_detection is not None
            else None
        ),
        "lineage_to_source": (
            _lineage_payload(tracked_from)
            if tracked_from is not None
            else None
        ),
        "lineage_to_tracklet": (
            _lineage_payload(grouped_from)
            if grouped_from is not None
            else None
        ),
        "frame_artifacts": [_artifact_payload(artifact) for artifact in frame_artifacts],
        "annotations": [_annotation_payload(annotation) for annotation in annotations],
        "annotation_summary": summarize_annotations(annotations),
    }


def _tracked_from_lineage(
    lineage: list[ObservationLineage],
    point: TrackPoint,
) -> ObservationLineage | None:
    source_id = point.payload_jsonb.get("source_detection_observation_id")
    return next(
        (
            row
            for row in lineage
            if row.relationship_type == "tracked_from"
            and row.parent_observation_id == source_id
            and row.child_observation_id == point.observation_id
        ),
        None,
    )


def _grouped_from_lineage(
    lineage: list[ObservationLineage],
    point: TrackPoint,
) -> ObservationLineage | None:
    return next(
        (
            row
            for row in lineage
            if row.relationship_type == "grouped_from"
            and row.parent_observation_id == point.observation_id
        ),
        None,
    )


def _summary_payload(
    tracklet: Tracklet,
    tracklet_observation: Observation | None,
    track_point_count: int,
    source_detection_count: int,
) -> dict[str, Any]:
    payload = tracklet_observation.payload_jsonb if tracklet_observation is not None else {}
    return {
        "track_status": payload.get("track_status") or tracklet.metadata_jsonb.get("track_status"),
        "identity_status": payload.get("identity_status")
        or tracklet.metadata_jsonb.get("identity_status"),
        "track_point_count": track_point_count,
        "source_detection_count": source_detection_count,
        "frame_start": tracklet.frame_start,
        "frame_end": tracklet.frame_end,
        "timestamp_start_ms": (
            tracklet_observation.timestamp_start_ms
            if tracklet_observation is not None
            else None
        ),
        "timestamp_end_ms": (
            tracklet_observation.timestamp_end_ms
            if tracklet_observation is not None
            else None
        ),
        "gap_count": payload.get("gap_count") or tracklet.metadata_jsonb.get("gap_count"),
        "confidence": tracklet.confidence,
        "warning": "candidate grouping only; not proof",
    }
