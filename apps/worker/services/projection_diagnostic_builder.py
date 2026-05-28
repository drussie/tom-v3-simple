from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.court import (
    COURT_TEMPLATE_NAME,
    COURT_TEMPLATE_VERSION,
    ProjectionDiagnosticObservationCreate,
    get_court_template,
)
from tom_v3_schema.enums import (
    CoordinateSpace,
    ObservationFamily,
    ObservationGranularity,
    RelationshipType,
)
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    HomographyCandidateObservation,
    MediaAsset,
    ModelRegistry,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

PROJECTION_DIAGNOSTIC_WARNINGS = {
    "projection_diagnostic_only": True,
    "diagnostic_geometry": True,
    "observation_only": True,
    "no_adjudication": True,
    "not_ball_player_projection": True,
    "no_tennis_event_interpretation": True,
}

DIAGNOSTIC_METHOD = "template_projection_diagnostic_v0"


def build_projection_diagnostic_plan(
    *,
    media_id: str = "<media_id>",
    homography_run_id: str = "<homography_run_id>",
    run_name: str = "projection-diagnostic-builder",
    frame_start: int | None = None,
    frame_end: int | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    command_parts = [
        "python -m apps.worker.cli build-projection-diagnostics",
        f"--media-id {media_id}",
        f"--homography-run-id {homography_run_id}",
    ]
    if frame_start is not None:
        command_parts.append(f"--frame-start {frame_start}")
    if frame_end is not None:
        command_parts.append(f"--frame-end {frame_end}")

    return {
        "steps": [
            "validate_media",
            "validate_source_homography_run",
            "query_source_homography_candidate_observations",
            "create_projection_diagnostic_model_registry_row",
            "create_projection_diagnostic_runtime_config",
            "create_processing_run_and_step",
            "project_court_template_geometry_into_image_pixels",
            "persist_projection_diagnostic_observations",
            "write_homography_candidate_lineage",
        ],
        "command": " ".join(command_parts),
        "run_name": run_name,
        "source_homography_run_id": homography_run_id,
        "frame_filter": {
            "frame_start": frame_start,
            "frame_end": frame_end,
            "frame_time_owner": "media_indexing",
        },
        "diagnostic_config": {
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "diagnostic_method": DIAGNOSTIC_METHOD,
            "coordinate_space": "image_pixels",
            "not_ball_player_projection": True,
        },
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
            f"?homographyRunId={homography_run_id}&projectionDiagnosticRunId=<run_id>"
        ),
        "warnings": dict(PROJECTION_DIAGNOSTIC_WARNINGS),
    }


