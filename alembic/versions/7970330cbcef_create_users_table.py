"""create users table

Revision ID: 7970330cbcef
Revises: 778acc3b6098
Create Date: 2023-08-08 17:49:47.652291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '7970330cbcef'
down_revision: Union[str, None] = '778acc3b6098'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.String, nullable=False, primary_key=True, server_default=text("gen_random_uuid()")),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("position", sa.String, nullable=False),
                    sa.Column("regis_time", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
                    sa.Column("modified_time", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))
                    )


def downgrade() -> None:
    op.drop_table("users")
