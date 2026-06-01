from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel

CAMERA_GEOMETRY_TYPE = "camera_geometry_evidence"
CAMERA_GEOMETRY_VERSION = "v0"


class CameraGeometrySchemaError(ValueError):
    pass


class CameraGeometryStatus(StrEnum):
    declared = "declared"
    partial = "partial"
    estimated = "estimated"
    unknown = "unknown"
    invalid = "invalid"


class CameraModel(StrEnum):
    pinhole_unknown_intrinsics = "pinhole_unknown_intrinsics"
    homography_backed_court_plane = "homography_backed_court_plane"
    manual_placeholder = "manual_placeholder"
    unknown = "unknown"


class CourtModel(StrEnum):
    itf_standard_tennis_court = "itf_standard_tennis_court"
    custom_tennis_court = "custom_tennis_court"
    unknown = "unknown"


TRUTH_LIKE_GEOMETRY_STATUSES = {
    "calibrated_truth",
    "true_camera_pose",
    "verified_3d",
    "verified_geometry",
    "accepted",
    "confirmed",
}

DEFAULT_ITF_COURT_DIMENSIONS_METERS = {
    "court_length": 23.77,
    "court_width": 10.97,
    "singles_width": 8.23,
    "doubles_width": 10.97,
    "net_height_center": 0.914,
    "net_height_posts": 1.07,
}

DEFAULT_WORLD_COORDINATE_SYSTEM = {
    "coordinate_space": "court_metric_3d_readiness_v0",
    "court_x": "meters_left_right_across_declared_court",
    "court_y": "meters_near_far_along_declared_court",
    "court_z": "meters_above_declared_court_plane",
    "z_axis": "positive_up_from_court_plane",
    "court_plane_z": 0.0,
    "origin": "declared_court_origin",
    "origin_description": "near_left_doubles_corner_declared",
    "status": "declared_not_verified",
}

DEFAULT_CAMERA_GEOMETRY_WARNINGS = {
    "geometry_evidence_only": True,
    "not_3d_truth": True,
    "not_camera_calibration_truth": True,
    "does_not_change_event_candidates": True,
    "does_not_create_in_out": True,
    "does_not_create_score": True,
    "no_adjudication": True,
}


class CameraGeometryEvidenceCreate(TOMBaseModel):
    media_id: str
    court_run_id: str | None = None
    court_projection_run_id: str | None = None
    homography_run_id: str | None = None
    geometry_run_id: str | None = None
    camera_model: str = CameraModel.homography_backed_court_plane.value
    geometry_status: str = CameraGeometryStatus.declared.value
    court_model: str = CourtModel.itf_standard_tennis_court.value
    court_units: str = "meters"
    court_length: float | None = None
    court_width: float | None = None
    net_height_center: float | None = None
    net_height_posts: float | None = None
    singles_sideline_width: float | None = None
    doubles_sideline_width: float | None = None
    near_baseline_y: float | None = 0.0
    far_baseline_y: float | None = 1.0
    camera_intrinsics_jsonb: dict[str, Any] = Field(default_factory=dict)
    camera_extrinsics_jsonb: dict[str, Any] = Field(default_factory=dict)
    distortion_jsonb: dict[str, Any] = Field(default_factory=dict)
    image_size_jsonb: dict[str, Any] = Field(default_factory=dict)
    homography_matrix_jsonb: list[list[float]] | None = None
    world_coordinate_system_jsonb: dict[str, Any] = Field(default_factory=dict)
    assumptions_jsonb: dict[str, Any] = Field(default_factory=dict)
    warnings_jsonb: dict[str, Any] = Field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_camera_geometry(self) -> CameraGeometryEvidenceCreate:
        validate_camera_geometry_status(self.geometry_status)
        if self.camera_model not in {item.value for item in CameraModel}:
            raise CameraGeometrySchemaError(f"invalid camera model: {self.camera_model}")
        if self.court_model not in {item.value for item in CourtModel}:
            raise CameraGeometrySchemaError(f"invalid court model: {self.court_model}")
        if self.court_model == CourtModel.itf_standard_tennis_court.value:
            dimensions = DEFAULT_ITF_COURT_DIMENSIONS_METERS
            self.court_length = self.court_length or dimensions["court_length"]
            self.court_width = self.court_width or dimensions["court_width"]
            self.singles_sideline_width = (
                self.singles_sideline_width or dimensions["singles_width"]
            )
            self.doubles_sideline_width = (
                self.doubles_sideline_width or dimensions["doubles_width"]
            )
            self.net_height_center = (
                self.net_height_center or dimensions["net_height_center"]
            )
            self.net_height_posts = self.net_height_posts or dimensions["net_height_posts"]
        if not self.world_coordinate_system_jsonb:
            self.world_coordinate_system_jsonb = dict(DEFAULT_WORLD_COORDINATE_SYSTEM)
        self.warnings_jsonb = {
            **DEFAULT_CAMERA_GEOMETRY_WARNINGS,
            **self.warnings_jsonb,
        }
        self.metadata_jsonb.setdefault("geometry_type", CAMERA_GEOMETRY_TYPE)
        self.metadata_jsonb.setdefault("geometry_version", CAMERA_GEOMETRY_VERSION)
        self.metadata_jsonb.setdefault("true_3d_reconstruction_available", False)
        self.metadata_jsonb.setdefault("3d_ball_trajectory_available", False)
        self.metadata_jsonb.setdefault("observation_only", True)
        self.metadata_jsonb.setdefault("no_adjudication", True)
        return self


class CameraGeometryEvidenceRead(CameraGeometryEvidenceCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class CameraGeometryEvidenceSummary(TOMBaseModel):
    available: bool
    camera_geometry_id: str | None = None
    media_id: str | None = None
    court_run_id: str | None = None
    court_projection_run_id: str | None = None
    homography_run_id: str | None = None
    geometry_run_id: str | None = None
    camera_model: str | None = None
    geometry_status: str | None = None
    court_model: str | None = None
    court_plane_geometry_declared: bool = False
    camera_intrinsics_known: bool = False
    camera_extrinsics_known: bool = False
    true_3d_reconstruction_available: bool = False
    ball_3d_trajectory_available: bool = False
    geometry_evidence_only: bool = True
    no_adjudication: bool = True


def validate_camera_geometry_status(status: str) -> str:
    if status in TRUTH_LIKE_GEOMETRY_STATUSES:
        raise CameraGeometrySchemaError(f"truth-like geometry status is not allowed: {status}")
    if status not in {item.value for item in CameraGeometryStatus}:
        raise CameraGeometrySchemaError(f"invalid camera geometry status: {status}")
    return status
