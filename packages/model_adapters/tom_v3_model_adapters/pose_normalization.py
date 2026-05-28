from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from math import isfinite
from typing import Any

from tom_v3_schema.pose import PoseObservationCreate, summarize_pose_keypoints
from tom_v3_schema.skeletons import (
    COCO17_FORMAT,
    COCO17_VERSION,
    SkeletonRegistryError,
    get_skeleton_definition,
    skeleton_schema_json,
)

SOURCE_RUNTIME = "pose_model_output"
ADAPTER_NAME = "fixture-pose-normalizer"
ADAPTER_VERSION = "v0"


@dataclass(frozen=True)
class NormalizedPoseObservation:
    frame_number: int
    timestamp_ms: int
    skeleton_format: str
    skeleton_version: str
    keypoint_schema_jsonb: dict[str, Any]
    keypoints_jsonb: list[dict[str, Any]]
    keypoint_count: int
    keypoints_present_count: int
    keypoints_missing_count: int
    mean_keypoint_confidence: float | None
    min_keypoint_confidence: float | None
    max_keypoint_confidence: float | None
    pose_confidence: float | None
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
    raw_model_payload_jsonb: dict[str, Any] = field(default_factory=dict)
    metadata_jsonb: dict[str, Any] = field(default_factory=dict)

    def as_pose_observation_create(self) -> PoseObservationCreate:
        return PoseObservationCreate(**self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "frame_number": self.frame_number,
            "timestamp_ms": self.timestamp_ms,
            "skeleton_format": self.skeleton_format,
            "skeleton_version": self.skeleton_version,
            "keypoint_schema_jsonb": self.keypoint_schema_jsonb,
            "keypoints_jsonb": self.keypoints_jsonb,
            "keypoint_count": self.keypoint_count,
            "keypoints_present_count": self.keypoints_present_count,
            "keypoints_missing_count": self.keypoints_missing_count,
            "mean_keypoint_confidence": self.mean_keypoint_confidence,
            "min_keypoint_confidence": self.min_keypoint_confidence,
            "max_keypoint_confidence": self.max_keypoint_confidence,
            "pose_confidence": self.pose_confidence,
            "bbox_x": self.bbox_x,
            "bbox_y": self.bbox_y,
            "bbox_w": self.bbox_w,
            "bbox_h": self.bbox_h,
            "bbox_confidence": self.bbox_confidence,
            "crop_x": self.crop_x,
            "crop_y": self.crop_y,
            "crop_w": self.crop_w,
            "crop_h": self.crop_h,
            "crop_source": self.crop_source,
            "subject_ref_type": self.subject_ref_type,
            "subject_detection_observation_id": self.subject_detection_observation_id,
            "subject_tracklet_id": self.subject_tracklet_id,
            "subject_track_point_id": self.subject_track_point_id,
            "association_status": self.association_status,
            "association_method": self.association_method,
            "association_confidence": self.association_confidence,
            "frame_time_owner": self.frame_time_owner,
            "raw_model_payload_jsonb": self.raw_model_payload_jsonb,
            "metadata_jsonb": self.metadata_jsonb,
        }


@dataclass(frozen=True)
class PoseNormalizationResult:
    poses: list[NormalizedPoseObservation]
    input_pose_count: int
    normalized_pose_count: int
    skipped_pose_count: int
    warnings: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "poses": [pose.as_dict() for pose in self.poses],
            "input_pose_count": self.input_pose_count,
            "normalized_pose_count": self.normalized_pose_count,
            "skipped_pose_count": self.skipped_pose_count,
            "warnings": self.warnings,
        }


@dataclass(frozen=True)
class PoseAdapterResult:
    adapter_name: str
    adapter_version: str
    poses: list[NormalizedPoseObservation]
    artifact_metadata: list[dict[str, Any]] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)


