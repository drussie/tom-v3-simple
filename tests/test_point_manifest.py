from __future__ import annotations

import json
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    BallTrajectory3DCandidate,
    Base,
    CameraGeometryEvidence,
    EventCandidate3DDiagnostic,
    EventCandidateReviewAnnotation,
    HumanAnnotation,
    MediaAsset,
    Observation,
    ProcessingRun,
    Trajectory3DDebugReviewAnnotation,
)

from apps.worker.services.point_manifest import (
    POINT_MANIFEST_TYPE,
    build_point_manifest,
    deterministic_point_manifest_id,
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


def test_point_manifest_writes_provenance_contract_and_counts(
    db_session: Session,
    tmp_path: Path,
) -> None:
    context = _seed_point_manifest_context(db_session)
    output_path = tmp_path / "manifests" / "point_manifest.json"
    generated_at = datetime(2026, 6, 17, 12, 0, tzinfo=UTC)
    before_counts = _source_counts(db_session)

    result = build_point_manifest(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry"].id,
        viewer_base_url="http://127.0.0.1:3000",
        output_path=output_path,
        generated_at=generated_at,
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert output_path.is_file()
    assert _source_counts(db_session) == before_counts

    manifest = json.loads(output_path.read_text(encoding="utf-8"))
    identity = {
        "manifest_type": POINT_MANIFEST_TYPE,
        "manifest_version": "v0",
        "media_id": context["media"].id,
        "event_candidate_run_id": context["event_run"].id,
        "trajectory_3d_run_id": context["trajectory_3d_run"].id,
        "camera_geometry_id": context["camera_geometry"].id,
    }
    expected_manifest_id = deterministic_point_manifest_id(identity)
    assert result["point_manifest_id"] == expected_manifest_id
    assert manifest["point_manifest_id"] == expected_manifest_id
    assert manifest["manifest_type"] == "point_evidence_provenance_manifest"
    assert manifest["manifest_version"] == "v0"
    assert manifest["generated_at"] == "2026-06-17T12:00:00+00:00"
    assert manifest["source_uri"] == "file:///tmp/source-point.mp4"
    assert manifest["source_media_path"] == "/tmp/source-point.mp4"
    assert manifest["stored_uri"] == "file:///tmp/stored-point.mp4"
    assert manifest["stored_path"] == "/tmp/stored-point.mp4"
    assert manifest["replay_url"].startswith(
        f"http://127.0.0.1:3000/replay/{context['media'].id}?"
    )
    assert manifest["tom_provenance"]["blueprint"] == "blueprint_23"

    assert manifest["associated_run_ids"] == {
        "event_candidate_run_id": context["event_run"].id,
        "trajectory_3d_run_id": context["trajectory_3d_run"].id,
        "camera_geometry_id": context["camera_geometry"].id,
    }
    assert manifest["evidence_availability"] == {
        "media_indexed": True,
        "replay_available": True,
        "event_candidates_available": True,
        "trajectory_3d_candidates_available": True,
        "event_candidate_3d_diagnostics_available": True,
        "review_annotations_available": True,
        "trajectory_3d_debug_reviews_available": True,
    }
    assert manifest["profile_counts"] == {
        "event_marker_count": 2,
        "hit_candidate_count": 1,
        "bounce_candidate_count": 1,
        "event_candidate_observation_count": 3,
        "event_candidate_rejection_diagnostic_count": 1,
        "trajectory_3d_candidate_count": 2,
        "event_candidate_3d_diagnostic_count": 1,
        "event_marker_review_count": 1,
        "trajectory_3d_debug_review_count": 1,
        "human_annotation_count": 1,
        "review_annotation_count": 3,
    }
    assert manifest["warnings"]["baseline_is_not_truth"] is True
    assert manifest["warnings"]["manifest_is_not_truth"] is True
    assert manifest["warnings"]["observation_only"] is True
    assert manifest["warnings"]["no_adjudication"] is True
    assert manifest["warnings"]["not_training_truth"] is True
    assert manifest["warnings"]["not_3d_truth"] is True
    assert manifest["warnings"]["does_not_create_in_out"] is True
    assert manifest["warnings"]["does_not_create_score"] is True
    assert manifest["warnings"]["does_not_identify_players"] is True
    assert manifest["warnings"]["does_not_determine_winner"] is True
    assert manifest["warnings"]["not_generalization_claim"] is True


def test_point_manifest_default_output_path_is_deterministic(
    db_session: Session,
    tmp_path: Path,
) -> None:
    context = _seed_point_manifest_context(db_session)

    result = build_point_manifest(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        output_dir=tmp_path,
        generated_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
    )

    manifest_path = tmp_path / f"{result['point_manifest_id']}.json"
    assert result["manifest_output"] == str(manifest_path)
    assert manifest_path.is_file()
    assert result["manifest"]["evidence_availability"]["trajectory_3d_candidates_available"] is True
    assert result["manifest"]["associated_run_ids"] == {
        "event_candidate_run_id": context["event_run"].id,
    }


def test_point_manifest_missing_media_fails_clearly(db_session: Session) -> None:
    result = build_point_manifest(session=db_session, media_id="missing-media")

    assert result["ok"] is False
    assert result["status"] == "missing_media"
    assert result["warnings"]["manifest_is_not_truth"] is True


def test_point_manifest_rejects_run_from_other_media(db_session: Session) -> None:
    context = _seed_point_manifest_context(db_session)
    other_media = MediaAsset(source_uri="file:///tmp/other.mp4", media_type="video")
    db_session.add(other_media)
    db_session.flush()
    other_run = _seed_run(db_session, other_media.id, "other-event-run")
    db_session.commit()

    result = build_point_manifest(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=other_run.id,
    )

    assert result["ok"] is False
    assert result["status"] == "event_candidate_run_media_mismatch"
    assert "does not belong to media" in result["message"]


def test_point_manifest_does_not_create_forbidden_decision_fields(
    db_session: Session,
    tmp_path: Path,
) -> None:
    context = _seed_point_manifest_context(db_session)

    result = build_point_manifest(
        session=db_session,
        media_id=context["media"].id,
        output_path=tmp_path / "point_manifest.json",
    )

    keys = _walk_keys(result)
    assert not {"in_out", "score", "point_winner", "player_identity"} & keys
    assert not {"rally_state", "server_state", "receiver_state"} & keys


def _source_counts(session: Session) -> dict[str, int]:
    return {
        "observations": session.scalar(select(func.count(Observation.id))) or 0,
        "trajectory_3d": session.scalar(select(func.count(BallTrajectory3DCandidate.id))) or 0,
        "diagnostics": session.scalar(select(func.count(EventCandidate3DDiagnostic.id))) or 0,
        "event_reviews": session.scalar(select(func.count(EventCandidateReviewAnnotation.id)))
        or 0,
        "trajectory_reviews": session.scalar(
            select(func.count(Trajectory3DDebugReviewAnnotation.id))
        )
        or 0,
        "human_annotations": session.scalar(select(func.count(HumanAnnotation.id))) or 0,
    }


def _seed_point_manifest_context(session: Session) -> dict[str, Any]:
    media = MediaAsset(
        source_uri="file:///tmp/stored-point.mp4",
        media_type="video",
        duration_ms=3000,
        frame_count=90,
        fps=30.0,
        width=1920,
        height=1080,
        checksum="sha256-test",
        metadata_jsonb={
            "original_source_uri": "file:///tmp/source-point.mp4",
            "original_source_path": "/tmp/source-point.mp4",
            "stored_uri": "file:///tmp/stored-point.mp4",
            "stored_path": "/tmp/stored-point.mp4",
            "storage_mode": "copied",
        },
    )
    session.add(media)
    session.flush()

    ball_trajectory_run = _seed_run(session, media.id, "ball-trajectory")
    trajectory_3d_run = _seed_run(session, media.id, "trajectory-3d")
    event_run = _seed_run(session, media.id, "event-candidates")
    camera_geometry = CameraGeometryEvidence(
        media_id=media.id,
        court_projection_run_id=None,
        homography_run_id=None,
        geometry_run_id=None,
        camera_model="homography_backed_court_plane",
        geometry_status="declared",
        court_model="itf_standard_tennis_court",
        court_units="m",
        image_size_jsonb={"width": 1920, "height": 1080},
        world_coordinate_system_jsonb={"origin": "near_left_baseline_corner"},
        assumptions_jsonb={"declared_geometry_only": True},
        warnings_jsonb={"not_3d_truth": True, "no_adjudication": True},
        metadata_jsonb={"true_3d_reconstruction_available": False},
    )
    session.add(camera_geometry)
    session.flush()

    hit = _seed_observation(session, media.id, event_run.id, "hit_candidate", 12, 400)
    bounce = _seed_observation(session, media.id, event_run.id, "bounce_candidate", 30, 1000)
    _seed_observation(
        session,
        media.id,
        event_run.id,
        "event_candidate_rejection_diagnostic",
        31,
        1033,
    )
    trajectory_sample = _seed_trajectory_3d_candidate(
        session=session,
        media_id=media.id,
        ball_trajectory_run_id=ball_trajectory_run.id,
        trajectory_3d_run_id=trajectory_3d_run.id,
        camera_geometry_id=camera_geometry.id,
        source_observation_id=hit.id,
        frame=12,
        timestamp_ms=400,
    )
    _seed_trajectory_3d_candidate(
        session=session,
        media_id=media.id,
        ball_trajectory_run_id=ball_trajectory_run.id,
        trajectory_3d_run_id=trajectory_3d_run.id,
        camera_geometry_id=camera_geometry.id,
        source_observation_id=bounce.id,
        frame=30,
        timestamp_ms=1000,
    )
    session.add(
        EventCandidate3DDiagnostic(
            media_id=media.id,
            event_candidate_run_id=event_run.id,
            event_observation_id=hit.id,
            candidate_type="hit_candidate",
            trajectory_3d_run_id=trajectory_3d_run.id,
            camera_geometry_id=camera_geometry.id,
            frame=12,
            timestamp_ms=400,
            nearest_3d_candidate_id=trajectory_sample.id,
            nearest_3d_frame=12,
            nearest_3d_timestamp_ms=400,
            nearest_time_delta_ms=0,
            height_status="height_unknown",
            diagnostic_status="evaluated",
            diagnostic_label="neutral_context",
            pre_window_sample_count=1,
            post_window_sample_count=1,
            local_window_sample_count=1,
            local_velocity_available=False,
            diagnostics_jsonb={"test": True},
            warnings_jsonb={"not_truth": True, "not_3d_truth": True},
            metadata_jsonb={"test": True},
        )
    )
    session.add(
        EventCandidateReviewAnnotation(
            media_id=media.id,
            event_candidate_run_id=event_run.id,
            observation_id=hit.id,
            annotation_kind="candidate_marker_review",
            review_label="useful",
            candidate_type="hit_candidate",
            frame=12,
            timestamp_ms=400,
            note="Review metadata only.",
            reviewer="pytest",
            payload_jsonb={"review_metadata_only": True, "not_truth": True},
        )
    )
    session.add(
        Trajectory3DDebugReviewAnnotation(
            media_id=media.id,
            trajectory_3d_run_id=trajectory_3d_run.id,
            event_candidate_run_id=event_run.id,
            camera_geometry_id=camera_geometry.id,
            trajectory_3d_candidate_id=trajectory_sample.id,
            annotation_kind="trajectory_3d_sample_review",
            review_label="bad_3d_position",
            frame=12,
            timestamp_ms=400,
            note="3D debug review metadata only.",
            reviewer="pytest",
            payload_jsonb={"review_metadata_only": True, "not_3d_truth": True},
        )
    )
    session.add(
        HumanAnnotation(
            media_id=media.id,
            observation_id=hit.id,
            annotation_type="manual_note",
            payload_jsonb={"review_metadata_only": True},
            created_by="pytest",
        )
    )
    session.commit()
    return {
        "media": media,
        "ball_trajectory_run": ball_trajectory_run,
        "trajectory_3d_run": trajectory_3d_run,
        "event_run": event_run,
        "camera_geometry": camera_geometry,
        "hit": hit,
        "bounce": bounce,
        "trajectory_sample": trajectory_sample,
    }


def _seed_run(session: Session, media_id: str, run_name: str) -> ProcessingRun:
    row = ProcessingRun(
        media_id=media_id,
        run_name=run_name,
        run_status="completed",
        metadata_jsonb={},
    )
    session.add(row)
    session.flush()
    return row


def _seed_observation(
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
        payload_jsonb={"observation_only": True, "no_adjudication": True},
    )
    session.add(row)
    session.flush()
    return row


def _seed_trajectory_3d_candidate(
    *,
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str,
    trajectory_3d_run_id: str,
    camera_geometry_id: str,
    source_observation_id: str,
    frame: int,
    timestamp_ms: int,
) -> BallTrajectory3DCandidate:
    row = BallTrajectory3DCandidate(
        media_id=media_id,
        ball_trajectory_run_id=ball_trajectory_run_id,
        camera_geometry_id=camera_geometry_id,
        trajectory_3d_run_id=trajectory_3d_run_id,
        source_observation_id=source_observation_id,
        frame=frame,
        timestamp_ms=timestamp_ms,
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
        diagnostics_jsonb={"test": True},
        warnings_jsonb={"not_3d_truth": True, "no_adjudication": True},
        metadata_jsonb={"test": True},
    )
    session.add(row)
    session.flush()
    return row


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_walk_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_walk_keys(item))
        return keys
    return set()
