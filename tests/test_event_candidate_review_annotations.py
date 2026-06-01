from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base, MediaAsset, Observation, ProcessingRun

from apps.api.db import get_session
from apps.api.main import create_app
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


def test_candidate_marker_review_crud_and_snapshot(
    client: TestClient,
    db_session: Session,
) -> None:
    media, event_run, hit = _seed_event_candidate(db_session)

    created = client.post(
        f"/replay/{media.id}/event-candidate-reviews",
        json={
            "event_candidate_run_id": event_run.id,
            "observation_id": hit.id,
            "annotation_kind": "candidate_marker_review",
            "review_label": "useful",
            "note": "Good visible candidate.",
            "reviewer": "pytest-operator",
        },
    )
    assert created.status_code == 201
    review = created.json()
    assert review["observation_id"] == hit.id
    assert review["review_label"] == "useful"
    assert review["candidate_type"] == "hit_candidate"
    assert review["frame"] == 12
    assert review["court_x"] == 0.4
    assert review["payload_jsonb"]["review_metadata_only"] is True

    listed = client.get(
        f"/replay/{media.id}/event-candidate-reviews",
        params={"event_candidate_run_id": event_run.id},
    )
    assert listed.status_code == 200
    body = listed.json()
    assert body["review_summary"]["total_reviews"] == 1
    assert body["review_summary"]["useful"] == 1
    assert body["reviews_by_observation_id"][hit.id][0]["id"] == review["id"]

    patched = client.patch(
        f"/replay/{media.id}/event-candidate-reviews/{review['id']}",
        json={"review_label": "wrong", "note": "Fly-through on closer review."},
    )
    assert patched.status_code == 200
    assert patched.json()["review_label"] == "wrong"
    assert patched.json()["note"] == "Fly-through on closer review."

    snapshot = build_point_evidence_snapshot(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )
    assert snapshot["review_summary"]["wrong"] == 1
    assert snapshot["review_annotations"][0]["review_label"] == "wrong"
    assert snapshot["observations"]["hit_candidate"] == 1
    assert len(snapshot["marker_summary"]) == 1

    deleted = client.delete(f"/replay/{media.id}/event-candidate-reviews/{review['id']}")
    assert deleted.status_code == 200
    assert deleted.json()["ok"] is True
    assert (
        client.get(
            f"/replay/{media.id}/event-candidate-reviews",
            params={"event_candidate_run_id": event_run.id},
        ).json()["review_summary"]["total_reviews"]
        == 0
    )


def test_missing_candidate_note_does_not_require_observation(
    client: TestClient,
    db_session: Session,
) -> None:
    media, event_run, _hit = _seed_event_candidate(db_session)

    created = client.post(
        f"/replay/{media.id}/event-candidate-reviews",
        json={
            "event_candidate_run_id": event_run.id,
            "annotation_kind": "missing_candidate_note",
            "review_label": "missing_bounce_candidate",
            "frame": 44,
            "timestamp_ms": 1467,
            "image_x": 900.0,
            "image_y": 400.0,
            "note": "Possible unmarked bounce here.",
        },
    )
    assert created.status_code == 201
    review = created.json()
    assert review["observation_id"] is None
    assert review["review_label"] == "missing_bounce_candidate"

    body = client.get(
        f"/replay/{media.id}/event-candidate-reviews",
        params={"event_candidate_run_id": event_run.id},
    ).json()
    assert body["review_summary"]["missing_candidate_note"] == 1
    assert body["review_summary"]["missing_bounce_candidate"] == 1


def test_truth_like_review_labels_are_rejected(
    client: TestClient,
    db_session: Session,
) -> None:
    media, event_run, hit = _seed_event_candidate(db_session)

    response = client.post(
        f"/replay/{media.id}/event-candidate-reviews",
        json={
            "event_candidate_run_id": event_run.id,
            "observation_id": hit.id,
            "annotation_kind": "candidate_marker_review",
            "review_label": "confirmed_hit",
        },
    )

    assert response.status_code == 400


def _seed_event_candidate(
    session: Session,
) -> tuple[MediaAsset, ProcessingRun, Observation]:
    media = MediaAsset(
        source_uri="file:///tmp/review-sample.mp4",
        duration_ms=2000,
        frame_count=60,
        fps=30.0,
        width=1920,
        height=1080,
    )
    session.add(media)
    session.flush()
    event_run = ProcessingRun(
        media_id=media.id,
        run_name="event-candidate-review-test",
        run_status="completed",
        metadata_jsonb={
            "source_ball_trajectory_run_id": "trajectory-run",
            "source_court_projection_run_id": "projection-run",
        },
    )
    session.add(event_run)
    session.flush()
    hit = Observation(
        media_id=media.id,
        run_id=event_run.id,
        observation_family="event_candidate",
        observation_type="hit_candidate",
        granularity="frame",
        frame_start=12,
        frame_end=12,
        timestamp_start_ms=400,
        timestamp_end_ms=400,
        confidence=0.61,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "candidate_type": "hit_candidate",
            "court_point": {"x": 0.4, "y": 0.2},
            "image_point": {"x": 800.0, "y": 600.0},
            "candidate_method": "pytest_hit_candidate",
            "reason_codes": ["pytest"],
            "candidate_only": True,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(hit)
    session.commit()
    assert session.scalar(select(Observation).where(Observation.id == hit.id)) is not None
    return media, event_run, hit
