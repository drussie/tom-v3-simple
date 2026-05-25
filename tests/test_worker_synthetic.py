from collections.abc import Generator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from tom_v3_observations.synthetic import create_synthetic_run, verify_synthetic_run
from tom_v3_schema.observations import ObservationQueryFilters
from tom_v3_storage.db_models import (
    EvidenceArtifact,
    GameplayObservation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProcessingStep,
    RuntimeConfig,
    Tracklet,
    TrackPoint,
)

from apps.api.services.query_builder import query_observations
from apps.worker.cli import main as worker_cli_main
from apps.worker.scenarios.baseline_tennis_clip import build_scenario


def test_worker_cli_imports() -> None:
    assert callable(worker_cli_main)


def test_baseline_synthetic_scenario_creates_viewer_ready_evidence(
    db_session: Session,
) -> None:
    scenario = build_scenario()
    result = create_synthetic_run(db_session, scenario=scenario)
    run_id = result["run_id"]

    assert db_session.get(MediaAsset, result["media_id"]) is not None
    assert db_session.get(RuntimeConfig, result["runtime_config_id"]) is not None
    assert db_session.get(ModelRegistry, result["model_id"]) is not None
    assert db_session.get(ProcessingRun, run_id) is not None
    assert len(result["processing_step_ids"]) == 7

    steps = db_session.scalars(
        select(ProcessingStep).where(ProcessingStep.run_id == run_id)
    ).all()
    assert {step.step_name for step in steps} == {
        "synthetic_media_indexing",
        "synthetic_gameplay_classification",
        "synthetic_detection_generation",
        "synthetic_tracking_generation",
        "synthetic_homography_generation",
        "synthetic_candidate_generation",
        "synthetic_artifact_generation",
    }

    view_states = db_session.scalars(
        select(GameplayObservation.view_state)
        .join(Observation, Observation.id == GameplayObservation.observation_id)
        .where(Observation.run_id == run_id)
    ).all()
    assert view_states.count("gameplay") == 2
    assert "non_gameplay" in view_states
    assert "uncertain" in view_states

    observation_ids_by_type = result["observation_ids_by_type"]
    assert len(observation_ids_by_type["ball_detection"]) >= 7
    assert len(observation_ids_by_type["player_detection"]) >= 8
    assert len(observation_ids_by_type["homography_placeholder"]) == 3
    assert len(observation_ids_by_type["bounce_candidate"]) == 1
    assert len(observation_ids_by_type["tracking_gap_candidate"]) == 1

    tracklets = db_session.scalars(
        select(Tracklet).where(Tracklet.run_id == run_id)
    ).all()
    assert len(tracklets) == 3
    coverage_segments = [
        segment
        for tracklet in tracklets
        for segment in tracklet.metadata_jsonb["coverage_segments"]
    ]
    assert any(segment["state"] == "gap" for segment in coverage_segments)
    assert any(segment["state"] == "low_confidence" for segment in coverage_segments)

    track_points = db_session.scalars(
        select(TrackPoint).join(Tracklet).where(Tracklet.run_id == run_id)
    ).all()
    assert len(track_points) >= 15

    missing_homography = db_session.scalar(
        select(Observation).where(
            Observation.run_id == run_id,
            Observation.observation_type == "homography_placeholder",
            Observation.frame_start == 801,
        )
    )
    assert missing_homography is not None
    assert missing_homography.payload_jsonb["homography_status"] == "missing"

    bounce_candidate_id = result["candidate_observation_ids"]["bounce_candidate"]
    lineage_rows = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == bounce_candidate_id
        )
    ).all()
    relationship_types = {row.relationship_type for row in lineage_rows}
    assert {"derived_from", "scoped_by", "projected_using"}.issubset(relationship_types)

    candidate_artifacts = db_session.scalars(
        select(EvidenceArtifact).where(
            EvidenceArtifact.target_observation_id == bounce_candidate_id
        )
    ).all()
    assert {artifact.artifact_type for artifact in candidate_artifacts} >= {
        "overlay_frame",
        "overlay_clip",
        "trajectory_plot",
    }

    ball_query = query_observations(
        db_session,
        ObservationQueryFilters(run_id=run_id, observation_type="ball_detection"),
    )
    assert ball_query.count >= 7

    gameplay_query = query_observations(
        db_session,
        ObservationQueryFilters(run_id=run_id, gameplay_label="uncertain"),
    )
    assert gameplay_query.count == 1

    verification = verify_synthetic_run(db_session, run_id)
    assert verification["ok"] is True


def test_synthetic_seed_creates_new_run_by_default(db_session: Session) -> None:
    first = create_synthetic_run(db_session)
    second = create_synthetic_run(db_session)

    assert first["run_id"] != second["run_id"]
    assert first["media_id"] != second["media_id"]
    assert first["rerun_behavior"] == "new_run_by_default"


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    from tom_v3_storage.db_models import Base

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
