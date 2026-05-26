from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.gameplay import (
    FixtureGameplayAdapter,
    GameplayAdapterInput,
    TomV1AdapterUnavailable,
    TomV1GameplayAdapter,
)
from tom_v3_storage.db_models import (
    Base,
    EvidenceArtifact,
    GameplayObservation,
    ModelRegistry,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.routers.viewer import build_viewer_run_payload
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
def sample_video(tmp_path) -> str:
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"tom-v3-gameplay-adapter")
    return str(video)


def probe_result() -> VideoProbeResult:
    return VideoProbeResult(
        duration_ms=2_000,
        frame_count=60,
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
        media_name="adapter test clip",
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )


def test_fixture_adapter_produces_frame_time_segments() -> None:
    adapter_input = GameplayAdapterInput(
        media_id="media-1",
        source_uri="file:///tmp/sample.mp4",
        local_path="/tmp/sample.mp4",
        fps=30.0,
        frame_count=60,
        duration_ms=2_000,
        frame_time_summary={"owner": "media_indexing"},
    )

    result = FixtureGameplayAdapter().run(adapter_input)

    assert result.adapter_name == "fixture-gameplay-adapter"
    assert [segment.label for segment in result.segments] == [
        "gameplay",
        "non_gameplay",
        "uncertain",
        "gameplay",
    ]
    assert result.segments[0].frame_start == 0
    assert result.segments[0].timestamp_end_ms == frame_to_timestamp_ms(30.0, 18)
    assert result.segments[2].metadata["media_frame_time_owner"] == "media_indexing"


def test_tom_v1_adapter_stub_reports_unavailable() -> None:
    adapter_input = GameplayAdapterInput(
        media_id="media-1",
        source_uri="file:///tmp/sample.mp4",
        local_path="/tmp/sample.mp4",
        fps=30.0,
        frame_count=60,
        duration_ms=2_000,
    )

    with pytest.raises(TomV1AdapterUnavailable, match="not available"):
        TomV1GameplayAdapter(tom_v1_path="/missing/tom-v1").run(adapter_input)


def test_gameplay_adapter_service_persists_observations(
    db_session: Session,
    sample_video: str,
    tmp_path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)

    result = run_gameplay_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="pytest-gameplay-run",
        output_debug_artifact=True,
    )

    assert result["media_id"] == media.id
    assert result["segment_count"] == 4
    assert result["counts_by_label"] == {"gameplay": 2, "non_gameplay": 1, "uncertain": 1}

    model = db_session.get(ModelRegistry, result["model_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    run = db_session.get(ProcessingRun, result["run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])
    assert model is not None
    assert model.model_family == "gameplay"
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["frame_time_owner"] == "media_indexing"
    assert run is not None
    assert run.run_status == "completed"
    assert step is not None
    assert step.step_status == "completed"

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["run_id"])
        .order_by(Observation.frame_start)
    ).all()
    assert len(observations) == 4
    assert all(observation.observation_family == "gameplay" for observation in observations)
    assert all(observation.observation_type == "view_state" for observation in observations)
    assert all(observation.model_id == model.id for observation in observations)
    assert all(observation.runtime_config_id == runtime_config.id for observation in observations)
    assert observations[0].timestamp_start_ms == 0
    assert observations[0].timestamp_end_ms == frame_to_timestamp_ms(media.fps, 18)
    assert observations[0].payload_jsonb["processing_step_id"] == step.id

    states = db_session.scalars(
        select(GameplayObservation.view_state)
        .join(Observation, Observation.id == GameplayObservation.observation_id)
        .where(Observation.run_id == result["run_id"])
    ).all()
    assert {"gameplay", "non_gameplay", "uncertain"}.issubset(set(states))

    artifacts = db_session.scalars(
        select(EvidenceArtifact).where(EvidenceArtifact.run_id == result["run_id"])
    ).all()
    assert len(artifacts) == 4
    assert {artifact.artifact_type for artifact in artifacts} == {
        "gameplay_adapter_debug_json"
    }


def test_viewer_payload_includes_gameplay_adapter_observations(
    db_session: Session,
    sample_video: str,
    tmp_path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    result = run_gameplay_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="viewer-gameplay-run",
    )

    payload = build_viewer_run_payload(db_session, result["run_id"])

    assert payload is not None
    assert payload["run"]["id"] == result["run_id"]
    assert payload["media"]["id"] == media.id
    view_states = {
        row["gameplay"]["view_state"]
        for row in payload["observations"]
        if row["gameplay"] is not None
    }
    assert {"gameplay", "non_gameplay", "uncertain"}.issubset(view_states)


def test_worker_cli_imports_gameplay_command() -> None:
    from apps.worker import cli

    assert callable(cli.main)
