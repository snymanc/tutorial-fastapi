"""posts - add columns published and created_at

Revision ID: 420ab2dd231c
Revises: 3e61b838d6a0
Create Date: 2022-06-07 07:29:01.338596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '420ab2dd231c'
down_revision = '3e61b838d6a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column(
                      "published",
                      sa.Boolean(),
                      nullable=False, server_default="TRUE"
                  ))
    op.add_column("posts",
                  sa.Column(
                      "created_at",
                      sa.TIMESTAMP(timezone=True),
                      nullable=False,
                      server_default=sa.text('now()')
                  ))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