class PoseNormalizationAdapter:
    name = ADAPTER_NAME
    version = ADAPTER_VERSION

    def normalize_frame_result(
        self,
        frame_result: Mapping[str, Any],
        *,
        model_registry_id: str | None = None,
        runtime_config_id: str | None = None,
        inference_metadata: Mapping[str, Any] | None = None,
    ) -> PoseNormalizationResult:
        return normalize_pose_frame_result(
            frame_result,
            model_registry_id=model_registry_id,
            runtime_config_id=runtime_config_id,
            inference_metadata=inference_metadata,
        )

    def normalize_results(
        self,
        frame_results: Iterable[Mapping[str, Any]],
        *,
        model_registry_id: str | None = None,
        runtime_config_id: str | None = None,
        inference_metadata: Mapping[str, Any] | None = None,
    ) -> PoseNormalizationResult:
        return normalize_pose_results(
            frame_results,
            model_registry_id=model_registry_id,
            runtime_config_id=runtime_config_id,
            inference_metadata=inference_metadata,
        )

    def build_adapter_result_from_normalized(
        self, result: PoseNormalizationResult
    ) -> PoseAdapterResult:
        return build_pose_adapter_result_from_normalized(result)


class FixturePoseAdapter(PoseNormalizationAdapter):
    name = "fixture-pose-adapter"
    version = "normalization-v0"


