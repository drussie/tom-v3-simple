from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.pose_inference import FakePoseResultProvider
from tom_v3_model_adapters.yolo_inference import FakeYoloResultProvider
from tom_v3_storage.db_models import (
    Base,
    Observation,
    ObservationLineage,
    PoseObservation,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.services.replay import pose_overlay_item_from_row, pose_timeline_item_from_row
from apps.worker.services.main_subject_filter import select_main_player_subjects
from apps.worker.services.real_detection_replay import run_real_detection_replay
from apps.worker.services.real_pose_replay import run_real_pose_replay


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
def indexed_media(db_session: Session, tmp_path: Path):
    video = tmp_path / "main-subject-filter.mp4"
    video.write_bytes(b"tom-v3-main-subject-filter")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="main subject filter test clip",
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


@pytest.fixture()
def detection_weights_path(tmp_path: Path) -> Path:
    weights_root = tmp_path / "weights" / "yolo"
    weights_root.mkdir(parents=True, exist_ok=True)
    weights = weights_root / "real-detection.pt"
    weights.write_bytes(b"fake-yolo-weights")
    return weights


@pytest.fixture()
def pose_weights_path(tmp_path: Path) -> Path:
    weights_root = tmp_path / "weights" / "pose"
    weights_root.mkdir(parents=True, exist_ok=True)
    weights = weights_root / "real-pose.pt"
    weights.write_bytes(b"fake-pose-weights")
    return weights


def runtime_ok(**kwargs):
    return {
        "status": "ok",
        "requested_device": kwargs.get("requested_device", "cpu"),
        "resolved_device": "cpu",
        "ultralytics_available": True,
        "torch_available": True,
        "opencv_available": True,
        "missing_packages": [],
    }


def create_noisy_player_detection_run(
    *,
    session: Session,
    media_id: str,
    weights_path: Path,
) -> dict[str, object]:
    return run_real_detection_replay(
        session=session,
        media_id=media_id,
        weights_path=str(weights_path),
        model_name="test-tom-v1-player-detector",
        model_version="subject-filter-test",
        device="cpu",
        every_n_frames=30,
        max_frames=3,
        allowed_roots=[str(weights_path.parent)],
        probe_runtime=runtime_ok,
        yolo_result_provider=FakeYoloResultProvider(
            boxes_by_frame={
                0: [
                    {
                        "xyxy": [270.0, 210.0, 355.0, 355.0],
                        "confidence": 0.91,
                        "class_id": 0,
                        "class_name": "person",
                    },
                    {
                        "xyxy": [285.0, 70.0, 335.0, 160.0],
                        "confidence": 0.88,
                        "class_id": 0,
                        "class_name": "person",
                    },
                    {
                        "xyxy": [6.0, 190.0, 44.0, 300.0],
                        "confidence": 0.96,
                        "class_id": 0,
                        "class_name": "person",
                    },
                    {
                        "xyxy": [500.0, 25.0, 518.0, 62.0],
                        "confidence": 0.85,
                        "class_id": 0,
                        "class_name": "person",
                    },
                ],
                30: [
                    {
                        "xyxy": [260.0, 205.0, 350.0, 356.0],
                        "confidence": 0.89,
                        "class_id": 0,
                        "class_name": "person",
                    },
                    {
                        "xyxy": [615.0, 180.0, 638.0, 300.0],
                        "confidence": 0.97,
                        "class_id": 0,
                        "class_name": "person",
                    },
                ],
                60: [
                    {
                        "xyxy": [620.0, 15.0, 638.0, 50.0],
                        "confidence": 0.99,
                        "class_id": 0,
                        "class_name": "person",
                    }
                ],
            }
        ),
    )


def test_main_subject_selector_persists_at_most_two_candidates_per_frame(
    db_session: Session,
    indexed_media,
    detection_weights_path: Path,
) -> None:
    detection = create_noisy_player_detection_run(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=detection_weights_path,
    )

    result = select_main_player_subjects(
        session=db_session,
        media_id=indexed_media.id,
        source_detection_run_id=str(detection["detection_run_id"]),
        max_frames=3,
    )

    assert result["ok"] is True
    assert result["observations"]["total"] == 3
    assert result["observations"]["near_player_candidate"] == 2
    assert result["observations"]["far_player_candidate"] == 1
    assert result["warnings"]["not_identity_truth"] is True

    candidates = db_session.scalars(
        select(Observation)
        .where(
            Observation.run_id == result["main_subject_run_id"],
            Observation.observation_type == "main_player_subject_candidate",
        )
        .order_by(Observation.frame_start, Observation.confidence.desc())
    ).all()
    assert len(candidates) == 3
    by_frame: dict[int, list[Observation]] = {}
    for candidate in candidates:
        by_frame.setdefault(int(candidate.frame_start), []).append(candidate)
        assert candidate.observation_family == "tracking"
        assert candidate.payload_jsonb["candidate_subject_only"] is True
        assert candidate.payload_jsonb["not_identity_truth"] is True
        assert candidate.payload_jsonb["observation_only"] is True
        assert candidate.payload_jsonb["no_adjudication"] is True
        assert candidate.payload_jsonb["source_detection_observation_id"]

    assert {frame: len(rows) for frame, rows in by_frame.items()} == {0: 2, 30: 1}

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id.in_([candidate.id for candidate in candidates])
        )
    ).all()
    assert len(lineage) == 3
    assert {row.relationship_type for row in lineage} == {
        "main_subject_candidate_from_player_detection"
    }


