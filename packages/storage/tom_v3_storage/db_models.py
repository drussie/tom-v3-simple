from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from tom_v3_schema.ids import new_uuid

JsonType = JSON().with_variant(JSONB, "postgresql")


class Base(DeclarativeBase):
    pass


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class MediaAsset(CreatedAtMixin, Base):
    __tablename__ = "media_asset"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    source_uri: Mapped[str] = mapped_column(Text, nullable=False)
    media_type: Mapped[str] = mapped_column(String(50), nullable=False, default="video")
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    frame_count: Mapped[int | None] = mapped_column(Integer)
    fps: Mapped[float | None] = mapped_column(Float)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    checksum: Mapped[str | None] = mapped_column(String(255))
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    runs: Mapped[list["ProcessingRun"]] = relationship(back_populates="media")
    observations: Mapped[list["Observation"]] = relationship(back_populates="media")


class ModelRegistry(CreatedAtMixin, Base):
    __tablename__ = "model_registry"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    model_family: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source: Mapped[str | None] = mapped_column(Text)
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)


class RuntimeConfig(CreatedAtMixin, Base):
    __tablename__ = "runtime_config"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    config_name: Mapped[str] = mapped_column(String(200), nullable=False)
    config_version: Mapped[str] = mapped_column(String(100), nullable=False, default="v0")
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)


class ProcessingRun(Base):
    __tablename__ = "processing_run"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    media_id: Mapped[str] = mapped_column(ForeignKey("media_asset.id"), nullable=False, index=True)
    run_name: Mapped[str] = mapped_column(String(200), nullable=False)
    run_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="queued", index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    runtime_config_id: Mapped[str | None] = mapped_column(ForeignKey("runtime_config.id"))
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    media: Mapped[MediaAsset] = relationship(back_populates="runs")
    runtime_config: Mapped[RuntimeConfig | None] = relationship()
    steps: Mapped[list["ProcessingStep"]] = relationship(back_populates="run")


class ProcessingStep(Base):
    __tablename__ = "processing_step"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    run_id: Mapped[str] = mapped_column(ForeignKey("processing_run.id"), nullable=False, index=True)
    step_name: Mapped[str] = mapped_column(String(200), nullable=False)
    step_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="queued", index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    runtime_config_id: Mapped[str | None] = mapped_column(ForeignKey("runtime_config.id"))
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    run: Mapped[ProcessingRun] = relationship(back_populates="steps")
    runtime_config: Mapped[RuntimeConfig | None] = relationship()


class Observation(CreatedAtMixin, Base):
    __tablename__ = "observation"
    __table_args__ = (
        Index("ix_observation_media_id", "media_id"),
        Index("ix_observation_run_id", "run_id"),
        Index("ix_observation_media_run", "media_id", "run_id"),
        Index("ix_observation_family", "observation_family"),
        Index("ix_observation_type", "observation_type"),
        Index("ix_observation_media_run_type", "media_id", "run_id", "observation_type"),
        Index("ix_observation_frame_range", "frame_start", "frame_end"),
        Index("ix_observation_timestamp_range", "timestamp_start_ms", "timestamp_end_ms"),
        Index("uq_observation_idempotency_key", "idempotency_key", unique=True),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    media_id: Mapped[str] = mapped_column(ForeignKey("media_asset.id"), nullable=False)
    run_id: Mapped[str] = mapped_column(ForeignKey("processing_run.id"), nullable=False)
    observation_family: Mapped[str] = mapped_column(String(100), nullable=False)
    observation_type: Mapped[str] = mapped_column(String(120), nullable=False)
    granularity: Mapped[str] = mapped_column(String(100), nullable=False)
    frame_start: Mapped[int | None] = mapped_column(Integer)
    frame_end: Mapped[int | None] = mapped_column(Integer)
    timestamp_start_ms: Mapped[int | None] = mapped_column(Integer)
    timestamp_end_ms: Mapped[int | None] = mapped_column(Integer)
    confidence: Mapped[float | None] = mapped_column(Float)
    model_id: Mapped[str | None] = mapped_column(ForeignKey("model_registry.id"))
    runtime_config_id: Mapped[str | None] = mapped_column(ForeignKey("runtime_config.id"))
    coordinate_space: Mapped[str | None] = mapped_column(String(100), default="none")
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(255))

    media: Mapped[MediaAsset] = relationship(back_populates="observations")
    run: Mapped[ProcessingRun] = relationship()
    model: Mapped[ModelRegistry | None] = relationship()
    runtime_config: Mapped[RuntimeConfig | None] = relationship()
    gameplay_detail: Mapped["GameplayObservation | None"] = relationship(
        back_populates="observation", uselist=False
    )
    atomic_detail: Mapped["AtomicObservation | None"] = relationship(
        back_populates="observation", uselist=False
    )
    derived_detail: Mapped["DerivedObservation | None"] = relationship(
        back_populates="observation", uselist=False
    )
    pose_detail: Mapped["PoseObservation | None"] = relationship(
        back_populates="observation",
        uselist=False,
        foreign_keys="PoseObservation.observation_id",
    )
    artifacts: Mapped[list["EvidenceArtifact"]] = relationship(back_populates="target_observation")
    annotations: Mapped[list["HumanAnnotation"]] = relationship(back_populates="observation")


