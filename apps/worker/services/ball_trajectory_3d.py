from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.ball_trajectory_3d import (
    BALL_TRAJECTORY_3D_TYPE,
    BALL_TRAJECTORY_3D_VERSION,
    DEFAULT_3D_TRAJECTORY_WARNINGS,
    BallTrajectory3DCandidateCreate,
    BallTrajectory3DSchemaError,
    CourtZStatus,
    HeightModel,
    validate_height_model,
)
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    CameraGeometryEvidence,
    MediaAsset,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

BALL_TRAJECTORY_3D_RUNTIME_CONFIG_NAME = "ball-trajectory-3d-candidate-config"
BALL_TRAJECTORY_3D_RUNTIME_CONFIG_VERSION = "v0"
BALL_TRAJECTORY_3D_RUN_NAME = "3d-ball-trajectory-candidate-evidence-v0"
BALL_TRAJECTORY_2D_OBSERVATION_TYPE = "ball_trajectory_court_candidate"
BALL_COURT_PROJECTION_OBSERVATION_TYPE = "ball_court_projection_candidate"
TRAJECTORY_3D_PROJECTION_METHOD = "declared_court_plane_metric_xy_unknown_z_v0"
TRAJECTORY_3D_PLACEHOLDER_PROJECTION_METHOD = (
    "declared_court_plane_metric_xy_z_plane_placeholder_v0"
)
SUPPORTED_HEIGHT_MODELS = {
    HeightModel.none_unknown.value,
    HeightModel.court_plane_placeholder.value,
}


@dataclass(frozen=True)
class SourceTrajectoryPoint:
    source_trajectory_observation_id: str
    source_projection_observation_id: str | None
    trajectory_segment_index: int | None
    frame: int
    timestamp_ms: int
    court_x: float | None
    court_y: float | None
    image_x: float | None
    image_y: float | None
    source_confidence: float | None
    source_homography_observation_id: str | None
    homography_time_delta_ms: int | None
    homography_carried_forward: bool | None
    inside_template_bounds: bool | None


