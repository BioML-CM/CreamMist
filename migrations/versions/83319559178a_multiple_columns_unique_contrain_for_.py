"""multiple columns unique contrain for experiments table

Revision ID: 83319559178a
Revises: 1d56a0bf646e
Create Date: 2022-05-07 19:08:49.348518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83319559178a'
down_revision = '1d56a0bf646e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'experiments', ['cellosaurus_id', 'standard_drug_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'experiments', type_='unique')
    # ### end Alembic commands ###