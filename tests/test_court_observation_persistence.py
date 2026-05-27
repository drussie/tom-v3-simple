from __future__ import annotations

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tom_v3_observations.writer import ObservationWriter, get_observation_detail
from tom_v3_schema.court import (
    COURT_KEYPOINT_NAMES,
    CameraViewObservationCreate,
    CourtKeypointObservationCreate,
    CourtLineObservationCreate,
    HomographyCandidateObservationCreate,
    ProjectionDiagnosticObservationCreate,
)
from tom_v3_schema.enums import (
    CoordinateSpace,
    ObservationFamily,
    ObservationGranularity,
    RelationshipType,
)
from tom_v3_schema.observations import ObservationCreate, ObservationLineageCreate
from tom_v3_storage.db_models import (
    Base,
    CameraViewObservation,
    CourtKeypointObservation,
    CourtLineObservation,
    HomographyCandidateObservation,
    HumanAnnotation,
    MediaAsset,
    ModelRegistry,
    Observation,
    ObservationLineage,
    ProcessingRun,
    ProjectionDiagnosticObservation,
    RuntimeConfig,
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
def court_context(db_session: Session) -> dict[str, str]:
    media = MediaAsset(
        source_uri="file:///court-schema-test.mp4",
        media_type="video",
        duration_ms=3000,
        frame_count=90,
        fps=30.0,
        width=1280,
        height=720,
        metadata_jsonb={"test": "court_schema"},
    )
    runtime_config = RuntimeConfig(
        config_name="fake-court-schema-runtime",
        config_version="v0",
        payload_jsonb={
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
        },
    )
    model = ModelRegistry(
        name="fake-court-model",
        version="v0",
        model_family="court",
        source="test",
        metadata_jsonb={"model_output_not_truth": True},
    )
    db_session.add_all([media, runtime_config, model])
    db_session.flush()
    run = ProcessingRun(
        media_id=media.id,
        run_name="fake-court-schema-run",
        run_status="completed",
        runtime_config_id=runtime_config.id,
        metadata_jsonb={
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
        },
    )
    db_session.add(run)
    db_session.commit()
    return {
        "media_id": media.id,
        "run_id": run.id,
        "model_id": model.id,
        "runtime_config_id": runtime_config.id,
    }


def court_keypoints() -> list[dict[str, object]]:
    keypoints: list[dict[str, object]] = []
    for index, name in enumerate(COURT_KEYPOINT_NAMES):
        keypoints.append(
            {
                "name": name,
                "x": 100.0 + index * 8.0,
                "y": 220.0 + index * 4.0,
                "confidence": 0.8,
                "present": True,
                "visibility": "visible",
                "source_index": index,
            }
        )
    return keypoints


def write_court_observation(
    session: Session,
    context: dict[str, str],
    observation_type: str,
    **typed_detail: object,
) -> str:
    request_kwargs = {
        "media_id": context["media_id"],
        "run_id": context["run_id"],
        "observation_family": ObservationFamily.court,
        "observation_type": observation_type,
        "granularity": ObservationGranularity.frame,
        "frame_start": 30,
        "frame_end": 30,
        "timestamp_start_ms": 1000,
        "timestamp_end_ms": 1000,
        "confidence": 0.8,
        "model_id": context["model_id"],
        "runtime_config_id": context["runtime_config_id"],
        "coordinate_space": CoordinateSpace.image_pixels,
        "payload_jsonb": {
            "observation_only": True,
            "no_adjudication": True,
            "geometry_evidence_only": True,
        },
    }
    request_kwargs.update(typed_detail)
    detail = ObservationWriter(session).write(ObservationCreate(**request_kwargs))
    return detail.id


def test_can_persist_court_keypoint_observation_with_spine_row(
    db_session: Session,
    court_context: dict[str, str],
) -> None:
    observation_id = write_court_observation(
        db_session,
        court_context,
        "court_keypoint_observation",
        court_keypoint=CourtKeypointObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            keypoints_jsonb=court_keypoints(),
        ),
    )

    observation = db_session.get(Observation, observation_id)
    keypoint = db_session.get(CourtKeypointObservation, observation_id)
    detail = get_observation_detail(db_session, observation_id)

    assert observation is not None
    assert observation.observation_family == "court"
    assert observation.observation_type == "court_keypoint_observation"
    assert observation.frame_start == 30
    assert observation.timestamp_start_ms == 1000
    assert keypoint is not None
    assert keypoint.media_id == court_context["media_id"]
    assert keypoint.run_id == court_context["run_id"]
    assert keypoint.keypoint_count == len(COURT_KEYPOINT_NAMES)
    assert keypoint.frame_time_owner == "media_indexing"
    assert keypoint.metadata_jsonb["geometry_evidence_only"] is True
    assert detail is not None
    assert detail.court_keypoint is not None


