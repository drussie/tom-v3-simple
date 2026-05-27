from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.exports import PoseReviewDatasetExportRequest
from tom_v3_schema.pose import PoseQueryFilters
from tom_v3_storage.db_models import (
    Base,
    EvidenceArtifact,
    HumanAnnotation,
    Observation,
    PoseObservation,
    QueryResult,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.db import get_session
from apps.api.main import create_app
from apps.api.services.pose_evidence_bundle import get_pose_evidence_bundle
from apps.api.services.pose_query import query_poses
from apps.api.services.pose_review_export import export_pose_review_dataset
from apps.worker.services.detection_adapter import run_detection_adapter
from apps.worker.services.pose_adapter import run_pose_adapter


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


def seed_pose_review_dataset(session: Session, tmp_path: Path) -> SimpleNamespace:
    video = tmp_path / "pose-query-review-export.mp4"
    video.write_bytes(b"tom-v3-pose-query-review-export")
    media = index_media_file(
        session=session,
        source_path=video,
        copy_to_storage=True,
        storage_root=tmp_path / "media",
        probe_result=probe_result(),
    )
    detection_result = run_detection_adapter(
        session=session,
        media_id=media.id,
        adapter_name="fixture",
        run_name="pose-query-source-detections",
        frame_sample_rate=30,
        max_frames=1,
    )
    source_detection = session.scalar(
        select(Observation)
        .where(
            Observation.run_id == detection_result["run_id"],
            Observation.observation_type == "player_detection",
        )
        .order_by(Observation.id)
    )
    assert source_detection is not None

    pose_result = run_pose_adapter(
        session=session,
        media_id=media.id,
        source_detection_run_id=str(detection_result["run_id"]),
        link_source_detections=True,
        max_frames=1,
    )
    pose_id = str(pose_result["observation_ids"][0])
    pose = session.get(PoseObservation, pose_id)
    assert pose is not None

    annotation = HumanAnnotation(
        media_id=media.id,
        observation_id=pose_id,
        evidence_artifact_id=None,
        frame_start=pose.frame_number,
        frame_end=pose.frame_number,
        timestamp_start_ms=pose.timestamp_ms,
        timestamp_end_ms=pose.timestamp_ms,
        annotation_type="bad_keypoint",
        payload_jsonb={
            "annotation_label": "bad_keypoint",
            "keypoint_name": "right_wrist",
            "keypoint_index": 10,
            "review_context": "pose_query_review_export_test",
        },
        created_by="pose-reviewer",
    )
    artifact = EvidenceArtifact(
        media_id=media.id,
        run_id=str(detection_result["run_id"]),
        target_observation_id=source_detection.id,
        artifact_type="frame_image",
        uri=(tmp_path / "source-frame.jpg").as_uri(),
        frame_start=source_detection.frame_start,
        frame_end=source_detection.frame_end,
        timestamp_start_ms=source_detection.timestamp_start_ms,
        timestamp_end_ms=source_detection.timestamp_end_ms,
        checksum="test-frame-checksum",
        metadata_jsonb={"source": "pose_query_review_export_test"},
    )
    session.add_all([annotation, artifact])
    session.commit()

    return SimpleNamespace(
        media_id=media.id,
        detection_run_id=str(detection_result["run_id"]),
        source_detection_id=source_detection.id,
        pose_run_id=str(pose_result["pose_run_id"]),
        pose_id=pose_id,
        annotation_id=annotation.id,
        artifact_id=artifact.id,
    )


def export_payload(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))[
        "pose_review_dataset_export"
    ]


