from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.exports import CourtReviewDatasetExportRequest
from tom_v3_storage.db_models import (
    Base,
    EvidenceArtifact,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    ProjectionDiagnosticObservation,
    QueryResult,
    RuntimeConfig,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.worker.cli import (
    _handle_build_projection_diagnostics,
    _handle_export_court_review_dataset,
)
from apps.worker.services.court_adapter import run_fixture_court_adapter
from apps.worker.services.court_review_export import export_court_review_dataset
from apps.worker.services.homography_candidate_builder import build_homography_candidates
from apps.worker.services.projection_diagnostic_builder import (
    build_projection_diagnostics,
    project_template_geometry_from_homography,
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
    video = tmp_path / "projection-diagnostics.mp4"
    video.write_bytes(b"tom-v3-projection-diagnostics")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="projection diagnostic test clip",
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


@pytest.fixture()
def court_and_homography_runs(
    db_session: Session,
    indexed_media: MediaAsset,
) -> dict[str, str]:
    court_result = run_fixture_court_adapter(
        session=db_session,
        media_id=indexed_media.id,
        frame_sample_rate=30,
        max_frames=3,
    )
    assert court_result["ok"] is True
    homography_result = build_homography_candidates(
        session=db_session,
        media_id=indexed_media.id,
        court_run_id=str(court_result["court_run_id"]),
    )
    assert homography_result["ok"] is True
    return {
        "court_run_id": str(court_result["court_run_id"]),
        "homography_run_id": str(homography_result["homography_run_id"]),
    }


def test_project_template_geometry_from_fixture_homography(
    db_session: Session,
    court_and_homography_runs: dict[str, str],
) -> None:
    homography = db_session.scalar(select(ProjectionDiagnosticObservation))
    assert homography is None
    from tom_v3_storage.db_models import HomographyCandidateObservation

    source = db_session.scalar(select(HomographyCandidateObservation))
    assert source is not None

    diagnostic = project_template_geometry_from_homography(source)

    assert diagnostic["status"] == "diagnostic_candidate"
    assert len(diagnostic["projected_template_keypoints_jsonb"]) == 12
    assert len(diagnostic["projected_template_lines_jsonb"]) == 8
    assert diagnostic["diagnostic_metrics_jsonb"]["projected_keypoint_count"] == 12
    assert diagnostic["diagnostic_metrics_jsonb"]["projected_line_count"] == 8
    assert diagnostic["diagnostic_metrics_jsonb"]["not_ball_player_projection"] is True
    assert diagnostic["confidence"] == source.confidence


def test_projection_diagnostic_plan_only_returns_expected_plan(db_session: Session) -> None:
    result = build_projection_diagnostics(
        session=db_session,
        media_id="media-plan",
        homography_run_id="homography-run-plan",
        plan_only=True,
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "build-projection-diagnostics" in result["plan"]["command"]
    assert result["plan"]["diagnostic_config"]["not_ball_player_projection"] is True
    assert result["warnings"]["projection_diagnostic_only"] is True
    assert db_session.scalar(select(func.count()).select_from(Observation)) == 0


def test_missing_media_and_homography_run_return_clean_errors(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    missing_media = build_projection_diagnostics(
        session=db_session,
        media_id="missing-media",
        homography_run_id="homography-run",
    )
    missing_run = build_projection_diagnostics(
        session=db_session,
        media_id=indexed_media.id,
        homography_run_id="missing-homography-run",
    )

    assert missing_media["ok"] is False
    assert missing_media["status"] == "missing_media"
    assert missing_run["ok"] is False
    assert missing_run["status"] == "missing_homography_run"
    assert db_session.scalar(select(func.count()).select_from(ProjectionDiagnosticObservation)) == 0


def test_fixture_homography_run_produces_projection_diagnostics_with_lineage(
    db_session: Session,
    indexed_media: MediaAsset,
    court_and_homography_runs: dict[str, str],
) -> None:
    result = build_projection_diagnostics(
        session=db_session,
        media_id=indexed_media.id,
        homography_run_id=court_and_homography_runs["homography_run_id"],
    )

    assert result["ok"] is True
    assert result["status"] == "completed"
    assert result["message"] == "projection diagnostic build complete"
    assert result["source_homography_run_id"] == court_and_homography_runs["homography_run_id"]
    assert result["projection_diagnostic_run_id"]
    assert result["projection_diagnostics"] == {
        "diagnostic_candidate": 3,
        "insufficient_homography": 0,
        "total": 3,
    }
    assert result["source_counts"] == {"homography_candidate_observations": 3}
    assert result["sampled_frames"] == [0, 30, 60]
    assert result["replay_url"].endswith(
        f"/replay/{indexed_media.id}?homographyRunId="
        f"{court_and_homography_runs['homography_run_id']}"
        f"&projectionDiagnosticRunId={result['projection_diagnostic_run_id']}"
    )

    model = db_session.get(ModelRegistry, result["model_registry_id"])
    runtime_config = db_session.get(RuntimeConfig, result["runtime_config_id"])
    run = db_session.get(ProcessingRun, result["projection_diagnostic_run_id"])
    step = db_session.get(ProcessingStep, result["processing_step_id"])

    assert model is not None
    assert model.model_family == "court"
    assert model.metadata_jsonb["projection_diagnostic_builder"] is True
    assert model.metadata_jsonb["not_ball_player_projection"] is True
    assert runtime_config is not None
    assert runtime_config.payload_jsonb["diagnostic_method"] == (
        "template_projection_diagnostic_v0"
    )
    assert run is not None
    assert run.run_status == "completed"
    assert run.metadata_jsonb["projection_diagnostic_count"] == 3
    assert step is not None
    assert step.step_status == "completed"
    assert step.metadata_jsonb["source_homography_candidate_count"] == 3

    observations = db_session.scalars(
        select(Observation)
        .where(Observation.run_id == result["projection_diagnostic_run_id"])
        .order_by(Observation.frame_start)
    ).all()
    assert len(observations) == 3
    assert {observation.observation_family for observation in observations} == {"court"}
    assert {observation.observation_type for observation in observations} == {
        "projection_diagnostic_observation"
    }
    assert {observation.coordinate_space for observation in observations} == {"image_pixels"}
    assert all(
        observation.payload_jsonb["not_ball_player_projection"] is True
        for observation in observations
    )

    diagnostics = db_session.scalars(
        select(ProjectionDiagnosticObservation).order_by(
            ProjectionDiagnosticObservation.frame_number
        )
    ).all()
    assert len(diagnostics) == 3
    for diagnostic in diagnostics:
        assert diagnostic.status == "diagnostic_candidate"
        assert diagnostic.source_homography_candidate_observation_id is not None
        assert len(diagnostic.projected_template_keypoints_jsonb) == 12
        assert len(diagnostic.projected_template_lines_jsonb) == 8
        assert diagnostic.diagnostic_metrics_jsonb["projected_keypoint_count"] == 12
        assert diagnostic.diagnostic_metrics_jsonb["projected_line_count"] == 8
        assert diagnostic.diagnostic_metrics_jsonb["not_ball_player_projection"] is True
        assert diagnostic.metadata_jsonb["geometry_evidence_only"] is True
        assert diagnostic.metadata_jsonb["not_ball_player_projection"] is True
        assert diagnostic.frame_time_owner == "media_indexing"

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id.in_([row.observation_id for row in diagnostics])
        )
    ).all()
    assert len(lineage) == 3
    assert {row.relationship_type for row in lineage} == {
        "projection_diagnostic_for_homography_candidate"
    }
    assert all(row.payload_jsonb["not_ball_player_projection"] is True for row in lineage)
    parent_types = {
        db_session.get(Observation, row.parent_observation_id).observation_type
        for row in lineage
    }
    assert parent_types == {"homography_candidate_observation"}


def test_court_review_export_includes_geometry_rows_lineage_and_annotations(
    db_session: Session,
    indexed_media: MediaAsset,
    court_and_homography_runs: dict[str, str],
    tmp_path: Path,
) -> None:
    diagnostic_result = build_projection_diagnostics(
        session=db_session,
        media_id=indexed_media.id,
        homography_run_id=court_and_homography_runs["homography_run_id"],
    )
    diagnostic = db_session.scalar(select(ProjectionDiagnosticObservation))
    assert diagnostic is not None
    db_session.add(
        HumanAnnotation(
            media_id=indexed_media.id,
            observation_id=diagnostic.observation_id,
            frame_start=diagnostic.frame_number,
            frame_end=diagnostic.frame_number,
            timestamp_start_ms=diagnostic.timestamp_ms,
            timestamp_end_ms=diagnostic.timestamp_ms,
            annotation_type="projection_diagnostic_review",
            payload_jsonb={"annotation_label": "likely_good_homography_candidate"},
            created_by="test",
        )
    )
    db_session.commit()

    response = export_court_review_dataset(
        db_session,
        CourtReviewDatasetExportRequest(
            media_id=indexed_media.id,
            court_run_id=court_and_homography_runs["court_run_id"],
            homography_run_id=court_and_homography_runs["homography_run_id"],
            projection_diagnostic_run_id=str(
                diagnostic_result["projection_diagnostic_run_id"]
            ),
            output_root=str(tmp_path / "exports"),
            created_by="test",
        ),
    )

    assert response.court_keypoint_count == 3
    assert response.court_line_count == 3
    assert response.camera_view_count == 3
    assert response.homography_candidate_count == 3
    assert response.projection_diagnostic_count == 3
    assert response.warnings["not_ball_player_projection"] is True
    assert response.query_result_id is not None

    artifact = db_session.get(EvidenceArtifact, response.artifact_id)
    query_result = db_session.get(QueryResult, response.query_result_id)
    assert artifact is not None
    assert artifact.artifact_type == "court_review_dataset_export"
    assert artifact.metadata_jsonb["projection_diagnostic_count"] == 3
    assert query_result is not None
    assert query_result.result_payload_jsonb["projection_diagnostic_count"] == 3

    payload = Path(response.path).read_text(encoding="utf-8")
    assert "court_review_dataset_v0" in payload
    assert "projection_diagnostic_observations" in payload
    assert "projection_diagnostic_for_homography_candidate" in payload
    assert "likely_good_homography_candidate" in payload
    assert "not_ball_player_projection" in payload


def test_cli_handlers_return_expected_json(db_session: Session, tmp_path: Path) -> None:
    plan = _handle_build_projection_diagnostics(
        db_session,
        Namespace(
            media_id="media-plan",
            homography_run_id="homography-run-plan",
            run_name="projection-diagnostic-builder",
            frame_start=None,
            frame_end=None,
            viewer_base_url="http://127.0.0.1:3000",
            plan_only=True,
        ),
    )

    assert plan["ok"] is True
    assert plan["status"] == "planned"
    assert plan["warnings"]["no_tennis_event_interpretation"] is True

    with pytest.raises(ValueError):
        _handle_export_court_review_dataset(
            db_session,
            Namespace(
                media_id="media-plan",
                court_run_id=None,
                homography_run_id=None,
                projection_diagnostic_run_id=None,
                include_annotations=True,
                include_artifacts=True,
                format="json",
                output_root=str(tmp_path),
                query_name=None,
                created_by="test",
            ),
        )
