from datetime import datetime
from typing import Any

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel
from tom_v3_schema.enums import MediaType


class MediaAssetCreate(TOMBaseModel):
    source_uri: str
    media_type: MediaType = MediaType.video
    duration_ms: int | None = None
    frame_count: int | None = None
    fps: float | None = None
    width: int | None = None
    height: int | None = None
    checksum: str | None = None
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)


class MediaAssetRead(MediaAssetCreate):
    id: str
    created_at: datetime
