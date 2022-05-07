"""test migration

Revision ID: 187e097d71dd
Revises: e9f277f44104
Create Date: 2022-05-07 15:44:49.967407

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '187e097d71dd'
down_revision = 'e9f277f44104'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cell_line_table', 'site',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.String(length=128),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cell_line_table', 'site',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=True)
    # ### end Alembic commands ###
