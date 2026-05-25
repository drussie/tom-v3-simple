from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tom_v3_schema.runs import (
    ModelRegistryCreate,
    ModelRegistryRead,
    RuntimeConfigCreate,
    RuntimeConfigRead,
)
from tom_v3_storage.db_models import ModelRegistry, RuntimeConfig

from apps.api.db import get_session

router = APIRouter(tags=["registry"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/models", response_model=ModelRegistryRead, status_code=status.HTTP_201_CREATED)
def create_model(
    request: ModelRegistryCreate, session: SessionDep
) -> ModelRegistry:
    model = ModelRegistry(**request.model_dump())
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@router.get("/models/{model_id}", response_model=ModelRegistryRead)
def get_model(model_id: str, session: SessionDep) -> ModelRegistry:
    model = session.get(ModelRegistry, model_id)
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    return model


@router.post(
    "/runtime-configs",
    response_model=RuntimeConfigRead,
    status_code=status.HTTP_201_CREATED,
)
def create_runtime_config(
    request: RuntimeConfigCreate, session: SessionDep
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(**request.model_dump())
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


@router.get("/runtime-configs/{runtime_config_id}", response_model=RuntimeConfigRead)
def get_runtime_config(
    runtime_config_id: str, session: SessionDep
) -> RuntimeConfig:
    runtime_config = session.get(RuntimeConfig, runtime_config_id)
    if runtime_config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="runtime config not found"
        )
    return runtime_config
