from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    HomographyCandidateObservation,
    MediaAsset,
    Observation,
    ObservationLineage,
    ProcessingRun,
)

from apps.worker.cli import _handle_project_objects_to_court
from apps.worker.services.object_court_projection import (
    match_homography_for_timestamp,
    project_image_point_to_court_template,
    project_objects_to_court,
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


def test_project_image_point_to_court_template() -> None:
    point = project_image_point_to_court_template(
        [[0.001, 0.0, 0.0], [0.0, 0.002, 0.0], [0.0, 0.0, 1.0]],
        100.0,
        200.0,
    )

    assert point == {"x": 0.1, "y": 0.4}


def test_object_court_projection_creates_candidates_and_lineage(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    motion_run, ball, near_player = _seed_motion_smoothing_run(db_session, media.id)
    homography_run, homography = _seed_homography_run(
        db_session,
        media.id,
        frame=1,
        timestamp_ms=33,
    )

    result = project_objects_to_court(
        session=db_session,
        media_id=media.id,
        motion_smoothing_run_id=motion_run.id,
        homography_run_id=homography_run.id,
        homography_max_gap_ms=1500,
    )

    assert result["ok"] is True
    assert result["observations"] == {
        "ball_court_projection_candidate": 1,
        "main_player_court_projection_candidate": 1,
        "total": 2,
    }
    assert result["skipped"] == {"missing_homography": 0, "invalid_projection": 0}

    rows = db_session.scalars(
        select(Observation).where(Observation.run_id == result["court_projection_run_id"])
    ).all()
    assert {row.observation_type for row in rows} == {
        "ball_court_projection_candidate",
        "main_player_court_projection_candidate",
    }
    ball_projection = next(
        row for row in rows if row.observation_type == "ball_court_projection_candidate"
    )
    player_projection = next(
        row
        for row in rows
        if row.observation_type == "main_player_court_projection_candidate"
    )
    assert ball_projection.observation_family == "projection"
    assert ball_projection.coordinate_space == "court_template_2d"
    assert ball_projection.payload_jsonb["court_point"] == {"x": 0.1, "y": 0.2}
    assert ball_projection.payload_jsonb["source_ball_observation_id"] == ball.id
    assert ball_projection.payload_jsonb["source_homography_observation_id"] == homography
    assert ball_projection.payload_jsonb["projection_candidate_only"] is True
    assert ball_projection.payload_jsonb["no_bounce_hit_in_out_score"] is True
    assert player_projection.payload_jsonb["image_anchor"] == {
        "anchor_type": "bbox_bottom_center",
        "x": 230.0,
        "y": 320.0,
        "bbox": {"x": 200.0, "y": 100.0, "w": 60.0, "h": 220.0},
    }
    assert player_projection.payload_jsonb["court_point"] == {"x": 0.23, "y": 0.32}
    assert player_projection.payload_jsonb["track_role_candidate"] == (
        "near_player_track_candidate"
    )

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id.in_([row.id for row in rows])
        )
    ).all()
    assert {row.relationship_type for row in lineage} == {
        "projected_from_smoothed_ball_position",
        "projected_from_smoothed_main_player_box",
        "projected_with_homography_candidate",
    }
    assert db_session.get(Observation, ball.id).observation_type == (
        "smoothed_ball_position_candidate"
    )
    assert db_session.get(Observation, near_player.id).observation_type == (
        "smoothed_main_player_box_candidate"
    )


def test_homography_matching_prefers_latest_prior_within_gap(db_session: Session) -> None:
    media = _seed_media(db_session)
    run, _ = _seed_homography_run(db_session, media.id, frame=0, timestamp_ms=0)
    _, _ = _seed_homography_run(
        db_session,
        media.id,
        run=run,
        frame=30,
        timestamp_ms=1000,
    )
    homographies = db_session.scalars(
        select(HomographyCandidateObservation).where(
            HomographyCandidateObservation.run_id == run.id
        )
    ).all()

    match = match_homography_for_timestamp(
        list(homographies),
        frame_number=31,
        timestamp_ms=1033,
        max_gap_ms=1500,
    )
    stale = match_homography_for_timestamp(
        list(homographies),
        frame_number=90,
        timestamp_ms=3000,
        max_gap_ms=500,
    )

    assert match is not None
    assert match.policy == "latest_prior_within_gap"
    assert match.time_delta_ms == 33
    assert match.carried_forward is True
    assert stale is None


