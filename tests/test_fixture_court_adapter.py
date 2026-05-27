from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    CameraViewObservation,
    CourtKeypointObservation,
    CourtLineObservation,
    HomographyCandidateObservation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    ProjectionDiagnosticObservation,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.worker.cli import _handle_run_fixture_court
from apps.worker.services.court_adapter import run_fixture_court_adapter


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
def indexed_media(db_session: Session, tmp_path: Path) -> MediaAsset:
    video = tmp_path / "court-fixture.mp4"
    video.write_bytes(b"tom-v3-court-fixture")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="fixture court evidence test clip",
        storage_root=tmp_path / "media",
        probe_result=VideoProbeResult(
            duration_ms=3_000,
            frame_count=90,
            fps=30.0,
            width=640,
            height=360,
            codec="h264",
            format="mp4",
            raw_probe={"streams": [{"codec_type": "video"}]},
            frame_count_source="test_fixture",
        ),
    )


def test_plan_only_returns_fixture_court_plan(db_session: Session) -> None:
    result = run_fixture_court_adapter(
        session=db_session,
        media_id="media-plan",
        frame_sample_rate=30,
        max_frames=30,
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert result["plan"]["sampling"]["frame_time_owner"] == "media_indexing"
    assert "run-fixture-court" in result["plan"]["command"]
    assert result["warnings"]["fixture_court_evidence"] is True
    assert result["warnings"]["no_homography_computation"] is True
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_missing_media_returns_clean_error(db_session: Session) -> None:
    result = run_fixture_court_adapter(
        session=db_session,
        media_id="missing-media",
    )

    assert result["ok"] is False
    assert result["status"] == "missing_media"
    assert "media asset not found" in result["message"]
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_fixture_court_adapter_persists_keypoint_line_and_camera_view_observations(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    result = run_fixture_court_adapter(
        session=db_session,
        media_id=indexed_media.id,
        frame_sample_rate=30,
        max_frames=3,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["message"] == "fixture court evidence run complete"
    assert result["media_id"] == indexed_media.id
    assert result["court_run_id"]
    assert result["model_registry_id"]
    assert result["runtime_config_id"]
    assert result["sampled_frames"] == [0, 30, 60]
    assert result["observations"] == {
        "court_keypoint_observation": 3,
        "court_line_observation": 3,
        "camera_view_observation": 3,
        "total": 9,
    }
    assert result["replay_url"].endswith(
        f"/replay/{indexed_media.id}?courtRunId={result['court_run_id']}"
    )

    model = db_session.get(ModelRegistry, result["model_registry_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    run = db_session.get(ProcessingRun, result["court_run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])

    assert model is not None
    assert model.model_family == "court"
    assert model.metadata_jsonb["fixture_adapter"] is True
    assert model.metadata_jsonb["geometry_evidence_only"] is True
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["court_template_name"] == (
        "tennis_court_template_normalized_v0"
    )
    assert runtime_config.payload_jsonb["frame_sample_rate"] == 30
    assert run is not None
    assert run.run_status == "completed"
    assert run.metadata_jsonb["sampled_frames"] == [0, 30, 60]
    assert run.metadata_jsonb["court_keypoint_observation_count"] == 3
    assert step is not None
    assert step.step_status == "completed"
    assert step.metadata_jsonb["camera_view_observation_count"] == 3

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["court_run_id"])
        .order_by(Observation.frame_start, Observation.observation_type)
    ).all()
    assert len(observations) == 9
    assert {observation.observation_family for observation in observations} == {"court"}
    assert {observation.model_id for observation in observations} == {
        result["model_registry_id"]
    }
    assert {observation.runtime_config_id for observation in observations} == {
        result["runtime_config_id"]
    }
    assert {observation.frame_start for observation in observations} == {0, 30, 60}
    assert {observation.timestamp_start_ms for observation in observations} == {
        frame_to_timestamp_ms(indexed_media.fps or 30.0, frame) for frame in [0, 30, 60]
    }
    assert all(
        observation.payload_jsonb["geometry_evidence_only"] is True
        for observation in observations
    )

    keypoint = db_session.scalar(select(CourtKeypointObservation))
    line = db_session.scalar(select(CourtLineObservation))
    camera = db_session.scalar(select(CameraViewObservation))
    assert keypoint is not None
    assert keypoint.keypoint_count == 12
    assert keypoint.keypoints_present_count == 12
    assert keypoint.metadata_jsonb["not_real_court_model"] is True
    assert line is not None
    assert line.line_count == 8
    assert "baseline_near" in line.line_classes_jsonb
    assert line.metadata_jsonb["fixture_court_evidence"] is True
    assert camera is not None
    assert camera.view_label == "broadcast_hardcam"
    assert camera.camera_motion_hint == "stable"
    assert camera.metadata_jsonb["fixture_camera_view_evidence"] is True


def test_fixture_court_adapter_creates_no_homography_or_projection_diagnostics(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    result = run_fixture_court_adapter(
        session=db_session,
        media_id=indexed_media.id,
        frame_sample_rate=30,
        max_frames=2,
    )

    assert result["ok"] is True
    assert db_session.scalar(select(func.count()).select_from(HomographyCandidateObservation)) == 0
    assert db_session.scalar(select(func.count()).select_from(ProjectionDiagnosticObservation)) == 0


def test_cli_handler_plan_only_returns_expected_json(db_session: Session) -> None:
    result = _handle_run_fixture_court(
        db_session,
        Namespace(
            media_id="media-plan",
            frame_sample_rate=30,
            max_frames=30,
            run_name="fixture-court-evidence",
            viewer_base_url="http://127.0.0.1:3000",
            plan_only=True,
        ),
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert result["warnings"]["no_tennis_event_interpretation"] is True
