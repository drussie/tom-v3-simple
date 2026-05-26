from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from tom_v3_model_adapters.detection import (
    BBox,
    DetectionAdapterResult,
    DetectionObservation,
    Point,
)
from tom_v3_model_adapters.yolo_weights import (
    default_yolo_class_mapping,
    validate_yolo_class_mapping,
)

SOURCE_RUNTIME = "ultralytics_yolo"
ADAPTER_NAME = "ultralytics-yolo-detection-normalizer"
ADAPTER_VERSION = "v0"


@dataclass(frozen=True)
class NormalizedYoloDetection:
    observation_type: str
    target_label: str
    frame_number: int
    timestamp_ms: int
    confidence: float
    bbox: dict[str, float]
    center: dict[str, float]
    class_id: int | None
    class_label: str | None
    raw_class_id: int | None
    raw_class_name: str | None
    coordinate_space: str = "image_pixels"
    frame_time_owner: str = "media_indexing"
    source_runtime: str = SOURCE_RUNTIME
    source_result_index: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_payload(self) -> dict[str, Any]:
        return {
            "label": self.target_label,
            "bbox": self.bbox,
            "center": self.center,
            "class_id": self.class_id,
            "class_label": self.class_label,
            "confidence": self.confidence,
            "coordinate_space": self.coordinate_space,
            "frame_time_owner": self.frame_time_owner,
            "source_runtime": self.source_runtime,
            **self.metadata,
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            "observation_type": self.observation_type,
            "target_label": self.target_label,
            "frame_number": self.frame_number,
            "timestamp_ms": self.timestamp_ms,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "center": self.center,
            "class_id": self.class_id,
            "class_label": self.class_label,
            "raw_class_id": self.raw_class_id,
            "raw_class_name": self.raw_class_name,
            "coordinate_space": self.coordinate_space,
            "frame_time_owner": self.frame_time_owner,
            "source_runtime": self.source_runtime,
            "source_result_index": self.source_result_index,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class YoloNormalizationResult:
    detections: list[NormalizedYoloDetection]
    input_box_count: int
    mapped_detection_count: int
    unmapped_detection_count: int
    unmapped_classes: list[dict[str, Any]]
    warnings: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "detections": [detection.as_dict() for detection in self.detections],
            "input_box_count": self.input_box_count,
            "mapped_detection_count": self.mapped_detection_count,
            "unmapped_detection_count": self.unmapped_detection_count,
            "unmapped_classes": self.unmapped_classes,
            "warnings": self.warnings,
        }


def normalize_yolo_frame_result(
    frame_result: Mapping[str, Any],
    class_mapping: Mapping[str, Any] | None = None,
    model_registry_id: str | None = None,
    runtime_config_id: str | None = None,
    inference_metadata: Mapping[str, Any] | None = None,
) -> YoloNormalizationResult:
    normalized_mapping = validate_yolo_class_mapping(class_mapping or default_yolo_class_mapping())
    frame_number = int(frame_result["frame_number"])
    timestamp_ms = int(frame_result["timestamp_ms"])
    boxes = list(frame_result.get("boxes") or [])
    detections: list[NormalizedYoloDetection] = []
    unmapped_classes: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for fallback_index, box in enumerate(boxes):
        source_result_index = _source_result_index(box, fallback_index)
        class_id = _optional_int(_box_value(box, "class_id", "cls"))
        class_name = _optional_string(_box_value(box, "class_name", "name", "class_label"))
        mapping_entry = _match_mapping(
            class_id=class_id,
            class_name=class_name,
            class_mapping=normalized_mapping,
        )
        if mapping_entry is None:
            unmapped_classes.append(
                {
                    "class_id": class_id,
                    "class_name": class_name,
                    "source_result_index": source_result_index,
                }
            )
            continue

        xyxy = _box_value(box, "xyxy")
        bbox = _xyxy_to_bbox(xyxy)
        if bbox is None:
            warnings.append(
                {
                    "warning_type": "invalid_bbox",
                    "message": "bbox xyxy must contain four numeric values with positive area",
                    "source_result_index": source_result_index,
                    "xyxy": xyxy,
                }
            )
            continue

        confidence = _numeric_confidence(_box_value(box, "confidence", "conf"))
        if confidence is None:
            warnings.append(
                {
                    "warning_type": "invalid_confidence",
                    "message": "confidence must be numeric",
                    "source_result_index": source_result_index,
                }
            )
            continue
        if confidence < 0 or confidence > 1:
            warnings.append(
                {
                    "warning_type": "confidence_out_of_range",
                    "message": "confidence is outside the expected 0..1 range",
                    "source_result_index": source_result_index,
                    "confidence": confidence,
                }
            )

        bbox_dict = {
            "x": bbox[0],
            "y": bbox[1],
            "width": bbox[2],
            "height": bbox[3],
        }
        center = {
            "x": bbox[0] + bbox[2] / 2,
            "y": bbox[1] + bbox[3] / 2,
        }
        xywh = [bbox[0], bbox[1], bbox[2], bbox[3]]
        target_label = mapping_entry["target_label"]
        metadata = {
            "adapter": "ultralytics_yolo_detection",
            "adapter_version": ADAPTER_VERSION,
            "raw_class_id": class_id,
            "raw_class_name": class_name,
            "target_label": target_label,
            "xyxy": [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]],
            "xywh": xywh,
            "source_result_index": source_result_index,
            "frame_time_owner": "media_indexing",
            "source_runtime": SOURCE_RUNTIME,
            "model_registry_id": model_registry_id,
            "runtime_config_id": runtime_config_id,
            "inference": dict(inference_metadata or {}),
        }
        detections.append(
            NormalizedYoloDetection(
                observation_type=mapping_entry["target_observation_type"],
                target_label=target_label,
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                confidence=confidence,
                bbox=bbox_dict,
                center=center,
                class_id=class_id,
                class_label=class_name,
                raw_class_id=class_id,
                raw_class_name=class_name,
                source_result_index=source_result_index,
                metadata=metadata,
            )
        )

    return YoloNormalizationResult(
        detections=detections,
        input_box_count=len(boxes),
        mapped_detection_count=len(detections),
        unmapped_detection_count=len(unmapped_classes),
        unmapped_classes=unmapped_classes,
        warnings=warnings,
    )


