"""add event candidate 3d diagnostics

Revision ID: 0007_event_candidate_3d_diagnostic
Revises: 0006_ball_trajectory_3d_candidate
Create Date: 2026-06-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0007_event_candidate_3d_diagnostic"
down_revision: str | None = "0006_ball_trajectory_3d_candidate"
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
        "event_candidate_3d_diagnostic",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("event_candidate_run_id", sa.String(length=36), nullable=False),
        sa.Column("event_observation_id", sa.String(length=36), nullable=False),
        sa.Column("candidate_type", sa.String(length=120), nullable=False),
        sa.Column("trajectory_3d_run_id", sa.String(length=36), nullable=True),
        sa.Column("camera_geometry_id", sa.String(length=36), nullable=True),
        sa.Column("frame", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("nearest_3d_candidate_id", sa.String(length=36), nullable=True),
        sa.Column("nearest_3d_frame", sa.Integer(), nullable=True),
        sa.Column("nearest_3d_timestamp_ms", sa.Integer(), nullable=True),
        sa.Column("nearest_time_delta_ms", sa.Integer(), nullable=True),
        sa.Column("nearest_court_x_m", sa.Float(), nullable=True),
        sa.Column("nearest_court_y_m", sa.Float(), nullable=True),
        sa.Column("nearest_court_z_m", sa.Float(), nullable=True),
        sa.Column("height_status", sa.String(length=80), nullable=False),
        sa.Column("diagnostic_status", sa.String(length=80), nullable=False),
        sa.Column("diagnostic_label", sa.String(length=120), nullable=False),
        sa.Column("diagnostic_confidence", sa.Float(), nullable=True),
        sa.Column("pre_window_sample_count", sa.Integer(), nullable=False),
        sa.Column("post_window_sample_count", sa.Integer(), nullable=False),
        sa.Column("local_window_sample_count", sa.Integer(), nullable=False),
        sa.Column("local_velocity_available", sa.Boolean(), nullable=False),
        sa.Column("local_speed_mps", sa.Float(), nullable=True),
        sa.Column("local_direction_delta_degrees", sa.Float(), nullable=True),
        sa.Column("diagnostics_jsonb", json_type, nullable=False),
        sa.Column("warnings_jsonb", json_type, nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        updated_at_column(),
        sa.ForeignKeyConstraint(["camera_geometry_id"], ["camera_geometry_evidence.id"]),
        sa.ForeignKeyConstraint(["event_candidate_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["event_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(
            ["nearest_3d_candidate_id"],
            ["ball_trajectory_3d_candidate.id"],
        ),
        sa.ForeignKeyConstraint(["trajectory_3d_run_id"], ["processing_run.id"]),
    )
    op.create_index(
        "ix_event_candidate_3d_diag_media_run",
        "event_candidate_3d_diagnostic",
        ["media_id", "event_candidate_run_id"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_event",
        "event_candidate_3d_diagnostic",
        ["event_observation_id"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_traj_run",
        "event_candidate_3d_diagnostic",
        ["trajectory_3d_run_id"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_nearest",
        "event_candidate_3d_diagnostic",
        ["nearest_3d_candidate_id"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_frame",
        "event_candidate_3d_diagnostic",
        ["media_id", "frame"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_timestamp",
        "event_candidate_3d_diagnostic",
        ["media_id", "timestamp_ms"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_label",
        "event_candidate_3d_diagnostic",
        ["diagnostic_label"],
    )
    op.create_index(
        "ix_event_candidate_3d_diag_status",
        "event_candidate_3d_diagnostic",
        ["diagnostic_status"],
    )


def downgrade() -> None:
    op.drop_index("ix_event_candidate_3d_diag_status", table_name="event_candidate_3d_diagnostic")
    op.drop_index("ix_event_candidate_3d_diag_label", table_name="event_candidate_3d_diagnostic")
    op.drop_index(
        "ix_event_candidate_3d_diag_timestamp",
        table_name="event_candidate_3d_diagnostic",
    )
    op.drop_index("ix_event_candidate_3d_diag_frame", table_name="event_candidate_3d_diagnostic")
    op.drop_index(
        "ix_event_candidate_3d_diag_nearest",
        table_name="event_candidate_3d_diagnostic",
    )
    op.drop_index(
        "ix_event_candidate_3d_diag_traj_run",
        table_name="event_candidate_3d_diagnostic",
    )
    op.drop_index("ix_event_candidate_3d_diag_event", table_name="event_candidate_3d_diagnostic")
    op.drop_index(
        "ix_event_candidate_3d_diag_media_run",
        table_name="event_candidate_3d_diagnostic",
    )
    op.drop_table("event_candidate_3d_diagnostic")
