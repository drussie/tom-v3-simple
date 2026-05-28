from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.exports import (
    CourtReviewDatasetExportRequest,
    CourtReviewDatasetExportResponse,
)
from tom_v3_schema.ids import new_uuid
from tom_v3_storage.db_models import (
    CameraViewObservation,
    CourtKeypointObservation,
    CourtLineObservation,
    EvidenceArtifact,
    HomographyCandidateObservation,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProjectionDiagnosticObservation,
    QueryResult,
    RuntimeConfig,
)
from tom_v3_storage.local_media import calculate_sha256

EXPORT_VERSION = "court_review_dataset_v0"
EXPORT_ARTIFACT_TYPE = "court_review_dataset_export"
EXPORT_WARNINGS = {
    "geometry_evidence_only": True,
    "observation_only": True,
    "no_adjudication": True,
    "not_ball_player_projection": True,
    "no_tennis_event_interpretation": True,
}


class CourtReviewExportError(ValueError):
    pass


def export_court_review_dataset(
    session: Session,
    request: CourtReviewDatasetExportRequest,
) -> CourtReviewDatasetExportResponse:
    media = session.get(MediaAsset, request.media_id)
    if media is None:
        raise CourtReviewExportError(f"media asset not found: {request.media_id}")

    rows = _selected_rows(session, request)
    observation_ids = _observation_ids(rows)
    if not observation_ids:
        raise CourtReviewExportError("no court geometry observations matched export request")

    observations = _observations(session, observation_ids)
    lineage = _lineage(session, observation_ids)
    annotations = _annotations(session, observation_ids) if request.include_annotations else []
    artifacts = _artifacts(session, observation_ids) if request.include_artifacts else []
    runs = _runs(session, rows)
    runtime_configs = _runtime_configs(session, observations)
    models = _models(session, observations)

    export_id = new_uuid()
    export_payload = {
        "court_review_dataset_export": {
            "export_version": EXPORT_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "export_id": export_id,
            "query_spec": _query_spec(request),
            "media": _media_payload(media),
            "runs": [_run_payload(run) for run in runs],
            "runtime_configs": [_runtime_config_payload(row) for row in runtime_configs],
            "models": [_model_payload(row) for row in models],
            "court_keypoint_observations": [
                _court_keypoint_payload(row) for row in rows["court_keypoints"]
            ],
            "court_line_observations": [_court_line_payload(row) for row in rows["court_lines"]],
            "camera_view_observations": [_camera_view_payload(row) for row in rows["camera_view"]],
            "homography_candidate_observations": [
                _homography_payload(row) for row in rows["homography_candidates"]
            ],
            "projection_diagnostic_observations": [
                _projection_diagnostic_payload(row)
                for row in rows["projection_diagnostics"]
            ],
            "lineage": [_lineage_payload(row) for row in lineage],
            "artifacts": [_artifact_payload(row) for row in artifacts],
            "annotations": [_annotation_payload(row) for row in annotations],
            "warnings": dict(EXPORT_WARNINGS),
            "provenance": {
                "generated_by": request.created_by or "tom-v3-worker",
                "repo_milestone": "8F",
                "blueprint": "Blueprint 8 - Court / Camera / Homography Evidence Layer",
                "diagnostic_review_export": True,
                **EXPORT_WARNINGS,
            },
        }
    }

    export_path = _export_path(request.output_root, export_id, request.format)
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text(json.dumps(export_payload, indent=2, sort_keys=True), encoding="utf-8")
    checksum = calculate_sha256(export_path)

    artifact = _persist_export_artifact(
        session=session,
        request=request,
        export_id=export_id,
        export_path=export_path,
        checksum=checksum,
        rows=rows,
        observation_ids=observation_ids,
    )
    query_result = _persist_query_result(
        session=session,
        request=request,
        observation_ids=observation_ids,
        artifact=artifact,
        counts=_counts(rows),
    )
    session.commit()
    session.refresh(artifact)
    session.refresh(query_result)

    counts = _counts(rows)
    return CourtReviewDatasetExportResponse(
        export_id=export_id,
        artifact_id=artifact.id,
        uri=artifact.uri,
        path=str(export_path),
        checksum=checksum,
        media_id=media.id,
        court_run_id=request.court_run_id,
        homography_run_id=request.homography_run_id,
        projection_diagnostic_run_id=request.projection_diagnostic_run_id,
        court_keypoint_count=counts["court_keypoint_count"],
        court_line_count=counts["court_line_count"],
        camera_view_count=counts["camera_view_count"],
        homography_candidate_count=counts["homography_candidate_count"],
        projection_diagnostic_count=counts["projection_diagnostic_count"],
        observation_ids=observation_ids,
        query_result_id=query_result.id,
        warnings=EXPORT_WARNINGS,
        metadata=artifact.metadata_jsonb,
    )


