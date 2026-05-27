from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.court import (
    COURT_KEYPOINT_SCHEMA,
    COURT_KEYPOINT_SCHEMA_VERSION,
    COURT_TEMPLATE_NAME,
    COURT_TEMPLATE_VERSION,
    CameraViewObservationCreate,
    CourtKeypointObservationCreate,
    CourtLineObservationCreate,
    get_court_template,
)
from tom_v3_schema.enums import CoordinateSpace, ObservationFamily, ObservationGranularity
from tom_v3_schema.observations import ObservationCreate
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.time_index import frame_to_timestamp_ms

FIXTURE_COURT_WARNINGS = {
    "fixture_court_evidence": True,
    "observation_only": True,
    "no_adjudication": True,
    "geometry_evidence_only": True,
    "no_homography_computation": True,
    "no_projection_diagnostics": True,
    "no_replay_court_overlay": True,
    "no_ball_player_court_projection": True,
    "no_tennis_event_interpretation": True,
}


class FixtureCourtAdapterRunError(ValueError):
    pass


def build_fixture_court_adapter_plan(
    *,
    media_id: str = "<media_id>",
    frame_sample_rate: int = 30,
    max_frames: int | None = 30,
    run_name: str = "fixture-court-evidence",
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    command_parts = [
        "python -m apps.worker.cli run-fixture-court",
        f"--media-id {media_id}",
        f"--frame-sample-rate {frame_sample_rate}",
    ]
    if max_frames is not None:
        command_parts.append(f"--max-frames {max_frames}")
    return {
        "steps": [
            "validate_media",
            "create_fixture_court_model_registry_row",
            "create_fixture_court_runtime_config",
            "create_processing_run_and_step",
            "sample_media_owned_frames",
            "persist_court_keypoint_observations",
            "persist_court_line_observations",
            "persist_camera_view_observations",
        ],
        "command": " ".join(command_parts),
        "run_name": run_name,
        "sampling": {
            "mode": "every_n_frames",
            "frame_sample_rate": frame_sample_rate,
            "max_frames": max_frames,
            "frame_time_owner": "media_indexing",
        },
        "court_schema": {
            "court_keypoint_schema": COURT_KEYPOINT_SCHEMA,
            "court_keypoint_schema_version": COURT_KEYPOINT_SCHEMA_VERSION,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
        },
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}?courtRunId=<run_id>"
        ),
        "warnings": dict(FIXTURE_COURT_WARNINGS),
    }


