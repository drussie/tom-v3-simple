from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.camera_geometry import (
    CAMERA_GEOMETRY_TYPE,
    CAMERA_GEOMETRY_VERSION,
    CameraGeometryEvidenceCreate,
    CameraGeometrySchemaError,
    CameraGeometryStatus,
    CameraModel,
    CourtModel,
)
from tom_v3_storage.db_models import (
    CameraGeometryEvidence,
    HomographyCandidateObservation,
    MediaAsset,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)

CAMERA_GEOMETRY_RUNTIME_CONFIG_NAME = "camera-geometry-evidence-declaration"
CAMERA_GEOMETRY_RUNTIME_CONFIG_VERSION = "v0"
CAMERA_GEOMETRY_RUN_NAME = "camera-geometry-readiness-v0"
CAMERA_GEOMETRY_WARNINGS = {
    "geometry_evidence_only": True,
    "not_3d_truth": True,
    "not_camera_calibration_truth": True,
    "does_not_change_event_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}


def declare_camera_geometry(
    *,
    session: Session,
    media_id: str,
    court_run_id: str | None = None,
    court_projection_run_id: str | None = None,
    homography_run_id: str | None = None,
    court_model: str = CourtModel.itf_standard_tennis_court.value,
    camera_model: str = CameraModel.homography_backed_court_plane.value,
    geometry_status: str = CameraGeometryStatus.declared.value,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_format: str = "json",
    output_path: str | None = None,
) -> dict[str, Any]:
    """Persist declared camera/court geometry evidence without creating 3D truth."""

    if output_format not in {"json", "markdown"}:
        return _failed("unsupported_format", f"unsupported camera geometry format: {output_format}")

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media not found: {media_id}")

    try:
        declaration = CameraGeometryEvidenceCreate(
            media_id=media.id,
            court_run_id=court_run_id,
            court_projection_run_id=court_projection_run_id,
            homography_run_id=homography_run_id,
            court_model=court_model,
            camera_model=camera_model,
            geometry_status=geometry_status,
            image_size_jsonb={
                "width": media.width,
                "height": media.height,
                "source": "media_asset",
            },
            camera_intrinsics_jsonb={
                "status": "unknown",
                "known": False,
            },
            camera_extrinsics_jsonb={
                "status": "unknown",
                "known": False,
            },
            distortion_jsonb={
                "status": "unknown",
                "known": False,
            },
            assumptions_jsonb={
                "camera_geometry_evidence": "declared_metadata_only",
                "homography_linkage": "optional_source_context",
                "future_3d_readiness": True,
                "does_not_create_3d_trajectory": True,
            },
        )
    except (CameraGeometrySchemaError, ValidationError) as exc:
        return _failed("invalid_camera_geometry_declaration", str(exc))

    source_runs = _resolve_and_validate_source_runs(
        session=session,
        media=media,
        court_run_id=declaration.court_run_id,
        court_projection_run_id=declaration.court_projection_run_id,
        homography_run_id=declaration.homography_run_id,
    )
    if source_runs.get("ok") is False:
        return source_runs

    if declaration.homography_run_id is None:
        derived_homography_run_id = _derive_homography_run_id(
            session=session,
            court_projection_run_id=declaration.court_projection_run_id,
        )
        if derived_homography_run_id is not None:
            declaration.homography_run_id = derived_homography_run_id
            source_runs = _resolve_and_validate_source_runs(
                session=session,
                media=media,
                court_run_id=declaration.court_run_id,
                court_projection_run_id=declaration.court_projection_run_id,
                homography_run_id=declaration.homography_run_id,
            )
            if source_runs.get("ok") is False:
                return source_runs

    if declaration.court_run_id is None:
        declaration.court_run_id = _derive_court_run_id(
            session=session,
            homography_run_id=declaration.homography_run_id,
        )

    declaration.homography_matrix_jsonb = _latest_homography_matrix(
        session=session,
        media_id=media.id,
        homography_run_id=declaration.homography_run_id,
    )

    now = datetime.now(UTC)
    runtime_config = RuntimeConfig(
        config_name=CAMERA_GEOMETRY_RUNTIME_CONFIG_NAME,
        config_version=CAMERA_GEOMETRY_RUNTIME_CONFIG_VERSION,
        payload_jsonb={
            "geometry_type": CAMERA_GEOMETRY_TYPE,
            "geometry_version": CAMERA_GEOMETRY_VERSION,
            "media_id": media.id,
            "court_run_id": declaration.court_run_id,
            "court_projection_run_id": declaration.court_projection_run_id,
            "homography_run_id": declaration.homography_run_id,
            "camera_model": declaration.camera_model,
            "geometry_status": declaration.geometry_status,
            "court_model": declaration.court_model,
            "warnings": dict(CAMERA_GEOMETRY_WARNINGS),
        },
    )
    session.add(runtime_config)
    session.flush()

    run = ProcessingRun(
        media_id=media.id,
        run_name=CAMERA_GEOMETRY_RUN_NAME,
        run_status="completed",
        started_at=now,
        completed_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "geometry_type": CAMERA_GEOMETRY_TYPE,
            "geometry_version": CAMERA_GEOMETRY_VERSION,
            "court_run_id": declaration.court_run_id,
            "court_projection_run_id": declaration.court_projection_run_id,
            "homography_run_id": declaration.homography_run_id,
            "camera_model": declaration.camera_model,
            "geometry_status": declaration.geometry_status,
            "court_model": declaration.court_model,
            "capabilities": _capabilities(declaration),
            "warnings": dict(CAMERA_GEOMETRY_WARNINGS),
        },
    )
    session.add(run)
    session.flush()
    step = ProcessingStep(
        run_id=run.id,
        step_name="declare_camera_geometry",
        step_status="completed",
        started_at=now,
        completed_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "camera_geometry_declaration_only": True,
            "no_3d_reconstruction": True,
            "no_event_candidate_changes": True,
            "warnings": dict(CAMERA_GEOMETRY_WARNINGS),
        },
    )
    session.add(step)
    session.flush()

    declaration.geometry_run_id = run.id
    row = CameraGeometryEvidence(**declaration.model_dump())
    session.add(row)
    session.commit()
    session.refresh(row)

    result = camera_geometry_evidence_payload(
        row,
        replay_url=_replay_url(
            viewer_base_url=viewer_base_url,
            media_id=media.id,
            court_run_id=row.court_run_id,
            court_projection_run_id=row.court_projection_run_id,
            homography_run_id=row.homography_run_id,
        ),
    )

    if output_format == "markdown":
        result["markdown"] = render_camera_geometry_markdown(result)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(result["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["output_path"] = str(path)

    return result


def latest_camera_geometry_evidence(
    *,
    session: Session,
    media_id: str,
    court_projection_run_id: str | None = None,
    homography_run_id: str | None = None,
) -> CameraGeometryEvidence | None:
    query = select(CameraGeometryEvidence).where(CameraGeometryEvidence.media_id == media_id)
    if court_projection_run_id is not None:
        query = query.where(
            CameraGeometryEvidence.court_projection_run_id == court_projection_run_id
        )
    if homography_run_id is not None:
        query = query.where(CameraGeometryEvidence.homography_run_id == homography_run_id)
    query = query.order_by(
        CameraGeometryEvidence.created_at.desc(),
        CameraGeometryEvidence.id.desc(),
    )
    return session.scalars(query).first()


def camera_geometry_summary(
    *,
    session: Session,
    media_id: str,
    court_projection_run_id: str | None = None,
    homography_run_id: str | None = None,
) -> dict[str, Any]:
    row = latest_camera_geometry_evidence(
        session=session,
        media_id=media_id,
        court_projection_run_id=court_projection_run_id,
        homography_run_id=homography_run_id,
    )
    if row is None:
        return {"available": False}
    return {
        "available": True,
        "camera_geometry_id": row.id,
        "media_id": row.media_id,
        "court_run_id": row.court_run_id,
        "court_projection_run_id": row.court_projection_run_id,
        "homography_run_id": row.homography_run_id,
        "geometry_run_id": row.geometry_run_id,
        "camera_model": row.camera_model,
        "geometry_status": row.geometry_status,
        "court_model": row.court_model,
        "court_plane_geometry_declared": row.geometry_status
        in {
            CameraGeometryStatus.declared.value,
            CameraGeometryStatus.partial.value,
            CameraGeometryStatus.estimated.value,
        },
        "camera_intrinsics_known": bool(
            (row.camera_intrinsics_jsonb or {}).get("known") is True
        ),
        "camera_extrinsics_known": bool(
            (row.camera_extrinsics_jsonb or {}).get("known") is True
        ),
        "true_3d_reconstruction_available": bool(
            (row.metadata_jsonb or {}).get("true_3d_reconstruction_available") is True
        ),
        "3d_ball_trajectory_available": bool(
            (row.metadata_jsonb or {}).get("3d_ball_trajectory_available") is True
        ),
        "geometry_evidence_only": True,
        "no_adjudication": True,
    }


def geometry_readiness_summary(
    *,
    session: Session,
    media_id: str,
    court_projection_run_id: str | None = None,
    homography_run_id: str | None = None,
) -> dict[str, Any]:
    summary = camera_geometry_summary(
        session=session,
        media_id=media_id,
        court_projection_run_id=court_projection_run_id,
        homography_run_id=homography_run_id,
    )
    return {
        "camera_geometry_available": bool(summary.get("available") is True),
        "camera_geometry_id": summary.get("camera_geometry_id"),
        "court_plane_geometry_declared": bool(
            summary.get("court_plane_geometry_declared") is True
        ),
        "camera_intrinsics_known": bool(summary.get("camera_intrinsics_known") is True),
        "camera_extrinsics_known": bool(summary.get("camera_extrinsics_known") is True),
        "true_3d_reconstruction_available": False,
        "3d_ball_trajectory_available": False,
        "geometry_evidence_only": True,
        "no_adjudication": True,
    }


def camera_geometry_evidence_payload(
    row: CameraGeometryEvidence,
    *,
    replay_url: str | None = None,
) -> dict[str, Any]:
    payload = {
        "ok": True,
        "status": "completed",
        "geometry_type": CAMERA_GEOMETRY_TYPE,
        "geometry_version": CAMERA_GEOMETRY_VERSION,
        "camera_geometry_id": row.id,
        "geometry_run_id": row.geometry_run_id,
        "media_id": row.media_id,
        "court_run_id": row.court_run_id,
        "court_projection_run_id": row.court_projection_run_id,
        "homography_run_id": row.homography_run_id,
        "camera_model": row.camera_model,
        "geometry_status": row.geometry_status,
        "court_model": row.court_model,
        "court_dimensions": {
            "units": row.court_units,
            "court_length": row.court_length,
            "court_width": row.court_width,
            "singles_width": row.singles_sideline_width,
            "doubles_width": row.doubles_sideline_width,
            "net_height_center": row.net_height_center,
            "net_height_posts": row.net_height_posts,
        },
        "world_coordinate_system": row.world_coordinate_system_jsonb,
        "capabilities": _capabilities(row),
        "warnings": dict(row.warnings_jsonb or CAMERA_GEOMETRY_WARNINGS),
    }
    if replay_url is not None:
        payload["replay_url"] = replay_url
    return payload


def render_camera_geometry_markdown(result: dict[str, Any]) -> str:
    dimensions = result.get("court_dimensions")
    if not isinstance(dimensions, dict):
        dimensions = {}
    capabilities = result.get("capabilities")
    if not isinstance(capabilities, dict):
        capabilities = {}
    rows = [
        "# Camera Geometry Evidence v0",
        "",
        f"Media ID: `{result.get('media_id')}`  ",
        f"Camera Geometry ID: `{result.get('camera_geometry_id')}`  ",
        f"Geometry status: `{result.get('geometry_status')}`  ",
        f"Camera model: `{result.get('camera_model')}`  ",
        f"Court model: `{result.get('court_model')}`",
        "",
        "## Declared Court Dimensions",
        "",
        f"- units: {dimensions.get('units', 'n/a')}",
        f"- court_length: {dimensions.get('court_length', 'n/a')}",
        f"- singles_width: {dimensions.get('singles_width', 'n/a')}",
        f"- doubles_width: {dimensions.get('doubles_width', 'n/a')}",
        f"- net_height_center: {dimensions.get('net_height_center', 'n/a')}",
        f"- net_height_posts: {dimensions.get('net_height_posts', 'n/a')}",
        "",
        "## 3D Readiness",
        "",
        f"- court_plane_geometry_declared: {capabilities.get('court_plane_geometry_declared')}",
        f"- camera_intrinsics_known: {capabilities.get('camera_intrinsics_known')}",
        f"- camera_extrinsics_known: {capabilities.get('camera_extrinsics_known')}",
        (
            "- true_3d_reconstruction_available: "
            f"{capabilities.get('true_3d_reconstruction_available')}"
        ),
        (
            "- 3d_ball_trajectory_available: "
            f"{capabilities.get('3d_ball_trajectory_available')}"
        ),
        "",
        "## Boundary",
        "",
        "This is declared camera/court geometry evidence only. It is not 3D truth, not in/out, "
        "not score, and not adjudication.",
    ]
    return "\n".join(rows) + "\n"


def _resolve_and_validate_source_runs(
    *,
    session: Session,
    media: MediaAsset,
    court_run_id: str | None,
    court_projection_run_id: str | None,
    homography_run_id: str | None,
) -> dict[str, Any]:
    for label, run_id in (
        ("court_run_id", court_run_id),
        ("court_projection_run_id", court_projection_run_id),
        ("homography_run_id", homography_run_id),
    ):
        if run_id is None:
            continue
        run = session.get(ProcessingRun, run_id)
        if run is None:
            return _failed(f"missing_{label}", f"source run not found: {run_id}")
        if run.media_id != media.id:
            return _failed(f"{label}_media_mismatch", f"{label} does not match media_id")
    return {"ok": True}


def _derive_homography_run_id(
    *,
    session: Session,
    court_projection_run_id: str | None,
) -> str | None:
    if court_projection_run_id is None:
        return None
    run = session.get(ProcessingRun, court_projection_run_id)
    if run is None:
        return None
    payload = _run_payload(session=session, run=run)
    return _string_or_none(payload.get("source_homography_run_id"))


def _derive_court_run_id(
    *,
    session: Session,
    homography_run_id: str | None,
) -> str | None:
    if homography_run_id is None:
        return None
    run = session.get(ProcessingRun, homography_run_id)
    if run is None:
        return None
    payload = _run_payload(session=session, run=run)
    return _string_or_none(payload.get("source_court_run_id"))


def _latest_homography_matrix(
    *,
    session: Session,
    media_id: str,
    homography_run_id: str | None,
) -> list[list[float]] | None:
    if homography_run_id is None:
        return None
    row = session.scalars(
        select(HomographyCandidateObservation)
        .where(
            HomographyCandidateObservation.media_id == media_id,
            HomographyCandidateObservation.run_id == homography_run_id,
        )
        .order_by(
            HomographyCandidateObservation.timestamp_ms.desc(),
            HomographyCandidateObservation.observation_id.desc(),
        )
    ).first()
    if row is None:
        return None
    return row.homography_matrix_jsonb


def _run_payload(*, session: Session, run: ProcessingRun) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if isinstance(run.metadata_jsonb, dict):
        payload.update(run.metadata_jsonb)
    if run.runtime_config_id is not None:
        runtime_config = session.get(RuntimeConfig, run.runtime_config_id)
        if runtime_config is not None and isinstance(runtime_config.payload_jsonb, dict):
            payload.update(runtime_config.payload_jsonb)
    return payload


def _capabilities(
    geometry: CameraGeometryEvidence | CameraGeometryEvidenceCreate,
) -> dict[str, bool]:
    return {
        "court_plane_geometry_declared": geometry.geometry_status
        in {
            CameraGeometryStatus.declared.value,
            CameraGeometryStatus.partial.value,
            CameraGeometryStatus.estimated.value,
        },
        "camera_intrinsics_known": bool(
            (geometry.camera_intrinsics_jsonb or {}).get("known") is True
        ),
        "camera_extrinsics_known": bool(
            (geometry.camera_extrinsics_jsonb or {}).get("known") is True
        ),
        "true_3d_reconstruction_available": False,
        "3d_ball_trajectory_available": False,
    }


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    court_run_id: str | None,
    court_projection_run_id: str | None,
    homography_run_id: str | None,
) -> str:
    params: dict[str, str] = {}
    if court_run_id is not None:
        params["courtRunId"] = court_run_id
    if court_projection_run_id is not None:
        params["courtProjectionRunId"] = court_projection_run_id
    if homography_run_id is not None:
        params["homographyRunId"] = homography_run_id
    if court_run_id is not None:
        params["courtTemporalPersistence"] = "carry_forward"
        params["courtPersistenceMaxGapMs"] = "1500"
    suffix = f"?{urlencode(params)}" if params else ""
    return f"{viewer_base_url.rstrip('/')}/replay/{media_id}{suffix}"


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "geometry_type": CAMERA_GEOMETRY_TYPE,
        "geometry_version": CAMERA_GEOMETRY_VERSION,
        "warnings": dict(CAMERA_GEOMETRY_WARNINGS),
        **extra,
    }