def _selected_rows(
    session: Session,
    request: CourtReviewDatasetExportRequest,
) -> dict[str, list[Any]]:
    rows: dict[str, list[Any]] = {
        "court_keypoints": [],
        "court_lines": [],
        "camera_view": [],
        "homography_candidates": [],
        "projection_diagnostics": [],
    }
    if request.court_run_id is not None:
        rows["court_keypoints"] = list(
            session.scalars(
                select(CourtKeypointObservation)
                .where(
                    CourtKeypointObservation.media_id == request.media_id,
                    CourtKeypointObservation.run_id == request.court_run_id,
                )
                .order_by(
                    CourtKeypointObservation.frame_number,
                    CourtKeypointObservation.observation_id,
                )
            ).all()
        )
        rows["court_lines"] = list(
            session.scalars(
                select(CourtLineObservation)
                .where(
                    CourtLineObservation.media_id == request.media_id,
                    CourtLineObservation.run_id == request.court_run_id,
                )
                .order_by(CourtLineObservation.frame_number, CourtLineObservation.observation_id)
            ).all()
        )
        rows["camera_view"] = list(
            session.scalars(
                select(CameraViewObservation)
                .where(
                    CameraViewObservation.media_id == request.media_id,
                    CameraViewObservation.run_id == request.court_run_id,
                )
                .order_by(CameraViewObservation.frame_number, CameraViewObservation.observation_id)
            ).all()
        )
    if request.homography_run_id is not None:
        rows["homography_candidates"] = list(
            session.scalars(
                select(HomographyCandidateObservation)
                .where(
                    HomographyCandidateObservation.media_id == request.media_id,
                    HomographyCandidateObservation.run_id == request.homography_run_id,
                )
                .order_by(
                    HomographyCandidateObservation.frame_number,
                    HomographyCandidateObservation.observation_id,
                )
            ).all()
        )
    if request.projection_diagnostic_run_id is not None:
        rows["projection_diagnostics"] = list(
            session.scalars(
                select(ProjectionDiagnosticObservation)
                .where(
                    ProjectionDiagnosticObservation.media_id == request.media_id,
                    ProjectionDiagnosticObservation.run_id
                    == request.projection_diagnostic_run_id,
                )
                .order_by(
                    ProjectionDiagnosticObservation.frame_number,
                    ProjectionDiagnosticObservation.observation_id,
                )
            ).all()
        )
    return rows


def _observation_ids(rows: dict[str, list[Any]]) -> list[str]:
    ids = {
        row.observation_id
        for typed_rows in rows.values()
        for row in typed_rows
        if row.observation_id is not None
    }
    return sorted(ids)


def _observations(session: Session, observation_ids: list[str]) -> list[Observation]:
    return list(
        session.scalars(
            select(Observation)
            .where(Observation.id.in_(observation_ids))
            .order_by(Observation.frame_start, Observation.observation_type, Observation.id)
        ).all()
    )


def _lineage(session: Session, observation_ids: list[str]) -> list[ObservationLineage]:
    return list(
        session.scalars(
            select(ObservationLineage)
            .where(
                ObservationLineage.parent_observation_id.in_(observation_ids),
                ObservationLineage.child_observation_id.in_(observation_ids),
            )
            .order_by(ObservationLineage.child_observation_id, ObservationLineage.created_at)
        ).all()
    )


def _annotations(session: Session, observation_ids: list[str]) -> list[HumanAnnotation]:
    return list(
        session.scalars(
            select(HumanAnnotation)
            .where(HumanAnnotation.observation_id.in_(observation_ids))
            .order_by(HumanAnnotation.created_at, HumanAnnotation.id)
        ).all()
    )


def _artifacts(session: Session, observation_ids: list[str]) -> list[EvidenceArtifact]:
    return list(
        session.scalars(
            select(EvidenceArtifact)
            .where(EvidenceArtifact.target_observation_id.in_(observation_ids))
            .order_by(
                EvidenceArtifact.frame_start,
                EvidenceArtifact.artifact_type,
                EvidenceArtifact.id,
            )
        ).all()
    )


def _runs(session: Session, rows: dict[str, list[Any]]) -> list[ProcessingRun]:
    run_ids = sorted({row.run_id for typed_rows in rows.values() for row in typed_rows})
    if not run_ids:
        return []
    return list(
        session.scalars(
            select(ProcessingRun).where(ProcessingRun.id.in_(run_ids)).order_by(ProcessingRun.id)
        ).all()
    )


