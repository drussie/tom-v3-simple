from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.tracklets import TrackletQueryFilters, TrackletQueryResponse

from apps.api.db import get_session
from apps.api.services.tracklet_evidence_bundle import build_tracklet_evidence_bundle
from apps.api.services.tracklet_query import query_tracklets

router = APIRouter(prefix="/tracklets", tags=["tracklets"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/query", response_model=TrackletQueryResponse)
def query_tracklet_candidates(
    request: TrackletQueryFilters,
    session: SessionDep,
) -> TrackletQueryResponse:
    return query_tracklets(session, request)


@router.get("/{tracklet_id}/evidence-bundle")
def get_tracklet_evidence_bundle(
    tracklet_id: str,
    session: SessionDep,
) -> dict[str, Any]:
    payload = build_tracklet_evidence_bundle(session, tracklet_id)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tracklet not found")
    return payload
