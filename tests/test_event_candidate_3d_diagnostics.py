from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.event_candidate_3d_diagnostic import EventCandidate3DDiagnosticCreate
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    Base,
    EventCandidate3DDiagnostic,
    MediaAsset,
    Observation,
    ProcessingRun,
)

from apps.api.db import get_session
from apps.api.main import create_app
from apps.worker.services.camera_geometry import declare_camera_geometry
from apps.worker.services.event_candidate_3d_diagnostics import (
    build_event_candidate_3d_diagnostics,
)
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


def test_event_candidate_3d_diagnostics_link_final_markers_to_nearest_3d(
    db_session: Session,
) -> None:
    context = _seed_context(db_session)
    before_counts = _event_counts(db_session, context["event_run"].id)

    result = build_event_candidate_3d_diagnostics(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
        time_window_ms=250,
    )

    assert result["ok"] is True
    assert result["diagnostic_type"] == "event_candidate_3d_diagnostic_evidence"
    assert result["diagnostic_version"] == "v0"
    assert result["diagnostic_summary"]["final_marker_count"] == 2
    assert result["diagnostic_summary"]["diagnostic_count"] == 2
    assert result["diagnostic_summary"]["nearest_3d_sample_found_count"] == 2
    assert result["diagnostic_summary"]["height_unknown_count"] == 2
    assert result["diagnostic_summary"]["neutral_context_count"] == 2
    assert result["warnings"]["diagnostic_only"] is True
    assert result["warnings"]["not_truth"] is True
    assert result["warnings"]["not_3d_truth"] is True

    rows = db_session.scalars(
        select(EventCandidate3DDiagnostic)
        .where(EventCandidate3DDiagnostic.event_candidate_run_id == context["event_run"].id)
        .order_by(EventCandidate3DDiagnostic.timestamp_ms)
    ).all()
    assert len(rows) == 2
    assert rows[0].event_observation_id == context["hit"].id
    assert rows[0].nearest_3d_candidate_id is not None
    assert rows[0].diagnostic_status == "height_unknown"
    assert rows[0].diagnostic_label == "neutral_context"
    assert rows[0].height_status == "unknown"
    assert rows[0].warnings_jsonb["does_not_change_event_candidates"] is True
    assert _event_counts(db_session, context["event_run"].id) == before_counts


def test_event_candidate_3d_diagnostics_handle_no_nearby_samples(db_session: Session) -> None:
    context = _seed_context(db_session, far_away_3d=True)

    result = build_event_candidate_3d_diagnostics(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
        time_window_ms=10,
    )

    assert result["ok"] is True
    assert result["diagnostic_summary"]["diagnostic_count"] == 2
    assert result["diagnostic_summary"]["nearest_3d_sample_found_count"] == 0
    rows = db_session.scalars(select(EventCandidate3DDiagnostic)).all()
    assert {row.diagnostic_status for row in rows} == {"insufficient_3d_evidence"}
    assert {row.diagnostic_label for row in rows} == {"insufficient_evidence"}


