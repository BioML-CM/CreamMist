"""add mutation-geneexpression

Revision ID: f3bc9b18a022
Revises: 79633ea5803d
Create Date: 2022-05-27 10:56:28.091594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3bc9b18a022'
down_revision = '79633ea5803d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gene_expressions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=True),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('dataset', sa.String(length=32), nullable=True),
    sa.Column('cancer_type', sa.String(length=64), nullable=True),
    sa.Column('pvalue', sa.Float(), nullable=True),
    sa.Column('correlation', sa.Float(), nullable=True),
    sa.Column('provided_pvalue', sa.Float(), nullable=True),
    sa.Column('provided_correlation', sa.Float(), nullable=True),
    sa.Column('n_cell_line', sa.Integer(), nullable=True),
    sa.Column('provided_n_cell_line', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gene'], ['genes.gene_name'], ),
    sa.ForeignKeyConstraint(['standard_drug_name'], ['drugs.standard_drug_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gene_expressions_cancer_type'), 'gene_expressions', ['cancer_type'], unique=False)
    op.create_index(op.f('ix_gene_expressions_dataset'), 'gene_expressions', ['dataset'], unique=False)
    op.create_table('mutations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=True),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('dataset', sa.String(length=32), nullable=True),
    sa.Column('cancer_type', sa.String(length=64), nullable=True),
    sa.Column('pvalue', sa.Float(), nullable=True),
    sa.Column('statistic', sa.Float(), nullable=True),
    sa.Column('provided_pvalue', sa.Float(), nullable=True),
    sa.Column('provided_statistic', sa.Float(), nullable=True),
    sa.Column('n_mut', sa.Integer(), nullable=True),
    sa.Column('n_wt', sa.Integer(), nullable=True),
    sa.Column('provided_n_mut', sa.Integer(), nullable=True),
    sa.Column('provided_n_wt', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gene'], ['genes.gene_name'], ),
    sa.ForeignKeyConstraint(['standard_drug_name'], ['drugs.standard_drug_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mutations_cancer_type'), 'mutations', ['cancer_type'], unique=False)
    op.create_index(op.f('ix_mutations_dataset'), 'mutations', ['dataset'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mutations_dataset'), table_name='mutations')
    op.drop_index(op.f('ix_mutations_cancer_type'), table_name='mutations')
    op.drop_table('mutations')
    op.drop_index(op.f('ix_gene_expressions_dataset'), table_name='gene_expressions')
    op.drop_index(op.f('ix_gene_expressions_cancer_type'), table_name='gene_expressions')
    op.drop_table('gene_expressions')
    # ### end Alembic commands ###