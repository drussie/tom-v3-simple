from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_observations.writer import get_observation_detail
from tom_v3_storage.db_models import (
    Base,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    PoseObservation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.routers.viewer import build_viewer_run_payload
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.pose_adapter import PoseAdapterRunError, run_pose_adapter
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )
    with session_factory() as session:
        yield session


@pytest.fixture()
def sample_video(tmp_path: Path) -> str:
    video = tmp_path / "pose-lineage-source.mp4"
    video.write_bytes(b"tom-v3-pose-lineage-source")
    return str(video)


def probe_result() -> VideoProbeResult:
    return VideoProbeResult(
        duration_ms=3_000,
        frame_count=90,
        fps=30.0,
        width=640,
        height=360,
        codec="h264",
        format="mp4",
        raw_probe={"streams": [{"codec_type": "video"}]},
        frame_count_source="test_fixture",
    )


def indexed_media(session: Session, sample_video: str, tmp_path: Path) -> MediaAsset:
    return index_media_file(
        session=session,
        source_path=sample_video,
        copy_to_storage=True,
        media_name="pose lineage test clip",
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )


def raw_coco17_keypoints() -> list[dict[str, object]]:
    keypoints: list[dict[str, object]] = []
    for index in range(17):
        keypoints.append(
            {
                "x": 100.0 + index * 4.0,
                "y": 80.0 + index * 5.0,
                "confidence": 0.8,
            }
        )
    return keypoints


def test_pose_processing_service_persists_unassociated_fixture_poses(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)

    result = run_pose_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        frame_sample_rate=30,
        max_frames=2,
    )

    assert result["media_id"] == media.id
    assert result["pose_observation_count"] == 2
    assert result["lineage_count"] == 0
    assert result["adapter_name"] == "fixture-pose-adapter"

    run = db_session.get(ProcessingRun, result["pose_run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])
    model = db_session.get(ModelRegistry, result["model_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    assert run is not None
    assert run.run_status == "completed"
    assert run.metadata_jsonb["pose_observation_count"] == 2
    assert step is not None
    assert step.step_status == "completed"
    assert step.metadata_jsonb["lineage_count"] == 0
    assert model is not None
    assert model.model_family == "pose"
    assert model.metadata_jsonb["model_task"] == "pose"
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["adapter"] == "fixture_pose"
    assert runtime_config.payload_jsonb["frame_sample_rate"] == 30

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["pose_run_id"])
        .order_by(Observation.frame_start)
    ).all()
    assert len(observations) == 2
    assert [observation.frame_start for observation in observations] == [0, 30]
    assert all(observation.observation_family == "pose" for observation in observations)
    assert all(
        observation.observation_type == "player_pose_observation"
        for observation in observations
    )
    assert all(observation.coordinate_space == "image_pixels" for observation in observations)
    assert observations[1].timestamp_start_ms == frame_to_timestamp_ms(media.fps, 30)

    pose = db_session.get(PoseObservation, observations[0].id)
    assert pose is not None
    assert pose.keypoint_count == 17
    assert pose.keypoints_present_count == 15
    assert pose.keypoints_missing_count == 2
    assert pose.subject_ref_type == "none"
    assert pose.association_status == "unassociated"
    assert pose.association_method == "full_frame_pose"
    assert pose.frame_time_owner == "media_indexing"
    assert get_observation_detail(db_session, observations[0].id).pose is not None


def test_pose_processing_service_links_to_source_player_detection(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    detection_result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        frame_sample_rate=30,
        max_frames=1,
    )
    source_detection = db_session.scalar(
        select(Observation)
        .where(
            Observation.run_id == detection_result["run_id"],
            Observation.observation_type == "player_detection",
        )
        .order_by(Observation.id)
    )
    assert source_detection is not None

    result = run_pose_adapter(
        session=db_session,
        media_id=media.id,
        source_detection_run_id=detection_result["run_id"],
        link_source_detections=True,
        max_frames=1,
    )

    assert result["pose_observation_count"] == 1
    assert result["lineage_count"] == 1
    pose_observation = db_session.get(Observation, result["observation_ids"][0])
    assert pose_observation is not None
    pose = db_session.get(PoseObservation, pose_observation.id)
    assert pose is not None
    assert pose.subject_ref_type == "player_detection"
    assert pose.subject_detection_observation_id == source_detection.id
    assert pose.association_status == "candidate"
    assert pose.association_method == "crop_from_player_detection"
    assert pose.frame_number == source_detection.frame_start
    assert pose.timestamp_ms == source_detection.timestamp_start_ms
    assert pose_observation.frame_start == source_detection.frame_start
    assert pose_observation.timestamp_start_ms == source_detection.timestamp_start_ms

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == pose_observation.id
        )
    ).all()
    assert len(lineage) == 1
    assert lineage[0].parent_observation_id == source_detection.id
    assert lineage[0].relationship_type == "pose_from_subject_detection_candidate"
    assert lineage[0].payload_jsonb["association_status"] == "candidate"


