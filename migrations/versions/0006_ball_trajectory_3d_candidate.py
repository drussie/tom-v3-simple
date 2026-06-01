"""add 3d ball trajectory candidate evidence

Revision ID: 0006_ball_trajectory_3d_candidate
Revises: 0005_camera_geometry_evidence
Create Date: 2026-06-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_ball_trajectory_3d_candidate"
down_revision: str | None = "0005_camera_geometry_evidence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

json_type = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def created_at_column() -> sa.Column:
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def updated_at_column() -> sa.Column:
    return sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "ball_trajectory_3d_candidate",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("ball_trajectory_run_id", sa.String(length=36), nullable=False),
        sa.Column("court_projection_run_id", sa.String(length=36), nullable=True),
        sa.Column("camera_geometry_id", sa.String(length=36), nullable=True),
        sa.Column("geometry_run_id", sa.String(length=36), nullable=True),
        sa.Column("trajectory_3d_run_id", sa.String(length=36), nullable=True),
        sa.Column("source_observation_id", sa.String(length=36), nullable=True),
        sa.Column("frame", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("image_x", sa.Float(), nullable=True),
        sa.Column("image_y", sa.Float(), nullable=True),
        sa.Column("court_x", sa.Float(), nullable=True),
        sa.Column("court_y", sa.Float(), nullable=True),
        sa.Column("court_x_m", sa.Float(), nullable=True),
        sa.Column("court_y_m", sa.Float(), nullable=True),
        sa.Column("court_z_m", sa.Float(), nullable=True),
        sa.Column("court_z_status", sa.String(length=80), nullable=False),
        sa.Column("height_model", sa.String(length=120), nullable=False),
        sa.Column("projection_method", sa.String(length=200), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("velocity_x_mps", sa.Float(), nullable=True),
        sa.Column("velocity_y_mps", sa.Float(), nullable=True),
        sa.Column("velocity_z_mps", sa.Float(), nullable=True),
        sa.Column("speed_mps", sa.Float(), nullable=True),
        sa.Column("diagnostics_jsonb", json_type, nullable=False),
        sa.Column("warnings_jsonb", json_type, nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        updated_at_column(),
        sa.ForeignKeyConstraint(["ball_trajectory_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["camera_geometry_id"], ["camera_geometry_evidence.id"]),
        sa.ForeignKeyConstraint(["court_projection_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["geometry_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["source_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["trajectory_3d_run_id"], ["processing_run.id"]),
    )
    op.create_index("ix_ball_trajectory_3d_media", "ball_trajectory_3d_candidate", ["media_id"])
    op.create_index(
        "ix_ball_trajectory_3d_source_run",
        "ball_trajectory_3d_candidate",
        ["ball_trajectory_run_id"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_projection_run",
        "ball_trajectory_3d_candidate",
        ["court_projection_run_id"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_camera_geometry",
        "ball_trajectory_3d_candidate",
        ["camera_geometry_id"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_run",
        "ball_trajectory_3d_candidate",
        ["trajectory_3d_run_id"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_source_observation",
        "ball_trajectory_3d_candidate",
        ["source_observation_id"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_frame",
        "ball_trajectory_3d_candidate",
        ["media_id", "frame"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_timestamp",
        "ball_trajectory_3d_candidate",
        ["media_id", "timestamp_ms"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_z_status",
        "ball_trajectory_3d_candidate",
        ["court_z_status"],
    )
    op.create_index(
        "ix_ball_trajectory_3d_height_model",
        "ball_trajectory_3d_candidate",
        ["height_model"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ball_trajectory_3d_height_model",
        table_name="ball_trajectory_3d_candidate",
    )
    op.drop_index("ix_ball_trajectory_3d_z_status", table_name="ball_trajectory_3d_candidate")
    op.drop_index("ix_ball_trajectory_3d_timestamp", table_name="ball_trajectory_3d_candidate")
    op.drop_index("ix_ball_trajectory_3d_frame", table_name="ball_trajectory_3d_candidate")
    op.drop_index(
        "ix_ball_trajectory_3d_source_observation",
        table_name="ball_trajectory_3d_candidate",
    )
    op.drop_index("ix_ball_trajectory_3d_run", table_name="ball_trajectory_3d_candidate")
    op.drop_index(
        "ix_ball_trajectory_3d_camera_geometry",
        table_name="ball_trajectory_3d_candidate",
    )
    op.drop_index(
        "ix_ball_trajectory_3d_projection_run",
        table_name="ball_trajectory_3d_candidate",
    )
    op.drop_index(
        "ix_ball_trajectory_3d_source_run",
        table_name="ball_trajectory_3d_candidate",
    )
    op.drop_index("ix_ball_trajectory_3d_media", table_name="ball_trajectory_3d_candidate")
    op.drop_table("ball_trajectory_3d_candidate")
