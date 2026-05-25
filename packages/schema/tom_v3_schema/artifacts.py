from datetime import datetime
from typing import Any

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel


class EvidenceArtifactCreate(TOMBaseModel):
    media_id: str | None = None
    run_id: str | None = None
    target_observation_id: str | None = None
    artifact_type: str
    uri: str
    frame_start: int | None = None
    frame_end: int | None = None
    timestamp_start_ms: int | None = None
    timestamp_end_ms: int | None = None
    checksum: str | None = None
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)


class EvidenceArtifactRead(EvidenceArtifactCreate):
    id: str
    media_id: str
    run_id: str | None = None
    created_at: datetime
