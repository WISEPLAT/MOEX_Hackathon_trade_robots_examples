"""Backtesting

Revision ID: 006
Revises: 005
Create Date: 2023-12-10 01:59:27.220531

"""
from typing import Optional, Sequence

import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "006"
down_revision: Optional[str] = "005"
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "algorithm_backtests",
        sa.Column("data", postgresql.JSON(astext_type=sa.Text()), nullable=False),
    )
    op.add_column("algorithm_backtests", sa.Column("graph_url", sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("algorithm_backtests", "graph_url")
    op.drop_column("algorithm_backtests", "data")
    # ### end Alembic commands ###
