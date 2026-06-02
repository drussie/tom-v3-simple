"""add trajectory 3d debug review annotations

Revision ID: 0008_trajectory_3d_debug_review_annotations
Revises: 0007_event_candidate_3d_diagnostic
Create Date: 2026-06-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0008_trajectory_3d_debug_review_annotations"
down_revision: str | None = "0007_event_candidate_3d_diagnostic"
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
        "trajectory_3d_debug_review_annotation",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("trajectory_3d_run_id", sa.String(length=36), nullable=True),
        sa.Column("camera_geometry_id", sa.String(length=36), nullable=True),
        sa.Column("event_candidate_run_id", sa.String(length=36), nullable=True),
        sa.Column("event_observation_id", sa.String(length=36), nullable=True),
        sa.Column("trajectory_3d_candidate_id", sa.String(length=36), nullable=True),
        sa.Column("event_candidate_3d_diagnostic_id", sa.String(length=36), nullable=True),
        sa.Column("annotation_kind", sa.String(length=80), nullable=False),
        sa.Column("review_label", sa.String(length=80), nullable=False),
        sa.Column("frame", sa.Integer(), nullable=True),
        sa.Column("timestamp_ms", sa.Integer(), nullable=True),
        sa.Column("image_x", sa.Float(), nullable=True),
        sa.Column("image_y", sa.Float(), nullable=True),
        sa.Column("court_x_m", sa.Float(), nullable=True),
        sa.Column("court_y_m", sa.Float(), nullable=True),
        sa.Column("court_z_m", sa.Float(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("reviewer", sa.String(length=200), nullable=True),
        created_at_column(),
        updated_at_column(),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["camera_geometry_id"], ["camera_geometry_evidence.id"]),
        sa.ForeignKeyConstraint(["event_candidate_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["event_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(
            ["event_candidate_3d_diagnostic_id"],
            ["event_candidate_3d_diagnostic.id"],
        ),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(
            ["trajectory_3d_candidate_id"],
            ["ball_trajectory_3d_candidate.id"],
        ),
        sa.ForeignKeyConstraint(["trajectory_3d_run_id"], ["processing_run.id"]),
    )
    op.create_index(
        "ix_trajectory_3d_debug_review_media_traj_run",
        "trajectory_3d_debug_review_annotation",
        ["media_id", "trajectory_3d_run_id"],
    )
    op.create_index(
        "ix_trajectory_3d_debug_review_media_event_run",
        "trajectory_3d_debug_review_annotation",
        ["media_id", "event_candidate_run_id"],
    )
    op.create_index(
        "ix_trajectory_3d_debug_review_sample",
        "trajectory_3d_debug_review_annotation",
        ["trajectory_3d_candidate_id"],
    )
    op.create_index(
        "ix_trajectory_3d_debug_review_diagnostic",
        "trajectory_3d_debug_review_annotation",
        ["event_candidate_3d_diagnostic_id"],
    )
    op.create_index(
        "ix_trajectory_3d_debug_review_kind_label",
        "trajectory_3d_debug_review_annotation",
        ["annotation_kind", "review_label"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_trajectory_3d_debug_review_kind_label",
        table_name="trajectory_3d_debug_review_annotation",
    )
    op.drop_index(
        "ix_trajectory_3d_debug_review_diagnostic",
        table_name="trajectory_3d_debug_review_annotation",
    )
    op.drop_index(
        "ix_trajectory_3d_debug_review_sample",
        table_name="trajectory_3d_debug_review_annotation",
    )
    op.drop_index(
        "ix_trajectory_3d_debug_review_media_event_run",
        table_name="trajectory_3d_debug_review_annotation",
    )
    op.drop_index(
        "ix_trajectory_3d_debug_review_media_traj_run",
        table_name="trajectory_3d_debug_review_annotation",
    )
    op.drop_table("trajectory_3d_debug_review_annotation")
