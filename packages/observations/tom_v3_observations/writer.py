from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tom_v3_schema.artifacts import EvidenceArtifactRead
from tom_v3_schema.observations import (
    AtomicObservationRead,
    CameraViewObservationRead,
    CourtKeypointObservationRead,
    CourtLineObservationRead,
    DerivedObservationRead,
    GameplayObservationRead,
    HomographyCandidateObservationRead,
    ObservationCreate,
    ObservationDetailRead,
    PoseObservationRead,
    ProjectionDiagnosticObservationRead,
)
from tom_v3_storage.db_models import (
    AtomicObservation,
    CameraViewObservation,
    CourtKeypointObservation,
    CourtLineObservation,
    DerivedObservation,
    EvidenceArtifact,
    GameplayObservation,
    HomographyCandidateObservation,
    Observation,
    ObservationLineage,
    PoseObservation,
    ProjectionDiagnosticObservation,
)


class ObservationWriterError(ValueError):
    pass


def enum_value(value: Any) -> Any:
    return getattr(value, "value", value)


def artifact_read_from_model(artifact: EvidenceArtifact) -> EvidenceArtifactRead:
    return EvidenceArtifactRead.model_validate(artifact)


def observation_detail_from_model(observation: Observation) -> ObservationDetailRead:
    gameplay = None
    if observation.gameplay_detail is not None:
        gameplay = GameplayObservationRead.model_validate(observation.gameplay_detail)

    atomic = None
    if observation.atomic_detail is not None:
        atomic = AtomicObservationRead.model_validate(observation.atomic_detail)

    derived = None
    if observation.derived_detail is not None:
        derived = DerivedObservationRead.model_validate(observation.derived_detail)

    pose = None
    if observation.pose_detail is not None:
        pose = PoseObservationRead.model_validate(observation.pose_detail)

    court_keypoint = None
    if observation.court_keypoint_detail is not None:
        court_keypoint = CourtKeypointObservationRead.model_validate(
            observation.court_keypoint_detail
        )

    court_line = None
    if observation.court_line_detail is not None:
        court_line = CourtLineObservationRead.model_validate(observation.court_line_detail)

    camera_view = None
    if observation.camera_view_detail is not None:
        camera_view = CameraViewObservationRead.model_validate(observation.camera_view_detail)

    homography_candidate = None
    if observation.homography_candidate_detail is not None:
        homography_candidate = HomographyCandidateObservationRead.model_validate(
            observation.homography_candidate_detail
        )

    projection_diagnostic = None
    if observation.projection_diagnostic_detail is not None:
        projection_diagnostic = ProjectionDiagnosticObservationRead.model_validate(
            observation.projection_diagnostic_detail
        )

    return ObservationDetailRead(
        id=observation.id,
        media_id=observation.media_id,
        run_id=observation.run_id,
        observation_family=observation.observation_family,
        observation_type=observation.observation_type,
        granularity=observation.granularity,
        frame_start=observation.frame_start,
        frame_end=observation.frame_end,
        timestamp_start_ms=observation.timestamp_start_ms,
        timestamp_end_ms=observation.timestamp_end_ms,
        confidence=observation.confidence,
        model_id=observation.model_id,
        runtime_config_id=observation.runtime_config_id,
        coordinate_space=observation.coordinate_space,
        schema_version=observation.schema_version,
        payload_jsonb=observation.payload_jsonb,
        idempotency_key=observation.idempotency_key,
        created_at=observation.created_at,
        gameplay=gameplay,
        atomic=atomic,
        derived=derived,
        pose=pose,
        court_keypoint=court_keypoint,
        court_line=court_line,
        camera_view=camera_view,
        homography_candidate=homography_candidate,
        projection_diagnostic=projection_diagnostic,
        artifacts=[artifact_read_from_model(artifact) for artifact in observation.artifacts],
    )


def get_observation_detail(session: Session, observation_id: str) -> ObservationDetailRead | None:
    observation = session.get(Observation, observation_id)
    if observation is None:
        return None
    return observation_detail_from_model(observation)


