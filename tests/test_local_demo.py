from __future__ import annotations

import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base, EvidenceArtifact, HumanAnnotation, Observation

from apps.worker.services.local_demo import (
    DEMO_CREATED_BY,
    build_local_demo_plan,
    resolve_demo_media_source,
    run_local_fixture_demo,
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


def test_demo_media_resolution_priority(tmp_path) -> None:
    env_media = tmp_path / "env.mp4"
    env_media.write_bytes(b"env")
    fixture_media = tmp_path / "demo_assets" / "tennis_fixture.mp4"
    fixture_media.parent.mkdir()
    fixture_media.write_bytes(b"fixture")

    resolved = resolve_demo_media_source(
        env={"DEMO_MEDIA_PATH": str(env_media)},
        fixture_path=fixture_media,
        generated_path=tmp_path / "generated.mp4",
    )
    assert resolved.path == env_media.resolve()
    assert resolved.source == "DEMO_MEDIA_PATH"

    resolved = resolve_demo_media_source(
        env={},
        fixture_path=fixture_media,
        generated_path=tmp_path / "generated.mp4",
    )
    assert resolved.path == fixture_media.resolve()
    assert resolved.source == "demo_fixture"

    generated_path = tmp_path / "generated" / "synthetic_demo_media.mp4"
    resolved = resolve_demo_media_source(
        env={},
        fixture_path=tmp_path / "missing.mp4",
        generated_path=generated_path,
        generator=lambda path: path.write_bytes(b"synthetic"),
    )
    assert resolved.path == generated_path.resolve()
    assert resolved.synthetic_demo_media is True
    assert resolved.generated is True


def test_demo_plan_lists_expected_fixture_stages() -> None:
    plan = build_local_demo_plan(source_path="/tmp/sample.mp4")

    assert plan["requires_yolo"] is False
    assert plan["requires_pose_weights"] is False
    assert plan["stages"] == [
        "resolve_media",
        "index_media",
        "run_fixture_gameplay",
        "run_fixture_detection",
        "extract_frame_artifacts",
        "build_candidate_tracklets",
        "run_fixture_pose",
        "seed_review_annotations",
        "export_pose_review_dataset",
        "export_tracklet_review_dataset",
        "summarize_demo",
    ]


def test_fixture_demo_runs_without_yolo_or_pose_weights(
    db_session: Session,
    tmp_path,
) -> None:
    source = tmp_path / "sample.mp4"
    source.write_bytes(b"demo-video")

    result = run_local_fixture_demo(
        session=db_session,
        source_path=str(source),
        storage_root=str(tmp_path / "media"),
        artifact_root=str(tmp_path / "artifacts"),
        export_root=str(tmp_path / "exports"),
        frame_sample_rate=30,
        max_frames=3,
        probe_runner=fake_probe_runner,
        frame_artifact_runner=fake_frame_runner,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["message"] == "TOM v3 Simple demo complete"
    assert result["warnings"]["fixture_outputs_are_demo_evidence_only"] is True
    assert result["warnings"]["no_adjudication"] is True

    summary = result["summary"]
    assert summary["media"]["media_id"]
    assert summary["runs"]["detection_run_id"]
    assert summary["runs"]["tracklet_run_id"]
    assert summary["runs"]["pose_run_id"]
    assert summary["observations"]["ball_detection"] > 0
    assert summary["observations"]["player_detection"] > 0
    assert summary["observations"]["tracklet_candidates"] > 0
    assert summary["observations"]["track_points"] > 0
    assert summary["observations"]["pose_observations"] > 0
    assert summary["artifacts"]["frame_artifact_count"] > 0
    assert summary["annotations"]["count"] == 3
    assert len(summary["annotations"]["seeded"]) == 3
    assert summary["exports"]["pose"]["artifact_id"]
    assert Path(summary["exports"]["pose"]["path"]).is_file()
    assert summary["exports"]["tracklet"]["artifact_id"]
    assert Path(summary["exports"]["tracklet"]["path"]).is_file()
    assert summary["viewer_urls"]["detection_run"].endswith(
        f"/runs/{summary['runs']['detection_run_id']}"
    )
    assert summary["viewer_urls"]["pose_run"].endswith(
        f"/runs/{summary['runs']['pose_run_id']}"
    )

    annotations = db_session.scalars(
        select(HumanAnnotation).where(HumanAnnotation.created_by == DEMO_CREATED_BY)
    ).all()
    assert len(annotations) == 3
    assert {annotation.payload_jsonb["review_only"] for annotation in annotations} == {True}
    assert any(
        annotation.payload_jsonb.get("keypoint_name") == "right_wrist"
        for annotation in annotations
    )

    export_artifacts = db_session.scalars(
        select(EvidenceArtifact).where(
            EvidenceArtifact.artifact_type.in_(
                ["pose_review_dataset_export", "tracklet_review_dataset_export"]
            )
        )
    ).all()
    assert {artifact.artifact_type for artifact in export_artifacts} == {
        "pose_review_dataset_export",
        "tracklet_review_dataset_export",
    }

    pose_observation = db_session.scalar(
        select(Observation).where(
            Observation.run_id == summary["runs"]["pose_run_id"],
            Observation.observation_type == "player_pose_observation",
        )
    )
    assert pose_observation is not None
    assert pose_observation.payload_jsonb["source_runtime"] == "fixture_pose"
    assert "annotation_label" not in pose_observation.payload_jsonb
