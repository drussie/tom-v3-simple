from __future__ import annotations

import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base, EvidenceArtifact
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.frame_extract import FfmpegNotFoundError, extract_frame_image
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.routers.viewer import build_viewer_run_payload
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run


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


def fake_ffmpeg_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
    Path(command[-1]).write_bytes(b"fake-jpeg-frame")
    return subprocess.CompletedProcess(command, 0, "", "")


def test_extract_frame_image_uses_media_indexed_timestamp(tmp_path) -> None:
    source = tmp_path / "source.mp4"
    output = tmp_path / "frame.jpg"
    source.write_bytes(b"video")
    commands: list[list[str]] = []

    def runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return fake_ffmpeg_runner(command, **kwargs)

    extracted = extract_frame_image(
        source_path=source,
        frame_number=30,
        fps=30.0,
        output_path=output,
        runner=runner,
    )

    assert extracted.timestamp_ms == frame_to_timestamp_ms(30.0, 30)
    assert commands[0][commands[0].index("-ss") + 1] == "1.000000"
    assert output.is_file()


def test_missing_ffmpeg_returns_actionable_error(tmp_path) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"video")

    def missing_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        raise FileNotFoundError(command[0])

    with pytest.raises(FfmpegNotFoundError, match="Install ffmpeg"):
        extract_frame_image(
            source_path=source,
            frame_number=0,
            fps=30.0,
            output_path=tmp_path / "frame.jpg",
            runner=missing_runner,
        )


def test_extract_frame_artifacts_persists_frame_and_targeted_artifacts(
    db_session: Session,
    client: TestClient,
    tmp_path,
) -> None:
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"tom-v3-frame-artifacts")
    media = index_media_file(
        session=db_session,
        source_path=video,
        copy_to_storage=True,
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )
    detection_result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="frame-artifact-detection-run",
        frame_sample_rate=30,
        max_frames=2,
    )

    result = extract_frame_artifacts_for_run(
        session=db_session,
        run_id=detection_result["run_id"],
        max_frames=1,
        output_root=tmp_path / "artifacts",
        runner=fake_ffmpeg_runner,
    )

    assert result["extracted_count"] == 1
    assert len(result["frames"]) == 1
    assert result["frames"][0]["frame_number"] == 0
    assert result["frames"][0]["timestamp_ms"] == 0

    artifacts = db_session.scalars(
        select(EvidenceArtifact)
        .where(EvidenceArtifact.run_id == detection_result["run_id"])
        .order_by(EvidenceArtifact.artifact_type, EvidenceArtifact.target_observation_id)
    ).all()
    assert {artifact.artifact_type for artifact in artifacts} == {
        "detection_frame_image",
        "frame_image",
    }
    assert any(artifact.target_observation_id is None for artifact in artifacts)
    assert any(artifact.target_observation_id is not None for artifact in artifacts)

    targeted = next(
        artifact for artifact in artifacts if artifact.target_observation_id is not None
    )
    assert targeted.metadata_jsonb["frame_time_owner"] == "media_indexing"
    assert targeted.metadata_jsonb["frame_number"] == 0
    assert targeted.metadata_jsonb["timestamp_ms"] == 0
    assert targeted.metadata_jsonb["extraction_method"] == "ffmpeg_seek_timestamp"
    assert targeted.metadata_jsonb["placeholder"] is False
    assert targeted.checksum is not None

    payload = build_viewer_run_payload(db_session, detection_result["run_id"])
    assert payload is not None
    frame_artifacts = [
        artifact
        for artifact in payload["artifacts"]
        if artifact["artifact_type"] in {"frame_image", "detection_frame_image"}
    ]
    assert frame_artifacts
    assert any(artifact["target_observation_id"] is None for artifact in frame_artifacts)
    assert any(artifact["target_observation_id"] is not None for artifact in frame_artifacts)

    content_response = client.get(f"/artifacts/{targeted.id}/content")
    assert content_response.status_code == 200
    assert content_response.content == b"fake-jpeg-frame"
