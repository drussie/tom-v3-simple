from datetime import datetime
from typing import Any

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel
from tom_v3_schema.enums import ModelFamily, RunStatus, StepStatus


class ModelRegistryCreate(TOMBaseModel):
    name: str
    version: str
    model_family: ModelFamily
    source: str | None = None
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)


class ModelRegistryRead(ModelRegistryCreate):
    id: str
    created_at: datetime


class RuntimeConfigCreate(TOMBaseModel):
    config_name: str
    config_version: str = "v0"
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class RuntimeConfigRead(RuntimeConfigCreate):
    id: str
    created_at: datetime


class ProcessingRunCreate(TOMBaseModel):
    run_name: str
    run_status: RunStatus = RunStatus.queued
    runtime_config_id: str | None = None
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)


class ProcessingRunRead(ProcessingRunCreate):
    id: str
    media_id: str
    started_at: datetime | None = None
    completed_at: datetime | None = None


class ProcessingStepCreate(TOMBaseModel):
    step_name: str
    step_status: StepStatus = StepStatus.queued
    runtime_config_id: str | None = None
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)


class ProcessingStepRead(ProcessingStepCreate):
    id: str
    run_id: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
