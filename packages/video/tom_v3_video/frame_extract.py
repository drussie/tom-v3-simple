from __future__ import annotations

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tom_v3_video.paths import local_path_from_uri_or_path
from tom_v3_video.time_index import frame_to_timestamp_ms


class FfmpegFrameExtractionError(RuntimeError):
    pass


class FfmpegNotFoundError(FfmpegFrameExtractionError):
    pass


@dataclass(frozen=True)
class ExtractedFrame:
    path: Path
    uri: str
    frame_number: int
    timestamp_ms: int
    image_format: str
    extraction_method: str
    extraction_version: str


Runner = Any


def extract_frame_image(
    source_path: str | Path,
    frame_number: int,
    fps: float,
    output_path: str | Path,
    image_format: str = "jpg",
    overwrite: bool = False,
    runner: Runner | None = None,
) -> ExtractedFrame:
    source = local_path_from_uri_or_path(source_path)
    if not source.is_file():
        raise FileNotFoundError(f"media file not found: {source}")
    if frame_number < 0:
        raise ValueError("frame_number must be greater than or equal to 0")

    timestamp_ms = frame_to_timestamp_ms(fps, frame_number)
    output = Path(output_path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        return _extracted_frame(output, frame_number, timestamp_ms, image_format)

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{timestamp_ms / 1000:.6f}",
        "-i",
        str(source),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output),
    ]
    _run_ffmpeg(command, runner=runner)
    if not output.is_file():
        raise FfmpegFrameExtractionError(f"ffmpeg did not create frame image: {output}")
    return _extracted_frame(output, frame_number, timestamp_ms, image_format)


def _extracted_frame(
    output: Path,
    frame_number: int,
    timestamp_ms: int,
    image_format: str,
) -> ExtractedFrame:
    return ExtractedFrame(
        path=output,
        uri=output.as_uri(),
        frame_number=frame_number,
        timestamp_ms=timestamp_ms,
        image_format=image_format,
        extraction_method="ffmpeg_seek_timestamp",
        extraction_version="frame_artifacts_v0",
    )


def _run_ffmpeg(command: Sequence[str], runner: Runner | None) -> subprocess.CompletedProcess[str]:
    run = runner or subprocess.run
    try:
        return run(command, capture_output=True, text=True, check=True)
    except FileNotFoundError as exc:
        raise FfmpegNotFoundError(
            "ffmpeg is required for frame artifact extraction. Install ffmpeg and retry."
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "no stderr"
        raise FfmpegFrameExtractionError(f"ffmpeg frame extraction failed: {stderr}") from exc
