"""posts - add column 'owner_id' and foreign key 'users.id'

Revision ID: 3e61b838d6a0
Revises: d8fbae0675bd
Create Date: 2022-06-07 07:14:56.772385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e61b838d6a0'
down_revision = 'd8fbae0675bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