def normalize_yolo_results(
    frame_results: Iterable[Mapping[str, Any]],
    class_mapping: Mapping[str, Any] | None = None,
    model_registry_id: str | None = None,
    runtime_config_id: str | None = None,
    inference_metadata: Mapping[str, Any] | None = None,
) -> YoloNormalizationResult:
    aggregate_detections: list[NormalizedYoloDetection] = []
    aggregate_unmapped: list[dict[str, Any]] = []
    aggregate_warnings: list[dict[str, Any]] = []
    input_box_count = 0

    for frame_result in frame_results:
        result = normalize_yolo_frame_result(
            frame_result,
            class_mapping=class_mapping,
            model_registry_id=model_registry_id,
            runtime_config_id=runtime_config_id,
            inference_metadata=inference_metadata,
        )
        aggregate_detections.extend(result.detections)
        aggregate_unmapped.extend(result.unmapped_classes)
        aggregate_warnings.extend(result.warnings)
        input_box_count += result.input_box_count

    return YoloNormalizationResult(
        detections=aggregate_detections,
        input_box_count=input_box_count,
        mapped_detection_count=len(aggregate_detections),
        unmapped_detection_count=len(aggregate_unmapped),
        unmapped_classes=aggregate_unmapped,
        warnings=aggregate_warnings,
    )


def build_detection_adapter_result_from_normalized(
    result: YoloNormalizationResult,
) -> DetectionAdapterResult:
    return DetectionAdapterResult(
        adapter_name=ADAPTER_NAME,
        adapter_version=ADAPTER_VERSION,
        detections=[
            DetectionObservation(
                label=detection.target_label,  # type: ignore[arg-type]
                frame_number=detection.frame_number,
                timestamp_ms=detection.timestamp_ms,
                confidence=detection.confidence,
                bbox=BBox(**detection.bbox),
                center=Point(**detection.center),
                class_id=detection.class_id,
                class_label=detection.class_label,
                metadata=detection.metadata,
            )
            for detection in result.detections
        ],
        diagnostics={
            "source_runtime": SOURCE_RUNTIME,
            "input_box_count": result.input_box_count,
            "mapped_detection_count": result.mapped_detection_count,
            "unmapped_detection_count": result.unmapped_detection_count,
            "unmapped_classes": result.unmapped_classes,
            "warnings": result.warnings,
            "note": "normalization-only adapter result; no real inference was run",
        },
    )


def _match_mapping(
    class_id: int | None,
    class_name: str | None,
    class_mapping: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    normalized_name = _normalize_class_name(class_name)
    for entry in class_mapping.values():
        source_ids = {int(value) for value in entry.get("source_class_ids", [])}
        source_names = {
            _normalize_class_name(name) for name in entry.get("source_class_names", [])
        }
        if class_id is not None and class_id in source_ids:
            return entry
        if normalized_name and normalized_name in source_names:
            return entry
    return None


def _normalize_class_name(class_name: str | None) -> str | None:
    if class_name is None:
        return None
    return " ".join(class_name.strip().lower().replace("_", " ").replace("-", " ").split())


def _xyxy_to_bbox(xyxy: Any) -> tuple[float, float, float, float] | None:
    if not isinstance(xyxy, list | tuple) or len(xyxy) != 4:
        return None
    try:
        x1, y1, x2, y2 = [float(value) for value in xyxy]
    except (TypeError, ValueError):
        return None
    width = x2 - x1
    height = y2 - y1
    if width <= 0 or height <= 0:
        return None
    return x1, y1, width, height


def _numeric_confidence(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _source_result_index(box: Any, fallback_index: int) -> int:
    value = _box_value(box, "source_result_index")
    parsed = _optional_int(value)
    return fallback_index if parsed is None else parsed


def _optional_int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _box_value(box: Any, *keys: str) -> Any:
    for key in keys:
        if isinstance(box, Mapping) and key in box:
            return box[key]
        if not isinstance(box, Mapping) and hasattr(box, key):
            return getattr(box, key)
    return None
