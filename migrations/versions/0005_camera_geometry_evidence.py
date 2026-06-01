"""add camera geometry evidence

Revision ID: 0005_camera_geometry_evidence
Revises: 0004_event_candidate_review_annotations
Create Date: 2026-06-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005_camera_geometry_evidence"
down_revision: str | None = "0004_event_candidate_review_annotations"
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
        "camera_geometry_evidence",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("court_run_id", sa.String(length=36), nullable=True),
        sa.Column("court_projection_run_id", sa.String(length=36), nullable=True),
        sa.Column("homography_run_id", sa.String(length=36), nullable=True),
        sa.Column("geometry_run_id", sa.String(length=36), nullable=True),
        sa.Column("camera_model", sa.String(length=120), nullable=False),
        sa.Column("geometry_status", sa.String(length=80), nullable=False),
        sa.Column("court_model", sa.String(length=120), nullable=False),
        sa.Column("court_units", sa.String(length=40), nullable=False),
        sa.Column("court_length", sa.Float(), nullable=True),
        sa.Column("court_width", sa.Float(), nullable=True),
        sa.Column("net_height_center", sa.Float(), nullable=True),
        sa.Column("net_height_posts", sa.Float(), nullable=True),
        sa.Column("singles_sideline_width", sa.Float(), nullable=True),
        sa.Column("doubles_sideline_width", sa.Float(), nullable=True),
        sa.Column("near_baseline_y", sa.Float(), nullable=True),
        sa.Column("far_baseline_y", sa.Float(), nullable=True),
        sa.Column("camera_intrinsics_jsonb", json_type, nullable=False),
        sa.Column("camera_extrinsics_jsonb", json_type, nullable=False),
        sa.Column("distortion_jsonb", json_type, nullable=False),
        sa.Column("image_size_jsonb", json_type, nullable=False),
        sa.Column("homography_matrix_jsonb", json_type, nullable=True),
        sa.Column("world_coordinate_system_jsonb", json_type, nullable=False),
        sa.Column("assumptions_jsonb", json_type, nullable=False),
        sa.Column("warnings_jsonb", json_type, nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        updated_at_column(),
        sa.ForeignKeyConstraint(["court_projection_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["court_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["geometry_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["homography_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
    )
    op.create_index("ix_camera_geometry_media", "camera_geometry_evidence", ["media_id"])
    op.create_index(
        "ix_camera_geometry_court_run",
        "camera_geometry_evidence",
        ["court_run_id"],
    )
    op.create_index(
        "ix_camera_geometry_court_projection_run",
        "camera_geometry_evidence",
        ["court_projection_run_id"],
    )
    op.create_index(
        "ix_camera_geometry_homography_run",
        "camera_geometry_evidence",
        ["homography_run_id"],
    )
    op.create_index(
        "ix_camera_geometry_geometry_run",
        "camera_geometry_evidence",
        ["geometry_run_id"],
    )
    op.create_index(
        "ix_camera_geometry_status",
        "camera_geometry_evidence",
        ["geometry_status"],
    )


def downgrade() -> None:
    op.drop_index("ix_camera_geometry_status", table_name="camera_geometry_evidence")
    op.drop_index("ix_camera_geometry_geometry_run", table_name="camera_geometry_evidence")
    op.drop_index("ix_camera_geometry_homography_run", table_name="camera_geometry_evidence")
    op.drop_index(
        "ix_camera_geometry_court_projection_run",
        table_name="camera_geometry_evidence",
    )
    op.drop_index("ix_camera_geometry_court_run", table_name="camera_geometry_evidence")
    op.drop_index("ix_camera_geometry_media", table_name="camera_geometry_evidence")
    op.drop_table("camera_geometry_evidence")
