from datetime import datetime
from typing import Any

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel


class HumanAnnotationCreate(TOMBaseModel):
    media_id: str | None = None
    observation_id: str | None = None
    evidence_artifact_id: str | None = None
    frame_start: int | None = None
    frame_end: int | None = None
    timestamp_start_ms: int | None = None
    timestamp_end_ms: int | None = None
    annotation_type: str
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)
    created_by: str | None = None


class HumanAnnotationRead(HumanAnnotationCreate):
    id: str
    media_id: str
    created_at: datetime
