from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tom_v3_observations.synthetic import create_synthetic_run

from apps.api.db import get_session

router = APIRouter(prefix="/dev", tags=["dev"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/synthetic-run")
def create_dev_synthetic_run(session: SessionDep) -> dict[str, object]:
    """Dev-only endpoint for proving backend persistence without real model integration."""
    return create_synthetic_run(session)
