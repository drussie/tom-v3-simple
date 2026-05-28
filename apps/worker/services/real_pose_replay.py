from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_model_adapters.pose_inference import (
    FakePoseResultProvider,
    PoseResultProvider,
    UltralyticsPoseResultProvider,
)
from tom_v3_model_adapters.pose_normalization import (
    PoseAdapterResult,
    PoseNormalizationAdapter,
)
from tom_v3_model_adapters.yolo_inference import (
    FrameInferenceInput,
    MetadataOnlyYoloFrameSource,
    OpenCvYoloFrameSource,
    YoloFrameSource,
    sample_frame_numbers,
)
from tom_v3_model_adapters.yolo_runtime import probe_yolo_runtime
from tom_v3_model_adapters.yolo_weights import (
    YoloWeightsValidationError,
    YoloWeightsValidationResult,
    validate_yolo_weights,
)
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_schema.pose import PoseObservationCreate, default_pose_runtime_config_payload
from tom_v3_schema.skeletons import COCO17_VERSION, skeleton_schema_json
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
)
from tom_v3_video.paths import local_path_from_uri_or_path
from tom_v3_video.time_index import frame_to_timestamp_ms

REAL_POSE_SOURCE_RUNTIME = "ultralytics_pose"
REAL_POSE_WARNINGS = {
    "observation_only": True,
    "no_adjudication": True,
    "pose_keypoints_not_movement_interpretation": True,
    "model_output_not_truth": True,
    "no_fixture_fallback": True,
}


class RealPoseReplayError(ValueError):
    pass