def build_3d_ball_trajectory_candidates(
    *,
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str | None = None,
    camera_geometry_id: str | None = None,
    height_model: str = HeightModel.none_unknown.value,
    run_name: str = BALL_TRAJECTORY_3D_RUN_NAME,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_format: str = "json",
    output_path: str | None = None,
) -> dict[str, Any]:
    """Build conservative 3D ball trajectory candidate evidence.

    v0 emits declared court-plane metric x/y candidates and keeps z unknown by default.
    It does not perform true 3D reconstruction.
    """

    if output_format not in {"json", "markdown"}:
        return _failed("unsupported_format", f"unsupported 3D trajectory format: {output_format}")

    try:
        validate_height_model(height_model)
    except BallTrajectory3DSchemaError as exc:
        return _failed("invalid_height_model", str(exc))
    if height_model not in SUPPORTED_HEIGHT_MODELS:
        return _failed(
            "unsupported_height_model",
            f"height model is declared but not implemented in v0: {height_model}",
        )

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media not found: {media_id}")

    ball_trajectory_run = session.get(ProcessingRun, ball_trajectory_run_id)
    if ball_trajectory_run is None:
        return _failed(
            "missing_ball_trajectory_run",
            f"ball trajectory run not found: {ball_trajectory_run_id}",
        )
    if ball_trajectory_run.media_id != media.id:
        return _failed(
            "ball_trajectory_run_media_mismatch",
            "ball_trajectory_run_id does not match media_id",
        )

    resolved_court_projection_run_id = court_projection_run_id or _source_court_projection_run_id(
        ball_trajectory_run
    )
    if resolved_court_projection_run_id is not None:
        court_projection_run = session.get(ProcessingRun, resolved_court_projection_run_id)
        if court_projection_run is None:
            return _failed(
                "missing_court_projection_run",
                f"court projection run not found: {resolved_court_projection_run_id}",
            )
        if court_projection_run.media_id != media.id:
            return _failed(
                "court_projection_run_media_mismatch",
                "court_projection_run_id does not match media_id",
            )

    camera_geometry = _resolve_camera_geometry(
        session=session,
        media_id=media.id,
        camera_geometry_id=camera_geometry_id,
        court_projection_run_id=resolved_court_projection_run_id,
    )
    if isinstance(camera_geometry, dict):
        return camera_geometry

    source_points = load_source_trajectory_points(
        session=session,
        media=media,
        ball_trajectory_run_id=ball_trajectory_run.id,
    )

    now = datetime.now(UTC)
    runtime_config = RuntimeConfig(
        config_name=BALL_TRAJECTORY_3D_RUNTIME_CONFIG_NAME,
        config_version=BALL_TRAJECTORY_3D_RUNTIME_CONFIG_VERSION,
        payload_jsonb={
            "trajectory_3d_type": BALL_TRAJECTORY_3D_TYPE,
            "trajectory_3d_version": BALL_TRAJECTORY_3D_VERSION,
            "source_ball_trajectory_run_id": ball_trajectory_run.id,
            "source_court_projection_run_id": resolved_court_projection_run_id,
            "camera_geometry_id": camera_geometry.id,
            "geometry_run_id": camera_geometry.geometry_run_id,
            "height_model": height_model,
            "metric_conversion_status": "declared_assumption",
            "does_not_change_event_candidates": True,
            **DEFAULT_3D_TRAJECTORY_WARNINGS,
        },
    )
    session.add(runtime_config)
    session.flush()

    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "trajectory_3d_type": BALL_TRAJECTORY_3D_TYPE,
            "trajectory_3d_version": BALL_TRAJECTORY_3D_VERSION,
            "source_ball_trajectory_run_id": ball_trajectory_run.id,
            "source_court_projection_run_id": resolved_court_projection_run_id,
            "camera_geometry_id": camera_geometry.id,
            "geometry_run_id": camera_geometry.geometry_run_id,
            "height_model": height_model,
            **DEFAULT_3D_TRAJECTORY_WARNINGS,
        },
    )
    session.add(run)
    session.flush()

    step = ProcessingStep(
        run_id=run.id,
        step_name="build_3d_ball_trajectory_candidates",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "source_point_count": len(source_points),
            "height_model": height_model,
            "does_not_change_event_candidates": True,
            **DEFAULT_3D_TRAJECTORY_WARNINGS,
        },
    )
    session.add(step)
    session.flush()

    candidates = _build_candidate_rows(
        media=media,
        run=run,
        camera_geometry=camera_geometry,
        ball_trajectory_run_id=ball_trajectory_run.id,
        court_projection_run_id=resolved_court_projection_run_id,
        source_points=source_points,
        height_model=height_model,
    )
    for candidate in candidates:
        session.add(candidate)

    summary = _candidate_summary(
        source_point_count=len(source_points),
        candidates=candidates,
        height_model=height_model,
    )
    completed_at = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = completed_at
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        "candidate_summary": summary,
        "capabilities": _capabilities(summary),
    }
    step.step_status = "completed"
    step.completed_at = completed_at
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "candidate_summary": summary,
        "capabilities": _capabilities(summary),
    }
    session.commit()

    result = _result_payload(
        media_id=media.id,
        trajectory_3d_run_id=run.id,
        ball_trajectory_run_id=ball_trajectory_run.id,
        court_projection_run_id=resolved_court_projection_run_id,
        camera_geometry_id=camera_geometry.id,
        summary=summary,
        replay_url=_replay_url(
            viewer_base_url=viewer_base_url,
            media_id=media.id,
            court_projection_run_id=resolved_court_projection_run_id,
            ball_trajectory_run_id=ball_trajectory_run.id,
            trajectory_3d_run_id=run.id,
        ),
    )

    if output_format == "markdown":
        result["markdown"] = render_ball_trajectory_3d_markdown(result)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(result["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["output_path"] = str(path)

    return result


def load_source_trajectory_points(
    *,
    session: Session,
    media: MediaAsset,
    ball_trajectory_run_id: str,
) -> list[SourceTrajectoryPoint]:
    rows = list(
        session.scalars(
            select(Observation)
            .where(
                Observation.media_id == media.id,
                Observation.run_id == ball_trajectory_run_id,
                Observation.observation_type == BALL_TRAJECTORY_2D_OBSERVATION_TYPE,
            )
            .order_by(
                Observation.timestamp_start_ms,
                Observation.frame_start,
                Observation.id,
            )
        ).all()
    )

    projection_cache: dict[str, Observation | None] = {}
    points: list[SourceTrajectoryPoint] = []
    for row in rows:
        payload = row.payload_jsonb or {}
        raw_points = payload.get("points")
        if not isinstance(raw_points, list):
            continue
        segment_index = _optional_int(payload.get("trajectory_segment_index"))
        for raw_point in raw_points:
            if not isinstance(raw_point, dict):
                continue
            point = _source_point_from_payload(
                session=session,
                raw_point=raw_point,
                source_trajectory=row,
                segment_index=segment_index,
                projection_cache=projection_cache,
            )
            if point is not None:
                points.append(point)

    points.sort(
        key=lambda item: (
            item.timestamp_ms,
            item.frame,
            item.source_trajectory_observation_id,
            item.source_projection_observation_id or "",
        )
    )
    return points


def latest_ball_trajectory_3d_summary(
    *,
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str | None = None,
    court_projection_run_id: str | None = None,
) -> dict[str, Any]:
    query = select(BallTrajectory3DCandidate).where(
        BallTrajectory3DCandidate.media_id == media_id
    )
    if ball_trajectory_run_id is not None:
        query = query.where(
            BallTrajectory3DCandidate.ball_trajectory_run_id == ball_trajectory_run_id
        )
    if court_projection_run_id is not None:
        query = query.where(
            BallTrajectory3DCandidate.court_projection_run_id == court_projection_run_id
        )
    row = session.scalars(
        query.order_by(
            BallTrajectory3DCandidate.created_at.desc(),
            BallTrajectory3DCandidate.id.desc(),
        )
    ).first()
    if row is None or row.trajectory_3d_run_id is None:
        return {"available": False}
    return ball_trajectory_3d_summary(
        session=session,
        media_id=media_id,
        trajectory_3d_run_id=row.trajectory_3d_run_id,
    )


def ball_trajectory_3d_summary(
    *,
    session: Session,
    media_id: str,
    trajectory_3d_run_id: str,
) -> dict[str, Any]:
    rows = list(
        session.scalars(
            select(BallTrajectory3DCandidate).where(
                BallTrajectory3DCandidate.media_id == media_id,
                BallTrajectory3DCandidate.trajectory_3d_run_id == trajectory_3d_run_id,
            )
        ).all()
    )
    if not rows:
        return {"available": False}
    source = rows[0]
    height_model = source.height_model
    known_height_count = sum(1 for row in rows if row.court_z_m is not None)
    unknown_height_count = sum(
        1 for row in rows if row.court_z_status == CourtZStatus.unknown.value
    )
    metric_count = sum(1 for row in rows if row.court_x_m is not None and row.court_y_m is not None)
    return {
        "available": True,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "media_id": media_id,
        "ball_trajectory_run_id": source.ball_trajectory_run_id,
        "court_projection_run_id": source.court_projection_run_id,
        "camera_geometry_id": source.camera_geometry_id,
        "candidate_count": len(rows),
        "height_model": height_model,
        "known_height_count": known_height_count,
        "unknown_height_count": unknown_height_count,
        "court_plane_xy_metric_count": metric_count,
        "height_candidate_available": known_height_count > 0,
        "true_3d_reconstruction_available": False,
        "3d_ball_trajectory_truth_available": False,
        "geometry_evidence_only": True,
        "no_adjudication": True,
    }


def trajectory_3d_readiness_summary(summary: dict[str, Any]) -> dict[str, Any]:
    if summary.get("available") is not True:
        return {
            "trajectory_3d_candidates_available": False,
            "height_candidate_available": False,
            "true_3d_reconstruction_available": False,
            "3d_ball_trajectory_truth_available": False,
            "geometry_evidence_only": True,
            "no_adjudication": True,
        }
    return {
        "trajectory_3d_candidates_available": True,
        "trajectory_3d_run_id": summary.get("trajectory_3d_run_id"),
        "candidate_count": summary.get("candidate_count", 0),
        "height_model": summary.get("height_model"),
        "height_candidate_available": bool(summary.get("height_candidate_available") is True),
        "true_3d_reconstruction_available": False,
        "3d_ball_trajectory_truth_available": False,
        "geometry_evidence_only": True,
        "no_adjudication": True,
    }


def render_ball_trajectory_3d_markdown(result: dict[str, Any]) -> str:
    summary = result.get("candidate_summary")
    if not isinstance(summary, dict):
        summary = {}
    capabilities = result.get("capabilities")
    if not isinstance(capabilities, dict):
        capabilities = {}
    rows = [
        "# 3D Ball Trajectory Candidate Evidence v0",
        "",
        f"Media ID: `{result.get('media_id')}`  ",
        f"3D Trajectory Run ID: `{result.get('trajectory_3d_run_id')}`  ",
        f"Ball Trajectory Run ID: `{result.get('ball_trajectory_run_id')}`  ",
        f"Court Projection Run ID: `{result.get('court_projection_run_id')}`  ",
        f"Camera Geometry ID: `{result.get('camera_geometry_id')}`",
        "",
        "## Candidate Summary",
        "",
        f"- source_trajectory_points: {summary.get('source_trajectory_points', 0)}",
        f"- trajectory_3d_candidate_count: {summary.get('trajectory_3d_candidate_count', 0)}",
        f"- height_model: {summary.get('height_model', 'n/a')}",
        f"- known_height_count: {summary.get('known_height_count', 0)}",
        f"- unknown_height_count: {summary.get('unknown_height_count', 0)}",
        f"- court_plane_xy_metric_count: {summary.get('court_plane_xy_metric_count', 0)}",
        "",
        "## Capabilities",
        "",
        (
            "- court_plane_xy_metric_available: "
            f"{capabilities.get('court_plane_xy_metric_available', False)}"
        ),
        (
            "- height_candidate_available: "
            f"{capabilities.get('height_candidate_available', False)}"
        ),
        (
            "- true_3d_reconstruction_available: "
            f"{capabilities.get('true_3d_reconstruction_available', False)}"
        ),
        (
            "- 3d_ball_trajectory_truth_available: "
            f"{capabilities.get('3d_ball_trajectory_truth_available', False)}"
        ),
        "",
        "## Boundary",
        "",
        "This is provisional 3D candidate evidence only. It is not true 3D reconstruction, "
        "not hit/bounce truth, not in/out, not score, and not adjudication.",
    ]
    return "\n".join(rows) + "\n"


def _build_candidate_rows(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    camera_geometry: CameraGeometryEvidence,
    ball_trajectory_run_id: str,
    court_projection_run_id: str | None,
    source_points: list[SourceTrajectoryPoint],
    height_model: str,
) -> list[BallTrajectory3DCandidate]:
    rows: list[BallTrajectory3DCandidate] = []
    previous_by_segment: dict[tuple[str, int | None], BallTrajectory3DCandidate] = {}
    for point in source_points:
        create = _candidate_create(
            media=media,
            run=run,
            camera_geometry=camera_geometry,
            ball_trajectory_run_id=ball_trajectory_run_id,
            court_projection_run_id=court_projection_run_id,
            point=point,
            height_model=height_model,
        )
        previous = previous_by_segment.get(
            (point.source_trajectory_observation_id, point.trajectory_segment_index)
        )
        if previous is not None:
            _populate_velocity(create, previous=previous, current_point=point)
        row = BallTrajectory3DCandidate(**create.model_dump())
        rows.append(row)
        previous_by_segment[
            (point.source_trajectory_observation_id, point.trajectory_segment_index)
        ] = row
    return rows


def _candidate_create(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    camera_geometry: CameraGeometryEvidence,
    ball_trajectory_run_id: str,
    court_projection_run_id: str | None,
    point: SourceTrajectoryPoint,
    height_model: str,
) -> BallTrajectory3DCandidateCreate:
    court_x_m = _metric_x(point.court_x, camera_geometry)
    court_y_m = _metric_y(point.court_y, camera_geometry)
    court_z_m: float | None = None
    court_z_status = CourtZStatus.unknown.value
    projection_method = TRAJECTORY_3D_PROJECTION_METHOD
    if height_model == HeightModel.court_plane_placeholder.value:
        court_z_m = 0.0
        court_z_status = CourtZStatus.court_plane_assumed.value
        projection_method = TRAJECTORY_3D_PLACEHOLDER_PROJECTION_METHOD

    return BallTrajectory3DCandidateCreate(
        media_id=media.id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        court_projection_run_id=court_projection_run_id,
        camera_geometry_id=camera_geometry.id,
        geometry_run_id=camera_geometry.geometry_run_id,
        trajectory_3d_run_id=run.id,
        source_observation_id=point.source_projection_observation_id
        or point.source_trajectory_observation_id,
        frame=point.frame,
        timestamp_ms=point.timestamp_ms,
        image_x=point.image_x,
        image_y=point.image_y,
        court_x=point.court_x,
        court_y=point.court_y,
        court_x_m=court_x_m,
        court_y_m=court_y_m,
        court_z_m=court_z_m,
        court_z_status=court_z_status,
        height_model=height_model,
        projection_method=projection_method,
        confidence=point.source_confidence,
        diagnostics_jsonb={
            "source_trajectory_observation_id": point.source_trajectory_observation_id,
            "source_projection_observation_id": point.source_projection_observation_id,
            "trajectory_segment_index": point.trajectory_segment_index,
            "metric_conversion_status": (
                "declared_assumption"
                if court_x_m is not None and court_y_m is not None
                else "insufficient_declared_court_dimensions"
            ),
            "court_width_m": camera_geometry.court_width,
            "court_length_m": camera_geometry.court_length,
            "height_status_reason": (
                "height_unknown_in_v0"
                if height_model == HeightModel.none_unknown.value
                else "court_plane_placeholder_not_ball_height"
            ),
            "source_homography_observation_id": point.source_homography_observation_id,
            "homography_time_delta_ms": point.homography_time_delta_ms,
            "homography_carried_forward": point.homography_carried_forward,
            "inside_template_bounds": point.inside_template_bounds,
        },
        metadata_jsonb={
            "projection_source": "ball_trajectory_court_candidate",
            "geometry_source": "camera_geometry_evidence",
            "coordinate_space": "court_metric_3d_readiness_v0",
            "source_ball_trajectory_run_id": ball_trajectory_run_id,
            "source_court_projection_run_id": court_projection_run_id,
            "camera_geometry_id": camera_geometry.id,
            "height_model": height_model,
        },
    )


def _populate_velocity(
    create: BallTrajectory3DCandidateCreate,
    *,
    previous: BallTrajectory3DCandidate,
    current_point: SourceTrajectoryPoint,
) -> None:
    if previous.timestamp_ms is None:
        return
    dt_seconds = (current_point.timestamp_ms - previous.timestamp_ms) / 1000.0
    if dt_seconds <= 0:
        return
    if previous.court_x_m is None or previous.court_y_m is None:
        return
    if create.court_x_m is None or create.court_y_m is None:
        return
    create.velocity_x_mps = _round((create.court_x_m - previous.court_x_m) / dt_seconds)
    create.velocity_y_mps = _round((create.court_y_m - previous.court_y_m) / dt_seconds)
    if create.court_z_m is not None and previous.court_z_m is not None:
        create.velocity_z_mps = _round((create.court_z_m - previous.court_z_m) / dt_seconds)
    create.speed_mps = _round(
        math.sqrt(
            create.velocity_x_mps**2
            + create.velocity_y_mps**2
            + (create.velocity_z_mps or 0.0) ** 2
        )
    )
    create.diagnostics_jsonb["velocity_source"] = "adjacent_candidate_points_same_segment"
    create.diagnostics_jsonb["velocity_dt_ms"] = int(round(dt_seconds * 1000.0))


def _source_point_from_payload(
    *,
    session: Session,
    raw_point: dict[str, Any],
    source_trajectory: Observation,
    segment_index: int | None,
    projection_cache: dict[str, Observation | None],
) -> SourceTrajectoryPoint | None:
    frame = _optional_int(raw_point.get("frame_number"))
    timestamp_ms = _optional_int(raw_point.get("timestamp_ms"))
    if frame is None or timestamp_ms is None:
        return None
    source_projection_id = _string_or_none(raw_point.get("source_observation_id"))
    projection = _projection_observation(
        session=session,
        observation_id=source_projection_id,
        cache=projection_cache,
    )
    projection_payload = projection.payload_jsonb if projection is not None else {}
    image_point = projection_payload.get("image_point")
    if not isinstance(image_point, dict):
        image_point = {}
    court_x = _number(raw_point.get("court_x"))
    court_y = _number(raw_point.get("court_y"))
    return SourceTrajectoryPoint(
        source_trajectory_observation_id=source_trajectory.id,
        source_projection_observation_id=source_projection_id,
        trajectory_segment_index=segment_index,
        frame=frame,
        timestamp_ms=timestamp_ms,
        court_x=court_x,
        court_y=court_y,
        image_x=_number(image_point.get("x")),
        image_y=_number(image_point.get("y")),
        source_confidence=(
            projection.confidence if projection is not None else source_trajectory.confidence
        ),
        source_homography_observation_id=_string_or_none(
            raw_point.get("source_homography_observation_id")
        ),
        homography_time_delta_ms=_optional_int(raw_point.get("homography_time_delta_ms")),
        homography_carried_forward=(
            bool(raw_point.get("homography_carried_forward"))
            if raw_point.get("homography_carried_forward") is not None
            else None
        ),
        inside_template_bounds=(
            bool(raw_point.get("inside_template_bounds"))
            if raw_point.get("inside_template_bounds") is not None
            else None
        ),
    )


def _projection_observation(
    *,
    session: Session,
    observation_id: str | None,
    cache: dict[str, Observation | None],
) -> Observation | None:
    if observation_id is None:
        return None
    if observation_id not in cache:
        row = session.get(Observation, observation_id)
        if row is not None and row.observation_type != BALL_COURT_PROJECTION_OBSERVATION_TYPE:
            row = None
        cache[observation_id] = row
    return cache[observation_id]


def _resolve_camera_geometry(
    *,
    session: Session,
    media_id: str,
    camera_geometry_id: str | None,
    court_projection_run_id: str | None,
) -> CameraGeometryEvidence | dict[str, Any]:
    if camera_geometry_id is not None:
        row = session.get(CameraGeometryEvidence, camera_geometry_id)
        if row is None:
            return _failed(
                "missing_camera_geometry",
                f"camera geometry evidence not found: {camera_geometry_id}",
            )
        if row.media_id != media_id:
            return _failed(
                "camera_geometry_media_mismatch",
                "camera_geometry_id does not match media_id",
            )
        return row

    query = select(CameraGeometryEvidence).where(CameraGeometryEvidence.media_id == media_id)
    if court_projection_run_id is not None:
        query = query.where(
            CameraGeometryEvidence.court_projection_run_id == court_projection_run_id
        )
    row = session.scalars(
        query.order_by(CameraGeometryEvidence.created_at.desc(), CameraGeometryEvidence.id.desc())
    ).first()
    if row is None:
        return _failed(
            "missing_camera_geometry",
            "camera geometry evidence is required before building 3D trajectory candidates",
        )
    return row


def _source_court_projection_run_id(run: ProcessingRun) -> str | None:
    payload = run.metadata_jsonb if isinstance(run.metadata_jsonb, dict) else {}
    value = payload.get("source_court_projection_run_id")
    return _string_or_none(value)


def _metric_x(court_x: float | None, camera_geometry: CameraGeometryEvidence) -> float | None:
    if court_x is None or camera_geometry.court_width is None:
        return None
    return _round(court_x * camera_geometry.court_width)


def _metric_y(court_y: float | None, camera_geometry: CameraGeometryEvidence) -> float | None:
    if court_y is None or camera_geometry.court_length is None:
        return None
    return _round(court_y * camera_geometry.court_length)


def _candidate_summary(
    *,
    source_point_count: int,
    candidates: list[BallTrajectory3DCandidate],
    height_model: str,
) -> dict[str, Any]:
    known_height_count = sum(1 for row in candidates if row.court_z_m is not None)
    unknown_height_count = sum(
        1 for row in candidates if row.court_z_status == CourtZStatus.unknown.value
    )
    metric_count = sum(
        1 for row in candidates if row.court_x_m is not None and row.court_y_m is not None
    )
    return {
        "source_trajectory_points": source_point_count,
        "trajectory_3d_candidate_count": len(candidates),
        "height_model": height_model,
        "known_height_count": known_height_count,
        "unknown_height_count": unknown_height_count,
        "court_plane_xy_metric_count": metric_count,
        "velocity_candidate_count": sum(1 for row in candidates if row.speed_mps is not None),
        "metric_conversion_status": "declared_assumption",
    }


def _capabilities(summary: dict[str, Any]) -> dict[str, bool]:
    return {
        "court_plane_xy_metric_available": summary.get("court_plane_xy_metric_count", 0) > 0,
        "height_candidate_available": summary.get("known_height_count", 0) > 0,
        "true_3d_reconstruction_available": False,
        "3d_ball_trajectory_truth_available": False,
    }


def _result_payload(
    *,
    media_id: str,
    trajectory_3d_run_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str | None,
    camera_geometry_id: str,
    summary: dict[str, Any],
    replay_url: str,
) -> dict[str, Any]:
    return {
        "ok": True,
        "status": "completed",
        "trajectory_3d_type": BALL_TRAJECTORY_3D_TYPE,
        "trajectory_3d_version": BALL_TRAJECTORY_3D_VERSION,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "media_id": media_id,
        "ball_trajectory_run_id": ball_trajectory_run_id,
        "court_projection_run_id": court_projection_run_id,
        "camera_geometry_id": camera_geometry_id,
        "candidate_summary": summary,
        "capabilities": _capabilities(summary),
        "replay_url": replay_url,
        "warnings": dict(DEFAULT_3D_TRAJECTORY_WARNINGS),
    }


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    court_projection_run_id: str | None,
    ball_trajectory_run_id: str,
    trajectory_3d_run_id: str,
) -> str:
    params = {
        "ballTrajectoryRunId": ball_trajectory_run_id,
        "trajectory3dRunId": trajectory_3d_run_id,
    }
    if court_projection_run_id is not None:
        params["courtProjectionRunId"] = court_projection_run_id
    return f"{viewer_base_url.rstrip('/')}/replay/{media_id}?{urlencode(params)}"


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _round(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(DEFAULT_3D_TRAJECTORY_WARNINGS),
    }
