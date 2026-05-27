from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.skeletons import COCO17_KEYPOINT_NAMES
from tom_v3_storage.db_models import (
    AtomicObservation,
    Base,
    MediaAsset,
    Observation,
    PoseObservation,
    ProcessingRun,
    Tracklet,
    TrackPoint,
)

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.services.replay import (
    current_time_seconds_to_frame,
    frame_to_replay_timestamp_ms,
    timestamp_ms_to_replay_frame,
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


def test_replay_frame_time_mapping_clamps_to_media_range() -> None:
    media = MediaAsset(
        source_uri="file:///tmp/sample.mp4",
        duration_ms=2000,
        frame_count=60,
        fps=30.0,
        width=640,
        height=360,
    )

    assert timestamp_ms_to_replay_frame(media, -100) == 0
    assert timestamp_ms_to_replay_frame(media, 1500) == 45
    assert timestamp_ms_to_replay_frame(media, 5000) == 59
    assert current_time_seconds_to_frame(media, 1.5) == 45

    assert frame_to_replay_timestamp_ms(media, -10) == 0
    assert frame_to_replay_timestamp_ms(media, 45) == 1500
    assert frame_to_replay_timestamp_ms(media, 5000) == 1967


def test_replay_info_returns_media_metadata_and_available_runs(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    _seed_run_with_observation(db_session, media.id, "demo-fixture-detection-run", "ball_detection")
    _seed_run_with_observation(
        db_session, media.id, "demo-candidate-tracklet-run", "track_point_candidate"
    )
    _seed_run_with_observation(
        db_session, media.id, "demo-fixture-pose-run", "player_pose_observation"
    )
    _seed_run_with_observation(db_session, media.id, "demo-fixture-gameplay-run", "view_state")

    response = client.get(f"/media/{media.id}/replay-info")

    assert response.status_code == 200
    body = response.json()
    assert body["media_id"] == media.id
    assert body["video_url"] == f"/media/{media.id}/video"
    assert body["width"] == 640
    assert body["height"] == 360
    assert body["duration_ms"] == 2000
    assert body["fps"] == 30.0
    assert body["frame_count"] == 60
    assert body["frame_time_mode"] == "indexed"
    assert body["frame_time_index"]["owner"] == "media_indexing"
    assert body["observation_only"] is True
    assert body["no_adjudication"] is True
    assert body["available_runs"]["detection"][0]["observation_count"] == 1
    assert body["available_runs"]["tracklet"][0]["run_name"] == "demo-candidate-tracklet-run"
    assert body["available_runs"]["pose"][0]["run_name"] == "demo-fixture-pose-run"
    assert body["available_runs"]["gameplay"][0]["run_name"] == "demo-fixture-gameplay-run"


def test_replay_info_returns_404_for_missing_media(client: TestClient) -> None:
    response = client.get("/media/missing-media/replay-info")
    assert response.status_code == 404


def test_media_video_endpoint_serves_local_indexed_file(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)

    response = client.get(f"/media/{media.id}/video")

    assert response.status_code == 200
    assert response.content == b"tom-v3-video"
    assert response.headers["content-type"].startswith("video/mp4")


def test_media_video_endpoint_returns_404_for_unavailable_local_file(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media = _seed_media(db_session, tmp_path / "missing.mp4")

    response = client.get(f"/media/{media.id}/video")

    assert response.status_code == 404
    assert response.json()["detail"] == "local media video file not found"


def test_replay_overlay_endpoint_returns_detection_bbox_items(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    run = _seed_run_with_observation(
        db_session,
        media.id,
        "demo-fixture-detection-run",
        "ball_detection",
        timestamp_ms=1000,
        bbox={"x": 511.0, "y": 280.0, "width": 18.0, "height": 18.0},
        confidence=0.82,
    )

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "detections",
            "detection_run_id": run.id,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["media_id"] == media.id
    assert body["coordinate_space"] == "image_pixels"
    assert body["video_width"] == 640
    assert body["video_height"] == 360
    assert body["tracklets"] == []
    assert body["poses"] == []
    assert body["observation_only"] is True
    assert body["no_adjudication"] is True
    assert body["detections"] == [
        {
            "overlay_type": "detection_bbox",
            "observation_id": body["detections"][0]["observation_id"],
            "run_id": run.id,
            "frame_number": 30,
            "timestamp_ms": 1000,
            "observation_type": "ball_detection",
            "label": "ball",
            "confidence": 0.82,
            "bbox": {"x": 511.0, "y": 280.0, "w": 18.0, "h": 18.0},
            "source_language": "detection observation",
            "source_runtime": "fixture",
            "coordinate_space": "image_pixels",
        }
    ]


def test_replay_overlay_endpoint_filters_by_detection_run_id(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    included = _seed_run_with_observation(
        db_session,
        media.id,
        "included-detection-run",
        "ball_detection",
        timestamp_ms=1000,
    )
    _seed_run_with_observation(
        db_session,
        media.id,
        "excluded-detection-run",
        "player_detection",
        timestamp_ms=1000,
    )

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "detections",
            "detection_run_id": included.id,
        },
    )

    assert response.status_code == 200
    detections = response.json()["detections"]
    assert len(detections) == 1
    assert detections[0]["run_id"] == included.id
    assert detections[0]["observation_type"] == "ball_detection"


def test_replay_overlay_endpoint_filters_by_min_confidence(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    run = _seed_run_with_observation(
        db_session,
        media.id,
        "demo-fixture-detection-run",
        "ball_detection",
        confidence=0.4,
    )
    _seed_detection_observation(
        db_session,
        media_id=media.id,
        run_id=run.id,
        observation_type="player_detection",
        confidence=0.9,
        timestamp_ms=1000,
        bbox=[50.0, 60.0, 70.0, 80.0],
    )

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "detections",
            "min_confidence": 0.8,
        },
    )

    assert response.status_code == 200
    detections = response.json()["detections"]
    assert len(detections) == 1
    assert detections[0]["observation_type"] == "player_detection"
    assert detections[0]["bbox"] == {"x": 50.0, "y": 60.0, "w": 70.0, "h": 80.0}


def test_replay_overlay_endpoint_returns_empty_detections_for_empty_window(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    _seed_run_with_observation(
        db_session,
        media.id,
        "demo-fixture-detection-run",
        "ball_detection",
        timestamp_ms=1000,
    )

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 3000,
            "end_ms": 4000,
            "layers": "detections",
        },
    )

    assert response.status_code == 200
    assert response.json()["detections"] == []


def test_replay_overlay_endpoint_returns_tracklet_candidate_items(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    run = _seed_tracklet_run(db_session, media.id)

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "tracklets",
            "tracklet_run_id": run.id,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["detections"] == []
    assert body["poses"] == []
    assert len(body["tracklets"]) == 1
    tracklet = body["tracklets"][0]
    assert tracklet["overlay_type"] == "tracklet_candidate"
    assert tracklet["run_id"] == run.id
    assert tracklet["track_type"] == "ball"
    assert tracklet["track_status"] == "candidate"
    assert tracklet["identity_status"] == "unverified"
    assert tracklet["source_language"] == "tracklet candidate"
    assert [point["timestamp_ms"] for point in tracklet["points"]] == [0, 1000]
    assert tracklet["points"][0]["bbox"] == {"x": 10.0, "y": 20.0, "w": 12.0, "h": 12.0}
    assert body["observation_only"] is True
    assert body["no_adjudication"] is True


def test_replay_overlay_endpoint_filters_by_tracklet_run_id(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    included = _seed_tracklet_run(db_session, media.id, run_name="included-tracklet-run")
    _seed_tracklet_run(db_session, media.id, run_name="excluded-tracklet-run", frame_offset=10)

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "tracklets",
            "tracklet_run_id": included.id,
        },
    )

    assert response.status_code == 200
    tracklets = response.json()["tracklets"]
    assert len(tracklets) == 1
    assert tracklets[0]["run_id"] == included.id


def test_replay_overlay_endpoint_returns_pose_keypoint_items(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    run = _seed_pose_run(db_session, media.id)

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "pose",
            "pose_run_id": run.id,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["detections"] == []
    assert body["tracklets"] == []
    assert len(body["poses"]) == 1
    pose = body["poses"][0]
    assert pose["overlay_type"] == "pose_skeleton"
    assert pose["run_id"] == run.id
    assert pose["skeleton_format"] == "coco17"
    assert pose["skeleton_version"] == "v1"
    assert pose["pose_confidence"] == 0.71
    assert pose["bbox"] == {"x": 100.0, "y": 40.0, "w": 80.0, "h": 210.0, "confidence": 0.8}
    assert len(pose["keypoints"]) == 17
    assert pose["keypoints"][0]["name"] == "nose"
    assert pose["keypoints"][0]["present"] is True
    assert pose["keypoints"][3]["present"] is False
    assert ["left_shoulder", "right_shoulder"] in pose["edges"]
    assert pose["subject_context"]["association_status"] == "candidate"
    assert pose["subject_context"]["association_method"] == "crop_from_player_detection"
    assert pose["source_language"] == "pose keypoint evidence"


def test_replay_overlay_endpoint_filters_by_pose_run_id_and_confidence(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    included = _seed_pose_run(
        db_session,
        media.id,
        run_name="included-pose-run",
        pose_confidence=0.9,
    )
    _seed_pose_run(
        db_session,
        media.id,
        run_name="excluded-pose-run",
        pose_confidence=0.4,
    )

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "pose",
            "pose_run_id": included.id,
            "min_pose_confidence": 0.8,
        },
    )

    assert response.status_code == 200
    poses = response.json()["poses"]
    assert len(poses) == 1
    assert poses[0]["run_id"] == included.id
    assert poses[0]["pose_confidence"] == 0.9


def test_replay_overlay_endpoint_returns_empty_tracklets_and_poses_for_empty_window(
    client: TestClient,
    db_session: Session,
    tmp_path,
) -> None:
    media_path = tmp_path / "sample.mp4"
    media_path.write_bytes(b"tom-v3-video")
    media = _seed_media(db_session, media_path)
    _seed_tracklet_run(db_session, media.id)
    _seed_pose_run(db_session, media.id)

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": media.id,
            "start_ms": 3000,
            "end_ms": 4000,
            "layers": "tracklets,pose",
        },
    )

    assert response.status_code == 200
    assert response.json()["tracklets"] == []
    assert response.json()["poses"] == []


