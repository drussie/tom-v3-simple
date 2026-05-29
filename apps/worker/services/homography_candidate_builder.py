from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from math import sqrt
from statistics import median
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.court import (
    COURT_TEMPLATE_COORDINATE_SPACE,
    COURT_TEMPLATE_NAME,
    COURT_TEMPLATE_VERSION,
    HomographyCandidateObservationCreate,
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
    CameraViewObservation,
    CourtKeypointObservation,
    CourtLineObservation,
    MediaAsset,
    ModelRegistry,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

HOMOGRAPHY_WARNINGS = {
    "homography_candidate_only": True,
    "candidate_geometry": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_projection_diagnostics": True,
    "no_ball_player_court_projection": True,
    "no_tennis_event_interpretation": True,
}

MIN_SOURCE_POINTS = 4


def build_homography_candidate_plan(
    *,
    media_id: str = "<media_id>",
    court_run_id: str = "<court_run_id>",
    run_name: str = "homography-candidate-builder",
    frame_start: int | None = None,
    frame_end: int | None = None,
    min_keypoint_confidence: float = 0.0,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    command_parts = [
        "python -m apps.worker.cli build-homography-candidates",
        f"--media-id {media_id}",
        f"--court-run-id {court_run_id}",
    ]
    if frame_start is not None:
        command_parts.append(f"--frame-start {frame_start}")
    if frame_end is not None:
        command_parts.append(f"--frame-end {frame_end}")
    if min_keypoint_confidence:
        command_parts.append(f"--min-keypoint-confidence {min_keypoint_confidence}")

    return {
        "steps": [
            "validate_media",
            "validate_source_court_run",
            "query_source_court_keypoint_observations",
            "query_optional_court_line_and_camera_view_context",
            "create_homography_model_registry_row",
            "create_homography_runtime_config",
            "create_processing_run_and_step",
            "compute_candidate_homographies",
            "persist_homography_candidate_observations",
            "write_source_evidence_lineage",
        ],
        "command": " ".join(command_parts),
        "run_name": run_name,
        "source_court_run_id": court_run_id,
        "frame_filter": {
            "frame_start": frame_start,
            "frame_end": frame_end,
            "frame_time_owner": "media_indexing",
        },
        "candidate_config": {
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "source_coordinate_space": "image_pixels",
            "target_coordinate_space": COURT_TEMPLATE_COORDINATE_SPACE,
            "matrix_direction": "image_pixels_to_court_template_2d",
            "min_keypoint_confidence": min_keypoint_confidence,
            "min_source_points": MIN_SOURCE_POINTS,
            "frame_time_owner": "media_indexing",
        },
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}"
            f"?courtRunId={court_run_id}&homographyRunId=<run_id>"
        ),
        "warnings": dict(HOMOGRAPHY_WARNINGS),
    }


