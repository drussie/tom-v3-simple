from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from tom_v3_video.time_index import frame_to_timestamp_ms

GameplayLabel = Literal["gameplay", "non_gameplay", "uncertain"]


class GameplayAdapterError(RuntimeError):
    pass


class TomV1AdapterUnavailable(GameplayAdapterError):
    pass


@dataclass(frozen=True)
class GameplayAdapterInput:
    media_id: str
    source_uri: str
    local_path: str | None
    fps: float | None
    frame_count: int | None
    duration_ms: int | None
    runtime_config: dict[str, Any] = field(default_factory=dict)
    frame_time_summary: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GameplaySegmentObservation:
    label: GameplayLabel
    frame_start: int
    frame_end: int
    timestamp_start_ms: int
    timestamp_end_ms: int
    confidence: float
    subtype: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GameplayAdapterResult:
    adapter_name: str
    adapter_version: str
    segments: list[GameplaySegmentObservation]
    artifact_metadata: list[dict[str, Any]] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)


class BaseGameplayAdapter(ABC):
    name: str
    version: str

    @abstractmethod
    def run(self, adapter_input: GameplayAdapterInput) -> GameplayAdapterResult:
        raise NotImplementedError


class FixtureGameplayAdapter(BaseGameplayAdapter):
    name = "fixture-gameplay-adapter"
    version = "fixture-v0"

    def run(self, adapter_input: GameplayAdapterInput) -> GameplayAdapterResult:
        if adapter_input.fps is None or adapter_input.fps <= 0:
            raise GameplayAdapterError("fixture gameplay adapter requires positive media fps")
        if adapter_input.frame_count is None or adapter_input.frame_count < 4:
            raise GameplayAdapterError(
                "fixture gameplay adapter requires at least 4 indexed frames"
            )

        segments: list[GameplaySegmentObservation] = []
        for label, subtype, start, end, confidence in _fixture_segments(
            adapter_input.frame_count
        ):
            segments.append(
                GameplaySegmentObservation(
                    label=label,
                    subtype=subtype,
                    frame_start=start,
                    frame_end=end,
                    timestamp_start_ms=frame_to_timestamp_ms(adapter_input.fps, start),
                    timestamp_end_ms=frame_to_timestamp_ms(adapter_input.fps, end),
                    confidence=confidence,
                    metadata={
                        "adapter_type": "fixture",
                        "media_frame_time_owner": adapter_input.frame_time_summary.get(
                            "owner", "media_indexing"
                        ),
                        "source": "deterministic fixture adapter",
                    },
                )
            )

        return GameplayAdapterResult(
            adapter_name=self.name,
            adapter_version=self.version,
            segments=segments,
            diagnostics={
                "segment_policy": "percentage_of_indexed_frame_count",
                "frame_count": adapter_input.frame_count,
                "fps": adapter_input.fps,
                "note": "fixture adapter for tests and development only",
            },
        )


class TomV1GameplayAdapter(BaseGameplayAdapter):
    name = "tom-v1-gameplay-detector"
    version = "v1-portable-wrapper-stub"

    def __init__(self, tom_v1_path: str | None = None) -> None:
        self.tom_v1_path = tom_v1_path

    def run(self, adapter_input: GameplayAdapterInput) -> GameplayAdapterResult:
        path_note = ""
        if self.tom_v1_path:
            path_note = f" Provided path: {Path(self.tom_v1_path).expanduser()}"
        raise TomV1AdapterUnavailable(
            "TOM v1 gameplay detector source/assets are not available as a portable "
            "function, package, or CLI in this repo/environment. Use --adapter fixture "
            "for development until the TOM v1 detector is supplied behind this interface."
            f"{path_note}"
        )


def get_gameplay_adapter(
    adapter_name: str,
    tom_v1_path: str | None = None,
) -> BaseGameplayAdapter:
    normalized = adapter_name.strip().lower()
    if normalized == "fixture":
        return FixtureGameplayAdapter()
    if normalized in {"tom-v1", "tom_v1", "tomv1"}:
        return TomV1GameplayAdapter(tom_v1_path=tom_v1_path)
    raise GameplayAdapterError(f"unknown gameplay adapter: {adapter_name}")


def _fixture_segments(
    frame_count: int,
) -> list[tuple[GameplayLabel, str, int, int, float]]:
    last_frame = frame_count - 1
    end_1 = max(0, round(last_frame * 0.30))
    start_2 = min(last_frame, end_1 + 1)
    end_2 = max(start_2, round(last_frame * 0.40))
    start_3 = min(last_frame, end_2 + 1)
    end_3 = max(start_3, round(last_frame * 0.45))
    start_4 = min(last_frame, end_3 + 1)
    end_4 = max(start_4, round(last_frame * 0.90))

    return [
        ("gameplay", "active_point", 0, end_1, 0.82),
        ("non_gameplay", "between_points", start_2, end_2, 0.76),
        ("uncertain", "unknown", start_3, end_3, 0.51),
        ("gameplay", "active_point", start_4, end_4, 0.84),
    ]
