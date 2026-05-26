from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_schema.exports import TrackletReviewDatasetExportRequest
from tom_v3_schema.tracklets import TrackletQueryFilters
from tom_v3_storage.db_models import Base, HumanAnnotation, Observation
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.services.tracklet_evidence_bundle import build_tracklet_evidence_bundle
from apps.api.services.tracklet_query import query_tracklets
from apps.api.services.tracklet_review_export import export_tracklet_review_dataset
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


def test_blueprint_2_query_review_and_export_preserve_source_observations(
    db_session: Session,
    tmp_path: Path,
) -> None:
    video = tmp_path / "blueprint-2-source.mp4"
    video.write_bytes(b"tom-v3-blueprint-2-invariant")
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
        run_name="blueprint-2-detection-run",
        frame_sample_rate=30,
        max_frames=3,
    )
    tracklet_result = build_tracklets_from_detection_run(
        session=db_session,
        detection_run_id=str(detection_result["run_id"]),
        max_gap_frames=30,
    )
    bundle = build_tracklet_evidence_bundle(
        db_session,
        str(tracklet_result["tracklet_ids"][0]),
    )
    assert bundle is not None

    source_detection_id = bundle["track_points"][0]["source_detection_observation_id"]
    source_before = db_session.get(Observation, source_detection_id)
    assert source_before is not None
    snapshot = {
        "observation_family": source_before.observation_family,
        "observation_type": source_before.observation_type,
        "frame_start": source_before.frame_start,
        "frame_end": source_before.frame_end,
        "timestamp_start_ms": source_before.timestamp_start_ms,
        "timestamp_end_ms": source_before.timestamp_end_ms,
        "payload_jsonb": dict(source_before.payload_jsonb),
        "confidence": source_before.confidence,
    }

    query = query_tracklets(
        db_session,
        TrackletQueryFilters(
            source_detection_run_id=str(detection_result["run_id"]),
            track_family=bundle["tracklet"]["typed"]["track_family"],
        ),
    )
    assert query.count >= 1

    db_session.add(
        HumanAnnotation(
            media_id=media.id,
            observation_id=bundle["tracklet"]["observation"]["id"],
            annotation_type="bad_tracklet",
            payload_jsonb={
                "annotation_label": "bad_tracklet",
                "review_context": "blueprint_2_invariant",
                "review_status": "reviewed",
            },
            created_by="pytest",
        )
    )
    db_session.commit()

    export = export_tracklet_review_dataset(
        db_session,
        TrackletReviewDatasetExportRequest(
            query=TrackletQueryFilters(has_annotation=True),
            output_root=str(tmp_path / "exports"),
        ),
    )
    assert export.warnings == {
        "candidate_evidence_only": True,
        "annotations_are_reviews_not_truth": True,
        "no_adjudication": True,
    }

    source_after = db_session.get(Observation, source_detection_id)
    assert source_after is not None
    assert {
        "observation_family": source_after.observation_family,
        "observation_type": source_after.observation_type,
        "frame_start": source_after.frame_start,
        "frame_end": source_after.frame_end,
        "timestamp_start_ms": source_after.timestamp_start_ms,
        "timestamp_end_ms": source_after.timestamp_end_ms,
        "payload_jsonb": dict(source_after.payload_jsonb),
        "confidence": source_after.confidence,
    } == snapshot

    source_annotations = db_session.scalars(
        select(HumanAnnotation).where(HumanAnnotation.observation_id == source_detection_id)
    ).all()
    assert source_annotations == []