def test_snapshot_evaluation_and_replay_include_3d_event_diagnostic_summary(
    client: TestClient,
    db_session: Session,
) -> None:
    context = _seed_context(db_session)
    build_event_candidate_3d_diagnostics(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
    )

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
    )
    assert snapshot["event_candidate_3d_diagnostic_summary"]["available"] is True
    assert snapshot["event_candidate_3d_diagnostic_summary"]["diagnostic_count"] == 2

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
    )
    assert evaluation["event_candidate_3d_diagnostics"]["available"] is True
    assert evaluation["event_candidate_3d_diagnostics"]["diagnostic_count"] == 2
    assert evaluation["candidate_counts"]["hit_candidate"] == 1
    assert evaluation["candidate_counts"]["bounce_candidate"] == 1

    response = client.get(
        "/replay/overlays",
        params={
            "media_id": context["media"].id,
            "start_ms": 0,
            "end_ms": 1000,
            "layers": "event_candidates",
            "event_candidate_run_id": context["event_run"].id,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["event_candidate_3d_diagnostic_summary"]["available"] is True
    assert len(body["event_candidate_3d_diagnostics"]) == 2
    assert body["marker_summary"][0]["event_candidate_3d_diagnostic"]["not_truth"] is True


def test_event_candidate_3d_diagnostics_reject_truth_like_labels() -> None:
    with pytest.raises(ValidationError, match="truth-like"):
        EventCandidate3DDiagnosticCreate(
            media_id="media",
            event_candidate_run_id="event-run",
            event_observation_id="observation",
            candidate_type="hit_candidate",
            frame=1,
            timestamp_ms=33,
            diagnostic_status="evaluated",
            diagnostic_label="confirmed_hit",
        )


def test_event_candidate_3d_diagnostics_do_not_introduce_truth_fields(
    db_session: Session,
) -> None:
    context = _seed_context(db_session)
    result = build_event_candidate_3d_diagnostics(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry_id"],
    )
    rendered = str(result)

    assert "confirmed_hit" not in rendered
    assert "confirmed_bounce" not in rendered
    assert "false_positive" not in rendered
    assert "true_positive" not in rendered
    assert "in_out_decision" not in rendered
    assert "score_decision" not in rendered
    assert result["warnings"]["no_adjudication"] is True


def _seed_context(db_session: Session, *, far_away_3d: bool = False) -> dict[str, object]:
    media = _seed_media(db_session)
    court_projection_run = _seed_run(db_session, media.id, "court-projection")
    ball_trajectory_run = _seed_run(db_session, media.id, "ball-trajectory")
    event_run = _seed_run(
        db_session,
        media.id,
        "event-candidates",
        metadata_jsonb={
            "source_ball_trajectory_run_id": ball_trajectory_run.id,
            "source_court_projection_run_id": court_projection_run.id,
        },
    )
    geometry = declare_camera_geometry(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=court_projection_run.id,
    )
    assert geometry["ok"] is True
    trajectory_3d_run = _seed_run(
        db_session,
        media.id,
        "3d-ball-trajectory",
        metadata_jsonb={
            "source_ball_trajectory_run_id": ball_trajectory_run.id,
            "source_court_projection_run_id": court_projection_run.id,
            "camera_geometry_id": geometry["camera_geometry_id"],
        },
    )
    hit = _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate", 10)
    bounce = _seed_event_candidate(db_session, media.id, event_run.id, "bounce_candidate", 20)
    timestamps = [5000, 6000] if far_away_3d else [333, 666]
    for index, timestamp_ms in enumerate(timestamps):
        _seed_3d_candidate(
            db_session,
            media_id=media.id,
            trajectory_3d_run_id=trajectory_3d_run.id,
            ball_trajectory_run_id=ball_trajectory_run.id,
            court_projection_run_id=court_projection_run.id,
            camera_geometry_id=geometry["camera_geometry_id"],
            frame=10 + index * 10,
            timestamp_ms=timestamp_ms,
            court_x_m=1.0 + index,
            court_y_m=5.0 + index,
        )
    db_session.commit()
    return {
        "media": media,
        "event_run": event_run,
        "trajectory_3d_run": trajectory_3d_run,
        "camera_geometry_id": geometry["camera_geometry_id"],
        "hit": hit,
        "bounce": bounce,
    }


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/event-candidate-3d-diagnostics.mp4",
        duration_ms=4000,
        frame_count=120,
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


def _seed_event_candidate(
    session: Session,
    media_id: str,
    run_id: str,
    candidate_type: str,
    frame: int,
) -> Observation:
    timestamp_ms = round(frame * 1000 / 30)
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family="event_candidate",
        observation_type=candidate_type,
        granularity="frame",
        frame_start=frame,
        frame_end=frame,
        timestamp_start_ms=timestamp_ms,
        timestamp_end_ms=timestamp_ms,
        confidence=0.5,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "candidate_type": candidate_type,
            "frame_number": frame,
            "timestamp_ms": timestamp_ms,
            "court_point": {"x": 0.4, "y": 0.2},
            "image_point": {"x": 800.0, "y": 600.0},
            "candidate_method": "pytest_candidate",
            "reason_codes": ["pytest"],
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


def _seed_3d_candidate(
    session: Session,
    *,
    media_id: str,
    trajectory_3d_run_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    camera_geometry_id: str,
    frame: int,
    timestamp_ms: int,
    court_x_m: float,
    court_y_m: float,
) -> BallTrajectory3DCandidate:
    row = BallTrajectory3DCandidate(
        media_id=media_id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        court_projection_run_id=court_projection_run_id,
        camera_geometry_id=camera_geometry_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        frame=frame,
        timestamp_ms=timestamp_ms,
        court_x=0.2,
        court_y=0.3,
        court_x_m=court_x_m,
        court_y_m=court_y_m,
        court_z_m=None,
        court_z_status="unknown",
        height_model="none_unknown",
        projection_method="declared_court_plane_metric_xy_unknown_z_v0",
        speed_mps=12.5,
        diagnostics_jsonb={"pytest": True},
        warnings_jsonb={
            "not_3d_truth": True,
            "height_not_verified": True,
            "no_adjudication": True,
        },
        metadata_jsonb={"pytest": True},
    )
    session.add(row)
    session.flush()
    return row


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
