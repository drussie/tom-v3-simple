from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from tom_v3_schema.ball_trajectory_3d import CourtZStatus
from tom_v3_schema.event_candidate_3d_diagnostic import (
    DEFAULT_EVENT_CANDIDATE_3D_DIAGNOSTIC_WARNINGS,
    EVENT_CANDIDATE_3D_DIAGNOSTIC_TYPE,
    EVENT_CANDIDATE_3D_DIAGNOSTIC_VERSION,
    EventCandidate3DDiagnosticCreate,
    EventCandidate3DDiagnosticLabel,
    EventCandidate3DDiagnosticSchemaError,
    EventCandidate3DDiagnosticStatus,
)
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    CameraGeometryEvidence,
    EventCandidate3DDiagnostic,
    MediaAsset,
    Observation,
    ProcessingRun,
)

EVENT_CANDIDATE_TYPES = {"hit_candidate", "bounce_candidate"}
DEFAULT_TIME_WINDOW_MS = 250


@dataclass(frozen=True)
class EventMarker:
    observation_id: str
    candidate_type: str
    frame: int
    timestamp_ms: int
    image_x: float | None
    image_y: float | None
    court_x: float | None
    court_y: float | None
    confidence: float | None
    candidate_method: str | None
    original_candidate_type: str | None
    arbitration_decision: str | None
    arbitration_reason: str | None


@dataclass(frozen=True)
class Local3DContext:
    nearest: BallTrajectory3DCandidate | None
    pre_count: int
    post_count: int
    local_count: int
    velocity_available: bool
    speed_mps: float | None
    direction_delta_degrees: float | None