def test_replay_overlay_endpoint_returns_404_for_missing_media(client: TestClient) -> None:
    response = client.get(
        "/replay/overlays",
        params={"media_id": "missing-media", "start_ms": 0, "end_ms": 2000},
    )
    assert response.status_code == 404


def test_replay_overlay_endpoint_rejects_invalid_time_window(client: TestClient) -> None:
    response = client.get(
        "/replay/overlays",
        params={"media_id": "media", "start_ms": 2000, "end_ms": 1000},
    )
    assert response.status_code == 400


def _seed_media(session: Session, media_path) -> MediaAsset:
    media = MediaAsset(
        source_uri=media_path.as_uri(),
        media_type="video",
        duration_ms=2000,
        frame_count=60,
        fps=30.0,
        width=640,
        height=360,
        metadata_jsonb={
            "stored_uri": media_path.as_uri(),
            "stored_path": str(media_path),
            "frame_time_index": {
                "owner": "media_indexing",
                "mapping": "constant_fps",
                "fps": 30.0,
                "frame_count": 60,
            },
        },
    )
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


def _seed_run_with_observation(
    session: Session,
    media_id: str,
    run_name: str,
    observation_type: str,
    timestamp_ms: int = 0,
    bbox: dict[str, float] | list[float] | None = None,
    confidence: float = 0.8,
) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        metadata_jsonb={"tom_v3_demo": True},
    )
    session.add(run)
    session.flush()
    _seed_detection_observation(
        session,
        media_id=media_id,
        run_id=run.id,
        observation_type=observation_type,
        timestamp_ms=timestamp_ms,
        bbox=bbox,
        confidence=confidence,
    )
    session.commit()
    session.refresh(run)
    return run