def build_real_pose_replay_plan(
    media_id: str = "<media_id>",
    weights_path: str = "model_assets/pose/<weights_file>.pt",
    source_detection_run_id: str | None = "<source_detection_run_id>",
    model_name: str | None = None,
    model_version: str = "v0",
    device: str = "auto",
    imgsz: int | None = None,
    conf: float = 0.25,
    iou: float | None = 0.7,
    every_n_frames: int = 1,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 120,
    mode: str = "crop_from_player_detection",
    fallback_to_full_frame: bool = False,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    command_parts = [
        "python -m apps.worker.cli run-real-pose",
        f"--media-id {media_id}",
        f"--weights {weights_path}",
        f"--mode {mode}",
        f"--device {device}",
        f"--every-n-frames {every_n_frames}",
    ]
    if source_detection_run_id:
        command_parts.append(f"--source-detection-run-id {source_detection_run_id}")
    if model_name:
        command_parts.append(f"--model-name {model_name}")
    if model_version:
        command_parts.append(f"--model-version {model_version}")
    if imgsz is not None:
        command_parts.append(f"--imgsz {imgsz}")
    command_parts.append(f"--conf {conf}")
    if iou is not None:
        command_parts.append(f"--iou {iou}")
    if frame_start is not None:
        command_parts.append(f"--frame-start {frame_start}")
    if frame_end is not None:
        command_parts.append(f"--frame-end {frame_end}")
    if max_frames is not None:
        command_parts.append(f"--max-frames {max_frames}")
    if fallback_to_full_frame:
        command_parts.append("--fallback-to-full-frame")

    return {
        "steps": [
            "validate_media",
            "probe_pose_runtime",
            "validate_pose_weights",
            "register_pose_model",
            "sample_media_owned_frames_or_source_player_detections",
            "run_ultralytics_pose",
            "normalize_coco17_keypoints",
            "persist_pose_observations",
            "open_replay_workstation",
        ],
        "command": " ".join(command_parts),
        "mode": mode,
        "sampling": {
            "mode": "every_n_frames",
            "every_n_frames": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "frame_time_owner": "media_indexing",
        },
        "runtime": {
            "source_runtime": REAL_POSE_SOURCE_RUNTIME,
            "device": device,
            "imgsz": imgsz,
            "conf": conf,
            "iou": iou,
            "requires_yolo": True,
            "requires_pose_weights": True,
        },
        "source_detection_run_id": source_detection_run_id,
        "fallback_to_full_frame": fallback_to_full_frame,
        "replay_url_template": (
            f"{viewer_base_url}/replay/{media_id}?"
            "detectionRunId=<source_detection_run_id>&poseRunId=<pose_run_id>"
        ),
        "warnings": dict(REAL_POSE_WARNINGS),
    }


def run_real_pose_replay(
    session: Session,
    media_id: str,
    weights_path: str | None,
    source_detection_run_id: str | None = None,
    model_name: str | None = None,
    model_version: str = "v0",
    required_sha256: str | None = None,
    device: str = "auto",
    imgsz: int | None = None,
    conf: float = 0.25,
    iou: float | None = 0.7,
    every_n_frames: int = 1,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 120,
    mode: str = "crop_from_player_detection",
    fallback_to_full_frame: bool = False,
    allowed_roots: Sequence[str] | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
    probe_runtime: Callable[..., dict[str, Any]] = probe_yolo_runtime,
    pose_result_provider: PoseResultProvider | None = None,
    pose_frame_source: YoloFrameSource | None = None,
) -> dict[str, Any]:
    normalized_mode = _normalize_mode(mode)
    plan = build_real_pose_replay_plan(
        media_id=media_id,
        weights_path=weights_path or "model_assets/pose/<weights_file>.pt",
        source_detection_run_id=source_detection_run_id,
        model_name=model_name,
        model_version=model_version,
        device=device,
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
        mode=normalized_mode,
        fallback_to_full_frame=fallback_to_full_frame,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "real pose replay run planned",
            "plan": plan,
            "warnings": dict(REAL_POSE_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    runtime_probe = probe_runtime(requested_device=device)
    if runtime_probe.get("status") != "ok":
        return _failed(
            "pose_runtime_unavailable",
            "Ultralytics pose runtime is unavailable; real pose replay was not run.",
            runtime_probe=runtime_probe,
        )

    if not weights_path:
        return _failed("missing_weights_path", "pose weights path is required.")

    try:
        weights_validation = validate_yolo_weights(
            weights_path,
            allowed_roots=list(allowed_roots) if allowed_roots else None,
            required_sha256=required_sha256,
        )
    except YoloWeightsValidationError as exc:
        return _failed(
            status=exc.result.status,
            message=str(exc),
            error_type=exc.__class__.__name__,
            weights_validation=exc.result.as_dict(),
            runtime_probe=runtime_probe,
        )

    if normalized_mode == "crop_from_player_detection":
        source_validation = _validate_source_detection_run(
            session=session,
            media=media,
            source_detection_run_id=source_detection_run_id,
        )
        if source_validation.get("ok") is False:
            if not fallback_to_full_frame:
                return _failed(
                    source_validation["status"],
                    source_validation["message"],
                    runtime_probe=runtime_probe,
                    weights_validation=weights_validation.as_dict(),
                )
            normalized_mode = "full_frame"

    run: ProcessingRun | None = None
    step: ProcessingStep | None = None
    try:
        model = _register_pose_model(
            session=session,
            weights_validation=weights_validation,
            model_name=model_name or Path(weights_validation.resolved_path).stem,
            model_version=model_version,
            runtime_probe=runtime_probe,
            device=device,
        )
        runtime_config = _create_runtime_config(
            session=session,
            model=model,
            weights_validation=weights_validation,
            device=device,
            imgsz=imgsz,
            conf=conf,
            iou=iou,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
            mode=normalized_mode,
            source_detection_run_id=source_detection_run_id,
            fallback_to_full_frame=fallback_to_full_frame,
        )
        run = _create_run(
            session=session,
            media=media,
            runtime_config=runtime_config,
            source_detection_run_id=source_detection_run_id,
            mode=normalized_mode,
        )
        step = _create_step(
            session=session,
            run=run,
            runtime_config=runtime_config,
            mode=normalized_mode,
        )
        provider = pose_result_provider or UltralyticsPoseResultProvider(
            weights_path=weights_validation.resolved_path,
            device=device,
            image_size=imgsz,
            confidence_threshold=conf,
            iou_threshold=iou,
            max_det=None,
        )
        frame_results, inference_summary = _build_frame_results(
            session=session,
            media=media,
            source_detection_run_id=source_detection_run_id,
            mode=normalized_mode,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
            provider=provider,
            frame_source=pose_frame_source,
        )
        adapter = PoseNormalizationAdapter()
        normalization = adapter.normalize_results(
            frame_results,
            model_registry_id=model.id,
            runtime_config_id=runtime_config.id,
            inference_metadata={
                "adapter": "real_pose_replay",
                "adapter_version": "v0",
                "source_runtime": REAL_POSE_SOURCE_RUNTIME,
                "real_model_output": True,
                "model_output_not_truth": True,
                "frame_time_owner": "media_indexing",
                "weights_sha256": weights_validation.sha256,
                "device": device,
                "imgsz": imgsz,
                "conf": conf,
                "iou": iou,
                "mode": normalized_mode,
            },
        )
        result = PoseAdapterResult(
            adapter_name="real-pose-replay",
            adapter_version="v0",
            poses=normalization.poses,
            diagnostics={
                "adapter_name": "real-pose-replay",
                "adapter_version": "v0",
                "input_pose_count": normalization.input_pose_count,
                "normalized_pose_count": normalization.normalized_pose_count,
                "skipped_pose_count": normalization.skipped_pose_count,
                "warnings": normalization.warnings,
                "source_runtime": REAL_POSE_SOURCE_RUNTIME,
                "real_model_output": True,
                "model_output_not_truth": True,
                **inference_summary,
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
        if run is not None and step is not None:
            _mark_failed(session, run, step, str(exc))
        return _failed(
            "failed",
            str(exc),
            error_type=exc.__class__.__name__,
            runtime_probe=runtime_probe,
            weights_validation=weights_validation.as_dict(),
        )

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
    replay_url = _replay_url(
        viewer_base_url=viewer_base_url,
        media_id=media.id,
        source_detection_run_id=source_detection_run_id,
        pose_run_id=run.id,
        tracklet_run_id=_find_tracklet_run_id(session, source_detection_run_id),
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "real pose replay run complete",
        "media_id": media.id,
        "pose_run_id": run.id,
        "source_detection_run_id": source_detection_run_id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            "player_pose_observation": len(observations),
            "total": len(observations),
        },
        "summary": {
            **result.diagnostics,
            "pose_observation_count": len(observations),
            "lineage_count": lineage_count,
            "device": device,
            "weights_sha256": weights_validation.sha256,
            "observation_only": True,
            "no_adjudication": True,
        },
        "weights_validation": weights_validation.as_dict(),
        "runtime_probe": runtime_probe,
        "run_label": "real pose model output run",
        "replay_url": replay_url,
        "warnings": dict(REAL_POSE_WARNINGS),
    }


def _normalize_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized not in {"crop_from_player_detection", "full_frame"}:
        raise RealPoseReplayError(
            "pose mode must be crop_from_player_detection or full_frame"
        )
    return normalized


def _validate_source_detection_run(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str | None,
) -> dict[str, Any]:
    if not source_detection_run_id:
        return {
            "ok": False,
            "status": "missing_source_detection_run",
            "message": "source detection run id is required in crop_from_player_detection mode.",
        }
    source_run = session.get(ProcessingRun, source_detection_run_id)
    if source_run is None:
        return {
            "ok": False,
            "status": "missing_source_detection_run",
            "message": f"source detection run not found: {source_detection_run_id}",
        }
    if source_run.media_id != media.id:
        return {
            "ok": False,
            "status": "source_detection_run_media_mismatch",
            "message": "source detection run media_id does not match pose media_id.",
        }
    count = session.scalar(
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == source_detection_run_id,
            Observation.observation_type == "player_detection",
        )
        .limit(1)
    )
    if count is None:
        return {
            "ok": False,
            "status": "no_source_player_detections",
            "message": "source detection run contains no player_detection observations.",
        }
    return {"ok": True}


def _register_pose_model(
    *,
    session: Session,
    weights_validation: YoloWeightsValidationResult,
    model_name: str,
    model_version: str,
    runtime_probe: dict[str, Any],
    device: str,
) -> ModelRegistry:
    existing = session.scalars(
        select(ModelRegistry).where(
            ModelRegistry.name == model_name,
            ModelRegistry.version == model_version,
            ModelRegistry.model_family == "pose",
            ModelRegistry.source == "tom_v3_model_adapters.pose_inference",
        )
    ).all()
    for model in existing:
        metadata = model.metadata_jsonb or {}
        if (
            metadata.get("weights_sha256") == weights_validation.sha256
            and metadata.get("model_runtime") == "ultralytics"
        ):
            return model

    metadata = {
        "model_family": "pose",
        "model_runtime": "ultralytics",
        "model_task": "pose",
        "model_name": model_name,
        "model_version": model_version,
        "weights_path": weights_validation.weights_path,
        "weights_resolved_path": weights_validation.resolved_path,
        "weights_sha256": weights_validation.sha256,
        "weights_size_bytes": weights_validation.size_bytes,
        "skeleton_format": "coco17",
        "skeleton_version": COCO17_VERSION,
        "keypoint_schema": skeleton_schema_json(),
        "source_runtime": REAL_POSE_SOURCE_RUNTIME,
        "runtime_probe": runtime_probe,
        "device": device,
        "real_model_output": True,
        "model_output_not_truth": True,
        "frame_time_owner": "media_indexing",
        "blueprint": 7,
        "milestone": "7D",
    }
    model = ModelRegistry(
        name=model_name,
        version=model_version,
        model_family="pose",
        source="tom_v3_model_adapters.pose_inference",
        metadata_jsonb=metadata,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_runtime_config(
    *,
    session: Session,
    model: ModelRegistry,
    weights_validation: YoloWeightsValidationResult,
    device: str,
    imgsz: int | None,
    conf: float,
    iou: float | None,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    mode: str,
    source_detection_run_id: str | None,
    fallback_to_full_frame: bool,
) -> RuntimeConfig:
    payload = default_pose_runtime_config_payload(
        model_registry_id=model.id,
        weights_path=weights_validation.resolved_path,
        device=device,
        frame_sample_policy="every_n_frames",
        subject_source_mode=mode,
    )
    payload.update(
        {
            "adapter": "real_pose_replay",
            "adapter_version": "v0",
            "source_runtime": REAL_POSE_SOURCE_RUNTIME,
            "weights_sha256": weights_validation.sha256,
            "weights_size_bytes": weights_validation.size_bytes,
            "imgsz": imgsz,
            "conf": conf,
            "iou": iou,
            "every_n_frames": every_n_frames,
            "frame_sample_rate": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "mode": mode,
            "source_detection_run_id": source_detection_run_id,
            "fallback_to_full_frame": fallback_to_full_frame,
            "real_model_output": True,
            "model_output_not_truth": True,
            "pose_keypoints_not_movement_interpretation": True,
            "frame_time_owner": "media_indexing",
            "blueprint": 7,
            "milestone": "7D",
        }
    )
    runtime_config = RuntimeConfig(
        config_name="real-pose-replay-config",
        config_version="v0",
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
    source_detection_run_id: str | None,
    mode: str,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name="real-pose-replay",
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": "real-pose-replay",
            "source": "worker real pose replay",
            "source_runtime": REAL_POSE_SOURCE_RUNTIME,
            "source_detection_run_id": source_detection_run_id,
            "mode": mode,
            "evidence_source": "real_pose_model_output",
            "source_label": "real pose model output",
            "real_model_output": True,
            "model_output_not_truth": True,
            "pose_keypoints_not_movement_interpretation": True,
            "frame_time_owner": "media_indexing",
            "blueprint": 7,
            "milestone": "7D",
        },
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def _create_step(
    *,
    session: Session,
    run: ProcessingRun,
    runtime_config: RuntimeConfig,
    mode: str,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="real_pose_replay_persistence",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": "real-pose-replay",
            "adapter_version": "v0",
            "source_runtime": REAL_POSE_SOURCE_RUNTIME,
            "mode": mode,
            "real_model_output": True,
            "model_output_not_truth": True,
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _build_frame_results(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str | None,
    mode: str,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    provider: PoseResultProvider,
    frame_source: YoloFrameSource | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if mode == "crop_from_player_detection":
        return _crop_frame_results(
            session=session,
            media=media,
            source_detection_run_id=source_detection_run_id,
            every_n_frames=every_n_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            max_frames=max_frames,
            provider=provider,
            frame_source=frame_source,
        )
    return _full_frame_results(
        media=media,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
        provider=provider,
        frame_source=frame_source,
    )


def _crop_frame_results(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str | None,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    provider: PoseResultProvider,
    frame_source: YoloFrameSource | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    detections = _source_player_detections(
        session=session,
        media=media,
        source_detection_run_id=source_detection_run_id,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
    )
    if not detections:
        raise RealPoseReplayError("no source player_detection observations selected for pose")

    frame_numbers = sorted({int(detection.frame_start) for detection in detections})
    frame_inputs = _frame_inputs_by_number(
        media=media,
        sampled_frames=frame_numbers,
        provider=provider,
        frame_source=frame_source,
    )
    frame_results: list[dict[str, Any]] = []
    for detection in detections:
        payload = _merged_payload(detection)
        bbox = _bbox(payload)
        if bbox is None:
            raise RealPoseReplayError(
                f"source player_detection observation {detection.id} has no usable bbox"
            )
        frame_input = frame_inputs[int(detection.frame_start)]
        crop_input = _crop_frame_input(frame_input, bbox)
        raw_result = provider.predict_frame(crop_input)
        frame_results.append(
            _frame_result_with_source_context(
                raw_result=raw_result,
                media=media,
                frame_number=int(detection.frame_start),
                timestamp_ms=int(detection.timestamp_start_ms),
                bbox=bbox,
                detection=detection,
            )
        )

    return frame_results, {
        "mode": "crop_from_player_detection",
        "frames_considered": len(frame_numbers),
        "source_player_detections_considered": len(detections),
        "frames_processed": len(frame_results),
        "sampled_frames": frame_numbers,
        "source_detection_run_id": source_detection_run_id,
    }


def _full_frame_results(
    *,
    media: MediaAsset,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    provider: PoseResultProvider,
    frame_source: YoloFrameSource | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sampled_frames = sample_frame_numbers(
        media.frame_count or 0,
        every_n_frames,
        max_frames,
        frame_start=frame_start,
        frame_end=frame_end,
    )
    source = _frame_source(provider, frame_source)
    frame_results = [
        _frame_result_with_defaults(
            provider.predict_frame(frame_input),
            frame_input=frame_input,
            media=media,
        )
        for frame_input in source.iter_sampled_frames(
            _local_media_path(media),
            media.fps or 0,
            media.width,
            media.height,
            sampled_frames,
        )
    ]
    return frame_results, {
        "mode": "full_frame",
        "frames_considered": len(sampled_frames),
        "frames_processed": len(frame_results),
        "sampled_frames": sampled_frames,
    }


def _source_player_detections(
    *,
    session: Session,
    media: MediaAsset,
    source_detection_run_id: str | None,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
) -> list[Observation]:
    if source_detection_run_id is None:
        raise RealPoseReplayError("source detection run id is required in crop mode")
    if every_n_frames <= 0:
        raise RealPoseReplayError("every_n_frames must be greater than 0")
    resolved_start = 0 if frame_start is None else int(frame_start)
    resolved_end = None if frame_end is None else int(frame_end)
    if resolved_start < 0:
        raise RealPoseReplayError("frame_start must be greater than or equal to 0")
    if resolved_end is not None and resolved_end < 0:
        raise RealPoseReplayError("frame_end must be greater than or equal to 0")
    if resolved_end is not None and resolved_start > resolved_end:
        raise RealPoseReplayError("frame_start must be less than or equal to frame_end")

    query = (
        select(Observation)
        .where(
            Observation.media_id == media.id,
            Observation.run_id == source_detection_run_id,
            Observation.observation_type == "player_detection",
            Observation.frame_start.is_not(None),
            Observation.timestamp_start_ms.is_not(None),
        )
        .order_by(Observation.frame_start, Observation.id)
    )
    query = query.where(Observation.frame_start >= resolved_start)
    if resolved_end is not None:
        query = query.where(Observation.frame_start <= resolved_end)
    rows = list(session.scalars(query).all())
    if every_n_frames > 1:
        rows = [
            row
            for row in rows
            if row.frame_start is not None
            and (int(row.frame_start) - resolved_start) % every_n_frames == 0
        ]
    if max_frames is not None:
        rows = rows[: max(1, int(max_frames))]
    return rows


def _frame_inputs_by_number(
    *,
    media: MediaAsset,
    sampled_frames: list[int],
    provider: PoseResultProvider,
    frame_source: YoloFrameSource | None,
) -> dict[int, FrameInferenceInput]:
    source = _frame_source(provider, frame_source)
    return {
        frame_input.frame_number: frame_input
        for frame_input in source.iter_sampled_frames(
            _local_media_path(media),
            media.fps or 0,
            media.width,
            media.height,
            sampled_frames,
        )
    }


def _frame_source(
    provider: PoseResultProvider,
    frame_source: YoloFrameSource | None,
) -> YoloFrameSource:
    if frame_source is not None:
        return frame_source
    if isinstance(provider, FakePoseResultProvider):
        return MetadataOnlyYoloFrameSource()
    return OpenCvYoloFrameSource()


def _crop_frame_input(
    frame_input: FrameInferenceInput,
    bbox: dict[str, float],
) -> FrameInferenceInput:
    width = max(1, int(round(bbox["width"])))
    height = max(1, int(round(bbox["height"])))
    image = None
    if frame_input.image is not None:
        x1 = max(0, int(round(bbox["x"])))
        y1 = max(0, int(round(bbox["y"])))
        x2 = max(x1 + 1, int(round(bbox["x"] + bbox["width"])))
        y2 = max(y1 + 1, int(round(bbox["y"] + bbox["height"])))
        image = frame_input.image[y1:y2, x1:x2]
        try:
            height, width = image.shape[:2]
        except AttributeError:
            pass
    return FrameInferenceInput(
        frame_number=frame_input.frame_number,
        timestamp_ms=frame_input.timestamp_ms,
        image=image,
        image_width=width,
        image_height=height,
        source_path=frame_input.source_path,
        metadata={
            **frame_input.metadata,
            "crop_source": "player_detection",
            "crop_bbox": bbox,
        },
    )


def _frame_result_with_source_context(
    *,
    raw_result: Mapping[str, Any],
    media: MediaAsset,
    frame_number: int,
    timestamp_ms: int,
    bbox: dict[str, float],
    detection: Observation,
) -> dict[str, Any]:
    frame_result = _frame_result_with_defaults(
        raw_result,
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        media=media,
    )
    poses = []
    for pose in frame_result.get("poses", []):
        pose_dict = dict(pose)
        pose_dict["keypoint_coordinate_space"] = "crop_pixels"
        pose_dict.setdefault(
            "crop",
            {
                "x": bbox["x"],
                "y": bbox["y"],
                "width": bbox["width"],
                "height": bbox["height"],
                "source": "player_detection",
            },
        )
        pose_dict["subject_context"] = {
            **dict(pose_dict.get("subject_context") or {}),
            "subject_ref_type": "player_detection",
            "subject_detection_observation_id": detection.id,
            "association_status": "candidate",
            "association_method": "crop_from_player_detection",
            "association_confidence": detection.confidence,
        }
        poses.append(pose_dict)
    frame_result["poses"] = poses
    return frame_result


def _frame_result_with_defaults(
    raw_result: Mapping[str, Any],
    *,
    media: MediaAsset,
    frame_input: FrameInferenceInput | None = None,
    frame_number: int | None = None,
    timestamp_ms: int | None = None,
) -> dict[str, Any]:
    resolved_frame = int(
        raw_result.get("frame_number")
        if raw_result.get("frame_number") is not None
        else frame_number
        if frame_number is not None
        else frame_input.frame_number
        if frame_input is not None
        else 0
    )
    resolved_timestamp = int(
        raw_result.get("timestamp_ms")
        if raw_result.get("timestamp_ms") is not None
        else timestamp_ms
        if timestamp_ms is not None
        else frame_input.timestamp_ms
        if frame_input is not None
        else frame_to_timestamp_ms(media.fps or 30.0, resolved_frame)
    )
    return {
        "frame_number": resolved_frame,
        "timestamp_ms": resolved_timestamp,
        "image_width": raw_result.get("image_width") or media.width,
        "image_height": raw_result.get("image_height") or media.height,
        "poses": list(raw_result.get("poses") or []),
        "skeleton_format": raw_result.get("skeleton_format") or "coco17",
        "skeleton_version": raw_result.get("skeleton_version") or COCO17_VERSION,
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
        pose = _pose_create_with_real_metadata(
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
                    f"{run.id}:real-pose:{index}:{pose.frame_number}:"
                    f"{pose.subject_detection_observation_id or 'none'}"
                ),
                pose=pose,
                lineage=lineage,
            )
        )
    writer = ObservationWriter(session)
    return [writer.write(request) for request in requests]


def _pose_create_with_real_metadata(
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
        "source_runtime": REAL_POSE_SOURCE_RUNTIME,
        "evidence_source": "real_pose_model_output",
        "source_label": "real pose model output",
        "model_registry_id": model_id,
        "runtime_config_id": runtime_config_id,
        "real_model_output": True,
        "model_output_not_truth": True,
        "pose_keypoints_not_movement_interpretation": True,
        "frame_time_owner": "media_indexing",
        "blueprint": 7,
        "milestone": "7D",
    }
    raw_model_payload = {
        **pose.raw_model_payload_jsonb,
        "source_runtime": REAL_POSE_SOURCE_RUNTIME,
        "real_model_output": True,
        "model_output_not_truth": True,
    }
    return pose.model_copy(
        update={
            "metadata_jsonb": metadata,
            "raw_model_payload_jsonb": raw_model_payload,
        }
    )


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
            raise RealPoseReplayError(
                "source detection observation not found: "
                f"{pose.subject_detection_observation_id}"
            )
        if source.observation_type != "player_detection":
            raise RealPoseReplayError(
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
                    "source_detection_run_id": source.run_id,
                    "source_runtime": REAL_POSE_SOURCE_RUNTIME,
                    "real_model_output": True,
                    "model_output_not_truth": True,
                    "frame_number": pose.frame_number,
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
        "source_runtime": REAL_POSE_SOURCE_RUNTIME,
        "evidence_source": "real_pose_model_output",
        "source_label": "real pose model output",
        "real_model_output": True,
        "model_output_not_truth": True,
        "pose_keypoints_not_movement_interpretation": True,
        "lineage": [
            {
                "parent_observation_id": row.parent_observation_id,
                "relationship_type": row.relationship_type,
            }
            for row in lineage
        ],
        "metadata": pose.metadata_jsonb,
    }


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
    counts = Counter({"player_pose_observation": pose_observation_count})
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "pose_observation_count": pose_observation_count,
        "lineage_count": lineage_count,
        "diagnostics": result.diagnostics,
        "counts_by_observation_type": dict(counts),
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
    run.metadata_jsonb = {**run.metadata_jsonb, "error": error_message}
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {**step.metadata_jsonb, "error": error_message}
    session.commit()


def _find_tracklet_run_id(session: Session, source_detection_run_id: str | None) -> str | None:
    if source_detection_run_id is None:
        return None
    run = session.scalar(
        select(ProcessingRun)
        .join(Tracklet, Tracklet.run_id == ProcessingRun.id)
        .where(
            ProcessingRun.metadata_jsonb["source_detection_run_id"].as_string()
            == source_detection_run_id
        )
        .order_by(ProcessingRun.completed_at.desc(), ProcessingRun.id)
        .limit(1)
    )
    return None if run is None else run.id


def _replay_url(
    *,
    viewer_base_url: str,
    media_id: str,
    source_detection_run_id: str | None,
    pose_run_id: str,
    tracklet_run_id: str | None,
) -> str:
    params = []
    if source_detection_run_id:
        params.append(f"detectionRunId={source_detection_run_id}")
    if tracklet_run_id:
        params.append(f"trackletRunId={tracklet_run_id}")
    params.append(f"poseRunId={pose_run_id}")
    return f"{viewer_base_url}/replay/{media_id}?{'&'.join(params)}"


def _local_media_path(media: MediaAsset) -> str | None:
    metadata = media.metadata_jsonb or {}
    for key in ("stored_path", "original_source_path"):
        value = metadata.get(key)
        if value:
            return str(Path(value).expanduser())
    if media.source_uri.startswith("file://"):
        return str(local_path_from_uri_or_path(media.source_uri))
    return None


def _merged_payload(observation: Observation) -> dict[str, Any]:
    atomic_payload = (
        observation.atomic_detail.payload_jsonb
        if observation.atomic_detail is not None
        else {}
    )
    return {**observation.payload_jsonb, **atomic_payload}


def _bbox(payload: dict[str, Any]) -> dict[str, float] | None:
    value = payload.get("bbox")
    if not isinstance(value, dict):
        return None
    x = _number(value.get("x"))
    y = _number(value.get("y"))
    width = _number(value.get("width", value.get("w")))
    height = _number(value.get("height", value.get("h")))
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None
    return {"x": x, "y": y, "width": width, "height": height}


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _failed(
    status: str,
    message: str,
    error_type: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(REAL_POSE_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
