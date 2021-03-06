"""add index to mutation and gene expression

Revision ID: f3e34d4f676b
Revises: deb5290f8f40
Create Date: 2022-05-13 00:34:18.533975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3e34d4f676b'
down_revision = 'deb5290f8f40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_cell_lines_site'), 'cell_lines', ['site'], unique=False)
    op.create_index(op.f('ix_gene_expressions_cancer_type'), 'gene_expressions', ['cancer_type'], unique=False)
    op.create_index(op.f('ix_gene_expressions_dataset'), 'gene_expressions', ['dataset'], unique=False)
    op.create_index(op.f('ix_mutations_cancer_type'), 'mutations', ['cancer_type'], unique=False)
    op.create_index(op.f('ix_mutations_dataset'), 'mutations', ['dataset'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mutations_dataset'), table_name='mutations')
    op.drop_index(op.f('ix_mutations_cancer_type'), table_name='mutations')
    op.drop_index(op.f('ix_gene_expressions_dataset'), table_name='gene_expressions')
    op.drop_index(op.f('ix_gene_expressions_cancer_type'), table_name='gene_expressions')
    op.drop_index(op.f('ix_cell_lines_site'), table_name='cell_lines')
    # ### end Alembic commands ###
