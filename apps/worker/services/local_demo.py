from __future__ import annotations

import os
import subprocess
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from tom_v3_schema.exports import (
    PoseReviewDatasetExportRequest,
    TrackletReviewDatasetExportRequest,
)
from tom_v3_schema.tracklets import TrackletQueryFilters
from tom_v3_storage.db_models import (
    EvidenceArtifact,
    HumanAnnotation,
    MediaAsset,
    Observation,
    Tracklet,
    TrackPoint,
)

from apps.api.services.pose_review_export import export_pose_review_dataset
from apps.api.services.tracklet_review_export import export_tracklet_review_dataset
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
from apps.worker.services.gameplay_adapter import run_gameplay_adapter
from apps.worker.services.media_indexer import index_media
from apps.worker.services.pose_adapter import run_pose_adapter
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run

VIEWER_BASE_URL = "http://127.0.0.1:3000"
DEMO_CREATED_BY = "tom-v3-demo"
DEMO_WARNINGS = {
    "fixture_outputs_are_demo_evidence_only": True,
    "observation_only": True,
    "no_adjudication": True,
    "no_tennis_event_interpretation": True,
    "no_real_pose_inference": True,
    "optional_yolo_smoke_separate": True,
}
DEMO_STAGES = [
    "resolve_media",
    "index_media",
    "run_fixture_gameplay",
    "run_fixture_detection",
    "extract_frame_artifacts",
    "build_candidate_tracklets",
    "run_fixture_pose",
    "seed_review_annotations",
    "export_pose_review_dataset",
    "export_tracklet_review_dataset",
    "summarize_demo",
]


class LocalDemoError(ValueError):
    pass


@dataclass(frozen=True)
class DemoMediaSource:
    path: Path
    source: str
    synthetic_demo_media: bool
    generated: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "source": self.source,
            "synthetic_demo_media": self.synthetic_demo_media,
            "generated": self.generated,
        }


SyntheticMediaGenerator = Callable[[Path], None]
Runner = Any


def build_local_demo_plan(
    *,
    source_path: str | None = None,
    frame_sample_rate: int = 30,
    max_frames: int = 3,
    artifact_root: str = ".data/artifacts",
    export_root: str = ".data/exports",
    viewer_base_url: str = VIEWER_BASE_URL,
) -> dict[str, Any]:
    media_hint = source_path or os.getenv("DEMO_MEDIA_PATH") or "synthetic fallback"
    return {
        "name": "tom-v3-simple-fixture-demo",
        "fixture_only": True,
        "requires_yolo": False,
        "requires_pose_weights": False,
        "stages": list(DEMO_STAGES),
        "media_strategy": [
            "DEMO_MEDIA_PATH if set and present",
            "demo_assets/tennis_fixture.mp4 if present",
            ".data/demo/media/synthetic_demo_media.mp4 generated locally",
        ],
        "media_hint": media_hint,
        "frame_sample_rate": frame_sample_rate,
        "max_frames": max_frames,
        "artifact_root": artifact_root,
        "export_root": export_root,
        "viewer_url_template": f"{viewer_base_url.rstrip('/')}/runs/<run_id>",
        "warnings": dict(DEMO_WARNINGS),
    }


def resolve_demo_media_source(
    *,
    source_path: str | None = None,
    env: dict[str, str] | None = None,
    fixture_path: str | Path = "demo_assets/tennis_fixture.mp4",
    generated_path: str | Path = ".data/demo/media/synthetic_demo_media.mp4",
    generator: SyntheticMediaGenerator | None = None,
) -> DemoMediaSource:
    environment = env if env is not None else os.environ
    explicit_source = source_path or environment.get("DEMO_MEDIA_PATH")
    if explicit_source:
        explicit_path = Path(explicit_source).expanduser().resolve()
        if not explicit_path.is_file():
            raise LocalDemoError(f"demo media file not found: {explicit_path}")
        return DemoMediaSource(
            path=explicit_path,
            source="source_path" if source_path else "DEMO_MEDIA_PATH",
            synthetic_demo_media=False,
        )

    fixture = Path(fixture_path).expanduser().resolve()
    if fixture.is_file():
        return DemoMediaSource(
            path=fixture,
            source="demo_fixture",
            synthetic_demo_media=False,
        )

    generated = Path(generated_path).expanduser().resolve()
    generated_before = generated.is_file()
    if not generated_before:
        generated.parent.mkdir(parents=True, exist_ok=True)
        (generator or generate_synthetic_demo_media)(generated)
    if not generated.is_file():
        raise LocalDemoError(f"synthetic demo media was not created: {generated}")
    return DemoMediaSource(
        path=generated,
        source="synthetic_generated",
        synthetic_demo_media=True,
        generated=not generated_before,
    )


