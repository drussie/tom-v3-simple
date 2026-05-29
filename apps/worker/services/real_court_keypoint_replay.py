from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_model_adapters.court_keypoints import (
    TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION,
    TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE,
    CourtKeypointAdapterError,
    CourtKeypointResultProvider,
    probe_tom_v1_court_keypoint_model,
    run_court_keypoint_frame_inference,
    validate_court_keypoint_calibration_options,
    validate_court_keypoint_weights,
)
from tom_v3_observations.writer import ObservationWriter
from tom_v3_schema.artifacts import EvidenceArtifactCreate
from tom_v3_schema.court import (
    COURT_KEYPOINT_SCHEMA,
    COURT_KEYPOINT_SCHEMA_VERSION,
    COURT_TEMPLATE_NAME,
    COURT_TEMPLATE_VERSION,
    CourtKeypointObservationCreate,
    CourtLineObservationCreate,
    get_court_template,
)
from tom_v3_schema.enums import (
    CoordinateSpace,
    ObservationFamily,
    ObservationGranularity,
    RelationshipType,
)
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_video.paths import local_path_from_uri_or_path

REAL_COURT_KEYPOINT_WARNINGS = {
    "real_model_output": True,
    "model_output_not_truth": True,
    "geometry_evidence_only": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_court_truth": True,
    "no_ball_player_court_projection": True,
    "no_tennis_event_interpretation": True,
}


