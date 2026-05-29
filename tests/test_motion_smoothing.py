from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.skeletons import COCO17_KEYPOINT_NAMES
from tom_v3_storage.db_models import (
    Base,
    MediaAsset,
    Observation,
    ObservationLineage,
    PoseObservation,
    ProcessingRun,
    Tracklet,
    TrackPoint,
)

from apps.worker.services.motion_smoothing import (
    MotionSmoothingConfig,
    smooth_motion_candidates,
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


def test_motion_smoothing_creates_candidate_observations_and_lineage(
    db_session: Session,
) -> None:
    media = _seed_media(db_session)
    detection_run, raw_ball = _seed_ball_detection_run(db_session, media.id)
    tracklet_run = _seed_ball_tracklet_run(db_session, media.id, raw_ball)
    track_run = _seed_main_player_track_run(db_session, media.id)
    pose_run = _seed_pose_run(db_session, media.id)

    result = smooth_motion_candidates(
        session=db_session,
        media_id=media.id,
        detection_run_id=detection_run.id,
        tracklet_run_id=tracklet_run.id,
        main_player_track_run_id=track_run.id,
        pose_run_id=pose_run.id,
        config=MotionSmoothingConfig(
            ball_window_frames=3,
            ball_max_gap_frames=3,
            player_box_alpha=0.5,
            player_box_max_gap_frames=5,
            pose_alpha=0.5,
            pose_max_gap_frames=5,
        ),
    )

    assert result["ok"] is True
    assert result["observations"] == {
        "smoothed_ball_position_candidate": 5,
        "smoothed_main_player_box_candidate": 4,
        "smoothed_pose_candidate": 2,
        "total": 11,
    }
    assert result["warnings"]["raw_observations_not_mutated"] is True

    rows = db_session.scalars(
        select(Observation).where(Observation.run_id == result["motion_smoothing_run_id"])
    ).all()
    assert {row.observation_type for row in rows} == {
        "smoothed_ball_position_candidate",
        "smoothed_main_player_box_candidate",
        "smoothed_pose_candidate",
    }
    smoothed_ball_frames = {
        row.frame_start
        for row in rows
        if row.observation_type == "smoothed_ball_position_candidate"
    }
    assert smoothed_ball_frames == {
        0,
        1,
        2,
        10,
        11,
    }
    assert not any(
        row.frame_start == 5 and row.observation_type == "smoothed_ball_position_candidate"
        for row in rows
    )

    player_rows = [
        row for row in rows if row.observation_type == "smoothed_main_player_box_candidate"
    ]
    far_frame_ten = next(
        row
        for row in player_rows
        if row.payload_jsonb["track_role_candidate"] == "far_player_track_candidate"
        and row.frame_start == 10
    )
    assert far_frame_ten.payload_jsonb["bbox"] == {
        "x": 420.0,
        "y": 130.0,
        "w": 70.0,
        "h": 170.0,
    }

    pose_rows = [row for row in rows if row.observation_type == "smoothed_pose_candidate"]
    frame_one_pose = next(row for row in pose_rows if row.frame_start == 1)
    missing_left_wrist = next(
        keypoint
        for keypoint in frame_one_pose.payload_jsonb["keypoints"]
        if keypoint["name"] == "left_wrist"
    )
    assert missing_left_wrist["present"] is False
    assert missing_left_wrist["smoothing_source_count"] == 0

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id.in_([row.id for row in rows])
        )
    ).all()
    assert {
        lineage_row.relationship_type for lineage_row in lineage
    } == {
        "smoothed_from_track_point_candidate",
        "smoothed_from_main_player_track_assignment",
        "smoothed_from_pose_observation",
    }

    assert db_session.get(Observation, raw_ball[0].id).observation_type == "ball_detection"


