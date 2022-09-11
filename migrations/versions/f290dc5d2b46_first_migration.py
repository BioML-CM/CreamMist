"""first migration

Revision ID: f290dc5d2b46
Revises: 
Create Date: 2022-09-12 01:03:12.538289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f290dc5d2b46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cell_lines',
    sa.Column('cellosaurus_id', sa.String(length=64), nullable=False),
    sa.Column('cellosaurus_index', sa.String(length=64), nullable=True),
    sa.Column('ccle_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp1_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp2_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc1_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc2_name', sa.String(length=64), nullable=True),
    sa.Column('site', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('cellosaurus_id')
    )
    op.create_index(op.f('ix_cell_lines_cellosaurus_index'), 'cell_lines', ['cellosaurus_index'], unique=False)
    op.create_index(op.f('ix_cell_lines_site'), 'cell_lines', ['site'], unique=False)
    op.create_table('drugs',
    sa.Column('standard_drug_name', sa.String(length=64), nullable=False),
    sa.Column('synonyms', sa.String(length=128), nullable=True),
    sa.Column('target', sa.String(length=64), nullable=True),
    sa.Column('pathway', sa.String(length=256), nullable=True),
    sa.Column('ccle_drug_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp1_drug_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp2_drug_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc1_drug_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc2_drug_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('standard_drug_name')
    )
    op.create_table('genes',
    sa.Column('gene_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('gene_name')
    )
    op.create_table('experiments',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('cellosaurus_id', sa.String(length=64), nullable=False),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=False),
    sa.Column('dataset', sa.String(length=32), nullable=False),
    sa.Column('info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['cellosaurus_id'], ['cell_lines.cellosaurus_id'], ),
    sa.ForeignKeyConstraint(['standard_drug_name'], ['drugs.standard_drug_name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cellosaurus_id', 'standard_drug_name', 'dataset')
    )
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
    op.create_table('omics_profiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cellosaurus_id', sa.String(length=64), nullable=False),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('values', sa.Float(), nullable=True),
    sa.Column('score', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['cellosaurus_id'], ['cell_lines.cellosaurus_id'], ),
    sa.ForeignKeyConstraint(['gene'], ['genes.gene_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dose_responses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dosage', sa.Float(), nullable=True),
    sa.Column('response', sa.Float(), nullable=True),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jags_samplings',
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.Column('n_dosage', sa.Integer(), nullable=True),
    sa.Column('min_dosage', sa.Float(), nullable=True),
    sa.Column('max_dosage', sa.Float(), nullable=True),
    sa.Column('beta0_mode', sa.Float(), nullable=True),
    sa.Column('beta0_HDI_low', sa.Float(), nullable=True),
    sa.Column('beta0_HDI_high', sa.Float(), nullable=True),
    sa.Column('beta1_mode', sa.Float(), nullable=True),
    sa.Column('beta1_HDI_low', sa.Float(), nullable=True),
    sa.Column('beta1_HDI_high', sa.Float(), nullable=True),
    sa.Column('ic90_mode', sa.Float(), nullable=True),
    sa.Column('ic90_HDI_low', sa.Float(), nullable=True),
    sa.Column('ic90_HDI_high', sa.Float(), nullable=True),
    sa.Column('ec50_mode', sa.Float(), nullable=True),
    sa.Column('ec50_HDI_low', sa.Float(), nullable=True),
    sa.Column('ec50_HDI_high', sa.Float(), nullable=True),
    sa.Column('einf_mode', sa.Float(), nullable=True),
    sa.Column('einf_HDI_low', sa.Float(), nullable=True),
    sa.Column('einf_HDI_high', sa.Float(), nullable=True),
    sa.Column('auc_mode', sa.Float(), nullable=True),
    sa.Column('auc_HDI_low', sa.Float(), nullable=True),
    sa.Column('auc_HDI_high', sa.Float(), nullable=True),
    sa.Column('fitted_mae', sa.Float(), nullable=True),
    sa.Column('beta0_jags_str', sa.Text(), nullable=True),
    sa.Column('beta1_jags_str', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('exp_id')
    )
    op.create_table('provided_sensitivity_scores',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.Column('ic50_provided', sa.Float(), nullable=True),
    sa.Column('auc_provided', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensitivity_scores',
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.Column('ic50_HDI_low', sa.Float(), nullable=True),
    sa.Column('ic50_HDI_high', sa.Float(), nullable=True),
    sa.Column('ic50_mode', sa.Float(), nullable=True),
    sa.Column('ic90_calculate', sa.Float(), nullable=True),
    sa.Column('ec50_calculate', sa.Float(), nullable=True),
    sa.Column('einf_calculate', sa.Float(), nullable=True),
    sa.Column('auc_calculate', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('exp_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensitivity_scores')
    op.drop_table('provided_sensitivity_scores')
    op.drop_table('jags_samplings')
    op.drop_table('dose_responses')
    op.drop_table('omics_profiles')
    op.drop_table('mutations')
    op.drop_table('gene_expressions')
    op.drop_table('experiments')
    op.drop_table('genes')
    op.drop_table('drugs')
    op.drop_index(op.f('ix_cell_lines_site'), table_name='cell_lines')
    op.drop_index(op.f('ix_cell_lines_cellosaurus_index'), table_name='cell_lines')
    op.drop_table('cell_lines')
    # ### end Alembic commands ###