def normalize_pose_frame_result(
    frame_result: Mapping[str, Any],
    *,
    model_registry_id: str | None = None,
    runtime_config_id: str | None = None,
    inference_metadata: Mapping[str, Any] | None = None,
) -> PoseNormalizationResult:
    poses_input = list(_mapping_value(frame_result, "poses") or [])
    warnings: list[dict[str, Any]] = []
    normalized_poses: list[NormalizedPoseObservation] = []

    skeleton_format = str(_mapping_value(frame_result, "skeleton_format") or COCO17_FORMAT)
    skeleton_version = str(_mapping_value(frame_result, "skeleton_version") or COCO17_VERSION)
    try:
        skeleton = get_skeleton_definition(skeleton_format, skeleton_version)
    except SkeletonRegistryError:
        return PoseNormalizationResult(
            poses=[],
            input_pose_count=len(poses_input),
            normalized_pose_count=0,
            skipped_pose_count=len(poses_input),
            warnings=[
                {
                    "warning_type": "unsupported_skeleton",
                    "message": "pose skeleton format/version is not registered",
                    "skeleton_format": skeleton_format,
                    "skeleton_version": skeleton_version,
                }
            ],
        )

    image_width = _optional_numeric(_mapping_value(frame_result, "image_width"))
    image_height = _optional_numeric(_mapping_value(frame_result, "image_height"))
    frame_number = int(_mapping_value(frame_result, "frame_number"))
    timestamp_ms = int(_mapping_value(frame_result, "timestamp_ms"))

    for fallback_index, pose_input in enumerate(poses_input):
        source_result_index = _source_result_index(pose_input, fallback_index)
        keypoints_input = _mapping_value(pose_input, "keypoints")
        if not isinstance(keypoints_input, list):
            warnings.append(
                {
                    "warning_type": "missing_keypoint_schema",
                    "message": "pose keypoints must be a list",
                    "source_result_index": source_result_index,
                }
            )
            continue
        if len(keypoints_input) != len(skeleton.keypoints):
            warnings.append(
                {
                    "warning_type": "invalid_keypoint_count",
                    "message": "pose keypoint count does not match skeleton schema",
                    "source_result_index": source_result_index,
                    "expected_count": len(skeleton.keypoints),
                    "actual_count": len(keypoints_input),
                }
            )
            continue

        coordinate_space = str(
            _mapping_value(pose_input, "keypoint_coordinate_space")
            or _mapping_value(frame_result, "keypoint_coordinate_space")
            or "image_pixels"
        )
        crop = _parse_crop(
            _mapping_value(pose_input, "crop") or _mapping_value(frame_result, "crop"),
            source_result_index=source_result_index,
            warnings=warnings,
        )
        should_project_crop = coordinate_space == "crop_pixels" and crop is not None

        crop_local_keypoints: list[dict[str, Any]] = []
        keypoints = _normalize_keypoints(
            keypoints_input=keypoints_input,
            skeleton_keypoints=skeleton.keypoints,
            image_width=image_width,
            image_height=image_height,
            crop=crop if should_project_crop else None,
            source_result_index=source_result_index,
            warnings=warnings,
            crop_local_keypoints=crop_local_keypoints,
        )
        summary = summarize_pose_keypoints(keypoints)
        pose_confidence = _confidence_or_mean(
            _mapping_value(pose_input, "pose_confidence", "confidence"),
            summary.mean_keypoint_confidence,
            warning_context="pose_confidence",
            source_result_index=source_result_index,
            warnings=warnings,
        )
        bbox_confidence = _confidence_or_none(
            _mapping_value(pose_input, "bbox_confidence"),
            warning_context="bbox_confidence",
            source_result_index=source_result_index,
            warnings=warnings,
        )
        bbox = _xyxy_to_bbox(_mapping_value(pose_input, "bbox_xyxy"))
        if bbox is None and _mapping_value(pose_input, "bbox_xyxy") is not None:
            warnings.append(
                {
                    "warning_type": "invalid_bbox",
                    "message": "bbox xyxy must contain four numeric values with positive area",
                    "source_result_index": source_result_index,
                    "bbox_xyxy": _mapping_value(pose_input, "bbox_xyxy"),
                }
            )

        subject_context = _subject_context(
            _mapping_value(frame_result, "subject_context"),
            _mapping_value(pose_input, "subject_context"),
        )
        association_confidence = _confidence_or_none(
            subject_context.get("association_confidence"),
            warning_context="association_confidence",
            source_result_index=source_result_index,
            warnings=warnings,
        )
        metadata: dict[str, Any] = {
            "adapter": "pose_normalization_adapter",
            "adapter_version": ADAPTER_VERSION,
            "source_runtime": SOURCE_RUNTIME,
            "source_result_index": source_result_index,
            "skeleton_format": skeleton_format,
            "skeleton_version": skeleton_version,
            "keypoint_coordinate_space": coordinate_space,
            "frame_time_owner": "media_indexing",
            "model_registry_id": model_registry_id,
            "runtime_config_id": runtime_config_id,
            "inference": dict(inference_metadata or {}),
            "normalization_only": True,
        }
        if subject_context:
            metadata["subject_context"] = dict(subject_context)
        if crop_local_keypoints:
            metadata["crop_local_keypoints"] = crop_local_keypoints

        crop_source = None if crop is None else crop.get("source")
        normalized_poses.append(
            NormalizedPoseObservation(
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                skeleton_format=skeleton_format,
                skeleton_version=skeleton_version,
                keypoint_schema_jsonb=skeleton_schema_json(skeleton_format, skeleton_version),
                keypoints_jsonb=keypoints,
                keypoint_count=summary.keypoint_count,
                keypoints_present_count=summary.keypoints_present_count,
                keypoints_missing_count=summary.keypoints_missing_count,
                mean_keypoint_confidence=summary.mean_keypoint_confidence,
                min_keypoint_confidence=summary.min_keypoint_confidence,
                max_keypoint_confidence=summary.max_keypoint_confidence,
                pose_confidence=pose_confidence,
                bbox_x=None if bbox is None else bbox[0],
                bbox_y=None if bbox is None else bbox[1],
                bbox_w=None if bbox is None else bbox[2],
                bbox_h=None if bbox is None else bbox[3],
                bbox_confidence=bbox_confidence,
                crop_x=None if crop is None else crop["x"],
                crop_y=None if crop is None else crop["y"],
                crop_w=None if crop is None else crop["width"],
                crop_h=None if crop is None else crop["height"],
                crop_source=crop_source,
                subject_ref_type=str(subject_context.get("subject_ref_type") or "none"),
                subject_detection_observation_id=subject_context.get(
                    "subject_detection_observation_id"
                ),
                subject_tracklet_id=subject_context.get("subject_tracklet_id"),
                subject_track_point_id=subject_context.get("subject_track_point_id"),
                association_status=str(
                    subject_context.get("association_status") or "unassociated"
                ),
                association_method=str(
                    subject_context.get("association_method") or "full_frame_pose"
                ),
                association_confidence=association_confidence,
                frame_time_owner="media_indexing",
                raw_model_payload_jsonb={
                    "frame_number": frame_number,
                    "timestamp_ms": timestamp_ms,
                    "source_result_index": source_result_index,
                    "pose": _jsonable_mapping(pose_input),
                },
                metadata_jsonb=metadata,
            )
        )

    return PoseNormalizationResult(
        poses=normalized_poses,
        input_pose_count=len(poses_input),
        normalized_pose_count=len(normalized_poses),
        skipped_pose_count=len(poses_input) - len(normalized_poses),
        warnings=warnings,
    )


