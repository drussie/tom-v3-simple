"""add event candidate review annotations

Revision ID: 0004_event_candidate_review_annotations
Revises: 0003_court_evidence_observations
Create Date: 2026-06-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0004_event_candidate_review_annotations"
down_revision: str | None = "0003_court_evidence_observations"
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
        "event_candidate_review_annotation",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("media_id", sa.String(length=36), nullable=False),
        sa.Column("event_candidate_run_id", sa.String(length=36), nullable=False),
        sa.Column("observation_id", sa.String(length=36), nullable=True),
        sa.Column("annotation_kind", sa.String(length=80), nullable=False),
        sa.Column("review_label", sa.String(length=80), nullable=False),
        sa.Column("candidate_type", sa.String(length=120), nullable=True),
        sa.Column("frame", sa.Integer(), nullable=True),
        sa.Column("timestamp_ms", sa.Integer(), nullable=True),
        sa.Column("image_x", sa.Float(), nullable=True),
        sa.Column("image_y", sa.Float(), nullable=True),
        sa.Column("court_x", sa.Float(), nullable=True),
        sa.Column("court_y", sa.Float(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("reviewer", sa.String(length=200), nullable=True),
        created_at_column(),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("payload_jsonb", json_type, nullable=False),
        sa.ForeignKeyConstraint(["event_candidate_run_id"], ["processing_run.id"]),
        sa.ForeignKeyConstraint(["media_id"], ["media_asset.id"]),
        sa.ForeignKeyConstraint(["observation_id"], ["observation.id"]),
    )
    op.create_index(
        "ix_event_candidate_review_media_run",
        "event_candidate_review_annotation",
        ["media_id", "event_candidate_run_id"],
    )
    op.create_index(
        "ix_event_candidate_review_observation",
        "event_candidate_review_annotation",
        ["observation_id"],
    )
    op.create_index(
        "ix_event_candidate_review_kind_label",
        "event_candidate_review_annotation",
        ["annotation_kind", "review_label"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_event_candidate_review_kind_label",
        table_name="event_candidate_review_annotation",
    )
    op.drop_index(
        "ix_event_candidate_review_observation",
        table_name="event_candidate_review_annotation",
    )
    op.drop_index(
        "ix_event_candidate_review_media_run",
        table_name="event_candidate_review_annotation",
    )
    op.drop_table("event_candidate_review_annotation")