def build_projection_diagnostics(
    *,
    session: Session,
    media_id: str,
    homography_run_id: str,
    run_name: str = "projection-diagnostic-builder",
    frame_start: int | None = None,
    frame_end: int | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    if frame_start is not None and frame_end is not None and frame_end < frame_start:
        return _failed(
            "invalid_frame_range",
            "frame_end must be greater than or equal to frame_start",
        )

    plan = build_projection_diagnostic_plan(
        media_id=media_id,
        homography_run_id=homography_run_id,
        run_name=run_name,
        frame_start=frame_start,
        frame_end=frame_end,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "projection diagnostic build planned",
            "plan": plan,
            "warnings": dict(PROJECTION_DIAGNOSTIC_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    source_run = session.get(ProcessingRun, homography_run_id)
    if source_run is None:
        return _failed(
            "missing_homography_run",
            f"homography run not found: {homography_run_id}",
        )
    if source_run.media_id != media.id:
        return _failed(
            "homography_run_media_mismatch",
            f"homography run {homography_run_id} does not belong to media {media.id}",
        )

    homographies = _source_homographies(
        session=session,
        media_id=media.id,
        homography_run_id=homography_run_id,
        frame_start=frame_start,
        frame_end=frame_end,
    )

    model = _get_or_create_projection_diagnostic_model(session)
    runtime_config = _create_runtime_config(
        session=session,
        model=model,
        source_homography_run_id=homography_run_id,
        frame_start=frame_start,
        frame_end=frame_end,
    )
    run = _create_run(
        session=session,
        media=media,
        runtime_config=runtime_config,
        run_name=run_name,
        source_homography_run_id=homography_run_id,
    )
    step = _create_step(
        session=session,
        run=run,
        runtime_config=runtime_config,
        source_homography_run_id=homography_run_id,
    )

    try:
        observations = _persist_projection_diagnostics(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            homographies=homographies,
        )
    except Exception as exc:
        _mark_failed(session=session, run=run, step=step, message=str(exc))
        raise

    statuses = Counter(
        observation.projection_diagnostic.status
        for observation in observations
        if observation.projection_diagnostic is not None
    )
    sampled_frames = [homography.frame_number for homography in homographies]
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_homography_candidate_count=len(homographies),
        projection_diagnostic_count=sum(statuses.values()),
        insufficient_homography_count=statuses.get("insufficient_homography", 0),
        sampled_frames=sampled_frames,
    )

    return {
        "ok": True,
        "status": "completed",
        "message": "projection diagnostic build complete",
        "media_id": media.id,
        "source_homography_run_id": homography_run_id,
        "projection_diagnostic_run_id": run.id,
        "run_id": run.id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "projection_diagnostics": {
            "diagnostic_candidate": statuses.get("diagnostic_candidate", 0),
            "insufficient_homography": statuses.get("insufficient_homography", 0),
            "total": sum(statuses.values()),
        },
        "source_counts": {
            "homography_candidate_observations": len(homographies),
        },
        "sampled_frames": sampled_frames,
        "observation_ids": [observation.id for observation in observations],
        "replay_url": (
            f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
            f"?homographyRunId={homography_run_id}&projectionDiagnosticRunId={run.id}"
        ),
        "warnings": dict(PROJECTION_DIAGNOSTIC_WARNINGS),
    }


def project_template_geometry_from_homography(
    homography: HomographyCandidateObservation,
) -> dict[str, Any]:
    matrix = _template_to_image_matrix(homography)
    if matrix is None:
        return {
            "status": "insufficient_homography",
            "projected_template_keypoints_jsonb": [],
            "projected_template_lines_jsonb": [],
            "diagnostic_metrics_jsonb": {
                "source_homography_status": homography.status,
                "diagnostic_method": DIAGNOSTIC_METHOD,
                "insufficient_reason": "missing_template_to_image_matrix",
                "diagnostic_evidence_only": True,
                "not_ball_player_projection": True,
            },
            "confidence": None,
        }

    template = get_court_template(
        template_name=homography.template_name or COURT_TEMPLATE_NAME,
        template_version=homography.template_version or COURT_TEMPLATE_VERSION,
    )
    projected_keypoints = []
    points_by_name: dict[str, dict[str, Any]] = {}
    for keypoint in template.keypoints:
        projected = _apply_matrix(matrix, keypoint.x, keypoint.y)
        item = {
            "name": keypoint.name,
            "template_x": keypoint.x,
            "template_y": keypoint.y,
            "image_x": _round(projected[0]) if projected is not None else None,
            "image_y": _round(projected[1]) if projected is not None else None,
            "valid": projected is not None,
        }
        projected_keypoints.append(item)
        points_by_name[keypoint.name] = item

    projected_lines = []
    for line in template.lines:
        start = points_by_name.get(line.start_keypoint)
        end = points_by_name.get(line.end_keypoint)
        valid = bool(start and end and start["valid"] and end["valid"])
        projected_lines.append(
            {
                "line_class": line.line_class,
                "start_keypoint": line.start_keypoint,
                "end_keypoint": line.end_keypoint,
                "x1": start["image_x"] if start is not None else None,
                "y1": start["image_y"] if start is not None else None,
                "x2": end["image_x"] if end is not None else None,
                "y2": end["image_y"] if end is not None else None,
                "valid": valid,
            }
        )

    projected_keypoint_count = sum(1 for point in projected_keypoints if point["valid"])
    projected_line_count = sum(1 for line in projected_lines if line["valid"])
    source_line_count = homography.source_line_count or 0
    metrics = {
        "source_homography_status": homography.status,
        "template_keypoint_count": len(template.keypoints),
        "projected_keypoint_count": projected_keypoint_count,
        "projected_line_count": projected_line_count,
        "source_point_count": homography.source_point_count or 0,
        "source_line_count": source_line_count,
        "line_count_delta": projected_line_count - source_line_count,
        "source_reprojection_error_mean": homography.reprojection_error_mean,
        "source_reprojection_error_median": homography.reprojection_error_median,
        "source_reprojection_error_max": homography.reprojection_error_max,
        "source_homography_confidence": homography.confidence,
        "diagnostic_method": DIAGNOSTIC_METHOD,
        "diagnostic_evidence_only": True,
        "not_ball_player_projection": True,
    }
    return {
        "status": "diagnostic_candidate",
        "projected_template_keypoints_jsonb": projected_keypoints,
        "projected_template_lines_jsonb": projected_lines,
        "diagnostic_metrics_jsonb": metrics,
        "confidence": homography.confidence,
    }


def _source_homographies(
    *,
    session: Session,
    media_id: str,
    homography_run_id: str,
    frame_start: int | None,
    frame_end: int | None,
) -> list[HomographyCandidateObservation]:
    query = (
        select(HomographyCandidateObservation)
        .where(
            HomographyCandidateObservation.media_id == media_id,
            HomographyCandidateObservation.run_id == homography_run_id,
        )
        .order_by(
            HomographyCandidateObservation.frame_number,
            HomographyCandidateObservation.observation_id,
        )
    )
    if frame_start is not None:
        query = query.where(HomographyCandidateObservation.frame_number >= frame_start)
    if frame_end is not None:
        query = query.where(HomographyCandidateObservation.frame_number <= frame_end)
    return list(session.scalars(query).all())


def _get_or_create_projection_diagnostic_model(session: Session) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == "projection-diagnostic-builder",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "court",
        )
    )
    if model is not None:
        return model

    model = ModelRegistry(
        name="projection-diagnostic-builder",
        version="v0",
        model_family="court",
        source="apps.worker.services.projection_diagnostic_builder",
        metadata_jsonb={
            "builder_name": "projection-diagnostic-builder",
            "projection_diagnostic_builder": True,
            "diagnostic_geometry": True,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "not_ball_player_projection": True,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    model: ModelRegistry,
    source_homography_run_id: str,
    frame_start: int | None,
    frame_end: int | None,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="projection-diagnostic-builder-config",
        config_version="v0",
        payload_jsonb={
            "model_registry_id": model.id,
            "builder_name": "projection-diagnostic-builder",
            "source_homography_run_id": source_homography_run_id,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "diagnostic_method": DIAGNOSTIC_METHOD,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "diagnostic_geometry": True,
            "observation_only": True,
            "no_adjudication": True,
            "not_ball_player_projection": True,
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _create_run(
    *,
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    source_homography_run_id: str,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "blueprint": 8,
            "milestone": "8F",
            "builder_name": "projection-diagnostic-builder",
            "source_homography_run_id": source_homography_run_id,
            "diagnostic_geometry": True,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "not_ball_player_projection": True,
            "no_tennis_event_interpretation": True,
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    *,
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
    source_homography_run_id: str,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="projection_diagnostic_builder",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "builder_name": "projection-diagnostic-builder",
            "source_homography_run_id": source_homography_run_id,
            "diagnostic_geometry": True,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "not_ball_player_projection": True,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _persist_projection_diagnostics(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    homographies: list[HomographyCandidateObservation],
):
    writer = ObservationWriter(session)
    observations = []
    for homography in homographies:
        projected = project_template_geometry_from_homography(homography)
        diagnostic = ProjectionDiagnosticObservationCreate(
            frame_number=homography.frame_number,
            timestamp_ms=homography.timestamp_ms,
            source_homography_candidate_observation_id=homography.observation_id,
            projected_template_keypoints_jsonb=projected["projected_template_keypoints_jsonb"],
            projected_template_lines_jsonb=projected["projected_template_lines_jsonb"],
            diagnostic_metrics_jsonb=projected["diagnostic_metrics_jsonb"],
            confidence=projected["confidence"],
            status=projected["status"],
            metadata_jsonb=_metadata(homography=homography, projected=projected),
        )
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family=ObservationFamily.court,
                    observation_type="projection_diagnostic_observation",
                    granularity=ObservationGranularity.frame,
                    frame_start=homography.frame_number,
                    frame_end=homography.frame_number,
                    timestamp_start_ms=homography.timestamp_ms,
                    timestamp_end_ms=homography.timestamp_ms,
                    confidence=diagnostic.confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space=CoordinateSpace.image_pixels,
                    payload_jsonb=_observation_payload(
                        step=step,
                        typed_payload=diagnostic.model_dump(mode="json"),
                    ),
                    idempotency_key=(
                        f"{run.id}:projection-diagnostic:{homography.observation_id}"
                    ),
                    projection_diagnostic=diagnostic,
                    lineage=_lineage(
                        homography=homography,
                        processing_step_id=step.id,
                    ),
                )
            )
        )
    return observations


def _lineage(
    *,
    homography: HomographyCandidateObservation,
    processing_step_id: str,
) -> list[ObservationLineageCreate]:
    return [
        ObservationLineageCreate(
            parent_observation_id=homography.observation_id,
            relationship_type=RelationshipType.projection_diagnostic_for_homography_candidate,
            processing_step_id=processing_step_id,
            payload_jsonb={
                "geometry_evidence_only": True,
                "diagnostic_candidate": True,
                "observation_only": True,
                "no_adjudication": True,
                "not_ball_player_projection": True,
                "source_evidence_type": "homography_candidate_observation",
            },
        )
    ]


def _metadata(
    *,
    homography: HomographyCandidateObservation,
    projected: dict[str, Any],
) -> dict[str, Any]:
    return {
        "builder_name": "projection-diagnostic-builder",
        "builder_version": "v0",
        "projection_diagnostic_only": True,
        "diagnostic_geometry": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "frame_time_owner": "media_indexing",
        "diagnostic_method": DIAGNOSTIC_METHOD,
        "source_homography_candidate_observation_id": homography.observation_id,
        "source_homography_status": homography.status,
        "not_ball_player_projection": True,
        "no_tennis_event_interpretation": True,
        "projected_keypoint_count": projected["diagnostic_metrics_jsonb"].get(
            "projected_keypoint_count"
        ),
        "projected_line_count": projected["diagnostic_metrics_jsonb"].get(
            "projected_line_count"
        ),
    }


def _observation_payload(
    *,
    step: ProcessingStep,
    typed_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "observation_type": "projection_diagnostic_observation",
        "processing_step_id": step.id,
        "builder_name": "projection-diagnostic-builder",
        "builder_version": "v0",
        "projection_diagnostic": True,
        "diagnostic_candidate": True,
        "diagnostic_geometry": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "frame_time_owner": "media_indexing",
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "not_ball_player_projection": True,
        "no_tennis_event_interpretation": True,
        "typed_payload": typed_payload,
    }


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_homography_candidate_count: int,
    projection_diagnostic_count: int,
    insufficient_homography_count: int,
    sampled_frames: list[int],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "source_homography_candidate_count": source_homography_candidate_count,
        "projection_diagnostic_count": projection_diagnostic_count,
        "insufficient_homography_count": insufficient_homography_count,
        "sampled_frames": sampled_frames,
        "diagnostic_geometry": True,
        "geometry_evidence_only": True,
        "observation_only": True,
        "no_adjudication": True,
        "not_ball_player_projection": True,
    }
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        **summary,
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        **summary,
    }
    session.commit()


