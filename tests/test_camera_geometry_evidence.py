from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    CameraGeometryEvidence,
    MediaAsset,
    Observation,
    ProcessingRun,
)

from apps.api.db import get_session
from apps.api.main import create_app
from apps.worker.services.camera_geometry import declare_camera_geometry
from apps.worker.services.point_candidate_evaluation import evaluate_point_candidates
from apps.worker.services.point_evidence_snapshot import build_point_evidence_snapshot


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


def test_declare_camera_geometry_persists_declared_evidence(db_session: Session) -> None:
    media = _seed_media(db_session)
    court_run = _seed_run(db_session, media.id, "court")
    court_projection_run = _seed_run(db_session, media.id, "court-projection")
    homography_run = _seed_run(db_session, media.id, "homography")
    db_session.commit()

    result = declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        court_run_id=court_run.id,
        court_projection_run_id=court_projection_run.id,
        homography_run_id=homography_run.id,
    )

    assert result["ok"] is True
    assert result["geometry_type"] == "camera_geometry_evidence"
    assert result["geometry_version"] == "v0"
    assert result["geometry_status"] == "declared"
    assert result["camera_model"] == "homography_backed_court_plane"
    assert result["court_model"] == "itf_standard_tennis_court"
    assert result["court_dimensions"]["court_length"] == 23.77
    assert result["court_dimensions"]["singles_width"] == 8.23
    assert result["world_coordinate_system"]["court_z"] == "meters_above_declared_court_plane"
    assert result["capabilities"]["true_3d_reconstruction_available"] is False
    assert result["capabilities"]["3d_ball_trajectory_available"] is False
    assert result["warnings"]["not_3d_truth"] is True
    assert result["warnings"]["does_not_change_event_candidates"] is True

    row = db_session.get(CameraGeometryEvidence, result["camera_geometry_id"])
    assert row is not None
    assert row.geometry_run_id == result["geometry_run_id"]
    assert row.court_projection_run_id == court_projection_run.id


def test_declare_camera_geometry_rejects_truth_like_status(db_session: Session) -> None:
    media = _seed_media(db_session)
    db_session.commit()

    result = declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        geometry_status="true_camera_pose",
    )

    assert result["ok"] is False
    assert result["status"] == "invalid_camera_geometry_declaration"
    assert "truth-like" in result["message"]


def test_snapshot_includes_camera_geometry_summary_when_available(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    court_projection_run = _seed_run(db_session, media.id, "court-projection")
    event_run = _seed_event_run(db_session, media.id, court_projection_run.id)
    _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate")
    db_session.commit()
    before_counts = _event_counts(db_session, event_run.id)

    geometry_result = declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=court_projection_run.id,
    )
    assert geometry_result["ok"] is True

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert snapshot["camera_geometry_summary"]["available"] is True
    assert snapshot["camera_geometry_summary"]["camera_model"] == "homography_backed_court_plane"
    assert snapshot["camera_geometry_summary"]["true_3d_reconstruction_available"] is False
    assert snapshot["camera_geometry_summary"]["3d_ball_trajectory_available"] is False
    assert _event_counts(db_session, event_run.id) == before_counts


def test_snapshot_shows_camera_geometry_unavailable_when_missing(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    event_run = _seed_event_run(db_session, media.id, court_projection_run_id=None)
    db_session.commit()

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert snapshot["camera_geometry_summary"] == {"available": False}


def test_evaluation_includes_geometry_readiness_without_changing_counts(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    court_projection_run = _seed_run(db_session, media.id, "court-projection")
    event_run = _seed_event_run(db_session, media.id, court_projection_run.id)
    _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate")
    _seed_event_candidate(db_session, media.id, event_run.id, "bounce_candidate")
    db_session.commit()
    before_counts = _event_counts(db_session, event_run.id)

    declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=court_projection_run.id,
    )

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert evaluation["geometry_readiness"]["camera_geometry_available"] is True
    assert evaluation["geometry_readiness"]["court_plane_geometry_declared"] is True
    assert evaluation["geometry_readiness"]["true_3d_reconstruction_available"] is False
    assert evaluation["geometry_readiness"]["3d_ball_trajectory_available"] is False
    assert evaluation["candidate_counts"]["hit_candidate"] == 1
    assert evaluation["candidate_counts"]["bounce_candidate"] == 1
    assert _event_counts(db_session, event_run.id) == before_counts


def test_replay_info_exposes_camera_geometry_summary(
    client: TestClient,
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    court_projection_run = _seed_run(db_session, media.id, "court-projection")
    db_session.commit()
    declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=court_projection_run.id,
    )

    response = client.get(f"/media/{media.id}/replay-info")

    assert response.status_code == 200
    body = response.json()
    assert body["camera_geometry_summary"]["available"] is True
    assert body["camera_geometry_summary"]["geometry_status"] == "declared"
    assert body["camera_geometry_summary"]["true_3d_reconstruction_available"] is False
    assert body["available_runs"]["camera_geometry"][0]["evidence_source"] == (
        "camera_geometry_evidence"
    )


def test_camera_geometry_outputs_do_not_introduce_adjudication_fields(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    db_session.commit()

    result = declare_camera_geometry(session=db_session, media_id=media.id)
    rendered = str(result)

    assert "in_out_decision" not in rendered
    assert "score_decision" not in rendered
    assert "accepted_track" not in rendered
    assert "accepted_event" not in rendered
    assert "adjudicated" not in rendered
    assert result["warnings"]["no_adjudication"] is True


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/camera-geometry.mp4",
        duration_ms=4000,
        frame_count=120,
        fps=30.0,
        width=1920,
        height=1080,
    )
    session.add(media)
    session.flush()
    return media


def _seed_run(session: Session, media_id: str, run_name: str) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        metadata_jsonb={},
    )
    session.add(run)
    session.flush()
    return run


def _seed_event_run(
    session: Session,
    media_id: str,
    court_projection_run_id: str | None,
) -> ProcessingRun:
    metadata = {"source_ball_trajectory_run_id": "ball-trajectory-run"}
    if court_projection_run_id is not None:
        metadata["source_court_projection_run_id"] = court_projection_run_id
    run = ProcessingRun(
        media_id=media_id,
        run_name="event-candidate-run",
        run_status="completed",
        metadata_jsonb=metadata,
    )
    session.add(run)
    session.flush()
    return run


def _seed_event_candidate(
    session: Session,
    media_id: str,
    run_id: str,
    candidate_type: str,
) -> Observation:
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family="event_candidate",
        observation_type=candidate_type,
        granularity="frame",
        frame_start=10,
        frame_end=10,
        timestamp_start_ms=333,
        timestamp_end_ms=333,
        confidence=0.5,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "candidate_type": candidate_type,
            "court_point": {"x": 0.4, "y": 0.2},
            "image_point": {"x": 800.0, "y": 600.0},
            "candidate_method": "pytest_candidate",
            "candidate_only": True,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(observation)
    session.flush()
    return observation


def _event_counts(session: Session, event_run_id: str) -> tuple[int, int]:
    hit_count = (
        session.query(Observation)
        .filter(
            Observation.run_id == event_run_id,
            Observation.observation_type == "hit_candidate",
        )
        .count()
    )
    bounce_count = (
        session.query(Observation)
        .filter(
            Observation.run_id == event_run_id,
            Observation.observation_type == "bounce_candidate",
        )
        .count()
    )
    return hit_count, bounce_count
