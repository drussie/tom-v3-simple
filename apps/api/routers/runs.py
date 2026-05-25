from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.runs import (
    ProcessingRunCreate,
    ProcessingRunRead,
    ProcessingStepCreate,
    ProcessingStepRead,
)
from tom_v3_storage.db_models import MediaAsset, ProcessingRun, ProcessingStep

from apps.api.db import get_session

router = APIRouter(tags=["runs"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(
    "/media/{media_id}/runs",
    response_model=ProcessingRunRead,
    status_code=status.HTTP_201_CREATED,
)
def create_run(
    media_id: str, request: ProcessingRunCreate, session: SessionDep
) -> ProcessingRun:
    if session.get(MediaAsset, media_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="media asset not found")
    run = ProcessingRun(media_id=media_id, **request.model_dump())
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


@router.get("/runs/{run_id}", response_model=ProcessingRunRead)
def get_run(run_id: str, session: SessionDep) -> ProcessingRun:
    run = session.get(ProcessingRun, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="run not found")
    return run


@router.post(
    "/runs/{run_id}/steps",
    response_model=ProcessingStepRead,
    status_code=status.HTTP_201_CREATED,
)
def create_step(
    run_id: str, request: ProcessingStepCreate, session: SessionDep
) -> ProcessingStep:
    if session.get(ProcessingRun, run_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="run not found")
    step = ProcessingStep(run_id=run_id, **request.model_dump())
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


@router.get("/runs/{run_id}/steps", response_model=list[ProcessingStepRead])
def list_steps(run_id: str, session: SessionDep) -> list[ProcessingStep]:
    if session.get(ProcessingRun, run_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="run not found")
    return list(
        session.scalars(select(ProcessingStep).where(ProcessingStep.run_id == run_id)).all()
    )
