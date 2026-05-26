from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_model_adapters.pose_normalization import FixturePoseAdapter, PoseAdapterResult
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_schema.pose import PoseObservationCreate, default_pose_runtime_config_payload
from tom_v3_schema.skeletons import COCO17_KEYPOINT_NAMES, COCO17_VERSION, skeleton_schema_json
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)
from tom_v3_video.time_index import frame_to_timestamp_ms


class PoseAdapterRunError(ValueError):
    pass


def run_pose_adapter(
    *,
    session: Session,
    media_id: str,
    adapter_name: str = "fixture",
    run_name: str = "fixture-pose-run",
    config_name: str = "pose-adapter-config",
    config_version: str = "v0",
    frame_sample_rate: int = 30,
    max_frames: int | None = 3,
    source_detection_run_id: str | None = None,
    link_source_detections: bool = False,
    frame_results: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise PoseAdapterRunError(f"media asset not found: {media_id}")
    if frame_sample_rate <= 0:
        raise PoseAdapterRunError("frame_sample_rate must be greater than zero")
    if media.fps is None:
        raise PoseAdapterRunError("media fps is required for pose frame/time mapping")

    normalized_adapter_name = adapter_name.strip().lower()
    if normalized_adapter_name not in {"fixture", "normalized_fixture", "fixture_pose"}:
        raise PoseAdapterRunError(
            f"unsupported pose adapter {adapter_name!r}; only fixture is available in 4C"
        )

    adapter = FixturePoseAdapter()
    model = _get_or_create_fixture_pose_model(session)
    runtime_config = _create_runtime_config(
        session=session,
        model=model,
        config_name=config_name,
        config_version=config_version,
        adapter=adapter,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        source_detection_run_id=source_detection_run_id,
        link_source_detections=link_source_detections,
    )
    run = _create_run(
        session=session,
        media=media,
        runtime_config=runtime_config,
        run_name=run_name,
        adapter=adapter,
        source_detection_run_id=source_detection_run_id,
    )
    step = _create_step(session, run, runtime_config, adapter)

    try:
        generated_frame_results = list(
            frame_results
            if frame_results is not None
            else _fixture_frame_results(
                session=session,
                media=media,
                frame_sample_rate=frame_sample_rate,
                max_frames=max_frames,
                source_detection_run_id=source_detection_run_id,
                link_source_detections=link_source_detections,
            )
        )
        normalization = adapter.normalize_results(
            generated_frame_results,
            model_registry_id=model.id,
            runtime_config_id=runtime_config.id,
            inference_metadata={
                "adapter": "fixture_pose",
                "adapter_version": adapter.version,
                "normalization_only": True,
                "frame_time_owner": "media_indexing",
            },
        )
        result = PoseAdapterResult(
            adapter_name=adapter.name,
            adapter_version=adapter.version,
            poses=normalization.poses,
            diagnostics={
                "adapter_name": adapter.name,
                "adapter_version": adapter.version,
                "input_pose_count": normalization.input_pose_count,
                "normalized_pose_count": normalization.normalized_pose_count,
                "skipped_pose_count": normalization.skipped_pose_count,
                "warnings": normalization.warnings,
                "note": "normalization only, no real pose inference",
            },
        )
        observations = _persist_poses(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            result=result,
        )
    except Exception as exc:
        _mark_failed(session, run, step, str(exc))
        raise

    lineage_count = sum(
        len(observation.payload_jsonb.get("lineage", [])) for observation in observations
    )
    _mark_completed(
        session=session,
        run=run,
        step=step,
        result=result,
        pose_observation_count=len(observations),
        lineage_count=lineage_count,
    )
    return {
        "media_id": media.id,
        "pose_run_id": run.id,
        "run_id": run.id,
        "processing_step_id": step.id,
        "pose_observation_count": len(observations),
        "lineage_count": lineage_count,
        "model_id": model.id,
        "runtime_config_id": runtime_config.id,
        "adapter": adapter_name,
        "adapter_name": adapter.name,
        "adapter_version": adapter.version,
        "observation_ids": [observation.id for observation in observations],
        "diagnostics": result.diagnostics,
        "source_detection_run_id": source_detection_run_id,
    }


def _get_or_create_fixture_pose_model(session: Session) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == "fixture-coco17-pose-adapter",
            ModelRegistry.version == "normalization-v0",
            ModelRegistry.model_family == "pose",
        )
    )
    if model is not None:
        return model

    model = ModelRegistry(
        name="fixture-coco17-pose-adapter",
        version="normalization-v0",
        model_family="pose",
        source="apps.worker.services.pose_adapter",
        metadata_jsonb={
            "adapter": "fixture_pose",
            "model_runtime": "fixture",
            "model_task": "pose",
            "model_family": "pose",
            "skeleton_format": "coco17",
            "skeleton_version": COCO17_VERSION,
            "keypoint_schema_json": skeleton_schema_json(),
            "blueprint": 4,
            "milestone": "4C",
            "frame_time_owner": "media_indexing",
            "normalization_only": True,
            "no_real_pose_inference": True,
        },
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    model: ModelRegistry,
    config_name: str,
    config_version: str,
    adapter: FixturePoseAdapter,
    frame_sample_rate: int,
    max_frames: int | None,
    source_detection_run_id: str | None,
    link_source_detections: bool,
) -> RuntimeConfig:
    payload = default_pose_runtime_config_payload(
        model_registry_id=model.id,
        frame_sample_policy="frame_sample_rate",
        subject_source_mode=(
            "player_detection_crop" if link_source_detections else "full_frame"
        ),
    )
    payload.update(
        {
            "adapter": "fixture_pose",
            "adapter_name": adapter.name,
            "adapter_version": adapter.version,
            "frame_sample_rate": frame_sample_rate,
            "max_frames": max_frames,
            "source_detection_run_id": source_detection_run_id,
            "link_source_detections": link_source_detections,
            "normalization_only": True,
            "no_real_pose_inference": True,
            "milestone": "4C",
        }
    )
    runtime_config = RuntimeConfig(
        config_name=config_name,
        config_version=config_version,
        payload_jsonb=payload,
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _create_run(
    *,
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    adapter: FixturePoseAdapter,
    source_detection_run_id: str | None,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": adapter.name,
            "source": "worker pose adapter",
            "source_detection_run_id": source_detection_run_id,
            "frame_time_owner": "media_indexing",
            "blueprint": 4,
            "milestone": "4C",
            "normalization_only": True,
            "no_real_pose_inference": True,
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
    adapter: FixturePoseAdapter,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="pose_adapter_persistence",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": adapter.name,
            "adapter_version": adapter.version,
            "frame_time_owner": "media_indexing",
            "normalization_only": True,
            "no_real_pose_inference": True,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _fixture_frame_results(
    *,
    session: Session,
    media: MediaAsset,
    frame_sample_rate: int,
    max_frames: int | None,
    source_detection_run_id: str | None,
    link_source_detections: bool,
) -> list[dict[str, Any]]:
    if source_detection_run_id and link_source_detections:
        detections = _source_player_detections(
            session=session,
            media=media,
            source_detection_run_id=source_detection_run_id,
            max_frames=max_frames,
        )
        return [
            _linked_fixture_frame_result(media, detection, index)
            for index, detection in enumerate(detections)
        ]

    sampled_frames = _sampled_frames(media, frame_sample_rate, max_frames)
    return [
        _full_frame_fixture_result(media, frame_number, index)
        for index, frame_number in enumerate(sampled_frames)
    ]


def _source_player_detections(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str,
    max_frames: int | None,
) -> list[Observation]:
    source_run = session.get(ProcessingRun, source_detection_run_id)
    if source_run is None:
        raise PoseAdapterRunError(f"source detection run not found: {source_detection_run_id}")
    if source_run.media_id != media.id:
        raise PoseAdapterRunError(
            "source detection run media_id does not match pose media_id: "
            f"{source_detection_run_id}"
        )

    rows = session.scalars(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == source_detection_run_id,
            Observation.observation_type == "player_detection",
        )
        .order_by(Observation.frame_start, Observation.id)
    ).all()
    if max_frames is not None:
        return list(rows[:max_frames])
    return list(rows)


def _sampled_frames(
    media: MediaAsset,
    frame_sample_rate: int,
    max_frames: int | None,
) -> list[int]:
    frame_count = (
        media.frame_count if media.frame_count is not None and media.frame_count > 0 else 1
    )
    frames = list(range(0, frame_count, frame_sample_rate))
    if not frames:
        frames = [0]
    if max_frames is not None:
        frames = frames[:max_frames]
    return frames


def _full_frame_fixture_result(
    media: MediaAsset,
    frame_number: int,
    source_result_index: int,
) -> dict[str, Any]:
    image_width = media.width or 1280
    image_height = media.height or 720
    bbox = _fixture_bbox(image_width=image_width, image_height=image_height)
    return {
        "frame_number": frame_number,
        "timestamp_ms": frame_to_timestamp_ms(media.fps or 30.0, frame_number),
        "image_width": image_width,
        "image_height": image_height,
        "poses": [
            {
                "bbox_xyxy": [
                    bbox["x"],
                    bbox["y"],
                    bbox["x"] + bbox["width"],
                    bbox["y"] + bbox["height"],
                ],
                "bbox_confidence": 0.86,
                "pose_confidence": 0.82,
                "source_result_index": source_result_index,
                "keypoints": _fixture_raw_keypoints(
                    width=image_width,
                    height=image_height,
                    origin_x=0.0,
                    origin_y=0.0,
                ),
            }
        ],
    }


def _linked_fixture_frame_result(
    media: MediaAsset,
    detection: Observation,
    source_result_index: int,
) -> dict[str, Any]:
    payload = _merged_payload(detection)
    bbox = _bbox(payload)
    if bbox is None:
        raise PoseAdapterRunError(
            f"source player_detection observation {detection.id} has no usable bbox"
        )
    frame_number = detection.frame_start
    timestamp_ms = detection.timestamp_start_ms
    if frame_number is None or timestamp_ms is None:
        raise PoseAdapterRunError(
            f"source player_detection observation {detection.id} is missing frame/time"
        )
    image_width = media.width or 1280
    image_height = media.height or 720
    return {
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "image_width": image_width,
        "image_height": image_height,
        "poses": [
            {
                "bbox_xyxy": [
                    bbox["x"],
                    bbox["y"],
                    bbox["x"] + bbox["width"],
                    bbox["y"] + bbox["height"],
                ],
                "bbox_confidence": detection.confidence,
                "pose_confidence": detection.confidence,
                "source_result_index": source_result_index,
                "keypoint_coordinate_space": "crop_pixels",
                "crop": {
                    "x": bbox["x"],
                    "y": bbox["y"],
                    "width": bbox["width"],
                    "height": bbox["height"],
                    "source": "player_detection",
                },
                "subject_context": {
                    "subject_ref_type": "player_detection",
                    "subject_detection_observation_id": detection.id,
                    "association_status": "candidate",
                    "association_method": "crop_from_player_detection",
                    "association_confidence": detection.confidence,
                },
                "keypoints": _fixture_raw_keypoints(
                    width=bbox["width"],
                    height=bbox["height"],
                    origin_x=0.0,
                    origin_y=0.0,
                ),
            }
        ],
    }


def _persist_poses(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    result: PoseAdapterResult,
) -> list[Any]:
    requests: list[ObservationCreate] = []
    for index, normalized_pose in enumerate(result.poses):
        pose = _pose_create_with_service_metadata(
            normalized_pose.as_pose_observation_create(),
            model_id=model.id,
            runtime_config_id=runtime_config.id,
            adapter_name=result.adapter_name,
            adapter_version=result.adapter_version,
        )
        lineage = _lineage_for_pose(session=session, pose=pose, step=step)
        requests.append(
            ObservationCreate(
                media_id=media.id,
                run_id=run.id,
                observation_family="pose",
                observation_type="player_pose_observation",
                granularity="frame",
                frame_start=pose.frame_number,
                frame_end=pose.frame_number,
                timestamp_start_ms=pose.timestamp_ms,
                timestamp_end_ms=pose.timestamp_ms,
                confidence=pose.pose_confidence,
                model_id=model.id,
                runtime_config_id=runtime_config.id,
                coordinate_space="image_pixels",
                payload_jsonb=_pose_payload(pose=pose, lineage=lineage),
                idempotency_key=(
                    f"{run.id}:pose-adapter:{result.adapter_name}:"
                    f"{index}:{pose.frame_number}:{pose.subject_detection_observation_id or 'none'}"
                ),
                pose=pose,
                lineage=lineage,
            )
        )

    writer = ObservationWriter(session)
    return [writer.write(request) for request in requests]


def _pose_create_with_service_metadata(
    pose: PoseObservationCreate,
    *,
    model_id: str,
    runtime_config_id: str,
    adapter_name: str,
    adapter_version: str,
) -> PoseObservationCreate:
    metadata = {
        **pose.metadata_jsonb,
        "adapter": adapter_name,
        "adapter_version": adapter_version,
        "source_runtime": "fixture_pose",
        "model_registry_id": model_id,
        "runtime_config_id": runtime_config_id,
        "normalization_only": True,
        "no_real_pose_inference": True,
        "frame_time_owner": "media_indexing",
        "blueprint": 4,
        "milestone": "4C",
    }
    return pose.model_copy(update={"metadata_jsonb": metadata})


def _lineage_for_pose(
    *,
    session: Session,
    pose: PoseObservationCreate,
    step: ProcessingStep,
) -> list[ObservationLineageCreate]:
    lineage: list[ObservationLineageCreate] = []
    if pose.subject_detection_observation_id:
        source = session.get(Observation, pose.subject_detection_observation_id)
        if source is None:
            raise PoseAdapterRunError(
                "source detection observation not found: "
                f"{pose.subject_detection_observation_id}"
            )
        if source.observation_type != "player_detection":
            raise PoseAdapterRunError(
                "pose source detection must be a player_detection observation: "
                f"{pose.subject_detection_observation_id}"
            )
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=source.id,
                relationship_type="pose_from_subject_detection_candidate",
                processing_step_id=step.id,
                payload_jsonb={
                    "source_observation_type": source.observation_type,
                    "frame_number": pose.frame_number,
                    "association_status": pose.association_status,
                    "association_method": pose.association_method,
                    "frame_time_owner": "media_indexing",
                },
            )
        )

    if pose.subject_tracklet_id:
        tracklet = session.get(Tracklet, pose.subject_tracklet_id)
        if tracklet is None or tracklet.observation_id is None:
            raise PoseAdapterRunError(
                f"source tracklet observation not found: {pose.subject_tracklet_id}"
            )
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=tracklet.observation_id,
                relationship_type="subject_context_candidate",
                processing_step_id=step.id,
                payload_jsonb={
                    "tracklet_id": tracklet.id,
                    "association_status": pose.association_status,
                    "association_method": pose.association_method,
                    "frame_time_owner": "media_indexing",
                },
            )
        )

    if pose.subject_track_point_id:
        track_point = session.get(TrackPoint, pose.subject_track_point_id)
        if track_point is None or track_point.observation_id is None:
            raise PoseAdapterRunError(
                f"source track point observation not found: {pose.subject_track_point_id}"
            )
        lineage.append(
            ObservationLineageCreate(
                parent_observation_id=track_point.observation_id,
                relationship_type="pose_from_track_point_candidate",
                processing_step_id=step.id,
                payload_jsonb={
                    "track_point_id": track_point.id,
                    "association_status": pose.association_status,
                    "association_method": pose.association_method,
                    "frame_time_owner": "media_indexing",
                },
            )
        )

    return lineage


