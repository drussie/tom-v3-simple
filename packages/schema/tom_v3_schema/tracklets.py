from typing import Any

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel


class TrackletQueryFilters(TOMBaseModel):
    media_id: str | None = None
    tracklet_run_id: str | None = None
    source_detection_run_id: str | None = None
    track_family: str | None = None
    subject_ref: str | None = None
    track_status: str | None = "candidate"
    identity_status: str | None = "unverified"
    frame_start_gte: int | None = None
    frame_end_lte: int | None = None
    timestamp_start_gte: int | None = None
    timestamp_end_lte: int | None = None
    confidence_gte: float | None = None
    confidence_lte: float | None = None
    min_track_points: int | None = None
    max_track_points: int | None = None
    gap_count_gte: int | None = None
    gap_count_lte: int | None = None
    has_gaps: bool | None = None
    review_label: str | None = None
    has_annotation: bool | None = None
    annotation_label: str | None = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class AnnotationSummary(TOMBaseModel):
    count: int
    labels: dict[str, int] = Field(default_factory=dict)
    latest_created_at: str | None = None


class TrackletQueryRow(TOMBaseModel):
    tracklet: dict[str, Any]
    observation: dict[str, Any] | None
    run_id: str
    source_detection_run_id: str | None
    media_id: str
    frame_start: int | None
    frame_end: int | None
    timestamp_start_ms: int | None
    timestamp_end_ms: int | None
    track_family: str
    subject_ref: str | None
    confidence: float | None
    track_point_count: int
    gap_count: int | None
    annotation_summary: AnnotationSummary
    evidence_bundle_url: str


class TrackletQueryResponse(TOMBaseModel):
    count: int
    tracklets: list[TrackletQueryRow]
    summary: dict[str, Any]
