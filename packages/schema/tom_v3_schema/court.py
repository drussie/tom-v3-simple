from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel

COURT_KEYPOINT_SCHEMA = "tennis_court_v0"
COURT_KEYPOINT_SCHEMA_VERSION = "v0"
COURT_TEMPLATE_NAME = "tennis_court_template_normalized_v0"
COURT_TEMPLATE_VERSION = "v0"
COURT_TEMPLATE_COORDINATE_SPACE = "court_template_2d"

COURT_KEYPOINT_NAMES = [
    "near_left_baseline_corner",
    "near_right_baseline_corner",
    "far_left_baseline_corner",
    "far_right_baseline_corner",
    "left_net_post",
    "right_net_post",
    "service_line_t_near_left",
    "service_line_t_near_right",
    "service_line_t_far_left",
    "service_line_t_far_right",
    "center_mark_near",
    "center_mark_far",
]

COURT_LINE_CLASSES = [
    "baseline_near",
    "baseline_far",
    "sideline_left",
    "sideline_right",
    "service_line_near",
    "service_line_far",
    "center_service_line",
    "net_line",
    "unknown_court_line",
]

COURT_VISIBILITY_VALUES = [
    "visible",
    "partial",
    "occluded",
    "inferred_by_adapter",
    "unknown",
]

CAMERA_VIEW_LABELS = [
    "broadcast_hardcam",
    "behind_baseline",
    "side_view",
    "closeup",
    "replay_overlay",
    "non_gameplay",
    "unknown",
]

CAMERA_MOTION_HINTS = [
    "stable",
    "panning",
    "zooming",
    "camera_cut",
    "unknown",
]

HOMOGRAPHY_CANDIDATE_STATUSES = [
    "candidate",
    "insufficient_source_evidence",
    "adapter_failed",
    "not_computed",
]

PROJECTION_DIAGNOSTIC_STATUSES = [
    "diagnostic_candidate",
    "insufficient_homography",
    "adapter_failed",
    "not_computed",
]

HOMOGRAPHY_MATRIX_DIRECTIONS = [
    "image_pixels_to_court_template_2d",
    "court_template_2d_to_image_pixels",
]


class CourtSchemaError(ValueError):
    pass


class CourtTemplateKeypoint(TOMBaseModel):
    name: str
    x: float
    y: float


class CourtTemplateLine(TOMBaseModel):
    line_class: str
    start_keypoint: str
    end_keypoint: str


