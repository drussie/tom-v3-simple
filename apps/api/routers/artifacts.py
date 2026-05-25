from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.artifacts import EvidenceArtifactCreate, EvidenceArtifactRead
from tom_v3_storage.db_models import EvidenceArtifact, Observation

from apps.api.db import get_session

router = APIRouter(tags=["artifacts"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(
    "/artifacts",
    response_model=EvidenceArtifactRead,
    status_code=status.HTTP_201_CREATED,
)
def create_artifact(
    request: EvidenceArtifactCreate, session: SessionDep
) -> EvidenceArtifact:
    payload = request.model_dump()
    if payload["media_id"] is None and payload["target_observation_id"] is not None:
        observation = session.get(Observation, payload["target_observation_id"])
        if observation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="observation not found",
            )
        payload["media_id"] = observation.media_id
        payload["run_id"] = payload["run_id"] or observation.run_id
    if payload["media_id"] is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="media_id is required")
    artifact = EvidenceArtifact(**payload)
    session.add(artifact)
    session.commit()
    session.refresh(artifact)
    return artifact


@router.get("/artifacts/{artifact_id}", response_model=EvidenceArtifactRead)
def get_artifact(artifact_id: str, session: SessionDep) -> EvidenceArtifact:
    artifact = session.get(EvidenceArtifact, artifact_id)
    if artifact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="artifact not found")
    return artifact
