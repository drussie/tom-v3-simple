from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.exports import (
    TrackletReviewDatasetExportRequest,
    TrackletReviewDatasetExportResponse,
)
from tom_v3_schema.tracklets import TrackletQueryFilters, TrackletQueryResponse

from apps.api.db import get_session
from apps.api.services.tracklet_evidence_bundle import build_tracklet_evidence_bundle
from apps.api.services.tracklet_query import query_tracklets
from apps.api.services.tracklet_review_export import (
    TrackletReviewExportError,
    export_tracklet_review_dataset,
)

router = APIRouter(prefix="/tracklets", tags=["tracklets"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/query", response_model=TrackletQueryResponse)
def query_tracklet_candidates(
    request: TrackletQueryFilters,
    session: SessionDep,
) -> TrackletQueryResponse:
    return query_tracklets(session, request)


@router.post("/export-review-dataset", response_model=TrackletReviewDatasetExportResponse)
def export_tracklet_review_dataset_endpoint(
    request: TrackletReviewDatasetExportRequest,
    session: SessionDep,
) -> TrackletReviewDatasetExportResponse:
    try:
        return export_tracklet_review_dataset(session, request)
    except TrackletReviewExportError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{tracklet_id}/evidence-bundle")
def get_tracklet_evidence_bundle(
    tracklet_id: str,
    session: SessionDep,
) -> dict[str, Any]:
    payload = build_tracklet_evidence_bundle(session, tracklet_id)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tracklet not found")
    return payload
