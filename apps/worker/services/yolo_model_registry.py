from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_model_adapters.yolo_runtime import probe_yolo_runtime
from tom_v3_model_adapters.yolo_weights import (
    DEFAULT_YOLO_ALLOWED_ROOTS,
    YoloWeightsValidationResult,
    default_yolo_class_mapping,
    probe_yolo_model_metadata,
    validate_yolo_class_mapping,
    validate_yolo_weights,
)
from tom_v3_storage.db_models import ModelRegistry


def register_yolo_model(
    session: Session,
    weights_path: str,
    model_name: str | None = None,
    model_version: str = "v0",
    required_sha256: str | None = None,
    allowed_roots: list[str] | None = None,
    class_map: dict[str, Any] | None = None,
    probe_model: bool = False,
    device: str = "cpu",
    created_by: str = "tom-v3-worker",
) -> dict[str, Any]:
    allowed_root_paths = (
        [Path(root) for root in allowed_roots]
        if allowed_roots
        else list(DEFAULT_YOLO_ALLOWED_ROOTS)
    )
    validation = validate_yolo_weights(
        weights_path=weights_path,
        allowed_roots=allowed_root_paths,
        required_sha256=required_sha256,
    )
    normalized_class_map = validate_yolo_class_mapping(class_map or default_yolo_class_mapping())
    resolved_model_name = model_name or Path(validation.resolved_path).stem
    runtime_probe = probe_yolo_runtime(requested_device=device)
    model_metadata = (
        probe_yolo_model_metadata(validation.resolved_path, device=device)
        if probe_model
        else {
            "status": "skipped",
            "message": "Model metadata probe was not requested.",
            "device": device,
        }
    )

    model, reused = register_yolo_detection_model(
        session=session,
        weights_validation=validation,
        model_name=resolved_model_name,
        model_version=model_version,
        class_map=normalized_class_map,
        runtime_probe=runtime_probe,
        model_metadata=model_metadata,
        created_by=created_by,
    )
    return {
        "ok": True,
        "status": "registered_reused" if reused else "registered_created",
        "model_registry_id": model.id,
        "model_name": model.name,
        "model_version": model.version,
        "weights_path": validation.weights_path,
        "resolved_weights_path": validation.resolved_path,
        "weights_sha256": validation.sha256,
        "weights_size_bytes": validation.size_bytes,
        "class_map": normalized_class_map,
        "runtime_probe": runtime_probe,
        "model_metadata": model_metadata,
        "reused": reused,
    }


def register_yolo_detection_model(
    session: Session,
    weights_validation: YoloWeightsValidationResult,
    model_name: str,
    model_version: str,
    class_map: dict[str, Any],
    runtime_probe: dict[str, Any],
    model_metadata: dict[str, Any] | None = None,
    created_by: str = "tom-v3-worker",
) -> tuple[ModelRegistry, bool]:
    metadata = _model_metadata(
        weights_validation=weights_validation,
        model_name=model_name,
        model_version=model_version,
        class_map=class_map,
        runtime_probe=runtime_probe,
        model_metadata=model_metadata or {},
        created_by=created_by,
    )
    existing = session.scalars(
        select(ModelRegistry).where(
            ModelRegistry.name == model_name,
            ModelRegistry.version == model_version,
            ModelRegistry.model_family == "detection",
            ModelRegistry.source == "tom_v3_model_adapters.yolo_weights",
        )
    ).all()
    for model in existing:
        existing_metadata = model.metadata_jsonb or {}
        if (
            existing_metadata.get("weights_sha256") == weights_validation.sha256
            and existing_metadata.get("class_map") == class_map
            and existing_metadata.get("model_runtime") == "ultralytics"
        ):
            return model, True

    model = ModelRegistry(
        name=model_name,
        version=model_version,
        model_family="detection",
        source="tom_v3_model_adapters.yolo_weights",
        metadata_jsonb=metadata,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model, False


def _model_metadata(
    weights_validation: YoloWeightsValidationResult,
    model_name: str,
    model_version: str,
    class_map: dict[str, Any],
    runtime_probe: dict[str, Any],
    model_metadata: dict[str, Any],
    created_by: str,
) -> dict[str, Any]:
    runtime_versions = {
        "ultralytics": runtime_probe.get("ultralytics_version"),
        "torch": runtime_probe.get("torch_version"),
        "opencv": runtime_probe.get("opencv_version"),
    }
    return {
        "model_runtime": "ultralytics",
        "model_task": "detect",
        "model_name": model_name,
        "model_version": model_version,
        "weights_path": weights_validation.weights_path,
        "weights_resolved_path": weights_validation.resolved_path,
        "weights_sha256": weights_validation.sha256,
        "weights_size_bytes": weights_validation.size_bytes,
        "class_map": class_map,
        "class_names": model_metadata.get("class_names"),
        "runtime_probe": runtime_probe,
        "runtime_package_versions": runtime_versions,
        "model_metadata": model_metadata,
        "created_by": created_by,
        "blueprint": 3,
        "milestone": "3B",
        "portability_status": "registered_weights_no_inference",
        "no_detection_persistence": True,
    }