def generate_synthetic_demo_media(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=640x360:rate=30",
        "-t",
        "3",
        "-pix_fmt",
        "yuv420p",
        str(path),
    ]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except FileNotFoundError as exc:
        raise LocalDemoError(
            "ffmpeg is required to generate default synthetic demo media. "
            "Install ffmpeg or set DEMO_MEDIA_PATH to an existing local video."
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "no stderr"
        raise LocalDemoError(f"synthetic demo media generation failed: {stderr}") from exc


def run_local_fixture_demo(
    *,
    session: Session,
    source_path: str | None = None,
    storage_root: str = ".data/media",
    artifact_root: str = ".data/artifacts",
    export_root: str = ".data/exports",
    frame_sample_rate: int = 30,
    max_frames: int = 3,
    viewer_base_url: str = VIEWER_BASE_URL,
    copy_to_storage: bool = True,
    probe_runner: Runner | None = None,
    frame_artifact_runner: Runner | None = None,
    media_generator: SyntheticMediaGenerator | None = None,
    plan_only: bool = False,
) -> dict[str, Any]:
    plan = build_local_demo_plan(
        source_path=source_path,
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        artifact_root=artifact_root,
        export_root=export_root,
        viewer_base_url=viewer_base_url,
    )
    if plan_only:
        return {
            "ok": True,
            "status": "planned",
            "message": "TOM v3 Simple fixture demo plan",
            "plan": plan,
            "warnings": dict(DEMO_WARNINGS),
        }

    media_source = resolve_demo_media_source(
        source_path=source_path,
        generator=media_generator,
    )
    media = index_media(
        session=session,
        source_path=media_source.path,
        copy_to_storage=copy_to_storage,
        media_name="tom-v3-simple-fixture-demo-media",
        storage_root=storage_root,
        probe_runner=probe_runner,
    )
    _mark_demo_media(media, media_source)
    session.commit()

    gameplay = run_gameplay_adapter(
        session=session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="demo-fixture-gameplay-run",
    )
    detection = run_detection_adapter(
        session=session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="demo-fixture-detection-run",
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        gameplay_run_id=gameplay["run_id"],
        output_debug_artifact=True,
    )
    frame_artifacts = extract_frame_artifacts_for_run(
        session=session,
        run_id=detection["run_id"],
        max_frames=max_frames,
        output_root=artifact_root,
        runner=frame_artifact_runner,
    )
    tracklets = build_tracklets_from_detection_run(
        session=session,
        detection_run_id=detection["run_id"],
        run_name="demo-candidate-tracklet-run",
    )
    pose = run_pose_adapter(
        session=session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="demo-fixture-pose-run",
        frame_sample_rate=frame_sample_rate,
        max_frames=max_frames,
        source_detection_run_id=detection["run_id"],
        link_source_detections=True,
    )
    annotations = seed_demo_review_annotations(
        session=session,
        media_id=media.id,
        detection_run_id=detection["run_id"],
        tracklet_run_id=tracklets["tracklet_run_id"],
        pose_run_id=pose["pose_run_id"],
    )
    pose_export = export_pose_review_dataset(
        session,
        PoseReviewDatasetExportRequest(
            run_id=pose["pose_run_id"],
            output_root=export_root,
            query_name="demo_pose_review_dataset",
            created_by=DEMO_CREATED_BY,
        ),
    )
    tracklet_export = export_tracklet_review_dataset(
        session,
        TrackletReviewDatasetExportRequest(
            query=TrackletQueryFilters(
                tracklet_run_id=tracklets["tracklet_run_id"],
                limit=500,
            ),
            output_root=export_root,
            query_name="demo_tracklet_review_dataset",
            created_by=DEMO_CREATED_BY,
        ),
    )

    summary = demo_summary(
        session=session,
        media=media,
        media_source=media_source,
        gameplay=gameplay,
        detection=detection,
        frame_artifacts=frame_artifacts,
        tracklets=tracklets,
        pose=pose,
        annotations=annotations,
        pose_export=pose_export.model_dump(),
        tracklet_export=tracklet_export.model_dump(),
        viewer_base_url=viewer_base_url,
    )
    return {
        "ok": True,
        "status": "completed",
        "message": "TOM v3 Simple demo complete",
        "plan": plan,
        "summary": summary,
        "warnings": dict(DEMO_WARNINGS),
    }


def seed_demo_review_annotations(
    *,
    session: Session,
    media_id: str,
    detection_run_id: str,
    tracklet_run_id: str,
    pose_run_id: str,
) -> list[dict[str, Any]]:
    annotations: list[HumanAnnotation] = []
    detection = _first_observation(
        session,
        run_id=detection_run_id,
        observation_types=["ball_detection", "player_detection"],
    )
    if detection is not None:
        annotations.append(
            _annotation_for_observation(
                media_id=media_id,
                observation=detection,
                annotation_type="uncertain",
                payload={
                    "annotation_label": "uncertain",
                    "demo_seeded": True,
                    "review_only": True,
                },
            )
        )

    tracklet = session.scalar(
        select(Tracklet)
        .where(Tracklet.run_id == tracklet_run_id, Tracklet.observation_id.is_not(None))
        .order_by(Tracklet.frame_start, Tracklet.id)
    )
    if tracklet is not None and tracklet.observation_id:
        tracklet_observation = session.get(Observation, tracklet.observation_id)
        if tracklet_observation is not None:
            annotations.append(
                _annotation_for_observation(
                    media_id=media_id,
                    observation=tracklet_observation,
                    annotation_type="likely_good_tracklet",
                    payload={
                        "annotation_label": "likely_good_tracklet",
                        "demo_seeded": True,
                        "review_only": True,
                    },
                )
            )

    pose = _first_observation(
        session,
        run_id=pose_run_id,
        observation_types=["player_pose_observation"],
    )
    if pose is not None:
        annotations.append(
            _annotation_for_observation(
                media_id=media_id,
                observation=pose,
                annotation_type="bad_keypoint",
                payload={
                    "annotation_label": "bad_keypoint",
                    "keypoint_name": "right_wrist",
                    "keypoint_index": 10,
                    "demo_seeded": True,
                    "review_only": True,
                },
            )
        )

    session.add_all(annotations)
    session.commit()
    return [_annotation_payload(annotation) for annotation in annotations]


def demo_summary(
    *,
    session: Session,
    media: MediaAsset,
    media_source: DemoMediaSource,
    gameplay: dict[str, Any],
    detection: dict[str, Any],
    frame_artifacts: dict[str, Any],
    tracklets: dict[str, Any],
    pose: dict[str, Any],
    annotations: list[dict[str, Any]],
    pose_export: dict[str, Any],
    tracklet_export: dict[str, Any],
    viewer_base_url: str,
) -> dict[str, Any]:
    observation_counts = _observation_counts(session, media.id)
    artifact_counts = _artifact_counts(session, media.id)
    annotation_count = _annotation_count(session, media.id)
    track_point_count = session.scalar(
        select(func.count())
        .select_from(TrackPoint)
        .join(Tracklet, Tracklet.id == TrackPoint.tracklet_id)
        .where(Tracklet.run_id == tracklets["tracklet_run_id"])
    )
    pose_count = session.scalar(
        select(func.count())
        .select_from(Observation)
        .where(
            Observation.run_id == pose["pose_run_id"],
            Observation.observation_type == "player_pose_observation",
        )
    )
    detection_run_id = detection["run_id"]
    tracklet_run_id = tracklets["tracklet_run_id"]
    pose_run_id = pose["pose_run_id"]
    return {
        "media": {
            "media_id": media.id,
            "source_uri": media.source_uri,
            "fps": media.fps,
            "frame_count": media.frame_count,
            "width": media.width,
            "height": media.height,
            **media_source.as_dict(),
        },
        "runs": {
            "gameplay_run_id": gameplay["run_id"],
            "detection_run_id": detection_run_id,
            "tracklet_run_id": tracklet_run_id,
            "pose_run_id": pose_run_id,
        },
        "observations": {
            "by_family": observation_counts["by_family"],
            "by_type": observation_counts["by_type"],
            "ball_detection": observation_counts["by_type"].get("ball_detection", 0),
            "player_detection": observation_counts["by_type"].get("player_detection", 0),
            "tracklet_candidates": tracklets["tracklet_count"],
            "track_points": int(track_point_count or 0),
            "pose_observations": int(pose_count or 0),
        },
        "artifacts": {
            "by_type": artifact_counts,
            "frame_artifact_ids": frame_artifacts["artifact_ids"],
            "frame_artifact_count": len(frame_artifacts["artifact_ids"]),
            "review_exports": [
                {
                    "kind": "pose_review_dataset_export",
                    "artifact_id": pose_export["artifact_id"],
                    "path": pose_export["path"],
                },
                {
                    "kind": "tracklet_review_dataset_export",
                    "artifact_id": tracklet_export["artifact_id"],
                    "path": tracklet_export["path"],
                },
            ],
        },
        "annotations": {
            "count": annotation_count,
            "seeded": annotations,
        },
        "exports": {
            "pose": pose_export,
            "tracklet": tracklet_export,
        },
        "viewer_urls": {
            "gameplay_run": _viewer_url(viewer_base_url, gameplay["run_id"]),
            "detection_run": _viewer_url(viewer_base_url, detection_run_id),
            "tracklet_run": _viewer_url(viewer_base_url, tracklet_run_id),
            "pose_run": _viewer_url(viewer_base_url, pose_run_id),
            "replay": (
                f"{viewer_base_url.rstrip('/')}/replay/{media.id}"
                f"?detectionRunId={detection_run_id}"
                f"&trackletRunId={tracklet_run_id}"
                f"&poseRunId={pose_run_id}"
            ),
        },
        "warnings": dict(DEMO_WARNINGS),
    }


def _mark_demo_media(media: MediaAsset, media_source: DemoMediaSource) -> None:
    media.metadata_jsonb = {
        **(media.metadata_jsonb or {}),
        "tom_v3_demo": True,
        "demo_source": media_source.source,
        "synthetic_demo_media": media_source.synthetic_demo_media,
    }


def _annotation_for_observation(
    *,
    media_id: str,
    observation: Observation,
    annotation_type: str,
    payload: dict[str, Any],
) -> HumanAnnotation:
    return HumanAnnotation(
        media_id=media_id,
        observation_id=observation.id,
        frame_start=observation.frame_start,
        frame_end=observation.frame_end,
        timestamp_start_ms=observation.timestamp_start_ms,
        timestamp_end_ms=observation.timestamp_end_ms,
        annotation_type=annotation_type,
        payload_jsonb=payload,
        created_by=DEMO_CREATED_BY,
    )


def _first_observation(
    session: Session,
    *,
    run_id: str,
    observation_types: Sequence[str],
) -> Observation | None:
    return session.scalar(
        select(Observation)
        .where(
            Observation.run_id == run_id,
            Observation.observation_type.in_(list(observation_types)),
        )
        .order_by(Observation.frame_start, Observation.observation_type, Observation.id)
    )


def _annotation_payload(annotation: HumanAnnotation) -> dict[str, Any]:
    return {
        "annotation_id": annotation.id,
        "observation_id": annotation.observation_id,
        "annotation_type": annotation.annotation_type,
        "payload_jsonb": annotation.payload_jsonb,
        "created_by": annotation.created_by,
    }


def _observation_counts(session: Session, media_id: str) -> dict[str, dict[str, int]]:
    by_family = Counter(
        dict(
            session.execute(
                select(Observation.observation_family, func.count())
                .where(Observation.media_id == media_id)
                .group_by(Observation.observation_family)
            ).all()
        )
    )
    by_type = Counter(
        dict(
            session.execute(
                select(Observation.observation_type, func.count())
                .where(Observation.media_id == media_id)
                .group_by(Observation.observation_type)
            ).all()
        )
    )
    return {
        "by_family": dict(by_family),
        "by_type": dict(by_type),
    }


def _artifact_counts(session: Session, media_id: str) -> dict[str, int]:
    return dict(
        session.execute(
            select(EvidenceArtifact.artifact_type, func.count())
            .where(EvidenceArtifact.media_id == media_id)
            .group_by(EvidenceArtifact.artifact_type)
        ).all()
    )


def _annotation_count(session: Session, media_id: str) -> int:
    return int(
        session.scalar(
            select(func.count())
            .select_from(HumanAnnotation)
            .where(HumanAnnotation.media_id == media_id)
        )
        or 0
    )


def _viewer_url(viewer_base_url: str, run_id: str) -> str:
    return f"{viewer_base_url.rstrip('/')}/runs/{run_id}"
