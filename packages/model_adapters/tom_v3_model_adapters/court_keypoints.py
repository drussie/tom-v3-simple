from __future__ import annotations

import hashlib
from collections import OrderedDict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from tom_v3_schema.court import COURT_KEYPOINT_NAMES

from tom_v3_model_adapters.yolo_inference import (
    FrameInferenceInput,
    MetadataOnlyYoloFrameSource,
    OpenCvYoloFrameSource,
    YoloFrameInferenceError,
    YoloFrameSource,
    sample_frame_numbers,
)
from tom_v3_model_adapters.yolo_runtime import (
    YoloDeviceUnavailable,
    resolve_yolo_device,
    try_import_yolo_runtime,
)

TOM_V1_COURT_KEYPOINT_MODEL_INPUT_SIZE = 224
TOM_V1_COURT_KEYPOINT_OUTPUT_PAIR_COUNT = 14
TOM_V1_COURT_KEYPOINT_OUTPUT_REFERENCE_SIZE = 224.0
TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE = "full_frame_resize_224"
TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION = "output_as_pixels_224"
SUPPORTED_TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODES = {
    TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE
}
SUPPORTED_TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATIONS = {
    TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION
}

TOM_V1_RAW_COURT_KEYPOINT_NAMES = [
    "far_left_baseline_corner",
    "far_right_baseline_corner",
    "near_left_baseline_corner",
    "near_right_baseline_corner",
    "far_left_singles_sideline_corner",
    "near_left_singles_sideline_corner",
    "far_right_singles_sideline_corner",
    "near_right_singles_sideline_corner",
    "service_line_t_far_left",
    "service_line_t_far_right",
    "service_line_t_near_left",
    "service_line_t_near_right",
    "center_service_t_far",
    "center_service_t_near",
]

DIRECT_TOM_V1_TO_TOM_V3_KEYPOINT_INDEX = {
    "near_left_baseline_corner": 2,
    "near_right_baseline_corner": 3,
    "far_left_baseline_corner": 0,
    "far_right_baseline_corner": 1,
    "service_line_t_near_left": 10,
    "service_line_t_near_right": 11,
    "service_line_t_far_left": 8,
    "service_line_t_far_right": 9,
}


class CourtKeypointAdapterError(RuntimeError):
    pass


@dataclass(frozen=True)
class CourtKeypointWeightsValidationResult:
    weights_path: str
    resolved_path: str
    exists: bool
    is_file: bool
    suffix: str | None
    size_bytes: int | None
    sha256: str | None
    status: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "weights_path": self.weights_path,
            "resolved_path": self.resolved_path,
            "exists": self.exists,
            "is_file": self.is_file,
            "suffix": self.suffix,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "status": self.status,
            "message": self.message,
        }


class CourtKeypointResultProvider(Protocol):
    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        pass


class FakeCourtKeypointResultProvider:
    def __init__(
        self,
        raw_keypoints_by_frame: Mapping[int, list[dict[str, Any]]] | None = None,
    ) -> None:
        self.raw_keypoints_by_frame = dict(raw_keypoints_by_frame or {})

    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        raw_keypoints = self.raw_keypoints_by_frame.get(frame_input.frame_number)
        if raw_keypoints is None:
            raw_keypoints = _default_tom_v1_raw_keypoints()
        return {
            "frame_number": frame_input.frame_number,
            "timestamp_ms": frame_input.timestamp_ms,
            "image_width": frame_input.image_width,
            "image_height": frame_input.image_height,
            "raw_keypoints": raw_keypoints,
            "raw_model_payload": {
                "provider": "fake_court_keypoint_result_provider",
                "tom_v1_raw_keypoint_count": len(raw_keypoints),
            },
        }


