from typing import Any


def frame_to_timestamp_ms(fps: float, frame_number: int) -> int:
    _validate_fps(fps)
    if frame_number < 0:
        raise ValueError("frame_number must be greater than or equal to 0")
    return round(frame_number * 1000 / fps)


def timestamp_ms_to_frame(fps: float, timestamp_ms: int) -> int:
    _validate_fps(fps)
    if timestamp_ms < 0:
        raise ValueError("timestamp_ms must be greater than or equal to 0")
    return round(timestamp_ms * fps / 1000)


def build_frame_time_summary(
    fps: float | None,
    frame_count: int | None,
    duration_ms: int | None,
) -> dict[str, Any]:
    if fps is None or frame_count is None:
        return {
            "mapping": "unavailable",
            "fps": fps,
            "frame_count": frame_count,
            "duration_ms": duration_ms,
            "owner": "media_indexing",
        }

    _validate_fps(fps)
    if frame_count < 0:
        raise ValueError("frame_count must be greater than or equal to 0")

    final_frame = max(0, frame_count - 1)
    return {
        "mapping": "constant_fps",
        "owner": "media_indexing",
        "fps": fps,
        "frame_count": frame_count,
        "duration_ms": duration_ms,
        "first_frame": {
            "frame_number": 0,
            "timestamp_ms": 0,
        },
        "final_frame": {
            "frame_number": final_frame,
            "timestamp_ms": frame_to_timestamp_ms(fps, final_frame),
        },
        "rule": "downstream_observations_reference_media_frame_time",
    }


def _validate_fps(fps: float) -> None:
    if fps <= 0:
        raise ValueError("fps must be greater than 0")