def test_motion_smoothing_plan_only_does_not_mutate(db_session: Session) -> None:
    result = smooth_motion_candidates(
        session=db_session,
        media_id="media-plan",
        detection_run_id="detection-plan",
        tracklet_run_id="tracklet-plan",
        main_player_track_run_id="track-plan",
        pose_run_id="pose-plan",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "smooth-motion-candidates" in result["plan"]["command"]
    assert db_session.scalars(select(ProcessingRun)).all() == []


def _seed_media(session: Session) -> MediaAsset:
    media = MediaAsset(
        source_uri="file:///tmp/sample.mp4",
        duration_ms=12000,
        frame_count=360,
        fps=30.0,
        width=640,
        height=360,
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


def _seed_ball_detection_run(
    session: Session,
    media_id: str,
) -> tuple[ProcessingRun, list[Observation]]:
    run = _seed_run(session, media_id, "real-ball-detection")
    observations = [
        _seed_observation(
            session,
            media_id=media_id,
            run_id=run.id,
            observation_type="ball_detection",
            frame=frame,
            timestamp_ms=frame_to_ms(frame),
            confidence=0.8,
            payload={
                "label": "ball",
                "bbox": {"x": 10.0 + frame, "y": 20.0 + frame, "w": 10.0, "h": 10.0},
                "real_model_output": True,
            },
        )
        for frame in [0, 1, 2, 10, 11]
    ]
    session.commit()
    session.refresh(run)
    return run, observations


def _seed_ball_tracklet_run(
    session: Session,
    media_id: str,
    source_observations: list[Observation],
) -> ProcessingRun:
    run = _seed_run(session, media_id, "ball-tracklet")
    tracklet_observation = _seed_observation(
        session,
        media_id=media_id,
        run_id=run.id,
        observation_type="ball_tracklet_candidate",
        frame=0,
        timestamp_ms=0,
        confidence=0.82,
        payload={"track_status": "candidate", "identity_status": "unverified"},
        family="tracklet",
        granularity="tracklet",
        frame_end=11,
        timestamp_end_ms=frame_to_ms(11),
    )
    tracklet = Tracklet(
        media_id=media_id,
        run_id=run.id,
        track_family="ball",
        subject_ref="ball",
        frame_start=0,
        frame_end=11,
        confidence=0.82,
        observation_id=tracklet_observation.id,
        metadata_jsonb={"track_status": "candidate", "identity_status": "unverified"},
    )
    session.add(tracklet)
    session.flush()
    for index, source in enumerate(source_observations):
        point_observation = _seed_observation(
            session,
            media_id=media_id,
            run_id=run.id,
            observation_type="track_point_candidate",
            frame=source.frame_start or 0,
            timestamp_ms=source.timestamp_start_ms or 0,
            confidence=0.82,
            payload={"track_status": "candidate", "identity_status": "unverified"},
            family="tracklet",
        )
        session.add(
            TrackPoint(
                tracklet_id=tracklet.id,
                observation_id=point_observation.id,
                frame_number=source.frame_start or 0,
                timestamp_ms=source.timestamp_start_ms or 0,
                x=80.0 + index * 7.0,
                y=120.0 + index * 5.0,
                width=12.0,
                height=12.0,
                confidence=0.82,
                payload_jsonb={"source_detection_observation_id": source.id},
            )
        )
    session.commit()
    session.refresh(run)
    return run


def _seed_main_player_track_run(session: Session, media_id: str) -> ProcessingRun:
    run = _seed_run(session, media_id, "main-player-track-assignment-v01")
    for role, frames in {
        "near_player_track_candidate": [0, 1],
        "far_player_track_candidate": [0, 10],
    }.items():
        track = _seed_observation(
            session,
            media_id=media_id,
            run_id=run.id,
            observation_type="main_player_track_candidate",
            frame=frames[0],
            timestamp_ms=frame_to_ms(frames[0]),
            confidence=0.86,
            payload={
                "track_candidate_id": f"{role}_001",
                "track_role_candidate": role,
                "candidate_track_only": True,
                "not_identity_truth": True,
                "observation_only": True,
                "no_adjudication": True,
            },
            family="tracking",
            granularity="frame_range",
            frame_end=frames[-1],
            timestamp_end_ms=frame_to_ms(frames[-1]),
        )
        for frame in frames:
            bbox = (
                {"x": 100.0 + frame * 2.0, "y": 150.0, "w": 80.0, "h": 190.0}
                if role == "near_player_track_candidate"
                else {"x": 420.0, "y": 130.0, "w": 70.0, "h": 170.0}
            )
            _seed_observation(
                session,
                media_id=media_id,
                run_id=run.id,
                observation_type="main_player_track_assignment_candidate",
                frame=frame,
                timestamp_ms=frame_to_ms(frame),
                confidence=0.86,
                payload={
                    "track_candidate_id": f"{role}_001",
                    "track_role_candidate": role,
                    "source_track_candidate_observation_id": track.id,
                    "source_subject_candidate_observation_id": f"subject-{role}-{frame}",
                    "source_detection_observation_id": f"detection-{role}-{frame}",
                    "assignment_score": 0.86,
                    "assignment_method": "nearest_temporal_continuity_v0",
                    "bbox": bbox,
                    "candidate_track_only": True,
                    "not_identity_truth": True,
                    "observation_only": True,
                    "no_adjudication": True,
                },
                family="tracking",
            )
    session.commit()
    session.refresh(run)
    return run


def _seed_pose_run(session: Session, media_id: str) -> ProcessingRun:
    run = _seed_run(session, media_id, "track-filtered-pose")
    for frame in [0, 1]:
        observation = _seed_observation(
            session,
            media_id=media_id,
            run_id=run.id,
            observation_type="player_pose_observation",
            frame=frame,
            timestamp_ms=frame_to_ms(frame),
            confidence=0.74,
            payload={
                "track_candidate_id": "near_player_track_candidate_001",
                "track_role_candidate": "near_player_track_candidate",
                "candidate_track_only": True,
                "not_identity_truth": True,
            },
            family="pose",
        )
        keypoints = _pose_keypoints(missing_left_wrist=frame == 1)
        session.add(
            PoseObservation(
                observation_id=observation.id,
                media_id=media_id,
                run_id=run.id,
                frame_number=frame,
                timestamp_ms=frame_to_ms(frame),
                skeleton_format="coco17",
                skeleton_version="v1",
                keypoint_schema_jsonb={},
                keypoints_jsonb=keypoints,
                keypoint_count=len(keypoints),
                keypoints_present_count=sum(1 for item in keypoints if item["present"]),
                keypoints_missing_count=sum(1 for item in keypoints if not item["present"]),
                mean_keypoint_confidence=0.75,
                min_keypoint_confidence=0.7,
                max_keypoint_confidence=0.8,
                pose_confidence=0.74,
                bbox_x=100.0,
                bbox_y=120.0,
                bbox_w=80.0,
                bbox_h=190.0,
                bbox_confidence=0.86,
                subject_ref_type="main_player_track_assignment_candidate",
                subject_detection_observation_id=None,
                association_status="candidate",
                association_method="main_player_track_assignment_v01_crop_from_player_track_candidate",
                association_confidence=0.86,
                frame_time_owner="media_indexing",
                raw_model_payload_jsonb={},
                metadata_jsonb={
                    "subject_context": {
                        "track_candidate_id": "near_player_track_candidate_001",
                        "track_role_candidate": "near_player_track_candidate",
                        "source_track_run_id": "track-run",
                        "track_assignment_observation_id": f"assignment-{frame}",
                        "candidate_track_only": True,
                        "not_identity_truth": True,
                    }
                },
            )
        )
    session.commit()
    session.refresh(run)
    return run


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
    family: str = "atomic",
    granularity: str = "frame",
    frame_end: int | None = None,
    timestamp_end_ms: int | None = None,
) -> Observation:
    observation = Observation(
        media_id=media_id,
        run_id=run_id,
        observation_family=family,
        observation_type=observation_type,
        granularity=granularity,
        frame_start=frame,
        frame_end=frame if frame_end is None else frame_end,
        timestamp_start_ms=timestamp_ms,
        timestamp_end_ms=timestamp_ms if timestamp_end_ms is None else timestamp_end_ms,
        confidence=confidence,
        coordinate_space="image_pixels",
        payload_jsonb=payload,
    )
    session.add(observation)
    session.flush()
    return observation


def _pose_keypoints(*, missing_left_wrist: bool) -> list[dict[str, object]]:
    keypoints = []
    for index, name in enumerate(COCO17_KEYPOINT_NAMES):
        present = name in {"nose", "left_shoulder", "right_shoulder", "left_wrist"}
        if name == "left_wrist" and missing_left_wrist:
            present = False
        keypoints.append(
            {
                "index": index,
                "name": name,
                "x": 120.0 + index if present else None,
                "y": 80.0 + index if present else None,
                "confidence": 0.75 if present else None,
                "present": present,
                "visibility": None,
            }
        )
    return keypoints


def frame_to_ms(frame: int) -> int:
    return round(frame / 30.0 * 1000)
