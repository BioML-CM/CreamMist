"""multiple columns unique contrain for experiments table

Revision ID: a29432bc3991
Revises: 83319559178a
Create Date: 2022-05-07 19:11:55.993278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a29432bc3991'
down_revision = '83319559178a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'experiments', ['cellosaurus_id', 'standard_drug_name', 'dataset'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'experiments', type_='unique')
    # ### end Alembic commands ###