def build_real_court_keypoint_plan(
    *,
    media_id: str = "<media_id>",
    weights_path: str = "model_assets/tom_v1/keypoints_model.pth",
    model_name: str | None = "tom-v1-court-keypoints",
    model_version: str = "v1-local",
    device: str = "auto",
    img_size: int | None = 224,
    every_n_frames: int = 30,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 214,
    derive_lines: bool = True,
    preprocessing_mode: str = TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE,
    coordinate_interpretation: str = TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION,
    emit_debug_artifacts: bool = False,
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    command_parts = [
        "python -m apps.worker.cli run-real-court-keypoints",
        f"--media-id {media_id}",
        f"--weights {weights_path}",
        f"--device {device}",
        f"--every-n-frames {every_n_frames}",
    ]
    if model_name:
        command_parts.append(f"--model-name {model_name}")
    if model_version:
        command_parts.append(f"--model-version {model_version}")
    if img_size is not None:
        command_parts.append(f"--img-size {img_size}")
    if frame_start is not None:
        command_parts.append(f"--frame-start {frame_start}")
    if frame_end is not None:
        command_parts.append(f"--frame-end {frame_end}")
    if max_frames is not None:
        command_parts.append(f"--max-frames {max_frames}")
    if not derive_lines:
        command_parts.append("--no-derive-lines")
    command_parts.append(f"--preprocessing-mode {preprocessing_mode}")
    command_parts.append(f"--coordinate-interpretation {coordinate_interpretation}")
    if emit_debug_artifacts:
        command_parts.append("--emit-debug-artifacts")
    return {
        "steps": [
            "validate_media",
            "probe_tom_v1_court_keypoint_model",
            "validate_weights",
            "sample_indexed_frames",
            "run_tom_v1_court_keypoint_model",
            "persist_court_keypoint_observations",
            "derive_court_line_candidates_when_possible",
            "open_replay_workstation",
        ],
        "command": " ".join(command_parts),
        "sampling": {
            "mode": "every_n_frames",
            "every_n_frames": every_n_frames,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "max_frames": max_frames,
            "frame_time_owner": "media_indexing",
        },
        "runtime": {
            "source_runtime": "tom_v1_court_keypoints",
            "device": device,
            "requested_img_size": img_size,
            "recognized_model_input_size": 224,
            "preprocessing_mode": preprocessing_mode,
            "coordinate_interpretation": coordinate_interpretation,
            "requires_local_weights": True,
        },
        "court_schema": {
            "court_keypoint_schema": COURT_KEYPOINT_SCHEMA,
            "court_keypoint_schema_version": COURT_KEYPOINT_SCHEMA_VERSION,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "derive_line_candidates": derive_lines,
            "emit_debug_artifacts": emit_debug_artifacts,
        },
        "replay_url_template": (
            f"{viewer_base_url.rstrip('/')}/replay/{media_id}?courtRunId=<run_id>"
        ),
        "warnings": dict(REAL_COURT_KEYPOINT_WARNINGS),
    }


def run_real_court_keypoint_replay(
    *,
    session: Session,
    media_id: str,
    weights_path: str | None,
    model_name: str | None = "tom-v1-court-keypoints",
    model_version: str = "v1-local",
    run_name: str = "real-court-keypoints-replay",
    device: str = "auto",
    img_size: int | None = 224,
    every_n_frames: int = 30,
    frame_start: int | None = None,
    frame_end: int | None = None,
    max_frames: int | None = 214,
    allowed_roots: Sequence[str] | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
    derive_lines: bool = True,
    preprocessing_mode: str = TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE,
    coordinate_interpretation: str = TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION,
    emit_debug_artifacts: bool = False,
    plan_only: bool = False,
    result_provider: CourtKeypointResultProvider | None = None,
    frame_source: Any | None = None,
) -> dict[str, Any]:
    try:
        validate_court_keypoint_calibration_options(
            preprocessing_mode=preprocessing_mode,
            coordinate_interpretation=coordinate_interpretation,
        )
    except CourtKeypointAdapterError as exc:
        status = str(exc).split(":", maxsplit=1)[0]
        return _failed(status, str(exc))

    plan = build_real_court_keypoint_plan(
        media_id=media_id,
        weights_path=weights_path or "model_assets/tom_v1/keypoints_model.pth",
        model_name=model_name,
        model_version=model_version,
        device=device,
        img_size=img_size,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
        derive_lines=derive_lines,
        preprocessing_mode=preprocessing_mode,
        coordinate_interpretation=coordinate_interpretation,
        emit_debug_artifacts=emit_debug_artifacts,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "real court keypoint replay run planned",
            "plan": plan,
            "warnings": dict(REAL_COURT_KEYPOINT_WARNINGS),
        }
    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")
    if media.fps is None or media.fps <= 0:
        return _failed("missing_media_fps", "media fps is required for court frame/time mapping")
    if media.frame_count is None:
        return _failed("missing_media_frame_count", "indexed frame_count is required")
    if not weights_path and result_provider is None:
        return _failed("missing_weights_path", "court keypoint weights path is required")

    weights_validation = None
    model_probe: dict[str, Any] | None = None
    if result_provider is None:
        model_probe = probe_tom_v1_court_keypoint_model(
            weights_path=str(weights_path),
            allowed_roots=list(allowed_roots) if allowed_roots else None,
            )
        if not model_probe.get("ok"):
            return _failed(
                str(
                    model_probe.get("status")
                    or "unsupported_model_format_or_missing_model_definition"
                ),
                str(model_probe.get("message") or "TOM v1 court keypoint model is unsupported."),
                model_probe=model_probe,
                weights_validation=model_probe.get("weights_validation"),
            )
        try:
            weights_validation = validate_court_keypoint_weights(
                str(weights_path),
                allowed_roots=list(allowed_roots) if allowed_roots else None,
            )
        except CourtKeypointAdapterError as exc:
            return _failed(
                "invalid_weights",
                str(exc),
                model_probe=model_probe,
            )

    model = _get_or_create_model(
        session=session,
        weights_validation=weights_validation.as_dict() if weights_validation else None,
        model_name=model_name or Path(str(weights_path or "tom-v1-court-keypoints")).stem,
        model_version=model_version,
    )
    runtime_config = _create_runtime_config(
        session=session,
        model=model,
        weights_validation=weights_validation.as_dict() if weights_validation else None,
        model_probe=model_probe,
        device=device,
        img_size=img_size,
        every_n_frames=every_n_frames,
        frame_start=frame_start,
        frame_end=frame_end,
        max_frames=max_frames,
        derive_lines=derive_lines,
        preprocessing_mode=preprocessing_mode,
        coordinate_interpretation=coordinate_interpretation,
        emit_debug_artifacts=emit_debug_artifacts,
    )
    run = _create_run(
        session=session,
        media=media,
        runtime_config=runtime_config,
        run_name=run_name,
    )
    step = _create_step(session=session, run=run, runtime_config=runtime_config)
    try:
        frame_results, inference_summary = run_court_keypoint_frame_inference(
            media_path=_local_media_path(media),
            fps=media.fps,
            frame_count=media.frame_count,
            width=media.width,
            height=media.height,
            frame_sample_rate=every_n_frames,
            max_frames=max_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            result_provider=result_provider,
            frame_source=frame_source,
            inference_metadata={
                "weights_path": weights_validation.resolved_path if weights_validation else None,
                "weights_sha256": weights_validation.sha256 if weights_validation else None,
                "device": device,
                "img_size": img_size,
                "preprocessing_mode": preprocessing_mode,
                "coordinate_interpretation": coordinate_interpretation,
                "model_registry_id": model.id,
                "runtime_config_id": runtime_config.id,
            },
        )
        observations = _persist_court_keypoint_results(
            session=session,
            media=media,
            run=run,
            step=step,
            model=model,
            runtime_config=runtime_config,
            frame_results=frame_results,
            derive_lines=derive_lines,
            emit_debug_artifacts=emit_debug_artifacts,
        )
    except Exception as exc:
        _mark_failed(session=session, run=run, step=step, message=str(exc))
        raise

    counts = Counter(observation.observation_type for observation in observations)
    sampled_frames = list(inference_summary.get("sampled_frames") or [])
    _mark_completed(
        session=session,
        run=run,
        step=step,
        sampled_frames=sampled_frames,
        counts=counts,
        inference_summary=inference_summary,
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "real court keypoint replay run complete",
        "media_id": media.id,
        "court_run_id": run.id,
        "run_id": run.id,
        "model_registry_id": model.id,
        "runtime_config_id": runtime_config.id,
        "processing_step_id": step.id,
        "observations": {
            "court_keypoint_observation": counts.get("court_keypoint_observation", 0),
            "court_line_observation": counts.get("court_line_observation", 0),
            "camera_view_observation": 0,
            "total": sum(counts.values()),
        },
        "sampled_frames": sampled_frames,
        "observation_ids": [observation.id for observation in observations],
        "model_probe": model_probe,
        "weights_validation": weights_validation.as_dict() if weights_validation else None,
        "calibration_debug": {
            "preprocessing_mode": preprocessing_mode,
            "coordinate_interpretation": coordinate_interpretation,
            "emit_debug_artifacts": emit_debug_artifacts,
            "debug_artifact_count": len(frame_results) if emit_debug_artifacts else 0,
        },
        "replay_url": f"{viewer_base_url.rstrip('/')}/replay/{media.id}?courtRunId={run.id}",
        "warnings": dict(REAL_COURT_KEYPOINT_WARNINGS),
    }


def _get_or_create_model(
    *,
    session: Session,
    weights_validation: dict[str, Any] | None,
    model_name: str,
    model_version: str,
) -> ModelRegistry:
    metadata = {
        "adapter_name": "tom-v1-court-keypoints",
        "adapter_version": "v0",
        "model_runtime": "torchvision_resnet50_fc28_tom_v1",
        "model_task": "court_keypoints",
        "real_model_output": True,
        "model_output_not_truth": True,
        "fixture_court_evidence": False,
        "court_keypoint_schema": COURT_KEYPOINT_SCHEMA,
        "court_keypoint_schema_version": COURT_KEYPOINT_SCHEMA_VERSION,
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "geometry_evidence_only": True,
        "observation_only": True,
        "no_adjudication": True,
    }
    if weights_validation:
        metadata.update(
            {
                "weights_sha256": weights_validation.get("sha256"),
                "weights_size_bytes": weights_validation.get("size_bytes"),
                "weights_path": weights_validation.get("resolved_path"),
            }
        )
    model = ModelRegistry(
        name=model_name,
        version=model_version,
        model_family="court",
        source="apps.worker.services.real_court_keypoint_replay",
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
    weights_validation: dict[str, Any] | None,
    model_probe: dict[str, Any] | None,
    device: str,
    img_size: int | None,
    every_n_frames: int,
    frame_start: int | None,
    frame_end: int | None,
    max_frames: int | None,
    derive_lines: bool,
    preprocessing_mode: str,
    coordinate_interpretation: str,
    emit_debug_artifacts: bool,
) -> RuntimeConfig:
    runtime_config = RuntimeConfig(
        config_name="real-court-keypoint-replay-config",
        config_version="v0",
        payload_jsonb={
            "model_registry_id": model.id,
            "adapter_name": "tom-v1-court-keypoints",
            "adapter_version": "v0",
            "source_runtime": "tom_v1_court_keypoints",
            "device": device,
            "requested_img_size": img_size,
            "recognized_model_input_size": 224,
            "preprocessing_mode": preprocessing_mode,
            "coordinate_interpretation": coordinate_interpretation,
            "supported_preprocessing_modes": ["full_frame_resize_224"],
            "supported_coordinate_interpretations": ["output_as_pixels_224"],
            "frame_sampling": {
                "mode": "every_n_frames",
                "every_n_frames": every_n_frames,
                "frame_start": frame_start,
                "frame_end": frame_end,
                "max_frames": max_frames,
            },
            "court_keypoint_schema": COURT_KEYPOINT_SCHEMA,
            "court_keypoint_schema_version": COURT_KEYPOINT_SCHEMA_VERSION,
            "court_template_name": COURT_TEMPLATE_NAME,
            "court_template_version": COURT_TEMPLATE_VERSION,
            "derive_line_candidates": derive_lines,
            "emit_debug_artifacts": emit_debug_artifacts,
            "line_source": "derived_from_real_keypoint_observations",
            "calibration_audit_v0": True,
            "uncalibrated_tom_v1_keypoint_mapping": True,
            "real_model_output": True,
            "model_output_not_truth": True,
            "fixture_court_evidence": False,
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
            "frame_time_owner": "media_indexing",
            "weights_validation": weights_validation,
            "model_probe": model_probe,
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
            "milestone": "tom-v1-court-keypoint-visual-calibration-audit-v0",
            "adapter_name": "tom-v1-court-keypoints",
            "calibration_audit_v0": True,
            "uncalibrated_tom_v1_keypoint_mapping": True,
            "real_model_output": True,
            "model_output_not_truth": True,
            "fixture_court_evidence": False,
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
            "frame_time_owner": "media_indexing",
            "no_ball_player_court_projection": True,
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
        step_name="tom_v1_court_keypoint_adapter",
        step_status="running",
        started_at=now,
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "adapter_name": "tom-v1-court-keypoints",
            "real_model_output": True,
            "model_output_not_truth": True,
            "frame_time_owner": "media_indexing",
            "geometry_evidence_only": True,
        },
    )
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


def _persist_court_keypoint_results(
    *,
    session: Session,
    media: MediaAsset,
    run: ProcessingRun,
    step: ProcessingStep,
    model: ModelRegistry,
    runtime_config: RuntimeConfig,
    frame_results: list[dict[str, Any]],
    derive_lines: bool,
    emit_debug_artifacts: bool,
) -> list[Observation]:
    writer = ObservationWriter(session)
    observations: list[Observation] = []
    for frame_index, frame_result in enumerate(frame_results):
        keypoint_observation = CourtKeypointObservationCreate(
            frame_number=frame_result["frame_number"],
            timestamp_ms=frame_result["timestamp_ms"],
            keypoints_jsonb=frame_result["keypoints"],
            raw_model_payload_jsonb=frame_result["raw_model_payload"],
            metadata_jsonb=_keypoint_metadata(frame_index),
        )
        keypoint_detail = writer.write(
            ObservationCreate(
                media_id=media.id,
                run_id=run.id,
                observation_family=ObservationFamily.court,
                observation_type="court_keypoint_observation",
                granularity=ObservationGranularity.frame,
                frame_start=keypoint_observation.frame_number,
                frame_end=keypoint_observation.frame_number,
                timestamp_start_ms=keypoint_observation.timestamp_ms,
                timestamp_end_ms=keypoint_observation.timestamp_ms,
                confidence=keypoint_observation.mean_keypoint_confidence,
                model_id=model.id,
                runtime_config_id=runtime_config.id,
                coordinate_space=CoordinateSpace.image_pixels,
                payload_jsonb=_observation_payload(
                    observation_type="court_keypoint_observation",
                    step=step,
                    typed_payload=keypoint_observation.model_dump(mode="json"),
                ),
                artifacts=(
                    [
                        _calibration_debug_artifact(
                            media=media,
                            run=run,
                            frame_result=frame_result,
                        )
                    ]
                    if emit_debug_artifacts
                    else []
                ),
                idempotency_key=(
                    f"{run.id}:tom-v1-court-keypoint:{keypoint_observation.frame_number}"
                ),
                court_keypoint=keypoint_observation,
            )
        )
        observations.append(keypoint_detail)
        if derive_lines:
            line_segments = derive_court_line_candidates_from_keypoints(
                keypoint_observation.keypoints_jsonb,
            )
            if line_segments:
                line_observation = CourtLineObservationCreate(
                    frame_number=keypoint_observation.frame_number,
                    timestamp_ms=keypoint_observation.timestamp_ms,
                    line_segments_jsonb=line_segments,
                    raw_model_payload_jsonb={
                        "line_source": "derived_from_real_keypoint_observations",
                        "source_court_keypoint_observation_id": keypoint_detail.id,
                    },
                    metadata_jsonb=_line_metadata(frame_index, keypoint_detail.id),
                )
                observations.append(
                    writer.write(
                        ObservationCreate(
                            media_id=media.id,
                            run_id=run.id,
                            observation_family=ObservationFamily.court,
                            observation_type="court_line_observation",
                            granularity=ObservationGranularity.frame,
                            frame_start=line_observation.frame_number,
                            frame_end=line_observation.frame_number,
                            timestamp_start_ms=line_observation.timestamp_ms,
                            timestamp_end_ms=line_observation.timestamp_ms,
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
                                f"{run.id}:tom-v1-court-line:{line_observation.frame_number}"
                            ),
                            court_line=line_observation,
                            lineage=[
                                ObservationLineageCreate(
                                    parent_observation_id=keypoint_detail.id,
                                    relationship_type=RelationshipType.derived_from,
                                    processing_step_id=step.id,
                                    payload_jsonb={
                                        "line_source": (
                                            "derived_from_real_keypoint_observations"
                                        ),
                                        "candidate_line_only": True,
                                        "geometry_evidence_only": True,
                                        "observation_only": True,
                                        "no_adjudication": True,
                                    },
                                )
                            ],
                        )
                    )
                )
    return observations


