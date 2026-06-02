from __future__ import annotations

from collections.abc import Generator

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
    MediaAsset,
    Observation,
    ProcessingRun,
    Trajectory3DDebugReviewAnnotation,
)

from apps.worker.services.reviewed_3d_debug_dataset_export import (
    export_reviewed_3d_debug_dataset,
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


def test_reviewed_3d_debug_dataset_json_export_includes_expected_sections(
    db_session: Session,
) -> None:
    context = _seed_reviewed_3d_export_context(db_session)

    result = export_reviewed_3d_debug_dataset(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry"].id,
    )

    assert result["ok"] is True
    assert result["export_type"] == "reviewed_3d_debug_dataset_export"
    assert result["export_version"] == "v0"
    assert result["summary"]["event_marker_count"] == 2
    assert result["summary"]["trajectory_3d_candidate_count"] == 2
    assert result["summary"]["event_candidate_3d_diagnostic_count"] == 1
    assert result["summary"]["trajectory_3d_debug_review_count"] == 2
    assert result["summary"]["event_marker_review_count"] == 1
    assert result["summary"]["missing_3d_sample_note_count"] == 1
    assert result["warnings"]["dataset_export_only"] is True
    assert result["warnings"]["not_truth"] is True
    assert result["warnings"]["not_3d_truth"] is True
    assert result["warnings"]["not_training_truth"] is True
    assert result["warnings"]["does_not_change_event_candidates"] is True

    marker = result["event_marker_summary"][0]
    assert marker["observation_id"] == context["hit"].id
    assert marker["review_label"] == "useful"
    assert marker["review_note"] == "Marker is helpful for dataset curation."

    candidate = result["trajectory_3d_candidates"][0]
    assert candidate["id"] == context["sample"].id
    assert candidate["court_z_status"] == "unknown"
    assert candidate["height_model"] == "none_unknown"

    diagnostic = result["event_candidate_3d_diagnostics"][0]
    assert diagnostic["event_observation_id"] == context["hit"].id
    assert diagnostic["nearest_3d_candidate_id"] == context["sample"].id
    assert diagnostic["height_status"] == "height_unknown"

    review_kinds = {
        row["annotation_kind"] for row in result["trajectory_3d_debug_reviews"]
    }
    assert review_kinds == {"trajectory_3d_sample_review", "missing_3d_sample_note"}
    assert result["event_candidate_reviews"][0]["review_label"] == "useful"
    assert "ground_truth_dataset" not in result
    assert "accepted_track" not in str(result)


def test_reviewed_3d_debug_dataset_markdown_and_output_file(
    db_session: Session,
    tmp_path,
) -> None:
    context = _seed_reviewed_3d_export_context(db_session)
    output_path = tmp_path / "exports" / "reviewed_3d_debug_dataset.md"

    result = export_reviewed_3d_debug_dataset(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry"].id,
        output_format="markdown",
        output_path=str(output_path),
    )

    assert result["ok"] is True
    assert result["output_path"] == str(output_path)
    assert output_path.read_text(encoding="utf-8") == result["markdown"]
    assert "# Reviewed 3D Debug Dataset Export v0" in result["markdown"]
    assert "| Event markers | 2 |" in result["markdown"]
    assert "Not truth, not 3D truth, and not training truth." in result["markdown"]


def test_reviewed_3d_debug_dataset_json_output_file_and_no_mutation(
    db_session: Session,
    tmp_path,
) -> None:
    context = _seed_reviewed_3d_export_context(db_session)
    before_counts = _source_counts(db_session)
    output_path = tmp_path / "nested" / "reviewed_3d_debug_dataset.json"

    result = export_reviewed_3d_debug_dataset(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry"].id,
        output_path=str(output_path),
    )
    after_counts = _source_counts(db_session)

    assert result["ok"] is True
    assert output_path.is_file()
    assert '"export_type": "reviewed_3d_debug_dataset_export"' in output_path.read_text(
        encoding="utf-8"
    )
    assert after_counts == before_counts


def test_reviewed_3d_debug_dataset_rejects_unsupported_format(
    db_session: Session,
) -> None:
    context = _seed_reviewed_3d_export_context(db_session)

    result = export_reviewed_3d_debug_dataset(
        session=db_session,
        media_id=context["media"].id,
        event_candidate_run_id=context["event_run"].id,
        trajectory_3d_run_id=context["trajectory_3d_run"].id,
        camera_geometry_id=context["camera_geometry"].id,
        output_format="csv",
    )

    assert result["ok"] is False
    assert result["status"] == "unsupported_format"
    assert result["warnings"]["not_training_truth"] is True


def _source_counts(session: Session) -> dict[str, int]:
    return {
        "observations": session.scalar(select(func.count(Observation.id))) or 0,
        "trajectory_3d": session.scalar(select(func.count(BallTrajectory3DCandidate.id))) or 0,
        "diagnostics": session.scalar(select(func.count(EventCandidate3DDiagnostic.id))) or 0,
        "trajectory_reviews": session.scalar(
            select(func.count(Trajectory3DDebugReviewAnnotation.id))
        )
        or 0,
        "event_reviews": session.scalar(select(func.count(EventCandidateReviewAnnotation.id)))
        or 0,
    }


def _seed_reviewed_3d_export_context(session: Session) -> dict[str, object]:
    media = MediaAsset(
        source_uri="file:///tmp/reviewed-3d-debug-export-sample.mp4",
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
    homography_run = _seed_run(session, media.id, "homography")
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
    geometry_run = _seed_run(session, media.id, "camera-geometry")
    camera_geometry = CameraGeometryEvidence(
        media_id=media.id,
        court_projection_run_id=court_projection_run.id,
        homography_run_id=homography_run.id,
        geometry_run_id=geometry_run.id,
        camera_model="homography_backed_court_plane",
        geometry_status="declared",
        court_model="itf_standard_tennis_court",
        court_units="m",
        court_length=23.77,
        court_width=10.97,
        net_height_center=0.914,
        image_size_jsonb={"width": 1920, "height": 1080},
        world_coordinate_system_jsonb={"origin": "near_left_baseline_corner"},
        assumptions_jsonb={"declared_geometry_only": True},
        warnings_jsonb={
            "geometry_evidence_only": True,
            "not_3d_truth": True,
            "no_adjudication": True,
        },
        metadata_jsonb={"true_3d_reconstruction_available": False},
    )
    session.add(camera_geometry)
    session.flush()

    hit = _seed_event_observation(session, media.id, event_run.id, "hit_candidate", 12, 400)
    bounce = _seed_event_observation(
        session,
        media.id,
        event_run.id,
        "bounce_candidate",
        30,
        1000,
    )
    sample = _seed_trajectory_3d_candidate(
        session=session,
        media_id=media.id,
        ball_trajectory_run_id=ball_trajectory_run.id,
        court_projection_run_id=court_projection_run.id,
        trajectory_3d_run_id=trajectory_3d_run.id,
        camera_geometry_id=camera_geometry.id,
        frame=12,
        timestamp_ms=400,
        court_x_m=3.1,
        court_y_m=7.2,
    )
    _seed_trajectory_3d_candidate(
        session=session,
        media_id=media.id,
        ball_trajectory_run_id=ball_trajectory_run.id,
        court_projection_run_id=court_projection_run.id,
        trajectory_3d_run_id=trajectory_3d_run.id,
        camera_geometry_id=camera_geometry.id,
        frame=30,
        timestamp_ms=1000,
        court_x_m=4.1,
        court_y_m=9.2,
    )
    diagnostic = EventCandidate3DDiagnostic(
        media_id=media.id,
        event_candidate_run_id=event_run.id,
        event_observation_id=hit.id,
        candidate_type="hit_candidate",
        trajectory_3d_run_id=trajectory_3d_run.id,
        camera_geometry_id=camera_geometry.id,
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
    session.add(
        Trajectory3DDebugReviewAnnotation(
            media_id=media.id,
            trajectory_3d_run_id=trajectory_3d_run.id,
            event_candidate_run_id=event_run.id,
            camera_geometry_id=camera_geometry.id,
            trajectory_3d_candidate_id=sample.id,
            annotation_kind="trajectory_3d_sample_review",
            review_label="bad_3d_position",
            frame=12,
            timestamp_ms=400,
            image_x=800.0,
            image_y=520.0,
            court_x_m=3.1,
            court_y_m=7.2,
            court_z_m=None,
            note="3D point drifts in debug review.",
            reviewer="pytest-operator",
            payload_jsonb={
                "review_metadata_only": True,
                "not_truth": True,
                "not_3d_truth": True,
                "does_not_change_3d_candidates": True,
            },
        )
    )
    session.add(
        Trajectory3DDebugReviewAnnotation(
            media_id=media.id,
            trajectory_3d_run_id=trajectory_3d_run.id,
            event_candidate_run_id=event_run.id,
            event_observation_id=bounce.id,
            annotation_kind="missing_3d_sample_note",
            review_label="missing_3d_sample",
            frame=30,
            timestamp_ms=1000,
            note="Missing 3D sample near bounce marker.",
            reviewer="pytest-operator",
            payload_jsonb={"review_metadata_only": True, "not_3d_truth": True},
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
            image_x=800.0,
            image_y=600.0,
            court_x=0.4,
            court_y=0.2,
            note="Marker is helpful for dataset curation.",
            reviewer="pytest-operator",
            payload_jsonb={"review_metadata_only": True, "not_truth": True},
        )
    )
    session.commit()
    return {
        "media": media,
        "ball_trajectory_run": ball_trajectory_run,
        "court_projection_run": court_projection_run,
        "trajectory_3d_run": trajectory_3d_run,
        "event_run": event_run,
        "camera_geometry": camera_geometry,
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
            "marker_level_arbitration": {
                "decision": "kept",
                "reason": "pytest_marker_context",
            },
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


def _seed_trajectory_3d_candidate(
    *,
    session: Session,
    media_id: str,
    ball_trajectory_run_id: str,
    court_projection_run_id: str,
    trajectory_3d_run_id: str,
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
        image_x=800.0,
        image_y=520.0,
        court_x=0.42,
        court_y=0.33,
        court_x_m=court_x_m,
        court_y_m=court_y_m,
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
    session.add(row)
    session.flush()
    return row
