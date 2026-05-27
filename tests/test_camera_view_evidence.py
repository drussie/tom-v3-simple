from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    CameraViewObservation,
    CourtKeypointObservation,
    HomographyCandidateObservation,
    HumanAnnotation,
    MediaAsset,
    ProjectionDiagnosticObservation,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.services.camera_view_evidence import (
    build_camera_view_evidence_bundle,
    query_camera_view_observations,
    summarize_camera_view_evidence,
)
from apps.worker.services.court_adapter import run_fixture_court_adapter


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
def indexed_media(db_session: Session, tmp_path: Path) -> MediaAsset:
    video = tmp_path / "camera-view.mp4"
    video.write_bytes(b"tom-v3-camera-view")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="camera view evidence test clip",
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
def fixture_court_run(db_session: Session, indexed_media: MediaAsset) -> dict[str, object]:
    result = run_fixture_court_adapter(
        session=db_session,
        media_id=indexed_media.id,
        frame_sample_rate=30,
        max_frames=3,
    )
    assert result["ok"] is True
    return result


def test_query_camera_view_observations_filters_fixture_rows(
    db_session: Session,
    indexed_media: MediaAsset,
    fixture_court_run: dict[str, object],
) -> None:
    response = query_camera_view_observations(
        db_session,
        filters=_filters(indexed_media.id, run_id=str(fixture_court_run["court_run_id"])),
    )

    assert response.total == 3
    assert [item.frame_number for item in response.items] == [0, 30, 60]
    assert {item.view_label for item in response.items} == {"broadcast_hardcam"}
    assert {item.camera_motion_hint for item in response.items} == {"stable"}
    assert all(item.fixture_camera_view_evidence for item in response.items)
    assert all(item.frame_time_owner == "media_indexing" for item in response.items)
    assert response.warnings["not_confirmed_camera_state"] is True

    view_filtered = query_camera_view_observations(
        db_session,
        filters=_filters(
            indexed_media.id,
            run_id=str(fixture_court_run["court_run_id"]),
            view_label="broadcast_hardcam",
        ),
    )
    assert view_filtered.total == 3

    missing_view = query_camera_view_observations(
        db_session,
        filters=_filters(
            indexed_media.id,
            run_id=str(fixture_court_run["court_run_id"]),
            view_label="side_view",
        ),
    )
    assert missing_view.total == 0


def test_query_camera_view_observations_filters_by_time_frame_confidence_and_pagination(
    db_session: Session,
    indexed_media: MediaAsset,
    fixture_court_run: dict[str, object],
) -> None:
    filtered = query_camera_view_observations(
        db_session,
        filters=_filters(
            indexed_media.id,
            run_id=str(fixture_court_run["court_run_id"]),
            start_ms=1000,
            end_ms=2000,
            frame_start=30,
            frame_end=60,
            camera_motion_hint="stable",
            min_view_confidence=0.75,
            limit=1,
            offset=1,
        ),
    )

    assert filtered.total == 2
    assert len(filtered.items) == 1
    assert filtered.items[0].frame_number == 60

    high_confidence = query_camera_view_observations(
        db_session,
        filters=_filters(
            indexed_media.id,
            run_id=str(fixture_court_run["court_run_id"]),
            min_view_confidence=0.85,
        ),
    )
    assert high_confidence.total == 0


def test_camera_view_summary_counts_labels_motion_and_metrics(
    db_session: Session,
    indexed_media: MediaAsset,
    fixture_court_run: dict[str, object],
) -> None:
    summary = summarize_camera_view_evidence(
        db_session,
        filters=_filters(indexed_media.id, run_id=str(fixture_court_run["court_run_id"])),
    )

    assert summary.camera_view_observation_count == 3
    assert summary.labels == {"broadcast_hardcam": 3}
    assert summary.motion_hints == {"stable": 3}
    assert summary.time_range == {"start_ms": 0, "end_ms": 2000}
    assert summary.frame_range == {"start": 0, "end": 60}
    assert summary.mean_view_confidence == 0.8
    assert summary.mean_stability_score == 0.8
    assert summary.max_cut_likelihood == 0.05
    assert summary.homography_context["candidate_context_only"] is True
    assert summary.homography_context["observed_useful_view_count"] == 3
    assert summary.homography_context["observed_unstable_count"] == 0
    assert summary.warnings["no_homography_decision"] is True


