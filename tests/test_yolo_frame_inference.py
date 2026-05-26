from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.detection import (
    DetectionAdapterInput,
    YoloDetectionAdapter,
    YoloDetectionAdapterUnavailable,
)
from tom_v3_model_adapters.yolo_inference import (
    FakeYoloResultProvider,
    FrameInferenceInput,
    sample_frame_numbers,
)
from tom_v3_storage.db_models import (
    AtomicObservation,
    Base,
    EvidenceArtifact,
    Observation,
    ProcessingRun,
    ProcessingStep,
    Tracklet,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.routers.viewer import build_viewer_run_payload
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.yolo_model_registry import register_yolo_model


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
def sample_video(tmp_path: Path) -> str:
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"tom-v3-yolo-frame-inference")
    return str(video)


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


def indexed_media(session: Session, sample_video: str, tmp_path: Path):
    return index_media_file(
        session=session,
        source_path=sample_video,
        copy_to_storage=True,
        media_name="yolo frame inference test clip",
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )


def test_fake_yolo_result_provider_produces_frame_result_dict() -> None:
    provider = FakeYoloResultProvider()
    frame_input = FrameInferenceInput(
        frame_number=30,
        timestamp_ms=1_000,
        image=None,
        image_width=640,
        image_height=360,
        source_path="/tmp/sample.mp4",
        metadata={"frame_time_owner": "media_indexing"},
    )

    result = provider.predict_frame(frame_input)

    assert result["frame_number"] == 30
    assert result["timestamp_ms"] == 1_000
    assert len(result["boxes"]) == 2
    assert {box["class_name"] for box in result["boxes"]} == {"sports ball", "person"}


def test_sample_frame_numbers_match_fixture_policy() -> None:
    assert sample_frame_numbers(frame_count=90, frame_sample_rate=30, max_frames=2) == [0, 30]


def test_yolo_adapter_uses_normalization_to_build_detection_result() -> None:
    adapter = YoloDetectionAdapter(
        model_path="/tmp/fake-yolo.pt",
        model_registry_id="model-1",
        device="cpu",
        result_provider=FakeYoloResultProvider(),
    )
    adapter_input = DetectionAdapterInput(
        media_id="media-1",
        source_uri="file:///tmp/sample.mp4",
        local_path="/tmp/sample.mp4",
        fps=30.0,
        frame_count=90,
        duration_ms=3_000,
        width=640,
        height=360,
        runtime_config={
            "frame_sample_rate": 30,
            "max_frames": 2,
            "weights_sha256": "abc123",
            "runtime_config_id": "config-1",
        },
        frame_time_summary={"owner": "media_indexing"},
    )

    result = adapter.run(adapter_input)

    assert result.adapter_name == "yolo-compatible-ball-player-detector"
    assert result.adapter_version == "frame-inference-v0"
    assert len(result.detections) == 4
    assert {detection.label for detection in result.detections} == {"ball", "player_unknown"}
    assert result.detections[0].frame_number == 0
    assert result.detections[2].frame_number == 30
    assert result.detections[2].timestamp_ms == frame_to_timestamp_ms(30.0, 30)
    assert result.detections[0].metadata["source_runtime"] == "ultralytics_yolo"
    assert result.detections[0].metadata["model_registry_id"] == "model-1"
    assert result.detections[0].metadata["inference"]["weights_sha256"] == "abc123"


def test_yolo_adapter_missing_runtime_or_weights_fails_clearly() -> None:
    adapter_input = DetectionAdapterInput(
        media_id="media-1",
        source_uri="file:///tmp/sample.mp4",
        local_path="/tmp/sample.mp4",
        fps=30.0,
        frame_count=90,
        duration_ms=3_000,
        width=640,
        height=360,
    )

    with pytest.raises(YoloDetectionAdapterUnavailable, match="YOLO26/Ultralytics"):
        YoloDetectionAdapter(model_path="/missing/yolo.pt").run(adapter_input)