def _pose_payload(
    *,
    pose: PoseObservationCreate,
    lineage: list[ObservationLineageCreate],
) -> dict[str, Any]:
    bbox = None
    if pose.bbox_x is not None and pose.bbox_y is not None:
        bbox = {
            "x": pose.bbox_x,
            "y": pose.bbox_y,
            "width": pose.bbox_w,
            "height": pose.bbox_h,
            "confidence": pose.bbox_confidence,
        }
    return {
        "skeleton_format": pose.skeleton_format,
        "skeleton_version": pose.skeleton_version,
        "keypoint_count": pose.keypoint_count,
        "keypoints_present_count": pose.keypoints_present_count,
        "keypoints_missing_count": pose.keypoints_missing_count,
        "mean_keypoint_confidence": pose.mean_keypoint_confidence,
        "min_keypoint_confidence": pose.min_keypoint_confidence,
        "max_keypoint_confidence": pose.max_keypoint_confidence,
        "pose_confidence": pose.pose_confidence,
        "bbox": bbox,
        "subject_ref_type": pose.subject_ref_type,
        "subject_detection_observation_id": pose.subject_detection_observation_id,
        "subject_tracklet_id": pose.subject_tracklet_id,
        "subject_track_point_id": pose.subject_track_point_id,
        "association_status": pose.association_status,
        "association_method": pose.association_method,
        "association_confidence": pose.association_confidence,
        "frame_time_owner": "media_indexing",
        "source_runtime": "fixture_pose",
        "normalization_only": True,
        "lineage": [
            {
                "parent_observation_id": row.parent_observation_id,
                "relationship_type": row.relationship_type,
            }
            for row in lineage
        ],
        "metadata": pose.metadata_jsonb,
    }


