"""add total_stock, added_time, modified_time columns to products table

Revision ID: 778acc3b6098
Revises: cee03c42ebd6
Create Date: 2023-08-08 16:55:17.090164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = '778acc3b6098'
down_revision: Union[str, None] = 'cee03c42ebd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("total_stock", sa.Integer, nullable=False))
    op.add_column("products", sa.Column("added_time", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    op.add_column("products", sa.Column("modified_time", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()")))
    


def downgrade() -> None:
    for elm in ["total_stock", "added_time", "modified_time"]:
        op.drop_column("products", elm)