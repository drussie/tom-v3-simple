from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.detection import (
    DetectionAdapterInput,
    FixtureDetectionAdapter,
    YoloDetectionAdapter,
    YoloDetectionAdapterUnavailable,
)
from tom_v3_storage.db_models import (
    AtomicObservation,
    Base,
    EvidenceArtifact,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.routers.viewer import build_viewer_run_payload
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.gameplay_adapter import run_gameplay_adapter


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
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_session() -> Generator[Session, None, None]:
        yield db_session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def sample_video(tmp_path) -> str:
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"tom-v3-detection-adapter")
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


def indexed_media(session: Session, sample_video: str, tmp_path):
    return index_media_file(
        session=session,
        source_path=sample_video,
        copy_to_storage=True,
        media_name="detection adapter test clip",
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )


def test_fixture_detection_adapter_produces_frame_time_detections() -> None:
    adapter_input = DetectionAdapterInput(
        media_id="media-1",
        source_uri="file:///tmp/sample.mp4",
        local_path="/tmp/sample.mp4",
        fps=30.0,
        frame_count=90,
        duration_ms=3_000,
        width=640,
        height=360,
        runtime_config={"frame_sample_rate": 30, "max_frames": 2},
        frame_time_summary={"owner": "media_indexing"},
    )

    result = FixtureDetectionAdapter().run(adapter_input)

    assert result.adapter_name == "fixture-ball-player-detector"
    assert len(result.detections) == 6
    assert {detection.label for detection in result.detections} == {
        "ball",
        "near_player",
        "far_player",
    }
    assert result.detections[0].frame_number == 0
    assert result.detections[3].frame_number == 30
    assert result.detections[3].timestamp_ms == frame_to_timestamp_ms(30.0, 30)
    assert result.detections[0].metadata["frame_time_owner"] == "media_indexing"


def test_yolo_adapter_stub_reports_unavailable() -> None:
    adapter_input = DetectionAdapterInput(
        media_id="media-1",
        source_uri="file:///tmp/sample.mp4",
        local_path="/tmp/sample.mp4",
        fps=30.0,
        frame_count=90,
        duration_ms=3_000,
        width=640,
        height=360,
    )

    with pytest.raises(YoloDetectionAdapterUnavailable, match="not available"):
        YoloDetectionAdapter(model_path="/missing/yolo26.pt").run(adapter_input)


def test_detection_adapter_service_persists_atomic_observations(
    db_session: Session,
    sample_video: str,
    tmp_path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    gameplay_result = run_gameplay_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="pytest-gameplay-scope",
    )

    result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="pytest-detection-run",
        frame_sample_rate=30,
        max_frames=3,
        gameplay_run_id=gameplay_result["run_id"],
        output_debug_artifact=True,
    )

    assert result["media_id"] == media.id
    assert result["detection_count"] == 9
    assert result["counts_by_label"] == {"ball": 3, "near_player": 3, "far_player": 3}
    assert result["counts_by_observation_type"] == {
        "ball_detection": 3,
        "player_detection": 6,
    }

    model = db_session.get(ModelRegistry, result["model_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    run = db_session.get(ProcessingRun, result["run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])
    assert model is not None
    assert model.model_family == "detection"
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["frame_time_owner"] == "media_indexing"
    assert runtime_config.payload_jsonb["gameplay_scope_run_id"] == gameplay_result["run_id"]
    assert run is not None
    assert run.run_status == "completed"
    assert step is not None
    assert step.step_status == "completed"

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["run_id"])
        .order_by(Observation.frame_start, Observation.observation_type)
    ).all()
    assert len(observations) == 9
    assert {observation.observation_type for observation in observations} == {
        "ball_detection",
        "player_detection",
    }
    assert all(observation.observation_family == "atomic" for observation in observations)
    assert all(observation.coordinate_space == "image_pixels" for observation in observations)
    assert observations[0].timestamp_start_ms == frame_to_timestamp_ms(media.fps, 0)
    assert observations[-1].timestamp_start_ms == frame_to_timestamp_ms(media.fps, 60)

    atomic_kinds = db_session.scalars(
        select(AtomicObservation.atomic_kind)
        .join(Observation, Observation.id == AtomicObservation.observation_id)
        .where(Observation.run_id == result["run_id"])
    ).all()
    assert atomic_kinds.count("ball_detection") == 3
    assert atomic_kinds.count("player_detection") == 6

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id.in_(result["observation_ids"])
        )
    ).all()
    assert len(lineage) == 9
    assert {row.relationship_type for row in lineage} == {"scoped_by"}

    artifacts = db_session.scalars(
        select(EvidenceArtifact).where(EvidenceArtifact.run_id == result["run_id"])
    ).all()
    assert len(artifacts) == 9
    assert {artifact.artifact_type for artifact in artifacts} == {
        "detection_adapter_debug_json"
    }


def test_query_endpoint_and_viewer_payload_include_detection_observations(
    db_session: Session,
    client: TestClient,
    sample_video: str,
    tmp_path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="viewer-detection-run",
        frame_sample_rate=30,
        max_frames=2,
    )

    ball_query = client.post(
        "/observations/query",
        json={
            "run_id": result["run_id"],
            "observation_type": "ball_detection",
            "confidence_gte": 0.5,
        },
    )
    player_query = client.post(
        "/observations/query",
        json={
            "run_id": result["run_id"],
            "observation_type": "player_detection",
            "frame_start_gte": 0,
            "frame_end_lte": 30,
        },
    )

    assert ball_query.status_code == 200
    assert ball_query.json()["count"] == 2
    assert player_query.status_code == 200
    assert player_query.json()["count"] == 4

    payload = build_viewer_run_payload(db_session, result["run_id"])
    assert payload is not None
    observation_types = {row["observation_type"] for row in payload["observations"]}
    assert {"ball_detection", "player_detection"}.issubset(observation_types)
    assert all(
        row["atomic"] is not None
        for row in payload["observations"]
        if row["observation_type"] in {"ball_detection", "player_detection"}
    )


def test_worker_cli_imports_detection_command() -> None:
    from apps.worker import cli

    assert callable(cli.main)
