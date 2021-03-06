"""add cellosorua_index index

Revision ID: 52a62931632b
Revises: 44465bed6b9e
Create Date: 2022-06-12 21:21:02.770658

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52a62931632b'
down_revision = '44465bed6b9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cell_lines', 'cellosaurus_index',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.create_index(op.f('ix_cell_lines_cellosaurus_index'), 'cell_lines', ['cellosaurus_index'], unique=False)
    op.create_index(op.f('ix_mut_exp_metadata_cellosaurus_index'), 'mut_exp_metadata', ['cellosaurus_index'], unique=False)
    op.create_foreign_key(None, 'mut_exp_metadata', 'cell_lines', ['cellosaurus_index'], ['cellosaurus_index'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mut_exp_metadata', type_='foreignkey')
    op.drop_index(op.f('ix_mut_exp_metadata_cellosaurus_index'), table_name='mut_exp_metadata')
    op.drop_index(op.f('ix_cell_lines_cellosaurus_index'), table_name='cell_lines')
    op.alter_column('cell_lines', 'cellosaurus_index',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###
