from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.lineage import get_lineage_for_observation
from tom_v3_observations.writer import get_observation_detail
from tom_v3_schema.annotations import HumanAnnotationRead
from tom_v3_schema.artifacts import EvidenceArtifactRead
from tom_v3_schema.observations import (
    ObservationBatchCreate,
    ObservationBatchRead,
    ObservationCreate,
    ObservationDetailRead,
    ObservationLineageResponse,
    ObservationQueryFilters,
    ObservationQueryResponse,
)
from tom_v3_storage.db_models import EvidenceArtifact, HumanAnnotation, Observation

from apps.api.db import get_session
from apps.api.services.observation_writer import ObservationWriter, ObservationWriterError
from apps.api.services.query_builder import query_observations

router = APIRouter(tags=["observations"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(
    "/observations",
    response_model=ObservationDetailRead,
    status_code=status.HTTP_201_CREATED,
)
def create_observation(
    request: ObservationCreate, session: SessionDep
) -> ObservationDetailRead:
    try:
        return ObservationWriter(session).write(request)
    except ObservationWriterError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post(
    "/observations/batch",
    response_model=ObservationBatchRead,
    status_code=status.HTTP_201_CREATED,
)
def create_observations_batch(
    request: ObservationBatchCreate, session: SessionDep
) -> ObservationBatchRead:
    try:
        observations = ObservationWriter(session).write_many(request.observations)
    except ObservationWriterError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return ObservationBatchRead(observations=observations)


@router.post("/observations/query", response_model=ObservationQueryResponse)
def query_observations_route(
    request: ObservationQueryFilters, session: SessionDep
) -> ObservationQueryResponse:
    return query_observations(session, request)


@router.get("/observations/{observation_id}", response_model=ObservationDetailRead)
def get_observation(
    observation_id: str, session: SessionDep
) -> ObservationDetailRead:
    detail = get_observation_detail(session, observation_id)
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="observation not found")
    return detail


@router.get(
    "/observations/{observation_id}/lineage",
    response_model=ObservationLineageResponse,
)
def get_observation_lineage(
    observation_id: str, session: SessionDep
) -> ObservationLineageResponse:
    if session.get(Observation, observation_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="observation not found")
    return get_lineage_for_observation(session, observation_id)


@router.get(
    "/observations/{observation_id}/artifacts",
    response_model=list[EvidenceArtifactRead],
)
def list_observation_artifacts(
    observation_id: str, session: SessionDep
) -> list[EvidenceArtifact]:
    if session.get(Observation, observation_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="observation not found")
    return list(
        session.scalars(
            select(EvidenceArtifact).where(
                EvidenceArtifact.target_observation_id == observation_id
            )
        ).all()
    )


@router.get(
    "/observations/{observation_id}/annotations",
    response_model=list[HumanAnnotationRead],
)
def list_observation_annotations(
    observation_id: str, session: SessionDep
) -> list[HumanAnnotation]:
    if session.get(Observation, observation_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="observation not found")
    return list(
        session.scalars(
            select(HumanAnnotation).where(HumanAnnotation.observation_id == observation_id)
        ).all()
    )
