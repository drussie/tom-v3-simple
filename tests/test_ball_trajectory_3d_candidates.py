from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    Base,
    MediaAsset,
    Observation,
    ProcessingRun,
)

from apps.api.db import get_session
from apps.api.main import create_app
from apps.worker.services.ball_trajectory_3d import build_3d_ball_trajectory_candidates
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


def test_build_3d_ball_trajectory_candidates_persists_unknown_height_rows(
    db_session: Session,
) -> None:
    context = _seed_trajectory_context(db_session)
    result = build_3d_ball_trajectory_candidates(
        session=db_session,
        media_id=context["media"].id,
        ball_trajectory_run_id=context["trajectory_run"].id,
        court_projection_run_id=context["projection_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
    )

    assert result["ok"] is True
    assert result["trajectory_3d_type"] == "ball_trajectory_3d_candidate_evidence"
    assert result["trajectory_3d_version"] == "v0"
    assert result["candidate_summary"]["source_trajectory_points"] == 3
    assert result["candidate_summary"]["trajectory_3d_candidate_count"] == 3
    assert result["candidate_summary"]["height_model"] == "none_unknown"
    assert result["candidate_summary"]["known_height_count"] == 0
    assert result["candidate_summary"]["unknown_height_count"] == 3
    assert result["candidate_summary"]["court_plane_xy_metric_count"] == 3
    assert result["capabilities"]["court_plane_xy_metric_available"] is True
    assert result["capabilities"]["height_candidate_available"] is False
    assert result["capabilities"]["true_3d_reconstruction_available"] is False
    assert result["capabilities"]["3d_ball_trajectory_truth_available"] is False
    assert result["warnings"]["not_3d_truth"] is True
    assert result["warnings"]["height_not_verified"] is True
    assert result["warnings"]["does_not_change_event_candidates"] is True

    rows = db_session.scalars(
        select(BallTrajectory3DCandidate)
        .where(BallTrajectory3DCandidate.trajectory_3d_run_id == result["trajectory_3d_run_id"])
        .order_by(BallTrajectory3DCandidate.frame)
    ).all()
    assert len(rows) == 3
    assert rows[0].court_x_m == pytest.approx(1.097)
    assert rows[0].court_y_m == pytest.approx(4.754)
    assert rows[0].court_z_m is None
    assert rows[0].court_z_status == "unknown"
    assert rows[0].height_model == "none_unknown"
    assert rows[0].image_x == pytest.approx(500.0)
    assert rows[1].speed_mps is not None
    assert rows[1].warnings_jsonb["not_3d_truth"] is True


def test_3d_ball_trajectory_can_use_court_plane_placeholder_explicitly(
    db_session: Session,
) -> None:
    context = _seed_trajectory_context(db_session)
    result = build_3d_ball_trajectory_candidates(
        session=db_session,
        media_id=context["media"].id,
        ball_trajectory_run_id=context["trajectory_run"].id,
        court_projection_run_id=context["projection_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
        height_model="court_plane_placeholder",
    )

    assert result["ok"] is True
    assert result["candidate_summary"]["height_model"] == "court_plane_placeholder"
    assert result["candidate_summary"]["known_height_count"] == 3
    row = db_session.scalar(
        select(BallTrajectory3DCandidate).where(
            BallTrajectory3DCandidate.trajectory_3d_run_id == result["trajectory_3d_run_id"]
        )
    )
    assert row is not None
    assert row.court_z_m == pytest.approx(0.0)
    assert row.court_z_status == "court_plane_assumed"
    assert row.warnings_jsonb["height_not_verified"] is True


def test_3d_ball_trajectory_rejects_truth_like_height_model(db_session: Session) -> None:
    context = _seed_trajectory_context(db_session)
    result = build_3d_ball_trajectory_candidates(
        session=db_session,
        media_id=context["media"].id,
        ball_trajectory_run_id=context["trajectory_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
        height_model="true_height",
    )

    assert result["ok"] is False
    assert result["status"] == "invalid_height_model"
    assert "truth-like" in result["message"]


def test_snapshot_and_evaluation_include_3d_readiness_without_changing_counts(
    db_session: Session,
) -> None:
    context = _seed_trajectory_context(db_session)
    event_run = _seed_event_run(
        db_session,
        context["media"].id,
        context["trajectory_run"].id,
        context["projection_run"].id,
    )
    _seed_event_candidate(db_session, context["media"].id, event_run.id, "hit_candidate")
    _seed_event_candidate(db_session, context["media"].id, event_run.id, "bounce_candidate")
    db_session.commit()
    before_counts = _event_counts(db_session, event_run.id)

    build_3d_ball_trajectory_candidates(
        session=db_session,
        media_id=context["media"].id,
        ball_trajectory_run_id=context["trajectory_run"].id,
        court_projection_run_id=context["projection_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
    )

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=event_run.id,
    )
    assert snapshot["trajectory_3d_summary"]["available"] is True
    assert snapshot["trajectory_3d_summary"]["candidate_count"] == 3
    assert snapshot["trajectory_3d_summary"]["height_model"] == "none_unknown"
    assert snapshot["trajectory_3d_summary"]["true_3d_reconstruction_available"] is False

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=event_run.id,
    )
    assert evaluation["trajectory_3d_readiness"]["trajectory_3d_candidates_available"] is True
    assert evaluation["trajectory_3d_readiness"]["height_candidate_available"] is False
    assert evaluation["trajectory_3d_readiness"]["true_3d_reconstruction_available"] is False
    assert evaluation["candidate_counts"]["hit_candidate"] == 1
    assert evaluation["candidate_counts"]["bounce_candidate"] == 1
    assert _event_counts(db_session, event_run.id) == before_counts


def test_snapshot_shows_3d_trajectory_unavailable_when_missing(db_session: Session) -> None:
    media = _seed_media(db_session)
    event_run = _seed_event_run(db_session, media.id, "trajectory-run", "projection-run")
    db_session.commit()

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert snapshot["trajectory_3d_summary"] == {"available": False}


def test_replay_info_exposes_3d_trajectory_summary(
    client: TestClient,
    db_session: Session,
) -> None:
    context = _seed_trajectory_context(db_session)
    result = build_3d_ball_trajectory_candidates(
        session=db_session,
        media_id=context["media"].id,
        ball_trajectory_run_id=context["trajectory_run"].id,
        court_projection_run_id=context["projection_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
    )

    response = client.get(f"/media/{context['media'].id}/replay-info")

    assert response.status_code == 200
    body = response.json()
    assert body["trajectory_3d_summary"]["available"] is True
    assert body["trajectory_3d_summary"]["trajectory_3d_run_id"] == result["trajectory_3d_run_id"]
    assert body["trajectory_3d_summary"]["candidate_count"] == 3
    assert body["trajectory_3d_summary"]["true_3d_reconstruction_available"] is False
    assert body["available_runs"]["trajectory_3d"][0]["evidence_source"] == (
        "ball_trajectory_3d_candidate_evidence"
    )


def test_3d_ball_trajectory_outputs_do_not_introduce_adjudication_fields(
    db_session: Session,
) -> None:
    context = _seed_trajectory_context(db_session)
    result = build_3d_ball_trajectory_candidates(
        session=db_session,
        media_id=context["media"].id,
        ball_trajectory_run_id=context["trajectory_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
    )
    rendered = str(result)

    assert "in_out_decision" not in rendered
    assert "score_decision" not in rendered
    assert "accepted_event" not in rendered
    assert "adjudicated" not in rendered
    assert result["warnings"]["no_adjudication"] is True


def _seed_trajectory_context(db_session: Session) -> dict[str, object]:
    media = _seed_media(db_session)
    projection_run = _seed_run(db_session, media.id, "court-projection")
    trajectory_run = _seed_run(
        db_session,
        media.id,
        "ball-trajectory",
        metadata_jsonb={"source_court_projection_run_id": projection_run.id},
    )
    projections = [
        _seed_ball_projection(
            db_session,
            media_id=media.id,
            run_id=projection_run.id,
            frame=frame,
            timestamp_ms=frame * 33,
            court_x=0.10 + frame * 0.02,
            court_y=0.20 + frame * 0.03,
            image_x=500.0 + frame * 12.0,
            image_y=400.0 - frame * 8.0,
        )
        for frame in range(3)
    ]
    _seed_ball_trajectory_segment(
        db_session,
        media_id=media.id,
        run_id=trajectory_run.id,
        projection_observations=projections,
    )
    db_session.commit()
    geometry = declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=projection_run.id,
    )
    assert geometry["ok"] is True
    return {
        "media": media,
        "projection_run": projection_run,
        "trajectory_run": trajectory_run,
        "camera_geometry_id": geometry["camera_geometry_id"],
    }


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/ball-trajectory-3d.mp4",
        duration_ms=3000,
        frame_count=90,
        fps=30.0,
        width=1920,
        height=1080,
    )
    session.add(media)
    session.flush()
    return media


def _seed_run(
    session: Session,
    media_id: str,
    run_name: str,
    metadata_jsonb: dict[str, object] | None = None,
) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        metadata_jsonb=metadata_jsonb or {},
    )
    session.add(run)
    session.flush()
    return run


def _seed_ball_projection(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    frame: int,
    timestamp_ms: int,
    court_x: float,
    court_y: float,
    image_x: float,
    image_y: float,
) -> Observation:
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family="projection",
        observation_type="ball_court_projection_candidate",
        granularity="frame",
        frame_start=frame,
        frame_end=frame,
        timestamp_start_ms=timestamp_ms,
        timestamp_end_ms=timestamp_ms,
        confidence=0.8,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "frame_number": frame,
            "timestamp_ms": timestamp_ms,
            "image_point": {"x": image_x, "y": image_y},
            "court_point": {"x": court_x, "y": court_y},
            "projection_candidate_only": True,
            "not_ball_truth": True,
            "not_court_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(observation)
    session.flush()
    return observation


def _seed_ball_trajectory_segment(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    projection_observations: list[Observation],
) -> Observation:
    points = []
    for projection in projection_observations:
        payload = projection.payload_jsonb
        court_point = payload["court_point"]
        points.append(
            {
                "frame_number": projection.frame_start,
                "timestamp_ms": projection.timestamp_start_ms,
                "court_x": court_point["x"],
                "court_y": court_point["y"],
                "source_observation_id": projection.id,
                "source_homography_observation_id": f"homography-{projection.frame_start}",
                "homography_time_delta_ms": projection.frame_start * 10,
                "homography_carried_forward": projection.frame_start > 0,
                "inside_template_bounds": True,
            }
        )
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family="trajectory",
        observation_type="ball_trajectory_court_candidate",
        granularity="segment",
        frame_start=projection_observations[0].frame_start,
        frame_end=projection_observations[-1].frame_start,
        timestamp_start_ms=projection_observations[0].timestamp_start_ms,
        timestamp_end_ms=projection_observations[-1].timestamp_start_ms,
        confidence=0.7,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "source_court_projection_run_id": projection_observations[0].run_id,
            "source_ball_court_projection_observation_ids": [
                projection.id for projection in projection_observations
            ],
            "trajectory_segment_index": 0,
            "point_count": len(points),
            "points": points,
            "trajectory_candidate_only": True,
            "not_ball_truth": True,
            "not_bounce_truth": True,
            "not_hit_truth": True,
            "not_in_out_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(observation)
    session.flush()
    return observation


def _seed_event_run(
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
) -> ProcessingRun:
    return _seed_run(
        session,
        media_id,
        "event-candidate-run",
        metadata_jsonb={
            "source_ball_trajectory_run_id": ball_trajectory_run_id,
            "source_court_projection_run_id": court_projection_run_id,
        },
    )


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