def test_pose_query_filters_and_annotation_summary(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_pose_review_dataset(db_session, tmp_path)

    by_run = query_poses(db_session, PoseQueryFilters(run_id=seeded.pose_run_id))
    assert by_run.count == 1
    row = by_run.poses[0]
    assert row.observation["id"] == seeded.pose_id
    assert row.pose["skeleton_format"] == "coco17"
    assert row.subject_detection_observation_id == seeded.source_detection_id
    assert row.annotation_summary["labels"]["bad_keypoint"] == 1

    assert (
        query_poses(db_session, PoseQueryFilters(pose_confidence_min=0.7)).count == 1
    )
    assert (
        query_poses(db_session, PoseQueryFilters(pose_confidence_max=0.1)).count == 0
    )
    assert (
        query_poses(db_session, PoseQueryFilters(keypoints_missing_count_min=2)).count
        == 1
    )
    assert (
        query_poses(db_session, PoseQueryFilters(keypoints_missing_count_max=1)).count
        == 0
    )
    assert query_poses(db_session, PoseQueryFilters(skeleton_format="coco17")).count == 1
    assert query_poses(db_session, PoseQueryFilters(association_status="candidate")).count == 1
    assert (
        query_poses(
            db_session,
            PoseQueryFilters(subject_detection_observation_id=seeded.source_detection_id),
        ).count
        == 1
    )
    assert query_poses(db_session, PoseQueryFilters(review_label="bad_keypoint")).count == 1


def test_pose_api_query_and_evidence_bundle_endpoints(
    db_session: Session,
    client: TestClient,
    tmp_path: Path,
) -> None:
    seeded = seed_pose_review_dataset(db_session, tmp_path)

    query_response = client.post("/pose/query", json={"run_id": seeded.pose_run_id})
    assert query_response.status_code == 200
    assert query_response.json()["count"] == 1

    bundle_response = client.get(f"/pose-observations/{seeded.pose_id}/evidence-bundle")
    assert bundle_response.status_code == 200
    bundle = bundle_response.json()
    assert bundle["pose_observation"]["pose"]["observation_id"] == seeded.pose_id
    assert bundle["source_context"]["source_detection"]["id"] == seeded.source_detection_id
    assert bundle["summary"]["no_movement_interpretation"] is True


def test_pose_evidence_bundle_includes_lineage_source_and_annotation(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_pose_review_dataset(db_session, tmp_path)

    bundle = get_pose_evidence_bundle(db_session, seeded.pose_id)

    assert bundle is not None
    assert bundle["pose_observation"]["pose"]["observation_id"] == seeded.pose_id
    assert bundle["source_context"]["source_detection"]["id"] == seeded.source_detection_id
    assert bundle["lineage"][0]["relationship_type"] == "pose_from_subject_detection_candidate"
    assert bundle["annotations"][0]["payload_jsonb"]["keypoint_name"] == "right_wrist"
    assert bundle["annotation_summary"]["labels"]["bad_keypoint"] == 1
    assert bundle["artifacts"][0]["id"] == seeded.artifact_id


def test_pose_annotation_does_not_mutate_pose_observation(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_pose_review_dataset(db_session, tmp_path)
    before = db_session.get(PoseObservation, seeded.pose_id)
    assert before is not None
    before_keypoints = list(before.keypoints_jsonb)

    db_session.add(
        HumanAnnotation(
            media_id=seeded.media_id,
            observation_id=seeded.pose_id,
            annotation_type="keypoint_occluded",
            payload_jsonb={
                "annotation_label": "keypoint_occluded",
                "keypoint_name": "left_wrist",
                "keypoint_index": 9,
            },
            created_by="pose-reviewer",
        )
    )
    db_session.commit()

    after = db_session.get(PoseObservation, seeded.pose_id)
    assert after is not None
    assert after.keypoints_jsonb == before_keypoints
    assert after.keypoints_missing_count == before.keypoints_missing_count


def test_pose_review_export_creates_artifact_query_result_and_tom_native_json(
    db_session: Session,
    tmp_path: Path,
) -> None:
    seeded = seed_pose_review_dataset(db_session, tmp_path)

    response = export_pose_review_dataset(
        db_session,
        PoseReviewDatasetExportRequest(
            run_id=seeded.pose_run_id,
            output_root=str(tmp_path / "exports"),
            query_name="pose-run-review-export",
        ),
    )

    assert response.pose_count == 1
    assert Path(response.path).is_file()
    assert response.checksum
    assert response.query_result_id is not None
    artifact = db_session.get(EvidenceArtifact, response.artifact_id)
    assert artifact is not None
    assert artifact.artifact_type == "pose_review_dataset_export"
    assert artifact.checksum == response.checksum
    assert artifact.metadata_jsonb["pose_evidence_only"] is True
    assert artifact.metadata_jsonb["no_movement_interpretation"] is True
    assert artifact.metadata_jsonb["no_adjudication"] is True
    query_result = db_session.get(QueryResult, response.query_result_id)
    assert query_result is not None
    assert query_result.query_name == "pose-run-review-export"
    assert query_result.result_payload_jsonb["pose_observation_ids"] == [seeded.pose_id]

    payload = export_payload(response.path)
    assert payload["warnings"]["pose_evidence_only"] is True
    assert payload["warnings"]["annotations_are_reviews_only"] is True
    assert payload["selection"]["pose_observation_ids"] == [seeded.pose_id]
    record = payload["records"][0]
    assert record["record_type"] == "pose_observation_review"
    assert record["pose_observation"]["observation_id"] == seeded.pose_id
    assert len(record["pose_observation"]["keypoints"]) == 17
    assert record["subject_context"]["source_detection_observation_id"] == (
        seeded.source_detection_id
    )
    assert record["lineage"][0]["relationship_type"] == "pose_from_subject_detection_candidate"
    assert record["annotations"][0]["payload_jsonb"]["annotation_label"] == "bad_keypoint"
