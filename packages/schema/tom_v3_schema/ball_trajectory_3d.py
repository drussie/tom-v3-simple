from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel

BALL_TRAJECTORY_3D_TYPE = "ball_trajectory_3d_candidate_evidence"
BALL_TRAJECTORY_3D_VERSION = "v0"


class BallTrajectory3DSchemaError(ValueError):
    pass


class CourtZStatus(StrEnum):
    unknown = "unknown"
    court_plane_assumed = "court_plane_assumed"
    estimated_candidate = "estimated_candidate"
    interpolated_candidate = "interpolated_candidate"
    insufficient_geometry = "insufficient_geometry"
    invalid = "invalid"


class HeightModel(StrEnum):
    none_unknown = "none_unknown"
    court_plane_placeholder = "court_plane_placeholder"
    image_motion_proxy = "image_motion_proxy"
    declared_geometry_placeholder = "declared_geometry_placeholder"
    future_model_placeholder = "future_model_placeholder"


class BallTrajectory3DStatus(StrEnum):
    candidate = "candidate"
    partial = "partial"
    diagnostic = "diagnostic"
    invalid = "invalid"


TRUTH_LIKE_3D_LABELS = {
    "true_height",
    "verified_height",
    "confirmed_3d",
    "true_3d",
    "truth",
    "accepted",
    "confirmed",
    "verified",
    "calibrated_truth",
}

DEFAULT_3D_TRAJECTORY_WARNINGS = {
    "trajectory_3d_candidate_only": True,
    "not_3d_truth": True,
    "not_camera_calibration_truth": True,
    "height_not_verified": True,
    "geometry_evidence_only": True,
    "does_not_change_event_candidates": True,
    "does_not_create_event_truth": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}


class BallTrajectory3DCandidateCreate(TOMBaseModel):
    media_id: str
    ball_trajectory_run_id: str
    court_projection_run_id: str | None = None
    camera_geometry_id: str | None = None
    geometry_run_id: str | None = None
    trajectory_3d_run_id: str | None = None
    source_observation_id: str | None = None
    frame: int
    timestamp_ms: int
    image_x: float | None = None
    image_y: float | None = None
    court_x: float | None = None
    court_y: float | None = None
    court_x_m: float | None = None
    court_y_m: float | None = None
    court_z_m: float | None = None
    court_z_status: str = CourtZStatus.unknown.value
    height_model: str = HeightModel.none_unknown.value
    projection_method: str = "declared_court_plane_metric_xy_unknown_z_v0"
    confidence: float | None = None
    velocity_x_mps: float | None = None
    velocity_y_mps: float | None = None
    velocity_z_mps: float | None = None
    speed_mps: float | None = None
    diagnostics_jsonb: dict[str, Any] = Field(default_factory=dict)
    warnings_jsonb: dict[str, Any] = Field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_candidate(self) -> BallTrajectory3DCandidateCreate:
        validate_height_model(self.height_model)
        validate_court_z_status(self.court_z_status)
        self.warnings_jsonb = {
            **DEFAULT_3D_TRAJECTORY_WARNINGS,
            **self.warnings_jsonb,
        }
        self.metadata_jsonb.setdefault("trajectory_3d_type", BALL_TRAJECTORY_3D_TYPE)
        self.metadata_jsonb.setdefault("trajectory_3d_version", BALL_TRAJECTORY_3D_VERSION)
        self.metadata_jsonb.setdefault("true_3d_reconstruction_available", False)
        self.metadata_jsonb.setdefault("3d_ball_trajectory_truth_available", False)
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        return self


class BallTrajectory3DCandidateRead(BallTrajectory3DCandidateCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class BallTrajectory3DRunSummary(TOMBaseModel):
    available: bool
    trajectory_3d_run_id: str | None = None
    media_id: str | None = None
    ball_trajectory_run_id: str | None = None
    court_projection_run_id: str | None = None
    camera_geometry_id: str | None = None
    candidate_count: int = 0
    height_model: str | None = None
    known_height_count: int = 0
    unknown_height_count: int = 0
    court_plane_xy_metric_count: int = 0
    height_candidate_available: bool = False
    true_3d_reconstruction_available: bool = False
    ball_3d_trajectory_truth_available: bool = False
    geometry_evidence_only: bool = True
    no_adjudication: bool = True


def validate_height_model(height_model: str) -> str:
    if height_model in TRUTH_LIKE_3D_LABELS:
        raise BallTrajectory3DSchemaError(
            f"truth-like 3D height model is not allowed: {height_model}"
        )
    if height_model not in {item.value for item in HeightModel}:
        raise BallTrajectory3DSchemaError(f"invalid height model: {height_model}")
    return height_model


def validate_court_z_status(court_z_status: str) -> str:
    if court_z_status in TRUTH_LIKE_3D_LABELS:
        raise BallTrajectory3DSchemaError(
            f"truth-like court z status is not allowed: {court_z_status}"
        )
    if court_z_status not in {item.value for item in CourtZStatus}:
        raise BallTrajectory3DSchemaError(f"invalid court z status: {court_z_status}")
    return court_z_status