def _seed_tracklet_run(
    session: Session,
    media_id: str,
    run_name: str = "demo-candidate-tracklet-run",
    frame_offset: int = 0,
) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        metadata_jsonb={"tom_v3_demo": True},
    )
    session.add(run)
    session.flush()
    tracklet_observation = Observation(
        media_id=media_id,
        run_id=run.id,
        observation_family="tracklet",
        observation_type="ball_tracklet_candidate",
        granularity="tracklet",
        frame_start=frame_offset,
        frame_end=frame_offset + 30,
        timestamp_start_ms=0,
        timestamp_end_ms=1000,
        confidence=0.82,
        coordinate_space="image_pixels",
        payload_jsonb={"track_status": "candidate", "identity_status": "unverified"},
    )
    session.add(tracklet_observation)
    session.flush()
    tracklet = Tracklet(
        media_id=media_id,
        run_id=run.id,
        track_family="ball",
        subject_ref="ball",
        frame_start=frame_offset,
        frame_end=frame_offset + 30,
        confidence=0.82,
        observation_id=tracklet_observation.id,
        metadata_jsonb={"track_status": "candidate", "identity_status": "unverified"},
    )
    session.add(tracklet)
    session.flush()
    for index, (frame_number, timestamp_ms, x, y) in enumerate(
        [
            (frame_offset, 0, 16.0, 26.0),
            (frame_offset + 30, 1000, 40.0, 52.0),
        ]
    ):
        point_observation = Observation(
            media_id=media_id,
            run_id=run.id,
            observation_family="tracklet",
            observation_type="track_point_candidate",
            granularity="frame",
            frame_start=frame_number,
            frame_end=frame_number,
            timestamp_start_ms=timestamp_ms,
            timestamp_end_ms=timestamp_ms,
            confidence=0.82,
            coordinate_space="image_pixels",
            payload_jsonb={"track_status": "candidate", "identity_status": "unverified"},
        )
        session.add(point_observation)
        session.flush()
        session.add(
            TrackPoint(
                tracklet_id=tracklet.id,
                observation_id=point_observation.id,
                frame_number=frame_number,
                timestamp_ms=timestamp_ms,
                x=x,
                y=y,
                width=12.0,
                height=12.0,
                confidence=0.82,
                payload_jsonb={
                    "source_detection_observation_id": f"source-detection-{index}",
                    "bbox": {"x": x - 6.0, "y": y - 6.0, "width": 12.0, "height": 12.0},
                    "track_status": "candidate",
                    "identity_status": "unverified",
                },
            )
        )
    session.commit()
    session.refresh(run)
    return run


