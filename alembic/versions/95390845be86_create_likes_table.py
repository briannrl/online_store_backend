"""create likes table

Revision ID: 95390845be86
Revises: 7970330cbcef
Create Date: 2023-08-08 18:10:58.990614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95390845be86'
down_revision: Union[str, None] = '7970330cbcef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("likes",
                    sa.Column("product_id", sa.String, sa.ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, primary_key=True),
                    sa.Column("user_id", sa.String, sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, primary_key=True)
                    )


def downgrade() -> None:
    op.drop_table("likes")
