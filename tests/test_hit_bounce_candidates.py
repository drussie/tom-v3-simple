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

from apps.api.services.replay import (
    build_event_candidate_overlay_items,
    build_event_candidate_timeline_items,
)
from apps.worker.cli import _handle_build_hit_bounce_candidates
from apps.worker.services.hit_bounce_candidates import build_hit_bounce_candidates


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


def test_hit_candidate_near_player_direction_change_has_lineage(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, ball_projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.31, 0.22, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        candidate_dedupe_ms=500,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert result["observations"]["bounce_candidate"] == 0

    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert hit.observation_family == "event_candidate"
    assert hit.coordinate_space == "court_template_2d"
    assert hit.payload_jsonb["candidate_only"] is True
    assert hit.payload_jsonb["not_hit_truth"] is True
    assert hit.payload_jsonb["not_bounce_truth"] is True
    assert hit.payload_jsonb["not_in_out_truth"] is True
    assert "near_main_player_projection" in hit.payload_jsonb["reason_codes"]
    assert "net_axis_reversal" in hit.payload_jsonb["reason_codes"]
    assert "trajectory_direction_change" in hit.payload_jsonb["reason_codes"]
    assert hit.payload_jsonb["source_ball_court_projection_observation_id"] == (
        ball_projection_ids[1]
    )
    assert hit.payload_jsonb["net_axis_reversal"]["reversal"] is True
    assert hit.payload_jsonb["net_axis_reversal"]["axis"] == "court_y"

    lineage = db_session.scalars(
        select(ObservationLineage).where(ObservationLineage.child_observation_id == hit.id)
    ).all()
    assert {row.relationship_type for row in lineage} == {
        "candidate_from_ball_trajectory",
        "candidate_from_ball_court_projection",
        "candidate_from_main_player_court_projection",
    }


def test_hit_candidate_not_produced_when_player_is_far(db_session: Session) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.90, 0.90, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0


def test_bounce_candidate_away_from_players_direction_change(db_session: Session) -> None:
    media = _seed_media(db_session)
    trajectory_run, ball_projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (1, 33, 0.30, 0.35),
            (2, 66, 0.34, 0.30),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        ball_projection_ids,
        image_points=[(200.0, 100.0), (300.0, 190.0), (340.0, 120.0)],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.90, 0.90, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["bounce_candidate"] == 1
    bounce = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "bounce_candidate",
        )
    )
    assert bounce is not None
    assert "away_from_main_player_projection" in bounce.payload_jsonb["reason_codes"]
    assert "descending_to_ascending_image_proxy" in bounce.payload_jsonb["reason_codes"]
    assert "speed_reduction_candidate" in bounce.payload_jsonb["reason_codes"]
    assert bounce.payload_jsonb["not_bounce_truth"] is True
    assert bounce.payload_jsonb["vertical_motion_proxy"][
        "descending_to_ascending"
    ] is True
    assert bounce.payload_jsonb["vertical_motion_proxy"]["image_y_current"] == 190.0
    assert bounce.payload_jsonb["speed_reduction"]["speed_reduced"] is True


def test_bounce_candidate_requires_speed_reduction(db_session: Session) -> None:
    media = _seed_media(db_session)
    trajectory_run, ball_projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (1, 33, 0.21, 0.35),
            (2, 66, 0.60, 0.30),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        ball_projection_ids,
        image_points=[(200.0, 100.0), (210.0, 190.0), (600.0, 120.0)],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.90, 0.90, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["bounce_candidate"] == 0