def test_mocked_yolo_adapter_run_persists_atomic_observations(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)
    weights_root = tmp_path / "weights" / "yolo"
    weights = weights_root / "mocked.pt"
    weights.parent.mkdir(parents=True, exist_ok=True)
    weights.write_bytes(b"mocked-yolo-weights")
    model_result = register_yolo_model(
        session=db_session,
        weights_path=str(weights),
        allowed_roots=[str(weights_root)],
        model_name="mocked-yolo",
        model_version="test-v0",
    )

    result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="yolo",
        run_name="mocked-yolo-detection-run",
        model_registry_id=model_result["model_registry_id"],
        device="cpu",
        image_size=640,
        confidence_threshold=0.25,
        iou_threshold=0.7,
        max_det=50,
        frame_sample_rate=30,
        max_frames=2,
        output_debug_artifact=True,
        yolo_result_provider=FakeYoloResultProvider(),
    )

    assert result["model_id"] == model_result["model_registry_id"]
    assert result["detection_count"] == 4
    assert result["counts_by_observation_type"] == {
        "ball_detection": 2,
        "player_detection": 2,
    }
    assert result["diagnostics"]["source_runtime"] == "ultralytics_yolo"
    assert result["diagnostics"]["weights_sha256"] == model_result["weights_sha256"]

    run = db_session.get(ProcessingRun, result["run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])
    assert run is not None
    assert run.run_status == "completed"
    assert step is not None
    assert step.step_status == "completed"

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["run_id"])
        .order_by(Observation.frame_start, Observation.observation_type)
    ).all()
    assert len(observations) == 4
    assert {observation.observation_family for observation in observations} == {"atomic"}
    assert {observation.observation_type for observation in observations} == {
        "ball_detection",
        "player_detection",
    }
    assert {observation.model_id for observation in observations} == {
        model_result["model_registry_id"]
    }
    assert observations[0].payload_jsonb["source_runtime"] == "ultralytics_yolo"
    assert observations[0].payload_jsonb["frame_time_owner"] == "media_indexing"
    assert observations[0].payload_jsonb["model_registry_id"] == model_result["model_registry_id"]
    assert observations[0].payload_jsonb["weights_sha256"] == model_result["weights_sha256"]
    assert observations[0].timestamp_start_ms == frame_to_timestamp_ms(media.fps, 0)
    assert observations[-1].timestamp_start_ms == frame_to_timestamp_ms(media.fps, 30)

    atomic_payloads = db_session.scalars(
        select(AtomicObservation.payload_jsonb)
        .join(Observation, Observation.id == AtomicObservation.observation_id)
        .where(Observation.run_id == result["run_id"])
    ).all()
    assert len(atomic_payloads) == 4
    assert all(payload["source_runtime"] == "ultralytics_yolo" for payload in atomic_payloads)
    assert all(payload["frame_time_owner"] == "media_indexing" for payload in atomic_payloads)

    artifacts = db_session.scalars(
        select(EvidenceArtifact).where(EvidenceArtifact.run_id == result["run_id"])
    ).all()
    assert len(artifacts) == 4
    assert all(
        artifact.metadata_jsonb["source_runtime"] == "ultralytics_yolo"
        for artifact in artifacts
    )

    assert db_session.scalar(select(func.count()).select_from(Tracklet)) == 0
    payload = build_viewer_run_payload(db_session, result["run_id"])
    assert payload is not None
    assert {
        row["observation_type"]
        for row in payload["observations"]
        if row["observation_family"] == "atomic"
    } == {"ball_detection", "player_detection"}


def test_failed_yolo_run_does_not_persist_observations(
    db_session: Session,
    sample_video: str,
    tmp_path: Path,
) -> None:
    media = indexed_media(db_session, sample_video, tmp_path)

    with pytest.raises(YoloDetectionAdapterUnavailable):
        run_detection_adapter(
            session=db_session,
            media_id=media.id,
            adapter_name="yolo",
            run_name="failed-yolo-detection-run",
            model_path=str(tmp_path / "missing.pt"),
            frame_sample_rate=30,
            max_frames=1,
        )

    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0
    failed_run = db_session.scalar(
        select(ProcessingRun).where(ProcessingRun.run_name == "failed-yolo-detection-run")
    )
    assert failed_run is not None
    assert failed_run.run_status == "failed"
    assert failed_run.metadata_jsonb["error"]
