"""add cellosorua_index primary

Revision ID: 44465bed6b9e
Revises: 3721a66d898c
Create Date: 2022-06-12 21:05:52.075096

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '44465bed6b9e'
down_revision = '3721a66d898c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cell_lines', 'cellosaurus_index',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.drop_constraint('experiments_ibfk_1', 'experiments', type_='foreignkey')
    op.create_foreign_key(None, 'experiments', 'cell_lines', ['cellosaurus_id'], ['cellosaurus_id'])
    op.alter_column('mut_exp_metadata', 'cellosaurus_index',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.create_foreign_key(None, 'mut_exp_metadata', 'cell_lines', ['cellosaurus_index'], ['cellosaurus_index'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mut_exp_metadata', type_='foreignkey')
    op.alter_column('mut_exp_metadata', 'cellosaurus_index',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.drop_constraint(None, 'experiments', type_='foreignkey')
    op.create_foreign_key('experiments_ibfk_1', 'experiments', 'cell_lines', ['cellosaurus_id'], ['cellosaurus_id'], onupdate='CASCADE')
    op.alter_column('cell_lines', 'cellosaurus_index',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###