class ObservationWriter:
    def __init__(self, session: Session):
        self.session = session

    def write(self, request: ObservationCreate) -> ObservationDetailRead:
        if request.idempotency_key:
            existing = self._find_by_idempotency_key(request.idempotency_key)
            if existing is not None:
                return observation_detail_from_model(existing)

        self._validate_typed_extension(request)
        observation = Observation(
            media_id=request.media_id,
            run_id=request.run_id,
            observation_family=str(enum_value(request.observation_family)),
            observation_type=request.observation_type,
            granularity=str(enum_value(request.granularity)),
            frame_start=request.frame_start,
            frame_end=request.frame_end,
            timestamp_start_ms=request.timestamp_start_ms,
            timestamp_end_ms=request.timestamp_end_ms,
            confidence=request.confidence,
            model_id=request.model_id,
            runtime_config_id=request.runtime_config_id,
            coordinate_space=(
                str(enum_value(request.coordinate_space)) if request.coordinate_space else None
            ),
            schema_version=request.schema_version,
            payload_jsonb=request.payload_jsonb,
            idempotency_key=request.idempotency_key,
        )

        try:
            self.session.add(observation)
            self.session.flush()
            self._insert_typed_extension(observation, request)
            self._insert_lineage(observation, request)
            self._insert_artifacts(observation, request)
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            if request.idempotency_key:
                existing = self._find_by_idempotency_key(request.idempotency_key)
                if existing is not None:
                    return observation_detail_from_model(existing)
            raise ObservationWriterError(str(exc)) from exc

        self.session.refresh(observation)
        return observation_detail_from_model(observation)

    def write_many(self, requests: list[ObservationCreate]) -> list[ObservationDetailRead]:
        return [self.write(request) for request in requests]

    def _find_by_idempotency_key(self, idempotency_key: str) -> Observation | None:
        return self.session.scalar(
            select(Observation).where(Observation.idempotency_key == idempotency_key)
        )

    def _validate_typed_extension(self, request: ObservationCreate) -> None:
        typed_count = sum(
            detail is not None
            for detail in (
                request.gameplay,
                request.atomic,
                request.derived,
                request.pose,
                request.court_keypoint,
                request.court_line,
                request.camera_view,
                request.homography_candidate,
                request.projection_diagnostic,
            )
        )
        if typed_count > 1:
            raise ObservationWriterError(
                "only one typed observation extension can be written at once"
            )

        family = str(enum_value(request.observation_family))
        if request.gameplay is not None and family != "gameplay":
            raise ObservationWriterError("gameplay detail requires observation_family=gameplay")
        if request.atomic is not None and family != "atomic":
            raise ObservationWriterError("atomic detail requires observation_family=atomic")
        if request.derived is not None and family != "derived":
            raise ObservationWriterError("derived detail requires observation_family=derived")
        if request.pose is not None and family != "pose":
            raise ObservationWriterError("pose detail requires observation_family=pose")
        court_details = (
            request.court_keypoint,
            request.court_line,
            request.camera_view,
            request.homography_candidate,
            request.projection_diagnostic,
        )
        if any(detail is not None for detail in court_details) and family != "court":
            raise ObservationWriterError("court details require observation_family=court")

    def _insert_typed_extension(
        self, observation: Observation, request: ObservationCreate
    ) -> None:
        if request.gameplay is not None:
            self.session.add(
                GameplayObservation(
                    observation_id=observation.id,
                    view_state=str(enum_value(request.gameplay.view_state)),
                    view_state_subtype=(
                        str(enum_value(request.gameplay.view_state_subtype))
                        if request.gameplay.view_state_subtype
                        else None
                    ),
                    payload_jsonb=request.gameplay.payload_jsonb,
                )
            )
        if request.atomic is not None:
            self.session.add(
                AtomicObservation(
                    observation_id=observation.id,
                    atomic_kind=str(enum_value(request.atomic.atomic_kind)),
                    payload_jsonb=request.atomic.payload_jsonb,
                )
            )
        if request.derived is not None:
            self.session.add(
                DerivedObservation(
                    observation_id=observation.id,
                    derived_kind=str(enum_value(request.derived.derived_kind)),
                    derivation_payload_jsonb=request.derived.derivation_payload_jsonb,
                )
            )
        if request.pose is not None:
            self.session.add(
                PoseObservation(
                    observation_id=observation.id,
                    media_id=observation.media_id,
                    run_id=observation.run_id,
                    frame_number=request.pose.frame_number,
                    timestamp_ms=request.pose.timestamp_ms,
                    skeleton_format=request.pose.skeleton_format,
                    skeleton_version=request.pose.skeleton_version,
                    keypoint_schema_jsonb=request.pose.keypoint_schema_jsonb,
                    keypoints_jsonb=request.pose.keypoints_jsonb,
                    keypoint_count=request.pose.keypoint_count or 0,
                    keypoints_present_count=request.pose.keypoints_present_count or 0,
                    keypoints_missing_count=request.pose.keypoints_missing_count or 0,
                    mean_keypoint_confidence=request.pose.mean_keypoint_confidence,
                    min_keypoint_confidence=request.pose.min_keypoint_confidence,
                    max_keypoint_confidence=request.pose.max_keypoint_confidence,
                    pose_confidence=request.pose.pose_confidence,
                    bbox_x=request.pose.bbox_x,
                    bbox_y=request.pose.bbox_y,
                    bbox_w=request.pose.bbox_w,
                    bbox_h=request.pose.bbox_h,
                    bbox_confidence=request.pose.bbox_confidence,
                    crop_x=request.pose.crop_x,
                    crop_y=request.pose.crop_y,
                    crop_w=request.pose.crop_w,
                    crop_h=request.pose.crop_h,
                    crop_source=request.pose.crop_source,
                    subject_ref_type=request.pose.subject_ref_type,
                    subject_detection_observation_id=request.pose.subject_detection_observation_id,
                    subject_tracklet_id=request.pose.subject_tracklet_id,
                    subject_track_point_id=request.pose.subject_track_point_id,
                    association_status=request.pose.association_status,
                    association_method=request.pose.association_method,
                    association_confidence=request.pose.association_confidence,
                    frame_time_owner=request.pose.frame_time_owner,
                    raw_model_payload_jsonb=request.pose.raw_model_payload_jsonb,
                    metadata_jsonb=request.pose.metadata_jsonb,
                )
            )
        if request.court_keypoint is not None:
            self.session.add(
                CourtKeypointObservation(
                    observation_id=observation.id,
                    media_id=observation.media_id,
                    run_id=observation.run_id,
                    frame_number=request.court_keypoint.frame_number,
                    timestamp_ms=request.court_keypoint.timestamp_ms,
                    court_keypoint_schema=request.court_keypoint.court_keypoint_schema,
                    schema_version=request.court_keypoint.schema_version,
                    keypoints_jsonb=request.court_keypoint.keypoints_jsonb,
                    keypoint_count=request.court_keypoint.keypoint_count or 0,
                    keypoints_present_count=request.court_keypoint.keypoints_present_count or 0,
                    keypoints_missing_count=request.court_keypoint.keypoints_missing_count or 0,
                    mean_keypoint_confidence=request.court_keypoint.mean_keypoint_confidence,
                    min_keypoint_confidence=request.court_keypoint.min_keypoint_confidence,
                    max_keypoint_confidence=request.court_keypoint.max_keypoint_confidence,
                    coordinate_space=request.court_keypoint.coordinate_space,
                    model_id=observation.model_id,
                    runtime_config_id=observation.runtime_config_id,
                    frame_time_owner=request.court_keypoint.frame_time_owner,
                    raw_model_payload_jsonb=request.court_keypoint.raw_model_payload_jsonb,
                    metadata_jsonb=request.court_keypoint.metadata_jsonb,
                )
            )
        if request.court_line is not None:
            self.session.add(
                CourtLineObservation(
                    observation_id=observation.id,
                    media_id=observation.media_id,
                    run_id=observation.run_id,
                    frame_number=request.court_line.frame_number,
                    timestamp_ms=request.court_line.timestamp_ms,
                    line_segments_jsonb=request.court_line.line_segments_jsonb,
                    line_classes_jsonb=request.court_line.line_classes_jsonb,
                    line_count=request.court_line.line_count or 0,
                    mean_line_confidence=request.court_line.mean_line_confidence,
                    coordinate_space=request.court_line.coordinate_space,
                    model_id=observation.model_id,
                    runtime_config_id=observation.runtime_config_id,
                    frame_time_owner=request.court_line.frame_time_owner,
                    raw_model_payload_jsonb=request.court_line.raw_model_payload_jsonb,
                    metadata_jsonb=request.court_line.metadata_jsonb,
                )
            )
        if request.camera_view is not None:
            self.session.add(
                CameraViewObservation(
                    observation_id=observation.id,
                    media_id=observation.media_id,
                    run_id=observation.run_id,
                    frame_number=request.camera_view.frame_number,
                    timestamp_ms=request.camera_view.timestamp_ms,
                    frame_start=request.camera_view.frame_start,
                    frame_end=request.camera_view.frame_end,
                    timestamp_start_ms=request.camera_view.timestamp_start_ms,
                    timestamp_end_ms=request.camera_view.timestamp_end_ms,
                    view_label=request.camera_view.view_label,
                    view_confidence=request.camera_view.view_confidence,
                    camera_motion_hint=request.camera_view.camera_motion_hint,
                    stability_score=request.camera_view.stability_score,
                    cut_likelihood=request.camera_view.cut_likelihood,
                    model_id=observation.model_id,
                    runtime_config_id=observation.runtime_config_id,
                    frame_time_owner=request.camera_view.frame_time_owner,
                    metadata_jsonb=request.camera_view.metadata_jsonb,
                )
            )
        if request.homography_candidate is not None:
            self.session.add(
                HomographyCandidateObservation(
                    observation_id=observation.id,
                    media_id=observation.media_id,
                    run_id=observation.run_id,
                    frame_number=request.homography_candidate.frame_number,
                    timestamp_ms=request.homography_candidate.timestamp_ms,
                    source_court_keypoint_observation_id=(
                        request.homography_candidate.source_court_keypoint_observation_id
                    ),
                    source_court_line_observation_id=(
                        request.homography_candidate.source_court_line_observation_id
                    ),
                    source_camera_view_observation_id=(
                        request.homography_candidate.source_camera_view_observation_id
                    ),
                    homography_matrix_jsonb=request.homography_candidate.homography_matrix_jsonb,
                    inverse_homography_matrix_jsonb=(
                        request.homography_candidate.inverse_homography_matrix_jsonb
                    ),
                    source_coordinate_space=request.homography_candidate.source_coordinate_space,
                    target_coordinate_space=request.homography_candidate.target_coordinate_space,
                    matrix_direction=request.homography_candidate.matrix_direction,
                    template_name=request.homography_candidate.template_name,
                    template_version=request.homography_candidate.template_version,
                    reprojection_error_mean=(
                        request.homography_candidate.reprojection_error_mean
                    ),
                    reprojection_error_median=(
                        request.homography_candidate.reprojection_error_median
                    ),
                    reprojection_error_max=request.homography_candidate.reprojection_error_max,
                    inlier_count=request.homography_candidate.inlier_count,
                    outlier_count=request.homography_candidate.outlier_count,
                    source_point_count=request.homography_candidate.source_point_count,
                    source_line_count=request.homography_candidate.source_line_count,
                    confidence=request.homography_candidate.confidence,
                    status=request.homography_candidate.status,
                    model_id=observation.model_id,
                    runtime_config_id=observation.runtime_config_id,
                    frame_time_owner=request.homography_candidate.frame_time_owner,
                    metadata_jsonb=request.homography_candidate.metadata_jsonb,
                )
            )
        if request.projection_diagnostic is not None:
            self.session.add(
                ProjectionDiagnosticObservation(
                    observation_id=observation.id,
                    media_id=observation.media_id,
                    run_id=observation.run_id,
                    frame_number=request.projection_diagnostic.frame_number,
                    timestamp_ms=request.projection_diagnostic.timestamp_ms,
                    source_homography_candidate_observation_id=(
                        request.projection_diagnostic.source_homography_candidate_observation_id
                    ),
                    projected_template_keypoints_jsonb=(
                        request.projection_diagnostic.projected_template_keypoints_jsonb
                    ),
                    projected_template_lines_jsonb=(
                        request.projection_diagnostic.projected_template_lines_jsonb
                    ),
                    diagnostic_metrics_jsonb=(
                        request.projection_diagnostic.diagnostic_metrics_jsonb
                    ),
                    overlay_artifact_id=request.projection_diagnostic.overlay_artifact_id,
                    confidence=request.projection_diagnostic.confidence,
                    status=request.projection_diagnostic.status,
                    model_id=observation.model_id,
                    runtime_config_id=observation.runtime_config_id,
                    frame_time_owner=request.projection_diagnostic.frame_time_owner,
                    metadata_jsonb=request.projection_diagnostic.metadata_jsonb,
                )
            )

    def _insert_lineage(self, observation: Observation, request: ObservationCreate) -> None:
        for lineage in request.lineage:
            self.session.add(
                ObservationLineage(
                    child_observation_id=observation.id,
                    parent_observation_id=lineage.parent_observation_id,
                    relationship_type=str(enum_value(lineage.relationship_type)),
                    processing_step_id=lineage.processing_step_id,
                    payload_jsonb=lineage.payload_jsonb,
                )
            )

    def _insert_artifacts(self, observation: Observation, request: ObservationCreate) -> None:
        for artifact in request.artifacts:
            self.session.add(
                EvidenceArtifact(
                    media_id=artifact.media_id or observation.media_id,
                    run_id=artifact.run_id or observation.run_id,
                    target_observation_id=artifact.target_observation_id or observation.id,
                    artifact_type=artifact.artifact_type,
                    uri=artifact.uri,
                    frame_start=artifact.frame_start,
                    frame_end=artifact.frame_end,
                    timestamp_start_ms=artifact.timestamp_start_ms,
                    timestamp_end_ms=artifact.timestamp_end_ms,
                    checksum=artifact.checksum,
                    metadata_jsonb=artifact.metadata_jsonb,
                )
            )
