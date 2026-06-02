from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from tom_v3_schema.trajectory_3d_debug_review import (
    Trajectory3DDebugReviewAnnotationCreate,
    Trajectory3DDebugReviewAnnotationUpdate,
)
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    CameraGeometryEvidence,
    EventCandidate3DDiagnostic,
    MediaAsset,
    Observation,
    ProcessingRun,
    Trajectory3DDebugReviewAnnotation,
)

REVIEW_KINDS = {
    "trajectory_3d_sample_review",
    "event_candidate_3d_diagnostic_review",
    "missing_3d_sample_note",
    "debug_view_note",
}

REVIEW_LABELS = {
    "useful",
    "wrong",
    "unclear",
    "needs_review",
    "missing_3d_sample",
    "bad_3d_position",
    "bad_diagnostic_link",
}

SAMPLE_REVIEW_LABELS = {
    "useful",
    "wrong",
    "unclear",
    "needs_review",
    "bad_3d_position",
}

DIAGNOSTIC_REVIEW_LABELS = {
    "useful",
    "wrong",
    "unclear",
    "needs_review",
    "bad_diagnostic_link",
}

MISSING_3D_SAMPLE_LABELS = {"missing_3d_sample"}

DEBUG_VIEW_NOTE_LABELS = {
    "useful",
    "wrong",
    "unclear",
    "needs_review",
}

