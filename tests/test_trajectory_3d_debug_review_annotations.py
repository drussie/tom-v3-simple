from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
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


def test_create_trajectory_3d_sample_review_and_summary(
    client: TestClient,
    db_session: Session,
) -> None:
    context = _seed_3d_debug_review_context(db_session)

    created = client.post(
        f"/replay/{context['media'].id}/trajectory-3d-debug-reviews",
        json={
            "trajectory_3d_run_id": context["trajectory_3d_run"].id,
            "event_candidate_run_id": context["event_run"].id,
            "trajectory_3d_candidate_id": context["sample"].id,
            "annotation_kind": "trajectory_3d_sample_review",
            "review_label": "bad_3d_position",
            "note": "3D point drifts away from the marker context.",
            "reviewer": "pytest-operator",
        },
    )

    assert created.status_code == 201
    review = created.json()
    assert review["trajectory_3d_candidate_id"] == context["sample"].id
    assert review["frame"] == 12
    assert review["court_x_m"] == 3.1
    assert review["payload_jsonb"]["review_metadata_only"] is True
    assert review["payload_jsonb"]["does_not_change_3d_candidates"] is True

    listed = client.get(
        f"/replay/{context['media'].id}/trajectory-3d-debug-reviews",
        params={
            "trajectory3dRunId": context["trajectory_3d_run"].id,
            "eventCandidateRunId": context["event_run"].id,
        },
    )
    assert listed.status_code == 200
    body = listed.json()
    assert body["review_summary"]["total_reviews"] == 1
    assert body["review_summary"]["sample_reviews"] == 1
    assert body["review_summary"]["bad_3d_position"] == 1
    assert (
        body["reviews_by_trajectory_3d_candidate_id"][context["sample"].id][0]["id"]
        == review["id"]
    )

    patched = client.patch(
        f"/replay/{context['media'].id}/trajectory-3d-debug-reviews/{review['id']}",
        json={"review_label": "wrong", "note": "Still wrong after refresh."},
    )
    assert patched.status_code == 200
    assert patched.json()["review_label"] == "wrong"

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
    )
    assert snapshot["trajectory_3d_debug_review_summary"]["total_reviews"] == 1
    assert snapshot["trajectory_3d_debug_review_summary"]["wrong"] == 1
    assert snapshot["observations"]["hit_candidate"] == 1
    assert snapshot["observations"]["bounce_candidate"] == 1

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
    )
    assert evaluation["trajectory_3d_debug_reviews"]["total_reviews"] == 1
    assert evaluation["candidate_counts"]["hit_candidate"] == 1
    assert evaluation["candidate_counts"]["bounce_candidate"] == 1
    assert (
        db_session.scalar(
            select(BallTrajectory3DCandidate).where(
                BallTrajectory3DCandidate.id == context["sample"].id
            )
        ).court_x_m
        == 3.1
    )


def test_create_diagnostic_review_and_missing_3d_sample_note(
    client: TestClient,
    db_session: Session,
) -> None:
    context = _seed_3d_debug_review_context(db_session)

    diagnostic_review = client.post(
        f"/replay/{context['media'].id}/trajectory-3d-debug-reviews",
        json={
            "trajectory_3d_run_id": context["trajectory_3d_run"].id,
            "event_candidate_run_id": context["event_run"].id,
            "event_candidate_3d_diagnostic_id": context["diagnostic"].id,
            "annotation_kind": "event_candidate_3d_diagnostic_review",
            "review_label": "bad_diagnostic_link",
            "note": "Nearest 3D sample looks like the wrong diagnostic link.",
        },
    )
    assert diagnostic_review.status_code == 201
    diagnostic_body = diagnostic_review.json()
    assert diagnostic_body["event_candidate_3d_diagnostic_id"] == context["diagnostic"].id
    assert diagnostic_body["event_observation_id"] == context["hit"].id
    assert diagnostic_body["trajectory_3d_candidate_id"] == context["sample"].id
    assert diagnostic_body["review_label"] == "bad_diagnostic_link"

    missing_note = client.post(
        f"/replay/{context['media'].id}/trajectory-3d-debug-reviews",
        json={
            "trajectory_3d_run_id": context["trajectory_3d_run"].id,
            "event_candidate_run_id": context["event_run"].id,
            "annotation_kind": "missing_3d_sample_note",
            "review_label": "missing_3d_sample",
            "frame": 44,
            "timestamp_ms": 1467,
            "note": "No nearby 3D sample for this marker review moment.",
        },
    )
    assert missing_note.status_code == 201
    assert missing_note.json()["review_label"] == "missing_3d_sample"

    overlay = client.get(
        "/replay/overlays",
        params={
            "media_id": context["media"].id,
            "start_ms": 0,
            "end_ms": 2000,
            "layers": "hit_candidates,bounce_candidates",
            "event_candidate_run_id": context["event_run"].id,
            "trajectory_3d_run_id": context["trajectory_3d_run"].id,
        },
    )
    assert overlay.status_code == 200
    summary = overlay.json()["trajectory_3d_debug_review_summary"]
    assert summary["total_reviews"] == 2
    assert summary["diagnostic_reviews"] == 1
    assert summary["missing_3d_sample_notes"] == 1
    assert summary["not_truth"] is True