class TorchvisionResNetCourtKeypointProvider:
    def __init__(
        self,
        *,
        weights_path: str,
        device: str = "cpu",
        requested_image_size: int | None = None,
        confidence: float = 0.7,
    ) -> None:
        self.weights_path = weights_path
        self.requested_device = device
        self.requested_image_size = requested_image_size
        self.confidence = confidence
        self.model_input_size = TOM_V1_COURT_KEYPOINT_MODEL_INPUT_SIZE
        self.output_reference_size = TOM_V1_COURT_KEYPOINT_OUTPUT_REFERENCE_SIZE
        self._model: Any | None = None
        self._resolved_device: str | None = None

    @property
    def resolved_device(self) -> str | None:
        return self._resolved_device

    def predict_frame(self, frame_input: FrameInferenceInput) -> Mapping[str, Any]:
        if frame_input.image is None:
            raise CourtKeypointAdapterError(
                "real TOM v1 court keypoint prediction requires a decoded image"
            )
        runtime = try_import_yolo_runtime()
        if runtime.cv2 is None:
            raise CourtKeypointAdapterError(
                "OpenCV is required for TOM v1 court keypoint frame preprocessing."
            )
        model = self._load_model()
        tensor = self._preprocess(frame_input.image, runtime)
        with runtime.torch.no_grad():
            output = model(tensor)
        values = _to_list(output.squeeze(0))
        raw_keypoints = _raw_pairs_from_output(values, confidence=self.confidence)
        return {
            "frame_number": frame_input.frame_number,
            "timestamp_ms": frame_input.timestamp_ms,
            "image_width": frame_input.image_width,
            "image_height": frame_input.image_height,
            "raw_keypoints": raw_keypoints,
            "raw_model_payload": {
                "provider": "torchvision_resnet50_fc28_tom_v1",
                "requested_device": self.requested_device,
                "resolved_device": self._resolved_device,
                "requested_image_size": self.requested_image_size,
                "preprocessing_mode": TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE,
                "coordinate_interpretation": (
                    TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION
                ),
                "model_input_size": self.model_input_size,
                "output_reference_size": self.output_reference_size,
                "raw_output_pair_count": len(raw_keypoints),
                "model_confidence_head": False,
            },
        }

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model
        runtime = try_import_yolo_runtime()
        if runtime.torch is None:
            raise CourtKeypointAdapterError(
                "Torch is required for TOM v1 court keypoint inference."
            )
        try:
            import torchvision
        except Exception as exc:  # pragma: no cover - exercised by runtime probes.
            raise CourtKeypointAdapterError(
                "torchvision is required for the recognized TOM v1 ResNet50 court "
                "keypoint state_dict."
            ) from exc
        try:
            resolved = resolve_yolo_device(
                requested_device=self.requested_device,
                torch_module=runtime.torch,
            )
        except YoloDeviceUnavailable as exc:
            raise CourtKeypointAdapterError(str(exc)) from exc
        weights_path = Path(self.weights_path).expanduser()
        if not weights_path.is_file():
            raise CourtKeypointAdapterError(
                f"TOM v1 court keypoint weights file does not exist: {weights_path}"
            )
        state_dict = runtime.torch.load(
            weights_path,
            map_location="cpu",
            weights_only=True,
        )
        if not is_recognized_tom_v1_resnet50_state_dict(state_dict):
            raise CourtKeypointAdapterError(
                "keypoints_model.pth is not a recognized TOM v1 ResNet50 fc28 state_dict."
            )
        model = torchvision.models.resnet50(weights=None)
        model.fc = runtime.torch.nn.Linear(
            model.fc.in_features,
            TOM_V1_COURT_KEYPOINT_OUTPUT_PAIR_COUNT * 2,
        )
        model.load_state_dict(state_dict)
        model.eval()
        model.to(resolved.resolved_device)
        self._resolved_device = resolved.resolved_device
        self._model = model
        return model

    def _preprocess(self, image: Any, runtime: Any) -> Any:
        cv2 = runtime.cv2
        torch = runtime.torch
        resized = cv2.resize(image, (self.model_input_size, self.model_input_size))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = torch.from_numpy(rgb).float().permute(2, 0, 1) / 255.0
        mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        tensor = ((tensor - mean) / std).unsqueeze(0)
        return tensor.to(self._resolved_device or "cpu")


