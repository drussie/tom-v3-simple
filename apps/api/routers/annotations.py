from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.annotations import HumanAnnotationCreate, HumanAnnotationRead
from tom_v3_storage.db_models import EvidenceArtifact, HumanAnnotation, Observation

from apps.api.db import get_session

router = APIRouter(tags=["annotations"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(
    "/annotations",
    response_model=HumanAnnotationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_annotation(
    request: HumanAnnotationCreate, session: SessionDep
) -> HumanAnnotation:
    payload = request.model_dump()
    if payload["media_id"] is None and payload["observation_id"] is not None:
        observation = session.get(Observation, payload["observation_id"])
        if observation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="observation not found",
            )
        payload["media_id"] = observation.media_id
    if payload["media_id"] is None and payload["evidence_artifact_id"] is not None:
        artifact = session.get(EvidenceArtifact, payload["evidence_artifact_id"])
        if artifact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="artifact not found")
        payload["media_id"] = artifact.media_id
    if payload["media_id"] is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="media_id is required")

    annotation = HumanAnnotation(**payload)
    session.add(annotation)
    session.commit()
    session.refresh(annotation)
    return annotation