def test_invalid_explicit_source_detection_id_fails_without_pose_rows(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    frame_result = {
        "frame_number": 0,
        "timestamp_ms": 0,
        "image_width": media.width,
        "image_height": media.height,
        "poses": [
            {
                "bbox_xyxy": [100.0, 50.0, 180.0, 240.0],
                "pose_confidence": 0.82,
                "keypoints": raw_coco17_keypoints(),
                "subject_context": {
                    "subject_ref_type": "player_detection",
                    "subject_detection_observation_id": "missing-source-observation",
                    "association_status": "candidate",
                    "association_method": "crop_from_player_detection",
                },
            }
        ],
    }

    with pytest.raises(PoseAdapterRunError, match="source detection observation not found"):
        run_pose_adapter(
            session=db_session,
            media_id=media.id,
            frame_results=[frame_result],
        )

    assert db_session.scalar(select(PoseObservation)) is None
    failed_run = db_session.scalar(
        select(ProcessingRun).where(ProcessingRun.run_status == "failed")
    )
    assert failed_run is not None
    assert "source detection observation not found" in failed_run.metadata_jsonb["error"]


def test_pose_processing_service_links_candidate_tracklet_and_track_point_context(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    detection_result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        frame_sample_rate=30,
        max_frames=2,
    )
    build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=detection_result["run_id"],
        max_gap_frames=30,
    )
    tracklet = db_session.scalar(select(Tracklet).order_by(Tracklet.id))
    assert tracklet is not None
    track_point = db_session.scalar(
        select(TrackPoint).where(TrackPoint.tracklet_id == tracklet.id).order_by(TrackPoint.id)
    )
    assert track_point is not None

    frame_result = {
        "frame_number": track_point.frame_number,
        "timestamp_ms": track_point.timestamp_ms,
        "image_width": media.width,
        "image_height": media.height,
        "poses": [
            {
                "bbox_xyxy": [100.0, 50.0, 180.0, 240.0],
                "pose_confidence": 0.82,
                "keypoints": raw_coco17_keypoints(),
                "subject_context": {
                    "subject_ref_type": "track_point",
                    "subject_tracklet_id": tracklet.id,
                    "subject_track_point_id": track_point.id,
                    "association_status": "candidate",
                    "association_method": "inherited_from_track_point_source_detection",
                },
            }
        ],
    }

    result = run_pose_adapter(
        session=db_session,
        media_id=media.id,
        frame_results=[frame_result],
    )

    assert result["pose_observation_count"] == 1
    assert result["lineage_count"] == 2
    pose = db_session.get(PoseObservation, result["observation_ids"][0])
    assert pose is not None
    assert pose.subject_tracklet_id == tracklet.id
    assert pose.subject_track_point_id == track_point.id

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == result["observation_ids"][0]
        )
    ).all()
    assert {row.relationship_type for row in lineage} == {
        "subject_context_candidate",
        "pose_from_track_point_candidate",
    }


def test_viewer_payload_includes_pose_detail_for_overlay(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = run_pose_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        frame_sample_rate=30,
        max_frames=1,
    )

    payload = build_viewer_run_payload(db_session, result["pose_run_id"])

    assert payload is not None
    pose_observations = [
        observation
        for observation in payload["observations"]
        if observation["observation_type"] == "player_pose_observation"
    ]
    assert len(pose_observations) == 1
    pose_observation = pose_observations[0]
    assert pose_observation["observation_family"] == "pose"
    assert pose_observation["pose"] is not None
    assert pose_observation["pose"]["skeleton_format"] == "coco17"
    assert pose_observation["pose"]["skeleton_version"] == "v1"
    assert len(pose_observation["pose"]["keypoints_jsonb"]) == 17
    assert pose_observation["pose"]["keypoints_present_count"] == 15
    assert pose_observation["pose"]["keypoints_missing_count"] == 2
    assert pose_observation["pose"]["frame_time_owner"] == "media_indexing"
    assert pose_observation["pose"]["subject_ref_type"] == "none"


def test_run_pose_adapter_cli_persists_fixture_pose(tmp_path: Path) -> None:
    db_path = tmp_path / "pose-cli.db"
    database_url = f"sqlite+pysqlite:///{db_path}"
    engine = create_engine(database_url, future=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )
    with session_factory() as session:
        media = MediaAsset(
            source_uri="file:///tmp/pose-cli.mp4",
            media_type="video",
            duration_ms=2_000,
            frame_count=60,
            fps=30.0,
            width=640,
            height=360,
            metadata_jsonb={"frame_time_index": {"owner": "media_indexing"}},
        )
        session.add(media)
        session.commit()
        media_id = media.id

    env = {**os.environ, "TOM_V3_DATABASE_URL": database_url}
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "apps.worker.cli",
            "run-pose-adapter",
            "--media-id",
            media_id,
            "--adapter",
            "fixture",
            "--frame-sample-rate",
            "30",
            "--max-frames",
            "1",
            "--skip-create-db",
        ],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["pose_observation_count"] == 1
    assert payload["lineage_count"] == 0
    with session_factory() as session:
        pose_count = session.scalar(select(PoseObservation))
        assert pose_count is not None
