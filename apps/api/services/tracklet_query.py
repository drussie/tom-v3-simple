from __future__ import annotations

from collections import Counter
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.tracklets import (
    AnnotationSummary,
    TrackletQueryFilters,
    TrackletQueryResponse,
    TrackletQueryRow,
)
from tom_v3_storage.db_models import HumanAnnotation, Observation, Tracklet

from apps.api.routers.viewer import _observation_payload
from apps.api.services.annotation_review import annotation_label, summarize_annotations
from apps.api.services.tracklet_evidence_bundle import _tracklet_payload


def query_tracklets(
    session: Session,
    filters: TrackletQueryFilters,
) -> TrackletQueryResponse:
    stmt = select(Tracklet).order_by(
        Tracklet.track_family,
        Tracklet.subject_ref,
        Tracklet.frame_start,
        Tracklet.id,
    )
    if filters.media_id is not None:
        stmt = stmt.where(Tracklet.media_id == filters.media_id)
    if filters.tracklet_run_id is not None:
        stmt = stmt.where(Tracklet.run_id == filters.tracklet_run_id)
    if filters.track_family is not None:
        stmt = stmt.where(Tracklet.track_family == filters.track_family)
    if filters.subject_ref is not None:
        stmt = stmt.where(Tracklet.subject_ref == filters.subject_ref)
    if filters.frame_start_gte is not None:
        stmt = stmt.where(Tracklet.frame_start >= filters.frame_start_gte)
    if filters.frame_end_lte is not None:
        stmt = stmt.where(Tracklet.frame_end <= filters.frame_end_lte)
    if filters.confidence_gte is not None:
        stmt = stmt.where(Tracklet.confidence >= filters.confidence_gte)
    if filters.confidence_lte is not None:
        stmt = stmt.where(Tracklet.confidence <= filters.confidence_lte)

    tracklets = list(session.scalars(stmt).all())
    observation_ids = [tracklet.observation_id for tracklet in tracklets if tracklet.observation_id]
    annotations_by_observation = _annotations_by_observation(session, observation_ids)

    filtered = [
        tracklet
        for tracklet in tracklets
        if _matches_python_filters(
            session=session,
            tracklet=tracklet,
            filters=filters,
            annotations=annotations_by_observation.get(tracklet.observation_id or "", []),
        )
    ]

    count = len(filtered)
    paged = filtered[filters.offset : filters.offset + filters.limit]
    rows = [
        _query_row(
            session=session,
            tracklet=tracklet,
            annotations=annotations_by_observation.get(tracklet.observation_id or "", []),
        )
        for tracklet in paged
    ]

    return TrackletQueryResponse(
        count=count,
        tracklets=rows,
        summary=_summary(filtered, annotations_by_observation),
    )


def _matches_python_filters(
    session: Session,
    tracklet: Tracklet,
    filters: TrackletQueryFilters,
    annotations: list[HumanAnnotation],
) -> bool:
    observation = _tracklet_observation(session, tracklet)
    metadata = tracklet.metadata_jsonb
    payload = observation.payload_jsonb if observation is not None else {}
    point_count = len(tracklet.points)
    gap_count = _int_value(payload.get("gap_count"), metadata.get("gap_count"))

    if filters.source_detection_run_id is not None:
        if metadata.get("source_detection_run_id") != filters.source_detection_run_id:
            return False
    if filters.track_status is not None:
        track_status = _text_value(payload.get("track_status"), metadata.get("track_status"))
        if track_status != filters.track_status:
            return False
    if filters.identity_status is not None:
        identity_status = _text_value(
            payload.get("identity_status"),
            metadata.get("identity_status"),
        )
        if identity_status != filters.identity_status:
            return False
    if filters.timestamp_start_gte is not None:
        if observation is None or observation.timestamp_start_ms is None:
            return False
        if observation.timestamp_start_ms < filters.timestamp_start_gte:
            return False
    if filters.timestamp_end_lte is not None:
        if observation is None or observation.timestamp_end_ms is None:
            return False
        if observation.timestamp_end_ms > filters.timestamp_end_lte:
            return False
    if filters.min_track_points is not None and point_count < filters.min_track_points:
        return False
    if filters.max_track_points is not None and point_count > filters.max_track_points:
        return False
    if filters.gap_count_gte is not None:
        if gap_count is None or gap_count < filters.gap_count_gte:
            return False
    if filters.gap_count_lte is not None:
        if gap_count is None or gap_count > filters.gap_count_lte:
            return False
    if filters.has_gaps is not None:
        has_gaps = (gap_count or 0) > 0
        if has_gaps != filters.has_gaps:
            return False
    label_filter = filters.review_label or filters.annotation_label
    if label_filter is not None:
        labels = {annotation_label(annotation) for annotation in annotations}
        if label_filter not in labels:
            return False
    if filters.has_annotation is not None:
        if bool(annotations) != filters.has_annotation:
            return False
    return True


