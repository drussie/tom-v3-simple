from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.pose_inference import FakePoseResultProvider
from tom_v3_model_adapters.yolo_inference import FakeYoloResultProvider
from tom_v3_storage.db_models import (
    Base,
    ModelRegistry,
    Observation,
    ObservationLineage,
    PoseObservation,
    ProcessingRun,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.db import get_session
from apps.api.main import create_app
from apps.worker.cli import _handle_run_real_pose
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
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_session() -> Generator[Session, None, None]:
        yield db_session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def indexed_media(db_session: Session, tmp_path: Path):
    video = tmp_path / "real-pose-replay.mp4"
    video.write_bytes(b"tom-v3-real-pose-replay")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="real pose replay test clip",
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


def runtime_missing(**kwargs):
    return {
        "status": "unavailable",
        "requested_device": kwargs.get("requested_device", "auto"),
        "resolved_device": None,
        "ultralytics_available": False,
        "torch_available": False,
        "opencv_available": False,
        "missing_packages": ["ultralytics", "torch", "opencv-python-headless"],
    }


def create_real_detection_run(
    *,
    session: Session,
    media_id: str,
    weights_path: Path,
) -> dict[str, object]:
    return run_real_detection_replay(
        session=session,
        media_id=media_id,
        weights_path=str(weights_path),
        model_name="test-real-yolo",
        model_version="7d-test",
        device="cpu",
        every_n_frames=30,
        max_frames=1,
        allowed_roots=[str(weights_path.parent)],
        probe_runtime=runtime_ok,
        yolo_result_provider=FakeYoloResultProvider(
            boxes_by_frame={
                0: [
                    {
                        "xyxy": [250.0, 50.0, 330.0, 330.0],
                        "confidence": 0.88,
                        "class_id": 0,
                        "class_name": "person",
                    }
                ]
            }
        ),
    )


def test_plan_only_returns_real_pose_summary(db_session: Session) -> None:
    result = run_real_pose_replay(
        session=db_session,
        media_id="media-1",
        weights_path="model_assets/pose/local.pt",
        source_detection_run_id="detection-1",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert result["plan"]["mode"] == "crop_from_player_detection"
    assert result["plan"]["sampling"]["frame_time_owner"] == "media_indexing"
    assert "run-real-pose" in result["plan"]["command"]
    assert result["warnings"]["pose_keypoints_not_movement_interpretation"] is True


def test_missing_media_returns_clean_error(db_session: Session, pose_weights_path: Path) -> None:
    result = run_real_pose_replay(
        session=db_session,
        media_id="missing-media",
        weights_path=str(pose_weights_path),
        source_detection_run_id="detection-1",
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_ok,
    )

    assert result["ok"] is False
    assert result["status"] == "missing_media"
    assert "media asset not found" in result["message"]


def test_missing_source_detection_run_returns_clean_error(
    db_session: Session,
    indexed_media,
    pose_weights_path: Path,
) -> None:
    result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(pose_weights_path),
        source_detection_run_id="missing-detection-run",
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_ok,
    )

    assert result["ok"] is False
    assert result["status"] == "missing_source_detection_run"
    assert "source detection run not found" in result["message"]
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_missing_weights_returns_clean_error(db_session: Session, indexed_media) -> None:
    result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path="/tmp/tom-v3-missing-pose.pt",
        source_detection_run_id="detection-1",
        probe_runtime=runtime_ok,
    )

    assert result["ok"] is False
    assert result["status"] == "missing"
    assert "weights file does not exist" in result["message"]
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_runtime_unavailable_returns_clean_error(
    db_session: Session,
    indexed_media,
    pose_weights_path: Path,
) -> None:
    result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(pose_weights_path),
        source_detection_run_id="detection-1",
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_missing,
    )

    assert result["ok"] is False
    assert result["status"] == "pose_runtime_unavailable"
    assert result["warnings"]["no_fixture_fallback"] is True
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_fake_real_pose_persists_pose_lineage_and_replay_payloads(
    db_session: Session,
    client: TestClient,
    indexed_media,
    detection_weights_path: Path,
    pose_weights_path: Path,
) -> None:
    detection = create_real_detection_run(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=detection_weights_path,
    )
    assert detection["ok"] is True

    result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(pose_weights_path),
        source_detection_run_id=str(detection["detection_run_id"]),
        model_name="test-real-pose",
        model_version="7d-test",
        device="cpu",
        every_n_frames=1,
        max_frames=1,
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_ok,
        pose_result_provider=FakePoseResultProvider(),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["message"] == "real pose replay run complete"
    assert result["media_id"] == indexed_media.id
    assert result["source_detection_run_id"] == detection["detection_run_id"]
    assert result["observations"] == {"player_pose_observation": 1, "total": 1}
    assert result["summary"]["mode"] == "crop_from_player_detection"
    assert result["summary"]["frames_processed"] == 1
    assert result["warnings"]["model_output_not_truth"] is True
    assert result["replay_url"].endswith(
        f"/replay/{indexed_media.id}?detectionRunId={detection['detection_run_id']}"
        f"&poseRunId={result['pose_run_id']}"
    )

    run = db_session.get(ProcessingRun, result["pose_run_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    model = db_session.get(ModelRegistry, result["model_registry_id"])
    assert run is not None
    assert run.run_name == "real-pose-replay"
    assert run.run_status == "completed"
    assert run.metadata_jsonb["source_runtime"] == "ultralytics_pose"
    assert run.metadata_jsonb["real_model_output"] is True
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["mode"] == "crop_from_player_detection"
    assert runtime_config.payload_jsonb["source_runtime"] == "ultralytics_pose"
    assert model is not None
    assert model.model_family == "pose"
    assert model.metadata_jsonb["model_task"] == "pose"

    pose = db_session.scalar(select(PoseObservation))
    assert pose is not None
    assert pose.keypoint_count == 17
    assert pose.keypoints_present_count == 17
    assert pose.frame_time_owner == "media_indexing"
    assert pose.subject_ref_type == "player_detection"
    assert pose.subject_detection_observation_id is not None
    assert pose.association_status == "candidate"
    assert pose.association_method == "crop_from_player_detection"
    assert pose.metadata_jsonb["source_runtime"] == "ultralytics_pose"
    assert pose.metadata_jsonb["real_model_output"] is True
    assert pose.raw_model_payload_jsonb["real_model_output"] is True
    assert pose.crop_source == "player_detection"

    observation = db_session.get(Observation, pose.observation_id)
    assert observation is not None
    assert observation.observation_family == "pose"
    assert observation.observation_type == "player_pose_observation"
    assert observation.model_id == result["model_registry_id"]
    assert observation.runtime_config_id == result["runtime_config_id"]
    assert observation.payload_jsonb["source_runtime"] == "ultralytics_pose"
    assert observation.payload_jsonb["evidence_source"] == "real_pose_model_output"
    assert observation.payload_jsonb["real_model_output"] is True
    assert observation.payload_jsonb["model_output_not_truth"] is True

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == pose.observation_id
        )
    ).all()
    assert len(lineage) == 1
    assert lineage[0].parent_observation_id == pose.subject_detection_observation_id
    assert lineage[0].relationship_type == "pose_from_subject_detection_candidate"
    assert lineage[0].payload_jsonb["source_runtime"] == "ultralytics_pose"

    replay_info = client.get(f"/media/{indexed_media.id}/replay-info")
    assert replay_info.status_code == 200
    pose_runs = replay_info.json()["available_runs"]["pose"]
    real_pose_run = next(
        run_item for run_item in pose_runs if run_item["run_id"] == result["pose_run_id"]
    )
    assert real_pose_run["evidence_source"] == "real_pose_model_output"
    assert real_pose_run["source_label"] == "real pose model output"
    assert real_pose_run["source_runtime"] == "ultralytics_pose"
    assert real_pose_run["is_real_model_output"] is True
    assert real_pose_run["model_output_not_truth"] is True

    overlays = client.get(
        "/replay/overlays",
        params={
            "media_id": indexed_media.id,
            "start_ms": 0,
            "end_ms": 1200,
            "layers": "pose",
            "pose_run_id": result["pose_run_id"],
        },
    )
    assert overlays.status_code == 200
    pose_overlay = overlays.json()["poses"][0]
    assert pose_overlay["evidence_source"] == "real_pose_model_output"
    assert pose_overlay["source_runtime"] == "ultralytics_pose"
    assert pose_overlay["real_model_output"] is True
    assert pose_overlay["model_output_not_truth"] is True
    assert pose_overlay["model_registry_id"] == result["model_registry_id"]
    assert pose_overlay["runtime_config_id"] == result["runtime_config_id"]
    assert len([keypoint for keypoint in pose_overlay["keypoints"] if keypoint["present"]]) == 17

    timeline = client.get(
        "/replay/timeline",
        params={
            "media_id": indexed_media.id,
            "pose_run_id": result["pose_run_id"],
        },
    )
    assert timeline.status_code == 200
    lanes = {lane["lane_type"]: lane for lane in timeline.json()["lanes"]}
    pose_timeline = lanes["pose"]["items"][0]
    assert pose_timeline["display_label"].endswith("· real pose model output")
    assert pose_timeline["evidence_source"] == "real_pose_model_output"
    assert pose_timeline["real_model_output"] is True


