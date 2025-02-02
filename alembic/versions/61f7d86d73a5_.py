"""empty message

Revision ID: 61f7d86d73a5
Revises: 11092252dedf
Create Date: 2024-07-04 09:19:26.207148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61f7d86d73a5'
down_revision: Union[str, None] = '11092252dedf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chapters', 'created_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('comments', 'created_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('novels', 'last_chapter_created_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.add_column('reviews', sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('reviews', 'created_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reviews', 'created_date',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATE(),
               existing_nullable=True)
    op.drop_column('reviews', 'updated_date')
    op.alter_column('novels', 'last_chapter_created_date',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('comments', 'created_date',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('chapters', 'created_date',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATE(),
               existing_nullable=True)
    # ### end Alembic commands ###
