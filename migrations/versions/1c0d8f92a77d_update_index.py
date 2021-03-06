"""update index

Revision ID: 1c0d8f92a77d
Revises: f3e34d4f676b
Create Date: 2022-05-13 17:44:10.692899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c0d8f92a77d'
down_revision = 'f3e34d4f676b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_gene_expressions_dataset'), 'gene_expressions', ['dataset'], unique=False)
    op.create_index(op.f('ix_mutations_cancer_type'), 'mutations', ['cancer_type'], unique=False)
    op.create_index(op.f('ix_mutations_dataset'), 'mutations', ['dataset'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mutations_dataset'), table_name='mutations')
    op.drop_index(op.f('ix_mutations_cancer_type'), table_name='mutations')
    op.drop_index(op.f('ix_gene_expressions_dataset'), table_name='gene_expressions')
    # ### end Alembic commands ###
