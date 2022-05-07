"""first migration

Revision ID: b15d160c4201
Revises: 
Create Date: 2022-05-07 15:34:45.975407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b15d160c4201'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('experiments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cellosaurus_index', sa.String(length=64), nullable=False),
    sa.Column('cellosaurus_id', sa.String(length=64), nullable=False),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=False),
    sa.Column('dataset', sa.String(length=32), nullable=False),
    sa.Column('info', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cell_line_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ccle_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp1_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp2_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc1_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc2_name', sa.String(length=64), nullable=True),
    sa.Column('site', sa.String(length=64), nullable=True),
    sa.Column('cellosaurus_id', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['cellosaurus_id'], ['experiments.cellosaurus_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dose_response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dosage', sa.Float(), nullable=True),
    sa.Column('response', sa.Float(), nullable=True),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drug_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('synonyms', sa.String(length=128), nullable=True),
    sa.Column('target', sa.String(length=64), nullable=True),
    sa.Column('pathway', sa.String(length=256), nullable=True),
    sa.Column('ccle_drug_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp1_drug_name', sa.String(length=64), nullable=True),
    sa.Column('ctrp2_drug_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc1_drug_name', sa.String(length=64), nullable=True),
    sa.Column('gdsc2_drug_name', sa.String(length=64), nullable=True),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['standard_drug_name'], ['experiments.standard_drug_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gene_expression',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('dataset', sa.String(length=32), nullable=True),
    sa.Column('cancer_type', sa.String(length=64), nullable=True),
    sa.Column('pvalue', sa.Float(), nullable=True),
    sa.Column('correlation', sa.Float(), nullable=True),
    sa.Column('pvalue_provided', sa.Float(), nullable=True),
    sa.Column('correlation_provided', sa.Float(), nullable=True),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['standard_drug_name'], ['experiments.standard_drug_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jags_sampling',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('n_dosage', sa.Integer(), nullable=True),
    sa.Column('min_dosage', sa.Float(), nullable=True),
    sa.Column('max_dosage', sa.Float(), nullable=True),
    sa.Column('beta0_mode', sa.Float(), nullable=True),
    sa.Column('beta0_HDI_low', sa.Float(), nullable=True),
    sa.Column('beta0_HDI_high', sa.Float(), nullable=True),
    sa.Column('beta1_mode', sa.Float(), nullable=True),
    sa.Column('beta0_jags_str', sa.Text(), nullable=True),
    sa.Column('beta1_jags_str', sa.Text(), nullable=True),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensitivity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ic50_HDI_low', sa.Float(), nullable=True),
    sa.Column('ic50_HDI_high', sa.Float(), nullable=True),
    sa.Column('ic50_mode', sa.Float(), nullable=True),
    sa.Column('ic90_calculate', sa.Float(), nullable=True),
    sa.Column('ec50_calculate', sa.Float(), nullable=True),
    sa.Column('einf_calculate', sa.Float(), nullable=True),
    sa.Column('auc_calculate', sa.Float(), nullable=True),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensitivity_provided',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ic50_provided', sa.Float(), nullable=True),
    sa.Column('auc_provided', sa.Float(), nullable=True),
    sa.Column('exp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exp_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wildtype_mutation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gene', sa.String(length=64), nullable=True),
    sa.Column('dataset', sa.String(length=32), nullable=True),
    sa.Column('cancer_type', sa.String(length=64), nullable=True),
    sa.Column('pvalue', sa.Float(), nullable=True),
    sa.Column('statistic', sa.Float(), nullable=True),
    sa.Column('pvalue_provided', sa.Float(), nullable=True),
    sa.Column('statistic_provided', sa.Float(), nullable=True),
    sa.Column('standard_drug_name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['standard_drug_name'], ['experiments.standard_drug_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wildtype_mutation')
    op.drop_table('sensitivity_provided')
    op.drop_table('sensitivity')
    op.drop_table('jags_sampling')
    op.drop_table('gene_expression')
    op.drop_table('drug_table')
    op.drop_table('dose_response')
    op.drop_table('cell_line_table')
    op.drop_table('experiments')
    # ### end Alembic commands ###