class GameplayObservation(Base):
    __tablename__ = "gameplay_observation"

    observation_id: Mapped[str] = mapped_column(
        ForeignKey("observation.id"), primary_key=True, nullable=False
    )
    view_state: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    view_state_subtype: Mapped[str | None] = mapped_column(String(100))
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    observation: Mapped[Observation] = relationship(back_populates="gameplay_detail")


class AtomicObservation(Base):
    __tablename__ = "atomic_observation"

    observation_id: Mapped[str] = mapped_column(
        ForeignKey("observation.id"), primary_key=True, nullable=False
    )
    atomic_kind: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    observation: Mapped[Observation] = relationship(back_populates="atomic_detail")


class DerivedObservation(Base):
    __tablename__ = "derived_observation"

    observation_id: Mapped[str] = mapped_column(
        ForeignKey("observation.id"), primary_key=True, nullable=False
    )
    derived_kind: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    derivation_payload_jsonb: Mapped[dict[str, Any]] = mapped_column(
        JsonType, default=dict, nullable=False
    )

    observation: Mapped[Observation] = relationship(back_populates="derived_detail")


class PoseObservation(CreatedAtMixin, Base):
    __tablename__ = "pose_observation"
    __table_args__ = (
        Index("ix_pose_observation_media_run", "media_id", "run_id"),
        Index("ix_pose_observation_media_frame", "media_id", "frame_number"),
        Index("ix_pose_observation_run_confidence", "run_id", "pose_confidence"),
        Index("ix_pose_observation_subject_detection", "subject_detection_observation_id"),
        Index("ix_pose_observation_subject_tracklet", "subject_tracklet_id"),
        Index("ix_pose_observation_subject_track_point", "subject_track_point_id"),
        Index("ix_pose_observation_skeleton_format", "skeleton_format"),
        Index("ix_pose_observation_missing_count", "keypoints_missing_count"),
    )

    observation_id: Mapped[str] = mapped_column(
        ForeignKey("observation.id"), primary_key=True, nullable=False
    )
    media_id: Mapped[str] = mapped_column(ForeignKey("media_asset.id"), nullable=False)
    run_id: Mapped[str] = mapped_column(ForeignKey("processing_run.id"), nullable=False)
    frame_number: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    skeleton_format: Mapped[str] = mapped_column(String(100), nullable=False)
    skeleton_version: Mapped[str] = mapped_column(String(100), nullable=False)
    keypoint_schema_jsonb: Mapped[dict[str, Any]] = mapped_column(
        JsonType, default=dict, nullable=False
    )
    keypoints_jsonb: Mapped[list[dict[str, Any]]] = mapped_column(
        JsonType, default=list, nullable=False
    )
    keypoint_count: Mapped[int] = mapped_column(Integer, nullable=False)
    keypoints_present_count: Mapped[int] = mapped_column(Integer, nullable=False)
    keypoints_missing_count: Mapped[int] = mapped_column(Integer, nullable=False)
    mean_keypoint_confidence: Mapped[float | None] = mapped_column(Float)
    min_keypoint_confidence: Mapped[float | None] = mapped_column(Float)
    max_keypoint_confidence: Mapped[float | None] = mapped_column(Float)
    pose_confidence: Mapped[float | None] = mapped_column(Float)
    bbox_x: Mapped[float | None] = mapped_column(Float)
    bbox_y: Mapped[float | None] = mapped_column(Float)
    bbox_w: Mapped[float | None] = mapped_column(Float)
    bbox_h: Mapped[float | None] = mapped_column(Float)
    bbox_confidence: Mapped[float | None] = mapped_column(Float)
    crop_x: Mapped[float | None] = mapped_column(Float)
    crop_y: Mapped[float | None] = mapped_column(Float)
    crop_w: Mapped[float | None] = mapped_column(Float)
    crop_h: Mapped[float | None] = mapped_column(Float)
    crop_source: Mapped[str | None] = mapped_column(String(100))
    subject_ref_type: Mapped[str] = mapped_column(String(100), nullable=False, default="none")
    subject_detection_observation_id: Mapped[str | None] = mapped_column(
        ForeignKey("observation.id")
    )
    subject_tracklet_id: Mapped[str | None] = mapped_column(ForeignKey("tracklet.id"))
    subject_track_point_id: Mapped[str | None] = mapped_column(ForeignKey("track_point.id"))
    association_status: Mapped[str] = mapped_column(
        String(100), nullable=False, default="unassociated"
    )
    association_method: Mapped[str | None] = mapped_column(String(200))
    association_confidence: Mapped[float | None] = mapped_column(Float)
    frame_time_owner: Mapped[str] = mapped_column(
        String(100), nullable=False, default="media_indexing"
    )
    raw_model_payload_jsonb: Mapped[dict[str, Any]] = mapped_column(
        JsonType, default=dict, nullable=False
    )
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    observation: Mapped[Observation] = relationship(
        back_populates="pose_detail", foreign_keys=[observation_id]
    )
    media: Mapped[MediaAsset] = relationship()
    run: Mapped[ProcessingRun] = relationship()
    subject_detection_observation: Mapped[Observation | None] = relationship(
        foreign_keys=[subject_detection_observation_id]
    )
    subject_tracklet: Mapped["Tracklet | None"] = relationship()
    subject_track_point: Mapped["TrackPoint | None"] = relationship()