def run_fixture_court_adapter(
    *,
    session: Session,
    media_id: str,
    frame_sample_rate: int = 30,
    max_frames: int | None = 30,
    run_name: str = "fixture-court-evidence",
    viewer_base_url: str = "http://127.0.0.1:3000",
    plan_only: bool = False,
) -> dict[str, Any]:
    if frame_sample_rate <= 0:
        return _failed("invalid_frame_sample_rate", "frame_sample_rate must be greater than zero")
    if max_frames is not None and max_frames < 0:
        return _failed("invalid_max_frames", "max_frames must be greater than or equal to zero")

    plan = build_fixture_court_adapter_plan(
        media_id=media_id,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        run_name=run_name,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "fixture court evidence run planned",
            "plan": plan,
            "warnings": dict(FIXTURE_COURT_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")
    if media.fps is None:
        return _failed("missing_media_fps", "media fps is required for court frame/time mapping")

    model = _get_or_create_fixture_court_model(session)
    runtime_config = _create_runtime_config(
        session=session,
        model=model,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
    )
    run = _create_run(
        session=session,
        media=media,
        runtime_config=runtime_config,
        run_name=run_name,
    )
    step = _create_step(session=session, run=run, runtime_config=runtime_config)

    try:
        sampled_frames = _sampled_frames(media, frame_sample_rate, max_frames)
        observations = _persist_fixture_court_observations(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            sampled_frames=sampled_frames,
        )
    except Exception as exc:
        _mark_failed(session=session, run=run, step=step, message=str(exc))
        raise

    counts = Counter(observation.observation_type for observation in observations)
    _mark_completed(
        session=session,
        run=run,
        step=step,
        sampled_frames=sampled_frames,
        counts=counts,
    )

    total = sum(counts.values())
    return {
        "ok": True,
        "status": "completed",
        "message": "fixture court evidence run complete",
        "media_id": media.id,
        "court_run_id": run.id,
        "run_id": run.id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            "court_keypoint_observation": counts.get("court_keypoint_observation", 0),
            "court_line_observation": counts.get("court_line_observation", 0),
            "camera_view_observation": counts.get("camera_view_observation", 0),
            "total": total,
        },
        "sampled_frames": sampled_frames,
        "observation_ids": [observation.id for observation in observations],
        "replay_url": f"{viewer_base_url.rstrip('/')}/replay/{media.id}?courtRunId={run.id}",
        "warnings": dict(FIXTURE_COURT_WARNINGS),
    }


def _get_or_create_fixture_court_model(session: Session) -> ModelRegistry:
    model = session.scalar(
        select(ModelRegistry).where(
            ModelRegistry.name == "fixture-court-evidence-adapter",
            ModelRegistry.version == "v0",
            ModelRegistry.model_family == "court",
        )
    )
    if model is not None:
        return model

    model = ModelRegistry(
        name="fixture-court-evidence-adapter",
        version="v0",
        model_family="court",
        source="apps.worker.services.court_adapter",
        metadata_jsonb={
            "adapter_name": "fixture-court-evidence",
            "fixture_adapter": True,
            "fixture_court_evidence": True,
            "model_runtime": "fixture",
            "model_task": "court_keypoints_lines_camera_view",
            "model_output_not_truth": True,
            "court_keypoint_schema": COURT_KEYPOINT_SCHEMA,
            "court_keypoint_schema_version": COURT_KEYPOINT_SCHEMA_VERSION,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
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
    frame_sample_rate: int,
    max_frames: int | None,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="fixture-court-evidence-config",
        config_version="v0",
        payload_jsonb={
            "model_registry_id": model.id,
            "adapter_name": "fixture-court-evidence",
            "adapter_version": "v0",
            "court_keypoint_schema": COURT_KEYPOINT_SCHEMA,
            "court_keypoint_schema_version": COURT_KEYPOINT_SCHEMA_VERSION,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "frame_sample_rate": frame_sample_rate,
            "max_frames": max_frames,
            "frame_sampling": {
                "mode": "every_n_frames",
                "frame_sample_rate": frame_sample_rate,
                "max_frames": max_frames,
            },
            "fixture_court_evidence": True,
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
            "frame_time_owner": "media_indexing",
            "no_homography_computation": True,
            "no_projection_diagnostics": True,
        },
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
) -> ProcessingRun:
    now = datetime.now(UTC)
    run = ProcessingRun(
        media_id=media.id,
        run_name=run_name,
        run_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "blueprint": 8,
            "milestone": "8B",
            "adapter_name": "fixture-court-evidence",
            "fixture_court_evidence": True,
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
            "frame_time_owner": "media_indexing",
            "no_homography_computation": True,
            "no_projection_diagnostics": True,
            "no_tennis_event_interpretation": True,
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
) -> ProcessingStep:
    now = datetime.now(UTC)
    step = ProcessingStep(
        run_id=run.id,
        step_name="fixture_court_evidence_adapter",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": "fixture-court-evidence",
            "fixture_court_evidence": True,
            "frame_time_owner": "media_indexing",
            "geometry_evidence_only": True,
            "no_homography_computation": True,
            "no_projection_diagnostics": True,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


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


def _persist_fixture_court_observations(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    sampled_frames: list[int],
) -> list[Observation]:
    writer = ObservationWriter(session)
    observations: list[Observation] = []
    width = float(media.width or 1280)
    height = float(media.height or 720)
    for frame_index, frame_number in enumerate(sampled_frames):
        timestamp_ms = frame_to_timestamp_ms(media.fps or 30.0, frame_number)
        keypoints = _fixture_keypoints(width=width, height=height)
        lines = _fixture_lines(keypoints)
        keypoint_observation = CourtKeypointObservationCreate(
            frame_number=frame_number,
            timestamp_ms=timestamp_ms,
            keypoints_jsonb=keypoints,
            raw_model_payload_jsonb=_raw_payload(frame_number, timestamp_ms, frame_index),
            metadata_jsonb=_metadata(frame_index),
        )
        line_observation = CourtLineObservationCreate(
            frame_number=frame_number,
            timestamp_ms=timestamp_ms,
            line_segments_jsonb=lines,
            raw_model_payload_jsonb=_raw_payload(frame_number, timestamp_ms, frame_index),
            metadata_jsonb=_metadata(frame_index),
        )
        camera_view_observation = CameraViewObservationCreate(
            frame_number=frame_number,
            timestamp_ms=timestamp_ms,
            view_label="broadcast_hardcam",
            view_confidence=0.8,
            camera_motion_hint="stable",
            stability_score=0.8,
            cut_likelihood=0.05,
            metadata_jsonb={
                **_metadata(frame_index),
                "fixture_camera_view_evidence": True,
            },
        )

        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family=ObservationFamily.court,
                    observation_type="court_keypoint_observation",
                    granularity=ObservationGranularity.frame,
                    frame_start=frame_number,
                    frame_end=frame_number,
                    timestamp_start_ms=timestamp_ms,
                    timestamp_end_ms=timestamp_ms,
                    confidence=keypoint_observation.mean_keypoint_confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space=CoordinateSpace.image_pixels,
                    payload_jsonb=_observation_payload(
                        observation_type="court_keypoint_observation",
                        step=step,
                        typed_payload=keypoint_observation.model_dump(mode="json"),
                    ),
                    idempotency_key=(
                        f"{run.id}:fixture-court:court_keypoint_observation:{frame_number}"
                    ),
                    court_keypoint=keypoint_observation,
                )
            )
        )
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family=ObservationFamily.court,
                    observation_type="court_line_observation",
                    granularity=ObservationGranularity.frame,
                    frame_start=frame_number,
                    frame_end=frame_number,
                    timestamp_start_ms=timestamp_ms,
                    timestamp_end_ms=timestamp_ms,
                    confidence=line_observation.mean_line_confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space=CoordinateSpace.image_pixels,
                    payload_jsonb=_observation_payload(
                        observation_type="court_line_observation",
                        step=step,
                        typed_payload=line_observation.model_dump(mode="json"),
                    ),
                    idempotency_key=(
                        f"{run.id}:fixture-court:court_line_observation:{frame_number}"
                    ),
                    court_line=line_observation,
                )
            )
        )
        observations.append(
            writer.write(
                ObservationCreate(
                    media_id=media.id,
                    run_id=run.id,
                    observation_family=ObservationFamily.court,
                    observation_type="camera_view_observation",
                    granularity=ObservationGranularity.frame,
                    frame_start=frame_number,
                    frame_end=frame_number,
                    timestamp_start_ms=timestamp_ms,
                    timestamp_end_ms=timestamp_ms,
                    confidence=camera_view_observation.view_confidence,
                    model_id=model.id,
                    runtime_config_id=runtime_config.id,
                    coordinate_space=None,
                    payload_jsonb=_observation_payload(
                        observation_type="camera_view_observation",
                        step=step,
                        typed_payload=camera_view_observation.model_dump(mode="json"),
                    ),
                    idempotency_key=(
                        f"{run.id}:fixture-court:camera_view_observation:{frame_number}"
                    ),
                    camera_view=camera_view_observation,
                )
            )
        )
    return observations