def _seed_pose_run(
    session: Session,
    media_id: str,
    run_name: str = "demo-fixture-pose-run",
    pose_confidence: float = 0.71,
) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        metadata_jsonb={"tom_v3_demo": True},
    )
    session.add(run)
    session.flush()
    observation = Observation(
        media_id=media_id,
        run_id=run.id,
        observation_family="pose",
        observation_type="player_pose_observation",
        granularity="frame",
        frame_start=30,
        frame_end=30,
        timestamp_start_ms=1000,
        timestamp_end_ms=1000,
        confidence=pose_confidence,
        coordinate_space="image_pixels",
        payload_jsonb={"source_runtime": "fixture_pose", "normalization_only": True},
    )
    session.add(observation)
    session.flush()
    keypoints = _pose_keypoints()
    session.add(
        PoseObservation(
            observation_id=observation.id,
            media_id=media_id,
            run_id=run.id,
            frame_number=30,
            timestamp_ms=1000,
            skeleton_format="coco17",
            skeleton_version="v1",
            keypoint_schema_jsonb={},
            keypoints_jsonb=keypoints,
            keypoint_count=17,
            keypoints_present_count=3,
            keypoints_missing_count=14,
            mean_keypoint_confidence=0.8,
            min_keypoint_confidence=0.7,
            max_keypoint_confidence=0.9,
            pose_confidence=pose_confidence,
            bbox_x=100.0,
            bbox_y=40.0,
            bbox_w=80.0,
            bbox_h=210.0,
            bbox_confidence=0.8,
            subject_ref_type="player_detection",
            subject_detection_observation_id="source-player-detection-id",
            association_status="candidate",
            association_method="crop_from_player_detection",
            association_confidence=0.8,
            frame_time_owner="media_indexing",
            raw_model_payload_jsonb={},
            metadata_jsonb={"normalization_only": True},
        )
    )
    session.commit()
    session.refresh(run)
    return run


