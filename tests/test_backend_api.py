from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_storage.db_models import Base

from apps.api.db import get_session
from apps.api.main import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
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

    def override_get_session() -> Generator[Session, None, None]:
        session = testing_session()
        try:
            yield session
        finally:
            session.close()

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


def create_foundation(client: TestClient) -> dict[str, str]:
    media = client.post(
        "/media",
        json={
            "source_uri": "file:///tmp/dev-tennis.mp4",
            "media_type": "video",
            "duration_ms": 120000,
            "frame_count": 3600,
            "fps": 30,
            "width": 1920,
            "height": 1080,
            "checksum": "dev-checksum",
        },
    )
    assert media.status_code == 201
    media_id = media.json()["id"]

    model = client.post(
        "/models",
        json={
            "name": "synthetic-test-model",
            "version": "0.0.0",
            "model_family": "synthetic",
            "source": "pytest",
        },
    )
    assert model.status_code == 201
    model_id = model.json()["id"]

    runtime_config = client.post(
        "/runtime-configs",
        json={
            "config_name": "pytest-config",
            "config_version": "v0",
            "payload_jsonb": {"mode": "test"},
        },
    )
    assert runtime_config.status_code == 201
    runtime_config_id = runtime_config.json()["id"]

    run = client.post(
        f"/media/{media_id}/runs",
        json={
            "run_name": "pytest-run",
            "run_status": "running",
            "runtime_config_id": runtime_config_id,
        },
    )
    assert run.status_code == 201
    run_id = run.json()["id"]

    step = client.post(
        f"/runs/{run_id}/steps",
        json={
            "step_name": "pytest-step",
            "step_status": "completed",
            "runtime_config_id": runtime_config_id,
        },
    )
    assert step.status_code == 201
    step_id = step.json()["id"]

    return {
        "media_id": media_id,
        "model_id": model_id,
        "runtime_config_id": runtime_config_id,
        "run_id": run_id,
        "step_id": step_id,
    }


