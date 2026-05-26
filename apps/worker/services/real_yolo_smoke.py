from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from tom_v3_model_adapters.yolo_runtime import probe_yolo_runtime
from tom_v3_model_adapters.yolo_weights import (
    YoloWeightsValidationError,
    validate_yolo_weights,
)

from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
from apps.worker.services.media_indexer import index_media
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run
from apps.worker.services.yolo_model_registry import register_yolo_model

OBSERVATION_ONLY_WARNING = {
    "observation_only": True,
    "candidate_evidence_only": True,
    "no_adjudication": True,
    "annotations_are_reviews_not_truth": True,
    "no_fixture_fallback": True,
}


def build_real_yolo_smoke_plan(
    source_path: str = "<sample_video_path>",
    weights_path: str = "model_assets/yolo/<weights_file>.pt",
    model_name: str = "local-yolo-smoke",
    model_version: str = "local-v0",
    device: str = "cpu",
    frame_sample_rate: int = 30,
    max_frames: int = 3,
    output_root: str = ".data/artifacts",
    run_tracklets: bool = True,
) -> dict[str, Any]:
    commands = [
        "python -m apps.worker.cli yolo-runtime-probe --device auto",
        f"python -m apps.worker.cli yolo-runtime-probe --device {device}",
        (
            "python -m apps.worker.cli register-yolo-model "
            f"--weights-path {weights_path} "
            f"--model-name {model_name} "
            f"--model-version {model_version} "
            f"--device {device}"
        ),
        f"python -m apps.worker.cli index-media --source-path {source_path}",
        (
            "python -m apps.worker.cli run-detection-adapter "
            "--media-id <media_id> "
            "--adapter yolo "
            "--model-registry-id <model_registry_id> "
            f"--device {device} "
            f"--frame-sample-rate {frame_sample_rate} "
            f"--max-frames {max_frames} "
            "--output-debug-artifact"
        ),
        (
            "python -m apps.worker.cli extract-frame-artifacts "
            "--run-id <detection_run_id> "
            f"--max-frames {max_frames} "
            f"--output-root {output_root}"
        ),
    ]
    if run_tracklets:
        commands.append(
            "python -m apps.worker.cli build-tracklets "
            "--detection-run-id <detection_run_id> "
            "--max-gap-frames 30"
        )
        commands.append("GET /tracklets/<tracklet_id>/evidence-bundle")

    return {
        "steps": [
            "probe_runtime",
            "register_model",
            "index_media",
            "run_yolo_detection",
            "extract_frame_artifacts",
            "build_tracklets" if run_tracklets else "skip_tracklets",
            "open_viewer",
        ],
        "commands": commands,
        "viewer_url": "http://127.0.0.1:3000/runs/<detection_run_id>",
        "warnings": dict(OBSERVATION_ONLY_WARNING),
        "notes": [
            "Real YOLO smoke is optional and local-only.",
            "The YOLO path does not fall back to fixture detections.",
            (
                "Tracklets, when requested, are built by the existing tracklet "
                "builder after detection."
            ),
        ],
    }


def run_real_yolo_local_smoke(
    session: Session,
    source_path: str | None,
    weights_path: str | None,
    model_name: str = "local-yolo-smoke",
    model_version: str = "local-v0",
    device: str = "cpu",
    frame_sample_rate: int = 30,
    max_frames: int = 3,
    output_root: str = ".data/artifacts",
    allowed_roots: Sequence[str] | None = None,
    copy_to_storage: bool = True,
    run_tracklets: bool = False,
    output_debug_artifact: bool = True,
    plan_only: bool = False,
    probe_runtime: Callable[..., dict[str, Any]] = probe_yolo_runtime,
) -> dict[str, Any]:
    plan = build_real_yolo_smoke_plan(
        source_path=source_path or "<sample_video_path>",
        weights_path=weights_path or "model_assets/yolo/<weights_file>.pt",
        model_name=model_name,
        model_version=model_version,
        device=device,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        output_root=output_root,
        run_tracklets=run_tracklets,
    )
    summary: dict[str, Any] = {
        "ok": True,
        "status": "planned" if plan_only else "running",
        "milestone": "3E",
        "plan": plan,
        "warnings": dict(OBSERVATION_ONLY_WARNING),
    }
    if plan_only:
        return summary

    runtime_probe = probe_runtime(requested_device=device)
    summary["runtime_probe"] = runtime_probe
    if runtime_probe.get("status") != "ok":
        return {
            **summary,
            "ok": True,
            "status": "skipped",
            "skip_reason": "yolo_runtime_unavailable",
            "message": "Optional YOLO runtime is unavailable; real YOLO smoke was skipped.",
        }

    if not weights_path:
        return _skip(summary, "missing_weights_path", "weights_path is required.")
    weights = Path(weights_path).expanduser()
    if not weights.is_file():
        return _skip(summary, "missing_weights", f"YOLO weights file not found: {weights}")
    try:
        weights_validation = validate_yolo_weights(
            weights,
            allowed_roots=allowed_roots,
            raise_on_error=True,
        )
    except YoloWeightsValidationError as exc:
        return {
            **summary,
            "ok": True,
            "status": "skipped",
            "skip_reason": exc.result.status,
            "message": str(exc),
            "weights_validation": exc.result.as_dict(),
        }
    summary["weights_validation"] = weights_validation.as_dict()

    if not source_path:
        return _skip(summary, "missing_source_path", "source_path is required.")
    source = Path(source_path).expanduser()
    if not source.is_file():
        return _skip(summary, "missing_source_media", f"source media file not found: {source}")

    try:
        model = register_yolo_model(
            session=session,
            weights_path=str(weights),
            model_name=model_name,
            model_version=model_version,
            allowed_roots=list(allowed_roots) if allowed_roots else None,
            device=device,
        )
        media = index_media(
            session=session,
            source_path=str(source),
            copy_to_storage=copy_to_storage,
        )
        detection = run_detection_adapter(
            session=session,
            media_id=media.id,
            adapter_name="yolo",
            model_registry_id=model["model_registry_id"],
            device=device,
            frame_sample_rate=frame_sample_rate,
            max_frames=max_frames,
            output_debug_artifact=output_debug_artifact,
        )
    except Exception as exc:
        return {
            **summary,
            "ok": False,
            "status": "failed",
            "message": str(exc),
            "error_type": exc.__class__.__name__,
        }

    artifacts: dict[str, Any] | None = None
    if detection["detection_count"] > 0:
        artifacts = extract_frame_artifacts_for_run(
            session=session,
            run_id=detection["run_id"],
            max_frames=max_frames,
            output_root=output_root,
        )

    tracklets: dict[str, Any] | None = None
    if run_tracklets and detection["detection_count"] > 0:
        tracklets = build_tracklets_from_detection_run(
            session=session,
            detection_run_id=detection["run_id"],
        )

    return {
        **summary,
        "ok": True,
        "status": "completed",
        "model": model,
        "media": {
            "media_id": media.id,
            "source_uri": media.source_uri,
            "fps": media.fps,
            "frame_count": media.frame_count,
            "width": media.width,
            "height": media.height,
        },
        "detection": detection,
        "frame_artifacts": artifacts,
        "tracklets": tracklets,
        "viewer_url": f"http://127.0.0.1:3000/runs/{detection['run_id']}",
    }


def _skip(summary: dict[str, Any], reason: str, message: str) -> dict[str, Any]:
    return {
        **summary,
        "ok": True,
        "status": "skipped",
        "skip_reason": reason,
        "message": message,
    }
