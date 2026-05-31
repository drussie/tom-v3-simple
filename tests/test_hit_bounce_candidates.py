from __future__ import annotations

from collections.abc import Generator
from dataclasses import replace
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
    build_event_candidate_marker_summary,
    build_event_candidate_overlay_items,
    build_event_candidate_timeline_items,
    build_replay_overlay_chunk,
    build_replay_timeline,
)
from apps.worker.cli import (
    _format_hit_bounce_cli_result,
    _handle_build_hit_bounce_candidates,
)
from apps.worker.services.hit_bounce_candidates import (
    BOUNCE_CANDIDATE_METHOD,
    HIT_CANDIDATE_METHOD,
    HIT_FALLBACK_CANDIDATE_METHOD,
    IMAGE_SPACE_DIRECTION_CHANGE_HIT_CANDIDATE_METHOD,
    IMAGE_SPACE_NET_AXIS_HIT_CANDIDATE_METHOD,
    LOCAL_EVIDENCE_DIRECTION_CHANGE_BOUNCE_CANDIDATE_METHOD,
    MARKER_LEVEL_ARBITRATION_PRIORITY,
    NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD,
    PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
    SIDE_ZONE_SEQUENCE_BOUNCE_METHOD,
    SIDE_ZONE_SEQUENCE_HIT_METHOD,
    UNIVERSAL_HIT_GUARD_BOUNCE_CANDIDATE_METHOD,
    UNIVERSAL_HIT_VALIDITY_GUARD_PRIORITY,
    EventCandidateDraft,
    HitBounceCandidateConfig,
    NearestPlayerContext,
    PlayerProjection,
    TrajectoryContext,
    TrajectoryPoint,
    apply_marker_level_event_arbitration,
    apply_side_zone_sequence_classification,
    apply_universal_hit_candidate_validity_guard,
    build_hit_bounce_candidates,
    dedupe_event_candidates_with_rejections,
    suppress_player_anchored_hits_overlapping_bounces,
    suppress_weak_image_space_direction_change_hits_overlapping_bounces,
    suppress_weak_net_axis_reversal_hits_overlapping_bounces,
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
        players=[(1, 33, 0.31, 0.22, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        candidate_dedupe_ms=500,
        hit_player_time_window_ms=40,
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
        image_space_direction_change_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0


def test_net_axis_reversal_emits_hit_without_player_proximity(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.30),
            (6, 200, 0.30, 0.70),
            (12, 400, 0.40, 0.30),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_direction_change_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert result["candidate_summary"]["net_axis_reversal_recovered_hit_count"] == 1
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert hit.payload_jsonb["candidate_method"] == NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD
    assert "player_proximity_not_required" in hit.payload_jsonb["reason_codes"]
    assert hit.payload_jsonb["source_player_court_projection_observation_id"] is None
    assert hit.payload_jsonb["net_axis_reversal_recall"][
        "player_proximity_required"
    ] is False
    assert hit.payload_jsonb["net_axis_reversal_recall"]["net_axis_reversal"] is True


def test_net_axis_reversal_player_proximity_boosts_confidence(
    db_session: Session,
) -> None:
    media_without_player = _seed_media(db_session)
    trajectory_without_player, _ = _seed_trajectory_run(
        db_session,
        media_without_player.id,
        points=[
            (0, 0, 0.20, 0.50),
            (6, 200, 0.25, 0.53),
            (12, 400, 0.30, 0.50),
        ],
    )
    projection_without_player = _seed_projection_run(
        db_session,
        media_without_player.id,
        players=[],
    )
    result_without_player = build_hit_bounce_candidates(
        session=db_session,
        media_id=media_without_player.id,
        ball_trajectory_run_id=trajectory_without_player.id,
        court_projection_run_id=projection_without_player.id,
    )
    hit_without_player = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result_without_player["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit_without_player is not None

    media_with_player = _seed_media(db_session)
    trajectory_with_player, _ = _seed_trajectory_run(
        db_session,
        media_with_player.id,
        points=[
            (0, 0, 0.20, 0.50),
            (6, 200, 0.25, 0.53),
            (12, 400, 0.30, 0.50),
        ],
    )
    projection_with_player = _seed_projection_run(
        db_session,
        media_with_player.id,
        players=[(9, 300, 0.25, 0.53, "far_player_track_candidate")],
    )
    result_with_player = build_hit_bounce_candidates(
        session=db_session,
        media_id=media_with_player.id,
        ball_trajectory_run_id=trajectory_with_player.id,
        court_projection_run_id=projection_with_player.id,
        hit_player_time_window_ms=40,
    )
    hit_with_player = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result_with_player["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit_with_player is not None

    assert hit_with_player.confidence > hit_without_player.confidence
    assert hit_with_player.payload_jsonb["net_axis_reversal_recall"][
        "player_proximity_required"
    ] is False
    assert hit_with_player.payload_jsonb["net_axis_reversal_recall"][
        "nearest_player_found"
    ] is True


def test_no_net_axis_reversal_does_not_emit_ball_first_hit(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (6, 200, 0.30, 0.40),
            (12, 400, 0.40, 0.60),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_direction_change_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert result["candidate_summary"]["net_axis_reversal_recovered_hit_count"] == 0
    assert "no_net_axis_reversal" in result["candidate_summary"][
        "net_axis_reversal_rejection_reasons"
    ]


def test_image_space_net_axis_reversal_emits_hit_without_player_proximity(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.48),
            (6, 200, 0.30, 0.50),
            (12, 400, 0.40, 0.52),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        projection_ids,
        image_points=[
            (100.0, 100.0),
            (120.0, 150.0),
            (140.0, 110.0),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_direction_change_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert (
        result["candidate_summary"]["image_net_axis_reversal_recovered_hit_count"]
        == 1
    )
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert hit.payload_jsonb["candidate_method"] == (
        IMAGE_SPACE_NET_AXIS_HIT_CANDIDATE_METHOD
    )
    recall = hit.payload_jsonb["image_space_net_axis_reversal_recall"]
    assert recall["player_proximity_required"] is False
    assert recall["image_axis_method"] == "broadcast_image_y_axis_fallback_v026"
    assert recall["image_axis_reversal"] is True
    assert hit.payload_jsonb["source_player_court_projection_observation_id"] is None
    assert "airborne_hit_projection_warning" in hit.payload_jsonb["reason_codes"]


def test_image_space_reversal_missing_image_points_writes_diagnostics(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.48),
            (6, 200, 0.30, 0.50),
            (12, 400, 0.40, 0.52),
        ],
    )
    _remove_ball_projection_image_points(db_session, projection_ids)
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_direction_change_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert "missing_image_point" in result["candidate_summary"][
        "image_net_axis_reversal_rejection_reasons"
    ]
    diagnostic = next(
        (
            row
            for row in db_session.scalars(
                select(Observation).where(
                    Observation.run_id == result["event_candidate_run_id"],
                    Observation.observation_type
                    == "event_candidate_rejection_diagnostic",
                )
            )
            if row.payload_jsonb.get("diagnostic_source")
            == "image_space_net_axis_hit_recall"
        ),
        None,
    )
    assert diagnostic is not None
    assert diagnostic.payload_jsonb["image_space_net_axis_reversal_recall"][
        "player_proximity_required"
    ] is False


def test_image_space_recall_uses_projection_points_outside_trajectory_segments(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (6, 200, 0.30, 0.30),
            (12, 400, 0.40, 0.40),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])
    projection_ids = _seed_ball_projection_rows(
        db_session,
        media_id=media.id,
        run_id=projection_run.id,
        points=[
            (34, 1133, 0.44, 0.90, 905.0, 324.0),
            (54, 1800, 0.45, 0.90, 900.0, 324.0),
            (55, 1833, 0.49, 1.04, 952.0, 244.0),
            (66, 2200, 0.40, 0.87, 854.0, 338.0),
        ],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_direction_change_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert result["candidate_summary"][
        "image_net_axis_reversal_source_point_count"
    ] == 4
    assert (
        result["candidate_summary"]["image_net_axis_reversal_recovered_hit_count"]
        == 1
    )
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert hit.payload_jsonb["candidate_method"] == (
        IMAGE_SPACE_NET_AXIS_HIT_CANDIDATE_METHOD
    )
    assert hit.payload_jsonb["source_ball_trajectory_observation_id"] is None
    assert hit.payload_jsonb["source_ball_court_projection_observation_id"] == (
        projection_ids[2]
    )
    lineage = db_session.scalars(
        select(ObservationLineage).where(ObservationLineage.child_observation_id == hit.id)
    ).all()
    assert {row.relationship_type for row in lineage} == {
        "candidate_from_ball_court_projection"
    }
    overlays = build_event_candidate_overlay_items(
        session=db_session,
        media=media,
        start_ms=0,
        end_ms=2400,
        event_candidate_run_id=result["event_candidate_run_id"],
        observation_type="hit_candidate",
    )
    assert overlays[0]["image_point"] == {"x": 952.0, "y": 244.0}
    assert overlays[0]["image_space_net_axis_reversal_recall"][
        "player_proximity_required"
    ] is False


def test_image_space_direction_change_midcourt_transit_is_guarded(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.48),
            (6, 200, 0.30, 0.50),
            (12, 400, 0.40, 0.52),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        projection_ids,
        image_points=[
            (100.0, 100.0),
            (140.0, 140.0),
            (120.0, 190.0),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert result["candidate_summary"]["hit_candidates_suppressed_by_guard"] == 1
    assert (
        result["candidate_summary"]["image_direction_change_recovered_hit_count"]
        == 0
    )
    assert (
        result["candidate_summary"]["image_direction_change_candidate_count"]
        == 1
    )
    assert (
        result["candidate_summary"]["image_net_axis_reversal_recovered_hit_count"]
        == 0
    )
    diagnostic = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "event_candidate_rejection_diagnostic",
            Observation.payload_jsonb["candidate_decision"]["reason"].as_string()
            == "suppressed_by_universal_hit_validity_guard",
        )
    )
    assert diagnostic is not None
    assert "fly_through_no_local_reversal" in diagnostic.payload_jsonb[
        "rejection_reasons"
    ]
    recall = diagnostic.payload_jsonb["image_space_direction_change_recall"]
    assert recall["player_proximity_required"] is False
    assert recall["image_direction_change_method"] == (
        "broadcast_image_2d_vector_direction_change_v027"
    )
    assert recall["image_direction_delta_degrees"] >= 45.0
    assert recall["pre_vector_length_pixels"] >= 8.0
    assert recall["post_vector_length_pixels"] >= 8.0
    assert diagnostic.payload_jsonb["local_evidence_event_type"][
        "hit_requires_prior_bounce"
    ] is False
    assert diagnostic.payload_jsonb["local_evidence_event_type"][
        "selected_candidate_type"
    ] == "hit_candidate"


def test_image_space_direction_change_in_landing_zone_reclassifies_to_bounce(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (6, 200, 0.30, 0.30),
            (12, 400, 0.40, 0.40),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        projection_ids,
        image_points=[
            (100.0, 100.0),
            (140.0, 140.0),
            (120.0, 190.0),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert result["observations"]["bounce_candidate"] == 1
    assert (
        result["candidate_summary"]["direction_change_reclassified_to_bounce_count"]
        == 1
    )
    bounce = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "bounce_candidate",
        )
    )
    assert bounce is not None
    assert bounce.payload_jsonb["candidate_method"] == (
        LOCAL_EVIDENCE_DIRECTION_CHANGE_BOUNCE_CANDIDATE_METHOD
    )
    assert "direction_change_reclassified_to_bounce_candidate" in bounce.payload_jsonb[
        "reason_codes"
    ]
    local_evidence = bounce.payload_jsonb["local_evidence_event_type"]
    assert local_evidence["selected_candidate_type"] == "bounce_candidate"
    assert local_evidence["bounce_like_court_landing_zone"] is True
    assert local_evidence["sequence_is_hard_gate"] is False
    assert local_evidence["hit_requires_prior_bounce"] is False


def test_image_space_direction_change_missing_image_points_writes_diagnostics(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (6, 200, 0.30, 0.30),
            (12, 400, 0.40, 0.40),
        ],
    )
    _remove_ball_projection_image_points(db_session, projection_ids)
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert "missing_image_point" in result["candidate_summary"][
        "image_direction_change_rejection_reasons"
    ]
    diagnostic = next(
        (
            row
            for row in db_session.scalars(
                select(Observation).where(
                    Observation.run_id == result["event_candidate_run_id"],
                    Observation.observation_type
                    == "event_candidate_rejection_diagnostic",
                )
            )
            if row.payload_jsonb.get("diagnostic_source")
            == "image_space_direction_change_hit_recall"
        ),
        None,
    )
    assert diagnostic is not None
    assert diagnostic.payload_jsonb["image_space_direction_change_recall"][
        "player_proximity_required"
    ] is False


def test_image_space_direction_change_below_vector_threshold_rejects(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (6, 200, 0.30, 0.30),
            (12, 400, 0.40, 0.40),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        projection_ids,
        image_points=[
            (100.0, 100.0),
            (103.0, 103.0),
            (101.0, 106.0),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_net_axis_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert "image_vector_below_threshold" in result["candidate_summary"][
        "image_direction_change_rejection_reasons"
    ]


def test_image_space_direction_change_below_delta_rejects(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (6, 200, 0.30, 0.30),
            (12, 400, 0.40, 0.40),
        ],
    )
    _update_ball_projection_image_points(
        db_session,
        projection_ids,
        image_points=[
            (100.0, 100.0),
            (130.0, 130.0),
            (170.0, 160.0),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        image_space_net_axis_hit_enabled=False,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert "image_direction_delta_below_threshold" in result["candidate_summary"][
        "image_direction_change_rejection_reasons"
    ]


def test_far_side_style_player_time_offset_hit_fallback(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (27, 900, 0.4350, 0.8510),
            (28, 933, 0.4374, 0.8603),
            (29, 967, 0.4398, 0.8696),
            (30, 1000, 0.4420, 0.8880),
            (31, 1033, 0.4434, 0.8939),
            (32, 1067, 0.4447, 0.8986),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(29, 967, 0.442, 0.750, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=300,
        candidate_dedupe_ms=500,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 0
    assert result["observations"]["bounce_candidate"] == 1
    assert result["candidate_summary"][
        "hit_candidates_reclassified_to_bounce_by_guard"
    ] == 1
    bounce = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "bounce_candidate",
        )
    )
    assert bounce is not None
    assert bounce.payload_jsonb["candidate_method"] == (
        UNIVERSAL_HIT_GUARD_BOUNCE_CANDIDATE_METHOD
    )
    assert "player_proximate_speed_change_fallback" in bounce.payload_jsonb[
        "reason_codes"
    ]
    assert bounce.payload_jsonb["net_axis_reversal"]["reversal"] is False
    assert bounce.payload_jsonb["nearest_player"]["track_role_candidate"] == (
        "far_player_track_candidate"
    )


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


def test_bounce_fallback_is_low_confidence_and_labeled_when_image_proxy_missing(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, ball_projection_ids = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (1, 33, 0.30, 0.50),
            (2, 66, 0.35, 0.50),
        ],
    )
    _remove_ball_projection_image_points(db_session, ball_projection_ids)
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
    assert bounce.confidence <= 0.42
    assert bounce.payload_jsonb["candidate_method"].endswith("_fallback")
    assert "vertical_proxy_partial_or_unavailable" in bounce.payload_jsonb["reason_codes"]


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
    assert hit.payload_jsonb["classification_priority"] == MARKER_LEVEL_ARBITRATION_PRIORITY
    assert hit.payload_jsonb["marker_level_arbitration"]["decision"] == "keep_hit"
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
        hit_player_time_window_ms=40,
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
        hit_player_time_window_ms=40,
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


def test_dedupe_preserves_one_pre_anchor_landing_candidate_for_sequence_prior() -> None:
    config = HitBounceCandidateConfig()
    near_hit = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=10,
            timestamp_ms=333,
            court_x=0.30,
            court_y=0.20,
            track_role_candidate="near_player_track_candidate",
            player_distance=0.16,
            candidate_method=HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        confidence=0.65,
    )
    pre_anchor_landing = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=30,
            timestamp_ms=1000,
            court_x=0.44,
            court_y=0.88,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.14,
            candidate_method=HIT_FALLBACK_CANDIDATE_METHOD,
            net_axis_reversal=False,
        ),
        confidence=0.46,
    )
    lower_pre_anchor_landing = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=29,
            timestamp_ms=967,
            court_x=0.44,
            court_y=0.87,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.15,
            candidate_method=HIT_FALLBACK_CANDIDATE_METHOD,
            net_axis_reversal=False,
        ),
        confidence=0.44,
    )
    anchored_hit = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=34,
            timestamp_ms=1133,
            court_x=0.45,
            court_y=0.90,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.13,
            candidate_method=PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        confidence=0.70,
    )

    deduped, rejections = dedupe_event_candidates_with_rejections(
        [
            near_hit,
            pre_anchor_landing,
            lower_pre_anchor_landing,
            anchored_hit,
        ],
        candidate_dedupe_ms=500,
    )

    assert [
        (candidate.frame_number, candidate.candidate_method) for candidate in deduped
    ] == [
        (10, HIT_CANDIDATE_METHOD),
        (30, HIT_FALLBACK_CANDIDATE_METHOD),
        (34, PLAYER_ANCHORED_HIT_CANDIDATE_METHOD),
    ]
    assert any(
        "deduped_by_player_anchored_hit" in diagnostic.rejection_reasons
        for diagnostic in rejections
    )

    final_candidates, summary = apply_side_zone_sequence_classification(
        deduped,
        config=config,
    )

    assert [
        candidate.observation_type for candidate in final_candidates
    ] == [
        "hit_candidate",
        "hit_candidate",
        "hit_candidate",
    ]
    assert summary["reclassified_hit_to_bounce_count"] == 0
    assert summary["sequence_prior_applied_count"] == 0


