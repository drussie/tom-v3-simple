from __future__ import annotations

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    EventCandidateReviewAnnotation,
    MediaAsset,
    Observation,
    ProcessingRun,
)

from apps.worker.services.point_candidate_evaluation import evaluate_point_candidates


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


def test_point_candidate_evaluation_summarizes_reviews_and_rates(
    db_session: Session,
) -> None:
    media, event_run = _seed_media_and_run(db_session)
    hit_one = _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate", 10)
    _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate", 20)
    bounce = _seed_event_candidate(db_session, media.id, event_run.id, "bounce_candidate", 30)
    _seed_rejection_diagnostic(db_session, media.id, event_run.id)
    _seed_review(
        db_session,
        media.id,
        event_run.id,
        hit_one.id,
        "candidate_marker_review",
        "useful",
    )
    _seed_review(db_session, media.id, event_run.id, bounce.id, "candidate_marker_review", "wrong")
    _seed_review(
        db_session,
        media.id,
        event_run.id,
        None,
        "missing_candidate_note",
        "missing_hit_candidate",
        frame=35,
        timestamp_ms=1167,
        note="Possible missing hit candidate.",
    )
    db_session.commit()

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert evaluation["ok"] is True
    assert evaluation["evaluation_type"] == "point_candidate_review_evaluation"
    assert evaluation["evaluation_version"] == "v0"
    assert evaluation["candidate_counts"] == {
        "hit_candidate": 2,
        "bounce_candidate": 1,
        "final_marker_count": 3,
        "event_candidate_rejection_diagnostic": 1,
        "total_observations": 4,
    }
    assert evaluation["review_summary"]["total_reviews"] == 3
    assert evaluation["review_summary"]["candidate_marker_reviews"] == 2
    assert evaluation["review_summary"]["missing_candidate_notes"] == 1
    assert evaluation["review_coverage"]["reviewed_final_markers"] == 2
    assert evaluation["review_coverage"]["unreviewed_final_markers"] == 1
    assert evaluation["review_coverage"]["reviewed_marker_fraction"] == 0.6667
    assert evaluation["reviewed_only_rates"]["useful_fraction"] == 0.5
    assert evaluation["reviewed_only_rates"]["wrong_fraction"] == 0.5
    assert evaluation["candidate_type_breakdown"]["hit_candidate"]["final_markers"] == 2
    assert evaluation["candidate_type_breakdown"]["hit_candidate"]["reviewed"] == 1
    assert evaluation["candidate_type_breakdown"]["hit_candidate"]["useful"] == 1
    assert evaluation["candidate_type_breakdown"]["bounce_candidate"]["wrong"] == 1
    assert [row["observation_id"] for row in evaluation["marker_evaluation_summary"]] == [
        hit_one.id,
        bounce.id,
    ]
    assert evaluation["missing_candidate_notes"][0]["review_label"] == "missing_hit_candidate"
    assert evaluation["warnings"]["not_truth"] is True
    assert evaluation["warnings"]["no_adjudication"] is True


def test_point_candidate_evaluation_handles_no_reviews(
    db_session: Session,
) -> None:
    media, event_run = _seed_media_and_run(db_session)
    _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate", 10)
    db_session.commit()

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert evaluation["candidate_counts"]["final_marker_count"] == 1
    assert evaluation["review_coverage"]["reviewed_final_markers"] == 0
    assert evaluation["review_coverage"]["unreviewed_final_markers"] == 1
    assert evaluation["reviewed_only_rates"]["wrong_fraction"] is None
    assert evaluation["warnings"]["no_reviewed_markers"] is True


def test_point_candidate_evaluation_handles_zero_final_markers(
    db_session: Session,
) -> None:
    media, event_run = _seed_media_and_run(db_session)
    _seed_rejection_diagnostic(db_session, media.id, event_run.id)
    db_session.commit()

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )

    assert evaluation["candidate_counts"]["final_marker_count"] == 0
    assert evaluation["review_coverage"]["reviewed_final_markers"] == 0
    assert evaluation["review_coverage"]["reviewed_marker_fraction"] == 0.0
    assert evaluation["reviewed_only_rates"]["useful_fraction"] is None


