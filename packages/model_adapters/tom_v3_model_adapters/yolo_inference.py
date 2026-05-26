from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from tom_v3_video.time_index import frame_to_timestamp_ms

from tom_v3_model_adapters.yolo_normalization import (
    build_detection_adapter_result_from_normalized,
    normalize_yolo_results,
)
from tom_v3_model_adapters.yolo_runtime import (
    YoloDeviceUnavailable,
    resolve_yolo_device,
    try_import_yolo_runtime,
)


class YoloFrameInferenceError(RuntimeError):
    pass


@dataclass(frozen=True)
class FrameInferenceInput:
    frame_number: int
    timestamp_ms: int
    image: Any | None
    image_width: int | None
    image_height: int | None
    source_path: str | None
    metadata: dict[str, Any]


class YoloFrameSource(Protocol):
    def iter_sampled_frames(
        self,
        media_path: str | None,
        fps: float,
        width: int | None,
        height: int | None,
        sampled_frames: Sequence[int],
    ) -> Iterator[FrameInferenceInput]:
        pass


class YoloResultProvider(Protocol):
    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        pass


class MetadataOnlyYoloFrameSource:
    def iter_sampled_frames(
        self,
        media_path: str | None,
        fps: float,
        width: int | None,
        height: int | None,
        sampled_frames: Sequence[int],
    ) -> Iterator[FrameInferenceInput]:
        for frame_number in sampled_frames:
            yield FrameInferenceInput(
                frame_number=frame_number,
                timestamp_ms=frame_to_timestamp_ms(fps, frame_number),
                image=None,
                image_width=width,
                image_height=height,
                source_path=media_path,
                metadata={"frame_time_owner": "media_indexing", "frame_source": "metadata_only"},
            )


class OpenCvYoloFrameSource:
    def iter_sampled_frames(
        self,
        media_path: str | None,
        fps: float,
        width: int | None,
        height: int | None,
        sampled_frames: Sequence[int],
    ) -> Iterator[FrameInferenceInput]:
        if media_path is None:
            raise YoloFrameInferenceError("media local path is required for YOLO frame inference")
        runtime = try_import_yolo_runtime()
        if runtime.cv2 is None:
            raise YoloFrameInferenceError(
                "OpenCV is required for real YOLO frame loading. "
                "Install the optional YOLO runtime and retry."
            )
        path = Path(media_path).expanduser()
        if not path.is_file():
            raise YoloFrameInferenceError(f"media local path does not exist: {path}")
        capture = runtime.cv2.VideoCapture(str(path))
        try:
            if not capture.isOpened():
                raise YoloFrameInferenceError(f"OpenCV could not open media file: {path}")
            for frame_number in sampled_frames:
                capture.set(runtime.cv2.CAP_PROP_POS_FRAMES, frame_number)
                ok, image = capture.read()
                if not ok:
                    raise YoloFrameInferenceError(
                        f"OpenCV could not decode frame {frame_number} from {path}"
                    )
                image_height, image_width = image.shape[:2]
                yield FrameInferenceInput(
                    frame_number=frame_number,
                    timestamp_ms=frame_to_timestamp_ms(fps, frame_number),
                    image=image,
                    image_width=int(image_width or width or 0),
                    image_height=int(image_height or height or 0),
                    source_path=str(path),
                    metadata={
                        "frame_time_owner": "media_indexing",
                        "frame_source": "opencv_video_capture",
                    },
                )
        finally:
            capture.release()


class FakeYoloResultProvider:
    def __init__(self, boxes_by_frame: Mapping[int, list[dict[str, Any]]] | None = None) -> None:
        self.boxes_by_frame = dict(boxes_by_frame or {})

    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        boxes = self.boxes_by_frame.get(frame_input.frame_number)
        if boxes is None:
            boxes = _default_fake_boxes(frame_input)
        return {
            "frame_number": frame_input.frame_number,
            "timestamp_ms": frame_input.timestamp_ms,
            "image_width": frame_input.image_width,
            "image_height": frame_input.image_height,
            "boxes": boxes,
        }


class UltralyticsYoloResultProvider:
    def __init__(
        self,
        weights_path: str,
        device: str = "cpu",
        image_size: int | None = None,
        confidence_threshold: float = 0.25,
        iou_threshold: float | None = None,
        max_det: int | None = None,
    ) -> None:
        self.weights_path = weights_path
        self.requested_device = device
        self.image_size = image_size
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.max_det = max_det
        self._model: Any | None = None
        self._resolved_device: str | None = None

    @property
    def resolved_device(self) -> str | None:
        return self._resolved_device

    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        if frame_input.image is None:
            raise YoloFrameInferenceError("real Ultralytics prediction requires a decoded image")
        model = self._load_model()
        predictions = model.predict(
            frame_input.image,
            device=self._resolved_device,
            imgsz=self.image_size,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            max_det=self.max_det,
            verbose=False,
        )
        result = predictions[0] if predictions else None
        return _ultralytics_result_to_frame_dict(frame_input, result, model)

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model
        runtime = try_import_yolo_runtime()
        if runtime.ultralytics is None:
            raise YoloFrameInferenceError(
                "Ultralytics is required for real YOLO frame inference. "
                "Install the optional YOLO runtime and retry."
            )
        if runtime.torch is None:
            raise YoloFrameInferenceError(
                "Torch is required for real YOLO frame inference. "
                "Install the optional YOLO runtime and retry."
            )
        try:
            resolved = resolve_yolo_device(
                requested_device=self.requested_device,
                torch_module=runtime.torch,
            )
        except YoloDeviceUnavailable as exc:
            raise YoloFrameInferenceError(str(exc)) from exc
        weights_path = Path(self.weights_path).expanduser()
        if not weights_path.is_file():
            raise YoloFrameInferenceError(f"YOLO weights file does not exist: {weights_path}")
        self._resolved_device = resolved.resolved_device
        self._model = runtime.ultralytics.YOLO(str(weights_path))
        return self._model


