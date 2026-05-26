from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_observations.synthetic import create_synthetic_run
from tom_v3_storage.db_models import Base

from apps.api.db import get_session
from apps.api.main import create_app


@pytest.fixture()
def seeded_viewer_client() -> Generator[tuple[TestClient, dict[str, object]], None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )

    with testing_session() as session:
        seed_result = create_synthetic_run(session)

    def override_get_session() -> Generator[Session, None, None]:
        session = testing_session()
        try:
            yield session
        finally:
            session.close()

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client, seed_result


def test_viewer_run_endpoint_composes_seeded_evidence(
    seeded_viewer_client: tuple[TestClient, dict[str, object]],
) -> None:
    client, seed_result = seeded_viewer_client
    run_id = str(seed_result["run_id"])

    response = client.get(f"/viewer/runs/{run_id}")
    assert response.status_code == 200
    body = response.json()

    assert body["run"]["id"] == run_id
    assert body["media"]["source_uri"] == "file:///dev/synthetic-tennis-clip.mp4"
    assert {step["step_name"] for step in body["steps"]} >= {
        "synthetic_gameplay_classification",
        "synthetic_candidate_generation",
    }

    observation_types = {row["observation_type"] for row in body["observations"]}
    assert {
        "view_state",
        "ball_detection",
        "player_detection",
        "homography_placeholder",
        "bounce_candidate",
        "tracking_gap_candidate",
        "hit_candidate",
    }.issubset(observation_types)

    gameplay_states = {
        row["gameplay"]["view_state"]
        for row in body["observations"]
        if row["gameplay"] is not None
    }
    assert {"gameplay", "non_gameplay", "uncertain"}.issubset(gameplay_states)

    tracklets = body["tracklets"]
    assert len(tracklets) == 3
    coverage_segments = [
        segment
        for tracklet in tracklets
        for segment in tracklet["metadata_jsonb"]["coverage_segments"]
    ]
    assert any(segment["state"] == "gap" for segment in coverage_segments)
    assert any(segment["state"] == "low_confidence" for segment in coverage_segments)
    assert sum(len(tracklet["points"]) for tracklet in tracklets) >= 15

    candidate_ids = {
        row["id"]
        for row in body["observations"]
        if row["observation_type"]
        in {"bounce_candidate", "tracking_gap_candidate", "hit_candidate"}
    }
    assert candidate_ids
    assert any(row["child_observation_id"] in candidate_ids for row in body["lineage"])
    assert any(row["target_observation_id"] in candidate_ids for row in body["artifacts"])


def test_viewer_run_endpoint_returns_404_for_missing_run(
    seeded_viewer_client: tuple[TestClient, dict[str, object]],
) -> None:
    client, _ = seeded_viewer_client
    response = client.get("/viewer/runs/missing-run")
    assert response.status_code == 404