def _runtime_configs(
    session: Session,
    observations: list[Observation],
) -> list[RuntimeConfig]:
    ids = sorted(
        {
            observation.runtime_config_id
            for observation in observations
            if observation.runtime_config_id is not None
        }
    )
    if not ids:
        return []
    return list(
        session.scalars(
            select(RuntimeConfig).where(RuntimeConfig.id.in_(ids)).order_by(RuntimeConfig.id)
        ).all()
    )


def _models(session: Session, observations: list[Observation]) -> list[ModelRegistry]:
    ids = sorted(
        {observation.model_id for observation in observations if observation.model_id is not None}
    )
    if not ids:
        return []
    return list(
        session.scalars(select(ModelRegistry).where(ModelRegistry.id.in_(ids)).order_by(ModelRegistry.id)).all()
    )


def _persist_export_artifact(
    *,
    session: Session,
    request: CourtReviewDatasetExportRequest,
    export_id: str,
    export_path: Path,
    checksum: str,
    rows: dict[str, list[Any]],
    observation_ids: list[str],
) -> EvidenceArtifact:
    artifact = EvidenceArtifact(
        media_id=request.media_id,
        run_id=(
            request.projection_diagnostic_run_id
            or request.homography_run_id
            or request.court_run_id
        ),
        target_observation_id=None,
        artifact_type=EXPORT_ARTIFACT_TYPE,
        uri=export_path.as_uri(),
        frame_start=None,
        frame_end=None,
        timestamp_start_ms=None,
        timestamp_end_ms=None,
        checksum=checksum,
        metadata_jsonb={
            "export_version": EXPORT_VERSION,
            "export_id": export_id,
            "observation_ids": observation_ids,
            "query_spec": _query_spec(request),
            "include_annotations": request.include_annotations,
            "include_artifacts": request.include_artifacts,
            "format": request.format,
            "path": str(export_path),
            **_counts(rows),
            **EXPORT_WARNINGS,
        },
    )
    session.add(artifact)
    session.flush()
    return artifact


def _persist_query_result(
    *,
    session: Session,
    request: CourtReviewDatasetExportRequest,
    observation_ids: list[str],
    artifact: EvidenceArtifact,
    counts: dict[str, int],
) -> QueryResult:
    row = QueryResult(
        query_name=request.query_name or "court_review_dataset_export",
        query_payload_jsonb=_query_spec(request),
        result_payload_jsonb={
            "observation_ids": observation_ids,
            "result_count": len(observation_ids),
            "export_artifact_id": artifact.id,
            "export_artifact_uri": artifact.uri,
            **counts,
            **EXPORT_WARNINGS,
        },
        created_by=request.created_by,
    )
    session.add(row)
    session.flush()
    return row


def _counts(rows: dict[str, list[Any]]) -> dict[str, int]:
    return {
        "court_keypoint_count": len(rows["court_keypoints"]),
        "court_line_count": len(rows["court_lines"]),
        "camera_view_count": len(rows["camera_view"]),
        "homography_candidate_count": len(rows["homography_candidates"]),
        "projection_diagnostic_count": len(rows["projection_diagnostics"]),
    }


def _query_spec(request: CourtReviewDatasetExportRequest) -> dict[str, Any]:
    return {
        "media_id": request.media_id,
        "court_run_id": request.court_run_id,
        "homography_run_id": request.homography_run_id,
        "projection_diagnostic_run_id": request.projection_diagnostic_run_id,
        "include_annotations": request.include_annotations,
        "include_artifacts": request.include_artifacts,
        "format": request.format,
        "query_name": request.query_name,
    }


def _export_path(output_root: str | Path, export_id: str, export_format: str) -> Path:
    return (
        Path(output_root).expanduser().resolve()
        / "court"
        / export_id
        / f"court_review_dataset.{export_format}"
    )


def _dt(value: Any) -> str | None:
    return value.isoformat() if value is not None else None


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


def _runtime_config_payload(row: RuntimeConfig) -> dict[str, Any]:
    return {
        "id": row.id,
        "config_name": row.config_name,
        "config_version": row.config_version,
        "payload_jsonb": row.payload_jsonb,
        "created_at": _dt(row.created_at),
    }


def _model_payload(row: ModelRegistry) -> dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "version": row.version,
        "model_family": row.model_family,
        "source": row.source,
        "metadata_jsonb": row.metadata_jsonb,
        "created_at": _dt(row.created_at),
    }


