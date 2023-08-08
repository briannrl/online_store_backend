"""create products table

Revision ID: cee03c42ebd6
Revises: 
Create Date: 2023-08-08 15:52:33.374716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = 'cee03c42ebd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    (op.create_table("products",
                     sa.Column("id", sa.String, nullable=False, primary_key=True, server_default=text("gen_random_uuid()")),
                     sa.Column("name", sa.String, nullable=False),
                     sa.Column("price", sa.Integer, nullable=False)
                    )
    )

def downgrade() -> None:
    op.drop_table("products")