def test_point_candidate_evaluation_markdown_output(
    db_session: Session,
    tmp_path,
) -> None:
    media, event_run = _seed_media_and_run(db_session)
    marker = _seed_event_candidate(db_session, media.id, event_run.id, "bounce_candidate", 77)
    _seed_review(db_session, media.id, event_run.id, marker.id, "candidate_marker_review", "wrong")
    db_session.commit()
    output_path = tmp_path / "evaluation.md"

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
        output_format="markdown",
        output_path=str(output_path),
    )

    assert evaluation["ok"] is True
    assert "# Point Candidate Review Evaluation v0" in evaluation["markdown"]
    assert "| Bounce candidates | 1 |" in evaluation["markdown"]
    assert "| Wrong | 1 |" in evaluation["markdown"]
    assert "It is not truth, not score, not in/out, and not adjudication." in evaluation["markdown"]
    assert output_path.read_text(encoding="utf-8") == evaluation["markdown"]


def test_point_candidate_evaluation_avoids_truth_metric_terms(
    db_session: Session,
) -> None:
    media, event_run = _seed_media_and_run(db_session)
    _seed_event_candidate(db_session, media.id, event_run.id, "hit_candidate", 10)
    db_session.commit()

    evaluation = evaluate_point_candidates(
        session=db_session,
        media_id=media.id,
        event_candidate_run_id=event_run.id,
    )
    rendered = str(evaluation)

    assert "true_positive" not in rendered
    assert "false_positive" not in rendered
    assert "false_negative" not in rendered
    assert "precision" not in rendered
    assert "recall" not in rendered
    assert "ground_truth" not in rendered
    assert "ground-truth" not in rendered
    assert "score_or_point_truth" in rendered


def _seed_media_and_run(session: Session) -> tuple[MediaAsset, ProcessingRun]:
    media = MediaAsset(
        source_uri="file:///tmp/evaluation-sample.mp4",
        duration_ms=4000,
        frame_count=120,
        fps=30.0,
        width=1920,
        height=1080,
    )
    session.add(media)
    session.flush()
    event_run = ProcessingRun(
        media_id=media.id,
        run_name="point-candidate-evaluation-test",
        run_status="completed",
        metadata_jsonb={
            "source_ball_trajectory_run_id": "trajectory-run",
            "source_court_projection_run_id": "projection-run",
        },
    )
    session.add(event_run)
    session.flush()
    return media, event_run


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


def _seed_rejection_diagnostic(session: Session, media_id: str, run_id: str) -> Observation:
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family="event_candidate",
        observation_type="event_candidate_rejection_diagnostic",
        granularity="frame",
        frame_start=40,
        frame_end=40,
        timestamp_start_ms=1333,
        timestamp_end_ms=1333,
        confidence=0.0,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "candidate_type": "event_candidate_rejection_diagnostic",
            "candidate_only": True,
            "observation_only": True,
            "no_adjudication": True,
        },
    )
    session.add(observation)
    session.flush()
    return observation


def _seed_review(
    session: Session,
    media_id: str,
    run_id: str,
    observation_id: str | None,
    annotation_kind: str,
    review_label: str,
    *,
    frame: int | None = None,
    timestamp_ms: int | None = None,
    note: str | None = None,
) -> EventCandidateReviewAnnotation:
    row = EventCandidateReviewAnnotation(
        media_id=media_id,
        event_candidate_run_id=run_id,
        observation_id=observation_id,
        annotation_kind=annotation_kind,
        review_label=review_label,
        frame=frame,
        timestamp_ms=timestamp_ms,
        note=note,
        payload_jsonb={
            "review_metadata_only": True,
            "candidate_evidence_preserved": True,
            "not_truth": True,
            "no_adjudication": True,
        },
    )
    session.add(row)
    session.flush()
    return row