def _court_keypoint_payload(row: CourtKeypointObservation) -> dict[str, Any]:
    return {
        "observation_id": row.observation_id,
        "media_id": row.media_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "court_keypoint_schema": row.court_keypoint_schema,
        "schema_version": row.schema_version,
        "keypoints_jsonb": row.keypoints_jsonb,
        "keypoint_count": row.keypoint_count,
        "keypoints_present_count": row.keypoints_present_count,
        "keypoints_missing_count": row.keypoints_missing_count,
        "mean_keypoint_confidence": row.mean_keypoint_confidence,
        "frame_time_owner": row.frame_time_owner,
        "metadata_jsonb": row.metadata_jsonb,
    }


def _court_line_payload(row: CourtLineObservation) -> dict[str, Any]:
    return {
        "observation_id": row.observation_id,
        "media_id": row.media_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "line_segments_jsonb": row.line_segments_jsonb,
        "line_classes_jsonb": row.line_classes_jsonb,
        "line_count": row.line_count,
        "mean_line_confidence": row.mean_line_confidence,
        "frame_time_owner": row.frame_time_owner,
        "metadata_jsonb": row.metadata_jsonb,
    }


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
        "frame_time_owner": row.frame_time_owner,
        "metadata_jsonb": row.metadata_jsonb,
    }


def _homography_payload(row: HomographyCandidateObservation) -> dict[str, Any]:
    return {
        "observation_id": row.observation_id,
        "media_id": row.media_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "source_court_keypoint_observation_id": row.source_court_keypoint_observation_id,
        "source_court_line_observation_id": row.source_court_line_observation_id,
        "source_camera_view_observation_id": row.source_camera_view_observation_id,
        "homography_matrix_jsonb": row.homography_matrix_jsonb,
        "inverse_homography_matrix_jsonb": row.inverse_homography_matrix_jsonb,
        "matrix_direction": row.matrix_direction,
        "template_name": row.template_name,
        "template_version": row.template_version,
        "reprojection_error_mean": row.reprojection_error_mean,
        "reprojection_error_median": row.reprojection_error_median,
        "reprojection_error_max": row.reprojection_error_max,
        "source_point_count": row.source_point_count,
        "source_line_count": row.source_line_count,
        "confidence": row.confidence,
        "status": row.status,
        "frame_time_owner": row.frame_time_owner,
        "metadata_jsonb": row.metadata_jsonb,
    }


def _projection_diagnostic_payload(row: ProjectionDiagnosticObservation) -> dict[str, Any]:
    return {
        "observation_id": row.observation_id,
        "media_id": row.media_id,
        "run_id": row.run_id,
        "frame_number": row.frame_number,
        "timestamp_ms": row.timestamp_ms,
        "source_homography_candidate_observation_id": (
            row.source_homography_candidate_observation_id
        ),
        "projected_template_keypoints_jsonb": row.projected_template_keypoints_jsonb,
        "projected_template_lines_jsonb": row.projected_template_lines_jsonb,
        "diagnostic_metrics_jsonb": row.diagnostic_metrics_jsonb,
        "overlay_artifact_id": row.overlay_artifact_id,
        "confidence": row.confidence,
        "status": row.status,
        "frame_time_owner": row.frame_time_owner,
        "metadata_jsonb": row.metadata_jsonb,
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


def _artifact_payload(row: EvidenceArtifact) -> dict[str, Any]:
    return {
        "id": row.id,
        "media_id": row.media_id,
        "run_id": row.run_id,
        "target_observation_id": row.target_observation_id,
        "artifact_type": row.artifact_type,
        "uri": row.uri,
        "frame_start": row.frame_start,
        "frame_end": row.frame_end,
        "timestamp_start_ms": row.timestamp_start_ms,
        "timestamp_end_ms": row.timestamp_end_ms,
        "checksum": row.checksum,
        "metadata_jsonb": row.metadata_jsonb,
        "created_at": _dt(row.created_at),
    }


def _annotation_payload(row: HumanAnnotation) -> dict[str, Any]:
    return {
        "id": row.id,
        "media_id": row.media_id,
        "observation_id": row.observation_id,
        "evidence_artifact_id": row.evidence_artifact_id,
        "frame_start": row.frame_start,
        "frame_end": row.frame_end,
        "timestamp_start_ms": row.timestamp_start_ms,
        "timestamp_end_ms": row.timestamp_end_ms,
        "annotation_type": row.annotation_type,
        "payload_jsonb": row.payload_jsonb,
        "created_by": row.created_by,
        "created_at": _dt(row.created_at),
    }
