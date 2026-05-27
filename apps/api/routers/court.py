from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from tom_v3_schema.court import (
    CameraViewEvidenceSummary,
    CameraViewQueryFilters,
    CameraViewQueryResponse,
)

from apps.api.db import get_session
from apps.api.services.camera_view_evidence import (
    CameraViewEvidenceError,
    build_camera_view_evidence_bundle,
    query_camera_view_observations,
    summarize_camera_view_evidence,
)

router = APIRouter(prefix="/court", tags=["court"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/camera-view", response_model=CameraViewQueryResponse)
def get_camera_view_observations(
    session: SessionDep,
    media_id: str,
    run_id: str | None = None,
    start_ms: int | None = None,
    end_ms: int | None = None,
    frame_start: int | None = None,
    frame_end: int | None = None,
    view_label: str | None = None,
    camera_motion_hint: str | None = None,
    min_view_confidence: float | None = None,
    limit: int = 100,
    offset: int = 0,
) -> CameraViewQueryResponse:
    try:
        filters = _filters(
            media_id=media_id,
            run_id=run_id,
            start_ms=start_ms,
            end_ms=end_ms,
            frame_start=frame_start,
            frame_end=frame_end,
            view_label=view_label,
            camera_motion_hint=camera_motion_hint,
            min_view_confidence=min_view_confidence,
            limit=limit,
            offset=offset,
        )
        return query_camera_view_observations(session, filters)
    except CameraViewEvidenceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.get("/camera-view/summary", response_model=CameraViewEvidenceSummary)
def get_camera_view_summary(
    session: SessionDep,
    media_id: str,
    run_id: str | None = None,
    start_ms: int | None = None,
    end_ms: int | None = None,
    frame_start: int | None = None,
    frame_end: int | None = None,
    view_label: str | None = None,
    camera_motion_hint: str | None = None,
    min_view_confidence: float | None = None,
) -> CameraViewEvidenceSummary:
    try:
        filters = _filters(
            media_id=media_id,
            run_id=run_id,
            start_ms=start_ms,
            end_ms=end_ms,
            frame_start=frame_start,
            frame_end=frame_end,
            view_label=view_label,
            camera_motion_hint=camera_motion_hint,
            min_view_confidence=min_view_confidence,
            limit=500,
            offset=0,
        )
        return summarize_camera_view_evidence(session, filters)
    except CameraViewEvidenceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.get("/camera-view/{observation_id}/bundle")
def get_camera_view_bundle(
    observation_id: str,
    session: SessionDep,
) -> dict[str, Any]:
    try:
        payload = build_camera_view_evidence_bundle(session, observation_id)
    except CameraViewEvidenceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    if payload is None:
        raise HTTPException(status_code=404, detail="camera view observation not found")
    return payload


def _filters(**kwargs: Any) -> CameraViewQueryFilters:
    try:
        return CameraViewQueryFilters(**kwargs)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