def sample_frame_numbers(
    frame_count: int,
    frame_sample_rate: int,
    max_frames: int | None,
) -> list[int]:
    if frame_count < 1:
        raise YoloFrameInferenceError("YOLO frame inference requires indexed frames")
    if frame_sample_rate <= 0:
        raise YoloFrameInferenceError("frame_sample_rate must be greater than 0")
    sampled_frames = list(range(0, frame_count, frame_sample_rate))
    if not sampled_frames:
        sampled_frames = [0]
    if max_frames is not None:
        sampled_frames = sampled_frames[: max(1, int(max_frames))]
    return sampled_frames


def run_yolo_frame_inference(
    media_path: str | None,
    fps: float | None,
    frame_count: int | None,
    width: int | None,
    height: int | None,
    frame_sample_rate: int,
    max_frames: int | None,
    class_mapping: Mapping[str, Any] | None,
    model_registry_id: str | None,
    runtime_config_id: str | None,
    weights_sha256: str | None,
    inference_metadata: Mapping[str, Any],
    result_provider: YoloResultProvider | None = None,
    frame_source: YoloFrameSource | None = None,
):
    if fps is None or fps <= 0:
        raise YoloFrameInferenceError("YOLO frame inference requires positive media fps")
    if frame_count is None:
        raise YoloFrameInferenceError("YOLO frame inference requires indexed frame_count")
    provider = result_provider or UltralyticsYoloResultProvider(
        weights_path=str(inference_metadata.get("weights_path") or ""),
        device=str(inference_metadata.get("device") or "cpu"),
        image_size=_optional_int(inference_metadata.get("imgsz")),
        confidence_threshold=float(inference_metadata.get("conf") or 0.25),
        iou_threshold=_optional_float(inference_metadata.get("iou")),
        max_det=_optional_int(inference_metadata.get("max_det")),
    )
    source = frame_source or (
        MetadataOnlyYoloFrameSource()
        if isinstance(provider, FakeYoloResultProvider)
        else OpenCvYoloFrameSource()
    )
    sampled_frames = sample_frame_numbers(frame_count, frame_sample_rate, max_frames)
    frame_inputs = source.iter_sampled_frames(
        media_path,
        fps,
        width,
        height,
        sampled_frames,
    )
    frame_results = [
        provider.predict_frame(frame_input)
        for frame_input in frame_inputs
    ]
    normalized = normalize_yolo_results(
        frame_results,
        class_mapping=class_mapping,
        model_registry_id=model_registry_id,
        runtime_config_id=runtime_config_id,
        inference_metadata={
            **dict(inference_metadata),
            "weights_sha256": weights_sha256,
            "sampled_frames": sampled_frames,
        },
    )
    adapter_result = build_detection_adapter_result_from_normalized(normalized)
    return adapter_result, {
        "frames_processed": len(sampled_frames),
        "sampled_frames": sampled_frames,
        "input_box_count": normalized.input_box_count,
        "mapped_detection_count": normalized.mapped_detection_count,
        "unmapped_detection_count": normalized.unmapped_detection_count,
        "unmapped_classes": normalized.unmapped_classes,
        "warnings": normalized.warnings,
        "source_runtime": "ultralytics_yolo",
    }


def _default_fake_boxes(frame_input: FrameInferenceInput) -> list[dict[str, Any]]:
    width = float(frame_input.image_width or 640)
    height = float(frame_input.image_height or 360)
    return [
        {
            "xyxy": [width * 0.45, height * 0.35, width * 0.45 + 12, height * 0.35 + 12],
            "confidence": 0.91,
            "class_id": 32,
            "class_name": "sports ball",
            "source_result_index": 0,
        },
        {
            "xyxy": [width * 0.58, height * 0.2, width * 0.78, height * 0.9],
            "confidence": 0.87,
            "class_id": 0,
            "class_name": "person",
            "source_result_index": 1,
        },
    ]


def _ultralytics_result_to_frame_dict(
    frame_input: FrameInferenceInput,
    result: Any,
    model: Any,
) -> dict[str, Any]:
    boxes_output: list[dict[str, Any]] = []
    if result is not None and getattr(result, "boxes", None) is not None:
        names = getattr(result, "names", None) or getattr(model, "names", {}) or {}
        boxes = result.boxes
        xyxy_values = _to_list(getattr(boxes, "xyxy", []))
        conf_values = _to_list(getattr(boxes, "conf", []))
        cls_values = _to_list(getattr(boxes, "cls", []))
        for index, xyxy in enumerate(xyxy_values):
            class_id = _optional_int(cls_values[index] if index < len(cls_values) else None)
            boxes_output.append(
                {
                    "xyxy": [float(value) for value in xyxy],
                    "confidence": _optional_float(
                        conf_values[index] if index < len(conf_values) else None
                    ),
                    "class_id": class_id,
                    "class_name": _class_name(names, class_id),
                    "source_result_index": index,
                }
            )
    return {
        "frame_number": frame_input.frame_number,
        "timestamp_ms": frame_input.timestamp_ms,
        "image_width": frame_input.image_width,
        "image_height": frame_input.image_height,
        "boxes": boxes_output,
    }


def _to_list(value: Any) -> list[Any]:
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value or [])


def _class_name(names: Any, class_id: int | None) -> str | None:
    if class_id is None:
        return None
    if isinstance(names, Mapping):
        return str(names.get(class_id) or names.get(str(class_id)) or class_id)
    if isinstance(names, Sequence) and 0 <= class_id < len(names):
        return str(names[class_id])
    return str(class_id)


def _optional_int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
