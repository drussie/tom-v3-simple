from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_schema.observations import ObservationCreate
from tom_v3_schema.pose import PoseObservationCreate, default_pose_runtime_config_payload
from tom_v3_schema.skeletons import (
    COCO17_KEYPOINT_NAMES,
    COCO17_VERSION,
    skeleton_schema_json,
)
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    PoseObservation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.time_index import frame_to_timestamp_ms

from tom_v3_observations.writer import ObservationWriter


class SyntheticPoseObservationError(ValueError):
    pass


def fixture_coco17_keypoints(
    *,
    image_width: int = 1280,
    image_height: int = 720,
    missing_names: set[str] | None = None,
) -> list[dict[str, Any]]:
    missing_names = missing_names or {"right_wrist", "left_ankle"}
    keypoints: list[dict[str, Any]] = []
    for index, name in enumerate(COCO17_KEYPOINT_NAMES):
        present = name not in missing_names
        if present:
            x = 500.0 + index * 8.0
            y = 180.0 + index * 18.0
            confidence = round(0.9 - index * 0.02, 3)
            keypoint = {
                "index": index,
                "name": name,
                "x": x,
                "y": y,
                "x_norm": round(x / image_width, 6),
                "y_norm": round(y / image_height, 6),
                "confidence": confidence,
                "present": True,
                "visibility": None,
            }
        else:
            keypoint = {
                "index": index,
                "name": name,
                "x": None,
                "y": None,
                "x_norm": None,
                "y_norm": None,
                "confidence": None,
                "present": False,
                "visibility": None,
            }
        keypoints.append(keypoint)
    return keypoints


def create_synthetic_pose_observation(
    *,
    session: Session,
    media_id: str,
    frame_number: int = 0,
    run_name: str = "fixture-pose-run",
    pose_confidence: float = 0.82,
    keypoints_jsonb: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise SyntheticPoseObservationError(f"media asset not found: {media_id}")
    if media.fps is None:
        raise SyntheticPoseObservationError("media fps is required for pose frame/time mapping")

    model = _get_or_create_fixture_pose_model(session)
    runtime_config = RuntimeConfig(
        config_name="fixture-pose-runtime-config",
        config_version="v0",
        payload_jsonb=default_pose_runtime_config_payload(model_registry_id=model.id),
    )
    session.add(runtime_config)
    session.flush()

    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="completed",
        started_at=now,
        completed_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "source": "synthetic fixture pose insertion",
            "frame_time_owner": "media_indexing",
            "blueprint": 4,
            "milestone": "4A",
        },
    )
    session.add(run)
    session.flush()
    step = ProcessingStep(
        run_id=run.id,
        step_name="fixture_pose_observation_insert",
        step_status="completed",
        started_at=now,
        completed_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "skeleton_format": "coco17",
            "skeleton_version": COCO17_VERSION,
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(step)
    session.commit()
    session.refresh(run)
    session.refresh(step)
    session.refresh(runtime_config)

    timestamp_ms = frame_to_timestamp_ms(media.fps, frame_number)
    keypoints = keypoints_jsonb or fixture_coco17_keypoints(
        image_width=media.width or 1280,
        image_height=media.height or 720,
    )
    pose = PoseObservationCreate(
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        keypoint_schema_jsonb=skeleton_schema_json(),
        keypoints_jsonb=keypoints,
        pose_confidence=pose_confidence,
        bbox_x=480.0,
        bbox_y=150.0,
        bbox_w=180.0,
        bbox_h=430.0,
        bbox_confidence=0.86,
        crop_source="full_frame",
        subject_ref_type="none",
        association_status="unassociated",
        association_method="full_frame_pose",
        frame_time_owner="media_indexing",
        raw_model_payload_jsonb={"fixture": True, "adapter": "fixture_pose"},
        metadata_jsonb={
            "fixture": True,
            "skeleton_format": "coco17",
            "skeleton_version": COCO17_VERSION,
            "frame_time_owner": "media_indexing",
        },
    )
    payload = {
        "skeleton_format": pose.skeleton_format,
        "skeleton_version": pose.skeleton_version,
        "keypoint_count": pose.keypoint_count,
        "keypoints_present_count": pose.keypoints_present_count,
        "keypoints_missing_count": pose.keypoints_missing_count,
        "pose_confidence": pose.pose_confidence,
        "bbox": {
            "x": pose.bbox_x,
            "y": pose.bbox_y,
            "width": pose.bbox_w,
            "height": pose.bbox_h,
            "confidence": pose.bbox_confidence,
        },
        "subject_ref_type": pose.subject_ref_type,
        "association_status": pose.association_status,
        "association_method": pose.association_method,
        "frame_time_owner": "media_indexing",
        "keypoints": pose.keypoints_jsonb,
    }
    detail = ObservationWriter(session).write(
        ObservationCreate(
            media_id=media.id,
            run_id=run.id,
            observation_family="pose",
            observation_type="player_pose_observation",
            granularity="frame",
            frame_start=frame_number,
            frame_end=frame_number,
            timestamp_start_ms=timestamp_ms,
            timestamp_end_ms=timestamp_ms,
            confidence=pose.pose_confidence,
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            coordinate_space="image_pixels",
            payload_jsonb=payload,
            pose=pose,
        )
    )
    pose_row = session.get(PoseObservation, detail.id)
    if pose_row is None:
        raise SyntheticPoseObservationError("pose observation row was not persisted")

    return {
        "media_id": media.id,
        "run_id": run.id,
        "processing_step_id": step.id,
        "model_id": model.id,
        "runtime_config_id": runtime_config.id,
        "observation_id": detail.id,
        "pose_observation_id": pose_row.observation_id,
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "keypoint_count": pose_row.keypoint_count,
        "keypoints_present_count": pose_row.keypoints_present_count,
        "keypoints_missing_count": pose_row.keypoints_missing_count,
    }


def _get_or_create_fixture_pose_model(session: Session) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == "fixture-coco17-pose-model",
            ModelRegistry.version == "fixture-v0",
            ModelRegistry.model_family == "pose",
        )
    )
    if model is not None:
        return model

    model = ModelRegistry(
        name="fixture-coco17-pose-model",
        version="fixture-v0",
        model_family="pose",
        source="tom_v3_observations.pose",
        metadata_jsonb={
            "model_runtime": "fixture",
            "model_task": "pose",
            "skeleton_format": "coco17",
            "skeleton_version": COCO17_VERSION,
            "keypoint_schema_json": skeleton_schema_json(),
            "blueprint": 4,
            "milestone": "4A",
            "frame_time_owner": "media_indexing",
            "no_real_pose_inference": True,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model
