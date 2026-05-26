from typing import Any, Literal

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel
from tom_v3_schema.tracklets import TrackletQueryFilters


class TrackletReviewDatasetExportRequest(TOMBaseModel):
    tracklet_ids: list[str] = Field(default_factory=list)
    query: TrackletQueryFilters | None = None
    include_frame_artifacts: bool = True
    include_annotations: bool = True
    format: Literal["json"] = "json"
    output_root: str = ".data/exports"
    query_name: str | None = None
    created_by: str | None = "tom-v3-worker"

    @model_validator(mode="after")
    def validate_selection(self) -> "TrackletReviewDatasetExportRequest":
        if not self.tracklet_ids and self.query is None:
            raise ValueError("tracklet_ids or query is required")
        return self


class TrackletReviewDatasetExportResponse(TOMBaseModel):
    export_id: str
    artifact_id: str
    uri: str
    path: str
    checksum: str
    tracklet_count: int
    tracklet_ids: list[str]
    query_result_id: str | None = None
    warnings: dict[str, bool]
    metadata: dict[str, Any] = Field(default_factory=dict)