def probe_tom_v1_court_keypoint_model(
    *,
    weights_path: str,
    allowed_roots: Sequence[str | Path] | None = None,
) -> dict[str, Any]:
    validation = validate_court_keypoint_weights(
        weights_path,
        allowed_roots=allowed_roots,
        raise_on_error=False,
    )
    result: dict[str, Any] = {
        "ok": validation.status == "ok",
        "weights_path": weights_path,
        "weights_validation": validation.as_dict(),
        "sha256": validation.sha256,
        "size_bytes": validation.size_bytes,
        "load_strategy": "not_loaded",
        "requires_custom_model_class": None,
        "expected_adapter_status": "unsupported",
        "no_adjudication": True,
        "geometry_evidence_only": True,
        "model_output_not_truth": True,
    }
    if validation.status != "ok":
        result.update(
            {
                "ok": False,
                "status": validation.status,
                "message": validation.message,
            }
        )
        return result

    runtime = try_import_yolo_runtime()
    if runtime.torch is None:
        result.update(
            {
                "ok": False,
                "status": "missing_torch",
                "message": "Torch is required to inspect keypoints_model.pth.",
            }
        )
        return result

    try:
        state_dict = runtime.torch.load(
            validation.resolved_path,
            map_location="cpu",
            weights_only=True,
        )
    except Exception as exc:
        result.update(
            {
                "ok": False,
                "status": "unsupported_model_format_or_missing_model_definition",
                "load_strategy": "torch_load_failed",
                "message": str(exc),
            }
        )
        return result

    try:
        import torchvision  # noqa: F401

        torchvision_available = True
    except Exception:
        torchvision_available = False

    result["load_strategy"] = "torch_load_state_dict"
    result["state_dict_type"] = type(state_dict).__name__
    result["state_dict_key_count"] = len(state_dict) if isinstance(state_dict, Mapping) else None
    result["state_dict_keys_preview"] = (
        list(state_dict.keys())[:20] if isinstance(state_dict, Mapping) else []
    )
    result["torchvision_available"] = torchvision_available
    result["recognized_architecture"] = (
        "torchvision_resnet50_fc28_xy224"
        if is_recognized_tom_v1_resnet50_state_dict(state_dict)
        else None
    )
    if is_recognized_tom_v1_resnet50_state_dict(state_dict) and torchvision_available:
        result.update(
            {
                "ok": True,
                "status": "ready",
                "requires_custom_model_class": False,
                "expected_adapter_status": "ready",
                "model_input_size": TOM_V1_COURT_KEYPOINT_MODEL_INPUT_SIZE,
                "raw_output_pair_count": TOM_V1_COURT_KEYPOINT_OUTPUT_PAIR_COUNT,
                "raw_output_coordinate_space": "model_input_pixels_224",
                "mapping_status": "tom_v1_14_point_to_tom_v3_12_point_mapping_v0",
                "message": (
                    "keypoints_model.pth is a recognized TOM v1 ResNet50 state_dict "
                    "with 14 xy output pairs. TOM v3 can run it through the local "
                    "court keypoint adapter."
                ),
            }
        )
        return result

    result.update(
        {
            "ok": False,
            "status": "unsupported_model_format_or_missing_model_definition",
            "requires_custom_model_class": True,
            "expected_adapter_status": "needs_tom_v1_model_definition",
            "message": (
                "keypoints_model.pth could be loaded as a state_dict, but TOM v3 "
                "does not recognize the architecture/output head yet."
            ),
        }
    )
    return result