def test_object_court_projection_plan_only_does_not_mutate(db_session: Session) -> None:
    result = project_objects_to_court(
        session=db_session,
        media_id="media-plan",
        motion_smoothing_run_id="motion-run-plan",
        homography_run_id="homography-run-plan",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "project-objects-to-court" in result["plan"]["command"]
    assert db_session.scalars(select(ProcessingRun)).all() == []


def test_cli_handler_exposes_project_objects_to_court(db_session: Session) -> None:
    class Args:
        media_id = "media-plan"
        motion_smoothing_run_id = "motion-run-plan"
        homography_run_id = "homography-run-plan"
        run_name = "object-to-court-projection-candidates-v0"
        homography_max_gap_ms = 1500
        viewer_base_url = "http://127.0.0.1:3000"
        plan_only = True

    result = _handle_project_objects_to_court(db_session, Args())

    assert result["ok"] is True
    assert result["status"] == "planned"


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/object-projection.mp4",
        duration_ms=2000,
        frame_count=60,
        fps=30.0,
        width=1000,
        height=500,
    )
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


def _seed_run(session: Session, media_id: str, run_name: str) -> ProcessingRun:
    run = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        metadata_jsonb={"test_run": True},
    )
    session.add(run)
    session.flush()
    return run


def _seed_motion_smoothing_run(
    session: Session,
    media_id: str,
) -> tuple[ProcessingRun, Observation, Observation]:
    run = _seed_run(session, media_id, "motion-smoothing")
    ball = _seed_observation(
        session,
        media_id=media_id,
        run_id=run.id,
        observation_type="smoothed_ball_position_candidate",
        frame=1,
        timestamp_ms=33,
        confidence=0.8,
        payload={
            "x": 100.0,
            "y": 200.0,
            "bbox": {"x": 95.0, "y": 195.0, "w": 10.0, "h": 10.0},
            "smoothing_method": "rolling_median_then_linear_interpolation_v0",
            "smoothed_candidate_only": True,
        },
    )
    player = _seed_observation(
        session,
        media_id=media_id,
        run_id=run.id,
        observation_type="smoothed_main_player_box_candidate",
        frame=1,
        timestamp_ms=33,
        confidence=0.7,
        payload={
            "bbox": {"x": 200.0, "y": 100.0, "w": 60.0, "h": 220.0},
            "track_candidate_id": "near_player_track_candidate_001",
            "track_role_candidate": "near_player_track_candidate",
            "source_main_player_track_run_id": "track-run",
            "smoothed_candidate_only": True,
        },
    )
    session.commit()
    return run, ball, player


def _seed_homography_run(
    session: Session,
    media_id: str,
    *,
    frame: int,
    timestamp_ms: int,
    run: ProcessingRun | None = None,
) -> tuple[ProcessingRun, str]:
    resolved_run = run or _seed_run(session, media_id, "homography")
    observation = _seed_observation(
        session,
        media_id=media_id,
        run_id=resolved_run.id,
        observation_type="homography_candidate_observation",
        frame=frame,
        timestamp_ms=timestamp_ms,
        confidence=0.9,
        payload={
            "homography_candidate": True,
            "candidate_geometry": True,
            "geometry_evidence_only": True,
        },
        family="court",
        coordinate_space="image_pixels",
    )
    homography = HomographyCandidateObservation(
        observation_id=observation.id,
        media_id=media_id,
        run_id=resolved_run.id,
        frame_number=frame,
        timestamp_ms=timestamp_ms,
        homography_matrix_jsonb=[
            [0.001, 0.0, 0.0],
            [0.0, 0.001, 0.0],
            [0.0, 0.0, 1.0],
        ],
        inverse_homography_matrix_jsonb=[
            [1000.0, 0.0, 0.0],
            [0.0, 1000.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        source_coordinate_space="image_pixels",
        target_coordinate_space="court_template_2d",
        matrix_direction="image_pixels_to_court_template_2d",
        template_name="tennis_court_template_normalized_v0",
        template_version="v0",
        source_point_count=12,
        source_line_count=8,
        confidence=0.9,
        status="candidate",
        metadata_jsonb={"candidate_geometry": True, "geometry_evidence_only": True},
    )
    session.add(homography)
    session.commit()
    return resolved_run, observation.id


def _seed_observation(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    observation_type: str,
    frame: int,
    timestamp_ms: int,
    confidence: float,
    payload: dict[str, object],
    family: str = "tracking",
    coordinate_space: str = "image_pixels",
) -> Observation:
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family=family,
        observation_type=observation_type,
        granularity="frame",
        frame_start=frame,
        frame_end=frame,
        timestamp_start_ms=timestamp_ms,
        timestamp_end_ms=timestamp_ms,
        confidence=confidence,
        coordinate_space=coordinate_space,
        payload_jsonb=payload,
    )
    session.add(observation)
    session.flush()
    return observation
