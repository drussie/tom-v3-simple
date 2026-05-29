from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    MediaAsset,
    Observation,
    ObservationLineage,
    ProcessingRun,
)

from apps.worker.cli import _handle_build_ball_court_trajectory
from apps.worker.services.ball_court_trajectory import (
    BallTrajectoryConfig,
    build_ball_court_trajectory,
    compute_trajectory_kinematics,
    segment_ball_court_projection_points,
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


def test_ball_court_trajectory_creates_segment_with_kinematics_and_lineage(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    projection_run = _seed_run(db_session, media.id, "court-projection")
    points = [
        _seed_ball_projection(
            db_session,
            media_id=media.id,
            run_id=projection_run.id,
            frame=frame,
            timestamp_ms=frame * 33,
            court_x=0.1 + frame * 0.01,
            court_y=0.2 + frame * 0.02,
        )
        for frame in range(5)
    ]
    db_session.commit()

    result = build_ball_court_trajectory(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=projection_run.id,
        max_gap_frames=6,
        max_gap_ms=250,
        min_points_per_segment=3,
    )

    assert result["ok"] is True
    assert result["observations"] == {
        "ball_trajectory_court_candidate": 1,
        "total": 1,
    }
    assert result["trajectory_summary"]["source_point_count"] == 5
    assert result["trajectory_summary"]["persisted_segment_count"] == 1

    trajectory = db_session.scalar(
        select(Observation).where(Observation.run_id == result["ball_trajectory_run_id"])
    )
    assert trajectory is not None
    assert trajectory.observation_family == "trajectory"
    assert trajectory.observation_type == "ball_trajectory_court_candidate"
    assert trajectory.granularity == "segment"
    assert trajectory.coordinate_space == "court_template_2d"
    assert trajectory.frame_start == 0
    assert trajectory.frame_end == 4
    assert trajectory.payload_jsonb["point_count"] == 5
    assert len(trajectory.payload_jsonb["points"]) == 5
    assert len(trajectory.payload_jsonb["kinematics"]) == 4
    assert trajectory.payload_jsonb["diagnostics"]["gap_count"] == 0
    assert trajectory.payload_jsonb["trajectory_candidate_only"] is True
    assert trajectory.payload_jsonb["not_ball_truth"] is True
    assert trajectory.payload_jsonb["not_bounce_truth"] is True
    assert trajectory.payload_jsonb["not_hit_truth"] is True
    assert trajectory.payload_jsonb["not_in_out_truth"] is True

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == trajectory.id
        )
    ).all()
    assert len(lineage) == len(points)
    assert {row.parent_observation_id for row in lineage} == {point.id for point in points}
    assert {row.relationship_type for row in lineage} == {
        "trajectory_from_ball_court_projection"
    }


def test_ball_court_trajectory_splits_gaps_and_drops_short_segments(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    projection_run = _seed_run(db_session, media.id, "court-projection")
    for frame in (0, 1, 2, 20, 21):
        _seed_ball_projection(
            db_session,
            media_id=media.id,
            run_id=projection_run.id,
            frame=frame,
            timestamp_ms=frame * 33,
            court_x=0.2,
            court_y=0.3,
        )
    db_session.commit()

    result = build_ball_court_trajectory(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=projection_run.id,
        max_gap_frames=3,
        max_gap_ms=250,
        min_points_per_segment=3,
    )

    assert result["ok"] is True
    assert result["trajectory_summary"]["source_point_count"] == 5
    assert result["trajectory_summary"]["segment_count"] == 2
    assert result["trajectory_summary"]["persisted_segment_count"] == 1
    assert result["trajectory_summary"]["dropped_short_segment_count"] == 1
    assert result["trajectory_summary"]["gap_split_count"] == 1


def test_ball_court_trajectory_flags_out_of_template_points(db_session: Session) -> None:
    media = _seed_media(db_session)
    projection_run = _seed_run(db_session, media.id, "court-projection")
    for frame, x in enumerate((0.2, 1.2, 0.4)):
        _seed_ball_projection(
            db_session,
            media_id=media.id,
            run_id=projection_run.id,
            frame=frame,
            timestamp_ms=frame * 33,
            court_x=x,
            court_y=0.5,
        )
    db_session.commit()

    result = build_ball_court_trajectory(
        session=db_session,
        media_id=media.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    trajectory = db_session.scalar(
        select(Observation).where(Observation.run_id == result["ball_trajectory_run_id"])
    )
    assert trajectory is not None
    assert trajectory.payload_jsonb["diagnostics"]["out_of_template_count"] == 1
    assert any(
        point["inside_template_bounds"] is False
        for point in trajectory.payload_jsonb["points"]
    )


def test_ball_court_trajectory_segment_helpers_are_deterministic(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    projection_run = _seed_run(db_session, media.id, "court-projection")
    raw_points = [
        _seed_ball_projection(
            db_session,
            media_id=media.id,
            run_id=projection_run.id,
            frame=frame,
            timestamp_ms=frame * 33,
            court_x=0.1 + frame * 0.01,
            court_y=0.2,
        )
        for frame in (2, 0, 1)
    ]
    db_session.commit()
    from apps.worker.services.ball_court_trajectory import _point_from_observation

    points = [
        point
        for raw_point in raw_points
        if (point := _point_from_observation(raw_point)) is not None
    ]
    segmented = segment_ball_court_projection_points(
        points,
        BallTrajectoryConfig(max_gap_frames=6, max_gap_ms=250, min_points_per_segment=3),
    )
    kinematics = compute_trajectory_kinematics(segmented.persisted_segments[0])

    assert [point.frame_number for point in segmented.persisted_segments[0]] == [0, 1, 2]
    assert len(kinematics) == 2
    assert kinematics[0]["dt_ms"] == 33
    assert kinematics[0]["dx"] == pytest.approx(0.01)
    assert "speed_template_units_per_second" in kinematics[0]
    assert "direction_angle_degrees" in kinematics[0]


def test_ball_court_trajectory_plan_only_and_cli_do_not_mutate(db_session: Session) -> None:
    result = build_ball_court_trajectory(
        session=db_session,
        media_id="media-plan",
        court_projection_run_id="court-projection-plan",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "build-ball-court-trajectory" in result["plan"]["command"]
    assert db_session.scalars(select(ProcessingRun)).all() == []

    class Args:
        media_id = "media-plan"
        court_projection_run_id = "court-projection-plan"
        run_name = "ball-trajectory-court-candidate-v0"
        max_gap_frames = 6
        max_gap_ms = 250
        min_points_per_segment = 3
        viewer_base_url = "http://127.0.0.1:3000"
        plan_only = True

    cli_result = _handle_build_ball_court_trajectory(db_session, Args())

    assert cli_result["ok"] is True
    assert cli_result["status"] == "planned"


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/ball-trajectory.mp4",
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


def _seed_ball_projection(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    frame: int,
    timestamp_ms: int,
    court_x: float,
    court_y: float,
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
            "court_point": {"x": court_x, "y": court_y},
            "source_homography_observation_id": f"homography-{frame}",
            "homography_time_delta_ms": frame * 10,
            "homography_carried_forward": frame > 0,
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
