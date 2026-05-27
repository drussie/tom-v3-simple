from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.yolo_inference import FakeYoloResultProvider
from tom_v3_storage.db_models import (
    AtomicObservation,
    Base,
    Observation,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.db import get_session
from apps.api.main import create_app
from apps.worker.cli import _handle_run_real_detection
from apps.worker.services.real_detection_replay import (
    coerce_real_detection_class_map,
    run_real_detection_replay,
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
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"tom-v3-real-detection-replay")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="real detection replay test clip",
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
def weights_path(tmp_path: Path) -> Path:
    weights_root = tmp_path / "weights" / "yolo"
    weights_root.mkdir(parents=True, exist_ok=True)
    weights = weights_root / "real-detection.pt"
    weights.write_bytes(b"fake-yolo-weights-for-real-detection-replay")
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


def test_plan_only_returns_real_detection_summary(db_session: Session) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id="media-1",
        weights_path="model_assets/yolo/local.pt",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert result["plan"]["sampling"]["frame_time_owner"] == "media_indexing"
    assert "run-real-detection" in result["plan"]["command"]
    assert result["warnings"]["model_output_not_truth"] is True


def test_missing_media_returns_clean_error(db_session: Session, weights_path: Path) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id="missing-media",
        weights_path=str(weights_path),
        probe_runtime=runtime_ok,
        allowed_roots=[str(weights_path.parent)],
    )

    assert result["ok"] is False
    assert result["status"] == "missing_media"
    assert "media asset not found" in result["message"]


def test_missing_weights_returns_clean_error(db_session: Session, indexed_media) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path="/tmp/tom-v3-missing-yolo.pt",
        probe_runtime=runtime_ok,
    )

    assert result["ok"] is False
    assert result["status"] == "missing"
    assert "YOLO weights file does not exist" in result["message"]
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_runtime_unavailable_returns_clean_error(
    db_session: Session,
    indexed_media,
    weights_path: Path,
) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(weights_path),
        probe_runtime=runtime_missing,
        allowed_roots=[str(weights_path.parent)],
    )

    assert result["ok"] is False
    assert result["status"] == "yolo_runtime_unavailable"
    assert result["warnings"]["no_fixture_fallback"] is True
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_invalid_class_map_returns_clean_error(db_session: Session) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id="media-1",
        weights_path="model_assets/yolo/local.pt",
        class_map={"person": {"observation_type": "player_detection"}},
        plan_only=True,
    )

    assert result["ok"] is False
    assert result["status"] == "invalid_class_mapping"


def test_class_map_shorthand_is_coerced_to_yolo_mapping() -> None:
    mapping = coerce_real_detection_class_map(
        {
            "person": {
                "observation_type": "player_detection",
                "label": "player_unknown",
            },
            "sports ball": {
                "observation_type": "ball_detection",
                "label": "ball",
            },
        }
    )

    assert mapping["person"]["source_class_names"] == ["person"]
    assert mapping["person"]["target_label"] == "player_unknown"
    assert mapping["sports ball"]["target_observation_type"] == "ball_detection"


