from __future__ import annotations

from typing import Any

from tom_v3_model_adapters.pose_inference import UltralyticsPoseResultProvider
from tom_v3_model_adapters.yolo_inference import (
    FrameInferenceInput,
    UltralyticsYoloResultProvider,
)


class PredictCapture:
    names: dict[int, str] = {}

    def __init__(self) -> None:
        self.kwargs: dict[str, Any] | None = None

    def predict(self, image: object, **kwargs: Any) -> list[Any]:
        self.kwargs = kwargs
        return []


class CapturingYoloProvider(UltralyticsYoloResultProvider):
    def __init__(self, model: PredictCapture, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.model = model

    def _load_model(self) -> PredictCapture:
        self._resolved_device = "cpu"
        return self.model


class CapturingPoseProvider(UltralyticsPoseResultProvider):
    def __init__(self, model: PredictCapture, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.model = model

    def _load_model(self) -> PredictCapture:
        self._resolved_device = "cpu"
        return self.model


def frame_input() -> FrameInferenceInput:
    return FrameInferenceInput(
        frame_number=0,
        timestamp_ms=0,
        image=object(),
        image_width=640,
        image_height=360,
        source_path="/tmp/sample.mp4",
        metadata={"frame_time_owner": "media_indexing"},
    )


def test_yolo_predict_omits_none_optional_kwargs() -> None:
    model = PredictCapture()
    provider = CapturingYoloProvider(
        model=model,
        weights_path="/tmp/model.pt",
        device="cpu",
        image_size=None,
        confidence_threshold=0.25,
        iou_threshold=None,
        max_det=None,
    )

    provider.predict_frame(frame_input())

    assert model.kwargs is not None
    assert model.kwargs["device"] == "cpu"
    assert model.kwargs["conf"] == 0.25
    assert model.kwargs["verbose"] is False
    assert "imgsz" not in model.kwargs
    assert "iou" not in model.kwargs
    assert "max_det" not in model.kwargs


def test_pose_predict_omits_none_optional_kwargs() -> None:
    model = PredictCapture()
    provider = CapturingPoseProvider(
        model=model,
        weights_path="/tmp/model.pt",
        device="cpu",
        image_size=None,
        confidence_threshold=0.25,
        iou_threshold=None,
        max_det=None,
    )

    provider.predict_frame(frame_input())

    assert model.kwargs is not None
    assert model.kwargs["device"] == "cpu"
    assert model.kwargs["conf"] == 0.25
    assert model.kwargs["verbose"] is False
    assert "imgsz" not in model.kwargs
    assert "iou" not in model.kwargs
    assert "max_det" not in model.kwargs


def test_yolo_predict_includes_real_optional_kwargs() -> None:
    model = PredictCapture()
    provider = CapturingYoloProvider(
        model=model,
        weights_path="/tmp/model.pt",
        device="cpu",
        image_size=1280,
        confidence_threshold=0.1,
        iou_threshold=0.7,
        max_det=50,
    )

    provider.predict_frame(frame_input())

    assert model.kwargs is not None
    assert model.kwargs["imgsz"] == 1280
    assert model.kwargs["conf"] == 0.1
    assert model.kwargs["iou"] == 0.7
    assert model.kwargs["max_det"] == 50