def test_health_and_foundation_resources(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    foundation = create_foundation(client)

    assert client.get(f"/media/{foundation['media_id']}").status_code == 200
    assert client.get(f"/models/{foundation['model_id']}").status_code == 200
    assert client.get(f"/runtime-configs/{foundation['runtime_config_id']}").status_code == 200
    assert client.get(f"/runs/{foundation['run_id']}").status_code == 200

    steps = client.get(f"/runs/{foundation['run_id']}/steps")
    assert steps.status_code == 200
    assert steps.json()[0]["id"] == foundation["step_id"]


def test_observation_writer_query_lineage_artifacts_and_annotations(
    client: TestClient,
) -> None:
    foundation = create_foundation(client)
    media_id = foundation["media_id"]
    run_id = foundation["run_id"]
    model_id = foundation["model_id"]
    runtime_config_id = foundation["runtime_config_id"]
    step_id = foundation["step_id"]

    gameplay_request = {
        "media_id": media_id,
        "run_id": run_id,
        "observation_family": "gameplay",
        "observation_type": "view_state",
        "granularity": "frame_range",
        "frame_start": 10,
        "frame_end": 40,
        "timestamp_start_ms": 333,
        "timestamp_end_ms": 1333,
        "confidence": 0.92,
        "model_id": model_id,
        "runtime_config_id": runtime_config_id,
        "coordinate_space": "none",
        "payload_jsonb": {"source": "pytest"},
        "idempotency_key": "pytest-gameplay-10-40",
        "gameplay": {
            "view_state": "gameplay",
            "view_state_subtype": "active_point",
            "payload_jsonb": {"reason_codes": ["pytest"]},
        },
    }
    gameplay = client.post("/observations", json=gameplay_request)
    assert gameplay.status_code == 201
    gameplay_id = gameplay.json()["id"]
    assert gameplay.json()["gameplay"]["view_state"] == "gameplay"

    duplicate = client.post("/observations", json=gameplay_request)
    assert duplicate.status_code == 201
    assert duplicate.json()["id"] == gameplay_id

    atomic = client.post(
        "/observations",
        json={
            "media_id": media_id,
            "run_id": run_id,
            "observation_family": "atomic",
            "observation_type": "ball_detection",
            "granularity": "frame",
            "frame_start": 20,
            "frame_end": 20,
            "timestamp_start_ms": 667,
            "timestamp_end_ms": 667,
            "confidence": 0.82,
            "model_id": model_id,
            "runtime_config_id": runtime_config_id,
            "coordinate_space": "image_pixels",
            "payload_jsonb": {"bbox": [100, 200, 10, 10]},
            "idempotency_key": "pytest-ball-20",
            "atomic": {
                "atomic_kind": "ball_detection",
                "payload_jsonb": {"center": [105, 205]},
            },
            "lineage": [
                {
                    "parent_observation_id": gameplay_id,
                    "relationship_type": "scoped_by",
                    "processing_step_id": step_id,
                }
            ],
            "artifacts": [
                {
                    "artifact_type": "overlay_frame",
                    "uri": "file:///tmp/artifacts/ball-20.png",
                    "frame_start": 20,
                    "frame_end": 20,
                }
            ],
        },
    )
    assert atomic.status_code == 201
    atomic_body = atomic.json()
    atomic_id = atomic_body["id"]
    assert atomic_body["atomic"]["atomic_kind"] == "ball_detection"
    assert atomic_body["artifacts"][0]["artifact_type"] == "overlay_frame"

    derived = client.post(
        "/observations",
        json={
            "media_id": media_id,
            "run_id": run_id,
            "observation_family": "derived",
            "observation_type": "bounce_candidate",
            "granularity": "frame",
            "frame_start": 21,
            "frame_end": 21,
            "timestamp_start_ms": 700,
            "timestamp_end_ms": 700,
            "confidence": 0.55,
            "model_id": model_id,
            "runtime_config_id": runtime_config_id,
            "coordinate_space": "image_pixels",
            "payload_jsonb": {"candidate": "placeholder"},
            "idempotency_key": "pytest-bounce-candidate-21",
            "derived": {
                "derived_kind": "bounce_candidate",
                "derivation_payload_jsonb": {"source_observation_id": atomic_id},
            },
            "lineage": [
                {
                    "parent_observation_id": atomic_id,
                    "relationship_type": "derived_from",
                    "processing_step_id": step_id,
                }
            ],
        },
    )
    assert derived.status_code == 201
    derived_id = derived.json()["id"]

    batch = client.post(
        "/observations/batch",
        json={
            "observations": [
                {
                    "media_id": media_id,
                    "run_id": run_id,
                    "observation_family": "atomic",
                    "observation_type": "player_detection",
                    "granularity": "frame",
                    "frame_start": 20,
                    "frame_end": 20,
                    "confidence": 0.91,
                    "model_id": model_id,
                    "runtime_config_id": runtime_config_id,
                    "coordinate_space": "image_pixels",
                    "payload_jsonb": {"subject_ref": "near_player"},
                    "idempotency_key": "pytest-player-20",
                    "atomic": {
                        "atomic_kind": "player_detection",
                        "payload_jsonb": {"subject_ref": "near_player"},
                    },
                },
                {
                    "media_id": media_id,
                    "run_id": run_id,
                    "observation_family": "gameplay",
                    "observation_type": "view_state",
                    "granularity": "frame_range",
                    "frame_start": 41,
                    "frame_end": 55,
                    "confidence": 0.76,
                    "model_id": model_id,
                    "runtime_config_id": runtime_config_id,
                    "coordinate_space": "none",
                    "idempotency_key": "pytest-non-gameplay-41-55",
                    "gameplay": {
                        "view_state": "non_gameplay",
                        "view_state_subtype": "between_points",
                    },
                },
            ]
        },
    )
    assert batch.status_code == 201
    assert len(batch.json()["observations"]) == 2

    type_query = client.post(
        "/observations/query",
        json={
            "media_id": media_id,
            "run_id": run_id,
            "observation_type": "ball_detection",
        },
    )
    assert type_query.status_code == 200
    assert type_query.json()["count"] == 1

    frame_query = client.post(
        "/observations/query",
        json={"media_id": media_id, "frame_start_gte": 20, "frame_end_lte": 21},
    )
    assert frame_query.status_code == 200
    assert frame_query.json()["count"] >= 2

    confidence_query = client.post(
        "/observations/query",
        json={"media_id": media_id, "confidence_gte": 0.9},
    )
    assert confidence_query.status_code == 200
    assert confidence_query.json()["count"] >= 2

    gameplay_query = client.post(
        "/observations/query",
        json={"media_id": media_id, "gameplay_label": "gameplay"},
    )
    assert gameplay_query.status_code == 200
    assert gameplay_query.json()["count"] == 1

    detail = client.get(f"/observations/{derived_id}")
    assert detail.status_code == 200
    assert detail.json()["derived"]["derived_kind"] == "bounce_candidate"

    atomic_lineage = client.get(f"/observations/{atomic_id}/lineage")
    assert atomic_lineage.status_code == 200
    assert atomic_lineage.json()["parents"][0]["parent_observation_id"] == gameplay_id

    gameplay_lineage = client.get(f"/observations/{gameplay_id}/lineage")
    assert gameplay_lineage.status_code == 200
    assert gameplay_lineage.json()["children"][0]["child_observation_id"] == atomic_id

    artifacts = client.get(f"/observations/{atomic_id}/artifacts")
    assert artifacts.status_code == 200
    artifact_id = artifacts.json()[0]["id"]
    assert client.get(f"/artifacts/{artifact_id}").status_code == 200

    direct_artifact = client.post(
        "/artifacts",
        json={
            "target_observation_id": derived_id,
            "artifact_type": "json_payload",
            "uri": "file:///tmp/artifacts/derived-21.json",
        },
    )
    assert direct_artifact.status_code == 201
    assert direct_artifact.json()["media_id"] == media_id

    before_annotation = client.get(f"/observations/{atomic_id}").json()
    annotation = client.post(
        "/annotations",
        json={
            "observation_id": atomic_id,
            "annotation_type": "review_note",
            "payload_jsonb": {"note": "inspect later"},
            "created_by": "pytest",
        },
    )
    assert annotation.status_code == 201
    annotations = client.get(f"/observations/{atomic_id}/annotations")
    assert annotations.status_code == 200
    assert annotations.json()[0]["id"] == annotation.json()["id"]
    after_annotation = client.get(f"/observations/{atomic_id}").json()
    assert after_annotation["id"] == before_annotation["id"]
    assert after_annotation["payload_jsonb"] == before_annotation["payload_jsonb"]


def test_dev_synthetic_run_and_tracklet_query(client: TestClient) -> None:
    synthetic = client.post("/dev/synthetic-run")
    assert synthetic.status_code == 200
    body = synthetic.json()
    assert body["scenario"] == "baseline-tennis-clip"
    assert body["seed_version"] == "0C"
    assert body["verification"]["ok"] is True
    assert len(body["observation_ids_by_type"]["view_state"]) == 4
    assert len(body["observation_ids_by_type"]["ball_detection"]) >= 7
    assert len(body["observation_ids_by_type"]["player_detection"]) >= 8
    assert len(body["observation_ids_by_type"]["homography_placeholder"]) == 3
    assert len(body["observation_ids_by_type"]["bounce_candidate"]) == 1
    assert len(body["observation_ids_by_type"]["tracking_gap_candidate"]) == 1
    assert body["artifact_count"] >= 6
    assert body["track_point_count"] >= 15

    tracklet_query = client.post(
        "/observations/query",
        json={"tracklet_id": body["tracklet_id"]},
    )
    assert tracklet_query.status_code == 200
    assert tracklet_query.json()["count"] >= 1

    uncertain_query = client.post(
        "/observations/query",
        json={"run_id": body["run_id"], "gameplay_label": "uncertain"},
    )
    assert uncertain_query.status_code == 200
    assert uncertain_query.json()["count"] == 1

    candidate_id = body["candidate_observation_ids"]["bounce_candidate"]
    detail = client.get(f"/observations/{candidate_id}")
    assert detail.status_code == 200
    assert detail.json()["derived"]["derived_kind"] == "bounce_candidate"

    lineage = client.get(f"/observations/{candidate_id}/lineage")
    assert lineage.status_code == 200
    assert len(lineage.json()["parents"]) >= 4

    artifacts = client.get(f"/observations/{candidate_id}/artifacts")
    assert artifacts.status_code == 200
    assert len(artifacts.json()) >= 3