def derive_court_line_candidates_from_keypoints(
    keypoints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_name = {str(keypoint.get("name")): keypoint for keypoint in keypoints}
    segments = []
    for line in get_court_template().lines:
        start = by_name.get(line.start_keypoint)
        end = by_name.get(line.end_keypoint)
        if not _present_xy(start) or not _present_xy(end):
            continue
        confidences = [
            float(value)
            for value in (start.get("confidence"), end.get("confidence"))
            if value is not None
        ]
        confidence = round(sum(confidences) / len(confidences), 6) if confidences else None
        segments.append(
            {
                "line_class": line.line_class,
                "x1": start["x"],
                "y1": start["y"],
                "x2": end["x"],
                "y2": end["y"],
                "confidence": confidence,
                "visibility": "inferred_by_adapter",
                "line_source": "derived_from_real_keypoint_observations",
                "candidate_line_only": True,
            }
        )
    return segments


def _present_xy(keypoint: dict[str, Any] | None) -> bool:
    return bool(
        keypoint
        and keypoint.get("present") is True
        and keypoint.get("x") is not None
        and keypoint.get("y") is not None
    )


def _keypoint_metadata(frame_index: int) -> dict[str, Any]:
    return {
        "adapter_name": "tom-v1-court-keypoints",
        "adapter_version": "v0",
        "fixture_court_evidence": False,
        "real_model_output": True,
        "model_output_not_truth": True,
        "tom_v1_court_keypoint_model_output": True,
        "calibration_audit_v0": True,
        "uncalibrated_tom_v1_keypoint_mapping": True,
        "adapter_frame_index": frame_index,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "not_court_truth": True,
        "frame_time_owner": "media_indexing",
        "no_ball_player_court_projection": True,
        "no_tennis_event_interpretation": True,
    }


def _line_metadata(frame_index: int, source_keypoint_observation_id: str) -> dict[str, Any]:
    return {
        **_keypoint_metadata(frame_index),
        "court_line_candidate": True,
        "candidate_line_only": True,
        "line_source": "derived_from_real_keypoint_observations",
        "source_court_keypoint_observation_id": source_keypoint_observation_id,
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
        "adapter_name": "tom-v1-court-keypoints",
        "adapter_version": "v0",
        "fixture_court_evidence": False,
        "real_model_output": True,
        "model_output_not_truth": True,
        "calibration_audit_v0": True,
        "uncalibrated_tom_v1_keypoint_mapping": True,
        "homography_from_uncalibrated_tom_v1_keypoints": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "not_court_truth": True,
        "frame_time_owner": "media_indexing",
        "court_template_name": COURT_TEMPLATE_NAME,
        "court_template_version": COURT_TEMPLATE_VERSION,
        "no_ball_player_court_projection": True,
        "no_tennis_event_interpretation": True,
        "typed_payload": typed_payload,
    }


def _mark_completed(
    *,
    session: Session,
    run: ProcessingRun,
    step: ProcessingStep,
    sampled_frames: list[int],
    counts: Counter[str],
    inference_summary: dict[str, Any],
) -> None:
    now = datetime.now(UTC)
    summary = {
        "sampled_frames": sampled_frames,
        "court_keypoint_observation_count": counts.get("court_keypoint_observation", 0),
        "court_line_observation_count": counts.get("court_line_observation", 0),
        "camera_view_observation_count": 0,
        "total_observation_count": sum(counts.values()),
        "inference_summary": inference_summary,
        "calibration_audit_v0": True,
        "uncalibrated_tom_v1_keypoint_mapping": True,
        "real_model_output": True,
        "model_output_not_truth": True,
        "observation_only": True,
        "no_adjudication": True,
        "geometry_evidence_only": True,
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


def _failed(status: str, message: str, **extra: Any) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "status": status,
        "message": message,
        "warnings": dict(REAL_COURT_KEYPOINT_WARNINGS),
    }
    result.update(extra)
    return result


def _calibration_debug_artifact(
    *,
    media: MediaAsset,
    run: ProcessingRun,
    frame_result: dict[str, Any],
) -> EvidenceArtifactCreate:
    raw_payload = frame_result.get("raw_model_payload") or {}
    metadata = {
        "export_version": "tom_v1_court_keypoint_calibration_frame_v0",
        "frame_number": frame_result["frame_number"],
        "timestamp_ms": frame_result["timestamp_ms"],
        "image_width": frame_result["image_width"],
        "image_height": frame_result["image_height"],
        "preprocessing_mode": raw_payload.get("preprocessing_mode"),
        "coordinate_interpretation": raw_payload.get("coordinate_interpretation"),
        "raw_output_coordinate_assumption": raw_payload.get("coordinate_interpretation"),
        "raw_model_output": raw_payload.get("tom_v1_raw_keypoints"),
        "tom_v1_raw_keypoint_names": raw_payload.get("tom_v1_raw_keypoint_names"),
        "raw_keypoints_scaled_to_image": raw_payload.get("raw_keypoints_scaled_to_image"),
        "mapped_tom_v3_keypoints": raw_payload.get("mapped_tom_v3_keypoints"),
        "inferred_keypoints": raw_payload.get("inferred_tom_v3_keypoints"),
        "mapping_version": raw_payload.get("mapping_version"),
        "warnings": {
            "geometry_evidence_only": True,
            "observation_only": True,
            "no_adjudication": True,
            "not_court_truth": True,
            "uncalibrated_tom_v1_keypoint_mapping": True,
        },
    }
    return EvidenceArtifactCreate(
        media_id=media.id,
        run_id=run.id,
        artifact_type="tom_v1_court_keypoint_calibration_debug_json",
        uri=(
            "file:///dev/artifacts/court-calibration/"
            f"{run.id}/frame-{frame_result['frame_number']}.json"
        ),
        frame_start=frame_result["frame_number"],
        frame_end=frame_result["frame_number"],
        timestamp_start_ms=frame_result["timestamp_ms"],
        timestamp_end_ms=frame_result["timestamp_ms"],
        metadata_jsonb=metadata,
    )


def _local_media_path(media: MediaAsset) -> str | None:
    metadata = media.metadata_jsonb or {}
    for key in ("stored_path", "original_source_path"):
        value = metadata.get(key)
        if value:
            return str(Path(value).expanduser())
    if media.source_uri.startswith("file://"):
        return str(local_path_from_uri_or_path(media.source_uri))
    return None
