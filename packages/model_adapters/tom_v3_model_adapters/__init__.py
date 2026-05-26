"""Model adapter interfaces for TOM v3 Simple."""

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
    "BaseGameplayAdapter",
    "FixtureGameplayAdapter",
    "GameplayAdapterError",
    "GameplayAdapterInput",
    "GameplayAdapterResult",
    "GameplaySegmentObservation",
    "TomV1AdapterUnavailable",
    "TomV1GameplayAdapter",
    "get_gameplay_adapter",
]
