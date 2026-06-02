from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    CameraGeometryEvidence,
    EventCandidate3DDiagnostic,
    EventCandidateReviewAnnotation,
    MediaAsset,
    ProcessingRun,
    Trajectory3DDebugReviewAnnotation,
)

from apps.api.services.event_candidate_reviews import serialize_event_candidate_review
from apps.api.services.replay import build_event_candidate_marker_summary
from apps.api.services.trajectory_3d_debug_reviews import (
    serialize_trajectory_3d_debug_review,
    trajectory_3d_debug_review_rows,
    trajectory_3d_debug_review_summary,
)
from apps.worker.services.ball_trajectory_3d import ball_trajectory_3d_summary
from apps.worker.services.event_candidate_3d_diagnostics import (
    event_candidate_3d_diagnostic_summary,
)

EXPORT_TYPE = "reviewed_3d_debug_dataset_export"
EXPORT_VERSION = "v0"

EXPORT_WARNINGS = {
    "dataset_export_only": True,
    "review_metadata_only": True,
    "not_truth": True,
    "not_3d_truth": True,
    "not_training_truth": True,
    "does_not_change_event_candidates": True,
    "does_not_change_3d_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}


def export_reviewed_3d_debug_dataset(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_format: str = "json",
    output_path: str | None = None,
) -> dict[str, Any]:
    """Export reviewed 3D debug evidence as an offline dataset package.

    The export is a read-only dataset view. It does not create or modify live
    observations, review annotations, candidate markers, diagnostics, or truth.
    """

    if output_format not in {"json", "markdown"}:
        return _failed(
            "unsupported_format",
            f"unsupported reviewed 3D debug export format: {output_format}",
        )

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media not found: {media_id}")

    event_run = _processing_run(session, media_id=media.id, run_id=event_candidate_run_id)
    if event_run is None:
        return _failed(
            "missing_event_candidate_run",
            f"event candidate run not found for media: {event_candidate_run_id}",
        )
    trajectory_run = _processing_run(session, media_id=media.id, run_id=trajectory_3d_run_id)
    if trajectory_run is None:
        return _failed(
            "missing_trajectory_3d_run",
            f"3D trajectory run not found for media: {trajectory_3d_run_id}",
        )
    camera_geometry = session.get(CameraGeometryEvidence, camera_geometry_id)
    if camera_geometry is None or camera_geometry.media_id != media.id:
        return _failed(
            "missing_camera_geometry",
            f"camera geometry evidence not found for media: {camera_geometry_id}",
        )

    marker_rows = _event_marker_summary(
        session=session,
        media=media,
        event_candidate_run_id=event_run.id,
    )
    trajectory_rows = _trajectory_3d_candidate_rows(
        session=session,
        media_id=media.id,
        trajectory_3d_run_id=trajectory_run.id,
    )
    diagnostic_rows = _event_candidate_3d_diagnostic_rows(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
        trajectory_3d_run_id=trajectory_run.id,
    )
    trajectory_review_rows = trajectory_3d_debug_review_rows(
        session=session,
        media_id=media.id,
        trajectory_3d_run_id=trajectory_run.id,
        event_candidate_run_id=event_run.id,
    )
    event_review_rows = _event_candidate_review_rows(
        session=session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    event_reviews_by_observation = _latest_event_reviews_by_observation(event_review_rows)
    marker_summary = [
        _with_event_review_context(marker, event_reviews_by_observation)
        for marker in marker_rows
    ]
    trajectory_reviews = [
        _json_safe(serialize_trajectory_3d_debug_review(row)) for row in trajectory_review_rows
    ]
    event_reviews = [
        _json_safe(serialize_event_candidate_review(row)) for row in event_review_rows
    ]
    trajectory_candidates = [_compact_trajectory_3d_candidate(row) for row in trajectory_rows]
    diagnostics = [_compact_event_candidate_3d_diagnostic(row) for row in diagnostic_rows]

    result: dict[str, Any] = {
        "ok": True,
        "status": "completed",
        "export_type": EXPORT_TYPE,
        "export_version": EXPORT_VERSION,
        "media_id": media.id,
        "event_candidate_run_id": event_run.id,
        "trajectory_3d_run_id": trajectory_run.id,
        "camera_geometry_id": camera_geometry.id,
        "replay_url": _replay_url(
            viewer_base_url=viewer_base_url,
            media_id=media.id,
            event_candidate_run_id=event_run.id,
            trajectory_3d_run_id=trajectory_run.id,
            camera_geometry=camera_geometry,
        ),
        "summary": {
            "event_marker_count": len(marker_summary),
            "trajectory_3d_candidate_count": len(trajectory_candidates),
            "event_candidate_3d_diagnostic_count": len(diagnostics),
            "trajectory_3d_debug_review_count": len(trajectory_reviews),
            "event_marker_review_count": len(event_reviews),
            "missing_3d_sample_note_count": sum(
                1
                for row in trajectory_review_rows
                if row.annotation_kind == "missing_3d_sample_note"
            ),
        },
        "camera_geometry_summary": _camera_geometry_summary(camera_geometry),
        "trajectory_3d_summary": ball_trajectory_3d_summary(
            session=session,
            media_id=media.id,
            trajectory_3d_run_id=trajectory_run.id,
        ),
        "event_candidate_3d_diagnostic_summary": event_candidate_3d_diagnostic_summary(
            session=session,
            media_id=media.id,
            event_candidate_run_id=event_run.id,
            trajectory_3d_run_id=trajectory_run.id,
        ),
        "trajectory_3d_debug_review_summary": trajectory_3d_debug_review_summary(
            trajectory_review_rows
        ),
        "event_marker_summary": marker_summary,
        "trajectory_3d_candidates": trajectory_candidates,
        "event_candidate_3d_diagnostics": diagnostics,
        "trajectory_3d_debug_reviews": trajectory_reviews,
        "event_candidate_reviews": event_reviews,
        "warnings": dict(EXPORT_WARNINGS),
        "known_limitations": [
            "Reviewed export labels are operator metadata, not ground truth.",
            (
                "3D candidates remain candidate evidence with unknown height unless "
                "future evidence says otherwise."
            ),
            "The export does not change live hit/bounce candidate behavior.",
            "The export does not create in/out, score, point, or adjudication decisions.",
        ],
    }

    if output_format == "markdown":
        result["markdown"] = render_reviewed_3d_debug_dataset_markdown(result)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "markdown":
            path.write_text(result["markdown"], encoding="utf-8")
        else:
            path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        result["output_path"] = str(path)

    return result


def render_reviewed_3d_debug_dataset_markdown(result: dict[str, Any]) -> str:
    summary = _dict(result.get("summary"))
    trajectory_summary = _dict(result.get("trajectory_3d_summary"))
    diagnostic_summary = _dict(result.get("event_candidate_3d_diagnostic_summary"))
    review_summary = _dict(result.get("trajectory_3d_debug_review_summary"))
    camera_summary = _dict(result.get("camera_geometry_summary"))

    rows = [
        "# Reviewed 3D Debug Dataset Export v0",
        "",
        f"Media ID: `{result.get('media_id')}`  ",
        f"Event Candidate Run ID: `{result.get('event_candidate_run_id')}`  ",
        f"3D Trajectory Run ID: `{result.get('trajectory_3d_run_id')}`  ",
        f"Camera Geometry ID: `{result.get('camera_geometry_id')}`  ",
        f"Replay URL: `{result.get('replay_url')}`",
        "",
        "## Summary",
        "",
        "| Field | Count |",
        "|---|---:|",
        f"| Event markers | {summary.get('event_marker_count', 0)} |",
        f"| 3D candidate rows | {summary.get('trajectory_3d_candidate_count', 0)} |",
        f"| 3D diagnostic rows | {summary.get('event_candidate_3d_diagnostic_count', 0)} |",
        f"| 3D debug reviews | {summary.get('trajectory_3d_debug_review_count', 0)} |",
        f"| Event marker reviews | {summary.get('event_marker_review_count', 0)} |",
        f"| Missing 3D sample notes | {summary.get('missing_3d_sample_note_count', 0)} |",
        "",
        "## Warnings",
        "",
        "- Dataset export only.",
        "- Review metadata only.",
        "- Not truth, not 3D truth, and not training truth.",
        "- Does not change event candidates, 3D candidates, in/out, score, or adjudication.",
        "",
        "## Camera Geometry",
        "",
        f"- Camera model: `{camera_summary.get('camera_model')}`",
        f"- Geometry status: `{camera_summary.get('geometry_status')}`",
        f"- Court model: `{camera_summary.get('court_model')}`",
        (
            "- True 3D reconstruction available: "
            f"`{camera_summary.get('true_3d_reconstruction_available')}`"
        ),
        "",
        "## 3D Candidate Summary",
        "",
        f"- Candidate count: `{trajectory_summary.get('candidate_count', 0)}`",
        f"- Height model: `{trajectory_summary.get('height_model')}`",
        f"- Known height count: `{trajectory_summary.get('known_height_count', 0)}`",
        f"- Unknown height count: `{trajectory_summary.get('unknown_height_count', 0)}`",
        (
            "- True 3D reconstruction available: "
            f"`{trajectory_summary.get('true_3d_reconstruction_available')}`"
        ),
        "",
        "## 3D Diagnostic Summary",
        "",
        f"- Diagnostic count: `{diagnostic_summary.get('diagnostic_count', 0)}`",
        (
            "- Nearest 3D sample found: "
            f"`{diagnostic_summary.get('nearest_3d_sample_found_count', 0)}`"
        ),
        (
            "- Insufficient 3D evidence: "
            f"`{diagnostic_summary.get('insufficient_3d_evidence_count', 0)}`"
        ),
        f"- Height unknown: `{diagnostic_summary.get('height_unknown_count', 0)}`",
        "",
        "## 3D Debug Review Summary",
        "",
        f"- Total reviews: `{review_summary.get('total_reviews', 0)}`",
        f"- Sample reviews: `{review_summary.get('sample_reviews', 0)}`",
        f"- Diagnostic reviews: `{review_summary.get('diagnostic_reviews', 0)}`",
        f"- Missing 3D sample notes: `{review_summary.get('missing_3d_sample_notes', 0)}`",
        "",
        "## Event Markers",
        "",
        "| # | Type | Frame | Time ms | Confidence | Review |",
        "|---|---|---:|---:|---:|---|",
    ]
    marker_summary = result.get("event_marker_summary")
    if isinstance(marker_summary, list) and marker_summary:
        for marker in marker_summary:
            if not isinstance(marker, dict):
                continue
            rows.append(
                (
                    "| {index} | {candidate_type} | {frame} | {timestamp_ms} | "
                    "{confidence} | {review} |"
                ).format(
                    index=marker.get("index", ""),
                    candidate_type=marker.get("candidate_type", ""),
                    frame=marker.get("frame", ""),
                    timestamp_ms=marker.get("timestamp_ms", ""),
                    confidence=marker.get("confidence", ""),
                    review=marker.get("review_label") or "",
                )
            )
    else:
        rows.append("| n/a | No event markers exported |  |  |  |  |")

    rows.extend(
        [
            "",
            "## 3D Candidate Examples",
            "",
            "| ID | Frame | Time ms | X m | Y m | Z m | Z status |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    candidates = [
        row for row in result.get("trajectory_3d_candidates", []) if isinstance(row, dict)
    ]
    for candidate in _first_last_examples(candidates):
        rows.append(
            (
                "| {id} | {frame} | {timestamp_ms} | {court_x_m} | {court_y_m} | "
                "{court_z_m} | {court_z_status} |"
            ).format(
                id=candidate.get("id", ""),
                frame=candidate.get("frame", ""),
                timestamp_ms=candidate.get("timestamp_ms", ""),
                court_x_m=candidate.get("court_x_m", ""),
                court_y_m=candidate.get("court_y_m", ""),
                court_z_m=candidate.get("court_z_m", ""),
                court_z_status=candidate.get("court_z_status", ""),
            )
        )
    if not candidates:
        rows.append("| n/a | No 3D candidate rows exported |  |  |  |  |  |")

    rows.extend(
        [
            "",
            "## Known Limitations",
            "",
        ]
    )
    for limitation in result.get("known_limitations", []):
        rows.append(f"- {limitation}")
    rows.append("")
    return "\n".join(rows)


def _failed(status: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": status,
        "message": message,
        "export_type": EXPORT_TYPE,
        "export_version": EXPORT_VERSION,
        "warnings": dict(EXPORT_WARNINGS),
    }


def _processing_run(
    session: Session,
    *,
    media_id: str,
    run_id: str,
) -> ProcessingRun | None:
    run = session.get(ProcessingRun, run_id)
    if run is None or run.media_id != media_id:
        return None
    return run


def _event_marker_summary(
    *,
    session: Session,
    media: MediaAsset,
    event_candidate_run_id: str,
) -> list[dict[str, Any]]:
    return build_event_candidate_marker_summary(
        session=session,
        media=media,
        event_candidate_run_id=event_candidate_run_id,
    )


def _trajectory_3d_candidate_rows(
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


def _event_candidate_3d_diagnostic_rows(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
) -> list[EventCandidate3DDiagnostic]:
    return list(
        session.scalars(
            select(EventCandidate3DDiagnostic)
            .where(
                EventCandidate3DDiagnostic.media_id == media_id,
                EventCandidate3DDiagnostic.event_candidate_run_id == event_candidate_run_id,
                EventCandidate3DDiagnostic.trajectory_3d_run_id == trajectory_3d_run_id,
            )
            .order_by(
                EventCandidate3DDiagnostic.timestamp_ms,
                EventCandidate3DDiagnostic.frame,
                EventCandidate3DDiagnostic.id,
            )
        ).all()
    )


def _event_candidate_review_rows(
    *,
    session: Session,
    media_id: str,
    event_candidate_run_id: str,
) -> list[EventCandidateReviewAnnotation]:
    return list(
        session.scalars(
            select(EventCandidateReviewAnnotation)
            .where(
                EventCandidateReviewAnnotation.media_id == media_id,
                EventCandidateReviewAnnotation.event_candidate_run_id == event_candidate_run_id,
            )
            .order_by(
                EventCandidateReviewAnnotation.created_at,
                EventCandidateReviewAnnotation.id,
            )
        ).all()
    )


def _latest_event_reviews_by_observation(
    rows: list[EventCandidateReviewAnnotation],
) -> dict[str, EventCandidateReviewAnnotation]:
    latest: dict[str, EventCandidateReviewAnnotation] = {}
    for row in rows:
        if row.observation_id is None:
            continue
        latest[row.observation_id] = row
    return latest


def _with_event_review_context(
    marker: dict[str, Any],
    latest_reviews: dict[str, EventCandidateReviewAnnotation],
) -> dict[str, Any]:
    enriched = dict(marker)
    review = latest_reviews.get(str(marker.get("observation_id") or ""))
    if review is not None:
        enriched["review_label"] = review.review_label
        enriched["review_note"] = review.note
        enriched["review_annotation_id"] = review.id
    return _json_safe(enriched)


def _camera_geometry_summary(row: CameraGeometryEvidence) -> dict[str, Any]:
    return _json_safe(
        {
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
            "court_dimensions": {
                "units": row.court_units,
                "court_length": row.court_length,
                "court_width": row.court_width,
                "singles_width": row.singles_sideline_width,
                "doubles_width": row.doubles_sideline_width,
                "net_height_center": row.net_height_center,
                "net_height_posts": row.net_height_posts,
            },
            "image_size": row.image_size_jsonb or {},
            "world_coordinate_system": row.world_coordinate_system_jsonb or {},
            "assumptions": row.assumptions_jsonb or {},
            "warnings": row.warnings_jsonb or {},
            "true_3d_reconstruction_available": bool(
                (row.metadata_jsonb or {}).get("true_3d_reconstruction_available") is True
            ),
            "geometry_evidence_only": True,
            "no_adjudication": True,
        }
    )


def _compact_trajectory_3d_candidate(row: BallTrajectory3DCandidate) -> dict[str, Any]:
    return _json_safe(
        {
            "id": row.id,
            "source_observation_id": row.source_observation_id,
            "ball_trajectory_run_id": row.ball_trajectory_run_id,
            "court_projection_run_id": row.court_projection_run_id,
            "camera_geometry_id": row.camera_geometry_id,
            "geometry_run_id": row.geometry_run_id,
            "trajectory_3d_run_id": row.trajectory_3d_run_id,
            "frame": row.frame,
            "timestamp_ms": row.timestamp_ms,
            "image_x": row.image_x,
            "image_y": row.image_y,
            "court_x": row.court_x,
            "court_y": row.court_y,
            "court_x_m": row.court_x_m,
            "court_y_m": row.court_y_m,
            "court_z_m": row.court_z_m,
            "court_z_status": row.court_z_status,
            "height_model": row.height_model,
            "projection_method": row.projection_method,
            "confidence": row.confidence,
            "velocity_x_mps": row.velocity_x_mps,
            "velocity_y_mps": row.velocity_y_mps,
            "velocity_z_mps": row.velocity_z_mps,
            "speed_mps": row.speed_mps,
            "diagnostics": row.diagnostics_jsonb or {},
            "warnings": row.warnings_jsonb or {},
            "metadata": row.metadata_jsonb or {},
        }
    )


def _compact_event_candidate_3d_diagnostic(row: EventCandidate3DDiagnostic) -> dict[str, Any]:
    return _json_safe(
        {
            "id": row.id,
            "event_observation_id": row.event_observation_id,
            "candidate_type": row.candidate_type,
            "event_candidate_run_id": row.event_candidate_run_id,
            "trajectory_3d_run_id": row.trajectory_3d_run_id,
            "camera_geometry_id": row.camera_geometry_id,
            "frame": row.frame,
            "timestamp_ms": row.timestamp_ms,
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
            "diagnostics": row.diagnostics_jsonb or {},
            "warnings": row.warnings_jsonb or {},
            "metadata": row.metadata_jsonb or {},
        }
    )


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    event_candidate_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry: CameraGeometryEvidence,
) -> str:
    params = {
        "eventCandidateRunId": event_candidate_run_id,
        "trajectory3dRunId": trajectory_3d_run_id,
    }
    if camera_geometry.court_run_id is not None:
        params["courtRunId"] = camera_geometry.court_run_id
    if camera_geometry.court_projection_run_id is not None:
        params["courtProjectionRunId"] = camera_geometry.court_projection_run_id
    if camera_geometry.homography_run_id is not None:
        params["homographyRunId"] = camera_geometry.homography_run_id
    return f"{viewer_base_url.rstrip('/')}/replay/{media_id}?{urlencode(params)}"


def _json_safe(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    return value


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _first_last_examples(rows: list[dict[str, Any]], count: int = 3) -> list[dict[str, Any]]:
    if len(rows) <= count * 2:
        return rows
    examples = rows[:count] + rows[-count:]
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for row in examples:
        key = str(row.get("id") or "")
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def review_label_counts(rows: list[Trajectory3DDebugReviewAnnotation]) -> dict[str, int]:
    return dict(Counter(row.review_label for row in rows))