def test_camera_view_bundle_returns_context_and_annotations(
    db_session: Session,
    indexed_media: MediaAsset,
    fixture_court_run: dict[str, object],
) -> None:
    camera = db_session.scalar(
        select(CameraViewObservation)
        .where(CameraViewObservation.run_id == str(fixture_court_run["court_run_id"]))
        .order_by(CameraViewObservation.frame_number)
    )
    assert camera is not None
    annotation = HumanAnnotation(
        media_id=indexed_media.id,
        observation_id=camera.observation_id,
        frame_start=camera.frame_start,
        frame_end=camera.frame_end,
        timestamp_start_ms=camera.timestamp_start_ms,
        timestamp_end_ms=camera.timestamp_end_ms,
        annotation_type="camera_view_review",
        payload_jsonb={"annotation_label": "uncertain_camera_view"},
        created_by="test",
    )
    db_session.add(annotation)
    db_session.commit()

    bundle = build_camera_view_evidence_bundle(db_session, camera.observation_id)

    assert bundle is not None
    assert bundle["camera_view_observation"]["observation"]["id"] == camera.observation_id
    assert bundle["camera_view_observation"]["camera_view"]["view_label"] == "broadcast_hardcam"
    assert bundle["media"]["id"] == indexed_media.id
    assert bundle["run"]["id"] == fixture_court_run["court_run_id"]
    assert bundle["runtime_config"]["id"] == fixture_court_run["runtime_config_id"]
    assert bundle["model_registry"]["id"] == fixture_court_run["model_registry_id"]
    assert bundle["annotation_summary"]["count"] == 1
    assert bundle["summary"]["camera_view_evidence_only"] is True
    assert bundle["summary"]["no_homography_decision"] is True
    assert bundle["warnings"]["no_tennis_event_interpretation"] is True


def test_camera_view_api_endpoints(
    client: TestClient,
    indexed_media: MediaAsset,
    fixture_court_run: dict[str, object],
) -> None:
    run_id = str(fixture_court_run["court_run_id"])

    query_response = client.get(
        "/court/camera-view",
        params={"media_id": indexed_media.id, "run_id": run_id, "view_label": "broadcast_hardcam"},
    )
    assert query_response.status_code == 200
    query_body = query_response.json()
    assert query_body["total"] == 3
    camera_observation_id = query_body["items"][0]["observation_id"]
    assert query_body["items"][0]["fixture_camera_view_evidence"] is True

    summary_response = client.get(
        "/court/camera-view/summary",
        params={"media_id": indexed_media.id, "run_id": run_id},
    )
    assert summary_response.status_code == 200
    summary_body = summary_response.json()
    assert summary_body["camera_view_observation_count"] == 3
    assert summary_body["warnings"]["not_confirmed_camera_state"] is True

    bundle_response = client.get(f"/court/camera-view/{camera_observation_id}/bundle")
    assert bundle_response.status_code == 200
    bundle_body = bundle_response.json()
    assert bundle_body["camera_view_observation"]["camera_view"]["view_label"] == (
        "broadcast_hardcam"
    )


def test_camera_view_bundle_missing_and_wrong_type_are_clean_api_errors(
    client: TestClient,
    fixture_court_run: dict[str, object],
    db_session: Session,
) -> None:
    missing_media = client.get("/court/camera-view", params={"media_id": "missing-media"})
    assert missing_media.status_code == 404
    assert "media asset not found" in missing_media.json()["detail"]

    missing = client.get("/court/camera-view/missing-observation/bundle")
    assert missing.status_code == 404

    keypoint = db_session.scalar(
        select(CourtKeypointObservation)
        .where(CourtKeypointObservation.run_id == str(fixture_court_run["court_run_id"]))
        .order_by(CourtKeypointObservation.frame_number)
    )
    assert keypoint is not None

    wrong_type = client.get(f"/court/camera-view/{keypoint.observation_id}/bundle")
    assert wrong_type.status_code == 400
    assert "not a camera_view_observation" in wrong_type.json()["detail"]


def test_camera_view_read_layer_does_not_create_homography_or_projection_rows(
    db_session: Session,
    indexed_media: MediaAsset,
    fixture_court_run: dict[str, object],
) -> None:
    query_camera_view_observations(
        db_session,
        filters=_filters(indexed_media.id, run_id=str(fixture_court_run["court_run_id"])),
    )
    summarize_camera_view_evidence(
        db_session,
        filters=_filters(indexed_media.id, run_id=str(fixture_court_run["court_run_id"])),
    )

    assert db_session.scalar(select(func.count()).select_from(HomographyCandidateObservation)) == 0
    assert db_session.scalar(select(func.count()).select_from(ProjectionDiagnosticObservation)) == 0


def _filters(media_id: str, **kwargs: object):
    from tom_v3_schema.court import CameraViewQueryFilters

    return CameraViewQueryFilters(media_id=media_id, **kwargs)
