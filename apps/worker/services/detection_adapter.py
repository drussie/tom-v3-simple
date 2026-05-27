from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_model_adapters.detection import (
    DetectionAdapterInput,
    DetectionAdapterResult,
    DetectionObservation,
    get_detection_adapter,
)
from tom_v3_model_adapters.yolo_weights import validate_yolo_weights
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.artifacts import EvidenceArtifactCreate
from tom_v3_schema.observations import (
    AtomicObservationCreate,
    ObservationCreate,
    ObservationLineageCreate,
)
from tom_v3_storage.db_models import (
    GameplayObservation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.paths import local_path_from_uri_or_path


class DetectionAdapterRunError(ValueError):
    pass


def run_detection_adapter(
    session: Session,
    media_id: str,
    adapter_name: str = "fixture",
    run_name: str = "detection-adapter-run",
    config_name: str = "detection-adapter-config",
    config_version: str = "v0",
    model_path: str | None = None,
    model_registry_id: str | None = None,
    device: str | None = None,
    image_size: int | None = None,
    confidence_threshold: float = 0.25,
    iou_threshold: float | None = 0.7,
    max_det: int | None = 50,
    frame_sample_rate: int = 30,
    max_frames: int | None = 5,
    frame_start: int | None = None,
    frame_end: int | None = None,
    gameplay_run_id: str | None = None,
    output_debug_artifact: bool = False,
    yolo_result_provider: Any | None = None,
    yolo_frame_source: Any | None = None,
) -> dict[str, Any]:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise DetectionAdapterRunError(f"media asset not found: {media_id}")

    normalized_adapter_name = adapter_name.strip().lower()
    registered_model: ModelRegistry | None = None
    model_metadata: dict[str, Any] = {}
    class_map: dict[str, Any] | None = None
    weights_sha256: str | None = None
    if model_registry_id is not None:
        registered_model = session.get(ModelRegistry, model_registry_id)
        if registered_model is None:
            raise DetectionAdapterRunError(f"model registry row not found: {model_registry_id}")
        model_metadata = registered_model.metadata_jsonb or {}
        if normalized_adapter_name in {"yolo", "yolo26", "ultralytics"}:
            model_path = model_path or model_metadata.get("weights_resolved_path")
            model_path = model_path or model_metadata.get("weights_path")
            class_map = model_metadata.get("class_map")
            weights_sha256 = model_metadata.get("weights_sha256")
            if model_path:
                validate_yolo_weights(
                    weights_path=model_path,
                    allowed_roots=None,
                    required_sha256=weights_sha256,
                )

    adapter = get_detection_adapter(
        adapter_name,
        model_path=model_path,
        device=device,
        image_size=image_size,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold,
        max_det=max_det,
        model_registry_id=model_registry_id,
        yolo_result_provider=yolo_result_provider,
        yolo_frame_source=yolo_frame_source,
    )
    gameplay_segments = _load_gameplay_segments(session, gameplay_run_id)
    runtime_config = _create_runtime_config(
        session=session,
        adapter_name=adapter_name,
        config_name=config_name,
        config_version=config_version,
        model_path=model_path,
        model_registry_id=model_registry_id,
        device=device,
        image_size=image_size,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold,
        max_det=max_det,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        gameplay_run_id=gameplay_run_id,
        class_map=class_map,
        weights_sha256=weights_sha256,
    )
    model = registered_model or _get_or_create_model(
        session=session,
        adapter_name=adapter_name,
        adapter_runtime_name=adapter.name,
        adapter_version=adapter.version,
        model_path=model_path,
        device=device,
        image_size=image_size,
        confidence_threshold=confidence_threshold,
    )
    run = _create_run(session, media, runtime_config, run_name, adapter.name, gameplay_run_id)
    step = _create_step(session, run, runtime_config, adapter.name)

    try:
        result = adapter.run(_adapter_input(media, runtime_config, gameplay_segments))
        observations = _persist_detections(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            result=result,
            gameplay_segments=gameplay_segments,
            gameplay_run_id=gameplay_run_id,
            output_debug_artifact=output_debug_artifact,
        )
    except Exception as exc:
        _mark_failed(session, run, step, str(exc))
        raise

    _mark_completed(session, run, step, result)
    counts_by_label = dict(Counter(detection.label for detection in result.detections))
    counts_by_type = dict(
        Counter(_observation_type_for_label(detection.label) for detection in result.detections)
    )
    return {
        "media_id": media.id,
        "run_id": run.id,
        "model_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "adapter": adapter_name,
        "adapter_name": result.adapter_name,
        "adapter_version": result.adapter_version,
        "detection_count": len(result.detections),
        "counts_by_label": counts_by_label,
        "counts_by_observation_type": counts_by_type,
        "observation_ids": [observation.id for observation in observations],
        "diagnostics": result.diagnostics,
    }


def _create_runtime_config(
    session: Session,
    adapter_name: str,
    config_name: str,
    config_version: str,
    model_path: str | None,
    model_registry_id: str | None,
    device: str | None,
    image_size: int | None,
    confidence_threshold: float,
    iou_threshold: float | None,
    max_det: int | None,
    frame_sample_rate: int,
    max_frames: int | None,
    frame_start: int | None,
    frame_end: int | None,
    gameplay_run_id: str | None,
    class_map: dict[str, Any] | None,
    weights_sha256: str | None,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name=config_name,
        config_version=config_version,
        payload_jsonb={
            "adapter": adapter_name,
            "model_path": model_path,
            "weights_path": model_path,
            "model_registry_id": model_registry_id,
            "weights_sha256": weights_sha256,
            "device": device,
            "image_size": image_size,
            "confidence_threshold": confidence_threshold,
            "iou": iou_threshold,
            "iou_threshold": iou_threshold,
            "max_det": max_det,
            "frame_sample_rate": frame_sample_rate,
            "max_frames": max_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "frame_sampling": {
                "mode": "every_n_frames",
                "every_n_frames": frame_sample_rate,
                "frame_start": frame_start,
                "frame_end": frame_end,
                "max_frames": max_frames,
            },
            "gameplay_scope_run_id": gameplay_run_id,
            "class_map": class_map,
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(runtime_config)
    session.commit()
    session.refresh(runtime_config)
    return runtime_config


def _get_or_create_model(
    session: Session,
    adapter_name: str,
    adapter_runtime_name: str,
    adapter_version: str,
    model_path: str | None,
    device: str | None,
    image_size: int | None,
    confidence_threshold: float,
) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == adapter_runtime_name,
            ModelRegistry.version == adapter_version,
            ModelRegistry.model_family == "detection",
        )
    )
    if model is not None:
        return model

    metadata = {
        "adapter_type": adapter_name,
        "model_path": model_path,
        "weights_path": model_path,
        "runtime": "ultralytics" if adapter_name in {"yolo", "yolo26"} else "fixture",
        "device": device,
        "image_size": image_size,
        "confidence_threshold": confidence_threshold,
        "class_map": {
            "0": "ball",
            "1": "player",
        },
        "portability_status": (
            "unavailable_runtime_or_assets"
            if adapter_name in {"yolo", "yolo26", "ultralytics"}
            else "fixture_dev_only"
        ),
        "frame_time_owner": "media_indexing",
    }
    model = ModelRegistry(
        name=adapter_runtime_name,
        version=adapter_version,
        model_family="detection",
        source="tom_v3_model_adapters.detection",
        metadata_jsonb=metadata,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def _create_run(
    session: Session,
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    run_name: str,
    adapter_runtime_name: str,
    gameplay_run_id: str | None,
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": adapter_runtime_name,
            "source": "worker detection adapter",
            "rerun_behavior": "new run",
            "frame_time_owner": "media_indexing",
            "gameplay_scope_run_id": gameplay_run_id,
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
    adapter_runtime_name: str,
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="detection_adapter_inference",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": adapter_runtime_name,
            "frame_time_owner": "media_indexing",
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _adapter_input(
    media: MediaAsset,
    runtime_config: RuntimeConfig,
    gameplay_segments: list[dict[str, Any]],
) -> DetectionAdapterInput:
    metadata = media.metadata_jsonb or {}
    runtime_payload = dict(runtime_config.payload_jsonb or {})
    runtime_payload["runtime_config_id"] = runtime_config.id
    return DetectionAdapterInput(
        media_id=media.id,
        source_uri=media.source_uri,
        local_path=_local_media_path(media),
        fps=media.fps,
        frame_count=media.frame_count,
        duration_ms=media.duration_ms,
        width=media.width,
        height=media.height,
        runtime_config=runtime_payload,
        frame_time_summary=metadata.get("frame_time_index", {}),
        gameplay_segments=gameplay_segments,
        metadata=metadata,
    )


def _persist_detections(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    result: DetectionAdapterResult,
    gameplay_segments: list[dict[str, Any]],
    gameplay_run_id: str | None,
    output_debug_artifact: bool,
) -> list[Any]:
    writer = ObservationWriter(session)
    observations = []
    for index, detection in enumerate(result.detections):
        observation_type = _observation_type_for_label(detection.label)
        parent_gameplay = _gameplay_parent_for_frame(gameplay_segments, detection.frame_number)
        observation = writer.write(
            ObservationCreate(
                media_id=media.id,
                run_id=run.id,
                observation_family="atomic",
                observation_type=observation_type,
                granularity="frame",
                frame_start=detection.frame_number,
                frame_end=detection.frame_number,
                timestamp_start_ms=detection.timestamp_ms,
                timestamp_end_ms=detection.timestamp_ms,
                confidence=detection.confidence,
                model_id=model.id,
                runtime_config_id=runtime_config.id,
                coordinate_space="image_pixels",
                payload_jsonb=_detection_payload(
                    detection=detection,
                    result=result,
                    step=step,
                    detection_index=index,
                    gameplay_run_id=gameplay_run_id,
                    parent_gameplay=parent_gameplay,
                ),
                idempotency_key=(
                    f"{run.id}:detection-adapter:{result.adapter_name}:"
                    f"{index}:{detection.frame_number}:{detection.label}"
                ),
                atomic=AtomicObservationCreate(
                    atomic_kind=observation_type,
                    payload_jsonb=_atomic_payload(
                        detection=detection,
                        result=result,
                        step=step,
                        gameplay_run_id=gameplay_run_id,
                        parent_gameplay=parent_gameplay,
                    ),
                ),
                lineage=(
                    [
                        ObservationLineageCreate(
                            parent_observation_id=parent_gameplay["observation_id"],
                            relationship_type="scoped_by",
                            processing_step_id=step.id,
                            payload_jsonb={
                                "gameplay_scope_run_id": gameplay_run_id,
                                "frame_number": detection.frame_number,
                            },
                        )
                    ]
                    if parent_gameplay is not None
                    else []
                ),
                artifacts=(
                    [_debug_artifact(media, run, detection, result, index)]
                    if output_debug_artifact
                    else []
                ),
            )
        )
        observations.append(observation)
    return observations


def _detection_payload(
    detection: DetectionObservation,
    result: DetectionAdapterResult,
    step: ProcessingStep,
    detection_index: int,
    gameplay_run_id: str | None,
    parent_gameplay: dict[str, Any] | None,
) -> dict[str, Any]:
    inference = detection.metadata.get("inference") or {}
    return {
        "adapter_name": result.adapter_name,
        "adapter_version": result.adapter_version,
        "detection_index": detection_index,
        "processing_step_id": step.id,
        "frame_time_owner": "media_indexing",
        "label": detection.label,
        "bbox": detection.bbox.as_dict(),
        "center": detection.center.as_dict(),
        "class_id": detection.class_id,
        "class_label": detection.class_label,
        "source_runtime": detection.metadata.get("source_runtime"),
        "real_model_output": bool(detection.metadata.get("real_model_output")),
        "model_output_not_truth": bool(detection.metadata.get("real_model_output")),
        "source_result_index": detection.metadata.get("source_result_index"),
        "model_registry_id": detection.metadata.get("model_registry_id"),
        "runtime_config_id": detection.metadata.get("runtime_config_id"),
        "weights_sha256": inference.get("weights_sha256"),
        "inference": inference,
        "metadata": detection.metadata,
        "gameplay_scope_run_id": gameplay_run_id,
        "gameplay_scope": parent_gameplay,
    }


def _atomic_payload(
    detection: DetectionObservation,
    result: DetectionAdapterResult,
    step: ProcessingStep,
    gameplay_run_id: str | None,
    parent_gameplay: dict[str, Any] | None,
) -> dict[str, Any]:
    inference = detection.metadata.get("inference") or {}
    return {
        "bbox": detection.bbox.as_dict(),
        "center": detection.center.as_dict(),
        "class_label": detection.class_label,
        "class_id": detection.class_id,
        "source_runtime": detection.metadata.get("source_runtime"),
        "real_model_output": bool(detection.metadata.get("real_model_output")),
        "model_output_not_truth": bool(detection.metadata.get("real_model_output")),
        "source_result_index": detection.metadata.get("source_result_index"),
        "model_registry_id": detection.metadata.get("model_registry_id"),
        "runtime_config_id": detection.metadata.get("runtime_config_id"),
        "weights_sha256": inference.get("weights_sha256"),
        "inference": inference,
        "detector": {
            "adapter_name": result.adapter_name,
            "adapter_version": result.adapter_version,
            "processing_step_id": step.id,
            "label": detection.label,
            "metadata": detection.metadata,
        },
        "frame_time_owner": "media_indexing",
        "gameplay_scope_run_id": gameplay_run_id,
        "gameplay_scope": parent_gameplay,
    }


def _debug_artifact(
    media: MediaAsset,
    run: ProcessingRun,
    detection: DetectionObservation,
    result: DetectionAdapterResult,
    index: int,
) -> EvidenceArtifactCreate:
    inference = detection.metadata.get("inference") or {}
    return EvidenceArtifactCreate(
        media_id=media.id,
        run_id=run.id,
        artifact_type="detection_adapter_debug_json",
        uri=f"file:///dev/artifacts/detection/{run.id}/detection-{index}.json",
        frame_start=detection.frame_number,
        frame_end=detection.frame_number,
        timestamp_start_ms=detection.timestamp_ms,
        timestamp_end_ms=detection.timestamp_ms,
        metadata_jsonb={
            "adapter_name": result.adapter_name,
            "adapter_version": result.adapter_version,
            "label": detection.label,
            "bbox": detection.bbox.as_dict(),
            "center": detection.center.as_dict(),
            "source_runtime": detection.metadata.get("source_runtime"),
            "model_registry_id": detection.metadata.get("model_registry_id"),
            "weights_sha256": inference.get("weights_sha256"),
            "inference": inference,
            "diagnostics": result.diagnostics,
            "note": "model outputs are persisted as observations only",
            "placeholder": True,
        },
    )


def _load_gameplay_segments(
    session: Session,
    gameplay_run_id: str | None,
) -> list[dict[str, Any]]:
    if gameplay_run_id is None:
        return []
    rows = session.scalars(
        select(Observation)
        .join(GameplayObservation, GameplayObservation.observation_id == Observation.id)
        .where(Observation.run_id == gameplay_run_id)
        .order_by(Observation.frame_start, Observation.id)
    ).all()
    return [
        {
            "observation_id": row.id,
            "frame_start": row.frame_start,
            "frame_end": row.frame_end,
            "timestamp_start_ms": row.timestamp_start_ms,
            "timestamp_end_ms": row.timestamp_end_ms,
            "view_state": row.gameplay_detail.view_state if row.gameplay_detail else None,
            "view_state_subtype": (
                row.gameplay_detail.view_state_subtype if row.gameplay_detail else None
            ),
        }
        for row in rows
    ]


def _gameplay_parent_for_frame(
    gameplay_segments: list[dict[str, Any]],
    frame_number: int,
) -> dict[str, Any] | None:
    for segment in gameplay_segments:
        start = segment.get("frame_start")
        end = segment.get("frame_end")
        if start is not None and end is not None and start <= frame_number <= end:
            return segment
    return None


def _observation_type_for_label(label: str) -> str:
    return "ball_detection" if label == "ball" else "player_detection"


def _mark_completed(
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    result: DetectionAdapterResult,
) -> None:
    now = datetime.now(UTC)
    counts_by_type = Counter(
        _observation_type_for_label(detection.label) for detection in result.detections
    )
    diagnostics = {
        **result.diagnostics,
        "persisted_ball_detections": counts_by_type.get("ball_detection", 0),
        "persisted_player_detections": counts_by_type.get("player_detection", 0),
        "observation_only": True,
        "no_adjudication": True,
    }
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "detection_count": len(result.detections),
        "diagnostics": diagnostics,
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "detection_count": len(result.detections),
        "diagnostics": diagnostics,
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


def _local_media_path(media: MediaAsset) -> str | None:
    metadata = media.metadata_jsonb or {}
    for key in ("stored_path", "original_source_path"):
        value = metadata.get(key)
        if value:
            return str(Path(value).expanduser())
    if media.source_uri.startswith("file://"):
        return str(local_path_from_uri_or_path(media.source_uri))
    return None
