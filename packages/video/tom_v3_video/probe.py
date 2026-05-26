from __future__ import annotations

import json
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tom_v3_video.paths import local_path_from_uri_or_path


class FfprobeError(RuntimeError):
    pass


class FfprobeNotFoundError(FfprobeError):
    pass


@dataclass(frozen=True)
class VideoProbeResult:
    duration_ms: int | None
    frame_count: int | None
    fps: float | None
    width: int | None
    height: int | None
    codec: str | None = None
    format: str | None = None
    raw_probe: dict[str, Any] | None = None
    frame_count_source: str | None = None

    def to_metadata(self) -> dict[str, Any]:
        return {
            "duration_ms": self.duration_ms,
            "frame_count": self.frame_count,
            "fps": self.fps,
            "width": self.width,
            "height": self.height,
            "codec": self.codec,
            "format": self.format,
            "frame_count_source": self.frame_count_source,
            "raw_probe": self.raw_probe,
        }


Runner = Any


def probe_video(path_or_uri: str | Path, runner: Runner | None = None) -> VideoProbeResult:
    path = local_path_from_uri_or_path(path_or_uri)
    if not path.is_file():
        raise FileNotFoundError(f"media file not found: {path}")

    command = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    completed = _run_ffprobe(command, runner=runner)
    try:
        raw_probe = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise FfprobeError("ffprobe returned invalid JSON") from exc
    return parse_ffprobe_json(raw_probe)


def parse_ffprobe_json(raw_probe: dict[str, Any]) -> VideoProbeResult:
    streams = raw_probe.get("streams", [])
    video_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "video"),
        None,
    )
    if video_stream is None:
        raise FfprobeError("ffprobe did not return a video stream")

    format_info = raw_probe.get("format", {})
    fps = _parse_fps(video_stream.get("avg_frame_rate")) or _parse_fps(
        video_stream.get("r_frame_rate")
    )
    duration_seconds = _as_float(video_stream.get("duration")) or _as_float(
        format_info.get("duration")
    )
    duration_ms = round(duration_seconds * 1000) if duration_seconds is not None else None
    frame_count, frame_count_source = _frame_count(video_stream, fps, duration_seconds)

    return VideoProbeResult(
        duration_ms=duration_ms,
        frame_count=frame_count,
        fps=fps,
        width=_as_int(video_stream.get("width")),
        height=_as_int(video_stream.get("height")),
        codec=video_stream.get("codec_name"),
        format=format_info.get("format_name"),
        raw_probe=raw_probe,
        frame_count_source=frame_count_source,
    )


def _run_ffprobe(command: Sequence[str], runner: Runner | None) -> subprocess.CompletedProcess[str]:
    run = runner or subprocess.run
    try:
        return run(command, capture_output=True, text=True, check=True)
    except FileNotFoundError as exc:
        raise FfprobeNotFoundError(
            "ffprobe is required for real media indexing. Install ffmpeg/ffprobe and retry."
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "no stderr"
        raise FfprobeError(f"ffprobe failed: {stderr}") from exc


def _parse_fps(value: Any) -> float | None:
    if value in (None, "", "0/0"):
        return None
    if isinstance(value, int | float):
        return float(value) if value > 0 else None
    if isinstance(value, str) and "/" in value:
        numerator, denominator = value.split("/", 1)
        denominator_value = float(denominator)
        if denominator_value == 0:
            return None
        fps = float(numerator) / denominator_value
        return fps if fps > 0 else None
    fps = float(value)
    return fps if fps > 0 else None


def _frame_count(
    video_stream: dict[str, Any],
    fps: float | None,
    duration_seconds: float | None,
) -> tuple[int | None, str | None]:
    explicit_count = _as_int(video_stream.get("nb_frames"))
    if explicit_count is not None:
        return explicit_count, "ffprobe_nb_frames"
    if fps is not None and duration_seconds is not None:
        return round(fps * duration_seconds), "duration_fps_estimate"
    return None, None


def _as_int(value: Any) -> int | None:
    if value in (None, "", "N/A"):
        return None
    return int(float(value))


def _as_float(value: Any) -> float | None:
    if value in (None, "", "N/A"):
        return None
    return float(value)
