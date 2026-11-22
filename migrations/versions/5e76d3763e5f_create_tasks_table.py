
"""create tasks table

Revision ID: 5e76d3763e5f
"""

from alembic import op
import sqlalchemy as sa


revision = "5e76d3763e5f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("0")
        ),
    )


def downgrade() -> None:
    op.drop_table("tasks")
