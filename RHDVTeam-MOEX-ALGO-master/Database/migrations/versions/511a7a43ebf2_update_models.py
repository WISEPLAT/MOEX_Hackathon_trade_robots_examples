"""update models

Revision ID: 511a7a43ebf2
Revises: 23af7ae7881f
Create Date: 2023-12-07 01:47:42.401707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '511a7a43ebf2'
down_revision: Union[str, None] = '23af7ae7881f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('tags', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('chats', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('webresources', sa.Column('rating', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('webresources', 'rating')
    op.drop_column('chats', 'rating')
    op.drop_column('chats', 'tags')
    # ### end Alembic commands ###