def test_can_persist_court_line_and_camera_view_observations(
    db_session: Session,
    court_context: dict[str, str],
) -> None:
    line_id = write_court_observation(
        db_session,
        court_context,
        "court_line_observation",
        court_line=CourtLineObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            line_segments_jsonb=[
                {
                    "line_class": "baseline_near",
                    "x1": 188.2,
                    "y1": 646.3,
                    "x2": 1092.7,
                    "y2": 642.9,
                    "confidence": 0.84,
                    "visibility": "partial",
                }
            ],
        ),
    )
    camera_id = write_court_observation(
        db_session,
        court_context,
        "camera_view_observation",
        camera_view=CameraViewObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            view_label="broadcast_hardcam",
            view_confidence=0.9,
            camera_motion_hint="stable",
            stability_score=0.8,
            cut_likelihood=0.03,
        ),
    )

    line = db_session.get(CourtLineObservation, line_id)
    camera = db_session.get(CameraViewObservation, camera_id)

    assert line is not None
    assert line.line_count == 1
    assert line.line_classes_jsonb == ["baseline_near"]
    assert line.frame_time_owner == "media_indexing"
    assert camera is not None
    assert camera.view_label == "broadcast_hardcam"
    assert camera.frame_start == 30
    assert camera.timestamp_start_ms == 1000
    assert camera.metadata_jsonb["no_adjudication"] is True


def test_can_persist_homography_candidate_with_source_lineage(
    db_session: Session,
    court_context: dict[str, str],
) -> None:
    keypoint_id = write_court_observation(
        db_session,
        court_context,
        "court_keypoint_observation",
        court_keypoint=CourtKeypointObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            keypoints_jsonb=court_keypoints(),
        ),
    )
    line_id = write_court_observation(
        db_session,
        court_context,
        "court_line_observation",
        court_line=CourtLineObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            line_segments_jsonb=[
                {
                    "line_class": "net_line",
                    "x1": 190.0,
                    "y1": 360.0,
                    "x2": 1090.0,
                    "y2": 361.0,
                    "confidence": 0.76,
                    "visibility": "visible",
                }
            ],
        ),
    )
    camera_id = write_court_observation(
        db_session,
        court_context,
        "camera_view_observation",
        camera_view=CameraViewObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            view_label="broadcast_hardcam",
            camera_motion_hint="stable",
        ),
    )

    homography_id = write_court_observation(
        db_session,
        court_context,
        "homography_candidate_observation",
        coordinate_space=CoordinateSpace.court_template_2d,
        homography_candidate=HomographyCandidateObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            source_court_keypoint_observation_id=keypoint_id,
            source_court_line_observation_id=line_id,
            source_camera_view_observation_id=camera_id,
            homography_matrix_jsonb=[
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            source_point_count=len(COURT_KEYPOINT_NAMES),
            source_line_count=1,
            confidence=0.72,
        ),
        lineage=[
            ObservationLineageCreate(
                parent_observation_id=keypoint_id,
                relationship_type=RelationshipType.homography_from_court_keypoints_candidate,
                payload_jsonb={"geometry_evidence_only": True},
            ),
            ObservationLineageCreate(
                parent_observation_id=line_id,
                relationship_type=RelationshipType.homography_from_court_lines_candidate,
                payload_jsonb={"geometry_evidence_only": True},
            ),
            ObservationLineageCreate(
                parent_observation_id=camera_id,
                relationship_type=RelationshipType.camera_context_for_homography_candidate,
                payload_jsonb={"geometry_evidence_only": True},
            ),
        ],
    )

    homography = db_session.get(HomographyCandidateObservation, homography_id)
    lineage = db_session.scalars(
        select(ObservationLineage)
        .where(ObservationLineage.child_observation_id == homography_id)
        .order_by(ObservationLineage.relationship_type)
    ).all()

    assert homography is not None
    assert homography.status == "candidate"
    assert homography.source_court_keypoint_observation_id == keypoint_id
    assert homography.source_court_line_observation_id == line_id
    assert homography.source_camera_view_observation_id == camera_id
    assert homography.target_coordinate_space == "court_template_2d"
    assert homography.frame_time_owner == "media_indexing"
    assert {row.relationship_type for row in lineage} == {
        "camera_context_for_homography_candidate",
        "homography_from_court_keypoints_candidate",
        "homography_from_court_lines_candidate",
    }


