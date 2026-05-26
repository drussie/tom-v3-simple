import subprocess
from collections.abc import Generator

import pytest
import tom_v3_storage.media_indexer as media_indexer_module
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base
from tom_v3_storage.local_media import LocalMediaStorage, calculate_sha256
from tom_v3_storage.media_indexer import MediaIndexingError, index_media_file
from tom_v3_video.probe import FfprobeNotFoundError, VideoProbeResult, probe_video
from tom_v3_video.time_index import (
    build_frame_time_summary,
    frame_to_timestamp_ms,
    timestamp_ms_to_frame,
)

from apps.api.db import get_session
from apps.api.main import create_app
from apps.worker.services.media_indexer import index_media


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
def sample_media_file(tmp_path) -> str:
    sample = tmp_path / "sample.mp4"
    sample.write_bytes(b"tom-v3-media")
    return str(sample)


def fake_probe_result() -> VideoProbeResult:
    return VideoProbeResult(
        duration_ms=2000,
        frame_count=60,
        fps=30.0,
        width=640,
        height=360,
        codec="h264",
        format="mov,mp4,m4a,3gp,3g2,mj2",
        raw_probe={"streams": [{"codec_type": "video"}], "format": {"duration": "2.0"}},
        frame_count_source="ffprobe_nb_frames",
    )


def patch_probe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        media_indexer_module,
        "probe_video",
        lambda *_args, **_kwargs: fake_probe_result(),
    )


def test_checksum_calculation_is_stable(sample_media_file: str) -> None:
    first = calculate_sha256(sample_media_file)
    second = calculate_sha256(sample_media_file)

    assert first == second
    assert len(first) == 64


def test_local_media_storage_copies_file(sample_media_file: str, tmp_path) -> None:
    stored = LocalMediaStorage(tmp_path / "media").store_file(sample_media_file, "media-1")

    assert stored.path.is_file()
    assert stored.path.read_bytes() == b"tom-v3-media"
    assert stored.uri.startswith("file://")
    assert stored.path.parent.name == "media-1"


def test_frame_time_mapping_utilities() -> None:
    assert frame_to_timestamp_ms(30.0, 45) == 1500
    assert timestamp_ms_to_frame(30.0, 1500) == 45

    summary = build_frame_time_summary(fps=30.0, frame_count=60, duration_ms=2000)
    assert summary["mapping"] == "constant_fps"
    assert summary["final_frame"] == {"frame_number": 59, "timestamp_ms": 1967}


def test_ffprobe_wrapper_parses_mocked_output(sample_media_file: str) -> None:
    def fake_runner(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout=(
                '{"streams":[{"codec_type":"video","codec_name":"h264",'
                '"width":640,"height":360,"avg_frame_rate":"30/1","nb_frames":"60",'
                '"duration":"2.000000"}],"format":{"format_name":"mov,mp4","duration":"2.000000"}}'
            ),
            stderr="",
        )

    probe = probe_video(sample_media_file, runner=fake_runner)

    assert probe.duration_ms == 2000
    assert probe.frame_count == 60
    assert probe.fps == 30.0
    assert probe.width == 640
    assert probe.height == 360


def test_missing_ffprobe_returns_actionable_error(sample_media_file: str) -> None:
    def missing_runner(*args, **kwargs):
        raise FileNotFoundError("ffprobe")

    with pytest.raises(FfprobeNotFoundError, match="ffprobe is required"):
        probe_video(sample_media_file, runner=missing_runner)


def test_index_media_file_copy_and_register_modes(
    db_session: Session,
    sample_media_file: str,
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_probe(monkeypatch)

    copied = index_media_file(
        session=db_session,
        source_path=sample_media_file,
        copy_to_storage=True,
        media_name="copied sample",
        storage_root=tmp_path / "stored",
    )
    registered = index_media_file(
        session=db_session,
        source_path=sample_media_file,
        copy_to_storage=False,
        media_name="registered sample",
        storage_root=tmp_path / "stored",
    )

    assert copied.duration_ms == 2000
    assert copied.frame_count == 60
    assert copied.fps == 30.0
    assert copied.width == 640
    assert copied.height == 360
    assert copied.checksum == calculate_sha256(sample_media_file)
    assert copied.metadata_jsonb["storage_mode"] == "copied"
    assert copied.metadata_jsonb["stored_uri"].startswith("file://")
    assert copied.metadata_jsonb["frame_time_index"]["mapping"] == "constant_fps"

    assert registered.metadata_jsonb["storage_mode"] == "registered"
    assert registered.source_uri == registered.metadata_jsonb["original_source_uri"]


def test_index_media_file_missing_source_returns_clear_error(db_session: Session, tmp_path) -> None:
    with pytest.raises(MediaIndexingError, match="media file not found"):
        index_media_file(db_session, tmp_path / "missing.mp4")


def test_api_register_file_endpoint(
    client: TestClient,
    sample_media_file: str,
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_probe(monkeypatch)

    response = client.post(
        "/media/register-file",
        json={
            "source_path": sample_media_file,
            "copy_to_storage": True,
            "media_name": "api sample",
            "storage_root": str(tmp_path / "api-media"),
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["duration_ms"] == 2000
    assert body["frame_count"] == 60
    assert body["fps"] == 30.0
    assert body["checksum"] == calculate_sha256(sample_media_file)
    assert body["metadata_jsonb"]["storage_mode"] == "copied"
    assert body["metadata_jsonb"]["frame_time_index"]["final_frame"]["frame_number"] == 59

    fetched = client.get(f"/media/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_api_register_file_missing_source_returns_400(client: TestClient, tmp_path) -> None:
    response = client.post(
        "/media/register-file",
        json={"source_path": str(tmp_path / "missing.mp4")},
    )

    assert response.status_code == 400
    assert "media file not found" in response.json()["detail"]


def test_worker_index_media_service(
    db_session: Session,
    sample_media_file: str,
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    patch_probe(monkeypatch)

    media = index_media(
        session=db_session,
        source_path=sample_media_file,
        copy_to_storage=True,
        storage_root=tmp_path / "worker-media",
    )

    assert media.id
    assert media.metadata_jsonb["storage_mode"] == "copied"
    assert media.metadata_jsonb["frame_time_index"]["owner"] == "media_indexing"
