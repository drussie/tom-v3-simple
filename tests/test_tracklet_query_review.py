from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.tracklets import TrackletQueryFilters
from tom_v3_storage.db_models import Base
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.services.tracklet_evidence_bundle import build_tracklet_evidence_bundle
from apps.api.services.tracklet_query import query_tracklets
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.tracklet_builder import build_tracklets_from_detection_run


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
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_session() -> Generator[Session, None, None]:
        yield db_session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


def probe_result() -> VideoProbeResult:
    return VideoProbeResult(
        duration_ms=3_000,
        frame_count=90,
        fps=30.0,
        width=640,
        height=360,
        codec="h264",
        format="mp4",
        raw_probe={"streams": [{"codec_type": "video"}]},
        frame_count_source="test_fixture",
    )


def seed_tracklet_run(
    db_session: Session,
    tmp_path: Path,
    max_gap_frames: int = 30,
) -> dict[str, object]:
    video = tmp_path / "tracklet-query-source.mp4"
    video.write_bytes(b"tom-v3-tracklet-query")
    media = index_media_file(
        session=db_session,
        source_path=video,
        copy_to_storage=True,
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )
    detection_result = run_detection_adapter(
        session=db_session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="tracklet-query-detection-run",
        frame_sample_rate=30,
        max_frames=3,
    )
    tracklet_result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=max_gap_frames,
    )
    return {
        "media_id": media.id,
        "detection_run_id": detection_result["run_id"],
        "tracklet_run_id": tracklet_result["tracklet_run_id"],
        "tracklet_ids": tracklet_result["tracklet_ids"],
    }


def test_tracklet_query_filters_by_family_subject_source_and_points(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path)

    ball = query_tracklets(db_session, TrackletQueryFilters(track_family="ball"))
    assert ball.count == 1
    assert ball.tracklets[0].track_family == "ball"
    assert ball.tracklets[0].track_point_count == 3
    assert ball.summary["by_track_family"] == {"ball": 1}

    near_player = query_tracklets(
        db_session,
        TrackletQueryFilters(subject_ref="near_player", min_track_points=2),
    )
    assert near_player.count == 1
    assert near_player.tracklets[0].subject_ref == "near_player"

    source_run = query_tracklets(
        db_session,
        TrackletQueryFilters(source_detection_run_id=str(seeded["detection_run_id"])),
    )
    assert source_run.count == 3


def test_tracklet_query_filters_by_frame_confidence_and_gaps(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seed_tracklet_run(db_session, tmp_path)

    result = query_tracklets(
        db_session,
        TrackletQueryFilters(
            frame_start_gte=0,
            frame_end_lte=60,
            confidence_gte=0.5,
            confidence_lte=1.0,
            gap_count_gte=2,
            has_gaps=True,
        ),
    )

    assert result.count == 3
    assert result.summary["by_gap_state"] == {"has_gaps": 3}
    assert all(row.gap_count == 2 for row in result.tracklets)


def test_tracklet_query_endpoint_returns_summaries(
    client: TestClient,
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path)

    response = client.post(
        "/tracklets/query",
        json={
            "source_detection_run_id": seeded["detection_run_id"],
            "track_family": "player",
            "limit": 50,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["summary"]["by_track_family"] == {"player": 2}
    assert all(row["evidence_bundle_url"].startswith("/tracklets/") for row in body["tracklets"])
    assert all(row["annotation_summary"]["count"] == 0 for row in body["tracklets"])


def test_review_annotations_attach_to_tracklet_point_and_source_detection(
    client: TestClient,
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path)
    bundle = build_tracklet_evidence_bundle(db_session, str(seeded["tracklet_ids"][0]))
    assert bundle is not None

    tracklet_observation_id = bundle["tracklet"]["observation"]["id"]
    point_observation_id = bundle["track_points"][0]["observation"]["id"]
    source_detection_observation_id = bundle["track_points"][0]["source_detection"]["id"]

    for observation_id, label in [
        (tracklet_observation_id, "bad_tracklet"),
        (point_observation_id, "wrong_point_assignment"),
        (source_detection_observation_id, "bad_bbox"),
    ]:
        response = client.post(
            "/annotations",
            json={
                "observation_id": observation_id,
                "annotation_type": label,
                "payload_jsonb": {
                    "annotation_label": label,
                    "review_context": "tracklet_evidence_bundle",
                    "review_status": "reviewed",
                    "notes": f"review note for {label}",
                },
                "created_by": "test-reviewer",
            },
        )
        assert response.status_code == 201

    refreshed = client.get(f"/tracklets/{seeded['tracklet_ids'][0]}/evidence-bundle").json()
    assert refreshed["tracklet"]["annotation_summary"]["labels"] == {"bad_tracklet": 1}
    assert refreshed["track_points"][0]["annotation_summary"]["labels"] == {
        "wrong_point_assignment": 1
    }
    source_summary = refreshed["source_detections"][0]["annotation_summary"]
    assert source_summary["labels"] == {"bad_bbox": 1}
    assert refreshed["annotation_summary"]["all"]["count"] == 3

    query_response = client.post(
        "/tracklets/query",
        json={"review_label": "bad_tracklet", "has_annotation": True},
    )
    assert query_response.status_code == 200
    assert query_response.json()["count"] == 1
