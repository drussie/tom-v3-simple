"""create observation store tables

Revision ID: 0001_observation_store
Revises:
Create Date: 2026-05-25
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_observation_store"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

json_type = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def id_column() -> sa.Column:
    return sa.Column("id", sa.String(length=36), primary_key=True, nullable=False)


def created_at_column() -> sa.Column:
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "media_asset",
        id_column(),
        sa.Column("source_uri", sa.Text(), nullable=False),
        sa.Column("media_type", sa.String(length=50), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("frame_count", sa.Integer(), nullable=True),
        sa.Column("fps", sa.Float(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("checksum", sa.String(length=255), nullable=True),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
    )
    op.create_table(
        "model_registry",
        id_column(),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("version", sa.String(length=100), nullable=False),
        sa.Column("model_family", sa.String(length=100), nullable=False),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
    )
    op.create_index("ix_model_registry_model_family", "model_registry", ["model_family"])
    op.create_table(
        "runtime_config",
        id_column(),
        sa.Column("config_name", sa.String(length=200), nullable=False),
        sa.Column("config_version", sa.String(length=100), nullable=False),
        sa.Column("payload_jsonb", json_type, nullable=False),
        created_at_column(),
    )
    op.create_table(
        "processing_run",
        id_column(),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_name", sa.String(length=200), nullable=False),
        sa.Column("run_status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
    )
    op.create_index("ix_processing_run_media_id", "processing_run", ["media_id"])
    op.create_index("ix_processing_run_run_status", "processing_run", ["run_status"])
    op.create_table(
        "processing_step",
        id_column(),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("step_name", sa.String(length=200), nullable=False),
        sa.Column("step_status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
    )
    op.create_index("ix_processing_step_run_id", "processing_step", ["run_id"])
    op.create_index("ix_processing_step_step_status", "processing_step", ["step_status"])
    op.create_table(
        "observation",
        id_column(),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("observation_family", sa.String(length=100), nullable=False),
        sa.Column("observation_type", sa.String(length=120), nullable=False),
        sa.Column("granularity", sa.String(length=100), nullable=False),
        sa.Column("frame_start", sa.Integer(), nullable=True),
        sa.Column("frame_end", sa.Integer(), nullable=True),
        sa.Column("timestamp_start_ms", sa.Integer(), nullable=True),
        sa.Column("timestamp_end_ms", sa.Integer(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("model_id", sa.String(length=36), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("coordinate_space", sa.String(length=100), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
    )
    op.create_index("ix_observation_media_id", "observation", ["media_id"])
    op.create_index("ix_observation_run_id", "observation", ["run_id"])
    op.create_index("ix_observation_media_run", "observation", ["media_id", "run_id"])
    op.create_index("ix_observation_family", "observation", ["observation_family"])
    op.create_index("ix_observation_type", "observation", ["observation_type"])
    op.create_index(
        "ix_observation_media_run_type",
        "observation",
        ["media_id", "run_id", "observation_type"],
    )
    op.create_index("ix_observation_frame_range", "observation", ["frame_start", "frame_end"])
    op.create_index(
        "ix_observation_timestamp_range",
        "observation",
        ["timestamp_start_ms", "timestamp_end_ms"],
    )
    op.create_index(
        "uq_observation_idempotency_key",
        "observation",
        ["idempotency_key"],
        unique=True,
    )
    op.create_table(
        "gameplay_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("view_state", sa.String(length=50), nullable=False),
        sa.Column("view_state_subtype", sa.String(length=100), nullable=True),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
    )
    op.create_index("ix_gameplay_observation_view_state", "gameplay_observation", ["view_state"])
    op.create_table(
        "atomic_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("atomic_kind", sa.String(length=120), nullable=False),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
    )
    op.create_index("ix_atomic_observation_atomic_kind", "atomic_observation", ["atomic_kind"])
    op.create_table(
        "derived_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("derived_kind", sa.String(length=120), nullable=False),
        sa.Column("derivation_payload_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
    )
    op.create_index("ix_derived_observation_derived_kind", "derived_observation", ["derived_kind"])
    op.create_table(
        "tracklet",
        id_column(),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("track_family", sa.String(length=100), nullable=False),
        sa.Column("subject_ref", sa.String(length=200), nullable=True),
        sa.Column("frame_start", sa.Integer(), nullable=True),
        sa.Column("frame_end", sa.Integer(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("observation_id", sa.String(length=36), nullable=True),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
    )
    op.create_index("ix_tracklet_track_family", "tracklet", ["track_family"])
    op.create_index("ix_tracklet_media_run", "tracklet", ["media_id", "run_id"])
    op.create_index("ix_tracklet_frame_range", "tracklet", ["frame_start", "frame_end"])
    op.create_table(
        "track_point",
        id_column(),
        sa.Column("tracklet_id", sa.String(length=36), nullable=False),
        sa.Column("observation_id", sa.String(length=36), nullable=True),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=True),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("width", sa.Float(), nullable=True),
        sa.Column("height", sa.Float(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["tracklet_id"], ["tracklet.id"]),
    )
    op.create_index("ix_track_point_tracklet_frame", "track_point", ["tracklet_id", "frame_number"])
    op.create_index("ix_track_point_observation", "track_point", ["observation_id"])
    op.create_table(
        "observation_lineage",
        id_column(),
        sa.Column("child_observation_id", sa.String(length=36), nullable=False),
        sa.Column("parent_observation_id", sa.String(length=36), nullable=False),
        sa.Column("relationship_type", sa.String(length=100), nullable=False),
        sa.Column("processing_step_id", sa.String(length=36), nullable=True),
        sa.Column("payload_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["child_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["parent_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["processing_step_id"], ["processing_step.id"]),
    )
    op.create_index("ix_lineage_child", "observation_lineage", ["child_observation_id"])
    op.create_index("ix_lineage_parent", "observation_lineage", ["parent_observation_id"])
    op.create_table(
        "evidence_artifact",
        id_column(),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=True),
        sa.Column("target_observation_id", sa.String(length=36), nullable=True),
        sa.Column("artifact_type", sa.String(length=120), nullable=False),
        sa.Column("uri", sa.Text(), nullable=False),
        sa.Column("frame_start", sa.Integer(), nullable=True),
        sa.Column("frame_end", sa.Integer(), nullable=True),
        sa.Column("timestamp_start_ms", sa.Integer(), nullable=True),
        sa.Column("timestamp_end_ms", sa.Integer(), nullable=True),
        sa.Column("checksum", sa.String(length=255), nullable=True),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["target_observation_id"], ["observation.id"]),
    )
    op.create_index("ix_artifact_media_run", "evidence_artifact", ["media_id", "run_id"])
    op.create_index(
        "ix_artifact_target_observation",
        "evidence_artifact",
        ["target_observation_id"],
    )
    op.create_table(
        "human_annotation",
        id_column(),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("observation_id", sa.String(length=36), nullable=True),
        sa.Column("evidence_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("frame_start", sa.Integer(), nullable=True),
        sa.Column("frame_end", sa.Integer(), nullable=True),
        sa.Column("timestamp_start_ms", sa.Integer(), nullable=True),
        sa.Column("timestamp_end_ms", sa.Integer(), nullable=True),
        sa.Column("annotation_type", sa.String(length=120), nullable=False),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.Column("created_by", sa.String(length=200), nullable=True),
        created_at_column(),
        sa.ForeignKeyConstraint(["evidence_artifact_id"], ["evidence_artifact.id"]),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
    )
    op.create_index("ix_annotation_observation", "human_annotation", ["observation_id"])
    op.create_index("ix_annotation_artifact", "human_annotation", ["evidence_artifact_id"])
    op.create_table(
        "query_result",
        id_column(),
        sa.Column("query_name", sa.String(length=200), nullable=True),
        sa.Column("query_payload_jsonb", json_type, nullable=False),
        sa.Column("result_payload_jsonb", json_type, nullable=False),
        sa.Column("created_by", sa.String(length=200), nullable=True),
        created_at_column(),
    )


def downgrade() -> None:
    op.drop_table("query_result")
    op.drop_index("ix_annotation_artifact", table_name="human_annotation")
    op.drop_index("ix_annotation_observation", table_name="human_annotation")
    op.drop_table("human_annotation")
    op.drop_index("ix_artifact_target_observation", table_name="evidence_artifact")
    op.drop_index("ix_artifact_media_run", table_name="evidence_artifact")
    op.drop_table("evidence_artifact")
    op.drop_index("ix_lineage_parent", table_name="observation_lineage")
    op.drop_index("ix_lineage_child", table_name="observation_lineage")
    op.drop_table("observation_lineage")
    op.drop_index("ix_track_point_observation", table_name="track_point")
    op.drop_index("ix_track_point_tracklet_frame", table_name="track_point")
    op.drop_table("track_point")
    op.drop_index("ix_tracklet_frame_range", table_name="tracklet")
    op.drop_index("ix_tracklet_media_run", table_name="tracklet")
    op.drop_index("ix_tracklet_track_family", table_name="tracklet")
    op.drop_table("tracklet")
    op.drop_index("ix_derived_observation_derived_kind", table_name="derived_observation")
    op.drop_table("derived_observation")
    op.drop_index("ix_atomic_observation_atomic_kind", table_name="atomic_observation")
    op.drop_table("atomic_observation")
    op.drop_index("ix_gameplay_observation_view_state", table_name="gameplay_observation")
    op.drop_table("gameplay_observation")
    op.drop_index("uq_observation_idempotency_key", table_name="observation")
    op.drop_index("ix_observation_timestamp_range", table_name="observation")
    op.drop_index("ix_observation_frame_range", table_name="observation")
    op.drop_index("ix_observation_media_run_type", table_name="observation")
    op.drop_index("ix_observation_type", table_name="observation")
    op.drop_index("ix_observation_family", table_name="observation")
    op.drop_index("ix_observation_media_run", table_name="observation")
    op.drop_index("ix_observation_run_id", table_name="observation")
    op.drop_index("ix_observation_media_id", table_name="observation")
    op.drop_table("observation")
    op.drop_index("ix_processing_step_step_status", table_name="processing_step")
    op.drop_index("ix_processing_step_run_id", table_name="processing_step")
    op.drop_table("processing_step")
    op.drop_index("ix_processing_run_run_status", table_name="processing_run")
    op.drop_index("ix_processing_run_media_id", table_name="processing_run")
    op.drop_table("processing_run")
    op.drop_table("runtime_config")
    op.drop_index("ix_model_registry_model_family", table_name="model_registry")
    op.drop_table("model_registry")
    op.drop_table("media_asset")
