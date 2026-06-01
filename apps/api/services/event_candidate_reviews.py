from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.event_candidate_reviews import (
    EventCandidateReviewCreate,
    EventCandidateReviewUpdate,
)
from tom_v3_storage.db_models import (
    EventCandidateReviewAnnotation,
    MediaAsset,
    Observation,
    ProcessingRun,
)

from apps.api.services.replay import event_candidate_overlay_item_from_observation

CANDIDATE_MARKER_REVIEW_LABELS = {"useful", "wrong", "unclear", "needs_review"}
MISSING_CANDIDATE_REVIEW_LABELS = {
    "missing_hit_candidate",
    "missing_bounce_candidate",
    "missing_event_candidate",
}
REVIEW_KINDS = {
    "candidate_marker_review",
    "point_moment_review",
    "missing_candidate_note",
}

REVIEW_WARNINGS = {
    "review_metadata_only": True,
    "candidate_evidence_preserved": True,
    "not_hit_truth": True,
    "not_bounce_truth": True,
    "not_in_out_truth": True,
    "no_score_or_point_truth": True,
    "no_adjudication": True,
}


class EventCandidateReviewError(ValueError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def list_event_candidate_reviews(
    session: Session,
    *,
    media_id: str,
    event_candidate_run_id: str,
) -> dict[str, Any]:
    _validate_media_and_run(
        session,
        media_id=media_id,
        event_candidate_run_id=event_candidate_run_id,
    )
    rows = session.scalars(
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
    return _review_list_payload(rows)


def create_event_candidate_review(
    session: Session,
    *,
    media_id: str,
    request: EventCandidateReviewCreate,
) -> EventCandidateReviewAnnotation:
    _validate_media_and_run(
        session,
        media_id=media_id,
        event_candidate_run_id=request.event_candidate_run_id,
    )
    _validate_kind_and_label(request.annotation_kind, request.review_label)
    payload = request.model_dump()
    payload["media_id"] = media_id
    payload = _enrich_review_payload(session, payload)
    row = EventCandidateReviewAnnotation(**payload)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def update_event_candidate_review(
    session: Session,
    *,
    media_id: str,
    review_id: str,
    request: EventCandidateReviewUpdate,
) -> EventCandidateReviewAnnotation:
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
            "review_metadata_only": True,
            "candidate_evidence_preserved": True,
        }
    row.updated_at = datetime.now(UTC)
    session.commit()
    session.refresh(row)
    return row


def delete_event_candidate_review(
    session: Session,
    *,
    media_id: str,
    review_id: str,
) -> dict[str, Any]:
    row = _get_review(session, media_id=media_id, review_id=review_id)
    session.delete(row)
    session.commit()
    return {"ok": True, "deleted_review_id": review_id, "review_metadata_only": True}


def serialize_event_candidate_review(
    row: EventCandidateReviewAnnotation,
) -> dict[str, Any]:
    return {
        "id": row.id,
        "media_id": row.media_id,
        "event_candidate_run_id": row.event_candidate_run_id,
        "observation_id": row.observation_id,
        "annotation_kind": row.annotation_kind,
        "review_label": row.review_label,
        "candidate_type": row.candidate_type,
        "frame": row.frame,
        "timestamp_ms": row.timestamp_ms,
        "image_x": row.image_x,
        "image_y": row.image_y,
        "court_x": row.court_x,
        "court_y": row.court_y,
        "note": row.note,
        "reviewer": row.reviewer,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "payload_jsonb": row.payload_jsonb or {},
    }


def build_event_candidate_review_summary(
    rows: list[EventCandidateReviewAnnotation],
) -> dict[str, int]:
    label_counts = Counter(row.review_label for row in rows)
    summary = {
        "total_reviews": len(rows),
        "useful": label_counts.get("useful", 0),
        "wrong": label_counts.get("wrong", 0),
        "unclear": label_counts.get("unclear", 0),
        "needs_review": label_counts.get("needs_review", 0),
        "missing_candidate_note": sum(
            1 for row in rows if row.annotation_kind == "missing_candidate_note"
        ),
        "missing_hit_candidate": label_counts.get("missing_hit_candidate", 0),
        "missing_bounce_candidate": label_counts.get("missing_bounce_candidate", 0),
        "missing_event_candidate": label_counts.get("missing_event_candidate", 0),
    }
    return summary


def _review_list_payload(rows: list[EventCandidateReviewAnnotation]) -> dict[str, Any]:
    reviews = [serialize_event_candidate_review(row) for row in rows]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for review in reviews:
        observation_id = review.get("observation_id")
        if isinstance(observation_id, str):
            grouped.setdefault(observation_id, []).append(review)
    return {
        "reviews": reviews,
        "reviews_by_observation_id": grouped,
        "review_summary": build_event_candidate_review_summary(rows),
        "warnings": REVIEW_WARNINGS,
    }


def _validate_media_and_run(
    session: Session,
    *,
    media_id: str,
    event_candidate_run_id: str,
) -> tuple[MediaAsset, ProcessingRun]:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise EventCandidateReviewError(404, "media asset not found")
    run = session.get(ProcessingRun, event_candidate_run_id)
    if run is None:
        raise EventCandidateReviewError(404, "event candidate run not found")
    if run.media_id != media_id:
        raise EventCandidateReviewError(
            400,
            "event candidate run does not belong to media",
        )
    return media, run


def _validate_kind_and_label(annotation_kind: str, review_label: str) -> None:
    if annotation_kind not in REVIEW_KINDS:
        raise EventCandidateReviewError(400, "unsupported review annotation kind")
    if annotation_kind == "missing_candidate_note":
        if review_label not in MISSING_CANDIDATE_REVIEW_LABELS:
            raise EventCandidateReviewError(
                400,
                "missing candidate notes require a missing_* candidate label",
            )
        return
    if review_label not in CANDIDATE_MARKER_REVIEW_LABELS:
        raise EventCandidateReviewError(
            400,
            "candidate marker reviews require useful, wrong, unclear, or needs_review",
        )


def _enrich_review_payload(session: Session, payload: dict[str, Any]) -> dict[str, Any]:
    payload["payload_jsonb"] = {
        **(payload.get("payload_jsonb") or {}),
        "review_metadata_only": True,
        "candidate_evidence_preserved": True,
        "not_truth": True,
        "no_adjudication": True,
    }
    if payload["annotation_kind"] == "candidate_marker_review" and not payload.get(
        "observation_id"
    ):
        raise EventCandidateReviewError(
            400,
            "candidate marker review requires observation_id",
        )
    observation_id = payload.get("observation_id")
    if not observation_id:
        return payload

    observation = session.get(Observation, observation_id)
    if observation is None:
        raise EventCandidateReviewError(404, "event candidate observation not found")
    if observation.media_id != payload["media_id"]:
        raise EventCandidateReviewError(400, "observation does not belong to media")
    if observation.run_id != payload["event_candidate_run_id"]:
        raise EventCandidateReviewError(
            400,
            "observation does not belong to event candidate run",
        )
    if observation.observation_type not in {"hit_candidate", "bounce_candidate"}:
        raise EventCandidateReviewError(400, "observation is not an event candidate marker")

    item = event_candidate_overlay_item_from_observation(
        observation,
        session=session,
        media_id=payload["media_id"],
    )
    if item is not None:
        image_point = item.get("image_point")
        court_point = item.get("court_point")
        payload["candidate_type"] = payload.get("candidate_type") or item.get("candidate_type")
        payload["frame"] = payload.get("frame") if payload.get("frame") is not None else item.get(
            "frame_number"
        )
        payload["timestamp_ms"] = (
            payload.get("timestamp_ms")
            if payload.get("timestamp_ms") is not None
            else item.get("timestamp_ms")
        )
        if isinstance(image_point, dict):
            payload["image_x"] = (
                payload.get("image_x")
                if payload.get("image_x") is not None
                else image_point.get("x")
            )
            payload["image_y"] = (
                payload.get("image_y")
                if payload.get("image_y") is not None
                else image_point.get("y")
            )
        if isinstance(court_point, dict):
            payload["court_x"] = (
                payload.get("court_x")
                if payload.get("court_x") is not None
                else court_point.get("x")
            )
            payload["court_y"] = (
                payload.get("court_y")
                if payload.get("court_y") is not None
                else court_point.get("y")
            )
    return payload


def _get_review(
    session: Session,
    *,
    media_id: str,
    review_id: str,
) -> EventCandidateReviewAnnotation:
    row = session.get(EventCandidateReviewAnnotation, review_id)
    if row is None:
        raise EventCandidateReviewError(404, "review annotation not found")
    if row.media_id != media_id:
        raise EventCandidateReviewError(404, "review annotation not found")
    return row
