from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.observations import ObservationQueryFilters
from tom_v3_storage.db_models import (
    Base,
    ModelRegistry,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.routers.viewer import build_viewer_run_payload
from apps.api.services.query_builder import query_observations
from apps.worker.services.detection_adapter import run_detection_adapter
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


def seed_detection_run(db_session: Session, tmp_path, max_frames: int = 3) -> dict[str, object]:
    video = tmp_path / "tracklet-source.mp4"
    video.write_bytes(b"tom-v3-tracklet-builder")
    media = index_media_file(
        session=db_session,
        source_path=video,
        copy_to_storage=True,
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )
    return run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="tracklet-source-detection-run",
        frame_sample_rate=30,
        max_frames=max_frames,
    )


def test_tracklet_builder_groups_fixture_detections_into_candidates(
    db_session: Session,
    tmp_path,
) -> None:
    detection_result = seed_detection_run(db_session, tmp_path)

    result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=30,
    )

    assert result["source_detection_run_id"] == detection_result["run_id"]
    assert result["tracklet_count"] == 3
    assert result["track_point_count"] == 9
    assert result["tracklets_by_family"] == {"ball": 1, "player": 2}

    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    run = db_session.get(ProcessingRun, result["tracklet_run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])
    model = db_session.get(ModelRegistry, result["model_id"])
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["source_detection_run_id"] == detection_result["run_id"]
    assert runtime_config.payload_jsonb["track_status"] == "candidate"
    assert runtime_config.payload_jsonb["identity_status"] == "unverified"
    assert run is not None
    assert run.run_status == "completed"
    assert step is not None
    assert step.step_name == "tracklet_candidate_builder"
    assert step.step_status == "completed"
    assert model is not None
    assert model.model_family == "tracker"

    tracklets = db_session.scalars(
        select(Tracklet)
        .where(Tracklet.run_id == result["tracklet_run_id"])
        .order_by(Tracklet.track_family, Tracklet.subject_ref)
    ).all()
    assert {tracklet.subject_ref for tracklet in tracklets} == {
        "ball",
        "far_player",
        "near_player",
    }
    assert all(tracklet.metadata_jsonb["track_status"] == "candidate" for tracklet in tracklets)
    assert all(
        tracklet.metadata_jsonb["identity_status"] == "unverified" for tracklet in tracklets
    )
    assert all(
        tracklet.metadata_jsonb["frame_time_owner"] == "media_indexing"
        for tracklet in tracklets
    )


def test_track_points_reference_source_detection_observations(
    db_session: Session,
    tmp_path,
) -> None:
    detection_result = seed_detection_run(db_session, tmp_path)
    result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=30,
    )

    points = db_session.scalars(
        select(TrackPoint)
        .join(Tracklet)
        .where(Tracklet.run_id == result["tracklet_run_id"])
        .order_by(TrackPoint.frame_number)
    ).all()

    assert len(points) == 9
    assert all(point.observation_id in detection_result["observation_ids"] for point in points)
    assert all(point.timestamp_ms == point.observation.timestamp_start_ms for point in points)
    assert all(point.frame_number == point.observation.frame_start for point in points)
    assert all(point.payload_jsonb["frame_time_owner"] == "media_indexing" for point in points)
    assert all(point.payload_jsonb["track_status"] == "candidate" for point in points)
    assert all("bbox" in point.payload_jsonb for point in points)


def test_max_gap_frames_starts_new_tracklets(
    db_session: Session,
    tmp_path,
) -> None:
    detection_result = seed_detection_run(db_session, tmp_path)
    result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=10,
    )

    assert result["tracklet_count"] == 9
    assert result["track_point_count"] == 9


def test_tracklet_run_is_viewer_and_query_compatible(
    db_session: Session,
    tmp_path,
) -> None:
    detection_result = seed_detection_run(db_session, tmp_path)
    result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=30,
    )

    viewer_payload = build_viewer_run_payload(db_session, str(result["tracklet_run_id"]))
    assert viewer_payload is not None
    assert viewer_payload["run"]["id"] == result["tracklet_run_id"]
    assert len(viewer_payload["tracklets"]) == 3
    assert sum(len(tracklet["points"]) for tracklet in viewer_payload["tracklets"]) == 9
    assert {
        segment["state"]
        for tracklet in viewer_payload["tracklets"]
        for segment in tracklet["metadata_jsonb"]["coverage_segments"]
    } == {"candidate"}

    source_query = query_observations(
        db_session,
        ObservationQueryFilters(tracklet_id=result["tracklet_ids"][0]),
    )
    assert source_query.count >= 1
    assert source_query.observations[0].id in detection_result["observation_ids"]


def test_worker_cli_imports_tracklet_command() -> None:
    from apps.worker import cli

    assert callable(cli.main)