def test_can_persist_projection_diagnostic_linked_to_homography_candidate(
    db_session: Session,
    court_context: dict[str, str],
) -> None:
    keypoint_id = write_court_observation(
        db_session,
        court_context,
        "court_keypoint_observation",
        court_keypoint=CourtKeypointObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            keypoints_jsonb=court_keypoints(),
        ),
    )
    homography_id = write_court_observation(
        db_session,
        court_context,
        "homography_candidate_observation",
        coordinate_space=CoordinateSpace.court_template_2d,
        homography_candidate=HomographyCandidateObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            source_court_keypoint_observation_id=keypoint_id,
            homography_matrix_jsonb=[
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            confidence=0.72,
        ),
        lineage=[
            ObservationLineageCreate(
                parent_observation_id=keypoint_id,
                relationship_type=RelationshipType.homography_from_court_keypoints_candidate,
            )
        ],
    )

    diagnostic_id = write_court_observation(
        db_session,
        court_context,
        "projection_diagnostic_observation",
        coordinate_space=CoordinateSpace.image_pixels,
        projection_diagnostic=ProjectionDiagnosticObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            source_homography_candidate_observation_id=homography_id,
            projected_template_keypoints_jsonb=[
                {"name": "near_left_baseline_corner", "x": 100.0, "y": 640.0}
            ],
            diagnostic_metrics_jsonb={"mean_projection_error": 2.4},
            confidence=0.7,
        ),
        lineage=[
            ObservationLineageCreate(
                parent_observation_id=homography_id,
                relationship_type=RelationshipType.projection_diagnostic_for_homography_candidate,
                payload_jsonb={"diagnostic_candidate": True},
            )
        ],
    )

    diagnostic = db_session.get(ProjectionDiagnosticObservation, diagnostic_id)
    lineage = db_session.scalar(
        select(ObservationLineage).where(
            ObservationLineage.child_observation_id == diagnostic_id
        )
    )

    assert diagnostic is not None
    assert diagnostic.source_homography_candidate_observation_id == homography_id
    assert diagnostic.status == "diagnostic_candidate"
    assert diagnostic.metadata_jsonb["not_ball_player_projection"] is True
    assert diagnostic.frame_time_owner == "media_indexing"
    assert lineage is not None
    assert lineage.parent_observation_id == homography_id
    assert lineage.relationship_type == "projection_diagnostic_for_homography_candidate"


def test_generic_annotations_can_target_court_observations(
    db_session: Session,
    court_context: dict[str, str],
) -> None:
    keypoint_id = write_court_observation(
        db_session,
        court_context,
        "court_keypoint_observation",
        court_keypoint=CourtKeypointObservationCreate(
            frame_number=30,
            timestamp_ms=1000,
            keypoints_jsonb=court_keypoints(),
        ),
    )
    annotation = HumanAnnotation(
        media_id=court_context["media_id"],
        observation_id=keypoint_id,
        frame_start=30,
        frame_end=30,
        timestamp_start_ms=1000,
        timestamp_end_ms=1000,
        annotation_type="uncertain_court_keypoint",
        payload_jsonb={"review_only": True},
        created_by="court-schema-test",
    )
    db_session.add(annotation)
    db_session.commit()

    observation = db_session.get(Observation, keypoint_id)
    assert observation is not None
    assert observation.annotations[0].annotation_type == "uncertain_court_keypoint"