def _query_row(
    session: Session,
    tracklet: Tracklet,
    annotations: list[HumanAnnotation],
) -> TrackletQueryRow:
    observation = _tracklet_observation(session, tracklet)
    metadata = tracklet.metadata_jsonb
    payload = observation.payload_jsonb if observation is not None else {}
    return TrackletQueryRow(
        tracklet=_tracklet_payload(tracklet),
        observation=_observation_payload(observation) if observation is not None else None,
        run_id=tracklet.run_id,
        source_detection_run_id=_text_value(metadata.get("source_detection_run_id")),
        media_id=tracklet.media_id,
        frame_start=tracklet.frame_start,
        frame_end=tracklet.frame_end,
        timestamp_start_ms=observation.timestamp_start_ms if observation is not None else None,
        timestamp_end_ms=observation.timestamp_end_ms if observation is not None else None,
        track_family=tracklet.track_family,
        subject_ref=tracklet.subject_ref,
        confidence=tracklet.confidence,
        track_point_count=len(tracklet.points),
        gap_count=_int_value(payload.get("gap_count"), metadata.get("gap_count")),
        annotation_summary=AnnotationSummary(**summarize_annotations(annotations)),
        evidence_bundle_url=f"/tracklets/{tracklet.id}/evidence-bundle",
    )


def _summary(
    tracklets: list[Tracklet],
    annotations_by_observation: dict[str, list[HumanAnnotation]],
) -> dict[str, Any]:
    return {
        "count": len(tracklets),
        "by_track_family": dict(sorted(Counter(row.track_family for row in tracklets).items())),
        "by_subject_ref": dict(
            sorted(Counter(row.subject_ref or "unknown" for row in tracklets).items())
        ),
        "by_annotation_label": _annotation_label_counts(tracklets, annotations_by_observation),
        "by_gap_state": dict(
            sorted(
                Counter(
                    "has_gaps" if _tracklet_gap_count(row) > 0 else "no_gaps"
                    for row in tracklets
                ).items()
            )
        ),
    }


def _annotation_label_counts(
    tracklets: list[Tracklet],
    annotations_by_observation: dict[str, list[HumanAnnotation]],
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for tracklet in tracklets:
        for annotation in annotations_by_observation.get(tracklet.observation_id or "", []):
            counts[annotation_label(annotation)] += 1
    return dict(sorted(counts.items()))


def _annotations_by_observation(
    session: Session,
    observation_ids: list[str],
) -> dict[str, list[HumanAnnotation]]:
    if not observation_ids:
        return {}
    rows = session.scalars(
        select(HumanAnnotation)
        .where(HumanAnnotation.observation_id.in_(observation_ids))
        .order_by(HumanAnnotation.created_at)
    ).all()
    grouped: dict[str, list[HumanAnnotation]] = {
        observation_id: [] for observation_id in observation_ids
    }
    for row in rows:
        if row.observation_id is not None:
            grouped.setdefault(row.observation_id, []).append(row)
    return grouped


def _tracklet_observation(session: Session, tracklet: Tracklet) -> Observation | None:
    if tracklet.observation_id is None:
        return None
    return session.get(Observation, tracklet.observation_id)


def _tracklet_gap_count(tracklet: Tracklet) -> int:
    return _int_value(tracklet.metadata_jsonb.get("gap_count")) or 0


def _text_value(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return None


def _int_value(*values: Any) -> int | None:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
    return None
