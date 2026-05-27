from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import (
    Base,
    CourtKeypointObservation,
    HomographyCandidateObservation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    ProjectionDiagnosticObservation,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult
from tom_v3_video.time_index import frame_to_timestamp_ms

from apps.worker.cli import _handle_build_homography_candidates
from apps.worker.services.court_adapter import run_fixture_court_adapter
from apps.worker.services.homography_candidate_builder import (
    build_homography_candidates,
    compute_homography_candidate_from_keypoints,
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


@pytest.fixture()
def indexed_media(db_session: Session, tmp_path: Path) -> MediaAsset:
    video = tmp_path / "homography-candidate.mp4"
    video.write_bytes(b"tom-v3-homography-candidate")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="homography candidate test clip",
        storage_root=tmp_path / "media",
        probe_result=VideoProbeResult(
            duration_ms=3_000,
            frame_count=90,
            fps=30.0,
            width=640,
            height=360,
            codec="h264",
            format="mp4",
            raw_probe={"streams": [{"codec_type": "video"}]},
            frame_count_source="test_fixture",
        ),
    )


def _run_fixture_court(
    db_session: Session,
    indexed_media: MediaAsset,
    *,
    max_frames: int = 3,
) -> dict[str, object]:
    return run_fixture_court_adapter(
        session=db_session,
        media_id=indexed_media.id,
        frame_sample_rate=30,
        max_frames=max_frames,
    )


def test_compute_homography_candidate_from_fixture_keypoints(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    fixture_result = _run_fixture_court(db_session, indexed_media, max_frames=1)
    keypoint = db_session.scalar(
        select(CourtKeypointObservation).where(
            CourtKeypointObservation.run_id == fixture_result["court_run_id"]
        )
    )
    assert keypoint is not None

    candidate = compute_homography_candidate_from_keypoints(keypoint.keypoints_jsonb)

    assert candidate["status"] == "candidate"
    assert candidate["homography_matrix_jsonb"][2] == [0.0, 0.0, 1.0]
    assert candidate["inverse_homography_matrix_jsonb"][2] == [0.0, 0.0, 1.0]
    assert candidate["source_point_count"] == 12
    assert candidate["reprojection_error_mean"] <= 1e-6
    assert candidate["reprojection_error_median"] <= 1e-6
    assert candidate["reprojection_error_max"] <= 1e-6
    assert candidate["confidence"] > 0.7
    assert candidate["matrix_method"] == "axis_aligned_affine_fit_v0"


def test_compute_homography_requires_at_least_four_points(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    fixture_result = _run_fixture_court(db_session, indexed_media, max_frames=1)
    keypoint = db_session.scalar(
        select(CourtKeypointObservation).where(
            CourtKeypointObservation.run_id == fixture_result["court_run_id"]
        )
    )
    assert keypoint is not None
    sparse_keypoints = [
        {**point, "present": index < 3}
        for index, point in enumerate(keypoint.keypoints_jsonb)
    ]

    candidate = compute_homography_candidate_from_keypoints(sparse_keypoints)

    assert candidate["status"] == "insufficient_source_evidence"
    assert candidate["source_point_count"] == 3
    assert candidate["required_source_point_count"] == 4


def test_plan_only_returns_expected_homography_plan(db_session: Session) -> None:
    result = build_homography_candidates(
        session=db_session,
        media_id="media-plan",
        court_run_id="court-run-plan",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "build-homography-candidates" in result["plan"]["command"]
    assert result["plan"]["candidate_config"]["frame_time_owner"] == "media_indexing"
    assert result["warnings"]["homography_candidate_only"] is True
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_missing_media_and_court_run_return_clean_errors(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    missing_media = build_homography_candidates(
        session=db_session,
        media_id="missing-media",
        court_run_id="court-run",
    )
    missing_run = build_homography_candidates(
        session=db_session,
        media_id=indexed_media.id,
        court_run_id="missing-court-run",
    )

    assert missing_media["ok"] is False
    assert missing_media["status"] == "missing_media"
    assert missing_run["ok"] is False
    assert missing_run["status"] == "missing_court_run"
    assert db_session.scalar(select(func.count()).select_from(HomographyCandidateObservation)) == 0


def test_fixture_court_run_produces_homography_candidates_with_lineage(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    fixture_result = _run_fixture_court(db_session, indexed_media)

    result = build_homography_candidates(
        session=db_session,
        media_id=indexed_media.id,
        court_run_id=str(fixture_result["court_run_id"]),
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["message"] == "homography candidate build complete"
    assert result["source_court_run_id"] == fixture_result["court_run_id"]
    assert result["homography_run_id"]
    assert result["processing_step_id"]
    assert result["homography_candidates"] == {
        "candidate": 3,
        "insufficient_source_evidence": 0,
        "total": 3,
    }
    assert result["source_counts"] == {
        "court_keypoint_observations": 3,
        "court_line_observations": 3,
        "camera_view_observations": 3,
    }
    assert result["sampled_frames"] == [0, 30, 60]
    assert result["replay_url"].endswith(
        f"/replay/{indexed_media.id}?courtRunId={fixture_result['court_run_id']}"
        f"&homographyRunId={result['homography_run_id']}"
    )
    assert result["warnings"]["no_projection_diagnostics"] is True

    model = db_session.get(ModelRegistry, result["model_registry_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    run = db_session.get(ProcessingRun, result["homography_run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])

    assert model is not None
    assert model.model_family == "court"
    assert model.metadata_jsonb["homography_candidate_builder"] is True
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["matrix_direction"] == (
        "image_pixels_to_court_template_2d"
    )
    assert runtime_config.payload_jsonb["no_projection_diagnostics"] is True
    assert run is not None
    assert run.run_status == "completed"
    assert run.metadata_jsonb["candidate_count"] == 3
    assert run.metadata_jsonb["source_court_run_id"] == fixture_result["court_run_id"]
    assert step is not None
    assert step.step_status == "completed"
    assert step.metadata_jsonb["source_court_keypoint_count"] == 3

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["homography_run_id"])
        .order_by(Observation.frame_start)
    ).all()
    assert len(observations) == 3
    assert {observation.observation_family for observation in observations} == {"court"}
    assert {observation.observation_type for observation in observations} == {
        "homography_candidate_observation"
    }
    assert {observation.coordinate_space for observation in observations} == {
        "court_template_2d"
    }
    assert {observation.frame_start for observation in observations} == {0, 30, 60}
    assert {observation.timestamp_start_ms for observation in observations} == {
        frame_to_timestamp_ms(indexed_media.fps or 30.0, frame) for frame in [0, 30, 60]
    }
    assert all(
        observation.payload_jsonb["candidate_geometry"] is True
        for observation in observations
    )

    homographies = db_session.scalars(
        select(HomographyCandidateObservation).order_by(
            HomographyCandidateObservation.frame_number
        )
    ).all()
    assert len(homographies) == 3
    for homography in homographies:
        assert homography.status == "candidate"
        assert homography.homography_matrix_jsonb is not None
        assert homography.inverse_homography_matrix_jsonb is not None
        assert homography.source_court_keypoint_observation_id is not None
        assert homography.source_court_line_observation_id is not None
        assert homography.source_camera_view_observation_id is not None
        assert homography.source_coordinate_space == "image_pixels"
        assert homography.target_coordinate_space == "court_template_2d"
        assert homography.matrix_direction == "image_pixels_to_court_template_2d"
        assert homography.template_name == "tennis_court_template_normalized_v0"
        assert homography.template_version == "v0"
        assert homography.source_point_count == 12
        assert homography.source_line_count == 8
        assert homography.reprojection_error_mean is not None
        assert homography.reprojection_error_median is not None
        assert homography.reprojection_error_max is not None
        assert homography.confidence is not None
        assert homography.metadata_jsonb["geometry_evidence_only"] is True

    lineage = db_session.scalars(select(ObservationLineage)).all()
    assert len(lineage) == 9
    assert {row.relationship_type for row in lineage} == {
        "homography_from_court_keypoints_candidate",
        "homography_from_court_lines_candidate",
        "camera_context_for_homography_candidate",
    }
    assert all(row.processing_step_id == result["processing_step_id"] for row in lineage)
    assert all(row.payload_jsonb["candidate_geometry"] is True for row in lineage)
    assert db_session.scalar(select(func.count()).select_from(ProjectionDiagnosticObservation)) == 0


def test_high_min_keypoint_confidence_skips_insufficient_candidates(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    fixture_result = _run_fixture_court(db_session, indexed_media)

    result = build_homography_candidates(
        session=db_session,
        media_id=indexed_media.id,
        court_run_id=str(fixture_result["court_run_id"]),
        min_keypoint_confidence=0.95,
    )

    assert result["ok"] is True
    assert result["homography_candidates"] == {
        "candidate": 0,
        "insufficient_source_evidence": 3,
        "total": 0,
    }
    assert db_session.scalar(select(func.count()).select_from(HomographyCandidateObservation)) == 0
    run = db_session.get(ProcessingRun, result["homography_run_id"])
    assert run is not None
    assert run.run_status == "completed"
    assert run.metadata_jsonb["insufficient_source_evidence_count"] == 3


def test_cli_handler_plan_only_returns_expected_json(db_session: Session) -> None:
    result = _handle_build_homography_candidates(
        db_session,
        Namespace(
            media_id="media-plan",
            court_run_id="court-run-plan",
            run_name="homography-candidate-builder",
            frame_start=None,
            frame_end=None,
            min_keypoint_confidence=0.0,
            viewer_base_url="http://127.0.0.1:3000",
            plan_only=True,
        ),
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert result["warnings"]["no_tennis_event_interpretation"] is True