class CourtTemplate(TOMBaseModel):
    template_name: str
    template_version: str
    target_coordinate_space: str
    keypoints: list[CourtTemplateKeypoint]
    lines: list[CourtTemplateLine]
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    def as_schema_json(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


TENNIS_COURT_TEMPLATE_NORMALIZED_V0 = CourtTemplate(
    template_name=COURT_TEMPLATE_NAME,
    template_version=COURT_TEMPLATE_VERSION,
    target_coordinate_space=COURT_TEMPLATE_COORDINATE_SPACE,
    keypoints=[
        CourtTemplateKeypoint(name="near_left_baseline_corner", x=0.0, y=0.0),
        CourtTemplateKeypoint(name="near_right_baseline_corner", x=1.0, y=0.0),
        CourtTemplateKeypoint(name="far_left_baseline_corner", x=0.0, y=1.0),
        CourtTemplateKeypoint(name="far_right_baseline_corner", x=1.0, y=1.0),
        CourtTemplateKeypoint(name="left_net_post", x=0.0, y=0.5),
        CourtTemplateKeypoint(name="right_net_post", x=1.0, y=0.5),
        CourtTemplateKeypoint(name="service_line_t_near_left", x=0.25, y=0.35),
        CourtTemplateKeypoint(name="service_line_t_near_right", x=0.75, y=0.35),
        CourtTemplateKeypoint(name="service_line_t_far_left", x=0.25, y=0.65),
        CourtTemplateKeypoint(name="service_line_t_far_right", x=0.75, y=0.65),
        CourtTemplateKeypoint(name="center_mark_near", x=0.5, y=0.0),
        CourtTemplateKeypoint(name="center_mark_far", x=0.5, y=1.0),
    ],
    lines=[
        CourtTemplateLine(
            line_class="baseline_near",
            start_keypoint="near_left_baseline_corner",
            end_keypoint="near_right_baseline_corner",
        ),
        CourtTemplateLine(
            line_class="baseline_far",
            start_keypoint="far_left_baseline_corner",
            end_keypoint="far_right_baseline_corner",
        ),
        CourtTemplateLine(
            line_class="sideline_left",
            start_keypoint="near_left_baseline_corner",
            end_keypoint="far_left_baseline_corner",
        ),
        CourtTemplateLine(
            line_class="sideline_right",
            start_keypoint="near_right_baseline_corner",
            end_keypoint="far_right_baseline_corner",
        ),
        CourtTemplateLine(
            line_class="service_line_near",
            start_keypoint="service_line_t_near_left",
            end_keypoint="service_line_t_near_right",
        ),
        CourtTemplateLine(
            line_class="service_line_far",
            start_keypoint="service_line_t_far_left",
            end_keypoint="service_line_t_far_right",
        ),
        CourtTemplateLine(
            line_class="center_service_line",
            start_keypoint="service_line_t_near_left",
            end_keypoint="service_line_t_far_left",
        ),
        CourtTemplateLine(
            line_class="net_line",
            start_keypoint="left_net_post",
            end_keypoint="right_net_post",
        ),
    ],
    metadata_jsonb={
        "normalized_template": True,
        "geometry_evidence_only": True,
        "real_dimensions_deferred": True,
    },
)

COURT_TEMPLATE_REGISTRY: dict[tuple[str, str], CourtTemplate] = {
    (COURT_TEMPLATE_NAME, COURT_TEMPLATE_VERSION): TENNIS_COURT_TEMPLATE_NORMALIZED_V0,
}


def get_court_template(
    template_name: str = COURT_TEMPLATE_NAME,
    template_version: str = COURT_TEMPLATE_VERSION,
) -> CourtTemplate:
    try:
        return COURT_TEMPLATE_REGISTRY[(template_name, template_version)]
    except KeyError as exc:
        raise CourtSchemaError(
            f"unknown court template: {template_name}/{template_version}"
        ) from exc


def court_template_schema_json(
    template_name: str = COURT_TEMPLATE_NAME,
    template_version: str = COURT_TEMPLATE_VERSION,
) -> dict[str, Any]:
    return get_court_template(template_name, template_version).as_schema_json()


class CourtKeypoint(TOMBaseModel):
    name: str
    x: float | None = None
    y: float | None = None
    confidence: float | None = None
    present: bool
    visibility: str = "unknown"
    source_index: int | None = None


class CourtKeypointSummary(TOMBaseModel):
    keypoint_count: int
    keypoints_present_count: int
    keypoints_missing_count: int
    mean_keypoint_confidence: float | None = None
    min_keypoint_confidence: float | None = None
    max_keypoint_confidence: float | None = None


def summarize_court_keypoints(keypoints: list[dict[str, Any]]) -> CourtKeypointSummary:
    keypoint_count = len(keypoints)
    present_keypoints = [keypoint for keypoint in keypoints if keypoint.get("present") is True]
    confidences = [
        float(keypoint["confidence"])
        for keypoint in present_keypoints
        if keypoint.get("confidence") is not None
    ]
    if confidences:
        mean_confidence = round(sum(confidences) / len(confidences), 6)
        min_confidence = min(confidences)
        max_confidence = max(confidences)
    else:
        mean_confidence = None
        min_confidence = None
        max_confidence = None

    return CourtKeypointSummary(
        keypoint_count=keypoint_count,
        keypoints_present_count=len(present_keypoints),
        keypoints_missing_count=keypoint_count - len(present_keypoints),
        mean_keypoint_confidence=mean_confidence,
        min_keypoint_confidence=min_confidence,
        max_keypoint_confidence=max_confidence,
    )


def validate_court_keypoints(keypoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(keypoints) != len(COURT_KEYPOINT_NAMES):
        raise CourtSchemaError(
            f"expected {len(COURT_KEYPOINT_NAMES)} court keypoints, got {len(keypoints)}"
        )
    for expected_name, keypoint in zip(COURT_KEYPOINT_NAMES, keypoints, strict=True):
        if keypoint.get("name") != expected_name:
            raise CourtSchemaError(
                f"court keypoint name mismatch: expected {expected_name}, "
                f"got {keypoint.get('name')}"
            )
        if keypoint.get("visibility", "unknown") not in COURT_VISIBILITY_VALUES:
            raise CourtSchemaError(f"invalid court keypoint visibility: {keypoint}")
        if keypoint.get("present") is True and (
            keypoint.get("x") is None or keypoint.get("y") is None
        ):
            raise CourtSchemaError(f"present court keypoint requires x/y: {expected_name}")
    return keypoints


class CourtKeypointObservationCreate(TOMBaseModel):
    frame_number: int
    timestamp_ms: int
    court_keypoint_schema: str = COURT_KEYPOINT_SCHEMA
    schema_version: str = COURT_KEYPOINT_SCHEMA_VERSION
    keypoints_jsonb: list[dict[str, Any]]
    keypoint_count: int | None = None
    keypoints_present_count: int | None = None
    keypoints_missing_count: int | None = None
    mean_keypoint_confidence: float | None = None
    min_keypoint_confidence: float | None = None
    max_keypoint_confidence: float | None = None
    coordinate_space: str = "image_pixels"
    frame_time_owner: str = "media_indexing"
    raw_model_payload_jsonb: dict[str, Any] = Field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_and_summarize_keypoints(self) -> CourtKeypointObservationCreate:
        validate_court_keypoints(self.keypoints_jsonb)
        summary = summarize_court_keypoints(self.keypoints_jsonb)
        self.keypoint_count = self.keypoint_count or summary.keypoint_count
        self.keypoints_present_count = (
            self.keypoints_present_count
            if self.keypoints_present_count is not None
            else summary.keypoints_present_count
        )
        self.keypoints_missing_count = (
            self.keypoints_missing_count
            if self.keypoints_missing_count is not None
            else summary.keypoints_missing_count
        )
        self.mean_keypoint_confidence = (
            self.mean_keypoint_confidence
            if self.mean_keypoint_confidence is not None
            else summary.mean_keypoint_confidence
        )
        self.min_keypoint_confidence = (
            self.min_keypoint_confidence
            if self.min_keypoint_confidence is not None
            else summary.min_keypoint_confidence
        )
        self.max_keypoint_confidence = (
            self.max_keypoint_confidence
            if self.max_keypoint_confidence is not None
            else summary.max_keypoint_confidence
        )
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        self.metadata_jsonb.setdefault("geometry_evidence_only", True)
        return self


class CourtKeypointObservationRead(CourtKeypointObservationCreate):
    observation_id: str
    media_id: str
    run_id: str
    created_at: datetime


class CourtLineSegment(TOMBaseModel):
    line_class: str
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float | None = None
    visibility: str = "unknown"


def validate_court_line_segments(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for segment in segments:
        if segment.get("line_class") not in COURT_LINE_CLASSES:
            raise CourtSchemaError(f"invalid court line class: {segment}")
        if segment.get("visibility", "unknown") not in COURT_VISIBILITY_VALUES:
            raise CourtSchemaError(f"invalid court line visibility: {segment}")
    return segments


def mean_confidence_from_items(items: list[dict[str, Any]]) -> float | None:
    confidences = [
        float(item["confidence"]) for item in items if item.get("confidence") is not None
    ]
    if not confidences:
        return None
    return round(sum(confidences) / len(confidences), 6)


class CourtLineObservationCreate(TOMBaseModel):
    frame_number: int
    timestamp_ms: int
    line_segments_jsonb: list[dict[str, Any]]
    line_classes_jsonb: list[str] = Field(default_factory=list)
    line_count: int | None = None
    mean_line_confidence: float | None = None
    coordinate_space: str = "image_pixels"
    frame_time_owner: str = "media_indexing"
    raw_model_payload_jsonb: dict[str, Any] = Field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_and_summarize_lines(self) -> CourtLineObservationCreate:
        validate_court_line_segments(self.line_segments_jsonb)
        self.line_classes_jsonb = self.line_classes_jsonb or sorted(
            {segment["line_class"] for segment in self.line_segments_jsonb}
        )
        self.line_count = (
            self.line_count if self.line_count is not None else len(self.line_segments_jsonb)
        )
        self.mean_line_confidence = (
            self.mean_line_confidence
            if self.mean_line_confidence is not None
            else mean_confidence_from_items(self.line_segments_jsonb)
        )
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        self.metadata_jsonb.setdefault("geometry_evidence_only", True)
        return self


class CourtLineObservationRead(CourtLineObservationCreate):
    observation_id: str
    media_id: str
    run_id: str
    created_at: datetime


class CameraViewObservationCreate(TOMBaseModel):
    frame_number: int
    timestamp_ms: int
    frame_start: int | None = None
    frame_end: int | None = None
    timestamp_start_ms: int | None = None
    timestamp_end_ms: int | None = None
    view_label: str
    view_confidence: float | None = None
    camera_motion_hint: str = "unknown"
    stability_score: float | None = None
    cut_likelihood: float | None = None
    frame_time_owner: str = "media_indexing"
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_camera_view(self) -> CameraViewObservationCreate:
        if self.view_label not in CAMERA_VIEW_LABELS:
            raise CourtSchemaError(f"invalid camera view label: {self.view_label}")
        if self.camera_motion_hint not in CAMERA_MOTION_HINTS:
            raise CourtSchemaError(f"invalid camera motion hint: {self.camera_motion_hint}")
        self.frame_start = self.frame_start if self.frame_start is not None else self.frame_number
        self.frame_end = self.frame_end if self.frame_end is not None else self.frame_number
        self.timestamp_start_ms = (
            self.timestamp_start_ms
            if self.timestamp_start_ms is not None
            else self.timestamp_ms
        )
        self.timestamp_end_ms = (
            self.timestamp_end_ms if self.timestamp_end_ms is not None else self.timestamp_ms
        )
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        self.metadata_jsonb.setdefault("geometry_evidence_only", True)
        return self


class CameraViewObservationRead(CameraViewObservationCreate):
    observation_id: str
    media_id: str
    run_id: str
    created_at: datetime


def validate_homography_matrix(matrix: list[list[float]] | None, *, required: bool) -> None:
    if matrix is None:
        if required:
            raise CourtSchemaError("candidate homography requires a 3x3 matrix")
        return
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise CourtSchemaError("homography matrix must be 3x3")


class HomographyCandidateObservationCreate(TOMBaseModel):
    frame_number: int
    timestamp_ms: int
    source_court_keypoint_observation_id: str | None = None
    source_court_line_observation_id: str | None = None
    source_camera_view_observation_id: str | None = None
    homography_matrix_jsonb: list[list[float]] | None = None
    inverse_homography_matrix_jsonb: list[list[float]] | None = None
    source_coordinate_space: str = "image_pixels"
    target_coordinate_space: str = COURT_TEMPLATE_COORDINATE_SPACE
    matrix_direction: str = "image_pixels_to_court_template_2d"
    template_name: str = COURT_TEMPLATE_NAME
    template_version: str = COURT_TEMPLATE_VERSION
    reprojection_error_mean: float | None = None
    reprojection_error_median: float | None = None
    reprojection_error_max: float | None = None
    inlier_count: int | None = None
    outlier_count: int | None = None
    source_point_count: int | None = None
    source_line_count: int | None = None
    confidence: float | None = None
    status: str = "candidate"
    frame_time_owner: str = "media_indexing"
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_homography_candidate(self) -> HomographyCandidateObservationCreate:
        if self.status not in HOMOGRAPHY_CANDIDATE_STATUSES:
            raise CourtSchemaError(f"invalid homography candidate status: {self.status}")
        if self.matrix_direction not in HOMOGRAPHY_MATRIX_DIRECTIONS:
            raise CourtSchemaError(f"invalid homography matrix direction: {self.matrix_direction}")
        if self.target_coordinate_space != COURT_TEMPLATE_COORDINATE_SPACE:
            raise CourtSchemaError(
                f"target coordinate space must be {COURT_TEMPLATE_COORDINATE_SPACE}"
            )
        validate_homography_matrix(
            self.homography_matrix_jsonb,
            required=self.status == "candidate",
        )
        validate_homography_matrix(self.inverse_homography_matrix_jsonb, required=False)
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        self.metadata_jsonb.setdefault("geometry_evidence_only", True)
        return self


class HomographyCandidateObservationRead(HomographyCandidateObservationCreate):
    observation_id: str
    media_id: str
    run_id: str
    created_at: datetime


class ProjectionDiagnosticObservationCreate(TOMBaseModel):
    frame_number: int
    timestamp_ms: int
    source_homography_candidate_observation_id: str
    projected_template_keypoints_jsonb: list[dict[str, Any]] = Field(default_factory=list)
    projected_template_lines_jsonb: list[dict[str, Any]] = Field(default_factory=list)
    diagnostic_metrics_jsonb: dict[str, Any] = Field(default_factory=dict)
    overlay_artifact_id: str | None = None
    confidence: float | None = None
    status: str = "diagnostic_candidate"
    frame_time_owner: str = "media_indexing"
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_projection_diagnostic(self) -> ProjectionDiagnosticObservationCreate:
        if self.status not in PROJECTION_DIAGNOSTIC_STATUSES:
            raise CourtSchemaError(f"invalid projection diagnostic status: {self.status}")
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        self.metadata_jsonb.setdefault("geometry_evidence_only", True)
        self.metadata_jsonb.setdefault("not_ball_player_projection", True)
        return self


class ProjectionDiagnosticObservationRead(ProjectionDiagnosticObservationCreate):
    observation_id: str
    media_id: str
    run_id: str
    created_at: datetime