def build_homography_candidates(
    *,
    session: Session,
    media_id: str,
    court_run_id: str,
    run_name: str = "homography-candidate-builder",
    frame_start: int | None = None,
    frame_end: int | None = None,
    min_keypoint_confidence: float = 0.0,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    if min_keypoint_confidence < 0:
        return _failed(
            "invalid_min_keypoint_confidence",
            "min_keypoint_confidence must be greater than or equal to zero",
        )
    if frame_start is not None and frame_end is not None and frame_end < frame_start:
        return _failed(
            "invalid_frame_range",
            "frame_end must be greater than or equal to frame_start",
        )

    plan = build_homography_candidate_plan(
        media_id=media_id,
        court_run_id=court_run_id,
        run_name=run_name,
        frame_start=frame_start,
        frame_end=frame_end,
        min_keypoint_confidence=min_keypoint_confidence,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "homography candidate build planned",
            "plan": plan,
            "warnings": dict(HOMOGRAPHY_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    source_run = session.get(ProcessingRun, court_run_id)
    if source_run is None:
        return _failed("missing_court_run", f"court run not found: {court_run_id}")
    if source_run.media_id != media.id:
        return _failed(
            "court_run_media_mismatch",
            f"court run {court_run_id} does not belong to media {media.id}",
        )

    keypoints = _source_keypoints(
        session=session,
        media_id=media.id,
        court_run_id=court_run_id,
        frame_start=frame_start,
        frame_end=frame_end,
    )
    lines_by_frame = _source_lines_by_frame(
        session=session,
        media_id=media.id,
        court_run_id=court_run_id,
        frame_start=frame_start,
        frame_end=frame_end,
    )
    camera_by_frame = _source_camera_by_frame(
        session=session,
        media_id=media.id,
        court_run_id=court_run_id,
        frame_start=frame_start,
        frame_end=frame_end,
    )

    model = _get_or_create_homography_model(session)
    runtime_config = _create_runtime_config(
        session=session,
        model=model,
        source_court_run_id=court_run_id,
        frame_start=frame_start,
        frame_end=frame_end,
        min_keypoint_confidence=min_keypoint_confidence,
    )
    run = _create_run(
        session=session,
        media=media,
        runtime_config=runtime_config,
        run_name=run_name,
        source_court_run_id=court_run_id,
    )
    step = _create_step(
        session=session,
        run=run,
        runtime_config=runtime_config,
        source_court_run_id=court_run_id,
    )

    try:
        observations = _persist_homography_candidates(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            keypoints=keypoints,
            lines_by_frame=lines_by_frame,
            camera_by_frame=camera_by_frame,
            min_keypoint_confidence=min_keypoint_confidence,
        )
    except Exception as exc:
        _mark_failed(session=session, run=run, step=step, message=str(exc))
        raise

    statuses = Counter(
        observation.homography_candidate.status
        for observation in observations
        if observation.homography_candidate is not None
    )
    insufficient_count = len(keypoints) - sum(statuses.values())
    sampled_frames = [keypoint.frame_number for keypoint in keypoints]
    _mark_completed(
        session=session,
        run=run,
        step=step,
        source_keypoint_count=len(keypoints),
        source_line_count=len(lines_by_frame),
        source_camera_count=len(camera_by_frame),
        candidate_count=statuses.get("candidate", 0),
        insufficient_count=insufficient_count,
        sampled_frames=sampled_frames,
    )

    total = sum(statuses.values())
    return {
        "ok": True,
        "status": "completed",
        "message": "homography candidate build complete",
        "media_id": media.id,
        "source_court_run_id": court_run_id,
        "homography_run_id": run.id,
        "run_id": run.id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "homography_candidates": {
            "candidate": statuses.get("candidate", 0),
            "insufficient_source_evidence": insufficient_count,
            "total": total,
        },
        "source_counts": {
            "court_keypoint_observations": len(keypoints),
            "court_line_observations": len(lines_by_frame),
            "camera_view_observations": len(camera_by_frame),
        },
        "sampled_frames": sampled_frames,
        "observation_ids": [observation.id for observation in observations],
        "replay_url": (
            f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
            f"?courtRunId={court_run_id}&homographyRunId={run.id}"
        ),
        "warnings": dict(HOMOGRAPHY_WARNINGS),
    }


def compute_homography_candidate_from_keypoints(
    keypoints_jsonb: list[dict[str, Any]],
    *,
    min_keypoint_confidence: float = 0.0,
) -> dict[str, Any]:
    template = get_court_template()
    template_by_name = {keypoint.name: keypoint for keypoint in template.keypoints}
    pairs: list[dict[str, Any]] = []
    for keypoint in keypoints_jsonb:
        name = str(keypoint.get("name"))
        template_keypoint = template_by_name.get(name)
        if template_keypoint is None:
            continue
        if keypoint.get("present") is not True:
            continue
        if keypoint.get("x") is None or keypoint.get("y") is None:
            continue
        confidence = keypoint.get("confidence")
        if confidence is not None and float(confidence) < min_keypoint_confidence:
            continue
        pairs.append(
            {
                "name": name,
                "source": (float(keypoint["x"]), float(keypoint["y"])),
                "target": (float(template_keypoint.x), float(template_keypoint.y)),
                "confidence": float(confidence) if confidence is not None else None,
            }
        )

    if len(pairs) < MIN_SOURCE_POINTS:
        return {
            "status": "insufficient_source_evidence",
            "source_point_count": len(pairs),
            "required_source_point_count": MIN_SOURCE_POINTS,
        }

    x_fit = _fit_axis(
        [(pair["source"][0], pair["target"][0]) for pair in pairs],
        axis_name="x",
    )
    y_fit = _fit_axis(
        [(pair["source"][1], pair["target"][1]) for pair in pairs],
        axis_name="y",
    )
    matrix = [
        [_round(x_fit["scale"]), 0.0, _round(x_fit["offset"])],
        [0.0, _round(y_fit["scale"]), _round(y_fit["offset"])],
        [0.0, 0.0, 1.0],
    ]
    inverse = _inverse_affine_matrix(matrix)
    errors = [
        _point_error(_apply_matrix(matrix, pair["source"][0], pair["source"][1]), pair["target"])
        for pair in pairs
    ]
    mean_error = sum(errors) / len(errors)
    confidences = [pair["confidence"] for pair in pairs if pair["confidence"] is not None]
    mean_confidence = sum(confidences) / len(confidences) if confidences else 0.5
    confidence = max(0.0, min(1.0, mean_confidence - mean_error))

    return {
        "status": "candidate",
        "homography_matrix_jsonb": matrix,
        "inverse_homography_matrix_jsonb": inverse,
        "reprojection_error_mean": _round(mean_error),
        "reprojection_error_median": _round(median(errors)),
        "reprojection_error_max": _round(max(errors)),
        "inlier_count": sum(error <= 0.03 for error in errors),
        "outlier_count": sum(error > 0.03 for error in errors),
        "source_point_count": len(pairs),
        "confidence": round(confidence, 6),
        "usable_keypoint_names": [pair["name"] for pair in pairs],
        "matrix_method": "axis_aligned_affine_fit_v0",
    }


def _source_keypoints(
    *,
    session: Session,
    media_id: str,
    court_run_id: str,
    frame_start: int | None,
    frame_end: int | None,
) -> list[CourtKeypointObservation]:
    query = (
        select(CourtKeypointObservation)
        .where(
            CourtKeypointObservation.media_id == media_id,
            CourtKeypointObservation.run_id == court_run_id,
        )
        .order_by(CourtKeypointObservation.frame_number, CourtKeypointObservation.observation_id)
    )
    if frame_start is not None:
        query = query.where(CourtKeypointObservation.frame_number >= frame_start)
    if frame_end is not None:
        query = query.where(CourtKeypointObservation.frame_number <= frame_end)
    return list(session.scalars(query).all())


def _source_lines_by_frame(
    *,
    session: Session,
    media_id: str,
    court_run_id: str,
    frame_start: int | None,
    frame_end: int | None,
) -> dict[int, CourtLineObservation]:
    query = (
        select(CourtLineObservation)
        .where(
            CourtLineObservation.media_id == media_id,
            CourtLineObservation.run_id == court_run_id,
        )
        .order_by(CourtLineObservation.frame_number, CourtLineObservation.observation_id)
    )
    if frame_start is not None:
        query = query.where(CourtLineObservation.frame_number >= frame_start)
    if frame_end is not None:
        query = query.where(CourtLineObservation.frame_number <= frame_end)
    return _first_by_frame(session.scalars(query).all())


def _source_camera_by_frame(
    *,
    session: Session,
    media_id: str,
    court_run_id: str,
    frame_start: int | None,
    frame_end: int | None,
) -> dict[int, CameraViewObservation]:
    query = (
        select(CameraViewObservation)
        .where(
            CameraViewObservation.media_id == media_id,
            CameraViewObservation.run_id == court_run_id,
        )
        .order_by(CameraViewObservation.frame_number, CameraViewObservation.observation_id)
    )
    if frame_start is not None:
        query = query.where(CameraViewObservation.frame_number >= frame_start)
    if frame_end is not None:
        query = query.where(CameraViewObservation.frame_number <= frame_end)
    return _first_by_frame(session.scalars(query).all())


def _first_by_frame(
    rows: list[CourtLineObservation] | list[CameraViewObservation],
) -> dict[int, CourtLineObservation] | dict[int, CameraViewObservation]:
    by_frame: dict[int, CourtLineObservation | CameraViewObservation] = {}
    for row in rows:
        by_frame.setdefault(row.frame_number, row)
    return by_frame


def _get_or_create_homography_model(session: Session) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == "fixture-homography-candidate-builder",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "court",
        )
    )
    if model is not None:
        return model

    model = ModelRegistry(
        name="fixture-homography-candidate-builder",
        version="v0",
        model_family="court",
        source="apps.worker.services.homography_candidate_builder",
        metadata_jsonb={
            "builder_name": "fixture-homography-candidate-builder",
            "homography_candidate_builder": True,
            "candidate_geometry": True,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "no_projection_diagnostics": True,
            "no_ball_player_court_projection": True,
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
    source_court_run_id: str,
    frame_start: int | None,
    frame_end: int | None,
    min_keypoint_confidence: float,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="homography-candidate-builder-config",
        config_version="v0",
        payload_jsonb={
            "model_registry_id": model.id,
            "builder_name": "fixture-homography-candidate-builder",
            "source_court_run_id": source_court_run_id,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "source_coordinate_space": "image_pixels",
            "target_coordinate_space": COURT_TEMPLATE_COORDINATE_SPACE,
            "matrix_direction": "image_pixels_to_court_template_2d",
            "matrix_method": "axis_aligned_affine_fit_v0",
            "frame_start": frame_start,
            "frame_end": frame_end,
            "min_keypoint_confidence": min_keypoint_confidence,
            "min_source_points": MIN_SOURCE_POINTS,
            "candidate_geometry": True,
            "observation_only": True,
            "no_adjudication": True,
            "no_projection_diagnostics": True,
            "no_ball_player_court_projection": True,
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
    source_court_run_id: str,
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
            "milestone": "8D",
            "builder_name": "fixture-homography-candidate-builder",
            "source_court_run_id": source_court_run_id,
            "candidate_geometry": True,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "no_projection_diagnostics": True,
            "no_ball_player_court_projection": True,
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
    source_court_run_id: str,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="homography_candidate_builder",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "builder_name": "fixture-homography-candidate-builder",
            "source_court_run_id": source_court_run_id,
            "candidate_geometry": True,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "no_projection_diagnostics": True,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _persist_homography_candidates(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    keypoints: list[CourtKeypointObservation],
    lines_by_frame: dict[int, CourtLineObservation],
    camera_by_frame: dict[int, CameraViewObservation],
    min_keypoint_confidence: float,
):
    writer = ObservationWriter(session)
    observations = []
    for keypoint in keypoints:
        candidate = compute_homography_candidate_from_keypoints(
            keypoint.keypoints_jsonb,
            min_keypoint_confidence=min_keypoint_confidence,
        )
        if candidate["status"] != "candidate":
            continue

        line = lines_by_frame.get(keypoint.frame_number)
        camera = camera_by_frame.get(keypoint.frame_number)
        line_count = line.line_count if line is not None else 0
        homography = HomographyCandidateObservationCreate(
            frame_number=keypoint.frame_number,
            timestamp_ms=keypoint.timestamp_ms,
            source_court_keypoint_observation_id=keypoint.observation_id,
            source_court_line_observation_id=line.observation_id if line is not None else None,
            source_camera_view_observation_id=(
                camera.observation_id if camera is not None else None
            ),
            homography_matrix_jsonb=candidate["homography_matrix_jsonb"],
            inverse_homography_matrix_jsonb=candidate["inverse_homography_matrix_jsonb"],
            source_coordinate_space="image_pixels",
            target_coordinate_space=COURT_TEMPLATE_COORDINATE_SPACE,
            matrix_direction="image_pixels_to_court_template_2d",
            template_name=COURT_TEMPLATE_NAME,
            template_version=COURT_TEMPLATE_VERSION,
            reprojection_error_mean=candidate["reprojection_error_mean"],
            reprojection_error_median=candidate["reprojection_error_median"],
            reprojection_error_max=candidate["reprojection_error_max"],
            inlier_count=candidate["inlier_count"],
            outlier_count=candidate["outlier_count"],
            source_point_count=candidate["source_point_count"],
            source_line_count=line_count,
            confidence=candidate["confidence"],
            status="candidate",
            metadata_jsonb=_metadata(candidate, keypoint=keypoint, line=line, camera=camera),
        )
        source_metadata = _source_court_evidence_metadata(
            keypoint=keypoint,
            line=line,
            camera=camera,
        )
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family=ObservationFamily.court,
                    observation_type="homography_candidate_observation",
                    granularity=ObservationGranularity.frame,
                    frame_start=keypoint.frame_number,
                    frame_end=keypoint.frame_number,
                    timestamp_start_ms=keypoint.timestamp_ms,
                    timestamp_end_ms=keypoint.timestamp_ms,
                    confidence=homography.confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space=CoordinateSpace.court_template_2d,
                    payload_jsonb=_observation_payload(
                        step=step,
                        typed_payload=homography.model_dump(mode="json"),
                        source_metadata=source_metadata,
                    ),
                    idempotency_key=(
                        f"{run.id}:homography-candidate:{keypoint.frame_number}"
                    ),
                    homography_candidate=homography,
                    lineage=_lineage(
                        keypoint=keypoint,
                        line=line,
                        camera=camera,
                        processing_step_id=step.id,
                    ),
                )
            )
        )
    return observations


def _lineage(
    *,
    keypoint: CourtKeypointObservation,
    line: CourtLineObservation | None,
    camera: CameraViewObservation | None,
    processing_step_id: str,
) -> list[ObservationLineageCreate]:
    payload = {
        "geometry_evidence_only": True,
        "candidate_geometry": True,
        "observation_only": True,
        "no_adjudication": True,
        **_source_court_evidence_metadata(keypoint=keypoint, line=line, camera=camera),
    }
    lineage = [
        ObservationLineageCreate(
            parent_observation_id=keypoint.observation_id,
            relationship_type=RelationshipType.homography_from_court_keypoints_candidate,
            processing_step_id=processing_step_id,
            payload_jsonb={
                **payload,
                "source_evidence_type": "court_keypoint_observation",
            },
        )
    ]
    if line is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=line.observation_id,
                relationship_type=RelationshipType.homography_from_court_lines_candidate,
                processing_step_id=processing_step_id,
                payload_jsonb={
                    **payload,
                    "source_evidence_type": "court_line_observation",
                },
            )
        )
    if camera is not None:
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=camera.observation_id,
                relationship_type=RelationshipType.camera_context_for_homography_candidate,
                processing_step_id=processing_step_id,
                payload_jsonb={
                    **payload,
                    "source_evidence_type": "camera_view_observation",
                },
            )
        )
    return lineage