def test_bounce_candidate_requires_descending_ascending_proxy(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, ball_projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (1, 33, 0.30, 0.35),
            (2, 66, 0.34, 0.40),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        ball_projection_ids,
        image_points=[(200.0, 100.0), (300.0, 190.0), (340.0, 220.0)],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.90, 0.90, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["bounce_candidate"] == 0


def test_player_proximate_trajectory_change_is_prioritized_as_hit(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.56, 0.39, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert result["observations"]["bounce_candidate"] == 0
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert "player_proximate_event_priority" in hit.payload_jsonb["reason_codes"]
    assert hit.payload_jsonb["classification_priority"] == "hit_first_when_player_proximate"
    assert hit.payload_jsonb["player_proximity_gate"]["threshold"] == 0.33
    assert hit.payload_jsonb["candidate_decision"]["suppressed_candidate_types"] == [
        "bounce_candidate"
    ]


def test_conflict_resolution_prefers_hit_over_same_window_bounce(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
            (8, 250, 0.60, 0.30),
            (9, 300, 0.70, 0.55),
            (10, 350, 0.75, 0.50),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.31, 0.22, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        candidate_dedupe_ms=500,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert result["observations"]["bounce_candidate"] == 0
    assert result["candidate_summary"]["suppressed_bounce_conflict_count"] >= 1


def test_candidate_dedupe_keeps_highest_confidence_per_window(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
            (3, 99, 0.50, 0.20),
            (4, 132, 0.60, 0.35),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[
            (1, 33, 0.36, 0.22, "near_player_track_candidate"),
            (2, 66, 0.40, 0.36, "near_player_track_candidate"),
            (3, 99, 0.50, 0.22, "near_player_track_candidate"),
        ],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        candidate_dedupe_ms=500,
    )

    assert result["ok"] is True
    assert result["candidate_summary"]["hit_candidate_count"] == 3
    assert result["candidate_summary"]["deduped_hit_candidate_count"] == 1
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert "player_proximate_event_priority" in hit.payload_jsonb["reason_codes"]


def test_event_candidate_replay_payloads_are_exposed(db_session: Session) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.31, 0.22, "far_player_track_candidate")],
    )
    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    overlays = build_event_candidate_overlay_items(
        session=db_session,
        media=media,
        start_ms=0,
        end_ms=200,
        event_candidate_run_id=result["event_candidate_run_id"],
        observation_type="hit_candidate",
    )
    timeline_items = build_event_candidate_timeline_items(
        session=db_session,
        media=media,
        event_candidate_run_id=result["event_candidate_run_id"],
    )

    assert len(overlays) == 1
    assert overlays[0]["overlay_type"] == "hit_candidate"
    assert overlays[0]["court_point"] == {"x": 0.3, "y": 0.2}
    assert overlays[0]["image_point"] == {"x": 300.0, "y": 100.0}
    assert overlays[0]["image_marker_source"] == "source_ball_court_projection_image_point"
    assert overlays[0]["classification_priority"] == "hit_first_when_player_proximate"
    assert overlays[0]["player_proximity_gate"]["nearest_player_found"] is True
    assert overlays[0]["candidate_decision"]["selected_candidate_type"] == "hit_candidate"
    assert overlays[0]["net_axis_reversal"]["reversal"] is True
    assert overlays[0]["vertical_motion_proxy"] is None
    assert overlays[0]["speed_reduction"] is None
    assert len(timeline_items) == 1
    assert timeline_items[0]["item_type"] == "hit_candidate"
    assert timeline_items[0]["image_point"] == {"x": 300.0, "y": 100.0}
    assert timeline_items[0]["image_marker_source"] == "source_ball_court_projection_image_point"
    assert timeline_items[0]["classification_priority"] == "hit_first_when_player_proximate"
    assert timeline_items[0]["net_axis_reversal"]["axis"] == "court_y"
    assert timeline_items[0]["candidate_only"] is True

    persistent_overlays = build_event_candidate_overlay_items(
        session=db_session,
        media=media,
        start_ms=1000,
        end_ms=1200,
        event_candidate_run_id=result["event_candidate_run_id"],
        observation_type="hit_candidate",
    )
    assert [item["observation_id"] for item in persistent_overlays] == [
        overlays[0]["observation_id"]
    ]


def test_event_candidate_replay_payload_handles_missing_source_image_point(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, ball_projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.35),
            (1, 33, 0.30, 0.20),
            (2, 66, 0.40, 0.35),
        ],
    )
    source_projection = db_session.get(Observation, ball_projection_ids[1])
    assert source_projection is not None
    source_payload = dict(source_projection.payload_jsonb or {})
    source_payload.pop("image_point", None)
    source_projection.payload_jsonb = source_payload
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(1, 33, 0.31, 0.22, "far_player_track_candidate")],
    )
    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    overlays = build_event_candidate_overlay_items(
        session=db_session,
        media=media,
        start_ms=0,
        end_ms=200,
        event_candidate_run_id=result["event_candidate_run_id"],
        observation_type="hit_candidate",
    )

    assert len(overlays) == 1
    assert overlays[0]["image_point"] is None
    assert overlays[0]["image_marker_source"] == "unavailable"