class Tracklet(Base):
    __tablename__ = "tracklet"
    __table_args__ = (
        Index("ix_tracklet_media_run", "media_id", "run_id"),
        Index("ix_tracklet_frame_range", "frame_start", "frame_end"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    media_id: Mapped[str] = mapped_column(ForeignKey("media_asset.id"), nullable=False)
    run_id: Mapped[str] = mapped_column(ForeignKey("processing_run.id"), nullable=False)
    track_family: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    subject_ref: Mapped[str | None] = mapped_column(String(200))
    frame_start: Mapped[int | None] = mapped_column(Integer)
    frame_end: Mapped[int | None] = mapped_column(Integer)
    confidence: Mapped[float | None] = mapped_column(Float)
    observation_id: Mapped[str | None] = mapped_column(ForeignKey("observation.id"))
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    observation: Mapped[Observation | None] = relationship()
    points: Mapped[list["TrackPoint"]] = relationship(back_populates="tracklet")


class TrackPoint(Base):
    __tablename__ = "track_point"
    __table_args__ = (
        Index("ix_track_point_tracklet_frame", "tracklet_id", "frame_number"),
        Index("ix_track_point_observation", "observation_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    tracklet_id: Mapped[str] = mapped_column(ForeignKey("tracklet.id"), nullable=False)
    observation_id: Mapped[str | None] = mapped_column(ForeignKey("observation.id"))
    frame_number: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_ms: Mapped[int | None] = mapped_column(Integer)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[float | None] = mapped_column(Float)
    height: Mapped[float | None] = mapped_column(Float)
    confidence: Mapped[float | None] = mapped_column(Float)
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    tracklet: Mapped[Tracklet] = relationship(back_populates="points")
    observation: Mapped[Observation | None] = relationship()


class ObservationLineage(CreatedAtMixin, Base):
    __tablename__ = "observation_lineage"
    __table_args__ = (
        Index("ix_lineage_child", "child_observation_id"),
        Index("ix_lineage_parent", "parent_observation_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    child_observation_id: Mapped[str] = mapped_column(ForeignKey("observation.id"), nullable=False)
    parent_observation_id: Mapped[str] = mapped_column(ForeignKey("observation.id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False)
    processing_step_id: Mapped[str | None] = mapped_column(ForeignKey("processing_step.id"))
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    child_observation: Mapped[Observation] = relationship(foreign_keys=[child_observation_id])
    parent_observation: Mapped[Observation] = relationship(foreign_keys=[parent_observation_id])
    processing_step: Mapped[ProcessingStep | None] = relationship()


class EvidenceArtifact(CreatedAtMixin, Base):
    __tablename__ = "evidence_artifact"
    __table_args__ = (
        Index("ix_artifact_media_run", "media_id", "run_id"),
        Index("ix_artifact_target_observation", "target_observation_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    media_id: Mapped[str] = mapped_column(ForeignKey("media_asset.id"), nullable=False)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("processing_run.id"))
    target_observation_id: Mapped[str | None] = mapped_column(ForeignKey("observation.id"))
    artifact_type: Mapped[str] = mapped_column(String(120), nullable=False)
    uri: Mapped[str] = mapped_column(Text, nullable=False)
    frame_start: Mapped[int | None] = mapped_column(Integer)
    frame_end: Mapped[int | None] = mapped_column(Integer)
    timestamp_start_ms: Mapped[int | None] = mapped_column(Integer)
    timestamp_end_ms: Mapped[int | None] = mapped_column(Integer)
    checksum: Mapped[str | None] = mapped_column(String(255))
    metadata_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)

    media: Mapped[MediaAsset] = relationship()
    run: Mapped[ProcessingRun | None] = relationship()
    target_observation: Mapped[Observation | None] = relationship(back_populates="artifacts")


class HumanAnnotation(CreatedAtMixin, Base):
    __tablename__ = "human_annotation"
    __table_args__ = (
        Index("ix_annotation_observation", "observation_id"),
        Index("ix_annotation_artifact", "evidence_artifact_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    media_id: Mapped[str] = mapped_column(ForeignKey("media_asset.id"), nullable=False)
    observation_id: Mapped[str | None] = mapped_column(ForeignKey("observation.id"))
    evidence_artifact_id: Mapped[str | None] = mapped_column(ForeignKey("evidence_artifact.id"))
    frame_start: Mapped[int | None] = mapped_column(Integer)
    frame_end: Mapped[int | None] = mapped_column(Integer)
    timestamp_start_ms: Mapped[int | None] = mapped_column(Integer)
    timestamp_end_ms: Mapped[int | None] = mapped_column(Integer)
    annotation_type: Mapped[str] = mapped_column(String(120), nullable=False)
    payload_jsonb: Mapped[dict[str, Any]] = mapped_column(JsonType, default=dict, nullable=False)
    created_by: Mapped[str | None] = mapped_column(String(200))

    media: Mapped[MediaAsset] = relationship()
    observation: Mapped[Observation | None] = relationship(back_populates="annotations")
    evidence_artifact: Mapped[EvidenceArtifact | None] = relationship()


class QueryResult(CreatedAtMixin, Base):
    __tablename__ = "query_result"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    query_name: Mapped[str | None] = mapped_column(String(200))
    query_payload_jsonb: Mapped[dict[str, Any]] = mapped_column(
        JsonType, default=dict, nullable=False
    )
    result_payload_jsonb: Mapped[dict[str, Any]] = mapped_column(
        JsonType, default=dict, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(String(200))