def normalize_pose_results(
    frame_results: Iterable[Mapping[str, Any]],
    *,
    model_registry_id: str | None = None,
    runtime_config_id: str | None = None,
    inference_metadata: Mapping[str, Any] | None = None,
) -> PoseNormalizationResult:
    aggregate_poses: list[NormalizedPoseObservation] = []
    aggregate_warnings: list[dict[str, Any]] = []
    input_pose_count = 0

    for frame_result in frame_results:
        result = normalize_pose_frame_result(
            frame_result,
            model_registry_id=model_registry_id,
            runtime_config_id=runtime_config_id,
            inference_metadata=inference_metadata,
        )
        aggregate_poses.extend(result.poses)
        aggregate_warnings.extend(result.warnings)
        input_pose_count += result.input_pose_count

    return PoseNormalizationResult(
        poses=aggregate_poses,
        input_pose_count=input_pose_count,
        normalized_pose_count=len(aggregate_poses),
        skipped_pose_count=input_pose_count - len(aggregate_poses),
        warnings=aggregate_warnings,
    )


def build_pose_adapter_result_from_normalized(result: PoseNormalizationResult) -> PoseAdapterResult:
    return PoseAdapterResult(
        adapter_name=ADAPTER_NAME,
        adapter_version=ADAPTER_VERSION,
        poses=result.poses,
        diagnostics={
            "adapter_name": ADAPTER_NAME,
            "adapter_version": ADAPTER_VERSION,
            "input_pose_count": result.input_pose_count,
            "normalized_pose_count": result.normalized_pose_count,
            "skipped_pose_count": result.skipped_pose_count,
            "warnings": result.warnings,
            "note": "normalization only, no real pose inference",
        },
    )


def _normalize_keypoints(
    *,
    keypoints_input: list[Any],
    skeleton_keypoints: list[Any],
    image_width: float | None,
    image_height: float | None,
    crop: dict[str, float | str] | None,
    source_result_index: int,
    warnings: list[dict[str, Any]],
    crop_local_keypoints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    keypoints: list[dict[str, Any]] = []
    for skeleton_keypoint, raw_keypoint in zip(
        skeleton_keypoints, keypoints_input, strict=True
    ):
        present_value = _mapping_value(raw_keypoint, "present")
        raw_x = _mapping_value(raw_keypoint, "x")
        raw_y = _mapping_value(raw_keypoint, "y")
        x = _optional_numeric(raw_x)
        y = _optional_numeric(raw_y)
        invalid_coordinate = (
            present_value is not False
            and (raw_x is not None or raw_y is not None)
            and (x is None or y is None)
        )
        if invalid_coordinate:
            warnings.append(
                {
                    "warning_type": "invalid_keypoint_coordinate",
                    "message": "keypoint x/y must both be numeric when present",
                    "source_result_index": source_result_index,
                    "keypoint_index": skeleton_keypoint.index,
                    "keypoint_name": skeleton_keypoint.name,
                }
            )

        confidence = _confidence_or_none(
            _mapping_value(raw_keypoint, "confidence"),
            warning_context=f"keypoint:{skeleton_keypoint.name}",
            source_result_index=source_result_index,
            warnings=warnings,
            allow_missing=True,
        )
        if present_value is False or x is None or y is None:
            keypoints.append(
                {
                    "index": skeleton_keypoint.index,
                    "name": skeleton_keypoint.name,
                    "x": None,
                    "y": None,
                    "x_norm": None,
                    "y_norm": None,
                    "confidence": None if present_value is False else confidence,
                    "present": False,
                    "visibility": _mapping_value(raw_keypoint, "visibility"),
                }
            )
            continue

        local_x = x
        local_y = y
        if crop is not None:
            crop_local_keypoints.append(
                {
                    "index": skeleton_keypoint.index,
                    "name": skeleton_keypoint.name,
                    "x": local_x,
                    "y": local_y,
                    "confidence": confidence,
                }
            )
            x = float(crop["x"]) + x
            y = float(crop["y"]) + y

        keypoints.append(
            {
                "index": skeleton_keypoint.index,
                "name": skeleton_keypoint.name,
                "x": x,
                "y": y,
                "x_norm": _normalized_coordinate(x, image_width),
                "y_norm": _normalized_coordinate(y, image_height),
                "confidence": confidence,
                "present": True,
                "visibility": _mapping_value(raw_keypoint, "visibility"),
            }
        )
    return keypoints


def _normalized_coordinate(value: float, denominator: float | None) -> float | None:
    if denominator is None or denominator <= 0:
        return None
    return round(value / denominator, 6)


def _parse_crop(
    crop_input: Any,
    *,
    source_result_index: int,
    warnings: list[dict[str, Any]],
) -> dict[str, float | str] | None:
    if crop_input is None:
        return None
    x = _optional_numeric(_mapping_value(crop_input, "x"))
    y = _optional_numeric(_mapping_value(crop_input, "y"))
    width = _optional_numeric(_mapping_value(crop_input, "width", "w"))
    height = _optional_numeric(_mapping_value(crop_input, "height", "h"))
    if x is None or y is None or width is None or height is None or width <= 0 or height <= 0:
        warnings.append(
            {
                "warning_type": "invalid_crop",
                "message": "crop must include numeric x, y, width, and height with positive area",
                "source_result_index": source_result_index,
            }
        )
        return None
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "source": str(_mapping_value(crop_input, "source") or "crop"),
    }