def test_rejected_contexts_persist_rejection_reason_diagnostics(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (0, 0, 0.20, 0.20),
            (1, 33, 0.30, 0.30),
            (2, 66, 0.40, 0.40),
        ],
    )
    projection_run = _seed_projection_run(db_session, media.id, players=[])

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    assert result["ok"] is True
    assert result["observations"]["event_candidate_rejection_diagnostic"] >= 1
    assert result["candidate_summary"]["rejected_context_count"] >= 1
    assert "no_nearest_player_in_time_window" in result["candidate_summary"][
        "rejection_reasons"
    ]
    diagnostics = db_session.scalars(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "event_candidate_rejection_diagnostic",
        )
    ).all()
    diagnostic = next(
        row
        for row in diagnostics
        if row.payload_jsonb["candidate_decision"]["reason"] == "rejected"
    )
    assert diagnostic is not None
    assert diagnostic.payload_jsonb["candidate_decision"]["reason"] == "rejected"
    assert diagnostic.payload_jsonb["diagnostic_only"] is True
    assert diagnostic.payload_jsonb["not_hit_truth"] is True
    assert diagnostic.payload_jsonb["not_bounce_truth"] is True


def test_dedupe_does_not_suppress_valid_far_side_event_from_near_side_event(
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
            (29, 967, 0.4398, 0.8696),
            (30, 1000, 0.4420, 0.8880),
            (31, 1033, 0.4434, 0.8390),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[
            (1, 33, 0.31, 0.22, "near_player_track_candidate"),
            (29, 967, 0.442, 0.750, "far_player_track_candidate"),
        ],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        candidate_dedupe_ms=500,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 2
    hits = db_session.scalars(
        select(Observation)
        .where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
        .order_by(Observation.timestamp_start_ms)
    ).all()
    assert [hit.payload_jsonb["nearest_player"]["track_role_candidate"] for hit in hits] == [
        "near_player_track_candidate",
        "far_player_track_candidate",
    ]


def test_player_anchored_far_side_hit_recall_uses_wide_window(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (80, 2600, 0.45, 0.72),
            (88, 2933, 0.46, 0.90),
            (98, 3300, 0.47, 0.70),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(103, 3433, 0.46, 0.91, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    assert result["candidate_summary"]["player_anchor_candidate_count"] == 1
    assert result["candidate_summary"]["player_anchor_recovered_hit_count"] == 1
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert hit.payload_jsonb["candidate_method"] == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
    assert "player_anchored_hit_recall" in hit.payload_jsonb["reason_codes"]
    assert "wide_window_net_axis_reversal" in hit.payload_jsonb["reason_codes"]
    recall = hit.payload_jsonb["player_anchored_hit_recall"]
    assert recall["anchor_track_role_candidate"] == "far_player_track_candidate"
    assert recall["anchor_ball_frame"] == 88
    assert recall["incoming_frame"] == 80
    assert recall["outgoing_frame"] == 98
    assert recall["net_axis_reversal"] is True


def test_player_anchored_near_side_hit_recall_uses_wide_window(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (10, 333, 0.30, 0.34),
            (18, 633, 0.32, 0.16),
            (28, 1000, 0.34, 0.34),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(33, 1100, 0.32, 0.17, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    assert result["observations"]["hit_candidate"] == 1
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    assert hit.payload_jsonb["candidate_method"] == PLAYER_ANCHORED_HIT_CANDIDATE_METHOD
    assert hit.payload_jsonb["nearest_player"]["track_role_candidate"] == (
        "near_player_track_candidate"
    )


def test_player_anchored_hit_persists_contact_zone_payload(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (80, 2600, 0.45, 0.72),
            (88, 2933, 0.46, 0.90),
            (98, 3300, 0.47, 0.70),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(103, 3433, 0.46, 0.91, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    hit = db_session.scalar(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "hit_candidate",
        )
    )
    assert hit is not None
    contact_zone = hit.payload_jsonb["player_anchor_contact_zone"]
    assert contact_zone["in_contact_zone"] is True
    assert contact_zone["side_matches_player_track"] is True
    assert contact_zone["open_court_landing_zone"] is False
    assert hit.payload_jsonb["player_anchored_hit_recall"]["contact_zone"][
        "in_contact_zone"
    ] is True


def test_player_anchored_hit_rejects_without_near_player_anchor(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (80, 2600, 0.45, 0.72),
            (88, 2933, 0.46, 0.90),
            (98, 3300, 0.47, 0.70),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(88, 2933, 0.10, 0.10, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    assert result["candidate_summary"]["player_anchor_candidate_count"] == 0
    assert result["candidate_summary"]["player_anchor_rejected_count"] == 1
    assert result["candidate_summary"]["player_anchor_rejection_reasons"] == {
        "not_player_contact_zone": 1
    }


def test_player_anchored_hit_rejects_without_wide_window_reversal(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (80, 2600, 0.45, 0.72),
            (88, 2933, 0.46, 0.82),
            (98, 3300, 0.47, 0.92),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(103, 3433, 0.46, 0.83, "far_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    assert result["candidate_summary"]["player_anchor_candidate_count"] == 0
    assert result["candidate_summary"]["player_anchor_rejected_count"] >= 1
    assert (
        result["candidate_summary"]["player_anchor_rejection_reasons"][
            "no_wide_window_net_axis_reversal"
        ]
        >= 1
    )
    diagnostics = db_session.scalars(
        select(Observation).where(
            Observation.run_id == result["event_candidate_run_id"],
            Observation.observation_type == "event_candidate_rejection_diagnostic",
        )
    ).all()
    diagnostic = next(
        (
            item
            for item in diagnostics
            if item.payload_jsonb.get("diagnostic_source")
            == "player_anchored_hit_recall"
        ),
        None,
    )
    assert diagnostic is not None
    assert diagnostic.payload_jsonb["player_anchored_hit_recall"]["enabled"] is True


def test_player_anchored_hit_rejects_side_mismatch(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    trajectory_run, _ = _seed_trajectory_run(
        db_session,
        media.id,
        points=[
            (80, 2600, 0.45, 0.72),
            (88, 2933, 0.46, 0.90),
            (98, 3300, 0.47, 0.70),
        ],
    )
    projection_run = _seed_projection_run(
        db_session,
        media.id,
        players=[(88, 2933, 0.46, 0.90, "near_player_track_candidate")],
    )

    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
        hit_player_time_window_ms=40,
    )

    assert result["ok"] is True
    assert result["candidate_summary"]["player_anchor_candidate_count"] == 0
    assert (
        result["candidate_summary"]["player_anchor_rejection_reasons"][
            "side_mismatch_player_track"
        ]
        >= 1
    )


def test_player_anchored_hit_overlap_with_bounce_is_suppressed() -> None:
    config = HitBounceCandidateConfig(candidate_dedupe_ms=500)
    bounce = _draft_event_candidate(
        observation_type="bounce_candidate",
        frame=30,
        timestamp_ms=1000,
        court_x=0.44,
        court_y=0.89,
        track_role_candidate="far_player_track_candidate",
        player_distance=0.30,
        candidate_method=BOUNCE_CANDIDATE_METHOD,
        net_axis_reversal=False,
    )
    hit = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=34,
            timestamp_ms=1133,
            court_x=0.445,
            court_y=0.90,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.12,
            candidate_method=PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        player_anchor_contact_zone={
            "in_contact_zone": True,
            "strong_contact_zone": True,
            "open_court_landing_zone": False,
        },
    )

    filtered, suppressed_count, diagnostics = (
        suppress_player_anchored_hits_overlapping_bounces(
            [bounce, hit],
            config=config,
        )
    )

    assert [candidate.observation_type for candidate in filtered] == [
        "bounce_candidate"
    ]
    assert suppressed_count == 1
    assert diagnostics[0].rejection_reasons == [
        "suppressed_by_bounce_candidate_overlap",
        "open_court_landing_zone_anchor",
    ]
    assert diagnostics[0].overlap_suppression is not None
    assert diagnostics[0].overlap_suppression["suppressed"] is True


def test_marker_level_arbitration_resolves_colocated_hit_bounce_to_bounce() -> None:
    bounce = _draft_event_candidate(
        observation_type="bounce_candidate",
        frame=30,
        timestamp_ms=1000,
        court_x=0.44,
        court_y=0.89,
        track_role_candidate="far_player_track_candidate",
        player_distance=0.30,
        candidate_method=BOUNCE_CANDIDATE_METHOD,
        net_axis_reversal=False,
    )
    hit = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=34,
            timestamp_ms=1133,
            court_x=0.445,
            court_y=0.90,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.12,
            candidate_method=PLAYER_ANCHORED_HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        player_anchor_contact_zone={
            "in_contact_zone": True,
            "strong_contact_zone": True,
            "open_court_landing_zone": False,
        },
    )

    final_candidates, diagnostics, summary = apply_marker_level_event_arbitration(
        [bounce, hit],
        config=HitBounceCandidateConfig(),
    )

    assert [candidate.observation_type for candidate in final_candidates] == [
        "bounce_candidate"
    ]
    assert summary["hit_bounce_conflicts_resolved_to_bounce"] == 1
    assert summary["marker_level_arbitration"]["sequence_is_hard_gate"] is False
    assert summary["marker_level_arbitration"]["hit_requires_prior_bounce"] is False
    assert diagnostics[0].candidate_decision["reason"] == (
        "hit_bounce_conflict_resolved_to_bounce"
    )
    assert "suppressed_hit_overlapping_bounce" in diagnostics[0].rejection_reasons
    assert diagnostics[0].marker_level_arbitration is not None
    assert diagnostics[0].marker_level_arbitration["decision"] == (
        "suppress_hit_keep_bounce"
    )


def test_marker_level_arbitration_keeps_independent_contact_hit() -> None:
    bounce = _draft_event_candidate(
        observation_type="bounce_candidate",
        frame=10,
        timestamp_ms=333,
        court_x=0.30,
        court_y=0.20,
        track_role_candidate="near_player_track_candidate",
        player_distance=0.40,
        candidate_method=BOUNCE_CANDIDATE_METHOD,
        net_axis_reversal=False,
    )
    hit = _draft_event_candidate(
        observation_type="hit_candidate",
        frame=10,
        timestamp_ms=333,
        court_x=0.301,
        court_y=0.201,
        track_role_candidate="near_player_track_candidate",
        player_distance=0.10,
        candidate_method=HIT_CANDIDATE_METHOD,
        net_axis_reversal=True,
    )

    final_candidates, diagnostics, summary = apply_marker_level_event_arbitration(
        [bounce, hit],
        config=HitBounceCandidateConfig(),
    )

    assert diagnostics == []
    assert [candidate.observation_type for candidate in final_candidates] == [
        "bounce_candidate",
        "hit_candidate",
    ]
    assert summary["hit_bounce_conflicts_resolved_to_bounce"] == 0
    kept_hit = next(
        candidate
        for candidate in final_candidates
        if candidate.observation_type == "hit_candidate"
    )
    assert kept_hit.marker_level_arbitration is not None
    assert kept_hit.marker_level_arbitration["decision"] == "keep_hit"
    assert kept_hit.marker_level_arbitration[
        "has_strong_independent_contact_evidence"
    ] is True


def test_marker_level_arbitration_suppresses_fly_through_hit() -> None:
    fly_through = _draft_event_candidate(
        observation_type="hit_candidate",
        frame=93,
        timestamp_ms=3100,
        court_x=0.20,
        court_y=0.12,
        track_role_candidate="near_player_track_candidate",
        player_distance=0.50,
        candidate_method=NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD,
        net_axis_reversal=True,
    )

    final_candidates, diagnostics, summary = apply_marker_level_event_arbitration(
        [fly_through],
        config=HitBounceCandidateConfig(),
    )

    assert final_candidates == []
    assert summary["fly_through_hits_suppressed"] == 1
    assert diagnostics[0].candidate_decision["reason"] == "fly_through_no_local_event"
    assert "fly_through_no_local_event" in diagnostics[0].rejection_reasons
    assert diagnostics[0].marker_level_arbitration is not None
    assert diagnostics[0].marker_level_arbitration["decision"] == (
        "suppress_as_diagnostic"
    )


def test_weak_net_axis_reversal_hit_overlap_with_bounce_is_suppressed() -> None:
    bounce = _draft_event_candidate(
        observation_type="bounce_candidate",
        frame=34,
        timestamp_ms=1133,
        court_x=0.44,
        court_y=0.88,
        track_role_candidate="far_player_track_candidate",
        player_distance=0.50,
        candidate_method=SIDE_ZONE_SEQUENCE_BOUNCE_METHOD,
        net_axis_reversal=False,
    )
    weak_reversal_hit = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=34,
            timestamp_ms=1133,
            court_x=0.445,
            court_y=0.885,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.50,
            candidate_method=NET_AXIS_REVERSAL_HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        confidence=0.45,
        nearest_player=None,
        reason_codes=[
            "net_axis_reversal",
            "ball_first_reversal_recall",
            "player_proximity_not_required",
        ],
        net_axis_reversal_recall={"player_proximity_required": False},
    )

    filtered, suppressed_count, diagnostics = (
        suppress_weak_net_axis_reversal_hits_overlapping_bounces(
            [weak_reversal_hit, bounce],
            config=HitBounceCandidateConfig(),
        )
    )

    assert [candidate.observation_type for candidate in filtered] == [
        "bounce_candidate"
    ]
    assert suppressed_count == 1
    assert diagnostics[0].diagnostic_source == "net_axis_reversal_hit_recall"
    assert "suppressed_by_bounce_candidate_overlap" in diagnostics[0].rejection_reasons


def test_weak_image_space_direction_change_hit_before_bounce_is_suppressed() -> None:
    bounce = _draft_event_candidate(
        observation_type="bounce_candidate",
        frame=81,
        timestamp_ms=2700,
        court_x=0.28,
        court_y=0.21,
        track_role_candidate="near_player_track_candidate",
        player_distance=0.50,
        candidate_method=SIDE_ZONE_SEQUENCE_BOUNCE_METHOD,
        net_axis_reversal=False,
    )
    weak_direction_hit = replace(
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=77,
            timestamp_ms=2567,
            court_x=0.31,
            court_y=0.44,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.58,
            candidate_method=IMAGE_SPACE_DIRECTION_CHANGE_HIT_CANDIDATE_METHOD,
            net_axis_reversal=False,
        ),
        confidence=0.58,
        reason_codes=[
            "image_space_direction_change",
            "image_space_hit_recall",
            "player_proximity_not_required",
        ],
        image_space_direction_change_recall={
            "player_proximity_required": False,
            "image_direction_delta_degrees": 50.0,
            "pre_vector_length_pixels": 40.0,
            "post_vector_length_pixels": 120.0,
        },
    )

    filtered, suppressed_count, diagnostics = (
        suppress_weak_image_space_direction_change_hits_overlapping_bounces(
            [weak_direction_hit, bounce],
            config=HitBounceCandidateConfig(candidate_dedupe_ms=500),
        )
    )

    assert [candidate.observation_type for candidate in filtered] == [
        "bounce_candidate"
    ]
    assert suppressed_count == 1
    assert diagnostics[0].diagnostic_source == (
        "image_space_direction_change_hit_recall"
    )
    assert "suppressed_by_bounce_candidate_overlap" in diagnostics[0].rejection_reasons


def test_side_zone_sequence_reclassifies_sample_style_sequence() -> None:
    candidates = [
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=10,
            timestamp_ms=333,
            court_x=0.30,
            court_y=0.16,
            track_role_candidate="near_player_track_candidate",
            player_distance=0.10,
            candidate_method=HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=30,
            timestamp_ms=1000,
            court_x=0.44,
            court_y=0.89,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.14,
            candidate_method=HIT_FALLBACK_CANDIDATE_METHOD,
            net_axis_reversal=False,
        ),
        _draft_event_candidate(
            observation_type="bounce_candidate",
            frame=81,
            timestamp_ms=2700,
            court_x=0.70,
            court_y=0.21,
            track_role_candidate="near_player_track_candidate",
            player_distance=0.44,
            candidate_method=BOUNCE_CANDIDATE_METHOD,
            net_axis_reversal=False,
        ),
        _draft_event_candidate(
            observation_type="bounce_candidate",
            frame=180,
            timestamp_ms=6000,
            court_x=0.80,
            court_y=0.20,
            track_role_candidate="near_player_track_candidate",
            player_distance=0.25,
            candidate_method=BOUNCE_CANDIDATE_METHOD,
            net_axis_reversal=False,
        ),
    ]

    final_candidates, summary = apply_side_zone_sequence_classification(
        candidates,
        config=HitBounceCandidateConfig(),
    )

    assert [candidate.observation_type for candidate in final_candidates] == [
        "hit_candidate",
        "hit_candidate",
        "bounce_candidate",
        "hit_candidate",
    ]
    assert summary["reclassified_hit_to_bounce_count"] == 0
    assert summary["reclassified_bounce_to_hit_count"] == 1
    assert summary["sequence_prior_applied_count"] == 0
    assert summary["sequence_is_hard_gate"] is False
    assert summary["hit_requires_prior_bounce"] is False

    first_hit, far_hit, near_bounce, near_hit = final_candidates
    assert first_hit.candidate_reclassification == {
        "original_candidate_type": "hit_candidate",
        "final_candidate_type": "hit_candidate",
        "reason": None,
        "reclassified": False,
    }
    assert first_hit.court_side_zone is not None
    assert first_hit.court_side_zone["side"] == "near_side"
    assert far_hit.candidate_reclassification == {
        "original_candidate_type": "hit_candidate",
        "final_candidate_type": "hit_candidate",
        "reason": None,
        "reclassified": False,
    }
    assert far_hit.candidate_method == HIT_FALLBACK_CANDIDATE_METHOD
    assert far_hit.court_side_zone is not None
    assert far_hit.court_side_zone["side"] == "far_side"
    assert far_hit.court_landing_zone is not None
    assert far_hit.court_landing_zone["landing_zone_candidate"] is True
    assert far_hit.candidate_sequence is not None
    assert far_hit.candidate_sequence["expected_candidate_type"] is None
    assert far_hit.candidate_sequence["sequence_context_hint"] == "bounce_candidate"
    assert far_hit.candidate_sequence["sequence_is_hard_gate"] is False
    assert far_hit.candidate_sequence["hit_requires_prior_bounce"] is False
    assert "reclassified_from_hit_candidate" not in far_hit.reason_codes
    assert "sequence_bounce_prior" not in far_hit.reason_codes

    assert near_bounce.candidate_reclassification is not None
    assert near_bounce.candidate_reclassification["reclassified"] is False
    assert near_hit.candidate_reclassification is not None
    assert near_hit.candidate_reclassification["original_candidate_type"] == (
        "bounce_candidate"
    )
    assert near_hit.candidate_method == SIDE_ZONE_SEQUENCE_HIT_METHOD
    assert near_hit.player_contact_zone is not None
    assert near_hit.player_contact_zone["in_contact_zone"] is True
    assert near_hit.candidate_sequence is not None
    assert near_hit.candidate_sequence["expected_candidate_type"] is None
    assert near_hit.candidate_sequence["sequence_context_hint"] == "hit_candidate"
    assert near_hit.candidate_sequence["sequence_prior_applied"] is False
    assert "reclassified_from_bounce_candidate" in near_hit.reason_codes
    assert "sequence_hit_prior" not in near_hit.reason_codes


def test_hit_can_follow_hit_without_required_intervening_bounce() -> None:
    candidates = [
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=10,
            timestamp_ms=333,
            court_x=0.30,
            court_y=0.16,
            track_role_candidate="near_player_track_candidate",
            player_distance=0.10,
            candidate_method=HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=20,
            timestamp_ms=667,
            court_x=0.42,
            court_y=0.88,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.12,
            candidate_method=HIT_CANDIDATE_METHOD,
            net_axis_reversal=True,
        ),
    ]

    final_candidates, summary = apply_side_zone_sequence_classification(
        candidates,
        config=HitBounceCandidateConfig(),
    )

    assert [candidate.observation_type for candidate in final_candidates] == [
        "hit_candidate",
        "hit_candidate",
    ]
    assert summary["sequence_prior_applied_count"] == 0
    assert summary["sequence_is_hard_gate"] is False
    assert final_candidates[1].candidate_sequence is not None
    assert final_candidates[1].candidate_sequence["sequence_context_hint"] == (
        "bounce_candidate"
    )
    assert final_candidates[1].candidate_sequence["hit_requires_prior_bounce"] is False

    guarded_candidates, rejections, guard_summary = (
        apply_universal_hit_candidate_validity_guard(
            final_candidates,
            config=HitBounceCandidateConfig(),
        )
    )

    assert [candidate.observation_type for candidate in guarded_candidates] == [
        "hit_candidate",
        "hit_candidate",
    ]
    assert rejections == []
    assert guard_summary["hit_candidates_kept_by_guard"] == 2
    assert guard_summary["hit_requires_prior_bounce"] is False
    assert guarded_candidates[1].universal_hit_validity_guard is not None
    assert (
        guarded_candidates[1].universal_hit_validity_guard["final_decision"]
        == "keep_as_hit"
    )


def test_universal_hit_guard_reclassifies_bounce_like_fallback_hit() -> None:
    candidates = [
        _draft_event_candidate(
            observation_type="hit_candidate",
            frame=30,
            timestamp_ms=1000,
            court_x=0.44,
            court_y=0.89,
            track_role_candidate="far_player_track_candidate",
            player_distance=0.50,
            candidate_method=HIT_FALLBACK_CANDIDATE_METHOD,
            net_axis_reversal=False,
        )
    ]

    final_candidates, rejections, summary = apply_universal_hit_candidate_validity_guard(
        candidates,
        config=HitBounceCandidateConfig(),
    )

    assert rejections == []
    assert summary["hit_candidates_reclassified_to_bounce_by_guard"] == 1
    assert [candidate.observation_type for candidate in final_candidates] == [
        "bounce_candidate"
    ]
    candidate = final_candidates[0]
    assert candidate.candidate_method == UNIVERSAL_HIT_GUARD_BOUNCE_CANDIDATE_METHOD
    assert candidate.universal_hit_validity_guard is not None
    assert (
        candidate.universal_hit_validity_guard["assessment"]["bounce_like_landing_zone"]
        is True
    )
    assert candidate.candidate_reclassification is not None
    assert candidate.candidate_reclassification["reclassified"] is True
    assert candidate.candidate_decision["classification_priority"] == (
        UNIVERSAL_HIT_VALIDITY_GUARD_PRIORITY
    )


def test_universal_hit_guard_suppresses_fly_through_hit_candidate() -> None:
    candidates, _ = apply_side_zone_sequence_classification(
        [
            _draft_event_candidate(
                observation_type="hit_candidate",
                frame=44,
                timestamp_ms=1467,
                court_x=1.30,
                court_y=0.52,
                track_role_candidate="far_player_track_candidate",
                player_distance=0.70,
                candidate_method=HIT_FALLBACK_CANDIDATE_METHOD,
                net_axis_reversal=False,
            )
        ],
        config=HitBounceCandidateConfig(),
    )

    final_candidates, rejections, summary = apply_universal_hit_candidate_validity_guard(
        candidates,
        config=HitBounceCandidateConfig(),
    )

    assert final_candidates == []
    assert len(rejections) == 1
    assert summary["hit_candidates_suppressed_by_guard"] == 1
    assert "suppressed_by_universal_hit_validity_guard" in rejections[0].rejection_reasons
    assert rejections[0].universal_hit_validity_guard is not None
    assert (
        rejections[0].universal_hit_validity_guard["assessment"]["fly_through_candidate"]
        is True
    )


def test_universal_hit_guard_keeps_strong_contact_reversal_hit() -> None:
    candidates, _ = apply_side_zone_sequence_classification(
        [
            _draft_event_candidate(
                observation_type="hit_candidate",
                frame=10,
                timestamp_ms=333,
                court_x=0.30,
                court_y=0.16,
                track_role_candidate="near_player_track_candidate",
                player_distance=0.10,
                candidate_method=HIT_CANDIDATE_METHOD,
                net_axis_reversal=True,
            )
        ],
        config=HitBounceCandidateConfig(),
    )

    final_candidates, rejections, summary = apply_universal_hit_candidate_validity_guard(
        candidates,
        config=HitBounceCandidateConfig(),
    )

    assert rejections == []
    assert summary["hit_candidates_kept_by_guard"] == 1
    assert final_candidates[0].observation_type == "hit_candidate"
    assert final_candidates[0].universal_hit_validity_guard is not None
    assert final_candidates[0].universal_hit_validity_guard["assessment"][
        "strong_contact_support"
    ] is True


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
        players=[(1, 33, 0.31, 0.22, "near_player_track_candidate")],
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
    assert overlays[0]["classification_priority"] == MARKER_LEVEL_ARBITRATION_PRIORITY
    assert overlays[0]["player_proximity_gate"]["nearest_player_found"] is True
    assert overlays[0]["candidate_decision"]["selected_candidate_type"] == "hit_candidate"
    assert overlays[0]["net_axis_reversal"]["reversal"] is True
    assert overlays[0]["vertical_motion_proxy"] is None
    assert overlays[0]["speed_reduction"] is None
    assert overlays[0]["court_side_zone"]["side"] == "near_side"
    assert overlays[0]["player_contact_zone"]["in_contact_zone"] is True
    assert overlays[0]["candidate_reclassification"]["reclassified"] is False
    assert overlays[0]["candidate_sequence"]["sequence_index"] == 0
    assert overlays[0]["candidate_sequence"]["sequence_is_hard_gate"] is False
    assert overlays[0]["candidate_sequence"]["hit_requires_prior_bounce"] is False
    assert overlays[0]["universal_hit_validity_guard"]["final_decision"] == (
        "keep_as_hit"
    )
    assert len(timeline_items) == 1
    assert timeline_items[0]["item_type"] == "hit_candidate"
    assert timeline_items[0]["image_point"] == {"x": 300.0, "y": 100.0}
    assert timeline_items[0]["image_marker_source"] == "source_ball_court_projection_image_point"
    assert timeline_items[0]["classification_priority"] == MARKER_LEVEL_ARBITRATION_PRIORITY
    assert timeline_items[0]["universal_hit_validity_guard"]["final_decision"] == (
        "keep_as_hit"
    )
    assert timeline_items[0]["net_axis_reversal"]["axis"] == "court_y"
    assert timeline_items[0]["court_side_zone"]["side"] == "near_side"
    assert timeline_items[0]["candidate_sequence"]["sequence_context_model"] == (
        "optional_bounce_between_hits_v0"
    )
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


def test_replay_marker_summary_exposes_compact_final_markers(
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
        players=[(1, 33, 0.31, 0.22, "near_player_track_candidate")],
    )
    result = build_hit_bounce_candidates(
        session=db_session,
        media_id=media.id,
        ball_trajectory_run_id=trajectory_run.id,
        court_projection_run_id=projection_run.id,
    )

    marker_summary = build_event_candidate_marker_summary(
        session=db_session,
        media=media,
        event_candidate_run_id=result["event_candidate_run_id"],
    )
    timeline = build_replay_timeline(
        db_session,
        media_id=media.id,
        event_candidate_run_id=result["event_candidate_run_id"],
    )
    overlay_chunk = build_replay_overlay_chunk(
        db_session,
        media_id=media.id,
        start_ms=0,
        end_ms=200,
        layers={"hit_candidates", "bounce_candidates"},
        event_candidate_run_id=result["event_candidate_run_id"],
    )

    assert len(marker_summary) == 1
    marker = marker_summary[0]
    assert marker["index"] == 1
    assert marker["candidate_type"] == "hit_candidate"
    assert marker["frame"] == 1
    assert marker["timestamp_ms"] == 33
    assert marker["source_method"] == HIT_CANDIDATE_METHOD
    assert marker["arbitration_decision"] == "keep_hit"
    assert marker["arbitration_reason"] == "local_event_evidence_supported_hit"
    assert marker["court_x"] == 0.3
    assert marker["court_y"] == 0.2
    assert marker["image_x"] == 300.0
    assert marker["image_y"] == 100.0
    assert marker["candidate_only"] is True
    assert marker["not_hit_truth"] is True
    assert marker["not_bounce_truth"] is True
    assert marker["not_in_out_truth"] is True
    assert marker["no_adjudication"] is True
    assert timeline is not None
    assert timeline["marker_summary"] == marker_summary
    assert overlay_chunk is not None
    assert overlay_chunk["marker_summary"] == marker_summary


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
    assert "--image-space-net-axis-min-delta-pixels 4.0" in result["plan"]["command"]
    assert (
        "--image-space-direction-change-min-delta-degrees 45.0"
        in result["plan"]["command"]
    )
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
        hit_player_time_window_ms = 300
        hit_contact_fallback_min_speed_delta_fraction = 0.45
        hit_contact_fallback_min_direction_delta_degrees = 5.0
        bounce_fallback_enabled = True
        bounce_fallback_min_speed_reduction_fraction = 0.35
        player_anchored_hit_enabled = True
        player_anchored_hit_lookback_ms = 700
        player_anchored_hit_lookahead_ms = 1300
        player_anchored_hit_distance_max_template = 0.24
        player_anchored_hit_min_net_axis_delta_template = 0.015
        player_anchored_hit_min_pre_post_gap_ms = 60
        event_overlap_distance_template = 0.08
        net_axis_reversal_hit_enabled = True
        net_axis_reversal_lookback_ms = 700
        net_axis_reversal_lookahead_ms = 700
        net_axis_reversal_min_delta_template = 0.015
        net_axis_reversal_min_pre_post_gap_ms = 60
        net_axis_reversal_dedupe_distance_template = 0.08
        image_space_net_axis_hit_enabled = True
        image_space_net_axis_lookback_ms = 700
        image_space_net_axis_lookahead_ms = 700
        image_space_net_axis_min_delta_pixels = 4.0
        image_space_net_axis_min_pre_post_gap_ms = 60
        image_space_net_axis_dedupe_distance_pixels = 18.0
        image_space_direction_change_hit_enabled = True
        image_space_direction_change_lookback_ms = 700
        image_space_direction_change_lookahead_ms = 700
        image_space_direction_change_min_vector_pixels = 8.0
        image_space_direction_change_min_delta_degrees = 45.0
        image_space_direction_change_min_pre_post_gap_ms = 60
        image_space_direction_change_dedupe_distance_pixels = 18.0
        candidate_dedupe_ms = 500
        viewer_base_url = "http://127.0.0.1:3000"
        plan_only = True

    cli_result = _handle_build_hit_bounce_candidates(db_session, Args())

    assert cli_result["ok"] is True
    assert cli_result["status"] == "planned"


def test_compact_hit_bounce_cli_response_defaults_to_marker_summary() -> None:
    full_result = {
        "ok": True,
        "status": "completed",
        "message": "hit/bounce candidate evidence build complete",
        "media_id": "media-1",
        "run_id": "event-run-1",
        "event_candidate_run_id": "event-run-1",
        "source_run_ids": {
            "ball_trajectory_run_id": "trajectory-run",
            "court_projection_run_id": "projection-run",
        },
        "processing_step_id": "step-1",
        "runtime_config_id": "runtime-1",
        "observations": {
            "hit_candidate": 1,
            "bounce_candidate": 1,
            "event_candidate_rejection_diagnostic": 2,
            "total": 4,
        },
        "candidate_summary": {
            "physics_heuristic_version": "v0.3.1",
            "marker_level_arbitration_version": "v0.3.1",
            "universal_hit_validity_guard_version": "v0.3.0",
            "local_evidence_event_type_classification_version": "v0.2.8",
            "image_space_direction_change_hit_recall_version": "v0.2.7",
            "image_space_net_axis_hit_recall_version": "v0.2.6",
            "net_axis_reversal_hit_recall_version": "v0.2.5",
            "rejection_reasons": {"no_speed_reduction": 2},
        },
        "marker_summary": [
            {
                "candidate_type": "bounce_candidate",
                "frame": 30,
                "timestamp_ms": 1000,
                "source_method": "bounce_method",
                "reason": "keep_bounce",
                "court_x": 0.4,
                "court_y": 0.2,
                "image_x": 700.0,
                "image_y": 300.0,
                "confidence": 0.45,
            },
            {
                "candidate_type": "hit_candidate",
                "frame": 10,
                "timestamp_ms": 333,
                "source_method": "hit_method",
                "arbitration_decision": "keep_hit",
                "reason": "strong_contact",
                "court_x": 0.3,
                "court_y": 0.1,
                "image_x": 650.0,
                "image_y": 250.0,
                "confidence": 0.67,
            },
            {
                "candidate_type": "event_candidate_rejection_diagnostic",
                "frame": 20,
                "timestamp_ms": 667,
            },
        ],
        "observation_ids": ["hit-obs", "bounce-obs", "diagnostic-obs-1", "diagnostic-obs-2"],
        "replay_url": "http://127.0.0.1:3000/replay/media-1?eventCandidateRunId=event-run-1",
        "warnings": {
            "candidate_only": True,
            "event_candidate_only": True,
            "not_hit_truth": True,
            "not_bounce_truth": True,
            "not_in_out_truth": True,
            "no_adjudication": True,
            "no_score_or_point_truth": True,
            "observation_only": True,
        },
    }

    compact = _format_hit_bounce_cli_result(full_result)

    assert compact["ok"] is True
    assert compact["run_id"] == "event-run-1"
    assert compact["replay_url"].endswith("eventCandidateRunId=event-run-1")
    assert "observation_ids" not in compact
    assert "candidate_summary" not in compact
    assert compact["active_versions"] == {
        "physics_heuristic": "v0.3.1",
        "marker_level_arbitration": "v0.3.1",
        "universal_hit_validity_guard": "v0.3.0",
        "local_evidence_classification": "v0.2.8",
        "image_space_direction_change_hit_recall": "v0.2.7",
        "image_space_net_axis_hit_recall": "v0.2.6",
        "net_axis_reversal_hit_recall": "v0.2.5",
    }
    assert compact["summary_counts"] == {
        "final_hit_candidates": 1,
        "final_bounce_candidates": 1,
        "rejection_diagnostics": 2,
        "marker_count": 2,
    }
    assert [row["candidate_type"] for row in compact["marker_summary"]] == [
        "hit_candidate",
        "bounce_candidate",
    ]
    assert compact["marker_summary"][0]["index"] == 1
    assert compact["marker_summary"][0]["arbitration_reason"] == "strong_contact"
    assert compact["warnings"]["no_score_or_point_truth"] is True

    with_ids = _format_hit_bounce_cli_result(
        full_result,
        include_observation_ids=True,
    )
    assert with_ids["observation_ids"] == full_result["observation_ids"]

    full = _format_hit_bounce_cli_result(
        full_result,
        diagnostic_summary="full",
    )
    assert full["candidate_summary"] == full_result["candidate_summary"]

    none = _format_hit_bounce_cli_result(
        full_result,
        diagnostic_summary="none",
    )
    assert "active_versions" not in none
    assert "marker_summary" not in none
    assert none["summary_counts"]["marker_count"] == 2

    assert _format_hit_bounce_cli_result(full_result, verbose=True) is full_result


def _draft_event_candidate(
    *,
    observation_type: str,
    frame: int,
    timestamp_ms: int,
    court_x: float,
    court_y: float,
    track_role_candidate: str,
    player_distance: float,
    candidate_method: str,
    net_axis_reversal: bool,
) -> EventCandidateDraft:
    current = _trajectory_point(frame, timestamp_ms, court_x, court_y)
    context = TrajectoryContext(
        previous=_trajectory_point(frame - 1, timestamp_ms - 33, court_x, court_y - 0.03),
        current=current,
        next=_trajectory_point(frame + 1, timestamp_ms + 33, court_x, court_y + 0.03),
        direction_before_degrees=-70.0,
        direction_after_degrees=70.0,
        direction_delta_degrees=140.0,
        speed_before=0.8,
        speed_after=0.5,
        speed_delta_fraction=0.37,
    )
    player = PlayerProjection(
        observation=Observation(id=f"player-projection-{frame}"),
        frame_number=frame,
        timestamp_ms=timestamp_ms,
        court_x=court_x,
        court_y=court_y,
        track_candidate_id=f"{track_role_candidate}_001",
        track_role_candidate=track_role_candidate,
    )
    nearest_player = NearestPlayerContext(
        player=player,
        distance_template_units=player_distance,
        time_delta_ms=0,
    )
    return EventCandidateDraft(
        observation_type=observation_type,  # type: ignore[arg-type]
        candidate_method=candidate_method,
        trajectory_context=context,
        nearest_player=nearest_player,
        reason_codes=["near_main_player_projection"],
        confidence=0.5,
        player_proximity_gate={
            "nearest_player_found": True,
            "distance_template_units": player_distance,
            "time_delta_ms": 0,
            "threshold": HitBounceCandidateConfig().hit_player_review_distance_max_template,
        },
        candidate_decision={
            "selected_candidate_type": observation_type,
            "reason": "synthetic_test_candidate",
        },
        net_axis_reversal={
            "axis": "court_y",
            "vy_before": -0.03,
            "vy_after": 0.03,
            "reversal": net_axis_reversal,
            "min_axis_delta": 0.015,
        },
        vertical_motion_proxy=(
            {
                "proxy_type": "image_y_descending_to_ascending_v0",
                "descending_to_ascending": True,
            }
            if observation_type == "bounce_candidate"
            else None
        ),
        speed_reduction=(
            {
                "speed_before": 0.8,
                "speed_after": 0.5,
                "speed_reduction_fraction": 0.37,
                "speed_reduced": True,
            }
            if observation_type == "bounce_candidate"
            else None
        ),
    )


def _trajectory_point(
    frame: int,
    timestamp_ms: int,
    court_x: float,
    court_y: float,
) -> TrajectoryPoint:
    return TrajectoryPoint(
        trajectory_observation=Observation(id=f"trajectory-{frame}-{timestamp_ms}"),
        frame_number=frame,
        timestamp_ms=timestamp_ms,
        court_x=court_x,
        court_y=court_y,
        source_ball_court_projection_observation_id=f"ball-projection-{frame}",
        source_homography_observation_id=f"homography-{frame}",
        homography_time_delta_ms=0,
        homography_carried_forward=False,
        inside_template_bounds=True,
        image_x=court_x * 1000.0,
        image_y=court_y * 500.0,
    )


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


def _remove_ball_projection_image_points(
    session: Session,
    projection_ids: list[str],
) -> None:
    for projection_id in projection_ids:
        observation = session.get(Observation, projection_id)
        assert observation is not None
        payload = dict(observation.payload_jsonb or {})
        payload.pop("image_point", None)
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


def _seed_ball_projection_rows(
    session: Session,
    *,
    media_id: str,
    run_id: str,
    points: list[tuple[int, int, float, float, float, float]],
) -> list[str]:
    observation_ids: list[str] = []
    for index, (frame, timestamp_ms, court_x, court_y, image_x, image_y) in enumerate(
        points
    ):
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
                "court_point": {"x": court_x, "y": court_y},
                "image_point": {"x": image_x, "y": image_y},
                "source_homography_observation_id": f"homography-{frame}",
                "homography_time_delta_ms": 0,
                "homography_carried_forward": False,
                "inside_template_bounds": (
                    0.0 <= court_x <= 1.0 and 0.0 <= court_y <= 1.0
                ),
                "projection_candidate_only": True,
                "not_ball_truth": True,
                "not_court_truth": True,
                "observation_only": True,
                "no_adjudication": True,
            },
            idempotency_key=f"ball-projection:{run_id}:{index}",
        )
        session.add(observation)
        session.flush()
        observation_ids.append(observation.id)
    session.commit()
    return observation_ids
