"""Model adapter interfaces for TOM v3 Simple."""

from tom_v3_model_adapters.detection import (
    BaseDetectionAdapter,
    BBox,
    DetectionAdapterError,
    DetectionAdapterInput,
    DetectionAdapterResult,
    DetectionObservation,
    FixtureDetectionAdapter,
    Point,
    YoloDetectionAdapter,
    YoloDetectionAdapterUnavailable,
    get_detection_adapter,
)
from tom_v3_model_adapters.gameplay import (
    BaseGameplayAdapter,
    FixtureGameplayAdapter,
    GameplayAdapterError,
    GameplayAdapterInput,
    GameplayAdapterResult,
    GameplaySegmentObservation,
    TomV1AdapterUnavailable,
    TomV1GameplayAdapter,
    get_gameplay_adapter,
)

__all__ = [
    "BBox",
    "BaseDetectionAdapter",
    "BaseGameplayAdapter",
    "DetectionAdapterError",
    "DetectionAdapterInput",
    "DetectionAdapterResult",
    "DetectionObservation",
    "FixtureDetectionAdapter",
    "FixtureGameplayAdapter",
    "GameplayAdapterError",
    "GameplayAdapterInput",
    "GameplayAdapterResult",
    "GameplaySegmentObservation",
    "Point",
    "TomV1AdapterUnavailable",
    "TomV1GameplayAdapter",
    "YoloDetectionAdapter",
    "YoloDetectionAdapterUnavailable",
    "get_detection_adapter",
    "get_gameplay_adapter",
]
