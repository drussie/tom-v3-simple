from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_observations.pose import create_synthetic_pose_observation
from tom_v3_observations.writer import get_observation_detail
from tom_v3_schema.observations import ObservationQueryFilters
from tom_v3_storage.db_models import (
    Base,
    ModelRegistry,
    Observation,
    PoseObservation,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.services.query_builder import query_observations


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
    video = tmp_path / "pose-source.mp4"
    video.write_bytes(b"tom-v3-pose-source")
    return str(video)


def probe_result() -> VideoProbeResult:
    return VideoProbeResult(
        duration_ms=3_000,
        frame_count=90,
        fps=30.0,
        width=1280,
        height=720,
        codec="h264",
        format="mp4",
        raw_probe={"streams": [{"codec_type": "video"}]},
        frame_count_source="test_fixture",
    )


def indexed_media(session: Session, sample_video: str, tmp_path: Path):
    return index_media_file(
        session=session,
        source_path=sample_video,
        copy_to_storage=True,
        media_name="pose persistence test clip",
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )


def test_pose_observation_table_exists(db_session: Session) -> None:
    inspector = inspect(db_session.bind)

    assert inspector.has_table("pose_observation")


def test_synthetic_pose_observation_persists_typed_row_and_spine(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)

    result = create_synthetic_pose_observation(
        session=db_session,
        media_id=media.id,
        frame_number=30,
    )

    observation = db_session.get(Observation, result["observation_id"])
    pose = db_session.get(PoseObservation, result["pose_observation_id"])
    assert observation is not None
    assert pose is not None
    assert observation.observation_family == "pose"
    assert observation.observation_type == "player_pose_observation"
    assert observation.granularity == "frame"
    assert observation.coordinate_space == "image_pixels"
    assert pose.observation_id == observation.id
    assert pose.frame_number == observation.frame_start == observation.frame_end == 30
    assert pose.timestamp_ms == observation.timestamp_start_ms
    assert pose.timestamp_ms == observation.timestamp_end_ms
    assert pose.timestamp_ms == frame_to_timestamp_ms(media.fps, 30)
    assert pose.frame_time_owner == "media_indexing"


def test_pose_keypoint_summary_and_unassociated_subject_are_persisted(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = create_synthetic_pose_observation(session=db_session, media_id=media.id)

    pose = db_session.get(PoseObservation, result["pose_observation_id"])

    assert pose is not None
    assert pose.skeleton_format == "coco17"
    assert pose.skeleton_version == "v1"
    assert pose.keypoint_count == 17
    assert pose.keypoints_present_count == 15
    assert pose.keypoints_missing_count == 2
    assert pose.mean_keypoint_confidence is not None
    assert pose.min_keypoint_confidence is not None
    assert pose.max_keypoint_confidence is not None
    assert pose.subject_ref_type == "none"
    assert pose.association_status == "unassociated"
    assert pose.association_method == "full_frame_pose"
    assert pose.subject_detection_observation_id is None
    assert pose.subject_tracklet_id is None
    assert pose.subject_track_point_id is None


def test_pose_model_registry_and_runtime_config_store_pose_contract(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = create_synthetic_pose_observation(session=db_session, media_id=media.id)

    model = db_session.get(ModelRegistry, result["model_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])

    assert model is not None
    assert model.model_family == "pose"
    assert model.metadata_jsonb["model_task"] == "pose"
    assert model.metadata_jsonb["skeleton_format"] == "coco17"
    assert model.metadata_jsonb["keypoint_schema_json"]["skeleton_format"] == "coco17"
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["adapter"] == "fixture_pose"
    assert runtime_config.payload_jsonb["subject_source_mode"] == "full_frame"
    assert runtime_config.payload_jsonb["frame_time_owner"] == "media_indexing"


def test_pose_observation_is_queryable_through_existing_observation_query(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = create_synthetic_pose_observation(
        session=db_session,
        media_id=media.id,
        frame_number=15,
    )

    response = query_observations(
        db_session,
        ObservationQueryFilters(
            media_id=media.id,
            run_id=result["run_id"],
            observation_family="pose",
            observation_type="player_pose_observation",
            frame_start_gte=15,
            frame_end_lte=15,
        ),
    )

    assert response.count == 1
    detail = response.observations[0]
    assert detail.id == result["observation_id"]
    assert detail.pose is not None
    assert detail.pose.frame_number == 15
    assert detail.pose.keypoints_missing_count == 2


def test_get_observation_detail_includes_pose_detail(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = create_synthetic_pose_observation(session=db_session, media_id=media.id)

    detail = get_observation_detail(db_session, result["observation_id"])

    assert detail is not None
    assert detail.pose is not None
    assert detail.pose.observation_id == result["observation_id"]
    assert detail.pose.keypoints_jsonb[0]["name"] == "nose"
    assert detail.pose.frame_time_owner == "media_indexing"


def test_pose_query_by_confidence_uses_observation_spine(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    create_synthetic_pose_observation(session=db_session, media_id=media.id, pose_confidence=0.82)

    observations = db_session.scalars(
        select(Observation).where(
            Observation.observation_family == "pose",
            Observation.confidence >= 0.8,
        )
    ).all()

    assert len(observations) == 1