def test_failure_does_not_silently_create_fixture_poses(
    db_session: Session,
    indexed_media,
    pose_weights_path: Path,
) -> None:
    result = run_real_pose_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(pose_weights_path),
        source_detection_run_id="missing-detection-run",
        allowed_roots=[str(pose_weights_path.parent)],
        probe_runtime=runtime_ok,
    )

    assert result["ok"] is False
    assert db_session.scalar(select(func.count()).select_from(PoseObservation)) == 0
    assert db_session.scalar(select(func.count()).select_from(ProcessingRun)) == 0


def test_cli_handler_supports_plan_only_real_pose(db_session: Session) -> None:
    result = _handle_run_real_pose(
        db_session,
        Namespace(
            media_id="media-1",
            weights="model_assets/pose/local.pt",
            source_detection_run_id="detection-1",
            model_name="local-pose",
            model_version="7d",
            required_sha256=None,
            device="cpu",
            imgsz=640,
            conf=0.25,
            iou=0.7,
            every_n_frames=1,
            frame_start=None,
            frame_end=None,
            max_frames=120,
            mode="crop_from_player_detection",
            fallback_to_full_frame=False,
            viewer_base_url="http://127.0.0.1:3000",
            allowed_roots=None,
            plan_only=True,
        ),
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "run-real-pose" in result["plan"]["command"]
