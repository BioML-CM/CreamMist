"""add mut exp metadata

Revision ID: 3721a66d898c
Revises: 085280bb1559
Create Date: 2022-06-07 16:23:32.770750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3721a66d898c'
down_revision = '085280bb1559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mut_exp_metadata',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cellosaurus_index', sa.String(length=64), nullable=True),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('values', sa.Float(), nullable=True),
    sa.Column('score', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mut_exp_metadata')
    # ### end Alembic commands ###
