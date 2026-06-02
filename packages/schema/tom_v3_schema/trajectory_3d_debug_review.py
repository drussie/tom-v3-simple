from datetime import datetime
from typing import Any, Literal

from pydantic import Field

from tom_v3_schema.base import TOMBaseModel

Trajectory3DDebugAnnotationKind = Literal[
    "trajectory_3d_sample_review",
    "event_candidate_3d_diagnostic_review",
    "missing_3d_sample_note",
    "debug_view_note",
]

Trajectory3DDebugReviewLabel = Literal[
    "useful",
    "wrong",
    "unclear",
    "needs_review",
    "missing_3d_sample",
    "bad_3d_position",
    "bad_diagnostic_link",
]


class Trajectory3DDebugReviewAnnotationCreate(TOMBaseModel):
    trajectory_3d_run_id: str | None = None
    camera_geometry_id: str | None = None
    event_candidate_run_id: str | None = None
    event_observation_id: str | None = None
    trajectory_3d_candidate_id: str | None = None
    event_candidate_3d_diagnostic_id: str | None = None
    annotation_kind: Trajectory3DDebugAnnotationKind
    review_label: str
    frame: int | None = None
    timestamp_ms: int | None = None
    image_x: float | None = None
    image_y: float | None = None
    court_x_m: float | None = None
    court_y_m: float | None = None
    court_z_m: float | None = None
    note: str | None = None
    reviewer: str | None = None
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class Trajectory3DDebugReviewAnnotationUpdate(TOMBaseModel):
    review_label: str | None = None
    note: str | None = None
    reviewer: str | None = None
    payload_jsonb: dict[str, Any] | None = None


class Trajectory3DDebugReviewAnnotationRead(TOMBaseModel):
    id: str
    media_id: str
    trajectory_3d_run_id: str | None = None
    camera_geometry_id: str | None = None
    event_candidate_run_id: str | None = None
    event_observation_id: str | None = None
    trajectory_3d_candidate_id: str | None = None
    event_candidate_3d_diagnostic_id: str | None = None
    annotation_kind: str
    review_label: str
    frame: int | None = None
    timestamp_ms: int | None = None
    image_x: float | None = None
    image_y: float | None = None
    court_x_m: float | None = None
    court_y_m: float | None = None
    court_z_m: float | None = None
    note: str | None = None
    reviewer: str | None = None
    created_at: datetime
    updated_at: datetime
    payload_jsonb: dict[str, Any] = Field(default_factory=dict)


class Trajectory3DDebugReviewSummary(TOMBaseModel):
    available: bool
    total_reviews: int
    sample_reviews: int = 0
    diagnostic_reviews: int = 0
    missing_3d_sample_notes: int = 0
    debug_view_notes: int = 0
    useful: int = 0
    wrong: int = 0
    unclear: int = 0
    needs_review: int = 0
    missing_3d_sample: int = 0
    bad_3d_position: int = 0
    bad_diagnostic_link: int = 0
    review_metadata_only: bool = True
    not_truth: bool = True
    not_3d_truth: bool = True
    does_not_change_event_candidates: bool = True
    does_not_change_3d_candidates: bool = True
    does_not_create_in_out: bool = True
    does_not_create_score: bool = True
    no_adjudication: bool = True


class Trajectory3DDebugReviewList(TOMBaseModel):
    reviews: list[Trajectory3DDebugReviewAnnotationRead]
    reviews_by_trajectory_3d_candidate_id: dict[
        str, list[Trajectory3DDebugReviewAnnotationRead]
    ]
    reviews_by_event_candidate_3d_diagnostic_id: dict[
        str, list[Trajectory3DDebugReviewAnnotationRead]
    ]
    review_summary: Trajectory3DDebugReviewSummary
    warnings: dict[str, bool]
