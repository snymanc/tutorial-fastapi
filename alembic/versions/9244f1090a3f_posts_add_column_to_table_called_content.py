"""posts - add column to table called content

Revision ID: 9244f1090a3f
Revises: f7d26e9d3e05
Create Date: 2022-06-06 08:19:05.594748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9244f1090a3f'
down_revision = 'f7d26e9d3e05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