def test_trajectory_3d_debug_reviews_reject_truth_like_labels(
    client: TestClient,
    db_session: Session,
) -> None:
    context = _seed_3d_debug_review_context(db_session)

    response = client.post(
        f"/replay/{context['media'].id}/trajectory-3d-debug-reviews",
        json={
            "trajectory_3d_run_id": context["trajectory_3d_run"].id,
            "event_candidate_run_id": context["event_run"].id,
            "trajectory_3d_candidate_id": context["sample"].id,
            "annotation_kind": "trajectory_3d_sample_review",
            "review_label": "confirmed_3d",
        },
    )

    assert response.status_code == 400


def _seed_3d_debug_review_context(session: Session) -> dict[str, object]:
    media = MediaAsset(
        source_uri="file:///tmp/trajectory-3d-review-sample.mp4",
        duration_ms=3000,
        frame_count=90,
        fps=30.0,
        width=1920,
        height=1080,
    )
    session.add(media)
    session.flush()

    ball_trajectory_run = _seed_run(session, media.id, "ball-trajectory")
    court_projection_run = _seed_run(session, media.id, "court-projection")
    trajectory_3d_run = _seed_run(session, media.id, "trajectory-3d")
    event_run = _seed_run(
        session,
        media.id,
        "event-candidates",
        metadata_jsonb={
            "source_ball_trajectory_run_id": ball_trajectory_run.id,
            "source_court_projection_run_id": court_projection_run.id,
        },
    )

    hit = _seed_event_observation(session, media.id, event_run.id, "hit_candidate", 12, 400)
    bounce = _seed_event_observation(
        session,
        media.id,
        event_run.id,
        "bounce_candidate",
        30,
        1000,
    )
    sample = BallTrajectory3DCandidate(
        media_id=media.id,
        ball_trajectory_run_id=ball_trajectory_run.id,
        court_projection_run_id=court_projection_run.id,
        trajectory_3d_run_id=trajectory_3d_run.id,
        frame=12,
        timestamp_ms=400,
        image_x=800.0,
        image_y=520.0,
        court_x=0.42,
        court_y=0.33,
        court_x_m=3.1,
        court_y_m=7.2,
        court_z_m=None,
        court_z_status="unknown",
        height_model="none_unknown",
        projection_method="declared_court_plane_metric_xy_unknown_z_v0",
        confidence=0.52,
        speed_mps=11.0,
        diagnostics_jsonb={"pytest": True},
        warnings_jsonb={
            "trajectory_3d_candidate_only": True,
            "not_3d_truth": True,
            "height_not_verified": True,
            "no_adjudication": True,
        },
        metadata_jsonb={"pytest": True},
    )
    session.add(sample)
    session.flush()

    diagnostic = EventCandidate3DDiagnostic(
        media_id=media.id,
        event_candidate_run_id=event_run.id,
        event_observation_id=hit.id,
        candidate_type="hit_candidate",
        trajectory_3d_run_id=trajectory_3d_run.id,
        frame=12,
        timestamp_ms=400,
        nearest_3d_candidate_id=sample.id,
        nearest_3d_frame=12,
        nearest_3d_timestamp_ms=400,
        nearest_time_delta_ms=0,
        nearest_court_x_m=3.1,
        nearest_court_y_m=7.2,
        nearest_court_z_m=None,
        height_status="height_unknown",
        diagnostic_status="evaluated",
        diagnostic_label="neutral_context",
        diagnostic_confidence=0.2,
        pre_window_sample_count=1,
        post_window_sample_count=1,
        local_window_sample_count=1,
        local_velocity_available=False,
        diagnostics_jsonb={"pytest": True},
        warnings_jsonb={
            "diagnostic_only": True,
            "not_truth": True,
            "not_3d_truth": True,
            "no_adjudication": True,
        },
        metadata_jsonb={"pytest": True},
    )
    session.add(diagnostic)
    session.commit()
    return {
        "media": media,
        "ball_trajectory_run": ball_trajectory_run,
        "court_projection_run": court_projection_run,
        "trajectory_3d_run": trajectory_3d_run,
        "event_run": event_run,
        "hit": hit,
        "bounce": bounce,
        "sample": sample,
        "diagnostic": diagnostic,
    }


def _seed_run(
    session: Session,
    media_id: str,
    run_name: str,
    *,
    metadata_jsonb: dict[str, object] | None = None,
) -> ProcessingRun:
    row = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        metadata_jsonb=metadata_jsonb or {},
    )
    session.add(row)
    session.flush()
    return row


def _seed_event_observation(
    session: Session,
    media_id: str,
    run_id: str,
    observation_type: str,
    frame: int,
    timestamp_ms: int,
) -> Observation:
    row = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family="event_candidate",
        observation_type=observation_type,
        granularity="frame",
        frame_start=frame,
        frame_end=frame,
        timestamp_start_ms=timestamp_ms,
        timestamp_end_ms=timestamp_ms,
        confidence=0.5,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "candidate_type": observation_type,
            "court_point": {"x": 0.4, "y": 0.2},
            "image_point": {"x": 800.0, "y": 600.0},
            "candidate_method": "pytest_event_candidate",
            "reason_codes": ["pytest"],
            "candidate_only": True,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(row)
    session.flush()
    return row
