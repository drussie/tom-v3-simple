from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.observations import ObservationLineageRead, ObservationLineageResponse
from tom_v3_storage.db_models import ObservationLineage


def lineage_read_from_model(lineage: ObservationLineage) -> ObservationLineageRead:
    return ObservationLineageRead.model_validate(lineage)


def get_lineage_for_observation(
    session: Session, observation_id: str
) -> ObservationLineageResponse:
    parent_rows = session.scalars(
        select(ObservationLineage).where(ObservationLineage.child_observation_id == observation_id)
    ).all()
    child_rows = session.scalars(
        select(ObservationLineage).where(ObservationLineage.parent_observation_id == observation_id)
    ).all()
    return ObservationLineageResponse(
        parents=[lineage_read_from_model(row) for row in parent_rows],
        children=[lineage_read_from_model(row) for row in child_rows],
    )