def _mark_failed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        "error": message,
        "observation_only": True,
        "no_adjudication": True,
        "not_ball_player_projection": True,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        "observation_only": True,
        "no_adjudication": True,
        "not_ball_player_projection": True,
    }
    session.commit()


def _failed(
    status: str,
    message: str,
    error_type: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(PROJECTION_DIAGNOSTIC_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result


def _template_to_image_matrix(
    homography: HomographyCandidateObservation,
) -> list[list[float]] | None:
    if (
        homography.matrix_direction == "image_pixels_to_court_template_2d"
        and homography.inverse_homography_matrix_jsonb is not None
    ):
        return _matrix_or_none(homography.inverse_homography_matrix_jsonb)
    if homography.matrix_direction == "court_template_2d_to_image_pixels":
        return _matrix_or_none(homography.homography_matrix_jsonb)
    return None


def _matrix_or_none(value: Any) -> list[list[float]] | None:
    if not isinstance(value, list) or len(value) != 3:
        return None
    matrix: list[list[float]] = []
    for row in value:
        if not isinstance(row, list) or len(row) != 3:
            return None
        matrix.append([float(cell) for cell in row])
    return matrix


def _apply_matrix(matrix: list[list[float]], x: float, y: float) -> tuple[float, float] | None:
    scale = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2]
    if abs(scale) < 1e-12:
        return None
    projected_x = (matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]) / scale
    projected_y = (matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]) / scale
    return projected_x, projected_y


def _round(value: float) -> float:
    return round(float(value), 6)
