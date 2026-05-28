from typing import Any, Literal

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel
from tom_v3_schema.pose import PoseQueryFilters
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


class PoseReviewDatasetExportRequest(TOMBaseModel):
    pose_observation_ids: list[str] = Field(default_factory=list)
    query: PoseQueryFilters | None = None
    run_id: str | None = None
    media_id: str | None = None
    include_annotations: bool = True
    include_artifacts: bool = True
    format: Literal["json"] = "json"
    output_root: str = ".data/exports"
    query_name: str | None = None
    created_by: str | None = "tom-v3-worker"

    @model_validator(mode="after")
    def validate_selection(self) -> "PoseReviewDatasetExportRequest":
        if not any((self.pose_observation_ids, self.query, self.run_id, self.media_id)):
            raise ValueError("pose_observation_ids, query, run_id, or media_id is required")
        return self


class PoseReviewDatasetExportResponse(TOMBaseModel):
    export_id: str
    artifact_id: str
    uri: str
    path: str
    checksum: str
    pose_count: int
    pose_observation_ids: list[str]
    query_result_id: str | None = None
    warnings: dict[str, bool]
    metadata: dict[str, Any] = Field(default_factory=dict)


class CourtReviewDatasetExportRequest(TOMBaseModel):
    media_id: str
    court_run_id: str | None = None
    homography_run_id: str | None = None
    projection_diagnostic_run_id: str | None = None
    include_annotations: bool = True
    include_artifacts: bool = True
    format: Literal["json"] = "json"
    output_root: str = ".data/exports"
    query_name: str | None = None
    created_by: str | None = "tom-v3-worker"

    @model_validator(mode="after")
    def validate_selection(self) -> "CourtReviewDatasetExportRequest":
        if not any(
            (
                self.court_run_id,
                self.homography_run_id,
                self.projection_diagnostic_run_id,
            )
        ):
            raise ValueError(
                "court_run_id, homography_run_id, or projection_diagnostic_run_id is required"
            )
        return self


class CourtReviewDatasetExportResponse(TOMBaseModel):
    export_id: str
    artifact_id: str
    uri: str
    path: str
    checksum: str
    media_id: str
    court_run_id: str | None = None
    homography_run_id: str | None = None
    projection_diagnostic_run_id: str | None = None
    court_keypoint_count: int
    court_line_count: int
    camera_view_count: int
    homography_candidate_count: int
    projection_diagnostic_count: int
    observation_ids: list[str]
    query_result_id: str | None = None
    warnings: dict[str, bool]
    metadata: dict[str, Any] = Field(default_factory=dict)