def _fixture_keypoints(*, width: float, height: float) -> list[dict[str, Any]]:
    template = get_court_template()
    margin_x = width * 0.15
    margin_y = height * 0.20
    usable_width = width - (2 * margin_x)
    usable_height = height - (2 * margin_y)
    return [
        {
            "name": keypoint.name,
            "x": round(margin_x + (keypoint.x * usable_width), 3),
            "y": round(margin_y + (keypoint.y * usable_height), 3),
            "confidence": 0.8,
            "present": True,
            "visibility": "visible",
            "source_index": index,
        }
        for index, keypoint in enumerate(template.keypoints)
    ]


def _fixture_lines(keypoints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    template = get_court_template()
    keypoint_by_name = {str(keypoint["name"]): keypoint for keypoint in keypoints}
    segments: list[dict[str, Any]] = []
    for line in template.lines:
        start = keypoint_by_name[line.start_keypoint]
        end = keypoint_by_name[line.end_keypoint]
        segments.append(
            {
                "line_class": line.line_class,
                "x1": start["x"],
                "y1": start["y"],
                "x2": end["x"],
                "y2": end["y"],
                "confidence": 0.75,
                "visibility": "visible",
            }
        )
    return segments


def _metadata(frame_index: int) -> dict[str, Any]:
    return {
        "adapter_name": "fixture-court-evidence",
        "adapter_version": "v0",
        "fixture_court_evidence": True,
        "fixture_frame_index": frame_index,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "not_real_court_model": True,
        "frame_time_owner": "media_indexing",
        "no_homography_computation": True,
        "no_projection_diagnostics": True,
        "no_tennis_event_interpretation": True,
    }


def _raw_payload(frame_number: int, timestamp_ms: int, frame_index: int) -> dict[str, Any]:
    return {
        "adapter_name": "fixture-court-evidence",
        "adapter_version": "v0",
        "frame_number": frame_number,
        "timestamp_ms": timestamp_ms,
        "fixture_frame_index": frame_index,
        "source": "deterministic normalized court template projected into image margins",
        "model_output_not_truth": True,
    }


def _observation_payload(
    *,
    observation_type: str,
    step: ProcessingStep,
    typed_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "observation_type": observation_type,
        "processing_step_id": step.id,
        "adapter_name": "fixture-court-evidence",
        "adapter_version": "v0",
        "fixture_court_evidence": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "not_real_court_model": True,
        "frame_time_owner": "media_indexing",
        "no_homography_computation": True,
        "no_projection_diagnostics": True,
        "no_tennis_event_interpretation": True,
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "typed_payload": typed_payload,
    }


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    sampled_frames: list[int],
    counts: Counter[str],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "sampled_frames": sampled_frames,
        "court_keypoint_observation_count": counts.get("court_keypoint_observation", 0),
        "court_line_observation_count": counts.get("court_line_observation", 0),
        "camera_view_observation_count": counts.get("camera_view_observation", 0),
        "total_observation_count": sum(counts.values()),
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "no_homography_computation": True,
        "no_projection_diagnostics": True,
    }
    run.run_status = "completed"
    run.completed_at = now
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        **summary,
    }
    step.step_status = "completed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        **summary,
    }
    session.commit()


def _mark_failed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    message: str,
) -> None:
    now = datetime.now(UTC)
    run.run_status = "failed"
    run.completed_at = now
    run.metadata_jsonb = {
        **(run.metadata_jsonb or {}),
        "error": message,
        "observation_only": True,
        "no_adjudication": True,
    }
    step.step_status = "failed"
    step.completed_at = now
    step.metadata_jsonb = {
        **(step.metadata_jsonb or {}),
        "error": message,
        "observation_only": True,
        "no_adjudication": True,
    }
    session.commit()


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
        "warnings": dict(FIXTURE_COURT_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
