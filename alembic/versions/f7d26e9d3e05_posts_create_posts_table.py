"""posts - create posts table

Revision ID: f7d26e9d3e05
Revises: 
Create Date: 2022-06-06 07:44:51.407509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7d26e9d3e05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("posts")