def _fixture_bbox(*, image_width: int, image_height: int) -> dict[str, float]:
    width = max(120.0, image_width * 0.14)
    height = max(280.0, image_height * 0.6)
    return {
        "x": max(0.0, image_width * 0.44 - width / 2),
        "y": max(0.0, image_height * 0.18),
        "width": min(width, float(image_width)),
        "height": min(height, float(image_height)),
    }


def _fixture_raw_keypoints(
    *,
    width: float,
    height: float,
    origin_x: float,
    origin_y: float,
) -> list[dict[str, Any]]:
    missing_names = {"right_wrist", "left_ankle"}
    keypoints: list[dict[str, Any]] = []
    for index, name in enumerate(COCO17_KEYPOINT_NAMES):
        if name in missing_names:
            keypoints.append({"present": False})
            continue
        column = index % 3
        row = index // 3
        x = origin_x + width * (0.35 + column * 0.15)
        y = origin_y + height * (0.12 + row * 0.11)
        keypoints.append(
            {
                "x": round(x, 3),
                "y": round(y, 3),
                "confidence": round(max(0.55, 0.92 - index * 0.02), 3),
            }
        )
    return keypoints


def _merged_payload(observation: Observation) -> dict[str, Any]:
    atomic_payload = (
        observation.atomic_detail.payload_jsonb
        if observation.atomic_detail is not None
        else {}
    )
    return {**observation.payload_jsonb, **atomic_payload}