def test_real_pose_can_consume_main_subject_run_and_preserve_candidate_lineage(
    db_session: Session,
    indexed_media,
    detection_weights_path: Path,
    pose_weights_path: Path,
) -> None:
    detection = create_noisy_player_detection_run(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=detection_weights_path,
    )
    subject_result = select_main_player_subjects(
        session=db_session,
        media_id=indexed_media.id,
        source_detection_run_id=str(detection["detection_run_id"]),
        max_frames=3,
    )
    assert subject_result["observations"]["total"] == 3

    pose_result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(pose_weights_path),
        source_detection_run_id=str(detection["detection_run_id"]),
        source_subject_run_id=str(subject_result["main_subject_run_id"]),
        model_name="test-real-pose",
        model_version="subject-filter-test",
        device="cpu",
        every_n_frames=1,
        max_frames=3,
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_ok,
        pose_result_provider=FakePoseResultProvider(),
    )

    assert pose_result["ok"] is True
    assert pose_result["source_subject_run_id"] == subject_result["main_subject_run_id"]
    assert pose_result["observations"] == {"player_pose_observation": 3, "total": 3}
    assert pose_result["summary"]["source_subject_filter"] == "main_tennis_subject_filter_v0"

    poses = db_session.scalars(select(PoseObservation)).all()
    assert len(poses) == 3
    assert {
        pose.association_method for pose in poses
    } == {"main_tennis_subject_filter_v0_crop_from_player_detection"}
    overlay_item = pose_overlay_item_from_row(poses[0])
    assert overlay_item["subject_context"]["candidate_subject_only"] is True
    assert overlay_item["subject_context"]["not_identity_truth"] is True
    assert overlay_item["subject_context"]["subject_candidate_observation_id"]
    assert overlay_item["subject_role_candidate"] in {
        "near_player_candidate",
        "far_player_candidate",
    }
    timeline_item = pose_timeline_item_from_row(poses[0])
    assert timeline_item is not None
    assert timeline_item["candidate_subject_only"] is True

    pose_observations = db_session.scalars(
        select(Observation).where(Observation.observation_type == "player_pose_observation")
    ).all()
    for observation in pose_observations:
        assert observation.payload_jsonb["subject_candidate_observation_id"]
        assert observation.payload_jsonb["candidate_subject_only"] is True
        assert observation.payload_jsonb["not_identity_truth"] is True

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id.in_(
                [observation.id for observation in pose_observations]
            )
        )
    ).all()
    assert len(lineage) == 6
    assert {row.relationship_type for row in lineage} == {
        "pose_from_subject_detection_candidate",
        "pose_from_main_subject_candidate",
    }


def test_real_pose_broad_detection_source_still_works_without_subject_run(
    db_session: Session,
    indexed_media,
    detection_weights_path: Path,
    pose_weights_path: Path,
) -> None:
    detection = create_noisy_player_detection_run(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=detection_weights_path,
    )

    pose_result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(pose_weights_path),
        source_detection_run_id=str(detection["detection_run_id"]),
        model_name="test-real-pose",
        model_version="broad-source-test",
        device="cpu",
        every_n_frames=1,
        max_frames=7,
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_ok,
        pose_result_provider=FakePoseResultProvider(),
    )

    assert pose_result["ok"] is True
    assert pose_result["source_subject_run_id"] is None
    assert pose_result["observations"]["player_pose_observation"] == 7
    assert db_session.scalars(select(PoseObservation)).first().association_method == (
        "crop_from_player_detection"
    )
