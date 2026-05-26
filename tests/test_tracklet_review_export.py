from __future__ import annotations

import json
import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.exports import TrackletReviewDatasetExportRequest
from tom_v3_schema.tracklets import TrackletQueryFilters
from tom_v3_storage.db_models import (
    Base,
    EvidenceArtifact,
    HumanAnnotation,
    QueryResult,
    Tracklet,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.services.tracklet_review_export import export_tracklet_review_dataset
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.frame_artifacts import extract_frame_artifacts_for_run
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


def fake_ffmpeg_runner(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
    Path(command[-1]).write_bytes(b"fake-review-export-frame")
    return subprocess.CompletedProcess(command, 0, "", "")


def seed_tracklet_run(
    db_session: Session,
    tmp_path: Path,
    *,
    with_artifacts: bool = False,
    with_annotation: bool = False,
) -> dict[str, object]:
    video = tmp_path / "tracklet-review-export-source.mp4"
    video.write_bytes(b"tom-v3-tracklet-review-export")
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
        run_name="tracklet-review-export-detection-run",
        frame_sample_rate=30,
        max_frames=3,
        output_debug_artifact=True,
    )
    if with_artifacts:
        extract_frame_artifacts_for_run(
            session=db_session,
            run_id=str(detection_result["run_id"]),
            max_frames=1,
            output_root=tmp_path / "artifacts",
            runner=fake_ffmpeg_runner,
        )
    tracklet_result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=30,
    )
    if with_annotation:
        tracklet = db_session.get(Tracklet, tracklet_result["tracklet_ids"][0])
        assert tracklet is not None
        annotation = HumanAnnotation(
            media_id=media.id,
            observation_id=tracklet.observation_id,
            evidence_artifact_id=None,
            frame_start=tracklet.frame_start,
            frame_end=tracklet.frame_end,
            timestamp_start_ms=None,
            timestamp_end_ms=None,
            annotation_type="bad_tracklet",
            payload_jsonb={
                "annotation_label": "bad_tracklet",
                "review_context": "tracklet_review_export_test",
                "review_status": "reviewed",
                "notes": "candidate grouping jumps in fixture evidence",
            },
            created_by="test-reviewer",
        )
        db_session.add(annotation)
        db_session.commit()
    return {
        "media_id": media.id,
        "detection_run_id": detection_result["run_id"],
        "tracklet_run_id": tracklet_result["tracklet_run_id"],
        "tracklet_ids": tracklet_result["tracklet_ids"],
    }


def export_payload(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))[
        "tracklet_review_dataset_export"
    ]


def test_export_by_tracklet_id_creates_json_artifact_and_checksum(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_artifacts=True, with_annotation=True)

    response = export_tracklet_review_dataset(
        db_session,
        TrackletReviewDatasetExportRequest(
            tracklet_ids=[str(seeded["tracklet_ids"][0])],
            output_root=str(tmp_path / "exports"),
        ),
    )

    assert response.tracklet_count == 1
    assert Path(response.path).is_file()
    assert response.checksum
    artifact = db_session.get(EvidenceArtifact, response.artifact_id)
    assert artifact is not None
    assert artifact.artifact_type == "tracklet_review_dataset_export"
    assert artifact.checksum == response.checksum
    assert artifact.metadata_jsonb["candidate_evidence_only"] is True
    assert artifact.metadata_jsonb["annotations_are_reviews_not_truth"] is True
    assert artifact.metadata_jsonb["no_adjudication"] is True

    payload = export_payload(response.path)
    assert payload["warnings"]["candidate_evidence_only"] is True
    assert payload["warnings"]["annotations_are_reviews_not_truth"] is True
    assert payload["warnings"]["no_adjudication"] is True
    assert payload["selection"]["tracklet_ids"] == [str(seeded["tracklet_ids"][0])]
    assert payload["tracklets"][0]["tracklet"]["typed"]["id"] == seeded["tracklet_ids"][0]
    assert payload["annotations"]
    assert payload["artifacts"]
    assert payload["lineage"]


def test_export_by_query_reuses_tracklet_query_and_persists_query_result(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_annotation=True)

    response = export_tracklet_review_dataset(
        db_session,
        TrackletReviewDatasetExportRequest(
            query=TrackletQueryFilters(
                track_family="ball",
                has_annotation=True,
                review_label="bad_tracklet",
            ),
            output_root=str(tmp_path / "exports"),
            query_name="annotated-ball-candidates",
        ),
    )

    assert response.tracklet_count == 1
    assert response.query_result_id is not None
    query_result = db_session.get(QueryResult, response.query_result_id)
    assert query_result is not None
    assert query_result.query_name == "annotated-ball-candidates"
    assert query_result.result_payload_jsonb["tracklet_ids"] == [
        str(seeded["tracklet_ids"][0])
    ]
    assert query_result.result_payload_jsonb["export_artifact_id"] == response.artifact_id
    payload = export_payload(response.path)
    assert payload["query_spec"]["query"]["track_family"] == "ball"


def test_export_can_exclude_annotations_and_frame_artifacts(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_artifacts=True, with_annotation=True)

    response = export_tracklet_review_dataset(
        db_session,
        TrackletReviewDatasetExportRequest(
            tracklet_ids=[str(seeded["tracklet_ids"][0])],
            include_annotations=False,
            include_frame_artifacts=False,
            output_root=str(tmp_path / "exports"),
        ),
    )

    payload = export_payload(response.path)
    assert payload["annotations"] == []
    assert payload["artifacts"] == []
    assert payload["tracklets"][0]["annotations"] == []
    assert payload["tracklets"][0]["annotation_summary"] == {}
    assert payload["tracklets"][0]["frame_artifacts"] == []
    assert all(point["frame_artifacts"] == [] for point in payload["tracklets"][0]["track_points"])


def test_export_succeeds_without_frame_artifacts(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path, with_artifacts=False)

    response = export_tracklet_review_dataset(
        db_session,
        TrackletReviewDatasetExportRequest(
            tracklet_ids=[str(seeded["tracklet_ids"][0])],
            output_root=str(tmp_path / "exports"),
        ),
    )

    payload = export_payload(response.path)
    assert payload["artifacts"] == []
    assert payload["tracklets"][0]["frame_artifacts"] == []


def test_export_endpoint_returns_artifact_metadata(
    client: TestClient,
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_tracklet_run(db_session, tmp_path)

    response = client.post(
        "/tracklets/export-review-dataset",
        json={
            "tracklet_ids": [seeded["tracklet_ids"][0]],
            "output_root": str(tmp_path / "exports"),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["tracklet_count"] == 1
    assert Path(body["path"]).is_file()
    assert body["metadata"]["export_version"] == "tracklet_review_dataset_v0"


def test_export_worker_cli_handler_exports_selected_tracklet(
    db_session: Session,
    tmp_path: Path,
) -> None:
    from argparse import Namespace

    from apps.worker.cli import _handle_export_tracklet_review_dataset

    seeded = seed_tracklet_run(db_session, tmp_path)

    result = _handle_export_tracklet_review_dataset(
        db_session,
        Namespace(
            tracklet_ids=[str(seeded["tracklet_ids"][0])],
            query_json=None,
            output_root=str(tmp_path / "exports"),
            format="json",
            include_frame_artifacts=True,
            include_annotations=True,
            query_name=None,
            created_by="worker-test",
        ),
    )

    assert result["tracklet_count"] == 1
    assert Path(result["path"]).is_file()
    assert db_session.get(EvidenceArtifact, result["artifact_id"]) is not None
