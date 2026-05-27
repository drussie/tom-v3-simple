from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from tom_v3_schema.skeletons import COCO17_KEYPOINT_NAMES

from tom_v3_model_adapters.yolo_inference import FrameInferenceInput, YoloFrameInferenceError
from tom_v3_model_adapters.yolo_runtime import (
    YoloDeviceUnavailable,
    resolve_yolo_device,
    try_import_yolo_runtime,
)


class PoseResultProvider(Protocol):
    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        pass


@dataclass(frozen=True)
class PoseProviderConfig:
    weights_path: str
    device: str = "cpu"
    image_size: int | None = None
    confidence_threshold: float = 0.25
    iou_threshold: float | None = None
    max_det: int | None = None


class FakePoseResultProvider:
    def __init__(self, poses_by_frame: Mapping[int, list[dict[str, Any]]] | None = None) -> None:
        self.poses_by_frame = dict(poses_by_frame or {})

    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        poses = self.poses_by_frame.get(frame_input.frame_number)
        if poses is None:
            poses = [_default_fake_pose(frame_input)]
        return {
            "frame_number": frame_input.frame_number,
            "timestamp_ms": frame_input.timestamp_ms,
            "image_width": frame_input.image_width,
            "image_height": frame_input.image_height,
            "poses": poses,
        }


class UltralyticsPoseResultProvider:
    def __init__(
        self,
        weights_path: str,
        device: str = "cpu",
        image_size: int | None = None,
        confidence_threshold: float = 0.25,
        iou_threshold: float | None = None,
        max_det: int | None = None,
    ) -> None:
        self.config = PoseProviderConfig(
            weights_path=weights_path,
            device=device,
            image_size=image_size,
            confidence_threshold=confidence_threshold,
            iou_threshold=iou_threshold,
            max_det=max_det,
        )
        self._model: Any | None = None
        self._resolved_device: str | None = None

    @property
    def resolved_device(self) -> str | None:
        return self._resolved_device

    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        if frame_input.image is None:
            raise YoloFrameInferenceError(
                "real Ultralytics pose prediction requires a decoded image"
            )
        model = self._load_model()
        predictions = model.predict(
            frame_input.image,
            device=self._resolved_device,
            imgsz=self.config.image_size,
            conf=self.config.confidence_threshold,
            iou=self.config.iou_threshold,
            max_det=self.config.max_det,
            verbose=False,
        )
        result = predictions[0] if predictions else None
        return _ultralytics_pose_result_to_frame_dict(frame_input, result)

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model
        runtime = try_import_yolo_runtime()
        if runtime.ultralytics is None:
            raise YoloFrameInferenceError(
                "Ultralytics is required for real pose frame inference. "
                "Install the optional YOLO runtime and retry."
            )
        if runtime.torch is None:
            raise YoloFrameInferenceError(
                "Torch is required for real pose frame inference. "
                "Install the optional YOLO runtime and retry."
            )
        try:
            resolved = resolve_yolo_device(
                requested_device=self.config.device,
                torch_module=runtime.torch,
            )
        except YoloDeviceUnavailable as exc:
            raise YoloFrameInferenceError(str(exc)) from exc
        weights_path = Path(self.config.weights_path).expanduser()
        if not weights_path.is_file():
            raise YoloFrameInferenceError(f"pose weights file does not exist: {weights_path}")
        self._resolved_device = resolved.resolved_device
        self._model = runtime.ultralytics.YOLO(str(weights_path))
        return self._model


def _default_fake_pose(frame_input: FrameInferenceInput) -> dict[str, Any]:
    width = float(frame_input.image_width or 320)
    height = float(frame_input.image_height or 480)
    keypoints: list[dict[str, Any]] = []
    for index, _name in enumerate(COCO17_KEYPOINT_NAMES):
        column = index % 4
        row = index // 4
        keypoints.append(
            {
                "x": round(width * (0.2 + column * 0.16), 3),
                "y": round(height * (0.12 + row * 0.16), 3),
                "confidence": round(max(0.5, 0.94 - index * 0.015), 3),
            }
        )
    return {
        "bbox_xyxy": [0.0, 0.0, width, height],
        "bbox_confidence": 0.86,
        "pose_confidence": 0.83,
        "source_result_index": 0,
        "keypoints": keypoints,
    }


def _ultralytics_pose_result_to_frame_dict(
    frame_input: FrameInferenceInput,
    result: Any,
) -> dict[str, Any]:
    poses: list[dict[str, Any]] = []
    keypoints = getattr(result, "keypoints", None) if result is not None else None
    if keypoints is not None:
        xy_values = _to_list(getattr(keypoints, "xy", []))
        conf_values = _to_list(getattr(keypoints, "conf", []))
        boxes = getattr(result, "boxes", None)
        bbox_values = _to_list(getattr(boxes, "xyxy", [])) if boxes is not None else []
        bbox_conf_values = _to_list(getattr(boxes, "conf", [])) if boxes is not None else []
        for pose_index, pose_xy in enumerate(xy_values):
            pose_conf = conf_values[pose_index] if pose_index < len(conf_values) else []
            pose_keypoints = [
                {
                    "x": _optional_float(point[0] if len(point) > 0 else None),
                    "y": _optional_float(point[1] if len(point) > 1 else None),
                    "confidence": _optional_float(
                        pose_conf[keypoint_index]
                        if keypoint_index < len(pose_conf)
                        else None
                    ),
                }
                for keypoint_index, point in enumerate(pose_xy)
            ]
            bbox_xyxy = (
                [float(value) for value in bbox_values[pose_index]]
                if pose_index < len(bbox_values)
                else None
            )
            poses.append(
                {
                    "bbox_xyxy": bbox_xyxy,
                    "bbox_confidence": _optional_float(
                        bbox_conf_values[pose_index]
                        if pose_index < len(bbox_conf_values)
                        else None
                    ),
                    "pose_confidence": _mean_confidence(pose_keypoints),
                    "source_result_index": pose_index,
                    "keypoints": pose_keypoints,
                }
            )
    return {
        "frame_number": frame_input.frame_number,
        "timestamp_ms": frame_input.timestamp_ms,
        "image_width": frame_input.image_width,
        "image_height": frame_input.image_height,
        "poses": poses,
    }


def _to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value or [])


def _optional_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _mean_confidence(keypoints: list[dict[str, Any]]) -> float | None:
    confidences = [
        keypoint["confidence"]
        for keypoint in keypoints
        if keypoint.get("confidence") is not None
    ]
    if not confidences:
        return None
    return round(sum(confidences) / len(confidences), 6)
