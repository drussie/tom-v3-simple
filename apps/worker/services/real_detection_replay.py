from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_model_adapters.yolo_runtime import probe_yolo_runtime
from tom_v3_model_adapters.yolo_weights import (
    YoloClassMappingError,
    YoloWeightsValidationError,
    default_yolo_class_mapping,
    validate_yolo_class_mapping,
    validate_yolo_weights,
)
from tom_v3_storage.db_models import MediaAsset

from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.yolo_model_registry import register_yolo_model

REAL_DETECTION_WARNINGS = {
    "observation_only": True,
    "no_adjudication": True,
    "model_output_not_truth": True,
    "no_fixture_fallback": True,
}


def build_real_detection_replay_plan(
    media_id: str = "<media_id>",
    weights_path: str = "model_assets/yolo/<weights_file>.pt",
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
    viewer_base_url: str = "http://127.0.0.1:3000",
) -> dict[str, Any]:
    command_parts = [
        "python -m apps.worker.cli run-real-detection",
        f"--media-id {media_id}",
        f"--weights {weights_path}",
        f"--device {device}",
        f"--every-n-frames {every_n_frames}",
    ]
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

    return {
        "steps": [
            "validate_media",
            "probe_yolo_runtime",
            "validate_weights",
            "register_model",
            "sample_indexed_frames",
            "run_yolo_detection",
            "persist_atomic_detection_observations",
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
            "source_runtime": "ultralytics_yolo",
            "device": device,
            "imgsz": imgsz,
            "conf": conf,
            "iou": iou,
            "requires_yolo": True,
            "requires_pose_weights": False,
        },
        "class_map": coerce_real_detection_class_map(None),
        "replay_url_template": f"{viewer_base_url}/replay/{media_id}?detectionRunId=<run_id>",
        "warnings": dict(REAL_DETECTION_WARNINGS),
    }