def test_hit_bounce_candidate_plan_only_and_cli_do_not_mutate(
    db_session: Session,
) -> None:
    result = build_hit_bounce_candidates(
        session=db_session,
        media_id="media-plan",
        ball_trajectory_run_id="trajectory-plan",
        court_projection_run_id="projection-plan",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "build-hit-bounce-candidates" in result["plan"]["command"]
    assert "--hit-min-net-axis-delta-template 0.015" in result["plan"]["command"]
    assert "--bounce-min-image-y-delta-pixels 2.0" in result["plan"]["command"]
    assert db_session.scalars(select(ProcessingRun)).all() == []

    class Args:
        media_id = "media-plan"
        ball_trajectory_run_id = "trajectory-plan"
        court_projection_run_id = "projection-plan"
        run_name = "hit-bounce-candidate-evidence-v0"
        hit_player_distance_max_template = 0.18
        bounce_player_distance_min_template = 0.18
        hit_min_direction_delta_degrees = 25.0
        bounce_min_direction_delta_degrees = 20.0
        hit_min_net_axis_delta_template = 0.015
        bounce_min_image_y_delta_pixels = 2.0
        bounce_min_speed_reduction_fraction = 0.05
        candidate_dedupe_ms = 500
        viewer_base_url = "http://127.0.0.1:3000"
        plan_only = True

    cli_result = _handle_build_hit_bounce_candidates(db_session, Args())

    assert cli_result["ok"] is True
    assert cli_result["status"] == "planned"


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/hit-bounce-candidates.mp4",
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


def _seed_trajectory_run(
    session: Session,
    media_id: str,
    *,
    points: list[tuple[int, int, float, float]],
) -> tuple[ProcessingRun, list[str]]:
    projection_ids: list[str] = []
    for frame, timestamp_ms, court_x, court_y in points:
        projection = _seed_ball_projection(
            session,
            media_id=media_id,
            frame=frame,
            timestamp_ms=timestamp_ms,
            court_x=court_x,
            court_y=court_y,
        )
        projection_ids.append(projection.id)
    run = _seed_run(session, media_id, "ball-trajectory")
    payload_points = [
        {
            "frame_number": frame,
            "timestamp_ms": timestamp_ms,
            "court_x": court_x,
            "court_y": court_y,
            "source_observation_id": source_id,
            "source_homography_observation_id": f"homography-{frame}",
            "homography_time_delta_ms": 0,
            "homography_carried_forward": False,
            "inside_template_bounds": 0.0 <= court_x <= 1.0 and 0.0 <= court_y <= 1.0,
        }
        for (frame, timestamp_ms, court_x, court_y), source_id in zip(
            points, projection_ids, strict=True
        )
    ]
    observation = Observation(
        media_id=media_id,
        run_id=run.id,
        observation_family="trajectory",
        observation_type="ball_trajectory_court_candidate",
        granularity="segment",
        frame_start=points[0][0],
        frame_end=points[-1][0],
        timestamp_start_ms=points[0][1],
        timestamp_end_ms=points[-1][1],
        confidence=0.7,
        coordinate_space="court_template_2d",
        payload_jsonb={
            "source_court_projection_run_id": "projection-run",
            "points": payload_points,
            "point_count": len(payload_points),
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
    session.commit()
    return run, projection_ids


def _seed_ball_projection(
    session: Session,
    *,
    media_id: str,
    frame: int,
    timestamp_ms: int,
    court_x: float,
    court_y: float,
) -> Observation:
    run = _seed_run(session, media_id, f"ball-projection-{frame}")
    observation = Observation(
        media_id=media_id,
        run_id=run.id,
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
            "image_point": {"x": court_x * 1000.0, "y": court_y * 500.0},
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


def _update_ball_projection_image_points(
    session: Session,
    projection_ids: list[str],
    *,
    image_points: list[tuple[float, float]],
) -> None:
    for projection_id, (image_x, image_y) in zip(
        projection_ids,
        image_points,
        strict=True,
    ):
        observation = session.get(Observation, projection_id)
        assert observation is not None
        payload = dict(observation.payload_jsonb or {})
        payload["image_point"] = {"x": image_x, "y": image_y}
        observation.payload_jsonb = payload
    session.commit()


def _seed_projection_run(
    session: Session,
    media_id: str,
    *,
    players: list[tuple[int, int, float, float, str]],
) -> ProcessingRun:
    run = _seed_run(session, media_id, "court-projection")
    for index, (frame, timestamp_ms, court_x, court_y, role) in enumerate(players):
        observation = Observation(
            media_id=media_id,
            run_id=run.id,
            observation_family="projection",
            observation_type="main_player_court_projection_candidate",
            granularity="frame",
            frame_start=frame,
            frame_end=frame,
            timestamp_start_ms=timestamp_ms,
            timestamp_end_ms=timestamp_ms,
            confidence=0.75,
            coordinate_space="court_template_2d",
            payload_jsonb={
                "court_point": {"x": court_x, "y": court_y},
                "track_candidate_id": f"{role}_001",
                "track_role_candidate": role,
                "source_label": "main player court projection candidate",
                "projection_candidate_only": True,
                "not_player_truth": True,
                "not_identity_truth": True,
                "not_court_truth": True,
                "observation_only": True,
                "no_adjudication": True,
            },
            idempotency_key=f"projection:{run.id}:{index}",
        )
        session.add(observation)
    session.commit()
    return run