def _metadata(
    candidate: dict[str, Any],
    *,
    keypoint: CourtKeypointObservation,
    line: CourtLineObservation | None,
    camera: CameraViewObservation | None,
) -> dict[str, Any]:
    return {
        "builder_name": "fixture-homography-candidate-builder",
        "builder_version": "v0",
        "homography_candidate_only": True,
        "candidate_geometry": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "frame_time_owner": "media_indexing",
        "matrix_method": candidate["matrix_method"],
        "usable_keypoint_names": candidate["usable_keypoint_names"],
        "source_line_observation_id": line.observation_id if line is not None else None,
        "source_camera_view_observation_id": (
            camera.observation_id if camera is not None else None
        ),
        **_source_court_evidence_metadata(keypoint=keypoint, line=line, camera=camera),
        "no_projection_diagnostics": True,
        "no_ball_player_court_projection": True,
        "no_tennis_event_interpretation": True,
    }


def _observation_payload(
    *,
    step: ProcessingStep,
    typed_payload: dict[str, Any],
    source_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "observation_type": "homography_candidate_observation",
        "processing_step_id": step.id,
        "builder_name": "fixture-homography-candidate-builder",
        "builder_version": "v0",
        "homography_candidate": True,
        "homography_candidate_only": True,
        "candidate_geometry": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "frame_time_owner": "media_indexing",
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        **(source_metadata or {}),
        "no_projection_diagnostics": True,
        "no_ball_player_court_projection": True,
        "no_tennis_event_interpretation": True,
        "typed_payload": typed_payload,
    }


