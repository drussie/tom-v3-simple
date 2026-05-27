from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from tom_v3_schema.base import TOMBaseModel
from tom_v3_schema.skeletons import (
    COCO17_FORMAT,
    COCO17_VERSION,
    skeleton_schema_json,
    validate_keypoint_schema,
)


class PoseKeypoint(TOMBaseModel):
    index: int
    name: str
    x: float | None = None
    y: float | None = None
    x_norm: float | None = None
    y_norm: float | None = None
    confidence: float | None = None
    present: bool
    visibility: str | None = None


class PoseKeypointSummary(TOMBaseModel):
    keypoint_count: int
    keypoints_present_count: int
    keypoints_missing_count: int
    mean_keypoint_confidence: float | None = None
    min_keypoint_confidence: float | None = None
    max_keypoint_confidence: float | None = None


def summarize_pose_keypoints(keypoints: list[dict[str, Any]]) -> PoseKeypointSummary:
    keypoint_count = len(keypoints)
    present_keypoints = [keypoint for keypoint in keypoints if keypoint.get("present") is True]
    present_confidences = [
        float(keypoint["confidence"])
        for keypoint in present_keypoints
        if keypoint.get("confidence") is not None
    ]
    if present_confidences:
        mean_confidence = round(sum(present_confidences) / len(present_confidences), 6)
        min_confidence = min(present_confidences)
        max_confidence = max(present_confidences)
    else:
        mean_confidence = None
        min_confidence = None
        max_confidence = None

    return PoseKeypointSummary(
        keypoint_count=keypoint_count,
        keypoints_present_count=len(present_keypoints),
        keypoints_missing_count=keypoint_count - len(present_keypoints),
        mean_keypoint_confidence=mean_confidence,
        min_keypoint_confidence=min_confidence,
        max_keypoint_confidence=max_confidence,
    )


class PoseObservationCreate(TOMBaseModel):
    frame_number: int
    timestamp_ms: int
    skeleton_format: str = COCO17_FORMAT
    skeleton_version: str = COCO17_VERSION
    keypoint_schema_jsonb: dict[str, Any] = Field(default_factory=skeleton_schema_json)
    keypoints_jsonb: list[dict[str, Any]]
    keypoint_count: int | None = None
    keypoints_present_count: int | None = None
    keypoints_missing_count: int | None = None
    mean_keypoint_confidence: float | None = None
    min_keypoint_confidence: float | None = None
    max_keypoint_confidence: float | None = None
    pose_confidence: float | None = None
    bbox_x: float | None = None
    bbox_y: float | None = None
    bbox_w: float | None = None
    bbox_h: float | None = None
    bbox_confidence: float | None = None
    crop_x: float | None = None
    crop_y: float | None = None
    crop_w: float | None = None
    crop_h: float | None = None
    crop_source: str | None = None
    subject_ref_type: str = "none"
    subject_detection_observation_id: str | None = None
    subject_tracklet_id: str | None = None
    subject_track_point_id: str | None = None
    association_status: str = "unassociated"
    association_method: str = "full_frame_pose"
    association_confidence: float | None = None
    frame_time_owner: str = "media_indexing"
    raw_model_payload_jsonb: dict[str, Any] = Field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_and_summarize_keypoints(self) -> PoseObservationCreate:
        validate_keypoint_schema(
            self.keypoints_jsonb,
            skeleton_format=self.skeleton_format,
            skeleton_version=self.skeleton_version,
        )
        summary = summarize_pose_keypoints(self.keypoints_jsonb)
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
        return self


class PoseObservationRead(PoseObservationCreate):
    observation_id: str
    media_id: str
    run_id: str
    created_at: datetime


class PoseQueryFilters(TOMBaseModel):
    media_id: str | None = None
    run_id: str | None = None
    frame_start_gte: int | None = None
    frame_end_lte: int | None = None
    timestamp_start_gte: int | None = None
    timestamp_end_lte: int | None = None
    pose_confidence_min: float | None = None
    pose_confidence_max: float | None = None
    keypoints_missing_count_min: int | None = None
    keypoints_missing_count_max: int | None = None
    skeleton_format: str | None = None
    association_status: str | None = None
    association_method: str | None = None
    subject_ref_type: str | None = None
    subject_detection_observation_id: str | None = None
    subject_tracklet_id: str | None = None
    subject_track_point_id: str | None = None
    review_label: str | None = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class PoseQueryRow(TOMBaseModel):
    observation: dict[str, Any]
    pose: dict[str, Any]
    media_id: str
    run_id: str
    frame_number: int
    timestamp_ms: int
    skeleton_format: str
    skeleton_version: str
    pose_confidence: float | None
    keypoints_present_count: int
    keypoints_missing_count: int
    subject_ref_type: str
    association_status: str
    association_method: str | None
    subject_detection_observation_id: str | None = None
    subject_tracklet_id: str | None = None
    subject_track_point_id: str | None = None
    annotation_summary: dict[str, Any] = Field(default_factory=dict)
    artifact_summary: dict[str, Any] = Field(default_factory=dict)
    evidence_bundle_url: str


class PoseQueryResponse(TOMBaseModel):
    count: int
    poses: list[PoseQueryRow]
    filters_applied: dict[str, Any]
    summary: dict[str, Any] = Field(default_factory=dict)


def default_pose_runtime_config_payload(
    *,
    model_registry_id: str | None = None,
    weights_path: str | None = None,
    device: str = "cpu",
    frame_sample_policy: str = "explicit_frames",
    subject_source_mode: str = "full_frame",
) -> dict[str, Any]:
    return {
        "adapter": "fixture_pose",
        "adapter_version": "v0",
        "frame_sample_policy": frame_sample_policy,
        "subject_source_mode": subject_source_mode,
        "model_registry_id": model_registry_id,
        "weights_path": weights_path,
        "device": device,
        "imgsz": None,
        "conf": None,
        "iou": None,
        "max_det": None,
        "skeleton_format": COCO17_FORMAT,
        "skeleton_version": COCO17_VERSION,
        "keypoint_schema_json": skeleton_schema_json(),
        "artifact_settings": {"emit_debug_artifact": False},
        "frame_time_owner": "media_indexing",
        "blueprint": 4,
        "milestone": "4A",
    }
