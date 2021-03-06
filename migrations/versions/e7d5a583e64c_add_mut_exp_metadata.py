"""add mut exp metadata

Revision ID: e7d5a583e64c
Revises: f3bc9b18a022
Create Date: 2022-06-07 15:27:28.143138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d5a583e64c'
down_revision = 'f3bc9b18a022'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mut_exp_metadata',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cellosaurus_index', sa.String(length=64), nullable=True),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('values', sa.Float(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['cellosaurus_index'], ['cell_lines.cellosaurus_index'], ),
    sa.ForeignKeyConstraint(['gene'], ['genes.gene_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mut_exp_metadata')
    # ### end Alembic commands ###