def validate_court_keypoint_weights(
    weights_path: str | Path,
    *,
    allowed_roots: Sequence[str | Path] | None = None,
    raise_on_error: bool = True,
) -> CourtKeypointWeightsValidationResult:
    original_path = str(weights_path)
    path = Path(weights_path).expanduser()
    resolved_path = path.resolve(strict=False)
    suffix = resolved_path.suffix.lower() or None
    if allowed_roots is not None and not _is_within_allowed_roots(
        resolved_path,
        allowed_roots,
    ):
        result = CourtKeypointWeightsValidationResult(
            weights_path=original_path,
            resolved_path=str(resolved_path),
            exists=resolved_path.exists(),
            is_file=resolved_path.is_file(),
            suffix=suffix,
            size_bytes=None,
            sha256=None,
            status="invalid_path",
            message="court keypoint weights path resolves outside the allowed roots.",
        )
        return _result_or_raise(result, raise_on_error)
    if not resolved_path.exists():
        result = CourtKeypointWeightsValidationResult(
            weights_path=original_path,
            resolved_path=str(resolved_path),
            exists=False,
            is_file=False,
            suffix=suffix,
            size_bytes=None,
            sha256=None,
            status="missing",
            message=f"court keypoint weights file does not exist: {resolved_path}",
        )
        return _result_or_raise(result, raise_on_error)
    if not resolved_path.is_file():
        result = CourtKeypointWeightsValidationResult(
            weights_path=original_path,
            resolved_path=str(resolved_path),
            exists=True,
            is_file=False,
            suffix=suffix,
            size_bytes=None,
            sha256=None,
            status="invalid_path",
            message="court keypoint weights path must point to a file.",
        )
        return _result_or_raise(result, raise_on_error)
    if suffix not in {".pth", ".pt"}:
        result = CourtKeypointWeightsValidationResult(
            weights_path=original_path,
            resolved_path=str(resolved_path),
            exists=True,
            is_file=True,
            suffix=suffix,
            size_bytes=None,
            sha256=None,
            status="invalid_suffix",
            message="court keypoint weights must use .pth or .pt.",
        )
        return _result_or_raise(result, raise_on_error)
    size_bytes = resolved_path.stat().st_size
    if size_bytes <= 0:
        result = CourtKeypointWeightsValidationResult(
            weights_path=original_path,
            resolved_path=str(resolved_path),
            exists=True,
            is_file=True,
            suffix=suffix,
            size_bytes=size_bytes,
            sha256=None,
            status="invalid_file",
            message="court keypoint weights file is empty.",
        )
        return _result_or_raise(result, raise_on_error)
    return CourtKeypointWeightsValidationResult(
        weights_path=original_path,
        resolved_path=str(resolved_path),
        exists=True,
        is_file=True,
        suffix=suffix,
        size_bytes=size_bytes,
        sha256=_sha256_file(resolved_path),
        status="ok",
        message="court keypoint weights file validated.",
    )


