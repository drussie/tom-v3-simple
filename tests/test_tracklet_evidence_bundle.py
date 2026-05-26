from __future__ import annotations

import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.services.tracklet_evidence_bundle import build_tracklet_evidence_bundle
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
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
    Path(command[-1]).write_bytes(b"fake-tracklet-frame")
    return subprocess.CompletedProcess(command, 0, "", "")


def seed_tracklet_run(
    db_session: Session,
    tmp_path,
    with_artifacts: bool = False,
) -> dict[str, object]:
    video = tmp_path / "tracklet-evidence-source.mp4"
    video.write_bytes(b"tom-v3-tracklet-evidence")
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
        run_name="tracklet-evidence-detection-run",
        frame_sample_rate=30,
        max_frames=3,
        output_debug_artifact=True,
    )
    if with_artifacts:
        extract_frame_artifacts_for_run(
            session=db_session,
            run_id=str(detection_result["run_id"]),
            max_frames=1,
            output_root=tmp_path / "artifacts",
            runner=fake_ffmpeg_runner,
        )
    tracklet_result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=30,
    )
    return {
        "media_id": media.id,
        "detection_run_id": detection_result["run_id"],
        "tracklet_run_id": tracklet_result["tracklet_run_id"],
        "tracklet_id": tracklet_result["tracklet_ids"][0],
    }


def test_tracklet_evidence_bundle_reconstructs_multirun_chain(
    db_session: Session,
    tmp_path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_artifacts=False)

    bundle = build_tracklet_evidence_bundle(db_session, str(seeded["tracklet_id"]))

    assert bundle is not None
    assert bundle["tracklet"]["typed"]["id"] == seeded["tracklet_id"]
    assert bundle["tracklet"]["observation"]["observation_family"] == "track"
    assert bundle["tracklet"]["observation"]["observation_type"] in {
        "ball_tracklet_candidate",
        "player_tracklet_candidate",
    }
    assert bundle["runs"]["tracklet_run"]["id"] == seeded["tracklet_run_id"]
    assert bundle["runs"]["source_detection_run"]["id"] == seeded["detection_run_id"]
    assert bundle["runtime_configs"]["tracklet_runtime_config"] is not None
    assert bundle["runtime_configs"]["source_detection_runtime_config"] is not None
    assert bundle["model_registry"]["tracklet_builder_model"] is not None
    assert bundle["model_registry"]["source_detection_model"] is not None
    assert bundle["track_points"]
    assert bundle["source_detections"]
    assert bundle["summary"]["track_status"] == "candidate"
    assert bundle["summary"]["identity_status"] == "unverified"
    assert bundle["summary"]["track_point_count"] == len(bundle["track_points"])
    assert bundle["summary"]["source_detection_count"] == len(bundle["source_detections"])
    assert "not proof" in bundle["summary"]["warning"]

    for point in bundle["track_points"]:
        assert point["typed"]["observation_id"] == point["observation"]["id"]
        assert point["observation"]["observation_type"] == "track_point_candidate"
        assert point["source_detection"]["id"] == point["source_detection_observation_id"]
        assert point["source_detection"]["observation_type"] in {
            "ball_detection",
            "player_detection",
        }
        assert point["lineage_to_source"]["relationship_type"] == "tracked_from"
        assert point["lineage_to_tracklet"]["relationship_type"] == "grouped_from"
        assert point["timestamp_ms"] == point["source_detection"]["timestamp_start_ms"]

    relationship_types = {row["relationship_type"] for row in bundle["lineage"]}
    assert {"tracked_from", "grouped_from"}.issubset(relationship_types)


def test_tracklet_evidence_bundle_includes_frame_artifacts_when_available(
    db_session: Session,
    tmp_path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_artifacts=True)

    bundle = build_tracklet_evidence_bundle(db_session, str(seeded["tracklet_id"]))

    assert bundle is not None
    assert bundle["frame_artifacts"]
    assert any(point["frame_artifacts"] for point in bundle["track_points"])
    artifact_types = {
        artifact["artifact_type"] for artifact in bundle["frame_artifacts"]
    }
    assert artifact_types.issubset({"frame_image", "detection_frame_image"})


def test_tracklet_evidence_bundle_endpoint_returns_expected_shape(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_artifacts=True)

    response = client.get(f"/tracklets/{seeded['tracklet_id']}/evidence-bundle")

    assert response.status_code == 200
    body = response.json()
    assert body["tracklet"]["typed"]["id"] == seeded["tracklet_id"]
    assert body["runs"]["source_detection_run"]["id"] == seeded["detection_run_id"]
    assert body["track_points"]
    assert body["source_detections"]
    assert body["lineage"]


def test_tracklet_evidence_bundle_endpoint_returns_404_for_missing_tracklet(
    client: TestClient,
) -> None:
    response = client.get("/tracklets/missing-tracklet/evidence-bundle")

    assert response.status_code == 404
