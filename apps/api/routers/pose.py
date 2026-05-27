from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.exports import (
    PoseReviewDatasetExportRequest,
    PoseReviewDatasetExportResponse,
)
from tom_v3_schema.pose import PoseQueryFilters, PoseQueryResponse

from apps.api.db import get_session
from apps.api.services.pose_evidence_bundle import get_pose_evidence_bundle
from apps.api.services.pose_query import query_poses
from apps.api.services.pose_review_export import (
    PoseReviewExportError,
    export_pose_review_dataset,
)

router = APIRouter(tags=["pose"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/pose/query", response_model=PoseQueryResponse)
def query_pose_observations(
    request: PoseQueryFilters,
    session: SessionDep,
) -> PoseQueryResponse:
    return query_poses(session, request)


@router.get("/pose-observations/{pose_observation_id}/evidence-bundle")
def get_pose_observation_evidence_bundle(
    pose_observation_id: str,
    session: SessionDep,
) -> dict[str, Any]:
    payload = get_pose_evidence_bundle(session, pose_observation_id)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="pose observation not found",
        )
    return payload


@router.post("/pose/export-review-dataset", response_model=PoseReviewDatasetExportResponse)
def export_pose_review_dataset_endpoint(
    request: PoseReviewDatasetExportRequest,
    session: SessionDep,
) -> PoseReviewDatasetExportResponse:
    try:
        return export_pose_review_dataset(session, request)
    except PoseReviewExportError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
