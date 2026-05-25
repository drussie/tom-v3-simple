from sqlalchemy import false, func, select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import get_observation_detail
from tom_v3_schema.observations import ObservationQueryFilters, ObservationQueryResponse
from tom_v3_storage.db_models import GameplayObservation, Observation, Tracklet, TrackPoint


def query_observations(
    session: Session, filters: ObservationQueryFilters
) -> ObservationQueryResponse:
    stmt = select(Observation)

    if filters.media_id:
        stmt = stmt.where(Observation.media_id == filters.media_id)
    if filters.run_id:
        stmt = stmt.where(Observation.run_id == filters.run_id)
    if filters.observation_family:
        stmt = stmt.where(Observation.observation_family == filters.observation_family)
    if filters.observation_type:
        stmt = stmt.where(Observation.observation_type == filters.observation_type)
    if filters.frame_start_gte is not None:
        stmt = stmt.where(Observation.frame_start >= filters.frame_start_gte)
    if filters.frame_end_lte is not None:
        stmt = stmt.where(Observation.frame_end <= filters.frame_end_lte)
    if filters.timestamp_start_gte is not None:
        stmt = stmt.where(Observation.timestamp_start_ms >= filters.timestamp_start_gte)
    if filters.timestamp_end_lte is not None:
        stmt = stmt.where(Observation.timestamp_end_ms <= filters.timestamp_end_lte)
    if filters.confidence_gte is not None:
        stmt = stmt.where(Observation.confidence >= filters.confidence_gte)
    if filters.confidence_lte is not None:
        stmt = stmt.where(Observation.confidence <= filters.confidence_lte)
    if filters.gameplay_label is not None:
        gameplay_label = getattr(filters.gameplay_label, "value", filters.gameplay_label)
        stmt = stmt.join(GameplayObservation).where(
            GameplayObservation.view_state == gameplay_label
        )
    if filters.tracklet_id is not None:
        observation_ids = _observation_ids_for_tracklet(session, filters.tracklet_id)
        if observation_ids:
            stmt = stmt.where(Observation.id.in_(observation_ids))
        else:
            stmt = stmt.where(false())

    count_stmt = select(func.count()).select_from(stmt.subquery())
    count = session.scalar(count_stmt) or 0
    rows = session.scalars(
        stmt.order_by(Observation.frame_start, Observation.created_at)
        .offset(filters.offset)
        .limit(filters.limit)
    ).all()
    details = [get_observation_detail(session, row.id) for row in rows]
    return ObservationQueryResponse(
        count=count,
        observations=[detail for detail in details if detail is not None],
    )


def _observation_ids_for_tracklet(session: Session, tracklet_id: str) -> list[str]:
    ids: list[str] = []
    tracklet = session.get(Tracklet, tracklet_id)
    if tracklet and tracklet.observation_id:
        ids.append(tracklet.observation_id)

    point_ids = session.scalars(
        select(TrackPoint.observation_id).where(TrackPoint.tracklet_id == tracklet_id)
    ).all()
    ids.extend([observation_id for observation_id in point_ids if observation_id])
    return sorted(set(ids))
