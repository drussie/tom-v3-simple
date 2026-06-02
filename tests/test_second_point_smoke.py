from collections.abc import Generator
from pathlib import Path

import pytest
import tom_v3_storage.media_indexer as media_indexer_module
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base
from tom_v3_video.probe import VideoProbeResult

from apps.api.services.replay import build_replay_info, build_replay_overlay_chunk
from apps.worker.services.second_point_smoke import run_second_point_ingestion_smoke


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


def _fake_probe_result() -> VideoProbeResult:
    return VideoProbeResult(
        duration_ms=3000,
        frame_count=90,
        fps=30.0,
        width=1280,
        height=720,
        codec="h264",
        format="mov,mp4",
        raw_probe={"streams": [{"codec_type": "video"}]},
        frame_count_source="test_fixture",
    )


def _patch_probe(monkeypatch) -> None:
    monkeypatch.setattr(
        media_indexer_module,
        "probe_video",
        lambda *_args, **_kwargs: _fake_probe_result(),
    )


def _sample_video(tmp_path: Path) -> Path:
    sample = tmp_path / "second_point.mp4"
    sample.write_bytes(b"tom-v3-second-point-smoke")
    return sample


def test_missing_second_point_media_path_returns_clear_error(db_session: Session) -> None:
    result = run_second_point_ingestion_smoke(session=db_session, media_path=None)

    assert result["ok"] is False
    assert result["status"] == "missing_second_point_media_path"
    assert result["warnings"]["not_truth"] is True
    assert result["warnings"]["not_generalization_claim"] is True


def test_nonexistent_second_point_media_path_returns_clear_error(
    db_session: Session,
    tmp_path: Path,
) -> None:
    result = run_second_point_ingestion_smoke(
        session=db_session,
        media_path=str(tmp_path / "missing.mp4"),
    )

    assert result["ok"] is False
    assert result["status"] == "second_point_media_path_not_found"
    assert "media file not found" in result["message"]


def test_valid_second_point_media_path_produces_smoke_summary(
    db_session: Session,
    tmp_path: Path,
    monkeypatch,
) -> None:
    _patch_probe(monkeypatch)
    sample = _sample_video(tmp_path)
    manifest = tmp_path / "second_point_smoke_manifest.json"

    result = run_second_point_ingestion_smoke(
        session=db_session,
        media_path=str(sample),
        run_name="second-point-ingestion-smoke-v0",
        viewer_base_url="http://127.0.0.1:3000",
        storage_root=tmp_path / "media",
        manifest_output=manifest,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["smoke_type"] == "second_point_ingestion_evidence_replay_smoke"
    assert result["media_id"]
    assert result["replay_url"].endswith(f"/replay/{result['media_id']}")
    assert result["media_metadata"] == {
        "duration_ms": 3000,
        "frame_count": 90,
        "fps": 30.0,
        "width": 1280,
        "height": 720,
    }
    assert result["warnings"]["candidate_only"] is True
    assert result["warnings"]["observation_only"] is True
    assert result["warnings"]["not_truth"] is True
    assert result["warnings"]["not_generalization_claim"] is True
    assert manifest.is_file()


def test_replay_read_model_handles_media_with_no_event_or_3d_candidates(
    db_session: Session,
    tmp_path: Path,
    monkeypatch,
) -> None:
    _patch_probe(monkeypatch)
    result = run_second_point_ingestion_smoke(
        session=db_session,
        media_path=str(_sample_video(tmp_path)),
        storage_root=tmp_path / "media",
    )

    replay_info = build_replay_info(db_session, result["media_id"])
    overlay_chunk = build_replay_overlay_chunk(
        db_session,
        media_id=result["media_id"],
        start_ms=0,
        end_ms=1000,
        layers={"hit_candidates", "bounce_candidates"},
    )

    assert replay_info is not None
    assert replay_info["media_id"] == result["media_id"]
    assert replay_info["trajectory_3d_summary"]["available"] is False
    assert overlay_chunk is not None
    assert overlay_chunk["hit_candidates"] == []
    assert overlay_chunk["bounce_candidates"] == []
    assert overlay_chunk["event_candidate_3d_diagnostic_summary"]["available"] is False
    assert overlay_chunk["trajectory_3d_debug"]["status"] == "no_trajectory_3d_run_selected"
    assert overlay_chunk["observation_only"] is True
    assert overlay_chunk["no_adjudication"] is True
