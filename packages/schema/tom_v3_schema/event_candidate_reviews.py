from datetime import datetime
from typing import Any, Literal

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel

EventCandidateReviewKind = Literal[
    "candidate_marker_review",
    "point_moment_review",
    "missing_candidate_note",
]

CandidateMarkerReviewLabel = Literal["useful", "wrong", "unclear", "needs_review"]
MissingCandidateReviewLabel = Literal[
    "missing_hit_candidate",
    "missing_bounce_candidate",
    "missing_event_candidate",
]


class EventCandidateReviewCreate(TOMBaseModel):
    event_candidate_run_id: str
    observation_id: str | None = None
    annotation_kind: EventCandidateReviewKind
    review_label: str
    candidate_type: str | None = None
    frame: int | None = None
    timestamp_ms: int | None = None
    image_x: float | None = None
    image_y: float | None = None
    court_x: float | None = None
    court_y: float | None = None
    note: str | None = None
    reviewer: str | None = None
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class EventCandidateReviewUpdate(TOMBaseModel):
    review_label: str | None = None
    note: str | None = None
    reviewer: str | None = None
    payload_jsonb: dict[str, Any] | None = None


class EventCandidateReviewRead(TOMBaseModel):
    id: str
    media_id: str
    event_candidate_run_id: str
    observation_id: str | None = None
    annotation_kind: str
    review_label: str
    candidate_type: str | None = None
    frame: int | None = None
    timestamp_ms: int | None = None
    image_x: float | None = None
    image_y: float | None = None
    court_x: float | None = None
    court_y: float | None = None
    note: str | None = None
    reviewer: str | None = None
    created_at: datetime
    updated_at: datetime
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class EventCandidateReviewList(TOMBaseModel):
    reviews: list[EventCandidateReviewRead]
    reviews_by_observation_id: dict[str, list[EventCandidateReviewRead]]
    review_summary: dict[str, int]
    warnings: dict[str, bool]