def _source_court_evidence_metadata(
    *,
    keypoint: CourtKeypointObservation,
    line: CourtLineObservation | None,
    camera: CameraViewObservation | None,
) -> dict[str, Any]:
    keypoint_metadata = keypoint.metadata_jsonb or {}
    keypoint_raw_payload = keypoint.raw_model_payload_jsonb or {}
    line_metadata = line.metadata_jsonb if line is not None else {}
    camera_metadata = camera.metadata_jsonb if camera is not None else {}
    keypoint_real_model_output = bool(
        keypoint_metadata.get("real_model_output")
        or keypoint_metadata.get("tom_v1_court_keypoint_model_output")
    )
    keypoint_fixture = bool(keypoint_metadata.get("fixture_court_evidence"))
    line_derived_from_real_keypoints = bool(
        line_metadata.get("line_source") == "derived_from_real_keypoint_observations"
        or line_metadata.get("real_model_output")
    )
    camera_fixture = bool(camera_metadata.get("fixture_camera_view_evidence"))
    evidence_source = (
        "real_model_output"
        if keypoint_real_model_output
        else "fixture_court_evidence"
        if keypoint_fixture
        else "court_evidence"
    )
    return {
        "source_court_evidence_source": evidence_source,
        "source_court_keypoint_real_model_output": keypoint_real_model_output,
        "source_court_keypoint_fixture_court_evidence": keypoint_fixture,
        "source_court_keypoint_model_output_not_truth": keypoint_real_model_output
        or bool(keypoint_metadata.get("model_output_not_truth")),
        "source_court_keypoint_preprocessing_mode": keypoint_raw_payload.get(
            "preprocessing_mode"
        ),
        "source_court_keypoint_coordinate_interpretation": keypoint_raw_payload.get(
            "coordinate_interpretation"
        ),
        "source_court_keypoint_mapping_version": (
            keypoint_raw_payload.get("mapping_version")
            or keypoint_raw_payload.get("adapter_mapping_version")
        ),
        "source_court_keypoint_uncalibrated_mapping": bool(
            keypoint_metadata.get("uncalibrated_tom_v1_keypoint_mapping")
            or keypoint_raw_payload.get("uncalibrated_tom_v1_keypoint_mapping")
            or keypoint_metadata.get("calibration_audit_v0")
            or keypoint_raw_payload.get("calibration_audit_v0")
        ),
        "homography_from_uncalibrated_tom_v1_keypoints": keypoint_real_model_output,
        "source_court_line_derived_from_real_keypoints": line_derived_from_real_keypoints,
        "source_court_line_fixture_court_evidence": bool(
            line_metadata.get("fixture_court_evidence")
        ),
        "source_camera_view_fixture_evidence": camera_fixture,
        "source_court_keypoint_observation_id": keypoint.observation_id,
        "source_court_line_observation_id": line.observation_id if line is not None else None,
        "source_camera_view_observation_id": (
            camera.observation_id if camera is not None else None
        ),
    }


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    source_keypoint_count: int,
    source_line_count: int,
    source_camera_count: int,
    candidate_count: int,
    insufficient_count: int,
    sampled_frames: list[int],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "source_court_keypoint_count": source_keypoint_count,
        "source_court_line_count": source_line_count,
        "source_camera_view_count": source_camera_count,
        "candidate_count": candidate_count,
        "insufficient_source_evidence_count": insufficient_count,
        "sampled_frames": sampled_frames,
        "candidate_geometry": True,
        "geometry_evidence_only": True,
        "observation_only": True,
        "no_adjudication": True,
        "no_projection_diagnostics": True,
        "no_ball_player_court_projection": True,
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
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        "observation_only": True,
        "no_adjudication": True,
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
        "warnings": dict(HOMOGRAPHY_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result


def _fit_axis(pairs: list[tuple[float, float]], *, axis_name: str) -> dict[str, float]:
    count = len(pairs)
    source_sum = sum(source for source, _ in pairs)
    target_sum = sum(target for _, target in pairs)
    source_square_sum = sum(source * source for source, _ in pairs)
    source_target_sum = sum(source * target for source, target in pairs)
    denominator = count * source_square_sum - source_sum * source_sum
    if abs(denominator) < 1e-12:
        raise ValueError(f"source {axis_name} coordinates cannot define a transform")
    scale = (count * source_target_sum - source_sum * target_sum) / denominator
    offset = (target_sum - scale * source_sum) / count
    return {"scale": scale, "offset": offset}


def _inverse_affine_matrix(matrix: list[list[float]]) -> list[list[float]]:
    scale_x = matrix[0][0]
    scale_y = matrix[1][1]
    offset_x = matrix[0][2]
    offset_y = matrix[1][2]
    if abs(scale_x) < 1e-12 or abs(scale_y) < 1e-12:
        raise ValueError("candidate homography matrix is not invertible")
    return [
        [_round(1.0 / scale_x), 0.0, _round(-offset_x / scale_x)],
        [0.0, _round(1.0 / scale_y), _round(-offset_y / scale_y)],
        [0.0, 0.0, 1.0],
    ]


def _apply_matrix(matrix: list[list[float]], x: float, y: float) -> tuple[float, float]:
    projected_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
    projected_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
    scale = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2]
    if abs(scale) < 1e-12:
        raise ValueError("candidate homography projection scale is zero")
    return projected_x / scale, projected_y / scale


def _point_error(projected: tuple[float, float], target: tuple[float, float]) -> float:
    return sqrt(((projected[0] - target[0]) ** 2) + ((projected[1] - target[1]) ** 2))


def _round(value: float) -> float:
    return round(float(value), 9)