def run_court_keypoint_frame_inference(
    *,
    media_path: str | None,
    fps: float | None,
    frame_count: int | None,
    width: int | None,
    height: int | None,
    frame_sample_rate: int,
    max_frames: int | None,
    frame_start: int | None = None,
    frame_end: int | None = None,
    result_provider: CourtKeypointResultProvider | None = None,
    frame_source: YoloFrameSource | None = None,
    inference_metadata: Mapping[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if fps is None or fps <= 0:
        raise CourtKeypointAdapterError("court keypoint inference requires positive media fps")
    if frame_count is None:
        raise CourtKeypointAdapterError("court keypoint inference requires indexed frame_count")
    inference_metadata = inference_metadata or {}
    preprocessing_mode = str(
        inference_metadata.get("preprocessing_mode")
        or TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE
    )
    coordinate_interpretation = str(
        inference_metadata.get("coordinate_interpretation")
        or TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION
    )
    validate_court_keypoint_calibration_options(
        preprocessing_mode=preprocessing_mode,
        coordinate_interpretation=coordinate_interpretation,
    )
    provider = result_provider or TorchvisionResNetCourtKeypointProvider(
        weights_path=str(inference_metadata.get("weights_path") or ""),
        device=str(inference_metadata.get("device") or "cpu"),
        requested_image_size=_optional_int(inference_metadata.get("img_size")),
    )
    source = frame_source or (
        MetadataOnlyYoloFrameSource()
        if isinstance(provider, FakeCourtKeypointResultProvider)
        else OpenCvYoloFrameSource()
    )
    try:
        sampled_frames = sample_frame_numbers(
            int(frame_count),
            frame_sample_rate,
            max_frames,
            frame_start=frame_start,
            frame_end=frame_end,
        )
    except YoloFrameInferenceError as exc:
        raise CourtKeypointAdapterError(str(exc)) from exc
    frame_inputs = source.iter_sampled_frames(
        media_path,
        fps,
        width,
        height,
        sampled_frames,
    )
    frame_results = [
        normalize_tom_v1_court_keypoint_frame_result(frame_result, inference_metadata)
        for frame_result in (provider.predict_frame(frame_input) for frame_input in frame_inputs)
    ]
    return frame_results, {
        "frames_considered": len(sampled_frames),
        "frames_processed": len(frame_results),
        "sampled_frames": sampled_frames,
        "frame_start": frame_start,
        "frame_end": frame_end,
        "frame_sample_rate": frame_sample_rate,
        "max_frames": max_frames,
        "source_runtime": "tom_v1_court_keypoints",
        "preprocessing_mode": preprocessing_mode,
        "coordinate_interpretation": coordinate_interpretation,
        "model_input_size": TOM_V1_COURT_KEYPOINT_MODEL_INPUT_SIZE,
        "raw_output_pair_count": TOM_V1_COURT_KEYPOINT_OUTPUT_PAIR_COUNT,
        "mapping_status": "tom_v1_14_point_to_tom_v3_12_point_mapping_v0",
    }


def normalize_tom_v1_court_keypoint_frame_result(
    frame_result: Mapping[str, Any],
    inference_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    inference_metadata = inference_metadata or {}
    raw_keypoints = list(frame_result.get("raw_keypoints") or [])
    image_width = int(frame_result.get("image_width") or 0)
    image_height = int(frame_result.get("image_height") or 0)
    preprocessing_mode = str(
        inference_metadata.get("preprocessing_mode")
        or TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE
    )
    coordinate_interpretation = str(
        inference_metadata.get("coordinate_interpretation")
        or TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION
    )
    validate_court_keypoint_calibration_options(
        preprocessing_mode=preprocessing_mode,
        coordinate_interpretation=coordinate_interpretation,
    )
    if len(raw_keypoints) != TOM_V1_COURT_KEYPOINT_OUTPUT_PAIR_COUNT:
        raise CourtKeypointAdapterError(
            "TOM v1 court keypoint output must contain 14 raw keypoint pairs."
        )
    raw_keypoints_scaled_to_image = scale_tom_v1_raw_keypoints_for_image(
        raw_keypoints,
        image_width=image_width,
        image_height=image_height,
        coordinate_interpretation=coordinate_interpretation,
    )
    v3_keypoints = map_tom_v1_raw_keypoints_to_tom_v3(
        raw_keypoints,
        image_width=image_width,
        image_height=image_height,
    )
    return {
        "frame_number": int(frame_result["frame_number"]),
        "timestamp_ms": int(frame_result["timestamp_ms"]),
        "image_width": image_width,
        "image_height": image_height,
        "keypoints": v3_keypoints,
        "raw_model_payload": {
            **dict(frame_result.get("raw_model_payload") or {}),
            "tom_v1_raw_keypoints": raw_keypoints,
            "tom_v1_raw_keypoint_names": TOM_V1_RAW_COURT_KEYPOINT_NAMES,
            "raw_keypoints_scaled_to_image": raw_keypoints_scaled_to_image,
            "tom_v1_to_tom_v3_mapping": DIRECT_TOM_V1_TO_TOM_V3_KEYPOINT_INDEX,
            "mapped_tom_v3_keypoints": v3_keypoints,
            "inferred_tom_v3_keypoints": [
                "left_net_post",
                "right_net_post",
                "center_mark_near",
                "center_mark_far",
            ],
            "adapter_mapping_version": "tom_v1_14_point_to_tom_v3_12_point_mapping_v0",
            "mapping_version": "tom_v1_14_point_to_tom_v3_12_point_mapping_v0",
            "preprocessing_mode": preprocessing_mode,
            "coordinate_interpretation": coordinate_interpretation,
            "model_input_size": TOM_V1_COURT_KEYPOINT_MODEL_INPUT_SIZE,
            "output_reference_size": TOM_V1_COURT_KEYPOINT_OUTPUT_REFERENCE_SIZE,
            "calibration_audit_v0": True,
            "uncalibrated_tom_v1_keypoint_mapping": True,
            "inference_metadata": dict(inference_metadata),
        },
    }


def validate_court_keypoint_calibration_options(
    *,
    preprocessing_mode: str,
    coordinate_interpretation: str,
) -> None:
    if preprocessing_mode not in SUPPORTED_TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODES:
        raise CourtKeypointAdapterError(
            "unsupported_preprocessing_mode: only full_frame_resize_224 is implemented "
            "in this audit pass."
        )
    if (
        coordinate_interpretation
        not in SUPPORTED_TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATIONS
    ):
        raise CourtKeypointAdapterError(
            "unsupported_coordinate_interpretation: only output_as_pixels_224 is "
            "implemented in this audit pass."
        )


def scale_tom_v1_raw_keypoints_for_image(
    raw_keypoints: Sequence[Mapping[str, Any]],
    *,
    image_width: int,
    image_height: int,
    coordinate_interpretation: str = TOM_V1_COURT_KEYPOINT_COORDINATE_INTERPRETATION,
) -> list[dict[str, Any]]:
    validate_court_keypoint_calibration_options(
        preprocessing_mode=TOM_V1_COURT_KEYPOINT_PREPROCESSING_MODE,
        coordinate_interpretation=coordinate_interpretation,
    )
    scaled = []
    for index, raw_keypoint in enumerate(raw_keypoints):
        point = _scale_raw_keypoint(
            raw_keypoint,
            image_width=image_width,
            image_height=image_height,
        )
        scaled.append(
            {
                "source_index": int(raw_keypoint.get("source_index", index)),
                "raw_name": str(
                    raw_keypoint.get("name")
                    or TOM_V1_RAW_COURT_KEYPOINT_NAMES[index]
                    if index < len(TOM_V1_RAW_COURT_KEYPOINT_NAMES)
                    else f"raw_{index}"
                ),
                "raw_x": _optional_float(raw_keypoint.get("x")),
                "raw_y": _optional_float(raw_keypoint.get("y")),
                "image_x": point["x"],
                "image_y": point["y"],
                "confidence": point["confidence"],
                "present": point["present"],
                "visibility": point["visibility"],
                "coordinate_interpretation": coordinate_interpretation,
            }
        )
    return scaled


def map_tom_v1_raw_keypoints_to_tom_v3(
    raw_keypoints: Sequence[Mapping[str, Any]],
    *,
    image_width: int,
    image_height: int,
) -> list[dict[str, Any]]:
    scaled = [
        _scale_raw_keypoint(raw_keypoint, image_width=image_width, image_height=image_height)
        for raw_keypoint in raw_keypoints
    ]
    direct: dict[str, dict[str, Any]] = {}
    for name, source_index in DIRECT_TOM_V1_TO_TOM_V3_KEYPOINT_INDEX.items():
        point = scaled[source_index]
        direct[name] = {
            "name": name,
            "x": point["x"],
            "y": point["y"],
            "confidence": point["confidence"],
            "present": point["present"],
            "visibility": point["visibility"],
            "source_index": source_index,
        }
    direct["left_net_post"] = _interpolated_keypoint(
        "left_net_post",
        scaled[0],
        scaled[2],
        source_indices=[0, 2],
    )
    direct["right_net_post"] = _interpolated_keypoint(
        "right_net_post",
        scaled[1],
        scaled[3],
        source_indices=[1, 3],
    )
    direct["center_mark_near"] = _interpolated_keypoint(
        "center_mark_near",
        scaled[2],
        scaled[3],
        source_indices=[2, 3],
    )
    direct["center_mark_far"] = _interpolated_keypoint(
        "center_mark_far",
        scaled[0],
        scaled[1],
        source_indices=[0, 1],
    )
    return [direct[name] for name in COURT_KEYPOINT_NAMES]


def is_recognized_tom_v1_resnet50_state_dict(value: Any) -> bool:
    if not isinstance(value, dict | OrderedDict):
        return False
    fc_weight = value.get("fc.weight")
    if fc_weight is None or tuple(getattr(fc_weight, "shape", ())) != (28, 2048):
        return False
    expected_blocks = {
        "layer1": ["0", "1", "2"],
        "layer2": ["0", "1", "2", "3"],
        "layer3": ["0", "1", "2", "3", "4", "5"],
        "layer4": ["0", "1", "2"],
    }
    for prefix, expected in expected_blocks.items():
        blocks = sorted(
            {
                key.split(".")[1]
                for key in value
                if key.startswith(f"{prefix}.") and key.split(".")[1].isdigit()
            }
        )
        if blocks != expected:
            return False
    return True


def _raw_pairs_from_output(values: Sequence[Any], *, confidence: float) -> list[dict[str, Any]]:
    pairs = []
    for index, name in enumerate(TOM_V1_RAW_COURT_KEYPOINT_NAMES):
        x_index = index * 2
        pairs.append(
            {
                "name": name,
                "x": _optional_float(values[x_index] if x_index < len(values) else None),
                "y": _optional_float(
                    values[x_index + 1] if x_index + 1 < len(values) else None
                ),
                "confidence": confidence,
                "source_index": index,
            }
        )
    return pairs


def _scale_raw_keypoint(
    raw_keypoint: Mapping[str, Any],
    *,
    image_width: int,
    image_height: int,
) -> dict[str, Any]:
    raw_x = _optional_float(raw_keypoint.get("x"))
    raw_y = _optional_float(raw_keypoint.get("y"))
    confidence = _optional_float(raw_keypoint.get("confidence"))
    present = raw_x is not None and raw_y is not None and image_width > 0 and image_height > 0
    if not present:
        return {
            "x": None,
            "y": None,
            "confidence": confidence,
            "present": False,
            "visibility": "unknown",
        }
    x = raw_x / TOM_V1_COURT_KEYPOINT_OUTPUT_REFERENCE_SIZE * image_width
    y = raw_y / TOM_V1_COURT_KEYPOINT_OUTPUT_REFERENCE_SIZE * image_height
    in_bounds = -0.1 * image_width <= x <= 1.1 * image_width and (
        -0.1 * image_height <= y <= 1.1 * image_height
    )
    return {
        "x": round(x, 3) if in_bounds else None,
        "y": round(y, 3) if in_bounds else None,
        "confidence": confidence,
        "present": in_bounds,
        "visibility": "visible" if in_bounds else "unknown",
    }


def _interpolated_keypoint(
    name: str,
    a: Mapping[str, Any],
    b: Mapping[str, Any],
    *,
    source_indices: list[int],
) -> dict[str, Any]:
    if not a.get("present") or not b.get("present"):
        return {
            "name": name,
            "x": None,
            "y": None,
            "confidence": None,
            "present": False,
            "visibility": "unknown",
            "source_index": None,
            "source_indices": source_indices,
        }
    confidences = [
        float(value)
        for value in (a.get("confidence"), b.get("confidence"))
        if value is not None
    ]
    confidence = round(min(confidences) * 0.75, 6) if confidences else None
    return {
        "name": name,
        "x": round((float(a["x"]) + float(b["x"])) / 2.0, 3),
        "y": round((float(a["y"]) + float(b["y"])) / 2.0, 3),
        "confidence": confidence,
        "present": True,
        "visibility": "inferred_by_adapter",
        "source_index": None,
        "source_indices": source_indices,
    }


def _default_tom_v1_raw_keypoints() -> list[dict[str, Any]]:
    values = [
        (58.0, 62.0),
        (166.0, 62.0),
        (38.0, 178.0),
        (186.0, 178.0),
        (78.0, 62.0),
        (58.0, 178.0),
        (146.0, 62.0),
        (166.0, 178.0),
        (76.0, 86.0),
        (148.0, 86.0),
        (64.0, 138.0),
        (160.0, 138.0),
        (112.0, 86.0),
        (112.0, 138.0),
    ]
    return [
        {
            "name": TOM_V1_RAW_COURT_KEYPOINT_NAMES[index],
            "x": x,
            "y": y,
            "confidence": 0.7,
            "source_index": index,
        }
        for index, (x, y) in enumerate(values)
    ]


def _is_within_allowed_roots(path: Path, allowed_roots: Sequence[str | Path]) -> bool:
    resolved_roots = [Path(root).expanduser().resolve(strict=False) for root in allowed_roots]
    return any(path == root or root in path.parents for root in resolved_roots)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _result_or_raise(
    result: CourtKeypointWeightsValidationResult,
    raise_on_error: bool,
) -> CourtKeypointWeightsValidationResult:
    if raise_on_error:
        raise CourtKeypointAdapterError(result.message)
    return result


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


def _optional_int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
