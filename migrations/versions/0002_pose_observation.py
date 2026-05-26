"""add pose observation table

Revision ID: 0002_pose_observation
Revises: 0001_observation_store
Create Date: 2026-05-26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_pose_observation"
down_revision: str | None = "0001_observation_store"
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


def upgrade() -> None:
    op.create_table(
        "pose_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("skeleton_format", sa.String(length=100), nullable=False),
        sa.Column("skeleton_version", sa.String(length=100), nullable=False),
        sa.Column("keypoint_schema_jsonb", json_type, nullable=False),
        sa.Column("keypoints_jsonb", json_type, nullable=False),
        sa.Column("keypoint_count", sa.Integer(), nullable=False),
        sa.Column("keypoints_present_count", sa.Integer(), nullable=False),
        sa.Column("keypoints_missing_count", sa.Integer(), nullable=False),
        sa.Column("mean_keypoint_confidence", sa.Float(), nullable=True),
        sa.Column("min_keypoint_confidence", sa.Float(), nullable=True),
        sa.Column("max_keypoint_confidence", sa.Float(), nullable=True),
        sa.Column("pose_confidence", sa.Float(), nullable=True),
        sa.Column("bbox_x", sa.Float(), nullable=True),
        sa.Column("bbox_y", sa.Float(), nullable=True),
        sa.Column("bbox_w", sa.Float(), nullable=True),
        sa.Column("bbox_h", sa.Float(), nullable=True),
        sa.Column("bbox_confidence", sa.Float(), nullable=True),
        sa.Column("crop_x", sa.Float(), nullable=True),
        sa.Column("crop_y", sa.Float(), nullable=True),
        sa.Column("crop_w", sa.Float(), nullable=True),
        sa.Column("crop_h", sa.Float(), nullable=True),
        sa.Column("crop_source", sa.String(length=100), nullable=True),
        sa.Column("subject_ref_type", sa.String(length=100), nullable=False),
        sa.Column("subject_detection_observation_id", sa.String(length=36), nullable=True),
        sa.Column("subject_tracklet_id", sa.String(length=36), nullable=True),
        sa.Column("subject_track_point_id", sa.String(length=36), nullable=True),
        sa.Column("association_status", sa.String(length=100), nullable=False),
        sa.Column("association_method", sa.String(length=200), nullable=True),
        sa.Column("association_confidence", sa.Float(), nullable=True),
        sa.Column("frame_time_owner", sa.String(length=100), nullable=False),
        sa.Column("raw_model_payload_jsonb", json_type, nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["subject_detection_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["subject_tracklet_id"], ["tracklet.id"]),
        sa.ForeignKeyConstraint(["subject_track_point_id"], ["track_point.id"]),
    )
    op.create_index("ix_pose_observation_media_run", "pose_observation", ["media_id", "run_id"])
    op.create_index(
        "ix_pose_observation_media_frame", "pose_observation", ["media_id", "frame_number"]
    )
    op.create_index(
        "ix_pose_observation_run_confidence",
        "pose_observation",
        ["run_id", "pose_confidence"],
    )
    op.create_index(
        "ix_pose_observation_subject_detection",
        "pose_observation",
        ["subject_detection_observation_id"],
    )
    op.create_index(
        "ix_pose_observation_subject_tracklet",
        "pose_observation",
        ["subject_tracklet_id"],
    )
    op.create_index(
        "ix_pose_observation_subject_track_point",
        "pose_observation",
        ["subject_track_point_id"],
    )
    op.create_index(
        "ix_pose_observation_skeleton_format",
        "pose_observation",
        ["skeleton_format"],
    )
    op.create_index(
        "ix_pose_observation_missing_count",
        "pose_observation",
        ["keypoints_missing_count"],
    )


def downgrade() -> None:
    op.drop_index("ix_pose_observation_missing_count", table_name="pose_observation")
    op.drop_index("ix_pose_observation_skeleton_format", table_name="pose_observation")
    op.drop_index("ix_pose_observation_subject_track_point", table_name="pose_observation")
    op.drop_index("ix_pose_observation_subject_tracklet", table_name="pose_observation")
    op.drop_index("ix_pose_observation_subject_detection", table_name="pose_observation")
    op.drop_index("ix_pose_observation_run_confidence", table_name="pose_observation")
    op.drop_index("ix_pose_observation_media_frame", table_name="pose_observation")
    op.drop_index("ix_pose_observation_media_run", table_name="pose_observation")
    op.drop_table("pose_observation")
