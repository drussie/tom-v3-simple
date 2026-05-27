"""add court evidence observation tables

Revision ID: 0003_court_evidence_observations
Revises: 0002_pose_observation
Create Date: 2026-05-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_court_evidence_observations"
down_revision: str | None = "0002_pose_observation"
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
        "court_keypoint_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("court_keypoint_schema", sa.String(length=120), nullable=False),
        sa.Column("schema_version", sa.String(length=100), nullable=False),
        sa.Column("keypoints_jsonb", json_type, nullable=False),
        sa.Column("keypoint_count", sa.Integer(), nullable=False),
        sa.Column("keypoints_present_count", sa.Integer(), nullable=False),
        sa.Column("keypoints_missing_count", sa.Integer(), nullable=False),
        sa.Column("mean_keypoint_confidence", sa.Float(), nullable=True),
        sa.Column("min_keypoint_confidence", sa.Float(), nullable=True),
        sa.Column("max_keypoint_confidence", sa.Float(), nullable=True),
        sa.Column("coordinate_space", sa.String(length=100), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("frame_time_owner", sa.String(length=100), nullable=False),
        sa.Column("raw_model_payload_jsonb", json_type, nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
    )
    op.create_index(
        "ix_court_keypoint_media_run", "court_keypoint_observation", ["media_id", "run_id"]
    )
    op.create_index(
        "ix_court_keypoint_media_frame",
        "court_keypoint_observation",
        ["media_id", "frame_number"],
    )
    op.create_index(
        "ix_court_keypoint_run_frame",
        "court_keypoint_observation",
        ["run_id", "frame_number"],
    )
    op.create_index(
        "ix_court_keypoint_schema",
        "court_keypoint_observation",
        ["court_keypoint_schema", "schema_version"],
    )

    op.create_table(
        "court_line_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("line_segments_jsonb", json_type, nullable=False),
        sa.Column("line_classes_jsonb", json_type, nullable=False),
        sa.Column("line_count", sa.Integer(), nullable=False),
        sa.Column("mean_line_confidence", sa.Float(), nullable=True),
        sa.Column("coordinate_space", sa.String(length=100), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("frame_time_owner", sa.String(length=100), nullable=False),
        sa.Column("raw_model_payload_jsonb", json_type, nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
    )
    op.create_index("ix_court_line_media_run", "court_line_observation", ["media_id", "run_id"])
    op.create_index(
        "ix_court_line_media_frame", "court_line_observation", ["media_id", "frame_number"]
    )
    op.create_index(
        "ix_court_line_run_frame", "court_line_observation", ["run_id", "frame_number"]
    )

    op.create_table(
        "camera_view_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("frame_start", sa.Integer(), nullable=True),
        sa.Column("frame_end", sa.Integer(), nullable=True),
        sa.Column("timestamp_start_ms", sa.Integer(), nullable=True),
        sa.Column("timestamp_end_ms", sa.Integer(), nullable=True),
        sa.Column("view_label", sa.String(length=100), nullable=False),
        sa.Column("view_confidence", sa.Float(), nullable=True),
        sa.Column("camera_motion_hint", sa.String(length=100), nullable=True),
        sa.Column("stability_score", sa.Float(), nullable=True),
        sa.Column("cut_likelihood", sa.Float(), nullable=True),
        sa.Column("model_id", sa.String(length=36), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("frame_time_owner", sa.String(length=100), nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
    )
    op.create_index("ix_camera_view_media_run", "camera_view_observation", ["media_id", "run_id"])
    op.create_index(
        "ix_camera_view_media_frame", "camera_view_observation", ["media_id", "frame_number"]
    )
    op.create_index(
        "ix_camera_view_run_frame", "camera_view_observation", ["run_id", "frame_number"]
    )
    op.create_index("ix_camera_view_label", "camera_view_observation", ["view_label"])

    op.create_table(
        "homography_candidate_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column("source_court_keypoint_observation_id", sa.String(length=36), nullable=True),
        sa.Column("source_court_line_observation_id", sa.String(length=36), nullable=True),
        sa.Column("source_camera_view_observation_id", sa.String(length=36), nullable=True),
        sa.Column("homography_matrix_jsonb", json_type, nullable=True),
        sa.Column("inverse_homography_matrix_jsonb", json_type, nullable=True),
        sa.Column("source_coordinate_space", sa.String(length=100), nullable=False),
        sa.Column("target_coordinate_space", sa.String(length=100), nullable=False),
        sa.Column("matrix_direction", sa.String(length=120), nullable=False),
        sa.Column("template_name", sa.String(length=200), nullable=False),
        sa.Column("template_version", sa.String(length=100), nullable=False),
        sa.Column("reprojection_error_mean", sa.Float(), nullable=True),
        sa.Column("reprojection_error_median", sa.Float(), nullable=True),
        sa.Column("reprojection_error_max", sa.Float(), nullable=True),
        sa.Column("inlier_count", sa.Integer(), nullable=True),
        sa.Column("outlier_count", sa.Integer(), nullable=True),
        sa.Column("source_point_count", sa.Integer(), nullable=True),
        sa.Column("source_line_count", sa.Integer(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("frame_time_owner", sa.String(length=100), nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
        sa.ForeignKeyConstraint(["source_camera_view_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["source_court_keypoint_observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["source_court_line_observation_id"], ["observation.id"]),
    )
    op.create_index(
        "ix_homography_candidate_media_run",
        "homography_candidate_observation",
        ["media_id", "run_id"],
    )
    op.create_index(
        "ix_homography_candidate_media_frame",
        "homography_candidate_observation",
        ["media_id", "frame_number"],
    )
    op.create_index(
        "ix_homography_candidate_run_frame",
        "homography_candidate_observation",
        ["run_id", "frame_number"],
    )
    op.create_index(
        "ix_homography_candidate_source_keypoint",
        "homography_candidate_observation",
        ["source_court_keypoint_observation_id"],
    )
    op.create_index(
        "ix_homography_candidate_source_line",
        "homography_candidate_observation",
        ["source_court_line_observation_id"],
    )
    op.create_index(
        "ix_homography_candidate_source_camera",
        "homography_candidate_observation",
        ["source_camera_view_observation_id"],
    )
    op.create_index(
        "ix_homography_candidate_status", "homography_candidate_observation", ["status"]
    )

    op.create_table(
        "projection_diagnostic_observation",
        sa.Column("observation_id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("timestamp_ms", sa.Integer(), nullable=False),
        sa.Column(
            "source_homography_candidate_observation_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column("projected_template_keypoints_jsonb", json_type, nullable=False),
        sa.Column("projected_template_lines_jsonb", json_type, nullable=False),
        sa.Column("diagnostic_metrics_jsonb", json_type, nullable=False),
        sa.Column("overlay_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=True),
        sa.Column("runtime_config_id", sa.String(length=36), nullable=True),
        sa.Column("frame_time_owner", sa.String(length=100), nullable=False),
        sa.Column("metadata_jsonb", json_type, nullable=False),
        created_at_column(),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
        sa.ForeignKeyConstraint(["overlay_artifact_id"], ["evidence_artifact.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["runtime_config_id"], ["runtime_config.id"]),
        sa.ForeignKeyConstraint(["source_homography_candidate_observation_id"], ["observation.id"]),
    )
    op.create_index(
        "ix_projection_diagnostic_media_run",
        "projection_diagnostic_observation",
        ["media_id", "run_id"],
    )
    op.create_index(
        "ix_projection_diagnostic_media_frame",
        "projection_diagnostic_observation",
        ["media_id", "frame_number"],
    )
    op.create_index(
        "ix_projection_diagnostic_run_frame",
        "projection_diagnostic_observation",
        ["run_id", "frame_number"],
    )
    op.create_index(
        "ix_projection_diagnostic_source_homography",
        "projection_diagnostic_observation",
        ["source_homography_candidate_observation_id"],
    )
    op.create_index(
        "ix_projection_diagnostic_status", "projection_diagnostic_observation", ["status"]
    )


def downgrade() -> None:
    op.drop_index("ix_projection_diagnostic_status", table_name="projection_diagnostic_observation")
    op.drop_index(
        "ix_projection_diagnostic_source_homography",
        table_name="projection_diagnostic_observation",
    )
    op.drop_index(
        "ix_projection_diagnostic_run_frame", table_name="projection_diagnostic_observation"
    )
    op.drop_index(
        "ix_projection_diagnostic_media_frame", table_name="projection_diagnostic_observation"
    )
    op.drop_index(
        "ix_projection_diagnostic_media_run", table_name="projection_diagnostic_observation"
    )
    op.drop_table("projection_diagnostic_observation")

    op.drop_index("ix_homography_candidate_status", table_name="homography_candidate_observation")
    op.drop_index(
        "ix_homography_candidate_source_camera", table_name="homography_candidate_observation"
    )
    op.drop_index(
        "ix_homography_candidate_source_line", table_name="homography_candidate_observation"
    )
    op.drop_index(
        "ix_homography_candidate_source_keypoint", table_name="homography_candidate_observation"
    )
    op.drop_index(
        "ix_homography_candidate_run_frame", table_name="homography_candidate_observation"
    )
    op.drop_index(
        "ix_homography_candidate_media_frame", table_name="homography_candidate_observation"
    )
    op.drop_index(
        "ix_homography_candidate_media_run", table_name="homography_candidate_observation"
    )
    op.drop_table("homography_candidate_observation")

    op.drop_index("ix_camera_view_label", table_name="camera_view_observation")
    op.drop_index("ix_camera_view_run_frame", table_name="camera_view_observation")
    op.drop_index("ix_camera_view_media_frame", table_name="camera_view_observation")
    op.drop_index("ix_camera_view_media_run", table_name="camera_view_observation")
    op.drop_table("camera_view_observation")

    op.drop_index("ix_court_line_run_frame", table_name="court_line_observation")
    op.drop_index("ix_court_line_media_frame", table_name="court_line_observation")
    op.drop_index("ix_court_line_media_run", table_name="court_line_observation")
    op.drop_table("court_line_observation")

    op.drop_index("ix_court_keypoint_schema", table_name="court_keypoint_observation")
    op.drop_index("ix_court_keypoint_run_frame", table_name="court_keypoint_observation")
    op.drop_index("ix_court_keypoint_media_frame", table_name="court_keypoint_observation")
    op.drop_index("ix_court_keypoint_media_run", table_name="court_keypoint_observation")
    op.drop_table("court_keypoint_observation")