def _bbox(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if isinstance(value, dict):
        x = _number(value.get("x"))
        y = _number(value.get("y"))
        width = _number(value.get("width"))
        height = _number(value.get("height"))
        if (
            x is not None
            and y is not None
            and width is not None
            and height is not None
            and width > 0
            and height > 0
        ):
            return {
                "x": float(x),
                "y": float(y),
                "width": float(width),
                "height": float(height),
            }
    if isinstance(value, list | tuple) and len(value) >= 4:
        x = _number(value[0])
        y = _number(value[1])
        width = _number(value[2])
        height = _number(value[3])
        if (
            x is not None
            and y is not None
            and width is not None
            and height is not None
            and width > 0
            and height > 0
        ):
            return {
                "x": float(x),
                "y": float(y),
                "width": float(width),
                "height": float(height),
            }
    return None


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    result: PoseAdapterResult,
    pose_observation_count: int,
    lineage_count: int,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "pose_observation_count": pose_observation_count,
        "lineage_count": lineage_count,
        "diagnostics": result.diagnostics,
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "pose_observation_count": pose_observation_count,
        "lineage_count": lineage_count,
        "diagnostics": result.diagnostics,
    }
    session.commit()


def _mark_failed(
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    error_message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "error": error_message,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "error": error_message,
    }
    session.commit()