def build_event_candidate_3d_diagnostics(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str | None = None,
    time_window_ms: int = DEFAULT_TIME_WINDOW_MS,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_format: str = "json",
    output_path: str | None = None,
) -> dict[str, Any]:
    """Build diagnostic-only 3D context rows for final hit/bounce markers."""

    if output_format not in {"json", "markdown"}:
        return _failed("unsupported_format", f"unsupported diagnostic format: {output_format}")

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media not found: {media_id}")

    event_run = session.get(ProcessingRun, event_candidate_run_id)
    if event_run is None:
        return _failed(
            "missing_event_candidate_run",
            f"event candidate run not found: {event_candidate_run_id}",
        )
    if event_run.media_id != media.id:
        return _failed(
            "event_candidate_run_media_mismatch",
            "event_candidate_run_id does not match media_id",
        )

    trajectory_run = session.get(ProcessingRun, trajectory_3d_run_id)
    if trajectory_run is None:
        return _failed(
            "missing_trajectory_3d_run",
            f"trajectory_3d_run_id not found: {trajectory_3d_run_id}",
        )
    if trajectory_run.media_id != media.id:
        return _failed(
            "trajectory_3d_run_media_mismatch",
            "trajectory_3d_run_id does not match media_id",
        )

    camera_geometry = _resolve_camera_geometry(
        session=session,
        media_id=media.id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        camera_geometry_id=camera_geometry_id,
    )
    if isinstance(camera_geometry, dict):
        return camera_geometry

    window_ms = max(0, int(time_window_ms))
    markers = _final_event_markers(
        session=session,
        media=media,
        event_candidate_run_id=event_candidate_run_id,
    )
    trajectory_rows = _trajectory_3d_rows(
        session=session,
        media_id=media.id,
        trajectory_3d_run_id=trajectory_3d_run_id,
    )

    diagnostics = [
        _diagnostic_row(
            marker=marker,
            media=media,
            event_candidate_run_id=event_candidate_run_id,
            trajectory_3d_run_id=trajectory_3d_run_id,
            camera_geometry_id=camera_geometry.id,
            context=_local_3d_context(
                marker=marker,
                trajectory_rows=trajectory_rows,
                time_window_ms=window_ms,
            ),
            time_window_ms=window_ms,
        )
        for marker in markers
    ]

    session.execute(
        delete(EventCandidate3DDiagnostic).where(
            EventCandidate3DDiagnostic.media_id == media.id,
            EventCandidate3DDiagnostic.event_candidate_run_id == event_candidate_run_id,
            EventCandidate3DDiagnostic.trajectory_3d_run_id == trajectory_3d_run_id,
        )
    )
    for row in diagnostics:
        session.add(row)
    session.commit()

    summary = event_candidate_3d_diagnostic_summary(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
    )
    summary = {
        **summary,
        "final_marker_count": len(markers),
        "time_window_ms": window_ms,
    }
    result = {
        "ok": True,
        "status": "completed",
        "diagnostic_type": EVENT_CANDIDATE_3D_DIAGNOSTIC_TYPE,
        "diagnostic_version": EVENT_CANDIDATE_3D_DIAGNOSTIC_VERSION,
        "media_id": media.id,
        "event_candidate_run_id": event_candidate_run_id,
        "trajectory_3d_run_id": trajectory_3d_run_id,
        "camera_geometry_id": camera_geometry.id,
        "diagnostic_summary": summary,
        "replay_url": _replay_url(
            viewer_base_url=viewer_base_url,
            media_id=media.id,
            event_candidate_run_id=event_candidate_run_id,
            trajectory_3d_run_id=trajectory_3d_run_id,
        ),
        "warnings": dict(DEFAULT_EVENT_CANDIDATE_3D_DIAGNOSTIC_WARNINGS),
    }

    if output_format == "markdown":
        result["markdown"] = render_event_candidate_3d_diagnostics_markdown(result)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(result["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["output_path"] = str(path)

    return result


def event_candidate_3d_diagnostic_summary(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str | None = None,
) -> dict[str, Any]:
    query = select(EventCandidate3DDiagnostic).where(
        EventCandidate3DDiagnostic.media_id == media_id,
        EventCandidate3DDiagnostic.event_candidate_run_id == event_candidate_run_id,
    )
    if trajectory_3d_run_id is not None:
        query = query.where(
            EventCandidate3DDiagnostic.trajectory_3d_run_id == trajectory_3d_run_id
        )
    rows = list(session.scalars(query).all())
    if not rows:
        return {
            "available": False,
            "diagnostic_only": True,
            "not_truth": True,
            "not_3d_truth": True,
            "no_adjudication": True,
        }
    by_type = Counter(row.candidate_type for row in rows)
    by_status = Counter(row.diagnostic_status for row in rows)
    by_label = Counter(row.diagnostic_label for row in rows)
    nearest_found = sum(1 for row in rows if row.nearest_3d_candidate_id is not None)
    return {
        "available": True,
        "event_candidate_run_id": event_candidate_run_id,
        "trajectory_3d_run_id": rows[0].trajectory_3d_run_id,
        "camera_geometry_id": rows[0].camera_geometry_id,
        "diagnostic_count": len(rows),
        "hit_candidate_diagnostic_count": by_type.get("hit_candidate", 0),
        "bounce_candidate_diagnostic_count": by_type.get("bounce_candidate", 0),
        "nearest_3d_sample_found_count": nearest_found,
        "height_unknown_count": sum(
            1 for row in rows if row.height_status in {"unknown", "height_unknown"}
        ),
        "cannot_evaluate_count": by_status.get(
            EventCandidate3DDiagnosticStatus.cannot_evaluate.value,
            0,
        ),
        "insufficient_3d_evidence_count": by_status.get(
            EventCandidate3DDiagnosticStatus.insufficient_3d_evidence.value,
            0,
        ),
        "supports_candidate_context_count": by_label.get(
            EventCandidate3DDiagnosticLabel.supports_candidate_context.value,
            0,
        ),
        "weakens_candidate_context_count": by_label.get(
            EventCandidate3DDiagnosticLabel.weakens_candidate_context.value,
            0,
        ),
        "neutral_context_count": by_label.get(
            EventCandidate3DDiagnosticLabel.neutral_context.value,
            0,
        ),
        "diagnostic_only": True,
        "not_truth": True,
        "not_3d_truth": True,
        "height_not_verified": True,
        "does_not_change_event_candidates": True,
        "does_not_create_in_out": True,
        "does_not_create_score": True,
        "no_adjudication": True,
    }


def latest_event_candidate_3d_diagnostic_summary(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
) -> dict[str, Any]:
    row = session.scalars(
        select(EventCandidate3DDiagnostic)
        .where(
            EventCandidate3DDiagnostic.media_id == media_id,
            EventCandidate3DDiagnostic.event_candidate_run_id == event_candidate_run_id,
        )
        .order_by(
            EventCandidate3DDiagnostic.created_at.desc(),
            EventCandidate3DDiagnostic.id.desc(),
        )
    ).first()
    if row is None:
        return {
            "available": False,
            "diagnostic_only": True,
            "not_truth": True,
            "not_3d_truth": True,
            "no_adjudication": True,
        }
    return event_candidate_3d_diagnostic_summary(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
        trajectory_3d_run_id=row.trajectory_3d_run_id,
    )


def event_candidate_3d_diagnostic_readiness_summary(
    summary: dict[str, Any],
) -> dict[str, Any]:
    if summary.get("available") is not True:
        return {
            "available": False,
            "diagnostic_only": True,
            "not_truth": True,
            "not_3d_truth": True,
            "height_unknown_count": 0,
            "supports_candidate_context_count": 0,
            "weakens_candidate_context_count": 0,
            "no_adjudication": True,
        }
    return {
        "available": True,
        "event_candidate_run_id": summary.get("event_candidate_run_id"),
        "trajectory_3d_run_id": summary.get("trajectory_3d_run_id"),
        "diagnostic_count": summary.get("diagnostic_count", 0),
        "height_unknown_count": summary.get("height_unknown_count", 0),
        "supports_candidate_context_count": summary.get(
            "supports_candidate_context_count",
            0,
        ),
        "weakens_candidate_context_count": summary.get(
            "weakens_candidate_context_count",
            0,
        ),
        "diagnostic_only": True,
        "not_truth": True,
        "not_3d_truth": True,
        "no_adjudication": True,
    }


def compact_event_candidate_3d_diagnostics(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
) -> list[dict[str, Any]]:
    rows = list(
        session.scalars(
            select(EventCandidate3DDiagnostic)
            .where(
                EventCandidate3DDiagnostic.media_id == media_id,
                EventCandidate3DDiagnostic.event_candidate_run_id == event_candidate_run_id,
            )
            .order_by(
                EventCandidate3DDiagnostic.timestamp_ms,
                EventCandidate3DDiagnostic.frame,
                EventCandidate3DDiagnostic.id,
            )
        ).all()
    )
    return [_compact_diagnostic(row) for row in rows]


def event_candidate_3d_diagnostics_by_event_observation_id(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
) -> dict[str, dict[str, Any]]:
    rows = compact_event_candidate_3d_diagnostics(
        session=session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
    )
    return {
        str(row["event_observation_id"]): row
        for row in rows
        if isinstance(row.get("event_observation_id"), str)
    }


def render_event_candidate_3d_diagnostics_markdown(result: dict[str, Any]) -> str:
    summary = result.get("diagnostic_summary")
    if not isinstance(summary, dict):
        summary = {}
    rows = [
        "# 3D-Assisted Event Candidate Diagnostics v0",
        "",
        f"Media ID: `{result.get('media_id')}`  ",
        f"Event Candidate Run ID: `{result.get('event_candidate_run_id')}`  ",
        f"3D Trajectory Run ID: `{result.get('trajectory_3d_run_id')}`  ",
        f"Camera Geometry ID: `{result.get('camera_geometry_id')}`",
        "",
        "## Diagnostic Summary",
        "",
        f"- final_marker_count: {summary.get('final_marker_count', 0)}",
        f"- diagnostic_count: {summary.get('diagnostic_count', 0)}",
        f"- nearest_3d_sample_found_count: {summary.get('nearest_3d_sample_found_count', 0)}",
        f"- height_unknown_count: {summary.get('height_unknown_count', 0)}",
        f"- supports_candidate_context_count: {summary.get('supports_candidate_context_count', 0)}",
        f"- weakens_candidate_context_count: {summary.get('weakens_candidate_context_count', 0)}",
        "",
        "## Boundary",
        "",
        "These diagnostics are evidence/debug metadata only. They do not change hit/bounce "
        "classification, do not create 3D truth, do not create in/out or score, and do not "
        "adjudicate the point.",
    ]
    return "\n".join(rows) + "\n"


def _final_event_markers(
    *,
    session: Session,
    media: MediaAsset,
    event_candidate_run_id: str,
) -> list[EventMarker]:
    observations = list(
        session.scalars(
            select(Observation)
            .where(
                Observation.media_id == media.id,
                Observation.run_id == event_candidate_run_id,
                Observation.observation_type.in_(sorted(EVENT_CANDIDATE_TYPES)),
                Observation.timestamp_start_ms.is_not(None),
            )
            .order_by(
                Observation.timestamp_start_ms,
                Observation.frame_start,
                Observation.observation_type,
                Observation.id,
            )
        ).all()
    )
    markers: list[EventMarker] = []
    for observation in observations:
        marker = _marker_from_observation(observation)
        if marker is not None:
            markers.append(marker)
    return markers


def _marker_from_observation(observation: Observation) -> EventMarker | None:
    payload = observation.payload_jsonb or {}
    frame = _optional_int(payload.get("frame_number") or observation.frame_start)
    timestamp_ms = _optional_int(payload.get("timestamp_ms") or observation.timestamp_start_ms)
    candidate_type = _string_or_none(payload.get("candidate_type")) or observation.observation_type
    if frame is None or timestamp_ms is None or candidate_type not in EVENT_CANDIDATE_TYPES:
        return None
    court_point = payload.get("court_point") if isinstance(payload.get("court_point"), dict) else {}
    image_point = payload.get("image_point") if isinstance(payload.get("image_point"), dict) else {}
    arbitration = (
        payload.get("marker_level_arbitration")
        if isinstance(payload.get("marker_level_arbitration"), dict)
        else {}
    )
    return EventMarker(
        observation_id=observation.id,
        candidate_type=candidate_type,
        frame=frame,
        timestamp_ms=timestamp_ms,
        image_x=_number(image_point.get("x")),
        image_y=_number(image_point.get("y")),
        court_x=_number(court_point.get("x")),
        court_y=_number(court_point.get("y")),
        confidence=observation.confidence,
        candidate_method=_string_or_none(payload.get("candidate_method")),
        original_candidate_type=_string_or_none(payload.get("original_candidate_type")),
        arbitration_decision=_string_or_none(arbitration.get("decision")),
        arbitration_reason=_string_or_none(arbitration.get("reason")),
    )


def _trajectory_3d_rows(
    *,
    session: Session,
    media_id: str,
    trajectory_3d_run_id: str,
) -> list[BallTrajectory3DCandidate]:
    return list(
        session.scalars(
            select(BallTrajectory3DCandidate)
            .where(
                BallTrajectory3DCandidate.media_id == media_id,
                BallTrajectory3DCandidate.trajectory_3d_run_id == trajectory_3d_run_id,
            )
            .order_by(
                BallTrajectory3DCandidate.timestamp_ms,
                BallTrajectory3DCandidate.frame,
                BallTrajectory3DCandidate.id,
            )
        ).all()
    )


def _local_3d_context(
    *,
    marker: EventMarker,
    trajectory_rows: list[BallTrajectory3DCandidate],
    time_window_ms: int,
) -> Local3DContext:
    if not trajectory_rows:
        return Local3DContext(None, 0, 0, 0, False, None, None)
    local = [
        row
        for row in trajectory_rows
        if abs(int(row.timestamp_ms) - marker.timestamp_ms) <= time_window_ms
    ]
    pre = [row for row in local if int(row.timestamp_ms) <= marker.timestamp_ms]
    post = [row for row in local if int(row.timestamp_ms) >= marker.timestamp_ms]
    nearest = min(
        trajectory_rows,
        key=lambda row: (
            abs(int(row.timestamp_ms) - marker.timestamp_ms),
            abs(int(row.frame) - marker.frame),
            row.id,
        ),
    )
    if abs(int(nearest.timestamp_ms) - marker.timestamp_ms) > time_window_ms:
        nearest = None
    velocity_rows = [row for row in local if row.speed_mps is not None]
    direction_delta = _direction_delta_degrees(pre, post)
    return Local3DContext(
        nearest=nearest,
        pre_count=len(pre),
        post_count=len(post),
        local_count=len(local),
        velocity_available=bool(velocity_rows),
        speed_mps=nearest.speed_mps if nearest is not None else None,
        direction_delta_degrees=direction_delta,
    )


def _diagnostic_row(
    *,
    marker: EventMarker,
    media: MediaAsset,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str | None,
    context: Local3DContext,
    time_window_ms: int,
) -> EventCandidate3DDiagnostic:
    nearest = context.nearest
    status, label, confidence = _diagnostic_decision(context)
    height_status = (
        "unavailable"
        if nearest is None
        else "unknown"
        if nearest.court_z_m is None or nearest.court_z_status == CourtZStatus.unknown.value
        else str(nearest.court_z_status)
    )
    try:
        create = EventCandidate3DDiagnosticCreate(
            media_id=media.id,
            event_candidate_run_id=event_candidate_run_id,
            event_observation_id=marker.observation_id,
            candidate_type=marker.candidate_type,
            trajectory_3d_run_id=trajectory_3d_run_id,
            camera_geometry_id=camera_geometry_id,
            frame=marker.frame,
            timestamp_ms=marker.timestamp_ms,
            nearest_3d_candidate_id=nearest.id if nearest is not None else None,
            nearest_3d_frame=nearest.frame if nearest is not None else None,
            nearest_3d_timestamp_ms=nearest.timestamp_ms if nearest is not None else None,
            nearest_time_delta_ms=(
                abs(int(nearest.timestamp_ms) - marker.timestamp_ms)
                if nearest is not None
                else None
            ),
            nearest_court_x_m=nearest.court_x_m if nearest is not None else None,
            nearest_court_y_m=nearest.court_y_m if nearest is not None else None,
            nearest_court_z_m=nearest.court_z_m if nearest is not None else None,
            height_status=height_status,
            diagnostic_status=status,
            diagnostic_label=label,
            diagnostic_confidence=confidence,
            pre_window_sample_count=context.pre_count,
            post_window_sample_count=context.post_count,
            local_window_sample_count=context.local_count,
            local_velocity_available=context.velocity_available,
            local_speed_mps=context.speed_mps,
            local_direction_delta_degrees=context.direction_delta_degrees,
            diagnostics_jsonb={
                "time_window_ms": time_window_ms,
                "nearby_3d_samples_found": context.local_count > 0,
                "nearest_3d_sample_found": nearest is not None,
                "candidate_marker": {
                    "observation_id": marker.observation_id,
                    "candidate_type": marker.candidate_type,
                    "frame": marker.frame,
                    "timestamp_ms": marker.timestamp_ms,
                    "court_x": marker.court_x,
                    "court_y": marker.court_y,
                    "image_x": marker.image_x,
                    "image_y": marker.image_y,
                    "confidence": marker.confidence,
                    "candidate_method": marker.candidate_method,
                    "original_candidate_type": marker.original_candidate_type,
                    "arbitration_decision": marker.arbitration_decision,
                    "arbitration_reason": marker.arbitration_reason,
                },
                "nearest_3d_sample": _nearest_payload(nearest),
                "diagnostic_support": label
                == EventCandidate3DDiagnosticLabel.supports_candidate_context.value,
                "diagnostic_conflict": label
                == EventCandidate3DDiagnosticLabel.weakens_candidate_context.value,
                "cannot_evaluate": status
                in {
                    EventCandidate3DDiagnosticStatus.cannot_evaluate.value,
                    EventCandidate3DDiagnosticStatus.insufficient_3d_evidence.value,
                },
                "height_unknown": height_status == "unknown",
            },
            metadata_jsonb={
                "source_event_candidate_run_id": event_candidate_run_id,
                "source_event_observation_id": marker.observation_id,
                "source_trajectory_3d_run_id": trajectory_3d_run_id,
                "camera_geometry_id": camera_geometry_id,
                "diagnostic_coordinate_space": "court_metric_3d_readiness_v0",
            },
        )
    except EventCandidate3DDiagnosticSchemaError as exc:
        raise ValueError(str(exc)) from exc
    return EventCandidate3DDiagnostic(**create.model_dump())


def _diagnostic_decision(context: Local3DContext) -> tuple[str, str, float | None]:
    if context.local_count <= 0 or context.nearest is None:
        return (
            EventCandidate3DDiagnosticStatus.insufficient_3d_evidence.value,
            EventCandidate3DDiagnosticLabel.insufficient_evidence.value,
            None,
        )
    if (
        context.nearest.court_z_m is None
        or context.nearest.court_z_status == CourtZStatus.unknown.value
    ):
        return (
            EventCandidate3DDiagnosticStatus.height_unknown.value,
            EventCandidate3DDiagnosticLabel.neutral_context.value,
            0.0,
        )
    return (
        EventCandidate3DDiagnosticStatus.evaluated.value,
        EventCandidate3DDiagnosticLabel.neutral_context.value,
        0.0,
    )


def _resolve_camera_geometry(
    *,
    session: Session,
    media_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str | None,
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
    candidate = session.scalars(
        select(BallTrajectory3DCandidate)
        .where(
            BallTrajectory3DCandidate.media_id == media_id,
            BallTrajectory3DCandidate.trajectory_3d_run_id == trajectory_3d_run_id,
            BallTrajectory3DCandidate.camera_geometry_id.is_not(None),
        )
        .order_by(BallTrajectory3DCandidate.timestamp_ms, BallTrajectory3DCandidate.id)
    ).first()
    if candidate is not None and candidate.camera_geometry_id is not None:
        row = session.get(CameraGeometryEvidence, candidate.camera_geometry_id)
        if row is not None:
            return row
    return _failed(
        "missing_camera_geometry",
        "camera geometry evidence is required before building event candidate 3D diagnostics",
    )


def _compact_diagnostic(row: EventCandidate3DDiagnostic) -> dict[str, Any]:
    return {
        "id": row.id,
        "event_observation_id": row.event_observation_id,
        "candidate_type": row.candidate_type,
        "frame": row.frame,
        "timestamp_ms": row.timestamp_ms,
        "trajectory_3d_run_id": row.trajectory_3d_run_id,
        "camera_geometry_id": row.camera_geometry_id,
        "nearest_3d_candidate_id": row.nearest_3d_candidate_id,
        "nearest_3d_frame": row.nearest_3d_frame,
        "nearest_3d_timestamp_ms": row.nearest_3d_timestamp_ms,
        "nearest_time_delta_ms": row.nearest_time_delta_ms,
        "nearest_court_x_m": row.nearest_court_x_m,
        "nearest_court_y_m": row.nearest_court_y_m,
        "nearest_court_z_m": row.nearest_court_z_m,
        "height_status": row.height_status,
        "diagnostic_status": row.diagnostic_status,
        "diagnostic_label": row.diagnostic_label,
        "diagnostic_confidence": row.diagnostic_confidence,
        "pre_window_sample_count": row.pre_window_sample_count,
        "post_window_sample_count": row.post_window_sample_count,
        "local_window_sample_count": row.local_window_sample_count,
        "local_velocity_available": row.local_velocity_available,
        "local_speed_mps": row.local_speed_mps,
        "local_direction_delta_degrees": row.local_direction_delta_degrees,
        "diagnostic_only": True,
        "not_truth": True,
        "not_3d_truth": True,
        "height_not_verified": True,
        "no_adjudication": True,
    }


def _nearest_payload(row: BallTrajectory3DCandidate | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "id": row.id,
        "frame": row.frame,
        "timestamp_ms": row.timestamp_ms,
        "court_x_m": row.court_x_m,
        "court_y_m": row.court_y_m,
        "court_z_m": row.court_z_m,
        "court_z_status": row.court_z_status,
        "height_model": row.height_model,
        "speed_mps": row.speed_mps,
    }


def _direction_delta_degrees(
    pre: list[BallTrajectory3DCandidate],
    post: list[BallTrajectory3DCandidate],
) -> float | None:
    if len(pre) < 2 or len(post) < 2:
        return None
    before_a, before_b = pre[-2], pre[-1]
    after_a, after_b = post[0], post[1]
    before = _vector(before_a, before_b)
    after = _vector(after_a, after_b)
    if before is None or after is None:
        return None
    before_angle = math.atan2(before[1], before[0])
    after_angle = math.atan2(after[1], after[0])
    delta = abs(math.degrees(after_angle - before_angle))
    while delta > 180.0:
        delta = abs(delta - 360.0)
    return round(delta, 3)


def _vector(
    left: BallTrajectory3DCandidate,
    right: BallTrajectory3DCandidate,
) -> tuple[float, float] | None:
    if (
        left.court_x_m is None
        or left.court_y_m is None
        or right.court_x_m is None
        or right.court_y_m is None
    ):
        return None
    return right.court_x_m - left.court_x_m, right.court_y_m - left.court_y_m


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
) -> str:
    params = {
        "eventCandidateRunId": event_candidate_run_id,
        "trajectory3dRunId": trajectory_3d_run_id,
    }
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
    return value if isinstance(value, str) and value.strip() else None


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(DEFAULT_EVENT_CANDIDATE_3D_DIAGNOSTIC_WARNINGS),
    }
