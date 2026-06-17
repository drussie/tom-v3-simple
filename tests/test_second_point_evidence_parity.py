import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
import tom_v3_storage.media_indexer as media_indexer_module
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base
from tom_v3_video.probe import VideoProbeResult

from apps.api.services.replay import build_replay_info, build_replay_overlay_chunk
from apps.worker.services.reviewed_3d_debug_baseline import DEFAULT_BASELINE_NAME
from apps.worker.services.second_point_evidence_parity import (
    build_second_point_evidence_parity,
)


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
        duration_ms=4200,
        frame_count=126,
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
    sample.write_bytes(b"tom-v3-second-point-evidence-parity")
    return sample


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_walk_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_walk_keys(item))
        return keys
    return set()


def test_missing_second_point_media_path_fails_clearly(db_session: Session) -> None:
    result = build_second_point_evidence_parity(session=db_session, media_path=None)

    assert result["ok"] is False
    assert result["status"] == "missing_second_point_media_path"
    assert result["warnings"]["not_truth"] is True
    assert result["warnings"]["not_generalization_claim"] is True


def test_nonexistent_second_point_media_path_fails_clearly(
    db_session: Session,
    tmp_path: Path,
) -> None:
    result = build_second_point_evidence_parity(
        session=db_session,
        media_path=str(tmp_path / "missing.mp4"),
    )

    assert result["ok"] is False
    assert result["status"] == "second_point_media_path_not_found"
    assert "media file not found" in result["message"]


def test_valid_media_path_produces_parity_output_and_manifest(
    db_session: Session,
    tmp_path: Path,
    monkeypatch,
) -> None:
    _patch_probe(monkeypatch)
    manifest = tmp_path / "second_point_evidence_parity.baseline_manifest.json"

    result = build_second_point_evidence_parity(
        session=db_session,
        media_path=str(_sample_video(tmp_path)),
        run_name="second-point-evidence-parity-v0",
        viewer_base_url="http://127.0.0.1:3000",
        storage_root=tmp_path / "media",
        baseline_manifest_output=manifest,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["parity_type"] == "second_point_evidence_parity_baseline"
    assert result["parity_version"] == "v0"
    assert result["media_id"]
    assert result["replay_url"].endswith(f"/replay/{result['media_id']}")
    assert result["second_point_profile"]["media_indexed"] is True
    assert result["second_point_profile"]["replay_available"] is True
    assert result["second_point_profile"]["event_candidates_available"] is False
    assert result["second_point_profile"]["trajectory_3d_candidates_available"] is False
    assert result["second_point_profile"]["review_annotations_available"] is False
    assert result["second_point_profile"]["baseline_available"] is True
    assert result["warnings"]["not_truth"] is True
    assert result["warnings"]["not_generalization_claim"] is True

    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert manifest_payload["manifest_type"] == "second_point_evidence_parity_baseline_manifest"
    assert manifest_payload["baseline_name"] == "second_point_evidence_parity_baseline_v0"
    assert manifest_payload["media_id"] == result["media_id"]
    assert manifest_payload["profile"]["baseline_available"] is True
    assert manifest_payload["warnings"]["baseline_is_not_truth"] is True


def test_replay_read_model_handles_second_media_with_no_candidate_layers(
    db_session: Session,
    tmp_path: Path,
    monkeypatch,
) -> None:
    _patch_probe(monkeypatch)
    result = build_second_point_evidence_parity(
        session=db_session,
        media_path=str(_sample_video(tmp_path)),
        storage_root=tmp_path / "media",
        baseline_manifest_output=tmp_path / "manifest.json",
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


def test_sample_point_baseline_helper_defaults_remain_unaffected() -> None:
    assert DEFAULT_BASELINE_NAME == "sample_point_reviewed_3d_debug_baseline_v0"


def test_second_point_parity_output_does_not_introduce_truth_fields(
    db_session: Session,
    tmp_path: Path,
    monkeypatch,
) -> None:
    _patch_probe(monkeypatch)
    result = build_second_point_evidence_parity(
        session=db_session,
        media_path=str(_sample_video(tmp_path)),
        storage_root=tmp_path / "media",
        baseline_manifest_output=tmp_path / "manifest.json",
    )

    keys = _walk_keys(result)
    assert not {"truth", "in_out", "score", "adjudication", "point_winner"} & keys
    assert result["warnings"]["does_not_create_in_out"] is True
    assert result["warnings"]["does_not_create_score"] is True
    assert result["warnings"]["no_adjudication"] is True
