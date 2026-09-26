"""add RAG documents and vectors

Revision ID: a6d075875681
Revises: 4d76b3cd4417
Create Date: 2026-09-26

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "a6d075875681"
down_revision: str | None = "4d76b3cd4417"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Required before creating vector columns.
    op.execute(
        "CREATE EXTENSION IF NOT EXISTS vector"
    )

    op.create_table(
        "documents",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "filename",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "content_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "chunk_count",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "document_chunks",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "document_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "embedding",
            Vector(768),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f(
            "ix_document_chunks_document_id"
        ),
        "document_chunks",
        ["document_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f(
            "ix_document_chunks_document_id"
        ),
        table_name="document_chunks",
    )

    op.drop_table(
        "document_chunks"
    )

    op.drop_table(
        "documents"
    )