from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.api.routers.viewer import build_viewer_run_payload
from apps.worker.services.detection_adapter import run_detection_adapter


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


def test_detection_overlay_payload_contract_contains_scaled_bbox_inputs(
    db_session: Session,
    tmp_path,
) -> None:
    video = tmp_path / "overlay-sample.mp4"
    video.write_bytes(b"tom-v3-detection-overlay")
    media = index_media_file(
        session=db_session,
        source_path=video,
        copy_to_storage=True,
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )
    result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="overlay-contract-detection-run",
        frame_sample_rate=30,
        max_frames=2,
    )

    payload = build_viewer_run_payload(db_session, result["run_id"])

    assert payload is not None
    assert payload["media"]["width"] == 640
    assert payload["media"]["height"] == 360

    detections = [
        observation
        for observation in payload["observations"]
        if observation["observation_type"] in {"ball_detection", "player_detection"}
    ]
    assert len(detections) == 6

    for observation in detections:
        assert observation["coordinate_space"] == "image_pixels"
        assert observation["frame_start"] == observation["frame_end"]
        assert observation["timestamp_start_ms"] == frame_to_timestamp_ms(
            30.0,
            observation["frame_start"],
        )
        assert observation["payload_jsonb"]["frame_time_owner"] == "media_indexing"
        assert observation["atomic"]["payload_jsonb"]["frame_time_owner"] == "media_indexing"

        bbox = observation["atomic"]["payload_jsonb"]["bbox"]
        assert {"x", "y", "width", "height"}.issubset(bbox)
        assert bbox["width"] > 0
        assert bbox["height"] > 0

        if observation["observation_type"] == "ball_detection":
            assert observation["payload_jsonb"]["label"] == "ball"
        else:
            assert observation["payload_jsonb"]["label"] in {"near_player", "far_player"}
