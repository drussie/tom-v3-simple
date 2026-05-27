from __future__ import annotations

import argparse
import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    AtomicObservation,
    Base,
    EvidenceArtifact,
    HumanAnnotation,
    MediaAsset,
    Observation,
    ObservationLineage,
)

from apps.worker.cli import _handle_completion_audit
from apps.worker.services.completion_audit import run_completion_audit
from apps.worker.services.local_demo import run_local_fixture_demo


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


def fake_probe_runner(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=args,
        returncode=0,
        stdout=(
            '{"streams":[{"codec_type":"video","codec_name":"h264",'
            '"width":640,"height":360,"avg_frame_rate":"30/1","nb_frames":"90",'
            '"duration":"3.000000"}],"format":{"format_name":"mov,mp4","duration":"3.000000"}}'
        ),
        stderr="",
    )


def fake_frame_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
    Path(command[-1]).write_bytes(b"demo-frame")
    return subprocess.CompletedProcess(command, 0, "", "")


def seed_fixture_demo(session: Session, tmp_path: Path) -> dict[str, Any]:
    source = tmp_path / "sample.mp4"
    source.write_bytes(b"demo-video")
    return run_local_fixture_demo(
        session=session,
        source_path=str(source),
        storage_root=str(tmp_path / "media"),
        artifact_root=str(tmp_path / "artifacts"),
        export_root=str(tmp_path / "exports"),
        frame_sample_rate=30,
        max_frames=3,
        probe_runner=fake_probe_runner,
        frame_artifact_runner=fake_frame_runner,
    )


def test_completion_audit_passes_after_fixture_demo(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seed_fixture_demo(db_session, tmp_path)

    result = run_completion_audit(db_session, demo_only=True)

    assert result["ok"] is True
    assert result["status"] == "passed"
    assert result["observation_only"] is True
    assert result["no_adjudication"] is True
    assert result["failures"] == []
    assert result["warnings"] == []
    assert result["summary"]["media_count"] == 1
    assert result["summary"]["observation_count"] > 0
    assert result["summary"]["typed_row_count"] > 0
    assert result["summary"]["lineage_count"] > 0
    assert result["summary"]["artifact_count"] > 0
    assert result["summary"]["annotation_count"] == 3
    assert result["summary"]["export_artifact_count"] == 2


def test_completion_audit_fails_without_demo_media(db_session: Session) -> None:
    result = run_completion_audit(db_session, demo_only=True)

    assert result["ok"] is False
    assert result["status"] == "failed"
    assert any(
        "Run make demo first" in detail
        for failure in result["failures"]
        for detail in failure["details"]
    )


def test_completion_audit_warns_on_empty_all_data_mode(db_session: Session) -> None:
    result = run_completion_audit(db_session, demo_only=False)

    assert result["ok"] is True
    assert result["status"] == "warning"
    assert any(check["name"] == "media_scope_has_rows" for check in result["warnings"])


def test_completion_audit_catches_observation_with_missing_media_and_run(
    db_session: Session,
) -> None:
    db_session.add(
        Observation(
            media_id="missing-media",
            run_id="missing-run",
            observation_family="atomic",
            observation_type="ball_detection",
            granularity="frame",
            frame_start=0,
            frame_end=0,
            timestamp_start_ms=0,
            timestamp_end_ms=0,
            payload_jsonb={},
        )
    )
    db_session.commit()

    result = run_completion_audit(db_session, demo_only=False)

    assert result["ok"] is False
    assert _failure_names(result) >= {
        "observations_reference_media",
        "observations_reference_runs",
    }


def test_completion_audit_catches_typed_row_with_missing_observation(
    db_session: Session,
) -> None:
    db_session.add(
        AtomicObservation(
            observation_id="missing-observation",
            atomic_kind="ball_detection",
            payload_jsonb={},
        )
    )
    db_session.commit()

    result = run_completion_audit(db_session, demo_only=False)

    assert result["ok"] is False
    assert "atomic_rows_reference_observations" in _failure_names(result)


def test_completion_audit_catches_lineage_with_missing_parent_or_child(
    db_session: Session,
) -> None:
    db_session.add(
        ObservationLineage(
            parent_observation_id="missing-parent",
            child_observation_id="missing-child",
            relationship_type="tracked_from",
            payload_jsonb={},
        )
    )
    db_session.commit()

    result = run_completion_audit(db_session, demo_only=False)

    assert result["ok"] is False
    assert _failure_names(result) >= {
        "lineage_parents_reference_observations",
        "lineage_children_reference_observations",
    }


def test_completion_audit_catches_artifact_with_missing_target(
    db_session: Session,
) -> None:
    media = _media()
    db_session.add(media)
    db_session.flush()
    db_session.add(
        EvidenceArtifact(
            media_id=media.id,
            target_observation_id="missing-observation",
            artifact_type="frame_image",
            uri="file:///tmp/missing-frame.jpg",
            checksum="sha256:demo",
            metadata_jsonb={},
        )
    )
    db_session.commit()

    result = run_completion_audit(db_session, demo_only=False)

    assert result["ok"] is False
    assert "artifacts_reference_target_observations" in _failure_names(result)


def test_completion_audit_catches_annotation_with_missing_observation(
    db_session: Session,
) -> None:
    media = _media()
    db_session.add(media)
    db_session.flush()
    db_session.add(
        HumanAnnotation(
            media_id=media.id,
            observation_id="missing-observation",
            annotation_type="uncertain",
            payload_jsonb={"annotation_label": "uncertain"},
            created_by="test",
        )
    )
    db_session.commit()

    result = run_completion_audit(db_session, demo_only=False)

    assert result["ok"] is False
    assert "annotations_reference_observations" in _failure_names(result)


def test_cli_completion_audit_handler_returns_json_ready_result(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seed_fixture_demo(db_session, tmp_path)
    result = _handle_completion_audit(
        db_session,
        argparse.Namespace(media_id=None, demo_only=True, strict=False),
    )

    assert result["ok"] is True
    assert result["status"] == "passed"
    assert result["summary"]["export_artifact_count"] == 2


def _media() -> MediaAsset:
    return MediaAsset(
        source_uri="file:///tmp/sample.mp4",
        media_type="video",
        duration_ms=1000,
        frame_count=30,
        fps=30.0,
        width=640,
        height=360,
        metadata_jsonb={"tom_v3_demo": False},
    )


def _failure_names(result: dict[str, Any]) -> set[str]:
    return {check["name"] for check in result["failures"]}
