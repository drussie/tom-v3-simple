from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Literal

from tom_v3_video.time_index import frame_to_timestamp_ms

DetectionLabel = Literal["ball", "player", "player_unknown", "near_player", "far_player"]


class DetectionAdapterError(RuntimeError):
    pass


class YoloDetectionAdapterUnavailable(DetectionAdapterError):
    pass


@dataclass(frozen=True)
class BBox:
    x: float
    y: float
    width: float
    height: float

    def as_dict(self) -> dict[str, float]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def as_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y}


@dataclass(frozen=True)
class DetectionAdapterInput:
    media_id: str
    source_uri: str
    local_path: str | None
    fps: float | None
    frame_count: int | None
    duration_ms: int | None
    width: int | None
    height: int | None
    runtime_config: dict[str, Any] = field(default_factory=dict)
    frame_time_summary: dict[str, Any] = field(default_factory=dict)
    gameplay_segments: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DetectionObservation:
    label: DetectionLabel
    frame_number: int
    timestamp_ms: int
    confidence: float
    bbox: BBox
    center: Point
    class_id: int | None = None
    class_label: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DetectionAdapterResult:
    adapter_name: str
    adapter_version: str
    detections: list[DetectionObservation]
    artifact_metadata: list[dict[str, Any]] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)


class BaseDetectionAdapter(ABC):
    name: str
    version: str

    @abstractmethod
    def run(self, adapter_input: DetectionAdapterInput) -> DetectionAdapterResult:
        raise NotImplementedError


class FixtureDetectionAdapter(BaseDetectionAdapter):
    name = "fixture-ball-player-detector"
    version = "fixture-v0"

    def run(self, adapter_input: DetectionAdapterInput) -> DetectionAdapterResult:
        if adapter_input.fps is None or adapter_input.fps <= 0:
            raise DetectionAdapterError("fixture detection adapter requires positive media fps")
        if adapter_input.frame_count is None or adapter_input.frame_count < 1:
            raise DetectionAdapterError("fixture detection adapter requires indexed frames")

        width = float(adapter_input.width or 1920)
        height = float(adapter_input.height or 1080)
        frame_sample_rate = int(adapter_input.runtime_config.get("frame_sample_rate") or 30)
        max_frames = adapter_input.runtime_config.get("max_frames")
        if frame_sample_rate <= 0:
            raise DetectionAdapterError("frame_sample_rate must be greater than 0")
        sampled_frames = list(range(0, adapter_input.frame_count, frame_sample_rate))
        if not sampled_frames:
            sampled_frames = [0]
        if max_frames is not None:
            sampled_frames = sampled_frames[: max(1, int(max_frames))]

        detections: list[DetectionObservation] = []
        for sample_index, frame_number in enumerate(sampled_frames):
            timestamp_ms = frame_to_timestamp_ms(adapter_input.fps, frame_number)
            detections.extend(
                _fixture_frame_detections(
                    sample_index=sample_index,
                    frame_number=frame_number,
                    timestamp_ms=timestamp_ms,
                    width=width,
                    height=height,
                    frame_time_owner=adapter_input.frame_time_summary.get(
                        "owner", "media_indexing"
                    ),
                )
            )

        return DetectionAdapterResult(
            adapter_name=self.name,
            adapter_version=self.version,
            detections=detections,
            diagnostics={
                "adapter_type": "fixture",
                "frame_sample_rate": frame_sample_rate,
                "max_frames": max_frames,
                "sampled_frame_count": len(sampled_frames),
                "note": "fixture adapter for tests and development only",
            },
        )


class YoloDetectionAdapter(BaseDetectionAdapter):
    name = "yolo-compatible-ball-player-detector"
    version = "unavailable-yolo26-stub"

    def __init__(
        self,
        model_path: str | None = None,
        device: str | None = None,
        image_size: int | None = None,
        confidence_threshold: float | None = None,
    ) -> None:
        self.model_path = model_path
        self.device = device
        self.image_size = image_size
        self.confidence_threshold = confidence_threshold

    def run(self, adapter_input: DetectionAdapterInput) -> DetectionAdapterResult:
        missing: list[str] = []
        if find_spec("ultralytics") is None:
            missing.append("ultralytics package")
        if not self.model_path:
            missing.append("model_path")
        elif not Path(self.model_path).expanduser().is_file():
            missing.append(f"model file not found: {Path(self.model_path).expanduser()}")
        missing_text = ", ".join(missing) if missing else "portable YOLO26 runtime"
        raise YoloDetectionAdapterUnavailable(
            "YOLO26/Ultralytics detection runtime is not available for TOM v3 in this "
            f"repo/environment: {missing_text}. Use --adapter fixture for development "
            "until model assets and runtime are supplied behind this interface."
        )


def get_detection_adapter(
    adapter_name: str,
    model_path: str | None = None,
    device: str | None = None,
    image_size: int | None = None,
    confidence_threshold: float | None = None,
) -> BaseDetectionAdapter:
    normalized = adapter_name.strip().lower()
    if normalized == "fixture":
        return FixtureDetectionAdapter()
    if normalized in {"yolo", "yolo26", "ultralytics"}:
        return YoloDetectionAdapter(
            model_path=model_path,
            device=device,
            image_size=image_size,
            confidence_threshold=confidence_threshold,
        )
    raise DetectionAdapterError(f"unknown detection adapter: {adapter_name}")


def _fixture_frame_detections(
    sample_index: int,
    frame_number: int,
    timestamp_ms: int,
    width: float,
    height: float,
    frame_time_owner: str,
) -> list[DetectionObservation]:
    ball_x = min(width - 8, width * 0.45 + sample_index * width * 0.03)
    ball_y = min(height - 8, height * 0.35 + sample_index * height * 0.025)
    ball = _detection(
        label="ball",
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        confidence=max(0.55, 0.88 - sample_index * 0.03),
        bbox=BBox(
            x=ball_x,
            y=ball_y,
            width=max(6.0, width * 0.012),
            height=max(6.0, width * 0.012),
        ),
        class_id=0,
        class_label="ball",
        frame_time_owner=frame_time_owner,
        sample_index=sample_index,
    )
    near_player = _detection(
        label="near_player",
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        confidence=max(0.65, 0.93 - sample_index * 0.02),
        bbox=BBox(
            x=width * 0.58,
            y=height * 0.48,
            width=width * 0.12,
            height=height * 0.34,
        ),
        class_id=1,
        class_label="player",
        frame_time_owner=frame_time_owner,
        sample_index=sample_index,
    )
    far_player = _detection(
        label="far_player",
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        confidence=max(0.62, 0.9 - sample_index * 0.025),
        bbox=BBox(
            x=width * 0.32,
            y=height * 0.16,
            width=width * 0.08,
            height=height * 0.22,
        ),
        class_id=1,
        class_label="player",
        frame_time_owner=frame_time_owner,
        sample_index=sample_index,
    )
    return [ball, near_player, far_player]


def _detection(
    label: DetectionLabel,
    frame_number: int,
    timestamp_ms: int,
    confidence: float,
    bbox: BBox,
    class_id: int,
    class_label: str,
    frame_time_owner: str,
    sample_index: int,
) -> DetectionObservation:
    center = Point(x=bbox.x + bbox.width / 2, y=bbox.y + bbox.height / 2)
    return DetectionObservation(
        label=label,
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        confidence=round(confidence, 4),
        bbox=bbox,
        center=center,
        class_id=class_id,
        class_label=class_label,
        metadata={
            "adapter_type": "fixture",
            "frame_time_owner": frame_time_owner,
            "sample_index": sample_index,
            "source": "deterministic fixture detector",
        },
    )