def run_real_detection_replay(
    session: Session,
    media_id: str,
    weights_path: str | None,
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
    class_map: Mapping[str, Any] | None = None,
    allowed_roots: Sequence[str] | None = None,
    viewer_base_url: str = "http://127.0.0.1:3000",
    output_debug_artifact: bool = False,
    plan_only: bool = False,
    probe_runtime: Callable[..., dict[str, Any]] = probe_yolo_runtime,
    yolo_result_provider: Any | None = None,
    yolo_frame_source: Any | None = None,
) -> dict[str, Any]:
    try:
        normalized_class_map = coerce_real_detection_class_map(class_map)
    except YoloClassMappingError as exc:
        return _failed(
            status="invalid_class_mapping",
            message=str(exc),
            error_type=exc.__class__.__name__,
        )

    plan = build_real_detection_replay_plan(
        media_id=media_id,
        weights_path=weights_path or "model_assets/yolo/<weights_file>.pt",
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
        viewer_base_url=viewer_base_url,
    )
    plan["class_map"] = normalized_class_map
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "real YOLO detection replay run planned",
            "plan": plan,
            "warnings": dict(REAL_DETECTION_WARNINGS),
        }

    media = session.get(MediaAsset, media_id)
    if media is None:
        return _failed("missing_media", f"media asset not found: {media_id}")

    runtime_probe = probe_runtime(requested_device=device)
    if runtime_probe.get("status") != "ok":
        return _failed(
            "yolo_runtime_unavailable",
            "YOLO runtime is unavailable; real detection replay was not run.",
            runtime_probe=runtime_probe,
        )

    if not weights_path:
        return _failed("missing_weights_path", "weights path is required.")

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

    try:
        model = register_yolo_model(
            session=session,
            weights_path=weights_validation.resolved_path,
            model_name=model_name,
            model_version=model_version,
            required_sha256=required_sha256,
            allowed_roots=list(allowed_roots) if allowed_roots else None,
            class_map=normalized_class_map,
            device=device,
            created_by="tom-v3-real-detection-replay",
        )
        detection = run_detection_adapter(
            session=session,
            media_id=media.id,
            adapter_name="yolo",
            run_name="real-yolo-detection-replay",
            config_name="real-yolo-detection-replay-config",
            config_version="v0",
            model_registry_id=model["model_registry_id"],
            device=device,
            image_size=imgsz,
            confidence_threshold=conf,
            iou_threshold=iou,
            max_det=50,
            frame_sample_rate=every_n_frames,
            max_frames=max_frames,
            frame_start=frame_start,
            frame_end=frame_end,
            output_debug_artifact=output_debug_artifact,
            yolo_result_provider=yolo_result_provider,
            yolo_frame_source=yolo_frame_source,
        )
    except Exception as exc:
        return _failed(
            "failed",
            str(exc),
            error_type=exc.__class__.__name__,
            weights_validation=weights_validation.as_dict(),
            runtime_probe=runtime_probe,
        )

    counts = detection.get("counts_by_observation_type", {})
    diagnostics = detection.get("diagnostics", {})
    summary = {
        "frames_considered": diagnostics.get("frames_considered"),
        "frames_processed": diagnostics.get("frames_processed"),
        "raw_detections": diagnostics.get("raw_detections", diagnostics.get("input_box_count")),
        "accepted_detections": diagnostics.get(
            "accepted_detections", diagnostics.get("mapped_detection_count")
        ),
        "persisted_ball_detections": counts.get("ball_detection", 0),
        "persisted_player_detections": counts.get("player_detection", 0),
        "skipped_unmapped_classes": diagnostics.get(
            "skipped_unmapped_classes", diagnostics.get("unmapped_detection_count", 0)
        ),
        "unmapped_classes": diagnostics.get("unmapped_classes", []),
        "sampled_frames": diagnostics.get("sampled_frames", []),
        "device": diagnostics.get("device") or device,
        "weights_sha256": model.get("weights_sha256") or weights_validation.sha256,
        "observation_only": True,
        "no_adjudication": True,
    }
    run_id = str(detection["run_id"])
    return {
        "ok": True,
        "status": "completed",
        "message": "real YOLO detection replay run complete",
        "media_id": media.id,
        "detection_run_id": run_id,
        "model_registry_id": model["model_registry_id"],
        "runtime_config_id": detection["runtime_config_id"],
        "processing_step_id": detection["processing_step_id"],
        "observations": {
            "ball_detection": counts.get("ball_detection", 0),
            "player_detection": counts.get("player_detection", 0),
            "total": detection.get("detection_count", 0),
        },
        "summary": summary,
        "weights_validation": weights_validation.as_dict(),
        "runtime_probe": runtime_probe,
        "class_map": normalized_class_map,
        "run_label": "real YOLO detection run",
        "replay_url": f"{viewer_base_url}/replay/{media.id}?detectionRunId={run_id}",
        "stream_proxy_replay_url": (
            f"{viewer_base_url}/replay/{media.id}?mode=stream_proxy&detectionRunId={run_id}"
        ),
        "api_command_hint": (
            "TOM_V3_DATABASE_URL=<db-url> .venv/bin/python -m uvicorn "
            "apps.api.main:app --reload"
        ),
        "web_command_hint": "cd apps/web && npm run dev",
        "warnings": dict(REAL_DETECTION_WARNINGS),
    }


def coerce_real_detection_class_map(
    class_map: Mapping[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    if class_map is None:
        return validate_yolo_class_mapping(default_yolo_class_mapping())

    coerced: dict[str, dict[str, Any]] = {}
    for mapping_name, entry in class_map.items():
        if not isinstance(entry, Mapping):
            raise YoloClassMappingError(f"class mapping entry must be an object: {mapping_name}")

        if "target_observation_type" in entry or "target_label" in entry:
            coerced[str(mapping_name)] = dict(entry)
            continue

        observation_type = str(entry.get("observation_type", ""))
        label = str(entry.get("label", ""))
        source_names = entry.get("source_class_names")
        if source_names is None:
            source_names = [str(mapping_name)]
        if isinstance(source_names, str):
            source_names = [source_names]
        source_ids = entry.get("source_class_ids", [])
        if isinstance(source_ids, int):
            source_ids = [source_ids]
        coerced[str(mapping_name)] = {
            "source_class_names": list(source_names),
            "source_class_ids": list(source_ids),
            "target_observation_type": observation_type,
            "target_label": label,
        }

    return validate_yolo_class_mapping(coerced)


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
        "warnings": dict(REAL_DETECTION_WARNINGS),
    }
    if error_type:
        result["error_type"] = error_type
    result.update(extra)
    return result