def test_fake_real_detection_run_persists_atomic_observations_and_replay_payloads(
    db_session: Session,
    client: TestClient,
    indexed_media,
    weights_path: Path,
) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(weights_path),
        model_name="test-real-yolo",
        model_version="7a-test",
        device="cpu",
        imgsz=640,
        conf=0.2,
        iou=0.6,
        every_n_frames=30,
        max_frames=2,
        allowed_roots=[str(weights_path.parent)],
        probe_runtime=runtime_ok,
        yolo_result_provider=FakeYoloResultProvider(
            boxes_by_frame={
                0: [
                    {
                        "xyxy": [100.0, 110.0, 112.0, 122.0],
                        "confidence": 0.91,
                        "class_id": 32,
                        "class_name": "sports ball",
                    },
                    {
                        "xyxy": [250.0, 50.0, 330.0, 330.0],
                        "confidence": 0.88,
                        "class_id": 0,
                        "class_name": "person",
                    },
                    {
                        "xyxy": [10.0, 10.0, 40.0, 40.0],
                        "confidence": 0.7,
                        "class_id": 16,
                        "class_name": "dog",
                    },
                ],
                30: [
                    {
                        "xyxy": [120.0, 125.0, 132.0, 137.0],
                        "confidence": 0.9,
                        "class_id": 32,
                        "class_name": "sports ball",
                    },
                    {
                        "xyxy": [260.0, 55.0, 340.0, 335.0],
                        "confidence": 0.86,
                        "class_id": 0,
                        "class_name": "person",
                    },
                ],
            }
        ),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["message"] == "real YOLO detection replay run complete"
    assert result["media_id"] == indexed_media.id
    assert result["observations"] == {
        "ball_detection": 2,
        "player_detection": 2,
        "total": 4,
    }
    assert result["summary"]["raw_detections"] == 5
    assert result["summary"]["accepted_detections"] == 4
    assert result["summary"]["skipped_unmapped_classes"] == 1
    assert result["summary"]["frames_processed"] == 2
    assert result["summary"]["sampled_frames"] == [0, 30]
    assert result["warnings"]["observation_only"] is True
    assert result["warnings"]["no_adjudication"] is True
    assert result["replay_url"].endswith(
        f"/replay/{indexed_media.id}?detectionRunId={result['detection_run_id']}"
    )

    run = db_session.get(ProcessingRun, result["detection_run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    assert run is not None
    assert run.run_name == "real-yolo-detection-replay"
    assert run.run_status == "completed"
    assert step is not None
    assert step.step_status == "completed"
    assert step.metadata_jsonb["diagnostics"]["skipped_unmapped_classes"] == 1
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["frame_sampling"] == {
        "mode": "every_n_frames",
        "every_n_frames": 30,
        "frame_start": None,
        "frame_end": None,
        "max_frames": 2,
    }
    assert runtime_config.payload_jsonb["class_map"]["player"]["target_label"] == (
        "player_unknown"
    )

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["detection_run_id"])
        .order_by(Observation.frame_start, Observation.observation_type)
    ).all()
    assert len(observations) == 4
    assert {observation.observation_family for observation in observations} == {"atomic"}
    assert {observation.observation_type for observation in observations} == {
        "ball_detection",
        "player_detection",
    }
    assert {observation.model_id for observation in observations} == {
        result["model_registry_id"]
    }
    assert {observation.runtime_config_id for observation in observations} == {
        result["runtime_config_id"]
    }
    assert observations[0].timestamp_start_ms == frame_to_timestamp_ms(indexed_media.fps, 0)
    assert observations[-1].timestamp_start_ms == frame_to_timestamp_ms(indexed_media.fps, 30)
    assert observations[0].payload_jsonb["real_model_output"] is True
    assert observations[0].payload_jsonb["model_output_not_truth"] is True
    assert observations[0].payload_jsonb["source_runtime"] == "ultralytics_yolo"
    assert observations[0].payload_jsonb["frame_time_owner"] == "media_indexing"
    assert observations[0].payload_jsonb["metadata"]["real_model_output"] is True

    atomic_payloads = db_session.scalars(
        select(AtomicObservation.payload_jsonb)
        .join(Observation, Observation.id == AtomicObservation.observation_id)
        .where(Observation.run_id == result["detection_run_id"])
    ).all()
    assert len(atomic_payloads) == 4
    assert all(payload["real_model_output"] is True for payload in atomic_payloads)
    assert all(payload["source_runtime"] == "ultralytics_yolo" for payload in atomic_payloads)

    replay_info = client.get(f"/media/{indexed_media.id}/replay-info")
    assert replay_info.status_code == 200
    detection_runs = replay_info.json()["available_runs"]["detection"]
    assert any(run_item["run_id"] == result["detection_run_id"] for run_item in detection_runs)

    overlays = client.get(
        "/replay/overlays",
        params={
            "media_id": indexed_media.id,
            "start_ms": 0,
            "end_ms": 1200,
            "layers": "detections",
            "detection_run_id": result["detection_run_id"],
        },
    )
    assert overlays.status_code == 200
    body = overlays.json()
    assert body["observation_only"] is True
    assert body["no_adjudication"] is True
    assert len(body["detections"]) == 4
    assert {item["source_runtime"] for item in body["detections"]} == {"ultralytics_yolo"}

    timeline = client.get(
        "/replay/timeline",
        params={
            "media_id": indexed_media.id,
            "detection_run_id": result["detection_run_id"],
        },
    )
    assert timeline.status_code == 200
    lanes = {lane["lane_type"]: lane for lane in timeline.json()["lanes"]}
    assert len(lanes["detections"]["items"]) == 4


def test_failure_does_not_silently_create_fixture_observations(
    db_session: Session,
    indexed_media,
    weights_path: Path,
) -> None:
    result = run_real_detection_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=str(weights_path),
        device="cpu",
        every_n_frames=30,
        max_frames=2,
        allowed_roots=[str(weights_path.parent)],
        probe_runtime=runtime_missing,
    )

    assert result["ok"] is False
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0
    assert db_session.scalar(select(func.count()).select_from(ProcessingRun)) == 0


def test_cli_handler_supports_plan_only_real_detection(db_session: Session) -> None:
    result = _handle_run_real_detection(
        db_session,
        Namespace(
            media_id="media-1",
            weights="model_assets/yolo/local.pt",
            model_name="local-yolo",
            model_version="7a",
            required_sha256=None,
            device="cpu",
            imgsz=640,
            conf=0.25,
            iou=0.7,
            every_n_frames=1,
            frame_start=None,
            frame_end=None,
            max_frames=120,
            class_map_json=None,
            viewer_base_url="http://127.0.0.1:3000",
            allowed_roots=None,
            output_debug_artifact=False,
            plan_only=True,
        ),
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "run-real-detection" in result["plan"]["command"]
