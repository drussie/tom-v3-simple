from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_model_adapters.gameplay import (
    GameplayAdapterInput,
    GameplayAdapterResult,
    get_gameplay_adapter,
)
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.artifacts import EvidenceArtifactCreate
from tom_v3_schema.observations import GameplayObservationCreate, ObservationCreate
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.paths import local_path_from_uri_or_path


class GameplayAdapterRunError(ValueError):
    pass


def run_gameplay_adapter(
    session: Session,
    media_id: str,
    adapter_name: str = "fixture",
    run_name: str = "gameplay-adapter-run",
    config_name: str = "gameplay-adapter-config",
    config_version: str = "v0",
    tom_v1_path: str | None = None,
    output_debug_artifact: bool = False,
    window_seconds: float | None = 2.0,
    stride_seconds: float | None = 1.0,
) -> dict[str, Any]:
    media = session.get(MediaAsset, media_id)
    if media is None:
        raise GameplayAdapterRunError(f"media asset not found: {media_id}")

    adapter = get_gameplay_adapter(adapter_name, tom_v1_path=tom_v1_path)
    runtime_config = _create_runtime_config(
        session=session,
        adapter_name=adapter_name,
        config_name=config_name,
        config_version=config_version,
        tom_v1_path=tom_v1_path,
        window_seconds=window_seconds,
        stride_seconds=stride_seconds,
    )
    model = _get_or_create_model(
        session=session,
        adapter_name=adapter_name,
        adapter_runtime_name=adapter.name,
        adapter_version=adapter.version,
        tom_v1_path=tom_v1_path,
    )
    run = _create_run(session, media, runtime_config, run_name, adapter.name)
    step = _create_step(session, run, runtime_config, adapter.name)

    try:
        result = adapter.run(_adapter_input(media, runtime_config))
        observations = _persist_segments(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            result=result,
            output_debug_artifact=output_debug_artifact,
        )
    except Exception:
        _mark_failed(session, run, step)
        raise

    _mark_completed(session, run, step, result)
    counts_by_label = dict(Counter(segment.label for segment in result.segments))
    return {
        "media_id": media.id,
        "run_id": run.id,
        "model_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "adapter": adapter_name,
        "adapter_name": result.adapter_name,
        "adapter_version": result.adapter_version,
        "segment_count": len(result.segments),
        "counts_by_label": counts_by_label,
        "observation_ids": [observation.id for observation in observations],
        "diagnostics": result.diagnostics,
    }


def _create_runtime_config(
    session: Session,
    adapter_name: str,
    config_name: str,
    config_version: str,
    tom_v1_path: str | None,
    window_seconds: float | None,
    stride_seconds: float | None,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name=config_name,
        config_version=config_version,
        payload_jsonb={
            "adapter": adapter_name,
            "tom_v1_path": tom_v1_path,
            "window_seconds": window_seconds,
            "stride_seconds": stride_seconds,
            "confidence_thresholds": {
                "gameplay": 0.5,
                "non_gameplay": 0.5,
                "uncertain": 0.0,
            },
            "uncertain_policy": "emit_uncertain_segment",
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
    tom_v1_path: str | None,
) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == adapter_runtime_name,
            ModelRegistry.version == adapter_version,
            ModelRegistry.model_family == "gameplay",
        )
    )
    if model is not None:
        return model

    metadata = {
        "adapter_type": adapter_name,
        "source_repo_or_path": tom_v1_path,
        "portability_status": (
            "stub_not_portable_in_current_repo"
            if adapter_name in {"tom-v1", "tom_v1", "tomv1"}
            else "fixture_dev_only"
        ),
        "frame_time_owner": "media_indexing",
    }
    model = ModelRegistry(
        name=adapter_runtime_name,
        version=adapter_version,
        model_family="gameplay",
        source="tom_v3_model_adapters.gameplay",
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
            "source": "worker gameplay adapter",
            "rerun_behavior": "new run",
            "frame_time_owner": "media_indexing",
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
        step_name="gameplay_adapter_classification",
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


def _adapter_input(media: MediaAsset, runtime_config: RuntimeConfig) -> GameplayAdapterInput:
    metadata = media.metadata_jsonb or {}
    return GameplayAdapterInput(
        media_id=media.id,
        source_uri=media.source_uri,
        local_path=_local_media_path(media),
        fps=media.fps,
        frame_count=media.frame_count,
        duration_ms=media.duration_ms,
        runtime_config=runtime_config.payload_jsonb,
        frame_time_summary=metadata.get("frame_time_index", {}),
        metadata=metadata,
    )


def _persist_segments(
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    result: GameplayAdapterResult,
    output_debug_artifact: bool,
) -> list[Any]:
    writer = ObservationWriter(session)
    observations = []
    for index, segment in enumerate(result.segments):
        observation = writer.write(
            ObservationCreate(
                media_id=media.id,
                run_id=run.id,
                observation_family="gameplay",
                observation_type="view_state",
                granularity="frame_range",
                frame_start=segment.frame_start,
                frame_end=segment.frame_end,
                timestamp_start_ms=segment.timestamp_start_ms,
                timestamp_end_ms=segment.timestamp_end_ms,
                confidence=segment.confidence,
                model_id=model.id,
                runtime_config_id=runtime_config.id,
                coordinate_space="none",
                payload_jsonb={
                    "adapter_name": result.adapter_name,
                    "adapter_version": result.adapter_version,
                    "segment_index": index,
                    "processing_step_id": step.id,
                    "frame_time_owner": "media_indexing",
                    "source": "gameplay adapter",
                    "metadata": segment.metadata,
                },
                idempotency_key=(
                    f"{run.id}:gameplay-adapter:{result.adapter_name}:"
                    f"{index}:{segment.frame_start}-{segment.frame_end}:{segment.label}"
                ),
                gameplay=GameplayObservationCreate(
                    view_state=segment.label,
                    view_state_subtype=segment.subtype or "unknown",
                    payload_jsonb={
                        "adapter_name": result.adapter_name,
                        "adapter_version": result.adapter_version,
                        "processing_step_id": step.id,
                        "frame_time_owner": "media_indexing",
                        "metadata": segment.metadata,
                    },
                ),
                artifacts=(
                    [_debug_artifact(media, run, segment, result, index)]
                    if output_debug_artifact
                    else []
                ),
            )
        )
        observations.append(observation)
    return observations


def _debug_artifact(
    media: MediaAsset,
    run: ProcessingRun,
    segment: Any,
    result: GameplayAdapterResult,
    index: int,
) -> EvidenceArtifactCreate:
    return EvidenceArtifactCreate(
        media_id=media.id,
        run_id=run.id,
        artifact_type="gameplay_adapter_debug_json",
        uri=f"file:///dev/artifacts/gameplay/{run.id}/segment-{index}.json",
        frame_start=segment.frame_start,
        frame_end=segment.frame_end,
        timestamp_start_ms=segment.timestamp_start_ms,
        timestamp_end_ms=segment.timestamp_end_ms,
        metadata_jsonb={
            "adapter_name": result.adapter_name,
            "adapter_version": result.adapter_version,
            "label": segment.label,
            "placeholder": True,
        },
    )


def _mark_completed(
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    result: GameplayAdapterResult,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **run.metadata_jsonb,
        "segment_count": len(result.segments),
        "diagnostics": result.diagnostics,
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **step.metadata_jsonb,
        "segment_count": len(result.segments),
        "diagnostics": result.diagnostics,
    }
    session.commit()


def _mark_failed(session: Session, run: ProcessingRun, step: ProcessingStep) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    step.step_status = "failed"
    step.completed_at = now
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