def _pose_keypoints() -> list[dict[str, object]]:
    present = {
        0: (120.0, 60.0, 0.9),
        5: (110.0, 120.0, 0.8),
        6: (155.0, 122.0, 0.7),
    }
    keypoints = []
    for index, name in enumerate(COCO17_KEYPOINT_NAMES):
        if index in present:
            x, y, confidence = present[index]
            keypoints.append(
                {
                    "index": index,
                    "name": name,
                    "x": x,
                    "y": y,
                    "x_norm": x / 640.0,
                    "y_norm": y / 360.0,
                    "confidence": confidence,
                    "present": True,
                    "visibility": None,
                }
            )
        else:
            keypoints.append(
                {
                    "index": index,
                    "name": name,
                    "x": None,
                    "y": None,
                    "x_norm": None,
                    "y_norm": None,
                    "confidence": None,
                    "present": False,
                    "visibility": None,
                }
            )
    return keypoints


def _seed_detection_observation(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    observation_type: str,
    timestamp_ms: int = 0,
    bbox: dict[str, float] | list[float] | None = None,
    confidence: float = 0.8,
) -> Observation:
    frame_number = round(timestamp_ms / 1000 * 30)
    label = observation_type.replace("_detection", "")
    bbox_payload = bbox or {"x": 10.0, "y": 20.0, "width": 30.0, "height": 40.0}
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family=_family_for_type(observation_type),
        observation_type=observation_type,
        granularity="frame",
        frame_start=frame_number,
        frame_end=frame_number,
        timestamp_start_ms=timestamp_ms,
        timestamp_end_ms=timestamp_ms,
        confidence=confidence,
        coordinate_space="image_pixels",
        payload_jsonb={"source_runtime": "fixture", "label": label, "bbox": bbox_payload},
    )
    session.add(observation)
    session.flush()
    if observation_type in {"ball_detection", "player_detection"}:
        session.add(
            AtomicObservation(
                observation_id=observation.id,
                atomic_kind=observation_type,
                payload_jsonb={
                    "source_runtime": "fixture",
                    "bbox": bbox_payload,
                    "detector": {"label": label},
                },
            )
        )
    session.commit()
    session.refresh(observation)
    return observation


def _family_for_type(observation_type: str) -> str:
    if observation_type == "view_state":
        return "gameplay"
    if observation_type == "player_pose_observation":
        return "pose"
    if observation_type in {"ball_detection", "player_detection"}:
        return "atomic"
    if observation_type in {
        "track_point_candidate",
        "ball_tracklet_candidate",
        "player_tracklet_candidate",
    }:
        return "tracklet"
    return "detection"