REVIEW_WARNINGS = {
    "review_metadata_only": True,
    "not_truth": True,
    "not_3d_truth": True,
    "does_not_change_event_candidates": True,
    "does_not_change_3d_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}


class Trajectory3DDebugReviewError(ValueError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def list_trajectory_3d_debug_reviews(
    session: Session,
    *,
    media_id: str,
    trajectory_3d_run_id: str | None = None,
    event_candidate_run_id: str | None = None,
) -> dict[str, Any]:
    _validate_media(session, media_id=media_id)
    if trajectory_3d_run_id is not None:
        _validate_run(session, media_id=media_id, run_id=trajectory_3d_run_id, name="3D run")
    if event_candidate_run_id is not None:
        _validate_run(
            session,
            media_id=media_id,
            run_id=event_candidate_run_id,
            name="event candidate run",
        )
    rows = trajectory_3d_debug_review_rows(
        session=session,
        media_id=media_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        event_candidate_run_id=event_candidate_run_id,
    )
    return trajectory_3d_debug_review_list_payload(rows)


def create_trajectory_3d_debug_review(
    session: Session,
    *,
    media_id: str,
    request: Trajectory3DDebugReviewAnnotationCreate,
) -> Trajectory3DDebugReviewAnnotation:
    _validate_media(session, media_id=media_id)
    _validate_kind_and_label(request.annotation_kind, request.review_label)
    payload = request.model_dump()
    payload["media_id"] = media_id
    payload = _enrich_review_payload(session, payload)
    row = Trajectory3DDebugReviewAnnotation(**payload)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def update_trajectory_3d_debug_review(
    session: Session,
    *,
    media_id: str,
    review_id: str,
    request: Trajectory3DDebugReviewAnnotationUpdate,
) -> Trajectory3DDebugReviewAnnotation:
    row = _get_review(session, media_id=media_id, review_id=review_id)
    next_label = request.review_label if request.review_label is not None else row.review_label
    _validate_kind_and_label(row.annotation_kind, next_label)
    if request.review_label is not None:
        row.review_label = request.review_label
    if request.note is not None:
        row.note = request.note
    if request.reviewer is not None:
        row.reviewer = request.reviewer
    if request.payload_jsonb is not None:
        row.payload_jsonb = {
            **(row.payload_jsonb or {}),
            **request.payload_jsonb,
            **REVIEW_WARNINGS,
        }
    row.updated_at = datetime.now(UTC)
    session.commit()
    session.refresh(row)
    return row


def serialize_trajectory_3d_debug_review(
    row: Trajectory3DDebugReviewAnnotation,
) -> dict[str, Any]:
    return {
        "id": row.id,
        "media_id": row.media_id,
        "trajectory_3d_run_id": row.trajectory_3d_run_id,
        "camera_geometry_id": row.camera_geometry_id,
        "event_candidate_run_id": row.event_candidate_run_id,
        "event_observation_id": row.event_observation_id,
        "trajectory_3d_candidate_id": row.trajectory_3d_candidate_id,
        "event_candidate_3d_diagnostic_id": row.event_candidate_3d_diagnostic_id,
        "annotation_kind": row.annotation_kind,
        "review_label": row.review_label,
        "frame": row.frame,
        "timestamp_ms": row.timestamp_ms,
        "image_x": row.image_x,
        "image_y": row.image_y,
        "court_x_m": row.court_x_m,
        "court_y_m": row.court_y_m,
        "court_z_m": row.court_z_m,
        "note": row.note,
        "reviewer": row.reviewer,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "payload_jsonb": row.payload_jsonb or {},
    }


def trajectory_3d_debug_review_summary(
    rows: list[Trajectory3DDebugReviewAnnotation],
) -> dict[str, Any]:
    label_counts = Counter(row.review_label for row in rows)
    return {
        "available": bool(rows),
        "total_reviews": len(rows),
        "sample_reviews": sum(
            1 for row in rows if row.annotation_kind == "trajectory_3d_sample_review"
        ),
        "diagnostic_reviews": sum(
            1
            for row in rows
            if row.annotation_kind == "event_candidate_3d_diagnostic_review"
        ),
        "missing_3d_sample_notes": sum(
            1 for row in rows if row.annotation_kind == "missing_3d_sample_note"
        ),
        "debug_view_notes": sum(1 for row in rows if row.annotation_kind == "debug_view_note"),
        "useful": label_counts.get("useful", 0),
        "wrong": label_counts.get("wrong", 0),
        "unclear": label_counts.get("unclear", 0),
        "needs_review": label_counts.get("needs_review", 0),
        "missing_3d_sample": label_counts.get("missing_3d_sample", 0),
        "bad_3d_position": label_counts.get("bad_3d_position", 0),
        "bad_diagnostic_link": label_counts.get("bad_diagnostic_link", 0),
        **REVIEW_WARNINGS,
    }


def trajectory_3d_debug_review_rows(
    *,
    session: Session,
    media_id: str,
    trajectory_3d_run_id: str | None = None,
    event_candidate_run_id: str | None = None,
) -> list[Trajectory3DDebugReviewAnnotation]:
    query = select(Trajectory3DDebugReviewAnnotation).where(
        Trajectory3DDebugReviewAnnotation.media_id == media_id
    )
    context_filters = []
    if trajectory_3d_run_id is not None:
        context_filters.append(
            Trajectory3DDebugReviewAnnotation.trajectory_3d_run_id == trajectory_3d_run_id
        )
    if event_candidate_run_id is not None:
        context_filters.append(
            Trajectory3DDebugReviewAnnotation.event_candidate_run_id
            == event_candidate_run_id
        )
    if context_filters:
        query = query.where(or_(*context_filters))
    query = query.order_by(
        Trajectory3DDebugReviewAnnotation.created_at,
        Trajectory3DDebugReviewAnnotation.id,
    )
    return list(session.scalars(query).all())


def trajectory_3d_debug_review_summary_for_media(
    *,
    session: Session,
    media_id: str,
    trajectory_3d_run_id: str | None = None,
    event_candidate_run_id: str | None = None,
) -> dict[str, Any]:
    rows = trajectory_3d_debug_review_rows(
        session=session,
        media_id=media_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        event_candidate_run_id=event_candidate_run_id,
    )
    return trajectory_3d_debug_review_summary(rows)


def trajectory_3d_debug_review_list_payload(
    rows: list[Trajectory3DDebugReviewAnnotation],
) -> dict[str, Any]:
    reviews = [serialize_trajectory_3d_debug_review(row) for row in rows]
    by_sample: dict[str, list[dict[str, Any]]] = {}
    by_diagnostic: dict[str, list[dict[str, Any]]] = {}
    for review in reviews:
        sample_id = review.get("trajectory_3d_candidate_id")
        diagnostic_id = review.get("event_candidate_3d_diagnostic_id")
        if isinstance(sample_id, str):
            by_sample.setdefault(sample_id, []).append(review)
        if isinstance(diagnostic_id, str):
            by_diagnostic.setdefault(diagnostic_id, []).append(review)
    return {
        "reviews": reviews,
        "reviews_by_trajectory_3d_candidate_id": by_sample,
        "reviews_by_event_candidate_3d_diagnostic_id": by_diagnostic,
        "review_summary": trajectory_3d_debug_review_summary(rows),
        "warnings": REVIEW_WARNINGS,
    }


def _validate_media(session: Session, *, media_id: str) -> MediaAsset:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise Trajectory3DDebugReviewError(404, "media asset not found")
    return media


def _validate_run(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    name: str,
) -> ProcessingRun:
    run = session.get(ProcessingRun, run_id)
    if run is None:
        raise Trajectory3DDebugReviewError(404, f"{name} not found")
    if run.media_id != media_id:
        raise Trajectory3DDebugReviewError(400, f"{name} does not belong to media")
    return run


def _validate_kind_and_label(annotation_kind: str, review_label: str) -> None:
    if annotation_kind not in REVIEW_KINDS:
        raise Trajectory3DDebugReviewError(400, "unsupported 3D debug review annotation kind")
    if review_label not in REVIEW_LABELS:
        raise Trajectory3DDebugReviewError(400, "unsupported 3D debug review label")
    if (
        annotation_kind == "trajectory_3d_sample_review"
        and review_label not in SAMPLE_REVIEW_LABELS
    ):
        raise Trajectory3DDebugReviewError(
            400,
            "3D sample reviews require useful, wrong, unclear, needs_review, or bad_3d_position",
        )
    if (
        annotation_kind == "event_candidate_3d_diagnostic_review"
        and review_label not in DIAGNOSTIC_REVIEW_LABELS
    ):
        raise Trajectory3DDebugReviewError(
            400,
            (
                "3D diagnostic reviews require useful, wrong, unclear, needs_review, "
                "or bad_diagnostic_link"
            ),
        )
    if (
        annotation_kind == "missing_3d_sample_note"
        and review_label not in MISSING_3D_SAMPLE_LABELS
    ):
        raise Trajectory3DDebugReviewError(
            400,
            "missing 3D sample notes require missing_3d_sample",
        )
    if annotation_kind == "debug_view_note" and review_label not in DEBUG_VIEW_NOTE_LABELS:
        raise Trajectory3DDebugReviewError(
            400,
            "debug view notes require useful, wrong, unclear, or needs_review",
        )


def _enrich_review_payload(session: Session, payload: dict[str, Any]) -> dict[str, Any]:
    payload["payload_jsonb"] = {
        **(payload.get("payload_jsonb") or {}),
        **REVIEW_WARNINGS,
    }
    media_id = payload["media_id"]
    trajectory_3d_run_id = payload.get("trajectory_3d_run_id")
    event_candidate_run_id = payload.get("event_candidate_run_id")
    camera_geometry_id = payload.get("camera_geometry_id")
    event_observation_id = payload.get("event_observation_id")
    sample_id = payload.get("trajectory_3d_candidate_id")
    diagnostic_id = payload.get("event_candidate_3d_diagnostic_id")

    if trajectory_3d_run_id is not None:
        _validate_run(session, media_id=media_id, run_id=trajectory_3d_run_id, name="3D run")
    if event_candidate_run_id is not None:
        _validate_run(
            session,
            media_id=media_id,
            run_id=event_candidate_run_id,
            name="event candidate run",
        )
    if camera_geometry_id is not None:
        camera_geometry = session.get(CameraGeometryEvidence, camera_geometry_id)
        if camera_geometry is None:
            raise Trajectory3DDebugReviewError(404, "camera geometry not found")
        if camera_geometry.media_id != media_id:
            raise Trajectory3DDebugReviewError(400, "camera geometry does not belong to media")
    if event_observation_id is not None:
        observation = session.get(Observation, event_observation_id)
        if observation is None:
            raise Trajectory3DDebugReviewError(404, "event observation not found")
        if observation.media_id != media_id:
            raise Trajectory3DDebugReviewError(400, "event observation does not belong to media")
        if event_candidate_run_id is not None and observation.run_id != event_candidate_run_id:
            raise Trajectory3DDebugReviewError(
                400,
                "event observation does not belong to event candidate run",
            )
    if sample_id is not None:
        _enrich_from_trajectory_3d_sample(session, payload, sample_id)
    if diagnostic_id is not None:
        _enrich_from_event_candidate_3d_diagnostic(session, payload, diagnostic_id)

    if payload["annotation_kind"] == "trajectory_3d_sample_review" and sample_id is None:
        raise Trajectory3DDebugReviewError(
            400,
            "3D sample review requires trajectory_3d_candidate_id",
        )
    if (
        payload["annotation_kind"] == "event_candidate_3d_diagnostic_review"
        and diagnostic_id is None
    ):
        raise Trajectory3DDebugReviewError(
            400,
            "3D diagnostic review requires event_candidate_3d_diagnostic_id",
        )
    return payload


def _enrich_from_trajectory_3d_sample(
    session: Session,
    payload: dict[str, Any],
    sample_id: str,
) -> None:
    sample = session.get(BallTrajectory3DCandidate, sample_id)
    if sample is None:
        raise Trajectory3DDebugReviewError(404, "3D trajectory candidate not found")
    if sample.media_id != payload["media_id"]:
        raise Trajectory3DDebugReviewError(
            400,
            "3D trajectory candidate does not belong to media",
        )
    if payload.get("trajectory_3d_run_id") is not None:
        if sample.trajectory_3d_run_id != payload["trajectory_3d_run_id"]:
            raise Trajectory3DDebugReviewError(
                400,
                "3D trajectory candidate does not belong to selected 3D run",
            )
    payload["trajectory_3d_run_id"] = (
        payload.get("trajectory_3d_run_id") or sample.trajectory_3d_run_id
    )
    payload["camera_geometry_id"] = payload.get("camera_geometry_id") or sample.camera_geometry_id
    payload["frame"] = payload.get("frame") if payload.get("frame") is not None else sample.frame
    payload["timestamp_ms"] = (
        payload.get("timestamp_ms")
        if payload.get("timestamp_ms") is not None
        else sample.timestamp_ms
    )
    payload["court_x_m"] = (
        payload.get("court_x_m") if payload.get("court_x_m") is not None else sample.court_x_m
    )
    payload["court_y_m"] = (
        payload.get("court_y_m") if payload.get("court_y_m") is not None else sample.court_y_m
    )
    payload["court_z_m"] = (
        payload.get("court_z_m") if payload.get("court_z_m") is not None else sample.court_z_m
    )


def _enrich_from_event_candidate_3d_diagnostic(
    session: Session,
    payload: dict[str, Any],
    diagnostic_id: str,
) -> None:
    diagnostic = session.get(EventCandidate3DDiagnostic, diagnostic_id)
    if diagnostic is None:
        raise Trajectory3DDebugReviewError(404, "3D diagnostic not found")
    if diagnostic.media_id != payload["media_id"]:
        raise Trajectory3DDebugReviewError(400, "3D diagnostic does not belong to media")
    if payload.get("event_candidate_run_id") is not None:
        if diagnostic.event_candidate_run_id != payload["event_candidate_run_id"]:
            raise Trajectory3DDebugReviewError(
                400,
                "3D diagnostic does not belong to selected event candidate run",
            )
    if (
        payload.get("trajectory_3d_run_id") is not None
        and diagnostic.trajectory_3d_run_id is not None
    ):
        if diagnostic.trajectory_3d_run_id != payload["trajectory_3d_run_id"]:
            raise Trajectory3DDebugReviewError(
                400,
                "3D diagnostic does not belong to selected 3D run",
            )
    payload["event_candidate_run_id"] = (
        payload.get("event_candidate_run_id") or diagnostic.event_candidate_run_id
    )
    payload["event_observation_id"] = (
        payload.get("event_observation_id") or diagnostic.event_observation_id
    )
    payload["trajectory_3d_run_id"] = (
        payload.get("trajectory_3d_run_id") or diagnostic.trajectory_3d_run_id
    )
    payload["camera_geometry_id"] = (
        payload.get("camera_geometry_id") or diagnostic.camera_geometry_id
    )
    payload["trajectory_3d_candidate_id"] = (
        payload.get("trajectory_3d_candidate_id") or diagnostic.nearest_3d_candidate_id
    )
    payload["frame"] = (
        payload.get("frame") if payload.get("frame") is not None else diagnostic.frame
    )
    payload["timestamp_ms"] = (
        payload.get("timestamp_ms")
        if payload.get("timestamp_ms") is not None
        else diagnostic.timestamp_ms
    )
    payload["court_x_m"] = (
        payload.get("court_x_m")
        if payload.get("court_x_m") is not None
        else diagnostic.nearest_court_x_m
    )
    payload["court_y_m"] = (
        payload.get("court_y_m")
        if payload.get("court_y_m") is not None
        else diagnostic.nearest_court_y_m
    )
    payload["court_z_m"] = (
        payload.get("court_z_m")
        if payload.get("court_z_m") is not None
        else diagnostic.nearest_court_z_m
    )


def _get_review(
    session: Session,
    *,
    media_id: str,
    review_id: str,
) -> Trajectory3DDebugReviewAnnotation:
    row = session.get(Trajectory3DDebugReviewAnnotation, review_id)
    if row is None or row.media_id != media_id:
        raise Trajectory3DDebugReviewError(404, "3D debug review annotation not found")
    return row
