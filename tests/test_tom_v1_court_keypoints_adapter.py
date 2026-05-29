from __future__ import annotations

from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_model_adapters.court_keypoints import (
    FakeCourtKeypointResultProvider,
    map_tom_v1_raw_keypoints_to_tom_v3,
    probe_tom_v1_court_keypoint_model,
)
from tom_v3_storage.db_models import (
    Base,
    CourtKeypointObservation,
    CourtLineObservation,
    EvidenceArtifact,
    HomographyCandidateObservation,
    MediaAsset,
    Observation,
    ObservationLineage,
)
from tom_v3_storage.media_indexer import index_media_file
from tom_v3_video.probe import VideoProbeResult

from apps.api.services.replay import court_keypoint_overlay_item_from_row
from apps.worker.cli import (
    _handle_run_real_court_keypoints,
    _handle_tom_v1_court_keypoints_probe,
)
from apps.worker.services.homography_candidate_builder import build_homography_candidates
from apps.worker.services.real_court_keypoint_replay import (
    derive_court_line_candidates_from_keypoints,
    run_real_court_keypoint_replay,
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
    video = tmp_path / "tom-v1-court-keypoints.mp4"
    video.write_bytes(b"tom-v3-tom-v1-court-keypoints")
    return index_media_file(
        session=db_session,
        source_path=str(video),
        copy_to_storage=True,
        media_name="tom v1 court keypoint adapter test clip",
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


def test_tom_v1_court_keypoints_probe_handles_missing_model(tmp_path: Path) -> None:
    missing = tmp_path / "model_assets" / "tom_v1" / "keypoints_model.pth"
    result = probe_tom_v1_court_keypoint_model(
        weights_path=str(missing),
        allowed_roots=[tmp_path / "model_assets" / "tom_v1"],
    )

    assert result["ok"] is False
    assert result["status"] == "missing"
    assert result["weights_validation"]["exists"] is False
    assert result["geometry_evidence_only"] is True


def test_cli_probe_handler_returns_clean_missing_model_result(
    db_session: Session,
    tmp_path: Path,
) -> None:
    result = _handle_tom_v1_court_keypoints_probe(
        db_session,
        Namespace(
            weights=str(tmp_path / "missing-keypoints.pth"),
            allowed_roots=[str(tmp_path)],
        ),
    )

    assert result["ok"] is False
    assert result["status"] == "missing"


def test_tom_v1_raw_keypoints_normalize_to_tom_v3_schema() -> None:
    provider = FakeCourtKeypointResultProvider()
    raw = provider.predict_frame(
        Namespace(
            frame_number=0,
            timestamp_ms=0,
            image_width=640,
            image_height=360,
        )
    )["raw_keypoints"]

    keypoints = map_tom_v1_raw_keypoints_to_tom_v3(raw, image_width=640, image_height=360)

    assert [point["name"] for point in keypoints] == [
        "near_left_baseline_corner",
        "near_right_baseline_corner",
        "far_left_baseline_corner",
        "far_right_baseline_corner",
        "left_net_post",
        "right_net_post",
        "service_line_t_near_left",
        "service_line_t_near_right",
        "service_line_t_far_left",
        "service_line_t_far_right",
        "center_mark_near",
        "center_mark_far",
    ]
    assert all(point["present"] for point in keypoints)
    assert {point["visibility"] for point in keypoints[-4:]} >= {
        "visible",
        "inferred_by_adapter",
    }


def test_derived_lines_require_present_keypoints() -> None:
    provider = FakeCourtKeypointResultProvider()
    raw = provider.predict_frame(
        Namespace(
            frame_number=0,
            timestamp_ms=0,
            image_width=640,
            image_height=360,
        )
    )["raw_keypoints"]
    keypoints = map_tom_v1_raw_keypoints_to_tom_v3(raw, image_width=640, image_height=360)

    all_lines = derive_court_line_candidates_from_keypoints(keypoints)
    assert {line["line_class"] for line in all_lines} == {
        "baseline_near",
        "baseline_far",
        "sideline_left",
        "sideline_right",
        "service_line_near",
        "service_line_far",
        "center_service_line",
        "net_line",
    }

    sparse_keypoints = [
        {**point, "present": False, "x": None, "y": None}
        if point["name"] == "near_right_baseline_corner"
        else point
        for point in keypoints
    ]
    sparse_lines = derive_court_line_candidates_from_keypoints(sparse_keypoints)
    assert "baseline_near" not in {line["line_class"] for line in sparse_lines}


def test_real_court_keypoint_run_persists_model_output_evidence(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    result = run_real_court_keypoint_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=None,
        result_provider=FakeCourtKeypointResultProvider(),
        every_n_frames=30,
        max_frames=3,
        emit_debug_artifacts=True,
    )

    assert result["ok"] is True
    assert result["observations"] == {
        "court_keypoint_observation": 3,
        "court_line_observation": 3,
        "camera_view_observation": 0,
        "total": 6,
    }
    assert result["warnings"]["real_model_output"] is True
    assert result["calibration_debug"]["debug_artifact_count"] == 3

    keypoint = db_session.scalar(
        select(CourtKeypointObservation).where(
            CourtKeypointObservation.run_id == result["court_run_id"]
        )
    )
    line = db_session.scalar(
        select(CourtLineObservation).where(CourtLineObservation.run_id == result["court_run_id"])
    )
    assert keypoint is not None
    assert keypoint.metadata_jsonb["real_model_output"] is True
    assert keypoint.metadata_jsonb["fixture_court_evidence"] is False
    assert keypoint.metadata_jsonb["model_output_not_truth"] is True
    assert keypoint.raw_model_payload_jsonb["preprocessing_mode"] == "full_frame_resize_224"
    assert (
        keypoint.raw_model_payload_jsonb["coordinate_interpretation"]
        == "output_as_pixels_224"
    )
    assert len(keypoint.raw_model_payload_jsonb["tom_v1_raw_keypoints"]) == 14
    assert len(keypoint.raw_model_payload_jsonb["raw_keypoints_scaled_to_image"]) == 14
    assert keypoint.raw_model_payload_jsonb["mapped_tom_v3_keypoints"]
    assert keypoint.raw_model_payload_jsonb["uncalibrated_tom_v1_keypoint_mapping"] is True
    assert line is not None
    assert line.metadata_jsonb["line_source"] == "derived_from_real_keypoint_observations"
    assert line.metadata_jsonb["candidate_line_only"] is True

    overlay = court_keypoint_overlay_item_from_row(keypoint)
    assert overlay["evidence_source"] == "real_model_output"
    assert overlay["source_label"] == "real court keypoint model output"
    assert overlay["is_real_model_output"] is True
    assert overlay["model_output_not_truth"] is True
    assert overlay["preprocessing_mode"] == "full_frame_resize_224"
    assert overlay["coordinate_interpretation"] == "output_as_pixels_224"
    assert overlay["raw_tom_v1_keypoints"][0]["label"] == "raw_0"
    assert overlay["raw_tom_v1_keypoints"][0]["image_x"] is not None
    assert overlay["mapped_keypoints"][0]["name"] == "near_left_baseline_corner"
    assert overlay["uncalibrated_tom_v1_keypoint_mapping"] is True

    artifact = db_session.scalar(
        select(EvidenceArtifact).where(
            EvidenceArtifact.target_observation_id == keypoint.observation_id
        )
    )
    assert artifact is not None
    assert artifact.artifact_type == "tom_v1_court_keypoint_calibration_debug_json"
    assert artifact.metadata_jsonb["raw_keypoints_scaled_to_image"]
    assert artifact.metadata_jsonb["mapped_tom_v3_keypoints"]
    assert artifact.metadata_jsonb["warnings"]["not_court_truth"] is True


def test_cli_handler_plan_only_for_real_court_keypoints(db_session: Session) -> None:
    result = _handle_run_real_court_keypoints(
        db_session,
        Namespace(
            media_id="media-plan",
            weights="model_assets/tom_v1/keypoints_model.pth",
            model_name="tom-v1-court-keypoints",
            model_version="v1-local",
            run_name="real-court-keypoints-replay",
            device="auto",
            img_size=640,
            every_n_frames=30,
            frame_start=None,
            frame_end=None,
            max_frames=214,
            allowed_roots=["model_assets/tom_v1"],
            viewer_base_url="http://127.0.0.1:3000",
            derive_lines=True,
            preprocessing_mode="full_frame_resize_224",
            coordinate_interpretation="output_as_pixels_224",
            emit_debug_artifacts=True,
            plan_only=True,
        ),
    )

    assert result["ok"] is True
    assert result["status"] == "planned"
    assert "run-real-court-keypoints" in result["plan"]["command"]
    assert result["plan"]["runtime"]["recognized_model_input_size"] == 224
    assert result["plan"]["runtime"]["preprocessing_mode"] == "full_frame_resize_224"
    assert result["plan"]["court_schema"]["emit_debug_artifacts"] is True


def test_real_court_keypoint_run_rejects_unsupported_calibration_modes(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    result = run_real_court_keypoint_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=None,
        result_provider=FakeCourtKeypointResultProvider(),
        preprocessing_mode="letterbox_224",
    )

    assert result["ok"] is False
    assert result["status"] == "unsupported_preprocessing_mode"
    assert "only full_frame_resize_224" in result["message"]


def test_homography_builder_preserves_real_court_source_metadata(
    db_session: Session,
    indexed_media: MediaAsset,
) -> None:
    court_result = run_real_court_keypoint_replay(
        session=db_session,
        media_id=indexed_media.id,
        weights_path=None,
        result_provider=FakeCourtKeypointResultProvider(),
        every_n_frames=30,
        max_frames=1,
    )

    homography_result = build_homography_candidates(
        session=db_session,
        media_id=indexed_media.id,
        court_run_id=str(court_result["court_run_id"]),
    )

    assert homography_result["ok"] is True
    homography = db_session.scalar(
        select(HomographyCandidateObservation).where(
            HomographyCandidateObservation.run_id == homography_result["homography_run_id"]
        )
    )
    assert homography is not None
    assert homography.metadata_jsonb["source_court_evidence_source"] == "real_model_output"
    assert homography.metadata_jsonb["source_court_keypoint_real_model_output"] is True
    assert homography.metadata_jsonb["source_court_line_derived_from_real_keypoints"] is True
    assert (
        homography.metadata_jsonb["source_court_keypoint_preprocessing_mode"]
        == "full_frame_resize_224"
    )
    assert (
        homography.metadata_jsonb["source_court_keypoint_coordinate_interpretation"]
        == "output_as_pixels_224"
    )
    assert homography.metadata_jsonb["source_court_keypoint_uncalibrated_mapping"] is True
    assert homography.metadata_jsonb["homography_from_uncalibrated_tom_v1_keypoints"] is True

    lineage = db_session.scalars(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == homography.observation_id
        )
    ).all()
    assert lineage
    assert all(row.payload_jsonb["geometry_evidence_only"] is True for row in lineage)
    assert any(
        row.payload_jsonb["source_court_keypoint_real_model_output"] is True
        for row in lineage
    )

    assert not db_session.scalars(
        select(Observation).where(
            Observation.observation_type.in_(
                ["bounce_detection", "hit_detection", "in_out_decision", "score"]
            )
        )
    ).all()