def _subject_context(*contexts: Any) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for context in contexts:
        if isinstance(context, Mapping):
            merged.update(context)
    return merged


def _xyxy_to_bbox(xyxy: Any) -> tuple[float, float, float, float] | None:
    if xyxy is None:
        return None
    if not isinstance(xyxy, list | tuple) or len(xyxy) != 4:
        return None
    try:
        x1, y1, x2, y2 = (_finite_float(value) for value in xyxy)
    except (TypeError, ValueError):
        return None
    width = x2 - x1
    height = y2 - y1
    if width <= 0 or height <= 0:
        return None
    return x1, y1, width, height


def _confidence_or_mean(
    value: Any,
    fallback: float | None,
    *,
    warning_context: str,
    source_result_index: int,
    warnings: list[dict[str, Any]],
) -> float | None:
    confidence = _confidence_or_none(
        value,
        warning_context=warning_context,
        source_result_index=source_result_index,
        warnings=warnings,
        allow_missing=True,
    )
    return fallback if confidence is None else confidence


def _confidence_or_none(
    value: Any,
    *,
    warning_context: str,
    source_result_index: int,
    warnings: list[dict[str, Any]],
    allow_missing: bool = False,
) -> float | None:
    if value is None:
        return None
    confidence = _optional_numeric(value)
    if confidence is None:
        warnings.append(
            {
                "warning_type": "invalid_confidence",
                "message": "confidence must be numeric or null",
                "source_result_index": source_result_index,
                "field": warning_context,
            }
        )
        return None
    if confidence < 0 or confidence > 1:
        warnings.append(
            {
                "warning_type": "confidence_out_of_range",
                "message": "confidence is outside the expected 0..1 range",
                "source_result_index": source_result_index,
                "field": warning_context,
                "confidence": confidence,
            }
        )
    return confidence


def _optional_numeric(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return _finite_float(value)
    except (TypeError, ValueError):
        return None


def _finite_float(value: Any) -> float:
    parsed = float(value)
    if not isfinite(parsed):
        raise ValueError("value must be finite")
    return parsed


def _source_result_index(pose_input: Any, fallback_index: int) -> int:
    value = _mapping_value(pose_input, "source_result_index")
    if value is None or isinstance(value, bool):
        return fallback_index
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback_index


def _mapping_value(source: Any, *keys: str) -> Any:
    for key in keys:
        if isinstance(source, Mapping) and key in source:
            return source[key]
        if not isinstance(source, Mapping) and hasattr(source, key):
            return getattr(source, key)
    return None


def _jsonable_mapping(source: Any) -> dict[str, Any]:
    if isinstance(source, Mapping):
        return dict(source)
    return {"repr": repr(source)}
